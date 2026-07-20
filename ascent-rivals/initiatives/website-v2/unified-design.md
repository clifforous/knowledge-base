# Ascent Rivals Unified Website Design

Date: 2026-04-10
Status: Draft
Framework decision updated: 2026-07-15

## Related
- [[ascent-rivals/system/overview|ascent-rivals-overview]]
- [[ascent-rivals/system/website|website]]
- [[ascent-rivals/system/eventun/overview|eventun]]
- [[ascent-rivals/system/accountun|accountun]]
- [[ascent-rivals/system/game-design|game-design]]
- [[ascent-rivals/archive/initiatives/website-v2/pencil-design-brief]]
- [[shell-concepts]]
- [[README|Website V2 initiative index]]
- [[information-architecture]]
- [[initial-release-scope]]
- [[non-functional-baseline]]
- [[delivery-plan]]
- [[route-api-matrix]]
- [[terminal-ops-design-system]]
- [[design-language-v0.1]]
- [[tone-and-voice]]
- [[flows/authentication]]
- [[flows/team-lifecycle]]
- [[ascent-rivals/initiatives/website-v2/pages/homepage]]
- [[ascent-rivals/initiatives/website-v2/pages/player-directory]]
- [[ascent-rivals/initiatives/website-v2/pages/player-profile]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlets-index]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlet-detail]]
- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]
- [[ascent-rivals/initiatives/website-v2/pages/teams-index]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]
- [[ascent-rivals/initiatives/website-v2/pages/sponsors-index]]
- [[flows/gauntlet-authoring]]
- [[ascent-rivals/initiatives/gauntlet-runtime/gauntlet-finals-and-tournament-modes-design-review]]

## Problem Statement

Ascent Rivals currently has a split web presence:

- a dev/admin-oriented application for players, teams, gauntlets, sponsors, wallets, and operations workflows
- a separate marketing-oriented website for brand and promotional content

That split is no longer aligned with the intended product experience.

The new website should be a single public-facing Next.js/React application that:

- supports discovery of the game for new visitors
- supports repeat usage for players and their followers
- preserves all approved non-blockchain operational and player-facing workflows
- expands into richer public stats, event discovery, lore, and eventually watch/live-stream features

The new site should feel cohesive across marketing, public competition browsing, and logged-in player workflows rather than behaving like disconnected products.

Tone direction:

- the site should feel like a shipboard computer or race operations terminal giving pilots, followers, and organizers precise competition intelligence
- terminal style should support clarity, not replace clear labels or accessible actions

## Goals

- unify the current marketing site and the current app into a single Next.js/React experience
- preserve all current non-blockchain `ascentun` feature coverage
- support both new-visitor discovery and repeat player/follower usage
- expose players, teams, gauntlets, courses, and related public information without requiring login
- create a stronger public competition surface for stats, rankings, tournament history, and event discovery
- provide a durable structure for future lore, course, planet, manufacturer, and world-building content
- support logged-in player workflows such as Steam auth and team management
- keep Eventun as the primary website backend integration point
- create a design artifact that can be used to derive implementation epics and sprint slices

## Non-Goals

- final visual design direction
- exact visual composition of the approved responsive top navigation at each measured width
- final endpoint, protobuf, or storage schemas; page-level Website API requirements remain in scope
- wallet-only spectator auth in phase 1
- betting, bounties, or other regulated interaction systems in the initial watch scope
- a CMS, MDX pipeline, or content framework in the initial release
- wallet linking, wallet management, token gating, or blockchain-dependent access in the initial release
- Accountun-related prize or reward presentation, configuration, funding, claims, payouts, wallet requirements, administration, or legacy workflow links in Website V2

## Constraints

- Framework: Next.js with React and TypeScript
- Repository direction: a new greenfield project rather than an extension of `ascent-website` or `ascentun`
- Existing website repositories are content, asset, behavior, and migration references only
- Existing non-blockchain feature parity with the current `ascentun` site is required
- Eventun is the source of truth for:
  - competition data, including course-record and leaderboard aggregation
  - sponsor data
  - website media metadata
- AccelByte is currently the source of truth for:
  - course configuration and feature state
  - items
  - battle pass state
  - ELO/rating data
- Website V2 does not consume Accountun or expose Accountun-related prize/reward data in the initial release
- Initial auth model is Steam-only
- Streaming API integrations are out of scope initially
- Legacy Ascentun remains only for the explicitly excluded Midnight/blockchain tournament workflows until those workflows are separately retired or relocated
- All current non-blockchain team, gauntlet, sponsor, and media-administration workflows move to Website V2 at launch
- Website V2 follows the planned team feature work; team analytics are launch requirements, while their exact presentation is finalized against the implemented team contracts

