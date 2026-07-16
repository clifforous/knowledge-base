# Eventun Foundation F14 Recovery Coding Worker

Use this prompt from a coding task attached directly to the Eventun repository. It resumes the interrupted F14 implementation after the approved pre-edit review checkpoint. It is not a request to repeat that checkpoint or redesign the feature.

---

You are recovering and completing the interrupted Ascent Rivals Eventun task `F14: Add Incremental Serving Projections And Cut Over Reads`.

The F14 pre-edit plan, its review corrections, and the final projection-revision amendment below are approved. Treat them as implementation requirements. Briefly audit the existing partial work, then continue implementation and verification. Do not stop for another pre-edit checkpoint unless the live repository proves an approved requirement cannot be implemented safely or two requirements conflict.

Do not begin F15 production backfill or legacy-event cleanup, T00 team-design approval, team membership/history work, team progression, team gauntlets, brackets, Ascentun feature work, or Ascent Rivals game-client work.

## Recovery State

The interrupted VS Code Codex session is locally recorded as session `019f6371-e02c-76c0-82ac-dfced47604d8`. Its rollout log was at:

`/home/cliff/.codex/sessions/2026/07/14/rollout-2026-07-14T18-43-55-019f6371-e02c-76c0-82ac-dfced47604d8.jsonl`

The Eventun worktree is authoritative. Preserve its coherent partial implementation even if that session cannot be resumed. Do not reset, revert wholesale, clean, discard, stage, commit, amend, or overwrite it. Correct a partial implementation only when repository evidence or the accepted requirements justify the change.

At recovery-audit time, Eventun was still at `36c1818c3f9aa96d210075f7097d76a6aebbf13d` with all F14 work unstaged and uncommitted. The partial work included:

- modified accepted-ingestion, Admin, gauntlet API/database/run/stage-run/standings, record, canonical SQL, and protobuf files;
- new `internal/eventun/gauntlet_qualification_admin.go`;
- new `migration/c11_func_serving_projection.sql` and `migration/c12_func_gauntlet_qualification.sql`;
- a first pass of serving schema and projector functions;
- career, leaderboard, match-history, and gauntlet reader conversion work;
- individual qualification preview/publication code and stage-run snapshot binding/admission work.

Known interrupted-session evidence is useful history, not current proof:

- one canonical PostgreSQL 16.14 schema load passed before later SQL edits;
- `go test ./internal/eventun` passed after the last logged Go edits;
- `go test ./internal/eventun ./event` exposed an existing ingestion mock that had not yet been updated for the new synchronous projector call;
- no complete schema, generated-contract, parity, concurrency, repair, migration, performance, or full verification pass was reported.

Known unfinished surfaces at recovery-audit time included at least:

- the ingestion mock expectation and any related focused tests;
- a fresh canonical-schema check after all SQL edits;
- the stable production delta and F15 cutover gate in `migration/migration.sql`;
- retirement of the eight leaderboard materialized views in `b2_view_ranks.sql`, four gauntlet materialized views, refresh procedure, pg_cron schedule, indexes, setup references, and stale operational assumptions;
- remaining insight selection/candidate work, including `c5_func_insight.sql`;
- complete parity, edge, concurrency, repair, schema, migration, query-plan, and performance fixtures/evidence;
- protobuf/Swagger generation and manifest proof if the Admin surface changed;
- final raw-event and retired-object scans;
- durable Knowledge Base updates and the final F14 report.

Re-audit the live diff and session tail before editing because the checkout may have advanced. Do not assume the list above is exhaustive.

## Read First

Read and follow Eventun's nearest `AGENTS.md`. Inspect the branch, index, worktree, recent commits, current migration state, every changed/untracked file, and the interrupted rollout tail before editing. Preserve all owner changes and local-only files.

Read these Knowledge Base sections:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F12 through F15 and the 2026-07-14 migration reconciliation;
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially `Selective Fact And Serving Layers`;
- `10_research/ascent-rivals/eventun-team-postgresql-derivation-review.md`, especially `Layer 4`, `Layer 5`, `Qualification Query Shape`, `Index Direction`, and `Performance Plan`;
- `30_designs/ascent-rivals/teams-solution-design.md`, only for the foundation gate;
- `30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design.md`, especially `Qualification`, `Cutoff And Correction`, and the conceptual operator mutations;
- `50_knowledge/ascent-rivals/eventun/data-model.md`;
- `50_knowledge/ascent-rivals/eventun/api.md`;
- `50_knowledge/ascent-rivals/team-gauntlet-current-state.md`.

