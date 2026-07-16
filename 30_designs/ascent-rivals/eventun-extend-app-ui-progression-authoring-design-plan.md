# Eventun Extend App UI Progression Authoring Design and Implementation Plan

Status: Draft
Date: 2026-06-12
Primary repository: `github.com/ikigai-github/eventun`
UI path: `eventun/app`
Related designs:

- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-requirements.md`
- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design.md`
- `30_designs/ascent-rivals/eventun-extend-app-ui-progression-admin-design-plan.md`
- `30_designs/ascent-rivals/eventun-progression-next-phase-ideation-notes.md`

## Purpose

Define the operator workflow, backend API additions, frontend structure, and implementation sequence for creating and maintaining Eventun achievements, masteries, challenges, challenge pools, and rewards through the AccelByte Extend App UI.

This document is a follow-on to the initial Extend App UI spike. It changes the previous V1 non-goal of "no dedicated admin UI" into active follow-on work for Eventun progression operations.

## Goals

- Create achievements, masteries, and challenge goal definitions.
- Edit existing goals through draft mutation or new immutable versions, depending on goal status.
- Manage daily, weekly, monthly, and seasonal challenge pools.
- Add and validate direct rewards while authoring goals.
- Optionally manage reusable reward packages.
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

- Versioned goals for achievements, masteries, and challenges in the current implementation, with a target migration toward draft authoring plus immutable published snapshots.
- A validated JSON requirement tree with one root `all` or `any` operator and leaf requirements.
- Direct rewards as the default admin authoring path, stored internally as generated single-goal reward bundle definitions.
- Reusable reward packages for rewards shared by multiple goals.
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

The current/expected implementation surface has expanded beyond the early plan and may include:

- `ListAdminProgressionGoals`
- `GetAdminProgressionGoal`
- `ValidateGoalDraft`
- `ValidateGoalVersion` as a transitional API
- `UpdateGoalDefinition`
- `SetGoalDefinitionStatus` as a transitional API
- challenge pool CRUD/status/membership APIs
- challenge pool import preview/apply APIs
- `ListAdminCourses`

Remaining API expectations for a proper operator UI:

- Use admin-grade progression goal list/detail APIs rather than client `ListProgressionGoals` for drafts, published snapshots, archived goals, rewards, and pool membership context.
- Use explicit challenge pool administration APIs rather than direct SQL for ordinary operator flows.
- Use no-write validation before creating draft goal rows.
- Use explicit status transition APIs for inactive/retired goals and pools rather than relying on SQL.

## Product Model

### Goal

A goal is one draft achievement or challenge definition. The UI should present achievements and challenges as one shared authoring model where useful, but challenge runtime availability is determined only by published challenge pools.

Operator-facing terminology:

- The UUID `id` / CSV `goal_id` is the durable identity for edits, imports, history, and API updates.
- `operator_key` / `code` is an optional human-readable reference. It is useful for logs, CSV readability, generated labels, and advanced operator lookup, but it should not be required for ordinary authoring.
- The UI may label `operator_key` as **Code** where it is exposed, but it should be treated as an advanced/reference field rather than a primary authoring field.
- Tooling should generate a unique code when omitted, usually from title, row key, or another stable local hint.
- Goal tag/category is visible in the editor and goals table. Tag maps to the current backend `category` field unless a separate multi-tag model is added later.
- Goal description is hidden in the editor for now. Backend and CSV import/export may still carry description fields.

Goal lifecycle:

- `draft`: editable authoring state.
- `published`: an immutable published snapshot exists for runtime.
- `archived`: hidden from normal authoring and publish flows; still readable for support/history.

`Unpublished changes` should be a derived UI badge, not a stored status. It means the editable draft differs from the latest published snapshot.

Achievements and masteries should share the same achievement authoring model. Mastery is a boolean or label on an achievement, not a separate lifecycle system.

### Challenge

A challenge is a goal with `goal_type='challenge'`. It becomes assignable only by inclusion in a published challenge pool snapshot.

The UI must therefore distinguish:

- draft challenge goal definition
- challenge pool draft membership
- published challenge pool membership snapshot
- player assignment generated from that published pool membership

### Reward

Direct rewards are the normal authoring path. The UI may also attach an existing reusable reward package.

Rules:

- Operators should work with SKU, currency code, and normalized Eventun reward targets.
- Eventun validates reward entries against local rules and AccelByte catalog state.
- The frontend does not store AccelByte secrets and does not call AccelByte catalog APIs directly.
- A goal may intentionally have no reward. The UI should make "No reward linked" explicit rather than treating it as an incomplete draft.

## Information Architecture

Use a workbench-style UI with persistent navigation:

1. **Goals**
   - Combined table for achievements, masteries, and challenges.
   - Filters by kind, status, tag, metric, SKU, reward type, pool membership, and text.
   - Detail drawer for create/edit/publish workflows.
   - Bulk actions and CSV export.

