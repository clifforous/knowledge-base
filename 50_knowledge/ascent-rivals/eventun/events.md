# Ascent Rivals - Eventun Events

## Related
- [[../overview]]
- [[overview]]
- [[api]]
- [[data-model]]
- [[../competition-runtime-terms]]
- [[../game-client]]

## Scope
This note documents the event types currently tracked by Eventun and the currently observed shape of their `event_data` payloads.

## Sources
- `github.com/ikigai-github/eventun/blob/main/migration/a0_create_init.sql`
- `github.com/ikigai-github/eventun/blob/main/internal/eventun/events.go`
- `github.com/ikigai-github/eventun/blob/main/migration/c2_func_match.sql`
- `github.com/ikigai-github/eventun/blob/main/internal/eventun/purge_replays.go`
- Ascent Rivals source: `Source/AscentRivals/Public/Server/Subsystems/HGEventunServerSubsystem.h`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/HGServerScript.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`
- Ascent Rivals source: `Source/AscentRivals/Public/Net/HGEventunEvents.h`

## Shared Record Shape
- `time`: event timestamp
- `name`: event key
- `client_id`: OAuth client identifier that submitted the event
- `session_id`: gameplay session identifier
- `match_id`: match number within the session; values can start at `0`
- `heat`: heat number within the match
- `user_id`: present on client events; null on server events
- `player_id`: persisted only when the sender supplies a non-empty, non-bot player id
- `progress`: `{ placement, lap, checkpoint }`
- `coordinate`: `{ x, y, z }`
- `event_data`: event-specific JSON payload

## Runtime Terminology Guardrail

Eventun gameplay events follow the runtime hierarchy:

```text
Session
  Match
    Heat
      Lap
        Checkpoint
