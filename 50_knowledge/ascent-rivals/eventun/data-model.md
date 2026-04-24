# Ascent Rivals - Eventun Data Model

## Related
- [[../overview]]
- [[overview]]
- [[api]]
- [[../competition-runtime-terms]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[../midnight]]

## Data Model Scope
This model captures operational competition knowledge across events, identity, social structures, progression, and prize/accounting bridges.

## Domain Groups

### 1. Event stream domain
Captures session, match, heat, and player lifecycle events as a durable telemetry timeline used for downstream summaries and analytics.

Runtime hierarchy:

```text
Session
  Match
    Heat
      Lap
        Checkpoint
```

Qualifiers are not part of this runtime hierarchy. Qualifiers belong to the competition-structure domain and can span multiple sessions and matches.

### 2. Identity and social domain
Captures player identity, access context, wallet linkage, team membership, join/invite state, and eligibility constraints.

### 3. Content and sponsorship domain
Captures course, sponsor, and media attachments used by competition and presentation surfaces.

### 4. Competition structure domain
Captures tournament/gauntlet structure, qualifier/stage composition, participant status, and placement outcomes used for rankings and progression.

Competition structure can bind to runtime data through match/session context, but the concepts remain distinct:

- heats are match-internal runtime units
- qualifiers are gauntlet-level time windows or qualification structures
- stages/finals/brackets are tournament structures that may allocate runtime sessions

### 5. Token metadata domain
Captures token metadata needed for entitlement and social eligibility checks.

### 6. Prize and accounting-bridge domain
Captures funding intent, distribution intent, outcomes, payout planning, receipt progression, and claim state as the operational bridge into [[../accountun]] and [[../midnight]].

## Ownership Boundary
- Eventun owns operational competition records and queryable competition state.
- [[../accountun]] owns accounting execution state transitions associated with [[../midnight]].
- Bridge fields in Eventun should be treated as operational state, not the final accounting source of truth.

## Open Questions
- What reconciliation policy governs operational bridge state versus accounting execution state?
- Which lifecycle transitions require strict idempotency guarantees at the domain boundary?
- What retention policy best balances historical analytics with storage growth?
