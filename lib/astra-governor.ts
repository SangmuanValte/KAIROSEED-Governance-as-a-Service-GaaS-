export type Decision = "ALLOW" | "DENY" | "APPROVAL_REQUIRED";

export type AuthorizationInput = {
  agent_id?: string;
  tool?: string;
  action?: string;
  resource?: string;
  context?: { environment?: string };
};

export type AuthorizationResult = {
  authorization_id: string;
  agent_id: string;
  tool: string;
  action: string;
  resource: string;
  environment: string;
  decision: Decision;
  reason: string;
  evaluated_at: string;
};

const policies: Record<string, { allowedTools: string[]; productionApproval: boolean }> = {
  "agent-soc": { allowedTools: ["create_ticket", "read_database"], productionApproval: true },
  "agent-research": { allowedTools: ["external_api", "read_database"], productionApproval: false },
  "agent-deploy": { allowedTools: ["deploy", "read_database"], productionApproval: true },
  "agent-grok": { allowedTools: ["grok_message", "grok_thread"], productionApproval: true },
};

export function evaluateAuthorization(body: AuthorizationInput, authorization_id: string, evaluated_at = new Date().toISOString()): AuthorizationResult {
  const agent_id = body.agent_id ?? "";
  const tool = body.tool ?? "";
  const resource = body.resource ?? "";
  const action = body.action ?? "execute";
  const environment = body.context?.environment ?? "simulation";
  const policy = policies[agent_id];

  let decision: Decision = "DENY";
  let reason = "unknown agent";

  if (policy) {
    if (!policy.allowedTools.includes(tool)) reason = "tool is outside agent policy scope";
    else if (environment === "production" && policy.productionApproval) {
      decision = "APPROVAL_REQUIRED";
      reason = "production write requires human approval";
    } else if (environment === "production" && tool === "read_database") {
      decision = "ALLOW";
      reason = "policy:read-production-v1";
    } else if (environment === "simulation") {
      decision = "ALLOW";
      reason = "policy:simulation-v1";
    } else reason = "environment is outside declared policy";
  }

  return { authorization_id, agent_id, tool, action, resource, environment, decision, reason, evaluated_at };
}
