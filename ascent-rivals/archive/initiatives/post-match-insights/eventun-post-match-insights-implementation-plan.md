# Eventun Post-Match Insights Implementation Plan

Archive notice: Historical execution plan. Phases 1–7 were incorporated into current-system
knowledge; phase 8 was extracted to the active automatic-presentation follow-on.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement backend-owned post-run insights for Ascent Rivals so Eventun can return coaching insights, kudo insights, or factual no-insight/readiness states after post-match and time-trial runs.

**Architecture:** Build the backend contract, status model, policy storage, deterministic insight scoring, and admin explainability first. Then integrate generated SDKs and Unreal client telemetry/rendering against the completed backend contract. Reuse existing recommendation metric/snapshot internals only where they reduce risk, but replace the public recommendation API and player-facing flow with Insights.

**Tech Stack:** Eventun Go service, PostgreSQL migrations/functions, protobuf/gRPC-gateway/OpenAPI, AccelByte Extend app UI React/TypeScript, Unreal Engine C++, generated AccelByte Eventun SDK models/APIs.

---

## Status
Implemented through Phase 7. The unchecked task markers below are retained as the original
execution checklist and are not a reliable completion ledger. Phase 8 is the current approved
game-client follow-on; integrated manual validation remains outstanding.

## Source Documents
- Solution design: `ascent-rivals/initiatives/post-match-insights/eventun-post-match-insights-solution-design.md`
- Existing recommendation API design: `ascent-rivals/initiatives/post-match-insights/recommendation-api-engineering-design.md`
- Time-trial metrics design: `ascent-rivals/initiatives/post-match-insights/match-summary-time-trial-improvement-metrics.md`
- Eventun events reference: `ascent-rivals/system/eventun/events.md`

## Repository Boundaries
Use repo-relative paths in implementation notes and review comments.

- Eventun service repo: `github.com/ikigai-github/eventun`
- Game client repo: Ascent Rivals Unreal project
- Knowledge Base repo: this plan and the solution design only

Do not mix backend and game-client commits unless the repository owner explicitly wants a combined integration commit. The expected order is backend first, then generated SDK/client integration.

## Implementation Principles
- Keep the first implementation deterministic and inspectable. Do not introduce ML ranking.
- Do not preserve legacy recommendation APIs for backward compatibility. Remove old
  recommendation RPCs, OpenAPI paths, client calls, and obsolete process code as the insight
  replacement lands.
- Do not preserve proto field numbers, enum values, or declaration order for deleted legacy
  recommendation messages. Keep only the new insight contract stable once consumed by the
  game client.
- Keep generated IDs, enum values, and localization keys stable once the game client consumes them.
- Policy rows tune known insights only. Policy cannot introduce unknown insight IDs, metric IDs, template keys, or template arguments.
- Supported policy edits go through the admin API and Extend app UI. Direct DB edits are a
  trusted-operator escape hatch, not the normal implementation workflow.
- Every phase ends with review and cleanup before moving to the next phase.
- Final implementation review should include a simplification pass to reduce line count, merge
  unnecessary files, and remove legacy recommendation code that is no longer needed.

## Phase Map
| Phase | Owner | Outcome |
|---|---|---|
| 0. Readiness and contract review | Backend + client leads | Reviewed task boundary, replacement strategy, and accepted contract details. |
| 1. Eventun API contract and policy schema | Eventun coder | New insight protos, generated Go/OpenAPI code, policy/audit schema, seeded policy rows. |
| 2. Eventun insight engine thin slice | Eventun coder | Status-aware insight APIs, deterministic scoring, coaching + kudo candidates using existing telemetry. |
| 3. Eventun telemetry enrichment and economy/loadout inputs | Eventun + game telemetry coder | Heat-start economy/loadout fields flow from Unreal events into Eventun metrics. |
| 4. Eventun admin explainability and Extend app UI | Eventun coder | Admin policy/explain APIs and dashboard controls for policy tuning and debugging. |
| 5. Unreal client integration | Game client coder | Client requests insights, retries pending states, localizes/render slots, and submits new heat-start telemetry. |
| 6. End-to-end review and legacy cleanup | Backend + client leads | E2E validation, dead-code cleanup, legacy recommendation removal, final simplification pass. |
| 7. Course metadata sync and build-shape insights | Eventun coder, then client review if needed | Eventun syncs course definition context and replaces shallow death/crash/loadout-category coaching with specific Speed, Agility, and Combat insights where supported. |
| 8. Automatic pre-summary presentation | Game client coder | Ready insights appear before the normal match summary; every non-ready outcome advances directly to summary. |

## File Map

### Eventun Backend
- Create: `proto/ikigai/eventun/v1/insight.proto`
  - Add shared insight enums/messages used by client and admin APIs.
- Modify: `proto/ikigai/eventun/v1/match.proto`
  - Remove legacy `RunRecommendations*` messages once no remaining proto imports use them.
- Modify: `proto/ikigai/eventun/v1/client.proto`
  - Import `insight.proto`.
  - Add `GetPostMatchInsights`.
  - Add `GetTimeTrialInsights`.
  - Remove legacy post-match/time-trial recommendation RPCs instead of aliasing them.
- Modify: `proto/ikigai/eventun/v1/admin.proto`
  - Import `insight.proto`.
  - Add admin insight policy and explain RPCs.
- Modify generated files after codegen:
  - `gen/ikigai/eventun/v1/*`
  - `gen/0_eventun.swagger.json`
- Create: `migration/d2_insight_policy.sql`
  - Create `insight_policy`.
  - Create `insight_policy_audit`.
  - Seed conservative policy rows.
- Create/modify: course metadata migration
  - Store current AccelByte `Courses` game record context used by insights, including course
    code, options, role weights, sync timestamp, and source diagnostics.
- Modify: `migration/c5_func_recommendation.sql`
  - Add comparator/history heat-start economy/loadout category values used by post-match
    baselines.
- Modify: `migration/c6_func_recommendation_metrics.sql`
  - Add heat-start economy/loadout category values to recommendation/insight metric JSON when present.
- Modify: `migration/c7_func_recommendation_snapshot.sql`
  - Include new metric fields in snapshots used by insights.
- Create: `internal/eventun/insight_api.go`
  - Request validation, readiness/status mapping, and public client RPC handlers.
- Create: `internal/eventun/insight_catalog.go`
  - Known insight IDs, metric IDs, template keys, catalog status, required facts, and default suppression groups.
- Create: `internal/eventun/insight_policy.go`
  - Policy model, clamps, defaults, and validation against catalog.
- Create: `internal/eventun/insight_policy_db.go`
  - Policy load/update/audit queries.
- Create: `internal/eventun/insight_inputs.go`
  - Adapter from existing recommendation snapshots to insight input structures.
- Create: `internal/eventun/insight_candidates.go`
  - Coaching and kudo candidate generation.
- Create: `internal/eventun/insight_scoring.go`
  - Confidence, priority, suppression, cooldown hooks, and slot selection.
- Create: `internal/eventun/insight_admin_api.go`
  - Admin list/update policy and explain endpoints.
- Modify: `internal/eventun/client.go`
  - Wire client insight RPC methods into the Eventun service implementation.
- Modify: `internal/eventun/admin.go`
  - Wire admin insight RPC methods into the Eventun service implementation.
- Create tests:
  - `internal/eventun/insight_api_test.go`
  - `internal/eventun/insight_catalog_test.go`
  - `internal/eventun/insight_policy_test.go`
  - `internal/eventun/insight_scoring_test.go`
  - `internal/eventun/insight_admin_api_test.go`

### Eventun Extend App UI
- Modify after backend OpenAPI generation:
  - `app/src/eventunapi/generated-admin/*`
  - `app/src/eventunapi/generated-definitions/*`
- Modify: `app/src/shared/api/eventunClient.ts`
  - Add admin API accessor if codegen produces a new generated admin client.
- Modify: `app/src/shared/api/queryKeys.ts`
  - Add insight policy/explain query keys.
- Modify: `app/src/app/routes.tsx`
  - Add an Insights admin route.
- Create: `app/src/features/insights/InsightPoliciesPage.tsx`
  - Policy table, filters, enable/disable, weight/threshold editing.
- Create: `app/src/features/insights/InsightExplainPage.tsx`
  - Player/session/match explain form and candidate diagnostics.
- Create: `app/src/features/insights/insightMappers.ts`
  - UI-safe mapping and validation for policy form values.

### Unreal Game Client
- Modify generated SDK files after importing Eventun OpenAPI:
  - `Plugins/AccelByteUe4Sdk/Source/AccelByteUe4SdkCustomization/Public/Models/AccelByteEventunModels.h`
  - `Plugins/AccelByteUe4Sdk/Source/AccelByteUe4SdkCustomization/Public/Api/AccelByteEventunApi.h`
  - `Plugins/AccelByteUe4Sdk/Source/AccelByteUe4SdkCustomization/Private/Api/AccelByteEventunApi.cpp`
  - `spec/eventun.json`
  - `spec/Client/eventun.json`
  - `spec/Models/eventun.json`
- Modify: `Source/AscentRivals/Public/Net/HGEventunEvents.h`
  - Add heat-start telemetry fields to `FHGPlayerHeatStart_EventData`.
- Modify: `Source/AscentRivals/Private/Net/HGEventunEvents.cpp`
  - Update any explicit event serialization helpers if present.
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
  - Populate `creditsAtHeatStart` and category scores at `PlayerHeatStart`.
- Modify: `Source/AscentRivals/Private/Loadout/HGResolvedLoadout.cpp`
  - Add helper accessors only if existing category scores are not accessible where heat-start events are built.
- Modify: `Source/AscentRivals/Public/Client/HGStatsSubsystem.h`
  - Add insight stream and request methods.
- Modify: `Source/AscentRivals/Private/Client/HGStatsSubsystem.cpp`
  - Call new insight endpoints, preserve status/failure distinction, and expose retry inputs.
- Modify: `Source/AscentRivals/Public/UserInterface/Routes/HGPostMatchRecommendationRoute.h`
  - Rename recommendation-facing code to insight terminology where feasible.
  - If Unreal asset/class renames are content-heavy, document the temporary leftover name and
    remove all player-facing recommendation terminology.
- Modify: `Source/AscentRivals/Private/UserInterface/Routes/HGPostMatchRecommendationRoute.cpp`
  - Render insight response slots, status states, and localized template arguments.
- Modify: `Source/AscentRivals/Private/UserInterface/Routes/HGMatchSummaryRoute.cpp`
  - Rename visible button text to Insights and use insight request flow.

## Phase 0: Readiness And Contract Review

Reviewable outcome:
- Backend and client implementers agree on the exact insight proto contract, legacy replacement
  strategy, and phase boundaries before code starts.

