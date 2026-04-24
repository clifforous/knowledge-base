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

This note is the practical runtime contract for gauntlet stage attempts.

It is intended to guide:

- Eventun implementation work
- dedicated server implementation work
- game-client implementation work
- admin web tooling

## Current Backend Assumptions

Current Eventun behavior assumes:

- a gauntlet stage creates at most one active shard in the current phase
- the shard key is currently `primary`
- Eventun persists a durable `gauntlet_stage_attempt` row
- `stage_attempt_id` is Eventun's durable attempt id
- `session_id` is the AccelByte game session id and server-event session id
- Eventun writes `StageAttemptId`, `AttemptNumber`, and `StageAttemptShardKey` into AccelByte session attributes
- the AccelByte session remains public for now
- the game client preflight result is advisory only
- the dedicated server is the final admission, seat replacement, and kick authority
- participation is consumed only when Eventun accepts final placement rows
- automatic retry and bracket advancement are not implemented yet
- team hierarchy/designated racer priority metadata is not implemented yet

## Identity

A gauntlet stage runtime attempt is identified by:

- `GauntletId`
- `GauntletStage`
- `StageAttemptId`
- `AttemptNumber`
- `StageAttemptShardKey`

The dedicated server should treat `StageAttemptId` as `stage_attempt_id`.

`session_id` always means the AccelByte session id reported by AccelByte and used by Eventun event tables.

Do not invent a second meaning for `session_id`.

## AccelByte Session Attributes

The dedicated server should expect these stage-related attributes in the AccelByte session:

- `Gauntlet`
- `GauntletId`
- `GauntletStage`
- `StageAttemptId`
- `AttemptNumber`
- `StageAttemptShardKey`
- `MatchStartTimeSeconds`
- `EntryRequirement`
- `PlayersPerTeam`
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

The dedicated server should not infer gauntlet stage identity from session name or browsing behavior.

## Eventun APIs

### Dedicated server / privileged APIs

The dedicated server uses AdminService with its trusted token:

- `ClaimGauntletStageAttempt(stage_attempt_id, session_id)`
- `CheckGauntletStageAttemptAdmission(stage_attempt_id, session_id, player_id)`
- `FinalizeGauntletStageAttempt(stage_attempt_id, session_id, match_id)`

Legacy `ReportGauntletStageResults` still exists, but the current dedicated-server target should be `FinalizeGauntletStageAttempt`.

### Client API

The game client uses:

- `GetGauntletStageJoinStatus(gauntlet_id, stage)`

This endpoint uses the logged-in player. It returns advisory joinability, reason, active `stage_attempt_id`, AccelByte `session_id`, match-start state, attempt status, stage rules, and player admission summary when applicable.

### Event ingest

The dedicated server should continue using the existing trusted telemetry path:

- `ServerService.Event`

Finalization derives standings from `match_summary(session_id, match_id)`, so the trusted server event stream must contain the expected `MatchStart` and `PlayerMatchEnd` data before finalization.

## Admission Model

The game client can guide players toward likely-valid sessions.

The dedicated server makes the final runtime decision.

The AccelByte session is public in the current model:

- public discovery is not permission
- every incoming join should be treated as untrusted
- the DS should reject or remove invalid players as early as the runtime allows

Eventun sparse admission rows are audit/cache records. They are not a participant roster and do not count as participation.

## Join Mode Behavior

### Pure unrestricted open

If the stage is open and has no team, group, stage-win, or stage-loss restriction:

- the DS can skip Eventun admission checks
- the DS admits players first come until full
- the DS still owns capacity and start readiness

### Qualification modes

For qualifier/qualification stages:

- call `CheckGauntletStageAttemptAdmission`
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

## Dedicated Server Implementation Checklist