2. **Challenge Pools**
   - Table of daily, weekly, monthly, and seasonal pools.
   - Pool detail drawer with linked challenge goals.
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
- Hide implementation versioning from normal authoring. Operators should understand draft, published, unpublished changes, archived, and publish blockers.
- Make pool membership visible for challenge goals. A challenge without published pool membership is not assignable.
- Keep draft/import/edit workflows permissive. Operators should be able to stage incomplete content without manually aligning every related status first.
- Treat publish operations as the strict validation boundary. Runtime invariants should be enforced before player assignment, not by making ordinary editing brittle.
- Keep reusable reward packages optional. They are useful for repeated packages, not required for the common single-reward case.
- Use operator-facing reward terminology consistently:
  - **Direct reward**: reward rows edited on the goal itself. Eventun may store this as a generated single-goal reward bundle, but the UI should not present it as a reusable bundle.
  - **Reusable reward package**: an explicitly reusable package selected by name or id because multiple goals should share it.
- Treat AccelByte namespace as Eventun deployment context, not editable authoring data.
- Use import preview for bulk validation. Never apply CSV changes without an explicit confirmation step.
- Treat CSV export/import as a round-trip workflow: operators should be able to export all goals, edit rows in a spreadsheet or with AI assistance, add rows, preview changes, and apply staged draft updates.
- Treat goal `title` and `description` as the only V1 localized goal fields. The default row fields remain English/default copy; localized variants may be handled through a dedicated localization import/export or an advanced editor instead of expanding the main goals table with many locale columns.

## Goals Workbench

### Table Columns

Minimum columns:

- `kind`
- `title`
- `status`
- `published_state`
- `visibility`
- `tag`
- `requirement_summary`
- `reward_summary`
- `challenge_pool_summary`
- `updated_at`

If the current transitional API still returns active-window fields, the UI should avoid emphasizing them and should display empty windows as `Always` until Phase 12 removes them from authoring.

Optional hidden/export columns:

- `goal_id`
- `version_id`
- `operator_key`
- `category` or `tag`
- `description`
- `counting_policy`
- `presentation_json`
- `requirement_json`
- `reward_bundle_definition_id`

### Filters

- kind: achievement, mastery, challenge
- status: draft, active, inactive, retired
- tag
- visibility
- metric code
- dimension key/value, especially SKU and medal name
- reward type
- reward SKU/currency
- challenge pool
- text search across title, tag, requirement content, reward summary, pool membership, Code/reference, and description where available
- UI text should prefer `Code` over `operator key`; backend fields may remain `operator_key`.

### Search Model

The goals list should support broad fuzzy search because operators will commonly search by gameplay content rather than exact title. For example, searching `SMG` should find goals whose requirement JSON includes `weapon_sku=SMG` even if the title does not contain `SMG`.

Initial implementation direction:

- The admin list API should still support pagination for normal table loading and export safety.
- The UI may fetch all goal summary rows by paging through the admin list and cache them client-side for fuzzy search. This is acceptable while the expected goal count is small to moderate, such as under 10,000 goals.
- Search should be debounced and should operate on a derived search document per goal, not only raw JSON text.
- The derived search document should include title, description, tag/category, kind, mastery flag, Code/reference, requirement metric codes, requirement dimension keys and values, resolved medal names, weapon SKUs/names, part SKUs/names, course codes/names, reward type, reward SKU/currency, Battle Pass XP amount, and challenge pool names/codes.
- Requirement JSON should remain the source data, but the UI can extract searchable tokens from it and join display labels from already-loaded selector/catalog metadata.
- If the goal count grows enough that client-side search becomes slow, add server-side search or an extracted search table/index. Server-side search should preserve the same semantics rather than falling back to title/code-only search.

### Detail Drawer

Use a drawer rather than a full page so the operator keeps table context.

Sections:

- Identity: kind, Code, status, and tag. Code maps to the backend `operator_key` field until the backend contract is renamed. Tag maps to the current backend category field unless a separate multi-tag model is added later.
- Presentation: title and visibility. Description and richer asset/presentation metadata remain hidden for now.
- Requirement builder.
- Rewards.
- Challenge pool memberships for challenge goals.
- Latest published snapshot and publish history.
- Validation results.

### Editing Rules

- New goal: validate draft input without writing, create draft goal, then publish only when the operator requests it.
- Draft goal: allow changing draft metadata, requirement, presentation, and reward configuration.
- Published goal: edits update the draft copy and create an `Unpublished changes` state until the operator publishes again.
- Archived goal: read-only in this UI except support inspection.
- Publishing must run backend requirement and reward validation and create an immutable snapshot.
- If save fails after creating a draft goal, retain the created draft goal id so the operator can retry instead of creating duplicate draft goals.
- Active-window controls are removed from the target authoring model. Challenge timing belongs to challenge pools and periods.
- Challenge goals may be linked to one or more draft challenge pools directly from the goal drawer. This is a staged membership edit only; it does not publish the pool.

## Requirement Builder

Use a structured builder for the V1 requirement tree.

Controls:

- Root operator: segmented control with `All` and `Any`.
- Requirement rows:
  - metric
  - implicit matcher for V1 counter metrics
  - target
  - dynamic dimensions
  - remove/duplicate row actions

Metric behavior:

- Load active metrics from `ListProgressionMetrics`.
- Current authorable metrics are counter-style metrics such as `medal.count`, `kill.count`, `heat.completed`, `match.completed`, and `podium.count`.
- V1 authoring treats numeric counter requirements as implicit `>=`. The UI should not expose `<`, `<=`, `==`, or other numeric matchers until a metric family explicitly supports them.
- Lap-time and finish-time metrics should stay deferred until the next metric family supports implicit `<=` or explicit under-time semantics.
- Boolean metrics, if exposed, should use true/false controls rather than generic matcher labels.
- Counting policy should display `Regulation Only` for the current storage value `canonical_only`.
- `Always` may be displayed as a disabled future option until the backend counter builder supports the all-completed-heats path.
- Dimension controls are generated from `allowed_dimensions`.
- Course dimensions (`course_code`) should resolve selector options from the AccelByte Cloud Save game record `Courses`, not Eventun's database-backed `course` table alias.
- Dimension values use stable identifiers, preferably SKU for items and medal names for medals.
- `weapon_sku` selectors should be catalog-backed and filtered to `/Gameplay/Weapon`.
- `part_sku` selectors should be catalog-backed and filtered to non-weapon gameplay part categories such as `/Gameplay/<Part Type>`.
- Cosmetic catalog categories such as `/Cosmetic/*` should not populate gameplay dimension selectors.
- `medal.count` selectors should be driven by Eventun medal definition admin data synced from the game medal definitions, not by distinct names already observed in player event rows.
- Target input type follows metric `value_type`.
- `medal.count` should not expose `parent_medal_name` or `is_augment` in the first UI slice. Those remain backend/game-tracking details unless a concrete authoring workflow needs them.

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

Direct reward rows should be embedded in the goal drawer.

Reward row controls:

- reward type: item, currency, or Battle Pass XP
- catalog target search for item rewards
- currency selector labeled `Currency`, with ARC as the only current option
- XP amount for Battle Pass XP rewards
- quantity
- fulfillment mode: claimable or automatic
- duplicate policy: convert duplicate item to ARC when possible, or award nothing for the duplicate item

Reward authoring should not expose an AccelByte namespace field. Catalog targets are resolved and validated against Eventun's configured namespace.

Currency reward authoring should not ask operators for an AccelByte catalog target or item SKU. The backend should know or derive the ARC catalog target needed for fulfillment.

Battle Pass XP authoring should not use catalog search. Operators should only choose the `battlepass_xp` reward type and enter a positive XP amount. Eventun should generate Season Pass grant source/tags from runtime context during fulfillment. Reward metadata remains backend/future-use data and should not be exposed as an editable preview in the current UI.

Battle Pass XP should apply to the current published Season Pass by default. If no current season exists, the authoring flow should support or clearly display the configured fallback behavior, such as awarding nothing for that entry or granting ARC replacement. Explicit season-pinned Battle Pass XP is deferred until there is a concrete use case.

The `Award nothing` duplicate policy maps to backend value `skip_duplicate`. Existing databases must have the reward duplicate-policy migration applied before operators can safely use this option.

Operators can either:

- choose no reward
- add direct reward rows, which Eventun stores internally as `generated_goal_reward`
- attach an existing reusable reward package

Direct reward storage titles should remain hidden. Eventun can generate or internalize a title unless reusable reward package authoring later needs an operator-visible label.

Validation:

- Validate direct rewards before save.
- Validate linked reusable bundles before publish.
- Show missing SKU, non-grantable item, inactive catalog target, and invalid quantity at row level.

## Challenge Pool Management

### Authoring Model

Challenge pool authoring should use a staged-then-publish model.

Draft/import/edit flows should be permissive:

- allow pool metadata to be staged before every linked challenge is publish-ready
- allow draft challenge goals in the goal picker
- validate shape and references early, but avoid blockers that require operators to manually align hidden lifecycle state during normal editing

Activation/publish is the strict boundary:

- published pool memberships are runtime snapshots and must point at published challenge goal snapshots
- publish validation should check goal shape, requirement validity, reward validity, challenge pool membership health, and assignment eligibility
- a backend publish operation should atomically snapshot the pool, linked challenge goals, and linked reward data
- if any linked object cannot be made valid, publish should fail without partial state changes and return clear blockers

This avoids exposing hidden status coupling as manual operator work.

### Pool List

Columns:

- scope: daily, weekly, monthly, seasonal
- Code
- status
- assignment count
- reset timezone
- repeat policy
- active goal count
- assignability status
- updated at

### Pool Detail Drawer

Pool fields:

- Code
- scope
- assignment count
- reset timezone
- repeat policy
- status

Status rule:

- Published challenge pool snapshots are immutable.
- Draft pools remain editable until published.
- Archived pools are hidden from normal authoring and cannot be published.
- Draft-only fields such as Code/backend `operator_key` and scope should not change in ways that make existing published snapshots ambiguous; create a new pool when the meaning changes materially.

Pool goal table:

- goal title
- goal id
- category
- weight
- cooldown periods
- eligibility summary
- publish validation state

Pool health checks:

