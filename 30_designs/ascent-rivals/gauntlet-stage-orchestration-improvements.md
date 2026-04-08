# Gauntlet Stage Orchestration Design

Date: 2026-04-08

## Purpose

This note captures the current gauntlet stage orchestration direction for Ascent Rivals.

The goals are:

- make stage session allocation and recovery durable
- keep Eventun authoritative for competition state without replicating full lobby state
- define the runtime contract between Eventun, the dedicated server, and the game client
- support the current single-session-per-stage case cleanly
- leave room for future bracket or group shard sessions without redesigning the model

## Current Implementation Status

Implemented in Eventun as of 2026-04-08:

- `RequestedRegions` is now passed to AccelByte session creation
- stage scheduling now uses raw `gauntlet_stage.stage` instead of the display-oriented calendar stage
- `gauntlet_stage_session` exists as a durable session-attempt table
- one active attempt per `(gauntlet_id, stage, shard_key)` is enforced in the database
- stage allocation now claims or creates a persisted attempt row before calling AccelByte
- stage session identity is written into AccelByte session attributes via:
  - `StageSessionId`
  - `StageSessionAttempt`
  - `StageSessionShardKey`
- allocation can reconcile an AccelByte session back into the DB attempt row using `StageSessionId`
- a minute-based sweep now:
  - expires overdue attempts
  - rechecks recent/upcoming stages
  - safely re-enters the DB-backed allocation path after restart or worker death

Not implemented yet:

- dedicated-server-to-Eventun stage status API
- stage-attempt-scoped final standings API with idempotent semantics
- dedicated-server eligibility snapshot API
- authoritative player assignment snapshot table
- automatic retry policy
- manual retry / hold / defer / cancel admin controls
- explicit failed-attempt session cleanup before the existing age-based cleanup window

## Core Invariants

- A player may compete at most once per gauntlet stage.
- A stage attempt must have exactly one authoritative owner session at a time.
- A stage attempt must end in one terminal state: `completed`, `aborted`, `failed`, `deferred`, or `cancelled`.
- Eventun is the source of truth for stage assignment, attempt ownership, and accepted outcomes.
- The dedicated server is the source of truth for runtime facts inside a claimed session.
- Region must be respected. If the requested region cannot run the stage, the system should fail or defer the attempt, not silently move it to another region.

## Current Operational Model

The current implementation is intentionally thin.

Eventun persists:

- which stage shard needs a session
- which attempt currently owns it
- the current status of that attempt
- the AccelByte `session_id` if one was created successfully
- the deadlines used to fail stuck attempts

Eventun does not yet persist:

- a per-attempt player roster snapshot table
- dedicated-server heartbeat timestamps
- started / claimed / finished timestamps

The current phase uses `shard_key = 'primary'` only.

## Stage Session State Machine

Recommended state set:

- `pending`
- `allocating`
- `session_created`
- `claimed`
- `started`
- `completed`
- `aborted`
- `failed`
- `deferred`
- `cancelled`

Current backend transitions already in place:

- `allocating -> session_created` when AccelByte session creation succeeds
- `allocating -> failed` when AccelByte session creation fails before a session id is stored
- `allocating -> failed(no_server_claim)` when `deadline_claim` expires
- `session_created -> failed(no_server_claim)` when `deadline_claim` expires
- `claimed -> failed(start_timeout)` when `deadline_start` expires
- `started -> failed(no_final_report)` when `deadline_finish` expires

Transitions still pending dedicated-server and admin API work:

- `session_created -> claimed`
- `claimed -> started`
- `claimed -> aborted(insufficient_players)`
- `started -> completed`
- `started -> failed(runtime_failure)`
- `* -> deferred`
- `* -> cancelled`

## Current Data Model Direction

### Implemented now: `gauntlet_stage_session`

This table represents one session attempt for one stage shard.

Current important fields:

