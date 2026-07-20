# Ascent Rivals - Eventun

## Related
- [[../overview]]
- [[api]]
- [[data-model]]
- [[progression]]
- [[identified-match-ingestion]]
- [[gauntlet-stage-runtime-contract]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[../midnight]]

## Role
Eventun is the central competition domain service responsible for operational tournament, player, team, and standings workflows.

## Split Notes
- Interface behavior and responsibility boundaries: [[api]]
- Domain entities and relationships: [[data-model]]
- Current player progression, challenges, and rewards: [[progression]]
- Event catalog and payload shapes: [[events]]
- Identified telemetry ingestion, derivation, cutover, and recovery contract: [[identified-match-ingestion]]
- Gauntlet stage runtime rules and DS/client contract: [[gauntlet-stage-runtime-contract]]
- Current team-gauntlet implementation facts and gaps: [[../team-gauntlet-current-state]]

## Boundary
Eventun governs operational competition state and coordinates with [[../accountun]] for accounting lifecycle transitions associated with [[../midnight]].
