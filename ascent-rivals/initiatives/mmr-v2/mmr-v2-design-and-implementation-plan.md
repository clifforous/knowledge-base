# Ascent Rivals MMR v2 Design and Implementation Plan

## Status

Draft for implementation review, 2026-07-16.

## Decision Summary

- Keep the Weng-Lin Plackett-Luce Bayesian rating model, but replace the current implementation with a direct, tested implementation of the published free-for-all algorithm.
- Treat MMR v2 as an internal lifetime skill estimate for the item recommender. It is not a matchmaking input, public rank, leaderboard value, progression reward, or gauntlet qualification score.
- Rate authoritative Ascent match outcomes only. Do not combine Classic, Deathmatch, time-trial, client-reported, or future-mode results into this rating without a separate design decision.
- Build rating inputs from finalized match participant rows, not live racer entities or Circuit Points reconstructed by the rating utility.
- Reuse `cp-skill-rating` and `cp-skill-uncertainty`, but reset every existing player to the active new-player defaults at the v2 cutover. Do not migrate or seed from v1 values.
- Add an algorithm-version marker so v1 state is never consumed as v2 state and missed accounts reset lazily on first use.
- Preserve the item recommender's career-rank fallback while a reset player remains provisional.

## Goal

Deliver a small, correct, and testable skill-rating system that gives the item recommender a better player-archetype signal without creating a premature competitive-ranking platform.

The implementation should:

- produce valid Weng-Lin Plackett-Luce updates for ordered multiplayer results and ties;
- use the same authoritative result and roster semantics as match summaries;
- retain committed disconnected racers and exclude spectators and non-participants;
- distinguish a real new player from a failed or incomplete rating load;
- avoid consuming or preserving known-untrustworthy v1 values;
- persist the rating pair reliably enough for its current low-stakes consumer; and
- leave an explicit boundary for a future matchmaking-grade or backend-owned rating service.

## Facts

- The existing implementation identifies itself as the Weng-Lin Plackett-Luce free-for-all model from "A Bayesian Approximation Method for Online Ranking."
- Its tie-bucket implementation is not equivalent to the published algorithm. Equal tied players can all gain mean rating from a complete tie.
- Match-end rating inputs currently come from live human racer entities. A disconnected committed participant can therefore be absent from rating calculation.
- The current human-competitor predicate checks human player type but does not prove that the entity is an active competitor.
- Rating and uncertainty load asynchronously from separate AccelByte statistic items and are persisted as separate statistic updates.
- The only identified runtime consumer is `HGItemRecommender`. It uses rating only when uncertainty is below `2.0`; otherwise it derives the player archetype from career rank.
- The item recommender maps skill-rating bands to recommendation archetypes. Its current final branch maps a rating at or above the Ascendant threshold back to `Beginner`, which is not a valid high-skill fallback.
- C++ fallback defaults are mean `25.0` and uncertainty `25.0 / 3.0`. The active `DefaultGameSettings` Data Asset can override those values and is authoritative for the reset.
- The current competitive-mode C++ default contains Ascent only.
- Eventun does not currently own MMR state. AccelByte Statistics remains the current persistence surface.

## Assumptions

- The participant-row and match-finalization work described in [[reconnect-state-restoration-initial-implementation-plan-2026-04-29]] is the source of truth for authoritative match membership and results.
- The active player population can tolerate becoming provisional again because MMR is not used for matchmaking, admission, rewards, or a public competitive surface.
- Career rank remains a safe item-recommender fallback while v2 uncertainty is above its confidence threshold.
- A player cannot legitimately complete overlapping authoritative matches. If this assumption changes, AccelByte statistic-item persistence is insufficient for ordered rating updates.
- V2 can remain game-computed and AccelByte-stored. Backend ownership, history, and seasonal rating remain later decisions.

## Non-Goals

V2 does not introduce:

- skill-based matchmaking;
- a visible division or leaderboard;
- seasonal rating resets after the one-time v2 cutover;
- team ratings;
- cross-mode or per-course ratings;
- kill, damage, survival-time, loadout, or telemetry-based rating evidence;
- Eventun rating ownership or history;
- bot ratings;
- client-authoritative or time-trial rating updates; or
- compatibility with existing v1 rating values.