- On session start, read AccelByte session attributes and verify `Gauntlet=true`.
- Require `StageAttemptId` and the AccelByte `session_id`.
- Call `ClaimGauntletStageAttempt(stage_attempt_id, session_id)`.
- Cache the claim response for the life of the attempt.
- Reject the stage if Eventun says the attempt/session binding is invalid.
- For each player join request, decide whether the stage is pure open or restricted.
- For pure open, admit first come until capacity is full.
- For restricted modes, call `CheckGauntletStageAttemptAdmission(stage_attempt_id, session_id, player_id)`.
- Reject denied players using the returned reason.
- For allowed restricted players, apply DS capacity and replacement rules.
- When replacing, use Eventun `priority_score` and returned team context as policy input.
- Do not count claim, join, or admission as participation.
- Do not include players rejected or kicked before a normally completed match in final standings.
- Do include every human participant in a normally completed match, including disconnected/DNF players.
- Post trusted server events through `ServerService.Event`.
- Call `FinalizeGauntletStageAttempt(stage_attempt_id, session_id, match_id)` after the match completes normally and required events have been posted.
- Retry finalization with the same inputs after transient failures; the call is intended to be idempotent.

## Game Client Implementation Checklist

- Fetch gauntlet calendar data for the target upcoming window.
- Detect stages near now using the configured join window.
- Call `GetGauntletStageJoinStatus(gauntlet_id, stage)` before AccelByte join.
- Treat returned `session_id` as the AccelByte session id.
- Treat returned `stage_attempt_id` as Eventun's attempt id for display/debugging only; the DS still owns admission.
- Treat `joinable=true` as advisory, not as a seat reservation.
- Hide or disable normal join affordances for non-joinable reasons.
- Still handle DS rejection or kick after AccelByte join.
- Present DS rejection/kick as a gauntlet rules outcome rather than a generic network failure.
- Refresh Eventun-backed gauntlet state after rejection, kick, match completion, or stage finalization.
- Treat Eventun-accepted standings as authoritative over provisional local race UI.

## Client Preflight Reasons

Known advisory reason strings:

- `no_active_attempt`
- `session_not_created`
- `match_started`
- `stage_completed`
- `already_completed_stage`
- `not_qualified`
- `not_invited`
- `wrong_session`
- `inactive_attempt`
- `player_not_found`
- `joinable`

## Start Rules

The dedicated server should not start the stage unless the lobby is valid under gauntlet rules.

For gauntlet stages:

- bot backfill should be disabled for now
- at least one human player must exist or the server should shut down
- `MinCompetitors` should be treated as a qualified human threshold
- `MinLobbySize` should be treated as a qualified human lobby threshold before a valid start

If the stage cannot validly start, do not publish final standings. A dedicated abort API is still pending.

## Participation Semantics

A player should only be considered to have competed in a stage if Eventun accepts finalization and writes `gauntlet_stage_placement`.

This means:

- joining the lobby does not count as competing
- being admitted by Eventun does not count as competing
- leaving before race start does not count as competing
- an aborted, deferred, or failed attempt does not count as competing
- a server crash does not count as competing if the attempt is not accepted as completed
- disconnecting mid-race still counts as competing if the attempt completes successfully and the DS emits the participant's final event

## Admin Web Expectations

The admin surface should eventually support:

- viewing stage attempts per gauntlet stage
- viewing current status and failure reason
- viewing region, `stage_attempt_id`, and AccelByte `session_id`
- manual retry / hold / defer / cancel controls
- attempt history

## Current Failure Semantics

Current Eventun sweep behavior enforces these fallback failures:

- `allocating` or `session_created` past `deadline_claim` -> `failed(no_server_claim)`
- `claimed` or `started` past `deadline_finish` -> `failed(no_final_report)`

Dedicated-server-driven abort/failure reporting should refine these generic timeout reasons later.

## Operational Notes

- Region is hard input. The dedicated server should not assume a cross-region fallback is acceptable.
- The current model is designed to remain safe with multiple Eventun instances because ownership is DB-backed.
- Manual retry is the current intended retry policy.
- Automatic retry is deferred.

## Outstanding Gaps

- explicit DS abort/failure status API
- explicit `claimed -> started` status API
- team hierarchy/designated racer priority metadata
- bracket advancement
- admin controls for retry / hold / defer / cancel
- better cleanup for failed attempts with live AccelByte sessions