Audit every consumer of career, leaderboard, rank, match-history, match-summary, insight, gauntlet list/detail/calendar/stats/standings, cutoff, admission, and stage-run claim data. Audit accepted ingestion, fact rebuild, F13 progression contributions, replay-purge/diagnostic reads, current materialized views, refresh scheduling, schema verification, generation, and production-delta scripts.

## Fixed Boundaries

- PostgreSQL 16.14 and the low-resource one-core production class remain the baseline.
- Keep identified complete-match ingestion, source/event-type `game_event` partitions, one current fact graph per batch, match artifacts, and F13 progression behavior.
- Preserve explicit `client` versus `server` provenance. Never silently merge their authority.
- Preserve `single_player_mode`. Do not infer time trial from `race_mode`, add `competition_period_id`, or introduce seasons/statistics scopes.
- Breaking pre-alpha replacement is intended. Do not preserve compatibility materialized views, duplicate read paths, or periodic refresh as a fallback after parity is accepted.
- Full match summaries, bot rows, player discovery, detailed stage summaries, and detailed insight metrics may remain bounded batch-local raw reads when compact facts do not contain equivalent detail. Document every retained raw read.
- F15 owns production historical fact/projection backfill, validation, rollback/recovery, legacy `server_event`/`client_event` cleanup, remaining `internal/` extraction, and the final release/smoke checklist.
- Do not add an ORM, generic repository framework, migration runner, automatic deploy-time migration, numbered production migration, general projection platform, team owner/membership/attribution data, team scores, competition slots, roster resolution, brackets, or automatic advancement.
- Do not modify or compile Ascent Rivals. Generated-contract verification may prove that Unreal inputs are unchanged.

## Approved Consumer And Authority Matrix

Implement and retain this source policy:

1. `PlayerCareer`/`Players` server lifetime data uses `career_overview`/`player_stats` backed by F14 contributions and player/player-course rollups. Match-level metrics use canonical facts. Individual heat lap, finish, and weight metrics use canonical heat facts. Mutable name, avatar, and team presentation joins at read time.
2. The eight leaderboard output families remain server finish/lap and client finish/lap/high-cost-finish/high-cost-lap/low-cost-finish/low-cost-lap, but read from `player_course_record` instead of materialized views.
3. Match history is server-authoritative and fact/artifact-backed. Its displayed and ordering match time is consistently `match_fact.started_at` (the MatchStart time), ordered descending with a deterministic batch tie-breaker.
4. Full `match_summary` and selected stage summaries may remain bounded batch-local raw reads after fact-backed match selection.
5. `gauntlet_view`, `gauntlet_calendar_view`, and other bounded ordinary list/detail/calendar views may remain. Counts and standings values come from serving projections.
6. Qualifier standings are server-only, do not require canonical matches, exclude known bots, use half-open qualifier windows, and retain the best trailing sequence plus exact selected-match evidence.
7. Overall standings and stats read from gauntlet projections.
8. F15 retains runtime raw phase-check cleanup. Do not pull that cleanup into F14.
9. Time-trial records retain client provenance, require canonical heat data, explicit `TimeTrial`/`single_player_mode`, positive lap time, and placed positive finish time.
10. Time-trial self-history uses facts to select candidates and then bounded raw detail for the selected batch.
11. Post-match current match and baselines may remain bounded batch-local raw. Self-history uses fact-backed selection and bounded raw detail.

Do not use old materialized-view behavior as the sole semantic specification. Preserve the approved filters, null handling, thresholds, deterministic ties, authority policy, and output contracts below.

## Approved Schema And Projection Shape

Complete and validate these ordinary relations and their concrete-query B-tree indexes:

- `match_serving_projection_state`;
- `serving_projection_cutover_state`;
- `player_course_record_contribution` and `player_course_record`;
- `player_career_contribution`, `player_career_rollup`, and `player_course_career_rollup`;
- `gauntlet_projection_state`;
- `gauntlet_player_match_contribution` and `gauntlet_player_stat_rollup`;
- `gauntlet_qualifier_match_contribution`, `gauntlet_qualifier_score_projection`, `gauntlet_qualifier_sequence_match`, and `gauntlet_player_score_projection`;
- immutable/versioned `gauntlet_qualification_snapshot`, `gauntlet_qualification_snapshot_entry`, `gauntlet_qualification_snapshot_qualifier`, and `gauntlet_qualification_snapshot_match` state.