If MMR becomes a matchmaking, reward, admission, or public-ranking input, it requires a new review of persistence atomicity, abuse resistance, calibration, mode separation, and operational recovery before that use is enabled.

## Terminology

| Term | Meaning |
|---|---|
| MMR v2 | Historical project name for the internal v2 skill estimate. It is not currently used for matchmaking. |
| Mean / `mu` | Current estimate of player skill, stored in `cp-skill-rating`. |
| Uncertainty / `sigma` | Standard deviation of the skill estimate, stored in `cp-skill-uncertainty`. |
| Provisional | A valid v2 rating whose uncertainty is too high for the item recommender to use. |
| Rating-ready | Rating state was loaded or initialized successfully, has algorithm version 2, and contains finite valid values. |
| Rated match | An authoritative completed match that passes the v2 eligibility contract. |
| Rank group | One or more participants with the same official outcome rank. |

## Model Decision

Use the Weng-Lin Plackett-Luce free-for-all update from Algorithm 4 of [A Bayesian Approximation Method for Online Ranking](https://jmlr.org/papers/volume12/weng11a/weng11a.pdf).

This remains the best fit because an Ascent result is an ordered multiplayer outcome, the model represents uncertainty, and it supports ties without converting one race into many correlated head-to-head matches. Retaining the model family also preserves the existing `mu`/`sigma` scale and keeps the item-recommender integration small.

Do not add TrueSkill2-style combat telemetry in v2. Individual kills or damage can be strategically useful, but a controllable secondary metric can also redirect behavior away from the official win condition. That extension requires historical validation and a separate design.

### Algorithm Requirements

The rating utility must be a pure function over explicit participant inputs:

```text
input participant:
  player_id
  pre_match_mu
  pre_match_sigma
  rank_group

output participant:
  player_id
  post_match_mu
  post_match_sigma
```

The utility must not read player entities, Circuit Points, credits, connection state, or session settings. A separate authoritative outcome adapter owns those decisions.

Required mathematical behavior:

- Implement the published per-participant iteration for ties. Do not collapse tied players into a unique bucket unless the aggregate formula is independently derived and proven equivalent.
- A complete tie between equal players must produce zero mean change for every player.
- Use numerically stable probability calculations instead of unbounded raw exponentials.
- Reject duplicate player ids, invalid rank groups, non-finite values, non-positive uncertainty, non-positive beta, and fewer than two participants.
- Never emit a non-finite mean or uncertainty.
- Keep uncertainty positive and cap it at the configured new-player uncertainty after applying dynamics.
- Add a configurable per-rated-match dynamics value `tau`. The initial candidate should be `InitialSkillUncertainty / 100`; confirm it through fixed simulations before rollout.
- Apply dynamics to the pre-match uncertainty:

```text
sigma_prior = min(initial_sigma, sqrt(sigma * sigma + tau * tau))
```

- Keep time-based inactivity inflation out of v2. It can be added if the rating later becomes operationally important and inactivity data is available at load time.

### Settings

Keep model parameters in `FHGSkillRatingSettings` and validate them when settings load:

- `InitialSkillRating`
- `InitialSkillUncertainty`
- `Beta`
- `Tau`
- uncertainty multiplier floor or an equivalent explicit numerical guard
- `MinCompetitiveParticipants`
- `CompetitiveRaceModes`
- `ItemRecommenderMaxSkillUncertainty`
- `AlgorithmVersion`, fixed to `2` for this release
- `bSkillRatingV2Enabled`
- `bSkillRatingWritesEnabled`

The reset and new-player initialization must use the resolved active settings values. The C++ fallback values are examples, not a release-runbook source of truth.

## Authoritative Match Outcome Contract

### Match Eligibility

A match updates MMR v2 only when all of the following are true:

- it completed normally on an authoritative dedicated server;
- the session explicitly marks the match as skill-rated;
- its race mode is enabled in `CompetitiveRaceModes`, initially Ascent only;
- final participant rows and final standings were finalized successfully;
- at least `MinCompetitiveParticipants` included human participants exist;
- every included participant has a rating-ready pre-match snapshot; and
- the match has not already produced a rating update in this server process.

Do not infer skill-rated status from race mode alone. Public playlists may enable it by default, while custom games, debug sessions, tournament stages, and other server flows must opt in deliberately.

If any included participant has a failed or unresolved rating load, skip the whole match update. Excluding only that player would change the field and corrupt every other update.

### Participant Inclusion

Build one rating input for each finalized match-standing row that represents a committed human competitor.

Include:

- connected committed human competitors;
- reconnected committed human competitors;
- committed human competitors who disconnected and received a finalized DNF/unplaced result; and
- timed-Ascent participants that the authoritative finalization rules grant a ranked result.

Exclude:

- bots;
- permanent and temporary spectators;
- players who never committed to the final match result;
- discarded replacement bots;
- late joiners who remained spectators;
- incomplete client/local matches; and
- participants lacking valid player identity or rating-ready state.

Participant inclusion must call the canonical competitor/result predicates. A function named `IsHumanCompetitor` must verify both properties rather than checking player type alone.

### Rank Construction

Use the finalized official result, not raw Circuit Points inside the rating utility.

- Numbered final placements define ordered rank groups.
- Official ties share one rank group.
- Finalized DNF/unplaced participants are tied in one group below every participant with a valid numbered placement.
- A disconnect does not remove a committed player from the outcome.
- Do not order DNFs by disconnect time, kills, partial progress, or frozen checkpoint unless the game-design result contract later makes that ordering official.
- If the match result cannot produce a complete deterministic sequence of rank groups, skip rating rather than inventing an order.

This makes rating semantics match the player-visible result and avoids using hidden tie-breakers that reward behavior outside the official objective.

## Rating State Lifecycle

### State Shape

Represent the runtime state explicitly:

```text
skill rating state:
  mu
  sigma
  algorithm_version
  load_state: unresolved | ready | failed
  initialization_source: existing_v2 | new_player | v1_reset
  request_generation
```

Do not use numeric defaults alone to imply that an asynchronous load completed successfully.

### Load And Initialization

On player registration:

1. Start one versioned rating-state request.
2. Load `cp-skill-rating`, `cp-skill-uncertainty`, and `cp-skill-version`.
3. Ignore callbacks whose request generation is no longer current.
4. If version is `2` and both values are present, finite, and valid, mark the state ready.
5. If version is missing or not `2`, ignore both legacy values, initialize from the active new-player defaults, and enqueue the v2 reset write.
6. If this is a genuinely new player with missing statistics, use the same default initialization path.
7. If version is `2` but either value is missing or invalid, mark the load failed and repair by resetting to defaults. Do not combine one stored value with one default value.
8. Do not let a stale load callback overwrite a computed or persisted match result.

When a player becomes committed to a skill-rated match, copy their ready `mu`, `sigma`, and version into match-owned participant state. Match completion must use that immutable snapshot even if the live entity disconnects or later receives another callback.

### Persistence

Continue using:

- `cp-skill-rating`
- `cp-skill-uncertainty`

Add:

- `cp-skill-version`

Persist absolute post-match values with `OVERRIDE`, not additive operations. This makes a retry of the same computed result idempotent.

Required write behavior:

- inspect success for every returned stat item;
- treat a missing response item as failure;
- retry failed rating or uncertainty writes with the same absolute computed pair;
- keep the player rating state non-ready for a subsequent rated match until both values are confirmed;
- log bounded failure details with match id and stat code;
- never advance the version marker for a reset until both default values are confirmed; and
- never mutate an entity to a partially persisted pair.

Before implementation, verify whether the configured AccelByte Statistics operation provides atomic all-item behavior. If it does not, v2 accepts bounded retry and reconciliation because the rating currently affects only item-recommender classification. This persistence model must be replaced with one atomic versioned record before MMR is used for matchmaking, rewards, admission, or a public competitive surface.

## V1 Reset And Cutover

V1 rating values are not migration inputs.

### Reset Rule

For every account:

```text
cp-skill-rating = resolved InitialSkillRating
cp-skill-uncertainty = resolved InitialSkillUncertainty
cp-skill-version = 2
```

At the current C++ fallback settings this is `25.0` and `25.0 / 3.0`, but release operations must read and record the deployed `DefaultGameSettings` values before reset.

### Reset Mechanism

Use both mechanisms:

1. Run an administrative bulk reset for existing accounts while v1 and v2 writes are disabled.
2. Keep lazy version-based reset in the game server so dormant, missed, or newly created accounts cannot consume v1 state later.

The lazy path is authoritative: any version other than `2` causes both old values to be discarded, even if they appear numerically valid.

### Cutover Sequence

1. Record the resolved production defaults and competitive settings in the release runbook.
2. Configure `cp-skill-version` in AccelByte.
3. Deploy the v2 load/reset logic with calculation and match-end writes feature-disabled.
4. Disable v1 writes.
5. Run the administrative reset and verify sampled accounts contain the default pair and version `2`.
6. Enable v2 calculation in shadow logging without persistence and verify outcome construction and deltas.
7. Enable v2 persistence.
8. Monitor initialization, skip, partial-write, retry, and non-finite counters.
9. Remove the v1 calculation path after the rollback window.

Rollback disables v2 writes and leaves the item recommender on its career-rank fallback. It does not restore v1 ratings.

## Item Recommender Contract

The item recommender remains the only v2 consumer.

- Use skill rating only when rating state is ready, algorithm version is `2`, and uncertainty is below `ItemRecommenderMaxSkillUncertainty`.
- Make the current `2.0` threshold a setting rather than a hard-coded literal.
- While a reset player is provisional, preserve the existing career-rank archetype fallback.
- Map ratings monotonically to archetypes. Ratings at or above the highest configured division threshold must map to the highest-skill recommendation archetype, not `Beginner`.
- Treat missing, failed, invalid, or version-mismatched rating state as provisional.
- Do not expose exact `mu` or `sigma` to the player.

The reset will temporarily increase career-rank fallback usage. That is accepted behavior. Do not lower the uncertainty threshold merely to make the new rating take effect sooner; calibrate the threshold from v2 convergence evidence.

Because corrected ties and reset state will change the rating distribution, review the existing `DivisionRatings` thresholds after shadow and early live data. Do not assume bands tuned against v1 retain the same population meaning.

## Observability

Record structured server diagnostics for:

- algorithm version;
- match id and race mode;
- included participant count and rank-group count;
- update applied or skipped;
- a bounded skip-reason code;
- reset source: administrative, new player, or lazy v1 reset;
- per-item persistence success/failure and retry outcome;
- invalid input or non-finite output rejection; and
- item-recommender use of v2 versus career fallback.

Do not emit verbose per-player rating deltas in normal production logs. A gated diagnostic mode may emit them for controlled validation.

Initial skip reasons should include:

```text
disabled
not_authoritative
not_skill_rated
unsupported_mode
incomplete_result
insufficient_participants
rating_state_not_ready
invalid_participant
invalid_rank_groups
already_processed
persistence_failed
```

Eventun rating history and analysis are deferred. If historical replay becomes necessary, add an explicit accepted rating-event contract rather than reconstructing rating state from general gameplay telemetry without version and outcome semantics.

## Implementation Plan

### Task 1: Confirm Runtime Configuration And AccelByte Contract

Review checkpoint before code mutation:

- Inspect the active `DefaultGameSettings` Data Asset and record the deployed `mu`, `sigma`, `beta`, competitive modes, participant minimum, division thresholds, and any existing overrides.
- Inspect AccelByte definitions and permissions for both existing stat codes.
- Confirm bulk `OVERRIDE` response and partial-failure semantics.
- Add and permission `cp-skill-version`.
- Confirm which session or match configuration should authoritatively expose `skill-rated` status.

Do not proceed with reset tooling until the deployed defaults and stat-write semantics are recorded.

### Task 2: Replace The Core Rating Utility

Primary files:

- `Source/AscentRivals/Public/Utils/HGSkillRatingUtils.h`
- `Source/AscentRivals/Private/Utils/HGSkillRatingUtils.cpp`
- `Source/AscentRivals/Public/HGGameSettings.h`

Work:

- Replace entity/Circuit-Points-shaped input with explicit `mu`, `sigma`, and rank-group inputs.
- Implement the published Weng-Lin Plackett-Luce update directly.
- Add stable exponent/probability calculation and input/output validation.
- Add `Tau`, algorithm version, feature flags, and the configurable recommender uncertainty threshold.
- Return a complete result or a typed failure; never return a partial player set.
- Keep the utility deterministic and free of persistence or Unreal entity access.

### Task 3: Build Rating Inputs From Finalized Participant Rows

Primary files:

- `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`
- `Source/AscentRivals/Public/Server/Subsystems/HGStatsServerSubsystem.h`
- `Source/AscentRivals/Private/Server/Entities/HGSessionEntity.cpp`
- participant-row types owned by the match/session implementation

Work:

- Add one authoritative outcome adapter from finalized match standings to rating rank groups.
- Use the canonical competitor predicate, not player type alone.
- Include finalized disconnected DNF rows and exclude spectators/bots.
- Tie all unplaced DNF rows below placed finishers.
- Require a complete rating-ready snapshot for every included player.
- Add a per-match processed guard.
- Remove MMR dependence on the live-racer enumeration and raw Circuit Points sorting.

This task depends on match-owned participant rows being complete enough to retain rating identity and pre-match rating state after disconnect.

### Task 4: Make Rating Load State Explicit

Primary files:

- `Source/AscentRivals/Public/Server/Entities/HGPlayerEntity.h`
- `Source/AscentRivals/Private/Server/HGServerScript.cpp`
- player lifecycle/participant snapshot types

Work:

- Add explicit unresolved, ready, and failed state.
- Load the v2 version marker with the rating pair.
- Add stale-callback generation protection.
- Initialize new and version-mismatched players from resolved defaults.
- Reset both values when either part of a purported v2 pair is missing or invalid.
- Capture immutable rating state when the player commits to a rated match.
- Prevent late callbacks from overwriting committed or newly persisted state.

### Task 5: Add Reliable Persistence And Reset Handling

Primary file:

- `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`

Work:

- Validate per-stat success in bulk responses.
- Keep one pending absolute result pair for retry.
- Retry partial failures without recomputing from a partially updated pair.
- Mark the player ready only after the full pair is confirmed.
- Write the reset version marker only after both reset values succeed.
- Add bounded skip/failure diagnostics.
- Keep v1 and v2 writes behind separate cutover flags until v1 is removed.

Create a separate reviewed operational reset procedure or tool for the administrative bulk reset. Do not hide a global account mutation inside ordinary match code.

### Task 6: Update The Item Recommender

Primary file:

- `Source/AscentRivals/Private/Item/HGItemRecommender.cpp`

Work:

- Require ready version-2 state before using skill.
- Replace the hard-coded uncertainty threshold with settings.
- Preserve career-rank fallback for provisional players.
- Fix the highest-rating branch so it maps to the highest-skill archetype.
- Add monotonic boundary tests for every division threshold.
- Add diagnostics distinguishing v2 use from career fallback.

### Task 7: Replace Self-Confirming Simulation With Fixed Verification

Primary files:

- `Source/AscentRivals/Public/Utils/HGSkillRatingSim.h`
- `Source/AscentRivals/Private/Utils/HGSkillRatingSim.cpp`
- existing editor simulation asset code

Work:

- Add immutable golden vectors derived independently from the published algorithm.
- Do not generate the expected fixture by running the implementation under test.
- Match runtime rank-group construction rather than using a separate Circuit Points table.
- Add adversarial fixtures for ties, DNFs, disconnects, invalid settings, extreme values, and participant-order permutations.
- Keep synthetic population simulation as exploratory evidence only.

### Task 8: Roll Out Behind Flags

- Run fixed algorithm and outcome tests.
- Exercise load failure, stale callback, partial response, and retry cases in controlled server tests.
- Shadow-log v2 results with writes disabled.
- Perform and sample the administrative reset.
- Enable writes for a small controlled environment first.
- Confirm provisional players use career fallback without recommendation regressions.
- Review early v2 distribution before accepting the existing division thresholds.
- Enable production writes and retain a write-disable rollback flag through the observation window.
- Remove v1 code and temporary shadow logging after acceptance.

## Verification Matrix

### Rating Math

- Two equal players tie: both mean changes are zero.
- Entire equal lobby ties: every mean change is zero.
- Equal symmetric lobby with unique order: winner increases, loser decreases, and all outputs remain finite.
- Participant input permutation does not change per-player results.
- Reordering players inside one tie group does not change results.
- An upset produces a larger correction than an expected result.
- Repeated evidence reduces uncertainty while per-match dynamics prevents a zero-uncertainty state.
- Invalid parameters and non-finite inputs fail closed without persistence.

### Outcome Construction

- Temporary and permanent spectators are excluded.
- A human entity that is not a competitor is excluded.
- A committed final-heat disconnect remains as DNF.
- Multiple DNF rows share the bottom rank group.
- A result completed before disconnect retains its official numbered placement.
- A timed-Ascent participant receives exactly the official finalized result.
- A late joiner who did not commit is excluded.
- Bots are excluded without deleting human relative ordering.
- Incomplete/crashed matches do not update ratings.

### State And Persistence

- Missing version discards both legacy values and resets to defaults.
- Version 2 with one missing stat resets the pair; it never mixes a stored value with a default.
- Stale load callbacks cannot overwrite newer state.
- Disconnect after commitment does not lose the pre-match snapshot.
- Partial write responses are detected and retried.
- Repeating an absolute write produces the same state.
- A player cannot enter another rated match with an unresolved partial write.
- A match-completion callback cannot apply the update twice in one server process.

### Item Recommender

- Reset/default uncertainty uses career-rank fallback.
- Ready v2 state below the threshold uses skill-rating bands.
- Every threshold boundary maps monotonically.
- Ratings at and above the highest threshold map to the highest-skill archetype.
- Invalid or version-mismatched state falls back safely.

## Acceptance Criteria

MMR v2 is ready when:

- no v1 rating or uncertainty value can be consumed after cutover;
- all active accounts resolve to the configured default pair before accumulating v2 evidence;
- published Weng-Lin golden vectors pass, including complete-tie cases;
- rating inputs come only from finalized authoritative participant rows;
- committed disconnects and DNFs follow the documented outcome policy;
- async load failure cannot masquerade as a successful default load;
- partial backend responses are detected and reconciled or the rating remains non-ready;
- the item recommender safely falls back while players are provisional;
- high ratings cannot map back to the beginner archetype;
- rollout can disable v2 writes without affecting match completion; and
- operational defaults, flags, reset evidence, and rollback steps are recorded.

## Risks And Follow-On Decisions

### AccelByte Statistic Pair Is Not An Atomic Rating Record

Two numeric statistic items cannot provide the same integrity as one versioned rating object. Bounded absolute-write retry is acceptable only because the current consumer is low-stakes. Before matchmaking or public rank, move to an atomic backend record with revision and last processed match identity.

### Reset Delays Item-Recommender Skill Use

Players return to the career-rank fallback until uncertainty falls below the configured threshold. This is intentional. Lowering the threshold without calibration would substitute immediacy for correctness.

### Participant-Row Dependency

MMR v2 should not ship on another live-entity workaround. If finalized participant rows cannot retain disconnected identity, official result, and the pre-match rating snapshot, finish that contract first.

### Mode Expansion

Classic and Deathmatch have different objectives. Do not mix them into the Ascent rating. A later expansion should prefer separate mode ratings or a researched shared-skill-plus-mode-offset model.

### Future Matchmaking Use

Using v2 for matchmaking would require additional design for match-quality calculation, latency/region constraints, party ratings, smurf handling, inactivity, seasonal policy, operational recovery, abuse resistance, and calibration. This document does not approve that use.

## Related Knowledge Base Documents

- [[ascent-rivals/system/game-design|game-design]]
- [[ascent-rivals/system/game-client|game-client]]
- [[ascent-rivals/system/race-roster-rules|race-roster-rules]]
- [[reconnect-state-restoration-initial-implementation-plan-2026-04-29]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

## External References

- Weng, R. C. and Lin, C. J., [A Bayesian Approximation Method for Online Ranking](https://jmlr.org/papers/volume12/weng11a/weng11a.pdf), JMLR 2011.
- Microsoft Research, [TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/).
- Minka, Cleven, and Zaykov, [TrueSkill 2: An Improved Bayesian Skill Rating System](https://www.microsoft.com/en-us/research/publication/trueskill-2-improved-bayesian-skill-rating-system/), 2018.
- Ebtekar and Liu, [Elo-MMR: A Rating System for Massive Multiplayer Competitions](https://cs.stanford.edu/people/paulliu/files/www-2021-elor.pdf), 2021.