## Core Product Decision

Build one unified Next.js/React application with multiple public-use modes rather than separate marketing and application sites.

## Framework and Repository Decision

Decision date: 2026-07-15

Use a new greenfield Next.js/React project for Website V2.

Rationale:

- React and Next.js remain the most maintainable choice for the current developer workflow.
- The ecosystem provides broad support for AI-assisted implementation, code review, design translation, accessible primitives, and common web tooling.
- Choosing a less familiar server or UI stack would add implementation and operational novelty without addressing a current product requirement.
- Starting from a new project avoids inheriting the structure, visual assumptions, and deferred legacy workflows of either current website.

Default design implementation loop:

1. implement an approved design or design revision in the application;
2. review the code;
3. inspect the result manually in the browser at the required responsive sizes;
4. iterate until the visual and functional review passes.

Storybook, automated screenshots, and visual-regression tooling are optional. Add them only when repeated component states, collaboration needs, or regression risk justify their ongoing cost.

This decision supersedes Nuxt/Vue/Reka UI references in the decomposed Website V2 drafts. Those references should be reconciled during the dedicated knowledge-base cleanup rather than treated as active constraints.

## Marketing Content Authoring Decision

Decision date: 2026-07-15

Keep the initial marketing-content workflow inside the Next.js repository using ordinary TypeScript and TSX.

- Keep short, layout-specific copy beside the component that presents it.
- Place long or structured route content in a typed `content.ts` file beside the route.
- Use shared typed content models only for repeated structures such as editorial event pages.
- Store each event's content in its own route-local content file, while allowing bespoke sections when a design cannot be represented cleanly by the shared model.
- Keep title, description, canonical URL, and social-image metadata with the route content they describe.
- Organize static assets by route or event slug using predictable repository paths.
- Do not introduce a CMS, MDX, content collection, or global copy registry for the initial release.

Content update loop:

1. designer supplies the approved mock, copy, and assets;
2. developer or coding agent updates the route, component, or typed content module;
3. changes receive code review and manual responsive browser review;
4. the content and implementation ship together.

The site should support three experience modes:

1. Marketing public
   - for visitors who are learning what Ascent Rivals is
   - focused on branding, game footage, features, lore entry points, social links, and conversion actions

2. Competition public
   - for visitors who already know the game and want players, teams, gauntlets, standings, stats, and event context
   - largely accessible without login

3. Logged-in player/private overlays
   - for workflows that require account state, team state, or user-specific participation context
   - private information should usually be layered into the public pages rather than isolated into an entirely separate product unless the workflow is inherently private

This avoids forcing a hard split between discovery and utility while still allowing navigation and selected modules to adapt based on visitor context.

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
- team management actions
- admin-only sponsor and tournament operations
- user-specific competition context not intended for public display

## Site Experience Modes

### Homepage behavior

Decision updated: 2026-07-16

Current direction:

- the root route `/` is the primary marketing and conversion homepage
- `/gauntlets` is the primary entry into competition and player-facing utility
- the homepage may use one bounded current-competition or recent-event teaser, but should not become a competition dashboard
- logged-in users may receive light personalization within fixed content slots without changing section order, module placement, responsive composition, or the page's primary marketing purpose; confirmed game ownership may replace the repeated `Play Now` emphasis with an `Explore Gauntlets` primary action, while sign-in alone does not prove ownership
- `/game` is deferred from the initial route map and should be added later only if a deeper game-systems overview can avoid duplicating the homepage

The [[ascent-rivals/initiatives/website-v2/pages/homepage]] specification now records the approved marketing-first hierarchy and replaces the superseded command-center homepage direction.

### Homepage module priorities

The approved homepage priority order is:

1. hero and primary conversion, using accurate `Play Now` or release-state copy
2. gameplay and Ascension Mode
3. ships and customization
4. one optional bounded race-network proof module
5. worlds, planets, and courses
6. events and community
7. final conversion and next actions

For logged-in users, preserve the same section order, module placement, responsive composition, and CTA region. Personalization may change copy, actions, or data inside an existing slot but must not create an authenticated layout variant. When reliable server-side data confirms ownership of the relevant Steam application, the hero and final CTA may prioritize `Explore Gauntlets` and retain a smaller accurate Steam play/launch action. Do not infer ownership from sign-in or claim to know installation state.

Possible logged-in enhancements:

- ownership-aware hero and final conversion actions when ownership is reliably confirmed
- a current or upcoming gauntlet teaser with participation context
- direct links to career or team destinations through the account menu

Personalization must remain additive and should not create a separate homepage information architecture.

