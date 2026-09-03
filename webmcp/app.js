const state = {
  authorized: false,
  executed: false,
  eventId: null
};

const $ = (id) => document.getElementById(id);

function detectWebMCP() {
  const supported = !!(navigator.modelContext && typeof navigator.modelContext.registerTool === 'function');
  $('mcp').textContent = supported ? 'AVAILABLE' : 'NOT DETECTED';
  return supported;
}

function evidence(event, result) {
  const record = {
    event,
    result,
    scope: 'webmcp-challenge',
    authorization: state.authorized ? 'GRANTED' : 'NOT GRANTED',
    timestamp: new Date().toISOString()
  };
  $('evidence').textContent = JSON.stringify(record, null, 2);
}

async function publishArtifact() {
  if (!state.authorized) {
    throw new Error('AUTHORIZATION_REQUIRED');
  }
  state.executed = true;
  state.eventId = crypto.randomUUID();
  return { ok: true, event_id: state.eventId, artifact: 'prototype-result' };
}

$('authorize').addEventListener('click', () => {
  state.authorized = true;
  $('auth').textContent = 'GRANTED';
  $('execution').textContent = 'ADMITTED';
  $('execute').disabled = false;
  $('authorize').disabled = true;
  $('status').textContent = 'Authorization admitted. Execution is now within the declared scope.';
  evidence('authorization', 'admitted');
});

$('execute').addEventListener('click', async () => {
  try {
    const result = await publishArtifact();
    $('execution').textContent = 'COMPLETED';
    $('status').textContent = 'The governed action executed successfully.';
    evidence('execution', result);
    $('execute').disabled = true;
  } catch (error) {
    $('execution').textContent = 'BLOCKED';
    $('status').textContent = `Execution blocked: ${error.message}`;
    evidence('execution', 'blocked');
  }
});

// WebMCP registration is progressive: the page remains usable when the
// experimental API is unavailable, while exposing the same governed action
// when navigator.modelContext is present.
if (navigator.modelContext && typeof navigator.modelContext.registerTool === 'function') {
  navigator.modelContext.registerTool({
    name: 'publish_artifact',
    description: 'Request a governed prototype publication. Authorization is required before execution.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
    execute: async () => publishArtifact()
  });
}

detectWebMCP();
evidence('initialization', 'ready');
