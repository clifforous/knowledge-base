# Eventun Medals, Achievements, Masteries, Challenges, and Rewards

Status: Requirements draft
Date: 2026-05-20
Primary repository: `github.com/ikigai-github/eventun`
Related UI repository: `github.com/ikigai-github/ascentun`

## Purpose

Define the product and system requirements for moving Ascent Rivals medal and progression-goal tracking into Eventun.

This document intentionally starts as a requirements draft. Architecture and implementation details should be finalized only after the open requirements are reviewed.

## Background

The initial research found that Eventun is a sound owner for game-specific medal and progression logic because it already ingests trusted gameplay events, stores combat telemetry, and derives player stats. AccelByte should remain the system of record for player item ownership and entitlement fulfillment, but AccelByte Statistics, Achievements, Rewards, and Challenges are not the best primary authoring model for Ascent Rivals weapon- and part-specific progression.

AccelByte Challenge support exists and includes rotating goals, fixed or randomized assignment, progression evaluation, and claimable rewards. However, it is available on request and still appears tied to configured AGS requirements and rewards. Because Ascent Rivals wants to derive progress from Eventun-owned medals, combat events, loadout context, and match summaries, Eventun should own the game-specific goal model unless later requirements strongly favor mirroring into AccelByte.

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

Ascentun currently:

- provides admin-ish website workflows for sponsors, gauntlets, teams, prizes, players, and stats
- can inform the future operator UX
- should not be assumed to be directly embeddable in AccelByte Extend App UI because Extend App UI templates are Vite/React module-federation applications rather than Next.js applications

## Terminology

### Medal

A medal is an immediate game-recognition event awarded for a specific gameplay occurrence.

Examples:

- `Elimination`: awarded for killing another player
- `Splatter Kill`: awarded for eliminating another player by running them over

Medals are primarily gameplay feedback and stat/progression inputs. They are not expected to directly grant rewards in the normal case.

The game runtime owns medal-rule evaluation. Eventun should receive final medal awards and store them; it should not become responsible for determining whether a gameplay occurrence qualifies as `Elimination`, `Splatter Kill`, `Double Kill`, or a comparable medal.

Medals are awarded during heats by the game server. Eventun receives them as part of the successful match event batch at the end of the match. If the match does not complete successfully, the game server does not send the match's gameplay events to Eventun for durable progression tracking.

### Medal Augment

A medal augment is a more specific medal variant that qualifies a base medal.

Rules:

- an augmented medal replaces the base medal for the same occurrence
- if a player earns `Splatter Kill`, they do not also receive `Elimination` for that same kill
- augments should attach directly to a base medal
- augments-on-augments are out of scope unless a strong design reason emerges

Rejected or discouraged example:

- `Flying Splatter Kill` as an augment on `Splatter Kill`

Preferred model:

- keep `Splatter Kill` as the medal if the run-over condition is the relevant distinction
- treat airborne context as a separate stat dimension only if it is needed by a later achievement, mastery, or challenge

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

Achievement, mastery, and challenge definitions may need presentation metadata, such as a 2D image/icon. The asset source is not settled. Assets may be built into the game client, referenced from the Eventun definition, or handled by a mixed approach.

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

Example assignment model:

- define a daily challenge pool
- when a player requests challenges for the day, select three daily challenges for that player
- persist that assignment until the daily window expires
- allow the player to progress only the assigned daily challenges during the active window

Seasonal challenges are expected to be a fixed set of goals that all players can progress during the season.

The initial challenge pool should be shared by all players. Later versions may segment or personalize by skill, progression, owned inventory, or other eligibility. Even in the initial shared-pool model, challenge assignment should avoid assigning goals that require unowned parts or weapons when ownership data is available.

Challenge rerolls are a possible future product feature, but require design-team input before becoming a requirement.

Challenges may grant rewards.

### Reward

A reward is granted when a player completes an achievement, mastery, or challenge goal.

Expected V1 reward examples:

- ARC
- skins

For V1, rewards should be treated as AccelByte-backed where possible. Titles are a future-facing example of how reward types could expand beyond skins and ARC; they are not yet a committed implementation requirement.

Rewards are generally not granted directly from medals.

Reward fulfillment should use AccelByte APIs where AccelByte owns the rewardable item or entitlement.

Rewards should not expire after a player earns them. Time windows constrain earning challenge progress, not post-completion reward availability.

### Competitive Stats Eligibility

Competitive stats eligibility is the match-level signal that tells Eventun whether the match's stats are valid for durable competitive use.

This is broader than medal, achievement, mastery, or challenge progression. It also applies to records and stat surfaces such as:

- best finish time for a course
- best lap time
- most kills
- career stats
- leaderboards and ranking views

