# Robotics: Restricted Zone Blocked

## Request

```json
{
  "session_id": "robot-001",
  "intent": "move_robot_arm",
  "args": {
    "zone": "restricted",
    "speed": 50
  }
}
```

## MCC Decision

```json
{
  "decision": "deny",
  "reason": {
    "code": "SAFETY_BOUNDARY",
    "message": "Restricted zone"
  }
}
```

## Principle
Execution must pass safety boundaries.
