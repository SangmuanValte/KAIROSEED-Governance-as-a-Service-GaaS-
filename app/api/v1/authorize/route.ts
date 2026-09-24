import { createHash, randomUUID } from "crypto";
import { NextResponse } from "next/server";
import { evaluateAuthorization, type AuthorizationInput } from "../../../../lib/astra-governor";

function sha256(value: string) {
  return createHash("sha256").update(value).digest("hex");
}

export async function POST(request: Request) {
  const body = (await request.json()) as AuthorizationInput;
  const event = evaluateAuthorization(body, "auth_" + randomUUID());

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

  if (supabaseUrl && supabaseKey) {
    try {
      await fetch(supabaseUrl + "/rest/v1/authorization_events", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          apikey: supabaseKey,
          authorization: `Bearer ${supabaseKey}`,
          prefer: "return=minimal",
        },
        body: JSON.stringify({
          organization_id: process.env.ASTRA_ORGANIZATION_ID,
          agent_id: process.env.ASTRA_AGENT_UUID,
          tool: event.tool,
          action: event.action,
          resource: event.resource,
          environment: event.environment,
          decision: event.decision,
          reason: event.reason,
          request_id: event.authorization_id,
          metadata: {
            policy_agent_id: event.agent_id,
            event_hash: sha256(JSON.stringify(event)),
          },
        }),
      });
    } catch {
      return NextResponse.json(
        { ...event, reason: event.reason + "; evidence persistence unavailable", invariant: "NO_AUTHORIZATION_NO_EXECUTION" },
        { status: 503 },
      );
    }
  }

  return NextResponse.json({
    ...event,
    invariant: event.decision === "DENY" ? "NO_AUTHORIZATION_NO_EXECUTION" : "AUTHORIZATION_REQUIRED_BEFORE_EXECUTION",
  });
}
