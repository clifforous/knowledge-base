# Reconnect State Restoration Initial Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first production-shaped reconnect foundation for non-gauntlet Ascent: Rivals sessions by preserving durable participant identity, reserved disconnected state, scoreboard rows, and final race results independently of live SnapNet player slots.

**Architecture:** Keep `UHGPlayerLifecycleServerSubsystem` as the server-only reconnect snapshot and seat-reservation owner. Use stable replicated participant/result rows on `AHGMatchEntity` as the client-facing roster, TAB scoreboard, heat history, and final-results projection. Keep `AHGRacerPlayerEntity` as the live simulation authority while connected; participant rows remain the durable projection for disconnected racers and are refreshed from live racer facts while connected.

**Tech Stack:** UE 5.7 C++, SnapNet/SnapNetGo replicated entities and struct-array serialization, AccelByte game sessions, existing Eventun event paths, existing Ascent Rivals server subsystems.

---

## Review Update

### Decision

Do **not** add `AHGParticipantEntity` in the initial reconnect implementation. Use match-owned stable participant rows instead.

The coworker designs and the earlier independent design leaned toward a non-visual participant entity for valid reasons: identity survives `playerIndex` churn, the existing UI cache is entity-add/remove oriented, and future multi-match gauntlet sessions may need participant state beyond one match entity. Those are real advantages, but they are not decisive for this initial pass because gauntlet re-entry is out of scope, per-recipient participant relevance is not needed, and the scoreboard needs one coherent list for live racers, disconnected racers, past heats, and overall standings.

A separate participant entity would force the scoreboard to merge `AHGRacerPlayerEntity` plus participant entities, or duplicate scoreboard state across both. `AHGMatchEntity.ParticipantRows` avoids that merge.

### SnapNet Array Finding

SnapNet arrays are viable for this. `FSnapNetArraySerializer` writes array length changes separately, then delta-serializes each element by index. Struct elements then get per-field deltas through `FSnapNetStructSerializer`.

The constraint: deltas are index based, not keyed by `PlayerId`. Therefore replicated participant arrays must be stable slot arrays:

- Add rows once.
- Keep each row at the same index for the match.
- Mark rows disconnected, expired, inactive, or DNF instead of removing them.
- Do not sort replicated arrays.
- UI and summary builders sort local copies for placement/leaderboard order.

This is practical for expected match sizes and the four-heat scoreboard. It would be wrong for constantly sorted or compacted arrays.

### When To Revisit `AHGParticipantEntity`

Revisit a participant entity in a later pass if we need gauntlet-stage identity that outlives a match, per-recipient relevance filtering, shoutcaster-specific roster rules, or cross-match session roster state in one dedicated server process.

---

## Scope

### In Scope

- Non-gauntlet dedicated server reconnect state restoration.
- Stable human participant rows keyed by durable `PlayerId`, not SnapNet `playerIndex`.
- Seat reservation and server-owned snapshot restore through existing `UHGPlayerLifecycleServerSubsystem`.
- Stable replicated participant rows on `AHGMatchEntity` for connected, disconnected, expired, and finalized participant state.
- Stable heat result rows on `AHGMatchEntity` so the end scoreboard can show previous heats and overall standings without relying on live racers.
- Participant-keyed heat/match result generation for heat summaries, match summaries, final Eventun player events, and skill-rating inputs.
- Client session backing state needed by a later UX pass, without player-facing UI.
- Explicit server-crash non-recovery behavior: no warm restore, no hot standby, no rating changes from incomplete in-memory results.

### Out Of Scope

- Gauntlet stage re-entry, admission, completion, or gauntlet-specific policy.
- Operational hardening such as dashboards, reconnect metrics, rate limiting, operator tools, persistent diagnostics, or fleet monitors.
- Player-facing UX for choosing rejoin versus queue.
- Exact moving-ship restoration during an active heat. Optional active-heat reconnect may spawn the player at the last known checkpoint, not at the exact last transform or velocity.
- Ghost ships, AI takeover, or fake racer entities for disconnected users.
- SnapNet transparent client rebind research.
- Gameplay changes for dropped-input handling.
- Adding `AHGParticipantEntity` or participant entity cache support.

---

## Dropped Input Versus Seat Reservation

Dropped input and seat reservation are different failure modes.

