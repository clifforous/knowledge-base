# Eventun Post-Match Insights Solution Design

## Status
Draft for review.

## Goal
Replace the current post-match and time-trial recommendation concept with a backend-owned
**insights** system that can return coaching, kudos, or an explicit no-insight state.

The system should improve player value without forcing shallow advice such as "drive
faster" or "get more kills." A strong result should be allowed to produce praise instead
of weak coaching.

## Background
The existing recommendation design establishes the right ownership boundary: Eventun
selects categories, baselines, scoring, confidence, priority, and suppression; the game
client requests completed-run guidance and renders the returned result. This design
extends that direction by changing the product object from "recommendations" to
"insights."

Existing references:

- `30_designs/ascent-rivals/recommendation-api-engineering-design.md`
- `30_designs/ascent-rivals/match-summary-time-trial-improvement-metrics.md`
- `50_knowledge/ascent-rivals/eventun/events.md`
- `50_knowledge/ascent-rivals/competition-runtime-terms.md`

Current implementation facts:

- Eventun already has time-trial and post-match recommendation endpoints.
- Eventun already derives recommendation snapshots from match events, lap events,
  checkpoint events, and historical comparator data.
- `PlayerHeatStart` already records the player's full loadout snapshot, weight,
  normalized weight, and loadout value.
- `PlayerHeatEnd` already records the player's current retained credit balance at heat
  end, placement, CP, kills, deaths, crashes, obelisks, and best lap time. This is not
  the same as credits earned during the heat.
- The game client/server already computes UI-facing loadout category scores for Speed,
  Agility, and Combat. These are tier-plus-augment presentation scores, not full physical
  capability metrics.
- Resolved loadouts also compute underlying ship and weapon stats after applying base
  weight-class stats, part modifiers, augment modifiers, engine stage modifiers, and weight
  fit penalties.
- `PlayerHeatStart` does not currently serialize remaining credits or category-score summary
  values. Versioned resolved capability metrics are a future extension, not phase 1 scope.
- Eventun's current recommendation metrics already join heat-end retained credit balance
  with heat-start loadout value.
- The current response is recommendation-shaped and lacks a first-class kudo or
  no-insight model.
- The current recommendation response reserves status/readiness fields and currently uses
  gRPC errors for several incomplete or unavailable cases.
- The game client currently maps recommendation categories to localized static text.
- The game client currently promotes the first recommendation to primary when no primary
  role is present.
- The game client can collapse recommendation API errors into an empty response, which
  makes failure difficult to distinguish from a true no-recommendation result.

Relevant code paths:

- Eventun: `proto/ikigai/eventun/v1/client.proto`
- Eventun: `proto/ikigai/eventun/v1/match.proto`
- Eventun: `internal/eventun/recommendation_api.go`
- Eventun: `internal/eventun/recommendation_scoring.go`
- Eventun: `migration/c5_func_recommendation.sql`
- Eventun: `migration/c6_func_recommendation_metrics.sql`
- Eventun: `migration/c7_func_recommendation_snapshot.sql`
- Game client: `Source/AscentRivals/Private/UserInterface/Routes/HGPostMatchRecommendationRoute.cpp`
- Game client: `Source/AscentRivals/Private/Client/HGStatsSubsystem.cpp`
- Game client: `Source/AscentRivals/Public/Net/HGEventunEvents.h`
- Game client: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Game client: `Source/AscentRivals/Private/Server/Subsystems/HGLoadoutServerSubsystem.cpp`
- Game client: `Source/AscentRivals/Private/Loadout/HGResolvedLoadout.cpp`
- Game client: `Source/AscentRivals/Public/Item/HGItemTypes.h`

Planned new Eventun contract path:

- Eventun: `proto/ikigai/eventun/v1/insight.proto`

## Product Direction
Use **Insights** as the player-facing and backend domain term.

An insight may be:

- coaching: a specific, evidence-backed improvement opportunity
- kudo: a specific, evidence-backed positive result or improvement
- no insight: analysis completed, but no result cleared the quality bar

This naming avoids conflict with the existing item/part recommendation system. Specific
part-buy recommendations and item recommender logic are out of scope. High-level
server-match economy and loadout insights are in scope when they are phrased as spend,
loadout-value, or stat-distribution observations rather than "buy this exact part" advice.

## Scope
Phase 1 covers:

- post-match insights for the server-match modes currently supported by Eventun
  recommendation metrics, with unsupported modes returning `unavailable`
- time-trial insights
- one primary insight slot and up to two secondary insight slots
- coaching and kudo candidate generation
- no-insight, pending, unavailable, and failed states
- Postgres-backed policy tuning
- admin/debug explainability in the Extend app UI dashboard
- client-owned localization
- bounded client retry for insight readiness
- high-level ARC/credit spend and loadout-value insights for server matches
- loadout category score insights using the existing Speed, Agility, and Combat presentation
  scores

Phase 1 should use existing Eventun and game-client telemetry where possible. One concrete
telemetry addition is expected: record `creditsAtHeatStart` and loadout category scores in
the heat-start analytics payload so spend and build-shape insights do not need to parse
nested loadout data for common comparisons.

Any insight that needs purchase timing, pre-run leaderboard rank, segment personal-best
history, versioned capability scores, or validated build-to-outcome correlations should
remain disabled until those data sources exist.

Out of scope for phase 1:

- specific part-buy recommendations
- item recommender logic or exact part selection
- time-trial economy/spending insights
- machine-learning ranking
- backend localization
- ELO or skill-bracket comparisons
- broad longitudinal player profiles
- exact player-facing CP gain estimates

## Terminology
| Term | Meaning |
|---|---|
| Insight | A backend-selected post-run result shown to the player. |
| Coaching insight | A recommended improvement with supporting evidence. |
| Kudo insight | Praise for a strong result, achievement, or improvement. |
| Primary insight | The main card on the insights screen. |
| Secondary insight | Optional supporting cards below the primary card. |
| No insight | Analysis completed, but no candidate cleared the quality bar. |
| Pending | Eventun cannot analyze yet because match data is not query-ready. |
| Unavailable | Insights are unsupported for this mode, map, or player state. |
| Failed | Eventun failed to evaluate the request. |
| Client timeout | The client stopped retrying before Eventun returned a final factual state. This is not a backend status. |
| Policy | DB-backed weights, thresholds, and enablement for known insight IDs. |
| ARC / credits | The in-match spend resource used by the server economy. The UI may call it ARC. |
| Loadout value | The resolved loadout's credit-equivalent investment value at heat start. |
| Ship capability vector | Future compact normalized build metrics derived from resolved loadout stats. |