The optional race-network module selects at most one featured item, with up to two compact supporting links: prefer a reliably active public gauntlet, then an upcoming gauntlet, a recently completed gauntlet with verified context, or a code-authored `/events` recap. Omit the module when none is strong enough. Do not add homepage telemetry, generated system logs, or multiple leaderboard/data panels.

### Existing homepage migration decision

Preserve the current marketing homepage's useful content categories, not its implementation or layout.

Preserve as inputs:

- hero and Steam conversion intent
- gameplay feature explanation
- gameplay video
- ship customization proof
- gallery or current media proof
- verified partners
- community links

Migration requirements:

- rewrite or revalidate all copy and gameplay claims
- refresh screenshots, video, partner approvals, and conversion wording
- rebuild layout and components from scratch in the revised Terminal Ops sci-fi direction
- treat current backgrounds, clipping treatments, styling, and React components as references only
- add one optional Website V2 race-network teaser that routes to `/gauntlets` or an explicitly labeled editorial fallback under `/events`

### Current shell concept candidate

The strongest reviewed shell concept so far is [[shell-concepts|Terminal Ops]].

Useful direction from that concept:

- command prompt-inspired top navigation
- terminal-style path/breadcrumb bars
- framed panels for data and entity surfaces
- telemetry/status strips as recurring context elements
- system-log style activity modules

The global navigation decision is now final at the information-architecture level: use one responsive top bar with stable `Gauntlets`, `Pilots`, `Teams`, `Courses`, and `Events` destinations, plus search and login/account. Do not add a persistent global side navigation or separate marketing/competition bridge control. Page-local tabs, rails, or section navigation remain available where a complex entity page needs them.

Visual implementation questions remain around typography, physical material treatment, and the exact compact/mobile composition. Resolve those through mocks without changing the approved route order or accessibility model.

### Navigation behavior

Use the approved consistent responsive top bar. Wide layouts may show all five primary destinations. As available width decreases, move `Events` and then other destinations from the right side of the ordered list into `More`; never wrap, compress, or ambiguously abbreviate labels. Mobile retains brand, search, menu, and login/account controls and places the complete destination list in the drawer. `About` and `Brand` remain secondary menu/footer destinations, and authorized sponsor operations live in the account/admin menu.

## Information Architecture Direction

The site should be organized around public entities first, not only around internal workflows.

### Likely top-level public areas

- Home
- Gauntlets
- Events
- Players
- Teams
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

- My Career through the approved account menu
- My Team through the approved account menu, with pending invitation/request status when relevant
- User-specific gauntlet participation context

`Admin / Operations` appears in the account menu only when authorized and when at least one destination exists. `Sign Out` remains a distinct final action. Team/gauntlet creation, editing, and other object-specific actions stay on their relevant pages rather than becoming global account-menu entries.

### Likely admin destinations

- sponsor management
- gauntlet creation/editing
- operational tournament controls already present in the current site

## Initial Page Map

This section captures the current page-priority model so the design work can stay anchored to concrete deliverables.

### Phase-1 must-have pages

- `/`
  - primary marketing and conversion homepage
  - may include selected competition and community proof
  - provides a clear bridge to `/gauntlets`
- `/gauntlets`
  - public gauntlet and event discovery
- `/gauntlets/[id]`
  - public gauntlet detail with personalized overlays when logged in
- `/events`
  - code-authored editorial listing for LANs, showcases, sponsored tournaments, historical competitions, and recordings
- `/events/[slug]`
  - code-authored editorial event detail; may link to a related gauntlet or legacy operational workflow when applicable
- `/about`
  - concise studio story, mission, current team, and verified recognition
- `/brand`
  - verified logo downloads and usage rules, rebuilt against the approved Website V2 visual direction
- `/players`
  - public player directory
- `/players/[id]`
  - public player detail
- `/teams`
  - public team directory
- `/teams/[id]`
  - public team detail with management affordances when authorized
- `/courses`
  - course discovery, search, and cross-course summaries
- `/courses/[code]`
  - shareable course briefing, category leaderboard, records, and pilot placement context

### Phase-1 nice-to-have pages

- `/features`
- `/media`
- `/press`

### Later pages

- `/game`
  - conditional deeper game-systems overview once enough distinct content exists
- `/watch`
- `/lore`
- `/faq`

### Preserved private routes and external operations handoff

Even when not called out in the public page inventory above, the new site must still preserve current authenticated and operational routes for:

- Steam login
- team creation and management
- gauntlet creation and management

Administrator-only sponsor administration and sponsor-owned media move to the Eventun Extend App before cutover. Website V2 does not preserve the Ascentun sponsor routes.

