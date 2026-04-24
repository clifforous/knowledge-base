# Ascent Rivals Unified Website Design

Date: 2026-04-10
Status: Draft

## Related
- [[../../../50_knowledge/ascent-rivals/overview|ascent-rivals-overview]]
- [[../../../50_knowledge/ascent-rivals/website|website]]
- [[../../../50_knowledge/ascent-rivals/eventun/overview|eventun]]
- [[../../../50_knowledge/ascent-rivals/accountun|accountun]]
- [[../../../50_knowledge/ascent-rivals/game-design|game-design]]
- [[pencil-design-brief]]
- [[shell-concepts]]
- [[design-doc-roadmap]]
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
- [[../gauntlet-finals-and-tournament-modes-design-review]]

## Problem Statement

Ascent Rivals currently has a split web presence:

- a dev/admin-oriented application for players, teams, gauntlets, sponsors, wallets, and operations workflows
- a separate marketing-oriented website for brand and promotional content

That split is no longer aligned with the intended product experience.

The new website should be a single public-facing Nuxt application that:

- supports discovery of the game for new visitors
- supports repeat usage for players and their followers
- preserves all current operational and player-facing workflows
- expands into richer public stats, event discovery, lore, and eventually watch/live-stream features

The new site should feel cohesive across marketing, public competition browsing, and logged-in player workflows rather than behaving like disconnected products.

Tone direction:

- the site should feel like a shipboard computer or race operations terminal giving pilots, followers, and organizers precise competition intelligence
- terminal style should support clarity, not replace clear labels or accessible actions

## Goals

- unify the current marketing site and the current app into a single Nuxt experience
- preserve all current `ascentun` feature coverage
- support both new-visitor discovery and repeat player/follower usage
- expose players, teams, gauntlets, sponsors, and related public information without requiring login
- create a stronger public competition surface for stats, rankings, tournament history, and event discovery
- provide a durable structure for future lore, course, planet, manufacturer, and world-building content
- support logged-in player workflows such as Steam auth, wallet linking, and team management
- keep Eventun as the primary website backend integration point
- create a design artifact that can be used to derive implementation epics and sprint slices

## Non-Goals

- final visual design direction
- final navigation form factor decision between side nav, top nav, or hybrid nav
- implementation-level API contracts beyond high-level ownership and system boundaries
- wallet-only spectator auth in phase 1
- betting, bounties, or other regulated interaction systems in the initial watch scope
- a full CMS-backed editorial workflow in the first version

## Constraints

- Framework: Nuxt
- Existing feature parity with the current `ascentun` site is required
- Eventun is the source of truth for:
  - competition data
  - wallet state exposed to the website
  - sponsor data
  - website media metadata
- AccelByte is currently the source of truth for:
  - items
  - battle pass state
  - ELO/rating data
- Accountun should generally remain behind Eventun rather than being consumed directly by the site
- Initial auth model is Steam-only
- Wallets can be linked after Steam login
- Streaming API integrations are out of scope initially

## Core Product Decision

Build one unified Nuxt application with multiple public-use modes rather than separate marketing and application sites.

The site should support three experience modes:

1. Marketing public
   - for visitors who are learning what Ascent Rivals is
   - focused on branding, game footage, features, lore entry points, social links, and conversion actions

2. Competition public
   - for visitors who already know the game and want players, teams, gauntlets, standings, stats, and event context
   - largely accessible without login

3. Logged-in player/private overlays
   - for workflows that require account state, team state, wallet state, or user-specific participation context
   - private information should usually be layered into the public pages rather than isolated into an entirely separate product unless the workflow is inherently private

This avoids forcing a hard split between discovery and utility while still allowing the homepage and navigation system to adapt based on visitor context.

## Audience Model

### Primary audience

- players
- followers of players, teams, and tournaments

### Secondary audience

- press and general game-discovery visitors
- tournament organizers and administrators
- sponsors and partners

### Operational implication

Most of the site should be public.

Private areas should be limited to workflows such as:

- login and session-bound identity
- wallet linking
- team management actions
- admin-only sponsor and tournament operations
- user-specific competition context not intended for public display

## Site Experience Modes

### Homepage behavior

The homepage should adapt over time instead of being permanently marketing-first or competition-first.

Current direction:

- the root route should function as a player/competition command center
- new visitors should still encounter enough brand and game-context onboarding to understand Ascent Rivals
- returning users should reach search, gauntlets, course records, players, teams, and sponsors quickly
- logged-in users should see personalized competition context layered into the same public page
- the dedicated `/game` route should carry the heavier marketing/game overview work

