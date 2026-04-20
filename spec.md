# MCC Protocol v0.1

## Overview

MCC (Meta-Cognitive Control) is a protocol that defines a control layer between AI reasoning and action execution.

All intents must be evaluated before execution.

---

## Endpoint

POST /evaluate

---

## Request

{
  "session_id": "string",
  "intent": "string",
  "args": {}
}

---

## Response

{
  "decision": "allow | deny",
  "reason": {
    "code": "string",
    "message": "string"
  }
}

---

## State model

MCC maintains state per session_id.

---

## Example: Orchestration control

Policy:
payment.amount > 5000 → requires validate_payment

Flow:
1. approve_payment (10000)
2. send_email

Result:

{
  "decision": "deny",
  "reason": {
    "code": "INVALID_SEQUENCE",
    "message": "approve_payment requires prior validate_payment"
  }
}
---

## Error codes

| Code | Description |
|------|------------|
| MISSING_FIELD | Required field is missing |
| INVALID_ARGS_TYPE | args must be an object |
| UNKNOWN_INTENT | Intent is not supported |
| MALFORMED_JSON | Invalid JSON payload |
| INTERNAL_ERROR | Unexpected server error |
| UNTRUSTED_RECIPIENT | Recipient not allowed |

## HTTP statuses

| Status | When |
|--------|------|
| 200 | Valid request processed |
| 400 | Bad request (missing/invalid fields) |
| 403 | Forbidden (policy deny) |
| 413 | Payload too large |
| 500 | Internal error |
