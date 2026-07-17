# Eventun Insights, Progression, And Seasons Review

**Status:** F16A season-semantics checkpoint accepted 2026-07-16; implementation and F16B retention decisions remain open
**Date:** 2026-07-16
**Reviewed repository:** [Eventun](https://github.com/ikigai-github/eventun) at [`5aaaea2f4991f19e69b1d9bad90e5208fb1d4994`](https://github.com/ikigai-github/eventun/commit/5aaaea2f4991f19e69b1d9bad90e5208fb1d4994)

## Related

- [[eventun-foundation-api-simplification-review]]
- [[../../30_designs/ascent-rivals/eventun-post-match-insights-solution-design]]
- [[../../30_designs/ascent-rivals/eventun-post-match-insights-next-phase-ideation-notes]]
- [[../../30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design]]
- [[../../30_designs/ascent-rivals/eventun-progression-next-phase-ideation-notes]]
- [[../../30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan]]
- [[../../40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams|eventun-foundation-and-teams-tasks]]

## Purpose

Record an adversarial review of Eventun's insight ranking and progression goal model, then re-triage the findings between immediate foundation work and later insight or progression iterations. Reconsider the previously deferred season decision now that seasons are expected to bound some player statistics, progression, gauntlets, queries, and historical data lifecycles.

This document is not an approved implementation plan. In particular, it does not yet approve a season schema, make F16 a dependency of F15, or select a physical partition and retention strategy.

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

### Working Definition

A season is a named Eventun product time window owned by Eventun. It commonly coincides with new content or a client release, but it is not identified by a client build and is not required to begin or end with one. An off-season is still an explicit season window.

This definition implies:

- every relevant instant resolves to at most one explicit season;
- gaps are valid and matches in a gap are unseasoned rather than rejected or assigned to a moving implicit season;
- game builds and seasons remain separate attributes;
- one season may contain multiple builds and one build may appear in more than one season; and
- competitions, challenge periods, and gauntlets may reference a season without becoming the season itself.

### Proposed Minimal Season Entity

The initial design discussion should start from the smallest useful entity:

| Field | Purpose |
|---|---|
| `id` | Stable immutable identity |
| `code` | Human-readable operator reference such as `2026-s01` or `2026-offseason-01` |
| `title` | Player/operator display title |
| `starts_at` | Inclusive UTC boundary |
| `ends_at` | Exclusive UTC boundary |
| `kind` | `regular`, `off_season`, or another deliberately bounded product classification |
| `created_at` | Operational creation timestamp |
| `updated_at` | Operational update timestamp |

Avoid draft, published, or independently mutable `active` state. A stored season is authoritative, and current/upcoming/past state is derived from its half-open window. Eventun's Extend App UI owns simple season creation, listing, future-unused editing/deletion, and cosmetic title editing. Code, kind, and bounds become immutable once matches reference the season.

Season splitting and reassignment between existing seasons are low-priority recovery considerations, not part of the initial implementation. General telemetry defects are repaired through fact/contribution repair and projection rebuilds rather than by manufacturing season boundaries. For example, an invalid ultra-low finish caused by treating an early heat exit as a completed race requires correction of the faulty semantic fact and its derived records.

### Attribution Recommendation

The working recommendation is:

- Eventun resolves season identity; producers do not submit a season id.
- A complete match is assigned once from the authoritative match-start instant using `starts_at <= match_started_at < ends_at`.
- A match crossing a season boundary remains wholly in the season in which it started.
- Late arrival uses gameplay occurrence time, not ingestion time.
- The compact `match_fact` stores the resolved nullable season id; individual events inherit it through batch identity unless measured query or retention needs justify denormalization.
- Attribution is immutable under ordinary operation and repairable only through an audited rebuild path.

Eventun accepts a match with no covering season as unseasoned. It still contributes to lifetime statistics and match history but not season-scoped records. The initial administration surface does not split an existing season or move matches from one season to another. A later narrowly bounded recovery may allow a newly created non-overlapping season to claim previously unseasoned matches, but that behavior requires a separate reviewed repair contract and is not implicit in ordinary creation.

The current fact model deliberately keeps each accepted client or server batch as an independent observation. Each fact therefore uses its own batch MatchStart consistently. Server-derived surfaces use server facts, while client-only time-trial surfaces use the player's client fact; client timing cannot reclassify a server-derived result. Season implementation does not introduce a separate cross-source logical-match canonicalization subsystem.

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

Likely changes include:

- season-aware player and player-course statistic projections;
- season keys on seasonal progression state and challenge periods;
- season filters or scope identifiers for selected leaderboard and record projections;
- season attribution on gauntlet configuration or participation where the gauntlet is season-scoped; and
- season coverage in backfill, repair, and reconciliation manifests.

Keep the existing lifetime tables and add explicit seasonal record projections rather than forcing records through a generic `scope_kind/scope_id` abstraction. Existing record contributions may carry nullable season attribution and feed both projections. Unseasoned contributions feed only lifetime records. Explicit off-seasons use the same seasonal projection machinery but are hidden from ordinary player-facing season history by default.

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
3. Each accepted fact uses its batch MatchStart. Server and client observations remain source-separated according to existing trust and serving policies.
4. Matches outside every season are accepted as unseasoned and remain in lifetime statistics and unfiltered Match History.
5. Future unused seasons may change or be deleted; title is cosmetic; referenced code, kind, and bounds freeze. Season splitting is deferred.
6. The first seasonal statistic families are best lap, best finish, and their leaderboards/ranks. Lifetime career aggregates and lifetime records remain.
7. Explicit off-seasons use normal projections but are hidden from ordinary player-facing season history by default.
8. Gauntlets remain independent unless a later feature adds an explicit season association; changing match season does not reinterpret qualification or sealed results.
9. AccelByte Season Pass may align operationally but has no required identity or date mapping in the initial model.
10. MMR remains game-computed and AccelByte-stored for now; seasonal rating ownership/reset is a separate design and implementation decision.
11. Historical conversion does not invent seasons. Existing retained facts are unseasoned unless a later reviewed repair classifies them.
12. The logical season implementation can follow the event cutover because retained MatchStart facts permit additive attribution without another destructive event rewrite.

## Planning Recommendation

Split the current F16 concept into two decisions:

### F16A: Season Semantics And Logical Attribution

The semantic checkpoint is accepted. Plan the smallest implementation after the event cutover: the Eventun-owned season catalog and Extend App UI, nullable fact attribution, explicit lifetime/exact-season query scopes, and seasonal best-lap/best-finish projections. Do not include a split/reassignment recovery tool in the initial scope.

### F16B: Statistics Scope, Physical Segmentation, And Retention

Keep this evidence-driven. Define per-statistic comparability, historical UI/API promises, partition strategy, hot/warm/cold tiers, archive format, restore, and destructive deletion only with representative volume and query-plan evidence.

This split recognizes seasons as foundational without prematurely coupling the product calendar to physical storage or making the entire long-term archive design a blocker.

## SQL And Go Boundary

- Keep set-based fact derivation, idempotent contribution application, projection updates, and season-window exclusion constraints in PostgreSQL.
- Keep insight candidate semantics, ranking, progression requirement validation, and season policy orchestration in Go.
- Have SQL preserve nullable evidence rather than deciding that missing telemetry equals zero.
- Resolve and persist season attribution in one owned transaction or deterministic repair path; do not let every query rediscover season from timestamps independently.
- Keep metric and season catalogs authoritative in one place each, with startup and publish validation for code-owned handlers.

## Review Scope And Verification

The review inspected the Knowledge Base contracts and the Eventun insight, progression, schema, SQL, API, and Extend App UI sources. It was read-only. No tests, builds, code generation, linters, vulnerability scans, or schema verification were rerun. Eventun work continued during documentation, so the findings remain tied to the reviewed commit rather than claiming review of later F14R changes.

## Source Index

Eventun at the reviewed commit:

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
