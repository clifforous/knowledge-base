# Ascent Rivals - Eventun Data Model

## Related
- [[../overview]]
- [[../accelbyte-game-records]]
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
Captures sponsor and media attachments used by competition and presentation surfaces. Eventun may store course references and derived course data for operational queries, but AccelByte Cloud Save `Courses` is the source of truth for official course configuration, including course code, default laps, and release feature state.

Eventun should not treat its local `course` table as authoritative for official course eligibility rules. For stat/progression eligibility, prefer game-authored runtime flags such as heat-level regulation status and, where course metadata is needed, use AccelByte `Courses` data or a controlled cache derived from it.

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

### 7. Progression and rewards domain
Captures gameplay medal definitions, progression metrics, draft goal definitions, published goal snapshots, challenge pools, published pool snapshots, player assignments, completed goals, reward bundles, reward entries, and reward grant attempts.

Progression authoring should distinguish staged operator work from player-facing runtime invariants:

- draft/import/edit flows may stage incomplete goals, reward definitions, pools, and memberships
- published snapshots are the runtime invariant for player-facing progression, challenge assignment, and reward creation
- challenge availability should be determined by inclusion in a published challenge pool snapshot
- publish operations should validate requirements, reward validity, membership health, and assignment eligibility before any player assignment can use the pool
- publish should atomically create immutable snapshots or fail with explicit blockers; no partial publish should occur

Medal definitions should be treated as an authored catalog, not inferred only from observed event rows. The preferred source for the initial Eventun medal definition set is the game client's medal and medal-augment data tables. Eventun may still use observed event data to detect drift or unknown emitted codes.

Progression selectors should use source-of-truth data:

- course selectors should use AccelByte Cloud Save `Courses`, not the legacy Eventun `course` table
- gameplay part and weapon SKU selectors should use AccelByte catalog gameplay categories
- cosmetic catalog categories should not populate gameplay requirement dimensions
- reward authoring should use Eventun's configured AccelByte namespace; namespace should not be stored as operator-authored reward data
- ARC is the current fixed currency option for currency rewards, and Eventun should know or derive the AccelByte catalog target needed to fulfill it

## Ownership Boundary
- Eventun owns operational competition records and queryable competition state.
- [[../accountun]] owns accounting execution state transitions associated with [[../midnight]].
- Bridge fields in Eventun should be treated as operational state, not the final accounting source of truth.

## Open Questions
- What reconciliation policy governs operational bridge state versus accounting execution state?
- Which lifecycle transitions require strict idempotency guarantees at the domain boundary?
- What retention policy best balances historical analytics with storage growth?