- Published daily/weekly/monthly pools should have at least `assignment_count` assignable linked challenges.
- Seasonal pools may have `assignment_count=0` and use all linked published challenges.
- Missing, archived, invalid, or unpublished linked challenges should be flagged before publish.
- Item-specific eligibility should be flagged as unsupported for assignment until ownership-aware assignment is active.
- If every otherwise eligible challenge is on cooldown, assignment logic falls back by ignoring cooldown. The UI should still show the cooldown configuration.

## CSV and Bulk Editing

CSV import/export should map to the same model used by the structured editor.

### Goal CSV

Recommended columns:

- `row_key`
- `goal_id`
- `code`
- `kind`
- `is_mastery`
- `tag`
- `category`
- `title`
- `description`
- `visibility`
- `counting_policy`
- `presentation_json`
- `requirement_expression_json`
- `requirement_operator`
- `requirement_1_metric`
- `requirement_1_matcher`
- `requirement_1_target`
- `requirement_1_dimensions_json`
- repeated requirement columns as needed
- `reward_mode`
- `reward_bundle_definition_id`
- `reward_fulfillment_mode`
- `reward_bundle_title`
- `reward_duplicate_policy`
- `reward_1_type`
- `reward_1_item_sku`
- `reward_1_item_id`
- `reward_1_currency_code`
- `reward_1_quantity`
- `reward_1_metadata_json`
- repeated reward columns as needed
- `challenge_pool_codes`
- `challenge_pool_memberships_json`

Goal CSV should not include per-locale title/description columns. Localization uses a separate CSV workflow because translation work happens at a different point in the content pipeline and can add many locale-specific columns or rows. Keeping it separate makes the main goal CSV easier to use for creating and tuning achievements, masteries, challenges, requirements, and rewards.

`code` is the operator-facing label for the backend `operator_key` concept. It is optional in CSV and should be generated when omitted. `tag` is the operator-facing label for the current backend category field. If both `tag` and `category` appear during a transition, `tag` should be treated as the preferred editable column and `category` should be retained only for backward compatibility.

Goal CSV identity and update behavior:

- A non-empty `goal_id` means update that existing draft goal. The import preview should show the row as an update, unchanged row, or validation failure.
- A blank `goal_id` means create a new draft goal.
- A blank `code` on create means generate a unique code from title, row key, or another stable local hint.
- A populated `code` on create is a requested reference, not the durable identity. If it conflicts with an existing goal, preview should either generate a unique replacement code and show that outcome or return a clear row-level blocker if automatic replacement is not implemented.
- Updating an existing row should not warn that its own `code` already exists. Code conflicts should only be reported when the row tries to change its code to one owned by a different goal.
- `row_key` is a spreadsheet/import convenience for preview messages and AI-assisted editing. It must not be the durable identity for updates.
- Export should include `goal_id` for existing goals and should allow operators to clear `goal_id` intentionally when duplicating a row into a new goal.

Requirement export behavior:

- Export should include `requirement_expression_json` as the canonical lossless requirement representation.
- Export may also include flattened `requirement_N_*` columns for common counter requirements so operators can do simple spreadsheet edits.
- Import should prefer `requirement_expression_json` when it is non-empty. If it is empty, import may build the expression from flattened requirement columns.
- When both JSON and flattened columns are present and disagree, preview should report the conflict rather than silently choosing a different rule than the operator expects.

Reward export and import behavior:

- Export must make rewards self-describing. It is not enough to export only `reward_bundle_definition_id` when the attached bundle is a generated direct reward.
- `reward_mode` should be one of `none`, `inline`, or `bundle`. This is a technical CSV/API field: UI and import preview should label `inline` as **Direct reward** and `bundle` as **Reusable reward package**.
- `reward_mode=none` means the goal intentionally has no reward. Reward entry columns should be ignored or warned on preview.
- `reward_mode=bundle` means attach the reusable reward package identified by `reward_bundle_definition_id`.
- `reward_mode=inline` means use the `reward_N_*` columns to create or replace the goal's direct reward. Eventun may create a generated single-goal reward bundle internally, but any generated `reward_bundle_definition_id` from a previous export should be ignored for apply because generated bundle ids are implementation detail.
- For round-trip editing, operators must be able to export a goal, modify the `reward_N_*` columns on a `reward_mode=inline` row, and import it back to replace that goal's direct reward. The populated `goal_id` identifies the goal being updated; the generated reward bundle id is not the editable reward identity.
- For backward compatibility, if `reward_mode` is omitted, import may infer `bundle` from `reward_bundle_definition_id`, `inline` from populated reward entry columns, or `none` when neither is present. New exports should always include `reward_mode`.
- Older CSVs that contain only a generated `reward_bundle_definition_id` can be imported in the same environment, but they are not self-describing. New exports should use `reward_mode=inline` plus reward entry columns for direct rewards.
- Rows without reward columns or with `reward_mode=none` represent intentional no-reward goals. The import preview should make this visible so operators can distinguish "no reward" from malformed reward input.
- Battle Pass XP direct rewards should export as `reward_N_type=battlepass_xp`, blank `reward_N_item_sku`, blank `reward_N_item_id`, blank `reward_N_currency_code`, `reward_N_quantity` as the XP amount, and `reward_N_metadata_json` as `{}` unless later metadata is required.
- ARC rewards should export as `reward_N_type=currency`, `reward_N_currency_code=ARC`, and the configured backend catalog target only when the current API still requires it. Operators should not have to manually discover the ARC catalog SKU.

