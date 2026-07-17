# Ascent Rivals Website V2 Delivery Plan

Date: 2026-07-17
Status: Delivery sequence approved; route/API map, slice acceptance details, and cutover runbook open

## Related

- [[unified-design]]
- [[initial-release-scope]]
- [[information-architecture]]
- [[terminal-ops-design-system]]
- [[non-functional-baseline]]
- [[route-api-matrix]]
- [[design-doc-roadmap]]
- [[flows/authentication]]
- [[flows/gauntlet-authoring]]
- [[../../../40_work_tracking/tasks/2026-07-15-website-v2-design-restart]]

## Goal

Deliver the greenfield Website V2 in complete, reviewable route slices while the current marketing website and Ascentun continue serving their existing responsibilities.

Do not cut public traffic over merely because the new shell or a subset of public pages exists. Website V2 replaces the current public marketing and non-blockchain Ascentun experiences only after the approved launch gates pass.

## Delivery Principles

- build a new Next.js/React/TypeScript repository rather than incrementally converting either current website;
- use the existing sites as content, asset, behavior, and migration references only;
- keep each implementation slice vertically complete enough to review real content, data, loading, empty, error, responsive, and permission states;
- keep Eventun and AccelByte as authoritative systems rather than copying product state into Website V2;
- add or revise a backend contract only when an approved route needs authoritative aggregation, visibility, or bounded composition that current contracts do not supply;
- do not expose unfinished Website V2 routes through the production navigation;
- do not require a single high-risk launch containing unreviewed pages, unverified backend reads, and a simultaneous legacy shutdown.

## Readiness Gates

Implementation may begin with the repository, visual system, marketing content, and reviewed public contracts. Launch depends on all of the following:

- the preceding Eventun team foundation has been implemented and exercised enough to review its actual Website-facing reads and permissions;
- Eventun F14 serving work and the F15 historical backfill/cutover have completed for production pilot, course, match-history, gauntlet, and leaderboard data used by Website V2;
- fact-backed team statistics and event-time membership attribution are available for the approved launch team surfaces;
- the Website V2 development deployment completes the same Steam OpenID to AccelByte token exchange already operating in Ascentun, including refresh and logout acceptance checks;
- AccelByte course visibility, Eventun public entity visibility, media upload, and permission contracts are verified in the matching development environment;
- the Eventun Extend App provides reviewed sponsor administration and administrator-authorized sponsor media upload in both matching environments;
- the revised Terminal Ops direction has been reviewed against marketing, data-dense, gauntlet, and mobile mocks.

Bracket implementation is not allowed to block unrelated Website slices. When published bracket and public match-state contracts ship, Website V2 renders them. Initially administrator-only bracket mutation and repair remain in the Eventun Extend App UI.

## Approved Delivery Sequence

### 1. Greenfield Foundation

- create the repository and baseline Next.js App Router structure;
- establish TypeScript, formatting/linting, environment configuration, and safe secret boundaries;
- implement the responsive shell, approved navigation order, page layout primitives, error boundaries, loading conventions, and cache helpers;
- connect development and production configuration to only their corresponding Eventun and AccelByte game environments;
- establish the initial Vercel projects/environments without moving public domains.

### 2. Terminal Ops Visual Validation

- produce the approved constrained mock pass for marketing, pilot/data, gauntlet, and mobile states;
- settle the working typography, surface, framing, responsive-collapse, and motion decisions needed for implementation;
- implement shared tokens and primitives from the reviewed designs;
- use code review and manual responsive browser review as the default design loop;
- add isolated component or screenshot tooling only when repeated-state coverage justifies its maintenance cost.

### 3. Repository-Authored Marketing and Editorial Routes

- implement `/`, `/about`, `/brand`, `/events`, and `/events/[slug]` from reviewed repository-authored content;
- migrate and verify approved copy, gameplay claims, downloads, video, screenshots, recognition, team information, partner references, and brand assets;
- keep `/game` deferred until it has material content not already served by the homepage;
- remove links to retired marketing routes; do not build a legacy redirect layer for the initial traffic level.

### 4. Public Gauntlet, Pilot, Course, and Search Routes

- implement `/gauntlets`, `/gauntlets/[id]`, `/players`, `/players/[id]`, `/courses`, `/courses/[code]`, and grouped global search;
- integrate the compact public discovery contracts and reviewed production-cut-over Eventun/AccelByte reads;
- implement exact tables, bounded visualizations, client-side collection search/filter/sort/display pagination, and public cache behavior;
- verify published/archived/hidden visibility and missing-versus-zero semantics before exposing production data.

### 5. Public Team Routes

- review the implemented team contracts after the team feature has been exercised;
- finalize the provisional team analytics modules against fact-backed data rather than current-roster inference;
- implement `/teams` and `/teams/[id]` with public roster, membership-mode, history, and statistics behavior;
- keep individual pilot identity more prominent until product use supports changing the balance.

### 6. Steam Authentication and Personalized Overlays

