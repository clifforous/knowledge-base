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
- [[../../../30_designs/ascent-rivals/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[../../../30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]
- [[../../../10_research/ascent-rivals/eventun-team-postgresql-derivation-review|eventun-team-postgresql-derivation-review]]
- [[../../../10_research/ascent-rivals/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]]
- [[../../../30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan|eventun-telemetry-lifecycle-plan]]

## Data Model Scope
This model captures operational competition knowledge across events, identity, social structures, progression, and prize/accounting bridges.

## Domain Groups

### 1. Event stream domain
Captures session, match, heat, and player lifecycle events as a durable telemetry timeline used for downstream summaries and analytics.

The foundation implementation accepts one complete-match envelope through a shared ingest operation, with a stable batch id, stable event ids, producer sequence, canonical hashing, idempotent acceptance, one logical source-tagged event relation, and physical client/server plus event-type partitions. Automatic sender retry remains separate. Telemetry payloads do not carry schema versions; retained rows and affected derived state are rewritten when a payload shape changes.

The revised derived model has three layers:

1. immutable identified raw telemetry in source/event-type partitions;
2. narrow semantic facts that collapse lifecycle rows or establish idempotent contributions; and
3. incrementally maintained serving projections for fresh reads whose cost would otherwise grow with retained history.

The current foundation implementation creates one current, source-preserving fact graph per accepted batch in the same transaction: narrow match, heat, match-player, heat-player, and progression-metric facts. Heat-player facts retain valid lap count, total valid lap time, best valid lap time, and the winning lap source identity. Detailed lap/checkpoint segment metrics remain in raw partitions; no one-row-per-event lap or checkpoint fact exists. Rebuild replaces the current graph transactionally rather than retaining parallel derivation revisions.

MatchStart is the authoritative course context. Present heat course metadata must agree. Nullable single-player context is retained as the bounded canonical game enum name (`None`, `TimeTrial`, and peers), without inference from race mode or boolean compatibility. Explicit true/false/missing podium state remains distinct; only explicit true contributes `podium.count`. HeatStart and HeatEnd alone discover boundaries. HeatStart, HeatEnd, AscensionStart, PlayerHeatStart, PlayerHeatEnd, PlayerCheckpoint, PlayerLap, PlayerDied, PlayerRespawn, PlayerKill, PlayerGate, and SlalomGate are explicitly heat-scoped and must fall strictly inside the matching nonoverlapping pair, except for the boundary events themselves. Other events may retain nonnegative ambient heat without creating or requiring a boundary; this covers generated-Unreal MatchStart heat 0 and terminal final-heat context. The emitted per-player `PlayerHeatStart` remains the only loadout snapshot for that player/heat; extraction preserves its item-ID slots and augment slots without duplicating loadout data onto later events or inventing SKU facts. Medal extraction uses emitted medal-count entries, and kill dimensions use the emitted weapon item id.

On a disposable PostgreSQL 16.14 instance configured for the Azure B1ms CPU/RAM envelope (one CPU, 2 GiB), alternating ten-sample pairs measured three-heat workloads. A 5-human/11-bot and a maximum-normal 16-human match each retained 4,681 raw events and produced 122 (2.606%) and 375 (8.011%) narrow facts. Projected p50/p95 committed times were 231.129/282.180 ms and 276.690/348.895 ms; projection itself was 42.018/55.465 ms and 62.024/75.876 ms. A separately labeled synthetic 32-human/9,362-event stress case produced 743 facts (7.936%) with 615.083/813.962 ms committed and 104.120/183.690 ms projection times. Warm 16-human batch-local raw/fact lap queries had p50 0.071/0.016 ms. Fact heap plus index allocation was about 55 KB, 163 KB, and 332 KB per projected match respectively, with no fact TOAST. The disposable Docker filesystem was not capacity- or IOPS-shaped to the production tier's 32 GiB Azure storage, so this is local latency, buffer, WAL-generation, and relative allocation evidence, not durable Azure latency. Current reads and materialized views remain unchanged until incremental serving projections prove parity.

Season policy, statistics comparability, retention-oriented storage segmentation, and historical-detail retention are separate unresolved concerns. Do not require a producer-supplied `competition_period_id` or add period-based partitions until those policies have an authoritative owner and lifecycle. The implemented `game_event` hierarchy preserves client/server source and event-type pruning because that layout has demonstrated query-performance value. Legacy `client_event` and `server_event` relations remain for current reads until F14/F15 projection cutover, backfill, and representative query-plan comparison are complete. Stable match identity, source, timestamps, and game-build metadata provide the inputs needed to classify retained data later. See [[../../../30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan|eventun-telemetry-lifecycle-plan]].

The current producer no longer authors `ReplaySaved` telemetry. Replay association uses `ClientService.CreateMatchArtifact` and the `match_artifact` relation, optionally linked to Eventun's canonical accepted batch id. Legacy replay-event rows remain only for later deterministic conversion and cleanup.

Event source is trust provenance, not only storage metadata:

- dedicated-server submissions are the higher-trust source because they come from the service-controlled simulation through the shared ingest operation using a subjectless Server-authorized token;
- client submissions are authenticated to a player and client application, but their gameplay payload is self-reported and can be altered by a hostile client;
- client telemetry remains necessary for time trials, career/local play, and other modes without a dedicated server; and
- authentication proves who submitted a client batch, not that its events are truthful.

Eventun must derive and preserve source from the verified actor class rather than accept a producer-selected trust value. Facts, projections, qualification inputs, leaderboards, progression, insights, and rewards must retain enough provenance to apply an explicit source policy. They must not silently treat client-reported and dedicated-server data as equally authoritative.

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

Current team model:

- `team` stores team identity, one of the supported `open`, `invite`, or `request` membership modes, and colors
- `team_media` stores team media
- `team_player` stores one team membership per player, including role-like `designation` and optional manual `rank`
- `team_join_request` and `team_invite_request` store pending team lifecycle requests

Team `rank` is current roster metadata. It can support future team-member priority rules, but Eventun does not currently materialize ranked team-stage candidate lists.

Current membership is not historical: leaving deletes `team_player`. Team contribution and qualification attribution therefore require membership validity intervals before they can reliably answer which team a player represented at trusted event time.

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
- `gauntlet_stage_team` stores allowed or invited teams for a stage
- `gauntlet_stage_bracket` stores simple required stage win/loss filters, not a bracket graph
- `gauntlet_player_status` stores gauntlet-wide player group and stage win/loss summary state

Admission records are not a participant roster. Claiming a run, joining a lobby, or being admitted by Eventun does not consume participation.

Current implementation note: multi-match stages are supported by accepting each configured match for the stage run, then completing the run once all required matches are accepted. Final stage placement rows are aggregate rows ordered by summed circuit points, then best placement, placement sum, and player id for deterministic tie-breaking.

Current team/bracket implementation note: team-restricted stages are eligibility filters over current player team membership. Final accepted placement remains per-player. Eventun does not yet compute team standings, concrete player-owned or team-owned racer slots, locked team rosters, team stage results, bracket seeds, or bracket graph progression. `gauntlet_stage_placement` contains `stage_run_id` but its primary key is not stage-run scoped.

The retired `token_meta` catalog, `team_gate_token` relation, and `token_gated` membership mode were removed during the foundation reset. Existing gated teams transition to invite-only. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.

### 5. Prize and accounting-bridge domain
Captures funding intent, distribution intent, outcomes, payout planning, receipt progression, and claim state as the operational bridge into [[../accountun]] and [[../midnight]].

### 6. Progression and rewards domain
Captures gameplay medal definitions, progression metrics, draft goal definitions, published goal snapshots, challenge pools, published pool snapshots, player assignments, completed goals, reward bundles, reward entries, and reward grant attempts.

Progression authoring should distinguish staged operator work from player-facing runtime invariants:

- draft/import/edit flows may stage incomplete goals, reward definitions, pools, and memberships
- published snapshots are the runtime invariant for player-facing progression, challenge assignment, and reward creation
- player progress and completion rows should store the published snapshot used for history while using source goal identity to prevent duplicate non-repeatable completions across republished snapshots
- challenge availability should be determined by inclusion in a published challenge pool snapshot
- publish operations should validate requirements, reward validity, membership health, and assignment eligibility before any player assignment can use the pool
- publish should atomically create immutable snapshots or fail with explicit blockers; no partial publish should occur
- goal title and description localization is presentation data. Keep localized text separate from requirement/reward rules so translation fixes can be patched without changing progression semantics. V1 localization scope is title and description only. Localization export/import should be separate from goal definition CSV so translation work does not add locale-specific columns to the main authoring workflow.

Medal definitions should be treated as an authored catalog, not inferred only from observed event rows. The preferred source for the initial Eventun medal definition set is the game client's medal and medal-augment data tables. Eventun may still use observed event data to detect drift or unknown emitted codes.

Progression selectors should use source-of-truth data:

- course selectors should use AccelByte Cloud Save `Courses`, not the legacy Eventun `course` table
- gameplay part and weapon SKU selectors should use AccelByte catalog gameplay categories
- cosmetic catalog categories should not populate gameplay requirement dimensions
- reward authoring should use Eventun's configured AccelByte namespace; namespace should not be stored as operator-authored reward data
- ARC is the current fixed currency option for currency rewards, and Eventun should know or derive the AccelByte catalog target needed to fulfill it

Team progression is not yet defined. If approved, Eventun should own team contribution facts, XP ledger/caps, levels, and team cosmetic entitlements because the team entity is Eventun-owned. AccelByte remains appropriate for delivering configured player rewards. Prefer SQL constraints, narrow replayable contributions, bounded views/functions, and idempotent incremental projections over order-dependent worker increments or periodic full refresh; use workers for external effects, expensive goal evaluation, and bulk repair/rebuild work.

Current schema delivery deliberately uses `a*` through `d*` as the canonical clean-slate schema and a manually applied `migration.sql` production delta without a migration runner or ledger. Canonical data/configuration is sequential: `d0_data_media_purpose.sql`, `d1_data_progression.sql`, `d2_insight_policy.sql`, and the environment-aware `d3_schedule_refresh_views.sql`, which safely skips scheduling when pg_cron is unavailable. The guarded operational setup reapplies `d3_schedule_refresh_views.sql` after pg_cron is provisioned. The former frozen production delta was deployed and removed on 2026-07-13; `migration/migration.sql` now targets the current deployed production baseline and is the stable filename for the one pending one-time delta. Guarded delta verification uses `scripts/database.sh production-delta --confirm-disposable-production-baseline=<target-fingerprint>` against an authentic disposable copy of that baseline. Optional development fixtures are independently ordered as `t0_seed_courses.sql` through `t3_seed_teams.sql`, so production-delta cleanup never renumbers them. The PostgreSQL image runs canonical `a*` through `d*` files; no production delta or development fixture participates in automatic empty-database initialization.

## Ownership Boundary
- Eventun owns operational competition records and queryable competition state.
- [[../accountun]] owns accounting execution state transitions associated with [[../midnight]].
- Bridge fields in Eventun should be treated as operational state, not the final accounting source of truth.

## Open Questions
- What reconciliation policy governs operational bridge state versus accounting execution state?
- Which lifecycle transitions require strict idempotency guarantees at the domain boundary?
- What retention policy best balances historical analytics with storage growth?