Fact enrichment must retain enough immutable identity for:

- best-lap occurrence;
- the source-matching SessionStart client version;
- the first AscensionStart occurrence;
- deterministic player-type provenance as of match start.

Every contribution is idempotent and retains source batch/fact/event identity needed for deterministic rebuild and audit. Normal accepted ingestion and one-batch repair must update only affected keys, not rescan lifetime history.

## Player/Course Records

Preserve these categories and thresholds exactly:

- server: `finish`, `lap`;
- client: `finish`, `lap`, `high_cost_finish`, `high_cost_lap`, `low_cost_finish`, `low_cost_lap`;
- high-cost loadout value is `<= 10000`;
- low-cost loadout value is `<= 3000`;
- base client categories allow a null loadout value; threshold categories require a non-null qualifying value;
- finish records require canonical, placed, positive finish data;
- lap records require canonical positive lap data.

Retain winning batch, fact/event identity, occurrence time, time, nullable loadout value, match, and heat identities. Equal-time replacement order is deterministic: time, loadout null-last, occurrence time, batch, heat, and event identity. Add the direct top-N index order needed by each course/category query and avoid speculative overlap.

`player_rank` presentation must use the approved loadout-aware ordering. Mutable player/profile/team fields remain read-time presentation rather than immutable performance identity.

## Career Contributions And Rollups

- Reconcile idempotent per-batch/player contributions when facts are changed or rebuilt.
- Store mergeable sums, counts, and minima in player and player/course rollups. Derive averages from sums/counts; never average averages.
- Preserve canonical dedicated-server lifetime policy and the exact `career_overview` JSON/numeric/null/course output contract except for the approved valid-lap correction below.
- Cover every returned field, including kills, deaths, crashes, obelisks, podiums, matches, lap/finish time, play time, weight, circuit points, credits, and any other live output.
- Use `reported_podium_finish`; do not infer podium from placement.
- Course `bestLapTimeMs` remains the minimum `reported_best_lap_time_ms` without adding a positive filter for parity.
- Separately, lap count, sum, average, and play time use only valid positive lap occurrences. This is an approved correction to invalid/non-positive legacy aggregation.

## Match History, Time Trial, And Insight Selection

- Match history reads `match_fact`, `match_player_fact`, and `match_artifact` or an equivalently narrow approved fact snapshot.
- Preserve server authority, limits, session/match identity formatting, replay association, returned player stats, and deterministic `started_at DESC, batch_id` ordering.
- `client_version` comes from the first nonblank source-matching SessionStart at or before MatchStart under deterministic time/batch/sequence/event ordering. `game_build` is diagnostic and does not replace that meaning.
- Time-trial and post-match self-history select candidates from facts, then fetch bounded batch-local raw detail where required.
- Post-match selection retains first AscensionStart time/event identity, and the selected heat end must precede the cutoff.
- Keep current/baseline post-match raw reads bounded and explicitly document them.

## Deterministic Player Type And Bot Policy

Player type freezes as of MatchStart using the latest source-matching PlayerJoin at or before MatchStart, ordered deterministically by time, batch, sequence, and event identity. A known bot is ineligible for qualifier scoring. Missing player type remains eligible/non-bot for parity. Later mutable join events must not rewrite historical eligibility.

## Synchronous Accepted-Batch Projection

The approved update mechanism is explicit synchronous PostgreSQL projection inside the accepted-batch transaction. Do not silently substitute a worker or hidden trigger.

The same transaction resolves facts and applies player/course records, career contributions/rollups, gauntlet contributions/stats/scores/sequence evidence, projection state, and revision changes. Retry, concurrent acceptance, repeated accepted batches, unchanged rebuild, and changed rebuild must be idempotent and atomic.

Performance gates on representative PostgreSQL 16.14 fixtures are:

- added F14 synchronous projection p95 `<= 50 ms` for the representative 5-human/11-bot workload;
- added F14 synchronous projection p95 `<= 75 ms` for the representative 16-human workload;
- total accepted-batch commit p95 `<= 353 ms` and `<= 436 ms`, respectively.

