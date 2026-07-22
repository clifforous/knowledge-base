# Ascent Rivals Teams Program Design

Status: T00 approved against the committed local Eventun foundation
Date: 2026-07-10
Last updated: 2026-07-21
Primary backend repository: [Eventun](https://github.com/ikigai-github/eventun)
Game repository: Ascent Rivals Unreal Engine project
Web reference repository: [Ascentun](https://github.com/ikigai-github/ascentun)

## Related

- [Delivery plan and gates](delivery-plan.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
- [[team-experience-and-progression-solution-design]]
- [[team-gauntlets-and-brackets-solution-design]]
- [[ascent-rivals/sources/analysis/eventun-team-postgresql-derivation-review]]
- [[ascent-rivals/sources/analysis/eventun-foundation-api-simplification-review]]
- [[ascent-rivals/decisions/README|Ascent Rivals decision log]]
- [[ascent-rivals/system/team-gauntlet-current-state|team-gauntlet-current-state]]
- [[ascent-rivals/system/game-client|game-client]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[ascent-rivals/system/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[gauntlet-finals-and-tournament-modes-design-review]]
- [[ascent-rivals/archive/initiatives/eventun-progression/eventun-medals-progression-goals-challenges-rewards-solution-design|progression solution design archive]]

## Purpose

This document is the program-level index for the next teams iteration. Detailed design is split into two independently deliverable workstreams:

1. [[team-experience-and-progression-solution-design|Team experience and progression]], covering team visibility, discovery, membership, notifications, cosmetics, social contribution, and shared backend foundations.
2. [[team-gauntlets-and-brackets-solution-design|Team gauntlets and brackets]], covering qualification, competition slots, runtime admission, roster replacement, results, and bracket authoring.

The split reflects different product and runtime concerns. The first workstream can ship useful team presence without waiting for tournament orchestration. The second can then reuse canonical team identity, membership history, notification delivery, and game-client team state.

## Product Goals

Teams are intended to:

- make the game more social by giving friends a durable shared identity;
- make competition easier to follow than a collection of transient individual competitors;
- include racers, friends, family, and approved fans without creating a separate persistent fan system;
- let any member attempt to contribute while limiting formal qualification to configurable top performers;
- give non-elite members meaningful participation paths without allowing large passive teams to dominate rewards or qualification.

Titles and social status do not determine skill contribution. A member described as a fan or supporter may still produce a qualifying performance. Formal stage access remains controlled separately through competition eligibility and priority.

## Original Review Baseline

The design is grounded in:

- Eventun commit `36c1818c3f9aa96d210075f7097d76a6aebbf13d`;
- Ascentun commit `589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57`;
- the current Ascent Rivals C++, configuration, generated Eventun SDK, and AccelByte SDK integrations;
- current official AccelByte Chat, Statistics, Season Pass, Challenges, Achievements, Rewards, Groups, and Extend documentation;
- a PostgreSQL review of Eventun schema, ingestion, progression workers, gauntlet queries, and materialized-view refreshes.

Since that review, the identified-match, compact-fact, incremental-serving,
qualification-cutoff, season, repair, historical-conversion, retained-data query, and runtime-
hardening work completed local implementation and review through Eventun `9213feb`. One combined
production-scale local cutover and populated API/performance smoke succeeded. The
shared-development cutover remains pending and is intentionally waiting for the next game-client
main integration. T00 approves the design against this committed local baseline. Eventun Team Core
subsequently passed implementation review and was committed as `c4260f3`; Ascentun replacement and
coordinated deployment remain pending. Affected contracts and runtime assumptions receive a narrow
reconfirmation before coordinated deployment.

## Decisions Revised During Review

| Topic | Earlier direction | Revised decision |
|---|---|---|
| Document shape | One broad solution design | Keep this file as an index and maintain two focused designs |
| Game-client administration | Create, disband, capabilities, and full roster administration in game | Keep create, disband, ownership, capability assignment, and most administration on the current website; the client focuses on viewing and member interactions |
| Membership API | Replace `AddTeamMember` with many action-specific RPCs | Keep additive transitions in one deterministic `AddTeamMember`; require exact action UUID/version for acceptance or approval, and reserve `ResolveTeamMembershipAction` for decline, deny, or cancel |
| Pagination | Require pagination for all team lists and rosters now | Defer it until measured team size or payloads require it; current iteration assumes approximately five or six members per team |
| Team progression | Commit immediately to Eventun progression tables and jobs | Define progression rules first, then select storage; AccelByte remains a candidate for player rewards but not the authoritative team entity |
| Notifications | Add an Eventun inbox and merge it with AccelByte messages | Use Eventun as the event source and AccelByte Chat system inbox/transient notifications for delivery and read state where the payload prototype proves sufficient |
| Aggregation | Maintain most derived state through Eventun asynchronous writes | Prefer PostgreSQL constraints, narrow semantic contributions, bounded views/functions, and idempotent incremental serving projections; use workers for external effects, expensive goal evaluation, and bulk repair |
| Wildcards | Model individual and team wildcard types | Model concrete competition slots with configurable allocation sources; wildcard is a policy or display label |
| Compatibility | Preserve old contracts during transition | Pre-alpha replacement is the default; remove obsolete paths and migrate or discard disposable state |
| Client verification | Broad automated game-client test plan | Use focused backend tests plus a documented manual client and visual QA matrix |
| Eventun foundation | Limit pre-teams work to local correctness fixes | Perform an incremental foundation reset: mandatory coarse Eventun permissions, current dependencies, domain packages, optional integration isolation, identified match ingestion, narrow facts, and incremental serving projections; retain the manual schema/release process and reject generic frameworks |

## Included Scope

### Shared Foundation

- Eventun remains the single authoritative team entity; the legacy game-client AccelByte Groups racing-team path is removed rather than synchronized.
- Gameplay-facing titles are separated from authorization capabilities.
- Team creation, disbanding, ownership transfer, capability assignment, and team-wide cosmetic administration remain website operations.
- Active membership gains historical validity intervals before historical progression or qualification attribution depends on it.
- Match delivery remains at most once in the current client. Stable batch ids, event ids, producer sequence, source classification, artifact association, idempotent acceptance, narrow fact derivation, fact-backed progression, serving projections, and season-aware records are implemented and locally rehearsed. T00 reapproval used that committed local foundation; the coordinated shared-development cutover remains the gate before Team Core deployment, not before isolated local implementation.
- Eventun records notification intent through an outbox and delivers through AccelByte Chat.
- The game client gains an Eventun-backed team subsystem and a shared player-relation resolver.
- Team and gauntlet read models are designed for indexed point reads, narrow contributions, incremental projections, and immutable cutoff snapshots rather than repeated scans of raw telemetry or hourly refreshes.

### Team Experience And Progression

- green teammate minimap markers visible throughout a race;
- optional teammate-specific bounty-beam color instead of the default yellow;
- richer team identity in lobbies, profiles, pre-race presentation, spectator views, and post-match surfaces;
- game-client team views and gamepad-first browsing; text search is optional last-mile work;
- join and leave for open teams;
- team invitations, acceptance, and decline; closed-team join requests remain design-gated until an approval flow is confirmed;
- public team-filtered leaderboard and roster statistics;
- Twitch or Discord watch links;
- region, time-zone, and recruiting metadata on the website;
- optional team affiliation plus fixed border/decal cosmetic ownership, administration, and member presentation preferences; course flags remain a later experiment;
- team notifications through existing inbox and popup surfaces;
- team challenges, XP, levels, capped participation, and cosmetic unlocks after the progression definition gate.

### Team Gauntlets And Brackets

- configurable team qualification using top N member scores;
- fixed per-team racer caps represented as concrete stage-run slots;
- team-owned and player-owned slots from qualification or explicit assignment;
- manager rank, qualification rank, first-come, or threshold admission policies;
- higher-priority pre-lock replacement where configured;
- mixed individual and team-qualified fields;
- optional unaffiliated-player fills;
- community or sponsored team allocations without a separate wildcard data model;
- explicit bracket positions, seeds, byes, upstream result routing, manual setup, repair, and visualization.

## Deferred Scope

- event-level rooting or persistent fan state;
- team-specific custom-game modes;
- dedicated spectator, shoutcaster, or coach stage slots;
- asymmetric racer and supporter gameplay;
- a team activity feed;
- token-gated team joins in the game client;
- large-team pagination and search redesign;
- team media upload from the game client, which is not planned; team avatar upload remains website-only;
- public team matchmaking queues;
- compatibility adapters for obsolete pre-alpha contracts.

The pre-foundation reset removed the TapTools/Koios-shaped token catalog and team gate. Token gating is unsupported and may return only through a separately designed provider-neutral asset source.

## Ownership Boundaries

| System | Responsibilities |
|---|---|
| Eventun | Team identity and membership, transition rules, capability checks, progression and competition facts, qualification snapshots, concrete stage slots, bracket state, audit, and notification intent |
| PostgreSQL | Transactional invariants, membership history, narrow facts, incremental serving projections, slot and bracket state, immutable snapshots, and durable outbox or work queues |
| AccelByte | Authentication, player-scoped Statistics and Season Pass state, reward fulfillment, Chat system inbox and transient delivery, parties, sessions, and other existing platform services |
| Game client | Team browsing and member interactions, cached Eventun team state, HUD relation presentation, cosmetic preferences, conditional reuse of existing party invite behavior, notification rendering, and read-only competition views |
| Dedicated server | Serialized live seat occupancy, configured pre-lock replacement, start lock, trusted roster and result reporting |
| Ascentun | Minimal website administration required for teams, capabilities, team-wide cosmetics, and gauntlet or bracket authoring |
| Eventun Extend App UI | Admin-only progression definitions, diagnostics, projection repair, and operational tooling |

## Data Architecture Direction

The target is a database-first hybrid, not a database-only system:

1. The implemented foundation adds identified complete-match batches, one source-tagged `game_event` relation, stable event ids and sequence, and physical source/event-type partitions. Legacy `server_event` and `client_event` reads remain only until the pending shared-development cutover. Automatic sender retry remains a separate behavior change.
2. Implemented synchronous derivation produces narrow match, heat, match-player, heat-player, progression-contribution, and qualification-serving facts plus revisioned individual cutoff evidence and season-aware record projections. Detailed lap/checkpoint telemetry remains in raw partitions.
3. Authoritative state uses ordinary tables and constraints for membership intervals, XP ledgers, unlock grants, stage slots, bracket matches, and snapshots.
4. Ordinary views and stable SQL functions calculate aggregates whose input is bounded by team, configured top N, stage field, or another explicit product limit.
5. Incrementally maintained ordinary projection tables serve fresh record, career, progression, and gauntlet reads whose direct cost grows with retained history. The former native player-facing materialized views are retired; future offline materialization would require a separate measured use case.
6. Workers handle external delivery, reward fulfillment, notification delivery, expensive goal evaluation, and bulk projection repair/backfill.

The sub-16 ms objective applies to measured hot database operations, not end-to-end calls through AccelByte or the public service. See [[ascent-rivals/sources/analysis/eventun-team-postgresql-derivation-review]].

## Delivery Sequence

### Phase 0: Correctness Foundations

The local foundation and rehearsal now include:

- authenticated client identity, mandatory auth, namespaced player ClientService access, and coarse Eventun Server/Admin permissions;
- explicit transaction ownership is used for read-decide-write commands, while pure write batches check `BatchResults.Close()`;
- the canonical clean schema plus one manually applied pending delta, with independent development fixtures outside automatic clean initialization and no numbered production migration series;
- dependency/toolchain and package-layout cleanup is complete through the scoped foundation passes;
- Accountun and Cardanoun proof-of-concept adapters are isolated, while Eventun's TapTools, Koios, and token-gating runtime/schema/API slice is removed;
- identified, idempotent complete-match ingestion, source/event-type partitions, artifacts, synchronous narrow facts, incremental serving projections, individual cutoff snapshots, and season-aware records;
- ClientService authentication, the five ServerService gauntlet runtime methods, twelve shared
  reads, two shared writes, full served/Admin Swagger, and split Unreal Client/GameServer/Models
  generation are implemented. The generated GameServer subset remains at the original ten
  dedicated-server reads.
- one accepted production-scale local historical-and-season cutover, a resettable migrated snapshot, populated API smoke, and representative retained-data query-plan evidence.

Remaining Phase 0 work before deploying the approved team slice:

- wait for the accepted game-client API changes to complete their next copy to main, then apply and validate the coordinated Eventun transition in shared development;
- treat the committed local runtime-hardening contract as the T00 baseline and reconfirm it during the coordinated shared-development cutover before Team Core deployment or production release;
- remove Ascentun's stale disabled token-gating types, dormant actions, and generated API contract during the coordinated contract refresh; its active forms already filter that mode out;
- retain production as a separate unscheduled owner decision after a shared-development soak period.

Membership intervals, notification delivery, and removal of the legacy AccelByte Groups team
source are team-foundation implementation work selected through T00; they are not prerequisites
for performing the design refresh itself. See the [delivery plan](delivery-plan.md) and
[foundation prerequisite plan](../eventun-foundation/development-cutover-and-runtime-hardening.md).
Production deployment is not a prerequisite for T00. Do not expand the reset into an ORM,
migration runner, CI service, generic repository layer, wholesale package relocation, or
unrelated product rewrite.

### Phase 1: Game-Client UI Baseline

- complete this phase before adding the T05 game-client routes; it does not gate the backend and
  existing-website Team Core cutoff;
- capture current game-client screens at target desktop resolutions;
- map routes and route transitions from configuration, C++, Blueprints, and available asset tooling;
- capture each route's widget/component tree and responsive slot properties in a separate Ascent Rivals project task with MCP access;
- reproduce the current navigation hierarchy in Pencil.dev;
- annotate motion and state transitions separately where static boards are insufficient;
- identify reusable views before designing new ones.

### Phase 2: Team Presence And Views

- add the Eventun-backed team subsystem and relation resolver;
- implement minimap and bounty-beam treatments;
- add team discovery, team detail, roster, profile, lobby, and race presentation;
- retain full-roster responses and client filtering for current scale.

### Phase 3: Membership, Notifications, And Cosmetics

- consume the typed, atomic Eventun `AddTeamMember` and exact-action resolution contract;
- support open joins, closed-team request and invitation flows, and leave; add team-to-party invitation only if the existing path requires no party-system changes;
- deliver actionable team messages through AccelByte Chat;
- add team cosmetic definitions, team administration, and member per-surface choices.

### Phase 4: Progression

- approve the progression product definition;
- implement contribution facts, caps, team XP or levels, durable cosmetic grants, and team challenges;
- use the Eventun Extend App UI for progression administration;
- use existing Eventun and AccelByte fulfillment paths only for configured player rewards.

### Phase 5: Team Qualification And Runtime Slots

- implement top-N team qualification and immutable cutoff snapshots;
- resolve individual-owned and team-owned slots;
- add point-read admission APIs and dedicated-server occupancy replacement;
- lock and persist the actual starting roster.

### Phase 6: Brackets

- make results stage-run scoped;
- add explicit bracket matches and positions;
- support manual authoring, seeding, byes, advancement, repair, and player-facing visualization.

## Cross-Workstream Gates

| Gate | Required before |
|---|---|
| Canonical Eventun team state in the client | Team menus, live relations, conditional existing-path party invites, and team competition client views |
| Membership intervals | Historical team progression or qualifier attribution |
| Complete-match facts and membership intervals | Durable progression calculations and authoritative qualification snapshots |
| Notification outbox and payload prototype | Closed-team actions and progression notifications |
| Approved progression definition | Team XP, levels, caps, and unlock implementation |
| Compact match and qualification facts | Low-latency standings and cutoff resolution |
| Stage-run-scoped result key | Multiple bracket matches using the same gauntlet stage |
| Concrete slot model | Mixed qualification sources and runtime team seat enforcement |

## Current Review Order

1. Review [[team-experience-and-progression-solution-design]] and answer its product, cosmetic, notification, and progression questions.
2. Treat the approved Team Core backend/existing-website cutoff, data disposition, roster limit,
   disband identity, capabilities, and public-read IAM as the first implementation contract.
3. Establish the Pencil.dev baseline before the later T05 game-client slice.
4. Review [[team-gauntlets-and-brackets-solution-design]] independently before gauntlet implementation begins.
5. Turn approved sections into implementation plans with repository-specific migrations, APIs, UI tasks, and verification steps.

Unresolved decisions are intentionally kept in the two focused designs rather than duplicated here.
