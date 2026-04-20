from datetime import datetime
from threading import Lock
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="MCC Protocol Reference Implementation", version="0.2")

# Error codes:
# - MALFORMED_JSON
# - MISSING_FIELD
# - INVALID_ARGUMENT
# - UNKNOWN_INTENT
# - INVALID_SEQUENCE
# - UNTRUSTED_RECIPIENT
# - POLICY_CHECK_FAILED

ALLOWED_INTENTS = {"send_email", "validate_payment", "approve_payment"}
TRUSTED_RECIPIENTS = {"ops@trusted.com", "finance@trusted.com", "admin@trusted.com"}

sessions: Dict[str, Dict[str, Any]] = {}
sessions_lock = Lock()


class EvaluateRequest(BaseModel):
    session_id: str = Field(..., min_length=1)
    intent: str = Field(..., min_length=1)
    args: Dict[str, Any]


class Reason(BaseModel):
    code: str
    message: str


class EvaluateResponse(BaseModel):
    decision: str
    reason: Optional[Reason] = None


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    if any(err.get("type") == "json_invalid" for err in errors):
        return JSONResponse(
            status_code=400,
            content=EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="MALFORMED_JSON",
                    message="request body is not valid JSON",
                ),
            ).model_dump(exclude_none=True),
        )

    return JSONResponse(
        status_code=400,
        content=EvaluateResponse(
            decision="deny",
            reason=Reason(
                code="INVALID_ARGUMENT",
                message="request validation failed",
            ),
        ).model_dump(exclude_none=True),
    )


def get_or_create_session(session_id: str) -> Dict[str, Any]:
    with sessions_lock:
        if session_id not in sessions:
            sessions[session_id] = {
                "last_intent": None,
                "payment_validated": False,
                "updated_at": datetime.utcnow().isoformat(),
            }
        return sessions[session_id]


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    if req.intent not in ALLOWED_INTENTS:
        response = EvaluateResponse(
            decision="deny",
            reason=Reason(
                code="UNKNOWN_INTENT",
                message=f"intent '{req.intent}' is not allowed",
            ),
        )
        return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

    session = get_or_create_session(req.session_id)

    # Intent: send_email -> args: {"to": str}
    if req.intent == "send_email":
        recipient = req.args.get("to")

        if recipient is None:
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(code="MISSING_FIELD", message="args.to is required"),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

        if not isinstance(recipient, str) or not recipient.strip():
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="INVALID_ARGUMENT",
                    message="args.to must be a non-empty string",
                ),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

        if recipient not in TRUSTED_RECIPIENTS:
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="UNTRUSTED_RECIPIENT",
                    message=f"recipient '{recipient}' is not trusted",
                ),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

    # Intent: validate_payment -> args: {}
    elif req.intent == "validate_payment":
        pass

    # Intent: approve_payment -> args: {"amount": int|float}
    elif req.intent == "approve_payment":
        amount = req.args.get("amount")

        if amount is None:
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(code="MISSING_FIELD", message="args.amount is required"),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

        if not isinstance(amount, (int, float)):
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="INVALID_ARGUMENT",
                    message="args.amount must be a number",
                ),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

        if session["last_intent"] != "validate_payment" or not session["payment_validated"]:
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="INVALID_SEQUENCE",
                    message="approve_payment requires prior validate_payment in this session",
                ),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

        if amount > 5000:
            response = EvaluateResponse(
                decision="deny",
                reason=Reason(
                    code="POLICY_CHECK_FAILED",
                    message="amount exceeds approval threshold",
                ),
            )
            return JSONResponse(status_code=403, content=response.model_dump(exclude_none=True))

    # update session only on allow
    with sessions_lock:
        session["last_intent"] = req.intent
        if req.intent == "validate_payment":
            session["payment_validated"] = True
        session["updated_at"] = datetime.utcnow().isoformat()

    response = EvaluateResponse(decision="allow")
    return JSONResponse(status_code=200, content=response.model_dump(exclude_none=True))
