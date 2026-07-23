# Teams And Team Gauntlets Delivery Plan

Status: in-progress
Status detail: T00 through T03B and the G01 dedicated-server integration passed local implementation
and review. The coordinated shared-development database cutover completed successfully, and
Eventun, Ascentun, and the game-client changes are deployed in shared development. Combined
player-authenticated Team Core, field/admission/roster/result, qualification, and public-consumer
smoke and soak remain active. Production remains a separate unscheduled gate.

Last consolidated: 2026-07-23

## Outcome And Boundary

Deliver the first useful team experience and then extend the cohesive gauntlet model with team
qualification, concrete competition slots, runtime roster enforcement, and brackets.

This plan defines work order and completion boundaries. The detailed product and technical
contracts remain in the linked solution designs. It does not treat proposed behavior as current
system state or authorize production deployment.

## Program Gates

| Gate | Required before |
|---|---|
| Committed and locally verified Eventun foundation and runtime hardening | Starting T00 design refresh and reapproval |
| Coordinated Eventun shared-development cutover and combined runtime smoke | Database/deployment completed 2026-07-23; combined smoke and soak remain before production acceptance |
| T00 selection of the initial delivery cutoff | Starting either implementation workstream |
| Canonical team identity and membership intervals | Historical team statistics, progression attribution, or team qualification |
| Notification payload prototype and outbox contract | Closed-team actionable notifications |
| Approved progression definition | Team XP, levels, caps, challenges, or unlock implementation |
| Concrete competition field and slot model | Mixed allocation and dedicated-server team-seat enforcement |
| Stage-run-scoped result identity | Multiple bracket matches using one logical stage |

The prerequisite execution details are maintained in
[Eventun Development Cutover And Runtime Hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md).

## T00 — Refresh And Reapprove The Team Designs

T00 was approved against the committed local foundation and retained migrated database. The
combined Eventun, Ascentun, and game-client implementation is now enabled in shared development.
Reconfirm affected contracts and runtime assumptions during combined smoke; do not repeat the
entire design checkpoint solely because deployment occurred later.

- Reconcile all three team designs with the implemented authentication, API generation, match
  ingestion, facts, serving projections, cutoff snapshots, seasons, repair, and migration
  boundaries.
- Revalidate the capability matrix against the actual schema and approve the initial
  individual, team, mixed-owner, invitation, qualification, and bracket use cases.
- Resolve the first-slice product decisions for progression, notification delivery, cosmetics,
  wildcard/fallback policy, competition slots, roster priority, and team result aggregation.
- Decide whether existing pre-alpha team, membership, invitation, and request state is migrated
  deterministically or discarded before replacement writes are enabled.
- Select the eventual game-client routes in scope and retain the complete route/widget/screenshot
  inventory plus controller-first Pencil design as the T05 gate before adding those routes; it is
  not a blocker for the backend-and-existing-website Team Core cutoff.
- Select the exact team-experience and team-gauntlet delivery cutoffs and explicit exclusions.

T00 is complete because Team Core has approved contracts, affected website flows, owner decisions,
dependencies, and verification boundaries. Later game-client UI flows retain their own T05 design
gate.

### T00 Approved Checkpoint

The committed Eventun foundation supports the approved competition capability model without
adding team identity to general match facts. T00 incorporates the following corrections:

- use MatchStart, represented by `match_fact.started_at`, as the membership-attribution time for
  the complete match;
- retain disbanded team identity and membership history instead of physically deleting teams;
- keep immutable membership validity separate from mutable title, capability, and competition-
  rank state;
- use typed player/team foreign keys for competition owners and one field-backed admission path,
  rather than polymorphic owner ids or parallel live filters;
- make exact pending-action identity, expiry, idempotency, cancellation, and player-scoped
  invitation discovery part of any slice that retains request/invite membership modes;
- keep additive acceptance/approval in `AddTeamMember` and decline/deny/cancel in
  `ResolveTeamMembershipAction`; every operation on an existing action requires its exact UUID and
  version and never infers a current generation;
- cancel effective pending actions when membership mode actually changes, but preserve them across
  ownership transfer because they represent team intent;
- defer historical membership correction tooling until before the first attribution-dependent
  team statistics or qualification slice; a future correction requires explicit supersession/void
  evidence and advances the roster revision;
- permit subjectless public `Team` and `Teams` reads only for an Ascentun confidential client with
  Eventun Server `READ`; player mutations continue to use the authenticated player's token with
  no custom player permission;
- move the full game-client route/widget/screenshot/Pencil exercise to the T05 gate because the
  first implementation cutoff changes the existing website and backend, not game-client menus;
- retire or reinterpret legacy allowed-team/player, `players_per_team`, and stage win/loss paths
  as their field, slot, and bracket replacements become authoritative.

The first implementation cutoff is one breaking T01+T02 deployment unit named
**Team Core**:

- Eventun-generated team identity and authenticated creator ownership;
- retained active/disbanded team state, one active team per player, and half-open membership
  intervals;
- separate presentation title, delegated capabilities, competition rank, and a monotonic
  competition-roster revision;
- transactional create, transfer, disband, browse/detail/current-team, join, leave, invite,
  request, accept/approve, decline/cancel, and removal behavior with typed outcomes and audit;
- compact public and current-player reads plus exact pending-state reads;
- the corresponding minimal Ascentun contract and UI update, removal of stale token-gating and
  numeric-designation artifacts, complete contract generation, and coordinated website/service/
  schema cutover without a compatibility branch.

Team Core explicitly excludes new game-client menus, Chat delivery, team statistics,
progression, cosmetics, qualification, competition fields, racer slots, and brackets. Those
features remain separately gated.

The accepted Team Core owner decisions are:

- discard the invalid pre-alpha team, membership, pending-action, and media state after a guarded
  target preflight; a 2026-07-20 read-only check of the retained migrated rehearsal found 10 teams,
  one general membership with no owner, no join requests, one expired invitation, 17 media rows,
  and no stage-team references;
- invalidate or version existing Ascentun sessions that cache discarded team identity;
- default the maximum active roster to 16 through Eventun's `TEAM_MAX_ACTIVE_MEMBERS` environment
  configuration rather than a hard schema constant; a lower configured value blocks later joins
  but does not evict existing members;
- let disbanded team names and tags be reused, enforcing case-insensitive uniqueness only among
  active teams while UUIDs preserve historical identity; and
- ship `MANAGE_MEMBERS`, `EDIT_TEAM_PROFILE`, and `MANAGE_COMPETITION_ROSTER`; the owner implicitly
  has all capabilities and exclusively assigns capabilities, transfers ownership, or disbands;
- use prefixed protobuf enums, signed 64-bit Unix-millisecond action/lifecycle timestamps, and a
  presence-aware team patch whose authorization is based only on fields that actually change;
