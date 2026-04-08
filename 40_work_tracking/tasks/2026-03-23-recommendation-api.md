# 2026-03-23 Recommendation API — Implementation Complete

**Status:** Done
**Project:** Ascent Rivals / Eventun
**Repository:** https://github.com/ikigai-github/eventun
**Design references:**
- `30_designs/ascent-rivals/recommendation-api-engineering-design.md`
- `30_designs/ascent-rivals/match-summary-time-trial-improvement-metrics.md`

---

## V1 Scope

- [x] Separate HTTP routes for time-trial and post-match recommendations
- [x] Common backend pipeline behind both routes
- [x] Synchronous generation for v1
- [x] Normal gRPC/HTTP status codes for invalid, missing, or incomplete runs
- [x] At most 3 recommendations per response
- [x] Telemetry-backed categories only in v1; economy/loadout deferred

## Implementation Notes

- [x] Thin handler: validate → load snapshot → score in Go → map to protobuf
- [x] Heavier aggregation kept in SQL functions; scoring and weighting kept in Go
- [x] JSONB-packed snapshot functions reduce Go-side fan-out to one query per mode
- [x] Heat-aware post-match selection; lobby and self-history comparators are heat-indexed
- [x] V1 categories:
  - time trial: `route_choice_shortcuts`, `corner_speed`, `straightaway_speed`, `warp_usage`, `strafes_used`, `energy_management`, `stall_time`, `overall_speed`
  - post-match: `route_choice_shortcuts`, `corner_speed`, `straightaway_speed`, `warp_usage`, `strafes_used`, `kills`, `deaths`, `crashes`

## Reviewer Notes

- [x] Pipeline split: SQL for shaping/aggregation, Go loaders for snapshots, Go scoring for deviation/weighting/suppression/role
- [x] Time-trial scoring: self-history on same course, course record finish, course record lap
- [x] Post-match scoring: lobby average, lobby leader (when player is not leader), same-heat player history
- [x] Segment categories driven by `PlayerCheckpoint.tags`; `shortcut`, `corner`, `straight`, `slotted` in use
- [x] Post-match segment categories use same-heat self-history only; lobby segment baselines deferred
- [x] Real-match metrics filtered to pre-ascension data inside SQL

## Code Review Findings — All Resolved

### Bugs Fixed

- [x] **SQL syntax error (`c6_func_recommendation_metrics.sql:338`)** — stray `bun` artifact removed; `recommendation_post_match_metrics` function was undeployable
- [x] **Misleading `NotFound` for courses with no records** — `recommendation_time_trial_records` now returns JSONB via `(SELECT 1) AS seed LEFT JOIN` pattern, guaranteeing exactly one row; zero-records case no longer masquerades as run-not-found
- [x] **NULL scan on partial course records** — JSONB approach with null-object detection replaces flat 12-column scan; missing benchmark runs cleanly decode as `nil`

### Correctness Fixed

- [x] **Post-match self-history included DNF runs** — `recommendation_post_match_histories` now filters `doneReason = 'Placed'`, matching time-trial behavior; DNF zero-time rows no longer pollute history distributions
- [x] **Zero-time fallback to index 0** — `buildBestFinishProfile` / `buildBestLapProfile` now return `false` when no positive-time entry exists instead of silently using index 0
- [x] **Double-scoring in heat candidate selection** — `buildPostMatchHeatCandidates` and `buildPostMatchSegmentCandidates` now return `[]*recommendationCandidate`; `computePostMatchRecommendations` scores all candidates in one pass; `keepBestRecommendationPerCategory` deduplicates afterward
- [x] **Inconsistent benchmark basis** — `calculateObservationDeviation` no longer overwrites `BenchmarkValue`; primary and supporting metrics both use arithmetic mean consistently for distribution observations

### Statistical Accuracy Fixed

