# Eventun Progression Next-Phase Ideation Notes

Status: Ideation notes for post-V1 review
Date: 2026-06-15
Related requirements: `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-requirements.md`
Related solution design: `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design.md`
Related authoring UI plan: `30_designs/ascent-rivals/eventun-extend-app-ui-progression-authoring-design-plan.md`
Draft/publish implementation plan: `30_designs/ascent-rivals/eventun-progression-draft-publish-implementation-plan.md`

## Purpose

Capture progression, achievement, challenge, and reward ideas that are intentionally outside the current V1 implementation commitment or need another product-design review before implementation.

This note is not an implementation plan. It is a review queue for the next design iteration.

## Recent V1 Decisions That Affect Next Phase

### No-Reward Goals

Some achievements may intentionally have no grantable reward. In those cases the achievement completion itself is the award.

Implications:

- Eventun must retain durable completion history even when no `player_reward_bundle` is created.
- Game client and website surfaces may later need a player-facing achievement gallery, profile badges, achievement history, or similar completion display.
- "No reward" must be explicit in operator tooling so it is not confused with an incomplete reward configuration.

### Duplicate Reward Handling

Duplicate durable item rewards now support at least two policy paths:

- `convert_item_to_arc_when_price_available`: convert a duplicate item to ARC compensation when catalog price is available.
- `skip_duplicate`: award nothing for that duplicate item and record the skip.

Future review should decide whether the product wants more granular duplicate policies, per-item overrides, or different messaging for skipped duplicates.

## Candidate Next-Phase Areas

### 1. Draft/Publish Lifecycle Simplification

The current progression implementation accumulated too many lifecycle concepts: goal status, goal version activation, active windows, challenge pool status, and pool membership active flags. Operators should not need to reason through those layers to understand whether a challenge is assignable or why a goal is inactive.

Recommended direction:

- Use editable draft definitions for goals, challenge pools, and reusable rewards.
- Use immutable published snapshots for runtime goal completion, challenge assignment, and reward creation.
- Remove operator-facing goal versions from normal authoring.
- Remove goal active windows from the target authoring model. Challenge timing should come from challenge pools and periods.
- Remove per-membership active toggles from challenge pools.
- Treat challenge player-facing availability as solely determined by inclusion in a published challenge pool snapshot.
- Treat mastery as an achievement flag or label, not a separate lifecycle type.
- Keep reusable reward bundles as an authoring convenience. Published goal snapshots should copy exact reward details.

Important runtime invariant:

- Player progress, completions, challenge assignments, reward bundles, and grant attempts must reference immutable published snapshot ids or copied snapshot data, not mutable draft rows.

Current implementation-plan decision:

- V1 published reward details are stored as JSON snapshots on `published_goal.reward_snapshot`.
- Normalized child rows such as `published_reward_entry` are deferred unless runtime fulfillment, admin diffing, or support reporting becomes materially harder with JSON snapshots.
- The current migration path is tracked in `30_designs/ascent-rivals/eventun-progression-draft-publish-implementation-plan.md`; review open schema questions against that plan.

Review questions:

- How should the UI compare draft versus published data to show `Unpublished changes`?
- Which current version/status APIs should be compatibility-wrapped versus removed?

### 2. Player-Facing Achievement Presentation

Current V1 work can complete achievements without requiring an external reward. A next phase should decide how players see those achievements.

Ideas to review:

- in-game achievement list
- player profile achievement history
- public website achievement display
- post-match achievement unlock presentation
- profile badges or featured achievements
- achievement completion timestamps and source context

Open product questions:

- Are all completed achievements public by default?
- Should achievement visibility differ from challenge progress visibility?
- Does the player need "new/unread" achievement state, or is completion history enough?
- Should rewardless achievements still trigger an end-of-match unlock moment?

### 3. Achievement Images And Presentation Metadata

Achievement, mastery, and challenge definitions may need richer presentation data once player-facing surfaces exist.

Candidate metadata:

- 2D image or icon
- rarity or tier
- sort order
- short display title and longer description
- hidden/unrevealed display copy for future hidden achievements
- category visual treatment

Likely implementation direction:

- Store presentation metadata on draft goal definitions and copy it into published goal snapshots.
- Use Eventun-hosted media or the existing media-upload pattern used by gauntlets and sponsors if the team decides assets should be uploaded through the admin UI.
- Keep exact asset storage and CDN behavior out of V1 until the player-facing surface is designed.