- implement Steam sign-in, callback validation, AccelByte exchange, secure session cookies, refresh, logout, and safe return paths;
- add personal placement, qualification, participation, current-team, invitation/request, and permission-aware action overlays to the existing public layouts;
- preserve one page composition rather than creating a separate logged-in application shell;
- verify cancellation, linking, Login Queue, expiry, replay, and invalid assertion behavior without logging sensitive material.

### 7. Team and Core Gauntlet Management

- implement team create/manage, membership, invitation, request, role, ownership, media, and disband workflows against the final team contract;
- implement permissioned core gauntlet create/edit/delete, schedule and competition-structure authoring, direct billboard/media upload, and optional advanced sponsor association;
- retain Eventun authorization at every mutation boundary;
- keep administrator-only bracket and runtime-repair tooling in the Eventun Extend App UI.

### 8. Eventun Extend App Sponsor Handoff

- implement administrator-only sponsor list/detail, create/edit/delete or approved dependency-block behavior, media, color, and social-link workflows in the Eventun Extend App rather than Website V2;
- add or deliberately reuse an administrator-authorized signed media-upload boundary without exposing object-store credentials to the Extend browser;
- make Eventun sponsor writes atomic, correct the stale delete query, and return typed validation/dependency failures before exposing the controls;
- preserve existing sponsor records, media, gauntlet relationships, tiers, and legacy `WideBillboard` data;
- keep sponsor registry/search/CRUD routes out of Website V2;
- verify direct gauntlet media and sponsor-associated media independently.

### 9. Migration and Release Verification

- complete the route-to-source/API map and confirm every approved non-blockchain Ascentun workflow has a tested Website V2 or Eventun Extend App destination or deliberate retirement;
- verify route-level anonymous, authenticated, owner/manager/creator, and administrator states;
- verify marketing content accuracy, canonical routes, metadata, sitemap behavior, data visibility, uploads, permissions, responsive layouts, accessibility, caching, safe logs, and rollback prerequisites;
- test Website V2 against production-shaped data in the development game environment before production cutover;
- create a concrete cutover and rollback runbook with owners and verification evidence.

### 10. Production Cutover and Stabilization

- freeze the reviewed Website and Eventun contract revisions used for cutover;
- deploy Website V2 production and run pre-domain smoke checks;
- point `ascentrivals.com` and approved canonical traffic at Website V2;
- allow retired marketing and replaced Ascentun routes to return `404`; keep only the explicitly retained Midnight prize flow and its required legacy authentication/API support reachable;
- run anonymous, authentication, permissioned mutation, media, data freshness, and critical-route smoke checks;
- retain a tested known-good deployment and the required temporary backend compatibility for immediate rollback during the stabilization window;
- remove temporary rollback compatibility only through a later explicit cleanup after Website V2 is stable.

## Slice Completion Standard

A route slice is complete only when its implementation worker reports and review verifies the applicable evidence:

- approved route purpose, data owner, and audience states are implemented;
- loading, empty, unavailable, not-found, authorization, validation, and dependency-failure states are deliberate;
- public/private cache boundaries and mutation invalidation follow [[non-functional-baseline]];
- mobile/narrow, keyboard, focus, reduced-motion, contrast, and relevant screen-reader behavior have been manually reviewed;
- metadata and canonical behavior match the route's indexing class;
- excluded wallet, token-gating, Accountun prize/reward, and unsupported live/broadcast behavior is absent;
- code review and manual visual review are complete;
- required build, lint, generation, test, or smoke evidence is reported by the implementation worker.

## Legacy-Site Boundary

The current marketing website can be retired after its content, domains, and historical routes have migrated and the stabilization window passes.

Ascentun is different:

- its public non-blockchain routes stop being the promoted experience after Website V2 cutover;
- Website V2 must not link users back to excluded prize/reward workflows;
- the legacy Ascentun deployment remains available for the explicitly deferred Midnight/blockchain sponsored-tournament workflow until that workflow is separately retired or relocated;
- do not describe Ascentun as fully retired while that dependency remains;
- legacy hosting does not justify maintaining duplicate non-blockchain product features in both applications.

## Rollback Boundary

Immediate website rollback means restoring the last verified site deployment/domain mapping and re-running critical smoke checks. It is only valid while the prior site remains compatible with the deployed Eventun and AccelByte contracts.

The stabilization plan must therefore make one explicit temporary compatibility choice:

- keep the prior site tested against the cutover backend contract for the rollback window; or
- declare deployment rollback unsafe and use a forward-fix plan.

Do not preserve legacy APIs indefinitely under the label of rollback. End the temporary compatibility window through a reviewed cleanup once the new site is stable.

## Remaining Planning Work

- convert the completed [[route-api-matrix]] contract gaps into implementation-slice requirements, including revised projections, new reads, team/bracket dependencies, and environment verification;
- detailed implementation acceptance and evidence per slice;
- final Vercel project names, development hostname, branch promotion, function region, and environment-variable inventory;
- final canonical domain plus the legacy Ascentun host required by the retained Midnight prize flow;
- cutover checklist, stabilization duration, rollback owner, and legacy cleanup criteria;
- handling of existing authenticated sessions at cutover;
- production support/contact path in the absence of external error monitoring.