- [ ] **Step 0.1: Review the solution design and existing code paths**

Read:
- `ascent-rivals/initiatives/post-match-insights/eventun-post-match-insights-solution-design.md`
- `proto/ikigai/eventun/v1/insight.proto` after Task 1.1 creates it
- `proto/ikigai/eventun/v1/client.proto`
- `proto/ikigai/eventun/v1/match.proto`
- `proto/ikigai/eventun/v1/admin.proto`
- `internal/eventun/client.go`
- `internal/eventun/admin.go`
- `internal/eventun/recommendation_api.go`
- `internal/eventun/recommendation_scoring.go`
- `Source/AscentRivals/Private/UserInterface/Routes/HGPostMatchRecommendationRoute.cpp`
- `Source/AscentRivals/Private/Client/HGStatsSubsystem.cpp`
- `Source/AscentRivals/Public/Net/HGEventunEvents.h`

Acceptance check:
- Implementer can explain current recommendation endpoint behavior, status gaps, client primary-promotion behavior, and heat-start telemetry gaps.

- [ ] **Step 0.2: Confirm legacy replacement strategy**

Decision to implement:
- Add new insight RPCs and data models.
- Remove legacy recommendation RPCs and response models instead of maintaining aliases.
- Do not wrap the new insight engine in the old recommendation response shape.
- Do not preserve proto index positions for removed recommendation fields/messages.
- Reuse existing internal SQL/snapshot helpers only while they remain useful implementation
  internals. Rename or delete them during cleanup once the insight engine owns the path.

Acceptance check:
- Implementer can list the public recommendation RPCs, generated SDK methods, backend
  handlers, and game-client call sites that will be removed or renamed.

- [ ] **Step 0.3: Confirm initial mode scope**

Decision to implement:
- Time trial insights support time-trial runs.
- Post-match insights initially support the same server-match mode coverage as the current post-match recommendation pipeline.
- Unsupported post-match modes return `UNAVAILABLE` with `UNSUPPORTED_MODE`.

Acceptance check:
- Backend tests cover unsupported post-match mode as `UNAVAILABLE`, not as a gRPC `FailedPrecondition`.

- [ ] **Step 0.4: Phase 0 review and cleanup**

Review:
- Confirm the plan still matches the solution design.
- Confirm no required client work starts before backend contract/codegen is complete.
- Update this plan if any Phase 0 decision changes the contract.

## Phase 1: Eventun API Contract And Policy Schema

Reviewable outcome:
- Eventun compiles with new insight protos and policy schema. The new APIs may return stubbed `UNAVAILABLE` or `NO_INSIGHT` responses until Phase 2 implements scoring.

### Task 1.1: Add Insight Proto Types

**Files:**
- Create: `proto/ikigai/eventun/v1/insight.proto`
- Modify: `proto/ikigai/eventun/v1/client.proto`
- Modify: `proto/ikigai/eventun/v1/admin.proto`

- [ ] **Step 1.1.1: Add enums**

Create `insight.proto` beside `match.proto`. Put shared insight enums and messages there,
then import it from `client.proto` and `admin.proto`. Move or delete legacy recommendation
messages when the old recommendation RPCs no longer need them.

Start the file with the same package and Go package conventions used by existing Eventun
protos:

```proto
syntax = "proto3";
package ikigai.eventun.v1;

option go_package = "github.com/ikigai-github/eventun";
```

Add these enums:

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

enum InsightId {
  INSIGHT_ID_UNSPECIFIED = 0;
  INSIGHT_ID_BEST_LAP_GAP = 1;
  INSIGHT_ID_COURSE_TIME_GAP = 2;
  INSIGHT_ID_CORNER_SPEED_GAP = 3;
  INSIGHT_ID_STRAIGHT_SPEED_GAP = 4;
  INSIGHT_ID_ENERGY_MANAGEMENT_GAP = 5;
  INSIGHT_ID_STALL_TIME_GAP = 6;
  INSIGHT_ID_CRASH_REDUCTION = 7;
  INSIGHT_ID_DEATH_REDUCTION = 8;
  INSIGHT_ID_WARP_USAGE_GAP = 9;
  INSIGHT_ID_LAP_CONSISTENCY_GAP = 10;
  INSIGHT_ID_LATE_ARC_INVESTMENT = 11;
  INSIGHT_ID_LOADOUT_VALUE_GAP = 12;
  INSIGHT_ID_MATCH_WINNER = 13;
  INSIGHT_ID_PODIUM_FINISH = 14;
  INSIGHT_ID_TOP_CIRCUIT_POINTS = 15;
  INSIGHT_ID_FASTEST_LAP = 16;
  INSIGHT_ID_PERSONAL_BEST_LAP = 17;
  INSIGHT_ID_PERSONAL_BEST_COURSE_TIME = 18;
  INSIGHT_ID_CLEAN_RACE = 19;
  INSIGHT_ID_SURVIVOR = 20;
  INSIGHT_ID_COMBAT_STANDOUT = 21;
  INSIGHT_ID_OBJECTIVE_STANDOUT = 22;
  INSIGHT_ID_ENERGY_EFFICIENCY_STANDOUT = 23;
  INSIGHT_ID_CONSISTENT_LAPS = 24;
  INSIGHT_ID_UNSPENT_ARC = 25;
  INSIGHT_ID_LOADOUT_CATEGORY_GAP = 26;
  INSIGHT_ID_EFFICIENT_SPENDER = 27;
}
```

- [ ] **Step 1.1.2: Add metric/template enums**

Add:

```proto
enum InsightMetricId {
  INSIGHT_METRIC_ID_UNSPECIFIED = 0;
  INSIGHT_METRIC_ID_TIME_MS = 1;
  INSIGHT_METRIC_ID_BEST_LAP_TIME_MS = 2;
  INSIGHT_METRIC_ID_FINISH_TIME_MS = 3;
  INSIGHT_METRIC_ID_AVERAGE_SPEED = 4;
  INSIGHT_METRIC_ID_CORNER_AVERAGE_SPEED = 5;
  INSIGHT_METRIC_ID_STRAIGHT_AVERAGE_SPEED = 6;
  INSIGHT_METRIC_ID_TIME_OUT_OF_ENERGY_MS = 7;
  INSIGHT_METRIC_ID_TIME_STALLED_MS = 8;
  INSIGHT_METRIC_ID_NUM_WARPS = 9;
  INSIGHT_METRIC_ID_LAP_VARIANCE_MS = 10;
  INSIGHT_METRIC_ID_PLACEMENT = 11;
  INSIGHT_METRIC_ID_CIRCUIT_POINTS = 12;
  INSIGHT_METRIC_ID_KILLS = 13;
  INSIGHT_METRIC_ID_DEATHS = 14;
  INSIGHT_METRIC_ID_CRASHES = 15;
  INSIGHT_METRIC_ID_OBELISKS = 16;
  INSIGHT_METRIC_ID_CREDITS_AT_HEAT_START = 17;
  INSIGHT_METRIC_ID_CREDITS_AT_HEAT_END = 18;
  INSIGHT_METRIC_ID_LOADOUT_VALUE_AT_HEAT_START = 19;
  INSIGHT_METRIC_ID_SPEED_SCORE = 20;
  INSIGHT_METRIC_ID_AGILITY_SCORE = 21;
  INSIGHT_METRIC_ID_COMBAT_SCORE = 22;
  INSIGHT_METRIC_ID_SPEED_AUGMENT_SCORE = 23;
  INSIGHT_METRIC_ID_AGILITY_AUGMENT_SCORE = 24;
  INSIGHT_METRIC_ID_COMBAT_AUGMENT_SCORE = 25;
  INSIGHT_METRIC_ID_WEIGHT = 26;
  INSIGHT_METRIC_ID_NORMALIZED_WEIGHT = 27;
}

enum InsightBenchmarkType {
  INSIGHT_BENCHMARK_TYPE_UNSPECIFIED = 0;
  INSIGHT_BENCHMARK_TYPE_CURRENT_MATCH_TOP_CP = 1;
  INSIGHT_BENCHMARK_TYPE_CURRENT_MATCH_LEADER = 2;
  INSIGHT_BENCHMARK_TYPE_CURRENT_MATCH_HIGH_CP_COHORT = 3;
  INSIGHT_BENCHMARK_TYPE_LOBBY_AVERAGE = 4;
  INSIGHT_BENCHMARK_TYPE_SELF_PERSONAL_BEST = 5;
  INSIGHT_BENCHMARK_TYPE_SELF_RECENT_RUNS = 6;
  INSIGHT_BENCHMARK_TYPE_TIME_TRIAL_LEADER = 7;
  INSIGHT_BENCHMARK_TYPE_COURSE_RECORD_LAP = 8;
  INSIGHT_BENCHMARK_TYPE_COURSE_RECORD_FINISH = 9;
}

enum InsightUnit {
  INSIGHT_UNIT_UNSPECIFIED = 0;
  INSIGHT_UNIT_TIME_MS = 1;
  INSIGHT_UNIT_SPEED_KPH = 2;
  INSIGHT_UNIT_COUNT = 3;
  INSIGHT_UNIT_PERCENT = 4;
  INSIGHT_UNIT_ARC = 5;
  INSIGHT_UNIT_SCORE = 6;
}

enum InsightConfidenceBand {
  INSIGHT_CONFIDENCE_BAND_UNSPECIFIED = 0;
  INSIGHT_CONFIDENCE_BAND_LOW = 1;
  INSIGHT_CONFIDENCE_BAND_MEDIUM = 2;
  INSIGHT_CONFIDENCE_BAND_HIGH = 3;
}

enum InsightTemplateArgKind {
  INSIGHT_TEMPLATE_ARG_KIND_UNSPECIFIED = 0;
  INSIGHT_TEMPLATE_ARG_KIND_METRIC = 1;
  INSIGHT_TEMPLATE_ARG_KIND_BENCHMARK_LABEL = 2;
  INSIGHT_TEMPLATE_ARG_KIND_LOCATION_LABEL = 3;
  INSIGHT_TEMPLATE_ARG_KIND_TEXT_KEY = 4;
}
```

- [ ] **Step 1.1.3: Add request/response messages**

Add:

```proto
message GetRunInsightsRequest {
  string player_id = 1;
  string session_id = 2;
  int32 match_id = 3;
  optional int32 max_insights = 4;
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

message InsightLocation {
  int32 heat = 1;
  int32 lap = 2;
  int32 checkpoint_start = 3;
  int32 checkpoint_end = 4;
  repeated string segment_tags = 5;
  string location_key = 6;
}

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
  InsightMetricId metric_id = 3;
  string text_key = 4;
}
```

Acceptance check:
- `RunInsight` has no role field.
- Slot assignment is represented only by `primary_insight` and `secondary_insights`.

### Task 1.2: Replace Client Recommendation RPCs

**Files:**
- Modify: `proto/ikigai/eventun/v1/client.proto`
- Modify: `proto/ikigai/eventun/v1/match.proto`

- [ ] **Step 1.2.1: Add insight RPCs and remove legacy recommendation RPCs**

Add:

```proto
rpc GetTimeTrialInsights(GetRunInsightsRequest) returns (GetRunInsightsResponse) {
  option (google.api.http) = {get: "/v1/match/insights/time-trial/player/{player_id}/session/{session_id}/match/{match_id}"};
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "Get time-trial insights for a completed run"
    description: "Returns coaching or kudo insights for a completed time-trial run"
    tags: ['Match']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}