The game runtime should own this decision because it knows whether the match used the expected course defaults, lap count, starting parts, race mode, or other settings that make the result comparable. Eventun should not infer eligibility from stale copied course defaults when the game can report the result directly.

Working field name:

- `competitiveStatsEligible`

Optional supporting field:

- `competitiveStatsDisabledReason`

The final payload field name can change during solution design, but the requirement is that `MatchStart` or equivalent match context carries a game-authored eligibility signal for durable competitive stats.

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
2. Eventun must distinguish base medals from augmented medals.
3. Eventun must enforce or represent the rule that an augmented medal replaces the base medal for the same occurrence.
4. Eventun should not require augments-on-augments for the initial model.
5. Eventun must preserve enough context to support weapon-specific, part-specific, match-specific, and time-windowed progression.
6. Eventun must support medals as inputs to achievements, masteries, and challenges.
7. Eventun should not treat medals as reward-granting entities by default.
8. Eventun must treat medal awards from the game runtime as final medal facts rather than re-deriving medal eligibility from raw combat events.
9. Eventun must only persist/progress medals from successfully completed matches that send the final event batch.
10. Eventun may derive aggregate tables, views, or materialized views from raw medal facts, following the existing Eventun pattern for career stats, rankings, recommendations, and gauntlet standings.

### Achievement Requirements

1. Eventun must support persistent achievements with one or more requirements.
2. Requirements must support medal-count predicates.
3. Requirements must support aggregate stat predicates that are not medal-driven.
4. Requirements must support item-specific dimensions such as weapon or part.
5. Requirements should support examples such as:
   - 10 double-kill medals with the SMG
   - 1,000 weapon kills
   - 10,000 total kills
   - Teleported 10 miles with the skip drive
   - 100 Perfect Warp medals with the Furokashi
6. Achievement completion may create one or more claimable rewards.
7. Achievement progress should be derived from Eventun-ingested gameplay events and Eventun-owned aggregate data.

### Mastery Requirements

1. Eventun must support masteries as an achievement category unless a later requirement requires a separate system.
2. Masteries must support ship-part and weapon-specific dimensions.
3. Masteries must support usage-based requirements for laps using a part.
4. Masteries should support performance-based requirements such as kills or podium finishes with a part or weapon.
5. Masteries may support heat-level or match-level usage if it can be derived without adding major complexity.
6. Mastery completion may create one claimable or automatic reward which may be a bundle (eg. Arc + Battlepass XP)

### Challenge Requirements

1. Eventun must support time-windowed goals.
2. Eventun must support daily, weekly, monthly, and seasonal challenge scopes.
3. Eventun must support pool-based challenge assignment for daily, weekly, and monthly challenges.
4. Eventun should support assigning a subset of challenges to each player for a period.
5. Eventun should support seasonal challenges as a fixed shared set for all players.
6. Eventun must support challenge completion rewards.
7. Eventun must preserve challenge-period boundaries so progress cannot leak between periods unless a challenge explicitly allows carryover.
8. Eventun must persist player-specific daily, weekly, and monthly challenge assignments for the active time window.
9. Eventun should assign active-window challenges when a player requests challenges and lacks current assignments for the relevant bucket.
10. Initial daily, weekly, and monthly challenge pools should be shared across players.
11. Challenge assignment should be able to filter out challenges that require a player to use an item they do not own.
12. Challenge rerolls are deferred until the design team decides whether rerolls are part of the product.
13. Seasonal challenges can be shared across all players for V1.
14. V1 seasonal challenge definitions should be treated as fixed once the season starts. Mid-season edits, lowered thresholds, replacement challenges, and retroactive completion from definition changes are V2 concerns.

### Reward Requirements

1. Completion of an achievement, mastery, or challenge goal may create claimable rewards.
2. Reward claim should be the default player-visible completion path.
3. Claimable rewards must support ARC, skins, and titles.
4. Eventun must record enough local reward state to avoid duplicate grants.
5. Eventun must be able to call AccelByte APIs to grant AccelByte-owned rewards.
6. Eventun must keep reward grant attempts auditable and retryable.
7. Completion should immediately create a claimable reward when the completed goal has a reward.
8. The initial design should avoid an approval workflow for normal achievement, mastery, and challenge rewards.
9. Earned claimable rewards should not expire by default.
10. Each completed achievement, mastery, or challenge goal should create one claimable reward bundle.
11. A reward bundle may contain multiple grant entries, for example granting both a part and a skin if the player does not already own the part.
12. The design must distinguish a true player claim from a "newly granted but unseen" reward presentation.
13. If Eventun grants AccelByte entitlements immediately, those rewards should be treated as owned, not unclaimed, unless AccelByte confirms a separate pending entitlement mechanism.
14. V1 should use Eventun-owned claimable reward state rather than raw AccelByte entitlement state for player-facing claims.
15. Eventun should grant AccelByte-backed rewards only when the player claims the Eventun reward.
16. Eventun should mark the local reward claimed only after the external grant succeeds.
17. Eventun must preserve enough local state to retry failed reward grants without duplicating successful grants.
18. V1 reward bundle state should be limited to `earned`, `claiming`, and `claimed`.
19. Claim failures should keep the reward claimable, usually in `earned`, and record `last_claim_error` plus `claim_attempt_count`.
20. Expected claim failures include configuration mismatches between Eventun and AccelByte, such as item id/SKU mistakes, entitlement configuration issues, and possible supply or quantity constraints.
21. Limited-supply rewards are not a V1 requirement, but the reward model should not make them impossible later.
22. V1 should assume reward grants are AccelByte-backed where possible.
23. Titles are a future reward-type example and should not force additional V1 implementation complexity.

