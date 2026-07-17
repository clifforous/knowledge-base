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

F14 adds synchronous, idempotent serving state in the accepted-batch transaction. `match_serving_projection_state` records one projected batch's source receipt, exact fact fingerprint, projection schema version, projector version, and timestamps. Accepted matches and repairs lock affected players in UUID order before additive singleton rollup updates, so concurrent distinct matches for one player serialize without losing either contribution. `player_course_record_contribution` retains each eligible batch/heat/player/category source identity, time, loadout value, occurrence, session/match, course, and `single_player_mode`; `player_course_record` retains the deterministic current winner keyed by source, record category, course, and player. Record categories remain server/client `finish` and `lap` plus client-only `high_cost_finish`, `high_cost_lap`, `low_cost_finish`, and `low_cost_lap`, with the legacy inclusive `<= 10,000` and `<= 3,000` loadout-value thresholds. Winner and top-N order is time, loadout value ascending with null last, then deterministic identity tie-breaks; `player_rank` applies the same two-non-null loadout ordering. Mutable profile and team presentation are joined at read time rather than stored as record identity.

`player_career_contribution` is one canonical dedicated-server contribution per batch/player. `player_career_rollup` and `player_course_career_rollup` retain mergeable sums, counts, and minima for matches, kills, deaths, crashes, obelisks, podiums, play/lap/finish time, weight, circuit points, and credits; APIs derive averages and null behavior at read time. Only explicit `reported_podium_finish = true` contributes a podium. Match History reads server `match_fact`/`match_player_fact` by MatchStart time and associates SessionStart client version and `match_artifact` replay data. SessionStart and PlayerJoin provenance use the complete time/batch/sequence/event tuple boundary, so an equal-time event ordered after MatchStart cannot change the frozen version or bot policy. Time-trial self-history selects and limits eligible current fact identities first and then fetches exact bounded client PlayerHeatStart/End detail, including the reported best-lap field and loadout. Time-trial and post-match candidate joins explicitly constrain every fact relation by source and are supported by the placed-player completion-history index; measured full shapes may instead choose a selective match-first primary-key join. Full match summary and current-match insight baselines/metrics remain deliberately session/match-scoped raw reads for bot rows, loadouts, complete heat/standing shape, and metrics absent from compact facts. Detailed post-match self-history analogously selects current canonical server Ascent/placed candidates from the fact graph, applies the ascension cutoff and per-heat limit, and then fetches only those selected PlayerHeatStart/End raw identities.

Eventun owns the accepted logical season model: explicit finite regular/off-season windows are non-overlapping and half-open, gaps are allowed, and a compact match fact will carry nullable season attribution resolved from its accepted batch MatchStart. Uncovered matches remain unseasoned and continue to support lifetime statistics and unfiltered Match History. Producers do not submit season identity. The initial seasonal projections cover best lap, best finish, and their ranks while existing lifetime records and career aggregates remain. Season splitting and reassignment between attributed seasons are deferred recovery concerns; telemetry defects use fact/contribution repair. Seasons do not define PostgreSQL partitions, retention tiers, game builds, AccelByte Season Pass identity, or MMR ownership. The implemented `game_event` hierarchy preserves client/server source and event-type pruning because that layout has demonstrated query-performance value. Legacy relations remain transition-only until the historical event cutover and cleanup. See [[../../../30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan|eventun-telemetry-lifecycle-plan]].

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
Captures sponsor and media attachments used by competition and presentation surfaces. Eventun may store course references and derived course data for operational queries, but AccelByte Cloud Save `Courses` is the source of truth for official course configuration, including course code, default laps, release feature state, and explicit Website archive metadata. Website-facing reads classify configured production-ready courses as `published`, explicitly retired previously public courses as `archived`, and all remaining or invalid configurations as hidden. Eventun's derived `course.active` value is not a publication contract.

Sponsor advertising currently has two independent ownership paths. `sponsor_media` can hold reusable advertising assets, while `gauntlet_media` can hold campaign-specific assets directly on one gauntlet. Both purpose catalogs currently contain `Billboard` and `WideBillboard`. The reviewed game client consumes normal `Billboard` media for course placement and uses the metadata field `Tileable` to decide whether an image can fill a ribbon-style placement; its separate `WideBillboards` collection has no identified runtime consumer. `gauntlet_sponsor` optionally associates a reusable sponsor record and a relationship-specific tier. Current organizer practice often uses direct gauntlet media because sponsor artwork varies by tournament; a reusable sponsor relation is not required merely to supply billboards.