## UX Model
Reuse the current high-level screen layout:

- one primary slot
- up to two secondary slots
- a compact run summary above the slots
- actions such as retry/play again, match details, or exit remain client-owned

Slots are not recommendation-only. A kudo can occupy primary or secondary slots.

Selection rule:

```text
strong kudo > medium coaching
strong coaching > medium kudo
specific evidence > broad aggregate
high confidence > speculative impact
personal or match-relevant benchmark > generic benchmark
```

A strong kudo may take the primary slot even when a valid coaching insight exists. This
prevents poor outcomes such as telling a match winner with fastest lap to "drive faster"
because one lower-confidence metric was technically below a benchmark.

## Client Display States
The backend status remains factual. The client may derive a display state based on how the
player entered the screen.

Backend statuses:

- `ready`
- `pending`
- `no_insight`
- `unavailable`
- `failed`

Status semantics:

- `ready`: analysis completed and at least one insight slot is present.
- `pending`: required event data is expected to become query-ready soon. This is retryable.
- `no_insight`: analysis completed, but no candidate cleared required quality gates. This
  includes cases such as a new racer or new map where the available facts are valid but too
  sparse to produce a credible insight.
- `unavailable`: this request is not supported for the mode, map, schema version, or player
  state. This is not retryable in the current post-match flow.
- `failed`: Eventun reached an unexpected evaluation failure after accepting a valid request.

Do not convert authentication, authorization, invalid-request, or service-outage failures
into insight statuses. Those remain transport/API errors. The insight status model is only
for run-analysis outcomes.

Phase 1 client display behavior:

- Manual entry: if the player clicks the Insights button, show an Insights screen. If no
  result is available, show a neutral "No insights available" state.
- Automatic entry is out of scope for the first implementation. The client may prefetch
  insights after match-event submission is accepted, but it should not automatically route
  players into the Insights screen until the feature has proven valuable enough to show
  immediately.

Future automatic-entry behavior:

- If the post-match flow tries to show insights before the normal match summary, only show
  the Insights screen when a ready result arrives quickly. Otherwise skip directly to the
  normal post-match summary.

Timeout is not the same as `no_insight`. If the client gives up after waiting, log it as a
client timeout or pending timeout, not as backend-confirmed no-insight.

## Timing And Readiness
The insight request should occur only after the match event batch is submitted and accepted.
For phase 1, the player enters the Insights screen through the manual button. The client may
also prefetch after accepted submission, but prefetch must not automatically route the player
into the Insights screen. There may be a small delay between match finish, event submission,
database commit, and query readiness.

Phase 1 should avoid a large async analysis pipeline:

1. The game client submits the match event batch.
2. Eventun persists the batch.
3. The game client requests insights after submission is accepted, either as optional prefetch
   or when the player enters through the manual Insights button.
4. Eventun derives insights on demand from committed match data.
5. If data is not ready, Eventun returns `pending`.

The client should retry `pending` within a small bounded window. The target product
behavior is roughly 1 to 2 seconds total waiting for this post-match surface. In phase 1,
after that window, manual entry shows an empty state. A future automatic-entry flow should
skip the screen when the window expires.

Eventun may return `retry_after_ms`, but the game client should cap it for this screen.

Suggested phase 1 retry state machine:

1. Request insights after match event submission is accepted, either as optional prefetch or
   when the manual Insights button is entered.
2. If `ready`, show the returned slots.
3. If `no_insight` or `unavailable`, stop retrying.
4. If `failed`, stop retrying and log a backend failure.
5. If `pending`, retry while all limits remain true:
   - no more than 3 total insight requests including the first request
   - no more than 2000 ms total wait for manual entry
   - per-retry sleep is `retry_after_ms` clamped to 150-500 ms, or 250 ms when omitted
6. If the client reaches its cap while the latest backend state is `pending`, record a
   client-side pending timeout. Manual entry renders the neutral empty state. A future
   automatic-entry flow should skip the insights screen.

Future work may materialize insight analyses in a table or worker if on-demand scoring
becomes too slow or expensive. The API contract should not require that change.

## Circuit Point Driver Analysis
Current circuit points are awarded from heat placement, not directly from kills, obelisks,
deaths, crashes, or lap metrics.

At heat end, the game server sorts racers by heat outcome. For placed racers, placement is
finish-time ordered. For non-placed racers, sorting considers finish state, progress, and
credits depending on state. The game then grants CP from placement:

```text
circuit_points_to_grant =
  max(0,
      CircuitPointAmountPerHeat * (heat_index + 1)
      - CircuitPointStepPerPosition * (heat_index + 1) * (placement - 1))
```

Implications:

- Later heats have larger CP stakes because both the available first-place CP and the
  per-position step scale by `heat_index + 1`.
- CP is a strong outcome signal but should not be treated as a decomposable point formula.
- Kills, deaths, crashes, obelisks, speed, route choice, and energy management can be
  causal contributors to placement or finish state, but they are not direct CP addends.
- Player-facing insights should avoid exact "estimated CP gain" claims in phase 1.
- Eventun may use heat-weighted CP context internally to rank candidates.

Player-facing payloads should expose stable facts instead of estimated CP math:

- heat
- lap
- segment/checkpoint location
- placement
- benchmark placement or comparator
- time gap
- metric delta
- comparison source

## Economy And Loadout Analysis
Economy insights are server-match insights only. Time trials and noncompetitive modes have
effectively unlimited money, so spend quality has little player value there.

Current server economy facts from the game client/server:

- Competitive matches seed credits from `PassiveCreditsPerHeat[0]`.
- Additional passive credits are awarded from later `PassiveCreditsPerHeat` buckets as lap
  completion credits. For a normal heat, the current heat bucket is divided across laps.
- Ascent mode does not award passive credits for the final lap because not every player
  reaches or completes it.
- Obelisk hits, kills, contracts, retained contracts, and final-lap bounties can add credits.
- Purchases happen before heat start, credits are preserved, and the economy is non-linear:
  by Heat 3 or Heat 4, many players can reach top-tier parts.

Design implications:

- Compare loadout value and spend only within the same mode, heat number, and rules context.
  Heat 1 should not be compared directly to Heat 4.
- Do not flag "saved Heat 1 money" by itself. Saving early can be correct if it produces a
  stronger Heat 2 buy.
- Stronger signals are late-match unspent ARC, low Heat 3/4 loadout value relative to
  high-CP players, or a repeated category/slot investment pattern that does not improve
  outcome.
- Because CP is heat-weighted, late-heat economy misses should receive higher internal
  priority than equivalent early-heat misses.
- Player-facing text should describe the observable fact, not claim exact lost CP.

Current usable data:

- `PlayerHeatStart`: loadout item IDs, augment IDs, weight class, weight, normalized weight,
  and loadout value.
- `PlayerHeatEnd`: `creditsAtHeatEnd` in design terminology, meaning current retained
  credit balance at heat end, plus placement, CP, kills, deaths, crashes, obelisks, and best
  lap.
- Eventun recommendation metrics already expose per-heat `credits` and `loadout_value`.
  The existing `credits` metric should be treated as retained balance, not earned credits.

### UI Scores Versus Resolved Capabilities
The Speed, Agility, and Combat bars shown in the client are presentation scores. They come
from resolved loadout slot categories:

- Speed: engine and warp drive
- Agility: stabilizer and PRS
- Combat: cockpit and weapon

Each category score is the sum of core item tier score plus equipped augments in that
category. This is useful for a readable UI comparison, but it is too coarse for insight
confidence because parts and augments affect many concrete stats.

Future resolved capability groups:

- Speed capability: engine top speed stages, acceleration stages, warp factor, warp duration,
  warp charge rate, warp energy cost, energy capacity, energy regen, and energy draw.
- Agility/control capability: engine and stabilizer turning, stabilizer lift range, lowline
  speed multiplier, hover stiffness, PRS active strafe strength/cost/cooldown, passive strafe
  strength/cost, air volume, and air refill.
- Combat capability: weapon damage, rate of fire, range, area of effect, charge/prefire
  timing, energy/air per shot, cockpit HP, engine HP, and warp expenditure damage.
- Weight/fit capability: weight, normalized weight, and part efficiency ratings after weight
  fit penalties.

These groups intentionally overlap. PRS and stabilizer primarily support movement, but also
matter in combat because lateral control helps evade shots. Engine and warp primarily support
speed, but can affect combat through energy availability, warp damage, and survivability.
Cockpit is currently combat-oriented through durability, but hull durability also affects
how aggressively a player can use warp.

Player-facing copy should stay broad:

- "Your opponents had stronger speed capability in the late heats."
- "Your build had less lateral control than the top CP players."
- "You won despite a lower loadout value."

Avoid player-facing text that names exact stats or specific parts unless a future item
recommender owns that flow.

### Future Capability Score Idea
Capability scores are a useful direction, but they should not be part of phase 1 until their
formula is explicit and versioned. A future implementation should define a compact
capability vector with stable scale, monotonic direction, clamping, and golden tests.

Candidate future scores:

- `speedCapabilityScore`: derived from max speed, acceleration, warp factor, warp charge,
  warp duration, and relevant energy constraints.
- `agilityCapabilityScore`: derived from turning, strafe strength, lift/hover control, air
  capacity, and air refill.
- `combatCapabilityScore`: derived from weapon damage, rate, range, durability, and warp
  damage.
- `energyCapabilityScore`: derived from energy capacity, regeneration, draw, and key action
  costs.

The value of these scores is backend simplicity: Eventun can compare build capabilities
without reimplementing the whole Unreal resolved-stat model. The risk is tuning ambiguity:
policy thresholds such as "25% lower speed capability" are only meaningful if the score
formula is stable. Future capability insights should therefore include:

- a `capabilityScoringVersion`
- exact Unreal-owned formulas
- 0.0-1.0 or 0-100 scale chosen once and used consistently
- documented higher-is-better semantics
- tests over representative loadouts
- admin explain output showing score inputs and version

Recommended Phase 1 telemetry additions:

- Add `creditsAtHeatStart` to `PlayerHeatStart`, representing remaining credits after
  pre-heat purchases are locked in.
- Add UI loadout category score summary to `PlayerHeatStart`:
  - `speedScore`
  - `speedAugmentScore`
  - `agilityScore`
  - `agilityAugmentScore`
  - `combatScore`
  - `combatAugmentScore`
- Continue sending existing `weight`, `normalizedWeight`, and `loadoutValueAtHeatStart`
  fields.
- Store those values in Eventun's heat-start event table and recommendation metric inputs.

Use explicit names in Eventun code and documentation:

- `creditsAtHeatStart`: retained credit balance after locked pre-heat purchases.
- `creditsAtHeatEnd`: retained credit balance at heat end.
- `loadoutValueAtHeatStart`: resolved credit-equivalent investment value at heat start.

Avoid using `credits` alone in new APIs or docs because it is unclear whether it means
earned credits, spendable balance, or retained end-state balance.

This keeps phase 1 simple. Eventun can use the full loadout snapshot internally when needed,
but common comparisons should not require parsing item IDs, reimplementing item economics, or
reconstructing the full Unreal stat model.

Optional later telemetry:

- A `PlayerLoadoutTransaction` or `PlayerPartChange` analytics event for buy, equip, undo,
  and clear-augment actions.
- Include action, slot/category, tier, price, credits after transaction, loadout value after
  transaction, and category scores after transaction.
- A versioned compact capability vector, after the future capability score formula is
  defined and validated.

That event would improve audit/debug quality and purchase-timing analysis, but it is not
required to ship high-level spend insights in phase 1.

## Benchmark Strategy
Phase 1 should use benchmarks that are available, understandable, and credible with the
current player population.

### Post-Match Benchmarks
Use:

- current-match top CP player or high-CP cohort
- adjacent placement player when explaining a concrete heat result
- lobby average where it is stable enough
- player same-course and same-heat history
- player recent same-course history
- same-heat high-CP or top-placement loadout value and loadout category scores for economy
  and build-shape insights

Do not use ELO or higher-skill bracket comparisons in phase 1. ELO exists but is not
tested enough, and the current player population is too small for reliable skill-bracket
baselines.

Economy and loadout benchmarks must be same heat number. A Heat 4 build is expected to be
stronger than a Heat 1 build because the in-match economy compounds over time.

### Time-Trial Benchmarks
Use:

- player personal best on the same course
- player recent same-course attempts
- current time-trial leader or course record
- best known lap or finish record

Time trial is the cleanest surface for segment-level execution insights because the run
context is more controlled and combat/objective confounders are absent.

### Benchmark Labels
Eventun should return stable benchmark enums. The game client should localize labels such
as:

- "the top player"
- "your personal best"
- "your recent runs"
- "the time-trial leader"

## Current State Versus Required Changes
| Area | Current state | Required phase 1 change |
|---|---|---|
| Client API | Recommendation endpoints exist. Several readiness fields are reserved or absent, and incomplete cases can surface as gRPC errors. | Add insight-oriented RPCs with explicit analysis statuses, slot invariants, and error-to-status mapping. |
| Eventun scoring | Recommendation scoring is deterministic but category-specific and recommendation-shaped. | Split candidate generation into coaching and kudo candidates, then rank them together with shared confidence and suppression rules. |
| Telemetry | Existing events support many racing, combat, CP, credit-balance, and loadout-value facts. | Add heat-start credit balance and loadout category scores before enabling economy/build-shape insights that depend on them. Keep compact capability scores for a future iteration. |
| Client UI | Current client maps recommendation categories to static localized text and can promote a first secondary recommendation to primary. | Render backend-selected primary and secondary insight slots exactly as returned; localize from stable template keys and arguments. |
| Timing | Client currently requests recommendations after event submission acceptance, but errors and empty results can collapse together. | Add a bounded retry state machine that distinguishes pending timeout, no insight, unavailable, and failure. |
| Policy/admin | Recommendation tuning is mostly code-driven. | Seed validated policy rows for known insight IDs and expose audited admin controls in the Extend app UI. |

## API Shape
Prefer a new insight-oriented API instead of extending the legacy recommendation response
in place.

Shared insight enums and messages should live in `proto/ikigai/eventun/v1/insight.proto`.
`client.proto` and `admin.proto` should import those shared types. Remove legacy
recommendation RPCs and recommendation-shaped messages as the insight replacement lands; do
not keep alias endpoints or reserve old proto positions.

Suggested client RPCs:

```proto
rpc GetPostMatchInsights(GetRunInsightsRequest) returns (GetRunInsightsResponse);
rpc GetTimeTrialInsights(GetRunInsightsRequest) returns (GetRunInsightsResponse);
```

The game client may already know the mode. Including mode in the response is acceptable as
an echo/debug field, but client routing should not depend on it.

### Request
```proto
message GetRunInsightsRequest {
  string player_id = 1;
  string session_id = 2;
  int32 match_id = 3;
  optional int32 max_insights = 4; // default 3, clamp to 3
}
```

### Response
```proto
enum InsightResponseStatus {
  INSIGHT_RESPONSE_STATUS_UNSPECIFIED = 0;
  INSIGHT_RESPONSE_STATUS_READY = 1;
  INSIGHT_RESPONSE_STATUS_PENDING = 2;
  INSIGHT_RESPONSE_STATUS_NO_INSIGHT = 3;
  INSIGHT_RESPONSE_STATUS_UNAVAILABLE = 4;
  INSIGHT_RESPONSE_STATUS_FAILED = 5;
}

enum InsightStatusReason {
  INSIGHT_STATUS_REASON_UNSPECIFIED = 0;
  INSIGHT_STATUS_REASON_NONE = 1;
  INSIGHT_STATUS_REASON_DATA_NOT_READY = 2;
  INSIGHT_STATUS_REASON_INSUFFICIENT_DATA = 3;
  INSIGHT_STATUS_REASON_UNSUPPORTED_MODE = 4;
  INSIGHT_STATUS_REASON_UNSUPPORTED_MAP = 5;
  INSIGHT_STATUS_REASON_SCHEMA_UNSUPPORTED = 6;
  INSIGHT_STATUS_REASON_EVALUATION_FAILED = 7;
}

enum InsightType {
  INSIGHT_TYPE_UNSPECIFIED = 0;
  INSIGHT_TYPE_COACHING = 1;
  INSIGHT_TYPE_KUDO = 2;
}

message GetRunInsightsResponse {
  InsightResponseStatus status = 1;
  InsightStatusReason status_reason = 2;
  int32 retry_after_ms = 3;
  string course_code = 4;
  string race_mode = 5;
  RunInsight primary_insight = 6;
  repeated RunInsight secondary_insights = 7;
  string scoring_version = 8;
}
```

Response invariants:

- `READY` means `primary_insight` is present. `secondary_insights` contains 0 to 2 entries.
- `NO_INSIGHT`, `PENDING`, `UNAVAILABLE`, and `FAILED` return no primary and no secondaries.
- `NO_INSIGHT` uses `INSUFFICIENT_DATA` only when analysis completed but no credible candidate
  could be produced. It is not a transport failure.
- `PENDING` uses `DATA_NOT_READY` and may include `retry_after_ms`.
- `UNAVAILABLE` uses a non-retryable reason such as unsupported mode, map, or schema.
- `FAILED` is for an unexpected evaluator failure after a valid request. Invalid request,
  auth, permission, and service-outage cases remain normal API errors.
- `scoring_version` is present for any response where Eventun attempted insight evaluation.

### Insight
```proto
message RunInsight {
  InsightType type = 1;
  InsightId insight_id = 2;
  string title_key = 3;
  string body_template_key = 4;
  InsightBenchmarkType benchmark_type = 5;
  InsightLocation location = 6;
  repeated InsightMetric metrics = 7;
  repeated InsightTemplateArg template_args = 8;
  InsightConfidenceBand confidence_band = 9;
}
```

The player-facing response should not include raw priority scores, internal confidence
component scores, estimated CP gain, or suppression internals.

Slot assignment is represented only by `primary_insight` and `secondary_insights`. Do not
also encode role on each `RunInsight`; otherwise the client has two competing sources of
truth. The client should not promote a secondary insight to primary when the primary field is
empty.

### Location
```proto
message InsightLocation {
  int32 heat = 1;
  int32 lap = 2;
  int32 checkpoint_start = 3;
  int32 checkpoint_end = 4;
  repeated string segment_tags = 5;
  string location_key = 6;
}
```