Accountun-related prize and reward data is entirely deferred. Legacy workflows may continue independently, but Website V2 does not expose or link them and they are not parity requirements. Verified prize descriptions may still appear as code-authored promotional copy on a related editorial event page.

## Feature Inventory

## Preserved from Current Site

All approved non-blockchain features from the current `ascentun` application should be preserved. The detailed behavioral inventory, exclusions, and Eventun readiness gates are defined in [[initial-release-scope]].

### Identity and auth

- Steam login
- session-aware navigation and account access
- player-associated identity context

### Players

- public pilot registry containing every real pilot with a usable public identity, including zero-match and inactive pilots
- compact unpaginated directory collection with client-side name/team search, sorting, filtering, and progressive display
- bot, test, and internal exclusion only through explicit source-system classification
- player cards use one pilot avatar, responsive `[TAG] Team Name` identity, and `Independent` for unaffiliated pilots; team colors are restrained accents rather than arbitrary tag foreground/background fills
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
- `/gauntlets` defaults to a unique-gauntlet `Current & Upcoming` directory sorted by active or nearest future occurrence, with `Past` as a URL-backed secondary scope
- the alternate URL-backed `Schedule` view is a chronological agenda of qualifier and stage occurrences and may repeat one gauntlet for multiple windows
- long-lived and ad hoc playtest gauntlets are current only during an actual occurrence window; between windows they sort by the next occurrence and move to Past when none exists
- schedule overlap supports `Current`, `Upcoming`, and `Past` timing language but not `Live`; stronger runtime/completion language requires an explicit state contract
- one compact, unpaginated Eventun discovery collection supplies shallow public identity/media, normalized occurrences, server time, and derived active/next/latest occurrence summaries for the directory, Schedule, homepage teaser, and search
- gauntlet creation and editing
- qualifier views
- stage views
- standings
- stats
- direct gauntlet advertising-media upload and optional sponsor-entity association
- non-blockchain create, edit, and delete workflows

Core create/edit uses one sectioned form with Core Details, Competition Structure, Branding and Advertising, and Review and Save. It is not a wizard, has no implied draft/autosave state, and does not absorb bracket authoring. See [[flows/gauntlet-authoring]].

Keep that core form in Website V2 so Eventun's delegated `gauntlet_creator` role and creator-ownership rules remain supported. Use the Eventun Extend App UI for initially administrator-only bracket generation/publication/repair and runtime result or stage-operation repair. Do not duplicate the core form in both surfaces. Website V2 still renders published bracket and match state when those public contracts ship; public rendering does not imply mutation permission.

The discovery contract is domain-neutral rather than named or shaped for one Website component. Website V2 is its first approved consumer. A later review should evaluate migrating public game-client discovery to the same read, while leaving runtime admission, detailed configuration, and operator APIs separate where their responsibilities differ. Existing game-client reads remain until that consumer review and migration occur.

### Explicit legacy exclusions

- wallet linking, verification, and management
- Cardano and Midnight wallet support
- token-gated teams and token catalogs
- all Accountun-related prize/reward presentation and workflows

### Sponsors and operations

- sponsor list/detail, CRUD, and sponsor-owned media administration in the Eventun Extend App;
- current Eventun Admin authorization, corrected atomic mutation contracts, and an administrator-authorized media upload boundary;
- no Website V2 sponsor registry or administration routes.

Terminology boundary:

- `Sponsor` is the Eventun-backed competition entity used in Extend App administration and optional gauntlet relationships;
- direct gauntlet-owned `Billboard` media are the primary initial creator workflow because tournament campaigns and artwork frequently vary; use explicit `Tileable` metadata and a three-copy tile preview for ribbon-style placement compatibility rather than a distinct new `WideBillboard` upload;
- retain an existing-sponsor picker as a scoped advanced gauntlet-authoring control without granting creators general registry access;
- sponsor registry/detail routes do not exist in Website V2; approved sponsor branding may still appear within its gauntlet context without exposing operational tier or linking to an operations surface;
- `Partner` is a broader code-authored marketing relationship and does not imply Eventun sponsorship;
- defer `/partners` until distinct partner content and ownership justify a separate route.

Do not infer custom Website behavior from every configured media-purpose label. Initial media management uses shared labeled upload and thumbnail controls except where a verified consumer, such as tileable billboard placement, requires a narrow purpose-specific control. Automatic image-dimension capture, aspect-ratio classification, and placement-slot matching belong to the later advertising redesign.

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
- richer public team stats, initially secondary to individual pilot results and subject to post-implementation review
- richer gauntlet stats
- exact course and gauntlet ranking context
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
- sponsored events
- manually operated showcase or LAN events