- Dropped input happens while SnapNet may still have a live player slot and the simulation is advancing.
- Seat reservation happens after the server accepts that the human is disconnected or removed.

Seat reservation is central to reconnect and remains in this plan. Dropped-input handling is deferred because this implementation does not replay missed input and does not restore the exact moving ship state. Active-race reconnect policy is explicit: temp-spectator until next heat, spawn at last known checkpoint, or reject until next heat.

---

## Source Of Truth Model

- `AHGRacerPlayerEntity`, ship entities, and `UHGStatsServerSubsystem` remain authoritative for live simulation while a player is connected and racing.
- `UHGPlayerLifecycleServerSubsystem` remains server-only authority for reconnect reservations and compact reconnect snapshots, including frozen disconnected-racer progress used for active-heat placement.
- `AHGMatchEntity` owns replicated stable participant/scoreboard/result rows.
- Heat finalization owns DNF decisions.
- Eventun and skill rating consume participant rows instead of live-only racer loops.

Reconnect does not decide whether a previous heat is DNF. Previous heat result rows are finalized at heat end. Reconnect only binds the returning `PlayerId` to the existing participant row and new `playerIndex`.

### Implementation Clarification: Active Disconnects

When a committed racer disconnects during an active heat, the lifecycle snapshot freezes the racer model values that no longer have a live `AHGRacerPlayerEntity`: participant slot, heat index, placement, progress, lap, checkpoint, done state, credits, and aggregate stats. `AHGMatchEntity.ParticipantRows` remains the replicated scoreboard projection.

The in-race TAB list should keep the disconnected row visible and greyed out. It should continue showing placement and sorting the row by the same placement/progress comparison used for live racers. As connected racers pass the frozen disconnected progress, the disconnected row naturally falls in placement. Heat finalization preserves that placement for the disconnected DNF row unless the reservation expires first.

Reserved disconnected human seats also count against bot backfill while the reservation is active. A bot must not fill a reserved human participant slot during pre-heat or between heats unless the reservation has expired or been explicitly released.

Editor-only manual bot injection is a separate debug workflow. Console/cheat-command `AddBots` may add bots to an active race when running from editor, but automatic bot backfill must continue to respect reserved seats and must not replace a disconnected human mid-heat.

### Implementation Clarification: Active Reconnect Modes

Replace the previous boolean temp-spectator rule with an explicit active-heat mode:

- `TempSpectatorUntilNextHeat`: a reserved reconnect during the same active heat rejoins as a temp spectator. Conversion to competitor happens at the normal next-heat boundary.
- `SpawnAtLastKnownCheckpoint`: a reserved reconnect during the same active heat rejoins as a competitor and respawns at the saved checkpoint. If the player remains disconnected into a later heat, the row is carried into the new heat at starting-line state so reconnecting does not miss the full heat.
- `RejectUntilNextHeat`: a reserved reconnect during the same active heat is rejected. Rejoin can be attempted again after that active heat is no longer running.

These modes intentionally override invalid `LateJoinersMustSpectate` combinations for reserved reconnects: checkpoint mode can force competitor for the same active heat, and temp-spectator mode can force temp spectator even if ordinary late joiners may race.

---

## Follow-Up Bugs And Policy Decisions

### Seat Reservation Expiry

Current code releases the reserved seat when `UHGPlayerLifecycleServerSubsystem::ExpireSnapshots()` marks the participant row `ReservationExpired` and removes the server-only disconnected snapshot. It is called from reconnect checks, disconnected-state queries, loadout/stat restore, reserved-seat join rejection, and bot-backfill seat counting.

Implementation update: expiry should be timer-driven. The lifecycle subsystem should keep one timer pointed at the earliest `ExpiresAtUtc`, expire all elapsed snapshots when it fires, then reschedule for the next earliest snapshot. Lazy expiry calls remain as a defensive fallback.

Follow-up fix:

- Keep the explicit server timer active when disconnected snapshots exist, so expiry is applied at the configured time without waiting for a join/backfill path.
- Keep the capacity-release behavior in `ShouldRejectJoinForReservedSeat()` and `GetReservedHumanCompetitorCount()` as a defensive lazy expiry fallback.
- After timer-driven expiry removes at least one reservation, notify server backfill so AccelByte tickets and configured bot backfill can react to the newly open seat.
- Add a verification case: disconnect one or more racers, wait past `DisconnectedSeatReservationSeconds`, confirm the lifecycle snapshots are removed, the seats no longer block bot/human admission, and the participant rows transition to the intended post-expiry presentation state.