- trim names before enforcing 4–16 Unicode code points, preserve the uppercase 2–4 ASCII
  alphanumeric tag and uppercase `#RRGGBB` color constraints; and
- ensure an authenticated creator has an ID-only Eventun player row before it is locked for owner
  membership creation.

The Team Core migration and review boundary is deliberately narrow:

- fail closed when any legacy foreign-key reference is unknown, even if the observed source table
  is empty; allow the known `gauntlet_stage_team` dependency only after proving it empty;
- establish the required `btree_gist` capability and replacement constraints before any historical
  reconstruction by executing the exact marked replacement DDL in an isolated preflight schema,
  then discard the approved pre-alpha rows rather than invent compatible state;
- use focused canonical-schema, transition, concurrency, authorization, access-plan, and real-runner
  discard/preflight coverage; do not require another production-scale historical rehearsal unless
  the owner separately requests it; and
- keep implementation evidence, review acceptance, source-control state, shared-development
  deployment, and production deployment as separate gates.

The first playable team-gauntlet vertical after Team Core is
explicitly assigned teams, one racer slot per team, current-member eligibility, first-come
provisional occupancy, disconnect release before lock, one authoritative roster lock, same-player
reconnect after lock, no post-lock substitution, and direct single-slot team results. Team top-N
qualification, priority replacement, multiple racers, mixed owners, and brackets then build on a
proven owner-to-result path.

## Team Experience Workstream

### T01 — Replace Team Identity And Membership State

Depends on T00. Local Eventun and Ascentun implementation may proceed independently; deployment is
one breaking unit after the shared-development cutover and combined runtime smoke.

- Generate team identity and derive the initial owner from the authenticated creator.
- Enforce exactly one explicit owner, atomic ownership transfer or disband, one active team per
  player, and nonoverlapping membership validity intervals.
- Separate visible title, effective management capabilities, and competition rank; remove numeric
  designation as an authorization fallback.
- Apply the T00 decision for deterministic migration or discard of existing team and pending
  membership state.
- Keep creation, disband, capabilities, and roster administration on the website initially.

### T02 — Add Team Reads And Membership Transitions

Depends on T01.

- Add compact team browse/detail, active roster, current-player team, open join, leave,
  invitation, accept/decline, request, cancellation, and typed transition outcomes selected by
  T00.
- Keep one deterministic contextual add-member command. Derive the actor from authentication,
  lock every discovered affected team in UUID order before players, then re-read the affected-team
  set under the player lock and abort for retry if it expanded before touching memberships, pending
  actions, or audit. Commit state and audit atomically. Append
  notification intent in the same transaction only after T07 selects delivery.
- Enforce expiry, renewal, idempotent repeat behavior, and transactional consumption or
  cancellation of pending state across membership-mode, removal, and disband races; ownership
  transfer preserves pending actions as team intent.
- Keep Team Core to existing profile needs. Add recruiting region, IANA time zone, display-only
  recruiting status, and allowlisted Twitch or Discord links in a later selected website slice.
- Defer server pagination and text search until measured team count, roster size, payload, or
  latency requires them.

### T03 — Add Fact-Backed Team Views

Depends on T01 membership intervals and the relevant T02 public read contracts.

- Replace the internal Team Core response as a public presentation dependency with domain-neutral
  public team summaries and public roster members that both Website V2 and the game client may use.
- Add a bounded authenticated viewer-state read so consumers receive the current relationship,
  exact pending-action reference, and allowed transitions without reproducing Eventun's membership
  state machine.
- Add fact-backed team performance summary, current-roster leaderboard comparison, represented-
  result history, and owner-aware gauntlet history as independently cacheable reads.
- Attribute complete-match performances to membership at canonical MatchStart
  (`match_fact.started_at`) rather than the current roster.
- Do not invent a generic team score by summing current members' lifetime careers.
- Prefer bounded SQL over mutable aggregate state; add an incremental projection only when
  representative plans show it is required.

#### T03 Public Read Contract Checkpoint

The following logical Eventun reads are approved. Names may follow repository protobuf conventions,
but the messages remain domain-neutral and must not contain Website component names, routes, copy,
or URLs.

1. **Public team directory.** Return one complete shallow collection of active teams at the
   accepted scale. Each summary contains stable team identity, name, tag, public membership mode,
   colors, bounded public media, status, and `active_member_count`. Disbanded teams are absent from
   normal browse; a direct historical reference may resolve to a read-only tombstone.
2. **Public team detail.** Return the public summary plus the complete active roster, bounded by the
   configured 16-member limit. A public member contains player identity, name, avatar, explicit
   owner marker, approved presentation title, and optional competition rank. It excludes effective
   capabilities, membership-interval identity, action versions, roster revision, and audit or
   correction evidence. Hiding affiliation suppresses optional badges and cosmetics on other
   player-facing surfaces; it does not make the canonical roster incomplete on the team's own
   public profile.
3. **Authenticated team viewer state.** For one viewed team, return the authenticated player's
   relationship, current team identity where relevant, one exact unexpired membership-action
   reference when applicable, and an explicit set of allowed transitions such as join, request,
   cancel, accept, decline, leave, or manage. This response is request-time private state. Detailed
   effective capabilities and team-wide pending queues remain separate permissioned management
   reads.
4. **Fact-backed performance summary.** Support lifetime and optional exact-season scope. Return
   distinct represented matches, represented player-match results, individual podium finishes,
   results in matches with ascension evidence, and latest represented-result time. Names must retain
   the `represented`
   or `individual` distinction: these are performances earned by players while their membership was
   effective at MatchStart, not team-format wins, podiums, or a synthetic team rating.
5. **Current-roster leaderboard comparison.** Accept team, public course, player-facing category,
   and optional season. Return every current public roster member with the player's global record
   and rank when one exists, explicit unranked state otherwise, and response-level as-of time.
   Filtering occurs before no global top-N truncation, global ranks are preserved, and no aggregate
   team rank or score is produced. A nested optional record carries rank, time, and optional loadout
   value so generated Unreal consumers preserve absence without interpreting zero as missing.
6. **Represented-result history.** Return newest-first public match results attributed to the team
   at MatchStart, with a caller limit capped at 100 and optional exact-season scope. Each row carries
   public player identity, match time, public course identity, player-facing race mode, and
   presence-aware placement, circuit points, podium, and ascension result. Do not expose session,
   match, batch, event, replay, client-version, membership-interval, or repair identities. A stable
   opaque continuation may be added only when a consumer needs more than the bounded first page.
7. **Owner-aware team gauntlet history.** Return only team qualification or accepted result evidence
   where the team itself is the competition owner. Member participation alone does not create a team
   result. Qualifier standing, accepted stage result, and generic participation remain distinct;
   an accepted result includes its exact StageRun identity and never implies a final, win, trophy,
   or medal unless the competition contract explicitly supplies that meaning.

