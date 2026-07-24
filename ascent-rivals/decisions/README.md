# Ascent Rivals Decision Log

## Purpose

Record concise, durable changes in direction without duplicating the current system
description.

Entries record the decision and its disposition. Linked current-system documents remain the
authority for how the system works now; linked archived designs preserve deeper rationale.

## Entry Shape

Each future entry should include a stable identifier and date, what changed from X to Y,
the rationale, affected documents, supporting evidence or task-log entries, and any later
superseding decision.

Future task-owned decision and delta logs may live under `tasks/`. Pending entries are
evidence and must not be presented as current truth before incorporation.

## Decisions

### AR-2026-001 — One identified complete-match ingest contract

- **Date:** 2026-07-13
- **Status:** Implemented in the known local-development state; production cutover remains
  separately gated.
- **Changed:** From fragmented or source-specific event submission toward one identified
  complete-match envelope submitted through shared `ClientService.IngestMatch` by both player
  and dedicated-server producers.
- **Why:** Stable batch/event identity, canonical hashing, producer ordering, derived source
  trust, and equal-content idempotency provide one repairable contract without duplicating
  APIs for authorization classes.
- **Affected knowledge:** [identified match ingestion](../system/eventun/identified-match-ingestion.md),
  [Eventun interface architecture](../system/eventun/interface-architecture.md),
  [game client](../system/game-client.md), and
  [gauntlet runtime](../system/eventun/gauntlet-stage-runtime-contract.md).
- **Evidence:** [foundation/API review](../sources/analysis/eventun-foundation-api-simplification-review.md).

### AR-2026-002 — Product seasons are separate from telemetry storage lifecycle

- **Date:** 2026-07-17
- **Status:** Season catalog and season-aware serving implemented locally; retention and
  archive choices remain open.
- **Changed:** From a proposed general competition-period/storage concept to explicit
  Eventun-owned product seasons while storage segments, retention tiers, game builds, Season
  Pass, and MMR ownership remain independent concepts.
- **Why:** Product comparison windows and physical data lifecycle have different owners and
  change at different rates.
- **Affected knowledge:** [identified match ingestion](../system/eventun/identified-match-ingestion.md),
  [data model](../system/eventun/data-model.md), and the active
  [telemetry lifecycle plan](../initiatives/eventun-foundation/eventun-telemetry-lifecycle-plan.md).
- **Evidence:** [insights/progression/seasons review](../sources/analysis/eventun-insights-progression-seasons-review.md).

### AR-2026-003 — Progression runtime uses immutable published snapshots

- **Date:** 2026-06-16
- **Status:** Incorporated into the known local-development state; operator UI follow-through
  remains active.
- **Changed:** From goal-version activation and row-level active flags as the runtime model to
  editable drafts plus immutable published goal and challenge-pool snapshots.
- **Why:** Later authoring edits must not rewrite assignments, completion history, or reward
  semantics already presented to players.
- **Affected knowledge:** [progression](../system/eventun/progression.md),
  [data model](../system/eventun/data-model.md), and the active
  [progression initiative](../initiatives/eventun-progression/README.md).
- **Evidence:** [archived progression design set](../archive/initiatives/eventun-progression/README.md).

### AR-2026-004 — Recommendations became backend-owned Insights

- **Date:** 2026-04-03
- **Status:** Backend and manual game-client integration implemented locally; automatic
  pre-summary presentation remains open.
- **Changed:** From recommendation endpoints and a recommendation-only player concept to typed
  Insights that can return coaching, kudos, no insight, pending, unavailable, or failed.
- **Why:** The system needs to praise strong play, suppress low-credibility advice, and expose
  readiness explicitly while keeping selection policy in Eventun and localization in the
  client.
- **Affected knowledge:** [post-match insights](../system/eventun/post-match-insights-rollout.md)
  and [automatic presentation](../initiatives/post-match-insights/automatic-pre-summary-presentation.md).
- **Evidence:** [archived Insights designs](../archive/initiatives/post-match-insights/README.md).

### AR-2026-005 — Gauntlet stages use durable runs and explicit match acceptance

- **Date:** 2026-05-06
- **Status:** Eventun orchestration and first game-server pass implemented locally; runtime
  validation and listed gaps remain open.
- **Changed:** From implicit stage/session lifecycle assumptions to durable stage-run identity,
  per-match acceptance, and explicit aggregate run completion.
- **Why:** Multi-match stages, recovery, idempotency, participation, and final standings require
  Eventun-owned durable state rather than session presence or admission rows.