For V1 counter-style authoring, `requirement_1_matcher` should default to `greater_than_or_equal` when omitted. Import preview should reject unsupported matcher values for author-created counter rows even if the backend preserves broader matcher compatibility for old/runtime data.

Do not add reward namespace columns to goal CSVs. Reward targets are implicitly in the AccelByte namespace configured for the Eventun deployment that processes the import.

Challenge pool membership from goal CSV:

- `challenge_pool_codes` may contain a delimiter-separated list of pool codes to stage memberships for challenge goals using default membership values.
- `challenge_pool_memberships_json` may carry advanced membership data, such as pool id/code, weight, cooldown periods, and eligibility overrides.
- Goal CSV import should support staging pool memberships as a convenience for content setup. It must not publish the pool automatically.
- Non-challenge goal rows with challenge-pool membership columns should produce a preview warning or validation error.

The frontend can parse CSV into `DefinitionImportGoalRow[]` and call the existing definition import preview/apply APIs. Server-side CSV parsing is not required for the first UI if frontend parsing is deterministic and export uses the same columns.

CSV behavior requirements:

- Editing or clearing CSV input must invalidate parsed rows and preview state.
- Numeric parsing must be strict integer parsing, not `parseInt`-style partial parsing.
- Export must support both selected rows and all rows matching the current filters. It must page through cursors instead of silently truncating at the first page of results.
- Goal CSV import should stage draft content. Strict publish-ready validation should happen when publishing a goal or challenge pool, not row by row during staging.
- Import preview should show creates, updates, unchanged rows, skipped rows, validation failures, and generated direct reward replacements.

### Localization CSV

Localization export/import is a separate workflow from goal CSV import. It is intended for translation passes after goals have been drafted or published, not for bulk requirement/reward tuning.

Recommended row-oriented columns:

- `goal_id`
- `published_goal_id`
- `code`
- `tag`
- `kind`
- `is_mastery`
- `default_title`
- `default_description`
- `locale`
- `localized_title`
- `localized_description`
- `source_updated_at`
- `localized_updated_at`

Behavior:

- Export all localizable goal strings should include every non-archived goal by default, with a control to include archived goals when needed.
- Export should support all configured locales, a selected subset of locales, or a template mode that emits blank rows for target locales that do not yet have translations.
- The row-oriented shape is preferred over one-column-per-locale because it stays stable as locales are added and is easier to import after translators add or remove target languages.
- `goal_id` is the source identity for draft/default localizations. `published_goal_id` may be included for audit/debugging, but import should normally write draft/source localization rows and then run the localization sync/publish path rather than requiring operators to edit published rows directly.
- `default_title` and `default_description` are context for translators and should not overwrite the default goal copy unless the operator is using the main goal CSV/update workflow.
- Import should upsert `localized_title` and `localized_description` for `(goal_id, locale)`.
- Blank `localized_title` should be treated as missing/invalid because a localized title must not be empty.
- Blank `localized_description` should be allowed as an intentional empty description. A missing cell or explicit clear marker may delete the localized description depending on the CSV parser convention, but the preview must make delete versus blank explicit.
- Import should support deleting a locale row for a goal so the runtime falls back to language root or default copy.
- After localization import apply, Eventun should sync published localization rows for affected goals so player-facing APIs can return the updated copy without a gameplay-rule publish.
- Preview should show creates, updates, deletes, unchanged rows, invalid locales, missing goals, and affected published snapshots.

### Challenge Pool CSV

Recommended columns:

- `pool_id`
- `pool_operator_key`
- `scope`
- `pool_status`
- `assignment_count`
- `reset_timezone`
- `repeat_policy`
- `goal_id`
- `weight`
- `cooldown_periods`
- `eligibility_json`

Challenge pool CSV requires Eventun admin APIs or a dedicated import endpoint because the definition import model only handles goal rows.

Challenge pool import behavior:

- Challenge pool CSV import should stage pool and membership changes. It should not require every referenced challenge to already be publish-ready.
- Import apply should not publish the pool automatically. Operators should use the same publish pool operation after reviewing staged changes.
- A successful challenge pool import apply should not be repeatedly applicable without a new preview.
- Failed previews should not expose non-durable generated IDs as if they can be reused.
- Rows for the same pool should be grouped and applied predictably.

### Bulk Edit

Bulk edit should operate on selected grid rows and generate the same internal payloads as CSV/import:

- duplicate selected goals
- set tag
- set visibility
- set counting policy
- attach reusable reward package
- add direct reward
- add selected challenge goals to a pool
- set pool goal weight/cooldown
- archive selected goals
- delete selected never-published draft goals, if backend support exists

Bulk selection requirements:

- The goals grid must support selecting multiple draft rows.
- Operators should be able to select all rows on the current page and, where backend support exists, all rows matching the current filter.
- Bulk edit/delete controls should be disabled or should return row-level blockers for archived goals, published-only historical rows, and rows that cannot be safely deleted because published snapshots or player history exist.
- If hard delete is only safe for never-published draft goals, the UI should label the general action as `Archive` and expose `Delete draft` only when every selected row is eligible.