Public reads are callable by authenticated players and by the Website confidential client through
an explicit subjectless Server `READ` allowlist. Existing internal Team Core responses are not made
broadly public merely to satisfy Website access. Website V2 composes these reads server-side and may
map them to route-specific view models; the generated game client may consume the same domain
messages directly. Management, authoring, admission, roster lock, repair, and audit responses remain
separate.

Public identity/roster, viewer state, summary, roster comparison, represented history, and gauntlet
history have independent failure and cache lifecycles. Mutations invalidate affected public team
identity, player affiliation, viewer state, and current-roster reads. Accepted facts or repaired
attribution invalidate the affected performance/history reads. Implementation must measure the
complete directory, one 16-member detail, the full roster comparison, summary, and bounded history
on representative migrated data before adding pagination, caches, or new aggregate projections.

#### T03A Implementation Review Checkpoint

The Eventun T03A implementation is committed as `efcedcd` after coder verification and independent
implementation review. It is verified local implementation evidence, not deployed current-system
behavior.
T03B performance summary, roster comparison, represented-result history, and team/player gauntlet
history remain out of this checkpoint.

T03A adds these domain-neutral Client operations:

- `PublicTeams`, `PublicTeam`, and player-authenticated `TeamViewerState`;
- `PublicGauntletDiscovery`;
- separate `PublicGauntletCurrentStageField` and exact-run
  `PublicGauntletStageRunField` reads;
- `PublicGauntletStageRuns` and exact-run `PublicGauntletStageRunResults`.

Seven public-safe reads join the explicit subjectless Server `READ` allowlist for the Website
confidential client. `TeamViewerState` remains subject-bearing and derives relationship, current
team conflict, exact unexpired action identity/version, capacity, membership mode, and allowed
transitions inside Eventun. Existing Team Core and evidence-rich field/runtime operations receive
no broader authorization. Current `Team` and `Teams` compatibility remains until the coordinated
consumer migration removes it.

Public field reads separate the current field head from the immutable snapshot bound to an exact
StageRun. Results require a nonzero exact run UUID plus matching gauntlet and stage. Team-owned
results and public participant attribution are separate, and the subjectless response has no
viewer-relative or personal-result concept. The public timeline exposes exact run identity, run
number, frozen scheduled time, factual lifecycle, result availability, and presence-aware actual
start/end times while omitting session, provider, failure, and evidence internals. Discovery uses an
exact active or sole StageRun's bound field snapshot for capacity. A future stage with no run may use
the current unbound field head; ambiguous historical/replay stages omit capacity rather than
misreporting a replacement head.

`gauntlet_stage_run.scheduled_start_at`, `started_at`, and `ended_at` are added in the canonical schema
and the additive prefix of the one-time `migration/migration.sql` delta. The scheduled time is copied
from authoring when the run is created, retained rows are backfilled from their referenced stage, and
the value is immutable thereafter. The delta derives retained lifecycle evidence from roster lock,
accepted match, and terminal update times, then fails preflight on incompatible retained state.
Constraints enforce finite millisecond timestamps, creation/start/end ordering,
prestart/started/terminal state coherence, and atomic status/timestamp transitions. Runtime roster
lock, first accepted match, completion, failure, and expiry paths write the lifecycle evidence in
their state transition. A repository-file regression passes the actual delta through the historical
runner's `splitMigration` boundary and proves the lifecycle block remains in the additive prefix.

Coder verification passed:

- `./scripts/verify.sh`, including protobuf format/lint/generation, 82-operation Client contract,
  21 subjectless/shared versus 61 player-only authorization partition, Go tests/vet, and build;
- `./scripts/verify_schema.sh` lifecycle/relational contracts and database-backed public team,
  viewer, current/run-field, exact-run result, frozen-schedule, run-bound discovery-capacity,
  cancellation, and existing runtime regression smoke;
- representative isolated access plans for 100 active teams and a 100-owner field. Observed public
  team reads were approximately 1.1 ms directory, 0.25 ms detail, and 0.07 ms viewer state; public
  gauntlet reads were approximately 0.11 ms discovery identity/media plus 0.58 ms discovery
  occurrence/window/capacity resolution, 0.07 ms current field, 0.06 ms run field, 0.02 ms timeline,
  0.01 ms owner results, and 0.02 ms participant attribution. The discovery measurements execute the
  production media selection, occurrence windowing, StageRun authority, stage/head joins, and
  capacity aggregation rather than a simplified surrogate;
- deterministic generated Unreal contract composition with explicit semantic presence wrappers and
  fully prefixed enums; no Website, Ascentun, or game-client consumer was changed;
- strict Knowledge Base validation and `git diff --check`.

No authentic reconstruction rehearsal or shared database mutation was run. T03A's next gate is the
coordinated shared-development cutover and combined consumer smoke. T03B fact-backed performance and
history reads may proceed as a separate implementation checkpoint against the committed T03A
contract.

#### T03B Implementation Review Checkpoint

T03B passed coder verification and independent implementation review and is committed as `a96d6b4`.
It is verified local implementation evidence, not deployed current-system behavior.

Five domain-neutral Client operations are added: `PublicTeamPerformance`,
`PublicTeamLeaderboardComparison`, `PublicTeamRepresentedResults`, `PublicTeamGauntletHistory`, and
`PublicPlayerGauntletHistory`. All five are player-callable public reads and join the explicit
subjectless Server `READ` allowlist. The resulting Client inventory is 87 operations: 26 shared
operations comprising 24 reads and two writes, plus 61 player-only operations. The generated Models
union contains 92 operations; Admin remains 74, Server remains five, and the GameServer subset
remains 17.

Performance and represented-result history read normalized server compact facts directly. They use
all accepted facts without filtering on the informational canonical flag, exclude explicit bots,
apply exact optional `match_fact.season_id`, and
resolve effective non-voided membership with the half-open interval at `match_fact.started_at` in the
same SQL statement. A result whose match starts before `left_at` remains attributed even when the
match ends later; a match starting at `left_at` is excluded. The public ascension fields are named
`represented_results_in_ascension_matches` and `ascension_match`, because retained evidence proves
match participation rather than a specific player's ascension. Historical result course codes remain
readable when the catalog row is null, missing, or inactive; presentation is explicitly unavailable
when no catalog row exists.

The current-roster comparison computes the complete global rank before joining the bounded current
roster. It returns all 16 members, including explicit unranked records, supports lifetime or exact
season scope, permits exact inactive-course reads, and returns `NotFound` for an unknown exact course.
Team qualification history exposes `competitive_rank`; individual qualification history exposes
`selection_rank`. Player history first selects the newest sealed individual snapshot for each
gauntlet/stage and only then filters for the player, so a player removed by V2 cannot reappear from
V1. Accepted player-owned and represented-team StageRun results remain separate typed evidence. The
team and player gauntlet-history request bound is named `max_entries`, because qualification and
accepted-result evidence share one ordered entry stream.

