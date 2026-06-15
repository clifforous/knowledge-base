# Eventun Extend App UI Progression Authoring Design and Implementation Plan

Status: Draft
Date: 2026-06-12
Primary repository: `github.com/ikigai-github/eventun`
UI path: `eventun/app`
Related designs:

- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-requirements.md`
- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design.md`
- `30_designs/ascent-rivals/eventun-extend-app-ui-progression-admin-design-plan.md`

## Purpose

Define the operator workflow, backend API additions, frontend structure, and implementation sequence for creating and maintaining Eventun achievements, masteries, challenges, challenge pools, and rewards through the AccelByte Extend App UI.

This document is a follow-on to the initial Extend App UI spike. It changes the previous V1 non-goal of "no dedicated admin UI" into active follow-on work for Eventun progression operations.

## Goals

- Create achievements, masteries, and challenge goal definitions.
- Edit existing goals through draft mutation or new immutable versions, depending on goal status.
- Manage daily, weekly, monthly, and seasonal challenge pools.
- Add and validate inline rewards while authoring goals.
- Optionally manage reusable reward bundles.
- Support low-click bulk workflows for seasonal challenge setup and adjustment.
- Support CSV import/export as a first-class authoring workflow.
- Add Eventun backend admin APIs where the current API surface is not shaped for operator UI workflows.

## Non-Goals

- No player-facing progression UI in this App UI.
- No replacement of game-client reward claim UX.
- No direct AccelByte catalog mutation from the frontend.
- No custom expression language for goal requirements.
- No nested mixed boolean requirement trees in the first authoring UI.
- No challenge reroll management UI.
- No limited-supply reward management UI.
- No automatic retroactive completion UI until the backend backfill/repair job surface is explicitly available.

## Existing Context

The Eventun progression solution already defines:

- Versioned goals for achievements, masteries, and challenges.
- A validated JSON requirement tree with one root `all` or `any` operator and leaf requirements.
- Inline rewards as the default admin authoring path, stored as generated reward bundle definitions.
- Reusable reward bundles for repeated reward packages.
- Challenge pools, pool goals, periods, assignments, weights, cooldowns, and eligibility.
- Definition import preview/apply APIs using `DefinitionImportGoalRow`.

The current App UI already has:

- React, Ant Design, Tailwind, React Query, and AccelByte App UI SDK wiring.
- Generated TypeScript clients under `eventun/app/src/eventunapi`.
- A minimal connectivity page that calls `ListProgressionMetrics`.

The current backend admin API has useful pieces:

- `ListProgressionMetrics`
- `CreateGoal`
- `CreateGoalVersion`
- `ActivateGoalVersion`
- `ListRewardCatalogTargets`
- `ValidateRewards`
- `CreateRewardBundleDefinition`
- `GetRewardBundleDefinition`
- `ListRewardBundleDefinitions`
- `CreateDefinitionImport`
- `GetDefinitionImport`
- `ApplyDefinitionImport`
- `ListPlayerRewardBundles`
- `RetryRewardBundle`

Known API gaps for a proper operator UI:

- Admin-grade progression goal list/detail APIs are missing. `ListProgressionGoals` exists on the client service and is not sufficient for drafts, inactive goals, versions, rewards, and pool membership context.
- Challenge pool administration APIs are missing.
- Challenge pool goal administration APIs are missing.
- A no-write validation endpoint for goal drafts would reduce noisy saved import previews during interactive editing.
- Status transition APIs for inactive/retired goals and pools should be explicit rather than relying on SQL.

## Product Model

### Goal

A goal is one achievement, mastery, or challenge definition. The UI should present these as one shared model with kind-specific filters and defaults.

Goal lifecycle:

- `draft`: editable metadata and draft versions.
- `active`: current version is live; edits create a new version.
- `inactive`: not currently live; edits still create versions unless backend rules allow draft-only changes.
- `retired`: read-only except support inspection.

### Challenge

A challenge is a goal with `kind='challenge'`. It becomes assignable only when an active goal version is linked into an active challenge pool.

The UI must therefore distinguish:

- challenge goal definition
- active goal version
- challenge pool membership
- player assignment generated from that pool membership

### Reward

Inline rewards are the normal authoring path. The UI may also attach an existing reusable reward bundle.

Rules:

- Operators should work with SKU, currency code, and normalized Eventun reward targets.
- Eventun validates reward entries against local rules and AccelByte catalog state.
- The frontend does not store AccelByte secrets and does not call AccelByte catalog APIs directly.