Media-purpose catalogs across sponsors, gauntlets, and teams were designed partly as anticipated use-location labels. Many values do not have a confirmed active Website or game-client consumer and should not be interpreted as distinct presentation contracts. Current billboard usage is predominantly square artwork. Dimension extraction and automatic matching to similarly shaped course slots were an intended direction, not an established workflow.

Eventun should not treat its local `course` table as authoritative for official course eligibility rules. For stat/progression eligibility, prefer game-authored runtime flags such as heat-level regulation status and, where course metadata is needed, use AccelByte `Courses` data or a controlled cache derived from it.

### 4. Competition structure domain
Captures tournament/gauntlet structure, qualifier/stage composition, participant status, and placement outcomes used for rankings and progression.

Competition structure can bind to runtime data through match/session context, but the concepts remain distinct:

- heats are match-internal runtime units
- qualifiers are gauntlet-level time windows or qualification structures
- stages/finals/brackets are tournament structures that may allocate runtime sessions
- a stage can define one or more configured stage matches/circuits through `gauntlet_stage_circuit(gauntlet_id, stage, match_id)`
- stage circuit `match_id` values are exact zero-based ordered positions within the stage/session context: an authored circuit must be contiguous `0..N-1`, and its frozen run rules preserve those same positional identities
- `gauntlet_stage_run` is the durable Eventun record for running one stage shard
- `gauntlet_stage_run.session_id` is the AccelByte session id, not another Eventun id
- `gauntlet_stage_run_admission` stores sparse on-demand evaluated join decisions for audit/cache use
- `gauntlet_stage_run_match` stores accepted match ids for a stage run; configured match plans remain in `gauntlet_stage_circuit`
- `gauntlet_stage_run_match_result` stores per-player accepted result rows for each accepted stage-run match
- `gauntlet_stage_placement` is the accepted final participation/result record and includes `stage_run_id`
- `gauntlet_stage_team` stores allowed or invited teams for a stage
- `gauntlet_stage_bracket` stores simple required stage win/loss filters, not a bracket graph
- `gauntlet_player_status` stores gauntlet-wide player group and stage win/loss summary state
- `gauntlet_projection_state` stores the gap-free semantic revision, projection schema version, and projector version for one gauntlet
- `gauntlet_player_match_contribution` and `gauntlet_player_stat_rollup` retain server-authoritative gauntlet match evidence and current player statistics
- `gauntlet_qualifier_match_contribution`, `gauntlet_qualifier_score_projection`, and `gauntlet_qualifier_sequence_match` retain server/non-bot qualifier contributions, the best configured trailing sequence, and its exact ordered source matches
- `gauntlet_player_score_projection` retains the current overall individual qualification score using configured `stat_top_k`
- `gauntlet_qualification_snapshot` plus entry, qualifier, and match-evidence children stores immutable versioned individual cutoff state; entries seal unique deterministic `selection_rank`, while qualifier children seal the competitive `qualifier_rank` already represented in cutoff protobuf evidence and the resolution hash

Admission records are not a participant roster. Claiming a run, joining a lobby, or being admitted by Eventun does not consume participation.

Current implementation note: multi-match stages are supported by accepting each configured match for the stage run, then completing the run once all required matches are accepted. Final stage placement rows are aggregate rows ordered by summed circuit points, then best placement, placement sum, and player id for deterministic tie-breaking.

F14 qualifier projection policy is server-only, canonical-unfiltered, and bot-excluding. The telemetry field historically named `activeQualifiers` contains gauntlet ids; a gauntlet id present there selects the server match for gauntlet contributions, and qualifier time windows determine qualifier membership. A normal in-order match evaluates only the new trailing `stat_window`; late or rewritten input and qualifier/configuration changes perform bounded affected recomputation. The batch updater is the only qualifier mutation path; the unused out-of-protocol single-match updater was removed. Batch-leading player and gauntlet/batch qualifier-contribution indexes bound accepted and repair access. A separate qualifier-contribution `(batch_id, player_id, gauntlet_id, qualifier_id)` index supports the child lookup when fact repair deletes a match-player fact; qualifier-leading contribution and score indexes support qualifier deletion cascades without retained-history scans. Both targeted repair entry points first serialize on `event_ingest_batch`, then use the shared player-before-gauntlet lock order. The semantic fingerprint includes the top-level projection configuration plus every non-operational contribution, score, and selected-evidence field, including source/player-type events and session/match identities. Accepted updates, configuration changes, repairs, targeted rebuilds, and full rebuilds acquire affected gauntlet locks in UUID order. A semantic output, configuration, or exact-evidence change increments the gauntlet revision exactly once and stamps every affected row; a proven identical retry/rebuild preserves the revision, including for empty gauntlets only when configuration is identical.

