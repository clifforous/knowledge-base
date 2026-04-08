# Ascent Rivals Recommendation API - Engineering Design

## Goal
Define the backend-owned API surface for match-summary and time-trial recommendations.

This note is for engineering implementation, not UI layout.

The client requirement is intentionally small:
- request recommendations for a completed run
- receive a prioritized list
- show 1 primary recommendation
- optionally show 1 or 2 secondary recommendations

The backend owns:
- selecting the recommendation categories
- choosing the comparison baselines
- scoring confidence and priority
- returning only the final prioritized recommendation list plus enough supporting evidence for display

## Scope
This design supports two recommendation modes:
- time trial
- real match

Comparison rules:
- Time trial compares the player against:
  - their own past performance on the course
  - the current best record lap run on the course
  - the current best record finish run on the course
- Real match compares the player against:
  - lobby average
  - lobby leader, if the player is not the leader
  - the player's own past performance for the same heat number on the same course
- Racing recommendations should ignore telemetry that occurs after ascension phase starts.
- Ascension phase currently starts when the first 3 racers finish their final lap.

## Initial Recommendation Categories
The backend should initially support only these categories:

1. `route_choice_shortcuts`
2. `straightaway_speed`
3. `corner_speed`
4. `warp_usage`
5. `energy_management`
6. `overall_lift`
7. `overall_speed`
8. `strafes_used`
9. `stall_time`
10. `combat_mode_time`
11. `kills`
12. `deaths`
13. `crashes`

These should be represented as an enum in the service contract.

## Client-Facing API Surface
Use one client-facing endpoint.

Reason:
- the client interaction is identical for time trial and match
- only the backend comparison logic differs
- one endpoint keeps the game client simple

## Suggested RPC
```proto
rpc GetRunRecommendations(GetRunRecommendationsRequest) returns (GetRunRecommendationsResponse);
```

## Request
`match_id` alone is not a stable run identifier. The backend should require:
- `player_id`
- `session_id`
- `match_id`

Suggested shape:

```proto
message GetRunRecommendationsRequest {
  string player_id = 1;
  string session_id = 2;
  int32 match_id = 3;
  int32 max_recommendations = 4; // default 3, clamp to 3
}
```

## Response
The response should be backend-ranked and ready for direct client rendering.

```proto
enum RecommendationStatus {
  RECOMMENDATION_STATUS_UNSPECIFIED = 0;
  RECOMMENDATION_STATUS_PENDING = 1;
  RECOMMENDATION_STATUS_READY = 2;
  RECOMMENDATION_STATUS_FAILED = 3;
}

enum RecommendationRole {
  RECOMMENDATION_ROLE_UNSPECIFIED = 0;
  RECOMMENDATION_ROLE_PRIMARY = 1;
  RECOMMENDATION_ROLE_SECONDARY = 2;
}

enum RecommendationCategory {
  RECOMMENDATION_CATEGORY_UNSPECIFIED = 0;
  RECOMMENDATION_CATEGORY_ROUTE_CHOICE_SHORTCUTS = 1;
  RECOMMENDATION_CATEGORY_STRAIGHTAWAY_SPEED = 2;
  RECOMMENDATION_CATEGORY_CORNER_SPEED = 3;
  RECOMMENDATION_CATEGORY_WARP_USAGE = 4;
  RECOMMENDATION_CATEGORY_ENERGY_MANAGEMENT = 5;
  RECOMMENDATION_CATEGORY_OVERALL_LIFT = 6;
  RECOMMENDATION_CATEGORY_OVERALL_SPEED = 7;
  RECOMMENDATION_CATEGORY_STRAFES_USED = 8;
  RECOMMENDATION_CATEGORY_STALL_TIME = 9;
  RECOMMENDATION_CATEGORY_COMBAT_MODE_TIME = 10;
  RECOMMENDATION_CATEGORY_KILLS = 11;
  RECOMMENDATION_CATEGORY_DEATHS = 12;
  RECOMMENDATION_CATEGORY_CRASHES = 13;
}

enum ComparatorType {
  COMPARATOR_TYPE_UNSPECIFIED = 0;
  COMPARATOR_TYPE_SELF_HISTORY = 1;
  COMPARATOR_TYPE_SELF_HEAT_HISTORY = 2;
  COMPARATOR_TYPE_RECORD_BEST_LAP = 3;
  COMPARATOR_TYPE_RECORD_BEST_FINISH = 4;
  COMPARATOR_TYPE_LOBBY_AVERAGE = 5;
  COMPARATOR_TYPE_LOBBY_LEADER = 6;
}

message RecommendationMetric {
  string metric_key = 1;
  double player_value = 2;
  double benchmark_value = 3;
  double delta = 4;
  string unit = 5;
  bool lower_is_better = 6;
}

message RecommendationLocation {
  int32 heat = 1;
  int32 lap = 2;
  int32 checkpoint_start = 3;
  int32 checkpoint_end = 4;
  repeated string segment_tags = 5;
}

message RecommendationEvidence {
  ComparatorType comparator = 1;
  double z_score = 2;
  double weighted_score = 3;
  string benchmark_label = 4;
}

message Recommendation {
  RecommendationRole role = 1;
  RecommendationCategory category = 2;
  double priority_score = 3;
  double confidence_score = 4;
  RecommendationMetric primary_metric = 5;
  RecommendationLocation location = 6;
  repeated RecommendationEvidence evidence = 7;
  repeated RecommendationMetric supporting_metrics = 8;
}

message GetRunRecommendationsResponse {
  RecommendationStatus status = 1;
  string pending_reason = 2;
  string course_code = 3;
  string race_mode = 4;
  repeated Recommendation recommendations = 5;
  string analyzed_at = 6;
}
```

