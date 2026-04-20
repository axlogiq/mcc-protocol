 ## Core Principle (Non-Negotiable)
Control is enforced at execution time, not at reasoning time.
No intelligence can bypass the control boundary without compromising the system itself.

---

⚠️ Warning: v0.1 does not include authentication or session management.
Do not use in production without additional security layers.
# MCC Protocol

Meta-Cognitive Control (MCC) is a protocol that defines the interface between AI reasoning and action.

## Core idea

AI systems do not execute actions directly.

All intents must be evaluated by MCC before execution.

## Minimal flow

intent → MCC → decision (allow / deny)

## Example

Request:
{
  "intent": "send_email",
  "args": {
    "to": "user@example.com",
    "body": "Hello"
  }
}

Response:
{
  "decision": "deny",
  "reason": {
    "code": "UNTRUSTED_RECIPIENT",
    "message": "recipient not allowed"
  }
}

## Orchestration (preview)

payment.amount > 5000 → requires validate_payment

## Status

v0.1 — minimal protocol (HTTP + JSON, allow/deny)

## Roadmap

v0.2 — escalate  
v0.3 — session model  
v0.4 — orchestration control
