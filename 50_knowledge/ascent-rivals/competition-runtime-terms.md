# Ascent Rivals - Competition Runtime Terms

## Related
- [[overview]]
- [[game-design]]
- [[eventun/overview|eventun]]
- [[eventun/data-model|eventun-data-model]]
- [[eventun/events|eventun-events]]

## Purpose

This note defines core gameplay-runtime and competition-structure terms so agents and design tools do not conflate gauntlet qualifiers with in-match heats.

## Core Guardrail

A **qualifier** is not a **heat**.

They belong to different layers of the system.

- **Qualifier**: competition-structure concept
- **Heat**: gameplay-runtime concept inside a match

## Runtime Hierarchy

The gameplay-runtime hierarchy is:

```text
Session
  Match
    Heat
      Lap
        Checkpoint
```

## Competition Structure Hierarchy

The competition/tournament hierarchy is conceptually:

```text
Gauntlet
  Qualifier window(s)
  Stage(s) / Final(s) / Bracket(s)
```

The two hierarchies can be linked, but they are not the same hierarchy.

## Term Definitions

### Session

A **session** is the runtime gameplay container.

It corresponds to the server/session context in which players join and gameplay runs.

A session can contain one or more matches.

### Match

A **match** is a gameplay contest inside a session.

A match has one or more heats.

Match-level results are used for:

- player career summaries
- match history
- gauntlet scoring inputs
- analytics and recommendations

### Heat

A **heat** is a round or sub-run inside a match.

A match can have one or more heats.

Heats are gameplay-runtime units.

They are not tournament qualifiers.

Heat-level data can include:

- placement
- finish time
- best lap time
- kills
- deaths
- crashes
- credits
- obelisks
- circuit points
- loadout context

In multi-heat modes, between-heat adaptation may matter because players can adjust or upgrade between heats.

### Lap

A **lap** is a traversal unit inside a heat.

A heat can have one or more laps.

Lap-level data is useful for:

- best lap records
- consistency analysis
- execution breakdowns
- route and segment comparison

### Checkpoint

A **checkpoint** is a course-progress unit inside a lap.

Checkpoints are used for:

- tracking player progress
- determining progress order
- segment telemetry
- respawning players

Checkpoint-level telemetry can support deeper performance analysis such as where a player gained or lost time.

### Qualifier

A **qualifier** is a gauntlet/tournament structure, usually represented as a time window.

A qualifier can span multiple sessions and multiple matches.

Qualifier scoring may aggregate results across many matches using rules such as:

- Circuit Points
- best-sequence logic
- Top K qualifier rollups

A match can be associated with active qualifier ids, but that association does not make the match's heats into qualifiers.

### Stage / Final / Bracket

Stages, finals, and brackets are gauntlet/tournament structures.

They may allocate gameplay sessions for runtime execution, but they are not the same thing as matches, heats, laps, or checkpoints.

A **stage attempt** is Eventun's durable record for trying to run a stage shard. Its `stage_attempt_id` is not an AccelByte session id.

For gauntlet stage runtime:

- `stage_attempt_id` identifies Eventun's durable attempt
- `session_id` identifies the AccelByte game session and server-event session
- final accepted placement, not lobby join, is the participation signal

## UI and Design Copy Guidance

Use these labels carefully:

- Use **heat** only for a round inside a match.
- Use **qualifier** only for gauntlet/tournament qualification windows or qualification standings.
- Use **match** for a completed gameplay contest inside a session.
- Use **session** for the runtime server/session container.
- Use **lap** for repeated course traversal inside a heat.
- Use **checkpoint** for course progress and respawn segments inside a lap.

Avoid phrases such as:

- `qualifier heat`
- `heat qualifier`
- `qualifier lap`

If a UI needs to show qualification performance, say:

- `Qualifier Standings`
- `Qualifier Window`
- `Qualified for Finals`
- `Best Matches in Qualifier`

If a UI needs to show in-match breakdowns, say:

- `Heat Breakdown`
- `Heat 1`
- `Lap Times`
- `Checkpoint Splits`