Qualification cutoff publication is explicit operator state, not a wall-clock side effect, and supports only pure individual stages scored by `circuit_points`. `row_number` and cutoff `selection_rank` are unique deterministic ordinals using the complete stable tie-break order; displayed `ranking`, including sealed `qualifier_rank`, is a dense competitive rank over performance fields without the final player-id tie-breaker. Top-N and pagination use the ordinals, so shared competitive rank never changes cardinality. Admin preview returns a locked projection revision and exact projection schema/projector versions plus configuration/resolution hashes and deterministic entry/evidence rows. Publish seals immutable parent and child rows at the exact revision/schema/projector tuple and is idempotent by operation/key/request hash. Replace creates a new version linked to the latest sealed snapshot and requires a correction reason. First stage-run claim locks gauntlet state before the run row, requires the latest sealed cutoff to match the live configuration hash/revision/schema/projector tuple, and stores both its exact cutoff id and serialized stage rules. A same-session retry returns that stored binding without current-revision revalidation or mutation. Admission uses the snapshot entry's deterministic selection ordinal for its legacy row/rank fields and selection policy, plus the sealed qualification points/counts and total circuit points; no separate overall competitive rank is added to cutoff entries or admission. All stage restrictions are read from `rules_snapshot`; configured-match validation and required-match/completion counts also use that frozen circuit. Stage-run allocation takes the same gauntlet projection lock before the stage-row lock, so it cannot insert after an update's run-history snapshot and then be cascade-deleted. Update preserves every stage parent that has run/history rows, editing open/invite configuration in place; a full-replacement request that omits any run-backed stage fails before mutation rather than silently retaining an extra active stage. Only qualification-bound stages receive the stricter cutoff-configuration freeze. Later cutoff replacement remains frozen, while permitted cosmetic, circuit, and other non-cutoff live edits cannot retroactively change the run.

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

Current schema delivery deliberately uses `a*` through `d*` as the canonical clean-slate schema and a manually applied `migration.sql` production delta without a migration runner or ledger. Canonical data/configuration is sequential: `d0_data_media_purpose.sql`, `d1_data_progression.sql`, and `d2_insight_policy.sql`. F14 removed `d3_schedule_refresh_views.sql`, `refresh_leaderboard_materialized_views`, all eight leaderboard and four gauntlet materialized views, and operational pg_cron provisioning because accepted transactions now maintain their replacements. The former frozen production delta was deployed and removed on 2026-07-13; `migration/migration.sql` now targets the current deployed production baseline and is the stable filename for the one pending one-time delta. Its F14 destructive serving cutover acquires the same advisory lock as F15 and fails closed unless `serving_projection_cutover_state` contains a `historical_backfill_validated` manifest. F14 verification proves that gate and cutover SQL against a canonical disposable schema; F15 still owns authentic production-baseline backfill, manifest validation, rollback/recovery, execution, and legacy cleanup. Optional development fixtures remain independently ordered as `t0_seed_courses.sql` through `t3_seed_teams.sql`, so production-delta cleanup never renumbers them. The PostgreSQL image runs canonical `a*` through `d*` files; no production delta or development fixture participates in automatic empty-database initialization.

## Ownership Boundary
- Eventun owns operational competition records and queryable competition state.
- [[../accountun]] owns accounting execution state transitions associated with [[../midnight]].
- Bridge fields in Eventun should be treated as operational state, not the final accounting source of truth.

## Open Questions
- What reconciliation policy governs operational bridge state versus accounting execution state?
- Which lifecycle transitions require strict idempotency guarantees at the domain boundary?
- What retention policy best balances historical analytics with storage growth?