## Information Architecture

Use a workbench-style UI with persistent navigation:

1. **Goals**
   - Combined table for achievements, masteries, and challenges.
   - Filters by kind, category, status, metric, SKU, reward type, pool membership, and text.
   - Detail drawer for create/edit/version workflows.
   - Bulk actions and CSV export.

2. **Challenge Pools**
   - Table of daily, weekly, monthly, and seasonal pools.
   - Pool detail drawer with linked challenge goal versions.
   - Pool health and assignability warnings.

3. **Rewards**
   - Catalog target lookup.
   - Reusable reward bundle management.
   - Reward validation checks.

4. **Imports**
   - CSV paste/upload.
   - Import preview.
   - Apply confirmation.
   - Export templates.

5. **Support**
   - Earned reward inspection and retry can remain a secondary page because it is not part of authoring.

## UX Principles

- Optimize for seasonal setup and bulk adjustment.
- Avoid forcing operators through one wizard per challenge.
- Use tables, drawers, tabs, tags, filters, and inline validation in the AccelByte Admin Portal style.
- Keep primary table density high enough for scanning dozens of goals.
- Make versioning visible. Operators should understand when an edit creates a new version.
- Make pool membership visible for challenge goals. A challenge without active pool membership is not assignable.
- Keep reusable reward bundles optional. They are useful for repeated packages, not required for the common single-reward case.
- Treat AccelByte namespace as Eventun deployment context, not editable authoring data.
- Use import preview for bulk validation. Never apply CSV changes without an explicit confirmation step.

## Goals Workbench

### Table Columns

Minimum columns:

- `kind`
- `category`
- `title`
- `status`
- `current_version`
- `visibility`
- `requirement_summary`
- `reward_summary`
- `challenge_pool_summary`
- `active_from`
- `active_until`
- `updated_at`

Optional hidden/export columns:

- `goal_id`
- `version_id`
- `operator_key`
- `counting_policy`
- `presentation_json`
- `requirement_json`
- `reward_bundle_definition_id`

### Filters

- kind: achievement, mastery, challenge
- status: draft, active, inactive, retired
- category
- visibility
- metric code
- dimension key/value, especially SKU and medal name
- reward type
- reward SKU/currency
- challenge pool
- text search across title, operator key, and description

### Detail Drawer

Use a drawer rather than a full page so the operator keeps table context.

Sections:

- Identity: kind, category, operator key, status.
- Presentation: title, description, visibility, asset/presentation metadata.
- Requirement builder.
- Rewards.
- Challenge pool memberships for challenge goals.
- Version history.
- Validation results.

### Editing Rules

- New goal: create goal, create draft version, optionally activate.
- Draft goal: allow changing draft-only metadata and creating/replacing draft versions according to backend rules.
- Active or inactive goal: edits create a new version. The previous active version remains historical.
- Retired goal: read-only in this UI.
- Activating a version must run backend requirement and reward validation.

## Requirement Builder

Use a structured builder for the V1 requirement tree.

Controls:

- Root operator: segmented control with `All` and `Any`.
- Requirement rows:
  - metric
  - matcher
  - target
  - dynamic dimensions
  - remove/duplicate row actions

Metric behavior:

- Load active metrics from `ListProgressionMetrics`.
- Dimension controls are generated from `allowed_dimensions`.
- Dimension values use stable identifiers, preferably SKU for items and medal names for medals.
- Target input type follows metric `value_type`.
- Matcher options are constrained by metric `value_type`.

Generated JSON shape:

```json
{
  "operator": "all",
  "requirements": [
    {
      "metric": "medal.count",
      "matcher": "greater_than_or_equal",
      "target": 10,
      "dimensions": {
        "medal_name": "double_kill",
        "weapon_sku": "weapon_smg_01"
      }
    }
  ]
}
```

V1 constraints:

- One root operator.
- One or more leaf rows.
- No nested operators.
- No raw SQL.
- No semantic expression parser.

## Reward Authoring

Inline reward rows should be embedded in the goal drawer.

Reward row controls:

- reward type: item, currency, battlepass XP, future custom
- catalog target search for item rewards
- currency code for ARC
- quantity
- fulfillment mode: claimable or automatic
- duplicate policy
- metadata preview

Reward authoring should not expose an AccelByte namespace field. Catalog targets are resolved and validated against Eventun's configured namespace.

