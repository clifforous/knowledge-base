# Ascent Rivals - Website

## Related
- [[overview]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[accountun]]
- [[cardano]]
- [[midnight]]

## Role
Primary web application surface for player-facing and operations-facing workflows.

## Responsibilities
- player identity and profile experiences
- competition discovery and context views
- team and social participation workflows
- sponsor and administrative operations
- entitlement and wallet-linked interaction flows

## Domain Boundary
- competition domain data is owned by [[eventun/overview|eventun]]
- accounting transitions are owned by [[accountun]] / [[midnight]]
- wallet/community identity context intersects with [[cardano]]

## Open Questions
- Which data requires strict real-time freshness versus eventual consistency?
- Which operations belong in public web workflows versus restricted operations tooling?
- Which views should expose private-versus-public distinction explicitly?
