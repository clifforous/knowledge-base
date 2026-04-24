# Ascent Rivals Website Design Documentation Roadmap

Date: 2026-04-13
Status: Draft

## Related
- [[unified-design]]
- [[information-architecture]]
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

The next step should be decomposition into focused documents.

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

## Outstanding Work

### 1. Product requirements extraction

Create a focused product requirements document or keep the unified doc as the PRD while adding a clear index.

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

Create a dedicated IA note.

Current draft:

- [[information-architecture]]

Required content:

- full route inventory by phase
- top-level navigation model
- secondary/contextual navigation model
- search architecture
- route ownership and purpose
- page state matrix for anonymous, logged-in, team-authorized, and admin users

Phase-1 page state matrix should cover:

- `/`
- `/game`
- `/gauntlets`
- `/gauntlets/[id]`
- `/players`
- `/players/[id]`
- `/teams`
- `/teams/[id]`
- `/sponsors`
- login
- wallet linking
- team management
- gauntlet management
- sponsor administration

### 3. Design system specification

Create a dedicated Terminal Ops design-system spec.

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

Create page-level specs for phase-1 must-have pages.

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
8. sponsors
9. game page

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

### 5. User flow documentation

Create flow notes for stateful interactions.

Initial flows:

- Steam auth: [[flows/authentication]]
- wallet linking and verification: [[flows/wallet-linking]]
- team creation: [[flows/team-lifecycle]]
- team join request: [[flows/team-lifecycle]]
- team invite accept/deny: [[flows/team-lifecycle]]
- team management: [[flows/team-lifecycle]]
- gauntlet creation/editing
- logged-in gauntlet participation context
- prize/funding/claim flows preserved from the current site

Current drafts:

- [[flows/authentication]]
- [[flows/wallet-linking]]
- [[flows/team-lifecycle]]

### 6. Responsive strategy

Create a responsive strategy note or include it in the design-system spec.

Required decisions:

- breakpoints
- command nav collapse behavior
- table handling on mobile
- two-column layout collapse
- status strip behavior on narrow screens
- touch target sizing
- mobile profile and gauntlet sub-navigation

### 7. Content strategy

Create a content strategy note.

Required decisions:

- source for homepage news/announcements
- no-CMS phase-1 authoring model
- static Nuxt content versus Eventun-served content
- media asset ownership
- Steam wishlist and social CTA placement
- lore relationship to courses, planets, manufacturers, and ship parts

### 8. Accessibility and SEO baseline

Create an accessibility and SEO baseline note or include these sections in page specs and the design-system spec.

Required decisions:

- semantic structure for terminal-inspired UI
- CSS framing over box-drawing text for critical UI
- keyboard navigation for command/search interaction
- screen reader labels for command nav and telemetry strips
- contrast validation for color tokens
- Nuxt SSR expectations for public pages
- meta and Open Graph patterns for public entities
- performance budget for image-heavy pages

### 9. Open-question register

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

1. Create the design system specification.
2. Create the information architecture spec with page state matrix.
3. Run the next Pencil pass against the completed core page specs.
4. Create the responsive/accessibility baseline.
5. Create user flow specs for authenticated workflows.
6. Create content strategy.
7. Consolidate open questions.

Reason:

- design-system and IA decisions unblock all page specs
- player profile, gauntlet detail, and course leaderboard are the highest-risk data-heavy pages for the Terminal Ops shell
- another open-ended mock pass would likely create more attractive but underspecified screens

## Verification Checklist

- [ ] Unified doc links to every focused design document.
- [ ] Every section of the unified doc has a destination in the decomposed set.
- [ ] Every phase-1 must-have page has a page spec.
- [ ] Phase-1 page state matrix exists.
- [ ] Design system maps Terminal Ops tokens to canonical game palette.
- [ ] Component inventory covers the core Terminal Ops components.
- [ ] User flows cover authenticated and admin workflows preserved from the current site.
- [ ] Responsive strategy addresses navigation, tables, and two-column layouts.
- [ ] Accessibility guidance addresses terminal metaphor and box-drawing risks.
- [ ] SEO baseline exists for public entity pages.
- [ ] Navigation has a recorded working decision and revisit criteria.
