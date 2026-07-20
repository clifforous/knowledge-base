# Gauntlet Stage Events Implementation Plan

Archive notice: Historical first-pass server plan. Use
`ascent-rivals/system/eventun/gauntlet-stage-runtime-contract.md` for current behavior and the
active gauntlet-runtime initiative for remaining client/runtime work.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add game-server support for Eventun gauntlet stage-run claim, admission, per-match acceptance, multi-match lobby return, and stage completion without changing ordinary matchmaking behavior.

**Architecture:** Do not add a new server subsystem in this pass. Keep Eventun API transport and stage-run coordination in `UHGEventunServerSubsystem`; keep human admission, reconnect, reserved seats, and stage participant lifecycle policy in `UHGPlayerLifecycleServerSubsystem`; keep join orchestration and travel decisions in `UHGServerScript`/race and lobby contexts.

**Tech Stack:** UE 5.7 C++, SnapNet/SnapNetGo server contexts and replicated entities, AccelByte game sessions, generated Eventun game-server APIs, Eventun trusted server events, existing match-owned participant rows.

---

## Status

Server implementation pass completed locally on 2026-05-06. The first server pass follows the reviewed ownership model: Eventun API coordination lives in `UHGEventunServerSubsystem`, admission and stage-long disconnected reservations live in `UHGPlayerLifecycleServerSubsystem`, and match/lobby orchestration stays in `UHGServerScript` plus race context. This checkpoint has static validation only; runtime validation still needs to happen in a follow-up pass.

Foundation supersession note (2026-07-13): the telemetry retry work in Task 3 is historical and must not be implemented as written. The game now records `ActiveMatchRequest` as one identified MatchStart/MatchEnd envelope and submits it through shared `ClientService.IngestMatch`; it clears the request before asynchronous dispatch and remains best-effort/at-most-once. Eventun already provides stable batch/event identities and idempotent equal-content acceptance, but enabling bounded sender retry is a separate deployment decision. The four gauntlet stage-run operations now live on ServerService, while ingestion is not duplicated there.

Current implementation checkpoint:

- Stage-run session settings are parsed into `FHGGauntletConfig`: `StageRunId`, `RunNumber`, `StageRunShardKey`, `OverflowPolicy`, `AdmissionPriorityRule`, and `RosterLockPoint`.
- `MatchStart` Eventun payloads now include `StageRunId` and `RunNumber`.
- `UHGEventunServerSubsystem` wraps the generated claim, admission, match acceptance, and completion APIs.
- Dedicated-server readiness for stage runs is gated on both gauntlet stats sync and successful stage-run claim.
- `UHGPlayerLifecycleServerSubsystem` rejects new competitors after first `MatchStart`, skips spectator-only admission for V1, and keeps disconnected competitor reservations through the full stage.
- Race finalization waits for Eventun match acceptance before returning a multi-match stage to lobby or ending the session.
- Multi-match stage continuation applies the next circuit entry and returns to the existing lobby flow within the same AccelByte session.
- Disconnected stage participants can seed current-match participant rows so later matches can still emit participant-keyed DNF rows.
- Stage-run sessions no longer end just because all live humans disconnect after the scheduled match start; reserved stage participants keep the server alive for disconnected/DNF completion.
- Client session discovery now carries `StageRunId`, but full join-status preflight and root-menu entry remain immediate follow-up work.

Known first-pass limitations:

- Eventun claim response `StageConfig` is cached only for required match count. Course/race settings still rely on session settings containing the full circuit for this pass.
- Final stage shutdown now waits for `CompleteGauntletStageRun` to resolve instead of relying only on match acceptance, but Eventun event/accept/complete retry state is still in-memory and not backed by a durable retry state machine.
- No role-aware spectator, shoutcaster, or administrator admission exists yet.
- No team backup/replacement policy exists yet.
- Stage-run sessions with no human ever joining still use the existing scheduled empty-session shutdown path.
- Client `ClientServiceGetGauntletStageJoinStatus(GauntletId, Stage)` integration remains the next required testability task.

Authoritative supporting docs:

- [[gauntlet-stage-orchestration-improvements]]
- [[gauntlet-finals-and-tournament-modes-design-review]]
- [[ascent-rivals/system/eventun/gauntlet-stage-runtime-contract]]
- [[ascent-rivals/system/eventun/events]]
- [[ascent-rivals/system/eventun/api]]
- [[reconnect-state-restoration-initial-implementation-plan-2026-04-29]]

## Key Decisions

- A gauntlet stage run is active only when the session config includes `StageRunId`.
- `stage_run_id` remains Eventun's durable run id.
- `session_id` remains the AccelByte game session id and Eventun server-event session id.
- A stage run uses one dedicated server and one AccelByte game session for every configured match in the stage.
- Multi-match stages return to lobby between matches when the match has a lobby.
- Stage participants are server-owned lifecycle state, not a new replicated participant entity.
- `AHGMatchEntity` participant rows remain the current-match replicated result projection.
- `UHGEventunServerSubsystem` owns Eventun API calls and retry state because it already owns the generated Eventun server API pointer.
- `UHGPlayerLifecycleServerSubsystem` owns admission decisions after Eventun returns policy input because it already owns reconnect snapshots, reserved seats, and human lifecycle rules.
- V1 rejects all new competitors after the first `MatchStart`; future behavior should be driven by Eventun stage/session configuration.
- V1 reserves disconnected competitor seats for the full stage by default.
- V1 adds a dedicated gauntlet stage between-match lobby delay setting instead of reusing the general next-match delay.
- V1 does not expose spectator/shoutcaster/admin joins. If a spectator-only path exists anyway, it skips Eventun admission until Eventun and the game join request can express role intent.
- Immediate follow-up client work must let a qualified player discover and join an active stage from the game client, likely from the root play menu first, with notification-based entry left as a presentation decision.
- Ordinary matchmaking sessions should pay no stage-run cost beyond cheap `StageRunId` checks.