The current page-level spec is [[pages/homepage]].

### Homepage module priorities

For anonymous visitors, the current homepage priority order is:

1. command hero with Ascent Rivals branding and a marketing/game bridge
2. search everywhere
3. active and upcoming gauntlets
4. high-level status strip
5. course record highlights
6. pilot highlights
7. generated system log from real snapshot data
8. optional sponsor strip

For logged-in users, the homepage should bias toward utility and immediate re-entry.

Current high-priority logged-in modules:

- search everywhere
- gauntlets with the user's current rank or participation context
- course leaderboard placement, where available
- career, wallet, and team links through the avatar menu

The homepage should therefore be treated as an adaptive composition problem, not as a single static landing page.

### Current shell concept candidate

The strongest reviewed shell concept so far is [[shell-concepts|Terminal Ops]].

Useful direction from that concept:

- command prompt-inspired top navigation
- terminal-style path/breadcrumb bars
- framed panels for data and entity surfaces
- telemetry/status strips as recurring context elements
- system-log style activity modules

This is not a final implementation decision.

Open questions remain around:

- whether prompt navigation replaces or complements side navigation
- how much monospace typography is appropriate
- how to make the concept gritty and physical enough without becoming a clean terminal dashboard
- how the shell adapts to mobile and data-heavy player pages

### Navigation behavior

Current preference is for a consistent navigation system across the site, likely influenced by the current app's side-navigation model.

However, the exact navigation pattern is intentionally still open:

- side navigation
- top navigation
- hybrid navigation

The design work should test these alternatives before the final information architecture is locked.

## Information Architecture Direction

The site should be organized around public entities first, not only around internal workflows.

### Likely top-level public areas

- Home
- Gauntlets / Events
- Players
- Teams
- Sponsors
- Watch
- Game
- Features
- Media
- Lore
- Courses
- FAQ
- Press

Not all of these need to appear in the initial primary navigation, but the content model should support them.

### Likely logged-in destinations

- My profile / career
- Wallets
- Team management
- User-specific gauntlet participation context

### Likely admin destinations

- sponsor management
- gauntlet creation/editing
- operational tournament controls already present in the current site

## Initial Page Map

This section captures the current page-priority model so the design work can stay anchored to concrete deliverables.

### Phase-1 must-have pages

- `/`
  - adaptive homepage
  - player/competition command center with lightweight branding
  - anonymous view should support search, current competition state, and a bridge to `/game`
  - logged-in view should layer in utility and personalized competition context
- `/game`
  - primary editorial or marketing page describing the game
- `/gauntlets`
  - public gauntlet and event discovery
- `/gauntlets/[id]`
  - public gauntlet detail with personalized overlays when logged in
- `/players`
  - public player directory
- `/players/[id]`
  - public player detail
- `/teams`
  - public team directory
- `/teams/[id]`
  - public team detail with management affordances when authorized
- `/sponsors`
  - sponsor and partner listing

### Phase-1 nice-to-have pages

- `/features`
- `/media`
- `/courses`
- `/press`

### Later pages

- `/watch`
- `/lore`
- `/faq`

### Preserved private and admin routes

Even when not called out in the public page inventory above, the new site must still preserve current authenticated and operational routes for:

- Steam login
- wallet linking and verification
- team creation and management
- gauntlet creation and management
- sponsor administration

## Feature Inventory

## Preserved from Current Site

All existing features from the current `ascentun` application should be preserved.

### Identity and auth

- Steam login
- session-aware navigation and account access
- player-associated identity context

### Players

- player directory
- public player profile
- player career stats
- course-level player stats

### Teams

- team directory
- public team profile
- team creation
- join team flows
- leave team flows
- invite flows
- join request flows
- team ownership and management actions
- team media management

### Gauntlets

- gauntlet list and detail pages
- gauntlet creation and editing
- qualifier views
- stage views
- standings
- stats
- sponsor association
- prize management and result flows already supported by the current app

### Wallets and entitlements

- wallet linking
- wallet verification
- Cardano wallet support
- Midnight wallet support

### Sponsors and operations

- sponsor list and sponsor detail
- sponsor CRUD/admin flows
- current admin-specific access controls

### Discovery

- global search across current core entities

## New or Expanded Public Capabilities

These are in scope for the long-term site design, though not all are phase-1 requirements.

### Marketing and brand

- a stronger branded homepage or landing experience
- game footage and feature showcases
- social and community links
- outbound links to YouTube and other channels
- Steam wishlist entry points
- richer Ascent Rivals world/brand presentation