### Lobby Visibility After Expiry

Stable participant rows are intentionally not removed during a match, and the race scoreboard currently shows any row with a valid participant slot and known participant kind. Expiring the lifecycle snapshot therefore releases capacity, but it does not automatically remove the participant from every UI projection.

Policy recommendation for ordinary non-final matches:

- Keep expired rows in heat and match summaries, because they are historical results.
- Hide expired, absent participant rows from the lobby after returning from a completed match unless the player has a live `AHGPlayerEntity`.
- Keep reserved-but-not-expired rows visible as disconnected in race/post-heat contexts while the seat can still be reclaimed.

Policy recommendation for finals or future gauntlet stages:

- Treat reservations as match-series policy rather than a global reconnect timeout.
- Finals may use permanent or stage-duration reservations so disconnected finalists remain visible in the lobby/roster and can reclaim their seat.
- Implement this as a gauntlet/finals-specific lifecycle policy in the gauntlet re-entry pass, not by making ordinary `DisconnectedSeatReservationSeconds` infinite for every mode.

### Circuit Points For Fully Missed Heats

Current code can award circuit points to a disconnected participant who misses an entire later heat. The risky path is that absent non-connected rows can be carried into a new heat as committed rows, and finalization currently grants placement CP to non-connected committed rows when they still have a positive placement.

Policy recommendation:

- A participant should only be eligible for positive heat circuit points if they were connected at heat start, reconnected during that heat, or otherwise had authoritative heat participation for that heat.
- A reserved disconnected player who is carried forward for scoreboard continuity but never reconnects during the heat should receive a DNF heat result with zero newly awarded circuit points for that heat.
- Existing completed heat history and match-summary rows should remain intact.
- Eventun should still receive the heat/match end rows with `ResultOrigin` so downstream analysis can distinguish live DNF, disconnected DNF, and reservation-expired DNF.

Follow-up fix:

- Add an explicit per-heat participation/CP-eligibility flag to the participant row or heat result row, instead of inferring eligibility from `CommittedToCurrentHeat`.
- Reset carried-forward disconnected placement/progress at heat start unless checkpoint reconnect mode intentionally gives them active-race progress.
- In `FinalizeParticipantHeatRows`, award new CP only when the row is CP-eligible for that heat.

---

## Deferred UX Proposal

Do not implement player-facing UX in this pass. Preserve backing state for a later UX pass.

Future recommended UX:

- Main menu/play-route card when a reconnectable session exists: `Rejoin Match` primary, `Find New Match` secondary.
- Queue intercept dialog if the player tries to queue while a reconnectable session exists: `Rejoin Current Match`, `Abandon and Queue`, `Cancel`.

Initial implementation only needs last known session id, last known server address when available, connection interruption state, and a query for whether same-session reconnect may be attempted.

---

## File Map

### Newly Added

- `Source/AscentRivals/Public/Server/HGParticipantTypes.h`
  - Shared participant enums and SnapNet row structs used by `AHGMatchEntity`, race result generation, Eventun emission, and stats.

### Modified

- `Source/AscentRivals/Public/Server/Entities/HGMatchEntity.h`
- `Source/AscentRivals/Private/Server/Entities/HGMatchEntity.cpp`
  - Add stable `ParticipantRows` and `HeatResultRows`, plus helper methods for registering, updating, disconnecting, committing, finalizing, and querying rows.

- `Source/AscentRivals/Public/Server/Subsystems/HGPlayerLifecycleServerSubsystem.h`
- `Source/AscentRivals/Private/Server/Subsystems/HGPlayerLifecycleServerSubsystem.cpp`
  - Keep snapshots and seat reservations. Notify `AHGMatchEntity` when a human participant connects, disconnects, restores, or expires.

- `Source/AscentRivals/Public/Server/HGServerScript.h`
- `Source/AscentRivals/Private/Server/HGServerScript.cpp`
  - Ensure register/unregister flow updates lifecycle and match participant rows in the correct order. Capacity checks still count reserved humans.