- [x] **Population std dev on small samples** — `standardDeviation` now divides by `N-1` (Bessel's correction); with default sample count of 3, the correction is material (~22%)

### Database Chatter Reduced

- [x] **Ascension cutoff queried three times per request** — `recommendation_post_match_metrics` now accepts `_ascension_cutoff TIMESTAMPTZ` directly; `queryPostMatchRecommendationSnapshot` passes `run.AscensionStartTime`; history runs derive their own cutoffs via lateral join inside the snapshot SQL
- [x] **Per-heat serial queries** — replaced by `recommendation_post_match_baselines` and `recommendation_post_match_histories`, both returning JSONB aggregated across all heats; post-match snapshot now does two benchmark round trips instead of two per heat
- [x] **N+1 time-trial metric queries** — replaced by `recommendation_time_trial_snapshot`, a single JSONB function that deduplicates requested runs via `UNION` before materializing metric rows

### Simplification

- [x] **12-column flat scan** — replaced with JSONB payload; positional coupling eliminated; null benchmarks decode naturally
- [x] **`heatMetrics` map parameter** — moved inside `buildPostMatchHeatCandidates`; callsites simplified
- [x] **No-primary response intent** — comment added to `selectFinalRecommendations`; "zero primary" case is intentional when no candidate clears both the priority and confidence thresholds

### Residual Minor Issue

- The `ZScore` in `RunRecommendationEvidence` is computed against the median (or mean when sample < 5); the displayed `BenchmarkValue` in the metric proto uses arithmetic mean. These don't correspond exactly for distribution observations. Scoring correctness is unaffected; only debuggability from the client side is slightly impaired. A `BenchmarkBasis` field on `RunRecommendationEvidence` would fully resolve this if it becomes a problem.

## Phase 0: Inputs and Boundaries — Confirmed

- [x] Time trial uses `client_*` events; real match uses `server_*` events
- [x] Mode detected from `SessionStart.singlePlayerMode = TimeTrial`; `MatchStart.raceMode` alone is insufficient
- [x] Human-vs-bot filtering deferred; minimum-human-player filter reserved for later tuning
- [x] `PlayerCheckpoint.event_data.tags` array assumed; initial vocabulary: `corner`, `canyon`, `shortcut`, `straight`, `objective`, `slotted`
- [x] Tags describe the previous segment, not the upcoming segment
- [x] `AscensionStart` is the canonical race-phase cutoff
- [x] `timeInCombatModeMs` on both `PlayerCheckpoint` and `PlayerLap`; not yet in production payloads
- [x] Human `Player*` events carry `player_id`; bot events may omit it
- [x] Self-history threshold default `3`, tunable
- [x] Separate HTTP routes for time-trial and post-match; path-parameter based

## Phase 1: API Contract — Done

- [x] Protobuf messages added: `RunRecommendationRole`, `RunRecommendationCategory`, `RunRecommendationComparatorType`, `RunRecommendationMetric`, `RunRecommendationLocation`, `RunRecommendationEvidence`, `RunRecommendation`, `RunRecommendationsRequest`, `RunRecommendationsResponse`
- [x] RPCs added to `ClientService`: `TimeTrialRecommendations`, `PostMatchRecommendations`
- [x] grpc-gateway annotations added; messages kept in `match.proto`
- [x] Code generation run; project builds

## Phase 2: Query Primitives — Done

- [x] Run context query: mode, player_id, session_id, match_id → course_code, race_mode, heats, laps, participation flags, ascension time
- [x] Ascension cutoff function: `recommendation_post_match_cutoff`; reused by snapshot SQL
- [x] Time-trial comparators: self-history, record best lap, record best finish
- [x] Post-match comparators: lobby average, lobby leader (when not self), same-heat player history
- [x] Per-run metric aggregates: checkpoint, lap, heat, match levels; pre-ascension filter for real matches

## Phase 3: Data — Done

- [x] Best-run identity preserved in `recommendation_time_trial_records` JSONB output
- [x] First-pass indexes added: player checkpoint, lap, heat-end, match-end, session-start, match-start, ascension-start, heat-start, player-heat-start (both client and server tables where applicable)

## Phase 4: Go Recommendation Domain — Done

- [x] Internal types: run context, benchmarks, metrics, candidates, scored candidates
- [x] Snapshot loaders: `loadTimeTrialRecommendationSnapshot`, `loadPostMatchRecommendationSnapshot`
- [x] All v1 categories implemented with category weights, comparator weights, and confidence modifiers
- [x] Deviation scoring: robust z-score (MAD, n≥5), standard z-score (n≥3), percent-difference fallback
- [x] Suppression: `suppressBroadOverallSpeed`, `keepBestRecommendationPerCategory`, priority floors
- [x] Role assignment: primary (high score + confidence), secondary (above floor), silent drop (below floor)

## Phase 5: Handler Wiring — Done

- [x] `TimeTrialRecommendations` and `PostMatchRecommendations` handlers in `internal/eventun/client.go`
- [x] Validation: player_id, session_id, match_id (non-negative), max_recommendations clamped to 3
- [x] Files: `recommendation_api.go`, `recommendation_db.go`, `recommendation_builders.go`, `recommendation_metrics_db.go`, `recommendation_scoring.go`, `recommendation_snapshot_db.go`
- [x] Response mapped directly to protobuf; errors use normal gRPC status codes

## Open Items Deferred Beyond V1

- Exact segment-by-segment comparison against a canonical best run
- Debug/explain endpoint for suppressed candidates
- Part-change attribution summaries
- Purchase timing and part-taxonomy recommendations
- Cost-bracket or cohort-based recommendation logic
- Materialized/async recommendation generation
- Lobby-average and lobby-leader baselines for tag-driven segment categories in real matches
- Fallback logic when `AscensionStart` event is absent
- Full lobby participant set as a comparator
- Checkpoint-range location precision (currently resolves to heat + lap + segment tags)
- Profile and add course/player history indexes once query patterns are observable in production
- Split `recommendation_scoring.go` into smaller files; current readability is medium
- Runtime validation of SQL functions against a real database
- Unit and integration tests for scoring, suppression, role assignment, and query behavior
