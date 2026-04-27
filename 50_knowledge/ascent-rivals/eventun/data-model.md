# Ascent Rivals - Eventun Data Model

## Related
- [[../overview]]
- [[overview]]
- [[api]]
- [[../competition-runtime-terms]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[../midnight]]

## Data Model Scope
This model captures operational competition knowledge across events, identity, social structures, progression, and prize/accounting bridges.

## Domain Groups

### 1. Event stream domain
Captures session, match, heat, and player lifecycle events as a durable telemetry timeline used for downstream summaries and analytics.

Runtime hierarchy:

```text
Session
  Match
    Heat
      Lap
        Checkpoint
```

Qualifiers are not part of this runtime hierarchy. Qualifiers belong to the competition-structure domain and can span multiple sessions and matches.

### 2. Identity and social domain
Captures player identity, access context, wallet linkage, team membership, join/invite state, and eligibility constraints.

### 3. Content and sponsorship domain
Captures course, sponsor, and media attachments used by competition and presentation surfaces.

### 4. Competition structure domain
Captures tournament/gauntlet structure, qualifier/stage composition, participant status, and placement outcomes used for rankings and progression.

Competition structure can bind to runtime data through match/session context, but the concepts remain distinct:

- heats are match-internal runtime units
- qualifiers are gauntlet-level time windows or qualification structures
- stages/finals/brackets are tournament structures that may allocate runtime sessions
- a stage can define one or more configured stage matches/circuits through `gauntlet_stage_circuit(gauntlet_id, stage, match_id)`
- stage circuit `match_id` values are match indexes within the stage/session context and can start at `0`
- `gauntlet_stage_run` is the durable Eventun record for running one stage shard
- `gauntlet_stage_run.session_id` is the AccelByte session id, not another Eventun id
- `gauntlet_stage_run_admission` stores sparse on-demand evaluated join decisions for audit/cache use
- `gauntlet_stage_run_match` stores accepted match ids for a stage run; configured match plans remain in `gauntlet_stage_circuit`
- `gauntlet_stage_run_match_result` stores per-player accepted result rows for each accepted stage-run match
- `gauntlet_stage_placement` is the accepted final participation/result record and includes `stage_run_id`

Admission records are not a participant roster. Claiming a run, joining a lobby, or being admitted by Eventun does not consume participation.

Current implementation note: multi-match stages are supported by accepting each configured match for the stage run, then completing the run once all required matches are accepted. Final stage placement rows are aggregate rows ordered by summed circuit points, then best placement, placement sum, and player id for deterministic tie-breaking.

### 5. Token metadata domain
Captures token metadata needed for entitlement and social eligibility checks.

### 6. Prize and accounting-bridge domain
Captures funding intent, distribution intent, outcomes, payout planning, receipt progression, and claim state as the operational bridge into [[../accountun]] and [[../midnight]].

## Ownership Boundary
- Eventun owns operational competition records and queryable competition state.
- [[../accountun]] owns accounting execution state transitions associated with [[../midnight]].
- Bridge fields in Eventun should be treated as operational state, not the final accounting source of truth.

## Open Questions
- What reconciliation policy governs operational bridge state versus accounting execution state?
- Which lifecycle transitions require strict idempotency guarantees at the domain boundary?
- What retention policy best balances historical analytics with storage growth?