## Current Source Facts

- `HGSessionSettings.h` has gauntlet settings for `GauntletId`, `GauntletStage`, `Circuit`, lobby size, allowed teams, and related stage config, but not `StageRunId`, `RunNumber`, or `StageRunShardKey`.
- `FHGGauntletConfig` has stage configuration and `Circuit`, but not stage-run identity or admission policy metadata.
- `HGMatchConfig.cpp` parses every circuit entry, but only applies the first entry to the initial course/laps/heats.
- `AHGMatchEntity` already exposes `SetNumMatchesInSeries`, `ResetHeats`, stable participant rows, and participant heat result rows.
- `UHGPlayerLifecycleServerSubsystem::IsEnabledForCurrentMatch()` intentionally returns false for `GauntletStageOnly`.
- `HGServerScript::OnPlayerJoinRequested()` currently performs legacy stat qualification for gauntlet sessions and then continues synchronous join handling.
- `UHGEventunServerSubsystem` records and submits trusted Eventun events, but `SubmitActiveMatchEvents()` clears the active request before the HTTP result is known.
- `HGRaceServerContext::OnFinished()` submits match events, records stats, and immediately schedules gauntlet final session shutdown.
- `HGLobbyServerContext` can auto-start a gauntlet lobby from `AHGGauntletEntity::MatchTimeSeconds`.
- The generated SDK already has game-server APIs for:
  - `AdminServiceClaimGauntletStageRun`
  - `AdminServiceCheckGauntletStageRunAdmission`
  - `AdminServiceAcceptGauntletStageRunMatch`
  - `AdminServiceCompleteGauntletStageRun`

## Ownership Model

### `UHGEventunServerSubsystem`

Owns Eventun server API integration and stage-run operation state:

- current claimed stage-run response
- current accepted match count and required match count
- active event submit request for the current match
- stage-run claim, admission API wrapper, match acceptance, and run completion calls
- retry timers for Eventun event submit, match acceptance, and run completion
- delegates or callbacks used by `HGServerScript`, lifecycle, and race context

It should not decide whether a player ultimately joins the game. It should return Eventun's admission response as policy input.

### `UHGPlayerLifecycleServerSubsystem`

Owns human competitor lifecycle and admission policy:

- stage-run admission decision request entry point
- stage participant roster while the dedicated server owns the run
- reserved reconnect snapshots across matches
- whether a player is treated as competitor, temp spectator, or rejected
- whether `GauntletStageOnly` reconnect support is active
- stage roster lock behavior

It should call into `UHGEventunServerSubsystem` for the actual Eventun admission API request, then combine that response with existing capacity, reservation, reconnect, spectator, and lifecycle rules.

### `UHGServerScript`

Owns server orchestration:

- parse initial stage-run config
- claim stage run before `DSSessionReady`
- hold or reject pending join requests while admission is async
- continue the existing SnapNet join path after lifecycle accepts admission
- mark server ready only after the stage run is claimed and gauntlet display data is safe enough for clients
- travel to lobby/course at stage boundaries
- end/delete the session only after stage completion succeeds or stage-run mode is not active

### `HGRaceServerContext` and `HGLobbyServerContext`

Own match-state transitions:

- race context records events and begins finalization after a natural match finish
- race context waits for Eventun event submit and stage-run match acceptance before advancing
- race context asks server script to return to lobby for non-final stage matches
- lobby context auto-starts the next stage match after the configured between-match delay

## Stage-Run Data Additions

### Session Settings

Add constants in `Source/AscentRivals/Public/Net/HGSessionSettings.h`:

- `SETTING_GAUNTLET_STAGE_RUN_ID` mapped to `StageRunId`
- `SETTING_GAUNTLET_RUN_NUMBER` mapped to `RunNumber`
- `SETTING_GAUNTLET_STAGE_RUN_SHARD_KEY` mapped to `StageRunShardKey`
- `SETTING_GAUNTLET_OVERFLOW_POLICY` mapped to `OverflowPolicy`
- `SETTING_GAUNTLET_ADMISSION_PRIORITY_RULE` mapped to `AdmissionPriorityRule`
- `SETTING_GAUNTLET_ROSTER_LOCK_POINT` mapped to `RosterLockPoint`

Keep existing names unchanged for backward compatibility with older sessions.

### Match Config

Extend `FHGGauntletConfig` in `Source/AscentRivals/Public/Server/HGMatchConfig.h`:

- `FString StageRunId`
- `int32 RunNumber`
- `FString StageRunShardKey`
- `FString OverflowPolicy`
- `FString AdmissionPriorityRule`
- `FString RosterLockPoint`
- helper predicates:
  - `bool IsStageRun() const`
  - `bool HasMultiMatchCircuit() const`

The helper can be inline and should return true for stage-run mode only when `StageRunId` is non-empty.

### Game Settings

