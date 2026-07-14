# Ascent Rivals Team Gauntlets And Brackets Solution Design

Status: Solution design draft
Date: 2026-07-10
Last updated: 2026-07-12
Program index: [[teams-solution-design]]
Primary backend repository: [Eventun](https://github.com/ikigai-github/eventun)
Web reference repository: [Ascentun](https://github.com/ikigai-github/ascentun)

## Related

- [[team-experience-and-progression-solution-design]]
- [[../../50_knowledge/ascent-rivals/team-gauntlet-current-state|team-gauntlet-current-state]]
- [[../../50_knowledge/ascent-rivals/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[../../10_research/ascent-rivals/eventun-team-postgresql-derivation-review]]
- [[../../10_research/ascent-rivals/eventun-foundation-api-simplification-review]]
- [[gauntlet-finals-and-tournament-modes-design-review]]
- [[gauntlet-stage-client-entry-plan-2026-05-07]]
- [[gauntlet-stage-orchestration-improvements]]
- [[website/pages/gauntlet-detail|gauntlet-detail]]

## Purpose

Extend one gauntlet model so it can support:

- individual qualification and individual racer slots;
- team qualification and team-controlled racer slots;
- explicit sponsored player or team slots;
- mixed allocation sources;
- configurable pre-lock team roster priority;
- multiple stage runs connected through a visible and repairable bracket.

The design avoids separate “individual wildcard” and “team wildcard” systems. A wildcard is a policy or display label on an ordinary slot allocation.

## Goals

- Keep individual and team tournaments structurally cohesive.
- Represent every racer seat as a concrete entitlement before runtime admission.
- Allow a qualified team to send one or more eligible racers without granting unlimited seats.
- Let a lower-priority member hold a provisional seat until a higher-priority member arrives when the configured policy permits replacement.
- Preserve first-come behavior as another explicit policy.
- Calculate qualification through compact PostgreSQL facts and freeze selection at a cutoff.
- Make every bracket match and follow-on path visible after the initial field is settled.
- Support manual authoring and repair even when automatic seeding is available.
- Keep current Ascentun changes minimal and operational.

## Non-Goals

- event-level rooting;
- spectator, shoutcaster, or coach slots;
- team-specific gameplay modes;
- asymmetric racer/supporter mechanics;
- persistent fan state;
- a full v2 tournament website redesign;
- compatibility with disposable pre-alpha gauntlet rows or obsolete APIs;
- automatic player registration for team slots in the first slice unless selected during question review.

## Confirmed Current State

### Existing Useful Foundations

- Gauntlets already define qualification periods and calculate player qualification points from each player's best configured performances.
- Stage configuration already contains `players_per_team`, allowed teams, overflow policy, priority, and roster-lock concepts.
- `UHGGauntletSubsystem` already supports the player-oriented calendar, standings, active-session discovery, Eventun join preflight, and exact-session joining.
- The dedicated server already asks Eventun whether a player may join a gauntlet stage.
- Stage match and accepted-result writes already use a useful transaction boundary that can be extended.
- Stage runs already have a `shard_key` field.

### Gaps Requiring Change

| Current behavior | Why it is insufficient |
|---|---|
| `players_per_team` and `team_player.rank` exist but are not enforced during admission | A team can be eligible without having a bounded racer-seat entitlement |
| Dedicated-server claim, admission, match acceptance, and completion RPCs have moved to `ServerService`, while ten existing reads remain on `ClientService` with an alternate Server `READ` policy | Generated GameServer input must select those two existing surfaces without duplicating the Client read APIs or admitting Admin operations/models |
| `gauntlet_stage_team` acts as an allowed-team filter | Eligibility alone does not say how many slots a team owns or how those slots were earned |
| Admission computes broad `gauntlet_stats` and then finds one player | Runtime admission should be an indexed point read against a frozen field |
| Dedicated server uses the allowed response but does not replace a lower-priority occupant | Manager rank or qualification priority cannot control a full team allocation |
| “match started” is primarily local server state | Eventun does not own an authoritative roster lock or actual starting roster |
| Stage runs are created with a primary shard in the reviewed path | A bracket needs multiple distinct runs for one logical stage |
| `gauntlet_stage_placement` includes `stage_run_id` but its primary key is gauntlet, stage, player | Multiple bracket matches in the same stage cannot persist independent accepted placements |
| Bracket configuration is limited to required prior wins and losses | It cannot express seeds, high-versus-low pairing, byes, explicit assignments, or visible upstream routing |
| Hourly materialized-view refresh underlies existing qualifier reads | It is too stale and too rebuild-oriented to be the authoritative cutoff mechanism |

## Terminology

Use the following terms consistently:

| Term | Meaning |
|---|---|
| Allocation rule | Authoring rule that selects slot owners, such as top 14 players, top 2 teams by Community CP, or an explicit sponsored team |
| Slot owner | The player or team that earned or was assigned an entitlement |
| Racer slot | One concrete player seat in one stage run |
| Occupant | The player currently using a racer slot |
| Qualified owner | A player or team selected by a qualification rule at a frozen cutoff |
| Roster policy | Rules that determine which team members may occupy team-owned slots and their priority |
| Roster lock | Point after which provisional occupancy becomes the accepted starting roster |
| Bracket position | One side of a bracket match, sourced from a seed, explicit owner, bye, or upstream result |

Do not use “entry” as a public API synonym for both a competition owner and a racer seat. An owner may have one or more racer slots; a slot has at most one locked occupant.

## Cohesive Competition Model

### Owner And Slot Expansion

All selection paths have the same two stages:

1. An allocation rule resolves one or more owners.
2. Each owner expands into the configured number of concrete racer slots.

Examples:

| Rule | Resolved owners | Racer slots |
|---|---|---|
| Top 14 individual qualification points | 14 players | One player-owned slot per player |
| Top 2 teams by Community CP | 2 teams | One or more team-owned slots per team |
| Explicit sponsored streamer | 1 player | One player-owned slot |
| Explicit community-selected team | 1 team | Configured number of team-owned slots |
| Bracket winner | Upstream player or team owner | Same configured slot count for that owner |

“14 individual plus 2 community team slots” and “14 team slots plus 2 individual slots” are therefore configuration, not separate tournament types.

### Individual Competition

- Owner type is player.
- Each selected owner normally receives one racer slot.
- Only that player may occupy the slot.
- Qualification and bracket result are player-scoped.

### Team Competition

- Owner type is team.
- Each selected owner receives `slots_per_owner` racer slots.
- Eligible current or registered team members may occupy those slots.
- Admission policy determines priority and pre-lock replacement.
- Team result groups slot results by owner.

### Mixed Competition

A stage may contain player-owned and team-owned slots if the author explicitly configures both. The runtime seat model remains valid. Whether a player owner may compete directly against a team owner in one bracket depends on the scoring policy and remains an explicit design decision.

## Allocation Rules

### Candidate Rule Shape

| Field | Purpose |
|---|---|
| `allocation_rule_id` | Stable authoring identity |
| `gauntlet_id` and `stage` | Target stage |
| `source_type` | Individual qualification, team qualification, explicit player, explicit team, bracket advancement, or unaffiliated fill |
| `metric_definition_id` | Qualification metric where applicable |
| `owner_count` | Number of player or team owners selected |
| `slots_per_owner` | Concrete racer slots granted to each owner |
| `selection_order` | Tie-break and precedence among rules |
| `display_label` | Optional “wildcard,” “community,” “sponsor,” or other presentation label |
| `cutoff_policy` | Snapshot time and late-correction behavior |
| `fallback_policy` | Vacant, next owner, unaffiliated fill, or operator assignment |

An explicit rule stores its selected owner separately. A qualification rule stores its metric and selection policy rather than a hand-entered owner.

### Supported Source Types

| Source | Use |
|---|---|
| `INDIVIDUAL_QUALIFICATION` | Top players by the existing qualification scoring model |
| `TEAM_QUALIFICATION` | Top teams by a configured team score, including Community CP |
| `EXPLICIT_PLAYER` | Sponsored player, streamer, operator invitation, or manual repair |
| `EXPLICIT_TEAM` | Community-selected, sponsored, or operator-selected team |
| `BRACKET_ADVANCEMENT` | Winner, loser, or placement from an upstream bracket match |
| `UNAFFILIATED_FILL` | Optional fallback from eligible players who do not belong to already represented teams |

Wildcard should not be a `source_type`. It may be the `display_label` or the event's name for one of these allocations.

## Qualification

### Player Score

The existing player scoring principle remains:

1. calculate each player's accepted performance score;
2. retain that player's best configured N performances;
3. sum or otherwise apply the configured gauntlet metric;
4. rank players with deterministic tie-breakers.

This prevents one player from accumulating unlimited score merely through volume.

### Team Score

For a team qualification rule:

1. attribute each accepted player fact to the membership interval active at trusted event time;
2. calculate the member's score using the same best-performance rule used by individual qualification;
3. rank members within each team;
4. take the configurable top N member scores;
5. aggregate those scores into the team score;
6. retain the contributing-member breakdown;
7. rank teams using deterministic tie-breakers.

Top N is configuration, not a hard-coded product constant.

### Database Execution

Qualification should operate over narrow immutable match-player contributions and incrementally retained player/qualifier sequence state, not rescan raw telemetry or refresh full-history materialized views on every update.

Recommended layers:

- `match_player_fact` or equivalent accepted performance facts;
- source/trust provenance on every performance fact so qualification policy can distinguish dedicated-server and client-reported results;
- an indexed incremental player qualification contribution and best-sequence projection by gauntlet, qualifier, and player;
- a SQL team score function or view using `row_number() over (partition by team_id order by member_score desc)`;
- an immutable cutoff snapshot containing selected owners, rank, score, tie-break values, and contributing members;
- a snapshot version and configuration hash for reproducibility.

Ordinary views or stable functions remain appropriate for team top-N calculations over an already bounded player-score projection. The player/qualifier score and retained best sequence should update incrementally after each accepted match so standings do not inherit the current hourly delay. Native materialized views are transitional only and must not determine the final field.

Client-reported performance remains necessary for time-trial or local qualification modes, but it can be altered by a hostile client. A qualifier must not silently combine client-reported and dedicated-server performance as though they have equal authority. The permitted source policy is a qualifier/competition decision and should be retained in the cutoff snapshot. Lightweight client-event validation is deferred; full dedicated-server replay is not the assumed solution.

### Cutoff And Correction

At cutoff:

1. acquire a resolver lock for the gauntlet and stage;
2. record the telemetry watermark and configuration version;
3. calculate all allocation rules from current incremental qualification projections and their narrow source contributions;
4. persist owner snapshots and contributor breakdowns;
5. expand owners into stage-run racer slots;
6. record unresolved deficits and applied fallback rules;
7. publish the field atomically.

A delayed complete-match batch or rewritten historical fact does not silently mutate a published field. An operator may run a recomputation before the roster-lock deadline, review the delta, and publish a replacement snapshot. After the deadline, correction requires an explicit repair decision and audit.

## Racer Slots

### Concrete Slot Shape

Each stage-run racer slot should contain:

| Field | Purpose |
|---|---|
| `stage_run_slot_id` | Stable slot identity |
| `stage_run_id` | Runtime match or heat |
| `slot_index` | Stable display and session ordering |
| `allocation_rule_id` | Why the slot exists |
| `owner_type` and `owner_id` | Player or team entitlement |
| `qualification_snapshot_id` | Frozen qualification source, if any |
| `display_label` | Community, sponsor, wildcard, seed, or other label |
| `occupancy_policy` | First-come or replace-by-priority |
| `eligibility_policy` | Current member, explicit roster, threshold, or another approved rule |
| `lock_state` | Open, locked, completed, void |

Before lock, live occupant state is owned by the dedicated server. At lock, Eventun persists one occupant per slot and the roster version.

### Multiple Slots Per Team

If a team has two racers, it receives two separate team-owned slots. The dedicated server fills those slots from one eligible member pool. A player may occupy at most one slot in the run.

This directly enforces fairness: team size changes the candidate pool, not the number of seats.

### Explicit Owners

- An explicit player slot is occupied only by that player.
- An explicit team slot follows the same roster policy as a qualified team slot.
- A later registration feature may pin a team slot to a selected player before runtime.
- The first slice may let the team choose implicitly by which eligible members join and survive priority replacement.

## Admission And Dedicated-Server Occupancy

### Runtime Admission Read

Replace broad standing evaluation with an indexed request:

```text
GetStageRunAdmission(stage_run_id, player_id)
```

The response should contain:

- allowed or denied with a typed reason;
- matching player-owned or team-owned slot ids;
- owner type and id;
- eligibility basis;
- priority value and tie-break data;
- occupancy policy;
- roster-lock state and version;
- stage and session identity needed for validation.

Eventun determines entitlement and priority from frozen slot state plus current approved roster data. It does not reserve a provisional live seat for every join attempt.

### Occupancy Algorithm

The dedicated server serializes admission for one stage run:

1. Reject if the Eventun response is denied or the roster is locked.
2. For a player-owned slot, accept only its owner if unoccupied.
3. For team-owned slots, reject if the player already occupies another slot.
4. If the owner has a free slot, assign it to the player.
5. If all owner slots are occupied and policy is first-come, reject the newcomer.
6. If policy is replace-by-priority, compare the newcomer with the lowest-priority current occupant.
7. Replace only when the newcomer is strictly higher priority; the incumbent wins ties.
8. Eject the displaced player from the racer seat and communicate the reason.
9. Re-evaluate occupancy after disconnects until lock.

Because one dedicated server owns the live lobby, it can make this decision without a distributed Eventun reservation for each provisional join. Eventun remains authoritative for eligibility and persists the final lock.

### Session Connection Capacity

Replacement cannot work if the AccelByte session rejects a higher-priority newcomer before the dedicated server sees them. When replace-by-priority is enabled, distinguish platform connection capacity from racer-slot capacity:

- configure a small bounded admission buffer above the concrete racer-slot count;
- place a newly connected candidate in a non-racing pending state while admission is evaluated;
- assign a slot and eject the displaced occupant as one serialized server operation;
- never treat buffered connections as extra racer or spectator slots;
- close replacement admission at roster lock and retain only the explicit reconnect policy.

If the buffer is exhausted, client preflight may explain that the player has higher priority, but it cannot guarantee immediate connection. The implementation plan must verify how current AccelByte session capacity and the dedicated-server join callbacks interact before finalizing the buffer size.

### Priority Policies

The stage selects one policy:

| Policy | Behavior |
|---|---|
| `FIRST_COME` | Eligible occupants retain seats until disconnect or lock |
| `TEAM_COMPETITION_RANK` | Lower manager-assigned rank number has higher priority; null may be ineligible |
| `QUALIFICATION_RANK` | Higher member qualification score or rank has priority |
| `QUALIFICATION_THRESHOLD` | Members must meet a configured threshold; ties use arrival |
| `EXPLICIT_ROSTER` | Only manager-registered players may join, in configured order |

Do not combine all policies implicitly. If composite priority is required, author and return an explicit ordered tuple.

### Provisional Seat UX

Before roster lock, a team-owned seat may be provisional:

- the join screen should state the active policy;
- a lower-priority occupant should be told that a higher-priority teammate may replace them;
- replacement should show the team slot and reason;
- no replacement occurs after lock;
- conversion to spectator is not assumed because dedicated spectator slots are deferred.

## Roster Lock

The first match start or another configured deadline locks the roster:

1. Dedicated server pauses new admission decisions.
2. It submits the actual slot-to-player map with the last observed roster version.
3. Eventun validates owner, eligibility, uniqueness, capacity, and stage-run state.
4. Eventun atomically records occupants, locks all slots, and opens the match result transaction.
5. Dedicated server starts the race only after lock acknowledgement.

The current local-only “mark started” behavior should be replaced by this contract. On timeout, the server should fail closed for formal finals unless an explicit operator bypass policy exists.

## Disconnects And Substitution

Before lock, a disconnected occupant releases the provisional slot. After lock, substitution changes competition integrity and requires an explicit policy:

- no substitution;
- substitution before the first scored heat;
- substitution from a registered alternate list;
- operator-approved repair.

The initial recommendation is no automatic post-lock substitution. Persist disconnect and no-show facts for operator review.

## Results

### Stage-Run Scope

All accepted placements and result uniqueness must include `stage_run_id`. The current stage-level primary key must be replaced before multiple bracket matches share a logical stage.

Recommended result layers:

| Layer | Purpose |
|---|---|
| Slot result | Locked occupant's accepted score, placement, finish state, and source match |
| Owner result | Player result or configured aggregation across a team's slots |
| Stage-run result | Accepted ordering of owners in one heat or match |
| Bracket advancement | Upstream owner routed to downstream bracket positions |

### Team Result Policy

One racer per team is straightforward: the slot result is the team owner result.

Multiple racers per team require an explicit policy such as:

- best finishing member;
- sum of placement points;
- sum or average of best lap times;
- first N finishers;
- heat wins across several matches.

The schema stores slot facts independently so the owner aggregation can be configured and reproduced. No default should be inferred silently.

### Transaction Boundary

When a stage run completes, one transaction should:

1. validate the locked roster and submitted match identity;
2. persist immutable slot results;
3. calculate and persist owner results;
4. mark the stage run complete;
5. resolve affected bracket positions;
6. create or activate downstream runs when both positions are ready;
7. append notification and session-allocation work to outboxes.

External session creation and player notification remain worker responsibilities. Result acceptance and bracket advancement remain synchronous database state.

## Bracket Model

### Entities

| Entity | Purpose |
|---|---|
| `gauntlet_bracket` | Bracket identity, format, publication state, and version |
| `gauntlet_bracket_match` | One matchup mapped to one stage run |
| `gauntlet_bracket_position` | Left or right side and its owner source |
| `gauntlet_bracket_advancement` | Auditable resolved routing from an upstream result |

Each bracket match receives a distinct non-primary `stage_run.shard_key`. A bye resolves a downstream position without creating or running an empty match.

### Position Sources

- explicit player owner;
- explicit team owner;
- qualification seed;
- winner of upstream match;
- loser of upstream match;
- owner at a configured upstream placement;
- bye.

### Automatic And Manual Authoring

Automatic generation may support:

- high seed versus low seed;
- standard single-elimination seed ordering;
- byes for high seeds when the field is not a power of two.

Manual editing is still required:

- assign or swap owners;
- add or remove a bye;
- change an unresolved upstream source;
- void and replay a run;
- repair an incorrectly advanced result;
- republish a corrected bracket version.

Edits after an affected run starts require void or repair workflow and audit. Direct silent mutation is prohibited.

### Publication

Publish the bracket after the initial field snapshot and manual review:

- player-facing reads show every match, seed, owner, label, bye, and upstream path;
- unresolved positions show their source, such as “Winner of Match 3”;
- later advancement updates the same graph;
- the graph remains readable before all downstream owners are known.

## APIs

Names are conceptual and should be reconciled with the existing proto style.

### Player And Public Reads

- get individual and team qualification standings with contributor breakdown where public;
- get published stage field and slot labels;
- get bracket graph and match status;
- get current player's admission status and priority explanation;
- get locked roster and accepted results.

### Operator Mutations

- configure allocation rules and roster policy;
- preview a cutoff;
- publish or replace a qualification snapshot;
- assign explicit player or team owners;
- generate, edit, publish, void, and repair a bracket;
- inspect unresolved deficits and projection watermarks.

### Dedicated-Server Operations

- point-read player admission;
- lock actual stage-run roster;
- submit match and slot results;
- report disconnect or no-show facts where required;
- retrieve an authoritative stage-run snapshot for recovery.

All mutations require idempotency keys or natural unique keys and return versioned state.

## Website Changes

Keep Ascentun modifications limited to operational needs:

- author allocation rules, owner counts, slots per owner, qualification metric, and fallback policy;
- configure top N team contributors;
- configure team roster eligibility, priority, and lock policy;
- preview and publish the resolved field;
- assign explicit players or teams;
- generate and manually edit the bracket;
- view run state and perform audited repair.

Reuse the existing gauntlet create/detail flows. Do not redesign unrelated team search, add site-wide pagination, or build the future v2 competition presentation here.

## Game-Client Changes

- extend standings to distinguish player and team owners;
- show why a slot exists, including community or sponsor labels;
- show team qualification score and contributing top N members where appropriate;
- update join preflight to explain team eligibility, priority, provisional status, replacement, and lock;
- render locked team rosters;
- render the published bracket graph and unresolved upstream paths;
- refresh after AccelByte inbox messages or Eventun state-change notifications;
- preserve exact-session joining through the existing gauntlet subsystem.

The client does not author allocation rules or brackets.

## Database And Performance Direction

- Derive qualifier facts from accepted complete-match batches and key them by session, match, and player.
- Attribute performance through membership validity intervals.
- Use narrow match-player contributions and indexed incremental qualification dimensions.
- Resolve and snapshot fields in PostgreSQL transactions.
- Keep stage slot, roster lock, result, and bracket advancement constraints in PostgreSQL.
- Use ordinary views or stable SQL functions for bounded team top-N and allocation calculations.
- Maintain player/qualifier contributions and retained best sequences incrementally after accepted matches, with targeted recomputation for late or rewritten input.
- Treat native materialized views as transitional or offline-only and remove current gauntlet dependencies after output and freshness parity.
- Use workers only for external session allocation, notification delivery, reward delivery, and repair or backfill.

Target measured hot database reads are p95 below 5 ms for runtime admission and below 10 ms for standings or bracket reads, with p99 below 16 ms where the deployed PostgreSQL tier permits. These are database execution goals, not end-to-end AccelByte service goals.

## Delivery Slices

### Slice G0: Correctness Foundation

- consume the separated Eventun boundary: dedicated-server runtime RPCs live in `ServerService`; the generated GameServer view selects ten authorized Client reads plus all five Server operations; Models contain the full Client+Server union; and the complete served/Admin Swagger remains separate;
- explicit complete-match derivation state where needed;
- membership validity intervals;
- narrow accepted performance contributions and incremental qualification projections;
- queue lease, retry, and dead-letter behavior;
- stage-run-scoped placement key.

### Slice G1: Allocation And Team Qualification

- allocation rule schema;
- player and top-N team scoring;
- cutoff preview and immutable snapshots;
- concrete player-owned and team-owned slots;
- minimal Ascentun authoring.

### Slice G2: Runtime Admission

- indexed point-read admission;
- priority and eligibility policies;
- dedicated-server provisional occupancy and replacement;
- actual roster lock and recovery;
- game-client admission explanations.

### Slice G3: Mixed And Explicit Allocations

- explicit player and team owners;
- community, sponsor, and wildcard display labels;
- fallback or unaffiliated fills;
- operator repair.

### Slice G4: Brackets

- explicit graph and stage-run shards;
- owner results;
- automatic seeding and byes;
- manual editor and repair;
- player-facing visualization and advancement.

## Verification

### Database And Service

- complete-match transaction, missing-submission, delayed-batch, and rebuild tests;
- membership-at-event-time tests;
- top-N member and tie-break property tests;
- immutable cutoff reproducibility tests;
- concurrent resolver and publish tests;
- one-owner/multiple-slot constraint tests;
- admission point-read benchmarks with realistic current and future stress datasets;
- roster-lock conflict and idempotency tests;
- stage-run-scoped result uniqueness tests;
- bracket graph validation, bye, advancement, void, and repair tests;
- `EXPLAIN (ANALYZE, BUFFERS, WAL)` and `pg_stat_statements` evidence on the deployed PostgreSQL major version and representative tier.

### Dedicated Server And Client

Use a manual multiplayer matrix for:

- individual-owned and team-owned slots;
- one and multiple slots per team;
- first-come and replace-by-priority;
- lower-priority first arrival followed by higher-priority replacement;
- equal priority;
- disconnect before lock;
- join during lock;
- Eventun timeout or version conflict;
- field labels and admission reasons;
- bracket paths, byes, unresolved owners, and completed advancement.

Automated game-client tests are not required for this iteration. Backend and dedicated-server logic should have focused unit or integration coverage where the harness permits it.

## Risks

| Risk | Mitigation |
|---|---|
| “Team eligible” is mistaken for unlimited seats | Resolve concrete slots before admission |
| Team size dominates qualification | Aggregate configurable top N member scores |
| Runtime scans miss latency goals | Use frozen slots and indexed player point reads |
| Provisional replacement surprises players | Explain policy before join and show displacement reason |
| Platform session fills before a replacement can connect | Reserve bounded connection capacity distinct from racer slots and validate it against AccelByte session behavior |
| Late telemetry changes published finalists | Snapshot at a watermark and require audited republish |
| Multiple team racers have no winner rule | Require owner-result aggregation before enabling slots per owner above one |
| Bracket repair corrupts history | Version, void, audit, and prohibit silent edits to started runs |
| Hourly materialized views remain stale or become authoritative accidentally | Replace them with incremental qualification projections and publish immutable cutoff tables |
| Session creation failure blocks result transaction | Advance database state first and allocate external sessions through durable work |

## Questions

### Allocation And Qualification

| ID | Decision needed | Working recommendation |
|---|---|---|
| G1 | Does `owner_count` mean qualified teams/players while `slots_per_owner` means racers each may send? | Yes; keep these as separate authoring values |
| G2 | Which team qualification metric ships first? | Reuse the current member qualification-point calculation, then sum configurable top N members |
| G3 | Is Community CP another team qualification metric or an operator-curated value? | Treat it as a metric if Eventun has authoritative facts; otherwise use explicit team assignment with a community label |
| G4 | What are the deterministic tie-breakers for player and team qualification? | Score, best single result, next-best result, earliest achievement time, then stable id |
| G5 | When may a late-event correction replace a published field? | Only before a configured roster-lock deadline and through an operator-reviewed new snapshot |
| G6 | Can one stage mix player owners and team owners? | Allow the data model, but enable it only when the scoring policy makes direct competition coherent |
| G7 | May an explicit player from a qualified team occupy a personal slot in addition to the team's slots? | Yes; the personal entitlement and team capacity are independent unless the event config forbids it |
| G8 | When does an unaffiliated fill apply and can it later be displaced by a qualified owner? | Resolve fallback at field publication; do not silently displace after publication without a new snapshot |

### Team Roster And Admission

| ID | Decision needed | Working recommendation |
|---|---|---|
| G9 | Is active team membership at join time sufficient, or must the member have belonged to the team at qualification cutoff? | Require current membership; optionally add cutoff membership or registration as an event policy |
| G10 | Does null `competition_rank` make a member ineligible for finals? | Yes under manager-rank policy, matching the intended fan/supporter behavior |
| G11 | Which priority policy is the default for team-owned slots? | Manager-controlled competition rank for formal team finals; first-come remains configurable |
| G12 | How are equal manager ranks handled? | Incumbent keeps the provisional seat; otherwise use arrival sequence |
| G13 | When exactly does roster lock occur? | Immediately before the first scored heat after the dedicated server successfully persists the roster |
| G14 | What happens to a displaced player in the session? | Remove them from the racer seat with a clear reason; do not assume a spectator conversion |
| G15 | May a disconnected provisional occupant reclaim the seat ahead of another eligible member? | No special claim unless their configured priority still wins when they return |
| G16 | Is any post-lock substitution allowed? | No in the first slice; add registered alternates only through a later explicit policy |
| G17 | Should managers register racers before the event or rely on rank and arrival? | Start with rank and arrival; design slot assignment so explicit registration can be added |
| G18 | Can a manager change competition rank after the field is published? | Yes until a configurable roster deadline; admission reads must include a version so stale decisions are rejected |

### Results And Brackets

| ID | Decision needed | Working recommendation |
|---|---|---|
| G19 | How is a team winner calculated when `slots_per_owner` is greater than one? | Require an explicit owner-result policy; do not enable multi-racer team brackets without it |
| G20 | Is the first team-gauntlet slice one racer per team or multiple? | Prefer one racer per team for the first end-to-end bracket, while retaining multiple-slot schema support |
| G21 | Does one bracket match always map to one stage run? | Yes; multiple heats may belong to that run if the existing match model supports them |
| G22 | Which bracket format ships first? | Single elimination with explicit seeds, byes, and manual repair |
| G23 | Are loser-bracket routes required now? | Model upstream winner/loser sources, but defer a full double-elimination authoring preset unless selected |
| G24 | Can an operator change a bracket after publication but before any affected run starts? | Yes through a new audited version |
| G25 | How is an already-started bracket match repaired? | Void the run and downstream affected results, then explicitly replay or assign an owner |
| G26 | When does the player-facing bracket become visible? | After the initial field and bracket version are published, including unresolved follow-on paths |

### Operations And UX

| ID | Decision needed | Working recommendation |
|---|---|---|
| G27 | Which allocation and repair controls are essential in the interim Ascentun UI? | Rule editor, cutoff preview/publish, explicit assignment, bracket graph editor, void, and replay |
| G28 | Should qualification previews expose contributing top N members publicly? | Show the breakdown unless competition integrity or privacy requirements identify a reason not to |
| G29 | What happens if Eventun cannot acknowledge roster lock? | Fail closed for formal stages and surface an operator-recoverable state |
| G30 | Which service owns creating downstream AccelByte sessions? | Eventun records advancement and queues idempotent session-allocation work; an external worker performs the call |
| G31 | How long should provisional admission and resolved field snapshots be retained? | Retain accepted competition facts durably; apply a shorter operational retention to verbose admission audit |
| G32 | How much AccelByte session capacity is reserved for pre-lock replacement candidates? | Start with the smallest buffer that permits one serialized replacement, then increase only if multiplayer tests show concurrent joins require it |