### Progress Evaluation Requirements

1. Existing gameplay events sent to Eventun must populate the data used by medals, achievements, masteries, and challenges.
2. The game should begin sending medal data in Eventun events; this is not currently the case.
3. Eventun should accumulate relevant stats after a successfully completed match.
4. After accumulation, Eventun should evaluate each player's medal, achievement, mastery, and challenge progression.
5. Eventun should record newly completed goals and claimable rewards.
6. Evaluation should be reliable if a match summary is accepted more than once or retried.
7. Evaluation should be able to backfill from historical Eventun events where sufficient source data exists.
8. Match-start or match-context events must identify whether the match is eligible for durable competitive stats.
9. Competitive stats eligibility must apply beyond achievements and medals, including course records, career stats, leaderboards, and similar derived stat surfaces.
10. Special matches, such as races with different starting parts, fewer laps, modified course defaults, or nonstandard modes, may be marked not eligible for competitive stats.
11. Eventun should rely on the game-authored eligibility signal rather than inferring comparability from copied course defaults where the game can provide the authoritative answer.
12. Progress, record, and stat evaluation must respect the match's competitive stats eligibility.

### Notification and Claim Requirements

1. Players need a way to learn that achievements, masteries, or challenges completed.
2. Claiming a reward can serve as a notification surface.
3. The design must evaluate whether claim-only notification is too brittle.
4. After the event batch for a match is accepted and evaluated, the game client must be able to determine which goals were achieved and which rewards became claimable.
5. The exact API shape for post-match completion lookup is a solution-design decision rather than a settled requirement.
6. If a post-match "new completions" API exists, Eventun may need an inbox/read-state model so already-seen completions are not repeatedly returned as new.
7. V1 should focus on game-client visibility before public website visibility.
8. The game client already knows which medals were awarded during the match, so Eventun does not need to be the immediate post-match medal notification source.
9. Eventun should support career medal totals so the game client and future website can replace AccelByte-backed medal stat display.
10. A durable notification inbox is not a V1 requirement.
11. AccelByte player messaging may be a candidate for later notification delivery and should be researched before building an Eventun notification system.
12. Completed achievements, masteries, challenges, medal totals, and related progression stats can be publicly readable by default unless a specific definition or future privacy requirement says otherwise.
13. The game client and website decide which public stats to surface in their own presentation contexts.
14. Achievement, mastery, and challenge presentation may require assets such as icons or 2D images, but asset storage and delivery are solution-design details rather than requirements. The solution may use Eventun uploads, client-bundled assets, or another approach.

### Administration Requirements

1. Operators eventually need UI to define and maintain achievements, masteries, challenges, and rewards.
2. Operators eventually need UI to inspect a player's progress and completed goals.
3. Operators eventually need UI to retry failed reward grants.
4. AccelByte Extend App UI remains a candidate operator surface.
5. Ascentun remains a useful reference for existing admin workflows but should not drive the final embedded UI architecture by default.
6. Initial admin correction can be handled through SQL until common correction workflows justify dedicated tools.

## Initial Product Rules

- Medals are gameplay-recognition events, not the primary reward surface.
- Achievements are persistent progression goals.
- Masteries are achievement-category goals focused on parts and weapons.
- Challenges are time-windowed achievement-category goals.
- Rewards are attached to achievement, mastery, or challenge completion.
- Augmented medals replace base medals for the same occurrence.
- Avoid augments-on-augments in the initial model.
- The game runtime owns medal-rule logic.
- Eventun stores medal facts and derives progression from those facts.
- Only qualified, successfully completed matches should affect durable medal/progression stats.
- Only competitively eligible matches should affect durable records, career stats, progression, leaderboards, and similar competitive stat surfaces.
- Eventun owns progression evaluation.
- AccelByte owns fulfillment for AccelByte-backed rewards.
- Earned rewards should not expire by default.
- Progression and medal data can be public by default; public API access is acceptable and can support community stats sites.
- The game client must be able to determine post-match achieved goals and claimable rewards after Eventun evaluates the accepted match batch.