rpc GetPostMatchInsights(GetRunInsightsRequest) returns (GetRunInsightsResponse) {
  option (google.api.http) = {get: "/v1/match/insights/post-match/player/{player_id}/session/{session_id}/match/{match_id}"};
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "Get post-match insights for a completed run"
    description: "Returns coaching or kudo insights for a completed post-match run"
    tags: ['Match']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}
```

Acceptance check:
- `TimeTrialRecommendations` and `PostMatchRecommendations` are removed from
  `ClientService`.
- Legacy recommendation request/response messages are removed from `match.proto` when no
  remaining proto file references them.
- Generated OpenAPI output does not expose legacy recommendation paths.

### Task 1.3: Add Admin Insight RPCs

**Files:**
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Use shared types from `proto/ikigai/eventun/v1/insight.proto`

- [ ] **Step 1.3.1: Add admin messages**

Add admin messages for policy and explain responses. Keep fields concrete:

```proto
message InsightPolicy {
  InsightId insight_id = 1;
  string mode = 2;
  bool enabled = 3;
  double base_weight = 4;
  double min_effect_size = 5;
  double min_confidence = 6;
  int32 min_benchmark_sample_count = 7;
  int32 min_required_samples = 8;
  double primary_salience_floor = 9;
  double secondary_salience_floor = 10;
  string suppression_group = 11;
  string diversity_group = 12;
  int32 cooldown_runs = 13;
  int32 max_per_response = 14;
  int32 scoring_version = 15;
}

message ListInsightPoliciesRequest {
  optional string mode = 1;
}

message ListInsightPoliciesResponse {
  repeated InsightPolicy policies = 1;
}

message UpdateInsightPolicyRequest {
  InsightPolicy policy = 1;
}

message UpdateInsightPolicyResponse {
  InsightPolicy policy = 1;
}

message ExplainRunInsightsRequest {
  string player_id = 1;
  string session_id = 2;
  int32 match_id = 3;
  string mode = 4;
}

message InsightCandidateExplain {
  RunInsight insight = 1;
  double priority_score = 2;
  double confidence_score = 3;
  repeated string suppression_reasons = 4;
  bool selected = 5;
}

message ExplainRunInsightsResponse {
  GetRunInsightsResponse player_response = 1;
  repeated InsightCandidateExplain candidates = 2;
  repeated string readiness_notes = 3;
  int32 scoring_version = 4;
}

message ListInsightPolicyAuditRequest {
  optional InsightId insight_id = 1;
  optional string mode = 2;
  optional int32 limit = 3;
}

message InsightPolicyAuditEntry {
  int64 id = 1;
  InsightId insight_id = 2;
  string mode = 3;
  string previous_policy_json = 4;
  string next_policy_json = 5;
  int64 changed_at_ms = 6;
  string changed_by = 7;
}

message ListInsightPolicyAuditResponse {
  repeated InsightPolicyAuditEntry entries = 1;
}
```

- [ ] **Step 1.3.2: Add admin RPCs**

Add to `AdminService`:

```proto
rpc ListInsightPolicies(ListInsightPoliciesRequest) returns (ListInsightPoliciesResponse) {
  option (google.api.http) = {get: "/v1/admin/insights/policies"};
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "List insight policies"
    description: "Lists post-run insight policy rows for admin tuning"
    tags: ['Insights']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}

rpc UpdateInsightPolicy(UpdateInsightPolicyRequest) returns (UpdateInsightPolicyResponse) {
  option (google.api.http) = {
    put: "/v1/admin/insights/policies"
    body: "*"
  };
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "Update an insight policy"
    description: "Updates a known insight policy row and records audit history"
    tags: ['Insights']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}

rpc ExplainRunInsights(ExplainRunInsightsRequest) returns (ExplainRunInsightsResponse) {
  option (google.api.http) = {get: "/v1/admin/insights/explain/player/{player_id}/session/{session_id}/match/{match_id}"};
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "Explain run insights"
    description: "Returns selected, rejected, and suppressed insight candidates for admin debugging"
    tags: ['Insights']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}

