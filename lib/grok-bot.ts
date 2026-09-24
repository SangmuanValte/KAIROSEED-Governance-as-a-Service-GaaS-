import { randomUUID } from "crypto";

export type GrokBotSendInput = {
  target: string;
  prompt: string;
  replyToId?: string;
};

export type GrokBotSendResult = {
  delivery: "accepted" | "unknown";
  messageId?: string;
  result: unknown;
};

function gatewayConfig() {
  const url = (process.env.GROK_BOT_GATEWAY_URL ?? "").replace(/\/$/, "");
  const token = process.env.GROK_BOT_GATEWAY_TOKEN ?? "";
  if (!url || !token) throw new Error("Grok Bot gateway is not configured");
  return { url, token };
}

/**
 * Low-level gbot transport. It deliberately contains no policy logic:
 * ASTRA authorization must happen before this function is called.
 */
export async function gbotSend(input: GrokBotSendInput, clientNonce = randomUUID()): Promise<GrokBotSendResult> {
  if (!input.target.trim()) throw new Error("Grok Bot target is required");
  if (!input.prompt.trim()) throw new Error("Grok Bot prompt is required");

  const { url, token } = gatewayConfig();
  const response = await fetch(url + "/api/sendPrompt", {
    method: "POST",
    redirect: "error",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      agentId: input.target,
      prompt: input.prompt,
      clientNonce,
      ...(input.replyToId ? { replyToId: input.replyToId } : {}),
    }),
    signal: AbortSignal.timeout(30000),
  });

  const result = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(`grok-bot gateway rejected request: ${response.status}`);

  const messageId = typeof result?.messageId === "string" ? result.messageId : undefined;
  return {
    delivery: messageId ? "accepted" : "unknown",
    ...(messageId ? { messageId } : {}),
    result,
  };
}
