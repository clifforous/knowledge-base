# Ascent Rivals - Eventun Events

## Related
- [[../overview]]
- [[overview]]
- [[api]]
- [[data-model]]
- [[identified-match-ingestion]]
- [[../competition-runtime-terms]]
- [[../game-client]]

## Scope
This note documents the event types currently tracked by Eventun and the currently observed shape of their `event_data` payloads.

## Sources
- `github.com/ikigai-github/eventun/blob/main/migration/a0_create_init.sql`
- `github.com/ikigai-github/eventun/blob/main/event/service.go`
- `github.com/ikigai-github/eventun/blob/main/event/validation.go`
- `github.com/ikigai-github/eventun/blob/main/migration/c9_func_match_facts.sql`
- [[identified-match-ingestion|Identified Match Ingestion]]
- Ascent Rivals source: `Source/AscentRivals/Public/Server/Subsystems/HGEventunServerSubsystem.h`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Subsystems/HGEventunServerSubsystem.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/HGServerScript.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Contexts/HGRaceServerContext.cpp`
- Ascent Rivals source: `Source/AscentRivals/Private/Server/Subsystems/HGStatsServerSubsystem.cpp`
- Ascent Rivals source: `Source/AscentRivals/Public/Net/HGEventunEvents.h`

## Identified Match Shape

The current producer sends one complete match from `MatchStart` through terminal `MatchEnd`.

Envelope fields:

- `batch_id`: stable non-nil UUID assigned once when MatchStart opens the envelope
- `session_id`: gameplay session UUID shared by every event
- `match_id`: nonnegative match index within the session; `0` is valid
- `game_build`: diagnostic game-build value, not a payload schema version or season
- `events`: complete event list in producer order

Event fields:

- `event_id`: stable non-nil UUID assigned when the event is recorded
- `sequence`: required zero-based list position
- `occurred_at_ms`: producer UTC Unix timestamp in milliseconds
- `event_type`: event key; `ReplaySaved` is rejected
- `heat`: optional nonnegative ambient or heat-scoped context
- `player_id`: optional canonical UUID; bots and events without a player omit it
- `progress`: `{ placement, lap, checkpoint }` when present
- `coordinate`: `{ x, y, z }` when present
- `event_data`: event-specific JSON payload

Eventun derives and persists `source_kind`, producer OAuth client, submitting player when present, receipt time, event count, bounds, and canonical SHA-256 hashes. A player subject is retained as self-reported `client` provenance. An exactly subjectless Server-authorized caller is retained as higher-trust `server` provenance. The producer cannot select this classification.

Season attribution exists only on the accepted compact `match_fact`, never on raw events or `match_player_fact`. Server facts resolve the catalog window containing MatchStart. Client facts are season-eligible only when the windows containing MatchStart and trusted batch receipt are the same non-null season; otherwise they remain unseasoned while still contributing to lifetime behavior. This policy classifies seasonal eligibility and does not validate gameplay or provide anti-cheat. Intention-specific historical derivation always leaves converted facts unseasoned.

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
- The buffer is `ActiveMatchRequest`, an in-memory `FAccelByteEventunMatchIngestRequest` whose `Events` array is appended during one active match.
- Race and server code record events through `RecordEvent`, `RecordPlayerEvent`, and `RecordParticipantEvent`.
- The templated overloads serialize Unreal `USTRUCT` payloads to the event `event_data` JSON at collection time.
- `UHGStatsServerSubsystem` owns local match statistics, medal counters, player result messages, and current AccelByte stat updates. Under the new Eventun progression contract, it is expected to supply per-player heat medal summaries for Eventun heat-end payloads. It does not submit Eventun events directly.

### Collection Behavior
- `MatchStart` initializes `ActiveMatchRequest` with a stable batch UUID, session UUID, nonnegative match index, and game build. A duplicate MatchStart for the same active match is ignored; a new match discards any stale unsubmitted envelope.
- `RecordEvent` appends one `FAccelByteEventunMatchIngestEvent`, assigns its event UUID and sequence immediately, and fills event type, occurrence time, and current ambient heat from server/session state.
- `RecordPlayerEvent` builds on `RecordEvent` and adds `PlayerId`, progress lap, placement, checkpoint, and ship coordinate when those values are available.
- `RecordParticipantEvent` builds on `RecordEvent` and fills `PlayerId`, lap, and placement from participant rows. This is used for end-of-heat and end-of-match rows when a live racer entity is not available, such as disconnected or DNF participants.
- Only canonical human player UUIDs are sent as `player_id`. Bots and invalid/absent identities serialize as the generated empty optional string, which Eventun narrowly normalizes to absence before validation and hashing.
- Events before MatchStart or after terminal MatchEnd are ignored by the identified-match producer. This means the earlier SessionStart call is not part of the current envelope.

### Primary Call Sites
- `UHGServerScript` registers `UHGEventunServerSubsystem` at server startup. Its earlier SessionStart event is outside the current MatchStart/MatchEnd envelope.
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
- `SubmitActiveMatchEvents` validates the complete local envelope, snapshots `ActiveMatchRequest`, and resets the active request before dispatching the asynchronous call.
- Dedicated-server and local/client paths both use the generated `ClientServiceIngestMatch` operation. The GameServer generated surface selects the same ClientService operation rather than defining a ServerService copy.
- If no Eventun API is available, the subsystem broadcasts failed match submission state and failed gauntlet match acceptance.
- On `ACCEPTED` or `ALREADY_ACCEPTED`, the subsystem retains Eventun's canonical response batch id, broadcasts accepted match submission state, and asks Eventun to accept the gauntlet stage-run match when a gauntlet stage run is active.
- On a rejected response or transport error, the subsystem broadcasts failed match submission state and failed gauntlet match acceptance.
- Ordinary gameplay event batches are not retained for retry after the active buffer is cleared. The current behavior is best-effort one-time submission for a completed match.
- Replay association is independent. The game submits `ClientServiceCreateMatchArtifact` after replay finalization and includes the canonical accepted batch id when available; otherwise the generated empty optional batch string is normalized to absence by Eventun.
- Gauntlet stage-run completion is separate from gameplay batch submission. Once Eventun accepts enough submitted matches for a stage run, the stage-run completion request has its own bounded retry behavior.

### Heat Context And Boundaries

- A supplied `heat` is retained telemetry context. It is not by itself evidence that an event belongs inside a heat interval.
- MatchStart may carry ambient heat 0 before the first HeatStart. PlayerMatchEnd and MatchEnd may carry the final heat after its HeatEnd. These global values are stored unchanged and do not create, count, or require a boundary.
- HeatStart, HeatEnd, AscensionStart, PlayerHeatStart, PlayerHeatEnd, PlayerCheckpoint, PlayerLap, PlayerDied, PlayerRespawn, PlayerKill, PlayerGate, and SlalomGate are explicitly heat-scoped and require a nonnegative heat.
- Only HeatStart and HeatEnd discover boundaries. Each heat has one nonoverlapping pair strictly inside MatchStart/MatchEnd; every other heat-scoped event must occur strictly inside its matching pair.
- Go validates these rules before persistence, and PostgreSQL repeats them for rebuild and direct-maintenance safety.

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
- `singlePlayerMode`: explicit canonical game enum name such as `None` or `TimeTrial`; it is not inferred from `raceMode`
- `stage`: stage index
- `gauntletId`: gauntlet identifier when the match is tied to a gauntlet
- `activeQualifiers`: gauntlet ids whose qualification windows should be evaluated for the match; Eventun resolves the applicable qualifier from MatchStart time

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

### Match Artifact

Replay association is not `event_data` and is not part of the complete match list. `CreateMatchArtifact` carries:

- `artifact_id`: stable UUID for idempotent artifact acceptance
- optional `batch_id`: Eventun's canonical accepted match batch when available
- `session_id` and nonnegative `match_id`
- `artifact_kind`: currently replay
- `external_record_key`: replay/object key
- `created_at_ms`: producer creation timestamp

### Unknown Payload
- No sampled rows and no stronger field evidence in the reviewed files.

## Observation Coverage
- The legacy source-specific schema defines 18 named event leaves, including `ReplaySaved`.
- The identified `game_event` hierarchy has 17 named leaves plus a default leaf in each source subtree. `ReplaySaved` is prohibited and uses `match_artifact` instead.
- The reviewed legacy client/server dumps observed 16 of the former 18 names; `ReplaySaved` and `PlayerMatchStart` were not observed.
- `PlayerGate` and `SlalomGate` are recognized as heat-scoped by current validation but route through the identified default event-type leaf and were not part of the reviewed legacy catalog.

## Event Catalog

The storage column describes new identified ingestion. Legacy `client_event` and `server_event` relations remain available to existing reads until serving projection cutover and deterministic historical conversion are complete.

| Event Key | Display Name | Description | Storage | Payload Shape | Evidence Status |
|---|---|---|---|---|---|
| `SessionStart` | Session Start | Captures runtime environment context for the gameplay session. The current Ascent Rivals identified producer begins at MatchStart and does not include this earlier event. | Named `game_event` leaf | Session Context Payload | Observed in both legacy dumps and retained for conversion/other producers. |
| `MatchStart` | Match Start | Captures authoritative course, race mode, explicit single-player mode, heat count, and active gauntlet qualifier bindings. | Named `game_event` leaf | Match Context Payload | Observed in both legacy dumps; current producer includes explicit `singlePlayerMode`. |
| `MatchEnd` | Match End | Terminal match marker with no observed payload beyond top-level context. | Named `game_event` leaf | Empty Payload | Observed in both dumps. |
| `HeatStart` | Heat Start | Captures a heat boundary, repeats course/lap context that must agree with MatchStart, and carries game-authored regulation eligibility. | Named `game_event` leaf | Heat Context Payload | Observed in both larger dumps; `canonical` is the stored regulation signal. |
| `HeatEnd` | Heat End | Terminal heat boundary with no observed payload beyond top-level context. | Named `game_event` leaf | Empty Payload | Observed in both dumps. |
| `AscensionStart` | Ascension Start | Marks transition into the ascension phase. It is explicitly heat-scoped. | Named `game_event` leaf | Empty Payload | Observed in both larger dumps with empty payloads. |
| `PlayerMatchStart` | Player Match Start | Marks the point where a player's match participation begins. | Named `game_event` leaf | Unknown Payload | Defined but not present in sampled dumps. |
| `PlayerMatchEnd` | Player Match End | Captures per-player final match results used for standings, career stats, and gauntlet scoring. | Named `game_event` leaf | Match Result Payload | Observed in both dumps. A normally completed trusted match must include every human participant, including disconnected/DNF players. |
| `PlayerHeatStart` | Player Heat Start | Captures the sole player/heat loadout snapshot and weight profile. | Named `game_event` leaf | Player Loadout Payload | Observed in both larger dumps; later events do not duplicate loadout state. |
| `PlayerHeatEnd` | Player Heat End | Captures per-player heat results, placement, and optional heat medal summary counts. | Named `game_event` leaf | Heat Result Payload | Observed in both dumps; `medalCounts` remains the progression input shape. |
| `PlayerCheckpoint` | Player Checkpoint | Captures checkpoint-level performance and combat-efficiency telemetry during a heat. | Named `game_event` leaf | Segment Stats Payload | Observed heavily in both dumps; detailed rows remain raw only. |
| `PlayerJoin` | Player Join | Captures a participant entering the match with display metadata. | Named `game_event` leaf | Join Identity Payload | Observed in both larger dumps. |
| `PlayerLeft` | Player Left | Captures a participant leaving the match as a lifecycle marker. | Named `game_event` leaf | Empty Payload | Observed in the larger client dump; not observed in the reviewed server dump. |
| `PlayerLap` | Player Lap | Captures lap-level performance and combat-efficiency telemetry. | Named `game_event` leaf | Segment Stats Payload | Observed in both dumps; valid-lap aggregates are projected at heat/player grain. |
| `PlayerDied` | Player Died | Captures a player death and responsible cause or instigator. | Named `game_event` leaf | Death Payload | Observed in both dumps. |
| `PlayerRespawn` | Player Respawn | Captures a respawn and spawn-point selection. | Named `game_event` leaf | Respawn Payload | Observed in both dumps. |
| `PlayerKill` | Player Kill | Captures a kill from the killer perspective, including victim state and geometry. | Named `game_event` leaf | Kill Payload | Observed in both dumps. |
| `PlayerGate` | Player Gate | Captures a heat-scoped gate event. | Default `game_event` leaf | Unknown Payload | Recognized by boundary validation; not covered by the reviewed legacy dumps. |
| `SlalomGate` | Slalom Gate | Captures a heat-scoped slalom gate event. | Default `game_event` leaf | Unknown Payload | Recognized by boundary validation; not covered by the reviewed legacy dumps. |

## Notes
- New raw telemetry is stored in `game_event`, partitioned first by actor-derived source and then by event type. Legacy `server_event` and `client_event` trees remain only for the controlled read/backfill transition.
- Payload observations in this note were inferred from reviewed event dumps during knowledge-base curation, but the transient inbox dump files are intentionally not cited as durable sources.
- `ReplaySaved` is retained only as a legacy-conversion concern. New match requests reject it and store replay association in `match_artifact`.
- `player_id` is intentionally absent for bots and non-player events. A nonempty submitted value must be a canonical non-nil UUID.
- Telemetry has no payload schema-version field. Payload changes require controlled retained-row and derived-state rewrites rather than permanent version branches.