Operators can either:

- add inline reward rows, which Eventun stores as `generated_goal_reward`
- attach an existing reusable reward bundle

Validation:

- Validate inline rewards before save.
- Validate linked reusable bundles before activation.
- Show missing SKU, non-grantable item, inactive catalog target, and invalid quantity at row level.

## Challenge Pool Management

### Pool List

Columns:

- scope: daily, weekly, monthly, seasonal
- operator key
- status
- assignment count
- reset timezone
- repeat policy
- active goal count
- assignability status
- updated at

### Pool Detail Drawer

Pool fields:

- operator key
- scope
- assignment count
- reset timezone
- repeat policy
- status

Pool goal table:

- goal title
- goal id
- version
- category
- weight
- cooldown periods
- eligibility summary
- active flag
- validation state

Pool health checks:

- Active daily/weekly/monthly pools should have at least `assignment_count` active selectable goals.
- Seasonal pools may have `assignment_count=0` and use all active pool goals.
- Inactive, retired, missing, or invalid goal versions should be flagged.
- Item-specific eligibility should be flagged as unsupported for assignment until ownership-aware assignment is active.
- If every otherwise eligible challenge is on cooldown, assignment logic falls back by ignoring cooldown. The UI should still show the cooldown configuration.

## CSV and Bulk Editing

CSV import/export should map to the same model used by the structured editor.

### Goal CSV

Recommended columns:

- `row_key`
- `goal_id`
- `operator_key`
- `kind`
- `category`
- `title`
- `description`
- `visibility`
- `counting_policy`
- `active_from`
- `active_until`
- `presentation_json`
- `requirement_operator`
- `requirement_1_metric`
- `requirement_1_matcher`
- `requirement_1_target`
- `requirement_1_dimensions_json`
- repeated requirement columns as needed
- `reward_bundle_definition_id`
- `reward_fulfillment_mode`
- `reward_bundle_title`
- `reward_duplicate_policy`
- `reward_1_type`
- `reward_1_item_sku`
- `reward_1_currency_code`
- `reward_1_quantity`
- `reward_1_metadata_json`
- repeated reward columns as needed

Do not add reward namespace columns to goal CSVs. Reward targets are implicitly in the AccelByte namespace configured for the Eventun deployment that processes the import.

The frontend can parse CSV into `DefinitionImportGoalRow[]` and call the existing definition import preview/apply APIs. Server-side CSV parsing is not required for the first UI if frontend parsing is deterministic and export uses the same columns.

### Challenge Pool CSV

Recommended columns:

- `pool_id`
- `pool_operator_key`
- `scope`
- `pool_status`
- `assignment_count`
- `reset_timezone`
- `repeat_policy`
- `goal_version_id`
- `weight`
- `cooldown_periods`
- `eligibility_json`
- `active`

Challenge pool CSV requires new Eventun admin APIs or a dedicated import endpoint because the current definition import model only handles goal rows.

### Bulk Edit

Bulk edit should operate on selected grid rows and generate the same internal payloads as CSV/import:

- duplicate selected goals
- set category
- set visibility
- set counting policy
- attach reward bundle
- add inline reward
- add selected challenge versions to a pool
- set pool goal weight/cooldown/active flag

## Backend API Design

### Admin Goal APIs

Add admin goal list/detail APIs. These should be distinct from client progression APIs.

Proposed RPCs:

```proto
rpc ListAdminProgressionGoals(ListAdminProgressionGoalsRequest) returns (ListAdminProgressionGoalsResponse);
rpc GetAdminProgressionGoal(GetAdminProgressionGoalRequest) returns (GetAdminProgressionGoalResponse);
rpc UpdateGoalDefinition(UpdateGoalDefinitionRequest) returns (UpdateGoalDefinitionResponse);
rpc SetGoalDefinitionStatus(SetGoalDefinitionStatusRequest) returns (SetGoalDefinitionStatusResponse);
rpc ValidateGoalVersion(ValidateGoalVersionRequest) returns (ValidateGoalVersionResponse);
```

`ListAdminProgressionGoals` should support filters, search, pagination, and enough summary fields to render the workbench without N+1 detail requests.

`GetAdminProgressionGoal` should return:

- goal definition
- all versions
- current version
- linked reward bundle summaries
- challenge pool memberships
- validation warnings

`UpdateGoalDefinition` should allow draft-safe metadata edits. It must not mutate active immutable version data.