## Client Contract Rules
- The client should not derive rankings itself.
- The backend must return recommendations already sorted by `priority_score` descending.
- The client should render:
  - first item as primary
  - next 1 or 2 items as secondary
- The client should tolerate:
  - only 1 recommendation returned
  - `PENDING` while latest match data is not fully ingested

## Backend Recommendation Flow
The backend pipeline should be:

1. Load the completed run.
2. Identify race mode.
3. Determine the racing-phase cutoff.
4. Build the comparator set.
5. Build candidate metrics for each supported category using only pre-ascension racing data.
6. Compute deviation against each comparator.
7. Convert deviation into weighted recommendation scores.
8. Suppress weak or low-confidence candidates.
9. Return the top ranked list.

## Racing-Phase Cutoff
For real matches, recommendation metrics should be computed only from the racing phase.

Reason:
- once ascension starts, the player goal changes from racing optimization to survival and reaching a point of interest
- racing metrics after that moment are no longer comparable to normal lap- and pace-oriented decision making

Current rule:
- ascension phase starts when the first 3 racers finish their final lap

Implementation guidance:
- identify the ascension start timestamp for the match
- ignore checkpoint, lap, warp, speed, stall, lift, strafe, combat-mode, and similar racing telemetry after that timestamp
- if a category depends on whole-heat or whole-match aggregates, use a pre-ascension aggregate instead of the final post-ascension total when the recommendation is intended to explain racing performance
- time trial is unaffected because ascension does not apply there

## Comparator Set
### Time Trial
Use:
- self history on the same course
- current best record lap run on the course
- current best record finish run on the course

Recommended comparison windows:
- recent attempts on the same course
- player historical baseline on the same course

The minimum version should still preserve record-lap and record-finish comparators even if self-history is collapsed into one distribution.

### Real Match
Use:
- lobby average
- lobby leader, if not the player
- self heat history for the same course and same heat number

Important:
- match guidance should be heat-index aware
- do not compare heat 1 to the player's own heat 3
- for racing recommendations, compare only pre-ascension metrics

## Scoring Model
The backend should not use raw standard deviation alone.

Recommended formula:

```text
priority_score = deviation_score * category_weight * comparator_weight * confidence_modifier
```

Where:
- `deviation_score`:
  - normalized deviation from benchmark, preferably z-score based
- `category_weight`:
  - product priority for how likely the category is to be causal
- `comparator_weight`:
  - trust level of the comparator source
- `confidence_modifier`:
  - suppression or reduction when the signal is sparse, ambiguous, or low-volume

## Deviation Score
Use z-scores or robust z-scores where possible.

Guidance:
- Use standard z-score if the comparator distribution is stable and large enough.
- Use robust z-score with median and MAD if the distribution is noisy or heavy-tailed.
- Fall back to normalized percent difference if the sample is too small for a useful distribution.

Suggested output fields:
- raw player metric
- benchmark metric
- raw delta
- z-score or equivalent normalized deviation

## Category Weights
The product requirement is that some categories should outrank others even when their raw deviation is smaller.

Example:
- missing shortcuts may be more important than slightly poor energy management

That means category weights should be explicit and configurable.

Suggested starting principle:
- high causal likelihood and high actionability get higher weight
- broad or ambiguous categories get lower weight

Suggested initial ordering to test:
1. `route_choice_shortcuts`
2. `corner_speed`
3. `straightaway_speed`
4. `warp_usage`
5. `energy_management`
6. `stall_time`
7. `overall_speed`
8. `crashes`
9. `deaths`
10. `kills`
11. `strafes_used`
12. `overall_lift`
13. `combat_mode_time`

This is not final product truth. It is a starting tuning table.

## Comparator Weights
Suggested starting weights:
- self heat history: highest for real match
- self history: highest for time trial
- record best lap: high for lap- and execution-oriented categories in time trial
- record best finish: high for route- and full-run-oriented categories in time trial
- lobby leader: high, but only when the leader is a credible benchmark
- lobby average: moderate

Reason:
- self-history is the cleanest baseline for "what should I do differently next time"
- course records are the cleanest aspirational baseline for "what is the fastest known execution on this course"
- lobby leader is useful but may reflect outlier skill
- lobby average is useful but less aspirational

## Confidence Modifier
Confidence should down-rank recommendations when:
- sample count is too low
- the benchmark population is too small
- the signal depends on an inferred segment type rather than an explicit tag
- the category lacks a clear location
- multiple categories explain the same loss equally well

