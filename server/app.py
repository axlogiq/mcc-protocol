from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    intent: str
    args: dict

@app.post("/evaluate")
def evaluate(req: Request):
    
    # simple rule example
    if req.intent == "send_email":
        to = req.args.get("to", "")
        
        if not to.endswith("@trusted.com"):
            return {
                "decision": "deny",
                "reason": {
                    "code": "UNTRUSTED_RECIPIENT",
                    "message": "recipient not allowed"
                }
            }
    
    return {
        "decision": "allow"
    }
