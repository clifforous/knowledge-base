# Eventun Team And Gauntlet PostgreSQL Derivation Review

Status: Technical research
Date: 2026-07-10
Last updated: 2026-07-13
Reviewed repository: [Eventun](https://github.com/ikigai-github/eventun) at `34b42861f2a698be50b0d7de134881544d072658`

## Related

- [[ascent-rivals/initiatives/teams-and-team-gauntlets/teams-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design]]
- [[eventun-foundation-api-simplification-review]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[ascent-rivals/system/team-gauntlet-current-state|team-gauntlet-current-state]]

## Question

How should Eventun use PostgreSQL to derive low-latency team progression, qualification, runtime admission, and bracket state while avoiding brittle asynchronous table updates and respecting a low-resource database tier?

## Executive Conclusion

Use a database-first hybrid:

- PostgreSQL should own temporal membership, match-level derivation state, ledgers, constraints, qualification snapshots, resolved slots, roster locks, results, brackets, and durable outboxes.
- SQL functions and ordinary views should calculate genuinely bounded aggregates over narrow domain facts.
- Incrementally maintained projection tables should serve fresh leaderboard, career, and gauntlet reads whose cost would otherwise grow with retained history.
- Native materialized views are not the target for player-facing or competition reads because refresh introduces avoidable delay and repeats full-history work. Retain them only as transitional or offline analytical artifacts until incremental replacements pass parity.
- Eventun workers should perform bulk replay or repair, call external services, deliver notifications or rewards, allocate sessions, and handle expensive goal evaluation; normal narrow fact derivation remains in the accepted-batch transaction.

The follow-up foundation review supersedes this document's original decision to defer event identity. Stable batch ids, event ids, and producer sequence are now approved foundation work alongside temporal membership, frozen admission state, stage-run-scoped results, and robust queue behavior.

## Review Scope

The review covered:

- raw server and client event schemas and bulk ingestion;
- player progression work creation, claiming, failure, and reward delivery;
- team membership schema and leave behavior;
- leaderboard and gauntlet materialized-view refresh;
- gauntlet admission query shape;
- stage-run match and placement keys;
- likely read paths for team qualification, roster views, slot admission, and bracket advancement.

This is a schema and query-path review, not a production load test. Performance targets below require validation on the deployed PostgreSQL tier.

## Accepted Operating Constraints

- Event submission is currently at most once. The replacement storage contract will be idempotent, while automatic sender retry remains a separate behavior change.
- Ordinary gameplay submissions contain one complete match: `MatchStart`, `MatchEnd`, and all intervening events.
- Replay association now uses a dedicated match-artifact operation rather than a later authored `ReplaySaved` event.
- Stable batch ids, event ids, and producer sequence are implemented in the coordinated Eventun/game-client working trees.
- Telemetry payloads do not carry schema versions. When a payload shape changes materially, retained rows and derived data are rewritten through a controlled migration.
- The current deployment is believed to be PostgreSQL 16.14 on an Azure B1ms-class instance with one core and 32 GiB storage, at approximately $16 per month.
- Raw telemetry is currently retained indefinitely.
- A season or major release may become a statistics-comparability boundary, but season cadence, scope ownership, and historical product behavior are not yet defined.
- Raw telemetry is not removed until retention tiers, archive/restore tooling, and durable historical outputs are explicitly approved and validated.

## Confirmed Findings

### 1. Current At-Most-Once Ingestion Lacks Durable Source Identity

[`server_event` and `client_event`](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L3-L113) have no event id, ingest batch id, ingest timestamp, primary key, or uniqueness constraint. [Bulk ingestion](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/events.go#L93-L133) copies the supplied rows in one transaction.

The current atomic copy prevents a partially committed request, but it cannot distinguish a retry from a second logical submission, preserve producer ordering when timestamps tie, or give derived facts a stable source row.

Approved replacement:

- client-generated `batch_id` on the complete-match envelope;
- client-generated `event_id` and contiguous producer `sequence` on every event;
- canonical payload hash for idempotent batch acceptance;
- same-content duplicate acceptance and conflicting-content rejection;
- sender retry deferred until the idempotent contract is deployed and verified.

### 2. Progression Work Already Uses The Match Boundary

The current match-ingest job unique index is player, scope, session, match, and trigger kind. That is consistent with complete-match submissions and one derivation pass per player and match.

The limitation is operational visibility:

- there is no first-class match-ingest record describing receipt, event count, derivation state, or failure;
- the system cannot distinguish “match never delivered” from “match delivered but derivation failed” through one compact record;
- partial or late additions are outside the contract and should be rejected rather than silently merged.

A small match-ingest ledger could simplify derivation and diagnostics without changing delivery semantics or introducing retries.

### 3. Team Membership Cannot Support Historical Attribution

[`team_player`](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L912-L922) stores only current membership. [Leaving removes the row](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/team_api.go#L263-L288).

Effects:

- a late match fact cannot be attributed to the team active at event time;
- rebuilding team qualification after a roster change produces a different answer;
- historical team challenge contribution cannot be audited;
- disputes require external logs rather than authoritative domain state.

Membership intervals are a prerequisite for team progression and team qualification.

### 4. Qualifier And Leaderboard Materialized Views Are Transitional

The refresh procedure rebuilds leaderboard and gauntlet materialized views sequentially with a commit after each refresh and runs [hourly](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/c4_proc_refresh_views.sql#L1-L53).

Effects:

- standings may lag by almost an hour;
- different views can temporarily represent different refresh points;
- the result is unsuitable as the final authoritative field without a separate cutoff transaction;
- full concurrent refresh can consume disproportionate resources on a free or low tier.

PostgreSQL's [native materialized-view model](https://www.postgresql.org/docs/current/rules-materializedviews.html) stores and refreshes a relation; it does not provide an automatic incremental-maintenance contract for this domain. Eventun should replace the current player-facing leaderboard and gauntlet views with incrementally maintained ordinary tables. Native materialized views may remain useful for offline or deliberately delayed analytics, but no current product surface requires their refresh delay.

### 5. Runtime Admission Recomputes A Broad Population

[`queryGauntletStageAdmissionCandidate`](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/gauntlet_stage_run_api.go#L709-L778) calls `gauntlet_stats(gauntlet_id)` and filters to one player afterward.

Effects:

- admission cost grows with the gauntlet population;
- the query recomputes mutable standing data while a player joins;
- it cannot directly answer which concrete team-owned slot the player may occupy;
- it is harder to keep admission latency predictable.

Runtime admission should be a point read against a frozen stage field and current approved roster policy.

### 6. Accepted Placement Uniqueness Is Not Stage-Run Scoped

[`gauntlet_stage_placement`](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L1145-L1156) stores `stage_run_id` but its primary key is `(gauntlet_id, stage, player_id)`.

Effects:

- one player cannot have accepted placements in multiple bracket runs for the same logical stage;
- replay and parallel bracket matches conflict;
- result identity does not match the existing stage-run match-result identity.

The replacement key must include `stage_run_id`.

### 7. Failed Progression Work Can Retry Hot

The progression scheduler selects queued and failed rows [oldest first without a row lease](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/progression_worker.go#L76-L101). Failure increments `attempt_count` but [does not advance `available_at` or apply a terminal attempt limit](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/progression_goal_check_workflow.go#L163-L177).

Effects:

- multiple workers can contend for the same candidate before a later state transition;
- a permanently failing oldest job can be selected repeatedly;
- no bounded exponential backoff or dead-letter state protects the database and external dependencies.

New team projection or notification work should not copy this queue behavior unchanged.

### 8. Processing-Order Totals Are Fragile During Rebuild Or Correction

Any worker that incrementally applies contribution caps in processing order risks producing a different accepted total when historical payloads are rewritten, facts are rebuilt, or operator correction occurs. Late partial events are not part of the current complete-match contract. This is an architectural risk rather than a single confirmed query defect.

Team caps should be derived from match-keyed contribution facts under deterministic ordering, or applied by one database function whose correction semantics are explicit.

## Target Data Layers

### Layer 1: Identified Complete-Match Telemetry

Replace the duplicated logical raw-event model with one source-tagged `game_event` parent plus one compact `event_ingest_batch` row per accepted complete batch. Preserve physical client/server and event-type partitions beneath that parent initially; the current leaf layout and indexes have demonstrated query benefits:

| Field | Purpose |
|---|---|
| `batch_id` | Stable idempotency and derivation identity |
| `source_kind`, `session_id`, `match_id` | Match context and immutable trust provenance derived from the authorized API path |
| `game_build` | Diagnostics and a future input to statistics-scope classification |
| `received_at` | Operational receipt time |
| `event_count` | Diagnostics and completeness checks |
| `match_start_at` and `match_end_at` | Confirm the complete-match envelope |
| `derivation_status` | Pending, succeeded, failed, or rebuilt |
| `last_error` | Bounded operational diagnostic |

Each `game_event` has stable event identity, producer sequence, source batch, occurred time, event type, and event-specific data. The batch hash and uniqueness constraints make the storage contract retry-safe even before sender retry is enabled.

`source_kind` is also a trust boundary. Dedicated-server batches are higher trust; authenticated client batches identify the submitter but remain self-reported and potentially alterable. Client data is still required for time trials and modes without a dedicated server. Derived facts and snapshots therefore retain source and apply an explicit consumer policy rather than erasing provenance during aggregation.

Move replay association to `match_artifact`; it is not part of the complete-match telemetry envelope.

When telemetry JSON changes, use a database migration or purpose-built rewrite tool to transform retained rows and rebuild affected facts. Do not retain multiple payload schema branches indefinitely.

### Layer 2: Narrow Semantic Contributions

Project only facts that collapse lifecycle events or establish an idempotent
semantic contribution:

| Fact | Example key and use |
|---|---|
| `match_fact` | Session and match completion, canonical status, course, mode |
| `match_player_fact` | Session, match, player; accepted placement, lap, kills, score |
| `heat_fact` and `heat_player_fact` | Circuit/course context, canonical heat state, player heat result, proven loadout dimensions, lap count/total/best, and best-lap source identity |
| `progression_metric_fact` | Idempotent normalized contribution keyed to the source result fact |
| `qualification_performance_fact` | Gauntlet, player, source match; reproducible qualifier contribution |
| `team_contribution_fact` | Team, player, source event or match; bounded progression input |

Do not create a one-to-one typed copy of every lap or checkpoint. Current
cross-match reads need aggregate lap values or retained records; current detailed
insight reads are bounded to one batch and player and can use the raw event-type
partitions. Add a segment projection only when a concrete cross-match query and
representative measurements justify it.

Facts include stable source identity and immutable trust provenance. Retain one
current fact set per accepted batch and replace it transactionally during a
payload rewrite or repair. Do not retain parallel global fact revisions unless a
future zero-downtime projection migration defines immutable projector ownership,
activation, and downstream reconciliation.

Raw telemetry remains available for diagnosis while its season/release partitions are retained. Product reads should not repeatedly parse large event payloads.

### Layer 3: Authoritative Domain State

Use ordinary tables and constraints for:

- membership validity intervals;
- team XP ledgers and cap allocations if progression is approved;
- durable team cosmetic entitlement grants;
- qualification cutoff and selected-owner snapshots;
- concrete stage-run racer slots;
- locked slot occupants;
- stage-run-scoped results;
- bracket matches, positions, and advancement;
- notification, reward, and session-allocation outboxes.

These records represent decisions or externally visible state and should not disappear during a view refresh.

### Layer 4: Bounded Query Views And Functions

Use ordinary views or `STABLE` SQL functions over narrow facts or incremental projections for:

- current active roster;
- team for player at event time;
- team-filtered roster leaderboard;
- top-N member team score;
- current team XP and level;
- current bracket graph;
- player admission point read.

These mechanisms preserve one source of truth while input cardinality remains
bounded by the team, configured top N, stage field, or another explicit product
limit. They are not the preferred serving path for lifetime player history or a
public population whose cost grows continuously.

### Layer 5: Incremental Serving Projections

Use ordinary projection tables for fresh reads whose direct cost grows with
retained history. Update mergeable records and rollups transactionally with the
accepted fact when the measured ingest budget permits. Otherwise enqueue one
idempotent immediate projection operation; do not use an hourly full refresh as
the normal freshness contract.

Each projection requires:

- explicit match/cutoff watermark;
- a clearly owned current projector definition rather than parallel unnamed revisions;
- `updated_at`;
- a complete rebuild path;
- a unique key matching the read;
- source-contribution idempotency and targeted reconciliation;
- a transactional rebuild/swap path when an online replacement is required.

Initial projections should include:

- one retained player/course record per source, record category, course, and player;
- player and player/course career rollups containing sums, counts, and minima;
- one gauntlet match contribution per player/match/qualifier plus the retained best sequence and its source matches; and
- progression counters backed by idempotent metric contributions.

A projection is rebuildable serving state, not the authoritative qualifier
cutoff snapshot. Cutoff publication copies the selected field and its evidence
into immutable competition state.

## Membership Interval Model

Minimum fields:

| Field | Requirement |
|---|---|
| `team_id` and `player_id` | Foreign-keyed identity |
| `joined_at` | Inclusive start |
| `left_at` | Null while active; exclusive end |
| `title_code` and `competition_rank` | Versioned metadata where historical policy needs it |
| `created_by`, `ended_by`, `reason` | Audit |

At minimum, enforce one open interval per player with a partial unique index on `player_id WHERE left_at IS NULL`. A database function should serialize join, leave, transfer, and correction.

If overlapping closed intervals must be prevented entirely, evaluate a range exclusion constraint using `tstzrange` and `btree_gist`. Measure extension availability and write cost on the deployed tier before requiring it.

PostgreSQL 18 adds native temporal `PRIMARY KEY` and `UNIQUE ... WITHOUT OVERLAPS` constraints. That can make the membership invariant more declarative, but an upgrade is not required: PostgreSQL 16 can enforce the same rule with a GiST exclusion constraint or a serialized transition function.

Queries should use half-open intervals:

```sql
joined_at <= occurred_at
AND (left_at IS NULL OR occurred_at < left_at)
```

## Aggregation Mechanism Matrix

| Need | Preferred mechanism | Reason |
|---|---|---|
| Active roster | Indexed table or ordinary view | Small, transactional, current state |
| Historical team attribution | Indexed membership interval query | Requires exact event-time answer |
| Team-filtered roster leaderboard | Ordinary view/function over the incremental player record projection | Current rosters are small while lifetime performance history is not |
| Top-N team qualification preview | SQL function/view over indexed player scores | Window functions express the rule directly |
| Published qualifier field | Immutable snapshot tables | Stable, reproducible competition decision |
| Runtime admission | Indexed slot and membership point read | Predictable low latency |
| Team XP and cap balance | Contribution ledger plus bounded SQL or an incremental current-balance projection | Preserves idempotency and replay without periodic full refresh |
| Bracket advancement | Synchronous transaction | Correctness and downstream routing must be atomic |
| Public leaderboard | Incremental player/course record projection | Fresh after each accepted contribution without full-history refresh |
| AccelByte delivery | Durable outbox and worker | External side effect cannot be one PostgreSQL transaction |

## Worker Responsibilities

### Workers Are Appropriate For

- bulk fact/projection replay, backfill, and reconciliation;
- expensive progression goal evaluation;
- AccelByte reward fulfillment;
- AccelByte Chat notification delivery;
- AccelByte session allocation;
- repair and reconciliation.

### Workers Are Not Required For

- current team roster;
- current team level from thresholds and a ledger;
- top-N score calculation at a requested cutoff;
- stage slot ownership;
- roster-lock validation;
- accepted result and bracket advancement.

These should be direct reads or synchronous database transactions.

## Queue Pattern

Use a claim operation that atomically leases rows. A typical PostgreSQL shape is:

```sql
WITH candidates AS (
  SELECT id
  FROM work_item
  WHERE status IN ('queued', 'retry')
    AND available_at <= now()
  ORDER BY available_at, created_at
  FOR UPDATE SKIP LOCKED
  LIMIT $1
)
UPDATE work_item AS work
SET status = 'running',
    locked_at = now(),
    lock_expires_at = now() + $2::interval,
    attempt_count = attempt_count + 1
FROM candidates
WHERE work.id = candidates.id
RETURNING work.*;
```

Add:

- lease expiry and abandoned-work recovery;
- bounded exponential backoff with jitter;
- maximum attempts;
- terminal or dead-letter status;
- deduplication key;
- match/cutoff watermark and configuration revision where relevant;
- concise error code and bounded diagnostic text.

PostgreSQL documents `SKIP LOCKED` as suitable for queue-like access to avoid lock contention, not as a general consistent read mechanism: [`SELECT` locking clause](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE).

## Qualification Query Shape

The logical team calculation is:

1. select player scores for the gauntlet and cutoff watermark;
2. join membership intervals at each contribution's trusted time;
3. calculate the accepted member score under the gauntlet's best-N-performance rule;
4. rank member scores per team;
5. retain member rank up to configured team contributor N;
6. aggregate team score;
7. apply deterministic team tie-breakers.

Store the selected contributor rows in the cutoff snapshot. Do not retain only the aggregate score; the breakdown is required for audit, display, and correction review.

## Season, Statistics, And Telemetry Retention

The earlier `competition_period_id` recommendation combined four concepts that are not yet defined: a player-facing product season, a statistics comparability scope, a physical telemetry storage segment, and a retention tier. Those concepts may align later, but they must not share an identifier or lifecycle by assumption.

No active-period API, producer period field, Eventun period catalog, or period-based partition should be implemented yet. Stable match identity, source, occurrence and receipt timestamps, and `game_build` are sufficient to classify retained matches after the product policy is known.

If the event reset proceeds first, use a unified logical event parent while retaining physical pruning by source and event type. Do not replace the demonstrated layout with one unpartitioned payload table without representative `EXPLAIN (ANALYZE, BUFFERS)` and latency comparisons. Select any additional retention partition key only after measuring volume, index size, hot-query predicates, partition count, and expected archive cadence. A time range or storage release segment may be more appropriate than a product season.

A plausible but unapproved retention direction is detailed relational history for current and recent play, durable compact summaries for older product views, and compressed raw telemetry in lower-cost storage. Exact durations, archive location, historical API detail, and restore tooling remain open. No relational source data should be dropped until an archive can be checksummed, restored, reprocessed, and reconciled against retained facts and authoritative outcomes.

See [[ascent-rivals/initiatives/eventun-foundation/eventun-telemetry-lifecycle-plan|eventun-telemetry-lifecycle-plan]] for the provisional terminology, phases, and decision triggers.

## Index Direction

Exact indexes must follow final query plans. Likely requirements include:

- match-ingest lookup by `(source_kind, session_id, match_id)` if the ledger is added;
- fact lookup by `(session_id, match_id, player_id)`;
- qualifier facts by `(gauntlet_id, player_id, occurred_at)`;
- active membership by player and by team;
- historical membership by `(player_id, joined_at, left_at)`;
- published owner snapshot by `(gauntlet_id, stage, owner_type, rank)`;
- admission slots by `(stage_run_id, owner_type, owner_id, lock_state)`;
- locked occupant uniqueness by `(stage_run_id, player_id)`;
- bracket position by bracket and match;
- queue candidate partial index by status and `available_at`.

Remove redundant indexes only after checking constraints and `pg_stat_user_indexes`. Do not add every plausible index before the finalized read shape exists.

## Performance Plan

### Deployment Baseline

Use PostgreSQL 16.14 on the current Azure B1ms-class deployment, one core and 32 GiB storage, as the implementation baseline until the actual server properties are verified. The low CPU ceiling makes repeated full materialized-view refreshes, broad admission calculations, excess indexes, and high worker concurrency more important concerns than raw storage capacity alone.

The production-launch plan is expected to move to a larger tier. Re-run the representative workload and revise pool, worker, refresh, and latency targets as part of that infrastructure change.

### Current Iteration Dataset

Use a representative dataset based on:

- current expected team counts;
- approximately five or six active members per team;
- realistic event and match volume;
- the largest expected gauntlet field;
- normal concurrent join bursts.

This is the release-relevant benchmark.

### Future Stress Dataset

Separately test larger teams and higher event volume to identify the point where pagination, projection tables, or partition changes become necessary. Do not make thousand-member teams a release gate for this iteration.

### Candidate Targets

| Operation | Candidate database target |
|---|---|
| Stage-run admission point read | p95 below 5 ms |
| Team detail and current roster | p95 below 10 ms |
| Team-filtered roster leaderboard | p95 below 10 ms |
| Published bracket graph | p95 below 10 ms |
| Hot database operations generally | p99 below 16 ms where the deployed tier permits |

These targets exclude network, service serialization, and AccelByte calls.

Collect:

- `EXPLAIN (ANALYZE, BUFFERS, WAL)`;
- `pg_stat_statements` mean, p95 approximation, calls, rows, and block activity;
- table and index size;
- temporary file and sort spill;
- connection-pool saturation;
- worker queue lag and projection freshness when an immediate worker is used;
- transitional materialized-view refresh duration until those views are retired.

Test on PostgreSQL 16.14 with the same extensions, storage class, connection limits, and B1ms resource tier used by the deployed environment.

## PostgreSQL Version Direction

PostgreSQL 16.14 is sufficient for the proposed team and gauntlet schema. Do not make a major-version upgrade a prerequisite.

PostgreSQL 18 has three potentially useful features:

- temporal `WITHOUT OVERLAPS` constraints can express non-overlapping membership intervals directly;
- asynchronous I/O can improve sequential scans, bitmap heap scans, and vacuum;
- partition planning and cost estimation are improved.

These benefits become more relevant after telemetry and partition count grow. On the current one-core tier, provider support, migration effort, and measured workload behavior matter more than adopting a feature early. Reassess PostgreSQL 18 during a planned infrastructure upgrade; do not use the PostgreSQL 19 beta for production work.

## Recommended Migration Order

1. Add the period-neutral identified ingest-batch ledger, unified logical event relation with source/event-type physical partitions, and match-artifact relation after that reset is approved to resume.
2. Update Eventun and the game client to require batch ids, event ids, and producer sequence.
3. Add narrow match, heat, player-result, lap-summary, progression, and qualification contributions keyed to identified sources; keep detailed lap/checkpoint telemetry in source/event-type partitions.
4. Add incremental player/course record, career, and gauntlet-sequence projections; move each product read to its appropriate projection, narrow fact, or batch-local raw path; then remove the legacy duplicated event trees and native materialized-view dependencies while preserving the replacement source/event-type partitions.
5. Add membership intervals and migrate current active memberships.
6. Replace stage placement uniqueness with stage-run scope.
7. Harden generic work claiming, retry, and dead-letter behavior for internal and external work.
8. Add team qualification functions and immutable cutoff snapshots.
9. Add concrete slots, roster locks, owner results, and bracket state.
10. Add team progression ledger and projections only after product definition approval.
11. Retire all player-facing leaderboard and gauntlet dependencies on hourly native materialized views after incremental output and freshness parity.

Pre-alpha status permits direct replacement. Preserve only audit or competition records that product owners explicitly require.

## Open Decisions

| ID | Decision | Working recommendation |
|---|---|---|
| D1 | What is the exact `event_ingest_batch` envelope and conflict response? | Require stable ids and canonical hash; return already accepted for equal content and reject conflicts |
| D2 | Are telemetry corrections append-and-supersede or transactional rewrite-and-rebuild? | Use rewrite-and-rebuild for payload migrations; preserve explicit audit rows for operator corrections to accepted competition outcomes |
| D3 | Is an extension-backed range exclusion constraint acceptable on PostgreSQL 16.14? | Prefer it if `btree_gist` is available; otherwise serialize membership transitions in one function and validate overlaps |
| D4 | Which facts and serving projections are synchronous with complete-match ingest versus projected immediately afterward? | Produce narrow match-final and progression contributions in the accepted-batch transaction; update simple record/career projections transactionally if the measured budget permits, otherwise use an idempotent immediate projector with an explicit freshness target; use workers for expensive goal evaluation and repair |
| D5 | How are product seasons, statistics scopes, storage segments, and retention tiers defined and owned? | Defer implementation; decide each lifecycle independently before seasonal comparison or destructive retention |
| D6 | Should PostgreSQL 18 be adopted during the next infrastructure upgrade? | Reassess using temporal constraints and representative I/O benchmarks; do not upgrade solely for teams |
| D7 | Is team progression seasonal, permanent, or both? | Resolve in the product design before selecting ledger partition and snapshot dimensions |

## Source Index

- [Event table schema](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L3-L113)
- [Event bulk insert](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/events.go#L93-L133)
- [Progression work schema](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L509-L543)
- [Progression work selection](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/progression_worker.go#L76-L101)
- [Progression work failure](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/progression_goal_check_workflow.go#L163-L177)
- [Team membership schema](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L912-L922)
- [Team leave deletion](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/team_api.go#L263-L288)
- [Materialized-view refresh](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/c4_proc_refresh_views.sql#L1-L53)
- [Gauntlet admission query](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/gauntlet_stage_run_api.go#L709-L778)
- [Stage placement schema](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql#L1145-L1156)
- [PostgreSQL materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html)
- [PostgreSQL row locking and `SKIP LOCKED`](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
- [PostgreSQL 16.14 release](https://www.postgresql.org/docs/16/release-16-14.html)
- [PostgreSQL declarative partitioning](https://www.postgresql.org/docs/16/ddl-partitioning.html)
- [PostgreSQL 18 release features](https://www.postgresql.org/docs/18/release-18.html)