Add a dedicated setting in `Source/AscentRivals/Public/HGGameSettings.h`:

- `GauntletStageBetweenMatchLobbyDelaySeconds`

This controls the lobby delay between accepted matches in one gauntlet stage run. It should not reuse `GeneralSettings.NextMatchDelaySeconds`, because gauntlet stage operations will later need administrator and shoutcaster controls such as pausing the next-match timer.

### Future Eventun Admission Configuration

V1 locks competitor admission at first `MatchStart`. Eventun should own this policy in a later pass through stage/session configuration from initial session creation or the stage-run claim response. The existing `RosterLockPoint` field is the likely first place to carry that policy, but the game should keep the first-pass behavior simple:

- before first `MatchStart`: admitted competitors can enter the stage roster
- at first `MatchStart`: roster locks
- after first `MatchStart`: new competitors are rejected
- reserved reconnect for locked stage participants remains allowed

### Immediate Client Join Follow-Up

The server work is hard to validate without a game-client path into the stage session. The immediate client follow-up should add a small, testable eligibility and join-entry path:

- use existing gauntlet calendar/session data to find active stage sessions
- check stage requirements using current gauntlet/player stats logic
- call `ClientServiceGetGauntletStageJoinStatus(GauntletId, Stage)` to confirm the stage is still joinable
- show a join option only when the player qualifies and Eventun reports the stage joinable
- join through the existing AccelByte session join flow
- keep server admission authoritative even when client preflight passes

The final UX surface is undecided. Root menu entry is the practical first test surface because `HGPlayRootMenu` already evaluates active gauntlets and joins gauntlet sessions. A notification or toast can later consume the same eligibility state once the product flow is designed.

### Stage Participant State

Add server-only structs in `HGPlayerLifecycleServerSubsystem.h`:

- `FHGGauntletStageAdmissionDecision`
  - `FString PlayerId`
  - `bool bEventunAllowed`
  - `FString EventunReason`
  - `int32 PriorityScore`
  - `FString TeamId`
  - `FString TeamName`
  - `FString TeamTag`
  - `bool bAllowedAsCompetitor`
  - `bool bAllowedAsSpectator`
  - `bool bReservedReconnect`
- `FHGGauntletStageParticipantState`
  - `FString PlayerId`
  - `int32 ParticipantSlot`
  - `FDateTime FirstAdmittedAtUtc`
  - `FDateTime LastSeenAtUtc`
  - `bool bRosterLocked`
  - `bool bDisconnected`
  - `bool bReservationExpired`

This state is not replicated directly. `AHGMatchEntity` remains the replicated current-match projection.

### Gauntlet Entity

Extend `AHGGauntletEntity` only with fields that clients benefit from seeing:

- `StageRunId`
- `CurrentMatchId`
- `AcceptedMatchCount`
- `RequiredMatchCount`
- `RunStatus`

Keep `IsFinalSession()` for compatibility, but add a clearer helper:

- `bool IsStageRunSession() const`

Stage-run code should use `IsStageRunSession()` instead of overloading "final session" semantics.

## Eventun Flow

### Server Start

1. `UHGServerScript::OnStart()` builds `InitialMatchConfig`.
2. If `InitialMatchConfig->GauntletConfig` has `StageRunId`, stage-run mode is active.
3. Create gauntlet entity and copy basic gauntlet config onto it.
4. Call `UHGEventunServerSubsystem::ClaimGauntletStageRun()`.
5. On claim success:
   - cache the claim response in `UHGEventunServerSubsystem`
   - validate `StageRunId`, `SessionId`, `GauntletId`, `Stage`, and required match count
   - copy current match count/status onto `AHGGauntletEntity`
   - set `AHGMatchEntity::SetNumMatchesInSeries(Circuit.Num())`
   - initialize current match config from circuit index 0
   - enable lifecycle stage-run mode
   - continue gauntlet metadata/stat sync
   - call `MarkServerAsReadyForConnections()` once all required startup gates are satisfied
6. On claim failure:
   - do not mark server ready
   - log `StageRunId`, `SessionId`, error code, and reason
   - request shutdown with a stage-run claim failure reason

Startup readiness should become a small gate model rather than being tied only to `OnGauntletStatsUpdated()`. The gates for stage-run mode are:

- AccelByte session is known
- stage run is claimed
- gauntlet entity is created
- gauntlet display data is initialized or explicitly skipped after a logged fetch failure

### Human Competitor Admission

1. `UHGServerScript::OnPlayerJoinRequested()` extracts player id and spectator intent from the join request.
2. If not stage-run mode, keep existing join flow.
3. If stage-run mode and the join is spectator-only, use existing spectator capacity rules and do not include the player in stage participant state.
4. If stage-run mode and the join is a human competitor or reserved reconnect:
   - hold the join request for async completion
   - call `UHGPlayerLifecycleServerSubsystem::RequestGauntletStageAdmission()`
   - lifecycle calls `UHGEventunServerSubsystem::CheckGauntletStageRunAdmission()`
   - lifecycle combines Eventun response with reserved-seat and roster-lock policy
   - server script resumes the existing join path on allow
   - server script rejects with a clear denial code on disallow

The first implementation task must verify the SnapNet join request object lifetime supports async completion. If the request cannot safely outlive `OnPlayerJoinRequested()`, add a server-owned pending join map keyed by player id and reject if a second pending join arrives for the same id.

Admission is v1 fail-closed for competitors:

- Eventun API error rejects new competitor joins.
- Reserved reconnect admission API error also rejects, because Eventun must validate run/session/phase.
- Open stages still call Eventun admission.
- Replacement by higher `priority_score` is not implemented in this pass; if Eventun allows a higher-priority player but the DS is full, the DS rejects with a logged "replacement unsupported" reason.

Spectator admission is intentionally deferred:

- The desired future behavior is for every human join to call Eventun admission with role intent.
- The current first-pass API/game join path does not clearly declare spectator, shoutcaster, or admin role.
- No player-facing spectator join UI is in scope for this pass.
- If a spectator-only path is reachable in v1, it skips Eventun admission and remains outside stage participant state.

### Roster Lock

Use conservative v1 roster locking:

- Before first match start, admitted human competitors become stage participants.
- At first `MatchStart`, lifecycle locks the stage roster.
- Between matches, reserved reconnect is allowed for locked stage participants.
- New human competitors after roster lock are rejected.
- Spectators remain outside roster lock and outside final standings.

This keeps gauntlet placement semantics stable while leaving richer replacement behavior for a separate pass. Future team and bracket support can allow a backup team player to take a disconnected teammate's slot, but that requires explicit Eventun policy, game role/team context, and clear replacement messaging.

### Match Event Submit

1. Race context records existing events:
   - `MatchStart`
   - `PlayerHeatStart`
   - `PlayerHeatEnd`
   - `HeatEnd`
   - `PlayerMatchEnd`
   - `MatchEnd`
2. `MatchStart` includes `GauntletId` and `Stage` for stage-run sessions.
3. Participant-row emission continues to include disconnected/DNF humans.
4. Bots and spectators are excluded from human participant final rows.
5. On natural match finish, race context calls a stage-aware submit path.

`SubmitActiveMatchEvents()` must stop discarding data before the HTTP result:

- move active match events into a pending request for the match id
- keep pending request until Eventun returns `Accepted == true` or the caller explicitly discards the match
- if Eventun returns transport error or `Accepted == false`, notify failure and leave the pending request retryable
- clear only the accepted match's pending request after successful submit

The hardening can be global; ordinary sessions benefit and stage-run sessions require it.

### Match Acceptance

After Eventun accepts the server event batch:

1. `UHGEventunServerSubsystem` calls `AcceptGauntletStageRunMatch(StageRunId, MatchId, { SessionId })`.
2. On success:
   - update `AcceptedMatchCount`
   - update `RequiredMatchCount`
   - update `AHGGauntletEntity`
   - notify race context that stage match acceptance succeeded
3. On failure:
   - keep the match in `WaitingForStageMatchAcceptance`
   - retry with the same `StageRunId`, `SessionId`, and `MatchId`
   - do not travel to lobby, next course, or shutdown

### Stage Completion

If `AcceptGauntletStageRunMatch` returns ready-to-complete:

1. `UHGEventunServerSubsystem` calls `CompleteGauntletStageRun(StageRunId, { SessionId })`.
2. On success:
   - update `AHGGauntletEntity.RunStatus`
   - clear lifecycle stage-run admission state
   - notify race context/server script that completion is accepted
   - schedule normal gauntlet post-match shutdown/session deletion
3. On failure:
   - keep the stage in `WaitingForStageRunCompletion`
   - retry with the same `StageRunId` and `SessionId`
   - keep the AccelByte session alive while the DS is alive
   - after bounded local retries are exhausted, log the completion failure and end the DS session through the normal shutdown grace path

Implementation note, 2026-05-07:

- The game server exposes a separate stage-run completion callback from `UHGEventunServerSubsystem`.
- `HGRaceServerContext` waits for that callback before scheduling final stage shutdown.
- The match-submission SnapNet notification message now initializes its `MatchId` range so multi-match stage IDs do not clamp to zero on clients.

## Multi-Match Stage Flow

Use one AccelByte session and one dedicated server for every match in the stage run.

### Initial Match

- Use circuit index 0 from the claim/session circuit.
- Set course, laps, heats, race mode, and `NumMatchesInSeries`.
- Start from lobby using the existing gauntlet autostart path.

### Returning To Lobby

After match N is accepted and N is not the final required match:

1. Race context asks server script to prepare match N+1.
2. Server script applies circuit index N+1 to `AHGMatchEntity`.
3. Server script updates `AHGGauntletEntity.CurrentMatchId`.
4. Race context starts a short "returning to lobby" countdown for clients already on match summary.
5. Server script travels to lobby.
6. Lobby context converts temp spectators as normal and refreshes hauler state.
7. Lobby context starts the next-match countdown from a stage-run between-match delay.

Use `FHGGameSettings::GauntletStageBetweenMatchLobbyDelaySeconds` for v1. This setting exists separately from `GeneralSettings.NextMatchDelaySeconds` so a later administrator/shoutcaster pass can pause or adjust the next-match timer without changing ordinary match summary flow.

### Applying The Next Circuit Entry

Add one helper in `UHGServerScript` or `AHGMatchEntity` rather than duplicating circuit logic in race and lobby contexts:

- `bool ApplyGauntletStageCircuitMatch(const int32 MatchIndex)`

Responsibilities:

- validate stage-run mode
- validate `GauntletConfig.Circuit.IsValidIndex(MatchIndex)`
- resolve `FHGCourseConfig.CourseId` to `UHGCourseDefinition`
- set match course
- set laps override if present
- set heats if present
- set race mode from gauntlet config
- reset current-match heat/result state only after prior match is accepted
- log match id, course id, laps, heats, and required match count