- **Affected knowledge:** [gauntlet runtime contract](../system/eventun/gauntlet-stage-runtime-contract.md)
  and [team gauntlet current state](../system/team-gauntlet-current-state.md).
- **Evidence:** [archived orchestration and server plans](../archive/initiatives/gauntlet-runtime/README.md).

### AR-2026-006 — Provider-specific team token gating was removed

- **Date:** 2026-07-13
- **Status:** Implemented in the known local-development state.
- **Changed:** From the TapTools-shaped token catalog, team gate relations, and `token_gated`
  membership mode to no token-gated mode; existing gated teams transition to invite-only.
- **Why:** A provider-specific asset contract should not be embedded in the foundational team
  model. A provider-neutral asset-source design is required before reintroduction.
- **Affected knowledge:** [Eventun interface architecture](../system/eventun/interface-architecture.md),
  [data model](../system/eventun/data-model.md), [game client](../system/game-client.md), and
  [team current state](../system/team-gauntlet-current-state.md).
- **Evidence:** [foundation/API review](../sources/analysis/eventun-foundation-api-simplification-review.md).

### AR-2026-007 — Coordinate development cutover with the game-client mainline

- **Date:** 2026-07-19
- **Status:** Fulfilled for shared development on 2026-07-23; production remains unscheduled.
- **Changed:** From applying the accepted Eventun migration as soon as its local rehearsal passed
  to waiting until the coordinated game-client API changes complete their next copy to main,
  then migrating the development database and service together.
- **Why:** The combined identified-match and season foundation should soak in development before
  production, but migrating Eventun first would create an avoidable shared-development
  service/client mismatch. The successful local rehearsal and retained snapshot make an earlier
  shared mutation unnecessary.
- **Affected knowledge:** [development cutover and runtime hardening](../initiatives/eventun-foundation/development-cutover-and-runtime-hardening.md),
  [teams delivery plan](../initiatives/teams-and-team-gauntlets/delivery-plan.md), and the
  [teams program design](../initiatives/teams-and-team-gauntlets/teams-solution-design.md).
- **Evidence:** [season and retained-data review](../sources/analysis/eventun-insights-progression-seasons-review.md)
  records the accepted local rehearsal and the still-pending development cutover.

### AR-2026-008 — Website V2 is one greenfield Next.js/React replacement

- **Date:** 2026-07-15
- **Status:** Approved initiative direction; implementation and deployment remain pending.
- **Changed:** From considering reuse of the existing sites or an alternate Nuxt/Svelte-style
  stack to one new Next.js/React/TypeScript application that replaces the marketing site and
  approved public/player Ascentun behavior.
- **Why:** The familiar stack provides the clearest maintainability, designer-to-code, AI-coder,
  review, Vercel, authentication, and data-heavy page workflow without coupling the new product
  structure to either legacy implementation.
- **Affected knowledge:** [Website V2 initiative](../initiatives/website-v2/README.md),
  [unified design](../initiatives/website-v2/unified-design.md), and
  [initial-release scope](../initiatives/website-v2/initial-release-scope.md).
- **Evidence:** The approved framework and replacement boundary are consolidated in the linked
  initiative documents; the [current website document](../system/website.md) records the two
  existing surfaces being replaced.

### AR-2026-009 — Website V2 excludes wallet and Accountun reward workflows

- **Date:** 2026-07-15
- **Status:** Approved initial-release boundary; future redesign remains possible.
- **Changed:** From treating wallet, token-gating, prize, and reward behavior as potential
  Ascentun parity to excluding wallet management, Cardano/Midnight wallet support, token gates,
  and every Accountun-driven prize/reward workflow or link from Website V2.
- **Why:** Those capabilities lack an approved product and ownership boundary and are not needed
  for the initial public website. Partial migration would expose confusing or unsafe state while
  delaying the replacement release.
- **Affected knowledge:** [initial-release scope](../initiatives/website-v2/initial-release-scope.md),
  [delivery plan](../initiatives/website-v2/delivery-plan.md), and the
  [archived wallet flow](../archive/initiatives/website-v2/wallet-linking.md).
- **Evidence:** The active scope excludes the workflows explicitly; the archived flow preserves
  the superseded design without presenting it as current intent.

### AR-2026-010 — Sponsor administration moves to the Eventun Extend App

- **Date:** 2026-07-17
- **Status:** Approved cutover boundary; Extend App implementation remains required.
- **Changed:** From preserving public-site sponsor registry/detail/CRUD routes to keeping only
  bounded gauntlet-context sponsor display and authoring selection in Website V2 while moving
  administrator registry and media operations to the Eventun Extend App.
