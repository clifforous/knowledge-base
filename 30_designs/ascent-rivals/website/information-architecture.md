# Ascent Rivals Website Information Architecture

Date: 2026-04-13
Status: Draft

## Related
- [[unified-design]]
- [[design-doc-roadmap]]
- [[shell-concepts]]
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
- [[pencil-design-brief]]
- [[../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]

## Purpose

This note defines the route, navigation, and page-state model for the unified Ascent Rivals website.

It is the first decomposition of the broader [[unified-design]] document.

## Working Navigation Decision

Use top-bar-based global navigation.

This is now the working direction for the new Nuxt site.

The top bar can adapt by site context:

- marketing context
- competition/player context
- logged-in player context
- admin/operations context

Page-local subnavigation should live inside pages instead of relying on a persistent global side navigation.

## Core Cross-Site Bridge Rule

There must always be a visible top-bar link between the marketing side and the player/competition side of the site.

The label is not final, but the behavior is required.

Example behavior:

- When a visitor is on the player/competition side, the top bar includes a link such as `Marketing`, `Game`, or `About Ascent`.
- When a visitor is on the marketing side, the top bar includes a link such as `Player Side`, `Pilot Portal`, `Competition`, or `Gauntlets`.

Purpose:

- new visitors can move from brand/game context into player and tournament context
- returning players can quickly return from marketing/editorial pages to gauntlets, players, teams, and stats
- the unified site does not feel like two disconnected products

Open naming question:

- choose final labels after testing mocks and confirming the top-level IA language

## Navigation Principles

### 1. Global nav is for major destinations

The top bar should expose major site areas, not every action.

Examples:

- Game
- Gauntlets
- Players
- Teams
- Sponsors
- Search
- Login / avatar menu

### 2. Context changes nav emphasis

The global nav can shift emphasis depending on where the user is.

Marketing pages can emphasize:

- Game
- Features
- Media
- Press
- Wishlist / Play

Competition/player pages can emphasize:

- Gauntlets
- Players
- Teams
- Sponsors
- Courses
- Search

Logged-in contexts can expose:

- user avatar
- profile/career
- wallets
- team state
- relevant management shortcuts

### 3. Page-local navigation handles depth

Detailed page sections should not be forced into the top bar.

Examples:

- player page sections
- team page sections
- gauntlet qualifier/finals/standings sections
- course leaderboard filters
- calendar/past-event links from gauntlets

### 4. Permissioned actions live near their object

Permissioned actions should appear on the page where the action makes sense, not as always-visible global nav items.

Examples:

- `Create Gauntlet` appears on `/gauntlets` for gauntlet creators/admins.
- `Edit Gauntlet` appears on `/gauntlets/[id]` for the gauntlet creator or admins.
- `Create Team` appears on `/teams` or related team-entry surfaces for eligible logged-in users.
- `Manage Team` appears on `/teams/[id]` for team managers/owners/admins.
- Sponsor admin actions appear on sponsor pages only for admins.

### 5. Search is a core primitive

Search-everywhere should be reachable from the top bar and should group results by entity type.

Priority entity groups:

- gauntlets
- players
- teams
- courses
- sponsors
- planets
- ship parts

## Top-Bar Nav Contexts

## Marketing Context

Used on:

- `/game`
- `/features`
- `/media`
- `/press`
- future `/about`
- future `/events`
- future `/brand`
- future `/lore`
- future `/faq`

Likely top-bar links:

- Game
- Features
- Media
- About
- Events
- Brand
- Player Side / Competition bridge link
- Press
- Wishlist / Play CTA
- Search
- Login / avatar

Notes:

- Marketing context must provide an escape hatch into competition content.
- The root route `/` is adaptive and currently leans toward the player/competition command-center behavior defined in [[pages/homepage]], while still retaining a marketing bridge.
- The bridge link can land on `/gauntlets`, `/players`, or a dedicated player-side landing view depending on final IA.
- Marketing nav should not retain obsolete tournament-specific links such as the old Cardano Clash entry if they no longer represent current product direction.

## Competition Context

Used on:

- `/gauntlets`
- `/gauntlets/[id]`
- `/players`
- `/players/[id]`
- `/teams`
- `/teams/[id]`
- `/sponsors`
- `/courses`

Likely top-bar links:

- Gauntlets
- Players
- Teams
- Courses
- Sponsors
- Marketing / Game bridge link
- Search
- Login / avatar

Notes:

- Competition context should bias toward entity discovery and fast re-entry.
- Marketing content remains reachable through the bridge link but should not dominate.

## Logged-In Player Context

Logged-in state layers account controls into the current context.

Flow spec:

- [[flows/authentication]]
- [[flows/wallet-linking]]
- [[flows/team-lifecycle]]

Likely avatar/account menu:

- My Career
- Wallets
- My Team or Team Requests
- Log out

Optional contextual indicators:

- active gauntlet status
- qualification status
- team invite/request count
- wallet verification warning

## Admin / Operations Context

Admin and creator actions should generally be in-page actions, not full-time global nav links.

Admin-only shortcuts may appear in an avatar/admin menu if needed:

- Sponsor Admin
- Gauntlet Admin
- Operations

Guardrail:

- Do not let admin tooling dominate the public shell.

## Route Inventory

## Phase 1 Must-Have Public Routes

| Route | Purpose | Primary Context |
|---|---|---|
| `/` | adaptive homepage and competition command center | competition / marketing bridge |
| `/game` | game overview and marketing explanation | marketing |
| `/gauntlets` | gauntlet/event discovery | competition |
| `/gauntlets/[id]` | gauntlet detail | competition |
| `/players` | player directory | competition |
| `/players/[id]` | player profile/career | competition |
| `/teams` | team directory | competition |
| `/teams/[id]` | team profile | competition |
| `/sponsors` | sponsor/partner listing | competition / marketing |

## Phase 1 Preserved Authenticated/Admin Routes

Exact route naming can change during implementation, but the capability must remain.

Authentication flow:

- [[flows/authentication]]
- [[flows/wallet-linking]]

| Capability | Purpose |
|---|---|
| login | Steam authentication |
| wallets | wallet linking and verification; see [[flows/wallet-linking]] |
| team create | create team when eligible |
| team manage | manage roster, invites, requests, media, roles |
| gauntlet create | create gauntlet when authorized |
| gauntlet edit | edit gauntlet when authorized |
| gauntlet prize | funding, result, claim flows preserved from current app |
| sponsor admin | create/edit sponsors for admins |

## Phase 1 Nice-to-Have Public Routes

| Route | Purpose |
|---|---|
| `/features` | marketing feature breakdown |
| `/media` | media, video, screenshots |
| `/courses` | course index and leaderboard entry point |
| `/press` | press/partner information |
| `/about` | company/team/ethos content migrated from current public site |
| `/events` | manually maintained showcase of LAN, venue, and historical tournament events |
| `/brand` | updated brand guidelines aligned to the new game and website design |

## Later Routes

| Route | Purpose |
|---|---|
| `/watch` | VODs first, live streams later |
| `/lore` | high-level lore/editorial |
| `/faq` | support/common questions |
| `/calendar` or `/gauntlets/calendar` | full gauntlet/event calendar |

## Existing Marketing Site Migration Notes

Current public-site content should be audited and migrated selectively.

Known existing content categories:

- About Us
- company/team/ethos content
- manually maintained tournament/event history
- event pages that link to YouTube content when competitions or physical events were recorded
- brand guideline page
- old tournament-specific links such as Cardano Clash

Migration guidance:

- Preserve company/team/ethos content if still accurate, likely under `/about`.
- Preserve historical event/tournament content, but consider renaming it to `Events` or `Showcase Events` rather than treating every historical item as a gauntlet.
- Historical physical/LAN/venue events are not necessarily gauntlets and should not be forced into the gauntlet data model.
- Preserve YouTube links associated with historical events where recordings exist.
- Remove or de-emphasize obsolete one-off links such as Cardano Clash unless they are intentionally kept as historical event content.
- Refresh the brand guideline page after the new game/site visual direction is settled.

Terminology guidance:

- `Gauntlets` are Eventun-backed competition structures.
- `Events` can include manually maintained LANs, physical venue appearances, historical tournaments, showcases, and recorded competitions.
- A historical event can link to a gauntlet if one exists, but it does not have to be a gauntlet.

## Page-Local Navigation Patterns

## Homepage

Page spec:

- [[pages/homepage]]

Homepage role:

- adaptive competition/player command center
- lightweight brand hero and marketing bridge
- not a replacement for the dedicated `/game` marketing overview

V1 modules:

- hero / command briefing
- search everywhere
- current and upcoming gauntlets
- high-level status strip
- course record highlights
- pilot highlights
- generated system log from real snapshot data
- optional sponsor strip

Logged-in utility overlays:

- gauntlets with the user's rank or participation status, where available
- course leaderboard placement, where available
- career, wallet, and team links through the always-visible avatar menu

## Gauntlets Index

Page spec:

- [[pages/gauntlets-index]]

Page-local sections:

- current gauntlets
- upcoming gauntlets
- featured events, if available
- past gauntlets link
- full calendar link

Permissioned actions:

- `Create Gauntlet` for gauntlet creators/admins

## Gauntlet Detail

Page spec:

- [[pages/gauntlet-detail]]

Page-local sections:

- overview / briefing
- qualifiers
- finals or brackets
- standings
- prizes
- sponsors
- schedule
- history / past winners, later

Personalized logged-in overlays:

- current rank
- qualification status
- eligible finals/stage status

Permissioned actions:

- `Edit Gauntlet` for creator/admin
- prize/admin actions for authorized users

Terminology guardrail:

- qualifiers are gauntlet/tournament windows
- heats are match-internal runtime rounds
- do not use these terms interchangeably

## Players

Page specs:

- [[pages/player-directory]]
- [[pages/player-profile]]

Page-local sections:

- Overview
- Course Stats
- Match History
- Gauntlet Results
- Trophies and Medals
- Rank History

Personalized own-profile overlays:

- private or more detailed rank context where appropriate
- wallet/team/account action links

Public privacy guardrail:

- public rank tier is allowed
- exact ELO remains private

## Course Leaderboards

Page spec:

- [[pages/course-leaderboards]]

Page-local sections:

- course selector
- selected course briefing
- category filter
- leaderboard table
- logged-in personal placement strip
- cross-course overview
- related context, later

Personalized logged-in overlays:

- current user's placement for the selected course/category where available

Public privacy guardrail:

- public leaderboard time/rank is allowed
- exact ELO remains private and unrelated to course leaderboard display

## Teams

Flow spec:

- [[flows/team-lifecycle]]

Page specs:

- [[pages/teams-index]]
- [[pages/team-profile]]

Page-local sections:

- Overview
- Roster
- Gauntlet Results
- Team Stats
- Trophies and Medals
- Manage, if authorized

Permissioned actions:

- request to join
- leave team
- manage invites/requests
- edit team media
- promote/demote/kick

Management guardrail:

- team management should remain attached to the team context
- management may be a page-local section or `/teams/[id]/manage` sub-route, but it should not feel like a disconnected admin product

## Sponsors

Page spec:

- [[pages/sponsors-index]]

Page-local sections:

- sponsor list
- featured sponsors
- sponsor detail links
- sponsor social/website links
- gauntlet relationship context where available

Permissioned actions:

- create/edit/delete sponsor for admins
- update sponsor media, colors, description, and social links

## Page State Matrix

This is the initial phase-1 state matrix. It should be expanded during page-spec work.

| Route | Anonymous View | Logged-In View | Authorized/Admin View |
|---|---|---|---|
| `/` | adaptive competition homepage with brand hero, search, active/upcoming gauntlets, course records, pilot highlights, system log, and marketing bridge | same plus personalized gauntlet/team/wallet context where available | same as logged-in plus minimal creator/admin alerts or create actions only if necessary |
| `/game` | public game overview | same, with account/avatar state in nav | same |
| `/gauntlets` | current/upcoming gauntlets, past link, calendar link | same plus personalized participation context when available | `Create Gauntlet` for creator/admin |
| `/gauntlets/[id]` | briefing, qualifiers, finals/brackets, standings, sponsors, prizes | same plus personal rank/qualification/eligibility context | `Edit Gauntlet`, prize/admin actions when authorized |
| `/players` | player directory and search/filter | same | same, possible admin-only moderation/actions later |
| `/players/[id]` | public profile, course stats, course placements, match-history overview, gauntlet results, trophies, rank tier | own profile may show wallet/team actions and own AccelByte medals/badges if available | admin-only actions later if needed |
| `/courses` | course selector, course metadata, selected leaderboard, player profile links | same plus personal placement strip when available | no V1 admin actions unless course administration is added later |
| `/teams` | team directory, search/filter, membership-mode context | same plus create team when eligible and `My Team` context if useful | admin may see broader moderation affordances later |
| `/teams/[id]` | public team briefing, roster, membership mode, token gate notice where public | join/request/leave actions based on membership and current team state | manage roster, invites, requests, media, colors, membership mode, token gates, ownership/disband for owner/manager/admin |
| `/sponsors` | sponsor/partner listing, search/sort, public sponsor links, optional detail | same | create/edit/delete sponsor and manage media/colors/social links for admins |
| login | Steam login entry | redirect or show already logged-in state | same |
| wallets | login required | wallet linking and verified wallet state | same |
| team management | login required | only visible if authorized by team role | admin override if supported |
| gauntlet management | login required | only visible to creator role where applicable | admin override |
| sponsor administration | login required | hidden unless admin | full sponsor CRUD |

## Search Architecture

Search should group results by entity type.

Initial groups:

- Gauntlets
- Players
- Teams
- Sponsors
- Courses

Future groups:

- Planets
- Ship parts
- Manufacturers
- News/media

General lore should not be the first search priority. Lore should mostly be reached through editorial pages or entity relationships.

## Open Questions

- What should the cross-site bridge labels be on each side?
  - player side to marketing side
  - marketing side to player/competition side
- Should the marketing-to-player bridge land on `/gauntlets`, `/players`, or a dedicated competition landing view?
- Should `/calendar` be a standalone route or nested under `/gauntlets/calendar`?
- Should top-bar nav changes be route-driven, user-state-driven, or both?
- Should logged-in utility modules replace anonymous homepage modules or reorder them?
- Should contextual page-local nav be tabs, anchor links, panel headers, or command-like section links?
- What is the exact avatar/account menu structure?
- Which pages need admin-only action affordances in phase 1 versus later?
- Should historical events live under `/events`, `/media`, or a combined `Events / Media` section?
- What brand guideline content can be migrated as-is versus rewritten after the new design direction lands?

## Next Steps

- Use page specs to drive the next Pencil pass.
- Create user-flow specs for authenticated and admin workflows.