`SetGoalDefinitionStatus` should enforce valid transitions:

- draft to retired
- active to inactive
- inactive to active through explicit version activation, not blind status change
- inactive to retired
- retired remains read-only

`ValidateGoalVersion` should validate requirement and reward input without creating a saved import record.

### Challenge Pool APIs

Add challenge pool admin APIs.

Proposed RPCs:

```proto
rpc ListChallengePools(ListChallengePoolsRequest) returns (ListChallengePoolsResponse);
rpc GetChallengePool(GetChallengePoolRequest) returns (GetChallengePoolResponse);
rpc CreateChallengePool(CreateChallengePoolRequest) returns (CreateChallengePoolResponse);
rpc UpdateChallengePool(UpdateChallengePoolRequest) returns (UpdateChallengePoolResponse);
rpc SetChallengePoolStatus(SetChallengePoolStatusRequest) returns (SetChallengePoolStatusResponse);
rpc UpsertChallengePoolGoal(UpsertChallengePoolGoalRequest) returns (UpsertChallengePoolGoalResponse);
rpc RemoveChallengePoolGoal(RemoveChallengePoolGoalRequest) returns (RemoveChallengePoolGoalResponse);
rpc PreviewChallengePoolImport(PreviewChallengePoolImportRequest) returns (PreviewChallengePoolImportResponse);
rpc ApplyChallengePoolImport(ApplyChallengePoolImportRequest) returns (ApplyChallengePoolImportResponse);
```

Challenge pool APIs should validate:

- pool scope is supported
- assignment count is non-negative
- daily, weekly, and monthly active pools have meaningful assignment count
- linked goal version exists
- linked goal is `kind='challenge'`
- linked version belongs to a non-retired goal
- weight is positive
- cooldown is non-negative
- eligibility JSON stays within V1-supported shape
- active item-specific eligibility is blocked or warned until ownership-aware assignment is enabled

### Reward APIs

Existing reward APIs are mostly sufficient:

- `ListRewardCatalogTargets`
- `ValidateRewards`
- `CreateRewardBundleDefinition`
- `GetRewardBundleDefinition`
- `ListRewardBundleDefinitions`

Potential additions:

- Add search/pagination fields to `ListRewardBundleDefinitions` if reusable bundles become numerous.
- Add update/status transition APIs for reusable bundles if operators need to revise draft bundles from the UI.

## Frontend Architecture

Split the current App UI into feature modules before adding authoring screens.

Recommended structure:

```text
eventun/app/src/
  app/
    AppShell.tsx
    routes.tsx
    theme.ts
  features/
    goals/
      GoalsPage.tsx
      GoalWorkbenchTable.tsx
      GoalDetailDrawer.tsx
      RequirementBuilder.tsx
      GoalVersionHistory.tsx
      goalCsv.ts
      goalMappers.ts
    challenge-pools/
      ChallengePoolsPage.tsx
      ChallengePoolDrawer.tsx
      ChallengePoolGoalTable.tsx
      challengePoolCsv.ts
      challengePoolMappers.ts
    rewards/
      RewardsPage.tsx
      RewardPicker.tsx
      RewardBundleDrawer.tsx
      rewardMappers.ts
    imports/
      ImportPreviewPage.tsx
      CsvUploadPanel.tsx
      ImportResultTable.tsx
    support/
      PlayerRewardsPage.tsx
  shared/
    api/
      eventunClient.ts
      queryKeys.ts
    components/
      ErrorAlert.tsx
      PageHeader.tsx
      StatusTag.tsx
      Toolbar.tsx
    csv/
      csvParser.ts
      csvWriter.ts
    forms/
      JsonField.tsx
      NullableTextInput.tsx
```

Keep generated code under `eventun/app/src/eventunapi` and do not manually edit generated files.

## Implementation Plan

### Phase 1: Backend Admin Goal Read APIs

Files:

- Modify: `proto/ikigai/eventun/v1/progression.proto`
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Modify: `internal/eventun/admin.go`
- Create: `internal/eventun/progression_goal_admin_query.go`
- Create: `internal/eventun/progression_goal_admin_query_test.go`

Tasks:

- Add admin list/detail messages and RPCs.
- Implement list filters for kind, status, category, text, metric, reward type, and pool id where practical.
- Include summary fields needed by the table.
- Include versions and pool memberships in detail responses.
- Add tests for drafts, active goals, inactive goals, retired goals, and challenge pool membership summaries.
- Regenerate Go and Swagger output.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun
go test ./internal/eventun -run 'Progression.*Goal|Admin.*Goal'
bun run gen
```

### Phase 2: Backend Goal Edit and Validation APIs

Files:

- Modify: `proto/ikigai/eventun/v1/progression.proto`
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Modify: `internal/eventun/admin.go`
- Modify: `internal/eventun/progression_admin_api.go`
- Modify: `internal/eventun/progression_goal_admin_input.go`
- Create: `internal/eventun/progression_goal_admin_validate.go`
- Create: `internal/eventun/progression_goal_admin_validate_test.go`

Tasks:

- Add no-write `ValidateGoalVersion`.
- Add draft-safe `UpdateGoalDefinition`.
- Add explicit `SetGoalDefinitionStatus`.
- Ensure active version data remains immutable.
- Ensure active edits produce new versions through existing `CreateGoalVersion`.
- Return row/path validation errors in the same style as definition import.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun
go test ./internal/eventun -run 'ValidateGoalVersion|UpdateGoalDefinition|SetGoalDefinitionStatus|CreateGoalVersion'
bun run gen
```

### Phase 3: Backend Challenge Pool Admin APIs

Files:

- Modify: `proto/ikigai/eventun/v1/progression.proto`
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Modify: `internal/eventun/admin.go`
- Create: `internal/eventun/progression_challenge_admin_api.go`
- Create: `internal/eventun/progression_challenge_admin_db.go`
- Create: `internal/eventun/progression_challenge_admin_input.go`
- Create: `internal/eventun/progression_challenge_admin_test.go`

Tasks:

- Add pool list/detail/create/update/status APIs.
- Add pool-goal upsert/remove APIs.
- Validate active pool goal links against active challenge goal versions.
- Return pool health fields for insufficient active candidates and invalid memberships.
- Do not add new DDL unless implementation reveals a missing index or constraint.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun
go test ./internal/eventun -run 'Challenge.*Admin|ChallengePool'
bun run gen
```

### Phase 4: Backend Challenge Pool Import APIs

Files:

- Modify: `proto/ikigai/eventun/v1/progression.proto`
- Modify: `proto/ikigai/eventun/v1/admin.proto`
- Create: `internal/eventun/progression_challenge_pool_import_api.go`
- Create: `internal/eventun/progression_challenge_pool_import_test.go`

Tasks:

- Add preview/apply APIs for pool CSV rows after frontend column shape is stable.
- Store preview results if durable audit is useful; otherwise return validation preview without persistence.
- Apply pool and pool-goal changes transactionally.
- Reuse the same validators as direct pool APIs.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun
go test ./internal/eventun -run 'ChallengePoolImport'
bun run gen
```

### Phase 5: Frontend Regeneration and App Split

Files:

- Modify: `eventun/app/src/federated-element.tsx`
- Create: `eventun/app/src/app/AppShell.tsx`
- Create: `eventun/app/src/app/routes.tsx`
- Create: `eventun/app/src/app/theme.ts`
- Create: `eventun/app/src/shared/api/eventunClient.ts`
- Create: `eventun/app/src/shared/api/queryKeys.ts`
- Create: shared components listed in the architecture section.

Tasks:

- Regenerate TypeScript clients after backend Swagger changes.
- Move theme and shell code out of `federated-element.tsx`.
- Preserve the connectivity page as a diagnostics route.
- Add temporary routes for Goals, Challenge Pools, Rewards, Imports, and Support.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run codegen
npm run build
npm run lint
```

### Phase 6: Goals Workbench Read-Only Slice

Files:

- Create: `eventun/app/src/features/goals/GoalsPage.tsx`
- Create: `eventun/app/src/features/goals/GoalWorkbenchTable.tsx`
- Create: `eventun/app/src/features/goals/GoalDetailDrawer.tsx`
- Create: `eventun/app/src/features/goals/goalMappers.ts`

Tasks:

- List goals through the new admin list API.
- Add filters for kind, status, category, and text.
- Show requirement, reward, and pool summaries.
- Open detail drawer with version history and read-only metadata.
- Show empty, loading, unauthorized, forbidden, and error states.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

### Phase 7: Requirement Builder and Goal Create/Edit

Files:

- Create: `eventun/app/src/features/goals/RequirementBuilder.tsx`
- Create: `eventun/app/src/features/goals/GoalEditorForm.tsx`
- Create: `eventun/app/src/features/goals/requirementMappers.ts`
- Create: `eventun/app/src/features/goals/requirementValidation.ts`

Tasks:

- Load active progression metrics.
- Build one-root `all`/`any` requirement expressions.
- Render dynamic dimension inputs from metric `allowed_dimensions`.
- Validate input locally for missing required fields.
- Call backend no-write validation.
- Save new goals and new versions.
- Make active-goal edits clearly create a new version.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

### Phase 8: Reward Picker and Inline Rewards

Files:

- Create: `eventun/app/src/features/rewards/RewardPicker.tsx`
- Create: `eventun/app/src/features/rewards/RewardBundleDrawer.tsx`
- Create: `eventun/app/src/features/rewards/rewardMappers.ts`
- Modify: `eventun/app/src/features/goals/GoalEditorForm.tsx`

Tasks:

- Add inline reward rows to goal editing.
- Query Eventun catalog targets.
- Support item, ARC currency, and battlepass XP shapes supported by the backend.
- Validate reward rows before save.
- Allow selecting an existing reusable reward bundle instead of inline rewards.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

### Phase 9: Challenge Pool Manager

Files:

- Create: `eventun/app/src/features/challenge-pools/ChallengePoolsPage.tsx`
- Create: `eventun/app/src/features/challenge-pools/ChallengePoolDrawer.tsx`
- Create: `eventun/app/src/features/challenge-pools/ChallengePoolGoalTable.tsx`
- Create: `eventun/app/src/features/challenge-pools/challengePoolMappers.ts`

Tasks:

- List pools with health indicators.
- Create and edit pool metadata.
- Add active challenge goal versions to pools.
- Edit weight, cooldown, eligibility, and active flag.
- Remove pool goals.
- Show assignment-count warnings and unsupported eligibility warnings.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

### Phase 10: CSV Export, Import, and Bulk Edit

Files:

- Create: `eventun/app/src/features/imports/CsvUploadPanel.tsx`
- Create: `eventun/app/src/features/imports/ImportPreviewPage.tsx`
- Create: `eventun/app/src/features/imports/ImportResultTable.tsx`
- Create: `eventun/app/src/features/goals/goalCsv.ts`
- Create: `eventun/app/src/features/challenge-pools/challengePoolCsv.ts`
- Create: `eventun/app/src/shared/csv/csvParser.ts`
- Create: `eventun/app/src/shared/csv/csvWriter.ts`

Tasks:

- Export selected goals to goal CSV.
- Parse goal CSV into `DefinitionImportGoalRow[]`.
- Preview goal imports through existing Eventun definition import APIs.
- Apply valid imports with explicit confirmation.
- Export challenge pool rows.
- Preview/apply challenge pool CSV through the new challenge pool import APIs.
- Add bulk table actions that generate the same import/update payloads.

Verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

### Phase 11: End-to-End Operator Workflow Check

Manual verification in a development namespace:

- Create a reusable reward bundle.
- Create an achievement with structured requirement rows and inline reward.
- Activate the achievement.
- Create a challenge goal.
- Add the challenge version to a daily pool.
- Export goals to CSV.
- Modify a CSV row and import it as a new version.
- Preview and apply the import.
- Confirm active challenge assignment still works through the game/client-facing API.

Backend verification:

```bash
cd /home/cgarvis/projects/genun/eventun
go test ./...
```

Frontend verification:

```bash
cd /home/cgarvis/projects/genun/eventun/app
npm run build
npm run lint
```

## Review Checkpoints

- After Phase 1 and Phase 2, review API shape before implementing pool APIs.
- After Phase 3, review challenge pool semantics against the assignment worker.
- After Phase 5, review frontend structure before building feature pages.
- After Phase 7, review requirement builder UX with sample achievement/challenge definitions.
- After Phase 9, review whether pool health warnings match design expectations.
- After Phase 10, review CSV column shape with likely seasonal setup data.

## Open Decisions

- Exact admin permission resource strings for each new API.
- Whether `ValidateGoalVersion` should also validate challenge pool eligibility context when the goal is already linked to pools.
- Whether challenge pool import previews should be stored durably like definition imports or returned as stateless previews.
- Whether reusable reward bundle draft editing is required in the first production UI slice.
- Whether bulk edit should apply immediately through update APIs or always route through import preview/apply.
