# MCC Governance Layer (Draft)

This document defines governance mechanisms that operate on top of the MCC protocol.

## Scope

MCC defines the execution boundary.
Governance defines how decisions can be reviewed, overridden, and audited.

## Components

### 1. Appeal

Agents may request a re-evaluation of a denied action.

Possible implementations:
- human-in-the-loop review
- secondary validator
- multi-party approval (two-key rule)

### 2. Override

Controlled override mechanisms allow specific actions to bypass default denial.

Requirements:
- explicit authorization
- audit logging
- scoped permissions

### 3. Policy Management

Policies are external to MCC and may be:
- static (embedded rules)
- dynamic (OPA / Rego / remote policy service)

### 4. Audit Log

All decisions should be recorded:

- session_id
- intent
- args_hash
- decision
- reason
- timestamp

## Design Principle

Governance must be composable and independent from the core protocol.

The MCC protocol should not be modified to support governance features.
