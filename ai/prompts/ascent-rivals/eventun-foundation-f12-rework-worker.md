# Eventun Foundation F12 Rework Coding Worker

> **Archived prompt:** This records the completed F12 worker instructions and must not be executed as current guidance. The former `t0_migration.sql` was deployed and removed; the former `t1_migration.sql` is now stable `migration/migration.sql`. Fixtures use `t0_seed_courses.sql` through `t3_seed_teams.sql`, canonical scheduling uses `d3_schedule_refresh_views.sql`, and disposable delta confirmation is `--confirm-disposable-production-baseline=<target-fingerprint>`. Older filename and hash instructions below are historical verification evidence.

This prompt was used from the existing VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset. Rework only `F12: Rework Narrow Facts And Projection Inputs`, verify it, update its durable task evidence, and stop for review. Do not begin F13 progression workers, F14 serving projections/read cutover, F15 backfill, teams, or game-client work.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the branch, worktree, recent commits, and all current F12 diffs before editing. The first F12 implementation is uncommitted and has been rejected; replace it rather than preserving compatibility with it. Do not reset, discard, stage, commit, or overwrite unrelated owner changes.

Read these Knowledge Base sections before changing code:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F10 through F14
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially `Selective Fact And Serving Layers`
- `10_research/ascent-rivals/eventun-team-postgresql-derivation-review.md`, especially `Target Data Layers`
- `50_knowledge/ascent-rivals/eventun/data-model.md`
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/game-client.md`, especially `Current Identified Telemetry Producer`

## Owner Decisions

- Preserve `event_ingest_batch`, `game_event_identity`, `match_artifact`, and the replacement `game_event` source/event-type partition tree. The existing partitioning and client/server trust distinction are intentional.
- Raw JSONB is immutable audit and detailed telemetry storage. There is no whole-document raw `event_data` GIN to replace.
- Keep only facts that collapse lifecycle rows or establish reusable idempotent contributions.
- Remove the one-row-per-event wide `lap_fact` and `checkpoint_fact`. Detailed lap/checkpoint metrics, coordinates, tags, and experimental fields remain in raw event-type partitions.
- Keep one current fact set per batch. Remove parallel fact revisions and selected-revision joins. Rebuild replaces the current batch facts transactionally.
- Keep native materialized views and current product reads untouched in F12. F14 will add incremental `player_course_record`, career rollup, and gauntlet contribution/best-sequence projections, prove parity, and then remove the hourly views.
- Telemetry payloads do not gain schema-version fields. `t0_migration.sql` remains frozen; all current foundation schema changes belong in canonical SQL and `t1_migration.sql` with exact parity.
- Pre-alpha replacement is intended. Delete rejected F12 machinery instead of adding compatibility branches.

## Required Implementation

1. Replace the current F12 schema with narrow `match_fact`, `heat_fact`, `match_player_fact`, `heat_player_fact`, and `progression_metric_fact` relations.
2. Remove `derivation_revision` from fact keys, SQL function arguments, Go constants/calls, rebuild queries, tests, and documentation. Remove it from `event_ingest_batch` as well unless a concrete repair operation requires a single current-projector marker; do not retain multiple online revisions.
3. Make `rebuild_match_facts(batch_id)` delete and recreate the one current fact graph atomically. Repeating it must produce identical rows without duplicating progression contributions.
4. Keep `source_kind` and stable source identities wherever required for explicit client-reported versus dedicated-server policy. Enforce, or directly contract-test, that each retained source event belongs to the same batch/source and expected event type.
5. Use `MatchStart` as authoritative course context. A course cannot change between heats. If a present heat course field conflicts, reject the batch as malformed rather than deriving multiple course identities.
6. Add nullable `single_player_mode` or equivalent explicit play context to `match_fact`, derived from `MatchStart` when present. Do not infer it from `race_mode`, and do not make it required until the separate game-client producer change is complete.
7. Preserve reported podium state separately from placement policy. Use a nullable `reported_podium_finish` or equally explicit shape. Missing values must remain valid, explicit false must not become true because placement is 1-3, and `podium.count` must preserve current explicit-true behavior.
8. Narrow `heat_player_fact` to current consumers: terminal heat result, player type, proven loadout/value/weight dimensions, and lap summary values. Add valid lap count, total valid lap time, best valid lap time, and winning lap source event id. Derive averages at read time.
9. Inspect the actual Ascent Rivals event structs before defining loadout and medal extraction. Use the real nested `Loadout` slots/augment slots and emitted medal-count shape. Remove synthetic top-level `weaponSku`/`partSku` assumptions and unconsumed typed speed/agility/combat/segment fields.
10. Keep `progression_metric_fact` as the bounded idempotent contribution ledger for the five active inputs. Retain bounded JSONB dimensions if useful, but remove its GIN index unless an implemented F13 containment query already proves it is required.
11. Validate every payload member that F12 casts, or consistently map PostgreSQL data-shape SQLSTATEs to gRPC `InvalidArgument`/HTTP 400. Malformed producer data must not surface as `Internal`; avoid duplicating a field validator across Go and SQL without a clear ownership reason.
12. Keep derivation in the accepted-batch transaction. Do not add triggers, an asynchronous normal-ingest projector, an ORM, repository-per-table wrappers, a migration runner, or generic projection framework.

## Contract And Measurement Evidence

- Replace the 18-event/two-player fixture as performance evidence with deterministic 16-player and 32-player complete matches near the observed production average of 4,681 server events per match. Keep smaller focused fixtures where they improve correctness diagnostics, but do not call them representative.
- Cover server and client source isolation, zero-based identifiers, optional result values, explicit true/false/missing podium values, one course across multiple heats, conflicting course rejection, actual nested loadout/medal payloads, lap aggregate correctness, source provenance, rebuild idempotency, and atomic rollback.
- Compare raw-only ingestion with narrow-fact derivation on disposable PostgreSQL 16.14. Report p50/p95 where the harness reasonably supports it, transaction time, buffers, WAL, heap/TOAST/index bytes, raw and derived rows per match, and peak relation growth. Do not extrapolate from the tiny fixture.
- Demonstrate that the current facts materially reduce rows relative to raw telemetry and that no checkpoint-sized one-to-one duplicate remains.
- Map every retained fact index to an implemented or approved F13/F14 access path. Do not add speculative GIN or overlapping B-tree indexes.

## Verification

Run the coder-owned focused schema/derivation tests and the repository's complete established verification workflow. Do not modify or compile Ascent Rivals in this task. Do not remove current leaderboard/gauntlet materialized views or alter product query behavior. Run formatting and diff checks, preserve the frozen `t0` hash, and verify canonical SQL and `t1_migration.sql` remain equivalent for this block.

## Completion Report

Report:

- the final relations, keys, source-provenance constraints, and indexes;
- every removed rejected-F12 relation, revision path, field, and assumption;
- the exact match/heat/player/progression mapping, including lap aggregation and actual loadout/medal shapes;
- podium, play-context, course, validation, and error behavior;
- rebuild and rollback behavior;
- representative row-count, storage, WAL, buffer, and latency evidence, clearly separating measurements from inference;
- focused and complete verification results;
- all changed files and confirmation that F13, F14, F15, materialized-view removal, game-client work, teams, and unrelated refactors were not started.

Update the F12 task evidence and affected durable Eventun documentation with implemented facts and measured results. Stop for review after F12.
