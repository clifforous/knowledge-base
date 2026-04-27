# Gauntlet Finals and Tournament Modes Design Review

Date: 2026-04-09

## Related
- [[gauntlet-stage-orchestration-improvements]]
- [[../50_knowledge/ascent-rivals/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[../50_knowledge/ascent-rivals/game-design|game-design]]

## Goal

Support these finals and tournament modes without turning Eventun into a pile of mode-specific branches:

- player qualified finals
- player invited finals
- team qualified finals
- team invited finals
- future single-elimination and double-elimination brackets

The core design question is not only how to support each mode individually. The harder question is how to support them through one coherent model so the dedicated server, game client, admin tools, and backend all operate on the same concepts.

## Short Answer

The current direction is mostly right, but the stage rule model will become brittle if it keeps growing sideways.

Good direction already in place:

- durable `gauntlet_stage_run`
- stage-run identity carried into the AccelByte session
- dedicated-server claim/admission by `StageRunId`
- explicit player invite list for a stage
- creator/admin defer control and admin launch-now control

Where the current shape starts to break down:

- `entry_requirement` is doing too much conceptual work
- `allowed_teams`, groups, explicit player invites, standings cutoffs, and bracket win/loss filters are all different kinds of selection input but are not modeled the same way
- `gauntlet_player_status` is gauntlet-wide, not stage-specific, so it is a weak place to store explicit entrant state
- team qualification and bracket progression need a cleaner abstraction than adding more conditionals to `GauntletStage`

## Design Conclusion

The simplest durable model is to separate these concerns explicitly:

1. competition unit
2. selection source
3. admission policy
4. runtime assignment snapshot
5. progression state

That gives one stage-run lifecycle and one DS contract that can support all of the requested modes.

## Real-World Pattern Review

## Motorsport separates individual and team qualification

Real-world racing usually separates the individual championship from the team championship.

Examples:

- Formula 1 Constructors' Championship aggregates points at the team level across both cars.
- Formula E has separate Drivers' and Teams' World Championships, with the teams title based on the combined score of the driver pairing.
- Endurance racing series often use entrant or manufacturer scoring rules that do not simply count every participant equally.

The important lesson is that the race can still be contested by individual drivers while qualification is computed at the team level with a configurable aggregation rule.

That maps cleanly to team qualified finals in Ascent Rivals:

- qualification can be computed from a team's top N scorers
- admission to the final can still be limited to the top M active racers from that team

## Invitationals materialize the field explicitly

Invitation-style motorsport events usually materialize the field before competition begins.

Race Of Champions is a clear example because it supports both:

- an invited individual field
- an invited team competition through the ROC Nations Cup

The field is explicit. The event does not depend on a live standings query at race-start time to decide who belongs.

That is a strong pattern for invite-only finals and later bracket rounds: resolve entrants first, then run the competition.

## Esports separates qualification from finals execution

Competitive games usually separate three things:

- qualification
- seeding
- bracket execution

Examples:

- ALGS runs a qualification or group phase first, then seeds teams into a bracket stage, then advances a final field.
- VALORANT Champions qualifies teams from league finish and points, then runs a separate tournament phase with group stage and playoffs.

The important lesson is that the match server does not recompute the whole tournament model from scratch during lobby joins. The competition system resolves who belongs in the phase, then the match runtime enforces that resolved field.

That is the right mental model for Eventun too.

## Recommended Unified Model

## 1. Competition Unit

Every stage should declare what the stage fundamentally selects and advances:

- `player`
- `team`

This matters more than `entry_requirement`.

Why:

- player finals qualify players directly
- team finals qualify teams even if individuals still race inside the session
- bracket progression may advance either players or teams

## 2. Selection Source

Every stage should declare how entrants are selected:

- `open`
- `explicit_invite`
- `player_standings`
- `team_standings`
- `progression`

This should become the main selection abstraction.

Semantics:

- `open`: any valid human competitor may join
- `explicit_invite`: explicit player or team list is authoritative
- `player_standings`: qualify from player leaderboard rules
- `team_standings`: qualify from team leaderboard rules
- `progression`: qualify from earlier stage outcomes, usually brackets or promotion/relegation rounds

This is cleaner than treating `invite`, `qualification`, `allowed_teams`, groups, and wins/losses as peer concepts.

## 3. Admission Policy

Selection and admission are not the same thing.

A team can qualify for a final while only a limited number of its players may actively race.

A stage therefore also needs admission policy.

Recommended admission fields:

- `players_per_team` as the current team admission cap
- `overflow_policy`
- `admission_priority_rule`
- `roster_lock_point`

Suggested semantics:

- `players_per_team`: maximum active racers from one team for team-based stages
- `overflow_policy`:
  - `reject_new`
  - `replace_lowest_prestart`
- `admission_priority_rule`: how allowed players are compared when capacity or replacement decisions need priority, for example `first_come`, `qualification_points`, `selection_rank`, `team_member_rank`, or `bracket_seed`
- `roster_lock_point`:
  - `match_start`

This directly supports the team final use case:

- team qualifies because its top N scorers produced enough team points
- the stage allows only M racers from that team
- before race start, if a higher-ranked teammate joins, the DS can replace a lower-ranked teammate already in the lobby
- after race start, the roster is frozen

## 4. Runtime Assignment Snapshot

No matter how a stage was selected, the dedicated server should always see one resolved shape:

- stage-run identity
- stage rules
- resolved entrants for that run
- ordered admission data when team caps matter

This is the main unifying idea in the design.

The DS should not care whether the stage came from:

- a player invite list
- a team invite list
- a player standings cutoff
- a team standings cutoff
- a bracket builder

The DS should receive one stage-run snapshot and enforce it.

Long term, this should be a real runtime table such as:

- `gauntlet_stage_run_entry`
- and optionally `gauntlet_stage_run_player`

The input sources can stay different. Runtime enforcement should be one shape.

`gauntlet_stage_run_entry` should represent the resolved entrant field for one run. For player stages, one row would represent one selected player. For team stages, one row would represent one selected team. Useful columns include run id, entrant type, player id or team id, selection source, seed/rank, priority score, and compact metadata used for audit/debugging.

`gauntlet_stage_run_player` should exist only if team stages need per-member eligibility or ordered roster data. It would sit under a team entry and record the candidate player id, team id, member priority/rank, qualification score, and whether the player is eligible to occupy one of the team's active racer slots.

These snapshot tables should not replace `gauntlet_stage_run_admission`. The snapshot says "these entrants were resolved for this run." Admission says "this player asked to join/rejoin and Eventun evaluated that request."

## 5. Progression State

Bracket routing should not be modeled only as current win/loss filters at join time.

Instead:

- bracket configuration defines the structure
- accepted stage outcomes update progression
- Eventun materializes the next stage entrants explicitly

`gauntlet_player_status` or a future team equivalent can still exist, but only as summary or convenience state. It should not be the sole authoritative bracket router.

## Participation Rule

A player or team should only be treated as having competed in a stage if the run reaches accepted completion after race start.

Recommended rule:

- not competed: joined the lobby and left before race start
- not competed: session failed, aborted, deferred, or crashed before accepted completion
- competed: the race actually started and the run completed successfully
- competed even if disconnected mid-race: yes, if the run completes and the player or team was a valid participant

That means participation should not be consumed on join, claim, or lobby presence. It should only be consumed when Eventun accepts a completed stage result.

This keeps retries fair for failed finals and failed bracket rounds.

## How The Requested Modes Fit This Model

| Mode | Competition Unit | Selection Source | Admission Policy | DS Responsibility | Eventun Responsibility |
| --- | --- | --- | --- | --- | --- |
| Player qualified final | `player` | `player_standings` | normal per-player admission | allow only listed players | compute standings and resolve entrant snapshot |
| Player invited final | `player` | `explicit_invite` | normal per-player admission | allow only listed players | store explicit player invite list and resolve entrant snapshot |
| Team qualified final | `team` | `team_standings` | `players_per_team`, ordered members, overflow policy | admit eligible team members, enforce cap, optionally replace lowest pre-start | compute team standings from aggregation rule and resolve team entrants plus ordered members |
| Team invited final | `team` | `explicit_invite` | `players_per_team` or free team-member join | admit only members of invited teams and enforce cap if configured | store invited teams and resolve entrant snapshot |
| Bracket round | `player` or `team` | `progression` | usually explicit per-round entrants | admit only routed entrants for that round | advance winners and losers, then resolve next-round entrants |

## Assessment Of The Current Eventun Direction

## What is aligned with the long-term model

These choices are good and should remain:

- `gauntlet_stage_run`
- stage-run-scoped DS claim/admission
- explicit stage player invite table
- creator/admin controls for defer and launch-now
- public AccelByte session with dedicated-server enforcement

These are compatible with the future generalized model.

## What should not become the long-term backbone

These parts should be treated as temporary, secondary, or authoring-level conveniences:

- `gauntlet_player_status.group_id` as the main invite mechanism
- `required_stage_wins` and `required_stage_losses` as the primary bracket routing mechanism
- putting more and more mode-specific meaning into `entry_requirement`

Why:

- `group_id` is gauntlet-wide, not stage-scoped
- win/loss filters are useful summary state but poor authoritative routing state
- `entry_requirement` becomes overloaded once team qualification, team invites, and bracket progression are introduced

## Recommended Treatment Of Groups

Groups can still be useful, but they should not become the long-term runtime authority.

A reasonable role for groups is:

- creator/admin authoring convenience
- a bulk-selection cohort for stage invites or seeding
- a way to organize participants before a stage-run snapshot is resolved

That means groups can still help drive a final, but the DS should not depend on live group membership plus live standings as the final authority for admission. Eventun should resolve groups into an explicit run snapshot first.

## Recommended Treatment Of `gauntlet_player_status`

`gauntlet_player_status` should not be the future home of explicit stage invite state.

A better role for it is:

- derived progression summary for a player in a gauntlet
- optional current group bucket if groups remain useful
- current bracket record summary such as wins and losses

If team progression becomes important, the parallel concept should probably be:

- `gauntlet_team_status`

Even then, bracket routing should still come from explicit entrant materialization.

## Short-Term Tactical Direction

Keep these:

- `gauntlet_stage_invite_player`
- `gauntlet_stage_invite_team`
- `allowed_teams`
- current `GauntletStage` timing and lobby fields
- `gauntlet_stage_run`
- DS claim/admission by `StageRunId`

Add next:

- clearer DS admission response support for team stages
- explicit team standings query or materialized read model

This is enough to support player invited finals now and move toward team invited and team qualified finals without a redesign.

Current support distinction:

- Team invitational v1 is close to supported: `gauntlet_stage_team`/`allowed_teams` can list invited teams, Eventun admission can validate that a joining player belongs to one of those teams, and the DS can enforce `players_per_team`.
- Team-restricted player qualification is partially supported: a player can be required to qualify individually and also belong to an allowed team.
- True team-qualified finals are not implemented: Eventun does not yet compute team standings, select teams by team score, or materialize ordered eligible members for a qualified team.

The current model is acceptable for simple team invitationals where any member of an invited team may try to join subject to DS capacity. Team-qualified finals should wait for explicit team standings and runtime entrant snapshots.

## Medium-Term Structural Direction

Add explicit stage-level semantics:

- `participant_type`: `player` or `team`
- `selection_mode`: `open`, `explicit_invite`, `player_standings`, `team_standings`, `progression`
- `team_score_top_n`: nullable, for team qualification
- `admission_priority_rule`: `first_come`, `qualification_points`, `selection_rank`, `team_member_rank`, or `bracket_seed`
- `overflow_policy`: nullable
- `roster_lock_point`: currently `match_start`
- `seed_source`: nullable

Then add runtime snapshot tables:

- `gauntlet_stage_run_entry`
  - one row per qualifying player or team for that run
- `gauntlet_stage_run_player`
  - optional per-player roster data when entrant type is team

This is the structural simplification. It lets all finals modes share:

- one DS contract
- one admission model
- one stage-run lifecycle

## Team Finals Design Notes

## Team qualified finals

Recommended shape:

- team qualification is computed from a configured aggregation rule such as `sum_top_n_player_scores`
- the team standings result determines which teams qualify
- Eventun returns qualified teams plus ordered candidate players within each team
- DS enforces `players_per_team`

Additional note:

- if team modes become common, Eventun may eventually need both player-count thresholds and team-count thresholds
- `min_competitors` and `min_lobby_size` are currently player-shaped concepts
- future team stages may also need `min_teams`

That does not need to be added immediately, but it should remain visible in the design.

## Team invited finals

Recommended shape:

- invite teams explicitly
- allow team members to join if they belong to an invited team
- optionally enforce a team admission cap and member priority ordering

This is structurally the same as team qualified finals. Only the selection source changes. That is exactly why the unified model is valuable.

## Bracket Design Notes

## What bracket configuration actually needs

The minimum useful bracket input is close to what was described:

- participant type: `player` or `team`
- elimination type: `single_elimination` or `double_elimination`
- initial field size
- seed source

From that, the system can derive:

- number of rounds or stages
- winner and loser paths
- how many entrants belong in each round

Manual stage times can still be operator-controlled after the bracket skeleton is created. That is a good separation.

## How later bracket rounds should work

The cleanest model is:

- opening round entrants come from standings or explicit invites
- later rounds use `progression`
- Eventun resolves explicit entrants for each later round from accepted earlier-round results

This is better than telling the DS to allow anyone with a particular global win/loss record.

That filtering approach becomes awkward quickly for:

- teams
- retries
- no-shows
- admin overrides
- bracket repairs or reseeding

Use wins and losses as summary. Use explicit round entrants as the real routing state.

## Brackets and team support

If team brackets are added later, explicit entrants become even more important.

Why:

- a team bracket round is really a team-versus-team assignment problem
- once the winning and losing teams are known, the next round should resolve those teams explicitly
- inside the session, the DS can still enforce which members of those teams may actually race

That is much simpler than trying to make team brackets emerge from global team status filters at lobby-join time.

## Suggested Implementation Order

1. Keep the new explicit player invite path for invite-only player finals.
2. Add explicit team invite support.
3. Add team standings logic with configurable `team_score_top_n`.
4. Extend DS eligibility snapshots to support team entrants and ordered team-member admission.
5. Introduce runtime entrant snapshot tables before implementing brackets.
6. Only then add bracket skeleton generation and bracket progression materialization.

This order keeps each new mode building on the same abstractions.

## Open Questions

These should be answered before team finals or brackets ship:

- Should `players_per_team` remain the canonical team admission cap, or should it be renamed later for clarity?
- Should pre-start overflow default to `reject_new` or `replace_lowest_prestart`?
- How should ties be broken in team standings when the top N player totals are equal?
- Do team finals need `min_teams` in addition to player-count thresholds?
- Should brackets allow manual reassignment of entrants after a failed run?
- When a bracket run fails after race start but before accepted completion, should the round replay with the same explicit entrants? The recommended answer is yes.

## Overall Recommendation

Do not keep expanding the current stage rule model sideways.

Use this rule instead:

- stage config decides what kind of competition a stage is
- Eventun resolves that into explicit entrants for the run
- the dedicated server only enforces the resolved run snapshot

That gives one durable stage-run lifecycle, one DS contract, one admin intervention model, and one place to support player finals, team finals, and brackets.

## References

- Formula 1 Constructors' Championship overview: https://www.formula1.com/en/latest/article/the-beginners-guide-to-the-f1-constructors-championship.66nTfWSqrUYv3bnbosPkHV
- Formula E rules and team championship overview: https://www.fiaformulae.com/en/championship/rules-and-regulations
- FIA WEC regulations hub: https://www.fia.com/Regulations/WEC
- Race Of Champions overview: https://www.raceofchampions.com/
- Race Of Champions Nations Cup field example: https://www.raceofchampions.com/post/final-20-driver-field-confirmed-for-roc-sydney-2025
- ALGS Championship competition overview: https://algs.ea.com/en/year-4/champs-2025/competition-overview
- VALORANT Champions Paris format overview: https://playvalorant.com/en-us/news/esports/everything-you-need-to-know-champions-paris/
