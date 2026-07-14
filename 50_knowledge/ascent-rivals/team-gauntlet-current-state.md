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
- [[../../30_designs/ascent-rivals/teams-solution-design|teams-solution-design]]
- [[../../30_designs/ascent-rivals/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[../../30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]
- [[../../10_research/ascent-rivals/eventun-team-postgresql-derivation-review|eventun-team-postgresql-derivation-review]]
- [[../../10_research/ascent-rivals/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]]

## Review Snapshot

Product/team sources were reviewed through 2026-07-10. Eventun and Ascent Rivals foundation changes are incorporated through 2026-07-13:

- `github.com/ikigai-github/eventun` at `34b4286`
- `github.com/ikigai-github/ascentun` at `deca852`
- Ascent Rivals game-client/server source, focused on gauntlet stage admission, session joins, team presentation, minimap behavior, party integration, and inbox behavior

This note captures implementation facts for the next teams design iteration. It should not be read as final product design.

## Confirmed Current Behavior

### Team lifecycle

Eventun owns team identity and roster state:

- `team` stores name, tag, membership mode, and colors.
- `team_media` stores team media.
- `team_player` stores one team membership per player, a role-like `designation`, and optional manual `rank`.
- `team_join_request` and `team_invite_request` store pending player-side requests and manager-side invites.

The former `token_meta`, `team_gate_token`, TapTools integration, token registration/sync APIs, and `token_gated` membership mode were removed during the foundation reset. Existing gated teams transition to invite-only. Token gating is unsupported until a provider-neutral asset-source contract is designed.

Ascentun exposes the current team lifecycle:

- team list and team profile
- team creation
- open join
- request-to-join
- invite-only acceptance through the team page flow
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

The generated Eventun client specification already exposes team list/detail/create/update, membership, pending-request, designation, and rank operations. `HGTeamMenu` and `HGNoTeamMenu` routes exist, but their reviewed C++ implementations are stubs, and no Eventun-backed Ascent Rivals team subsystem was found. Blueprint presentation still requires visual verification. The current Eventun team list API returns the full team list with full rosters. That contract is acceptable for the expected five-to-six-member teams in this iteration; a gamepad-first browser should precede optional text search, and payload size should be measured before later pagination work.

The game client currently has two different team paths:

- menu-side `UHGClientLocalPlayerSubsystem` racing-team helpers query AccelByte Groups using configuration code `racing-team` and expose legacy `Member`/`Captain` roles
- dedicated-server registration queries Eventun `Player`, builds session team metadata, and replicates Eventun team indexes to the race client

Current implication: most game-client team features need an Eventun-backed client team subsystem. The current solution design replaces the legacy AccelByte Groups path rather than synchronizing it. Session team identity is already sufficient for in-race presentation, but it is not a reusable menu-side team roster or membership cache.

Existing social infrastructure can be reused, but it does not complete the proposed features by itself:

- `UHGChatSubsystem` queries AccelByte Chat persistent and transient system messages, marks persistent messages read, and supplies unread and popup state through `UHGSocialSubsystem`; team notifications still need an Eventun producer/outbox, routing policy, and a prototype proving typed action payloads survive the installed SDK
- party and social code can invite selected players; a team-roster action may resolve the linked AccelByte id and call that existing path, but the current teams design does not change party behavior or friend synchronization

Current implication: green teammate minimap markers are lower effort than the initial estimate, while team notifications, team activity feeds, stream links, team XP, and team-filtered leaderboards all cross backend/data-contract boundaries and should not be estimated as presentation-only work.

### Game-client gauntlet and challenge support

The Ascent Rivals client already has functional player-oriented Eventun integration:

- `UHGGauntletSubsystem` caches gauntlets, calendar entries, standings, sponsors, and player gauntlet state.
- The join path locates an active public AccelByte session, calls `GetGauntletStageJoinStatus`, verifies the exact stage run/session candidate, and joins through the existing session subsystem.
- `UHGChallengesSubsystem` calls Eventun `MyActiveChallenges` and carries active assignments, progress, lanes, and reward previews into existing challenge UI models.

Current implication: general player-shaped gauntlet browsing and stage entry do not need to be rebuilt before team work. Team modes instead need extensions for team standings, resolved player-owned and team-owned racer slots, roster status, mixed allocation sources, and team-specific admission reasons. Team challenges can reuse client presentation patterns, but the current Eventun progression model is player-scoped.

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
- stage-run creation currently persists run/session lifecycle state but does not resolve or persist entrant, team, representative, or slot-pool rows
- the AccelByte `session_id` is distinct from Eventun `stage_run_id`.
- `gauntlet_stage_run_admission` records sparse evaluated join decisions.
- `gauntlet_stage_run_match` records accepted configured matches.
- `gauntlet_stage_run_match_result` records per-player accepted match results.
- `gauntlet_stage_placement` stores final aggregate player placements and is the participation signal.

Multi-match stages are supported. Eventun accepts each configured `match_id`, then completes the run after all required matches are accepted. Final aggregate placement is ordered by summed circuit points, best placement, placement sum, then player id.

Current implication: team stage winners are not computed as teams. Final accepted stage placements are still per-player rows. A future team gauntlet needs an explicit rule for deriving team results from player results before progression or prize/accounting flows treat a team as the stage participant.

### Database correctness and derivation

The current PostgreSQL model has additional constraints relevant to both team progression and gauntlets:

- the foundation implementation adds stable match-batch ids, event ids, producer sequence, source classification, artifact association, and idempotent acceptance while preserving source/event-type partitions
- accepted batches now derive one current narrow match/heat/player/progression fact graph transactionally; detailed lap/checkpoint rows remain only in raw partitions, and current product reads have not yet moved to these facts
- leaving a team deletes `team_player`, so membership at historical event time cannot be reconstructed
- gauntlet leaderboard and qualifier materialized views still refresh hourly, are stale between refreshes, and are not a stable final-selection snapshot; the approved direction is incremental per-match qualification contributions and retained best-sequence projections followed by an immutable cutoff snapshot
- stage admission invokes broad `gauntlet_stats` calculation and filters to one player rather than reading a resolved slot
- `gauntlet_stage_placement` includes `stage_run_id` but its primary key is still gauntlet, stage, and player
- progression jobs now use token-fenced two-minute leases, bounded exponential backoff, five-attempt dead-lettering, and one-at-a-time claiming; all fact application, challenge rebuilding, goal evaluation, completion, and reward-record creation serialize on the player row

These are documented with source references and database recommendations in [[../../10_research/ascent-rivals/eventun-team-postgresql-derivation-review|eventun-team-postgresql-derivation-review]].

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
- concrete stage-run racer slots with player or team owners
- mixed individual and team allocation rules
- automatic resolution of qualification, explicit, community, sponsor, or fallback slot sources
- ordered eligible member snapshots for team stages
- Eventun enforcement of `players_per_team`
- dedicated-server enforcement of `players_per_team`
- Eventun or dedicated-server enforcement of `team_player.rank`
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

3. Keep qualification sources cohesive through concrete slots.

   Qualification or explicit assignment should choose a player or team slot owner, then expand each owner into a configured number of racer slots. “Wildcard” remains a label or policy rather than a separate entrant type.

4. Enforce `players_per_team` through resolved slots and dedicated-server occupancy.

   Eventun should resolve the number of owned slots and answer indexed eligibility/priority reads. The dedicated server should serialize live provisional occupancy, replace lower-priority members where configured, and submit the actual roster to Eventun at lock.

5. Decide how team results are represented.

   Current accepted placements are per-player. Team gauntlets need a durable team result or a documented derivation from per-player rows before standings, progression, prizes, and accounting can safely use team outcomes.

6. Add stage-run-scoped slots and results before serious brackets.

   Materialize player-owned and team-owned racer slots per run, persist the locked occupants, and change accepted result uniqueness to include `stage_run_id` before adding an explicit bracket graph.

## Recommended Near-Term Order

1. Use the implemented compact complete-match facts as inputs; add membership validity intervals and stage-run-scoped result identity.
2. Add incremental qualification contributions, retained best-sequence projections, and configurable top-N team standings.
3. Resolve allocation rules into concrete player-owned and team-owned racer slots.
4. Add indexed admission plus dedicated-server provisional occupancy, replacement, and roster lock.
5. Add owner-level result rules before enabling more than one racer per team.
6. Add explicit bracket matches, positions, stage-run shards, advancement, and repair.
