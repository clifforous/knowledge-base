# Website V2 Initiative

Status: in-progress
Status detail: Approved baselines and draft specifications remain an active design and
delivery initiative; they are not the deployed website.

Last consolidated: 2026-07-21

Website V2 remains initiative material because the current deployed website is described in
[the website system document](../../system/website.md). Status statements in each document
control where this index identifies a mixture of approved and draft material.

## Outcome

Deliver one greenfield Next.js/React website that replaces the current marketing site and
the approved public/player non-blockchain responsibilities of Ascentun. The release adds
stronger public gauntlet, pilot, course, and team presentation while keeping authoritative
domain behavior in Eventun and AccelByte.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Product, route, and delivery baseline | `approved` | Linked scope, architecture, route/API, non-functional, page, and flow documents | `not-applicable` | Close remaining contract gaps and slice-specific acceptance detail |
| Terminal Ops visual calibration | `approved` | Cliff's live external Pencil workfile, reviewed through the completed 2026-07-21 Design Language v0.2 reference board, plus the linked Markdown baselines | `not-applicable`; design artifact | Preserve one reviewed snapshot, begin the greenfield application foundation, and later validate team and form extensions |
| Website V2 application | `not-started` | No implementation revision is recorded | `not-deployed` | Greenfield repository foundation and first approved route slice |
| Production cutover | `not-started` | Delivery sequence only; no release or runbook exists | `not-deployed` | Implementation, environment verification, cutover plan, and rollback choice |

## Reading Order

1. [Initial release scope](initial-release-scope.md) for the approved product boundary.
2. [Unified design](unified-design.md) for the integrated experience direction.
3. [Information architecture](information-architecture.md) and the
   [route/API matrix](route-api-matrix.md) for route and contract detail.
4. [Design language v0.2](design-language-v0.2.md) and the
   [Terminal Ops design system](terminal-ops-design-system.md) for the visual baseline.
5. Page and flow specifications for implementation-specific behavior.
6. [Delivery plan](delivery-plan.md) for the approved sequence and remaining planning work.

## Scope and Delivery

- [Initial release scope](initial-release-scope.md)
- [Delivery plan](delivery-plan.md)
- [Information architecture](information-architecture.md)
- [Route and API matrix](route-api-matrix.md)
- [Non-functional baseline](non-functional-baseline.md)
- [Sponsor-administration handoff](sponsor-administration-handoff.md)

## Experience and Visual Design

- [Unified design](unified-design.md)
- [Design language v0.2](design-language-v0.2.md)
- [Terminal Ops design system](terminal-ops-design-system.md)
- [Shell concepts](shell-concepts.md)
- [Tone and voice](tone-and-voice.md)

The live Pencil artifact is owner-managed by Cliff outside this repository because Pencil does
not work reliably against the WSL filesystem. No shareable durable artifact identity is
currently recorded. The artifact was last reviewed on 2026-07-21 through the shared page-state
and Design Language v0.2 reference-board checkpoint; the approved Design Language v0.2 and the
checkpoint below capture the accepted frame direction and extracted implementation rules.
Import one reviewed preservation copy only at an explicit design checkpoint; label it as a
snapshot and do not maintain two nominally live copies.

## Detailed Specifications

- [User flows](flows/README.md)
- [Page specifications](pages/README.md)

## Current Design Checkpoint

- Homepage desktop and mobile calibration are reviewed and provide the original visual thesis now
  consolidated in Design Language v0.2.
- Gauntlet directory and Schedule desktop/mobile calibration are reviewed applications of
  that language.
- Active combined, sparse/upcoming, and active mobile gauntlet-detail calibrations are
  reviewed. They validate conditional section omission, stage circuits, desktop qualifier
  standings, and an open mobile rank-list translation.
- Public player-profile desktop/mobile calibration is reviewed. It validates a bounded
  public career lead, Podium Rate and Ascension Rate comparisons, published-course records,
  bounded recent races, and a three-entry recent gauntlet history. Candidate private career
  detail and recognition remain reversible own-profile additions rather than public defaults.
