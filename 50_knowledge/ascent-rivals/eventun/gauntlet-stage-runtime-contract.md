# Ascent Rivals - Eventun Gauntlet Stage Runtime Contract

## Related
- [[../overview]]
- [[overview]]
- [[api]]
- [[data-model]]
- [[events]]
- [[../game-client]]
- [[../../30_designs/ascent-rivals/gauntlet-stage-orchestration-improvements|gauntlet-stage-orchestration-design]]

## Purpose

This is the authoritative runtime contract for gauntlet stage runs.

It is intended to guide:

- Eventun implementation work
- dedicated server implementation work
- game-client implementation work
- admin web tooling

## Implementation Status

Current Eventun behavior:

- a gauntlet stage creates at most one active shard in the current phase
- the shard key is currently `primary`
- a gauntlet stage can define one or more configured matches/circuits
- Eventun persists a durable `gauntlet_stage_run` row
- `stage_run_id` is Eventun's durable run id
- `session_id` is the AccelByte game session id and server-event session id
- `match_id` is the match index within that AccelByte/session-event context and can be `0`
- Eventun writes `StageRunId`, `RunNumber`, and `StageRunShardKey` into AccelByte session attributes
- the AccelByte session remains public for now
- the game client preflight result is advisory only
- the dedicated server is the final admission, seat replacement, and kick authority
- participation is consumed only when Eventun completes the run and writes final stage placement rows
- multi-match stages are supported through per-match acceptance and aggregate run completion
- automatic retry and bracket advancement are not implemented yet
- team hierarchy/designated racer priority metadata is not implemented yet

## Identity

A gauntlet stage runtime run is identified by:

- `GauntletId`
- `GauntletStage`
- `StageRunId`
- `RunNumber`
- `StageRunShardKey`

The dedicated server should treat `StageRunId` as `stage_run_id`.

`session_id` always means the AccelByte session id reported by AccelByte and used by Eventun event tables.

Do not invent a second meaning for `session_id`.

## AccelByte Session Attributes

The dedicated server should expect these stage-related attributes in the AccelByte session:

- `Gauntlet`
- `GauntletId`
- `GauntletStage`
- `StageRunId`
- `RunNumber`
- `StageRunShardKey`
- `MatchStartTimeSeconds`
- `EntryRequirement`
- `PlayersPerTeam`
- `OverflowPolicy`
- `AdmissionPriorityRule`
- `RosterLockPoint`
- `IsBracket`
- `HasGroups`
- `GroupId`
- `RequiredStageWins`
- `RequiredStageLosses`
- `RaceMode`
- `MinCompetitors`
- `MaxCompetitors`
- `MinLobbySize`
- `MaxLobbySize`
- `Circuit`
- `AllowedTeams`
- `GAME_SESSION_REQUEST_TYPE=GAUNTLET_STAGE`

Each `Circuit` entry includes its configured `match_id`, course, laps, and heats. The dedicated server should use that as the stage run's required match plan.

The dedicated server should not infer gauntlet stage identity from session name or browsing behavior.

## Eventun APIs

### Dedicated server / privileged APIs

The dedicated server uses AdminService with its trusted token:

- `ClaimGauntletStageRun(stage_run_id, session_id)`
- `CheckGauntletStageRunAdmission(stage_run_id, session_id, player_id)`
- `AcceptGauntletStageRunMatch(stage_run_id, session_id, match_id)`
- `CompleteGauntletStageRun(stage_run_id, session_id)`

The claim response includes `allow_any_human_player` and `requires_restricted_admission`. These fields describe whether the stage needs restricted eligibility policy, not whether the DS should call admission. The DS should still call admission for every human competitor join/rejoin.

`AcceptGauntletStageRunMatch` accepts one completed match summary for the run. It verifies:

- the run exists and is active
- the run is bound to the provided `session_id`
- the `match_id` is configured in `gauntlet_stage_circuit`
- trusted server `MatchStart` exists for `session_id + match_id + gauntlet_id + stage`
- `match_summary(session_id, match_id)` has standings

`CompleteGauntletStageRun` completes the run only after all configured matches have been accepted. It writes aggregate final `gauntlet_stage_placement` rows and marks the run `completed`.