Review questions:

- Are images required for every achievement, only featured achievements, or only player-profile badges?
- Should challenge images be distinct from achievement images?
- Who owns art naming and upload workflow?

### 4. Localization Review

V1 now requires simple goal localization for `title` and `description`, with English/default fallback and locale-aware player reads. The next design iteration should review fields beyond those two.

Already in V1 scope:

- achievement, mastery, and challenge display titles
- achievement, mastery, and challenge descriptions

Likely fields to review later:

- reward bundle display copy, if Eventun owns any player-facing reward text
- medal display names where Eventun-backed medal totals appear outside game-owned UI copy
- category, rarity, tier, and status labels if they are displayed directly from Eventun data
- hidden or unrevealed achievement copy if hidden achievements are added later
- compact/short titles if tight UI surfaces need alternate copy

Likely non-localized fields:

- operator keys and internal names
- metric names and requirement JSON fields
- medal codes emitted by the game client
- AccelByte SKUs and other catalog identifiers
- database ids and API ids

Review questions:

- Which fields are admin-only and should never be treated as player-facing copy?
- Should AccelByte catalog item names be treated as the source of localized reward copy, or should Eventun provide its own reward presentation text?
- Should future hidden achievements require separate localized locked/unrevealed copy?

### 5. Platform Achievements

Some Eventun achievements may need to grant or synchronize with platform achievements, such as Steam achievements.

Design considerations:

- Eventun can remain the authoritative gameplay-completion detector.
- The game client may be the correct place to unlock Steam achievements if Steam APIs are client-bound.
- Eventun may need to expose a "newly completed platform-sync candidate" API so the game client can perform platform-specific unlocks.
- Platform achievement sync must be idempotent and tolerant of the player completing an achievement while offline or before the platform mapping exists.

Open questions:

- Which platforms need achievement support first?
- Is Steam achievement unlock available only from the client, or can a trusted backend service perform it?
- Should every Eventun achievement map to a platform achievement, or only a curated subset?
- How should retroactive completion unlock platform achievements?

### 6. Reward Model Expansion

Deferred or not-yet-settled reward ideas:

- titles
- limited-supply rewards
- premium currency or additional currencies beyond ARC
- regular account/game XP as a future reward type distinct from Battle Pass XP
- more granular duplicate compensation
- reward presentation when a duplicate item is skipped

Review questions:

- Should skipped duplicate rewards show a player-facing message, or should they be silent?
- Should some reward types default to automatic fulfillment while others default to claimable?
- Do no-reward goals need any reward-ledger row, or is `player_goal_completion` enough?

### 7. Challenge System Expansion

Deferred challenge ideas:

- challenge rerolls
- operator/support-triggered challenge pull and replacement during an active period
- segmented challenge pools by skill, progression, owned inventory, or other eligibility
- item-specific challenge assignment once ownership filtering is reliable
- mid-season challenge edits or replacement rules
- repeat/cooldown tuning
- private versus public challenge assignment surfaces

Operator pull and replacement is distinct from player rerolls. It is an operational escape hatch for cases where an assigned challenge becomes inappropriate before the period ends, such as:

- a map or mode update makes the goal unachievable
- a promotional event daily goal ends early
- a challenge is discovered to be incorrectly scoped after players already received it

The likely behavior is to mark affected active assignments as `replaced`, preserve historical/audit rows, remove them from the active challenge response, and let the assignment system choose a replacement from the current eligible pool. Completed assignments should normally remain completed unless a later support policy explicitly authorizes reversal.

Review questions:

- Should rerolls be free, limited per period, currency-priced, or event-specific?
- Should operator-pulled challenges be replaced immediately for all affected players, lazily on next challenge fetch, or only for players who have not completed the challenge?
- What audit detail is required when support pulls an assigned challenge early?
- How should the system behave when all eligible challenges are on cooldown?
- What player-facing explanation is needed when a challenge requires an item the player does not own?

### 8. Achievement Semantics Expansion

Deferred achievement ideas:

- prerequisite-gated achievements
- hidden achievements
- repeatable achievements
- tiered achievements
- retroactive completion rules for new goals created after historical partitions move to archive

Review questions:

- Are prerequisite gates a visibility rule, a completion rule, or both?
- Should hidden achievements hide requirements, progress, rewards, or only presentation?
- Should repeatable achievements share the same completion table or use a separate repeat-instance model?

