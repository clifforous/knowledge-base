# Eventun Medals, Progression Goals, Challenges, and Rewards Requirements Draft

Status: Requirements draft
Date: 2026-05-22
Primary repository: `github.com/ikigai-github/eventun`
Related UI repository: `github.com/ikigai-github/ascentun`

## Purpose

Define the product and system requirements for moving Ascent Rivals medal and progression-goal tracking into Eventun.

This document intentionally starts as a requirements draft. Architecture and implementation details should be finalized only after the open requirements are reviewed.

## Background

The initial research found that Eventun is a sound owner for game-specific medal and progression logic because it already ingests trusted gameplay events, stores combat telemetry, and derives player stats. AccelByte should remain the system of record for player item ownership and entitlement fulfillment, but AccelByte Statistics, Achievements, Rewards, and Challenges are not the best primary authoring model for Ascent Rivals weapon- and part-specific progression.

AccelByte Challenge support exists and includes rotating goals, fixed or randomized assignment, progression evaluation, and claimable rewards. However, it is available on request and still appears tied to configured AGS requirements and rewards. Because Ascent Rivals wants to derive progress from Eventun-owned medals, combat events, loadout context, and match summaries, Eventun should own the game-specific goal model unless later requirements strongly favor mirroring into AccelByte.

## Product Scope Classification

This table separates V1 solution-design scope from future intent. Implementation may still be delivered over multiple engineering iterations, but the requirements and solution design should cover the full feature set.

| Area | Current classification |
| --- | --- |
| Runtime-awarded gameplay medal summaries sent to Eventun | V1 design requirement |
| Career medal totals backed by Eventun | V1 design requirement |
| Persistent achievements | V1 design requirement |
| Masteries as achievement-category goals | V1 design requirement |
| Reward bundles for completed goals, including claimable and automatic rewards | V1 design requirement |
| AccelByte fulfillment for AccelByte-backed rewards | V1 design requirement |
| Daily, weekly, and monthly challenges | V1 design requirement |
| Seasonal challenges | V1 design requirement |
| Historical retention for assignments, completions, claims, and grant attempts | V1 design requirement |
| Public medal and progression stats | Allowed by product policy; exact public API surface is solution scope |
| Active challenge assignment visibility | Public visibility acceptable; first-party UI may show only the current player's challenges |
| Claimable reward visibility | Private by default; low sensitivity if exposed later |
| Battle pass XP rewards | Supported design candidate if AccelByte Season Pass or another battle pass owner is adopted; exact implementation scope is solution/product scope |
| Titles, limited-supply rewards, challenge rerolls, segmented challenge pools, prerequisite-gated achievements, repeatable achievements, hidden achievements | Deferred or future expansion |
| Dedicated admin UI and AccelByte Extend App UI | Deferred product surface; not required for initial operation |
| Presentation asset storage and delivery | Solution scope |

## Existing Context

Eventun currently:

- accepts trusted server gameplay events through `ServerService.Event`
- stores `PlayerKill`, `PlayerDied`, `PlayerMatchEnd`, `PlayerHeatStart`, `PlayerHeatEnd`, lap, checkpoint, and related runtime events
- records kill payload fields such as `method`, `weaponItemId`, victim data, speed, distance, and placement context
- records match and heat summary stats such as kills, deaths, crashes, credits, obelisks, placement, podium finish, lap times, circuit points, and finish time
- derives current player career and course stats from stored events
- uses SQL functions, views, and materialized views for several derived stats surfaces today, including career overview, recommendation metrics, best-lap/best-finish rankings, and gauntlet standings
- currently uses Eventun course data such as default lap counts to decide whether some stats and records are comparable, but that data is copied from the game client and can become stale
- does not yet own a durable medal, achievement, mastery, challenge, reward-claim, or notification/read-state model

Existing Eventun gameplay event identity is sufficient for V1 progression facts. The combination of session id, match number, heat number, event type, and timestamp is guaranteed unique for persisted gameplay event rows; player id and event payload provide player-scoped counting context. The solution design should not introduce separate occurrence ids, heat ids, or match ids solely for medals, achievements, masteries, challenges, or rewards. Events such as `PlayerKill` do not need a separate occurrence identity when the downstream requirement is counting qualifying rows. Medal progression does not require one Eventun row per medal occurrence; per-player heat summary counts are sufficient for V1.

Ascentun currently:

