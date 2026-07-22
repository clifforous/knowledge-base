# Teams And Team Gauntlets Delivery Plan

Status: in-progress
Status detail: T00 is approved against the committed local Eventun foundation. Team Core is the
selected first implementation cutoff. The Eventun implementation based on `9213feb` passed local
verification and implementation review and is committed as `c4260f3`; the staged Ascentun working
tree implementation based on `a0a40ad` has passed implementation review but is not committed.
A bounded fresh-database local smoke passed for the public Team reads, authentication boundaries,
Ascentun proxies, and empty directory render; player-authenticated mutation smoke remains pending.
The Eventun G01 field, slot, roster-lock, and result foundation passed implementation review and is
committed as `6343438`. The unsubmitted Ascent Rivals default changelist implements the G01
dedicated-server integration and passed its Development Editor build, focused roster automations,
Eventun PostgreSQL smoke, and implementation review. Coordinated deployment remains gated by
source-control decisions, the shared-development cutover, and combined runtime smoke.
Eventun G02 Pass 1 closed-membership correction passed implementation review and is committed as
`3e1606c`. The unstaged Eventun G02 Pass 2 working tree implements frozen team qualification and
has passed coder verification; it is awaiting implementation review and is not deployed.

Last consolidated: 2026-07-21

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
| Coordinated Eventun shared-development cutover and combined runtime smoke | Deploying or enabling the combined T01/T02 implementation in shared development |
| T00 selection of the initial delivery cutoff | Starting either implementation workstream |
| Canonical team identity and membership intervals | Historical team statistics, progression attribution, or team qualification |
| Notification payload prototype and outbox contract | Closed-team actionable notifications |
| Approved progression definition | Team XP, levels, caps, challenges, or unlock implementation |
| Concrete competition field and slot model | Mixed allocation and dedicated-server team-seat enforcement |
| Stage-run-scoped result identity | Multiple bracket matches using one logical stage |

The prerequisite execution details are maintained in
[Eventun Development Cutover And Runtime Hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md).

## T00 — Refresh And Reapprove The Team Designs

T00 was approved against the committed local foundation and retained migrated database. Local
Eventun implementation and isolated verification may proceed before the coordinated cutover.
Before the combined Eventun and Ascentun implementation is enabled in shared development,
reconfirm affected contracts and runtime assumptions; do not repeat the entire design checkpoint
solely because deployment occurred later.

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

- Add public team-filtered roster statistics, bounded roster comparison, and approved team
  leaderboard/history reads.
- Attribute complete-match performances to membership at canonical MatchStart
  (`match_fact.started_at`) rather than the current roster.
- Do not invent a generic team score by summing current members' lifetime careers.
- Prefer bounded SQL over mutable aggregate state; add an incremental projection only when
  representative plans show it is required.

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
  exact team, player, membership interval, match fact, and `server` source identity remain relational
  evidence; incremental ingestion and full rebuild use the same attribution.
- Team-qualification configuration is stage-scoped. Member-scoring identity excludes aggregate-only
  `top_n_members` and `minimum_contributors`; changing only those values rewrites only changed
  configuration rows and advances the gauntlet projection state once, without member-row rewrites or
  player locks. Configuration creation, removal, or member-scoring changes discover and lock the
  ordered player set, take the gauntlet lock, revalidate the set, and rebuild projections.
- Member ordering is qualification points, counted qualifiers, played qualifiers, total circuit
  points with null last, earliest final achievement, then UUID. Team aggregate score is the `BIGINT`
  sum of selected contributors' qualification points. Team ordering compares contributor tuples
  lexicographically, then contributor count descending after an equal shared prefix, team final
  achievement, and UUID; competitive dense rank excludes the UUID tiebreaker.
- `top_n_members` must be positive. `minimum_contributors` defaults to one and must remain between one
  and top N. Team activity participates in cutoff resolution but does not rewrite member projection
  identity.
- Admin preview, publish, and replace expose immutable team cutoff evidence: selected teams,
  contributors, qualifier and match evidence, exact membership identities, projection/configuration
  versions and hashes, and deterministic ranks. Callers supply a nonzero idempotency UUID and ordinary
  semantic payload; Eventun owns the SHA-256 request hash. Exact retries return retained state and
  changed semantic reuse returns `Aborted`.
- Stage modes are mutually exclusive. An explicit configured-team field uses an opening `invite`
  stage and `gauntlet_stage_team`; a qualified-team field uses an opening `qualification` stage with
  team configuration and a current team cutoff but no configured teams. Both allocate through the
  existing G01 field, slot, claim, roster-lock, and result path.
- Qualified-field publication freezes its cutoff, full configuration hash, selected team identities,
  ranks, scores, contributor counts, and final-achievement evidence. Later membership, match, repair,
  projection-revision, or cutoff-head changes do not invalidate a published field. Cutoff-relevant
  configuration changes stale an unbound field; claim validates frozen identities and configuration
  without requiring the current live revision or cutoff head.
- Canonical SQL ownership remains singular: `c11` owns serving projections, `c12` owns the individual-
  cutoff assertion, and `c17` owns team qualification and cutoff functions. The production delta
  reinstalls exact canonical definitions after its unchanged historical prefix. Existing explicit
  fields backfill `allocation_source = 'explicit_team'` before the column becomes non-null, projector
  state promotes to `2/2`, and incompatible sealed individual cutoff evidence fails migration
  preflight rather than being reinterpreted.

`bun run gen` and `./scripts/verify.sh` passed protobuf formatting, lint, generation, API and
permission inventories, Go and Bun tests, vet, and the linux/amd64 build. `./scripts/verify_schema.sh`
passed canonical/delta parity, migration preflight and transition, deterministic contributor and team
ranking, immutable cutoff and field identities, the real membership-mutation versus ingestion race,
publication/repair/full-rebuild serialization, populated access plans, cold reads, and targeted/full
rebuild parity. The populated team-cutoff candidate path observed p95 between 62.767 ms and 68.102 ms
under the one-CPU disposable fixture, below its 100 ms gate. No authentic reconstruction or shared
database was used.

This is coder verification, not implementation-review acceptance, source-control completion, or
deployment. Detailed Pass 2 behavior remains in this initiative until the owner accepts the
implementation review and directs incorporation into current-system knowledge. The unrelated stale
G01 `ServerService` wording remains a separate cleanup.

### G03 — Add Priority Replacement And Roster Policies

Depends on the G01 runtime and approved team competition-rank behavior.

- Add the monotonic competition-roster revision to point-read admission and roster lock.
- Support configured first-come or strictly higher-priority pre-lock replacement; incumbents win
  ties.
- Release a provisional slot on disconnect. A returning player has no permanent claim and must
  still win under the current policy.
- Lock occupancy at the approved roster boundary and perform no automatic post-lock substitution
  in the first slice.
- Return explicit allow, replace, reject, and reason responses and verify the bounded AccelByte
  connection-capacity buffer needed for replacement.
- Regenerate only the required ServerService, GameServer, shared Models, and client explanation
  contracts without widening authorization by code-generation convenience.

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