Suggested confidence bands:
- `high`: stable metric, explicit segment or event support, sufficient sample count
- `medium`: good metric but comparator sample is modest
- `low`: inference-heavy or sparse

Only `high` or `medium` should be eligible for primary recommendation by default.

## Recommendation Suppression Rules
Do not return filler.

Suggested rules:
- always return at most 3 recommendations
- primary recommendation must exceed a minimum priority threshold
- secondary recommendations must exceed a lower threshold
- suppress near-duplicate categories

Examples:
- `overall_speed` should usually be suppressed if `straightaway_speed` and `corner_speed` are both already selected
- `stall_time` and `energy_management` may need deduping if they point to the same underlying issue
- `kills` may be suppressed if its variance is fully explained by `combat_mode_time`

## Metric Definitions For Query Work
These definitions are the minimum contract the next query task should satisfy.

| Category | Primary metric | Direction | Likely source inputs | Notes |
|---|---|---|---|---|
| `route_choice_shortcuts` | shortcut opportunities taken / available | higher is better | checkpoint path, `shortcut` tag | Needs route divergence on the course. |
| `straightaway_speed` | average speed on straight/open tagged segments | higher is better | checkpoint speed, segment tags or inferred open segments | If no explicit straight tag exists, derive from absence of restrictive tags. |
| `corner_speed` | average speed on `corner` segments | higher is better | checkpoint speed, `corner` tag | Prefer tagged segments over inferred curves. |
| `warp_usage` | warps used / warp opportunities | higher is usually better | `numWarps`, segment tags | Needs a stable definition of warp opportunity. |
| `energy_management` | time out of energy | lower is better | `timeOutOfEnergyMs` | Candidate supporting metric: energy spent. |
| `overall_lift` | time in air ratio or lift duration | depends on course intent | `timeInAirMs` | Needs careful tuning. This is likely a secondary-only category at first. |
| `overall_speed` | average speed over whole run or heat | higher is better | `averageSpeed` | Broad fallback category. |
| `strafes_used` | active strafes used in `slotted` or control-heavy segments | depends on track section | `numActiveStrafes`, segment tags | Should be context-sensitive, not globally "more is better." |
| `stall_time` | time stalled | lower is better | `timeStalledMs` | Strong direct execution metric. |
| `combat_mode_time` | time in combat mode or weapon-active state | context dependent | dedicated combat mode signal preferred | If no explicit event exists, this needs instrumentation or a carefully defined proxy. |
| `kills` | kills per heat or run | higher is better in match | match and heat results | Only relevant for real matches. |
| `deaths` | deaths per heat or run | lower is better | match and heat results | Strong direct penalty signal. |
| `crashes` | crashes per heat or run | lower is better | match and heat results | Strong direct penalty signal. |

For real matches, these metrics should use pre-ascension values when the recommendation is intended to explain racing performance rather than extraction survival.

## Required Query Inputs
The recommendation query task should assume the backend needs these inputs:

### Run identity
- `player_id`
- `session_id`
- `match_id`
- `course_code`
- `race_mode`

### Time-trial comparator inputs
- player's prior runs on the same course
- distribution per category for that player on that course
- current best record lap metrics for the course
- current best record finish metrics for the course

### Real-match comparator inputs
- full lobby participant set for the match
- lobby leader metrics for the match or heat
- lobby average metrics for the match or heat
- player's historical same-heat runs for the same course
- ascension start timestamp for the match
- pre-ascension filtered metrics for player, lobby average, and lobby leader

### Per-run metric inputs
- lap and checkpoint metrics
- tagged segment grouping
- part-change records if they are later folded into other recommendation logic
- heat result and match result stats
- ascension lifecycle marker or derived ascension start time

## Recommended Internal Backend Surfaces
These do not need to be client-facing, but the implementation will likely want them:

- `build_time_trial_recommendation_inputs(player_id, session_id, match_id)`
- `build_match_recommendation_inputs(player_id, session_id, match_id)`
- `compute_recommendation_candidates(inputs)`
- `score_recommendation_candidates(inputs, candidates)`
- `select_final_recommendations(candidates)`

## Optional Debug API
This will help tune weighting and suppression.

```proto
rpc ExplainRunRecommendations(GetRunRecommendationsRequest) returns (ExplainRunRecommendationsResponse);
```

This debug response should include:
- all candidate categories
- raw metrics
- comparator metrics
- z-scores
- applied weights
- suppression reasons

This endpoint should not be exposed to the normal game client.

## Non-Goals
- The client does not compute recommendation logic.
- The client does not re-rank recommendations.
- This API does not replace existing match summary or history endpoints.
- This API does not return a coaching sentence.

## Open Questions
- Should recommendation results be computed synchronously on request or materialized after match ingest completes?
- What minimum sample count is required before self-history categories are considered stable?
- Do `overall_lift`, `strafes_used`, and `combat_mode_time` need stronger instrumentation before they can become primary?
- Should the API return the benchmark source used for each recommendation in a user-visible way or only as internal/debug metadata?