- provides admin-ish website workflows for sponsors, gauntlets, teams, prizes, players, and stats
- can inform the future operator UX
- should not be assumed to be directly embeddable in AccelByte Extend App UI because Extend App UI templates are Vite/React module-federation applications rather than Next.js applications

## Relationship To Existing Player Profile Guidance

The website player-profile design notes currently say medals and badges are AccelByte-owned and should not be faked from Eventun aggregate stats. That guidance was correct for the earlier website work because Eventun did not own official medal facts at that time.

This requirements draft supersedes that older guidance for future gameplay-medal and progression-goal ownership if this project proceeds. The intended terminology split is:

- Gameplay medals: runtime-awarded medal facts produced by the game server and durably tracked by Eventun after this project.
- Achievements, masteries, and challenges: Eventun-owned progression goals evaluated from Eventun facts and aggregates after this project.
- Rewards: claimable Eventun records that may fulfill AccelByte-backed items, currency, or other reward types.
- AccelByte badges, trophies, or unrelated platform recognitions: remain AccelByte-owned unless explicitly migrated.

Until Eventun actually receives and exposes official medal facts, website surfaces should still avoid inventing medals from incomplete aggregate stats.

## Terminology

### Medal

A medal is an immediate game-recognition event awarded by the game runtime for a specific gameplay occurrence.

Examples:

- `Elimination`: awarded for killing another player
- `Splatter Kill`: awarded for eliminating another player by running them over

Medals are primarily gameplay feedback and stat/progression inputs. They are not expected to directly grant rewards in the normal case.

The game runtime owns medal-rule evaluation. Eventun should receive final medal counts and store them; it should not become responsible for determining whether a gameplay occurrence qualifies as `Elimination`, `Splatter Kill`, `Double Kill`, or a comparable medal.

Medals are awarded during heats by the game server. Eventun receives aggregated per-player, per-heat medal counts as part of the successful match event batch at the end of the match. If the match does not complete successfully, the game server does not send the match's gameplay events to Eventun for durable progression tracking.

Medal summary payloads should preserve augment parent context when the game sends augment medal counts. For example, the `airborne` augment can apply to a kill medal or to a warp medal, so the event payload should count `airborne` separately for each parent medal context.

Eventun V1 medal progression does not require the timestamp, location, order, or display values for each individual medal occurrence. Those details should stay in the game runtime unless a later replay, support, anti-abuse, or post-match presentation feature creates a concrete need for occurrence-level medal data.

For time-windowed goals, medal counts may be attributed at heat granularity. V1 does not need to split medal counts across period boundaries inside a single heat.

### Specialized Medal Codes

Specialized medals are distinct game-authored medal codes awarded by the runtime. The game may still have medal concepts such as base medals and augmented medals, but that relationship belongs to game-server medal-rule logic.

Example:

- `Splatter Kill` may be awarded for eliminating another player by running them over.

The game runtime decides whether to award a base medal, a more specific primary medal, or augment medals for a gameplay occurrence. Eventun does not need to derive relationship metadata between medal names right now. It should persist and count the final primary medal and attached augment counts sent by the game runtime, using the primary medal name as parent context for attached augments.

If a later achievement, mastery, or challenge needs additional context, such as airborne state, that context should be modeled as a metric dimension only when it is actually needed.

### Achievement

An achievement is a persistent goal that is completed when a player reaches one or more requirements.

Achievements may be driven by:

- medal counts
- weapon-specific medal counts
- aggregate combat stats
- aggregate match stats
- loadout or part usage
- other Eventun-derived gameplay facts

Examples:

- `SMG Multi-Killer`: get 10 double-kill medals with the SMG
- `Weapon Killer`: get 1,000 weapon kills
- `Career Eliminator`: get 10,000 total kills

Achievements may grant rewards.

Achievement, mastery, and challenge definitions may need presentation metadata, such as a 2D image or icon. Asset storage and delivery are solution-design details, not product requirements.

### Mastery

A mastery is an achievement category focused on sustained use or demonstrated skill with a ship part, weapon, or similar game component.

Masteries are not a separate conceptual system from achievements unless future requirements justify a different lifecycle. They should initially be modeled as achievements with a `mastery` category or type.

Possible mastery requirement patterns:

- use a specific part for a number of heats
- use a specific part for a number of matches, if match-level tracking can be derived cheaply from heat usage
- get a number of kills with a weapon
- get podium finishes while using a part
- complete a match, heat, or event with a specific part equipped

Masteries may have baseline and augmented forms:

- baseline: use the part for a count of matches or heats
- augmented: meet a performance requirement while using the part, such as kills or podium finishes