### Client API

The game client uses:

- `GetGauntletStageJoinStatus(gauntlet_id, stage)`

This endpoint uses the logged-in player. It returns advisory joinability, reason, active `stage_run_id`, AccelByte `session_id`, match-start state, run status, run phase, accepted/required match counts, optional current match id, stage rules, and player admission summary when applicable.

### Event ingest

The dedicated server should continue using the existing trusted telemetry path:

- `ServerService.Event`

Match acceptance derives standings from `match_summary(session_id, match_id)`, so the trusted server event stream must contain the expected `MatchStart` and `PlayerMatchEnd` data before each match is accepted.

For multi-match stages, each match has its own `session_id + match_id` event and replay identity. Eventun stores accepted stage-run match rows separately from final aggregate placement rows.

## Data Model

Primary runtime tables:

- `gauntlet_stage_run`: durable owner row for one stage shard run
- `gauntlet_stage_run_admission`: sparse on-demand admission evaluation/audit records
- `gauntlet_stage_run_match`: accepted-match ledger for a run
- `gauntlet_stage_run_match_result`: per-player results for accepted matches
- `gauntlet_stage_placement`: final aggregate stage placements and participation signal

Important naming:

- `run_number` is the per-stage/shard sequence
- `stage_run_id` links accepted match rows and final placements to the run
- configured match plans live in `gauntlet_stage_circuit`; `gauntlet_stage_run_match` only records matches Eventun accepted for this run
- final aggregate stage placement rows use `match_id = NULL`

Final stage standings are ordered by:

1. summed `circuit_points` descending
2. best single-match placement ascending
3. summed placement ascending
4. `player_id` ascending

This follows a circuit/cup-style scoring model while keeping combat-derived circuit points as the primary competition score.

## Admission Model

The game client can guide players toward likely-valid sessions.

The dedicated server makes the final runtime decision.

The AccelByte session is public in the current model:

- public discovery is not permission
- every incoming join should be treated as untrusted
- the DS should reject or remove invalid players as early as the runtime allows

Eventun sparse admission rows are audit/cache records. They are not a participant roster and do not count as participation.

The dedicated server should call `CheckGauntletStageRunAdmission` for every human competitor join or rejoin, including pure open stages. Open stages do not require a restricted eligibility lookup, but the admission call still validates run/session/phase, applies already-completed-stage rules, and records the admission evaluation.

Stage admission policy fields:

- `overflow_policy`: `reject_new` or `replace_lowest_prestart`
- `admission_priority_rule`: `first_come`, `qualification_points`, `selection_rank`, `team_member_rank`, or `bracket_seed`
- `roster_lock_point`: currently `match_start`

The DS owns capacity, replacement, and kick behavior. Eventun returns policy inputs and audit state.

## Join Mode Behavior

### Pure unrestricted open

If the stage is open and has no team, group, stage-win, or stage-loss restriction:

- the DS should still call `CheckGauntletStageRunAdmission`
- Eventun should return `allowed=true`, `reason=joinable` when the run/session/phase checks pass
- the DS admits players first come until full
- the DS still owns capacity and start readiness

### Qualification modes

For qualifier/qualification stages:

- call `CheckGauntletStageRunAdmission`
- Eventun returns allowed/denied and `priority_score=qualification_points`
- if the lobby is full, the DS may replace the lowest-priority current player with a higher-priority joiner
- Eventun does not decide who to kick

### Team-restricted qualifier modes

For team-scoped stages:

- Eventun validates player qualification and team membership/scope
- Eventun returns `team_id` and qualification context
- the DS applies the current team priority policy

### Invite-only

For invite-only stages:

- Eventun validates explicit player, team, or group invite
- after Eventun validation, the DS defaults to first come
- future team hierarchy/designated racer data may refine this, but it is not implemented now

## Dedicated Server Checklist