```

A qualifier is not a heat.

`activeQualifiers` on a match context payload means the match is bound to one or more gauntlet qualifier windows. It does not mean the match's heats are qualifiers.

## Game-Side Event Collection And Submission

### Ownership
- `UHGEventunServerSubsystem` owns the game-side Eventun buffer and transport.
- The buffer is `ActiveRequest`, an in-memory `FAccelByteEventunEventRequest` whose `Events` array is appended during the session.
- Race and server code record events through `RecordEvent`, `RecordPlayerEvent`, and `RecordParticipantEvent`.
- The templated overloads serialize Unreal `USTRUCT` payloads to the event `event_data` JSON at collection time.
- `UHGStatsServerSubsystem` owns local match statistics, medal counters, player result messages, and current AccelByte stat updates. Under the new Eventun progression contract, it is expected to supply per-player heat medal summaries for Eventun heat-end payloads. It does not submit Eventun events directly.

### Collection Behavior
- `RecordEvent` appends one `FAccelByteEventunAEvent` to `ActiveRequest.Events` and fills `EpochMs`, `EventName`, `SessionId`, `MatchId`, and `Heat` from the current server/session state.
- `RecordPlayerEvent` builds on `RecordEvent` and adds `PlayerId`, progress lap, placement, checkpoint, and ship coordinate when those values are available.
- `RecordParticipantEvent` builds on `RecordEvent` and fills `PlayerId`, lap, and placement from participant rows. This is used for end-of-heat and end-of-match rows when a live racer entity is not available, such as disconnected or DNF participants.
- Current events do not carry a dedicated event id. The existing natural event identity is the session, match, heat, event name, event timestamp, player id when present, and payload context.
- If a future idempotent retry feature adds event ids, the id should be assigned when the event is collected into `ActiveRequest`, not when a submit request is sent. A send-time UUID would change across retries and would not deduplicate an at-least-once resend.

### Primary Call Sites
- `UHGServerScript` registers `UHGEventunServerSubsystem` at server startup and records `SessionStart`.
- `UHGServerScript` records `PlayerJoin` and `PlayerLeft` as players enter, leave, or convert from temporary spectator to competitor.
- `UHGRaceServerContext::RecordMatchStart` records `MatchStart` when a match starts or restarts.
- Heat startup records `HeatStart` and then one `PlayerHeatStart` per active racer, including the player's loadout snapshot and weight profile.
- Race progression and combat hooks record segment and combat events such as `PlayerCheckpoint`, `PlayerLap`, `PlayerRespawn`, `PlayerKill`, and `PlayerDied`.
- Heat end records `PlayerHeatEnd` for active racers and participant rows, then emits `HeatEnd`.
- Match end records `PlayerMatchEnd` for active racers and participant rows, emits `MatchEnd`, and then decides whether to submit or clear the collected events.
- Medal award logic flows through `UHGRaceServerContext::AwardMedal` into `UHGStatsServerSubsystem::AwardMedal`. That path spawns a `UHGMedalEvent` for the affected player and increments in-memory medal tallies. The V1 progression contract should summarize those tallies into `PlayerHeatEnd.event_data.medalCounts` once per player per heat, rather than appending one Eventun row per medal occurrence.

### Match-End Submission Gate
- Current gameplay event submission is gated by successful match completion.
- A match is considered naturally finished when all configured heats finish naturally, with an editor override for stat recording.
- Single-player training is excluded from event submission.
- If the match can submit, `SubmitActiveMatchEvents` is called.
- If the match cannot submit, the game broadcasts a failed Eventun submission state and clears active events for the current match id.
- On context teardown or restart paths, the race context also clears active Eventun events to avoid leaking stale match data.

### Transport Behavior
- `SubmitActiveMatchEvents` snapshots the current `ActiveRequest` into a local `MatchRequest`.
- It then calls `Clear()` before dispatching the async API call. `Clear()` without a match id resets the whole active event buffer.
- Dedicated servers submit through `AccelByte::GameServerApi::Eventun::ServerServiceEvent`.
- Non-dedicated sessions use the client Eventun API when available.
- If no Eventun API is available, the subsystem broadcasts failed match submission state and failed gauntlet match acceptance.
- On an accepted response, the subsystem broadcasts accepted match submission state and asks Eventun to accept the gauntlet stage-run match when a gauntlet stage run is active.
- On a rejected response or transport error, the subsystem broadcasts failed match submission state and failed gauntlet match acceptance.
- Ordinary gameplay event batches are not retained for retry after the active buffer is cleared. The current behavior is best-effort one-time submission for a completed match.
- Gauntlet stage-run completion is separate from gameplay batch submission. Once Eventun accepts enough submitted matches for a stage run, the stage-run completion request has its own bounded retry behavior.

## Indexed Payload Fields
The schema extracts and stores these `event_data` fields for indexing or direct query use:
- `courseCode`
- `laps`
- `timeMs`
- `doneTimeMs`
- `loadoutValue`
- `playerType`
- `playerName`
- `playerAvatarUrl`

## Payload Shape Library

### Empty Payload
- Observed as `{}`.
- Used for pure lifecycle markers where the context is already carried by the top-level columns.

### Session Context Payload
- `clientVersion`: game build version
- `contentId`: content/environment identifier
- `matchPool`: matchmaking pool identifier
- `serverType`: server mode/type
- `localServer`: whether the session is running against a local server
- `singlePlayerMode`: local mode label such as `Scrimmage`

### Match Context Payload
- `courseCode`: stable course identifier
- `uniqueCourseCode`: course key used by the session
- `courseVersion`: course content version
- `laps`: laps per heat
- `heats`: total heats in the match
- `raceMode`: mode label such as `Deathrace`
- `stage`: stage index
- `gauntletId`: gauntlet identifier when the match is tied to a gauntlet
- `activeQualifiers`: qualifier ids active for the match; these are gauntlet qualification windows, not heats

For gauntlet stage runs, Eventun match acceptance verifies `MatchStart` by `session_id`, `match_id`, `gauntletId`, and `stage`. Multi-match stages accept each required match summary separately before completing the aggregate stage run.

### Heat Context Payload
- `courseCode`: stable course identifier (course code cannot change per heat so repeat information from match context payload)
- `uniqueCourseCode`: course key used by the session (unique course code cannot change per heat so repeat information from match context payload)
- `courseVersion`: course content version (course version cannot change per heat so repeat information from match context payload)
- `laps`: laps per heat (laps cannot change per heat so repeat information from match context payload)
- `heatId`: unique identifier for the current heat
- `canonical`: current stored payload field for whether the heat meets regulation gameplay requirements. For V1, custom game mode alone still counts as regulation. The game sets this to `false` for gauntlet finals, reduced-lap heats, and per-heat/special rules overrides. Operator-facing UI should label this concept as `Regulation`.

### Player Loadout Payload
- `loadout`: nested loadout object with `key`, `slots`, `version`, and `augmentSlots`
- `loadoutValue`: aggregate loadout score/value
- `weight`: absolute ship/loadout weight
- `normalizedWeight`: normalized weight value
- `weightClass`: weight bucket such as `Medium`
- `playerType`: player category such as `Bot`

### Join Identity Payload
- `playerName`: The players name at the time of the join event
- `playerAvatarUrl`: The url to the players current selected avatar image 
- `playerType`: player category such as `Bot`
- `converted`: whether the joining player was converted from another identity/context

### Segment Stats Payload
- `timeMs`: elapsed time for the lap or checkpoint segment
- `numWarps`: number of warps used in the segment
- `shotsHit`: number of shots that hit another player in the segment
- `shotsFired`: number of shots fired in the segment
- `energySpent`: amount of energy spent in the segment
- `timeInAirMs`: time spent when ship isn't on the "ground"
- `averageSpeed`: average velocity of the ship through the segment
- `timeStalledMs`: time spent stalled (usually for warping)
- `numActiveStrafes`: number of times the pilot used strafe for movement in the segment
- `timeOutOfEnergyMs`: amount of time spent unable to boost or use energy-consuming actions because energy was depleted

### Death Payload
- `method`: cause of death such as `Weapon` or `WorldImpact`
- `instigatorId`: killer or impact source identifier
- `weaponItemId`: weapon identifier when relevant
- `instigatorSpeed`: Speed of the killer when it is not a static object
- `instigatorDistance`: Distance from pilot when the kill occurred

### Respawn Payload
- `spawnPoint`: spawn point identifier; sample uses `-1`

### Kill Payload
- `speed`: killer speed at the moment of kill
- `method`: kill method such as `Weapon` or `PlayerImpact`
- `distance`: distance to victim
- `victimId`: The pilot that was killed
- `victimSpeed`: The speed the pilot was going when they were destroyed
- `victimPlacement`: The current placement of the pilot before being killed
- `weaponItemId`: The weapon used to kill the pilot if not killed by vehicle
- `victimCoordinate`: nested coordinate for the victim location

### Heat Result Payload
- `kills`: Number of kills the pilot made during the heat
- `deaths`: Number of times the pilot died during the heat
- `crashes`: Number of times the pilot crashed during the heat
- `credits`: Amount of credits earned during the heat
- `obelisks`: Number of Obelisks the pilot activated during the heat
- `placement`: The pilots final placement for the heat
- `doneReason`: The reason the heat ended for the pilot 
- `doneTimeMs`: The total time the heat took the pilot in milliseconds
- `bestLapTimeMs`: The fastest lap for the pilot during the heat
- `circuitPoints`: Amount of circuit points earned during the heat
- `medalCounts`: Optional array of per-player heat medal summary entries for Eventun progression. Missing or empty means no medals are counted from the heat row.

### Match Result Payload
- `kills`: Number of kills the pilot made during the full match
- `deaths`: Number of times the pilot died during the full match
- `crashes`: Number of times the pilot crashed during the full match
- `credits`: Amount of credits earned during the full match
- `obelisks`: Number of Obelisks the pilot activated during the full match
- `placement`: The pilot's final placement for the match
- `podiumFinish`: Whether the pilot finished in a podium position
- `bestLapTimeMs`: The fastest lap recorded by the pilot during the match
- `circuitPoints`: Amount of circuit points earned during the match
- `bestFinishTimeMs`: The pilot's best completed heat finish time within the match

### Medal Count Payload
- `medalName`: primary medal name or augment medal name being counted.
- `parentMedalName`: optional parent primary medal name. Present when the row counts an augment medal under a specific primary medal context.
- `count`: positive integer number of times this medal fact occurred for the player in the heat.

### Replay Payload
- `replayRecordKey`: replay artifact key used by replay lookup and purge logic

### Unknown Payload
- No sampled rows and no stronger field evidence in the reviewed files.

## Observation Coverage
- Schema-defined event types: 18
- Observed in the reviewed 10,000-row client/server dumps: 16
- Still unobserved in the reviewed dumps: `ReplaySaved`, `PlayerMatchStart`

## Event Catalog

| Event Key | Display Name | Description | Source Tables | Payload Shape | Evidence Status |
|---|---|---|---|---|---|
| `SessionStart` | Session Start | Captures runtime environment context for the gameplay session, including client version, server mode, and matchmaking or single-player mode. | `client_event`, `server_event` | Session Context Payload | Observed in both larger dumps; `clientVersion` is queried by replay workflows. |
| `MatchStart` | Match Start | Captures the full match context, including course, race mode, heat count, and any active gauntlet qualifier bindings. | `client_event`, `server_event` | Match Context Payload | Observed in both larger dumps; server queries use `raceMode`, `courseCode`, `heats`, and `activeQualifiers`. |
| `MatchEnd` | Match End | Match-level completion marker with no observed payload beyond top-level context. | `client_event`, `server_event` | Empty Payload | Observed in both dumps. |
| `HeatStart` | Heat Start | Captures the start of a heat, repeats the active course and lap context for that heat, and carries game-authored regulation heat eligibility. | `client_event`, `server_event` | Heat Context Payload | Observed in both larger dumps; `canonical` is the current stored payload field for the regulation signal. |
| `HeatEnd` | Heat End | Heat-level completion marker with no observed payload beyond top-level context. | `client_event`, `server_event` | Empty Payload | Observed in both dumps. |
| `AscensionStart` | Ascension Start | Marks the transition into the ascension phase as a lifecycle marker with no currently observed payload fields. | `client_event`, `server_event` | Empty Payload | Observed in both larger dumps with empty payloads. |
| `ReplaySaved` | Replay Saved | Records that a replay artifact was saved for a match. | `client_event`, `server_event` | Replay Payload | Schema-defined; `replayRecordKey` is referenced by match-summary and replay purge logic. |
| `PlayerMatchStart` | Player Match Start | Marks the point where a player's match participation begins. | `client_event`, `server_event` | Unknown Payload | Schema-defined only; not present in sampled dumps. |
| `PlayerMatchEnd` | Player Match End | Captures per-player final match results used for standings, career stats, and gauntlet scoring. | `client_event`, `server_event` | Match Result Payload | Observed in both dumps and used heavily by analytics SQL. For accepted gauntlet stage completion, the dedicated server must emit this for every human participant in a normally completed match, including disconnected/DNF players. |
| `PlayerHeatStart` | Player Heat Start | Captures the player's ship, loadout snapshot, and weight profile at the start of a heat. | `client_event`, `server_event` | Player Loadout Payload | Observed in both larger dumps; server match summary joins this event for loadout details. |
| `PlayerHeatEnd` | Player Heat End | Captures per-player heat results, placement, and optional heat medal summary counts. | `client_event`, `server_event` | Heat Result Payload | Observed in both dumps and used by match summary heat standings; `medalCounts` is a planned server payload extension for Eventun progression. |
| `PlayerCheckpoint` | Player Checkpoint | Captures checkpoint-level performance and combat-efficiency telemetry during a heat. | `client_event`, `server_event` | Segment Stats Payload | Observed heavily in both dumps. |
| `PlayerJoin` | Player Join | Captures a participant entering the session with the display metadata needed to identify them in the match. | `client_event`, `server_event` | Join Identity Payload | Observed in both larger dumps. |
| `PlayerLeft` | Player Left | Captures a participant leaving the session as a pure lifecycle marker. | `client_event`, `server_event` | Empty Payload | Observed in the larger client dump; still not observed in the reviewed server dump. |
| `PlayerLap` | Player Lap | Captures lap-level performance and combat-efficiency telemetry. | `client_event`, `server_event` | Segment Stats Payload | Observed in both dumps. |
| `PlayerDied` | Player Died | Captures a player death event and the responsible cause or instigator. | `client_event`, `server_event` | Death Payload | Observed in both dumps. |
| `PlayerRespawn` | Player Respawn | Captures a respawn event and spawn-point selection. | `client_event`, `server_event` | Respawn Payload | Observed in both dumps. |
| `PlayerKill` | Player Kill | Captures a kill event from the killer perspective, including victim state and geometry. | `client_event`, `server_event` | Kill Payload | Observed in both dumps. |

## Notes
- The schema defines the tracked event set via table partitions on `server_event` and `client_event`.
- Payload observations in this note were inferred from reviewed event dumps during knowledge-base curation, but the transient inbox dump files are intentionally not cited as durable sources.
- The reviewed 10,000-row dumps still do not cover every schema-defined event, so `ReplaySaved` and `PlayerMatchStart` remain intentionally marked as unknown or unobserved.
- `player_id` is not uniformly populated in the sampled rows. The ingestion code only persists it when the sender supplies a non-empty id that is not bot-prefixed.