### Challenge

A challenge is a time-windowed achievement-like goal.

Challenge types currently expected:

- daily
- weekly
- monthly
- seasonal

Daily, weekly, and monthly challenges are expected to come from a challenge pool. Each player may receive a subset of active challenges for that period.

Illustrative assignment model, not a fixed requirement:

- define a daily challenge pool
- when a player requests challenges for the day, select three daily challenges for that player
- persist that assignment until the daily window expires
- allow the player to progress only the assigned daily challenges during the active window

Seasonal challenges are expected to be a fixed set of goals that all players can progress during the season.

The initial challenge pool should be shared by all players. Later versions may segment or personalize by skill, progression, owned inventory, or other eligibility. Even in the initial shared-pool model, challenge assignment should avoid assigning goals that require unowned parts or weapons when ownership data is available.

Item-specific challenges may be deferred from the first implementation slice. If item-specific challenge assignment is deferred, item-specific challenge goals should not be activated into player-facing pools until ownership filtering is available.

Challenge rerolls are a supported future product option, but exact reroll counts, pricing, and UX are not V1 requirements.

Challenges may grant rewards.

### Reward

A reward is granted when a player completes an achievement, mastery, or challenge goal.

Expected V1 reward examples:

- ARC
- skins

For V1, rewards should be treated as AccelByte-backed where possible. Titles are a future-facing example of how reward types could expand beyond skins and ARC; they are not yet a committed implementation requirement.

V1 assumes ARC is the only spendable currency reward. The remaining V1 AccelByte catalog rewards expected for achievements, masteries, and challenges are in-game items such as skins or other grantable gameplay cosmetics. Default account bundles and Season Pass catalog items are not achievement/challenge reward targets.

Rewards are generally not granted directly from medals.

Reward fulfillment should use AccelByte APIs where AccelByte owns the rewardable item or entitlement.

Rewards should not expire after a player earns them. Time windows constrain earning challenge progress, not post-completion reward availability.

### Canonical Heat Context

Canonical heat context is game-authored event context that tells Eventun whether a heat used default/canonical gameplay settings or a special-case configuration.

This requirement is related to existing Eventun stat correctness rather than being specific to medals, achievements, masteries, challenges, or rewards. Eventun currently uses copied course defaults, such as lap counts, to decide whether some stats and records are comparable. That can become stale. The game runtime has the authoritative context for whether a heat used canonical defaults.

Examples of special-case contexts include:

- gauntlet finals
- modified heat lap counts
- special loadout or starting-part rules

Custom game mode alone should not make a heat special-case for V1. A custom-game heat may still be special-case if that heat uses modified lap counts, special loadout rules, or another non-default gameplay setting.

The signal should be heat-level, not only match-level, because a multi-heat match may have one heat with modified settings while later heats use canonical settings.

For this draft:

- Completed match means the game server sent a final successful event batch to Eventun.
- Canonical heat means a heat that the game runtime reports as using default/canonical settings.
- Special-case heat means a heat that the game runtime reports as modified or non-canonical.
- Which aggregate functions, SQL views, medals, achievements, masteries, challenges, records, or leaderboards count canonical versus special-case heats is solution-design and stat-policy scope.

The exact event, field name, payload shape, and downstream counting policy are implementation and solution-design details.

### AccelByte Reward And Entitlement Findings

Current AccelByte documentation and OpenAPI specs indicate three relevant but distinct reward paths:

- Platform fulfillment and entitlement grant APIs grant ownership directly. Fulfillment invokes entitlement grant and additionally records transaction information in fulfillment history.
- Platform entitlement records expose ownership/status concepts such as `ACTIVE`, `CONSUMED`, `INACTIVE`, `REVOKED`, and `SOLD`. They do not appear to expose a generic `UNCLAIMED` entitlement state.
- AccelByte Challenge rewards do expose `CLAIMED` and `UNCLAIMED` user reward states, with public and admin claim endpoints. That claimable state appears to belong to the Challenge service's goal/reward model, not to raw Platform entitlements.
- Platform `fulfillRewards` can fulfill a list of reward items/currencies through a service-communication endpoint and accepts a `transactionId`, `source`, metadata, and reward entries. This may be useful for Eventun-initiated grants, but it still appears to grant immediately rather than create a player-claimable pending reward.
- Public entitlement and ownership endpoints can let the game client verify whether a player owns an item by item id or SKU after it has been granted.

Implication:

- The flow `completed goal -> Eventun grants entitlement -> game client checks AccelByte for unclaimed entitlement -> player claims` is probably not supported by raw AccelByte entitlements because the entitlement is already owned once granted.
- If player claim is a hard requirement, Eventun likely needs to own the claimable reward state, or Ascent Rivals must use AccelByte Challenge's reward model closely enough to rely on its `UNCLAIMED` / `CLAIMED` state.
- If immediate grant is acceptable, Eventun can grant via AccelByte and the game client can show a "newly earned/unseen reward" experience using Eventun completion records, AccelByte entitlement history/ownership, or local client read state. That is not the same as a true entitlement claim.

Decision:

- V1 should use Eventun-owned claimable reward state.
- When a goal completes, Eventun records that the player has earned a claimable reward.
- When the player claims the reward, Eventun grants the AccelByte entitlement, currency, or other reward, then marks the local reward claimed only after the grant succeeds.
- This preserves a true player-facing claim moment while still allowing a future UX to appear closer to immediate grant by auto-opening or auto-claiming rewards behind the scenes.

## Requirements

### Medal Requirements

1. Eventun must support receiving medal information from gameplay events.
2. Eventun must preserve enough context to support weapon-specific, part-specific, match-specific, and time-windowed progression.
3. Eventun must support medals as inputs to achievements, masteries, and challenges.
4. Eventun should not treat medals as reward-granting entities by default.
5. Eventun must treat medal awards from the game runtime as final medal facts rather than re-deriving medal eligibility from raw combat events.
6. Medal persistence and progression should have access to game-authored canonical/special-case heat context when solution design decides which facts should count.
7. Medal events should preserve primary medal context for attached augment medals so the same augment can be counted globally or within a specific parent medal context.

### Achievement Requirements

1. Eventun must support persistent achievements built from one or more measurable gameplay requirements.
2. Requirements must support medal-count predicates.
3. Requirements must support aggregate stat predicates that are not medal-driven.
4. Requirements must support item-specific dimensions such as weapon or part.
5. Requirements should support examples such as:
   - 10 double-kill medals with the SMG
   - 1,000 weapon kills
   - 10,000 total kills
   - Teleported 10 miles with the skip drive
   - 100 Perfect Warp medals with the Furokashi
6. Achievement completion may create a reward bundle.
7. Achievement progress should be derived from Eventun-ingested gameplay events and Eventun-owned aggregate data.
8. Achievement requirements should support simple boolean composition, such as all-of and any-of requirement groups, as long as this does not add disproportionate complexity.
9. Prerequisite-gated achievements, where one achievement must be completed before another can progress or complete, are not a V1 requirement without a concrete use case. The solution design should avoid blocking this future capability.
10. Repeatable achievements and hidden achievements are not V1 requirements without concrete use cases. The solution design should avoid blocking these future capabilities.

### Mastery Requirements

1. Eventun must support masteries as an achievement category unless a later requirement requires a separate system.
2. Masteries must support ship-part and weapon-specific dimensions.
3. Masteries must support usage-based requirements for laps using a part.
4. Masteries should support performance-based requirements such as kills or podium finishes with a part or weapon.
5. Heat-level part usage is the required initial usage primitive because players choose parts per heat.
6. Match-level usage may be supported if it can be derived from heat-level usage without changing product semantics.
7. For event-specific mastery requirements, a part or weapon counts as "used" when it was equipped for the heat in which the qualifying event occurred.
8. Because parts can only change at heat start, "equipped at heat start" and "equipped for the full heat" are equivalent for mastery purposes.
9. Mastery completion may create a reward bundle.

### Challenge Requirements

