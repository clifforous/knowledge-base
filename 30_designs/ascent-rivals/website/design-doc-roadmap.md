# Ascent Rivals Website Design Documentation Roadmap

Date: 2026-05-11
Status: Active Draft

## Related
- [[unified-design]]
- [[information-architecture]]
- [[non-functional-baseline]]
- [[delivery-plan]]
- [[route-api-matrix]]
- [[terminal-ops-design-system]]
- [[tone-and-voice]]
- [[flows/authentication]]
- [[flows/wallet-linking]]
- [[flows/team-lifecycle]]
- [[pages/homepage]]
- [[pages/player-directory]]
- [[pages/player-profile]]
- [[pages/gauntlets-index]]
- [[pages/gauntlet-detail]]
- [[pages/course-leaderboards]]
- [[pages/teams-index]]
- [[pages/team-profile]]
- [[pages/sponsors-index]]
- [[shell-concepts]]
- [[pencil-design-brief]]
- [[pencil-terminal-ops-follow-up-prompt]]
- [[../../../50_knowledge/ascent-rivals/design-language|design-language]]
- [[../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]

## Purpose

This note defines the remaining documentation work needed to turn the current unified website design material into an implementation-ready design document set.

The current unified design doc is useful but too broad to serve every audience well. It mixes:

- product requirements
- information architecture
- visual direction
- feature inventory
- page priorities
- data ownership
- project phasing
- open questions

The current step is to keep the decomposition accurate, close the remaining gaps, and use the focused specs to drive the next Pencil design pass.

## Important Adjustment

Do not replace or delete [[unified-design]] yet.

For now, keep it as:

- the canonical product/design index
- the top-level product requirements summary
- the place where cross-document decisions are linked

Only consider archiving or replacing it after the decomposed documents are complete and every section has a verified destination.

Likewise, keep [[shell-concepts]] as a durable review artifact. Do not archive it just because adopted ideas are copied into a design-system spec. The review note preserves rationale, cautions, and rejected ideas.

## Assessment

The existing docs are strong in:

- product framing
- audience model
- phase planning
- entity-first information architecture
- Eventun / AccelByte / Accountun boundaries
- Terminal Ops shell concept capture
- Pencil prompt/reference material
- qualifier versus heat terminology guardrails

The remaining gaps are mostly specification gaps rather than strategy gaps.

## Current Status

As of 2026-07-17, the design documentation has moved from broad discovery into focused draft specifications.

Completed or substantially drafted:

- [[unified-design]] remains the top-level PRD and product/design index.
- [[information-architecture]] defines the working route model, top-bar navigation direction, bridge rule, search architecture, and initial phase-1 page state matrix.
- [[terminal-ops-design-system]] defines Terminal Ops as the primary working visual direction, with component inventory, navigation behavior, responsive collapse guidance, accessibility guardrails, and SEO guardrails.
- [[delivery-plan]] defines the approved greenfield route-slice sequence, launch readiness gates, cutover/stabilization direction, legacy-site boundary, and rollback constraint.
- [[route-api-matrix]] records the approved server/browser integration boundary, all initial route groups, shared response/metadata/sitemap behavior, deliberate legacy-route retirement, and the bounded team/gauntlet upload-intent contract.
- Page specs exist for homepage, gauntlets, gauntlet detail, player directory, player profile, course leaderboards, teams, team profile, and sponsors.
- Flow specs exist for authentication, wallet linking, team lifecycle, and core gauntlet authoring workflows.
- Terminal Ops concept images and the original broad [[pencil-design-brief]] are preserved as durable reference artifacts.

Still missing or incomplete:

- A later `/game` page spec if material game-system, mode, ship, course, or world content eventually justifies the currently deferred route.
- A consolidated open-question register.
- A standalone content strategy.
- Vercel provisioning and cutover remain implementation work. Accessibility, responsive/performance, SEO, and hosting/deployment have approved baselines in [[non-functional-baseline]]; external analytics and observability are deliberately deferred rather than missing launch requirements.
- A dedicated sponsor-administration flow. Core gauntlet create/edit now has a flow spec; initially administrator-only bracket authoring and runtime-repair operations are assigned to the Eventun Extend App UI, while their detailed implementation flows remain unwritten. Prize/reward flows are deferred outside Website V2.
- A second Pencil pass against constrained page specs and Terminal Ops instead of another broad shell exploration.

## Outstanding Work

### 1. Product requirements extraction

Status: substantially complete for now.

Keep [[unified-design]] as the PRD while adding focused spec links and status notes as the document set evolves.

Minimum content:

- problem statement
- goals and non-goals
- constraints
- audience model
- experience modes
- preserved current features
- new and expanded capabilities
- entity model
- data/system boundaries
- phased roadmap
- risks
- consolidated open questions

Recommendation:

- keep the unified doc as the PRD for now
- add links from it to focused specs as they are created

### 2. Information architecture spec

Status: substantially drafted.

Current draft:

- [[information-architecture]]

Required content:

- full route inventory by phase
- top-level navigation model
- secondary/contextual navigation model
- search architecture
- route ownership and purpose
- page state matrix for anonymous, logged-in, team-authorized, and admin users

Current gap:

- expand or validate the page-state matrix as page specs and auth/admin implementation decisions become firmer

Phase-1 page state matrix should cover:

- `/`
- `/game`
- `/gauntlets`
- `/gauntlets/[id]`
- `/players`
- `/players/[id]`
- `/teams`
- `/teams/[id]`
- login
- wallet linking
- team management
- gauntlet management
- Eventun Extend App sponsor-administration handoff

### 3. Design system specification

Status: substantially drafted.

Current draft:

- [[terminal-ops-design-system]]

Required content:

- working decision status for Terminal Ops
- typography roles
- color tokens mapped to the canonical game palette
- surface/elevation model
- spacing scale
- layout architecture
- component inventory
- accessibility guardrails
- responsive behavior

Initial components to specify:

- command prompt navigation
- path/breadcrumb bar
- bracket/framed panel
- telemetry/status strip
- data table
- system log
- hero/briefing section
- terminal label
- entity cards
- player strength modules

Recommendation:

- mark Terminal Ops as the primary working direction, not the irreversible final decision
- revisit after player profile, course leaderboard, gauntlet detail, and mobile mocks are reviewed

### 4. Page specifications

Status: mostly drafted.

Create or finish page-level specs for phase-1 must-have pages.

Each page spec should include:

- purpose
- primary audience
- layout zones
- required modules
- auth-state variants
- component usage
- data dependencies
- empty/loading/error states
- responsive notes
- SEO requirements

Initial page spec priority:

1. homepage
2. gauntlets list
3. gauntlet detail
4. player profile
5. course leaderboard
6. team profile
7. directories for players and teams
8. game page when distinct content justifies it

Current drafts:

- [[pages/homepage]]
- [[pages/player-directory]]
- [[pages/player-profile]]
- [[pages/gauntlets-index]]
- [[pages/gauntlet-detail]]
- [[pages/course-leaderboards]]
- [[pages/teams-index]]
- [[pages/team-profile]]
- [[pages/sponsors-index]]

Current gap:

- create a dedicated `/game` page spec

### 5. User flow documentation

Status: partially drafted.

Create or finish flow notes for stateful interactions.

Initial flows:

- Steam auth: [[flows/authentication]]
- team creation: [[flows/team-lifecycle]]
- team join request: [[flows/team-lifecycle]]
- team invite accept/deny: [[flows/team-lifecycle]]
- team management: [[flows/team-lifecycle]]
- gauntlet creation/editing
- logged-in gauntlet participation context

Current drafts:

- [[flows/authentication]]
- [[flows/wallet-linking]]
- [[flows/team-lifecycle]]

Current gaps:

- gauntlet creation/editing
- logged-in gauntlet participation context
- Eventun Extend App sponsor administration/media implementation and cutover verification

### 6. Responsive strategy

Status: partially covered in [[terminal-ops-design-system]] and page specs.

Create a dedicated responsive strategy note if the distributed guidance is not enough for implementation.

Required decisions:

- breakpoints
- command nav collapse behavior
- table handling on mobile
- two-column layout collapse
- status strip behavior on narrow screens
- touch target sizing
- mobile profile and gauntlet sub-navigation

### 7. Content strategy

Status: not started as a dedicated note.

Create a content strategy note.

Required decisions:

- source for homepage news/announcements
- no-CMS phase-1 authoring model
- static Next.js content versus Eventun-served content
- media asset ownership
- Steam wishlist and social CTA placement
- lore relationship to courses, planets, manufacturers, and ship parts

### 8. Accessibility and SEO baseline

Status: rendering/caching, Vercel hosting/deployment, WCAG 2.2 AA accessibility, responsive/performance, and lightweight SEO requirements are recorded in [[non-functional-baseline]]; external analytics/observability are deferred, and Vercel provisioning/cutover remains implementation work.

The accessibility and SEO baseline is approved in [[non-functional-baseline]]. Retain its implementation verification as release work.

Required decisions:

- semantic structure for terminal-inspired UI
- CSS framing over box-drawing text for critical UI
- keyboard navigation for command/search interaction
- screen reader labels for command nav and telemetry strips
- contrast validation for color tokens
- Next.js rendering and caching expectations for public and authenticated pages
- meta and Open Graph patterns for public entities
- performance budget for image-heavy pages

### 9. Open-question register

Status: not started.

Create a single open-question register.

Track:

- question
- owner
- status
- decision date
- related document
- impact if unresolved

This prevents questions from being scattered across the unified design doc, shell concept review, and Pencil brief.

## Working Navigation Recommendation

Adopt this as a working direction, not a final decision:

- command prompt-inspired top navigation for global navigation
- contextual side panels or local section navigation on data-heavy interior pages where needed

Rationale:

- Terminal Ops' command nav is the strongest current visual shell idea
- data-heavy pages may still need local navigation density that pure top nav cannot provide
- this preserves the best of the concept without prematurely rejecting side-navigation utility

Conditions for revisiting:

- player profile mock cannot support section discovery
- course leaderboard mock needs persistent filters that top nav cannot handle
- mobile shell cannot collapse the command nav cleanly
- usability review shows the prompt metaphor confuses non-technical visitors

## Next Mock Pass Recommendation

Use [[pencil-terminal-ops-follow-up-prompt]] for the next pass.

Before asking Pencil for another broad exploration, provide tighter page constraints.

Recommended next mocks:

1. player profile
2. course leaderboard
3. gauntlet detail refinement
4. mobile shell state

Design goals:

- test dense stats with Terminal Ops
- test contextual navigation
- test player strength modules
- test course/ranked leaderboard filtering
- test qualifier-vs-heat terminology correctness
- test mobile viability

## Execution Order

Recommended order:

1. Complete or accept the current draft design system specification. Status: drafted.
2. Complete or accept the current draft information architecture spec with page state matrix. Status: drafted.
3. Run the next Pencil pass against the completed core page specs. Status: prompt drafted in [[pencil-terminal-ops-follow-up-prompt]].
4. Keep `/game` deferred until material content justifies it. Status: not an initial-release documentation gap.
5. Maintain the accessibility, responsive/performance, and SEO portions of [[non-functional-baseline]]. Status: approved; implementation verification remains.
6. Create remaining user-flow specs for later bracket/runtime operations; sponsor administration is assigned to the approved Eventun Extend App handoff. Status: partial.
7. Create content strategy. Status: not started.
8. Consolidate open questions. Status: not started.

Reason:

- design-system and IA decisions unblock all page specs
- player profile, gauntlet detail, and course leaderboard are the highest-risk data-heavy pages for the Terminal Ops shell
- another open-ended mock pass would likely create more attractive but underspecified screens

## Verification Checklist

- [x] Unified doc links to every focused design document created so far.
- [ ] Every section of the unified doc has a destination in the decomposed set.
- [x] Every initial-release must-have public page has a page spec or an approved grouped spec; `/game` is explicitly deferred rather than missing.
- [x] Phase-1 page state matrix exists.
- [x] Design system maps Terminal Ops tokens to canonical game palette.
- [x] Component inventory covers the core Terminal Ops components.
- [ ] User flows cover authenticated Website workflows and remaining administrator operations. Core gauntlet authoring is specified; sponsor administration has an approved Eventun Extend App handoff, while later bracket/runtime operations remain. Prize/reward flows are intentionally excluded.
- [ ] Responsive strategy addresses navigation, tables, and two-column layouts.
- [x] Accessibility guidance addresses terminal metaphor and box-drawing risks.
- [ ] SEO baseline exists for public entity pages.
- [x] Navigation has a recorded working decision and revisit criteria.
- [x] Next Pencil pass prompt exists for Terminal Ops validation.