- On session start, read AccelByte session attributes and verify `Gauntlet=true`.
- Require `StageRunId` and the AccelByte `session_id`.
- Call `ClaimGauntletStageRun(stage_run_id, session_id)`.
- Cache the claim response for the life of the run.
- Reject the stage if Eventun says the run/session binding is invalid.
- Use claim response `stage_config.circuit[]` as the required match plan.
- For each human competitor join/rejoin request, call `CheckGauntletStageRunAdmission(stage_run_id, session_id, player_id)`.
- Reject denied players using the returned reason.
- For allowed players, apply DS capacity and replacement rules.
- Use stage `overflow_policy`, `admission_priority_rule`, `roster_lock_point`, Eventun `priority_score`, and returned team context as policy input.
- Do not count claim, join, or admission as participation.
- Do not include players rejected or kicked before a normally completed match in final standings.
- Do include every human participant in a normally completed match, including disconnected/DNF players.
- Post trusted server events through `ServerService.Event`.
- After each normally completed stage match, call `AcceptGauntletStageRunMatch(stage_run_id, session_id, match_id)` after required events have been posted.
- When the response reports `ready_to_complete=true`, call `CompleteGauntletStageRun(stage_run_id, session_id)`.
- Retry match acceptance and run completion with the same inputs after transient failures; both calls are intended to be idempotent for the same accepted facts.

## Game Client Checklist

- Fetch gauntlet calendar data for the target upcoming window.
- Detect stages near now using the configured join window.
- Call `GetGauntletStageJoinStatus(gauntlet_id, stage)` before joining through AccelByte.
- Treat returned `session_id` as the AccelByte session id.
- Treat returned `stage_run_id` as Eventun run context for display/debugging only; the DS still owns admission.
- Treat `joinable=true` as advisory, not as a seat reservation.
- Hide or disable normal join affordances for non-joinable reasons.
- Still handle DS rejection or kick after AccelByte join.
- Present DS rejection/kick as a gauntlet rules outcome rather than a generic network failure.
- Refresh Eventun-backed gauntlet state after rejection, kick, match completion, match acceptance, or run completion.
- Treat Eventun-accepted standings as authoritative over provisional local race UI.

## Client Preflight Reasons

Known advisory reason strings:

- `no_active_run`
- `session_not_created`
- `match_started`
- `stage_completed`
- `already_completed_stage`
- `not_qualified`
- `not_invited`
- `wrong_session`
- `inactive_run`
- `player_not_found`
- `run_ready_to_complete`
- `joinable`

Known `run_phase` values:

- `prestart`
- `match_in_progress`
- `between_matches`
- `ready_to_complete`
- `completed`

## Start Rules

The dedicated server should not start the stage unless the lobby is valid under gauntlet rules.

For gauntlet stages:

- bot backfill should be disabled for now
- at least one human player must exist or the server should shut down
- `MinCompetitors` should be treated as a qualified human threshold
- `MinLobbySize` should be treated as a qualified human lobby threshold before a valid start

If the stage cannot validly start, do not publish final standings. A dedicated abort API is still pending.

## Participation Semantics

A player should only be considered to have competed in a stage if Eventun completes the run and writes `gauntlet_stage_placement`.

This means:

- joining the lobby does not count as competing
- being admitted by Eventun does not count as competing
- leaving before race start does not count as competing
- an aborted, deferred, cancelled, or failed run does not count as competing
- a server crash does not count as competing if the run is not completed
- disconnecting mid-race still counts as competing if the run completes successfully and the DS emits the participant's final event

## Admin Tooling Expectations

Admin tooling should eventually support:

- viewing stage runs per gauntlet stage
- viewing current status/deadlines/failure reason/manual hold
- viewing region, `stage_run_id`, and AccelByte `session_id`
- viewing accepted match count versus required match count
- viewing accepted per-match result rows
- run history
- manual hold/release
- manual defer/cancel/fail/abort
- optional explicit relaunch after a failed run

## Still Pending

Known follow-up work:

- explicit abort API for insufficient players or runtime failure
- explicit `started` transition from trusted match start or DS callback
- dedicated admin operations for hold/release/defer/cancel/fail/abort
- better cleanup for failed runs with live AccelByte sessions
- reconnect/reserved-seat game-server lifecycle work
- richer admission modes for reconnect, replacement, spectator, and shoutcaster joins
- bracket advancement and progression materialization
- team hierarchy/designated-racer priority metadata