### Metrics
```proto
message InsightMetric {
  string argument_name = 1;
  InsightMetricId metric_id = 2;
  double player_value = 3;
  double benchmark_value = 4;
  double delta_value = 5;
  double delta_percent = 6;
  InsightUnit unit = 7;
  bool lower_is_better = 8;
  string label_key = 9;
}

message InsightTemplateArg {
  string name = 1;
  InsightTemplateArgKind kind = 2;
  InsightMetricId metric_id = 3; // used when kind is METRIC
  string text_key = 4; // optional localizable static token when needed
}

enum InsightTemplateArgKind {
  INSIGHT_TEMPLATE_ARG_KIND_UNSPECIFIED = 0;
  INSIGHT_TEMPLATE_ARG_KIND_METRIC = 1;
  INSIGHT_TEMPLATE_ARG_KIND_BENCHMARK_LABEL = 2;
  INSIGHT_TEMPLATE_ARG_KIND_LOCATION_LABEL = 3;
  INSIGHT_TEMPLATE_ARG_KIND_TEXT_KEY = 4;
}
```

The client owns unit formatting, localized text, and message assembly. Eventun supplies
stable IDs, values, units, locations, and template keys.

The proto package should define `InsightId`, `InsightMetricId`, `InsightBenchmarkType`,
`InsightUnit`, and `InsightConfidenceBand` as enums, not open strings.

`InsightUnit` should support at least time, speed, count, percent, ARC/credits, and generic
score units so economy and loadout-stat facts can share the same metric payload.

## Localization Contract
Eventun must not return localized player-facing prose.

Eventun returns:

- insight ID enum
- title key
- body template key
- metric ID enums
- benchmark type enum
- unit enum
- confidence band enum
- stable template argument names
- player values
- benchmark values
- deltas
- locations

Template keys must declare a stable argument schema. For example,
`insight.best_lap_gap.body` might require:

| Argument | Source |
|---|---|
| `delta_percent` | `InsightMetric.argument_name = "delta_percent"` |
| `benchmark_label` | `InsightBenchmarkType` localized by the client |
| `location_label` | `InsightLocation` localized by the client |

The client should reject or fall back when an insight ID/template key requires an argument
that Eventun did not provide. The DB policy table must not be able to change template keys
or argument names independently of code/proto support.

The game client renders localized text such as:

- "20% slower than the top player"
- "20% slower than your personal best"
- "20% slower than your recent runs"
- "Heat 3"
- "Lap 2, sectors 3-5"

This keeps localization in the Unreal client, where the localization workflow already
exists.

## Insight Candidate Catalog
The valid insight catalog should be defined in code/proto and mirrored by seeded DB policy
rows. DB policy rows may tune known insights, but they must not invent unsupported insight
IDs that the client cannot localize or render.

Catalog status should be explicit:

- `default_enabled`: can ship in phase 1 with existing telemetry and conservative policy.
- `enabled_after_phase1_telemetry`: can ship after the heat-start additions in this design.
- `seed_disabled`: known insight ID exists, but policy starts disabled until validation.
- `future`: keep out of phase 1 code unless implementation is intentionally expanded.

### Default-Enabled Phase 1 Coaching Insights
| Insight ID | Modes | Notes |
|---|---|---|
| `best_lap_gap` | match, time trial | Best lap behind personal best, leader, or comparator. |
| `course_time_gap` | time trial | Finish time behind personal best or course leader. |
| `corner_speed_gap` | match, time trial | Tagged corner segment speed below benchmark when course tags/checkpoint data are available. |
| `straight_speed_gap` | match, time trial | Tagged or derived straight/open segment speed below benchmark when segment classification is available. |
| `energy_management_gap` | match, time trial | Excess out-of-energy time or inefficient energy use. |
| `stall_time_gap` | match, time trial | Excess stalled time. |
| `crash_reduction` | match | Crashes plausibly harmed heat result, placement, or time. |
| `death_reduction` | match | Deaths plausibly harmed heat result, placement, or time. |
| `warp_usage_gap` | match, time trial | Lower warp use in contexts where benchmark use is clearly better. |
| `lap_consistency_gap` | match, time trial | Lap-to-lap variance is high versus self or benchmark. |
| `late_arc_investment` | match | Player's loadout value stayed low until later heats compared with high-CP same-heat players. Do not claim exact purchase timing. |
| `loadout_value_gap` | match | Same-heat loadout value is materially below high-CP or top-placement comparators. |

### Default-Enabled Phase 1 Kudo Insights
| Insight ID | Modes | Notes |
|---|---|---|
| `match_winner` | match | Player finished first. |
| `podium_finish` | match | Player reached podium. |
| `top_circuit_points` | match | Player had top or near-top CP. |
| `fastest_lap` | match | Player had fastest lap in the match. |
| `personal_best_lap` | match, time trial | Player improved personal best lap when prior PB exists. |
| `personal_best_course_time` | time trial | Player improved personal best finish when prior PB exists. |
| `clean_race` | match, time trial | No crashes or no major penalties. |
| `survivor` | match | No deaths or unusually low deaths in a combat-heavy match. |
| `combat_standout` | match | High combat output when supported by clear facts. |
| `objective_standout` | match | High obelisk/objective contribution as praise, not CP explanation. |
| `energy_efficiency_standout` | match, time trial | Very low empty-energy or stall time. |
| `consistent_laps` | match, time trial | Low lap variance. |

### Enabled After Phase 1 Heat-Start Telemetry
| Insight ID | Modes | Required data | Default |
|---|---|---|---|
| `unspent_arc` | match | `creditsAtHeatStart`, `creditsAtHeatEnd`, same-heat loadout value comparators. | Enabled conservatively after telemetry lands. |
| `loadout_category_gap` | match | Speed, Agility, and Combat category score summaries plus observed weakness that aligns with the category gap. | Seed disabled until validation. |
| `efficient_spender` | match | Loadout value, retained credits, strong outcome, and same-heat comparators. | Seed disabled until validation. |

