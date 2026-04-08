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

This note is the practical runtime contract for gauntlet stage sessions.

It is intended to help:

- Eventun implementation work
- dedicated server implementation work
- game-client implementation work
- admin web tooling

## Current Backend Assumptions

Current Eventun behavior assumes:

- a gauntlet stage creates at most one active shard in the current phase
- the shard key is currently `primary`
- Eventun persists a durable `gauntlet_stage_session` attempt row
- Eventun writes `StageSessionId`, `StageSessionAttempt`, and `StageSessionShardKey` into AccelByte session attributes
- the AccelByte session remains public for now
- the dedicated server is the final admission gate
- automatic retry is not implemented yet
- player assignment snapshots are not implemented yet

## Session Identity

A gauntlet stage runtime session is identified by:

- `GauntletId`
- `GauntletStage`
- `StageSessionId`
- `StageSessionAttempt`
- `StageSessionShardKey`

The dedicated server should treat `StageSessionId` as the durable attempt identity.

`session_id` is the AccelByte transport/session handle.

`StageSessionId` is the Eventun competition-attempt handle.

## Current Session Attributes

The dedicated server should expect these stage-related attributes in the AccelByte session:

- `Gauntlet`
- `GauntletId`
- `GauntletStage`
- `StageSessionId`
- `StageSessionAttempt`
- `StageSessionShardKey`
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

## Eligibility Fetch Model

The dedicated server should fetch and cache a stage-attempt eligibility snapshot from Eventun.

Recommended flow:

1. read `StageSessionId` from the AccelByte session attributes
2. call an Eventun endpoint such as `GetGauntletStageEligibility`
3. cache the returned eligibility snapshot locally for the life of that attempt
4. use the cached snapshot for all join decisions in that session

The dedicated server should not derive final eligibility from live gauntlet standings at join time.

Live standings can change or become ambiguous later. A stage-attempt eligibility snapshot is the cleaner source of truth.

### Expected eligibility response shape

The snapshot should include:

- `StageSessionId`
- `GauntletId`
- `GauntletStage`
- `StageSessionAttempt`
- `StageSessionShardKey`
- stage rules such as `EntryRequirement`, `AllowedTeams`, `PlayersPerTeam`, `MinCompetitors`, `MinLobbySize`, and `Circuit`
- the eligible player list for that attempt
- any team, group, or bracket metadata needed for admission

## Admission Model

### General Rule

The game client is allowed to guide players toward valid sessions.

The dedicated server is responsible for the final allow or reject decision.

### Public Session Constraint

The AccelByte session is public in the current model.

That means:

- any player may technically discover or attempt to join the session
- discovery is not permission
- the dedicated server must treat every incoming join as untrusted until validated

## Dedicated Server Allow Rules

For gauntlet stages, the dedicated server should allow a player to remain only if all applicable rules pass.

### Base rules

- The session must be a gauntlet stage session.
- The player must be a real human competitor.
- The player must be present in the cached eligibility snapshot for this attempt.
- The player must not already be participating in a conflicting stage shard.

### Team / bracket / group rules

When applicable, the dedicated server should enforce:

- `AllowedTeams`
- `EntryRequirement`
- `RequiredStageWins`
- `RequiredStageLosses`
- `GroupId`
- `PlayersPerTeam`

## Dedicated Server Kick / Removal Rules

If a player is not valid for the session, the dedicated server should reject them as early as possible.

Preferred behavior:

- deny before the player is treated as a valid competitor if the runtime stack allows it
- if the runtime has already admitted the player, remove or kick them immediately
- do not count rejected players toward readiness, start thresholds, or final standings

Players should be removed when:

- they are not qualified for the stage
- they are not in the cached eligibility snapshot
- they are not in the allowed team or bracket/group scope
- they are a bot in a human-only gauntlet stage
- they are duplicated or otherwise invalid for the current shard

The dedicated server should log or emit telemetry for unauthorized join attempts.