The 32-human case is synthetic stress only. If an approved gate fails, stop and return measurements plus the smallest concrete options for review. Do not introduce an asynchronous worker without approval.

## Gauntlet Contributions, Scores, And Sequences

- `active_qualifier_ids` retains its current contract even though the values are gauntlet IDs; do not silently reinterpret or rename it during F14.
- Accepted contributions are server-only, do not require canonical matches, and exclude known bots. Missing player type is eligible.
- Qualifier windows are half-open. Retain null circuit-points contributions for matches-played and average denominators.
- An all-null qualifier score is unranked and excluded. Use explicit `NULLS LAST` for deterministic ranking.
- A partial leading sequence window is valid. `stat_window` selects the best trailing match sequence.
- `stat_top_k = 0` combines all scored qualifiers; otherwise combine the top K qualifier scores.
- On an in-order match, evaluate only the new ending sequence. A late match, fact rewrite, qualifier/window/configuration change, targeted repair, or full rebuild performs bounded recomputation for affected player/qualifier/gauntlet state.
- Retain exact selected source matches in deterministic sequence order; a total score alone is insufficient.
- Preserve current fields and deterministic tie behavior in qualifier and overall standings.

## Gap-Free Gauntlet Projection Revision Protocol

`gauntlet_projection_state` is keyed by gauntlet and carries `projection_revision`, diagnostics, projector version, and `updated_at`.

Every operation capable of changing gauntlet contributions, rollups, scores, or selected evidence must use one shared transaction protocol, including:

- accepted-batch projection;
- `rebuild_match_serving_projections(batch_id)`;
- `rebuild_match_facts_with_serving(batch_id)`;
- targeted player/qualifier/gauntlet repair;
- qualifier or configuration recomputation;
- full serving rebuild.

For each operation:

1. Determine the union of old and prospective affected gauntlets before mutation. For fact rebuilds, prospective IDs come from immutable batch MatchStart data; old IDs come from current facts and F14 contributions.
2. Acquire the same transaction-scoped gauntlet locks in UUID order, then lock the gauntlet state rows. Competing older open transactions receive the later revision if they acquire the lock later.
3. Stage or fingerprint semantic before/after state, excluding operational timestamps.
4. Apply contributions, stat rollups, qualifier scores, overall scores, and sequence evidence.
5. Increment `projection_revision` exactly once per affected gauntlet whose semantic state changed.
6. Preserve the revision only when contribution, score, rollup, and evidence fingerprints prove an identical no-op.
7. Commit content and revision mutations atomically.

Changed mutable rows record the new revision. A sealed cutoff snapshot records the exact revision used by preview and publication. Configuration changes use the same lock and revision mechanism.

Required races include repair-lock/preview waiting, stale preview publication, proven no-op repair, publication followed by a waiting repair, targeted/full rebuild races, and F13 rejection. Details appear under verification.

## F13-Safe Repair And Rebuild

- `rebuild_match_serving_projections(batch_id)` rebuilds only F14 serving state from current facts. It never reconciles or mutates F13 progression.
- `rebuild_match_facts_with_serving(batch_id)` rebuilds the fact graph and F14 state in one transaction.
- F13's exact deferred consumed-progression foreign-key/invariant remains authoritative. If a changed fact tuple was consumed, the fact rebuild fails; the entire transaction, all F14 mutations, and any provisional revision increment roll back.
- Never delete/cascade/rewrite/compensate progression contributions to force a fact repair through.
- Provide bounded targeted repair and a complete rebuild from current narrow facts. They prepare F15 but do not perform production backfill.

## Individual Qualification Cutoff Contract

F14 cutoff publication supports only a pure individual qualification field. Reject other shapes with `FailedPrecondition`. The supported stage must have:

- an entry requirement based on qualification/qualifier scoring;
- `players_per_team = 0`;
- no teams, groups, win/loss predicates, or team allocation semantics;
- the existing approved server circuit-points policy.

The immutable snapshot replaces only the `playerQualifies` predicate. Live run/session/phase readiness, prior-placement, and capacity checks remain live.

Eligibility at publication:

- when `stat_top_k = 0`, the player needs at least one scored qualifier;
- otherwise the player needs at least `stat_top_k` scored qualifiers;
- order by current overall deterministic ranking and cap at `max_competitors`.