### Requires New Derived Stores Or History
| Insight ID | Modes | Reason |
|---|---|---|
| `time_trial_rank_improved` | time trial | Requires pre-run and post-run leaderboard rank or stored rank history. Current input can report rank, but not prove improvement. |
| `segment_personal_best` | match, time trial | Requires a durable segment/PB store, not only current-run checkpoint facts. |
| `major_improvement` | match, time trial | Requires comparable personal history windows and stable definitions of meaningful improvement. |
| `first_finish` | match, time trial | Requires player run-history query and a clear definition of finish by mode. |
| `smart_arc_use` | match | Requires purchase timing or transaction-level loadout change history. Heat-start snapshots alone can show value by heat, but not timely buying behavior. |
| `repeated_slot_investment` | match | Requires transaction or multi-heat slot-change analysis and validation that the pattern correlates with weak outcomes. |
| `loadout_capability_gap` | match | Requires a versioned compact capability vector and validation that score gaps correlate with actionable observed outcomes. |
| `strong_build_fit` | match | Requires versioned capability scores, same-heat effective comparator patterns, and enough sample data to avoid disguised part recommendations. |

### Disabled Or Cautious Phase 1 Insights
| Insight ID | Reason |
|---|---|
| `route_choice_gap` | Shortcut advice is build- and speed-dependent; needs observed segment outcomes. |
| `shortcut_entry_speed_gap` | Needs enough successful and unsuccessful shortcut samples. |
| `objective_focus` | Objectives affect credits and play state, but CP is placement-awarded. Use cautiously. |
| `combat_efficiency_gap` | Needs clear causal connection between combat time/output and result. |
| `combat_overcommit` | Easy to overstate without context. |
| `active_strafe_usage_gap` | Must be segment-contextual, not globally "use more strafes." |
| `hover_speed_control_gap` | Current time-in-air telemetry is not enough to explain hover height tradeoffs directly. |
| `overall_speed_gap` | Too broad for primary; use only as fallback if enabled. |
| `specific_part_purchase` | Out of scope; belongs to the item recommender, not post-match insights. |

Shortcut insights should become stronger only after Eventun can learn from enough races
that used the shortcut, including observed entry speeds, build/loadout context, and
whether the shortcut improved position, lead, or segment time.

## Scoring And Ranking
Use a deterministic weighted ranker for phase 1. Do not use a machine-learning model.

Each generated candidate has:

- insight ID
- type
- metric evidence
- benchmark evidence
- location
- effect size
- confidence score
- priority score
- suppression group

Priority answers: should this insight be shown, and how high?

```text
priority_score =
  base_weight
  * effect_size_score
  * benchmark_relevance
  * outcome_relevance
  * confidence_score
  * mode_weight
```

Definitions:

- `base_weight`: product priority from DB policy.
- `effect_size_score`: normalized gap or achievement magnitude.
- `benchmark_relevance`: trust and relevance of the comparator.
- `outcome_relevance`: relationship to placement, lap time, finish time, or achievement.
- `confidence_score`: trust in the conclusion.
- `mode_weight`: mode-specific adjustment.

Score scale:

- `effect_size_score`, `benchmark_relevance`, `outcome_relevance`, and
  `confidence_score` are normalized to 0.0-1.0.
- `base_weight` is policy-controlled and should normally stay in the 0.25-3.0 range.
- `mode_weight` is policy-controlled and should normally stay in the 0.0-2.0 range.
- `priority_score` thresholds are stored on the same resulting scale as the formula. Admin
  controls should show the effective score range so tuning is not guesswork.
- Per-insight generators own required facts and metric construction. DB policy can disable,
  gate, and weight a known insight, but it cannot create new metrics or template arguments.

Selection rules:

- Coaching and kudo candidates compete in one ranked set.
- Primary slot goes to the highest-value candidate that clears primary thresholds.
- Secondary slots take the next eligible candidates that clear secondary thresholds.
- Strong kudos can outrank valid coaching.
- Weak coaching must not displace meaningful achievements.
- No candidate should be shown only to fill a slot.

Suppression rules:

- suppress near-duplicate categories
- suppress `overall_speed_gap` when specific speed categories are selected
- suppress energy/stall duplicates when they explain the same event cluster
- suppress broad combat advice when death/crash/combat facts are more specific
- suppress shortcut advice unless confidence is high enough for the selected segment
- suppress economy insights in time trial and noncompetitive modes
- suppress Heat 1-only spend advice unless the pattern persists or creates a later missed
  opportunity
- suppress low-loadout-value advice when the player achieved a strong kudo-worthy outcome
  with efficient spend

## Confidence Model
Confidence answers: do we trust this conclusion?

Use an inspectable score built from components:

```text
confidence_score =
  weighted_average(
    data_completeness,
    benchmark_quality,
    effect_strength,
    consistency,
    specificity,
    comparability,
    recency
  )
```

Components:

- `data_completeness`: required match, heat, lap, checkpoint, and benchmark facts exist.
- `benchmark_quality`: comparator sample count and source quality.
- `effect_strength`: the observed gap or achievement is large enough to matter.
- `consistency`: the signal appears across enough relevant samples or moments.
- `specificity`: the insight names a useful heat, lap, checkpoint, or segment.
- `comparability`: course, mode, heat number, rules, and phase are comparable.
- `recency`: recent history has higher weight than stale history.

For economy/loadout insights, `comparability` must include heat number and economy context.
Signals that compare different heats should be low confidence unless normalized by the
known economy curve.

Confidence bands:

- `high`: stable metric, strong comparator, clear effect, specific location.
- `medium`: useful signal with modest comparator or less specific location.
- `low`: sparse, inference-heavy, or weakly comparable.

Hard gates:

- Primary insights require at least medium confidence, with higher thresholds for cautious
  categories.
- Low-confidence insights are not player-facing by default.
- Insight-specific DB policy can require high confidence.
- Candidate generators must declare required facts before policy scoring runs.
- Comparator-backed insights must meet the policy's minimum sample count for the selected
  benchmark type.
- Repeat/cooldown rules suppress recently shown insights before slot selection.

Default confidence thresholds:

- `high`: `confidence_score >= 0.80`
- `medium`: `confidence_score >= 0.55`
- `low`: `confidence_score < 0.55`

These defaults can be tuned, but the band names should remain stable for client rendering
and admin explanations.

Suggested comparator sample-count defaults:

- direct current-match leader or match winner comparison: 1 comparator is acceptable
- current-match high-CP cohort comparison: at least 3 comparators when available
- personal best comparison: 1 prior valid PB
- recent-history comparison: at least 5 comparable runs, with 10 preferred for stable deltas
- same-heat economy/loadout comparison: at least 3 same-mode, same-heat comparators
- route, shortcut, or capability-to-outcome comparison: seed disabled until enough samples are
  validated per course and mode

Examples:

- `match_winner` is high confidence if match-end data exists.
- `personal_best_lap` is high confidence if historical PB is known and the lap event is valid.
- `current_match_top_cp_player` comparison is relevant but may have lower benchmark quality
  than personal-history comparisons.
- `last_10_runs` comparisons require same course and mode for raw time metrics.
- Shortcut insights require enough observed outcomes for the shortcut path and comparable
  movement/build context.
- `unspent_arc` is high confidence only when late-heat or match-end credits are high, the
  player's loadout value is below same-heat comparators, and the player did not also earn a
  strong efficiency kudo.
- `loadout_category_gap` is medium at best because Speed, Agility, and Combat scores are
  presentation summaries. It should require an aligned observed weakness such as corner speed,
  combat survivability, or late-heat loadout value before becoming player-facing.
- Future `loadout_capability_gap` insights stay disabled until capability scores and outcome
  relationships are validated across enough same-course or same-heat samples.

## Postgres Policy Tuning
Use Postgres-backed policy rows so tuning does not require code deployment.

The DB should tune only known insight IDs. Eventun code/proto remains the source of truth
for valid IDs, modes, metric IDs, and client-localizable template keys.

The supported editing path should be the admin API and Extend app UI. Direct DB edits remain
available to trusted operators with database access, but they are an escape hatch rather than
the normal workflow because they bypass request validation and UI guardrails.

Suggested table:

```sql
create table insight_policy (
  insight_id text not null,
  mode text not null,
  enabled boolean not null default true,
  base_weight numeric not null,
  min_effect_size numeric not null default 0,
  min_confidence numeric not null default 0,
  min_benchmark_sample_count integer not null default 1,
  min_required_samples integer not null default 1,
  primary_threshold numeric not null,
  secondary_threshold numeric not null,
  confidence_weights jsonb not null default '{}'::jsonb,
  benchmark_weights jsonb not null default '{}'::jsonb,
  suppression_group text,
  diversity_group text,
  cooldown_runs integer not null default 0,
  max_per_response integer not null default 1,
  scoring_version integer not null default 1,
  updated_at timestamptz not null default now(),
  updated_by text,
  primary key (insight_id, mode)
);
```

Recommended behavior:

- Seed policy rows through migrations.
- Validate policy IDs against known code/proto IDs.
- Cache active policy in Eventun with a short TTL or reload-on-update strategy.
- Log `scoring_version` with every explain/debug result.
- Keep default rows conservative. Enable cautious categories only after validation.
- Clamp policy numeric values to safe ranges at write time.
- Treat empty `confidence_weights` and `benchmark_weights` as code-defined defaults.
- Keep required facts in code, not arbitrary policy JSON, so policy cannot make unsupported
  insights appear valid.
- Apply cooldown and diversity after confidence gates but before final slot assignment.

Optional audit table:

```sql
create table insight_policy_audit (
  id bigserial primary key,
  insight_id text not null,
  mode text not null,
  previous_policy jsonb,
  next_policy jsonb not null,
  changed_at timestamptz not null default now(),
  changed_by text
);
```

## Backend Flow
Phase 1 flow:

1. Validate request identity.
2. Load match/run readiness.
3. Load current policy.
4. Build mode-specific metrics and benchmarks.
5. Build economy/loadout inputs for server-match requests.
6. Generate coaching candidates.
7. Generate kudo candidates.
8. Score candidates.
9. Apply confidence gates and suppression.
10. Select primary and secondary slots.
11. Return a player-facing response or a factual status.

Status/error mapping:

- Valid request, event batch not query-ready yet: `PENDING` with `DATA_NOT_READY`.
- Valid request, required facts available, no candidate clears gates: `NO_INSIGHT`.
- Valid request for unsupported mode, map, or analytics schema: `UNAVAILABLE`.
- Valid request reaches an unexpected evaluator error after loading run context: `FAILED`.
- Invalid request, unauthenticated request, forbidden request, service outage, and database
  connectivity failures remain normal API errors. They should not be disguised as
  player-facing no-insight.

Suggested internal surfaces:

- `build_post_match_insight_inputs`
- `build_time_trial_insight_inputs`
- `generate_coaching_candidates`
- `generate_kudo_candidates`
- `score_insight_candidates`
- `select_insight_slots`
- `explain_insight_candidates`

Keep these surfaces small and deterministic. The progression system recently became large;
this design should favor narrow modules and DB policy tuning over a broad framework.

## Client Responsibilities
The game client should:

- request insights after match event submission is accepted
- retry `pending` using the phase 1 state machine and cap described above
- render primary and secondary slots without recomputing ranking
- localize title/body templates and metric labels
- format values and units
- for phase 1 manual entry, show "No insights available" for true no-insight or bounded
  timeout while logging timeout separately
- expose the player-facing screen as Insights
- log client pending timeouts separately from backend `no_insight`

The game client should not:

- compute coaching logic
- synthesize kudos from empty responses
- promote secondary insights to primary
- treat empty response, timeout, failure, and no-insight as the same internal state

## Admin Explainability And Extend App UI
Add insight controls to the Eventun Extend app UI dashboard.

Admin APIs should be permissioned and separate from the normal game-client API.

Suggested admin APIs:

```proto
rpc ListInsightPolicies(ListInsightPoliciesRequest) returns (ListInsightPoliciesResponse);
rpc UpdateInsightPolicy(UpdateInsightPolicyRequest) returns (UpdateInsightPolicyResponse);
rpc ExplainRunInsights(ExplainRunInsightsRequest) returns (ExplainRunInsightsResponse);
rpc ListInsightPolicyAudit(ListInsightPolicyAuditRequest) returns (ListInsightPolicyAuditResponse);
```

The Extend app UI should support:

- policy list by mode and insight ID
- enable/disable controls
- weight and threshold editing
- suppression group review
- policy version display
- policy audit history
- run debugger by `player_id`, `session_id`, `match_id`, and mode
- candidate review for selected and rejected candidates
- data readiness diagnostics

Explain response should include admin-only details:

- all generated candidates
- selected primary and secondary slots
- rejected candidates
- raw metrics
- comparator metrics
- effect size
- priority score
- confidence score
- confidence component breakdown
- benchmark source
- suppression reason
- data readiness state
- active policy/scoring version

This debug payload is not player-facing and should not be used by the normal Unreal client.

## Data Readiness Diagnostics
For admin and operational debugging, Eventun should be able to explain whether required
facts were present:

- `MatchStart`
- `HeatStart`
- `PlayerHeatStart`
- `PlayerCheckpoint`
- `PlayerLap`
- `PlayerHeatEnd`
- `HeatEnd`
- `PlayerMatchEnd`
- `MatchEnd`
- ascension cutoff when applicable
- comparator history
- course/record data
- `creditsAtHeatStart` and `creditsAtHeatEnd` for economy insights
- `loadoutValueAtHeatStart`, category scores, weight, and normalized weight for loadout
  insights
- future compact capability vector when capability insights are enabled
- pre-run leaderboard rank when rank-improvement insights are enabled
- segment PB store when segment PB insights are enabled

This is necessary to distinguish real no-insight from missing data or slow ingestion.

## Phase Plan
### Phase 1
Build the typed insight system:

- new insight API contract
- status model and error-to-status mapping
- primary and secondary insight slots
- coaching and kudo candidate generation
- DB-backed policy tuning
- deterministic scoring and confidence
- client localization contract
- bounded client retry
- `creditsAtHeatStart`, loadout category scores, weight, and normalized weight telemetry
- server-match economy and loadout insight candidates
- admin explain/debug APIs
- Extend app UI dashboard controls
- catalog readiness classification so unsupported insights remain disabled until their data
  sources exist

Use existing telemetry except for the small heat-start economy/loadout summary additions
called out above.

### Phase 2
Add longitudinal player-development capabilities:

- player trends over many races
- normalized cross-course skill signals
- more robust recent-history comparison windows
- route and shortcut outcome learning
- build/loadout-aware shortcut and handling comparisons
- versioned compact capability scores, if the formula is stable enough for player-facing
  comparisons
- optional player loadout transaction event for exact purchase timing audit/debugging
- materialized insight analysis if needed

ELO or skill-bracket comparisons remain phase 2 or later. They should not become
player-facing until rating quality and player population make them credible.

## Testing And Validation
Backend tests:

- API status mapping: ready, pending, no-insight, unavailable, failed
- transport/API errors are not converted to player-facing no-insight
- no client-visible insight when confidence is too low
- strong kudo can outrank medium coaching
- weak coaching does not fill empty slots
- DB policy disablement suppresses an insight ID
- DB threshold changes affect ranking deterministically
- invalid policy insight IDs fail validation or are ignored safely
- CP heat weighting affects internal priority but not player-facing CP text
- economy insights are generated only for server-match modes
- Heat 1-only saving does not produce spend coaching by itself
- late unspent ARC can produce coaching when `creditsAtHeatStart`, `creditsAtHeatEnd`,
  same-heat loadout value, and confidence clear required gates
- efficient-spender kudos suppress low-loadout-value coaching
- loadout category comparisons require same-heat comparators, category score data, and an
  aligned observed outcome
- future capability comparisons cannot be selected without a versioned capability scoring
  formula and required data
- disabled catalog entries cannot be selected even when policy rows exist
- time-trial personal-best and leader benchmarks produce correct deltas
- post-match ascension cutoff excludes racing telemetry after ascension

Client tests:

- manual entry shows "No insights available" for no-insight or timeout
- client does not promote secondary insight to primary
- client distinguishes timeout, failure, no-insight, and unavailable internally
- localized template keys render expected values and units
- missing template arguments fall back safely and are logged

Admin tests:

- policy edits update active scoring behavior
- policy audit records changes
- explain endpoint shows selected, rejected, and suppressed candidates
- data readiness diagnostics identify missing event classes

Validation metrics:

- percentage of ready requests
- percentage of pending timeouts
- percentage of no-insight results
- distribution of selected insight IDs
- primary kudo versus primary coaching ratio
- economy insight selection rate by heat
- economy insight suppression count by reason
- low-confidence suppression counts
- manual-entry empty-state frequency

## Risks
- Shortcut advice can be wrong if it ignores build maneuverability, minimum jump speed, or
  observed shortcut outcomes.
- Objective advice can be overstated if it treats obelisks as direct CP inputs.
- Exact CP impact can become stale if the CP formula changes.
- DB tuning can drift if not audited and versioned.
- Too many enabled categories can recreate the current shallow/filler problem.
- Economy advice can become wrong if it ignores heat number, non-linear credit growth, or
  valid early saving.
- Loadout stat advice can become a disguised part recommender if templates are too specific.
- Policy can become a hidden content system if it can introduce unsupported IDs, template
  keys, or metric arguments.
- On-demand analysis may become slow if comparator queries expand without indexes or
  materialization.

## Open Questions
- Should policy reload be request-time, TTL-cached, or admin-triggered?
- Which cautious categories should ship disabled by default versus absent from the seeded
  policy table?
- Should admin explain responses be stored for later audit, or generated only on demand?
- Should kudo repeat suppression consider recent prior kudos so the same player does not
  see the same praise too often?
- For the future capability-score phase, should Unreal author versioned capability scores, or
  should Eventun receive selected raw resolved stats and compute scores in Go?
- When should a detailed `PlayerLoadoutTransaction` event become mandatory instead of
  optional debug telemetry?
- If non-Ascent server modes need post-match insights in phase 1, which existing metrics are
  valid for those modes and which should return `unavailable`?
- If `time_trial_rank_improved` is desired earlier, where should pre-run rank be captured so
  the insight can prove rank improvement instead of only reporting current rank?

## External Patterns Consulted
- Dota Plus uses bracket-aware and context-aware comparison for suggestions and
  post-game analytics: https://www.dota2.com/plus
- Leetify uses calibrated benchmarks, z-scores, and transparent subratings:
  https://leetify.com/blog/cs2-benchmarks/
- Leetify also weights player impact by round context and win-probability swing:
  https://leetify.com/blog/leetify-rating-explained/
- Mobalytics turns performance gaps into structured improvement challenges:
  https://mobalytics.gg/blog/dev-blog-mobalytics-challenges/
- Chess.com Game Review combines key-moment analysis, positive move labels, and coaching:
  https://support.chess.com/en/articles/8584089-how-does-game-review-work
- Trackmania emphasizes personal bests, medals, records, and positive feedback:
  https://www.trackmania.com/news/8256
- AccelByte Extend service architecture supports the current Eventun Go/gRPC/gateway
  direction: https://docs.accelbyte.io/gaming-services/modules/foundations/extend/service-extension/