## Start Rules

The dedicated server should not start the stage unless the stage is valid under gauntlet rules.

### Human-player requirements

For gauntlet stages:

- bot backfill should be disabled for now
- at least one human player must exist or the server should shut down
- `MinCompetitors` should be treated as a qualified human threshold
- `MinLobbySize` should be treated as a qualified human lobby threshold before a valid start

### If start conditions are not met

If the stage cannot validly start by the configured start deadline:

- report `aborted(insufficient_players)` to Eventun once that API exists
- close the session cleanly
- do not publish final standings

## Participation Semantics

A player should only be considered to have competed in a stage if the stage attempt completes successfully after race start.

This means:

- joining the lobby does not count as competing
- leaving before race start does not count as competing
- an aborted, deferred, or failed attempt does not count as competing
- a server crash does not count as competing if the attempt is not accepted as completed
- disconnecting mid-race still counts as competing if the attempt completes successfully

The dedicated server should therefore avoid treating lobby presence alone as participation. Eventun should consume participation only when final completed results are accepted.

## Runtime Reporting Expected From the Dedicated Server

The dedicated server should continue using the existing trusted telemetry path:

- `Server.Event`

That covers:

- session lifecycle telemetry
- match lifecycle telemetry
- heat telemetry
- player telemetry

In addition, the dedicated server is expected to call new or updated Eventun gauntlet-stage APIs.

### Expected status API

Planned Eventun API:

- `ReportGauntletStageStatus`

Expected status transitions reported by the dedicated server:

- `claimed`
- `started`
- `heartbeat`
- `aborted` with reason
- `failed` with reason

Expected reasons include:

- `insufficient_players`
- `runtime_failure`
- `invalid_assignment`

### Expected final-results API

Planned Eventun API:

- `ReportGauntletStageResults`

Expectations:

- report final standings for the whole stage attempt
- include `StageSessionId` or another attempt identity input once the API is updated
- treat the call as idempotent
- retries must be safe

## Game Client Rules

The game client should follow these rules.

### Join UX

- show a gauntlet stage join action only when Eventun says the player is qualified
- do not use public AccelByte session visibility as join permission
- if the player is not qualified, do not expose the join affordance in normal UI

### Rejection handling

If the dedicated server rejects or removes the player:

- treat that as a competition-rules outcome
- show a clear stage-specific message
- refresh Eventun-backed gauntlet state after the rejection
- return the player to the correct gauntlet or menu state without implying generic network failure

### End-of-stage behavior

- runtime placement shown immediately after play may be provisional
- Eventun-accepted standings remain authoritative for the gauntlet stage record
- after completion or abort, refresh Eventun-backed gauntlet state

## Admin Web Expectations

The admin surface should eventually support:

- viewing stage attempts per gauntlet stage
- viewing current status and failure reason
- viewing region, `StageSessionId`, and AccelByte `session_id`
- manual retry / hold / defer / cancel controls
- attempt history

## Current Failure Semantics

Current Eventun sweep behavior already enforces these fallback failures:

- `allocating` or `session_created` past `deadline_claim` -> `failed(no_server_claim)`
- `claimed` past `deadline_start` -> `failed(start_timeout)`
- `started` past `deadline_finish` -> `failed(no_final_report)`

Dedicated-server-driven reporting should replace or refine those generic timeout reasons whenever possible.

## Operational Notes

- Region is hard input. The dedicated server should not assume a cross-region fallback is acceptable.
- The current model is designed to remain safe with multiple Eventun instances because ownership is DB-backed.
- Manual retry is the current intended retry policy.
- Automatic retry is deferred.

## Outstanding Gaps

The following backend pieces are still needed before the full contract exists:

- dedicated-server eligibility snapshot API
- dedicated server status API
- stage-attempt-aware final standings API
- player assignment snapshot storage
- admin controls for retry / hold / defer / cancel
- better cleanup for failed attempts with live AccelByte sessions
