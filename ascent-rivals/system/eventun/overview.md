---
id: ascent-rivals:eventun
status: current
applicability: environment-independent
---
# Eventun

Eventun is the part of Ascent Rivals that turns race and tournament activity into durable product
state. It knows which matches were accepted, how a gauntlet is progressing, what a player or team
has accomplished, and which results are safe to show to clients.

A useful way to think about it is that the game produces activity, while Eventun decides how that
activity becomes trusted competition history.

## Responsibilities

Eventun is authoritative for:

- gauntlets, stages, stage runs, qualification, admission, accepted matches, and standings;
- player and team identity within competition workflows;
- match telemetry acceptance, provenance, fact derivation, and competitive projections;
- player progression, challenges, completions, and reward intent;
- public competition reads and privileged operational controls.

Eventun does not own wallet accounting or final blockchain transitions. Those operations cross
into [Accountun](../accountun.md). AccelByte supplies player identity, sessions, service
credentials, and selected platform services described in the
[AccelByte chapter](../accelbyte-platform.md).

## Reading Guide

You do not need to read every Eventun chapter. Start with the question you are trying to answer:

| If you want to understand… | Read… |
|---|---|
| how callers reach Eventun and how requests are authenticated, validated, and answered | [How Eventun interfaces work](interface-architecture.md) |
| how Eventun uses its database and providers, records activity, applies deadlines, and shuts down | [Running Eventun](operations.md) |
| the entities Eventun stores and the projections it maintains | [Data model](data-model.md) |
| how match telemetry becomes trusted facts and serving state | [Match ingestion](identified-match-ingestion.md) |
| how a live gauntlet run admits players, locks a roster, accepts matches, and completes | [Gauntlet runtime contract](gauntlet-stage-runtime-contract.md) |
| goals, challenges, completions, and rewards | [Progression](progression.md) |
| the telemetry events and payloads produced by the game | [Event catalog](events.md) |
| teams and team gauntlets across Eventun, the game client, and web surfaces | [Team and gauntlet current state](../team-gauntlet-current-state.md) |

## Choosing The Right Chapter

Eventun knowledge is organized by the kind of question it answers:

- **How Eventun interfaces work** explains the common journey of a request. It does not enumerate
  endpoints or collect every domain rule reachable through an API.
- **Running Eventun** explains service-wide operating behavior such as resource limits,
  observability, scheduled work, and shutdown.
- **Domain chapters** explain player, team, gauntlet, progression, and ingestion behavior without
  being organized around transport methods.
- **The data model** explains stored meaning, relationships, facts, and projections. It should not
  become a catalogue of request handlers.
- **Initiatives** describe behavior that is proposed, being implemented, or not yet adopted into
  the current system.

When a new subject has enough independent behavior to teach, it should get a focused chapter. New
facts should not be added to the most recently edited file simply because that file already mentions
the same API or database table.

## Environment Boundary

The chapters in this section state their own applicability. Shared-development behavior may be
ahead of production, and accepted local implementation may be ahead of both. A source revision,
review, or initiative milestone does not by itself prove deployment.