- `id`
- `gauntlet_id`
- `stage`
- `shard_key`
- `attempt`
- `region_code`
- `session_id`
- `status`
- `failure_reason`
- `manual_hold`
- `deadline_claim`
- `deadline_start`
- `deadline_finish`
- `created_at`
- `updated_at`

Current important constraints:

- unique `(gauntlet_id, stage, shard_key, attempt)`
- partial unique index allowing at most one active attempt per `(gauntlet_id, stage, shard_key)`

Active statuses:

- `pending`
- `allocating`
- `session_created`
- `claimed`
- `started`

### Planned next: dedicated-server eligibility snapshot

The next DS-facing step should be an explicit stage-attempt eligibility endpoint.

Recommended shape:

- DS requests by `StageSessionId`
- Eventun returns a frozen eligibility snapshot for that attempt
- DS caches the snapshot locally and uses it for all join decisions in that session

The response should include:

- `StageSessionId`
- `GauntletId`
- `GauntletStage`
- `StageSessionAttempt`
- `StageSessionShardKey`
- stage rules such as `EntryRequirement`, `AllowedTeams`, `PlayersPerTeam`, `MinCompetitors`, `MinLobbySize`, and `Circuit`
- the eligible player list for that attempt
- any team, group, or bracket metadata needed for admission

That keeps the DS pattern simple:

- fetch once on claim or startup
- cache locally
- enforce locally for all joins

It also avoids deriving eligibility from live standings at join time.

### Deferred: `gauntlet_stage_session_player`

A dedicated `gauntlet_stage_session_player` table is still the expected long-term storage model for authoritative assignment snapshots.

That table is not implemented yet.

The eligibility endpoint can ship before the table if Eventun can still produce a stable per-attempt snapshot from existing data. Later, the endpoint can read from `gauntlet_stage_session_player` without changing the DS contract.

### `gauntlet_stage_placement`

This remains the final accepted per-stage result table.

Future work should add `stage_session_id` when the stage-attempt result API is updated.

## Current Dedicated Server Contract

Current Eventun behavior assumes the dedicated server reads gauntlet stage context from AccelByte session attributes.

The current session attribute payload includes:

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

Current direction:

- keep using session attributes for stage identity and basic rules in this phase
- add a dedicated DS eligibility endpoint next
- keep the DS fetch-once-and-cache-locally model
- add dedicated-server status and final-results APIs after or alongside the eligibility endpoint

## Participation Semantics

A player should only be considered to have competed in a stage if the stage attempt runs to accepted completion after the race has actually started.

This means:

- joining a lobby does not consume stage participation
- leaving before race start does not consume stage participation
- an aborted, deferred, or failed attempt does not consume stage participation
- a server crash does not consume stage participation if the attempt is not accepted as completed
- disconnecting mid-race does count as participation if the stage attempt completes successfully

Operationally, participation should be consumed only when Eventun accepts a `completed` stage result for that attempt.

That avoids penalizing players for infrastructure failure while still counting real competitive participation once the race has started and the attempt completed.

## Public Session Model

The current gauntlet-session model keeps AccelByte sessions public.

Why:

- it is simpler than creating private sessions and distributing invite codes
- the dedicated server can still act as the final gatekeeper

Implications:

- the client must not treat session visibility as join authorization
- the dedicated server must validate every join request against gauntlet rules and the cached eligibility snapshot
- unauthorized users may still hit the server and should be rejected quickly

Current tradeoff:

- competition integrity can still be preserved
- some server attention can be consumed by unauthorized join attempts

If abuse becomes operationally significant, private or invite-based distribution should be revisited.

## Failure Handling

### No dedicated server claim

Current backend behavior:

- if an attempt stays in `allocating` or `session_created` past `deadline_claim`, it transitions to `failed(no_server_claim)`

Interpretation:

- this currently covers both "no server in region" and "server never claimed"
- a future DS-status or AccelByte-status mapping can distinguish `region_unavailable` more precisely

