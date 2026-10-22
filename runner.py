import json 
from pydantic import ValidationError
from tools import REGISTRY
from validation import ARG_M0DELS


def execute_tools(name:str,raw_json:str)->dict:
    if name not in REGISTRY:
        return {"error":f"Unknown tool {name} : avaliable tools: {sorted(REGISTRY)}"}
    try:
        args = json.loads(raw_json)
    except json.JSONDecodeError as e:
        return {"error": f"Inavlid Json object ,{e.msg} Please send a valid json object "}
    if not isinstance(args,dict):
        return {"error":f"arguments must be a json object "} 
    try:
        parsed = ARG_M0DELS[name](**args)
    except ValidationError as e:
        return {"error": f"argument Validation failed :{e} "} 
    # try:
        return REGISTRY[name](**parsed.model_dump())  
    # except Exception as e:
    #     return {"error": f"The tool failed ({type(e).__name__}). Do not retry with the same arguments."}
