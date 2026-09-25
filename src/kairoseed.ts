/**
 * KAIROSEED Adapter — reference implementation.
 *
 * Verification-first execution governance for AI agent tool calls.
 * Capability != Permission.
 *
 * Boundary: this is a reference adapter, not proof of a production deployment.
 */

export type Decision = "ALLOW" | "DENY" | "PAUSE";
export type ClaimStatus = "ACTIVE" | "REVOKED" | "USED" | "EXPIRED";

export interface Claim {
  id: string;
  subject: string;
  action: string;
  scope: string;
  status: ClaimStatus;
  expiresAt: number;
  policyVersion: string;
  createdAt: number;
  paramsHash?: string;
  singleUse?: boolean;
  revokedAt?: number;
}

export interface ExecRequest<TParams = unknown> {
  subject: string;
  action: string;
  scope: string;
  claim: string;
  params?: TParams;
  tool: () => Promise<unknown> | unknown;
}

export interface EvidenceEvent {
  id: string;
  timestamp: number;
  event: "BLOCKED" | "EXECUTED" | "VERIFICATION";
  subject: string;
  action: string;
  scope: string;
  claimId: string;
  decision: Decision;
  reason?: string;
  resultHash?: string;
}

export interface ClaimStore {
  get(id: string): Promise<Claim | undefined> | Claim | undefined;
  save?(claim: Claim): Promise<void> | void;
}

export interface EvidenceSink {
  append(event: EvidenceEvent): Promise<void> | void;
}

export interface PolicyInput {
  claim: Claim;
  request: ExecRequest;
}

export interface Policy {
  version: string;
  evaluate(input: PolicyInput): Promise<Decision> | Decision;
}

export interface KairoseedResult<T = unknown> {
  decision: Decision;
  executed: boolean;
  value?: T;
  evidence: EvidenceEvent;
  reason?: string;
}

export interface KairoseedOptions {
  claims: ClaimStore;
  evidence: EvidenceSink;
  policy?: Policy;
  now?: () => number;
}

export class InMemoryClaimStore implements ClaimStore {
  private readonly claims = new Map<string, Claim>();

  constructor(claims: Claim[] = []) {
    for (const claim of claims) this.claims.set(claim.id, { ...claim });
  }

  get(id: string): Claim | undefined {
    const claim = this.claims.get(id);
    return claim ? { ...claim } : undefined;
  }

  save(claim: Claim): void {
    this.claims.set(claim.id, { ...claim });
  }
}

export class InMemoryEvidenceSink implements EvidenceSink {
  readonly events: EvidenceEvent[] = [];

  append(event: EvidenceEvent): void {
    this.events.push({ ...event });
  }
}

export class DefaultPolicy implements Policy {
  constructor(public readonly version = "kairoseed/v1") {}

  evaluate({ claim, request }: PolicyInput): Decision {
    if (claim.policyVersion !== this.version) return "DENY";
    if (claim.subject !== request.subject) return "DENY";
    if (claim.action !== request.action) return "DENY";
    if (claim.scope !== request.scope) return "DENY";
    return "ALLOW";
  }
}

function createId(): string {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function stableSerialize(value: unknown): string {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value) ?? "undefined";
  }

  if (Array.isArray(value)) {
    return `[${value.map(stableSerialize).join(",")}]`;
  }

  const object = value as Record<string, unknown>;
  return `{${Object.keys(object).sort().map(
    key => `${JSON.stringify(key)}:${stableSerialize(object[key])}`
  ).join(",")}}`;
}

async function sha256(value: string): Promise<string> {
  const bytes = new TextEncoder().encode(value);
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);

  return Array.from(new Uint8Array(digest))
    .map(byte => byte.toString(16).padStart(2, "0"))
    .join("");
}

export class Kairoseed {
  private readonly policy: Policy;
  private readonly now: () => number;

  constructor(private readonly options: KairoseedOptions) {
    this.policy = options.policy ?? new DefaultPolicy();
    this.now = options.now ?? (() => Date.now());
  }

  async exec<T>(request: ExecRequest): Promise<KairoseedResult<T>> {
    const attemptTimestamp = this.now();

    const block = async (reason: string): Promise<KairoseedResult<T>> => {
      const evidence: EvidenceEvent = {
        id: createId(),
        timestamp: attemptTimestamp,
        event: "BLOCKED",
        subject: request.subject,
        action: request.action,
        scope: request.scope,
        claimId: request.claim,
        decision: "DENY",
        reason
      };

      await this.options.evidence.append(evidence);

      return { decision: "DENY", executed: false, evidence, reason };
    };

    const claim = await this.options.claims.get(request.claim);
    if (!claim) return block("claim_not_found");

    if (claim.status !== "ACTIVE") {
      return block(`claim_${claim.status.toLowerCase()}`);
    }

    if (claim.expiresAt <= attemptTimestamp) {
      return block("claim_expired");
    }

    if (claim.paramsHash !== undefined) {
      const actualHash = await sha256(stableSerialize(request.params));
      if (actualHash !== claim.paramsHash) {
        return block("params_hash_mismatch");
      }
    }

    const policyDecision = await this.policy.evaluate({ claim, request });

    if (policyDecision !== "ALLOW") {
      return block(`policy_${policyDecision.toLowerCase()}`);
    }

    let value: T;

    try {
      value = (await request.tool()) as T;
    } catch (error) {
      const reason = `tool_error:${error instanceof Error ? error.message : String(error)}`;

      const evidence: EvidenceEvent = {
        id: createId(),
        timestamp: this.now(),
        event: "VERIFICATION",
        subject: request.subject,
        action: request.action,
        scope: request.scope,
        claimId: request.claim,
        decision: "ALLOW",
        reason
      };

      await this.options.evidence.append(evidence);

      return { decision: "ALLOW", executed: false, evidence, reason };
    }

    if (claim.singleUse) {
      claim.status = "USED";
      await this.options.claims.save?.(claim);
    }

    const resultHash = await sha256(stableSerialize(value));

    const evidence: EvidenceEvent = {
      id: createId(),
      timestamp: this.now(),
      event: "EXECUTED",
      subject: request.subject,
      action: request.action,
      scope: request.scope,
      claimId: request.claim,
      decision: "ALLOW",
      resultHash
    };

    await this.options.evidence.append(evidence);

    return { decision: "ALLOW", executed: true, value, evidence };
  }
}
