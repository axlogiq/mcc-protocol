# Agent: Dangerous Command Blocked

## Request

```json
{
  "session_id": "agent-001",
  "intent": "execute_command",
  "args": {
    "command": "rm -rf /"
  }
}
```

## MCC Decision

```json
{
  "decision": "deny",
  "reason": {
    "code": "POLICY_CHECK_FAILED",
    "message": "Destructive command"
  }
}
```

## Principle
Capability is not permission.