## Backend API Design

### Admin Goal APIs

Add admin goal list/detail APIs. These should be distinct from client progression APIs.

Proposed RPCs:

```proto
rpc ListAdminProgressionGoals(ListAdminProgressionGoalsRequest) returns (ListAdminProgressionGoalsResponse);
rpc GetAdminProgressionGoal(GetAdminProgressionGoalRequest) returns (GetAdminProgressionGoalResponse);
rpc ValidateGoalDraft(ValidateGoalDraftRequest) returns (ValidateGoalDraftResponse);
rpc UpdateGoalDefinition(UpdateGoalDefinitionRequest) returns (UpdateGoalDefinitionResponse);
rpc PublishGoal(PublishGoalRequest) returns (PublishGoalResponse);
rpc ArchiveGoal(ArchiveGoalRequest) returns (ArchiveGoalResponse);
```

`ListAdminProgressionGoals` should support filters, search, pagination, and enough summary fields to render the workbench without N+1 detail requests.

`GetAdminProgressionGoal` should return:

- goal definition
- latest published snapshot, if any
- linked direct reward or reusable reward package summaries
- challenge pool memberships
- validation warnings

`UpdateGoalDefinition` should edit draft authoring data. It must not mutate published snapshot data.

`PublishGoal` should validate draft goal shape, requirement expression, reward references, and any relevant achievement/mastery metadata. It should atomically create an immutable published snapshot or return explicit publish blockers.

`ArchiveGoal` should hide the draft goal from normal authoring and prevent future publish operations. Published snapshots remain readable for history.

`ValidateGoalDraft` should validate new-goal metadata before a draft goal row is created. This keeps the new-goal path no-write until the draft identity itself is valid.