Do not clear lifecycle stage participants when applying a new match. Current-match participant rows may reset, but lifecycle must preserve stage roster and reconnect reservations between matches.

### Final Match

After the final match is accepted:

- do not return to lobby
- call stage completion
- only schedule `EndSession()` after completion succeeds

## Edge Cases

### Disconnected Competitors

- Existing stable participant rows should continue to produce disconnected/DNF `PlayerHeatEnd` and `PlayerMatchEnd` rows for the current match.
- Lifecycle must preserve stage participants across lobby return.
- Before each match starts, seed current-match participant rows from locked lifecycle stage participants so a competitor who misses an entire subsequent match still receives a participant-keyed DNF row.

### Reservation Expiry

- Non-stage ordinary reservation settings remain unchanged.
- Stage-run participants use stage-duration reservation while the run is active.
- A disconnected stage participant keeps their competitor slot for the full stage by default.
- If the player misses a later match, they still receive participant-keyed DNF rows.
- Future team modes may allow a backup team player to replace a disconnected teammate, but that is out of scope for the first pass.

### Server Crash Or Non-Completion

- If the DS crashes before event submit, Eventun has no accepted match and the stage run remains incomplete until backend expiry/recovery handles it.
- If the DS crashes after event submit but before match acceptance, Eventun may have a match summary but no accepted stage-run match.
- If the DS crashes after match acceptance but before completion, Eventun has accepted match rows but no final stage placement.
- This pass does not add a game-side abort API because the Eventun contract has not exposed that control yet.

### Eventun Failure

- Claim failure prevents readiness.
- Admission failure rejects competitor joins.
- Event submit failure prevents match acceptance.
- Match acceptance failure prevents lobby return, next match, completion, and shutdown.
- Completion failure prevents shutdown while the DS remains alive.

### Spectators And Shoutcasters

- The desired long-term behavior is for every human join to call stage-run admission with declared role intent.
- The current first pass does not expose spectator, shoutcaster, or admin join UI.
- Spectator-only joins do not call stage-run admission in v1 if such joins are still reachable.
- Spectators do not create lifecycle stage participant state.
- Spectators are excluded from `PlayerMatchEnd` participant rows and Eventun stage placements.
- Shoutcaster/admin-specific admission is deferred until Eventun exposes richer role policy or the game has a dedicated role signal in join requests.

### Bots

- Bots may fill race slots according to existing bot policy.
- Bots are not stage participants.
- Bots should not be emitted as human `PlayerMatchEnd` rows for Eventun stage placement.
- Bot circuit points can affect local race order but must not become Eventun gauntlet placement records.
- Early developer testing is expected to use one or two local clients or a small number of developers, not a full 16-player lobby.
- Test gauntlet stages should be configured to allow small human counts and bot backfill.
- Bot backfill should not block stage acceptance because Eventun completion consumes human participant placements, not bot rows.
- Verify the game does not wait for 16 humans when a stage is explicitly configured for small-team developer testing with bots.

### Replacement And Priority

- Eventun admission response includes priority and team context.
- V1 records/logs priority and team context but does not kick or replace already-admitted competitors.
- If a stage is full, new competitors are rejected even when priority is higher.
- A separate replacement pass can add explicit kick, replacement messaging, and roster rebalancing.

## Source File Plan

### Task 1: Parse Stage-Run Session Settings

**Files:**

- Modify: `Source/AscentRivals/Public/Net/HGSessionSettings.h`
- Modify: `Source/AscentRivals/Public/Server/HGMatchConfig.h`
- Modify: `Source/AscentRivals/Private/HGMatchConfig.cpp`

Steps:

- [ ] Open files with `p4 edit`.
- [ ] Add stage-run setting constants.
- [ ] Extend `FHGGauntletConfig` with stage-run identity and policy fields.
- [ ] Parse the new settings from AccelByte session settings.
- [ ] Parse or default `RosterLockPoint`, but use first `MatchStart` as the only v1 competitor lock point.
- [ ] Preserve legacy gauntlet config parsing when `StageRunId` is absent.
- [ ] Update `FHGMatchConfig::ToString()` and `ToURLOptions()` if they are used for session/debug visibility of gauntlet settings.
- [ ] Add logging for parsed `StageRunId`, `RunNumber`, `StageRunShardKey`, circuit count, and roster policy.

Verification:

- [ ] Start from a session settings sample with `StageRunId`; confirm parsed config has `IsStageRun() == true`.
- [ ] Start from a legacy gauntlet settings sample with no `StageRunId`; confirm behavior remains legacy.
- [ ] Confirm a multi-entry `Circuit` produces the same number of parsed `FHGCourseConfig` entries.

### Task 2: Add Stage-Run API Wrappers To `UHGEventunServerSubsystem`

**Files:**

