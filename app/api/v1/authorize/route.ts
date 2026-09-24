import { randomUUID } from "crypto";
import { NextResponse } from "next/server";

type RequestBody = {
  agent_id?: string;
  tool?: string;
  action?: string;
  resource?: string;
  context?: { environment?: string };
};

const agentPolicies: Record<string, { allowedTools: string[]; productionApproval: boolean }> = {
  "agent-soc": { allowedTools: ["create_ticket", "read_database"], productionApproval: true },
  "agent-research": { allowedTools: ["external_api", "read_database"], productionApproval: false },
  "agent-deploy": { allowedTools: ["deploy", "read_database"], productionApproval: true },
};

export async function POST(request: Request) {
  const body = (await request.json()) as RequestBody;
  const agent = body.agent_id ?? "";
  const tool = body.tool ?? "";
  const resource = body.resource ?? "";
  const environment = body.context?.environment ?? "simulation";
  const policy = agentPolicies[agent];

  let decision: "ALLOW" | "DENY" | "APPROVAL_REQUIRED" = "DENY";
  let reason = "unknown agent";

  if (policy) {
    if (!policy.allowedTools.includes(tool)) {
      reason = "tool is outside agent policy scope";
    } else if (environment === "production" && policy.productionApproval) {
      decision = "APPROVAL_REQUIRED";
      reason = "production write requires human approval";
    } else if (environment === "production" && tool === "read_database") {
      decision = "ALLOW";
      reason = "policy:read-production-v1";
    } else if (environment === "simulation") {
      decision = "ALLOW";
      reason = "policy:simulation-v1";
    } else {
      reason = "environment is outside declared policy";
    }
  }

  return NextResponse.json({
    authorization_id: "auth_" + randomUUID(),
    decision,
    reason,
    agent_id: agent,
    tool,
    action: body.action ?? "execute",
    resource,
    evaluated_at: new Date().toISOString(),
    invariant: decision === "DENY" ? "NO_AUTHORIZATION_NO_EXECUTION" : "AUTHORIZATION_REQUIRED_BEFORE_EXECUTION",
  });
}
