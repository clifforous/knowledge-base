# Ascent Rivals - Team Gauntlet Current State

## Related
- [[overview]]
- [[competition-runtime-terms]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[eventun/data-model|eventun-data-model]]
- [[eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[website]]
- [[../../30_designs/ascent-rivals/gauntlet-finals-and-tournament-modes-design-review|gauntlet-finals-and-tournament-modes-design-review]]

## Review Snapshot

Sources reviewed on 2026-07-09:

- `github.com/ikigai-github/eventun` at `34b4286`
- `github.com/ikigai-github/ascentun` at `deca852`
- Ascent Rivals game-client/server source, focused on gauntlet stage admission, session joins, team presentation, minimap behavior, party integration, and inbox behavior

This note captures implementation facts for the next teams design iteration. It should not be read as final product design.

## Confirmed Current Behavior

### Team lifecycle

Eventun owns team identity and roster state:

- `team` stores name, tag, membership mode, and colors.
- `team_media` stores team media.
- `team_gate_token` stores token-gate policy ids.
- `team_player` stores one team membership per player, a role-like `designation`, and optional manual `rank`.
- `team_join_request` and `team_invite_request` store pending player-side requests and manager-side invites.

Ascentun exposes the current team lifecycle:

- team list and team profile
- team creation
- open join
- request-to-join
- invite-only acceptance through the team page flow
- token-gated join checks using linked/current wallet token policy ids
- team management for owners, managers, and admins
- roster role changes, manual rank edits, member removal, owner transfer, and disband
- pending invite and pending join-request management

Current implication: team `rank` exists and is editable, but it is only ordinary roster metadata today. It is not yet materialized into gauntlet-stage candidate lists or enforced by Eventun as a team-stage admission order.

### Game-client team and social surfaces

Current Ascent Rivals source already carries team identity into several session UI paths:

- player and session entities carry team indexes and session-level team metadata
- the reusable player-card path can render a team tag, primary color, and team icon when present
- race-roster rows use the team-aware player card
- ranking and match-summary rows carry the player's team index into the same presentation path

The proposed green teammate minimap marker is partially stubbed:

- the minimap already defines `FriendlyPlayerIconColor` as green
- `DecoratePlayerIcon` currently paints the spectated racer blue and every other racer red
- the current minimap path does not compare the local/spectated player's team index with the target player's team index, so the green color is unused

The generated Eventun client specification already exposes team list/detail/create/update, membership, pending-request, designation, and rank operations. No dedicated Ascent Rivals team subsystem or team browser/management route was found in the reviewed source. The current Eventun team list API returns the full team list, so an initial small-catalog search can be client-filtered, but scalable search would need a server-side query contract.

Existing social infrastructure can be reused, but it does not complete the proposed features by itself:

- the inbox supports AccelByte persistent and transient system messages, unread state, and popup delivery; team notifications still need an event producer, routing/category rules, and action payload handling
- party and social code can invite selected friends to the retained party; quick team-member invites still need team roster/presence data and a team-roster action path

Current implication: green teammate minimap markers are lower effort than the initial estimate, while team notifications, team activity feeds, stream links, team XP, and team-filtered leaderboards all cross backend/data-contract boundaries and should not be estimated as presentation-only work.

### Stage-level team restrictions

Eventun supports a simple team-restricted stage shape:

- stage entry requirements currently accept `open`, `invite`, `qualification`, and `qualifier`; Ascentun's visible form uses `qualifier` and `open`.
- `gauntlet_stage.players_per_team` stores the intended active racer cap per team.
- `gauntlet_stage_team` stores allowed/invited teams for a stage.
- client-facing APIs can list, add, and remove stage invited teams.
- `GauntletStage.allowed_teams` is included in the generated API shape.
- stage admission returns the player's current `team_id`, `team_name`, and `team_tag` when available.

When Eventun admission is called, eligibility is live-evaluated rather than snapshot-based:

- unrestricted open stages allow any human player after run/session/phase checks.
- invite stages allow an explicitly invited player, a member of an allowed team, or a member of an allowed group.
- qualification stages require the player to qualify individually and may also require allowed-team, allowed-group, or stage win/loss filters.
- allowed teams on non-invite stages act as an additional restriction.

Current Ascent Rivals dedicated-server code skips the Eventun admission call for pure unrestricted stages. Restricted team stages do call Eventun, but the unrestricted fast path currently bypasses Eventun's already-completed-stage check and admission audit row; see [[eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]].

Current implication: team invitational V1 is partially supported. If a stage lists allowed teams, Eventun can validate that a joining player belongs to one of those teams and can return team context to the dedicated server. The dedicated server owns actual session admission, overall capacity, replacement, and kick behavior, but per-team racer cap enforcement is not implemented in the reviewed paths.

Follow-up code review found that `players_per_team` is not currently enforced in the reviewed Eventun admission path or the reviewed Ascent Rivals game-server join path. The game code has a gauntlet-type comment describing intended top-N-per-team qualifier behavior, but the runtime currently appears to enforce run/session/phase checks, individual qualification/invite/team membership, and overall server capacity rather than per-team racer caps.

### Bracket-related stubs

Eventun has limited bracket-shaped data:

- `gauntlet_stage_bracket` stores required stage wins and losses for one stage.
- `GauntletStage.required_stage_wins` and `required_stage_losses` are exposed in the API.
- admission compares the player's current `gauntlet_stats.stage_wins` and `stage_losses` against those filters.
- `gauntlet_player_status` stores gauntlet-wide `group_id`, `stage_wins`, and `stage_losses`.

Current implication: this is not a bracket system. There is no bracket graph, no bracket seeding, no player or team round assignment table, no automatic progression materialization, and no team bracket status. The current fields are stage filters over gauntlet-wide player summary state.

### Stage runs and participation

Current gauntlet stage runtime support is player-result based:

- `gauntlet_stage_run` owns a durable run id.
- the AccelByte `session_id` is distinct from Eventun `stage_run_id`.
- `gauntlet_stage_run_admission` records sparse evaluated join decisions.
- `gauntlet_stage_run_match` records accepted configured matches.
- `gauntlet_stage_run_match_result` records per-player accepted match results.
- `gauntlet_stage_placement` stores final aggregate player placements and is the participation signal.

Multi-match stages are supported. Eventun accepts each configured `match_id`, then completes the run after all required matches are accepted. Final aggregate placement is ordered by summed circuit points, best placement, placement sum, then player id.

Current implication: team stage winners are not computed as teams. Final accepted stage placements are still per-player rows. A future team gauntlet needs an explicit rule for deriving team results from player results before progression or prize/accounting flows treat a team as the stage participant.

### Ascentun gauntlet authoring and display

Ascentun currently carries some team/bracket fields in types and schema:

- `playersPerTeam`
- `allowedTeams`
- `requiredStageWins`
- `requiredStageLosses`
- `groups`

But the visible gauntlet create/edit UI currently exposes only basic stage fields:

- stage type selector limited to `qualifier` and `open`
- match start time
- race mode
- max competitors
- circuit course/heats/laps
- advanced min/max player/lobby counts

The visible gauntlet detail page shows stage requirement, start time, race mode, max competitors, and circuit. It does not show allowed teams, `playersPerTeam`, groups, bracket filters, overflow policy, admission priority rule, roster lock point, or join status.

Current implication: Ascentun cannot currently author team gauntlet stages or bracket-filtered stages through the visible form. It can preserve some hidden/default fields in the submitted object, but that is not an operator workflow.

### Stale seed data

`eventun` has a temporary seed gauntlet named `Team Battles` with `gauntlet_stage_team` rows. That seed file also references old `gauntlet_stage` columns such as `threshold_metric` and `max_per_team` that do not match the current schema.

Current implication: treat the seed as evidence of an old team-battle stub, not as runnable current source of truth.

## Not Implemented Yet

The following are not implemented in the reviewed code:

- team standings for gauntlets
- configurable team score aggregation such as top N members
- `gauntlet_team_status`
- `participant_type` or `selection_mode` stage semantics
- `team_score_top_n`
- `min_teams`
- runtime entrant snapshot tables such as `gauntlet_stage_run_entry` or `gauntlet_stage_run_player`
- ordered eligible member snapshots for team stages
- Eventun enforcement of `players_per_team`
- dedicated-server enforcement of `players_per_team`
- Eventun or dedicated-server enforcement of `team_member_rank`
- Eventun computation of team stage placement or team winner
- automatic bracket advancement
- bracket seeding or bracket graph materialization
- team bracket progression
- Ascentun UI for stage invited teams, player stage invites, team-stage caps, bracket filters, overflow policy, admission priority, or roster lock

## Design Implications For The Next Iteration

1. Do not treat `gauntlet_stage_team` as full team gauntlet support.

   It is a team eligibility list. It does not compute team qualification, team scoring, or team progression.

2. Do not treat `gauntlet_stage_bracket` as a bracket system.

   It is a wins/losses admission filter over player summary state. Brackets still need explicit seeding, round assignment, progression, and repair/retry rules.

3. Decide whether the next iteration is team invitationals, team-qualified finals, or brackets.

   Team invitationals can build on current allowed-team admission. Team-qualified finals require team standings and a team-result model. Brackets should wait for explicit entrant snapshots or they will compound the current filter-based limitations.

4. Decide where `players_per_team` is enforced.

   Current code stores the field but does not enforce it in the reviewed admission or join paths. If Eventun makes advisory team-cap decisions, the admission API needs current lobby composition or a stage-run roster snapshot. If the dedicated server owns enforcement, it needs explicit per-team occupancy and replacement logic rather than only overall lobby capacity.

5. Decide how team results are represented.

   Current accepted placements are per-player. Team gauntlets need a durable team result or a documented derivation from per-player rows before standings, progression, prizes, and accounting can safely use team outcomes.

6. Add runtime entrant snapshots before serious brackets.

   The existing design review recommendation still matches the code gap: materialize resolved player/team entrants per run, then make the dedicated server enforce the resolved run snapshot.

## Recommended Near-Term Order

1. Expose explicit stage invited-team authoring in Ascentun if the next mode is team invitational.
2. Add visible stage detail fields for allowed teams, `players_per_team`, and admission policy so operators can verify what they authored.
3. Implement and verify per-team stage racer cap behavior before relying on fixed team slot counts.
4. Add team standings and a team score aggregation rule before team-qualified finals.
5. Add runtime entrant snapshots before bracket progression or team-qualified run enforcement.
6. Add team result rows or a clearly documented team-result derivation before prizes or progression depend on team outcomes.