### Not enough players joined

Target behavior:

- the dedicated server claims the session
- the dedicated server loads and caches the eligibility snapshot for the attempt
- the dedicated server waits for the minimum required qualified human players
- if it cannot validly start before `deadline_start`, it reports `aborted(insufficient_players)`
- Eventun records the abort and leaves retry policy to operators or later automation

### Dedicated server crashes mid-session

Current fallback:

- if the stage reaches `started` in the future and then no final report arrives before `deadline_finish`, Eventun will transition it to `failed(no_final_report)`

### Duplicate or delayed reports

Target behavior:

- status updates should be monotonic
- final results should be idempotent
- stale updates from older attempts should be rejected once a newer active attempt exists

## Multi-Instance Behavior

The current implementation is intended to be safe if multiple Eventun instances are running.

The key rules are:

- scheduling intent comes from the database, not from one-time in-memory jobs
- the stage row is locked before allocation work begins
- the stage-session row is the durable ownership record
- the active-attempt unique index prevents two active owners for the same shard
- a short allocation lease on `updated_at` stops a second worker from duplicating a still-live external create
- if one worker dies, another worker can recover on the next sweep after the lease or deadline logic takes effect

Current sweep behavior:

- runs every minute in-process
- checks recent and upcoming stages
- re-enters the same DB-backed create/reconcile flow from any instance

## Current Client and Admin Expectations

### Game client

The game client should:

- show gauntlet join affordances only when Eventun says the player is qualified for that stage
- never treat the public AccelByte session as proof that the player is allowed to join
- expect the dedicated server to perform a final admission check against the cached eligibility snapshot
- handle a server-side rejection or kick as a normal competitive rules outcome, not a networking anomaly
- refresh Eventun-backed gauntlet state when a stage ends, aborts, or rejects the player

### Admin web client

The admin surface should eventually expose:

- stage attempts by gauntlet and stage
- current status and failure reason
- region and AccelByte `session_id`
- retry / hold / defer / cancel controls
- attempt history

That work is still pending.

## Rollout Status

### Phase 1: Durable attempt ownership

Completed:

- `gauntlet_stage_session`
- stage-session identity in AccelByte attributes
- durable create/reconcile flow
- minute sweep
- deadline-based failure for stuck attempts

### Phase 2: Dedicated server runtime contract

Next:

- DS eligibility snapshot API
- `ReportGauntletStageStatus`
- stage-attempt-aware `ReportGauntletStageResults`
- idempotent status/result handling
- persisted claimed / started / finished timestamps

### Phase 3: Assignment enforcement

Later:

- `gauntlet_stage_session_player`
- authoritative player allow-list or assignment snapshot storage
- stricter join validation and anti-duplication enforcement
- `gauntlet_player_status` updates driven from accepted stage outcomes

### Phase 4: Operations

Later:

- manual retry / hold / defer / cancel / replace controls
- better failed-session cleanup
- better observability

## Open Items

- Define the exact DS eligibility endpoint payload shape and authentication model.
- Define the exact DS-to-Eventun status API payloads and allowed transitions.
- Define the exact stage-result payload shape for idempotent final standings submission.
- Decide whether retry stays manual-only or gains targeted automation for specific failure reasons.
- Decide how and when failed attempts should trigger immediate AccelByte session deletion rather than waiting for generic cleanup.
- Map AccelByte DS lifecycle states to Eventun attempt states if polling or reconciliation is added later.

## Summary

The current end state for this phase is:

- Eventun owns durable stage attempt identity and allocation recovery
- the dedicated server should fetch and cache a stage-attempt eligibility snapshot from Eventun
- participation should only be consumed on accepted completed attempts after race start
- the game client must treat Eventun qualification as authoritative and public-session visibility as non-authoritative
- the system is materially safer with multiple Eventun instances than the old in-memory watcher model
