# Eventun Challenges Game Client Integration Plan

## Goal

Integrate Eventun-owned challenge assignments and progress into the Ascent Rivals game client so the main UI can show the player's current challenge progress.

The V1 client surface should show:

- two daily challenges
- one weekly challenge
- current progress for each shown challenge
- enough challenge detail for the existing challenge route to show all currently assigned challenges

This replaces the current AccelByte Challenge API backed client path. Eventun remains the owner for challenge assignment, progress, completion, and rewards.

## Current Client State

The game client already has a dedicated challenge presentation seam:

- `UHGChallengesSubsystem`
- `FHGChallengesSnapshot`
- `FHGChallengeLaneView`
- `FHGChallengeGoalView`
- `UHGChallengesPreviewWidget`
- `UHGChallengeLaneWidget`
- `UHGChallengeButton`
- `UHGChallengesRoute`

This is the right client-side boundary to reuse. The widgets consume view models rather than raw AccelByte types, so the integration should replace the subsystem data source and mapping logic instead of rewiring widgets to generated Eventun models.

The current subsystem is still AccelByte Challenge shaped:

- fetch challenge catalog
- select active challenges
- fetch progress per challenge
- optionally fetch schedules
- build lanes and top goals

Eventun should collapse this to one logged-in player request for active assignments and progress.

## Eventun API Gaps

The generated game-client Eventun API currently includes:

```text
GET /v1/player/me/challenges/active?locale=en-US
```

Generated C++ method:

```cpp
AccelByte::Api::Eventun::ClientServiceMyActiveChallenges(...)
```

The current response returns `ProgressionGoal` rows. That is close, but not sufficient for a clean game-client integration.

### Required API Adjustment

`MyActiveChallenges` should return assigned challenge records, not only bare goals.

Recommended shape:

```proto
message MyActiveChallengesRequest {
  optional string locale = 1; // BCP 47, e.g. en-US. Omit for English/default.
}

message PlayerActiveChallenge {
  string assignment_id = 1;
  string assignment_status = 2; // active, completed, expired
  string scope = 3;             // daily, weekly, monthly, seasonal
  string period_id = 4;
  string period_key = 5;
  int32 period_starts_at_seconds = 6;
  int32 period_ends_at_seconds = 7;
  ProgressionGoal goal = 8;
  GoalRewardPreview reward_preview = 9;
}

message GoalRewardPreview {
  repeated GoalRewardPreviewEntry entries = 1;
}

message GoalRewardPreviewEntry {
  string type = 1;          // item, currency, battlepass_xp, title, custom, no_reward
  optional string label = 2;
  optional string item_sku = 3;
  optional string currency_code = 4;
  double quantity = 5;
}

message MyActiveChallengesResponse {
  repeated PlayerActiveChallenge challenges = 1;
}
```

The exact reward preview type can be adjusted to match existing Eventun reward structs, but the client should not need to parse opaque reward snapshot JSON just to display a short reward line.

### Required Backend Behavior

`MyActiveChallenges` should return all current-period assigned challenges that the player should still see, including completed assignments until the period expires.

The current backend query filters to active assignments and incomplete progress. That can make a challenge disappear immediately after completion, which is not the desired main-menu experience. It also makes the client unable to show a completed challenge in the same daily or weekly window.

For daily and weekly display, the endpoint should expose:

- assignment id
- assignment status
- pool scope
- period start/end
- period key
- locale-resolved goal title and description
- progress current value, target value, percent complete, and status
- reward preview

When a player has no current assignments, the endpoint should return a successful empty response:

```json
{ "challenges": [] }
```

### Nice-To-Have API Behavior

The endpoint may sort results server-side by:

1. scope priority: daily, weekly, monthly, seasonal
2. period start
3. assignment creation or deterministic assignment order
4. title

The game client should still apply its own display limits for the main preview.

## Client Architecture

Use `UHGChallengesSubsystem` as the Eventun-backed client owner for this slice.

Do not add a new `UHGGoalsSubsystem` only for this feature. A broader goals subsystem may make sense later when achievement galleries, reward claiming, and progression summaries become larger client features. For V1 challenge display, replacing the existing challenge subsystem keeps the integration focused and avoids a compatibility facade.

### Subsystem Responsibilities

`UHGChallengesSubsystem` should own:

- Eventun active challenge request lifecycle
- refresh state and stale-response protection
- mapping Eventun active challenge records into `FHGChallengeLaneView` and `FHGChallengeGoalView`
- snapshot caching
- update broadcasts for existing UI widgets
- feature flag and mock-data behavior if still needed for rollout

The subsystem should not own:

- reward claiming
- achievement gallery state
- Eventun match/event submission
- raw AccelByte Challenge service calls

### Data Source Changes

Remove AccelByte Challenge API dependencies from `UHGChallengesSubsystem`:

- `Models/AccelByteChallengeModels.h`
- `Api/AccelByteChallengeApi.h`
- `FAccelByteModelsChallenge`
- challenge catalog task
- per-challenge progress tasks
- schedule tasks
- AccelByte Challenge status and matcher helpers

Add Eventun dependencies in the `.cpp`:

- `Api/AccelByteEventunApi.h`
- `Models/AccelByteEventunModels.h`

Keep generated Eventun models out of the public header where possible. The public header should continue exposing game-client view models.

### Refresh Flow

`RefreshChallenges()` should:

1. cancel the outstanding Eventun request
2. increment the active refresh token
3. mark the snapshot refreshing
4. call `ClientServiceMyActiveChallenges`
5. map the response into lanes and preview goals
6. broadcast the updated snapshot

Failures should preserve the last successful snapshot when possible, clear the refreshing state, store an error message, and broadcast. The main UI should not block or crash if Eventun is unavailable.

