import { createHash, randomUUID } from "crypto";
import { NextResponse } from "next/server";
import { evaluateAuthorization, type AuthorizationInput } from "../../../../../lib/astra-governor";

type GrokRequest = AuthorizationInput & {
  target?: string;
  prompt?: string;
  reply_to_id?: string;
};

function sha256(value: string) {
  return createHash("sha256").update(value).digest("hex");
}

export async function POST(request: Request) {
  const body = (await request.json()) as GrokRequest;
  const authorization_id = "auth_" + randomUUID();
  const decision = evaluateAuthorization(body, authorization_id);

  const evidence = {
    ...decision,
    metadata: {
      target: body.target ?? "",
      event_hash: sha256(JSON.stringify(decision)),
    },
  };

  if (decision.decision !== "ALLOW") {
    return NextResponse.json(
      { ...evidence, executed: false, invariant: "NO_AUTHORIZATION_NO_EXECUTION" },
      { status: decision.decision === "APPROVAL_REQUIRED" ? 202 : 403 },
    );
  }

  const gatewayUrl = (process.env.GROK_BOT_GATEWAY_URL ?? "").replace(/\/$/, "");
  const gatewayToken = process.env.GROK_BOT_GATEWAY_TOKEN;

  // ASTRA never falls through to an ungoverned send. A missing gateway is a denial.
  if (!gatewayUrl || !gatewayToken) {
    return NextResponse.json(
      { ...evidence, executed: false, decision: "DENY", reason: "Grok gateway is not configured; execution blocked" },
      { status: 503 },
    );
  }

  if (!body.target || !body.prompt) {
    return NextResponse.json(
      { ...evidence, executed: false, decision: "DENY", reason: "target and prompt are required" },
      { status: 400 },
    );
  }

  try {
    const response = await fetch(gatewayUrl + "/api/sendPrompt", {
      method: "POST",
      redirect: "error",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${gatewayToken}`,
      },
      body: JSON.stringify({
        agentId: body.target,
        prompt: body.prompt,
        clientNonce: authorization_id,
        ...(body.reply_to_id ? { replyToId: body.reply_to_id } : {}),
      }),
      signal: AbortSignal.timeout(30000),
    });

    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
      return NextResponse.json(
        { ...evidence, executed: false, decision: "DENY", reason: "Grok gateway rejected request", gateway_status: response.status },
        { status: 502 },
      );
    }

    const messageId = typeof result?.messageId === "string" ? result.messageId : undefined;
    return NextResponse.json({
      ...evidence,
      executed: Boolean(messageId),
      delivery: messageId ? "accepted" : "unknown",
      message_id: messageId,
      result,
      invariant: messageId ? "AUTHORIZED_BEFORE_EXECUTION" : "DELIVERY_UNKNOWN_CHECK_THREAD_BEFORE_RETRY",
    });
  } catch {
    return NextResponse.json(
      { ...evidence, executed: false, delivery: "unknown", reason: "Grok delivery outcome is unknown; inspect the thread before retrying" },
      { status: 502 },
    );
  }
}
