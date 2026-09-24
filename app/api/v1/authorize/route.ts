import { createHash, randomUUID } from "crypto";
import { NextResponse } from "next/server";

type RequestBody = { agent_id?: string; tool?: string; action?: string; resource?: string; context?: { environment?: string } };

const policies: Record<string,{allowedTools:string[];productionApproval:boolean}> = {
  "agent-soc": { allowedTools:["create_ticket","read_database"], productionApproval:true },
  "agent-research": { allowedTools:["external_api","read_database"], productionApproval:false },
  "agent-deploy": { allowedTools:["deploy","read_database"], productionApproval:true },
};

function sha256(value:string){ return createHash("sha256").update(value).digest("hex"); }

export async function POST(request:Request){
  const body=(await request.json()) as RequestBody;
  const agent=body.agent_id??"", tool=body.tool??"", resource=body.resource??"";
  const environment=body.context?.environment??"simulation";
  const policy=policies[agent];
  let decision:"ALLOW"|"DENY"|"APPROVAL_REQUIRED"="DENY";
  let reason="unknown agent";

  if(policy){
    if(!policy.allowedTools.includes(tool)) reason="tool is outside agent policy scope";
    else if(environment==="production" && policy.productionApproval){decision="APPROVAL_REQUIRED";reason="production write requires human approval";}
    else if(environment==="production" && tool==="read_database"){decision="ALLOW";reason="policy:read-production-v1";}
    else if(environment==="simulation"){decision="ALLOW";reason="policy:simulation-v1";}
    else reason="environment is outside declared policy";
  }

  const authorization_id="auth_"+randomUUID();
  const event={
    authorization_id, agent_id:agent, tool, action:body.action??"execute", resource,
    environment, decision, reason, evaluated_at:new Date().toISOString()
  };

  // Prototype boundary: persist only when the application is explicitly configured
  // with a server-side Supabase URL/key. Never expose a service-role key to clients.
  const supabaseUrl=process.env.SUPABASE_URL;
  const supabaseKey=process.env.SUPABASE_SERVICE_ROLE_KEY;
  if(supabaseUrl && supabaseKey){
    try{
      await fetch(supabaseUrl+"/rest/v1/authorization_events",{
        method:"POST",
        headers:{"content-type":"application/json","apikey":supabaseKey,"authorization":`Bearer ${supabaseKey}`,"prefer":"return=minimal"},
        body:JSON.stringify({
          organization_id:process.env.ASTRA_ORGANIZATION_ID,
          agent_id:process.env.ASTRA_AGENT_UUID,
          tool, action:event.action, resource, environment, decision, reason,
          request_id:authorization_id,
          metadata:{policy_agent_id:agent, event_hash:sha256(JSON.stringify(event))}
        })
      });
    }catch{
      // Authorization remains fail-closed; persistence failure is surfaced as evidence state.
      reason=reason+"; evidence persistence unavailable";
    }
  }

  return NextResponse.json({...event,invariant:decision==="DENY"?"NO_AUTHORIZATION_NO_EXECUTION":"AUTHORIZATION_REQUIRED_BEFORE_EXECUTION"});
}
