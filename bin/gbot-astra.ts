#!/usr/bin/env node
import { randomUUID } from "crypto";
import { gbotSend } from "../lib/grok-bot";

const [target, ...promptParts] = process.argv.slice(2);
const prompt = promptParts.join(" ").trim();

if (!target || !prompt) {
  console.error("Usage: gbot-astra <target-agent-id> <prompt>");
  process.exit(2);
}

const authorizationId = "auth_" + randomUUID();
const baseUrl = (process.env.ASTRA_BASE_URL ?? "http://localhost:3000").replace(/\/$/, "");

const response = await fetch(baseUrl + "/api/v1/grok/send", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({
    agent_id: "agent-grok",
    tool: "grok_message",
    action: "send",
    resource: target,
    target,
    prompt,
    context: { environment: process.env.ASTRA_ENVIRONMENT ?? "simulation" },
    request_id: authorizationId,
  }),
});

const data = await response.json();
console.log(JSON.stringify(data, null, 2));
if (!response.ok || data.executed !== true) process.exit(1);