## Initial Processing Flow

The desired high-level flow is:

1. Gameplay sends existing match, player, combat, loadout, and result events to Eventun.
2. Match context identifies whether the match is eligible for durable competitive stats.
3. Gameplay also sends final medal awards to Eventun as part of the successful match event batch.
4. Eventun stores the raw event and medal facts.
5. After a competitively eligible successful match, Eventun accumulates player stats and medal counts.
6. Eventun evaluates achievement, mastery, and challenge progress for participating players.
7. Eventun records newly completed goals.
8. Eventun creates claimable rewards for completed goals that have rewards.
9. The game client surfaces new completions and claimable rewards from Eventun.
10. On claim, Eventun grants the reward through the appropriate AccelByte API or Eventun-owned economy path.
11. Eventun marks the local reward as claimed after the grant succeeds, or keeps it retryable if the grant fails.

## Assumptions

- Player rewards should be claimed through Eventun-owned claimable reward state. V1 local states are `earned`, `claiming`, and `claimed`; claim errors are tracked as fields rather than first-class visible states.
- Medals are useful as normalized progression events even when a raw Eventun event could also derive the same fact.
- A "double kill" or similar compound medal will be generated by game/runtime logic.
- ARC and skins are expected V1 reward examples and should be AccelByte-backed where possible. Titles are a future reward-type example and may be AccelByte-backed if/when implemented.
- Item identity details are solution scope. The current expectation is that weapon and part progression will likely use SKU and not AccelByte item ids.
- A player-specific read/inbox state may be useful later if the game needs reliable post-match "new completion" notifications, but it is not a V1 requirement.
- Raw AccelByte entitlements do not appear to support generic player-side `UNCLAIMED` state. AccelByte Challenge rewards do, but only inside the Challenge service model.

## Resolved Requirements Decisions

1. The game runtime owns medal-rule logic; Eventun should not derive medal eligibility.
2. Medals are awarded during heats and sent to Eventun in the final successful match event batch.
3. Raw event tables hold the facts; derived views, materialized views, or tables can be added as the solution requires.
4. Heat-level part usage is the required mastery primitive because players choose parts per heat; match-level usage is optional if easy to derive.
5. Boolean requirement expressions are desirable if they do not add disproportionate complexity.
6. Each completed goal should create one claimable reward bundle, and the bundle may contain multiple grant entries.
7. Completion should immediately create locally claimable rewards; no normal approval flow is expected.
8. V1 reward bundle state should be `earned`, `claiming`, and `claimed`, with errors tracked as fields.
9. Limited-supply rewards are deferred, but the model should not rule them out.
10. Match context should include a game-authored competitive stats eligibility signal.
11. Earned rewards should not expire by default.
12. Daily, weekly, and monthly challenge assignments should be persisted per player for each active time window.
13. Initial daily, weekly, and monthly challenge pools should be shared across players.
14. Challenge assignment should consider owned items when the challenge requires a specific part or weapon.
15. Rerolls are deferred pending design-team direction.
16. Seasonal challenges are fixed for V1 once the season starts; mid-season definition edits are V2.
17. Eventun should support career medal totals for game client and future website display.
18. Progression and medal data can be public by default, with game client and website presentation deciding what to show.
19. Public stats APIs are acceptable and may help community tools and external stats sites.
20. The exact post-match completion lookup API is a solution-design concern, not a settled requirements constraint.
21. V1 rewards should be AccelByte-backed where possible; titles are a future expansion example, not a committed V1 reward type.
22. Presentation asset storage and delivery should not be prescribed as a requirement.
23. Initial administration and correction can use SQL until repeated workflows justify dedicated tools.

## Open Requirements Questions

1. Should old challenge data be saved or lost when a new set of challenges
2. What other historical tracking is required if any
3. 

## Deferred Solution Areas

These areas should be designed after the requirements are settled:

- Eventun schema
- event payload shape for medals
- item identity and reward reference model, likely SKU-oriented rather than AccelByte item-id-oriented
- match context field naming and payload shape for competitive stats eligibility
- stat and medal aggregation strategy
- requirement expression model
- challenge assignment model
- reward claim and fulfillment state machine
- notification/read-state model
- admin API surface
- Extend App UI scope
- backfill and reconciliation tooling

## Sources

- Prior research draft: `00_inbox/2026-05-20-eventun-medal-management-accelbyte-extend-ui.md`
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
