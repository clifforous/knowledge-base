# Eventun Progression Draft/Publish Implementation Plan

Status: Implementation plan draft
Date: 2026-06-16
Primary repository: `github.com/ikigai-github/eventun`
Related solution design: `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design.md`
Related authoring UI plan: `30_designs/ascent-rivals/eventun-extend-app-ui-progression-authoring-design-plan.md`
Related next-phase notes: `30_designs/ascent-rivals/eventun-progression-next-phase-ideation-notes.md`

## Purpose

Migrate Eventun progression authoring from version activation and row-level active flags toward a draft authoring model with immutable published runtime snapshots.

The current implementation already has goals, goal versions, challenge pools, reward definitions, player progress, completions, assignments, and reward grants. This plan adds the published snapshot model beside the existing schema first, then moves runtime and UI paths over in controlled phases.

## Target Model

Operators author mutable draft content. Runtime progression reads immutable published snapshots.

Draft authoring rows remain editable:

- goal definitions and current transitional goal versions
- challenge pools and pool memberships
- reusable reward bundle definitions

Published runtime rows are append-only:

- published goal snapshots
- copied reward snapshots on published goals
- published challenge pool snapshots
- copied published challenge pool memberships

Runtime player records should eventually reference published snapshot ids so later draft edits do not change historical player outcomes.

## Target Schema

### `progression_publish_revision`

Purpose: Records each publish operation or deterministic legacy backfill.

Fields:

- `id`
- `source_kind`: `goal`, `challenge_pool`, or `bulk_backfill`
- `source_id`
- `published_by`
- `published_at`
- `status`
- `validation_summary`
- `created_at`

Rules:

- Insert-only after creation.
- Failed publish attempts may be recorded only if that is useful for audit; runtime should use successful published snapshots only.

### `published_goal`

Purpose: Immutable runtime copy of a goal definition at publish time.

Fields:

- `id`
- `source_goal_id`
- `legacy_goal_version_id` while migrating from the current versioned model
- `publish_revision_id`
- copied identity: `operator_key`, `goal_type`, `is_mastery`, `category`
- copied presentation: `title`, `description`, `presentation`, `visibility`
- copied rules: `requirement_expression`, `counting_policy`
- copied reward snapshot: fulfillment mode, duplicate policy, entry list, and metadata useful for fulfillment/display/audit
- `published_at`
- `created_at`

Rules:

- Insert-only after creation.
- Runtime goal checking reads the copied requirement and counting policy from this table.
- Runtime should not depend on mutable `goal_definition_version` rows after the runtime read switch.

### `published_goal.reward_snapshot`

Purpose: Immutable runtime copy of reward details linked to a published goal.

V1 decision:

- Store copied reward details as JSONB on `published_goal.reward_snapshot`.
- Do not create a normalized `published_goal_reward_entry` table in V1.
- Consider normalized child rows later only if runtime reward creation, admin diffing, or support reporting becomes materially harder with the JSON shape.

Expected JSON content:

- source reward bundle definition id
- source reward bundle operator key/title when useful for audit
- fulfillment mode
- duplicate policy
- ordered `entries` array
- for each entry: source reward entry id, reward type, item SKU, item id only if required for fulfillment or audit, currency code, quantity, and metadata

Rules:

- Do not store AccelByte namespace as authored reward data. Fulfillment uses the configured Eventun `AB_NAMESPACE`.
- Reward creation after goal completion should read copied entries from `published_goal.reward_snapshot`, not mutable `reward_entry_definition`.
- Reusable reward bundles remain an authoring convenience; published goals copy exact reward details.

### `published_challenge_pool`

Purpose: Immutable runtime copy of a challenge pool at publish time.

Fields:

- `id`
- `source_pool_id`
- `legacy_pool_id` while migrating from the current active-pool model, if useful for idempotent backfill
- `publish_revision_id`
- copied pool config: `scope`, `assignment_count`, `reset_timezone`, `repeat_policy`, `metadata`
- `published_at`
- `created_at`

Rules:

- Insert-only after creation.
- Challenge assignment should eventually choose periods and candidates from published pool snapshots.

