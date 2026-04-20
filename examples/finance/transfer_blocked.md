# Finance: Block Transfer to Untrusted Recipient

## Request

```json
{
  "session_id": "finance-001",
  "intent": "send_money",
  "args": {
    "amount": 10000,
    "recipient": "unknown_wallet"
  }
}
```
## MCC Decision

```json
{
  "decision": "deny",
  "reason": {
    "code": "UNTRUSTED_RECIPIENT",
    "message": "Recipient not trusted"
  }
}
```

## Principle
MCC does not constrain reasoning.
It constrains execution.