The site should avoid over-splitting these too early if the live catalog is sparse.

### Public content entities

- players
- teams
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
- ship parts

A later permission-filtered administrative group may add Eventun sponsors through a separate authenticated response. Sponsor records are not public content entities or public/general creator search results.

General lore should not be the first search priority and may instead be discoverable through dedicated content pages and entity relationships.

## Public Player Experience

The public player page should evolve beyond a simple stat card.

### Required direction

- basic public stats
- exact per-course leaderboard positions and gauntlet standings in their scoped contexts
- finish times and lap times by course
- gauntlet/tournament performance context
- completed public Eventun achievements/masteries
- known Eventun gameplay-medal totals through a safe public presentation contract

### Ranking privacy model

The initial Website has no generic global rank tier, named division, or rank-history surface. The current AccelByte MMR V2 is an internal lifetime skill estimate for the item recommender. It is not a public rank, leaderboard, matchmaking input, or stable history contract.

Publicly visible ranking information is limited to explicitly scoped competition facts:

- per-course leaderboard positions for an explicit category;
- gauntlet qualifier or stage standings with their actual semantics.

The current player may be able to retrieve their exact MMR from AccelByte, but Website V2 does not expose it because no approved Website use requires it.

A future Eventun-owned public division layer may map internal rating evidence into named divisions such as Bronze or Diamond. It may use stateful promotion thresholds, delayed promotion, or hysteresis rather than instant numeric bands. That is a separate product and backend design covering source atomicity, update ordering, provisional state, calibration, promotion and demotion, mode and season scope, correction, privacy, and history. The Website must not derive divisions from MMR or reuse item-recommender bands.

### Public/private blending

The player experience should not create an entirely separate private profile unless needed.

When logged in, the player should often see additional personal context layered into the same surface rather than navigating to a wholly separate product area.

### Default public player page structure

The current default player-page structure is:

- Overview
- Course Stats
- Recent Races
- Gauntlets, presented as `Gauntlet History`
- Achievements & Medals

This can be implemented as tabs, stacked sections, or a responsive hybrid, but the information model should remain stable.

The initial `Gauntlet History` is a compact structure-aware collection rather than one cross-gauntlet performance chart. Active gauntlets with real public player results appear first; completed entries follow in order of the player's latest actual participation. Qualifier standing, accepted stage placement, and generic race participation remain separate result types. Invitation, eligibility, admission, group, and status-only state are not public profile history. Eventun should provide this as one Website-oriented projection with presentation metadata and explicit result presence rather than require browser-side N+1 composition.

The initial `Achievements & Medals` section presents completed public Eventun achievements and masteries before known gameplay-medal totals. It is text-first and may use approved authored presentation assets when available. It does not infer trophies from stage placements or expose active challenges, incomplete progress, raw counters/dimensions, source identifiers, or reward data. Eventun should provide a purpose-built public recognition projection and explicit historical-coverage metadata when medal totals are not complete career totals.

Default first-view priority:

- identity and career totals first
- course stats and course placements second
- optional best-lap/best-finish strength modules only when the data supports them cleanly
- `Recent Races` overview later on the page, without a dedicated match-detail route in phase 1

## Private Player Experience

Private player functionality should remain intentionally small in phase 1.

### Phase-1 private priorities

- account-aware access to team state
- user-specific context embedded into otherwise public pages

Examples:

- a gauntlet page can show the logged-in user's current rank
- a gauntlet page can show whether the user has qualified
- a player/team surface can expose actions only relevant to the current user
- a player's own public profile can expose team and account actions
- a future self-only progression destination can show active goals or challenges only after that surface is separately approved

### Deferred/private candidates

These may be added later but are not current launch requirements:

- owned items
- battle pass progress
- broader account settings
- notifications center

## Team Experience

The team experience should preserve all current management flows and add a richer public surface.

### Public team direction

- roster
- public membership mode using `Open`, `Request to Join`, or `Invite Only` for every audience
- prominent individual pilot identities and profile links
- fact-backed team stats as a secondary launch surface, with exact modules re-evaluated after team-feature iteration
- team standings in gauntlets only when the competition defines team-result semantics
- medals earned by the team
- trophies earned in team-based finals
- public team history over time

### Private team direction

Private team actions can remain attached to the team context rather than moving to a separate profile/settings model.

Route decision:

- `/teams/[id]` remains the public team context and owns ordinary join/request/leave actions;
- `/teams/[id]/manage` is the dedicated permissioned workspace for metadata, media, roster administration, invitations, requests, ownership transfer, and disbanding;
- a contextual `Manage Team` action connects the two routes and the management view retains the selected team's identity.

