# Ascent Rivals - Eventun

## Related
- [[../overview]]
- [[api]]
- [[data-model]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[../midnight]]

## Role
Eventun is the central competition domain service responsible for operational tournament, player, team, and standings workflows.

## Split Notes
- Interface behavior and responsibility boundaries: [[api]]
- Domain entities and relationships: [[data-model]]
- Event catalog and payload shapes: [[events]]

## Boundary
Eventun governs operational competition state and coordinates with [[../accountun]] for accounting lifecycle transitions associated with [[../midnight]].
