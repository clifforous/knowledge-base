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
- Should call Eventun `GetGauntletStageJoinStatus(gauntlet_id, stage)` before joining a gauntlet stage AccelByte session.
- Should expose gauntlet-stage join only when Eventun returns an advisory joinable status.
- Must treat Eventun preflight as advisory; the dedicated server remains the final admission authority.
- Must treat returned `session_id` as the AccelByte session id.
- Should treat returned `stage_run_id` as Eventun run context, not as a join token.
- Must treat dedicated-server rejection or kick during gauntlet stage admission as a normal competition-rules flow, not just a transport failure.
- Should refresh Eventun-backed gauntlet state after rejection, kick, stage completion, or run completion.
- Can use `run_phase`, accepted/required match counts, and `current_match_id` from join status to distinguish prestart, match-in-progress, between-match, ready-to-complete, and completed stage states.

## Open Questions
- What is the canonical sequence from match completion to externalized competition state updates?
- Which caches are authoritative versus convenience layers for UI responsiveness?
- Which gameplay outputs are required for downstream standings and accounting workflows?
- Which gauntlet-stage rejection and abort reasons should have distinct UX messaging?
- What UI state should represent "between stage matches and rejoinable" for stage runs?