### Public competition browsing

- stronger gauntlet/event discovery
- clearer distinction between current, upcoming, and past gauntlets
- event calendar views for qualifiers, finals, and showcase events
- public event and winner showcase pages
- broader historical context around tournaments and notable outcomes

### Public stats

- richer public player stats
- richer public team stats
- richer gauntlet stats
- historical ranking context
- medal and trophy display models
- future season-oriented views for general competitive play beyond specific tournaments

### Lore and world content

- general lore pages
- course and planet content
- manufacturer and ship-part lore
- narrative context for concepts such as obelisks and ascension zones

### Watch

- a dedicated `/watch` page
- embedded Twitch or YouTube live stream when relevant
- future VOD links via YouTube

## Entity Model for Presentation

The site should present several public entity types consistently.

### Competition entities

- gauntlets
- showcase events
- finals/brackets
- qualifiers
- stages

The underlying model can remain generic, but the presentation layer should be able to emphasize different event shapes when the catalog becomes richer.

Examples:

- qualifier-only gauntlets that behave more like matchmaking windows
- stage-only or bracket-only special events
- invite-only team events
- traditional gauntlets with qualifiers and finals
- sponsored prize events
- manually operated showcase or LAN events

The site should avoid over-splitting these too early if the live catalog is sparse.

### Public content entities

- players
- teams
- sponsors
- courses
- planets
- ship parts
- manufacturers

### Search entities

Search should eventually support grouped results across:

- players
- teams
- courses
- planets
- gauntlets
- sponsors
- ship parts

General lore should not be the first search priority and may instead be discoverable through dedicated content pages and entity relationships.

## Public Player Experience

The public player page should evolve beyond a simple stat card.

### Required direction

- basic public stats
- rankings and rank-tier presentation
- finish times and lap times by course
- gauntlet/tournament performance context
- public trophies for tournaments won
- public medals or badges only if a backend/API exposes safe public medal data

### Ranking privacy model

The exact ELO should remain private.

Publicly visible ranking information can include:

- public rank tier such as Bronze, Silver, Gold, and similar tiers
- historical rank progression across competitive seasons

This implies a split between:

- private raw rating data
- public rank presentation

### Public/private blending

The player experience should not create an entirely separate private profile unless needed.

When logged in, the player should often see additional personal context layered into the same surface rather than navigating to a wholly separate product area.

### Default public player page structure

The current default player-page structure is:

- Overview
- Course Stats
- Match History
- Gauntlet Results
- Trophies and Medals
- Rank History

This can be implemented as tabs, stacked sections, or a responsive hybrid, but the information model should remain stable.

Default first-view priority:

- identity and career totals first
- course stats and course placements second
- optional best-lap/best-finish strength modules only when the data supports them cleanly
- match-history overview later on the page, without a dedicated match-detail route in phase 1

## Private Player Experience

Private player functionality should remain intentionally small in phase 1.

### Phase-1 private priorities

- wallet linking and verification
- account-aware access to team state
- user-specific context embedded into otherwise public pages

Examples:

- a gauntlet page can show the logged-in user's current rank
- a gauntlet page can show whether the user has qualified
- a player/team surface can expose actions only relevant to the current user
- a player's own public profile can expose wallet and team actions
- a player's own public profile can show AccelByte-owned medals or badges if available through the logged-in token

### Deferred/private candidates

These may be added later but are not current launch requirements:

- owned items
- battle pass progress
- broader account settings
- notifications center
- reward history

## Team Experience

The team experience should preserve all current management flows and add a richer public surface.

### Public team direction

- roster
- team stats
- team standings in gauntlets
- medals earned by the team
- trophies earned in team-based finals
- public team history over time

### Private team direction

Private team actions can remain attached to the team context rather than moving to a separate profile/settings model.

This includes:

- invites
- join requests
- accepting/denying requests
- canceling a join request
- leaving a team
- promoting and demoting members
- kicking members
- editing media and team presentation

The team area should become materially more user-friendly than the current admin/developer-oriented implementation.

### Default public team page structure

The current default team-page structure is:

- Overview
- Roster
- Gauntlet Results
- Team Stats
- Trophies and Medals
- Manage

`Manage` should only appear for authorized users, but it should remain attached to the main team context rather than being treated as a disconnected admin surface.

## Gauntlet and Event Experience

Gauntlets are a central product surface and may eventually cover multiple event shapes.

### Required preserved behavior

- list and browse gauntlets
- detail pages
- qualifiers
- stages
- standings
- stats
- sponsor display
- prize display and claim/funding/result flows already supported by the current app