No table, cache, materialized view, or background worker was added. Three supporting history indexes
are present in the canonical schema and production delta: effective membership by team, accepted team
result by team, and accepted placement by player. Coder verification passed:

- `./scripts/verify.sh` and `./scripts/verify.sh unreal`, including deterministic protobuf, Gateway,
  Swagger, integration-client, and Unreal generation, Go tests/vet/build, and exact generated
  inventory checks;
- `./scripts/verify_schema.sh`, including MatchStart join/leave boundaries, exact-season versus
  seasonless lifetime reads, accepted noncanonical facts, explicit-bot exclusion, multiple represented
  players in one match, absent podium evidence, null and removed course presentation, fact repair
  visibility, all-16-member comparison, global rank outside ordinary top N, seasonal loadout records,
  inactive and unknown course behavior, team qualification evidence, team-owned versus represented
  and player-owned result separation, and newest sealed snapshot authority;
- `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` of the five captured production SQL statements after
  adding 1,200 unrelated membership and gauntlet-result histories. The gate requires the exact
  membership/team-result/player-placement indexes and bounds execution time, shared buffers, visited
  rows, and rows removed by filters; the existing long-retained-history and rebuild plan matrix also
  passed;
- wrapped cancellation/deadline mapping, strict Knowledge Base validation, and `git diff --check`.

No authentic reconstruction rehearsal, retained/shared database mutation, Website, Ascentun, or
Ascent Rivals change was run. The next gate is the coordinated shared-development cutover and
combined consumer smoke.

#### T03C — Public Gauntlet Occurrence-Fact Correction

Before an established consumer freezes the T03A discovery response, remove the query-time
`timing_state`, `active_occurrence`, `next_occurrence`, `latest_ended_occurrence`, and
`additional_scheduled_occurrence_count` fields. Eventun continues to return the complete stable
gauntlet identity, presentation, occurrence, type, start/end, field, and capacity facts required by
public consumers. This is an approved breaking replacement; no compatibility alias or parallel
version is required.

Website V2 owns `Current`, `Upcoming`, `Past`, active, next, latest-ended, and additional-count
presentation. It renders from one Website-server timestamp, hydrates from that same timestamp,
advances it monotonically, and recalculates at the nearest occurrence boundary and on visibility
changes. A boundary does not invalidate or refetch the Eventun collection. Normal TTL, authored
schedule changes, new gauntlets, field changes, and explicit invalidation remain data-freshness
reasons.

The correction is schema-neutral. Update the protobuf/OpenAPI/generated contracts, Eventun response
construction, focused semantic and authorization inventories, Website V2 runtime schema and
derivation, and exact consumer tests. Preserve the overlap rule that the primary active occurrence
is the active occurrence ending soonest. Do not use this correction to redesign runtime/result
lifecycle or migrate the game client.

#### T03C Implementation-Review Checkpoint

The Eventun implementation passed coder verification and independent implementation review and is
committed as `0e4d656`. It removes the five query-time
presentation fields, reserves their protobuf names and numbers, and removes the now-unused timing
enum and occurrence-selection message. `PublicGauntletDiscoveryResponse` retains
`server_time_unix_ms` only as response metadata and a repeated gauntlet collection; each entry
retains only gauntlet identity and the deterministically ordered normalized occurrence facts.
Eventun no longer derives Current, Upcoming, Past, active, next, latest-ended, or additional-count
presentation.

For a stage with no StageRun, discovery now returns configured capacity from the current published
field head regardless of whether the occurrence start time has passed. Exact, sole, and uniquely
active StageRuns retain run-bound field authority, while multiple runs without one authoritative
run continue omitting capacity. The response does not expose a capacity-basis field. Focused
database smoke covers otherwise equivalent past and future no-run stages so configured capacity
cannot disappear solely at an occurrence boundary.

Fresh generation and exact inventories passed: merged Swagger has 147 paths, 166 operations, and
445 definitions; Client has 79/87/257, Admin 63/74/217, and Server 5/5/36; generated GameServer has
17 operations and 269 definitions, while Models has 92 operations and 269 definitions. Contract
checks reject both retired supporting definitions, and the retained discovery entry and response
properties are exact. The HTTP route, `READ` action, subjectless server permission inventory, and
all operation counts remain unchanged.

Coder verification passed:

- focused protobuf-reflection, discovery lifecycle/media, generated Swagger inventory, and Unreal
  composition tests;
- `./scripts/verify.sh` and `./scripts/verify.sh unreal`, including deterministic protobuf,
  Gateway, Swagger, integration-client, and Unreal generation;
- `./scripts/verify_schema.sh`, including the production discovery access-plan query and
  database-backed normalized occurrence/capacity smoke;
- strict Knowledge Base validation and `git diff --check`.

The Eventun work changes no canonical schema, production or post-development delta, historical
conversion, Website V2, Ascentun, game client, shared database, or IAM state. Commit `0e4d656` is
source evidence only and is not deployed; shared development may continue serving the previous
response until a later coordinated deployment. The review found no blocking Eventun defect.

The compatible Website consumer correction passed coder verification and independent implementation
review and is committed as `ar-web` `7d1d00c`. It accepts both response generations, ignores Eventun
response time and redundant presentation fields, caches only normalized occurrence facts, derives
SSR from one fresh Website-server timestamp, and uses the same timestamp for hydration before
monotonic browser advancement and suspension recovery. Coordinated deployment remains separate from
the accepted Eventun and Website source evidence.

### T04 — Add Initial Team Cosmetics

- Implement only the T00-approved fixed border/effect and compatible decal experiment.
- Let members choose whether and where to display team affiliation and entitled shared
  cosmetics.
- Keep upload and team-wide administration on the website and fixed entitlements in Eventun.
- Defer course flags, holograms, and broader profile decoration.

### T05 — Add Game-Client Team Views And Membership Flow

Depends on the T02 contract and the dedicated T05 controller-first design checkpoint.

- Implement current team, browse, team detail, roster, open join, leave, and invitation-response
  flows selected by T00.
- Reuse existing navigation and controls where the captured UI inventory supports it.
- Keep creation, disband, promotion/demotion, capability management, and token gating out of the
  game client.
- Add a roster-to-party convenience invite only if it is a thin call to the unchanged existing
  party path.

### T06 — Add Team Awareness In Lobbies And Matches

- Show approved team identity in lobby, profile, player-card, and pre-heat presentation.
- Show teammates with the green minimap treatment and visually test an optional green teammate
  bounty beam.
- Keep private teammate relation indicators distinct from public affiliation/cosmetic visibility.
- Do not change party-member marker behavior.

### T07 — Integrate Team Notifications

- Prototype the installed AccelByte Chat system-inbox payload path before freezing actionable
  message contracts.
- Persist invitations and approved join-request actions until expiry or response; keep ordinary
  informational changes transient unless T00 selects otherwise.
