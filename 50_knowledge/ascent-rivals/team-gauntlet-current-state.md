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

Product/team sources were reviewed through 2026-07-10. The migration audit refreshed committed implementation state through accepted F13 work on 2026-07-14, the unstaged F14 Eventun implementation was incorporated on 2026-07-15, and the current correction rechecked both repositories on 2026-07-15:

- `github.com/ikigai-github/eventun` on `teams` at committed base `5aaaea2`, with the current correction in the review worktree
- `github.com/ikigai-github/ascentun` on `dev` at `a0a40ad`; the locally recorded `main`, `origin/main`, and `origin/dev` refs identify the same commit
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

The active create/edit forms intentionally filter out `token_gated`, but the checked-in Ascentun contract is not fully synchronized with Eventun: `api.json`, team types/constants, and two unused gate-token actions still expose the retired mode and endpoints. Treat those as stale disabled artifacts to delete during the next coordinated contract refresh, not as supported behavior or a reason to restore the Eventun gate.

The current active route/component graph calls the legacy create, update, membership, invitation, ownership-transfer, roster rank/designation, and disband writes. No tracked workflow or deployment metadata, authenticated deployment history, or runtime access evidence was available in the review, so checked-in reachability is fact while deployment and production use remain unproven. On 2026-07-15 the owner explicitly selected temporary-risk option 2: leave those writes unchanged until the team-authority work, with no feature flag, compatibility layer, temporary safety patch, or numeric-designation extension. A future authority integration may replace this workflow through a breaking Ascentun change.

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

When Eventun admission is called, runtime and non-qualification restrictions remain live-evaluated, while pure individual qualification now uses a run-bound immutable cutoff:

- unrestricted open stages allow any human player after run/session/phase checks.
- invite stages allow an explicitly invited player, a member of an allowed team, or a member of an allowed group.
- a first qualification stage-run claim locks the gauntlet before the run row, requires the latest sealed individual cutoff to match the live configuration hash/revision/schema/projector tuple, and binds its exact snapshot id plus a complete rules snapshot; a same-session retry returns the stored binding without rechecking the later live projection, and admission replaces both rank fields plus every snapshot-carried points/count field while configured-match validation/completion count consume the frozen circuit and allowed-team, allowed-group, and stage win/loss filters remain live.
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
- accepted batches now derive one current narrow match/heat/player/progression fact graph and idempotent serving projections transactionally; detailed lap/checkpoint rows remain only in raw partitions
- leaving a team deletes `team_player`, so membership at historical event time cannot be reconstructed
- F13 now consumes normalized progression facts through idempotent contributions and bounded, lease-backed workers
- F14 now maintains ordinary player record/career and gauntlet contribution/projection tables synchronously, with accepted-batch serialization followed by ordered player and gauntlet locks plus a gap-free semantic revision shared by accepted changes, configuration changes, repairs, and rebuilds; the fingerprint includes the top-level projection configuration and every exact contribution/evidence identity, while only proven identical no-ops preserve the revision; batch/player and qualifier-leading child indexes bound fact-repair and qualifier-deletion cascades
- all eight leaderboard and four gauntlet native materialized views, their refresh procedure, and the hourly pg_cron schedule are retired from the canonical schema and product reads
- individual circuit-points qualification cutoff preview/publish/replace creates immutable versioned entry, qualifier, and selected-match evidence at an exact projection revision/schema/projector tuple; first stage-run claim binds only a snapshot current with the locked live tuple, same-session retry returns that stored binding, and runtime uses the frozen cutoff/circuit; allocation and update share gauntlet-before-stage lock order, update preserves all stage parents with run/history rows and edits open/invite stages in place, and a full-replacement omission of a run-backed stage fails before mutation, while the stricter cutoff-configuration freeze applies only to qualification-bound stages
- F15 has not started: legacy `server_event` and `client_event` relations, remaining legacy reads, and the `internal/` package tree remain; no production backfill or destructive event cutover is complete
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

### Development seed data

`eventun` retains an optional `Team Battles` development fixture with `gauntlet_stage_team` rows. The fixture now matches the current schema and is not part of automatic or production initialization.

Current implication: the fixture is runnable development data, but it remains evidence of a simple allowed-team stub rather than implemented team qualification, scoring, slots, or brackets.

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

1. Use the implemented compact complete-match facts and F14 individual gauntlet contributions as inputs; add membership validity intervals and stage-run-scoped result identity.
2. Add membership-attributed team qualification contributions and configurable top-N team standings without collapsing history through current membership.
3. Resolve allocation rules into concrete player-owned and team-owned racer slots.
4. Add indexed admission plus dedicated-server provisional occupancy, replacement, and roster lock.
5. Add owner-level result rules before enabling more than one racer per team.
6. Add explicit bracket matches, positions, stage-run shards, advancement, and repair.