- **Why:** Sponsor administration is restricted operational work, while public Website V2 needs
  only the approved identity and campaign presentation associated with a gauntlet. Separating
  the surfaces avoids creating public sponsor routes or duplicating administration.
- **Affected knowledge:** [sponsor-administration handoff](../initiatives/website-v2/sponsor-administration-handoff.md),
  [gauntlet authoring](../initiatives/website-v2/flows/gauntlet-authoring.md), and
  [Website V2 delivery](../initiatives/website-v2/delivery-plan.md).
- **Evidence:** The handoff defines the required Eventun contract, upload, preservation, and
  cutover acceptance boundaries.

### AR-2026-011 — Website V2 uses a purpose-built race-control language

- **Date:** 2026-07-20
- **Status:** Approved design direction; implementation and final visual-system promotion remain
  pending.
- **Changed:** From faux scrap-metal terminal styling and varied sci-fi panel geometry to one
  matte-graphite race-control field with restrained signal lighting, consistent corner rules,
  sparse directional marks, and grit supplied primarily by world imagery and atmosphere.
- **Why:** Simulated metal, random border fragments, and repeated cutouts made composed pages
  noisy and gimmicky. The revised language preserves the in-world terminal character while
  keeping repeated content readable and implementable in CSS and SVG.
- **Affected knowledge:** [Design Language v0.2](../initiatives/website-v2/design-language-v0.2.md),
  [Terminal Ops design system](../initiatives/website-v2/terminal-ops-design-system.md), and the
  [Website V2 initiative checkpoint](../initiatives/website-v2/README.md#current-design-checkpoint).
- **Evidence:** The owner-reviewed external Pencil checkpoints summarized by the affected
  initiative documents.

### AR-2026-012 — Public pilot profiles use a bounded career surface

- **Date:** 2026-07-20
- **Status:** Approved initial public-profile direction; authorized own-profile additions remain
  undecided and unimplemented.
- **Changed:** From a broad public career and recognition surface to public Matches, Podiums,
  Podium Rate, Ascension Rate, course performance, bounded recent races, and the three gauntlets
  with the pilot's latest activity. Broader totals, play time, economy, achievements, and medals
  became reversible own-profile candidates.
- **Why:** The bounded public surface provides useful competitive context without publishing
  every available account or progression measure. Any later private detail requires an
  authorized response rather than browser-side hiding.
- **Affected knowledge:** [Player profile specification](../initiatives/website-v2/pages/player-profile.md),
  [initial-release scope](../initiatives/website-v2/initial-release-scope.md), and the
  [route/API matrix](../initiatives/website-v2/route-api-matrix.md).
- **Evidence:** The reviewed player-profile desktop/mobile calibration and its incorporated
  initiative checkpoint.

### AR-2026-013 — Course discovery and course records use separate routes

- **Date:** 2026-07-20
- **Status:** Approved responsive information architecture; implementation remains pending.
- **Changed:** From an embedded course selector, archive scope, local directory search, and
  cross-course summary concepts to a simple published-course directory at `/courses` and one
  focused record surface at `/courses/[code]`. Course changes use ordinary route navigation.
- **Why:** A persistent selector crowded both desktop and mobile detail layouts, while the small
  course catalog and persistent global search make another page-local search unnecessary.
  Separating discovery from records keeps each route coherent and prevents accidental
  cross-course comparison of unlike times.
- **Affected knowledge:** [Course leaderboards specification](../initiatives/website-v2/pages/course-leaderboards.md),
  [information architecture](../initiatives/website-v2/information-architecture.md), and the
  [route/API matrix](../initiatives/website-v2/route-api-matrix.md).
- **Evidence:** The reviewed course directory/detail desktop/mobile calibrations, faceted-selection
  state study, and the Website V2 initiative delivery checkpoint.

### AR-2026-014 — Team Core replaces the pre-alpha team model

- **Date:** 2026-07-20
- **Status:** Approved contract deployed to shared development on 2026-07-23; production remains
  pending.
- **Changed:** From disposable team rows, delete-on-leave membership, numeric designation,
  nonhistorical requests/invitations, and caller-shaped identity to Eventun-generated durable team
  identity, retained active/disbanded lifecycle, half-open membership intervals, explicit owner,
  separate presentation title/capabilities/competition rank, a bounded configurable roster, exact
  versioned pending-action identity, and breaking replacement of the pre-alpha contract and data.
- **Why:** The old shape cannot preserve membership-at-event-time evidence, cleanly separate social
  presentation from authority, or support future team qualification and roster snapshots. The
  retained UUID and interval model supplies that foundation without preserving disposable alpha
  compatibility.
- **Affected knowledge:** [Teams initiative](../initiatives/teams-and-team-gauntlets/README.md),
  [delivery plan](../initiatives/teams-and-team-gauntlets/delivery-plan.md), and
  [team experience design](../initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design.md).
- **Evidence:** The owner accepted the T00 checkpoint, selected Team Core as the first delivery
  cutoff, approved a default maximum active roster of 16, approved durable disbanded identity and
  case-insensitive active-name/tag reuse, and accepted the three-capability boundary. Acceptance is
  a design/status decision, not implementation or deployment evidence.

### AR-2026-015 — Local Team Core implementation may precede shared-development cutover

- **Date:** 2026-07-20
- **Status:** Fulfilled for shared development on 2026-07-23; production deployment remains
  pending.
- **Changed:** From treating the coordinated Eventun foundation cutover as a prerequisite for all
  team implementation to allowing local Team Core implementation and isolated verification
  against committed Eventun `9213feb`. The cutover and combined runtime smoke remain mandatory
  before enabling the breaking Eventun and Ascentun contract in shared development.
- **Why:** The committed local foundation is sufficient for productive implementation work, while
  keeping deployment coupled avoids creating a shared service/client mismatch before the pending
  game-client API changes reach mainline.
- **Affected knowledge:** [Eventun cutover and hardening](../initiatives/eventun-foundation/development-cutover-and-runtime-hardening.md),
  [teams initiative](../initiatives/teams-and-team-gauntlets/README.md), and the
  [teams delivery plan](../initiatives/teams-and-team-gauntlets/delivery-plan.md).
- **Evidence:** The owner explicitly chose to continue local development while deferring the shared
  migration and later confirmed that Team Core implementation could start. This does not imply
  deployment, production readiness, or acceptance of an unreviewed implementation artifact.

### AR-2026-016 — Azure development cutover may retain unlimited backend temporary files

- **Date:** 2026-07-22
- **Status:** Approved exception exercised by the successful shared-development cutover;
  production remains pending.
- **Changed:** From requiring the historical runner to install the rehearsed 14 GiB session-local
  `temp_file_limit` on every target to accepting Azure's effective `-1` value only when PostgreSQL
  rejects that setting with `42501`. The independent 28 GiB physical-storage monitor remains the
  enforced cutover stop and records the unlimited effective value in evidence.
- **Why:** Azure Database for PostgreSQL owns this superuser-scoped parameter and rejects the
  operator session change. The first guarded invocation failed before migration work and rolled
  back safely; the owner chose not to change Azure's server-level `-1` setting.
- **Affected knowledge:** [Eventun cutover and hardening](../initiatives/eventun-foundation/development-cutover-and-runtime-hardening.md)
  and [identified match ingestion](../system/eventun/identified-match-ingestion.md).
- **Evidence:** The owner accepted the Azure-specific `-1` behavior after the guarded Step 6 error.
  The later guarded shared-development migration completed successfully; this does not authorize
  production.

### AR-2026-017 — Freeze the historical production delta after development cutover

- **Date:** 2026-07-23
- **Status:** Active temporary migration policy until production cutover cleanup.
- **Changed:** From appending every pending transition to `migration/migration.sql` to freezing that
  file as the historical transition already consumed by shared development. Database changes
  authored afterward accumulate in the separately ordered
  `migration/post_development_cutover.sql`; production applies the historical delta first and the
  post-development delta second.
- **Why:** Production still starts from the older schema. Mixing later changes into the historical
  delta could reproduce the ordering defects exposed during development or make development and
  production execute materially different transitions.
- **Affected knowledge:** [Eventun cutover and hardening](../initiatives/eventun-foundation/development-cutover-and-runtime-hardening.md),
  [foundation delivery snapshot](../initiatives/eventun-foundation/README.md), and the Eventun
  historical cutover runbook.
- **Evidence:** The owner reported that the guarded development migration completed successfully
  and that Eventun, Ascentun, and the game client are deployed in development. This decision records
  sequencing only; it does not imply production approval. After successful production migration and
  observation, both consumed transition files and the historical machinery are removed and the
  repository returns to one `migration/migration.sql`.

### AR-2026-018 — Public gauntlet timing is derived from occurrence facts

- **Date:** 2026-07-23
- **Status:** Eventun source correction is committed as `0e4d656`; the compatible Website V2
  correction passed verification and implementation review and is committed as `7d1d00c`.
  Coordinated deployment remains pending.
- **Changed:** From Website V2 consuming Eventun's query-time `timing_state`, active, next,
  latest-ended, and additional-occurrence summaries to consuming occurrence facts and deriving
  clock-relative presentation itself. SSR uses a fresh Website-server presentation timestamp;
  hydration shares that timestamp, then the browser advances it monotonically and recalculates at
  boundaries and visibility changes without a boundary-only refetch. Eventun's response timestamp
  remains transport/as-of metadata and is not the Website presentation clock.
- **Why:** The snapshot summaries become stale as soon as cached time crosses a boundary and do not
  represent durable Eventun state. The complete collection is already small enough for
  deterministic local classification, including choosing the active occurrence ending soonest.
- **Affected knowledge:** [Gauntlets index specification](../initiatives/website-v2/pages/gauntlets-index.md),
  [Website non-functional baseline](../initiatives/website-v2/non-functional-baseline.md), and the
  [teams/T03 delivery plan](../initiatives/teams-and-team-gauntlets/delivery-plan.md).
- **Evidence:** The owner accepted Website temporal ownership after reviewing the discovery
  response's query-time semantics. Eventun `0e4d656` removes the five presentation fields and keeps
  response time only as transport/as-of metadata. Website revision `7d1d00c` accepts both response
  generations, excludes Eventun time from factual cache and presentation, and derives initial state
  from one fresh Website-server timestamp. Its verification and independent implementation review
  found no blocking defect. Neither correction is claimed deployed.

### AR-2026-019 — First-party contracts use coordinated replacement and data migration

- **Date:** 2026-07-23
- **Status:** Approved project-wide engineering policy; applied in reviewed Eventun commit
  `cb79df3`.
- **Changed:** From considering runtime schema/algorithm capability negotiation and retaining
  multiple compatible first-party shapes to changing Eventun, generated contracts, the game client,
  Ascentun, and websites as one coordinated deployment unit. Mutable state is migrated to the
  current model. Per-table schema versions, compatibility matrices, parallel endpoints, and
  duplicate response generations are not added by default.
- **Why:** These components are controlled and deployed together. Maintaining combinations that
  will not be operated adds code, tests, failure modes, and rollout ceremony without useful product
  value. A one-time data migration is simpler and preserves one authoritative current model.
- **Boundary:** Immutable historical events, sealed snapshots, or derived evidence may retain the
  exact version needed to interpret or reproduce past results. External protocols and a genuinely
  independently deployed consumer may also justify a narrow exception. Historical provenance must
  not become a live compatibility handshake, and every exception must name the concrete need.
- **Affected knowledge:** [Ascent Rivals overview](../system/overview.md),
  [Eventun interface architecture](../system/eventun/interface-architecture.md),
  [Eventun data model](../system/eventun/data-model.md), [team gauntlet design](../initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design.md),
  and [G03 delivery plan](../initiatives/teams-and-team-gauntlets/delivery-plan.md).
- **Evidence:** The owner explicitly rejected version matrices and per-table schema versions,
  confirmed coordinated first-party deployment as the norm, and preferred data migration over
  backward-compatibility machinery. The corrected G03 implementation removed claim-time capability
  negotiation and algorithm generation 3, passed implementation review, and was committed as
  `cb79df3`; deployment is not implied.

### AR-2026-020 — Internal validation has one owner and simplicity is measurable

- **Date:** 2026-07-23
- **Status:** Approved engineering policy; post-teams cleanup planned as G08.
- **Changed:** From treating repeated validation, sanity checks, fingerprints, and defensive
  branches at every internal layer as inherently safer to validating and normalizing once at the
  owning trust boundary, then relying on typed internal contracts. Production-code size and branch
  count are explicit design concerns.
- **Why:** Rechecking the same already-established fact through API, service, database adapter, SQL
  function, and other internal layers increases lines of code, obscures the primary behavior, and
  creates inconsistent error paths without addressing a new threat. Focused tests and one
  authoritative invariant owner provide clearer assurance.
- **Boundary:** External inputs, authentication and authorization, provider responses,
  concurrency-sensitive transaction checks, durable database constraints, historically distinct
  retained data, and irreversible operations remain independently guarded. A later check remains
  valid when the layer is independently reachable or can observe a new failure mode.
- **Affected knowledge:** [Ascent Rivals overview](../system/overview.md) and the
  [post-teams G08 cleanup](../initiatives/teams-and-team-gauntlets/delivery-plan.md#g08--post-teams-simplification-and-technical-debt-cleanup).
- **Evidence:** The owner requested a post-teams cleanup of overzealous versioning, compatibility,
  defense-in-depth, and repeated field checks; preferred straightforward code with fewer
  conditionals and non-expansive production LOC; and retained validation at boundaries where
  Eventun receives data from the Website, game client, or another external actor.