- Use an Eventun outbox with stable deduplication and revalidate current Eventun state when an
  action is opened.
- Do not add team chat or a separate activity feed.

### T08 — Define Team Progression Before Implementing It

- Define XP sources, active-participation rules, member/team caps, reset periods, permanent versus
  seasonal scope, levels, challenges, cosmetic unlocks, and team-owned versus player-owned
  rewards.
- Decide how team challenges reuse Eventun goal evaluation and normalized progression facts.
- Validate economy impact before granting player rewards.
- Start implementation only after the product definition is approved.

## Team Gauntlet Workstream

This workstream may be designed alongside the experience work, but authoritative team
qualification depends on T01 membership intervals.

### G01 — Deliver An Explicit-Team Runtime Vertical

- Publish one opening stage field containing explicitly assigned team owners and expand each into
  one concrete team-owned racer slot.
- Treat field owners and slots as the sole entitlement path for that field-backed run; legacy
  allowed-team/player filters become authoring inputs rather than parallel runtime checks.
- Add current-member indexed point-read admission while the dedicated server alone serializes
  first-come provisional occupancy and disconnect release before one authoritative pre-match
  roster lock.
- Allow only the locked occupant to reconnect after lock; perform no substitution.
- Persist the single slot result as the team result and make every accepted placement and
  completion guard stage-run scoped.
- Keep the broader player/team/mixed field schema extensible, but do not implement every allocation
  source in this first vertical.

#### G01 Implementation-Review Checkpoint

The local Eventun working tree implements the approved narrow slice without an Ascentun, game-
client, shared-database, or historical-field conversion:

- Admin preview, publication, and unbound replacement seal one opening-stage explicit-team field;
  Client reads expose its immutable owner, binding, roster, and result evidence; the fifth
  ServerService operation locks the complete roster. Claim binds the current field leaf, freezes
  the relevant stage rules, creates one concrete slot per owner, and returns the exact binding.
- Publication requires the team-owner count to satisfy `min_competitors`, `max_competitors`, and
  `max_lobby_size`. Roster lock instead requires occupied slots to satisfy the frozen
  `min_lobby_size`, while rejecting occupancy above the frozen `max_lobby_size` or concrete slot
  count. Every other slot is sealed as a no-show and cannot accept a substitute after lock.
- The caller supplies only a nonzero publication/replacement or roster-lock UUID plus the ordinary
  request payload. Eventun canonicalizes and hashes that payload with SHA-256. Exact retries return
  retained state; global UUID reuse with different semantics returns `Aborted`. Configuration and
  owner preview hashes remain explicit stale-preview guards, not caller-computed idempotency hashes.
- PostgreSQL composite foreign keys bind every roster entry to its exact StageRun, field snapshot,
  slot, owner, team, player, and membership interval. Field-backed per-match rows and final slot,
  player-placement, and team-owner results retain those same identities; placement also proves its
  gauntlet and stage match the StageRun.
- Per-match results are keyed by StageRun, match, and player with one exact occupied slot per row;
  accepted standings receive a server-computed semantic hash. Final slot results are keyed by
  StageRun and slot, player participation placement by StageRun and player, and direct one-slot team
  results by StageRun and field owner, with unique team and slot identities.
- Legacy match acceptance still filters null, statless, and bot/non-player standings before hashing;
  field-bound acceptance rejects them. Stage standings require one completed `stage_run_id`, while
  the player-event timeline deterministically selects the latest completed run by `updated_at`,
  `run_number`, and UUID and returns that identity with the event.
- G01 query, scan, transaction, and commit failures pass through request-context infrastructure
  mapping, preserving wrapped cancellation and deadline statuses across field, claim, roster-lock,
  acceptance, and completion paths.
- The dependency order is team UUID, player UUID, gauntlet projection, stage, field head, StageRun,
  slots, then lock/result rows. Publication uses team to gauntlet/stage/head; claim starts at the
  gauntlet tier and never relocks teams; roster lock uses team/player/StageRun/slot order; result
  acceptance starts at the StageRun tier.
- The additive field schema follows the Team Core replacement rather than entering its marked
  replacement-constraint block. It creates no historical fields and converts no legacy filters.

`./scripts/verify.sh` passed generation, protobuf contracts, Go and Bun tests, vet, and the
linux/amd64 build. The isolated PostgreSQL 16 suite passed canonical/delta parity, focused
publication/claim/roster/result races, relational constraints, access plans, and the complete
repository schema/benchmark matrix, including the two-completed-run StageRun isolation regression.
The field admission fixture observed p95 0.056 ms before lock and 0.016 ms after lock. No
authentic-data or production-scale reconstruction was run.

The owner accepted this implementation-review checkpoint on 2026-07-21. The reviewed Eventun
implementation is committed as `6343438`; this acceptance does not imply deployment. G01 remains
open until the reviewed dedicated-server integration and Eventun foundation are submitted and
proven together through the coordinated runtime smoke.

#### G01 Dedicated-Server Runtime Verification Checkpoint

The unsubmitted Ascent Rivals default changelist implements the approved server-owned half of G01:

- Every human competitor join and rejoin for a claimed StageRun calls Eventun; bots and
  spectator-only joins remain outside competitor admission.
- Explicit-field admissions preserve first-arrival ordering for provisional occupancy. Non-field
  admissions resolve independently and create no field occupancy.
- The first countdown request establishes one cutoff and coalesced lock operation. Later eligible
  arrivals cannot change occupancy; only the exact locked player may reconnect after acknowledgement.
- Candidate denial, transport failure, cancellation, pre-freeze disconnect, and registration
  expiry release provisional occupancy without failing the StageRun. A registration that misses
  the bounded window is disconnected before SnapNet player registration and becomes an explicit
  no-show in the immutable roster.
- Claim, recovered roster, `LOCKED`, and `ALREADY_LOCKED` responses receive complete semantic
  validation. Malformed local player or client identity rejects only that candidate.
- The dedicated server starts countdown only after one complete roster body and roster-lock UUID
  receive a validated acknowledgement.

The Development Editor target compiled successfully. All five
`AscentRivals.Eventun.GauntletRoster` automations passed without warnings or errors, and the Eventun
PostgreSQL smoke passed. The build also updated five existing read call sites to pass empty optional
season or StageRun filters, preserving their existing behavior and API names. The implementation
remains in the unsubmitted default changelist; no shared environment or production deployment is
claimed, and the player-connected combined runtime smoke remains part of the coordinated cutover
gate.

### G02 — Add Frozen Team Qualification

Depends on T01 membership intervals and G01.

- Implement in two reviewable passes controlled by the repository owner. Pass 1 adds closed
  historical-membership correction and the shared membership/projection serialization boundary;
  Pass 2 adds attribution, configuration, cutoff, and qualified-field integration. Each pass remains
  unstaged and uncommitted until its implementation review is accepted.