1. Eventun must support time-windowed goals.
2. Eventun must support daily, weekly, monthly, and seasonal challenge scopes for the V1 design.
3. Eventun must support pool-based challenge assignment for daily, weekly, and monthly challenges.
4. Eventun should support assigning a subset of challenges to each player for a period.
5. Eventun should support seasonal challenges as a fixed shared set for all players.
6. Eventun must support challenge completion rewards.
7. Eventun must preserve challenge-period boundaries so progress cannot leak between periods unless a challenge explicitly allows carryover.
8. Eventun must persist player-specific daily, weekly, and monthly challenge assignments for the active time window.
9. Eventun should ensure a player has active-window assignments before the game client needs to display or progress assigned challenges.
10. Initial daily, weekly, and monthly challenge pools should be shared across players.
11. Challenge assignment should be able to filter out challenges that require a player to use an item they do not own before item-specific challenges are activated into player-facing pools.
12. Challenge rerolls are a supported future product option, but exact reroll counts, pricing, and UX are not V1 requirements.
13. Seasonal challenges can be shared across all players for V1.
14. V1 seasonal definitions should be treated as fixed once the season starts. Mid-season edits, lowered thresholds, replacement challenges, and retroactive completion from definition changes are V2 concerns unless product design explicitly requires them.
15. Eventun must retain historical challenge assignments, progress, and completions after a challenge period ends or a new challenge set is assigned.
16. Historical challenge data should remain available for player history, support, reward reconciliation, analytics, and future UI surfaces.
17. Daily, weekly, and monthly challenge assignment counts must be configurable settings rather than hard-coded product constants.
18. Daily, weekly, and monthly challenge reset windows must be calendar-based daily, weekly, and monthly periods.
19. The exact reset timezone is not a V1 requirement and should be decided during solution design.
20. Challenge repeat behavior and cooldown windows must be configurable.
21. By default, assigned challenges may repeat in later periods unless a cooldown is configured.
22. If all otherwise eligible challenges are on cooldown, assignment should ignore cooldowns rather than failing to assign challenges.
23. Non-currency item unlocks are permanent for challenge eligibility; Eventun does not need V1 behavior for replacing assigned challenges because a player lost access to a required unlocked item.
24. Spendable currency is not part of item-ownership eligibility for item-specific challenges.
25. Active challenge assignments and in-progress challenge values can be public by default unless a future privacy requirement says otherwise.
26. The game client and website may choose to surface only the current player's active challenge assignments even if the underlying data is publicly readable.

### Reward Requirements

1. Completion of an achievement, mastery, or challenge goal should generally create a reward bundle.
2. Reward bundles may be player-claimable or automatically fulfilled, depending on the reward definition.
3. Reward bundles must support ARC and skins as expected V1 reward examples, should be able to support battle pass XP if a battle pass system is adopted, and should remain extensible to future reward types such as titles.
4. V1 currency reward behavior may assume ARC is the only supported spendable currency.
5. V1 non-currency catalog rewards may assume rewardable AccelByte items are grantable in-game items.
6. Eventun must record enough local reward history to avoid duplicate grants.
7. Eventun must be able to call AccelByte APIs to grant AccelByte-owned rewards.
8. Eventun must keep reward grant attempts auditable and retryable.
9. Completion should immediately create a reward record when the completed goal has a reward.
10. The initial design should avoid an approval workflow for normal achievement, mastery, and challenge rewards.
11. Earned claimable rewards should not expire by default.
12. Each completed achievement, mastery, or challenge goal should create one reward bundle.
13. A reward bundle may contain multiple grant entries, for example granting both a part and a skin if the player does not already own the part.
14. The design must distinguish a true player claim from a "newly granted but unseen" reward presentation.
15. If Eventun grants AccelByte entitlements immediately, those rewards should be treated as owned, not unclaimed, unless AccelByte confirms a separate pending entitlement mechanism.
16. V1 should use Eventun-owned reward state rather than raw AccelByte entitlement state for player-facing claimable rewards.
17. Eventun should grant claimable AccelByte-backed rewards only when the player claims the Eventun reward.
18. Eventun should mark a claimable local reward claimed only after the external grant succeeds.
19. Eventun must preserve enough local state to retry failed reward grants without duplicating successful grants.
20. Claimable reward state must distinguish at least claimable, claim in progress, claimed, and retryable failed-claim outcomes. Exact state names and fields are solution scope.
21. Claim failures should keep the reward claimable unless the failure proves the reward definition is invalid and requires operator intervention.
22. Expected claim failures include configuration mismatches between Eventun and AccelByte, such as item id/SKU mistakes, entitlement configuration issues, and possible supply or quantity constraints.
23. Limited-supply rewards are not a V1 requirement, but the reward model should not make them impossible later.
24. V1 should assume reward grants are AccelByte-backed where possible.
25. Titles are a future reward-type example and should not force additional V1 implementation complexity.
26. Eventun must retain historical reward bundle, claim, and grant-attempt data after rewards are claimed.
27. Historical reward data should remain available for player history, support, reconciliation with AccelByte, analytics, and future UI surfaces.
28. If a reward bundle contains an item the player already owns, that duplicate item should not block claiming the bundle or granting the remaining non-duplicate entries.
29. Duplicate item rewards should generally convert to ARC compensation using a global duplicate-reward percentage of the item's catalog price, where the relevant catalog price is available.
30. V1 should not require per-item bespoke duplicate reward definitions. More granular duplicate compensation rules can be revisited later if needed.
31. Goals are expected to normally have rewards, even if the reward is ephemeral such as battle pass XP.
32. Rewardless goals are not a primary V1 use case; whether to allow them is a solution-design choice.
33. The default choice between claimable and automatic rewards should be decided during solution design after concrete reward definitions are known.

