# Eventun Foundation F14 Coding Worker

Use this prompt from a coding task attached directly to the Eventun repository. This is an active implementation prompt, not historical evidence.

---

You are continuing the Ascent Rivals Eventun foundation reset. Plan, implement, and verify only `F14: Add Incremental Serving Projections And Cut Over Reads`, update its durable Knowledge Base evidence, and stop for review. Do not begin F15 production backfill or legacy-event cleanup, T00 team-design approval, team membership/history work, team progression, team gauntlets, brackets, Ascentun feature work, or Ascent Rivals game-client work.

At prompt preparation time, Eventun `teams` was at `36c1818c3f9aa96d210075f7097d76a6aebbf13d`, synchronized with `origin/teams`. Treat the live checkout as authoritative if it has advanced. Preserve all owner changes and local-only files.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the branch, index, worktree, recent commits, current migration state, and all changed or untracked files before editing. Do not reset, discard, stage, commit, amend, clean, or overwrite unrelated work.

Read these Knowledge Base sections before proposing the implementation:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F12 through F15 and the 2026-07-14 migration reconciliation
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially `Selective Fact And Serving Layers`
- `10_research/ascent-rivals/eventun-team-postgresql-derivation-review.md`, especially `Layer 4`, `Layer 5`, `Qualification Query Shape`, `Index Direction`, and `Performance Plan`
- `30_designs/ascent-rivals/teams-solution-design.md`, only for the foundation gate
- `30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design.md`, especially `Qualification`, `Cutoff And Correction`, and the conceptual operator mutations
- `50_knowledge/ascent-rivals/eventun/data-model.md`
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/team-gauntlet-current-state.md`

Audit the current implementations and every consumer of:

- `career_overview`, `leaderboard`, `player_rank`, `match_history`, and `match_summary`;
- the eight leaderboard materialized views in `migration/b2_view_ranks.sql`;
- the four gauntlet materialized views and every direct or indirect consumer in SQL and Go;
- `refresh_leaderboard_materialized_views`, `d3_schedule_refresh_views.sql`, operational database setup, and schema verification;
- `match_fact`, `match_player_fact`, `heat_fact`, `heat_player_fact`, `match_artifact`, fact rebuild, accepted ingestion, and F13 progression contributions;
- insight, gauntlet runtime, replay-purge, and diagnostic raw-event reads that may intentionally remain.

Do not accept the old materialized views as a complete semantic specification merely because they exist. Record their actual filters, null handling, tie-breakers, source policy, canonical policy, thresholds, and output shape, then compare those rules with the current API and approved design.

## Mandatory Review Checkpoint Before Editing

Do not edit code or SQL until Cliff approves a concise F14 implementation plan. The plan must contain:

1. A consumer matrix for every career, leaderboard, match-history, gauntlet, and insight read. For each consumer, name its current relations, accepted source/canonical policy, output contract, proposed serving source, and whether any raw read deliberately remains.
2. The proposed projection and contribution tables, keys, foreign keys, retained source identities, watermarks, `updated_at` fields, B-tree indexes, rebuild functions, and deletion/reconciliation behavior.
3. The exact record categories and existing loadout-value thresholds that will be preserved. Do not rename or reinterpret the current high-cost/low-cost behavior without an explicit product decision.
4. The update mechanism decision: synchronous in the accepted-batch transaction or an immediate idempotent queue. Support the choice with a measurement plan and an explicit freshness target. Do not choose a worker merely because one already exists.
5. The gauntlet sequence algorithm for in-order matches, late arrivals, rewritten facts, qualifier/configuration changes, deterministic ties, and retained source-match evidence.
6. The exact immutable cutoff publication boundary. Eventun currently has no approved qualifier-cutoff snapshot table or publication RPC. Propose the smallest explicit operator-owned preview/publish/replace contract, telemetry watermark representation, configuration hash, source policy, immutable entry/evidence shape, authorization, and generated-contract impact. Do not invent automatic wall-clock publication.
7. The canonical-schema and `migration/migration.sql` transition order, including how F14 remains testable while F15 still owns production historical backfill and destructive legacy cleanup.
8. The parity, query-plan, concurrency, repair, and performance verification matrix.

Surface weak assumptions at this checkpoint. In particular, do not infer an approved competition period, season, automatic cutoff owner, client-event trust upgrade, or team allocation model. Wait for approval before implementation.

## Fixed Boundaries

- PostgreSQL 16.14 and the low-resource one-core production class remain the baseline. Do not require a major PostgreSQL upgrade.
- Keep identified complete-match ingestion, source/event-type `game_event` partitions, one current fact graph per batch, match artifacts, and F13 progression behavior.
- Preserve explicit `client` versus `server` provenance. Client-reported and dedicated-server facts are not equally authoritative and must never be silently merged.
- Preserve `single_player_mode`. Do not infer time trial from `race_mode`, add `competition_period_id`, or introduce season/statistics-scope behavior.
- Breaking pre-alpha replacement is intended. Do not retain compatibility materialized views, duplicate read paths, or periodic refresh as a hidden fallback after parity is accepted.
- F14 changes serving state and current read implementations. F15 owns production historical conversion/backfill, removal of the legacy `server_event`/`client_event` model, remaining `internal/` extraction, and the final release/smoke checklist.
- Full match summaries, bot rows, player discovery, and detailed insight metrics may remain batch-local raw reads where the compact facts do not contain equivalent detail. Every remaining raw read must be deliberate and documented.
- Do not add an ORM, generic repository framework, migration runner, automatic deploy-time migration, numbered production migrations, or a general-purpose projection platform.

## Required Implementation After Approval

### 1. Add Idempotent Player/Course Record Projections

- Add one ordinary serving row per accepted source, record category, course, and player.
- Preserve the current server finish/lap and client finish/lap/high-cost/low-cost output families and exact thresholds unless the approved plan records an intentional correction.
- Retain the winning batch, fact/event identity, occurrence time, time value, loadout value, and enough match/heat identity to audit and repair the result.
- Make replacement deterministic under equal times, nullable loadout value, repeated ingestion, fact rebuild, and concurrent acceptance. Preserve or explicitly correct existing tie behavior only through the approved plan.
- Add a B-tree order that serves course/category top-N reads directly. Map every index to a concrete query and reject overlapping speculative indexes.
- Join mutable player name/avatar/team presentation at read time unless measurement proves a different reviewed design is required; do not make profile data part of immutable performance identity.

### 2. Add Career Contributions And Rollups

- Add idempotent per-batch/player contribution state sufficient to reconcile current rollups when facts are rebuilt or corrected.
- Add player and player/course rollups containing mergeable sums, counts, and minima. Derive averages at read time rather than incrementally averaging averages.
- Preserve the current canonical dedicated-server career policy and the exact `career_overview` JSON shape, numeric/null behavior, and course breakdown unless the approved parity review identifies and documents a bug correction.
- Cover current kills, deaths, crashes, obelisks, podiums, matches, lap/finish time, play time, weight, circuit points, credits, and any other field actually returned by the current function. Use `reported_podium_finish` semantics; do not derive podium from placement.
- Rebuild or reconcile only affected players/courses. Normal accepted ingestion and one batch repair must not rescan lifetime history globally.

### 3. Move Match-History Lists To Facts

- Move the bounded match-history list to `match_fact`, `match_player_fact`, and `match_artifact` or an equally narrow approved snapshot.
- Preserve ordering, limit behavior, server-authoritative policy, session/match identity formatting, replay association, game-build/client-version semantics, and returned player stats.
- Keep full `match_summary` raw/batch-local where required for bot rows, complete standings, loadouts, and detailed heat presentation. Do not widen compact facts merely to eliminate a bounded raw read.

### 4. Add Incremental Gauntlet Contributions And Best Sequences

- Add one idempotent accepted contribution per server match/player/gauntlet/qualifier with circuit points, trusted occurrence time, source batch/fact identity, and qualifier/configuration identity.
- Preserve current qualifier-window, active-qualifier, canonical/server, and non-bot eligibility semantics. Audit the emitted `active_qualifier_ids` meaning instead of assuming the field name is sufficient.
- Maintain the current best configured trailing sequence and retain the exact selected source matches in deterministic order. Storing only the summed score is insufficient.
- Evaluate only the new trailing window for a normal in-order match. A late arrival, changed current fact, qualifier-window edit, `stat_window` change, or relevant gauntlet configuration change must trigger bounded targeted recomputation for affected player/qualifier state.
- Replace the current gauntlet score/standings materialized views with ordinary projection tables plus bounded views or `STABLE` functions where appropriate. Preserve current output fields and deterministic ranking semantics.
- Implement the approved individual qualifier cutoff preview/publish/replace boundary as immutable, versioned competition state. Retain watermark, configuration hash, source policy, rank, score, tie-break values, and contributing match evidence. Replacement creates a new version and audit relationship; it must not mutate prior published rows.
- Do not add team owners, membership attribution, team top-N scores, competition slots, stage-run roster resolution, brackets, or automatic advancement. Those remain T/G work after T00.

### 5. Make Updates Fresh, Repairable, And Atomic

- Prefer explicit PostgreSQL functions called by accepted ingestion and fact rebuild; do not hide ownership in triggers.
- If the approved measurements keep synchronous work within an acceptable ingest budget, update records, contributions, career rollups, and affected gauntlet state in the acceptance transaction.
- If an immediate projector is approved instead, use a durable idempotent work item with deduplication, watermark, lease token, `SKIP LOCKED`, bounded exponential backoff, maximum attempts, dead-letter state, freshness measurement, and an operator repair/rebuild path. Reuse the proven F13 queue rules without coupling unrelated job semantics.
- Replaying an already accepted batch, concurrent work, or rebuilding an unchanged fact graph must not double-count or change a winner.
- Rebuilding a changed batch must remove its old serving contribution and apply its new contribution atomically for every affected projection.
- Provide complete rebuild and targeted repair operations from current narrow facts. These are required inputs to F15 production backfill but do not perform that production backfill in F14.

### 6. Cut Over Reads And Remove Hourly Materialized Views

- Cut `leaderboard`, `player_rank`, `career_overview`, match-history, gauntlet list/detail/stats/standings, and every other identified materialized-view consumer to the approved projections or bounded functions.
- Preserve public protobuf/HTTP response contracts unless the approved cutoff Admin contract adds explicitly reviewed operations. Do not redesign player APIs or website/game-client flows.
- Compare old and new outputs before deletion. Explain every intentional difference; do not normalize away nulls, ties, profile freshness, bot exclusion, or source policy silently.
- After output, freshness, rebuild, and query-plan parity pass, remove all eight leaderboard and four gauntlet native materialized views, their indexes, `refresh_leaderboard_materialized_views`, the obsolete hourly pg_cron schedule, and all operational/test/documentation assumptions that refresh them.
- Preserve `gauntlet_view`, `gauntlet_calendar_view`, and other ordinary views that still have clear bounded ownership.
- Audit final raw-event reads. Leave only batch-local, diagnostic, operational, or explicitly F15-deferred consumers, and list each one with its reason.

### 7. Preserve The Manual SQL Lifecycle

- Update canonical `a*`/`b*`/`c*`/`d*` SQL according to Eventun's repository rules.
- Put the one-time transition from the deployed production baseline in stable `migration/migration.sql`. Do not create a numbered migration or modify historical/deployed files.
- Remove `d3_schedule_refresh_views.sql` and its setup references if no scheduled refresh remains; do not retain a misleading empty schedule file. Confirm the remaining `d*` sequence and database scripts are coherent.
- Keep the pending delta executable and parity-checked against an authentic disposable production-baseline copy through the existing guarded command. Do not apply it to production.
- Record clearly that F14 code/schema cutover is not independently deployable until F15 supplies historical fact/projection backfill, validation, rollback/recovery, and final cleanup.

## Required Evidence

- Create deterministic old-versus-new parity fixtures before deleting the old view definitions. The retained test must not require production materialized views at runtime.
- Cover server/client isolation, canonical filtering, time-trial `single_player_mode`, high/low loadout thresholds, null loadouts, equal-time ties, profile changes, zero/missing values, explicit true/false/missing podium state, match-history ordering/limit/replay association, and batch repair.
- Cover multi-qualifier gauntlets, `stat_window`, `stat_top_k`, equal-score ties, bot exclusion, in-order incremental updates, late matches, rewritten facts, qualifier/config changes, selected-source evidence, cutoff preview/publication/replacement, immutability, and concurrent publication.
- Prove accepted-batch retry, concurrent processing, unchanged rebuild, changed rebuild, full projection rebuild, and targeted repair are idempotent.
- Use the established PostgreSQL 16.14 representative 5-human/11-bot and 16-human three-heat workloads, with the 32-human case labeled synthetic stress only. Add realistic multi-match qualifier history rather than using a tiny fixture as performance evidence.
- Report old/new row counts, relation and index bytes, WAL, buffers, sort/temp spill, synchronous ingest cost or queue freshness/lag, rebuild time, and cold/warm read latency. Use `EXPLAIN (ANALYZE, BUFFERS, WAL)` for representative reads and updates where supported.
- Compare every player-facing and gauntlet output. Separate exact parity, intentional corrections, and inference.

## Verification

The coder owns verification for this implementation.

1. Run focused Go, SQL contract, concurrency, rebuild, migration, and parity tests while iterating.
2. Run the repository's complete `./scripts/verify.sh` workflow and the established PostgreSQL 16.14 schema/production-delta verification workflow.
3. Run focused race tests and vet for the touched Go packages.
4. If the approved cutoff contract changes protobuf/Admin Swagger, regenerate through the established workflow, update the reviewed manifest, run `./scripts/verify.sh appui`, and prove Unreal Client/GameServer/Models inputs are unchanged. Do not modify or compile Ascent Rivals.
5. If Docker/PostgreSQL prerequisites are unavailable, report the missing evidence and leave F14 incomplete. Do not substitute mocked SQL or claim parity without executing the real schema contracts.
6. Run shell syntax checks and `git diff --check`. Inspect the complete Eventun and Knowledge Base diffs. Do not stage or commit.
7. Search the final tree for the twelve retired materialized-view names, refresh procedure, pg_cron schedule, accidental lifetime raw scans, stale production-deploy claims, and any new period/team/compatibility path.

Do not independently rerun game-client builds or tests. This task does not modify the game client.

## Durable Updates

Update only the existing relevant Knowledge Base documents with implemented facts and measured evidence:

- the F14 section of `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`;
- `50_knowledge/ascent-rivals/eventun/data-model.md` and `api.md` where current serving behavior changes;
- `50_knowledge/ascent-rivals/team-gauntlet-current-state.md` for the materialized-view and individual qualification state;
- the foundation/program design only if implementation changes an approved boundary.

Do not mark F15, T00, or any T/G task complete. Preserve historical evidence and label supersession rather than rewriting past measurements as though they used the new schema.

## Completion Report

Before stopping, report:

- the approved pre-edit plan and any deviations;
- final projection/contribution/snapshot relations, keys, identities, watermarks, indexes, and immutability rules;
- the update mechanism, freshness contract, retry/repair/rebuild behavior, and changed-batch reconciliation;
- the complete consumer/source-policy matrix and every deliberately retained raw read;
- record categories, thresholds, ties, career aggregation, match-history, gauntlet sequence, and cutoff behavior;
- exact old/new output parity and intentional corrections;
- representative query plans, latency, ingest/update cost, freshness, WAL, buffer, row-count, and storage evidence;
- all removed materialized-view, refresh, schedule, script, and operational paths;
- canonical and production-delta migration behavior plus the explicit F15 deployment boundary;
- focused and complete verification commands and results;
- every changed file and confirmation that F15, team schemas/features, team gauntlets, brackets, Ascentun features, and game-client work were not started;
- confirmation that nothing was staged or committed.

Stop for review after F14. Do not continue into F15 or T00.