- Attribute complete-match performance to membership at `match_fact.started_at` and derive
  team/member scores from narrow match contributions, never current-roster joins over collapsed
  player totals.
- Configure individual scoring, team top-N aggregation, minimum contributors, and deterministic
  tie-breaks.
- Freeze selected teams, contributing members, exact match evidence, projection/configuration
  revision, and membership-attribution evidence at cutoff.
- Require explicit replacement when a repair changes unbound selection evidence; never mutate a
  field already bound to a run.
- Feed selected teams into the already proven G01 field, slot, roster-lock, and result path.

#### G02 Pass 1 Implementation-Review Checkpoint

The unstaged Eventun working tree implements only the approved correction prerequisite:

- Ordinary create, join, leave, remove, and disband membership boundaries take the ordered player
  serving-projection lock after team/player row locks and capture their millisecond timestamp with
  `clock_timestamp()` only after that lock. A repair that wins the lock observes no new membership;
  a membership mutation that wins is committed before the repair projects it.
- The Admin correction operation accepts a nonzero correction UUID, one exact retained interval,
  `VOID` or `REPLACE`, the ordinary semantic replacement payload, and a reason. Eventun canonicalizes
  UUIDs and enums and owns the SHA-256 semantic request hash. An exact retry returns the retained
  correction and replacement identity; changed semantic reuse returns `Aborted`.
- Only closed effective intervals may be retired. A replacement is also closed and must carry exact
  existing join/end actors and normal join/end reasons. Active intervals remain governed by normal
  membership operations and are rejected by both application and database constraints.
- Deferrable composite foreign keys permit one transaction to insert the correction identity,
  retire the exact old interval, insert an optional exact replacement, advance each affected team's
  roster revision once, and append exact correction-team and audit evidence. Old intervals remain
  addressable by historical snapshot foreign keys; `is_effective` excludes retired rows from future
  live attribution and overlap checks.
- Correction evidence and correction-team identities are immutable. Audit references prove the
  correction, team, and subject player agree, including corrections that move evidence across a
  team or player identity.
- The canonical and pending-delta Team replacement definitions remain byte-equivalent through the
  existing isolated pre-reconstruction proof. No authentic reconstruction, shared database,
  Ascentun, or Ascent Rivals change is part of this pass.

`./scripts/verify.sh` passed protobuf formatting, lint, generation, contract inventories, Go and Bun
tests, vet, and the linux/amd64 build. `./scripts/verify_schema.sh` passed canonical/delta parity,
the isolated replacement migration, schema and mutation contracts, the deterministic post-lock
timestamp race, cross-team replace and void correction, exact retry/change detection, effective-
history access plans, the existing mixed-operation races, and the full benchmark matrix. Strict
Knowledge Base validation and `git diff --check` also pass. No authentic reconstruction or shared
database was used. The owner accepted the implementation-review checkpoint on 2026-07-21 and the
reviewed Pass 1 implementation is committed as `3e1606c`; this establishes a local source baseline,
not shared-development or production deployment. Pass 2 remains a separate reviewable change.

#### G02 Pass 2 Implementation-Review Checkpoint

The unstaged Eventun working tree based on `3e1606c` implements the approved frozen-team-
qualification pass without changing Ascentun, Ascent Rivals, shared databases, or current-system
documentation:

- Server-authored canonical, unfiltered, non-bot match contributions resolve the effective
  membership interval at `match_fact.started_at` only after the ordered player serving lock. The
  exact team, player, membership interval, immutable membership semantic fingerprint, match event,
  and `server` source identity remain relational evidence. Sequence rows have composite constraints
  to that exact contribution identity; incremental ingestion and full rebuild use the same
  attribution. Contribution and sequence projection fingerprints include the membership semantic
  hash, so a membership-evidence change discovered during rebuild advances the projection revision.
- Team-qualification configuration is stage-scoped. Member-scoring identity excludes aggregate-only
  `top_n_members` and `minimum_contributors`; changing only those values rewrites only changed
  configuration rows and advances the gauntlet projection state once, without member-row rewrites or
  player locks. Configuration creation, removal, or member-scoring changes discover and lock the
  ordered player set, take the gauntlet lock, revalidate the set, and rebuild projections.
- Member ordering is qualification points, counted qualifiers, played qualifiers, total circuit
  points with null last, earliest final achievement, then UUID. Team aggregate score is the `BIGINT`
  sum of selected contributors' qualification points. Team ordering compares the complete
  contributor tuples—including each contributor's final-achievement time and player UUID—
  lexicographically, then contributor count descending after an equal shared prefix, team final
  achievement, and team UUID; competitive dense rank excludes only the final team UUID tiebreaker.
- Team qualification reuses the individual eligibility contract: the gauntlet stat must be
  `circuit_points`, and a member must satisfy the same `stat_top_k` qualifier-participation gate
  before contributor selection. Per-qualifier `qualifier_rank` is nevertheless computed over the
  full team-member qualifier population before top-N contributor filtering, so non-contributor
  members still participate in the competitive rank population.
- `top_n_members` must be positive. `minimum_contributors` defaults to one and must remain between one
  and top N. Team activity participates in cutoff resolution but does not rewrite member projection
  identity.
- Qualified selection uses the effective field capacity `min(max_competitors, max_lobby_size)`.
  Preview, candidate selection, the sealed cutoff `entry_limit`, and field publication therefore
  agree even when the competitor and lobby limits differ.
- Admin preview, publish, and replace expose immutable team cutoff evidence: selected teams,
  contributors, qualifier and match evidence, exact membership identities, projection/configuration
  versions and hashes, and deterministic ranks. Snapshot match evidence references the immutable
  event-identity ledger by exact event and batch rather than mutable compact facts, allowing fact
  repair without changing sealed history. Sealed snapshot and field identity is also independent of
  replaceable live stage and qualifier authoring rows. Callers supply a nonzero idempotency UUID and
  ordinary semantic payload; Eventun owns the SHA-256 request hash. Exact retries return retained
  state and changed semantic reuse returns `Aborted`. Field snapshots retain a non-cascading
  gauntlet identity foreign key without coupling to mutable stage authoring; hard deletion rejects a
  gauntlet with any immutable field history.
- Stage modes are mutually exclusive. An explicit configured-team field uses an opening `invite`
  stage and `gauntlet_stage_team`; a qualified-team field uses an opening `qualification` stage with
  team configuration and a current team cutoff but no configured teams. Both allocate through the
  existing G01 field, slot, claim, roster-lock, and result path. A team-qualified run cannot be
  claimed until that qualified field exists, and claim and active-run join status preserve the
  `team_qualification` entitlement source.
