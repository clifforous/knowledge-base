# Website V2 Initiative

Status: in-progress
Status detail: Approved baselines and draft specifications remain an active design and
delivery initiative; they are not the deployed website.

Last consolidated: 2026-07-23

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
| Product, route, and delivery baseline | `approved` | Linked scope, architecture, route/API, non-functional, page, and flow documents; Website team and gauntlet-result semantics are reconciled to the deployed-development T03 public reads and reviewed occurrence-fact source corrections | `not-applicable` | Coordinate development adoption, close remaining contract gaps, and add slice-specific acceptance detail |
| Terminal Ops visual calibration | `approved` | Cliff's live external Pencil workfile, reviewed through the completed 2026-07-21 Design Language v0.2 reference board, plus the linked Markdown baselines | `not-applicable`; design artifact | Preserve one reviewed snapshot; calibrate team directory/profile and affected gauntlet annotations against the approved T03 semantics; later validate form extensions |
| Website V2 foundation and repository-authored routes | `verified` | `ar-web` revision `da73e6964c2e85684b339fe616a063973a1a2f12` contains the greenfield shell, shared clipped-layer polygon borders, static `/about`, `/brand`, `/events`, and `/events/[slug]` routes, typed event content, and migrated approved repository assets | Local 2026-07-22 formatting, ESLint, TypeScript, optimized production build, responsive browser, keyboard, reduced-motion, polygon-state, route, metadata, canonical, shared `404`, and console verification is recorded by the completed implementation pass. The revision is committed and `not-deployed` | Close the repository-authored content gaps below and retain this verified baseline through later slices |
| Website V2 gauntlet discovery slice | `verified` | Committed `ar-web` revision `7d1d00c` accepts the preceding and `0e4d656` discovery shapes, caches only normalized occurrence facts, ignores Eventun response time, derives SSR from one fresh Website-server timestamp, hydrates from that exact timestamp, advances locally with a monotonic clock plus wall-clock suspension fallback, retains a nondecreasing floor across visibility and replacement data, and keeps all prior occurrence semantics | Local 2026-07-23 formatting, ESLint, TypeScript, nineteen focused Node tests, optimized production build, strict Knowledge Base validation, and diff checks passed. Windows Edge headless verification rendered Upcoming, Current, and Past from one cached malformed-old-response fixture with token/discovery counters fixed at `1/1`, no hydration/console failures, and CDP freeze/reactivation recovery from Upcoming to Current with the page visible afterward and counters still `1/1`. Independent implementation review found no blocking defect. The unchanged CSS retains the 2026-07-22 full `320`, `390`, `759/760`, `1024`, and `1440` review; the stripped WSL Chromium runtime remains unavailable because required browser libraries are absent. The expected unavailable UI still streams HTTP `200` after shell commitment. The revision is committed and `not-deployed` | Separately address the remaining streamed-5xx, development-service, representative-media, and coordinated deployment gates |
| Website V2 gauntlet detail contract | `approved-pre-implementation` | The 2026-07-23 read-only checkpoint selects a compact domain-neutral `GET /v1/public/gauntlet/{gauntlet_id}` projection plus independent field, factual StageRun, standings/result, and optional sponsor modules; [[route-api-matrix]] and [[pages/gauntlet-detail]] record the exact boundary. Eventun G03 is committed as `cb79df3`, clearing the overlapping-worktree gate; the owner selected the Eventun projection as T03D alongside G04 | Design/API review only. No detail implementation, verification, deployment, or environment change is implied | Implement and review T03D before beginning the Website detail route |
| Production cutover | `not-started` | Delivery sequence only; no release or runbook exists | `not-deployed` | Implementation, environment verification, cutover plan, and rollback choice |

### Current Repository-Authored Content Gaps

- The migrated source provides team names and role labels but no approved individual biographies;
  `/about` therefore does not add biographies.
- The MSI Grand Prix source leaves the official-rules, livestream, Monolith Gaming, and Mezzcast
  destinations undefined. Its queue/setup instructions and random-racer prize selection are marked
  unfinished; those destinations, instructions, and promotional copy remain omitted.
- The historical event source provides concise dates, summaries, winners, prizes, artwork, and most
  recap links, but not long-form reports. The migrated historical routes do not expand those records.
- `/brand` provides the six current repository logo variants and the existing complete-kit link. No
  standalone downloadable font package was added because the source does not provide one complete,
  reviewed distribution set.

### Current Gauntlet Slice Gates

- Eventun source commit `0e4d656` removes query-time `timing_state`, `active_occurrence`,
  `next_occurrence`, `latest_ended_occurrence`, and
  `additional_scheduled_occurrence_count`. It is not deployed; shared development may still return
  the preceding response. Website V2 accepts both response generations, ignores the redundant
  fields when present, and derives presentation from cached occurrence facts and a fresh
  Website-server timestamp.
- No real AccelByte/Eventun development credentials or endpoint values were placed in the repository,
  and the local pass used a contract double. Provision the confidential Website client with Eventun
  Server `READ`, configure the matching Vercel development environment, and repeat integration
  verification before deployment.
- Next.js 16 Cache Components requires request-backed query and integration work below Suspense. The
  partial-prerender shell commits HTTP `200` before an Eventun failure resolves; the reviewed unavailable
  body is deliberate, but it does not yet meet the approved essential-route 5xx response requirement.
- Directory and Schedule entries use their approved canonical `/gauntlets/[id]` links. Gauntlet detail
  remains outside this slice, so those destinations intentionally use the shared non-revealing `404`
  until the separate detail pass and remain a production navigation gate.
- Bounded allowlisted media, missing media, and responsive crops were exercised with a contract fixture.
  Representative real gauntlet uploads and their media-purpose selection still require development-
  environment review.
- The 2026-07-23 stripped WSL Chromium harness loads the self-hosted display/mono fonts but renders
  them at zero height and crashes its renderer when the shell switches at `760` CSS pixels. A
  test-only body-font substitution allowed the new 390px temporal and overflow checks; rerun
  `760`, `1024`, and `1440` in a healthy browser before accepting new desktop visual evidence.
- The accepted gauntlet-detail direction deliberately excludes field-owner and racer-slot capacity
  from the stable primary detail response. Current capacity comes from the current-field projection;
  historical capacity comes from the exact StageRun-field projection.
- Existing overall and qualifier standings are valid only for supported player-owned qualification
  models with a recognized public scoring metric. Team-owned qualification requires an owner-aware
  public projection; unsupported or unknown scoring configurations omit standings rather than being
  interpreted in the Website.
- Eventun G03 field/runtime work was reviewed and committed as `cb79df3`, clearing the source-
  ownership prerequisite for the public-detail implementation. The unsafe legacy detail error
  mapping remains a separate cleanup; the new public projection must implement its own sanitized
  status boundary rather than consume or broaden the legacy handler.

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
- Team directory/profile content and data-state requirements are reconciled to the approved T03
  public-read checkpoint. Dedicated desktop/mobile visual calibration remains open and must cover
  populated, sparse, unranked, independently unavailable, and no-team-result states. Affected
  gauntlet frames also require a bounded annotation pass separating field owners, racer slots,
  personal participation, and team-owned results.

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
- implement and review the approved T03 public reads, then validate the team and affected gauntlet
  visual states against representative data;
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
