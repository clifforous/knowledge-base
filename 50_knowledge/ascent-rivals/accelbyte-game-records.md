# Ascent Rivals - AccelByte Game Records

## Related
- [[overview]]
- [[game-client]]
- [[game-design]]
- [[battle-pass]]
- [[eventun/overview|eventun]]
- [[eventun/data-model|eventun-data-model]]

## Scope
This note captures known Ascent Rivals configuration stored in AccelByte Cloud Save game records.

These records are namespace-scoped AccelByte configuration. Consumers should read them from the AccelByte namespace configured for the current environment. Eventun tables may cache, derive from, or join against this information for operational workflows, but should not be treated as the source of truth when a Cloud Save game record owns the configuration.

## Current Known Records

### `BattlePassSettings`

Current known contents:

- bonus XP awarded by player placement

This is distinct from player battle pass state. It is configuration that influences XP awards.

### `CareerMode`

Current known contents:

- list of career cups
- circuits associated with each cup
- career-mode configuration and metadata

This appears to be the source for authored career structure rather than a player progress record.

### `Courses`

Current known contents:

- official course list
- course code
- lap configuration
- feature state, where `Prod` means the course is officially released
- other course configuration

`Courses` is the source of truth for official course configuration. The Eventun `course` table is not the authoritative owner for official courses or default lap counts. As Eventun becomes more integrated with AccelByte, Eventun-side logic that needs official course configuration should prefer this AccelByte game record or a controlled cache derived from it.

### `ProgressionSettings`

Current known contents:

- multipliers for converting circuit points to XP
- multipliers for converting credits to XP
- max XP
- max player level
- difficulty scaling
- other XP and player-level progression settings

This record owns general XP and player-level tuning.

### `ShipWeightClasses`

Current known contents:

- light, medium, and heavy ship weight-class configuration
- movement-related configuration for each weight class

This record influences ship movement tuning by weight class.

## Other Known Records

The following records are known to exist, but their durable product ownership and contents have not yet been documented here:

- `CreditMetrics`
- `GameSettings`
- `GameFeatureFlags`
- `ItemRecommenderSettings`
- `LoadoutPresets`
- `MatchPools`
- `NewnessConfig`

Add details for these records when their current use is confirmed.

## Ownership Notes

- AccelByte Cloud Save game records are authoritative for the configuration listed above unless a later design explicitly moves ownership elsewhere.
- Eventun should not rely on its own `course` table as the source of truth for official course default laps or release state.
- The game client and dedicated server are expected to know whether a played heat is regulation or special-case at runtime. Eventun should use game-authored event fields for stat eligibility when available instead of reverse-engineering eligibility from stale local course data.