### `published_challenge_pool_goal`

Purpose: Immutable runtime copy of a challenge pool membership.

Fields:

- `id`
- `published_pool_id`
- `source_pool_goal_id` if useful
- `source_pool_id`
- `source_goal_id`
- `legacy_goal_version_id` while migrating from the current versioned model
- `published_goal_id`
- copied membership config: `weight`, `cooldown_periods`, `eligibility`
- `created_at`

Rules:

- Insert-only after creation.
- There is no runtime active flag. A goal included in a published pool snapshot is intended pool content.
- Publish validation blocks invalid pool content before a snapshot is created.

### Compatibility Columns

Add nullable compatibility columns before runtime switches need them:

- `player_goal_progress.published_goal_id`
- `player_goal_progress.source_goal_id`
- `player_goal_completion.published_goal_id`
- `player_goal_completion.source_goal_id`
- `player_reward_bundle.published_goal_id`
- `player_challenge_assignment.published_pool_id`, if direct assignment-to-pool lookup remains useful
- `player_challenge_assignment.published_pool_goal_id`
- `challenge_period.published_pool_id`

These columns allow old runtime rows and new published snapshot rows to coexist during migration.

## Migration Rules

Use current Eventun migration conventions:

- `migration/a0_create_init.sql`: fresh-schema DDL and indexes.
- `migration/b*.sql`: views.
- `migration/c*.sql`: functions and stored procedures.
- `migration/d*.sql`: minimal seed data.
- `migration/temp_migration.sql`: current dev/prod migration until the next production deployment.

The first migration slice should be additive:

- no runtime read-path switch
- no destructive schema changes
- no removal of current versioning columns
- no UI dependency on new publish APIs yet

## Backfill Rules

Backfill must be deterministic and repeatable.

Goals:

- Backfill from `goal_definition.current_version` joined to `goal_definition_version`.
- Snapshot only old-model rows that were runtime-visible under current rules:
  - active goal definition
  - current version exists
  - goal version is activated
  - active window is currently valid, if an active window is present
- Copy reward bundle entries into `published_goal.reward_snapshot`.
- Do not reference mutable reward definition rows from runtime snapshots.
- Use deterministic ids or unique legacy keys so rerunning does not duplicate snapshots.

Challenge pools:

- Backfill active challenge pools into `published_challenge_pool`.
- Backfill only pool memberships that are active under the transitional model.
- Link each published membership to the corresponding published goal snapshot.
- Use deterministic ids or unique legacy keys so rerunning does not duplicate snapshots.

Existing player records:

- Backfill nullable published ids where a deterministic legacy mapping exists.
- Leave rows null when no safe mapping exists; later repair/backfill tooling can address those cases.

## Admin API Direction

Goal APIs should move toward:

- `ListAdminProgressionGoals`
- `GetAdminProgressionGoal`
- `ValidateGoalDraft`
- `UpdateGoalDefinition`
- `ValidateGoalPublish`
- `PublishGoal`
- `ArchiveGoal`

Challenge pool APIs should move toward:

- `ValidateChallengePoolPublish`
- `PublishChallengePool`
- `ArchiveChallengePool`

Publish validation responses should include explicit blockers:

- `path`
- `code`
- `message`
- `severity`
- affected goal, pool, membership, or reward id when available

Examples:

- missing reward target
- unsupported counting policy
- unsupported item-specific eligibility
- linked goal is archived
- linked challenge cannot produce a valid published snapshot
- not enough assignable challenges for assignment count

Existing version and activation APIs remain compatibility-only during migration:

- `CreateGoalVersion`
- `ActivateGoalVersion`
- `SetGoalDefinitionStatus`
- `ActivateChallengePoolGoals`

Do not build new operator UI workflows around those transitional calls.

## Published State Semantics

Admin read APIs should expose a simple authoring state:

- `draft`: no successful published snapshot exists.
- `published`: latest draft content matches the latest successful snapshot.
- `unpublished_changes`: latest draft content differs from the latest successful snapshot.
- `archived`: authoring row is archived or retired.

For goals, the comparison must include:

- goal identity fields
- presentation fields
- requirement expression
- counting policy
- linked reward details copied into the published snapshot

For challenge pools, the comparison must include:

- pool config fields
- linked challenge set
- linked published goal identities
- membership weights
- membership cooldowns
- membership eligibility

Pool membership edits are material draft changes and must not still display as `published`.

## Runtime Switch Direction

Do runtime changes after schema and admin-read compatibility are stable.

Goal checking:

- Load candidates from `published_goal`.
- Evaluate copied `requirement_expression`.
- Store the exact snapshot in `published_goal_id`.
- Use `source_goal_id` as the non-repeatable progress identity so republishing the same authored goal does not make prior progress disappear.

Completions:

- Unique completion keys should include player, `source_goal_id`, scope, and assignment where relevant.
- Store `published_goal_id` on the completion for historical display and reward snapshot lookup.
- Store completion snapshots from the published goal and counter values.

Challenge assignment:

- Challenge periods should reference `published_challenge_pool`.
- Assignment candidates should come from `published_challenge_pool_goal`.
- Assigned challenges should reference `published_goal_id` and preferably `published_pool_goal_id`.

Reward creation:

- Create player rewards from copied entries in `published_goal.reward_snapshot`.
- Do not read mutable `reward_bundle_definition` or `reward_entry_definition` for runtime reward details after the switch.

## Frontend Direction

Replace operator-facing activation concepts with:

- `Draft`
- `Published`
- `Unpublished Changes`
- `Archived`

Goals table:

- remove version emphasis
- remove active window emphasis
- show latest published snapshot state
- show publish blockers inline or in a drawer

Challenge pool drawer:

- remove membership active toggle
- treat linked membership as intended pool content
- show publish validation state per row
- use `Publish Pool` as the strict operation
- if publish is blocked, show row-level reasons directly in the table

## Phase Breakdown

### Phase 1: Snapshot Schema And Backfill

Goal: Add immutable publish infrastructure beside existing runtime tables.

Reviewable outcome:

- Fresh schema contains publish revision, published goal with reward snapshot JSON, published pool, and published pool goal tables.
- Current dev/prod migration contains additive, idempotent DDL and deterministic backfill.
- Existing runtime behavior is unchanged.

Implementation tasks:

- Add publish snapshot DDL and indexes to `migration/a0_create_init.sql`.
- Add current environment migration to `migration/temp_migration.sql`.
- Put trigger/function definitions in the appropriate `migration/c*.sql` file for fresh schema and mirror needed deployment steps in `temp_migration.sql`.
- Add idempotent backfill for active/current/activated goals.
- Add idempotent backfill for active challenge pools and active memberships.
- Add nullable compatibility columns where needed for later runtime switch.
- Add tests or migration verification notes that prove backfill can be rerun without duplicating snapshots.

Out of scope:

- runtime read switch
- publish APIs
- frontend lifecycle changes

### Phase 2: Admin Read APIs Include Snapshots

Goal: Let admin readers see latest published snapshots and draft-vs-published state without changing runtime behavior.

Reviewable outcome:

- Goal list and detail responses include latest published snapshot data.
- Challenge pool list and detail responses include latest published snapshot data.
- Responses expose derived state: `draft`, `published`, `unpublished_changes`, or `archived`.
- State comparison catches the draft changes operators care about, including reward edits and challenge pool membership edits.

Implementation tasks:

- Extend progression proto messages for goal and challenge pool snapshot fields.
- Regenerate Go and TypeScript clients.
- Query latest published goal snapshot by source goal id.
- Query latest published challenge pool snapshot by source pool id.
- Add mapping and validation-safe JSON decoding for snapshot records.
- Add state-comparison helpers for goals and pools.
- Add tests for:
  - no snapshot yields `draft`
  - matching snapshot yields `published`
  - changed goal field yields `unpublished_changes`
  - changed reward entry yields `unpublished_changes`
  - changed pool config yields `unpublished_changes`
  - added/removed/changed pool membership yields `unpublished_changes`
  - retired or archived rows yield `archived`

Out of scope:

- publish validation API
- publish write API
- runtime read switch

### Phase 3: Publish Validation APIs

Goal: Add strict validation boundaries without writing published snapshots.

Reviewable outcome:

- `ValidateGoalPublish` returns actionable blockers for a goal.
- `ValidateChallengePoolPublish` returns actionable blockers for a pool and linked challenge content.
- Validation can be used by the UI before a publish attempt.

Implementation tasks:

- Validate goal shape, metric support, counting policy support, reward validity, and publishable state.
- Validate pool assignment count, linked challenge health, linked reward validity, unsupported item eligibility, and published-goal availability.
- Return structured blockers with stable paths and codes.

### Phase 4: Goal Publish API

Goal: Atomically publish one goal snapshot and its copied reward snapshot.

Reviewable outcome:

- `PublishGoal` validates the draft goal and inserts a new published goal snapshot with copied reward entries in `reward_snapshot`.
- Runtime remains on old read paths until Phase 6.

Implementation tasks:

- Lock source goal and relevant reward definitions during publish.
- Run publish validation inside the write transaction.
- Insert publish revision and published goal reward snapshot atomically.
- Return the published snapshot and any warnings.

### Phase 5: Challenge Pool Publish API

Goal: Atomically publish one challenge pool snapshot and its intended linked goals.

Reviewable outcome:

- `PublishChallengePool` validates the pool, publishes any eligible linked challenge goals if that behavior is explicitly supported, and inserts the pool snapshot plus membership snapshots.
- If any linked content cannot be made valid, nothing changes and blockers are returned.

Implementation tasks:

- Lock source pool and membership rows.
- Validate linked challenge goals and rewards.
- Create or reuse current published goal snapshots according to the chosen publish policy.
- Insert publish revision, published pool, and published pool membership snapshots atomically.

### Phase 6: Runtime Read Switch

Goal: Move runtime progression, challenge assignment, completion, and reward creation to published snapshots.

Reviewable outcome:

- Goal checking uses `published_goal`.
- Challenge assignment uses `published_challenge_pool` and `published_challenge_pool_goal`.
- Completion, progress, assignment, and reward rows reference published snapshot ids.
- Existing old rows still read correctly during compatibility.

Implementation tasks:

- Update goal candidate queries.
- Update challenge assignment queries.
- Update completion uniqueness and insertion paths.
- Update reward creation to read copied entries from `published_goal.reward_snapshot`.
- Backfill or repair current rows where safe.

### Phase 7: Frontend Lifecycle Simplification

Goal: Make the operator workflow match draft/publish semantics.

Reviewable outcome:

- UI no longer asks operators to reason about goal versions, active windows, or pool membership active flags.
- UI shows draft/published/unpublished changes/archived state and publish blockers.

Implementation tasks:

- Update goal list, detail, and editor flows.
- Update challenge pool list, detail, and editor flows.
- Add publish actions and blockers UI.
- Keep compatibility screens only where needed for old-data inspection.

### Phase 8: Compatibility Retirement

Goal: Stop extending old lifecycle concepts after runtime and UI paths are migrated.

Reviewable outcome:

- Version activation APIs are compatibility-wrapped, hidden from normal UI, or retired.
- Transitional fields remain only for old data inspection and safe migration.

Implementation tasks:

- Remove feature logic that depends on `goal_definition.current_version`, `goal_definition_version.activated_at`, active windows, and `challenge_pool_goal.active`.
- Keep database columns until old records no longer need them.
- Document final deprecation behavior.

## Phase 2 Review Checklist

When reviewing Phase 2, check:

- The implementation does not switch runtime behavior.
- Latest snapshot queries choose the correct source row and deterministic ordering.
- Challenge pool membership state compares against a published goal snapshot matching the linked draft content, not merely the latest snapshot for the source goal.
- Goal published state compares all meaningful draft fields.
- Goal published state detects reward entry changes, not just reward bundle id changes.
- Pool published state detects membership set and membership config changes.
- Snapshot response fields do not imply mutable reward definitions are runtime-safe.
- Generated API output matches proto changes.
- Tests cover both list and detail responses.
