import openai
import os,json
from dotenv import load_dotenv
from runner import execute_tools
from tools import TOOLS_PRECISE
from pathlib import Path

load_dotenv(override=True)
MAX_STEPS = 4
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
LLM_model = "gpt-4.1-mini"
question="My License is expiring in next thirty days , can I renew online?"
bad_args = '{"days_to_expiry":"next thirty days"}'
messages= [
    {"role":"user","content":question},
    {"role":"assistant","content":None,"tool_calls":[{
        "id":"call_injected_1","type":"function",
        "function":{"name":"check_online_renewal_eligibility","arguments":bad_args}
    }]}
]

result = execute_tools("check_online_renewal_eligibility", bad_args)
print("ERROR FED BACK:", result)
messages.append({"role":"tool","tool_call_id":"call_injected_1","content":json.dumps(result)})

for step in range(1,MAX_STEPS+1):
    msg =client.chat.completions.create(model=LLM_model, messages=messages, tools=TOOLS_PRECISE).choices[0].message
    messages.append(msg)
    if not msg.tool_calls:
        print(f"Final step : {step}",{msg.content})
        break
    
    for call in msg.tool_calls:
        output = execute_tools(call.function.name,call.function.arguments)
        print(f"tool called: {call.function.name} and arguments: {call.function.arguments}")
        messages.append({"role":"tool" , "tool_call_id":call.id,"content":json.dumps(output)})
else:
    print("The stop limit reached")
Path("output").mkdir(exist_ok=True)
Path("output/w1d4_recovery.json").write_text(
    json.dumps([m if isinstance(m, dict) else m.model_dump() for m in messages], indent=2), encoding="utf-8")        