- `Source/AscentRivals/Public/Server/Contexts/HGRaceServerContext.h`
- `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
  - Mark participants committed at heat start. Sync participant rows from live racers. Finalize heat rows from participant rows instead of live racers only.

- `Source/AscentRivals/Public/Server/Subsystems/HGEventunServerSubsystem.h`
- `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`
  - Add participant-identity event recording for final heat/match events that no longer require a live player entity.

- `Source/AscentRivals/Public/Server/Subsystems/HGStatsServerSubsystem.h`
- `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`
  - Add participant-result-row paths for final skill-rating inputs and conservative career/economy handling.

- `Source/AscentRivals/Public/Server/HGMessages.h`
- `Source/AscentRivals/Private/Server/HGMessages.cpp`
  - Add `ResultOrigin` to heat/match summary standing structs so UI and telemetry can distinguish live finish, live DNF, and disconnected DNF. Existing `Standings` arrays remain reliable-message payloads.

- `Source/AscentRivals/Public/Client/HGSessionSubsystem.h`
- `Source/AscentRivals/Private/Client/HGSessionSubsystem.cpp`
  - Add non-UX reconnect context state for a later UI pass.

### Explicitly Not Added

- Do not create `Source/AscentRivals/Public/Server/Entities/HGParticipantEntity.h`.
- Do not create `Source/AscentRivals/Private/Server/Entities/HGParticipantEntity.cpp`.
- Do not extend `UHGEntityCacheSubsystem` for participant entities in this pass.

### Moved Responsibility

No source files move physically.

- Final heat/match result authority moves from live `AHGRacerPlayerEntity` iteration in `UHGRaceServerContext::OnHeatFinished` to stable rows owned by `AHGMatchEntity`.
- Final `PlayerHeatEnd` and `PlayerMatchEnd` Eventun emission moves from `RecordPlayerEvent(PlayerIndex, ...)` to `RecordParticipantEvent(...)` for participant rows.
- Skill-rating inputs move from currently connected human racers to committed participant match rows.
- Client-facing scoreboard identity moves from live player entities toward `AHGMatchEntity.ParticipantRows`; the TAB race list should read participant rows for roster/stats values whenever a row exists, with live racer entities remaining the simulation write source.
- Heat summary UI should prefer reliable summary messages when present, but can rebuild missing heat/match standings from replicated `AHGMatchEntity` heat result rows after reconnect.

---

## Task 1: Define Participant Row Types

**Files:**
- Create: `Source/AscentRivals/Public/Server/HGParticipantTypes.h`

- [ ] Add Perforce file: `p4 add Source\AscentRivals\Public\Server\HGParticipantTypes.h`.
- [ ] Add enums: `EHGParticipantKind`, `EHGParticipantConnectionState`, `EHGParticipantHeatState`, `EHGParticipantResultOrigin`.
- [ ] Add `FHGParticipantScoreboardRow` using SnapNet properties for stable participant slot, `FHGPlayerProperty`, kind, connection state, current player index, reservation expiry, current heat state, result origin, live placement/progress, circuit points, credits, kills, deaths, crashes, obelisks, best lap, and best finish.
- [ ] Add `FHGParticipantHeatResultRow` using SnapNet properties for participant slot, heat index, player identity, result origin, placement, circuit points, credits, kills, deaths, crashes, obelisks, best lap, done reason, and done time.
- [ ] Keep heat history as a flat `HeatResultRows` array on `AHGMatchEntity`; do not nest a dynamic heat array inside each participant row in this pass.

---

## Task 2: Add Stable Rows To `AHGMatchEntity`

**Files:**
- Modify: `Source/AscentRivals/Public/Server/Entities/HGMatchEntity.h`
- Modify: `Source/AscentRivals/Private/Server/Entities/HGMatchEntity.cpp`

- [ ] Open files for edit with `p4 edit`.
- [ ] Include `Server/HGParticipantTypes.h`.
- [ ] Add private replicated arrays: `TArray<FHGParticipantScoreboardRow> ParticipantRows` and `TArray<FHGParticipantHeatResultRow> HeatResultRows`.
- [ ] Add a private server-authored `int32 NextParticipantSlot` slot allocator. Clients read assigned `ParticipantSlot` values from rows; they do not need to inspect the next slot value.
- [ ] Add query methods: `GetParticipantRows`, `GetHeatResultRows`, `FindParticipantRowByPlayerId`, and `FindParticipantRowBySlot`.
- [ ] Add mutation methods: `EnsureParticipantRowFromPlayerEntity`, `MarkParticipantConnected`, `MarkParticipantReservedDisconnected`, `MarkParticipantExpired`, `MarkParticipantCommittedForHeat`, `SyncParticipantFromRacer`, `FinalizeHeatParticipantRows`, `BuildHeatSummaryStandings`, and `BuildMatchSummaryStandings`.
- [ ] Enforce row stability: append new rows, never remove or compact rows during a match, and never sort `ParticipantRows` or `HeatResultRows` in place.

---

## Task 3: Keep Lifecycle Server-Only And Bridge To Match Rows

**Files:**
- Modify: `Source/AscentRivals/Public/Server/Subsystems/HGPlayerLifecycleServerSubsystem.h`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGPlayerLifecycleServerSubsystem.cpp`