- Qualified-field publication freezes its cutoff, full configuration hash, selected team identities,
  ranks, scores, contributor counts, and final-achievement evidence. Later membership, match, repair,
  team disband, projection-revision, or cutoff-head changes do not invalidate a published field.
  Publication revalidates that every selected cutoff team is active, so a disbanded team cannot enter
  a newly published field. Cutoff-relevant configuration changes stale an unbound field; claim
  validates frozen identities and configuration without requiring the current live revision or
  cutoff head.
- Canonical SQL ownership remains singular: `c11` owns serving projections, `c12` owns the individual-
  cutoff assertion, and `c17` owns team qualification and cutoff functions. The production delta
  reinstalls exact canonical definitions after its unchanged historical prefix. Existing explicit
  fields backfill `allocation_source = 'explicit_team'` before the column becomes non-null, projector
  state promotes to `2/2`, and incompatible sealed individual cutoff evidence fails migration
  preflight rather than being reinterpreted. The full team-qualification configuration hash includes
  lobby limits, overflow policy, admission-priority rule, and roster-lock point as well as the
  scoring and aggregate settings.

`bun run gen` and `./scripts/verify.sh` passed protobuf formatting, lint, generation, API and
permission inventories, Go and Bun tests, vet, and the linux/amd64 build. `./scripts/verify_schema.sh`
passed canonical/delta parity, migration preflight and transition, deterministic contributor and team
ranking, individual stat and participation-rule reuse, full-population qualifier ranking, immutable
cutoff, membership, and field identities, sealed-cutoff compact-fact repair and authoring replacement,
qualified-field-required claim, active-team publication with post-publication freezing, correct
entitlement-source responses, membership-semantic closure/rebuild revisioning, asymmetric
competitor/lobby capacity, API and relational field-history deletion rejection, the real membership-
mutation versus ingestion race, publication/repair/full-rebuild serialization, populated access
plans, cold reads, and targeted/full rebuild parity. The latest populated team-cutoff candidate path
observed p95 92.348 ms under the
one-CPU disposable fixture, below its 100 ms gate. No authentic reconstruction or shared database was
used.

The owner accepted the Pass 2 implementation-review checkpoint on 2026-07-22 after the independent
database, functionality, and cross-consumer review found no remaining G02 correctness issue. The
reviewed implementation is committed as Eventun `1e3b76e`; this records a clean local source
baseline, not shared-development behavior or production deployment. Detailed Pass 2 behavior
remains in this initiative until deployment gates justify incorporation into current-system
knowledge. The unrelated stale G01 `ServerService` wording remains a separate cleanup.

### G03 — Add Priority Replacement And Roster Policies

Depends on the G01 runtime and approved team competition-rank behavior.

- Add the monotonic competition-roster revision to point-read admission and roster lock.
- Support configured first-come or strictly higher-priority pre-lock replacement; incumbents win
  ties.
- Release a provisional slot on disconnect. A returning player has no permanent claim and must
  still win under the current policy.
- Lock occupancy at the approved roster boundary and perform no automatic post-lock substitution
  in the first slice.
- Eventun returns eligibility, typed reason, explicit admission policy, exact field snapshot,
  applicable slot/team, presence-aware competition rank, and observed roster revision. The dedicated
  server alone serializes provisional occupancy and derives accept, replace, or reject from that
  evidence and its incumbent state.
- Claim binds one current field contract and its explicit policy; it does not exchange supported
  schema/algorithm pairs or maintain a compatibility matrix. Eventun, generated contracts, and the
  dedicated server change as one coordinated deployment unit.
- Qualified-team authoring defaults to `replace_lowest_prestart + team_member_rank` only when both
  values are absent. Explicit-team authoring defaults to `reject_new + first_come`. Those are the
  only supported pairs in this slice; other enumerated authoring policies fail closed.
- Each occupied lock entry carries the positive roster revision returned by admission; no-shows must
  omit it. A changed live revision returns `Aborted` without roster or lifecycle mutation. Exact
  committed lock retries return retained state before live revision validation, even if membership,
  rank, disband, or correction later advances the team revision.
- Verify the bounded AccelByte connection-capacity buffer needed for replacement in the later
  dedicated-server pass; Eventun does not change session capacity in this slice.
- Regenerate only the required ServerService, GameServer, shared Models, and client explanation
  contracts without widening authorization by code-generation convenience.
- Canonical schema permits first-come and team-rank field policies. The already-migrated development
  transition lives only in `migration/post_development_cutover.sql`; production applies the frozen
  historical migration first and this guarded delta second.
- Migrate, republish, or explicitly replace incompatible mutable and unbound field state rather than
  retaining a live compatibility branch. Preserve version evidence only where an immutable bound or
  sealed historical result requires its original interpretation.

#### G03 Implementation-Review Checkpoint

The Eventun G03 implementation passed local verification and implementation review and is committed
as `cb79df3`. This is accepted source evidence, not deployed behavior. No shared environment,
product repository outside Eventun, or frozen `migration/migration.sql` was modified.

The corrected protobuf contract follows AR-2026-019. Claim carries no supported-capability
collection, schema/algorithm handshake, omission fallback, or compatibility matrix. Team-rank
replacement uses the existing explicit and qualified field-version provenance; the explicit
`FIRST_COME` or `TEAM_COMPETITION_RANK` policy is the live domain contract. Same-session committed
claim retries return their retained exact field binding without a current-client compatibility
check, including after the mutable current field head changes.

Field-backed evaluations have one authoritative shape containing typed outcome, reason, policy,
exact snapshot, applicable slot/team, conditional rank, and roster revision. It is present for every
field-backed result, including denial and locked reconnect. The former admission summary no longer
contains field outcome, snapshot, or slot data and is returned only for genuinely non-field
admission.

Authoring defaults the two field policy values only when both are absent. A half-specified pair is
invalid; the two accepted complete pairs remain first-come and team-rank replacement. Roster lock
requires the admission-observed positive revision for occupied entries, forbids it for no-shows,
validates the exact live revision under ordered locks, and includes it in the server-owned semantic
hash. A first-time stale lock aborts atomically. An exact committed lock retry returns retained state
before live revision validation.

Focused tests cover both complete defaults, half-specified rejection, mutually exclusive
field/non-field response authority, missing rank, locked reconnect, exact claim retry after current
head replacement, revision/hash validation, and exact roster-lock retry after a later revision. A
real blocked two-session database regression proves concurrent rank/revision mutation cannot
partially lock or start the run and that reevaluation succeeds. Canonical schema verification proves
the guarded post-development delta converges to the canonical occupancy constraint. Its guard now
checks only the field table and exact old constraint; it has no unrelated serving-projection
generation dependency.

Reported verification:

- `go test ./internal/eventun`;
- `./scripts/verify.sh`;
- `./scripts/verify.sh unreal`, including deterministic generated SDK comparison;
- `./scripts/verify_schema.sh`, including field access plans and database-backed runtime races;
- `python tools/validate_kb.py --strict`;
- `git diff --check` in both changed repositories.

