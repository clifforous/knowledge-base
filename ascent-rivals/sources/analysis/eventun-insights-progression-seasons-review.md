# Eventun Insights, Progression, And Seasons Review

**Status:** F16A initial season implementation, its one combined local rehearsal, and retained-data API/performance smoke are complete; the migrated rehearsal database and resettable snapshot are retained, while development cutover remains pending. F16B retention decisions remain open.
**Date:** 2026-07-18
**Original reviewed repository:** [Eventun](https://github.com/ikigai-github/eventun) at [`5aaaea2f4991f19e69b1d9bad90e5208fb1d4994`](https://github.com/ikigai-github/eventun/commit/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994)
**Implementation reconciled through:** [`37c030791720e8b4a10958b2d2dcecec227473aa`](https://github.com/ikigai-github/eventun/commit/37c030791720e8b4a10958b2d2dcecec227473aa)

## Related

- [[eventun-foundation-api-simplification-review]]
- [[ascent-rivals/archive/initiatives/post-match-insights/eventun-post-match-insights-solution-design]]
- [[ascent-rivals/initiatives/post-match-insights/eventun-post-match-insights-next-phase-ideation-notes]]
- [[ascent-rivals/archive/initiatives/eventun-progression/eventun-medals-progression-goals-challenges-rewards-solution-design]]
- [[ascent-rivals/initiatives/eventun-progression/eventun-progression-next-phase-ideation-notes]]
- [[ascent-rivals/initiatives/eventun-foundation/eventun-telemetry-lifecycle-plan]]
- [[ascent-rivals/decisions/README|Ascent Rivals decision log]]

## Purpose

Record an adversarial review of Eventun's insight ranking and progression goal model, then re-triage the findings between immediate foundation work and later insight or progression iterations. Reconsider the previously deferred season decision now that seasons are expected to bound some player statistics, progression, gauntlets, queries, and historical data lifecycles.

This document began as a review rather than an implementation plan. The accepted
F16A checkpoint and implementation closure below now record the approved initial
season contract and its evidence. They do not select a physical partition or
retention strategy; those decisions remain F16B work.

## Executive Assessment

The insight implementation has a reasonable high-level boundary: Eventun owns candidate generation, credibility gates, ranking, and suppression; the client owns localized presentation. The current score units and benchmark semantics are not reliable enough to treat all enabled candidates as legitimate recommendations. Score and evidence correctness should be repaired before expanding the catalog.

The progression fact ledger, contribution identity, counters, immutable published goals, and completion history are a sound V1 foundation for additive goals. The current metric model is not a general achievement engine, but it does not need to become one during the current foundation phase if V1 remains explicitly limited to additive counters. Reducers, same-occurrence predicates, distinct counts, streaks, and goal-check scaling belong in the next progression/goals iteration before those achievement shapes are authored.

Seasons should be reopened as a foundational design concern. The near-term need is a logical season model and deterministic attribution policy. Physical telemetry partitioning, archive format, and destructive retention must remain separate, evidence-driven decisions. A product season may be a useful archive or partition boundary, but it must not become the physical storage key merely because it is a convenient player-facing calendar.

## Triage

### Immediate Foundation Corrections

1. Correct insight signal units and ranking thresholds so policy values mean what the admin UI says they mean.
2. Preserve missing insight metrics as absent rather than zero and prevent candidates from claiming comparator types they did not use.
3. Remove or clearly quarantine inert insight policy controls until their runtime behavior exists.
4. Define season semantics, ownership, attribution, and affected data families before approving a season schema or retention coupling.
5. Decide whether the logical season model should be included in the pending historical backfill and development cutover. Do not make this sequencing choice implicitly.

### Next Insights Iteration

1. Persist selected-insight delivery history with ranker version and immutable policy revision.
2. Implement cooldown from delivery history or remove it from policy.
3. Replace the current confidence heuristic with a typed evidence-quality model.
4. Increase comparable self-history depth and add distribution data such as median and dispersion.
5. Add leave-one-out cohort construction and minimum cohort-population rules.
6. Replace positional floating-point candidate arguments with named evidence components and split candidate generation by domain.
7. Add sampled or durable outcome evaluation so tuning can measure whether selected coaching correlates with later improvement.

### Next Progression/Goals Iteration

1. Add explicit metric reducer semantics rather than treating every numeric metric as an additive counter.
2. Support bounded same-heat, same-match, or same-run qualifying conditions for correlated achievements.
3. Consolidate the metric registry so a new metric does not require duplicated catalog edits across schema, seed SQL, fact constraints, derivation SQL, and Go validation.
4. Add goal-to-metric dependency projections and evaluate only goals affected by changed metrics.
5. Add distinct-count, streak, ratio, and minimum-sample capabilities only when concrete authored goals require them.
6. Keep prerequisite, hidden, tiered, and repeatable achievement lifecycle behavior separate from metric aggregation.

## Insight Findings

### P1: Signal Thresholds Use The Wrong Scale

The admin surface presents `min_effect_size` as a percentage-like minimum observed gap. Candidate generation transforms a positive relative gap with `0.65 + effect`, clamps the result as high as `1.5`, and compares that transformed score to policy defaults such as `0.05` and `0.10`.

Consequences:

- a one-percent gap becomes approximately `0.66`, not `0.01`;
- the default signal gates accept nearly every generated positive gap;
- the documented 0.0-1.0 component scale is not the implemented scale;
- the `0.35` primary salience floor is lower than many near-zero-gap candidate scores; and
- an operator cannot infer behavior from the values shown in the UI.

Recommendation:

- retain a raw `relative_gap` or well-defined `signal_magnitude`;
- compare `minimum_relative_gap` in the same units;
- normalize every rank component to an explicit bounded range; and
- use an explainable weighted score with typed component output rather than an opaque multiplication of mismatched scales.

### P1: Some Benchmark Labels Do Not Describe The Evidence

Current examples include:

- missing energy and stall telemetry becoming zero before historical averaging;
- energy or stall coaching comparing a present current value with zero-filled historical rows;
- `consistent_laps` reporting a recent-runs benchmark while using a threshold derived only from the current run; and
- `objective_standout` reporting a high-CP cohort while comparing the player with a literal zero benchmark.

This is more serious than weak tuning. The response can describe evidence that was not actually used.

Recommendation:

- preserve presence independently from numeric value;
- require real player and comparator observations for comparator-backed candidates;
- derive benchmark type from the selected benchmark object rather than assigning it at the call site; and
- distinguish an authored threshold from player history, lobby average, leader, record, and cohort benchmarks.

### P1: Policy Contains Inert Controls

`min_required_samples`, confidence-weight JSON, benchmark-weight JSON, cooldown runs, per-insight maximum per response, and row scoring version do not affect selection. Mode weight is also a stub that always returns `1.0`.

Recommendation:

- remove unused controls until implemented;
- represent the code algorithm as `ranker_version`;
- represent every policy change with an immutable policy-set revision; and
- do not expose cooldown until selected insight delivery is stored durably enough to enforce it.

### P2: Confidence Is An Evidence Heuristic

Confidence currently comes mainly from sample-count buckets plus a bonus for larger effects. Three recent samples are loaded by default. The model does not incorporate metric presence, comparator variance, course or ruleset comparability, schema continuity, recency decay, or source trust in a consistent way.

Use `evidence_quality` terminology until a stronger model exists. More raw telemetry is not the primary need. Better presence, provenance, comparable sample selection, distribution statistics, and delivery/outcome history are more important.

### P2: Candidate Construction Is Hard To Audit

Candidate helpers accept adjacent positional floating-point values for effect, outcome relevance, benchmark relevance, and confidence. Repeated literal sequences such as `0.85, 0.75` are difficult to interpret and easy to transpose.

Use a named evidence value object, for example:

```text
signal_magnitude
comparator_quality
outcome_link_strength
evidence_quality
comparator_sample_count
```

Keep factual kudos, pace/control coaching, combat, and economy/build candidates in separate modules with a common candidate contract.

## Insight Naming Recommendation

| Current name | Assessment | Recommended direction |
|---|---|---|
| `BaseWeight` / Weight | Mostly understandable; `base` implies another weight that does not exist | `RankingWeight`; UI `Ranking weight` |
| `EffectSizeScore` / Signal | Misleading because the value is transformed and not a percentage | Raw `RelativeGap` or bounded `SignalMagnitude` |
| `MinEffectSize` | Does not operate in the units presented to operators | `MinimumRelativeGap` |
| `BenchmarkRelevance` | Conflates trust and applicability | `ComparatorQuality` |
| `OutcomeRelevance` | Does not say whether this is correlation, causality, or product importance | `OutcomeLinkStrength` |
| `ConfidenceScore` | Overstates the statistical meaning | `EvidenceQualityScore` |
| `PrimarySalienceFloor` | Technical and tied to an unclear score scale | `MinimumPrimaryPriority` |
| `SecondarySalienceFloor` | Same issue | `MinimumSecondaryPriority` |
| `MinBenchmarkSampleCount` | Reasonably clear | UI `Minimum comparator samples` |
| `MinRequiredSamples` | Ambiguous and unused | Remove |
| `ConfidenceWeightsJSON` / `BenchmarkWeightsJSON` | Opaque and unused | Remove; add typed policy only if needed |
| `ScoringVersion` | Confuses code algorithm with mutable policy | Split into `RankerVersion` and `PolicyRevision` |

## Legitimate Insight Boundary

The current system can produce useful descriptive insights, but not every descriptive difference supports a recommendation.

| Insight family | Current confidence in legitimacy | Required treatment |
|---|---|---|
| Winner, podium, and other direct result kudos | High when source facts are present | Keep factual and avoid invented comparator language |
| Direct time, lap, and tagged-segment gaps | Moderate to high | Require real comparable benchmark and presence |
| Self-history consistency and behavior | Moderate to low with three samples | Increase history depth and show sample/dispersion evidence |
| Combat and objective standout | Low to moderate | Use actual lobby/cohort distributions and contextual thresholds |
| Energy and stall coaching | Low while missing values become zero | Disable or repair presence semantics first |
| Economy and loadout coaching | Experimental | Use same-heat leave-one-out cohorts and avoid causal build claims |
| Build-shape coaching | Experimental and appropriately disabled | Require observed symptom plus validated relationship to outcome |

Player-facing copy should state the observation it can prove. For example, `corner speed was lower than your comparable recent runs` is narrower and more defensible than prescribing a build change.

## Progression Findings

### Current Strengths

- Stable source batch and event identity support replayable contributions.
- The contribution ledger makes counter application idempotent.
- Counters are rebuildable rather than authoritative source history.
- Goal requirements are validated bounded JSON rather than executable SQL.
- Published goal snapshots and completion history preserve historical meaning.
- Achievements, masteries, and challenges share a coherent definition model.

### Current Boundary

The implemented progression pipeline accepts positive integer facts and sums them. That supports additive goals with dimension filters and simple root `all` or `any` composition.

It does not support:

| Achievement shape | Needed capability |
|---|---|
| Finish or lap under a target time | `min`/best reducer with absent-not-zero semantics |
| Win under a target time | Same-match correlated qualification |
| Complete a heat without crashing or dying | Same-heat qualifying occurrence |
| Use N distinct weapons or courses | Distinct-count state |
| Win N consecutive matches | Ordered streak state |
| Average fewer than X crashes after N heats | Sum, denominator, and minimum sample count |

These limitations do not need to block the current foundation if the product accepts an explicitly count-only V1. They become blocking before the next progression iteration authors core racing-time, clean-run, distinct-use, streak, or average-based goals.

### Recommended Next Model

Keep counters as one reducer within a broader metric-state model. Add two bounded requirement families:

1. Aggregate metric requirements using code-owned reducers such as `count`, `sum`, `min`, `max`, and later `distinct_count` or `streak`.
2. Qualified-occurrence requirements that evaluate allowed fields within one code-owned heat, match, or run observation before incrementing progress.

Do not introduce arbitrary SQL, general scripts, or an unbounded expression language. Root `all`/`any`, metric-specific matcher families, and validated observation schemas cover the expected use cases without creating a generic rules platform.

### Goal-Check Scalability

Each career job currently loads every incomplete career goal and every player counter, then scans the counter collection for each leaf. That is acceptable for a small catalog but scales with all goals and all dimension combinations, even when one match changed only a few metrics.

During the next progression iteration, derive goal-to-metric dependencies at publish time, carry changed metric codes in check work, and index loaded state by metric, policy, and dimensions.

## Season Direction

### Delivery Sequence

The representative read-only baseline, focused season design, and additive
implementation were completed without assigning converted facts. The single
allowed combined historical-and-season local cutover then committed
successfully. Its migrated database and resettable snapshot are retained, and
the local API smoke matrix completed against that retained state. Development
still awaits the combined event/season cutover. No second production-scale
rehearsal is authorized during this correction pass; a production rehearsal is
refreshed later against the final release delta and a current dump.

### Working Definition

A season is a named Eventun product time window owned by Eventun. It commonly coincides with new content or a client release, but it is not identified by a client build and is not required to begin or end with one. An off-season is still an explicit season window.

This definition implies:

- every relevant instant resolves to at most one explicit season;
- gaps are valid and matches in a gap are unseasoned rather than rejected or assigned to a moving implicit season;
- game builds and seasons remain separate attributes;
- one season may contain multiple builds and one build may appear in more than one season; and
- competitions, challenge periods, and gauntlets may reference a season without becoming the season itself.

### Implemented Minimal Season Entity

The initial implementation uses the smallest useful entity:

| Field | Purpose |
|---|---|
| `season_id` | Stable immutable UUID database/API identity |
| `title` | Mutable, non-unique player/operator display title of 1–128 Unicode characters |
| `starts_at` | Inclusive finite UTC boundary aligned exactly to Unix milliseconds |
| `ends_at` | Exclusive finite UTC boundary aligned exactly to Unix milliseconds |
| `kind` | `regular` or `off_season` |
| `created_at` | Operational creation timestamp |
| `updated_at` | Operational update timestamp |

There is no human-readable season code in the initial model, and title is never
an identifier. Such a code is deferred until a concrete integration, import,
configuration, or operator workflow requires it. Avoid draft, published, or
independently mutable `active` state. A stored season is authoritative, and
current/upcoming/past state is derived from its half-open window. Eventun's
Extend App UI owns simple season creation, listing, future-unused
editing/deletion, and cosmetic title editing. Referenced kind and bounds freeze;
title remains mutable with the accepted last-writer-wins behavior.

Season splitting and reassignment between existing seasons are low-priority recovery considerations, not part of the initial implementation. General telemetry defects are repaired through fact/contribution repair and projection rebuilds rather than by manufacturing season boundaries. For example, an invalid ultra-low finish caused by treating an early heat exit as a completed race requires correction of the faulty semantic fact and its derived records.

### Attribution Recommendation

The implemented policy is:

- Eventun resolves season identity; producers do not submit a season id.
- A dedicated-server fact resolves once from the authoritative MatchStart instant using `starts_at <= match_started_at < ends_at`.
- A client fact is season-attribution eligible only when MatchStart and trusted batch receipt resolve to the same non-null season. Otherwise it remains unseasoned while retaining lifetime behavior.
- A match crossing a season boundary remains wholly in the season in which it started.
- This is season-attribution eligibility, not anti-cheat or result validation. It deliberately revises the prior occurrence-time-only late-arrival statement.
- The compact `match_fact` stores the resolved nullable season id as canonical acceptance-time semantic evidence. Raw events and `match_player_fact` do not copy it.
- Ordinary fact repair requires a prior fact and preserves its exact null or non-null attribution rather than resolving the current catalog again.
- Historical conversion uses a narrow intention-specific derivation entry point that derives null attribution directly.

Eventun accepts a match with no covering season as unseasoned. It still contributes to lifetime statistics and match history but not season-scoped records. The initial administration surface does not split an existing season or move matches from one season to another. A later narrowly bounded recovery may allow a newly created non-overlapping season to claim previously unseasoned matches, but that behavior requires a separate reviewed repair contract and is not implicit in ordinary creation.

The current fact model deliberately keeps each accepted client or server batch
as an independent observation. Server-derived surfaces use server facts, while
client-only time-trial surfaces use the player's client fact; client timing
cannot reclassify a server-derived result. Season implementation does not
introduce a separate cross-source logical-match canonicalization subsystem.

### Season Versus Related Concepts

| Concept | Relationship to season |
|---|---|
| Game build | Diagnostic/content version; many-to-many relationship with seasons |
| Statistics scope | A comparability policy that may use season as its boundary but may require a narrower ruleset/build boundary |
| Challenge period | May be contained by and reference a season; daily/weekly periods are not seasons |
| AccelByte Season Pass | External reward/progression product that may be mapped to an Eventun season but is not automatically the same identity |
| Gauntlet | May be season-scoped, cross-season, or global according to an explicit scope policy |
| Telemetry storage segment | Physical archive/detach unit selected for operations; need not equal a season |
| Retention tier | Detail and storage policy; may transition at season closure but is not season identity |

### Data Families Requiring An Explicit Season Policy

| Data family | Initial direction to discuss |
|---|---|
| Player statistics | Preserve lifetime career totals; the initial seasonal projections cover only best lap and best finish records and their ranks |
| Records and leaderboards | Preserve lifetime lap/finish records and add exact-season views; the player UI defaults to the current regular season |
| Progression goals | Career achievements remain lifetime unless authored otherwise; seasonal goals and counters reference an exact season |
| Challenges | Seasonal challenge periods must reference the Eventun season rather than relying only on similar timestamps |
| Gauntlets | Use an explicit `global` or `season` scope; require season-scoped schedules to fit the season window |
| Insights | Include season in explain/context, but do not automatically discard cross-season history when the compared metric remains compatible |
| Match history | Store nullable season attribution, label attributed matches, and support exact-season filters without hiding unseasoned history from unfiltered queries |
| Permanent competition results | Retain independently of raw-event retention and preserve exact season identity |

### Query And Projection Implications

Season identity should be present in semantic facts and serving projections that promise seasonal behavior. It should not be added indiscriminately to every primary key.

The initial implemented changes are:

- nullable season evidence on `match_fact` only;
- exact-season Match History, seasonal leaderboard, and player-rank reads;
- `player_season_course_record` for seasonal lap/finish winners while preserving lifetime records; and
- match/player serving projection generation `2/2`, while gauntlet projection and sealed qualification evidence remain `1/1`.

The existing lifetime tables remain, with explicit seasonal record projections
rather than a generic `scope_kind/scope_id` abstraction.
`player_course_record_contribution` remains normalized and has no `season_id`;
seasonal winner projection joins its existing batch/source identity to
`match_fact`. Unseasoned contributions feed only lifetime records. Seasonal
reads enumerate course codes represented by persisted records, so a later
course deactivation does not hide past-season results. Explicit off-seasons use
the same seasonal projection machinery but are hidden from ordinary
player-facing season listings by default.

Season-aware read contracts use an explicit `lifetime` scope or exact season id. Omission must not silently mean the season current at request time because replaying the same request later would change its meaning. A client may resolve the current regular season first and then request that exact id.

### Partitioning And Retention Implications

Season should be modeled before destructive lifecycle work because it affects historical product behavior and archive manifests. It should not automatically become a PostgreSQL partition key.

Reasons to keep the decisions separate:

- seasons may have irregular lengths;
- off-seasons may be very short or long;
- physical detach cadence may need monthly or size-bounded segments;
- hot queries already rely on source/event-type pruning;
- adding season to the partition hierarchy may create excessive partition counts; and
- statistics may need a new season even when physical data remains in the same storage segment.

A later retention design may choose season-aligned time segments, but only after representative volume, partition count, ingest cost, hot-query pruning, detach, restore, and reprocessing measurements. Archive manifests should always record season coverage even when archive objects use another physical segmentation.

Raw events must not be dropped merely because a season closed. Before destructive removal, Eventun must preserve and reconcile:

- accepted batch identity and source provenance;
- permanent match and competition outcomes;
- awarded progression and reward history;
- required lifetime and seasonal aggregates;
- season attribution;
- archive counts and checksums; and
- a tested restore and re-derivation path.

## Accepted F16A Checkpoint

1. Eventun owns the season schedule and manages it through the Extend App UI.
2. Seasons are finite, half-open, and non-overlapping; contiguous coverage is not required.
3. Server facts resolve from MatchStart. Client facts are eligible only when MatchStart and trusted batch receipt resolve to the same non-null season. Server and client observations remain source-separated.
4. Matches outside every season are accepted as unseasoned and remain in lifetime statistics and unfiltered Match History.
5. UUID `season_id` is the immutable identity. Title is mutable, non-unique, and never an identifier; the initial model has no human-readable code. Future unused semantics may change or be deleted, while referenced kind and bounds freeze. Season splitting is deferred.
6. The first seasonal statistic families are best lap, best finish, and their leaderboards/ranks. Lifetime career aggregates and lifetime records remain.
7. Explicit off-seasons use normal projections but are hidden from ordinary player-facing season history by default.
8. Gauntlets remain independent unless a later feature adds an explicit season association; changing match season does not reinterpret qualification or sealed results.
9. AccelByte Season Pass may align operationally but has no required identity or date mapping in the initial model.
10. MMR remains game-computed and AccelByte-stored for now; seasonal rating ownership/reset is a separate design and implementation decision.
11. Historical conversion does not invent seasons. Existing retained facts are unseasoned unless a later reviewed repair classifies them.
12. The logical season implementation can join the pending development cutover because it is additive and converted facts remain unseasoned; it does not require another destructive event rewrite.

### F16A Implementation Closure

- Normal attribution and fact repair use the shared schedule lock. Serving-only
  targeted repair and full rebuild consume persisted attribution without that
  lock. Static defensive constraints remain, while application mutations route
  through the locked database functions and database-owner direct SQL is
  treated as trusted maintenance.
- The seasonal record projection retains normalized contribution attribution,
  exact lifetime-equivalent winner/tie ordering, and parent-winner integrity for
  normal projection, targeted repair, and full rebuild. No contribution season
  column, new reconciliation surface, or new manifest was added.
- The focused next-winner plan contains 1,500 faster cross-season candidates.
  It examined 1,501 contribution rows and 4,566 shared buffers in isolation
  through the contribution winner index and keyed `match_fact` access, produced
  exactly one deterministic winner, and used no sequential scan. The complete
  schema suite observed 1,501/4,590. The accepted maxima are 2,000 candidates
  and 6,500 shared buffers; the latter represents about three B-tree buffer
  visits per candidate plus bounded overhead. The earlier combined-fixture
  observation of 1,501/4,591 is also retained as evidence.
- The API and Extend App enforce the 1–128-character title rule, exact Unix-
  millisecond UTC boundaries, deterministic listing, explicit exact-season
  filters, canonical cancellation/deadline behavior, and non-UTC-browser exact
  round-tripping.
- Retained-data read verification replaced per-course/category leaderboard
  helper calls with one set-based lifetime and seasonal assembly. On the
  authentic 11-course snapshot, lifetime SQL measured 24.935 ms p50 and 36.313
  ms p95 with 730 shared-hit buffers; the handler measured 25.369 ms p50 and
  25.862 ms p95. `player_view` is evaluated once per request. Match History
  resolves player/source candidates first and then performs keyed fact and
  artifact lookups; limits 30 and 100 measured 2.771 ms and 3.306 ms handler
  p95 respectively, with no sequential fact scan or spill. No new index,
  cache, materialized database object, denormalization, or API change was
  required.
- The one combined local rehearsal execution
  `d569e068-1bf9-41af-93f6-ad7446d73468` converted 4,973,624 historical events
  into 3,219 explicitly unseasoned facts, completed the `2/2` serving cutover,
  and retained the migrated database and resettable snapshot. A final populated
  API smoke restored that snapshot into a disposable clone, projected
  deterministic attributed regular/off-season fixtures, and passed seasonal
  leaderboard, player-rank, exact-season Match History, off-season exact-ID,
  and lifetime checks. Its fixture transaction rolled back and the clone was
  discarded. Development cutover remains pending; no shared database was
  changed.

## Planning Recommendation

Split the current F16 concept into two decisions:

### F16A: Season Semantics And Logical Attribution

The semantic checkpoint and smallest additive implementation are complete. The
remaining F16A delivery action is the owner-controlled combined development
cutover. Converted facts remain unseasoned, and split/reassignment recovery is
still outside the initial scope.

### F16B: Statistics Scope, Physical Segmentation, And Retention

Keep this evidence-driven. Define per-statistic comparability, historical UI/API promises, partition strategy, hot/warm/cold tiers, archive format, restore, and destructive deletion only with representative volume and query-plan evidence.

This split recognizes seasons as foundational without prematurely coupling the product calendar to physical storage or making the entire long-term archive design a blocker.

## SQL And Go Boundary

- Keep set-based fact derivation, idempotent contribution application, projection updates, and season-window exclusion constraints in PostgreSQL.
- Keep insight candidate semantics, ranking, progression requirement validation, and season policy orchestration in Go.
- Have SQL preserve nullable evidence rather than deciding that missing telemetry equals zero.
- Resolve and persist season attribution in the acceptance transaction, and preserve that exact evidence during ordinary repair; do not let queries or repair rediscover season from current timestamps independently.
- Keep metric and season catalogs authoritative in one place each, with startup and publish validation for code-owned handlers.

## Review Scope And Verification

The initial review was read-only and remains tied to the reviewed commit. This
2026-07-18 reconciliation additionally records the accepted F16A implementation,
focused plan proof, combined rehearsal, retained database/snapshot, populated
API smoke, and final retained-data query-performance correction through
`37c0307`. Repository and complete schema/transition verification for the final
correction passes are recorded in the linked work tracker rather than
retroactively attributed to the original review.

## Source Index

Eventun at the original reviewed commit:

- [Insight scoring and selection](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/insight_scoring.go)
- [Insight candidate generation](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/insight_candidates.go)
- [Insight policy](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/insight_policy.go)
- [Insight admin policy UI](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/app/src/features/insights/InsightPoliciesPage.tsx)
- [Insight metric SQL](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/migration/c6_func_insight_metrics.sql)
- [Progression requirement evaluation](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/progression_goal_eval.go)
- [Progression publish validation](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/progression_validation.go)
- [Progression goal candidate and counter loading](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/internal/eventun/progression_goal_check_db.go)
- [Progression counter projection SQL](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/migration/c10_func_progression.sql)
- [Canonical schema](https://github.com/ikigai-github/eventun/blob/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994/migration/a0_create_init.sql)
