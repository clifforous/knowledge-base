# Website V2 Initiative

Status: in-progress
Status detail: Approved baselines and draft specifications remain an active design and
delivery initiative; they are not the deployed website.

Last consolidated: 2026-07-20

Website V2 remains initiative material because the current deployed website is described in
[the website system document](../../system/website.md). Status statements in each document
control where this index identifies a mixture of approved and draft material.

## Outcome

Deliver one greenfield Next.js/React website that replaces the current marketing site and
the approved public/player non-blockchain responsibilities of Ascentun. The release adds
stronger public gauntlet, pilot, course, and team presentation while keeping authoritative
domain behavior in Eventun and AccelByte.

## Reading Order

1. [Initial release scope](initial-release-scope.md) for the approved product boundary.
2. [Unified design](unified-design.md) for the integrated experience direction.
3. [Information architecture](information-architecture.md) and the
   [route/API matrix](route-api-matrix.md) for route and contract detail.
4. [Design language v0.1](design-language-v0.1.md) and the
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
- [Design language v0.1](design-language-v0.1.md)
- [Terminal Ops design system](terminal-ops-design-system.md)
- [Shell concepts](shell-concepts.md)
- [Tone and voice](tone-and-voice.md)

The live Pencil artifact is intentionally kept outside this repository during active visual
iteration. Import one reviewed preservation copy only at an explicit design checkpoint; do
not maintain two nominally live copies.

## Detailed Specifications

- [User flows](flows/README.md)
- [Page specifications](pages/README.md)

## Current Design Checkpoint

- Homepage desktop and mobile calibration are reviewed and define Design Language v0.1.
- Gauntlet directory and Schedule desktop/mobile calibration are reviewed applications of
  that language.
- The active gauntlet-detail desktop calibration exists in the live Pencil workfile and
  awaits review; a sparse/upcoming composition remains to be created.
- Player-profile and course-detail/leaderboard validation remain next. Team-page validation
  follows review of the implemented team contracts.

## Authoritative Current System

- [Current website surfaces](../../system/website.md)
- [Eventun](../../system/eventun/overview.md)
- [AccelByte platform](../../system/accelbyte-platform.md)
- [Current team and gauntlet behavior](../../system/team-gauntlet-current-state.md)

## Remaining Before Closure

- finish representative gauntlet-detail, pilot, course, and later team design validation;
- promote the provisional design language only after dense tables, filters, charts, forms,
  partial-data states, and responsive entity layouts are coherent;
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