- Modify: `Source/AscentRivals/Public/Server/Subsystems/HGEventunServerSubsystem.h`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`

Steps:

- [ ] Open files with `p4 edit`.
- [ ] Add cached stage-run fields for claim response, accepted match count, required match count, and current run status.
- [ ] Add `IsGauntletStageRunActive()` and `GetClaimedGauntletStageRun()` accessors.
- [ ] Add `ClaimGauntletStageRun(const FHGGauntletConfig& GauntletConfig, TFunction<void(bool)> Completion)`.
- [ ] Add `CheckGauntletStageRunAdmission(const FString& PlayerId, TFunction<void(const FAccelByteEventunCheckGauntletStageRunAdmissionResponse*, int32, const FString&)> Completion)`.
- [ ] Add `AcceptGauntletStageRunMatch(int32 MatchId, TFunction<void(bool, bool)> Completion)` where the second bool means ready-to-complete.
- [ ] Add `CompleteGauntletStageRun(TFunction<void(bool)> Completion)`.
- [ ] Register every SDK task with `RegisterTask`.
- [ ] Log success and failure with `StageRunId`, `SessionId`, `MatchId` when present.

Verification:

- [ ] Confirm each wrapper no-ops or fails cleanly when `EventunServerApi` is invalid.
- [ ] Confirm wrappers use `GetServerScriptChecked<UHGServerScript>().GetSessionId()` for the body `SessionId`.
- [ ] Confirm ordinary non-stage sessions do not call stage-run APIs.

### Task 3: Harden Active Match Event Submission (Historical; Superseded)

Do not execute the former pending-request/retry checklist. The foundation implementation now records stable batch/event identities in one `ActiveMatchRequest`, validates a complete MatchStart/MatchEnd envelope, clears it before asynchronous `ClientService.IngestMatch` dispatch, and reports accepted or failed state through the existing messages. Eventun provides equal-content idempotent acceptance, but the producer remains at-most-once until bounded retry is separately designed and approved.

### Task 4: Move Stage Admission Policy Into Lifecycle

**Files:**

- Modify: `Source/AscentRivals/Public/Server/Subsystems/HGPlayerLifecycleServerSubsystem.h`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGPlayerLifecycleServerSubsystem.cpp`
- Modify: `Source/AscentRivals/Public/HGGameSettings.h`

Steps:

- [ ] Open files with `p4 edit`.
- [ ] Add server-only stage participant and admission decision structs.
- [ ] Add lifecycle state for active stage run, locked roster, and stage participants.
- [ ] Add `BeginGauntletStageRun(const FHGGauntletConfig& GauntletConfig)`.
- [ ] Add `EndGauntletStageRun()`.
- [ ] Add `RequestGauntletStageAdmission(...)` with an async completion delegate.
- [ ] In `RequestGauntletStageAdmission`, call Eventun admission through `UHGEventunServerSubsystem`.
- [ ] Combine Eventun result with reserved reconnect, spectator-only, capacity, and roster-lock decisions.
- [ ] Add `LockGauntletStageRoster()` and call it when the first stage match starts.
- [ ] Make `EHGDisconnectedParticipantMode::GauntletStageOnly` return true only for active stage-run sessions.
- [ ] Keep disconnected stage participant reservations valid for the full active stage run.
- [ ] Keep existing non-stage reconnect behavior unchanged.

Verification:

- [ ] Non-gauntlet match with `GauntletStageOnly` leaves lifecycle disabled.
- [ ] Stage-run match with `GauntletStageOnly` enables lifecycle.
- [ ] A connected admitted competitor creates stage participant state.
- [ ] A reserved reconnect for an existing stage participant is allowed through lifecycle after Eventun admission allows it.
- [ ] A new competitor after roster lock is rejected.
- [ ] A disconnected stage participant keeps their reserved slot across lobby return and subsequent matches.

### Task 5: Make Join Requests Stage-Run Aware

**Files:**

- Modify: `Source/AscentRivals/Public/Server/HGServerScript.h`
- Modify: `Source/AscentRivals/Private/Server/HGServerScript.cpp`

Steps:

- [ ] Open files with `p4 edit`.
- [ ] Add pending join state if `USnapNetPlayerJoinRequest` cannot safely be completed asynchronously.
- [ ] Split existing `OnPlayerJoinRequested()` into:
  - initial request extraction
  - stage-run admission gate
  - existing capacity/reservation checks
  - final call to `Super::OnPlayerJoinRequested()`
- [ ] For stage-run competitors, call lifecycle admission before legacy gauntlet qualification.
- [ ] Skip legacy `QualifiedPlayers` admission for `StageRunId` sessions.
- [ ] Keep legacy `QualifiedPlayers` admission for older gauntlet sessions.
- [ ] Keep spectator-only joins outside Eventun participant admission in v1.
- [ ] Add a clear comment/log note that future role-aware admission should call Eventun for spectator, shoutcaster, and admin joins.
- [ ] Reject duplicate pending joins for the same player id.
- [ ] Preserve pending reserved reconnect force flags only for the join request being completed.

Verification:

- [ ] Legacy gauntlet session still uses existing stat qualification.
- [ ] Stage-run session calls Eventun admission for competitor join.
- [ ] Stage-run spectator join does not create stage participant state.
- [ ] Rejected admission completes the join request with a rejection code and logs the Eventun reason.
- [ ] Accepted admission continues through existing SnapNet registration.

### Task 6: Claim Stage Run Before Server Readiness

**Files:**

- Modify: `Source/AscentRivals/Public/Server/HGServerScript.h`
- Modify: `Source/AscentRivals/Private/Server/HGServerScript.cpp`
- Modify: `Source/AscentRivals/Public/Server/Entities/HGGauntletEntity.h`
- Modify: `Source/AscentRivals/Private/Server/Entities/HGGauntletEntity.cpp`

Steps:

- [ ] Add startup readiness gates for stage-run claim and gauntlet display initialization.
- [ ] In `OnStart()`, detect `StageRunId` before calling `MarkServerAsReadyForConnections()`.
- [ ] Call `UHGEventunServerSubsystem::ClaimGauntletStageRun()`.
- [ ] On claim success, populate gauntlet entity stage-run fields.
- [ ] Call lifecycle `BeginGauntletStageRun()`.
- [ ] Set `AHGMatchEntity::SetNumMatchesInSeries()` from circuit count.
- [ ] Apply circuit match 0 before lobby/course travel.
- [ ] On claim failure, request shutdown without marking ready.
- [ ] Keep non-stage and legacy gauntlet readiness paths unchanged.

Verification:

- [ ] Stage-run DS does not call `DSSessionReady` before claim success.
- [ ] Claim failure leaves server unready and requests shutdown.
- [ ] Legacy non-stage DS readiness behavior is unchanged.

### Task 7: Apply Multi-Match Circuit Entries

**Files:**

- Modify: `Source/AscentRivals/Public/Server/HGServerScript.h`
- Modify: `Source/AscentRivals/Private/Server/HGServerScript.cpp`

Steps:

- [ ] Add `ApplyGauntletStageCircuitMatch(int32 MatchIndex)`.
- [ ] Resolve the circuit course id to a course definition.
- [ ] Set active course, laps override, heats, and race mode.
- [ ] Update gauntlet entity `CurrentMatchId`.
- [ ] Reset current-match heat state after prior match is accepted.
- [ ] Preserve lifecycle stage participant state across match changes.
- [ ] Log every applied match plan.

Verification:

- [ ] Single-match stage applies circuit index 0 and required match count 1.
- [ ] Multi-match stage applies index 0 on startup and index 1 after match 0 acceptance.
- [ ] Missing course id fails the stage flow before travel and logs the bad course id.

### Task 8: Gate Race Completion On Eventun Acceptance

**Files:**

- Modify: `Source/AscentRivals/Public/Server/Contexts/HGRaceServerContext.h`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`

Steps:

- [ ] Add race-context state for gauntlet stage finalization:
  - idle
  - waiting for event submit
  - waiting for match acceptance
  - waiting for run completion
  - accepted
  - failed retrying
- [ ] In `OnFinished()`, for stage-run sessions, submit events and return without scheduling shutdown.
- [ ] On event submit accepted, call `AcceptGauntletStageRunMatch()`.
- [ ] On match acceptance accepted and ready-to-complete false, schedule return to lobby.
- [ ] On match acceptance accepted and ready-to-complete true, call `CompleteGauntletStageRun()`.
- [ ] On completion accepted, schedule existing gauntlet shutdown/session end.
- [ ] On transient stage-run completion failure, retry before scheduling shutdown.
- [ ] Keep non-stage match summary and shutdown behavior unchanged.

Verification:

- [ ] Stage-run final match does not call `EndSession()` before `CompleteGauntletStageRun()` succeeds.
- [ ] Non-final stage match travels to lobby only after match acceptance succeeds.
- [ ] Event submit failure prevents match acceptance and leaves retry state.
- [ ] Match acceptance failure prevents lobby return.

### Task 9: Auto-Start Next Match From Lobby

**Files:**

- Modify: `Source/AscentRivals/Public/Server/Contexts/HGLobbyServerContext.h`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGLobbyServerContext.cpp`
- Modify: `Source/AscentRivals/Public/HGGameSettings.h`

Steps:

- [ ] Detect active stage-run session in lobby context.
- [ ] If `CurrentMatchId == 0` and official `MatchTimeSeconds` is still in the future, keep existing gauntlet autostart behavior.
- [ ] If `CurrentMatchId > 0`, use the between-match delay instead of the original absolute `MatchTimeSeconds`.
- [ ] Read the delay from `GauntletStageBetweenMatchLobbyDelaySeconds`.
- [ ] Do not require session leader to start the next stage match.
- [ ] Keep hauler enter/leave and temp spectator conversion behavior unchanged.
- [ ] If minimum competitors are not present, hold in lobby until either reserved participants reconnect or the configured timeout policy requests shutdown.

Verification:

- [ ] First match still starts from official start time.
- [ ] Second match starts after the dedicated gauntlet stage return-to-lobby delay.
- [ ] Session leader button is not required for gauntlet stage continuation.

### Task 10: Ensure Stage Participants Produce Final Events

**Files:**