Existing version-oriented APIs such as `ValidateGoalVersion` and `CreateGoalVersion` are transitional. The simplified lifecycle phase should compatibility-wrap or retire them after runtime moves to published snapshots.

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
rpc ValidateChallengePoolPublish(ValidateChallengePoolPublishRequest) returns (ValidateChallengePoolPublishResponse);
rpc PublishChallengePool(PublishChallengePoolRequest) returns (PublishChallengePoolResponse);
rpc PreviewChallengePoolImport(PreviewChallengePoolImportRequest) returns (PreviewChallengePoolImportResponse);
rpc ApplyChallengePoolImport(ApplyChallengePoolImportRequest) returns (ApplyChallengePoolImportResponse);
```

Challenge pool edit APIs should validate shape and references:

- pool scope is supported
- assignment count is non-negative
- daily, weekly, and monthly published pools have meaningful assignment count
- linked goal exists
- linked goal is a challenge
- linked goal is not archived
- weight is positive
- cooldown is non-negative
- eligibility JSON stays within V1-supported shape
- published snapshots are immutable

Challenge pool publish APIs should enforce player-facing runtime invariants:

- published pools have enough assignable linked challenges for `assignment_count`
- every pool membership can produce or reference a valid published challenge goal snapshot
- rewards linked to challenge goals are valid
- item-specific eligibility is blocked or warned until ownership-aware assignment is enabled
- publish creates all pool, goal, and reward snapshots atomically or applies none

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

Catalog lookup behavior:

- Eventun reward catalog lookup should use AccelByte Platform admin item search, currently `/platform/admin/namespaces/{namespace}/items/search`.
- Namespace is supplied by Eventun runtime configuration, not authoring input.
- The lookup currently relies on default/published store behavior.
- Search requests should send required `language` and `keyword` values and avoid empty searches.

Catalog-backed gameplay selectors:

- `weapon_sku` selector options should come from `/Gameplay/Weapon`.
- `part_sku` selector options should come from non-weapon `/Gameplay/<Part Type>` categories.
- `/Cosmetic/*` categories should be ignored for gameplay requirement dimensions.
- Currency reward authoring should show ARC as a currency option rather than requiring operators to select an ARC catalog item.

### Medal Definition APIs

`medal.count` authoring should use Eventun medal definition admin data instead of distinct medal names observed in player event rows.

Recommended admin capabilities:

- list medal definitions for selector population
- create/update/deactivate medal definitions when the game medal data table changes
- distinguish base medals from augment medal codes
- preserve optional parent/base medal context for backend counting and validation without exposing `parent_medal_name` or `is_augment` in the first goal-authoring UI

The preferred source for the initial medal definition list is the game client medal and augment data tables, not historical Eventun events.

### Course APIs

Add or use `ListAdminCourses` for authoring selectors.

Rules:

- Course selector source of truth is AccelByte Cloud Save game record `Courses`.
- UI should display course code plus `FeatureState`.
- CSV import/export should continue to use raw `course_code`.
- Eventun's database `course` table is legacy/alias data and should not be treated as the source of truth.

### Admin/Auth Behavior

Admin role and token failures should map precisely:

- expired or invalid token: unauthenticated
- transient IAM/admin lookup failures: unavailable
- real non-admin user: permission denied

This distinction matters because intermittent local testing or page reload failures should not be misreported as permanent "not admin" authorization failures.

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
- Implement list filters for goal type, published/archive state, category, text, metric, reward type, and pool id where practical.
- Include summary fields needed by the table.
- Include latest published snapshot and pool memberships in detail responses.
- Add tests for draft, published, archived, and challenge pool membership summaries.
- Regenerate Go and Swagger output.

Verification:

```bash
# Run from the Eventun repository root.
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

- Add no-write draft validation.
- Add draft-safe `UpdateGoalDefinition`.
- Add explicit publish/archive operations.
- Ensure published snapshot data remains immutable.
- Ensure draft edits do not affect published runtime state until publish.
- Return row/path validation errors in the same style as definition import.

Verification:

```bash
# Run from the Eventun repository root.
go test ./internal/eventun -run 'ValidateGoal|UpdateGoalDefinition|PublishGoal|ArchiveGoal'
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
- Allow draft challenge goals to be staged into pools.
- Validate pool goal links against challenge draft goals.
- Add publish validation and publish pool APIs that enforce runtime invariants and snapshot linked content atomically.
- Return pool health fields for insufficient candidates and invalid memberships.
- Do not add new DDL unless implementation reveals a missing index or constraint.

Verification:

```bash
# Run from the Eventun repository root.
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
- Apply pool and pool-goal changes transactionally as staged edits, not automatic publish.
- Reuse the same validators as direct pool APIs.
- Route strict publish-ready validation through the publish pool API after import review.

Verification:

```bash
# Run from the Eventun repository root.
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
# Run from the Eventun repository root/app directory.
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
- Open detail drawer with draft metadata, latest published snapshot, and history/status context.
- Show empty, loading, unauthorized, forbidden, and error states.

Verification:

```bash
# Run from the Eventun repository root/app directory.
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
- Restrict the first UI slice to counter metrics with implicit `>=`.
- Render only supported dynamic dimension inputs from metric `allowed_dimensions`.
- Hide medal-specific backend fields such as `parent_medal_name` and `is_augment`.
- Use medal definition admin data for `medal.count` selectors.
- Validate input locally for missing required fields.
- Call backend no-write validation.
- Save new goals and draft edits.
- Make published-goal edits clearly remain draft-only until publish.

Verification:

```bash
# Run from the Eventun repository root/app directory.
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

- Add direct reward rows to goal editing.
- Query Eventun catalog targets.
- Support item rewards, ARC currency rewards, and Battle Pass XP rewards in the current UI slice.
- Do not require operators to choose an AccelByte catalog target for ARC currency rewards.
- Do not require catalog search or catalog target selection for Battle Pass XP rewards; collect only a positive XP amount.
- Validate reward rows before save.
- Allow selecting an existing reusable reward package instead of direct rewards.

Verification:

```bash
# Run from the Eventun repository root/app directory.
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
- Add draft challenge goals to pools.
- Edit weight, cooldown, and eligibility.
- Remove pool goals.
- Show assignment-count warnings and unsupported eligibility warnings.
- Add a publish pool action that runs strict backend validation and shows blockers.

Verification:

```bash
# Run from the Eventun repository root/app directory.
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
- Export all goals matching the current filter to goal CSV.
- Page through admin list cursors for export so exported CSV is not silently truncated at the first result page.
- Include `goal_id`, `code`, `tag`, `requirement_expression_json`, `reward_mode`, direct reward entry columns, and challenge-pool membership columns in goal CSV exports.
- Keep per-locale title/description out of goal CSV; use the dedicated localization CSV workflow instead.
- Export direct rewards as self-describing `reward_mode=inline` rows with reward entry columns. Do not export only the generated reward bundle id.
- Export Battle Pass XP rewards as `reward_N_type=battlepass_xp` with quantity as XP amount and no item/currency target columns.
- Parse goal CSV into `DefinitionImportGoalRow[]`.
- Support CSV round-trip updates: non-empty `goal_id` updates an existing draft goal; blank `goal_id` creates a new draft goal.
- Treat `code` as optional. Generate it when omitted, suppress duplicate-code warnings when the code belongs to the same `goal_id`, and avoid blocking blank-`goal_id` creates solely because a copied code already exists unless no automatic replacement behavior is implemented.
- Add client-side fuzzy search over all loaded goals, including requirement metrics and dimensions such as medal name, weapon SKU, part SKU, and course code.
- Use strict numeric parsing for integer fields.
- Clear parsed rows and preview state when CSV input is edited or cleared.
- Preview goal imports through existing Eventun definition import APIs.
- Apply valid goal imports with explicit confirmation as staged draft content where appropriate.
- Stage challenge-pool memberships from goal CSV rows where `challenge_pool_codes` or `challenge_pool_memberships_json` is populated.
- Export localizable goal strings to localization CSV independently from goal CSV.
- Import localization CSV by upserting/deleting draft/source localization rows and syncing affected published localization rows without changing requirement or reward snapshots.
- Export challenge pool rows.
- Preview/apply challenge pool CSV through the new challenge pool import APIs.
- Treat challenge pool import as staging. Do not require publish-ready linked goals row by row and do not publish automatically.
- Prevent repeat apply after a successful challenge pool import apply unless the operator creates a new preview.
- Add bulk table actions that generate the same import/update payloads.
- Add bulk selection for draft rows, including bulk tag changes, archive, and draft-only delete where safe.
- Default list views should hide archived goals, challenge pools, and reusable reward packages. Provide an explicit filter/control to show archived records.
- Goal and challenge-pool list views should show compact reward summaries, including ARC amount and Battle Pass XP amount when present.
- Diagnose and fix false "no active Battle Pass" validation when the configured development namespace has an active AccelByte Season Pass. Surface namespace/API/fallback details clearly when validation fails.

Verification:

```bash
# Run from the Eventun repository root/app directory.
npm run build
npm run lint
```

### Phase 11: End-to-End Operator Workflow Check

Manual verification in a development namespace:

- Create a reusable reward package.
- Create an achievement with structured requirement rows and direct reward.
- Publish the achievement.
- Create a challenge goal.
- Add the challenge goal to a daily pool.
- Export goals to CSV.
- Modify a CSV row and import it as a draft edit.
- Export a goal with a generated direct Battle Pass XP reward and re-import it without losing the reward shape.
- Export mastery rows, duplicate them by clearing `goal_id`, adjust target/reward values, preview creates, and apply.
- Export existing goals, edit rows with populated `goal_id`, preview updates without duplicate-code warnings, and apply.
- Search `SMG` or another weapon/part/medal term and confirm goals with matching requirement dimensions appear even when the title does not contain that text.
- Preview and apply the import.
- Publish the daily pool and confirm challenge assignment still works through the game/client-facing API.

Backend verification:

```bash
# Run from the Eventun repository root.
go test ./...
```

Frontend verification:

```bash
# Run from the Eventun repository root/app directory.
npm run build
npm run lint
```

### Phase 12: Draft/Publish Lifecycle Simplification

This phase migrates the authoring app and supporting APIs away from operator-facing goal versions, active windows, and pool-membership active flags.

Backend tasks:

- Add immutable published snapshot tables for goals, rewards, challenge pools, and challenge-pool memberships.
- Backfill snapshots from current active/current-version data.
- Move runtime assignment, progress, completion, and reward creation APIs to published snapshot ids.
- Add draft edit, publish, and archive APIs for goals and challenge pools.
- Publish goals by validating draft requirement, reward, presentation, and achievement/mastery metadata, then snapshotting the result.
- Publish challenge pools by validating linked challenge drafts, linked rewards, eligibility, and assignment count, then snapshotting the pool and linked challenge goals atomically.
- Compatibility-wrap or retire `goal_definition_version`, goal active-window fields, version activation APIs, and `challenge_pool_goal.active`.

Frontend tasks:

- Replace version and activation UI with draft, published, unpublished changes, archived, and publish-blocker states.
- Remove active-window controls from goal editing.
- Remove per-membership active toggles from challenge-pool editing.
- Show publish blockers directly in goal and pool detail views without requiring operators to query separate diagnostics.
- Treat mastery as an achievement flag/filter.
- Treat challenge availability as solely determined by inclusion in a published challenge pool snapshot.
- Keep reusable reward packages as authoring convenience while showing that published snapshots freeze reward details.

Review checkpoint:

- Validate the new authoring model with a daily pool update, a seasonal pool planning flow, an achievement edit, a mastery edit, a no-reward achievement, and a direct reward change.

## Review Checkpoints

- After Phase 1 and Phase 2, review API shape before implementing pool APIs.
- After Phase 3, review challenge pool semantics against the assignment worker.
- After Phase 5, review frontend structure before building feature pages.
- After Phase 7, review requirement builder UX with sample achievement/challenge definitions.
- After Phase 9, review whether staged pool memberships, publish blockers, and pool health warnings match design expectations.
- After Phase 10, review CSV column shape with likely seasonal setup data.
- Before Phase 12 implementation, review the published snapshot schema and migration/backfill strategy against existing player progress, completion, challenge assignment, and reward tables.

## Cleanup Follow-Ups

- Remove the Eventun database `course` table and related seed/alias plumbing. The source of truth for authoring and runtime course metadata should be the AccelByte Cloud Save game record `Courses`.
- Replace the existing non-admin `Courses` endpoint implementation with the same Cloud Save-backed course source used by `ListAdminCourses`, or otherwise retire the non-admin endpoint if no client still needs it.
- Keep CSV and persisted progression requirement dimensions using raw `course_code`; only selector display and validation should depend on the Cloud Save course list.

## Open Decisions

- Exact admin permission resource strings for each new API.
- Whether draft goal validation should also validate challenge pool eligibility context when the goal is already linked to pools.
- Whether challenge pool import previews should be stored durably like definition imports or returned as stateless previews.
- Exact published snapshot schema for later publish phases; V1 reward details are copied into `published_goal.reward_snapshot` JSONB, with normalized child rows deferred unless runtime/support queries justify them.
- Whether reusable reward package draft editing is required in the first production UI slice.
- Whether bulk edit should apply immediately through update APIs or always route through import preview/apply.
