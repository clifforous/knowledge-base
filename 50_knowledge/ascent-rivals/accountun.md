# Ascent Rivals - Accountun

## Related
- [[overview]]
- [[midnight]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[eventun/data-model|eventun-data-model]]
- [[website]]

## Role
Accountun is the accounting execution service for tournament economics.

## Responsibilities
- manage tournament accounting lifecycle transitions
- process funding and outcome-linked payout planning
- finalize receipts and completion state
- support dust-related allocation and registration workflows

## Boundary
- Upstream domain intent is provided primarily by [[eventun/overview|eventun]].
- Accounting execution is aligned to [[midnight]] responsibilities.
- Website and operations tooling consume account state but should not own accounting transition logic.

## Open Questions
- Which transitions require asynchronous orchestration for operational resilience?
- What policy governs retry, replay, and audit of accounting operations?
- How should accounting version changes be introduced without lifecycle ambiguity?
