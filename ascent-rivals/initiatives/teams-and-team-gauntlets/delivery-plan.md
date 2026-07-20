# Teams And Team Gauntlets Delivery Plan

Status: proposed
Status detail: The solution designs are retained, but T00 reapproval waits for the coordinated
Eventun shared-development cutover. Runtime hardening must complete before implementation.

Last consolidated: 2026-07-20

## Outcome And Boundary

Deliver the first useful team experience and then extend the cohesive gauntlet model with team
qualification, concrete competition slots, runtime roster enforcement, and brackets.

This plan defines work order and completion boundaries. The detailed product and technical
contracts remain in the linked solution designs. It does not treat proposed behavior as current
system state or authorize production deployment.

## Program Gates

| Gate | Required before |
|---|---|
| Coordinated Eventun shared-development cutover | T00 design refresh and reapproval |
| Runtime resource and service-boundary hardening | T01/T02 and all other team implementation |
| T00 selection of the initial delivery cutoff | Starting either implementation workstream |
| Canonical team identity and membership intervals | Historical team statistics, progression attribution, or team qualification |
| Notification payload prototype and outbox contract | Closed-team actionable notifications |
| Approved progression definition | Team XP, levels, caps, challenges, or unlock implementation |
| Concrete competition field and slot model | Mixed allocation and dedicated-server team-seat enforcement |
| Stage-run-scoped result identity | Multiple bracket matches using one logical stage |

The prerequisite execution details are maintained in
[Eventun Development Cutover And Runtime Hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md).

## T00 — Refresh And Reapprove The Team Designs

Depends on the successful shared-development cutover. Runtime hardening may proceed in parallel.

- Reconcile all three team designs with the implemented authentication, API generation, match
  ingestion, facts, serving projections, cutoff snapshots, seasons, repair, and migration
  boundaries.
- Revalidate the capability matrix against the actual schema and approve the initial
  individual, team, mixed-owner, invitation, qualification, and bracket use cases.
- Resolve the first-slice product decisions for progression, notification delivery, cosmetics,
  wildcard/fallback policy, competition slots, roster priority, and team result aggregation.
- Decide whether existing pre-alpha team, membership, invitation, and request state is migrated
  deterministically or discarded before replacement writes are enabled.
- Capture the current game-client team/social/lobby/profile/gauntlet routes, navigation graph,
  widget hierarchy, and screenshots. Produce controller-first Pencil designs before adding new
  game-client team routes.
- Select the exact team-experience and team-gauntlet delivery cutoffs and explicit exclusions.

T00 completes when the first implementation slice has approved contracts, UI flows, owner
decisions, dependencies, and verification boundaries.

## Team Experience Workstream

### T01 — Replace Team Identity And Membership State

Depends on T00 and completed runtime hardening.

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
  lock affected team/membership/pending rows, and commit state, audit, and notification intent
  atomically.
- Enforce expiry, renewal, idempotent repeat behavior, and transactional consumption or
  cancellation of pending state across membership-mode, removal, transfer, and disband races.
- Expose approved recruiting region, IANA time zone, recruiting status, and allowlisted Twitch or
  Discord links. Keep editing on the website.
- Defer server pagination and text search until measured team count, roster size, payload, or
  latency requires them.

### T03 — Add Fact-Backed Team Views

Depends on T01 membership intervals and the relevant T02 public read contracts.

- Add public team-filtered roster statistics, bounded roster comparison, and approved team
  leaderboard/history reads.
- Attribute historical performances to membership at trusted performance time rather than the
  current roster.
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

Depends on the T02 contract and the T00 controller-first design checkpoint.

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

### G01 — Publish A Unified Competition Field And Concrete Slots

- Retain individual cutoff snapshots as source-specific selection evidence.
- Publish one ordered field whose owners are players or teams and whose sources are qualification,
  explicit assignment, bracket advancement, or configured fallback.
- Expand each owner into concrete player-owned or team-owned stage-run racer slots.
- Keep sponsor, community, and wildcard as allocation policy or display labels rather than owner
  types.

### G02 — Add Frozen Team Qualification And Roster Control

Depends on T01 membership intervals and G01.

- Attribute performance to membership at trusted performance time and derive team/member scores
  from narrow match contributions, never current-roster joins over collapsed player totals.
- Configure individual scoring, team top-N aggregation, fixed slots per owner, deterministic
  tie-breaks, and the first approved roster priority policy.
- Freeze selected teams, contributing members, exact match evidence, projection/configuration
  revision, and membership-attribution evidence at cutoff.
- Require explicit replacement when a repair changes unbound selection evidence; never mutate a
  field already bound to a run.

### G03 — Extend Dedicated-Server Runtime Contracts

Depends on G01 and the approved G02 policies.

- Extend claim, admission, match acceptance, and completion with field, slot, owner, occupancy,
  roster-version, and lock context.
- Regenerate the existing service-specific Unreal GameServer and shared Client/Server Models
  surfaces without duplicating operations for authorization.
- Make accepted matches and results stage-run scoped and idempotent.
- Enforce Eventun Server permission on every dedicated-server runtime operation.

### G04 — Implement Pre-Start Slot Replacement

Depends on G03.

- Resolve eligibility and priority through an indexed point read against the frozen field.
- Support configured first-come or strictly higher-priority pre-lock replacement; incumbents win
  ties.
- Release a provisional slot on disconnect. A returning player has no permanent claim and must
  still win under the current policy.
- Lock occupancy at the approved roster boundary and perform no automatic post-lock substitution
  in the first slice.
- Return explicit allow, replace, reject, and reason responses and verify the bounded AccelByte
  connection-capacity buffer needed for replacement.

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

- Complete the shared-development Eventun cutover and runtime hardening gates.
- Complete T00 and select the exact first delivery cutoff.
- Implement, verify, and incorporate the selected team-experience and gauntlet behavior into
  current-system documents.
- Preserve later slices here until selected, superseded, rejected, or moved into a successor
  initiative.

## Related Knowledge

- [Teams program design](teams-solution-design.md)
- [Team experience and progression design](team-experience-and-progression-solution-design.md)
- [Team gauntlets and brackets design](team-gauntlets-and-brackets-solution-design.md)
- [Current team and gauntlet state](../../system/team-gauntlet-current-state.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
