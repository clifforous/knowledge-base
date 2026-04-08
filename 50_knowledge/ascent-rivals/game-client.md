# Ascent Rivals - Game Client

## Related
- [[overview]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[eventun/data-model|eventun-data-model]]
- [[eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[website]]
- [[game-design]]
- [[lore]]

## Role
Primary gameplay execution surface for racing/combat sessions, player experience, and in-session competitive behavior.

## Functional Domains
- client and server runtime gameplay logic
- race, lobby, and session orchestration
- player, ship, loadout, and progression systems
- in-game UI routes and interaction flows
- stats tracking and end-of-match progression handling

## Service Relationship
- Consumes competition domain state represented by [[eventun/overview|eventun]].
- Uses service-owned persistent state for competition/accounting concerns instead of treating client runtime as the source of truth.
- Must not treat public AccelByte session visibility as gauntlet join authorization.
- Should expose gauntlet-stage join only when Eventun-backed qualification rules say the player may join.
- Must treat dedicated-server rejection or kick during gauntlet stage admission as a normal competition-rules flow, not just a transport failure.

## Open Questions
- What is the canonical sequence from match completion to externalized competition state updates?
- Which caches are authoritative versus convenience layers for UI responsiveness?
- Which gameplay outputs are required for downstream standings and accounting workflows?
- Which gauntlet-stage rejection and abort reasons should have distinct UX messaging?