### 9. Achievement Backfill Preview And Apply

Potential V2+ feature: add an admin/support workflow to retroactively evaluate published achievements against existing progression counters before mutating player state.

Preview should show, per player and achievement:

- current progress
- whether the achievement would complete
- whether the achievement is already completed
- the reward snapshot that would be used
- existing completion and reward history relevant to duplicate protection

Apply should let an operator choose per achievement whether to:

- create only the completion
- create the completion and reward records
- skip reward creation
- auto-grant a normally claimable reward for this backfill run
- leave claimable rewards in their normal claimable state

Apply must be audited with:

- operator id
- timestamp
- selected options
- affected players and achievements
- created completion ids
- created reward bundle ids
- failures

Constraints and default assumptions:

- Preview is non-mutating.
- Duplicate protection remains based on player, source goal, and scope.
- Reward creation remains one bundle per completion.
- Retroactive rewards use the currently published reward snapshot by default.
- Historical reward snapshot selection is deferred unless a future design explicitly adds it.

Review questions:

- Should the first version support all published achievements or only a selected achievement list?
- Should masteries use the same backfill workflow, or remain achievement-only until there is a concrete support need?
- Should backfill apply support a dry-run export for external review before operator confirmation?

### 10. Requirement Matcher And Final-Stat Semantics

The current V1 progression model is built around additive counters. Numeric requirements should therefore behave like implicit "at least" checks unless a later design adds richer metric semantics.

High-priority next-version requirement: support racing time achievements and challenges, especially finish-time and lap-time goals. Ascent Rivals is a racing game, so time-based goals should be treated as a core next-version progression capability rather than a distant edge case.

Priority examples:

- finish a course under a target time
- complete a lap under a target time
- win or podium with a finish time under a target
- complete a regulation heat with every lap under a target time
- set a personal-best finish time or lap time on a course
- complete an Illus-0 heat without crashing or dying
- average fewer than 3 crashes across 100 Illus-0 heats

Current V1-safe behavior:

- Numeric metric leaves should usually be rendered as "at least" / `>=`.
- The authoring UI can hide numeric matcher selection for additive counters.
- Boolean metrics can use explicit true/false controls rather than generic comparison operators.

Risky matcher patterns:

- `==` can miss completion when a counter jumps past the target between evaluations, such as moving from 9 to 11 before the checker runs.
- `<` and `<=` are often true immediately for counters that start at 0, unless paired with a window, completion trigger, denominator, or final-state condition.

Examples that likely need richer semantics:

- finish a heat with 0 crashes
- average fewer than 10 crashes across 100 Illus-0 heats
- complete a challenge before 3 failed attempts
- win with lap time under 40 seconds, which is high priority because it is a racing-time goal

Likely future model additions:

- course-scoped finish-time and lap-time metrics
- run/session-scoped final-stat requirements
- denominator requirements for ratios and averages
- evaluation-at-completion behavior
- metric definitions that declare which matcher families are valid
- UI controls that use product wording, such as "finish with no crashes" or "under 40 seconds", instead of exposing raw operators

Recommended representation:

- Keep additive counters for simple progress goals.
- Add best/final-stat metrics for lower-is-better values such as finish time and lap time. Missing values should be `NULL` or absent, not `0`, so an unplayed course does not satisfy an under-time goal.
- Represent "complete a heat without crashing or dying" as a qualifying completed-heat fact that increments an additive counter, rather than as lifetime `deaths <= 0` or `crashes <= 0`.
- Represent average goals with numerator and denominator semantics. For example, "average fewer than 3 crashes over 100 Illus-0 heats" should require both `completed_illus_0_heats >= 100` and `total_crashes / completed_illus_0_heats < 3`.

Possible metric shapes:

```json
{
  "metric": "finish_time.best_ms",
  "matcher": "less_than_or_equal",
  "target": 120000,
  "dimensions": {
    "course_code": "illus_0"
  }
}
```

```json
{
  "metric": "heat.clean_completion.count",
  "target": 1,
  "dimensions": {
    "course_code": "illus_0",
    "max_deaths": 0,
    "max_crashes": 0
  }
}
```

```json
{
  "metric": "heat.crashes.average",
  "matcher": "less_than",
  "target": 3,
  "minimum_sample_count": 100,
  "dimensions": {
    "course_code": "illus_0"
  }
}
```