### Login And UI Refresh Triggers

Refresh challenges:

- after login
- when the preview widget or challenges route appears and no snapshot is loaded
- when returning to the main menu after a match
- after Eventun match submission/progression processing is accepted or known ready

For the first V1 integration, it is acceptable to refresh after the match event batch is accepted and again when the main menu challenge preview appears. A later post-match progression summary surface can refresh after `MyMatchProgressionSummary` returns `ready`.

### Main Preview Selection

The main preview should not simply sort all goals by completion priority. It should intentionally show:

- up to two daily challenges
- up to one weekly challenge

If fewer than the target count are available, the preview may show fewer cards. A fallback fill from other scopes can be added later if product wants it, but the initial behavior should keep the daily/weekly contract obvious.

The full challenge route can show all returned current-period assignments grouped by scope.

### View Model Mapping

Map Eventun active challenge records to existing client view models:

- lane title: client-localized text from scope, such as `Daily Challenges`, `Weekly Challenges`, `Monthly Challenges`, or `Seasonal Challenges`
- lane period text/time remaining: from period start/end
- goal code: Eventun goal `code` if present, otherwise `publishedGoalId`
- challenge code: assignment id or period/scope key
- title: Eventun goal title resolved for the requested locale
- description: Eventun goal description resolved for the requested locale
- progress text: `current / target`, `Completed`, or a status fallback
- progress bar: clamp Eventun percent complete to `0..1`
- reward text: format from `GoalRewardPreview`
- completed state: assignment status or goal progress status is `completed`

The client should not parse requirement-expression JSON to compute V1 progress. Eventun should return display-ready progress numbers.

### Player-Facing Display Guidance

The current challenge UI mapping should be treated as the baseline:

```text
button title       <- resolved goal.title
button subtext     <- resolved goal.description
progress text      <- goal.progress.currentValue / targetValue, Completed, or status fallback
reward text        <- reward preview formatted by reward type
lane title         <- client-localized scope label
lane description   <- period/time presentation, not raw periodKey unless used as a debug fallback
```

Use Eventun goal `title` and `description` as authored player-facing copy. Do not generate player-facing challenge descriptions from requirement JSON in the game client for V1. Requirement-to-text generation may be useful later for admin preview, debugging, or missing-description fallback, but authored localized copy should be the primary game UI path.

Reward text needs type-specific handling:

- `battlepass_xp`: format with a client-localized `Battle Pass XP` label and quantity.
- `currency`: for V1, format ARC with a client-localized/fixed `ARC` label and quantity.
- `item`: prefer a localized AccelByte catalog or client catalog display name resolved from `item_sku`; fall back to Eventun `label`, then SKU, then a generic localized reward label.
- `no_reward`: hide reward text or show a client-localized no-reward treatment only if the UX explicitly wants one.
- `custom` or future types: use Eventun `label` as a fallback until the type has a dedicated client formatter.

`GoalRewardPreviewEntry.label` should be treated as an optional display hint or fallback, not proof that the reward is correctly localized. If Eventun later resolves reward labels for a requested locale, the API contract should make that explicit; until then, catalog-backed reward names should come from the catalog/client data path.

Lane description should not expose `periodKey` as polished player copy. The client should prefer period start/end, time remaining, or local UI labels such as `Today` / `This Week`. `periodKey` is useful for grouping, logging, and fallback debugging.

## Implementation Phases

### Phase 0: Eventun API Contract

- Add `PlayerActiveChallenge` style response data or equivalent fields.
- Include period scope and bounds.
- Include completed current-period assignments.
- Include reward preview data.
- Ensure progress defaults are useful when a progress row does not exist yet.
- Regenerate the game-client Eventun API code.

### Phase 1: Subsystem Refactor

- Refactor `UHGChallengesSubsystem` to call `ClientServiceMyActiveChallenges`.
- Remove AccelByte Challenge API request flow.
- Replace catalog/progress/schedule task state with one Eventun request task.
- Keep `FHGChallengesSnapshot`, `FHGChallengeLaneView`, and `FHGChallengeGoalView` unless the implementation finds a concrete mismatch.
- Keep or adapt mock data if the feature flag is still useful for rollout.

### Phase 2: UI Mapping

- Build lanes grouped by Eventun challenge scope.
- Build preview goals as two daily plus one weekly.
- Keep existing widgets consuming view models.
- Update empty/error/loading states if the new response shape makes any wording inaccurate.

### Phase 3: Post-Match Refresh

- Trigger a challenge refresh after Eventun accepts the completed match event batch.
- Prefer refreshing again when returning to the main menu or when a post-match progression summary later reports `ready`.
- Keep this refresh non-blocking.

### Phase 4: Cleanup

- Remove unused AccelByte Challenge includes, helper methods, state fields, and matcher code.
- Remove stale route assumptions that challenge data comes from AccelByte schedules.
- Keep file size under the existing project preference of roughly 1000 lines. The subsystem should shrink materially once the AccelByte multi-call flow is removed; split helper code only if it remains oversized.

### Phase 5: Verification

The coder should verify:

- login triggers active challenge fetch
- main preview shows two daily and one weekly when available
- completed current-period challenges remain visible as completed
- empty response shows the empty state
- Eventun error does not clear a previously useful snapshot unless intentionally chosen
- no AccelByte Challenge API calls remain in this client path
- post-match return can refresh challenge progress

## Review Checkpoint

Before game-client implementation starts, update Eventun if needed so `MyActiveChallenges` returns assigned challenge context rather than bare goals. Without scope and period data, the game client cannot reliably implement the two-daily-one-weekly preview or display reset timing.