- Modify: `Source/AscentRivals/Public/Server/Entities/HGMatchEntity.h`
- Modify: `Source/AscentRivals/Private/Server/Entities/HGMatchEntity.cpp`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGPlayerLifecycleServerSubsystem.cpp`

Steps:

- [ ] Add a way for lifecycle to seed current-match participant rows from locked stage participants.
- [ ] Seed rows before a stage match can emit `MatchStart`.
- [ ] Mark absent locked stage participants as disconnected/DNF for the current match.
- [ ] Keep connected human competitors synced from live racer entities.
- [ ] Exclude spectators and bots from participant final events.
- [ ] Confirm `PlayerHeatEnd` and `PlayerMatchEnd` are emitted for every locked human stage participant for every naturally completed match.

Verification:

- [ ] A player who disconnects in match 0 and misses match 1 still receives match 1 DNF participant events.
- [ ] A player who reconnects in the lobby before match 1 is represented as connected for match 1.
- [ ] A spectator present for both matches produces no stage participant final rows.

### Task 11: Client Stage Eligibility And Join Entry

**Files:**

- Modify: `Source/AscentRivals/Public/HGGauntletSubsystem.h`
- Modify: `Source/AscentRivals/Private/HGGauntletSubsystem.cpp`
- Modify: `Source/AscentRivals/Public/UserInterface/Menus/HGPlayRootMenu.h`
- Modify: `Source/AscentRivals/Private/UserInterface/Menus/HGPlayRootMenu.cpp`

Steps:

- [ ] Add a thin wrapper for `ClientServiceGetGauntletStageJoinStatus(GauntletId, Stage)`.
- [ ] Add a client-side query result that combines local stage requirement qualification and Eventun join status.
- [ ] Reuse existing gauntlet calendar/session data to identify active stage sessions.
- [ ] Reuse existing player stat qualification checks before presenting a stage join option.
- [ ] Use the Eventun join-status wrapper before joining an active gauntlet stage session from client gauntlet UI.
- [ ] Show a root play-menu join option when the player qualifies and Eventun reports the stage joinable.
- [ ] Keep the join-entry state reusable so a later notification/toast can use the same data without duplicating qualification logic.
- [ ] Treat the response as advisory only.
- [ ] If `Joinable == false`, show the existing unavailable route/message pattern.
- [ ] Continue to rely on server admission as authoritative.

Verification:

- [ ] Qualified player plus joinable stage shows the root menu join option and proceeds to AccelByte join.
- [ ] Qualified player plus non-joinable stage does not attempt client join.
- [ ] Unqualified player plus joinable stage does not show the join option.
- [ ] Server still rejects a competitor if client preflight is stale.
- [ ] The eligibility state can be consumed by a later notification entry point without changing server admission.

### Task 12: Logging And Operator Diagnostics

**Files:**

- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGPlayerLifecycleServerSubsystem.cpp`
- Modify: `Source/AscentRivals/Private/Server/HGServerScript.cpp`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGLobbyServerContext.cpp`

Steps:

- [ ] Log claim start/success/failure with `StageRunId` and `SessionId`.
- [ ] Log admission allowed/rejected with player id and Eventun reason.
- [ ] Log event submit accepted/failure with match id.
- [ ] Log match acceptance accepted/failure with accepted/required match counts.
- [ ] Log completion accepted/failure with final run status.
- [ ] Log every lobby return and next-match apply with match id and course.

Verification:

- [ ] A single-match successful run has a readable log chain from claim to completion.
- [ ] A multi-match successful run has a readable log chain for each match acceptance.
- [ ] Admission rejection logs enough data to diagnose Eventun policy versus DS capacity.

### Task 13: Knowledge Base Update After Implementation

**Files:**

- Modify: `ascent-rivals/initiatives/gauntlet-runtime/gauntlet-stage-events-implementation-plan-2026-05-04.md`
- Modify: `ascent-rivals/system/eventun/gauntlet-stage-runtime-contract.md` if the implemented game behavior changes the runtime contract assumptions
- Modify: `ascent-rivals/initiatives/gauntlet-runtime/gauntlet-stage-orchestration-improvements.md` if implementation status changes

Steps:

- [ ] Record final ownership decision: Eventun subsystem for API coordination, lifecycle subsystem for admission/re-entry policy.
- [ ] Record implemented multi-match behavior: same session, lobby between matches, server-owned auto-advance.
- [ ] Record implemented spectator/shoutcaster policy.
- [ ] Record remaining limitations: no replacement by priority, no backup team slot replacement, no spectator role admission, no administrator timer pause, no game-side abort API, crash recovery remains backend-owned.

Verification:

- [ ] KB docs do not include local machine paths.
- [ ] KB docs distinguish implemented behavior from deferred follow-up work.

## Suggested Implementation Order

1. Parse `StageRunId` and stage-run settings.
2. Add Eventun server subsystem wrappers.
3. Harden event submission.
4. Add lifecycle stage-run admission state.
5. Gate join requests through lifecycle admission.
6. Claim before server readiness.
7. Apply circuit match plans.
8. Gate race completion on event submit, match acceptance, and run completion.
9. Add the dedicated gauntlet stage between-match delay and auto-start the next match from lobby.
10. Seed participant rows for disconnected stage participants.
11. Add client stage eligibility and root-menu join entry for end-to-end testing.
12. Update KB docs with final behavior.

This order keeps each checkpoint testable and avoids starting a stage run before claim/admission/event retry behavior exists.

## Resolved Review Decisions

1. V1 rejects all new competitors after first `MatchStart`. Future behavior should be session/stage configuration supplied by Eventun, either during initial session creation or in the claim response.
2. Disconnected competitor reservations last for the full stage by default. Future team modes may allow backup team-player replacement, but that is out of scope for the first pass.
3. Gauntlet stages get a dedicated between-match lobby delay setting. Future administrator/shoutcaster support should be able to pause or adjust this timer.
4. Long term, every human join should call Eventun admission with role intent. V1 has no exposed spectator join UI and no role-aware admission contract, so spectator-only paths skip admission and remain outside participant state.
5. Client join-entry UX is not final. The immediate implementation should expose a root-menu join option for qualified players when Eventun reports the stage joinable, while keeping the eligibility state reusable for a later notification surface.
6. Early test stages should support a small number of human racers plus bot backfill. Bots must not become Eventun stage participants or placement rows.