Review questions:

- Should richer matchers be metric-specific instead of globally available?
- Which first concrete finish-time or lap-time goal should drive the V2 model?
- Should clean-completion goals be a specialized counter metric or a reusable final-stat requirement leaf?
- Should average goals be represented as first-class aggregate metric leaves with `minimum_sample_count`?
- Should V2 migrate existing JSON requirement leaves, or add new requirement leaf kinds for final-stat and aggregate goals?

### 11. Non-Regulation And Client-Event Progression Sources

Some next-version achievements should be allowed to count non-regulation play. This should be explicit at the goal, metric, or counting-policy level rather than assumed from the current `Regulation Only` / `canonical_only` policy.

Potential examples:

- career-mode achievements
- time-trial achievements
- custom or special-mode achievements where the product intentionally wants that mode to count

Time achievements will likely come mostly from time trials or career mode, and those are expected to arrive as `client_event` rows. Client events are less trusted than server-authenticated completed-match event batches, so time achievements need their own trust policy instead of inheriting assumptions from server-trusted progression metrics.

Design considerations:

- keep time-trial and career timing metrics separate from trusted server-match progression metrics
- expose source or trust level in metric definitions, such as `server_trusted` versus `client_reported`
- restrict high-value rewards or platform-achievement synchronization for client-reported timing until the abuse policy is decided
- validate course code, course version, feature state, lap count, and regulation metadata against AccelByte `Courses` where possible
- use client-event timing first for achievement/progression surfaces where lightweight trust is acceptable, and reserve server-authenticated timing for competitive leaderboards or high-value rewards
- make `Non-Regulation` or `All Completed` counting explicit in the authoring UI rather than overloading `Regulation Only`

Review questions:

- Which achievement categories are allowed to count non-regulation play?
- Which time achievements are safe to award from client events?
- Are client-event timing achievements allowed to grant rewards, platform achievements, or only Eventun achievement completion?
- Do time-trial and career-mode time achievements need separate metric codes from server-match time metrics?
- Should non-regulation counting use existing all-completed policy concepts or a more explicit policy name?

### 12. Event And Counter Expansion

Deferred technical ideas:

- collection-time event ids for future at-least-once match batch retries
- dedicated `PlayerHeatMedalSummary` event if `PlayerHeatEnd` becomes too large
- occurrence-level medal events only for concrete replay, support, anti-abuse, or period-boundary requirements
- additional counting policies beyond current `Regulation Only` / `canonical_only`
- definition-specific counting policy support
- more complex requirement composition

Review questions:

- Is the current completed-match best-effort event delivery still acceptable after progression becomes player-facing?
- Which player-facing surfaces actually need occurrence-level medal detail?
- Should broad career stats expose both regulation-only and all-completed totals?

### 13. Notification And Read-State

V1 does not include an Eventun notification inbox. Later player-facing achievement and reward surfaces may need some way to avoid repeatedly showing old unlocks.

Possible directions:

- Game client asks Eventun for post-match progression summary and locally presents new completions.
- Eventun tracks "seen" or "read" state for achievement completions and rewards.
- AccelByte player messaging is used for durable notifications where it fits.

Review questions:

- Is post-match presentation enough, or does the hangar/main menu need persistent indicators?
- Should read state be per surface, such as achievement gallery versus reward claim list?
- Should notifications expire, or remain in history indefinitely?

## Suggested Review Order

1. Draft/publish lifecycle simplification and published snapshot migration.
2. Player-facing achievement presentation and no-reward achievements.
3. Achievement image and presentation metadata requirements.
4. Localization review for player-facing progression, challenge, medal, and reward fields.
5. Platform achievement synchronization, starting with Steam.
6. Reward expansion decisions, especially duplicate skip messaging and regular account/game XP ownership.
7. Achievement backfill preview/apply workflow and retroactive reward policy.
8. Racing time goals: finish-time and lap-time achievements/challenges.
9. Client-event and non-regulation progression policy for time-trial and career-mode achievements.
10. Broader requirement matcher and final-stat semantics, driven by concrete example achievements.
11. Challenge expansion decisions, especially rerolls and ownership-filtered item-specific challenges.
12. Technical reliability work, such as event ids or at-least-once batch delivery, only if V1 progression usage exposes a real need.