Membership-mode decision:

- use the stable public labels `Open`, `Request to Join`, and `Invite Only`;
- show the same label to anonymous and authenticated visitors;
- vary the available action according to authentication, current membership, and invitation state;
- map the reviewed new-team enums to these labels rather than exposing backend terminology directly.

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

### Expanded direction

- distinguish unique gauntlet discovery from qualifier/stage occurrence scheduling
- classify directory relevance from an active or nearest future occurrence rather than the broad first-to-final gauntlet span
- support bracketed tournaments
- support invite-only tournaments
- support team tournaments
- show qualifier timelines and finals timing more clearly
- support a responsive chronological Schedule agenda that may repeat one gauntlet for separate occurrences
- show an approved sponsor association when one exists, but do not infer sponsor identity from direct billboard artwork

### Listing model

The current preferred listing structure for `/gauntlets` is:

- default to a unique-gauntlet `Current & Upcoming` scope;
- sort active occurrence windows first and remaining gauntlets by their nearest future occurrence;
- keep `Past` as a URL-backed secondary scope;
- keep every successfully created gauntlet public; Past is a discovery scope rather than a hidden or unpublished state;
- provide `Schedule` as a URL-backed chronological occurrence agenda where one gauntlet may appear multiple times;
- avoid separate empty Current and Upcoming bands.

Do not add a dedicated calendar route until it provides value beyond the initial responsive Schedule agenda. Schedule-derived timing supports Current, Upcoming, and Past labels but does not justify `Live` without an explicit runtime or broadcast contract.

The initial release has no gauntlet draft/public lifecycle. Successful creation publishes the gauntlet immediately. Any future private draft, embargo, cancellation, or administrative suppression feature requires explicit Eventun state and authorization rather than a Website-only inference.

### Detail page priority order

The current gauntlet detail priority order is:

1. qualifiers
2. finals or brackets
3. personal status when logged in
4. hero and branding
5. sponsors
6. watch stream
7. past winners or history

Standings remain required because they exist in the current site, but they may live within qualifier and finals sections rather than dominating the page structure on their own.

Terminology guardrail:

- qualifiers are gauntlet/tournament qualification windows and may span multiple sessions and matches
- heats are runtime rounds inside a match
- do not use qualifier and heat interchangeably in route names, API mocks, UI labels, or Pencil prompts

### Prize and reward boundary

Prize and reward data is Accountun-related and entirely deferred from Website V2.

- do not integrate Accountun into Website V2 for the initial release;
- do not display prize pools, reward descriptions, distribution, funding, claims, payouts, wallet requirements, or reward state;
- do not link public or authenticated Website V2 surfaces into legacy prize/reward workflows;
- permit verified code-authored promotional prize copy on `/events/[slug]` without Accountun reads or live funding/eligibility/claim/payout implications;
- revisit the product, authorization, and system boundary as one deliberate later design rather than preserving partial presentation.

## Recent Races and Future Match Detail

General standalone match-history browsing is not a priority as an independent site area.

Match history is more relevant when scoped to:

- a specific player
- a specific gauntlet

The initial player-profile surface is `Recent Races`, not complete account activity:

- at most the newest 100 server-backed multiplayer matches;
- public published/archived courses only;
- time trials, Career Cup, and other single-player play excluded, while retained best lap and finish records remain on course/career surfaces;
- exact newest-first table as the canonical view;
- optional discrete raw circuit-points chart for recent Ascent Mode matches, with no rolling/improvement trend;
- client-side filtering and progressive display over the returned collection;
- Eventun season grouping after the implemented season-attribution contract is reviewed.

The Website response must preserve missing-versus-zero match-stat semantics and remove unused client version, replay, session, match, and hidden-course data before it reaches the browser.

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

Current broadcasts are user-operated: a shoutcaster launches the game, joins as a spectator, and streams the client through their own Twitch channel. Eventun does not currently provide a canonical broadcaster, stream URL, or reliable live-status contract for Website V2.

## Initial direction when watch ships

- start with a YouTube VOD list
- allow an offline-but-useful watch surface even when no live stream exists
- permit manually verified Twitch, YouTube, or VOD links on code-authored event pages before a first-party watch system exists
- consider embedded live broadcasts only after broadcaster authorization, spectator admission, stream registration, status, moderation, and ownership are designed
- never auto-discover a user's personal stream or fabricate a `Live` state

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
- Partners, if separately verified code-authored content later justifies a route
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

Search-everywhere is a persistent shared-shell utility for anonymous and logged-in visitors. It should be treated as a core site primitive without becoming a separate homepage dashboard module.

### High-priority entity groups