### Progress Evaluation Requirements

1. Existing gameplay events sent to Eventun must populate the data used by medals, achievements, masteries, and challenges.
2. The game should begin sending medal data in Eventun events; this is not currently the case.
3. Eventun should record newly completed goals and reward records.
4. Eventun must support operator-triggered retroactive completion for newly created or changed achievements and masteries when sufficient historical source data exists.
5. Completed goal history should be retained even if the underlying achievement, mastery, or challenge definition is later inactive, retired, or replaced.
6. Gameplay events should provide Eventun with heat-level context that distinguishes canonical/default heats from special-case heats.
7. Eventun should rely on the game-authored canonical/special-case context rather than inferring comparability from copied course defaults where the game can provide the authoritative answer.
8. Which aggregate functions, views, records, medals, achievements, masteries, challenges, and leaderboards count canonical versus special-case heats should be decided during solution design.
9. The solution design should decide whether retroactive completion runs from derived event facts, maintained counters, or another model.
10. The solution design should define the historical range available for retroactive evaluation, including how archived or partitioned event history is handled.
11. V1 progression should use existing Eventun gameplay event identity and should not require new occurrence ids or surrogate heat or match ids to count, join, or evaluate gameplay facts.

### Notification and Claim Requirements

1. The game client must be able to retrieve the player's unclaimed rewards.
2. Unclaimed reward data should include enough context for the client to decide how to present it, including the reward reason, source type such as achievement, mastery, or challenge, source identifier, and reward bundle contents.
3. The game client should be able to retrieve achievement and challenge progression data needed by UX surfaces.
4. The exact API shape is a solution-design decision and may be split across multiple APIs, such as match-result progression, achievement/challenge lists, unclaimed rewards, or item-specific reward lookups.
5. The requirements should not prescribe whether completions or rewards are surfaced through post-match summary, inbox notifications, hangar indicators, shop indicators, or another client UX.
6. A durable notification inbox is not a V1 requirement.
7. AccelByte player messaging may be a candidate for later notification delivery and should be researched before building an Eventun notification system.
8. V1 should focus on game-client visibility before public website visibility.
9. The game client already knows which medals were awarded during the match, so Eventun does not need to be the immediate post-match medal notification source.
10. Eventun should support career medal totals so the game client and future website can replace AccelByte-backed medal stat display.
11. Completed achievements, masteries, challenges, medal totals, and related progression stats can be publicly readable by default unless a specific definition or future privacy requirement says otherwise.
12. The game client and website decide which public stats to surface in their own presentation contexts.
13. Achievement, mastery, and challenge presentation may require assets such as icons or 2D images, but asset storage and delivery are solution-design details rather than requirements. The solution may use Eventun uploads, client-bundled assets, or another approach.
14. Active challenge assignments and in-progress challenge values can be public by default unless a future privacy requirement says otherwise.
15. The game client and website may choose to surface only the current player's active challenge assignments.
16. Claimable rewards should be private to the player by default.
17. Claimable reward visibility is low sensitivity; accidental or future intentional exposure that a player has rewards to claim is not a major product concern.

### Administration Requirements

1. Operators eventually need UI to define and maintain achievements, masteries, challenges, and rewards.
2. Operators eventually need UI to inspect a player's progress and completed goals.
3. Operators eventually need UI to retry failed reward grants.
4. AccelByte Extend App UI remains a candidate operator surface.
5. Ascentun remains a useful reference for existing admin workflows but should not drive the final embedded UI architecture by default.
6. Dedicated administration UI is not required for initial operation if controlled operator correction and support workflows exist.

## Initial Product Rules

- Medals are gameplay-recognition events, not the primary reward surface.
- Achievements are persistent progression goals.
- Masteries are achievement-category goals focused on parts and weapons.
- Challenges are time-windowed achievement-category goals.
- Rewards are attached to achievement, mastery, or challenge completion.
- The game runtime owns medal-rule logic.
- Eventun stores medal facts and derives progression from those facts.
- Gameplay events should include game-authored heat context that lets Eventun distinguish canonical/default heats from special-case heats.
- Eventun owns progression evaluation.
- AccelByte owns fulfillment for AccelByte-backed rewards.
- Earned rewards should not expire by default.
- Progression and medal data can be public by default; public API access is acceptable and can support community stats sites.
- The game client must be able to retrieve unclaimed rewards and relevant achievement or challenge progression data from Eventun.