rpc ListInsightPolicyAudit(ListInsightPolicyAuditRequest) returns (ListInsightPolicyAuditResponse) {
  option (google.api.http) = {get: "/v1/admin/insights/policies/audit"};
  option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
    summary: "List insight policy audit history"
    description: "Lists audit entries for insight policy changes"
    tags: ['Insights']
    security: {
      security_requirement: {
        key: "Bearer"
        value: {}
      }
    }
  };
}
```

Acceptance check:
- Admin APIs are under `/v1/admin/insights/*`.
- Normal game client API does not expose raw scores or rejected candidates.

- [ ] **Step 1.3.3: Wire permission-gated admin stubs**

Add methods to `internal/eventun/admin.go` for each new admin RPC. Until Phase 4 implements
real policy/explain behavior, the methods should still pass through `apiActionWithPermission`
and `g.checkIsAdmin`, then return an explicit empty/stub response or `UNAVAILABLE`-style
application error chosen for admin APIs.

Acceptance check:
- New admin routes do not fall through to `pb.UnimplementedAdminServiceServer`.
- Unauthorized callers still fail permission checks before any stub response is returned.

### Task 1.4: Generate Eventun Go/OpenAPI Code

**Files:**
- Generated: `gen/ikigai/eventun/v1/*`
- Generated: `gen/0_eventun.swagger.json`

- [ ] **Step 1.4.1: Run Eventun codegen**

Run from Eventun repo root:

```bash
bun run gen
```

Expected:
- Go protobuf bindings update.
- OpenAPI output includes new client and admin insight paths.

- [ ] **Step 1.4.2: Run backend compile tests**

Run:

```bash
go test ./...
```

Expected at this point:
- Backend compile should pass after new insight methods are wired and removed legacy methods
  are deleted from service implementations.
- Do not leave missing method implementation failures for later phases.

### Task 1.5: Add Policy Schema

**Files:**
- Create: `migration/d2_insight_policy.sql`

- [ ] **Step 1.5.1: Create policy table**

Add:

```sql
CREATE TABLE IF NOT EXISTS insight_policy (
  insight_id TEXT NOT NULL,
  mode TEXT NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  base_weight NUMERIC NOT NULL,
  min_effect_size NUMERIC NOT NULL DEFAULT 0,
  min_confidence NUMERIC NOT NULL DEFAULT 0,
  min_benchmark_sample_count INTEGER NOT NULL DEFAULT 1,
  min_required_samples INTEGER NOT NULL DEFAULT 1,
  primary_salience_floor NUMERIC NOT NULL,
  secondary_salience_floor NUMERIC NOT NULL,
  confidence_weights JSONB NOT NULL DEFAULT '{}'::JSONB,
  benchmark_weights JSONB NOT NULL DEFAULT '{}'::JSONB,
  suppression_group TEXT,
  diversity_group TEXT,
  cooldown_runs INTEGER NOT NULL DEFAULT 0,
  max_per_response INTEGER NOT NULL DEFAULT 1,
  scoring_version INTEGER NOT NULL DEFAULT 1,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by TEXT,
  PRIMARY KEY (insight_id, mode),
  CHECK (base_weight >= 0.0 AND base_weight <= 3.0),
  CHECK (min_effect_size >= 0.0),
  CHECK (min_confidence >= 0.0 AND min_confidence <= 1.0),
  CHECK (min_benchmark_sample_count >= 1),
  CHECK (min_required_samples >= 1),
  CHECK (primary_salience_floor >= 0.0),
  CHECK (secondary_salience_floor >= 0.0),
  CHECK (cooldown_runs >= 0),
  CHECK (max_per_response >= 1 AND max_per_response <= 3)
);
```

- [ ] **Step 1.5.2: Create policy audit table**

Add:

```sql
CREATE TABLE IF NOT EXISTS insight_policy_audit (
  id BIGSERIAL PRIMARY KEY,
  insight_id TEXT NOT NULL,
  mode TEXT NOT NULL,
  previous_policy JSONB,
  next_policy JSONB NOT NULL,
  changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  changed_by TEXT
);

CREATE INDEX IF NOT EXISTS insight_policy_audit_lookup_idx
  ON insight_policy_audit (insight_id, mode, changed_at DESC);
```

- [ ] **Step 1.5.3: Seed conservative policy rows**

Seed rows for all Phase 1 default-enabled IDs and seed-disabled IDs. Use lowercase string IDs that match Go catalog constants exactly, for example:

```sql
INSERT INTO insight_policy (
  insight_id,
  mode,
  enabled,
  base_weight,
  min_effect_size,
  min_confidence,
  min_benchmark_sample_count,
  min_required_samples,
  primary_salience_floor,
  secondary_salience_floor,
  suppression_group,
  diversity_group,
  cooldown_runs,
  max_per_response,
  scoring_version
) VALUES
  ('match_winner', 'post_match', TRUE, 3.0, 0, 0.80, 1, 1, 1.0, 0.6, 'kudo_result', 'kudo', 3, 1, 1),
  ('podium_finish', 'post_match', TRUE, 2.3, 0, 0.75, 1, 1, 1.0, 0.6, 'kudo_result', 'kudo', 3, 1, 1),
  ('best_lap_gap', 'post_match', TRUE, 1.2, 0.05, 0.55, 1, 1, 0.7, 0.45, 'lap_time', 'pace', 2, 1, 1),
  ('best_lap_gap', 'time_trial', TRUE, 1.4, 0.05, 0.55, 1, 1, 0.7, 0.45, 'lap_time', 'pace', 2, 1, 1),
  ('unspent_arc', 'post_match', FALSE, 1.0, 0.10, 0.65, 3, 1, 0.8, 0.55, 'economy', 'economy', 2, 1, 1),
  ('efficient_spender', 'post_match', FALSE, 1.2, 0.10, 0.70, 3, 1, 0.9, 0.60, 'economy_positive', 'economy', 2, 1, 1)
ON CONFLICT (insight_id, mode) DO NOTHING;
```

Acceptance check:
- Disabled rows exist for telemetry-gated insights.
- Policy rows do not seed future/history-only insights such as `time_trial_rank_improved`,
  `segment_personal_best`, or `loadout_capability_gap`.

### Task 1.6: Phase 1 Review And Cleanup

- [ ] **Step 1.6.1: Review contract against solution design**

Check:
- Insight response has explicit statuses and status reasons.
- `READY` response has a primary slot.
- Non-ready responses have no slots.
- Admin explain response includes rejected candidates only in admin API.

- [ ] **Step 1.6.2: Run phase validation**

Run from Eventun repo root:

```bash
bun run gen
go test ./...
```

Run from Eventun app root after OpenAPI exists:

```bash
npm run cg:clean-and-generate
npm run build
```

Expected:
- Backend should pass with temporary insight method stubs returning `UNAVAILABLE` or
  `NO_INSIGHT` as appropriate.
- No legacy recommendation RPC should remain in generated client OpenAPI output.
- App build should pass after generated admin/client types are available.

Review checkpoint:
- Backend contract is stable enough for client SDK generation.
- No insight scoring logic has been added before policy validation and status contracts are in place.

## Phase 2: Eventun Insight Engine Thin Slice

Reviewable outcome:
- New client insight endpoints return deterministic statuses and selected slots using existing telemetry. Phase 2 does not require new heat-start telemetry.

### Task 2.1: Implement API Status Mapping

**Files:**
- Create: `internal/eventun/insight_api.go`
- Modify: `internal/eventun/client.go`
- Test: `internal/eventun/insight_api_test.go`

- [ ] **Step 2.1.1: Add request validation helper**

Implement:

```go
func validateRunInsightsRequest(request *pb.GetRunInsightsRequest) error {
	if strings.TrimSpace(request.PlayerId) == "" {
		return status.Error(codes.InvalidArgument, "player_id is required")
	}
	if strings.TrimSpace(request.SessionId) == "" {
		return status.Error(codes.InvalidArgument, "session_id is required")
	}
	if request.MatchId < 0 {
		return status.Error(codes.InvalidArgument, "match_id must be non-negative")
	}
	if request.MaxInsights != nil && *request.MaxInsights < 1 {
		return status.Error(codes.InvalidArgument, "max_insights must be positive when provided")
	}
	return nil
}
```

- [ ] **Step 2.1.2: Add status response helpers**

Implement:

```go
func insightStatusResponse(
	status pb.InsightResponseStatus,
	reason pb.InsightStatusReason,
	run *RecommendationRun,
) *pb.GetRunInsightsResponse {
	response := &pb.GetRunInsightsResponse{
		Status:       status,
		StatusReason: reason,
		ScoringVersion: "1",
	}
	if run != nil {
		response.CourseCode = run.CourseCode
		response.RaceMode = run.RaceMode
	}
	if status == pb.InsightResponseStatus_INSIGHT_RESPONSE_STATUS_PENDING {
		response.RetryAfterMs = 250
	}
	return response
}
```

- [ ] **Step 2.1.3: Add endpoint handlers**

Implement:

```go
func timeTrialInsights(ctx context.Context, conn *pgxpool.Conn, request *pb.GetRunInsightsRequest) (*pb.GetRunInsightsResponse, error) {
	return runInsights(ctx, conn, RecommendationModeTimeTrial, request)
}

func postMatchInsights(ctx context.Context, conn *pgxpool.Conn, request *pb.GetRunInsightsRequest) (*pb.GetRunInsightsResponse, error) {
	return runInsights(ctx, conn, RecommendationModePostMatch, request)
}
```

Wire these methods into `internal/eventun/client.go` in the same pattern as
`timeTrialRecommendations` and `postMatchRecommendations`.

- [ ] **Step 2.1.4: Add tests**

Tests:
- empty `player_id` returns `InvalidArgument`
- negative `match_id` returns `InvalidArgument`
- unsupported post-match mode returns `UNAVAILABLE` with `UNSUPPORTED_MODE`
- incomplete run returns `PENDING` with `DATA_NOT_READY` when Eventun can reasonably expect event data to complete
- completed run with no selected candidate returns `NO_INSIGHT`

Run:

```bash
go test ./internal/eventun -run 'TestInsightAPI' -count=1
```

### Task 2.2: Add Catalog And Template Contract

**Files:**
- Create: `internal/eventun/insight_catalog.go`
- Test: `internal/eventun/insight_catalog_test.go`

- [ ] **Step 2.2.1: Add catalog entry type**

Implement:

```go
type insightCatalogStatus string

const (
	insightCatalogDefaultEnabled       insightCatalogStatus = "default_enabled"
	insightCatalogAfterPhase1Telemetry insightCatalogStatus = "enabled_after_phase1_telemetry"
	insightCatalogSeedDisabled         insightCatalogStatus = "seed_disabled"
	insightCatalogFuture               insightCatalogStatus = "future"
)

type insightCatalogEntry struct {
	ID              pb.InsightId
	Key             string
	Type            pb.InsightType
	Modes           map[RecommendationMode]bool
	Status          insightCatalogStatus
	TitleKey        string
	BodyTemplateKey string
	RequiredMetrics []pb.InsightMetricId
	SuppressionGroup string
	DiversityGroup   string
}
```

- [ ] **Step 2.2.2: Add default catalog**

Add catalog rows for Phase 1 default-enabled coaching/kudos, telemetry-gated insights, and future insights listed in the solution design.

Acceptance check:
- `time_trial_rank_improved`, `segment_personal_best`, `major_improvement`, `first_finish`, and `smart_arc_use` are present only as future/disabled entries and cannot be selected by default.

- [ ] **Step 2.2.3: Add catalog tests**

Tests:
- every catalog entry has non-empty key/title/body.
- no duplicate string key.
- every default-enabled entry has a supported mode.
- every policy seed string in `migration/d2_insight_policy.sql` maps to a catalog entry.

Run:

```bash
go test ./internal/eventun -run 'TestInsightCatalog' -count=1
```

### Task 2.3: Implement Policy Loading And Validation

**Files:**
- Create: `internal/eventun/insight_policy.go`
- Create: `internal/eventun/insight_policy_db.go`
- Test: `internal/eventun/insight_policy_test.go`

- [ ] **Step 2.3.1: Add policy type and clamps**

Implement:

```go
type InsightPolicy struct {
	InsightKey              string
	Mode                    RecommendationMode
	Enabled                 bool
	BaseWeight              float64
	MinEffectSize           float64
	MinConfidence           float64
	MinBenchmarkSampleCount int32
	MinRequiredSamples      int32
	PrimaryThreshold        float64
	SecondaryThreshold      float64
	SuppressionGroup        string
	DiversityGroup          string
	CooldownRuns            int32
	MaxPerResponse          int32
	ScoringVersion          int32
}
```

Clamp rules:
- `BaseWeight`: 0.0 to 3.0
- `MinConfidence`: 0.0 to 1.0
- `MinBenchmarkSampleCount`: minimum 1
- `MinRequiredSamples`: minimum 1
- `CooldownRuns`: minimum 0
- `MaxPerResponse`: 1 to 3

- [ ] **Step 2.3.2: Add policy lookup**

Implement a loader that returns a map:

```go
type InsightPolicySet map[RecommendationMode]map[pb.InsightId]InsightPolicy
```

Rules:
- Unknown policy `insight_id` is ignored and logged.
- Missing policy row uses catalog default policy for default-enabled entries.
- Disabled policy row prevents candidate generation or selection.

- [ ] **Step 2.3.3: Add tests**

Tests:
- invalid policy key is rejected or ignored safely.
- disabled policy suppresses selected candidate.
- clamping prevents out-of-range values.
- missing policy for known default-enabled insight uses default.

Run:

```bash
go test ./internal/eventun -run 'TestInsightPolicy' -count=1
```

### Task 2.4: Build Insight Inputs From Existing Recommendation Snapshots

**Files:**
- Create: `internal/eventun/insight_inputs.go`
- Modify: `internal/eventun/recommendation_builders.go` only if shared snapshot loading needs a neutral name.

- [ ] **Step 2.4.1: Add input wrapper**

Implement:

```go
type RunInsightInputs struct {
	Mode          RecommendationMode
	Run           *RecommendationRun
	Current       *RecommendationMetrics
	PostMatch     *PostMatchRecommendationSnapshot
	TimeTrial     *TimeTrialRecommendationSnapshot
	Policy        InsightPolicySet
	ScoringVersion string
}
```

- [ ] **Step 2.4.2: Load existing snapshots**

Rules:
- Time trial uses `loadTimeTrialRecommendationSnapshot`.
- Post-match uses `loadPostMatchRecommendationSnapshot`.
- These recommendation-named snapshot loaders may remain temporarily as internal helpers.
  Public recommendation handlers/RPCs should already be removed.
- Rename loaders and SQL functions to insight terminology during the simplification pass if the
  rename reduces confusion without destabilizing the implementation.

Acceptance check:
- No duplicate SQL query path is introduced before the current recommendation snapshot path is proven insufficient.

### Task 2.5: Generate Coaching And Kudo Candidates

**Files:**
- Create: `internal/eventun/insight_candidates.go`
- Create: `internal/eventun/insight_scoring.go`
- Test: `internal/eventun/insight_scoring_test.go`

- [ ] **Step 2.5.1: Add candidate type**

Implement:

```go
type insightCandidate struct {
	Entry           insightCatalogEntry
	Benchmark       pb.InsightBenchmarkType
	Location        *pb.InsightLocation
	Metrics         []*pb.InsightMetric
	TemplateArgs    []*pb.InsightTemplateArg
	EffectSizeScore float64
	OutcomeRelevance float64
	BenchmarkRelevance float64
	ConfidenceScore float64
	SuppressionReasons []string
}
```

- [ ] **Step 2.5.2: Add default-enabled kudos first**

Implement these kudo generators before coaching:
- `match_winner`
- `podium_finish`
- `top_circuit_points`
- `fastest_lap`
- `personal_best_lap`
- `personal_best_course_time`
- `clean_race`
- `survivor`
- `combat_standout`
- `objective_standout`
- `energy_efficiency_standout`
- `consistent_laps`

Acceptance check:
- A match winner with fastest lap produces a kudo candidate with higher default priority than broad coaching.

- [ ] **Step 2.5.3: Add default-enabled coaching candidates**

Implement these coaching generators using current telemetry:
- `best_lap_gap`
- `course_time_gap`
- `corner_speed_gap`
- `straight_speed_gap`
- `energy_management_gap`
- `stall_time_gap`
- `crash_reduction` as fallback coaching
- `death_reduction` as fallback coaching
- `warp_usage_gap`
- `lap_consistency_gap`
- `late_arc_investment`
- `loadout_value_gap`

Rules:
- Do not generate `unspent_arc` until `creditsAtHeatStart` exists.
- Do not expose generic `loadout_category_gap` as player-facing coaching. Prefer later
  specific build-shape IDs once loadout category score fields and observed symptoms exist.
- Do not generate `loadout_capability_gap` until a future versioned capability-score phase
  defines and validates the scoring formula.
- Do not generate future/history-only insights.

- [ ] **Step 2.5.4: Implement scoring and slots**

Implement:

```go
func selectInsightSlots(candidates []*insightCandidate, policy InsightPolicySet, limit int) (*pb.GetRunInsightsResponse, []*insightCandidate)
```

Rules:
- Confidence gates and sample-count gates decide whether a candidate is credible enough to be
  considered.
- Candidate priority/salience uses `base_weight * effect_size_score * benchmark_relevance * outcome_relevance * mode_weight`.
- Primary requires the primary salience floor and at least medium confidence unless policy is stricter.
- Secondary requires the secondary salience floor and at least medium confidence unless policy is stricter.
- Salience floors should be low enough to avoid suppressing credible but modest insights when
  no stronger candidate exists; initial defaults should be about `0.35`-`0.40` primary and
  `0.30`-`0.35` secondary.
- Low confidence is never player-facing by default.
- Suppress duplicate suppression groups.
- Strong kudo can take primary over medium coaching.
- Never fill a slot with weak filler.

- [ ] **Step 2.5.5: Add scoring tests**

Tests:
- strong kudo outranks medium coaching.
- weak coaching does not fill primary.
- a credible medium-confidence time-trial gap below the old `0.70` threshold but above the
  salience floor returns `READY` with a primary insight.
- a very low-salience candidate, such as roughly `0.23`, still returns `NO_INSIGHT`.
- disabled policy suppresses candidate.
- duplicate suppression group selects only highest-scored candidate.
- no candidate returns `NO_INSIGHT`.
- ready response has primary and at most two secondaries.
- non-ready responses have no slots.

Run:

```bash
go test ./internal/eventun -run 'TestInsightScoring|TestInsightSlots' -count=1
```

### Task 2.6: Wire Insight APIs End To End

**Files:**
- Modify: `internal/eventun/insight_api.go`
- Modify: `internal/eventun/client.go`

- [ ] **Step 2.6.1: Implement `runInsights`**

Flow:
1. Validate request.
2. Load run with existing `queryRecommendationRun`.
3. Map unsupported mode to `UNAVAILABLE`.
4. Map incomplete run to `PENDING`.
5. Load policy.
6. Load snapshot.
7. Build candidates.
8. Select slots.
9. Return `READY` or `NO_INSIGHT`.

- [ ] **Step 2.6.2: Preserve transport errors**

Rules:
- Invalid argument remains gRPC `InvalidArgument`.
- Permission/auth failures remain transport errors.
- Database connectivity failures remain `Internal`.
- Only valid run-analysis outcomes become insight statuses.

- [ ] **Step 2.6.3: Run backend tests**

Run:

```bash
go test ./internal/eventun -run 'TestInsight' -count=1
go test ./...
```

### Task 2.7: Phase 2 Review And Cleanup

Review:
- Is insight code smaller and clearer than expanding `recommendation_scoring.go` further?
- Are default-enabled insights supported by current telemetry?
- Are telemetry-gated insights impossible to select?
- Are status responses factual and not hiding transport failures?

Cleanup:
- Move small helpers back into fewer files if the new files are too thin.
- Split only if a file becomes difficult to review.
- Delete public legacy recommendation API code once insight handlers cover the flow. Keep
  only internal metric/snapshot helpers that are still actively used.

## Phase 3: Telemetry Enrichment And Economy/Loadout Inputs

Reviewable outcome:
- Unreal emits heat-start economy/loadout summary fields, Eventun stores and exposes them in insight metric inputs, and telemetry-gated economy/loadout insights can be enabled conservatively.

### Task 3.1: Add Unreal Heat-Start Telemetry Fields

**Files:**
- Modify: `Source/AscentRivals/Public/Net/HGEventunEvents.h`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Modify: `Source/AscentRivals/Private/Loadout/HGResolvedLoadout.cpp` only if a small accessor is needed.

- [ ] **Step 3.1.1: Add event payload fields**

Add to `FHGPlayerHeatStart_EventData`:

```cpp
UPROPERTY()
int32 CreditsAtHeatStart = 0;

UPROPERTY()
int32 SpeedScore = 0;

UPROPERTY()
int32 SpeedAugmentScore = 0;

UPROPERTY()
int32 AgilityScore = 0;

UPROPERTY()
int32 AgilityAugmentScore = 0;

UPROPERTY()
int32 CombatScore = 0;

UPROPERTY()
int32 CombatAugmentScore = 0;
```

Acceptance check:
- Serialized JSON uses lower camel case names such as `creditsAtHeatStart`.

- [ ] **Step 3.1.2: Populate credits and category scores**

In the heat-start event construction in `HGRaceServerContext.cpp`:
- Set `CreditsAtHeatStart` from the racer's current credit balance after pre-heat purchases are locked.
- Use existing resolved loadout category score logic for Speed, Agility, and Combat.
- Keep `LoadoutValue`, `Weight`, and `NormalizedWeight` unchanged.

### Task 3.2: Add Eventun Metric Fields

**Files:**
- Modify: `migration/c5_func_recommendation.sql`
- Modify: `migration/c6_func_recommendation_metrics.sql`
- Modify: `migration/c7_func_recommendation_snapshot.sql`
- Modify: `internal/eventun/recommendation_metrics_db.go`
- Modify: `internal/eventun/recommendation_db.go`

- [ ] **Step 3.2.1: Add JSON extraction in SQL functions**

Add heat metric JSON keys:
- `credits_at_heat_start`
- `credits_at_heat_end`
- `loadout_value_at_heat_start`
- `speed_score`
- `speed_augment_score`
- `agility_score`
- `agility_augment_score`
- `combat_score`
- `combat_augment_score`
- `weight`, if not already present in the recommendation metric JSON
- `normalized_weight`, if not already present in the recommendation metric JSON

Rules:
- `credits_at_heat_end` comes from existing `PlayerHeatEnd.Credits`.
- `credits_at_heat_start` comes from `PlayerHeatStart.CreditsAtHeatStart`.
- Do not preserve old ambiguous `credits` JSON solely for compatibility. Keep it only while
  an internal helper still consumes it, and remove or rename it when that helper is migrated.
- In `c5_func_recommendation.sql`, extend `recommendation_post_match_baselines` and
  `recommendation_post_match_histories` so comparator and history JSON carries the same
  heat-start economy/loadout fields used by candidate generation.
- Same-heat baselines should include enough sample context for policy gates, including
  comparator count and high-CP/top-placement cohort values where available.
- In `c7_func_recommendation_snapshot.sql`, update the `jsonb_to_recordset` declarations for
  those `c5` functions so the new comparator fields survive into the snapshot.

- [ ] **Step 3.2.2: Add Go struct fields**

Add to `RecommendationHeatMetricInput`:

```go
CreditsAtHeatStart       int32   `json:"credits_at_heat_start"`
CreditsAtHeatEnd         int32   `json:"credits_at_heat_end"`
LoadoutValueAtHeatStart  int32   `json:"loadout_value_at_heat_start"`
SpeedScore               int32   `json:"speed_score"`
SpeedAugmentScore        int32   `json:"speed_augment_score"`
AgilityScore             int32   `json:"agility_score"`
AgilityAugmentScore      int32   `json:"agility_augment_score"`
CombatScore              int32   `json:"combat_score"`
CombatAugmentScore       int32   `json:"combat_augment_score"`
Weight                   float64 `json:"weight"`
NormalizedWeight         float64 `json:"normalized_weight"`
```

Add matching fields where the comparator JSON is unmarshaled:

- `RecommendationPostMatchHeatHistoryRun`
- `RecommendationLobbyHeatBaseline`
- any snapshot/benchmark struct added during the insight input adapter work

At minimum, post-match history and baseline structs need:

```go
CreditsAtHeatStart       int32   `json:"credits_at_heat_start"`
LoadoutValueAtHeatStart  int32   `json:"loadout_value_at_heat_start"`
SpeedScore               int32   `json:"speed_score"`
SpeedAugmentScore        int32   `json:"speed_augment_score"`
AgilityScore             int32   `json:"agility_score"`
AgilityAugmentScore      int32   `json:"agility_augment_score"`
CombatScore              int32   `json:"combat_score"`
CombatAugmentScore       int32   `json:"combat_augment_score"`
Weight                   float64 `json:"weight"`
NormalizedWeight         float64 `json:"normalized_weight"`
```

Same-heat baseline/cohort structs also need:

```go
ComparatorSampleCount    int32   `json:"comparator_sample_count"`
```

Acceptance check:
- Existing ambiguous `Credits` and `LoadoutValue` fields remain only while actively consumed
  by shared internal helpers. Remove or replace them once the insight-specific fields are in
  use.
- Same-heat comparator/history data includes the new heat-start fields before `unspent_arc`
  or `efficient_spender` can be enabled, and before Phase 7 build-shape insights can be
  generated.

### Task 3.3: Enable Conservative Economy/Loadout Insights

**Files:**
- Modify: `internal/eventun/insight_candidates.go`
- Modify: `migration/d2_insight_policy.sql`
- Test: `internal/eventun/insight_scoring_test.go`

- [ ] **Step 3.3.1: Enable `unspent_arc` only with new fields**

Generation gates:
- late heat or match-end context exists
- `creditsAtHeatStart` or `creditsAtHeatEnd` is materially high
- same-heat loadout value is below high-CP or top-placement comparators
- player did not earn an efficient-spender kudo

After tests pass, update seeded policy or an admin migration step so `unspent_arc` can be
enabled conservatively for post-match mode.

- [ ] **Step 3.3.2: Enable `efficient_spender` conservatively**

Generation gates:
- player has a strong outcome such as podium, high CP, fastest lap, or strong placement gain
- player's retained credits are not high relative to same-heat peers
- player's loadout value is not materially above same-heat high-CP comparators
- no stronger result kudo suppresses it

After tests pass, update seeded policy or an admin migration step so `efficient_spender` can
be enabled conservatively for post-match mode.

- [ ] **Step 3.3.3: Keep generic `loadout_category_gap` seed-disabled**

If the generic ID exists in the catalog during migration, do not expose it as a player-facing
insight. Keep candidate construction disabled or treat it only as an internal suppression
group until Phase 7 adds specific build-shape IDs.

The future specific insights should require observed weakness aligned with the category gap:
- lower Speed score plus pace/straight/warp weakness
- lower Agility score plus corner/control weakness
- lower Combat score plus death/combat-survivability weakness

Acceptance check:
- Admin explain can show why a generic category-gap candidate is unavailable or rejected.
- Player-facing response does not show generic category-gap insights.
- No capability-score insight is generated in phase 1.

### Task 3.4: Phase 3 Review And Cleanup

Review:
- Confirm `creditsAtHeatStart` and `creditsAtHeatEnd` are not confused in SQL, Go, or UI copy.
- Confirm telemetry payload did not balloon with raw stats.
- Confirm economy insights do not fire for time trial or noncompetitive modes.

Validation commands:

Eventun:

```bash
go test ./internal/eventun -run 'TestInsight|TestRecommendation' -count=1
go test ./...
```

Unreal:

```powershell
& "$env:UE_ENGINE_DIR\Engine\Build\BatchFiles\Build.bat" AscentRivalsEditor Win64 Development -Project="$pwd\AscentRivals.uproject" -WaitMutex
```

## Phase 4: Admin Explainability And Extend App UI

Reviewable outcome:
- Operators can view/edit policy, inspect candidate scoring, and distinguish no-insight from missing data or pending ingestion.

### Task 4.1: Implement Admin APIs

**Files:**
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Create: `internal/eventun/insight_admin_api.go`
- Modify: `internal/eventun/admin.go`
- Modify: `internal/eventun/insight_policy_db.go`
- Test: `internal/eventun/insight_admin_api_test.go`

- [ ] **Step 4.1.1: Implement list/update/audit**

Rules:
- Admin list returns policy rows sorted by mode then insight key.
- Admin policy rows include read-only insight type from the code-owned insight catalog, for
  example `InsightType type` on `InsightPolicy`. This type is derived server-side and is not
  stored in `insight_policy`.
- Update validates known insight ID and supported mode.
- Update clamps numeric values.
- Update ignores or validates the read-only policy type field without persisting it.
- Update writes audit row with previous and next policy JSON.
- Direct DB edits remain possible for trusted operators, but the implemented product path is
  admin API validation plus audit.

- [ ] **Step 4.1.2: Implement explain**

Explain response includes:
- player-facing response
- selected candidates
- rejected candidates
- priority/confidence scores
- confidence component breakdown when available
- suppression reasons
- readiness notes
- active scoring version

Rules:
- Explain endpoint is admin-only.
- Normal client endpoint never returns rejected candidates or raw scores.

### Task 4.2: Build Extend App UI Pages

**Files:**
- Modify: `app/src/shared/api/eventunClient.ts`
- Modify: `app/src/shared/api/queryKeys.ts`
- Modify: `app/src/app/routes.tsx`
- Create: `app/src/features/insights/InsightPoliciesPage.tsx`
- Create: `app/src/features/insights/InsightExplainPage.tsx`
- Create: `app/src/features/insights/insightMappers.ts`

- [ ] **Step 4.2.1: Regenerate app API client**

Run from Eventun app root:

```bash
npm run cg:clean-and-generate
```

- [ ] **Step 4.2.2: Add policy page**

UI requirements:
- table by mode and insight ID
- show the insight type as `Coaching` or `Kudo`; do not show raw enum IDs such as
  `INSIGHT_ID_EFFICIENT_LOW_LOADOUT_KUDO` as the prominent secondary text
- filter rows by type: all, coaching, or kudo
- add a quick sort control for current `baseWeight` descending so operators can quickly see
  the strongest configured insights first; table-column sorting may also remain available
- enabled toggle
- base weight
- min effect size
- min confidence
- primary and secondary salience floors
- benchmark sample count
- cooldown runs
- scoring version display

- [ ] **Step 4.2.3: Add explain page**

UI requirements:
- input fields: player ID, session ID, match ID, mode
- player-facing selected response panel
- candidate table with selected/rejected status
- show each candidate's type as `Coaching` or `Kudo` near the title; keep the raw insight ID
  available only as lower-priority debug detail if useful
- filter candidate rows by type: all, coaching, or kudo
- suppression reasons
- readiness notes

### Task 4.3: Phase 4 Review And Cleanup

Validation commands:

```bash
npm run lint
npm run build
```

Review:
- Admin UI does not expose template-key editing.
- Admin UI cannot create unknown insight IDs.
- Policy row type is server-derived from the insight catalog, not hard-coded separately in
  the Extend app UI.
- Type filtering works for both policy rows and explain candidates.
- Base-descending sort uses current editable policy `baseWeight` values and does not mutate
  policy state.
- Explain view is useful without becoming a full analytics dashboard.
- If the UI grows beyond this scope, split advanced diagnostics into a later phase.

## Phase 5: Unreal Client Integration

Reviewable outcome:
- The game client submits enriched heat-start telemetry, requests insight APIs from the
  manual Insights button entry, retries pending for a bounded window, and renders one
  primary plus up to two secondary insights using client-owned localization.

Implementation note, 2026-06-26:
- The Unreal client integration keeps `UHGPostMatchRecommendationRoute`,
  `HGPostMatchRecommendationRoute`, `RecommendationsButton`, and
  `SecondaryRecommendationHorizontalBox` as temporary technical names to avoid Unreal
  asset/content rename churn.
- `UHGStatsSubsystem` streams `FHGPostMatchInsightsResult` so transport/API failure is a
  client-side side channel, not a backend `NO_INSIGHT` status.
- The route treats backend `PENDING`, `NO_INSIGHT`, `UNAVAILABLE`, and `FAILED` distinctly,
  logs client pending timeouts separately, and renders manual-entry timeout/fallback as
  "No insights available".
- The manual-entry retry cap is three total requests, 2000 ms total wait, and
  `retry_after_ms` clamped to 150-500 ms with a 250 ms default.
- The client uses `Response.PrimaryInsight` directly and renders up to the first two
  `Response.SecondaryInsights`; it does not promote secondary insights to primary.
- Transport/API failures are retried within the same manual-entry cap instead of being
  cached as terminal backend statuses for later route openings.
- Secondary insight rendering preserves backend slot indices 0 and 1; invalid slots are
  hidden rather than compacting later response entries forward.
- The route config display name for `post-match-recommendation` is player-facing
  "Insights" while the route and widget technical names remain temporary.
- Heat-start telemetry now includes `CreditsAtHeatStart` plus Speed, Agility, and Combat
  tier and augment scores from `FHGResolvedLoadout::QueryCategoryScores`.
- The match summary route does not prefetch insights after Eventun submission acceptance;
  the post-match insights route owns the manual request/retry lifecycle after the player
  clicks the Insights button and ignores updates after a terminal UI state.
- The post-match insights header omits gap-to-first because match placement is CP/credits
  based while available finish times are best heat/course times, not a comparable ranking
  gap.

### Task 5.1: Import Generated Eventun SDK Changes

**Files:**
- Modify generated SDK/spec files under:
  - `spec/*.json`
  - `Plugins/AccelByteUe4Sdk/Source/AccelByteUe4SdkCustomization/*`

- [ ] **Step 5.1.1: Update Eventun OpenAPI specs**

Use the project's existing Eventun SDK import workflow to update:
- client insight endpoints
- admin insight models if the game repo carries shared model specs
- `GetRunInsightsResponse`, `RunInsight`, and insight enums

Acceptance check:
- `FAccelByteEventunGetRunInsightsResponse` or equivalent generated model exists.
- `ClientServiceGetPostMatchInsights` and `ClientServiceGetTimeTrialInsights` or equivalent generated API methods exist.

- [ ] **Step 5.1.2: Build generated SDK**

Run from Ascent Rivals repo root:

```powershell
& "$env:UE_ENGINE_DIR\Engine\Build\BatchFiles\Build.bat" AscentRivalsEditor Win64 Development -Project="$pwd\AscentRivals.uproject" -WaitMutex
```

### Task 5.2: Add Insight Request State In Stats Subsystem

**Files:**
- Modify: `Source/AscentRivals/Public/Client/HGStatsSubsystem.h`
- Modify: `Source/AscentRivals/Private/Client/HGStatsSubsystem.cpp`

- [ ] **Step 5.2.1: Add stream and request method**

Replace the old post-match recommendation stream with an insight stream:

```cpp
mutable TMap<FHGMatchKey, THotStream<FAccelByteEventunGetRunInsightsResponse>> PostMatchInsights;
```

Add methods:

```cpp
void SyncPostMatchInsights(const FString& SessionId, int32 MatchId, bool bUseTimeTrialEndpoint = false, int32 MaxInsights = 3);
void ClearPostMatchInsights(const FString& SessionId, int32 MatchId);
THotStream<FAccelByteEventunGetRunInsightsResponse>& GetPostMatchInsights(const FString& SessionId, int32 MatchId) const;
```

- [ ] **Step 5.2.2: Preserve errors distinctly**

Do not convert request failure into a default `READY` or empty response. Emit a response state or side-channel state that the route can distinguish from backend `NO_INSIGHT`.

Acceptance check:
- A backend `PENDING` response reaches UI as pending.
- A network/API error reaches UI as failure/timeout path, not no-insight.

### Task 5.3: Implement Client Retry State Machine

**Files:**
- Modify: `Source/AscentRivals/Public/UserInterface/Routes/HGPostMatchRecommendationRoute.h`
- Modify: `Source/AscentRivals/Private/UserInterface/Routes/HGPostMatchRecommendationRoute.cpp`

- [ ] **Step 5.3.1: Add retry state fields**

Add:

```cpp
int32 InsightRequestCount = 0;
double InsightRequestStartTimeSeconds = 0.0;
bool bInsightTimedOut = false;
```

- [ ] **Step 5.3.2: Apply retry caps**

Implement:
- max 3 total requests including first request
- manual entry cap: 2000 ms
- sleep from backend `retry_after_ms`, clamped to 150-500 ms, default 250 ms

Acceptance check:
- Manual entry shows neutral empty state on timeout.
- Timeout is logged separately from backend `NO_INSIGHT`.

### Task 5.4: Render Insight Slots And Localization

**Files:**
- Modify: `Source/AscentRivals/Private/UserInterface/Routes/HGPostMatchRecommendationRoute.cpp`

- [ ] **Step 5.4.1: Rename visible text**

Change player-facing labels:
- `Recommendations` -> `Insights`
- `Loading recommendations...` -> `Loading insights...`
- Manual empty state -> `No insights available`

- [ ] **Step 5.4.2: Render primary and secondary slots exactly**

Rules:
- Use `Response.PrimaryInsight` for the primary card.
- Use up to first two `Response.SecondaryInsights` for secondary cards.
- Do not promote a secondary insight to primary.
- `READY` with missing primary is treated as unavailable/failure and logged.

- [ ] **Step 5.4.3: Localize by insight ID/template key**

Add switch helpers:
- `GetInsightTitleText(InsightId, TitleKey)`
- `BuildInsightBodyText(RunInsight)`
- `GetInsightMetricLabelText(MetricId, LabelKey)`
- `GetInsightBenchmarkText(InsightBenchmarkType)`
- `FormatInsightMetricValue(InsightMetric)`

Rules:
- Prefer enum switches over string parsing.
- Use `LOCTEXT` for all player-facing text.
- If a required template argument is missing, show a neutral fallback and log warning.

### Task 5.5: Wire Match Summary Entry

**Files:**
- Modify: `Source/AscentRivals/Private/UserInterface/Routes/HGMatchSummaryRoute.cpp`

- [ ] **Step 5.5.1: Request insights after Eventun submission acceptance**

Initial rollout is manual-button entry. If the current match summary already prefetches
recommendations after Eventun submission acceptance, replace that prefetch with
`SyncPostMatchInsights`; otherwise request insights when the player clicks the Insights
button. Do not automatically route the player into the insights screen in phase 1.

- [ ] **Step 5.5.2: Update button label**

Set button text to:

```cpp
RecommendationsButton->SetText(LOCTEXT("ViewInsights", "Insights"));
```

The widget variable can remain named `RecommendationsButton` for the first pass to avoid asset churn.

### Task 5.6: Phase 5 Review And Cleanup

Validation commands:

```powershell
& "$env:UE_ENGINE_DIR\Engine\Build\BatchFiles\Build.bat" AscentRivalsEditor Win64 Development -Project="$pwd\AscentRivals.uproject" -WaitMutex
```

Manual checks:
- Time trial run returns insight or neutral empty state.
- Matchmade/custom Ascent run returns insight or neutral empty state.
- Unsupported post-match mode does not show broken UI.
- Pending response retries within cap.
- No client-side promotion from secondary to primary.
- Localization shows readable title/body/metrics.
- The player enters insights through the manual button, not automatic post-match routing.

Cleanup:
- Remove old recommendation SDK calls, streams, and helper functions.
- Rename local C++ helper functions from recommendation wording to insight wording.
- If class/asset renames create excessive Unreal content churn, leave only the minimum
  temporary technical name and document it for a dedicated content rename pass.

## Phase 6: End-To-End Review And Legacy Cleanup

Reviewable outcome:
- Backend and client run together, line count is reduced where the first implementation
  over-split, and obsolete recommendation APIs/processes are removed.

### Task 6.0: Correct Scoring Semantics

- [ ] **Step 6.0.1: Split credibility gates from salience ranking**

Eventun implementation must treat confidence as an evidence/credibility gate and priority as
salience for ordering eligible candidates. Do not reject an otherwise credible candidate only
because an old high primary threshold treated priority like confidence.

Required selector behavior:
- Apply hard eligibility gates first: enabled policy, required facts, minimum effect size,
  minimum confidence, minimum benchmark/sample counts, cooldown, and category-specific safety
  constraints.
- Compute priority/salience for eligible candidates using policy weight, effect size,
  benchmark relevance, outcome relevance, and mode weighting. Do not multiply by confidence
  again unless the implementation deliberately uses a soft, documented confidence adjustment.
- Select the highest-salience eligible candidate above `primary_salience_floor` as primary.
- Select secondary candidates above `secondary_salience_floor` after suppression/diversity.
- Keep floors low enough to suppress junk filler only. Suggested defaults are `0.35`-`0.40`
  primary and `0.30`-`0.35` secondary.

- [ ] **Step 6.0.2: Rename policy and explain terms**

Rename implementation, proto/admin fields, DB columns, and Extend app labels from overloaded
`primary_threshold` / `secondary_threshold` terminology to `primary_salience_floor` /
`secondary_salience_floor` unless a concrete migration constraint requires a temporary alias.
Backward compatibility is not required by default for this feature.

Explain output should distinguish:
- failed eligibility gate, such as insufficient confidence or insufficient benchmark samples
- selected/rejected by salience floor
- selected/rejected by suppression or diversity

Do not return `NO_INSIGHT` with only a `no_candidate_met_primary_threshold`-style reason when
eligible candidates exist above the salience floor.

- [ ] **Step 6.0.3: Add regression tests for the observed time-trial case**

Add deterministic tests for:
- a medium-confidence time-trial pace gap around the observed shape, such as confidence `0.55`
  and old priority near `0.58`-`0.63`, returning `READY` with a primary insight when it clears
  the salience floor
- a low-salience candidate around `0.23` returning `NO_INSIGHT`
- secondary selection still respecting suppression groups and secondary salience floor
- low-confidence candidates still suppressed even if their computed salience is high

### Task 6.1: End-To-End Scenario Matrix

- [ ] **Step 6.1.1: Validate backend scenarios**

Run:

```bash
go test ./...
```

Scenario coverage:
- ready with primary kudo
- ready with primary coaching
- ready with primary plus two secondaries
- no insight because no eligible candidate clears credibility gates or the low salience floor
- pending
- unavailable unsupported mode
- failed evaluator path
- policy disabled insight
- admin explain selected/rejected candidates

- [ ] **Step 6.1.2: Validate app UI**

Run from Eventun app root:

```bash
npm run lint
npm run build
```

- [ ] **Step 6.1.3: Validate Unreal client**

Run from Ascent Rivals repo root:

```powershell
& "$env:UE_ENGINE_DIR\Engine\Build\BatchFiles\Build.bat" AscentRivalsEditor Win64 Development -Project="$pwd\AscentRivals.uproject" -WaitMutex
```

Manual game validation:
- Submit match events.
- Enter insights through the manual button after accepted submission.
- Confirm pending retry does not exceed 1-2 seconds.
- Confirm manual entry empty behavior.
- Confirm generated telemetry appears in Eventun event JSON.

### Task 6.2: Simplification Pass

- [ ] **Step 6.2.1: Review backend line count and boundaries**

Look for:
- one-line wrappers that can be merged
- duplicate metric-format helpers
- catalog/policy code that can share validation helpers
- scoring functions that can be table-driven
- old recommendation helpers that are no longer used

Rules:
- Do not merge files if it makes review or tests less clear.
- Do not rewrite working SQL functions solely for style.

- [ ] **Step 6.2.2: Review client churn**

Look for:
- recommendation-named helper functions that now only handle insights
- duplicate formatting functions
- localizable text switches that can be grouped by insight ID
- dead recommendation code after all call sites use insights

### Task 6.3: Remove Legacy Recommendation Surface

- [ ] **Step 6.3.1: Remove backend public legacy APIs**

Remove:
- legacy recommendation RPCs from `client.proto`
- legacy recommendation request/response messages that are no longer referenced
- legacy recommendation OpenAPI paths from generated specs
- `PostMatchRecommendations` and `TimeTrialRecommendations` methods from
  `internal/eventun/client.go`
- obsolete recommendation API/scoring code that is not used by insight internals

Acceptance check:
- `rg -n "PostMatchRecommendations|TimeTrialRecommendations|RunRecommendation"` in Eventun
  returns no public API references.
- Any remaining `recommendation_*` SQL or Go helper is internal-only and has an explicit
  reason to stay until a later rename.

- [ ] **Step 6.3.2: Remove game-client legacy calls**

Remove:
- old Eventun SDK calls for recommendation endpoints
- old recommendation streams/cache entries in stats subsystems
- player-facing recommendation button/copy
- obsolete UI fallback logic that promoted secondary recommendations

Acceptance check:
- The game client requests only insight endpoints for this flow.
- Any remaining recommendation-named Unreal class/asset is a documented technical rename
  follow-up, not a separate product flow.

### Task 6.4: Final Implementation Review

Review checklist:
- No player-facing backend localization.
- Kudos are first-class backend-returned insights.
- Strong kudo can take primary.
- One primary plus up to two secondaries.
- No client primary promotion.
- Pending, no insight, unavailable, failed, and client timeout are distinct.
- Economy insights use `creditsAtHeatStart` and `creditsAtHeatEnd` correctly.
- Disabled/future insights cannot appear through policy edits.
- Admin UI cannot create unsupported IDs or template arguments.
- No exact part-buy recommendation appears in player-facing copy.
- No exact player-facing CP gain estimate appears.
- Phase 1 scope does not rely on ELO.

Final cleanup:
- Remove dead code.
- Reduce unnecessary adapter layers.
- Remove legacy recommendation RPC/process code rather than keeping aliases.
- Update KB docs with implementation deltas that differ from the design.
- Prepare a short rollout note for QA that lists expected insight statuses and test scenarios.

## Phase 7: Course Metadata Sync And Build-Shape Insight Upgrade

Reviewable outcome:
- Eventun can sync current course definition context from AccelByte and use it to improve
  insight confidence/salience.
- Generic death/crash/loadout-category coaching is replaced by more meaningful Speed,
  Agility, and Combat insights whenever the required evidence exists.
- Missing course metadata remains non-blocking.

### Task 7.1: Apply Current Insight Catalog Decisions

- [ ] **Step 7.1.1: Keep concrete existing insights**

Keep the existing concrete insight families:
- strong result and standout kudos
- best lap and course time gaps
- corner and straight segment speed gaps
- warp, energy, stall, and lap-consistency gaps
- late ARC investment, unspent ARC, efficient spender, and broad loadout value gap

Implementation notes:
- `loadout_value_gap` stays useful, but category-specific build-shape insights should outrank
  it when both explain the same weakness.
- `crash_reduction` and `death_reduction` remain fallback-only candidates.
- Generic `loadout_category_gap` should not be player-facing. Remove it from enabled policy
  rows or keep it only as an internal suppression/migration group.

- [ ] **Step 7.1.2: Update catalog, policy seeds, and localization keys**

Add explicit player-facing insight IDs:
- `speed_capability_gap`
- `agility_control_gap`
- `combat_survivability_gap`
- `combat_pressure_gap`
- `efficient_low_loadout_kudo`

Policy defaults:
- Seed disabled or very conservative until validated with explain output and local smoke
  tests.
- Put `agility_control_gap` in a suppression group with `crash_reduction`.
- Put `combat_survivability_gap` in a suppression group with `death_reduction`.
- Put build-shape coaching in a diversity group separate from economy/loadout-value coaching
  so a response does not overfill with build advice.

Acceptance check:
- Admin policy validation rejects unknown IDs.
- Game client localization can map every new template key and metric ID.
- No response exposes `loadout_category_gap` as a generic title or template.

### Task 7.2: Add Eventun Course Metadata Sync

- [ ] **Step 7.2.1: Add a course metadata table**

If Eventun already has a manually maintained course table, prefer migrating or extending it
instead of creating a parallel source of truth.

Recommended columns:
- `course_code` primary key
- `stat_code` nullable
- `course_version` nullable
- `feature_state` nullable
- `laps` nullable
- `target_lap_time` nullable
- `max_ascension_zones` nullable
- `options` JSONB
- `role_weights` JSONB
- `source_json` JSONB for diagnostics
- `synced_at` timestamp

Acceptance check:
- Upsert is idempotent.
- Missing optional fields do not fail sync.
- Role weight values are clamped or rejected if they are non-numeric or outside expected
  bounds.

- [ ] **Step 7.2.2: Sync from AccelByte `Courses` game record**

Implement a small sync path that fetches the same `Courses` game record consumed by the game
client. Use existing Eventun AccelByte configuration/client helpers if available.

Requirements:
- daily/background refresh if the service already has a scheduler
- admin-triggered refresh endpoint in the Extend app UI
- structured logs for record version, course count, changed courses, and failures
- no dependency on course metadata during player insight request evaluation

Acceptance check:
- Admin explain can report whether course metadata was available, missing, stale, or unused.
- A failed sync does not make post-match insight APIs fail.

### Task 7.3: Generate Build-Shape Candidates

- [ ] **Step 7.3.1: Add `speed_capability_gap`**

Generate only when:
- player Speed score is materially lower than same-heat high-CP/top-placement comparators
- an observed symptom aligns, such as straight speed gap, warp usage gap, best-lap gap, or
  course-time/pace gap
- benchmark sample count and confidence gates pass

Course speed-oriented role weights may increase salience. Missing role weights should not
block generation.

- [ ] **Step 7.3.2: Add `agility_control_gap`**

Generate only when:
- player Agility score is materially lower than same-heat comparators
- an observed symptom aligns, such as corner/bend segment gap, crashes, or poor controlled
  segment outcome
- benchmark sample count and confidence gates pass

When selected, suppress generic `crash_reduction` for the same run.

- [ ] **Step 7.3.3: Add `combat_survivability_gap` and `combat_pressure_gap`**

Generate survivability coaching only when:
- player Combat score is materially lower than same-heat comparators
- deaths, survival, or durability-adjacent outcome weakness is present
- benchmark sample count and confidence gates pass

Generate pressure coaching only when:
- player Combat score is materially lower than same-heat comparators
- low kills or low combat output appears meaningful for high-CP comparators
- survivability is not the clearer problem

When `combat_survivability_gap` is selected, suppress generic `death_reduction` for the same
run.

- [ ] **Step 7.3.4: Add `efficient_low_loadout_kudo`**

Generate only when:
- player achieved a strong result, strong CP, standout lap, or standout objective result
- player had lower loadout value or lower category score than same-heat comparators
- retained ARC was not simply unspent to a harmful degree

This is a kudo and may take primary if its confidence and salience beat coaching.

### Task 7.4: Apply Course Context Modifiers

- [ ] **Step 7.4.1: Use role weights as modifiers, not facts**

Rules:
- course role weights can raise salience/confidence when they agree with the observed symptom
- course role weights can lower confidence when they conflict with the observed symptom
- course role weights must never generate a candidate without observed performance evidence
- segment tags and same-run metrics should carry more weight than course-level archetypes

Acceptance check:
- Tests prove a course role weight alone does not create an insight.
- Tests prove missing course metadata still allows non-course-context insights.

### Task 7.5: Phase 7 Review And Cleanup

- [ ] **Step 7.5.1: Run backend validation**

The Eventun coder owns the final compile/test commands for this phase. Expected evidence:

```bash
go test ./internal/eventun -run 'TestInsight|TestCourse|TestRecommendation' -count=1
go test ./...
```

- [ ] **Step 7.5.2: Review with explain output**

Review admin explain output for:
- selected build-shape insight
- rejected build-shape insight due to missing observed symptom
- fallback `crash_reduction` selected when no agility/context evidence exists
- fallback `death_reduction` selected when no combat/context evidence exists
- course metadata available, missing, stale, and unused states

- [ ] **Step 7.5.3: Simplify after implementation**

Cleanup checklist:
- remove generic `loadout_category_gap` player-facing code if it exists
- avoid duplicate course metadata models
- keep AccelByte sync code small and isolated
- avoid reimplementing Unreal resolved-stat formulas in Eventun
- update this plan and the solution design if implementation constraints change the design

## Phase 8: Automatic Pre-Summary Presentation

Reviewable outcome:
- A completed final match shows a ready insight surface before the normal match summary.
- `NO_INSIGHT`, `UNAVAILABLE`, `FAILED`, client timeout, transport failure, rejected or
  missing submission state, and malformed ready responses advance directly to match summary.
- Non-final heat summaries keep their current behavior.

### Task 8.1: Centralize The Final Summary Transition

- [ ] **Step 8.1.1: Add one Insights-or-summary controller entry point**

Add a controller method such as `GoToPostMatchInsightsOrSummary(bool bAllowBack)` and use it
only for final-match transitions:

- the `UHGMatchCompleteMessage` timer/direct path used when no player-results route replaces it
- `UHGPlayerMatchResultsRoute::GoToMatchSummary()` in dedicated-server matches

Keep non-final `UHGHeatSummaryMessage` handling on `GoToMatchSummary(false)`.

The dedicated-server message order is significant: `MatchComplete` schedules the initial
transition, then `UHGStatsServerSubsystem::OnMatchFinished` sends `PlayerMatchResults`; both
currently use `ShowResultsTimer`, so the later player-results callback replaces the direct
summary callback. The normal server path is therefore montage, player results, Insights when
ready, then match summary. Standalone/time-trial paths may go directly from the finish delay to
the Insights-or-summary decision.

- [ ] **Step 8.1.2: Preserve route-stack semantics**

When leaving Insights, remove the Insights route before pushing the normal match summary. Do
not leave Insights beneath match summary. Do not blindly replace the active route either:
dedicated-server flow should retain `UHGPlayerMatchResultsRoute` beneath match summary when
`bAllowBack` is true.

Guard repeated input so one final match cannot push duplicate Insights or summary routes.

### Task 8.2: Prefetch From Accepted Submission

- [ ] **Step 8.2.1: Retain exact submitted-match identity**

When `UHGMatchEventunSubmissionMessage` arrives, retain its exact `SessionId`, `MatchId`, and
accepted state for the current completed match. Do not rebuild the request identity only from
the session entity's current match index; session state can advance independently of the
completed submission being presented.

Reset this retained state at the next match boundary or when finished-screen state is cleared.

- [ ] **Step 8.2.2: Start insight prefetch on acceptance**

When submission is accepted, call `SyncPostMatchInsights` with the correct post-match versus
time-trial endpoint. This lets Eventun ingestion/retry latency overlap the montage and player
results screen.

At the final transition:

- rejected or missing submission state goes directly to match summary
- a cached `READY` response can render immediately
- cached `PENDING` or an unresolved accepted request may use the existing bounded retry window
- cached terminal non-ready states go directly to match summary

Do not add a second independent retry state machine in the player controller.

### Task 8.3: Add Automatic Route Behavior

- [ ] **Step 8.3.1: Pass explicit automatic-flow parameters**

Pass route parameters for automatic entry and the existing `bAllowBack` summary behavior. Move
the current session/match/course/finish/placement parameter construction out of
`UHGMatchSummaryRoute::ViewInsights()` so the final-flow controller owns it once.

- [ ] **Step 8.3.2: Auto-advance every non-ready outcome**

In automatic mode, route all of the following through one `ContinueToMatchSummary` helper:

- backend `NO_INSIGHT`, `UNAVAILABLE`, or `FAILED`
- client request timeout or transport/API failure after the bounded retry policy
- missing route/request context
- `READY` without a valid primary insight

The existing `EmptyInsightsWindowPanel` may remain only for an explicitly retained manual or
debug entry. If no such entry remains, remove the unused empty-state branch during cleanup.

- [ ] **Step 8.3.3: Continue after a ready insight**

Bind a Continue action that removes the Insights route and asks
`AHGPlayerController_Race` to open the normal match summary with the preserved `bAllowBack`
value. Treat Back the same as Continue in automatic mode so the player cannot loop back into
the pre-summary gate.

### Task 8.4: Blueprint And Legacy Entry Cleanup

- [ ] **Step 8.4.1: Update `PostMatchRecommendation_WBP`**

Required Blueprint work:

- add a visible `UHGTextButton` named `ContinueButton`
- bind it to the new C++ `BindWidget` property
- use player-facing text `Continue` or `Match Summary`
- make it the desired focus target for keyboard/gamepad navigation
- verify one primary with zero secondary cards still leaves the action reachable

No new route asset or route configuration is required.

- [ ] **Step 8.4.2: Remove manual match-summary entry**

Remove the obsolete `RecommendationsButton` from `MatchSummaryRoute_WBP` and remove its C++
binding, click handler, submission-state subscription, and `ViewInsights()` parameter builder.
Backward compatibility for the manual entry flow is not required.

The remaining `PostMatchRecommendation` native class/asset/route-key names are documented
technical debt. Rename them only if the Unreal asset/class migration can be performed cleanly
in the same change; the rename is not required for the behavior change.

### Task 8.5: Review And Validation

The game-client coder owns compilation and runtime validation. Required evidence:

- dedicated-server custom match with bots: player results, ready Insights, Continue, summary
- dedicated-server no-insight response: player results then summary without empty Insights
- standalone/time trial ready response: ready Insights then summary
- standalone/time trial no-insight/timeout: summary without empty Insights
- Eventun submission rejected or absent: summary without an insight request loop
- backend transport failure: bounded wait then summary
- non-final heat: existing heat summary only
- repeated Continue/Back input: no duplicate routes
- summary Back behavior still returns to player results where previously allowed

After validation, remove duplicate flow helpers and any manual-entry-only state that no longer
has a caller.

## Known Implementation Risks
- Proto enum names may need minor adjustment to match existing generated SDK naming conventions.
- Unreal SDK generation can create wider diffs than hand-written code; review generated files separately.
- Capability scores are useful only after validation. Keep them out of phase 1 implementation
  until a versioned formula and sample data prove they are stable.
- Admin policy editing can become too broad. Keep it to numeric tuning, enablement, and suppression/cooldown controls.
- Internal recommendation-named snapshot helpers can confuse future work if they survive too
  long. Rename or delete them once the insight path is stable.
- Course metadata sync should not become a second source of truth for course design. Eventun
  consumes current AccelByte course data for insight context only.
- Course role weights are authored map archetype hints, not proof of player weakness. Keep
  observed symptoms and comparator data as hard requirements for build-shape insights.

## Final Handoff
Plan complete when:
- Phase 1-8 outcomes are implemented or explicitly deferred with a documented reason.
- Backend tests, app build, and Unreal build have been run for the final integrated state.
- Reviewers have completed the final implementation review and simplification pass.
- Any final design deltas are reflected in the Knowledge Base.