- gauntlets
- courses
- players
- teams
- planets
- ship parts

Sponsor lookup is an authorized operational search group rather than part of public search-everywhere.

Search-everywhere behavior is desirable, but result grouping by entity type should remain explicit so the experience does not become noisy or ambiguous.

## Stats Architecture

The initial replacement release ships richer stats inside entity pages rather than creating a dedicated `/stats` hub.

Current priority order for deeper stats surfaces:

1. pilots
2. courses
3. teams
4. gauntlets

Individual pilot performance remains the primary competitive lens during the current design phase. Team analytics stay in launch scope, but they must not displace pilot profiles, roster members, or exact individual results until the team implementation and its real usage have been reviewed.

Tables remain the primary representation for exact standings, leaderboards, rosters, schedules, and match rows. Visualizations are required where they communicate a bounded trend, comparison, gap, or contribution more clearly than a table. They must not imply population percentiles from top-N data, compare unlike course times on one scale, or derive historical team performance from current rosters.

Eventun F14 supplies incremental pilot career, pilot-course career, current-record, player-rank, recent-match-history, and gauntlet read paths in its current worktree. Website launch depends on F14 review and the F15 production backfill/cutover. Credible team analytics also depend on the planned T03 fact-backed team reads and event-time membership attribution after the F15/T00 checkpoint.

See [[initial-release-scope]] for the initial analytics matrix and contract gaps.

## Auth and Personalization Model

## Phase-1 auth

- Steam login only

## Personalization direction

Logged-in users should receive more game-focused entry points and more contextual information on public pages.

Examples:

- personalized competition context on gauntlet pages
- easy access to profile/avatar state
- team-aware actions

Wallet-only spectator sign-in can be revisited later if spectator interaction systems become important.

## Data and System Boundaries

### Eventun

Primary website integration point for:

- competition data, including authoritative course-record and leaderboard aggregation
- gauntlet, player, and team state exposed on the web
- sponsor data
- media metadata

Existing game-client endpoints are reusable inputs, not a fixed Website contract. Extend Eventun or add purpose-built Website read endpoints when a page requires different authoritative aggregation, bounded series, visibility semantics, or response composition. Ordinary directory filtering and pagination controls do not by themselves justify a new server contract.

### Website-facing read contracts

- reuse an existing endpoint when its meaning and shape fit the Website requirement cleanly;
- prefer server-computed, authoritative metrics and aggregates over reconstruction in React or browser code;
- allow the Next.js server layer to authenticate, cache, and compose responses, but do not make it a competing system of record;
- add stable Website-oriented contracts when reusing several client-oriented calls would create N+1 access, inconsistent snapshots, excessive payloads, or duplicated metric logic;
- include explicit metric meaning, unit, scope, time window, freshness/as-of context, pagination, and null/no-data behavior where applicable;
- preserve source-system visibility and permission rules on the server rather than filtering sensitive records only in the browser;
- keep implementation and validation details that could assist event forgery or abuse out of public response metadata and UI copy.

The browser integration boundary is now explicit: generated Eventun gateway clients, AccelByte service credentials, and player tokens remain server-only. Server Components and server-only data functions obtain initial reads; same-origin Server Actions or route handlers own authenticated refreshes and mutations; direct browser transfer is limited to authorized signed media uploads. Browser components receive deliberate view models rather than complete generated transport records. See [[route-api-matrix]].

### Rendering and caching

Use Next.js 16 Cache Components with explicit public data/component caching rather than blanket caching of mixed public and private routes. Repository-authored marketing content is static by deployment. Public entity and directory reads use domain-tagged stale-while-revalidate caching, schedule-sensitive gauntlet data uses short or occurrence-boundary-aware freshness, and standings/recent results use short caching with explicit refresh where useful. Authenticated overlays, permissions, forms, and operations remain request-time and never enter the shared public cache.

Successful mutations invalidate affected entity and collection tags before the canonical public page is treated as refreshed. The approved Vercel Pro deployment baseline uses two fixed Website environments paired to the matching AccelByte/Eventun environments, protected development-only previews, the Node.js runtime, and an initial single function region near the backends. Project names, measured region, hostnames, branch promotion, and DNS/cutover remain implementation setup. See [[non-functional-baseline]] and [[delivery-plan]].

### Collection loading and pagination