Preview records exact gauntlet projection revision, projector/schema versions, configuration hash, resolution hash, ranked candidates, tie values, qualifier evidence, and exact selected matches.

Publication/replacement acquires the gauntlet lock and requires the live revision, configuration hash, and resolution hash to equal the preview. Otherwise return `FailedPrecondition` and require a new preview.

Snapshot lifecycle and immutability:

- Create draft header and all child rows, validate, and seal in one operator transaction. Do not expose externally durable drafts.
- Snapshot entry primary identity is snapshot/player with unique rank; qualifier identity is snapshot/player/qualifier; match evidence identity is snapshot/player/qualifier/sequence with deterministic evidence uniqueness.
- Child insert/update/delete is allowed only while the parent is draft. Reject every child mutation after seal.
- Header mutation permits only the validated draft-to-sealed transition. Reject all later mutation.
- Initial publication requires no prior sealed version. Replacement identifies the current version and a reason, creates a new version, and references the replaced snapshot. Never mutate a prior version.
- Idempotency is unique on `(gauntlet_id, stage, operation, idempotency_key)`. The same request returns the same result; a different request under the same key returns `AlreadyExists`.

The configuration hash includes source/canonical/bot policy, algorithm, `stat_window`, `stat_top_k`, qualifiers and windows, entry alias, predicates, and capacity. A cutoff-relevant configuration change advances the projection revision and makes an existing snapshot stale for any unbound claim. A replacement snapshot must be explicitly previewed and published.

At stage-run claim, bind one valid sealed snapshot. Admission then requires exact snapshot membership and uses its frozen rank/points. There is no live-score fallback.

Unavailable behavior is exact:

- admission check: `allowed = false`, reason `qualification_cutoff_not_ready`;
- join-status: `joinable = false`, same reason;
- stage-run claim without a valid snapshot: `FailedPrecondition`.

After any run has bound a snapshot, reject cutoff-relevant configuration mutation and cutoff replacement for that target. Freeze is deliberately at stage-run claim rather than MatchStart.

A later accepted batch or repair may advance live projections after publication. It never mutates or automatically deletes the immutable sealed field. For an unbound future claim the old field is stale/not-ready and requires explicit replacement. An already-bound run continues to use its immutable snapshot.

## Canonical Schema And Stable Production Delta

The canonical fresh schema must contain the new F14 schema and no retired materialized views, indexes, refresh procedure, or schedule. Seed `serving_projection_cutover_state` for a fresh database as `fresh_empty` with projector/schema version, counts, manifest SHA, validation time, and state. Do not manufacture `historical_backfill_validated` in a production delta.

F14 and F15 share the stable `migration/migration.sql`; do not create a numbered migration or rewrite historical deployed migration files.

Before production read cutover, unscheduling, or destructive drops, `migration/migration.sql` must require the exact F15 historical-backfill validation marker. If it is absent or mismatched, raise and roll back without partial cutover.

After that gate, the eventual production transition must be quiesced, acquire the advisory lock keyed by `hashtext('refresh_leaderboard_materialized_views')`, revalidate the marker, unschedule refresh, replace reads, drop all twelve materialized views and their indexes plus the refresh procedure, and assert their absence. F15 will complete the validated production marker/backfill portions in this same stable file; F14 must remain safely non-deployable against unvalidated history.

## Approved Intentional Corrections

These are deliberate F14 corrections, not parity failures:

- career average/play-time derives from valid positive lap occurrences;
- record, MatchHistory, SessionStart, sequence, and bot-provenance ties become fully deterministic;
- `player_rank` displayed order is loadout-aware;
- mutable profile/team presentation is joined at read time;
- bot eligibility freezes as of MatchStart;
- individual qualification requires an explicit sealed cutoff snapshot;
- the cutoff field and cutoff-relevant configuration freeze at stage-run claim.

Do not silently add other corrections. Classify any discovered difference as exact parity, an approved correction above, or a new decision requiring review.

## Required Verification And Evidence

The coder owns all implementation verification. Do not treat interrupted-session evidence as final.