### Expanded direction

- differentiate current, upcoming, and past gauntlets
- support bracketed tournaments
- support invite-only tournaments
- support team tournaments
- show qualifier timelines and finals timing more clearly
- support event calendar views
- show sponsor associations prominently
- show prize pools and non-currency prizes in the presentation layer

### Listing model

The current preferred listing structure for `/gauntlets` is:

- emphasize current gauntlets
- emphasize upcoming gauntlets
- provide a separate way to browse past gauntlets
- optionally call out featured events when the catalog supports it

Calendar support is still desirable, but it should likely arrive later as a separate view unless the final design work shows that calendar-first discovery is materially better.

### Detail page priority order

The current gauntlet detail priority order is:

1. qualifiers
2. finals or brackets
3. personal status when logged in
4. hero and branding
5. sponsors
6. prize pool or prizes
7. watch stream
8. past winners or history

Standings remain required because they exist in the current site, but they may live within qualifier and finals sections rather than dominating the page structure on their own.

Terminology guardrail:

- qualifiers are gauntlet/tournament qualification windows and may span multiple sessions and matches
- heats are runtime rounds inside a match
- do not use qualifier and heat interchangeably in route names, API mocks, UI labels, or Pencil prompts

### Prize representation gap

The current prize API is primarily currency-oriented.

The website design should anticipate richer prize presentation such as:

- hardware prizes
- sponsored physical prizes
- showcase rewards

This may require presentation-layer accommodation before the underlying prize APIs are expanded.

## Match History and Match Detail

General standalone match-history browsing is not a priority as an independent site area.

Match history is more relevant when scoped to:

- a specific player
- a specific gauntlet

### Likely future match-detail support

- results
- per-heat breakdown
- player comparisons
- loadout context

### Not currently expected

- first-class VOD generation
- automated recap generation tied to the game

## Watch Experience

`/watch` is not a phase-1 must-have page.

## Initial direction when watch ships

- start with a YouTube VOD list
- allow an offline-but-useful watch surface even when no live stream exists
- later add embedded Twitch or YouTube live broadcasts when tournaments are actively being broadcast

## Deferred ideas

The following concepts are intentionally out of scope for the initial watch implementation:

- betting
- bounties on players
- advanced real-time spectator interaction
- deeper streaming API integrations

These are potentially interesting product directions but they introduce design, compliance, moderation, and economic complexity that should not be smuggled into the initial website scope.

## Marketing and Lore Structure

The content model should support both branded marketing content and deeper world-building content.

### Candidate content areas

- Game
- Features
- Media
- Lore
- Courses
- FAQ
- Press
- Sponsors
- Watch

### Current editorial structure direction

Early content should favor a few high-level editorial pages rather than trying to ship a large lore/wiki surface immediately.

Current page priority:

- `Must`: `Game`
- `Nice`: `Features`, `Media`, `Courses`, `Press`
- `Later`: `Lore`, `FAQ`, `Watch`

### Lore/content relationship model

Lore should not be treated only as a disconnected wiki.

Much of it should be reachable through entity relationships such as:

- course pages referencing planets
- ship parts referencing manufacturers
- event pages referencing world context where useful

This allows lore work to deepen the world without isolating it from the rest of the site.

## Search and Discovery

The long-term goal should be broad search coverage with grouped results.

Search-everywhere is also a homepage priority for logged-in users and should be treated as a core site primitive rather than a small convenience feature.

### High-priority entity groups

- gauntlets
- courses
- players
- teams
- sponsors
- planets
- ship parts

Search-everywhere behavior is desirable, but result grouping by entity type should remain explicit so the experience does not become noisy or ambiguous.

## Stats Architecture

The current direction is to ship richer stats inside entity pages first rather than creating a dedicated `/stats` hub in phase 1.

Current priority order for deeper stats surfaces:

1. gauntlets
2. courses
3. players
4. teams

This keeps the initial implementation anchored to the places where users already have strong intent instead of creating a separate stats destination too early.

## Auth and Personalization Model

## Phase-1 auth

- Steam login only

## Phase-1 account extension

- post-login wallet linking

## Personalization direction

Logged-in users should receive more game-focused entry points and more contextual information on public pages.

Examples:

- personalized competition context on gauntlet pages
- easy access to profile/avatar state
- easy access to wallets
- team-aware actions

Wallet-only spectator sign-in can be revisited later if spectator interaction systems become important.

## Data and System Boundaries

### Eventun

Primary website integration point for:

- competition data
- gauntlet, player, and team state exposed on the web
- sponsor data
- media metadata
- wallet state surfaced in the site
- mediated access to accounting-related data

### Accountun

- accounting execution remains an internal/domain service concern
- website usage should generally flow through Eventun rather than integrating Accountun directly

### AccelByte

Current external source of truth for:

- items
- battle pass state
- ELO/rating data

These may be surfaced on the website later, but they are not the primary phase-1 focus.

## Phased Delivery

## Phase 1

Unified branded site plus current core workflows with improved UX.

Primary outcomes:

- one Nuxt application
- preserved current operational features
- stronger public-facing polish
- better bridge between marketing and competition usage
- must-have public pages for home, game, gauntlets, players, teams, and sponsors
- stats embedded in entity pages rather than a separate stats hub
- adaptive homepage behavior for anonymous versus logged-in users

## Phase 2

Expanded gauntlet workflows for:

- bracketed tournaments
- invite-only tournaments
- team tournaments

## Phase 3

Gauntlet and event showcase.

Potential scope:

- historical winners
- manually run event showcases
- user-created gauntlet showcases
- prize and winner presentation
- season/circuit overview patterns if appropriate

## Phase 4

Lore and course details.

Potential scope:

- planets
- courses
- manufacturers
- world-building content

## Phase 5

Deeper stats.

Potential scope:

- richer comparisons
- more historical context
- more public stat surfaces across players, teams, and gauntlets

## Phase 6

Live streams.

Potential scope:

- dedicated watch experience
- embedded live broadcasts
- richer event-linked viewing

## Risks

- Trying to solve marketing, operations, competition discovery, stats, lore, and watch in a single pass will create an unfocused first version.
- Over-separating event types too early could make the site feel empty when the actual event volume is still low.
- Under-specifying the adaptive homepage could lead to a weak compromise that serves neither new users nor returning players well.
- Public/private blending is directionally correct, but it can produce confusing permission edges if actions are not clearly scoped.
- Richer prize presentation may outgrow the current prize APIs.
- Future interaction concepts such as betting or bounties should be treated as separate product and policy workstreams, not as simple website features.

## Open Questions

- What should the homepage do by default for:
  - anonymous first-time visitors
  - anonymous returning visitors
  - logged-in players
- Should navigation be:
  - side nav
  - top nav
  - hybrid
- How should seasonal rank history be modeled if general competitive seasons exist outside gauntlets?
- Which public event types should receive distinct listing categories versus shared listing/filter treatment?
- What authoring path will be used for homepage news or announcements if the site does not use a CMS?
- Which backend source should own course leaderboard aggregation and public rank-tier history presentation?
- When `/watch` ships, should the first live experience be embedded on gauntlet pages, on a dedicated page, or both?

## Initial Epic Breakdown

These are not yet sprint plans, but they are strong candidates for implementation epics and initial workstreams.

### 1. Unified shell and adaptive homepage

- common Nuxt shell
- navigation experiments and final shell decision
- anonymous versus logged-in homepage composition
- search-everywhere entry point

### 2. Public gauntlet discovery and detail redesign

- `/gauntlets` listing model
- current/upcoming/past separation
- featured-event treatment
- gauntlet detail layout with qualifier and finals emphasis
- personalized overlays when logged in

### 3. Public player experience redesign

- richer player overview
- course stats
- gauntlet results
- trophies and medals
- rank-history model

### 4. Public team experience redesign plus preserved management workflows

- richer public team pages
- team stats and historical results
- improved team management UX
- preserved invite, join-request, and roster-management flows

### 5. Marketing and editorial content foundation

- `/game`
- optional `/features`, `/media`, `/courses`, `/press`
- homepage announcements and brand modules
- Steam CTA and social-link integration

### 6. Sponsor and partner presentation

- public sponsor index
- sponsor relationship display on gauntlets and other surfaces
- preserved sponsor admin workflows

### 7. Shared data, auth, and personalization foundation

- Steam auth migration
- wallet linking migration
- Eventun integration foundation
- AccelByte-derived public data integration where needed
- session-aware personalization on public pages

### 8. Deferred content and watch foundation

- editorial lore expansion
- future watch page
- future VOD and live-stream support
- future calendar view support

## Validation Plan

- produce design passes for homepage, nav, and entity-page shell options
- define a page inventory for phase 1 and map each page to audience, auth level, and data dependencies
- derive implementation epics from the feature inventory
- validate that every existing `ascentun` workflow has a destination in the new site
- validate the Eventun and AccelByte integration boundaries before implementation work begins