- Pilot-directory desktop/mobile calibration is reviewed. It validates client-side name/team
  search and sorting, compact public identity cards, neutral team affiliation, missing-avatar and
  zero-stat cases, bounded long names, and progressive reveal without server pagination.
- Course-directory and course-detail desktop/mobile calibrations are reviewed. The directory
  uses complete responsive collections without redundant page-local search, result count,
  archive scope, or pagination. The detail validates exact record and gap presentation,
  responsive rank rows, class-dependent Loadout Value presentation, and balanced mobile footers.
  The canonical course-detail frames now use the reviewed faceted category controls in place of
  the earlier labeled category grid.
- Global-search desktop/mobile calibration and its compact state study are reviewed. They validate
  a modal/sheet command over the stable shell, grouped shallow public results, direct entity links,
  deterministic keyboard focus, local no-match recovery, and independent partial availability.
- Shared page-state desktop/mobile calibration is reviewed. It validates route loading, a valid
  empty collection, essential-route unavailability, non-revealing not-found handling, local
  optional-module failure, and safe stale-content refresh without replacing the stable shell.
- The bounded cross-frame alignment pass is reviewed. Current canonical frames use the same
  desktop/mobile shell and footer measurements, generic sign-in language, search identity,
  profile record terminology, natural user-facing numbers, route metadata, and accepted faceted
  and segmented control variants. One immutable, nonvisual pilot-profile root metadata field still
  contains legacy `RACE FINISH`; it is an artifact caveat and is not implementation guidance.
- The Design Language v0.2 reference board is reviewed. It consolidates the canonical palette,
  typography, spacing, geometry, shells, footers, actions, selectors, content specimens, shared
  states, focus treatment, and responsive transformations. It defines static states and motion
  intent; implementation timing and easing remain provisional until reviewed in the browser.
- Team-page validation follows review of the implemented team contracts.

## Material Decisions

- [AR-2026-008](../../decisions/README.md#ar-2026-008--website-v2-is-one-greenfield-nextjsreact-replacement)
  selects the greenfield Next.js/React replacement.
- [AR-2026-009](../../decisions/README.md#ar-2026-009--website-v2-excludes-wallet-and-accountun-reward-workflows)
  defines the wallet and Accountun exclusion.
- [AR-2026-010](../../decisions/README.md#ar-2026-010--sponsor-administration-moves-to-the-eventun-extend-app)
  assigns sponsor administration to the Eventun Extend App.
- [AR-2026-011](../../decisions/README.md#ar-2026-011--website-v2-uses-a-purpose-built-race-control-language)
  records the revised visual direction.
- [AR-2026-012](../../decisions/README.md#ar-2026-012--public-pilot-profiles-use-a-bounded-career-surface)
  records the public-profile privacy and scope boundary.
- [AR-2026-013](../../decisions/README.md#ar-2026-013--course-discovery-and-course-records-use-separate-routes)
  records the course directory/detail separation.

## Authoritative Current System

- [Current website surfaces](../../system/website.md)
- [Eventun](../../system/eventun/overview.md)
- [AccelByte platform](../../system/accelbyte-platform.md)
- [Current team and gauntlet behavior](../../system/team-gauntlet-current-state.md)

## Remaining Before Closure

- preserve one reviewed Pencil snapshot at this checkpoint and carry the approved v0.2 baseline
  through later team, form, and in-browser motion validation without treating it as immutable;
- close the route/API contract gaps and review the implemented team-facing contracts;
- implement and verify the route slices, Steam session boundary, permissions, uploads,
  accessibility, responsive behavior, caching, metadata, and release evidence;
- complete the Eventun Extend App sponsor-administration handoff before Ascentun cutover;
- provision the final Vercel environments and produce the domain cutover, stabilization,
  rollback, retained-Midnight-host, and cleanup runbook;
- incorporate accepted deployed behavior into `system/` before archiving this initiative.

The [superseded exploratory Pencil brief](../../archive/initiatives/website-v2/pencil-design-brief.md)
and the [excluded wallet-linking flow](../../archive/initiatives/website-v2/wallet-linking.md)
are retained as historical evidence. The old follow-up prompt and documentation roadmap were
removed after their durable direction and remaining work were reconciled into the active
design, delivery, and index documents.