## Candidate Solution Flow

This flow is non-binding and should be validated during solution design:

1. Gameplay sends existing match, player, combat, loadout, and result events to Eventun.
2. Heat context identifies whether each heat is canonical/default or special-case.
3. Gameplay also sends final medal awards to Eventun as part of the successful match event batch.
4. Eventun stores the raw event and medal facts.
5. Eventun uses canonical/special-case heat context according to the counting policy defined in solution design.
6. Eventun evaluates achievement, mastery, and challenge progress for participating players.
7. Eventun records newly completed goals.
8. Eventun creates reward records for completed goals that have rewards.
9. The game client retrieves progression and reward data from Eventun and decides how to surface it.
10. Claimable rewards are granted when the player claims them; automatic rewards are fulfilled according to the reward definition.
11. Eventun records reward fulfillment results and keeps failed claimable rewards retryable when appropriate.

## Assumptions

- Player-facing claimable rewards should use Eventun-owned claimable reward records. Automatically fulfilled rewards still need Eventun-owned history for audit and reconciliation.
- The game server best-effort sends each completed match event batch once. The V1 requirements do not require duplicate match-batch or event-batch protection unless a later delivery contract adds retry behavior.
- Existing persisted event identity is sufficient for V1: session id, match number, heat number, event type, and timestamp identify a gameplay event row; player id and event payload are counting context. New occurrence ids, heat ids, or match ids should only be added if a future delivery, deduplication, or gameplay requirement creates a concrete need.
- Medals are useful as normalized progression events even when a raw Eventun event could also derive the same fact.
- A "double kill" or similar compound medal will be generated by game/runtime logic.
- ARC and skins are expected V1 reward examples and should be AccelByte-backed where possible. Battle pass XP is a supported reward candidate if a battle pass system is adopted. Titles are a future reward-type example and may be AccelByte-backed if/when implemented.
- Item identity details are solution scope. The current expectation is that weapon and part progression will likely use SKU and not AccelByte item ids.
- A player-specific read/inbox state may be useful later if the game needs reliable post-match "new completion" notifications, but it is not a V1 requirement.
- Raw AccelByte entitlements do not appear to support generic player-side `UNCLAIMED` state. AccelByte Challenge rewards do, but only inside the Challenge service model.

## Resolved Requirements Decisions