- [ ] Open files for edit with `p4 edit`.
- [ ] Extend `FHGDisconnectedPlayerSnapshot` with participant slot, heat index, last known placement/progress/lap/checkpoint, done state, and whether the player was committed to the heat.
- [ ] In `CaptureDisconnectingPlayer`, sync the live racer into the match participant row before the live entity is removed.
- [ ] In `CaptureDisconnectingPlayer`, mark the row `ReservedDisconnected`, clear current player index, and store reservation expiry.
- [ ] In `CaptureDisconnectingPlayer` and heat carry-forward paths, refresh the reconnect snapshot aggregate stats from the participant row so later reconnect does not overwrite the scoreboard with stale stats.
- [ ] In `RestoreRegisteredPlayer`, restore current server-only stats/credits/loadout as today, then mark the existing participant row connected with the new `playerIndex`.
- [ ] Add active-heat reconnect policy helpers for temp-spectator, checkpoint respawn, and reject modes.
- [ ] In `ExpireSnapshots`, mark the participant row expired before removing the snapshot. Do not create DNF here; DNF is created only at heat finalization.

---

## Task 4: Wire Register/Unregister Flow

**Files:**
- Modify: `Source/AscentRivals/Public/Server/HGServerScript.h`
- Modify: `Source/AscentRivals/Private/Server/HGServerScript.cpp`

- [ ] Open files for edit with `p4 edit`.
- [ ] On human player register, ensure a match participant row exists and mark it connected.
- [ ] Let `UHGPlayerLifecycleServerSubsystem::RestoreRegisteredPlayer` restore reserved reconnect state after the row is bound to the new `playerIndex`.
- [ ] Override reserved reconnect join policy independently from ordinary late-join policy so invalid `LateJoinersMustSpectate` combinations are resolved by the explicit reconnect mode.
- [ ] On unregister, confirm lifecycle capture runs before live racer stats/loadout/credits are lost.
- [ ] Do not create participant entities or entity-cache hooks.

---

## Task 5: Mark Commitment At Heat Start

**Files:**
- Modify: `Source/AscentRivals/Public/Server/Contexts/HGRaceServerContext.h`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`

- [ ] Open files for edit with `p4 edit`.
- [ ] At the authoritative heat-start boundary, iterate live human competitors.
- [ ] For each competitor, call `MarkParticipantCommittedForHeat(PlayerId, CurrentHeatIndex)`.
- [ ] Sync each committed live racer into the participant row.
- [ ] For `SpawnAtLastKnownCheckpoint`, carry still-reserved disconnected racers into the new heat as committed rows at starting-line state.
- [ ] Treat commitment as the point where a human competitor becomes accountable for DNF if the heat completes normally.

---

## Task 6: Finalize Heat Results From Match Rows

**Files:**
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Modify: `Source/AscentRivals/Private/Server/Entities/HGMatchEntity.cpp`

- [ ] Keep live-racer simulation operations in `OnHeatFinished`: clear latent actions, set post-heat camera, disable controls, mark live `NotDone` racers, award retained contracts, and update live placement/circuit points.
- [ ] After live placement is assigned, sync every live human racer into its participant row.
- [ ] Call `MatchEntity->FinalizeHeatParticipantRows(CurrentHeatIndex, EndOfHeatTimestamp)`.
- [ ] In `FinalizeHeatParticipantRows`, create one heat result row per committed participant for the heat.
- [ ] For connected/rejoined participants, use current row values copied from live racers.
- [ ] For reserved-disconnected or expired participants, emit `DoneReason = NotDone` and `ResultOrigin = DisconnectedDnf`.
- [ ] Leave never-committed participants out of heat results.
- [ ] Preserve disconnected DNF placement from the active placement pass; do not automatically move disconnected rows to the bottom while their reservation is active.
- [ ] Populate `UHGHeatSummaryMessage::Standings` from `BuildHeatSummaryStandings`, not by appending live racers directly.

---

## Task 7: Emit Eventun Events By Participant Identity

**Files:**
- Modify: `Source/AscentRivals/Public/Server/Subsystems/HGEventunServerSubsystem.h`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`