The AccelByte connection-capacity buffer and provisional occupancy/replacement execution remain for
the later dedicated-server pass. No authentic reconstruction rehearsal was run.

The owner accepted this implementation-review checkpoint after the focused follow-up confirmed all
five requested corrections: capability negotiation and algorithm generation 3 were removed,
committed claim retries again return retained state, field admission is separate from the non-field
summary, half-specified policy pairs fail, and the post-development delta no longer depends on
unrelated projection generation. The reviewed source was then committed as `cb79df3`.

### T03D — Add The Website Public Gauntlet Detail Projection

Implement this as a small Eventun companion slice while G04 proceeds. It is logically separate from
mixed-owner allocation and must retain its own implementation-review checkpoint, even if one coder
serializes the overlapping Eventun edits.

- Add subjectless Server `READ` access to a compact domain-neutral
  `GET /v1/public/gauntlet/{gauntlet_id}` projection.
- Return stable public identity, approved bounded media, occurrence facts, qualifiers, explicit
  player/team qualification ownership, a bounded recognized scoring metric, and visitor-facing
  stage/circuit structure with deterministic order and course-code fallback.
- Exclude creator identity, arbitrary authoring/runtime fields, current field-owner or racer-slot
  capacity, generic participant count, sponsor relationships, prizes/rewards, and administrative
  evidence. Existing current-field and exact StageRun-field reads remain authoritative for
  capacity.
- Replace clock-derived StageRun `UPCOMING` and `OPEN` presentation with factual bounded status
  mapped only from persisted run lifecycle. Website presentation continues to derive
  Current/Upcoming/Past from occurrence facts and its own clock.
- Distinguish an unknown gauntlet (`NotFound`) from a valid gauntlet with no StageRuns. Preserve
  sanitized `InvalidArgument`, `Internal`, and `Unavailable` mappings.
- Add generated-gateway dispatch tests proving the parameterized detail route cannot capture
  discovery, current-field, exact StageRun-field, StageRun-list, or exact-result routes.
- Regenerate and verify the normal public transport contracts without adding this Website read to
  the dedicated-server GameServer subset by convenience.
- Reuse existing normalized tables and bounded read patterns; add no schema, projection, cache, or
  compatibility generation unless a measured query requirement proves it necessary.
- Do not implement Website rendering, sponsor display, private player overlays, team-owned public
  standings, or bracket modules in this Eventun slice.

The complete response boundary and Website composition rules remain in the
[Website route/API matrix](../website-v2/route-api-matrix.md#gauntlet-detail-read-decomposition) and
[gauntlet-detail page specification](../website-v2/pages/gauntlet-detail.md).

### G04 — Add Mixed And Expanded Allocations

- Add explicit player owners, mixed-owner fields, community/sponsor labels, configured fallback,
  and unaffiliated-player fill through the same field resolver.
- Retain individual and team qualification as separate source rankings; never blend them into an
  implicit cross-owner score.
- Enable multiple team slots only with an explicit reproducible owner-result aggregation.
- Add operator preview, repair, and replacement for unbound fields.

### G05 — Add Durable Bracket State

Depends on stage-run-scoped results and approved owner-result semantics.

- Add bracket entries, seeds, matches, sides, byes, upstream winner/loser references, results,
  versions, and advancement.
- Start with single elimination, explicit seeds, byes, and manual repair; retain graph support for
  later loser routing without promising an automatic double-elimination preset.
- Publish the initial graph only after the field settles and keep accepted results and
  advancement stage-run scoped.
- Require audited void/replay or reassignment for already-started repair.

### G06 — Define Wildcard And Fallback Policies

- Define unaffiliated-player fill behavior and explicit sponsored/community team allocations.
- Decide whether Community CP is an authoritative team metric or an explicit curated assignment.
- Keep owner counts, slots per owner, fallback precedence, and display labels configurable.
- Do not add voting or persistent fan/rooting state.

### G07 — Add Minimal Administration

- Update Ascentun only for required team/gauntlet contract changes and bounded create/edit flows.
- Add cutoff preview/publish, explicit owner assignment, slot/roster controls, bracket authoring,
  void, replay, and repair with minimal interim styling.
- Keep progression configuration and operational diagnostics in the Eventun Extend App UI.
- Do not introduce pagination or a broader website redesign for these small operator views.

### G08 — Post-Teams Simplification And Technical-Debt Cleanup

Begin after the accepted teams and team-gauntlet delivery slices are complete enough to evaluate as
one system. This is a behavior-preserving simplification pass, not another compatibility program or
feature redesign.

- Inventory schema, payload, projection, algorithm, and API version fields plus compatibility
  branches across Eventun and its first-party consumers. Retain only immutable-history provenance or
  a named external-protocol requirement; migrate current data and remove unused negotiation paths.
- Trace representative API-to-database call paths and assign each input invariant to one owning
  boundary. Remove repeated field validation, normalization, sanity checks, fallbacks, and
  fingerprints from downstream layers that receive an already validated internal representation.
- Preserve authentication, authorization, untrusted-input validation, transaction-time concurrency
  checks, independently valuable database constraints, external-provider response validation, and
  irreversible-operation guards.
- Prefer typed validated values over repeated primitive-field conditionals. Consolidate shared
  behavior only when it makes the primary path easier to read; do not introduce a framework merely
  to remove duplicated lines.
- Use existing semantic, integration, race, and database tests to prove behavior and integrity.
  Add focused tests only for a boundary whose ownership was previously unclear.
- Report production-code lines added and removed separately from tests and generated artifacts.
  The intended result is fewer branches and a net reduction in maintained production code.
- Record each retained defensive or version check with its distinct failure model. A check that
  cannot identify one is a removal candidate.

## Explicitly Deferred

- Persistent rooting/fan state, team chat, and a team activity feed.
- Team-specific or asymmetric racer/supporter game modes.
- Spectator, shoutcaster, coach, or automatic post-lock substitute slots.
- Token-gated membership without a separately approved provider-neutral asset-source contract.
- Party-system changes beyond a conditional thin convenience invite.
- Full Website V2 visual work as part of the interim team administration slice.
- Team progression implementation before T08 approval.

## Remaining Before Closure

- Accept the coder-verified Ascentun Team Core implementation and exact generated-contract update
  through implementation review.
- Complete the shared-development Eventun cutover and combined runtime smoke before deploying or
  enabling the breaking Team Core unit.
- Implement, verify, and incorporate the selected later gauntlet behavior into current-system
  documents.
- Preserve later slices here until selected, superseded, rejected, or moved into a successor
  initiative.

## Related Knowledge

- [Teams program design](teams-solution-design.md)
- [Team experience and progression design](team-experience-and-progression-solution-design.md)
- [Team gauntlets and brackets design](team-gauntlets-and-brackets-solution-design.md)
- [Current team and gauntlet state](../../system/team-gauntlet-current-state.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