1. The game runtime owns medal-rule logic; Eventun should not derive medal eligibility.
2. Medals are awarded during heats and sent to Eventun in the final successful match event batch.
3. Medal events should preserve primary medal context for attached augment medals.
4. Existing gameplay event identity is sufficient for V1 progression; new occurrence ids, heat ids, or match ids are not required unless a future delivery or gameplay requirement creates a concrete need.
5. Eventun should preserve authoritative gameplay facts needed for progression; physical storage and derived-data strategy are solution scope.
6. V1 solution design scope includes medals, achievements, masteries, rewards, daily/weekly/monthly challenges, and seasonal challenges; implementation may still be phased.
7. Heat-level part usage is the required mastery primitive because players choose parts per heat; match-level usage is optional if easy to derive.
8. A part or weapon counts as used for event-specific mastery requirements when it was equipped for the heat in which the qualifying event occurred.
9. Each completed goal should create one reward bundle, and the bundle may contain multiple grant entries.
10. Reward bundles may be player-claimable or automatically fulfilled; no normal approval flow is expected.
11. Limited-supply rewards are deferred, but the model should not rule them out.
12. Gameplay events should include game-authored heat-level canonical/special-case context.
13. Earned rewards should not expire by default.
14. Daily, weekly, and monthly challenge assignments should be persisted per player for each active time window.
15. Initial daily, weekly, and monthly challenge pools should be shared across players.
16. Daily, weekly, and monthly challenge assignment counts should be configurable.
17. Daily, weekly, and monthly challenge reset windows should be calendar-based; exact timezone is solution scope.
18. Challenge assignment should consider owned items when the challenge requires a specific part or weapon. Item-specific challenge activation can be deferred until this ownership-aware path is implemented.
19. Challenge repeat behavior and cooldown windows should be configurable, with repeat allowed by default unless a cooldown is configured.
20. Challenge assignment should ignore cooldowns if every otherwise eligible challenge is on cooldown.
21. Non-currency item unlocks are permanent, so assigned item-specific challenges do not need replacement behavior for item loss.
22. Rerolls are a supported future product option, but exact reroll counts, pricing, and UX are not V1 requirements.
23. V1 seasonal challenges are fixed once the season starts; mid-season definition edits are V2 unless explicitly required.
24. Eventun should support career medal totals for game client and future website display.
25. Progression and medal data can be public by default, with game client and website presentation deciding what to show.
26. Active challenge assignments and in-progress challenge values can be public by default, with game client and website presentation deciding what to show.
27. Claimable rewards should be private by default, but their existence is low sensitivity if exposed later.
28. Public stats APIs are acceptable and may help community tools and external stats sites.
29. Exact progression and reward API shapes are solution-design concerns, not settled requirements constraints.
30. V1 rewards should be AccelByte-backed where possible; battle pass XP is a supported reward candidate if a battle pass system is adopted, and titles are a future expansion example rather than a committed V1 reward type.
31. V1 currency reward behavior may assume ARC is the only supported spendable currency.
32. V1 non-currency AccelByte catalog rewards may assume rewardable items are grantable in-game items.
33. Presentation asset storage and delivery should not be prescribed as a requirement.
34. Historical challenge assignments, progress, completions, reward bundles, claims, and grant attempts should be retained after active windows close or rewards are claimed.
35. Operator-triggered retroactive completion should be supported for achievements and masteries when historical data is available.
36. Simple boolean requirement composition should be supported for achievements where it does not add disproportionate complexity.
37. Already-owned item rewards should not block reward bundle claims; duplicate item rewards should generally convert to ARC using a global duplicate-reward percentage of catalog price.
38. V1 should not require per-item bespoke duplicate reward definitions.
39. Goals are expected to normally have rewards, and reward bundles may be claimable or automatically fulfilled depending on reward definition.
40. Dedicated administration UI is deferred until repeated workflows justify dedicated tools.

## Open Requirements Questions

No open product requirements are currently identified. Remaining UX, API, storage, and implementation decisions are deferred to solution design.

## Deferred Solution Areas

These areas should be designed after the requirements are settled:

- Eventun schema
- raw versus aggregate storage strategy
- derived tables, views, materialized views, and recalculation cadence
- event payload shape for medals
- item identity and reward reference model, likely SKU-oriented rather than AccelByte item-id-oriented
- heat-level canonical/special-case context event shape and downstream counting policy
- stat and medal aggregation strategy
- requirement expression model
- challenge assignment model
- reward claim and fulfillment state machine, including exact state names and failure fields
- progression and reward API surface, including match-result progression, unclaimed rewards, and optional item-specific reward lookup
- notification/read-state model if required by UX design
- admin API surface
- Extend App UI scope
- operator correction workflow, including whether direct SQL remains acceptable
- operator-triggered retroactive completion, backfill, and reconciliation tooling
- historical scan range and archived/partitioned event history policy

## Sources

- Eventun knowledge notes: `50_knowledge/ascent-rivals/eventun/overview.md`, `api.md`, `data-model.md`, `events.md`
- Website and profile design notes: `30_designs/ascent-rivals/website/unified-design.md`, `pages/player-profile.md`, `information-architecture.md`
- AccelByte Challenges overview: https://docs.accelbyte.io/gaming-services/modules/online/challenges/
- AccelByte Challenge OpenAPI spec: https://raw.githubusercontent.com/AccelByte/accelbyte-go-sdk/refs/heads/main/spec/challenge.json
- AccelByte Developer FAQ: https://docs.accelbyte.io/gaming-services/knowledge-base/developer-faq/
- AccelByte challenge interaction guide: https://docs.accelbyte.io/gaming-services/services/engagement/challenge/challenge-interaction-within-game-client/
- AccelByte Platform OpenAPI spec: https://raw.githubusercontent.com/AccelByte/accelbyte-go-sdk/refs/heads/main/spec/platform.json
- AccelByte Extend App UI templates: https://github.com/AccelByte/extend-app-ui-templates
- Eventun repository evidence: `github.com/ikigai-github/eventun`
- Ascentun repository evidence: `github.com/ikigai-github/ascentun`
- Ascent Rivals game code evidence: `Source/AscentRivals/Public/Race/HGMedal.h`, `Source/AscentRivals/Private/Race/HGMedal.cpp`, `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`, `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
