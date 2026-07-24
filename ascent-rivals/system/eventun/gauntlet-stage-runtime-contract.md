# Ascent Rivals - Eventun Gauntlet Stage Runtime Contract

Status: current

Applicability: deployed shared-development behavior as of 2026-07-23. Production deployment remains
a separate gate.

Last consolidated: 2026-07-23

## Related
- [[../overview]]
- [[overview]]
- [[interface-architecture]]
- [[data-model]]
- [[events]]
- [[../game-client]]
- [[ascent-rivals/archive/initiatives/gauntlet-runtime/gauntlet-stage-orchestration-improvements|gauntlet-stage-orchestration-design]]

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
- `match_id` is the zero-based ordered match index within the AccelByte/session-event context
- Eventun writes only gauntlet stage bootstrap/search data into AccelByte session attributes
- the AccelByte session remains public for now
- the game client preflight result is advisory only
- the dedicated server is the final admission, seat replacement, and kick authority
- current Ascent Rivals dedicated-server code bypasses the Eventun admission call for pure unrestricted stages, even though this contract requires admission evaluation for every human competitor join/rejoin
- participation is consumed only when Eventun completes the run and writes final stage placement rows
- multi-match stages are supported through per-match acceptance and aggregate run completion
- stage allowed-team lists are implemented as player team-membership eligibility filters
- stage win/loss bracket fields are implemented as player summary admission filters
- background automatic retry and bracket advancement are not implemented yet; caller retry of an
  ambiguous allocation first reconciles the retained run identity
- team standings, team stage results, and runtime entrant snapshots are not implemented yet
- team hierarchy/designated racer priority metadata is not implemented yet

AccelByte session creation has an explicit ambiguity boundary. A timeout, transport failure,
provider-server failure, blank session id, or other incomplete create response leaves the original
`StageRunId` in `allocating`. A later caller retry reconciles that exact identity before it may
attempt another create. Only a definitive provider rejection marks the run failed. Malformed or
incomplete reconciliation rows fail closed as `Unavailable` and prevent a second provider create;
HTTP 400, 401, and 403 create rejections map to `InvalidArgument`, `Unauthenticated`, and
`PermissionDenied` respectively.

Eventun authoring rejects any stage circuit whose supplied `match_id` is not its exact array position. Every nonempty circuit therefore uses contiguous identities `0..N-1`; persistence enumerates the validated positions, and a claimed run retains those identities in its immutable rules snapshot.

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

The dedicated server should treat AccelByte session attributes as bootstrap and discovery data only.

The dedicated server should expect these stage-related attributes in the AccelByte session:

- `GauntletId`
- `GauntletStage`
- `StageRunId`
- `RunNumber`
- `StageRunShardKey`
- `RaceMode`
- `MinCompetitors`
- `MaxCompetitors`
- `GAME_SESSION_REQUEST_TYPE=GAUNTLET_STAGE`

`GAME_SESSION_REQUEST_TYPE=GAUNTLET_STAGE` is the stage-session discriminator. `StageRunId` is the Eventun run identity. The `RaceMode`, `MinCompetitors`, and `MaxCompetitors` attributes are capacity/rules settings for early setup and discovery. For the current implementation, the dedicated server applies race mode from the session settings and uses Eventun's claim response as authoritative for schedule, admission policy, and circuit runtime data.

The dedicated server should not expect stage schedule, admission policy, bracket/group/team policy, lobby-size policy, allowed teams, or circuit data in the AccelByte session attributes.

The dedicated server must call `ClaimGauntletStageRun` and use `stage_config` from the response as the stage run's required runtime plan. Each `stage_config.circuit[]` entry includes course, laps, and heats; its ordered circuit index is the Eventun `match_id`.

The dedicated server should not infer gauntlet stage identity from session name or browsing behavior.

## Eventun APIs

### Dedicated server / privileged APIs

The dedicated server uses ServerService with its subjectless token and Eventun Server permission:

- `ClaimGauntletStageRun(stage_run_id, session_id)`
- `CheckGauntletStageRunAdmission(stage_run_id, session_id, player_id)`
- `AcceptGauntletStageRunMatch(stage_run_id, session_id, match_id)`
- `CompleteGauntletStageRun(stage_run_id, session_id)`

The claim response includes `allow_any_human_player` and `requires_restricted_admission`. These fields describe whether the stage needs restricted eligibility policy, not whether the DS should call admission. The DS should still call admission for every human competitor join/rejoin.

`AcceptGauntletStageRunMatch` accepts one completed match summary for the run. It verifies:

- the run exists and is active
- the run is bound to the provided `session_id`
- the `match_id` is a valid zero-based ordered circuit index
- trusted server `MatchStart` exists for `session_id + match_id + gauntlet_id + stage`
- `match_summary(session_id, match_id)` has standings

`CompleteGauntletStageRun` completes the run only after all configured matches have been accepted. It writes aggregate final `gauntlet_stage_placement` rows and marks the run `completed`.

### Client API

The game client uses:

- `GetGauntletStageJoinStatus(gauntlet_id, stage)`

This endpoint uses the logged-in player. It returns advisory joinability, reason, active `stage_run_id`, AccelByte `session_id`, match-start state, run status, run phase, accepted/required match counts, optional current match id, stage rules, and player admission summary when applicable.

### Event ingest

The dedicated server submits the complete match through the shared operation:

- `ClientService.IngestMatch`

The generated GameServer surface selects this ClientService operation; Eventun authorizes the subjectless caller with Server `CREATE` and derives `source_kind = server`. There is no duplicate ServerService ingest operation.

Match acceptance derives standings from `match_summary(session_id, match_id)`, so the accepted server-source envelope must contain the expected `MatchStart` and `PlayerMatchEnd` data before each match is accepted. The producer records stable batch/event identities and sequence but remains best-effort/at-most-once; automatic match retransmission is separate deferred work.

Foundation cutover remains coordinated: current `match_summary` and other product reads still use the legacy event relations. The new producer/ingest path is not independently deployable until progression and serving reads move to the replacement model, retained history is converted, outputs and query plans are compared, and the legacy dependency is removed.

For multi-match stages, each match has its own `session_id + match_id` event and replay identity. Eventun stores accepted stage-run match rows separately from final aggregate placement rows.

## Data Model

Primary runtime tables:

- `gauntlet_stage_run`: durable owner row for one stage shard run
- `gauntlet_stage_run_admission`: sparse on-demand admission evaluation/audit records
- `gauntlet_stage_run_match`: accepted-match ledger for a run
- `gauntlet_stage_run_match_result`: per-player results for accepted matches
- `gauntlet_stage_placement`: StageRun/player-scoped final aggregate placements and participation signal
- immutable explicit-team field head/snapshot/owner rows
- one concrete StageRun slot per field owner plus complete occupied/no-show roster-lock evidence
- direct aggregate slot and one-slot team-owner results for occupied field slots

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

Eventun commit `6343438` makes the complete roster lock authoritative for an
explicit-team field. Before lock, Eventun performs indexed eligibility only and does not reserve a
seat. The dedicated server must serialize provisional occupancy and release it on a failed join or
pre-lock disconnect. After lock, only the exact locked player may reconnect; a no-show slot cannot
be filled. This Eventun contract and its dedicated-server integration are deployed to shared
development; player-connected smoke and soak remain outstanding.

The dedicated server should call `CheckGauntletStageRunAdmission` for every human competitor join or rejoin, including pure open stages. Open stages do not require a restricted eligibility lookup, but the admission call still validates run/session/phase, applies already-completed-stage rules, and records the admission evaluation.

Stage admission policy fields:

- `overflow_policy`: `reject_new` or `replace_lowest_prestart`
- `admission_priority_rule`: `first_come`, `qualification_points`, `selection_rank`, `team_member_rank`, or `bracket_seed`
- `roster_lock_point`: currently `match_start`

The DS owns capacity, replacement, and kick behavior. Eventun returns policy inputs and audit state.

Current implementation gap: the accepted Eventun G01 field enforces one concrete slot per team, but
the reviewed Ascent Rivals dedicated-server path does not yet consume that field, own provisional
occupancy, or submit the roster lock. `team_member_rank` and priority replacement remain configured
future policy rather than active enforcement.

## Join Mode Behavior

### Pure unrestricted open

If the stage is open and has no team, group, stage-win, or stage-loss restriction:

- the DS should still call `CheckGauntletStageRunAdmission`
- Eventun should return `allowed=true`, `reason=joinable` when the run/session/phase checks pass
- the DS admits players first come until full
- the DS still owns capacity and start readiness

The reviewed Ascent Rivals implementation does not yet satisfy the first bullet because it short-circuits unrestricted admission locally.

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

Current limit: Eventun does not compute team qualification, team standings, ordered team-member candidate lists, or team stage winners. `allowed_teams` restricts which current team members may pass admission. `players_per_team` is configured policy intent, not an Eventun-enforced stage roster, and current Ascent Rivals join handling does not appear to enforce it either.

### Bracket-shaped filters

Current bracket support is limited to required stage win/loss filters on the stage. Eventun compares those requirements to the player's gauntlet-wide status during admission.

This is not bracket progression. Eventun does not yet materialize seeds, round pairings, round entrants, winner/loser paths, or team bracket state.

### Invite-only

For invite-only stages:

- Eventun validates explicit player, team, or group invite
- after Eventun validation, the DS defaults to first come
- future team hierarchy/designated racer data may refine this, but it is not implemented now

## Dedicated Server Checklist

- On session start, read AccelByte session attributes and verify `GAME_SESSION_REQUEST_TYPE=GAUNTLET_STAGE`.
- Require `StageRunId` and the AccelByte `session_id`.
- Call `ClaimGauntletStageRun(stage_run_id, session_id)`.
- Cache the claim response for the life of the run.
- Apply the claimed `stage_config` before marking the server ready for player connections.
- Use the zero-based ordered circuit index as `match_id` for server events, match acceptance, and accepted-match tracking.
- Reject the stage if Eventun says the run/session binding is invalid.
- Use claim response `stage_config.circuit[]` as the required match plan.
- For each human competitor join/rejoin request, call `CheckGauntletStageRunAdmission(stage_run_id, session_id, player_id)`.
- Reject denied players using the returned reason.
- For allowed players, apply DS capacity and replacement rules.
- Use stage `overflow_policy`, `admission_priority_rule`, `roster_lock_point`, Eventun `priority_score`, and returned team context as policy input.
- Add explicit per-team cap and team-rank behavior before relying on `players_per_team` or `team_member_rank` in competitive team stages.
- Do not count claim, join, or admission as participation.
- Do not include players rejected or kicked before a normally completed match in final standings.
- Do include every human participant in a normally completed match, including disconnected/DNF players.
- Post the complete trusted server match through shared `ClientService.IngestMatch`.
- After each normally completed stage match, call `AcceptGauntletStageRunMatch(stage_run_id, session_id, match_id)` after required events have been posted.
- When the response reports `ready_to_complete=true`, call `CompleteGauntletStageRun(stage_run_id, session_id)`.
- Retry match acceptance and run completion with the same inputs after transient failures; both calls are intended to be idempotent for the same accepted facts.
- Do not shut down a final stage-run dedicated server solely because the final match was accepted. Wait for `CompleteGauntletStageRun` success, or for local bounded retries to exhaust and log a terminal completion failure.

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
- team standings and team-stage result materialization
- runtime entrant snapshot tables for resolved player/team fields
- team hierarchy/designated-racer priority metadata
