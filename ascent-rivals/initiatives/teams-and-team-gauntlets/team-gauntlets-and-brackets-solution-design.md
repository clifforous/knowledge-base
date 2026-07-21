# Ascent Rivals Team Gauntlets And Brackets Solution Design

Status: Solution design draft
Date: 2026-07-10
Last updated: 2026-07-20
Program index: [[teams-solution-design]]
Primary backend repository: [Eventun](https://github.com/ikigai-github/eventun)
Web reference repository: [Ascentun](https://github.com/ikigai-github/ascentun)

Foundation alignment: the capability review below originated from the pre-implementation projection and individual-cutoff contract. The projection, individual cutoff, season, repair, historical rehearsal, and runtime-hardening work is now implemented and committed locally. T00 approved the revised capability design against that baseline. An uncommitted Eventun Team Core artifact has coder-reported isolated verification and remains under implementation review; Ascentun integration is unfinished, shared deployment remains gated by the coordinated shared-development cutover and combined runtime smoke, and later team-gauntlet work remains separately gated by accepted Team Core identity and membership behavior.

## Related

- [Delivery plan and gates](delivery-plan.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
- [[team-experience-and-progression-solution-design]]
- [[ascent-rivals/system/team-gauntlet-current-state|team-gauntlet-current-state]]
- [[ascent-rivals/system/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]
- [[ascent-rivals/sources/analysis/eventun-team-postgresql-derivation-review]]
- [[ascent-rivals/sources/analysis/eventun-foundation-api-simplification-review]]
- [[gauntlet-finals-and-tournament-modes-design-review]]
- [[gauntlet-stage-client-entry-plan-2026-05-07]]
- [[ascent-rivals/archive/initiatives/gauntlet-runtime/gauntlet-stage-orchestration-improvements|gauntlet stage orchestration archive]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlet-detail|gauntlet-detail]]

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
- Represent every restricted or published-field racer seat as a concrete entitlement before runtime admission; unrestricted open stages remain capacity-based outside this field model.
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
| The implemented cutoff is player-specific selection evidence rather than a generalized competition field | Team qualification, explicit assignment, mixed owners, slots, and bracket positions require a cohesive field layer without widening one player snapshot into every concept |

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

## Capability Model And Coverage

### Dimensions

Use **field owner composition** instead of “group type.” `group` already means an authoring or cohort filter in the current gauntlet model and should not also mean player-versus-team competition.

| Dimension | Supported values | Meaning |
|---|---|---|
| Field owner composition | `PLAYER_ONLY`, `TEAM_ONLY`, `MIXED_OWNER` | Whether published field entitlements belong to players, teams, or an explicit combination |
| Allocation source | individual qualification, team qualification, explicit player, explicit team, bracket advancement, unaffiliated fill | Why an owner receives an entitlement; one field may combine several rules |
| Qualification score | individual best-performance score, team top-N member aggregation | How a standings rule ranks owners before cutoff |
| Slots per owner | normally one for a player; one or more for a team | How an owner entitlement expands into concrete racer seats |
| Roster policy | exact player, current member, cutoff member, explicit roster, rank, threshold, first-come | Which player may occupy an owned slot and with what priority |
| Owner-result policy | player result or explicit aggregation of team slot results | How accepted slot results become the owner result used by a stage or bracket |
| Progression format | none, single elimination, manually authored winner/loser routing, later presets | How accepted owner results resolve downstream positions |

“Hybrid” means `MIXED_OWNER`: player-owned and team-owned entitlements exist in the same published field. It does not mean that individual and team scores are blended into one ranking. Team qualification already derives a team score from individual member performances, but the selected owner remains the team. `MIXED_OWNER` is a derived field composition, not a third owner type; every owner row remains either player or team.

Bracket advancement is an allocation source, not an initial access rule. Qualification or invitation settles the opening field; accepted upstream owner results settle later bracket positions.

### Owner Composition By Allocation Source

`Aligned` means the target owner/slot model can represent the capability without another core abstraction. It does not mean the capability is implemented today.

| Field owner composition | Open or fill | Qualification cutoff | Explicit invite or assignment | Bracket advancement |
|---|---|---|---|---|
| Player-only | Current unrestricted open stages remain outside the formal published-field path. A bounded unaffiliated-player fill can be resolved at field publication. | **Aligned:** rank player owners by the existing individual best-performance model and expand each selected player into one slot. | **Aligned:** materialize explicit player owners and one slot per owner. | **Aligned:** route accepted player-owner results into downstream player positions. |
| Team-only | **Not designed for dynamic open entry:** arbitrary teams cannot acquire formal owner slots merely when members join. Use team registration, qualification, or explicit assignment. | **Aligned:** calculate each member through the individual scoring policy, aggregate configurable top N members, snapshot the contributor breakdown, and select team owners. | **Aligned:** materialize explicit team owners and expand each into configured team-owned slots. | **Aligned with a result policy:** route team-owner results; one racer per team is the simplest first slice. |
| Mixed-owner | A resolved unaffiliated-player fill may coexist with other allocations. Dynamic open creation of team owners is not supported. | **Aligned as separate rules:** individual and team rankings resolve their own owners and are combined only at field publication. There is no implicit cross-type qualification ranking. | **Aligned:** explicit player and team owners may share a field. | **Conditional:** player and team owners may share a bracket only when one approved owner-result order compares them coherently. |

Invite-only and sponsored/community selections use the same explicit owner source. “Wildcard,” “community,” and “sponsor” remain display labels or fallback policies rather than new owner or access types.

### Qualification Scoring Capability

| Capability | Individual qualification | Team top-N qualification |
|---|---|---|
| Input performance | Accepted player match contributions under the configured source and canonical policy | The same accepted player contributions, attributed to the membership interval active at canonical MatchStart (`match_fact.started_at`) |
| Per-player score | Existing qualifier best-sequence and top-K model | Same per-player model; team size does not create additional per-player accumulation |
| Owner aggregation | None; the player score is the owner score | Rank eligible member scores, select configurable top N, and apply the configured team aggregate |
| Cutoff evidence | Player rank, score, tie values, and selected qualifier/match evidence | Team rank, score, tie values, selected member identities/scores, membership attribution, and each member's selected evidence |
| Selected owner | Player | Team |
| Runtime expansion | Normally one player-owned slot occupied only by that player | Fixed `slots_per_owner`; eligible members compete for those slots under the roster policy |
| Stage result | The accepted slot result is the owner result | One slot may map directly; multiple slots require an explicit reproducible owner-result aggregation |

Top-N team scoring includes `N = 1`; that is “best member represents the team,” not individual-owner qualification. `top_n` means at most N contributors. A separate `minimum_contributors`, initially defaulting to one, decides whether a smaller team remains eligible. Average-of-N, minimum performance thresholds, or another aggregate may be added as explicit metric definitions, but must not be inferred from `top_n` alone.

### Representative Use-Case Coverage

| Use case | Configuration | Coverage assessment |
|---|---|---|
| Individual qualifier final | Top 16 players by individual qualification score; one slot each | **Covered by design:** the implemented individual cutoff supplies immutable selection evidence; the later field-allocation extension expands it into player-owned slots. |
| Individual invitational | Sixteen explicitly invited players; one slot each | **Covered by design:** the later explicit-player allocation does not require a standings query. |
| Team qualifier final | Top eight teams by the sum of their top three member scores; one racer per team; manager rank controls admission | **Covered by design after membership intervals:** G02 snapshots contributors and feeds selected team owners into the proven field/slot runtime; G03 adds priority replacement. |
| Team invitational | Eight explicitly invited teams; one racer per team; first-come admission | **First playable vertical:** G01 materializes explicit team owners, one slot each, first-come occupancy, roster lock, and team result. |
| Multi-racer team final | Top eight teams by top-three qualification score; two racers per team; sum of placement points determines the team result | **Conditionally covered:** slot and roster models fit, but the placement-points owner-result policy must be approved before enabling multiple racers. |
| Mixed qualification and sponsor field | Twelve individually qualified players plus two explicitly sponsored teams with one racer each | **Covered when all owners use the same racer-result order:** separate rules publish one mixed-owner field. More than one racer per team would require a cross-owner aggregation policy. |
| Player single-elimination bracket | Qualified or invited players seed a bracket; winners advance | **Covered by the G05 model:** opening selection, player results, stage-run-scoped routing, byes, and repair have defined homes. |
| Team single-elimination bracket | Qualified or invited teams; one racer per team; winning team advances | **Covered after team owner results exist:** the same bracket graph routes team owners. |
| Double-elimination tournament | Player-only or team-only field with winner and loser routes | **Partially covered:** the graph supports explicit winner/loser sources, but the automatic double-elimination authoring preset remains deferred. |
| Player-versus-team bracket | Player owners and multi-racer team owners compete in the same bracket | **Not approved:** requires a common, fair owner-result policy before mixed-owner bracket progression may be enabled. |
| Open team gauntlet | Any team can appear by having members join until capacity | **Not covered intentionally:** formal team ownership and per-team caps require registration, qualification, or explicit field materialization before runtime admission. |

This matrix is a coverage tool, not a promise to enable every representable combination. Authoring validation must reject configurations whose owner-result, roster, or progression policies are incomplete.

## Allocation Rules

### Candidate Rule Shape

| Field | Purpose |
|---|---|
| `allocation_rule_id` | Stable authoring identity |
| `gauntlet_id` and `stage` | Target stage |
| target stage | Opening field uses typed gauntlet/stage identity; later bracket sources reference typed bracket-match relations rather than a free-form key |
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

### Owner Uniqueness And Rule Precedence

The first implementation permits one entitlement row for each field snapshot and typed player or
team owner. Nullable `player_id` and `team_id` foreign keys enforce exactly one owner kind.
Allocation rules resolve in `selection_order`:

1. the first rule selecting an owner claims that owner's entitlement and display provenance;
2. a later rule skips the duplicate and continues to its next candidate until its configured `owner_count` is filled or exhausted;
3. duplicate suppression and any unresolved deficit are retained in the field-resolution audit;
4. no rule silently grants additional slots to an already selected owner.

An event that deliberately grants one owner multiple independent entitlements needs an explicit later policy. A player owner and a team owner remain distinct even when that player is a member of the selected team; runtime still enforces that one player may occupy at most one slot in the run.

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

1. attribute the complete accepted match contribution to the membership interval active at
   canonical MatchStart (`match_fact.started_at`); heat, kill, or player-summary timestamps do not
   split one match across teams;
2. group the attributed qualifier-match contributions by team and member;
3. calculate that member's team-attributed score using the same sequence-window and top-K rules used by individual qualification, but only from contributions attributed to that team;
4. rank members within each team;
5. take the configurable top N member scores;
6. aggregate those scores into the team score;
7. retain the contributing-member breakdown;
8. rank teams by aggregate score, a deterministic lexicographic comparison of the ordered
   contributing-member evidence, earliest final achievement boundary, then team UUID.

Top N is configuration, not a hard-coded product constant. A team with fewer than N scored
members remains eligible only when it satisfies the separately configured
`minimum_contributors`, initially one. The team itself must remain active at cutoff. A membership
change can split one player's qualifier history across teams; it must not assign the player's
collapsed whole-gauntlet score to either the current team or the team active at cutoff.

### Database Execution

Qualification should operate over narrow immutable match-player contributions and incrementally retained player/qualifier sequence state, not rescan raw telemetry or refresh full-history materialized views on every update.

Recommended layers:

- `match_player_fact` or equivalent accepted performance facts;
- source/trust provenance on every performance fact so qualification policy can distinguish dedicated-server and client-reported results;
- an indexed incremental player qualification contribution and best-sequence projection by gauntlet, qualifier, and player;
- a targeted team-attributed member score projection by gauntlet, qualifier, team, and player, derived from the same narrow contributions plus membership intervals;
- a SQL team score function or view using `row_number() over (partition by team_id order by member_score desc)`;
- an immutable cutoff snapshot containing selected owners, rank, score, tie-break values, and contributing members;
- a snapshot version and configuration hash for reproducibility.

General match and player facts remain team-neutral. Team-attributed qualification contributions
store the resolved `team_id` and exact `membership_interval_id`; the sealed cutoff copies or
references the exact selected membership evidence.

Ordinary views or stable functions remain appropriate for team top-N calculations over an already bounded player-score projection. The player/qualifier score and retained best sequence should update incrementally after each accepted match so standings do not inherit the current hourly delay. Native materialized views are transitional only and must not determine the final field.

Client-reported performance remains necessary for time-trial or local qualification modes, but it can be altered by a hostile client. A qualifier must not silently combine client-reported and dedicated-server performance as though they have equal authority. The permitted source policy is a qualifier/competition decision and should be retained in the cutoff snapshot. Lightweight client-event validation is deferred; full dedicated-server replay is not the assumed solution.

### Cutoff And Correction

At cutoff:

1. acquire a resolver lock for the gauntlet and stage;
2. record the exact source projection revision, projector/algorithm version, configuration
   version, and selected membership-interval evidence required by the rules;
3. calculate all allocation rules from current incremental qualification projections and their narrow source contributions;
4. persist owner snapshots and contributor breakdowns;
5. persist each owner's slot count and slot policy as immutable field entitlements;
6. record unresolved deficits and applied fallback rules;
7. publish the field atomically.

A delayed complete-match batch or rewritten historical fact does not silently mutate a published field. An operator may run a recomputation, review the delta, and publish a replacement only before a stage run is claimed and bound to that field. Claim validates that the field still references the current valid source snapshots and configuration, then atomically binds the field and instantiates its concrete stage-run slots. Once bound, field owners and slots remain fixed; only provisional occupants may change until roster lock. A later field correction requires an explicit audited void/rebind or repair decision rather than an ordinary replacement.

### Current Individual Projection And Cutoff Boundary

The implemented individual qualification snapshot is immutable selection evidence, not the generalized competition field. Team work should preserve that boundary instead of widening the player-specific snapshot until it also means team selection, invitations, bracket positions, slots, and roster state.

| Layer | Responsibility | Current foundation and team-phase relationship |
|---|---|---|
| Incremental performance projection | Maintain player qualifier contributions, best sequences, overall scores, and the gauntlet projection revision | Implemented foundation; team scoring reuses the narrow contributions and evidence, not a current-team join over the collapsed player score |
| Source-specific selection snapshot | Freeze selected player owners or selected team owners and their exact scoring evidence | The current foundation supplies individual qualification; G02 adds team qualification and contributor evidence |
| Published field snapshot | Resolve selected allocation rules into one ordered, versioned owner field | G01 proves explicit team assignment; G02 adds team qualification and G04 adds player, mixed, and fallback sources |
| Concrete stage-run slots | At stage-run claim, expand each published owner into the configured racer-seat count | G01 onward; slots reference the field owner and retain source provenance |
| Locked roster and owner results | Persist actual occupants, slot results, owner aggregation, and downstream advancement | G01 proves the one-racer team path; G03 through G05 extend policies and progression |

The conceptual field relations are `gauntlet_field_snapshot` and `gauntlet_field_owner`; final names should follow the implemented schema conventions. G01 initially publishes only the opening stage-target field. Later bracket matches reference typed bracket relations rather than a free-form target key. A stage run binds exactly one matching field snapshot. Each field-owner row has nullable `player_id` and `team_id` foreign keys with an exactly-one-non-null check, plus allocation rule, selection order, source snapshot or bracket position, and display label. Slots reference field owners rather than binding runtime admission directly to a player-only qualification row.

G01 introduces the field/slot binding for explicit team stages without widening the existing
player-only qualification snapshot. When an individual qualification stage is later moved into the
field model, replace its direct `qualification_snapshot_id` admission dependency rather than
retaining two entitlement paths; keep the individual snapshot reference only as provenance for the
selected player owners.

A formal field-bound run has exactly one entitlement path: published owners and concrete slots.
Existing allowed-team/player rows are either legacy non-field invite-stage behavior or authoring
inputs resolved into explicit field owners. They do not remain an additional live filter after a
field is bound. `slots_per_owner` replaces `players_per_team` for field-backed stages. The current
stage win/loss filters retire when the real bracket graph becomes authoritative.

G02 must not calculate team standings by joining `gauntlet_player_score_projection` to current membership. Event-time membership can split one player's matches across several teams, changing sequence windows and top-K results. G02 should maintain targeted team-attributed member qualifier/overall projections from the implemented narrow match contributions, with the same score algorithm and deterministic evidence order. The bounded top-N team aggregate then operates over those member-score rows.

Team qualification extends the existing gauntlet consistency domain with membership-at-MatchStart evidence. A team cutoff preview must therefore bind all of:

- the exact gauntlet projection revision and scoring/configuration hash;
- the exact identity and semantic fingerprint of every membership interval used;
- the team metric definition, including top N and deterministic tie-breaks;
- the complete selected-team, contributing-member, and selected-match evidence.

Team Core intentionally does not implement historical membership correction. Before G02 creates
the first attribution-dependent statistics or qualification state, add an audited interval
supersession/void model capable of retaining exact old and new evidence. A correction then
determines the union of old and prospective affected gauntlets, follows the shared ordered
team/player/gauntlet locking discipline, advances the team's competition-roster revision, and
recomputes affected team contributions and scores while advancing each semantically changed
gauntlet projection revision exactly once. This remains the same repair/revision protocol as
performance facts rather than a second global membership-freshness system. An ordinary
current-roster change after field publication does not transfer or recalculate team ownership; it
affects runtime eligibility only according to the field's roster policy and competition-roster
revision. Roster lock freezes the actual occupants.

Multi-source field publication is atomic. It validates every source preview, resolves fallback and duplicate-owner policy, persists the final owner entitlements, and publishes one field version. A repair or replacement of an upstream selection snapshot may make an unbound field stale, in which case stage-run claim fails until an explicit replacement field is published. It cannot silently mutate the published field or a bound stage run.

## Racer Slots

### Concrete Slot Shape

Each stage-run racer slot should contain:

| Field | Purpose |
|---|---|
| `stage_run_slot_id` | Stable slot identity |
| `stage_run_id` | Runtime match or heat |
| `slot_index` | Stable display and session ordering |
| `field_owner_id` | Immutable published owner entitlement from which this run slot was instantiated |
| `allocation_rule_id` | Why the slot exists |
| `player_id` or `team_id` | Typed player or team entitlement with exactly one foreign key set |
| `display_label` | Community, sponsor, wildcard, seed, or other label |
| `occupancy_policy` | First-come or replace-by-priority |
| `eligibility_policy` | Current member, explicit roster, threshold, or another approved rule |
| `lock_state` | Open, locked, completed, void |

Before lock, live occupant state is owned by the dedicated server. At lock, Eventun persists one occupant per slot and the roster version.

Field publication proves that total concrete racer slots fit the stage competitor capacity and
that any unresolved deficit is either explicitly allowed to remain vacant or blocks publication.
AccelByte connection capacity is racer-slot capacity plus a separately bounded replacement buffer;
it is not another source of racer slots.

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

The monotonic competition-roster revision advances for active membership join/end,
competition-rank or explicit-roster changes, and disband. Future correction tooling must also
advance it. It does not advance for titles, cosmetics, capabilities, or pending membership actions.
A stale roster lock causes the server to re-resolve every proposed occupant before retrying.

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

The initial recommendation is no automatic post-lock substitution. Before lock, the current
game-server reserved-reconnect shortcut must not preserve a team slot: disconnect releases it and
returning players are evaluated under the current occupancy policy. After lock, the same locked
occupant may reconnect through the ordinary match reconnect policy, but no different player may
inherit that slot. Persist disconnect and no-show facts for operator review.

## Results

### Stage-Run Scope

All accepted placements and result uniqueness must include `stage_run_id`. Before multiple bracket
matches share a logical stage, replace not only the current stage-level placement primary key but
also stage-wide completed-run guards, already-completed admission checks, and primary-shard-only
join-status lookup with stage-run or bracket-match identity.

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

Each bracket match also owns explicit readiness and scheduling state. The first bracket slice may
require an operator to release session allocation after both positions resolve, but it must record
a match-specific start or readiness window, check-in deadline where used, and manual hold rather
than reusing one logical stage start time for every round.

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
- inspect unresolved deficits and exact projection revisions.

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

### Slice G1: Explicit-Team Runtime Vertical

- explicitly assigned team owners through one opening stage field;
- one team-owned racer slot per owner;
- current-member eligibility and `FIRST_COME` provisional occupancy;
- disconnect release before lock, same-player reconnect after lock, and no substitution;
- authoritative roster lock and direct single-slot team result; and
- minimal Ascentun authoring and dedicated-server/client admission explanation.

### Slice G2: Team Qualification

- player and top-N team scoring from MatchStart-attributed contributions;
- cutoff preview and immutable contributor evidence;
- qualified team owners feeding the proven field and slot runtime; and
- deterministic tie-break and minimum-contributor policy.

### Slice G3: Priority And Roster Policies

- manager competition rank and other approved eligibility policies;
- strictly-higher-priority pre-lock replacement and recovery;
- indexed admission and stale-roster revision handling; and
- explicit roster registration only if selected after the rank-and-arrival flow is proven.

### Slice G4: Mixed And Expanded Allocations

- explicit player and team owners in one field;
- community, sponsor, and wildcard display labels;
- fallback or unaffiliated fills;
- operator repair; and
- multiple team slots only with an approved owner-result aggregation.

### Slice G5: Brackets

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
| Late telemetry changes published finalists | Snapshot at exact projection/configuration revisions and require audited replacement before stage-run binding |
| Multiple team racers have no winner rule | Require owner-result aggregation before enabling slots per owner above one |
| Bracket repair corrupts history | Version, void, audit, and prohibit silent edits to started runs |
| Broad live standings are reused as team cutoff evidence | Extend the revisioned contribution/projection model and publish immutable source-specific snapshots before resolving the unified field |
| Session creation failure blocks result transaction | Advance database state first and allocate external sessions through durable work |

## Questions

### Allocation And Qualification

| ID | Decision needed | Working recommendation |
|---|---|---|
| G1 | Does `owner_count` mean qualified teams/players while `slots_per_owner` means racers each may send? | Yes; keep these as separate authoring values |
| G2 | Which team qualification metric ships first? | Reuse the current member qualification-point calculation, sum at most configurable top N members, require separately configured minimum contributors, initially one |
| G3 | Is Community CP another team qualification metric or an operator-curated value? | Treat it as a metric if Eventun has authoritative facts; otherwise use explicit team assignment with a community label |
| G4 | What are the deterministic tie-breakers for player and team qualification? | Preserve the implemented player order; for teams use aggregate score, lexicographically ordered contributing-member evidence, earliest final achievement boundary, then team UUID |
| G5 | When may a late-event correction replace a published field? | Only before a stage run is claimed and bound to the field; later correction requires audited void/rebind or repair |
| G6 | Can one stage mix player owners and team owners? | Allow the data model, but enable it only when the scoring policy makes direct competition coherent |
| G7 | May an explicit player from a qualified team occupy a personal slot in addition to the team's slots? | Yes; the personal entitlement and team capacity are independent unless the event config forbids it |
| G8 | When does an unaffiliated fill apply and can it later be displaced by a qualified owner? | Resolve fallback at field publication; do not silently displace after publication without a new snapshot |

### Team Roster And Admission

| ID | Decision needed | Working recommendation |
|---|---|---|
| G9 | Is active team membership at join time sufficient, or must the member have belonged to the team at qualification cutoff? | Require current membership; optionally add cutoff membership or registration as an event policy |
| G10 | Does null `competition_rank` make a member ineligible for finals? | Yes under manager-rank policy, matching the intended fan/supporter behavior |
| G11 | Which priority policy is the default for team-owned slots? | Manager-controlled competition rank for formal team finals; first-come remains configurable |
| G12 | How are equal manager ranks handled? | Allow duplicate non-null competition ranks; the incumbent keeps the provisional seat, otherwise use arrival sequence |
| G13 | When exactly does roster lock occur? | Immediately before the first scored heat after the dedicated server successfully persists the roster |
| G14 | What happens to a displaced player in the session? | Remove them from the racer seat with a clear reason; do not assume a spectator conversion |
| G15 | May a disconnected provisional occupant reclaim the seat ahead of another eligible member? | No special claim unless their configured priority still wins when they return |
| G16 | Is any post-lock substitution allowed? | No in the first slice; the same locked occupant may reconnect, but a different member may not inherit the slot |
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
| G33 | How are downstream bracket matches scheduled? | Store match-specific readiness/scheduling and manual-hold state; initially let operators release session allocation after both positions resolve rather than deriving every round from one stage start time |