1. Create deterministic old-versus-new fixtures before deleting old definitions. Retained parity tests must not require the retired materialized views at runtime.
2. Cover server/client isolation, canonical filtering, explicit time-trial mode, thresholds, null loadouts, equal-time ties, mutable profile presentation, zero/missing values, true/false/missing podium state, match-history time/order/limit/replay/client version, bounded insight selection, and changed/unchanged batch repair.
3. Cover multi-qualifier gauntlets, half-open windows, `stat_window`, `stat_top_k`, null/all-null points, partial leading windows, equal scores, bot/missing-type policy, in-order updates, late matches, rewritten facts, qualifier/config changes, exact sequence evidence, preview/publish/replace, configuration staleness, claim binding, admission, and snapshot immutability.
4. Required concurrency cases:
   - repair holds the lock; preview waits and returns the new revision;
   - preview returns revision `R`; repair commits `R+1`; publication of the old preview fails with `FailedPrecondition`;
   - a proven identical repair preserves `R`, so publication may proceed;
   - publication seals at `R`; a waiting repair commits afterward as `R+1` without changing the snapshot;
   - targeted and full rebuild races exercise the same cases;
   - a repair rejected by F13 leaves progression, projections, contents, and revision unchanged.
5. Prove retry, concurrent acceptance, no-op rebuild, changed rebuild, full rebuild, and targeted repair idempotency and atomicity.
6. Use representative PostgreSQL 16.14 workloads: 5 humans/11 bots and 16 humans across three heats, plus realistic multi-match qualifier history. Label 32 humans synthetic stress.
7. Report old/new row counts, relation/index bytes, WAL, buffers, sort/temp spill, synchronous projection and total commit p50/p95/max, rebuild time, and cold/warm reads. Use `EXPLAIN (ANALYZE, BUFFERS, WAL)` where supported.
8. Run focused Go, SQL contract, parity, concurrency, repair/rebuild, migration, and generation tests while iterating.
9. Run the repository's complete `./scripts/verify.sh`, PostgreSQL 16.14 fresh-schema verification, and guarded authentic production-baseline delta verification.
10. Run focused race tests and vet for touched Go packages, shell syntax checks, and `git diff --check`.
11. If Admin protobuf/Swagger changed, regenerate using the established workflow, update the reviewed manifest, run `./scripts/verify.sh appui`, and prove Unreal Client/GameServer/Models inputs are unchanged.
12. Inspect the complete Eventun and Knowledge Base diffs. Search for every retired materialized-view name, refresh procedure, cron schedule, accidental lifetime raw scan, stale deployment claim, or new period/team/compatibility path.

If Docker/PostgreSQL or another prerequisite is unavailable, report the exact missing evidence and leave F14 incomplete. Do not replace real SQL verification with mocks or claim parity without executing the schema contracts.

## Durable Knowledge Base Updates

Update only existing relevant durable documents with implemented facts and measured evidence:

- the F14 section of `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`;
- `50_knowledge/ascent-rivals/eventun/data-model.md` and `api.md` where serving behavior changes;
- `50_knowledge/ascent-rivals/team-gauntlet-current-state.md` for the materialized-view and individual qualification state;
- foundation/program design only if implementation reveals a required approved-boundary change.

Do not mark F15, T00, or any T/G task complete. Preserve historical measurements and label supersession. Do not cite transient `00_inbox/` content or the crashed chat as durable evidence.

## Completion Report

Before stopping, report:

- how the interrupted work was recovered, the final diff, and any approved-plan deviation;
- final projection, contribution, state, snapshot, evidence, key, identity, index, version, hash, and immutability design;
- synchronous update and revision protocol, performance results, F13-safe repair/rebuild behavior, and no-op handling;
- the complete consumer/authority matrix and every deliberately retained raw read;
- record categories/thresholds/ties, career aggregation, MatchHistory time/client-version behavior, bot policy, insight selection, gauntlet scoring/sequence behavior, and cutoff/claim/admission behavior;
- old/new exact parity, every approved correction, and any unresolved inference;
- representative query plans, latency, ingest cost, WAL, buffers, row counts, and storage;
- every retired materialized view, index, procedure, schedule, setup/script, and operational assumption;
- canonical fresh-schema behavior, guarded production-delta behavior, and the explicit F15 deployment boundary;
- all verification commands and exact results, including generated-contract/manifest proof;
- every changed Eventun and Knowledge Base file;
- confirmation that nothing was staged or committed and that F15, team schemas/features, team gauntlets, brackets, Ascentun, and game-client work were not started.

Stop for review after F14. Do not continue into F15 or T00.