- [ ] Add `RecordParticipantEvent` overloads that accept a participant row and optional event data.
- [ ] Set `Event.PlayerId` from `ParticipantRow.Player.Id` instead of live player lookup.
- [ ] Fill progress from row fields when no live racer exists.
- [ ] After heat finalization, emit `PlayerHeatEnd` for each finalized committed participant row, including disconnected DNF rows.
- [ ] Do not call `RecordPlayerEvent(PlayerIndex, NAME_Event_PlayerHeatEnd, ...)` for finalized participant rows that may not have a live player index.

---

## Task 8: Refactor Match Summary And Skill Rating Inputs

**Files:**
- Modify: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Modify: `Source/AscentRivals/Public/Server/Subsystems/HGStatsServerSubsystem.h`
- Modify: `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`

- [ ] On final heat, build `UHGMatchSummaryMessage::Standings` from `AHGMatchEntity` participant rows through `BuildMatchSummaryStandings`.
- [ ] Add a stats subsystem path that accepts participant rows for final skill-rating inputs.
- [ ] Include committed disconnected DNF rows for skill-rated modes when the match completes normally.
- [ ] Keep positive career/economy rewards conservative: live/rejoined rows only unless product explicitly decides otherwise.
- [ ] Continue sending `UHGPlayerMatchResultsMessage` only to connected players.

---

## Task 9: Add Client Reconnect Backing State Only

**Files:**
- Modify: `Source/AscentRivals/Public/Client/HGSessionSubsystem.h`
- Modify: `Source/AscentRivals/Private/Client/HGSessionSubsystem.cpp`

- [ ] Open files for edit with `p4 edit`.
- [ ] Add backing fields for last known game session id, last known server address when available, last interruption reason, reconnect candidate timestamp, and whether same-session reconnect may be attempted.
- [ ] Expose small query methods for a future UI pass.
- [ ] Do not add widgets, routes, buttons, copy, or queue intercepts.

---

## Task 10: Verification

- [ ] Row stability: add two participants, disconnect one, finish one, expire one, add a third. Existing rows keep their indices; no replicated array is compacted or sorted in place.
- [ ] Disconnect mid-heat: committed human disconnects, TAB keeps the greyed row in placement order, heat completes normally, heat summary includes `DisconnectedDnf`/`NotDone`, and `PlayerHeatEnd` emits by `PlayerId` without live racer lookup.
- [ ] Active checkpoint reconnect: with `SpawnAtLastKnownCheckpoint`, a reserved reconnect during the same active heat spawns as a competitor at the saved checkpoint with loadout, credits, and aggregate stats restored.
- [ ] Reconnect after previous heat: heat 1 remains DNF after reconnect; heat 2 can commit the same participant row with a new `playerIndex` or carry the disconnected reservation at starting-line state; end scoreboard shows heat 1 plus overall.
- [ ] Late-join setting matrix: verify reserved reconnect behavior for `TempSpectatorUntilNextHeat`, `SpawnAtLastKnownCheckpoint`, and `RejectUntilNextHeat` with `LateJoinersMustSpectate` both true and false.
- [ ] Normal four-heat match: no-disconnect summaries and standings match current behavior.
- [ ] Competitive rating: committed disconnected DNF row is included in skill-rating inputs for skill-rated modes; positive rewards follow the conservative policy.
- [ ] Server crash: incomplete in-memory rows do not produce rating or accepted match results.

---

## Final Recommendation

Proceed with match-owned stable participant rows for the initial implementation.

This preserves the useful parts of the coworker proposals: durable participant identity, participant-keyed Eventun events, commitment semantics, DNF rows for disconnected committed players, and live-racer independence for final results. It removes the extra participant entity layer from this pass so TAB, heat history, and overall standings can use one match-owned scoreboard source.