- Default every initial collection experience to one compact, cacheable response followed by client-side search, filtering, sorting, and display pagination.
- This applies initially to gauntlets, courses, players, teams, and collection-style history modules; deliberately scoped recent/top-N data remains valid when it is the actual product view rather than disguised data pagination.
- UI pagination, progressive reveal, infinite-style loading, and virtualization are presentation alternatives over the locally held collection; they do not require server pagination.
- Exclude unneeded nested detail from collection responses so complete collection loading does not mean loading every entity's full page payload.
- Do not require a server-side cursor or page contract in the initial release, including for histories.
- Introduce server pagination only after measured database query time, response transfer, parse/hydration cost, memory, or interaction latency becomes material; histories and feeds are likely to reach that point first.
- Do not use a fixed entity-count threshold as a substitute for measurements, and do not introduce server pagination solely for hypothetical future scale.

### Accountun

- accounting execution remains an internal/domain service concern
- Website V2 has no initial Accountun integration and exposes no Accountun-related prize or reward data

### AccelByte

Current external source of truth for:

- course configuration and feature state
- items
- battle pass state
- ELO/rating data

These may be surfaced on the website later, but they are not the primary phase-1 focus.

## Phased Delivery

## Phase 1

Replacement branded site plus current non-blockchain workflows and improved public analytics.

Primary outcomes:

- one greenfield Next.js/React application
- preserved current non-blockchain operational features
- stronger public-facing polish
- better bridge between marketing and competition usage
- must-have public pages for home, events, about, brand, gauntlets, players, teams, and courses
- pilot, course, and team analytics embedded in entity pages rather than a separate stats hub
- adaptive homepage behavior for anonymous versus logged-in users
- production-cut-over Eventun reads for statistics, with fact-backed team attribution rather than current-roster inference

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
- winner presentation
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
- Treating the replacement target as a visual merge without migrating authenticated non-blockchain operations would leave a second operational site in place.
- Team charts are incorrect until Eventun can attribute performance to membership at event time; summing current roster careers is not an acceptable shortcut.
- Over-separating event types too early could make the site feel empty when the actual event volume is still low.
- Overloading the marketing homepage with player utility could weaken conversion and recreate the superseded command-center compromise.
- Public/private blending is directionally correct, but it can produce confusing permission edges if actions are not clearly scoped.
- Accidentally preserving prize/reward fragments would create an undefined Accountun and authorization boundary; exclude the area completely until it is redesigned.
- Future interaction concepts such as betting or bounties should be treated as separate product and policy workstreams, not as simple website features.

## Open Questions

- Which supported source can confirm Steam ownership for homepage CTA personalization in the Shared Cloud architecture?
- Should the bounded homepage race-network item use code-authored curation, an Eventun feature marker, or a deterministic state/recency rule?
- Which public event types should receive distinct listing categories versus shared listing/filter treatment?
- When `/watch` ships, should the first live experience be embedded on gauntlet pages, on a dedicated page, or both?

## Initial Epic Breakdown

These are not yet sprint plans, but they are strong candidates for implementation epics and initial workstreams.

### 1. Unified shell and marketing homepage

- common Next.js/React shell
- implementation of the approved responsive top-bar and page-local navigation model
- marketing proposition and conversion path
- limited anonymous versus logged-in personalization
- competition bridge to `/gauntlets`

### 2. Public gauntlet discovery and detail redesign

- `/gauntlets` listing model
- current/upcoming/past separation
- featured-event treatment
- gauntlet detail layout with qualifier and finals emphasis
- personalized overlays when logged in

### 3. Public player experience redesign

- richer player overview
- course stats
- structure-aware gauntlet history
- achievements and gameplay medals
- no global rank/history module until a separate Eventun public-division design is approved

### 4. Public team experience redesign plus preserved management workflows

- richer public team pages
- team stats and historical results
- improved team management UX
- preserved invite, join-request, and roster-management flows

### 5. Marketing and editorial content foundation

- `/` marketing homepage
- optional `/features`, `/media`, `/courses`, `/press`
- homepage announcements and brand modules
- Steam CTA and social-link integration

### 6. Sponsor and partner presentation

- administrator-only sponsor registry/detail and media management in the Eventun Extend App
- approved sponsor relationship display in public gauntlet context without a public sponsor profile link
- preserved sponsor admin workflows as an explicit Website parity handoff
- direct gauntlet `Billboard` upload as the primary creator path, with explicit tileable metadata and reusable sponsor association optional/advanced
- code-authored partner presentation where separately verified

### 7. Shared data, auth, and personalization foundation

- Steam auth migration
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
- validate that every approved non-blockchain `ascentun` workflow has a destination in the new site
- validate that excluded wallet, token-gating, and all Accountun prize/reward data and links remain outside Website V2 acceptance criteria
- validate the Eventun and AccelByte integration boundaries before implementation work begins
- use code review and manual browser review as the default visual validation loop
- introduce isolated component workshops or automated screenshot comparison only where their value exceeds their maintenance and AI-token cost
