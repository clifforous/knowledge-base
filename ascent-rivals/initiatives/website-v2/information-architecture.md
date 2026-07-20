# Ascent Rivals Website Information Architecture

Date: 2026-04-13
Status: Draft

Foundation supersession (2026-07-13): references to `token_gated` teams, team token-gate notices, or token-gate management are historical and must not be implemented from this draft. Eventun removed the TapTools-shaped token catalog, gate relations, and APIs; existing gated teams transition to invite-only until a provider-neutral asset-source contract is separately designed.

## Related
- [[unified-design]]
- [[initial-release-scope]]
- [[README|Website V2 initiative index]]
- [[shell-concepts]]
- [[terminal-ops-design-system]]
- [[tone-and-voice]]
- [[flows/authentication]]
- [[flows/gauntlet-authoring]]
- [[flows/team-lifecycle]]
- [[ascent-rivals/initiatives/website-v2/pages/homepage]]
- [[ascent-rivals/initiatives/website-v2/pages/player-directory]]
- [[ascent-rivals/initiatives/website-v2/pages/player-profile]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlets-index]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlet-detail]]
- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]
- [[ascent-rivals/initiatives/website-v2/pages/teams-index]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]
- [[sponsor-administration-handoff]]
- [[ascent-rivals/archive/initiatives/website-v2/pencil-design-brief]]
- [[ascent-rivals/system/competition-runtime-terms|competition-runtime-terms]]

## Purpose

This note defines the route, navigation, and page-state model for the unified Ascent Rivals website.

It is the first decomposition of the broader [[unified-design]] document.

## Working Navigation Decision

Use one top-bar-based global navigation system across the new Next.js/React site.

The stable semantic order is:

1. Ascent Rivals brand linking to `/`;
2. `Gauntlets`;
3. `Pilots`, linking to `/players`;
4. `Teams`;
5. `Courses`;
6. `Events`;
7. global search;
8. Steam login or the authenticated account menu.

The active state, density, and surrounding shell treatment may adapt to marketing or data-heavy pages, but route names and ordering must not change by context. `About` and `Brand` are secondary destinations available through `More` and the footer. Sponsor administration belongs to the Eventun Extend App and has no Website V2 route.

Page-local subnavigation should live inside pages instead of relying on a persistent global side navigation.

## Cross-Site Continuity Rule

The shared navigation itself provides the cross-site bridge:

- the brand always returns to the marketing homepage;
- `Gauntlets` always enters the competition experience;
- the remaining core entity destinations stay in the same order throughout the site.

Do not add a separate `Marketing`, `Player Side`, `Portal`, or `Competition` link. When links collapse into a mobile drawer, `Gauntlets` is the first destination after the homepage/brand entry.

Purpose:

- new visitors can move from brand/game context into player and tournament context
- returning players can quickly return from marketing/editorial pages to gauntlets, players, teams, and stats
- the unified site does not feel like two disconnected products

## Navigation Principles

### 1. Global nav is for major destinations

The top bar should expose major site areas, not every action.

The initial major destinations are `Gauntlets`, `Pilots`, `Teams`, `Courses`, and `Events`. Search and login/account are persistent utilities rather than destination links.

### 2. Width changes disclosure, not semantics

Do not force all destinations into an undersized row. Preserve labels and touch targets, and move links into `More` or the mobile drawer before the bar wraps or becomes crowded.

Persistent at every width:

- brand/home access;
- search;
- login/account;
- a menu trigger whenever any destination is hidden.

Destination-retention priority, highest to lowest:

- Gauntlets
- Pilots
- Teams
- Courses
- Events

Use measured available width rather than relying on one fixed breakpoint. Wide desktop may show every destination. Compact desktop and tablet progressively move `Events`, then lower-priority links from the right side of the list, into `More`. Mobile uses a complete drawer.

Context may still affect presentation outside the destination list:

- marketing pages may use a more cinematic shell and place the primary Steam conversion action in page content;
- competition pages use a calmer data-forward shell;
- logged-in and admin state changes the account menu, not the public destination order.

### 3. Page-local navigation handles depth

Detailed page sections should not be forced into the top bar.

Examples:

- player page sections
- team page sections
- gauntlet qualifier/finals/standings sections
- course leaderboard filters
- Schedule view and Past scope controls from gauntlets

Page-local navigation contract:

- use readable in-page section anchors as the default for long entity pages and sectioned forms;
- use tabs only when panels are mutually exclusive views of the same region rather than sections of one document;
- use segmented controls for a small set of short module-level filters, such as leaderboard category groups;
- preserve meaningful tab or filter state in the URL when sharing or browser history should reproduce the selected view;
- command-like prefixes or system labels may provide visual character, but the accessible name and primary visible label must remain ordinary product language;
- on compact layouts, replace a long section row with a labeled jump menu or disclosure instead of requiring hidden horizontal scrolling;
- render navigation only for sections that structurally exist; do not create empty qualifier, stage, bracket, sponsor, or other optional destinations;
- distinguish a structurally absent section from an ordinary no-data state inside a supported section.

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
- planets
- ship parts

A later permission-filtered administrative group may add sponsors for administrators through a separate authenticated response. Sponsor results are not part of public search or general creator search.

## Responsive Top-Bar Behavior

Wide desktop:

- show the brand, all five destinations, compact search, and login/account when they fit without compression;
- keep the bar on one line and preserve readable spacing.

Compact desktop and tablet:

- retain brand, search, login/account, and `More`;
- keep destination links visible in priority order only while measured space permits;
- place hidden destinations in `More` in their normal semantic order.

Mobile:

- show brand, search, menu, and login/account as compact direct controls;
- put the complete destination list in the drawer, starting with `Gauntlets`;
- include `About` and `Brand` after the primary destinations;
- retain ordinary touch navigation and do not simulate a miniature command line.

The top bar must never wrap, horizontally scroll, abbreviate labels into unclear terms, or reduce touch targets merely to retain another visible link.

Anonymous authentication uses one direct `Sign in with Steam` control, not a provider picker. Compact layouts may present the Steam icon with `Sign In`, but the accessible name remains `Sign in with Steam` and activation starts the Steam flow immediately. Epic, Discord, or other providers remain future product/identity decisions rather than initial navigation placeholders.

## Logged-In Player Context

Logged-in state layers account controls into the current context.

Flow spec:

- [[flows/authentication]]
- [[flows/team-lifecycle]]

Approved initial avatar/account menu:

- My Career
- My Team
- Admin / Operations, only when authorized and a destination exists
- Sign Out

Account-menu behavior:

- `My Career` links to the authenticated pilot's canonical profile;
- `My Team` links to the current team, or to `/teams` when the player has no team;
- pending team invitations and join requests appear as one concise count/status on `My Team`, not as separate menu entries;
- creation, editing, and management actions remain on their relevant entity pages;
- authorization is checked before showing `Admin / Operations` and again at the destination;
- `Sign Out` remains visually separated and easy to find.

## Admin / Operations Context

Admin and creator actions should generally be in-page actions, not full-time global nav links.

`Admin / Operations` may expose authorized destinations such as:

- Sponsor Admin
- Gauntlet Admin
- Operations

Guardrail:

- Do not let admin tooling dominate the public shell.

## Route Inventory

## Phase 1 Must-Have Public Routes

| Route | Purpose | Primary Context |
|---|---|---|
| `/` | primary game-marketing and conversion homepage | marketing |
| `/gauntlets` | Eventun-backed unique-gauntlet discovery, Past scope, and repeated-occurrence Schedule agenda | competition |
| `/gauntlets/[id]` | gauntlet detail | competition |
| `/events` | code-authored editorial event listing | marketing |
| `/events/[slug]` | code-authored event detail | marketing |
| `/about` | studio story, mission, current team, and verified recognition | marketing |
| `/brand` | verified downloadable brand assets and current usage guidance | marketing |
| `/players` | player directory | competition |
| `/players/[id]` | player profile/career | competition |
| `/teams` | team directory | competition |
| `/teams/[id]` | team profile | competition |
| `/courses` | course directory, category leaderboards, and pilot placement | competition |
| `/courses/[code]` | shareable course briefing, selected category leaderboard, records, and pilot placement | competition |

## Phase 1 Preserved Authenticated Routes

Exact route naming can change during implementation, but the capability must remain.

Authentication flow:

- [[flows/authentication]]

| Capability | Purpose |
|---|---|
| login | Steam authentication |
| team create | create team when eligible |
| team manage | manage roster, invites, requests, media, roles |
| gauntlet create | create gauntlet when authorized |
| gauntlet edit | edit gauntlet when authorized |

Accountun-related prize and reward data is entirely deferred. Website V2 does not expose or administer data-driven prize pools, funding, claims, payouts, wallet requirements, or legacy workflows. Verified prize copy may still appear as manually maintained promotional content on a related `/events/[slug]` page.

Gauntlet create/edit uses the one-page sectioned flow in [[flows/gauntlet-authoring]]. It has Core Details, Competition Structure, Branding and Advertising, and Review and Save sections; it is not a wizard and does not imply a persisted draft. Successful create and edit both return to a freshly revalidated `/gauntlets/[id]` detail view for manual review.

## Phase 1 Nice-to-Have Public Routes

| Route | Purpose |
|---|---|
| `/features` | marketing feature breakdown |
| `/media` | media, video, screenshots |
| `/press` | press/partner information |

## Later Routes

| Route | Purpose |
|---|---|
| `/game` | conditional deeper game-systems overview once enough distinct content exists |
| `/watch` | VODs first, live streams later |
| `/lore` | high-level lore/editorial |
| `/faq` | support/common questions |
| `/calendar` or `/gauntlets/calendar` | conditional full calendar only if it later provides value beyond `/gauntlets?view=schedule` |

## Existing Marketing Site Migration Notes

Current public-site content should be audited and migrated selectively.

Known existing content categories:

- `/`: hero and Steam conversion, partner proof, game features, gameplay video, ship customization, gallery, and community links
- `/about`: mission, team, awards and appearances, and development/event vlogs
- `/brand`: downloadable brand kit plus logo, spacing, dimensions, color, and typography guidance
- `/tournaments`: one current featured tournament plus a code-authored historical tournament gallery with dates, winners, prizes, sponsors, and YouTube links
- `/tournaments/msi-grand-prix-2026`: a detailed, code-authored event page with schedule, qualifier format, physical prizes, FAQ, system requirements, controls, and participation guidance

Migration guidance:

- Preserve the current homepage's hero/Steam conversion, gameplay features, video, ship customization, gallery, partners, and community as content categories rather than as reusable implementation.
- Rewrite or verify the homepage copy, gameplay claims, partner approvals, screenshots, video, and conversion wording before migration.
- Rebuild the homepage layout and components for the revised Terminal Ops sci-fi direction; current backgrounds, clipping treatments, styling, and React components are references only.
- Add a restrained competition teaser or bridge to `/gauntlets` without turning the homepage into a dashboard.
- Keep `/about` as one concise page containing the studio story, mission, current team, and a small set of verified recognition.
- Move LAN, venue, tournament, and showcase appearances from the current About page to `/events`.
- Place event-specific videos on the related `/events/[slug]` page when useful; otherwise link to the maintained YouTube playlist instead of recreating a large vlog archive on `/about`.
- Verify team membership, roles, mission copy, and recognition claims before migration.
- Migrate the current marketing `/tournaments` area to `/events` rather than treating every item as a gauntlet.
- Historical physical/LAN/venue events are not necessarily gauntlets and should not be forced into the gauntlet data model.
- Preserve YouTube links associated with historical events where recordings exist.
- Allow verified prize descriptions as static promotional event copy; never derive them from Accountun or imply live funding, eligibility, claim, or payout state.
- Remove or de-emphasize obsolete one-off links such as Cardano Clash unless they are intentionally kept as historical event content.
- Retain `/brand` as a public route for partners, press, tournament organizers, and creators.
- Preserve verified logo downloads and essential logo-usage rules, but revalidate spacing and minimum-size guidance.
- Replace color, typography, and website-usage examples only after the revised Terminal Ops visual direction is approved.
- Keep downloadable brand assets in the repository and update them through the code-authored workflow; do not introduce a CMS or asset-management service for the initial release.
- A future `/press` page may link to `/brand`, but should not replace or absorb it initially.

Content disposition summary:

- Preserve after verification: homepage content categories, studio story and mission, current team, verified recognition, logo downloads and essential usage rules, historical event facts, approved event media, and useful recording links.
- Rewrite or refresh: homepage copy and media, brand-system guidance, About copy, event descriptions, metadata, and any time-sensitive instructions.
- Move: event appearances and recaps from `/about` to `/events`; event-specific videos to their event detail when useful.
- Retire: current `/tournaments` URLs after their content moves to the canonical `/events` routes; no legacy redirect layer is required initially.
- Retire: the current homepage implementation and layout, unverified claims or partner marks, obsolete one-off navigation links, duplicate `/game` content, and a standalone vlog archive on `/about`.

Terminology guidance:

- `Gauntlets` are Eventun-backed competition structures.
- `Events` can include manually maintained LANs, physical venue appearances, historical tournaments, showcases, and recorded competitions.
- A historical event can link to a gauntlet if one exists, but it does not have to be a gauntlet.

Canonical URL and legacy-route decision:

- `/`, `/about`, `/brand`, `/events`, and `/events/[slug]` are canonical marketing routes for the initial Website V2 release.
- `/events` is the canonical editorial event index.
- `/events/[slug]` is the canonical route for manually authored event details.
- `/gauntlets` and `/gauntlets/[id]` remain reserved for Eventun-backed competition data.
- Retire `/tournaments` and `/tournaments/msi-grand-prix-2026` at Website V2 cutover rather than adding redirects for the current negligible external traffic.
- Do not include legacy prize, reward, funding, claim, payout, or wallet links on Website V2 event pages.
- Each marketing route must define a unique title, description, canonical URL, social image, and social-image alt text alongside its route content.
- Historical event pages retain stable slugs when practical; changed slugs update repository content and internal links, with an exact redirect added later only if measured inbound use justifies it.

## Code-Authored Content Convention

Website V2 does not require a CMS, MDX pipeline, or separate content framework for the initial release.

Authoring rules:

- Keep short, layout-specific copy beside its TSX component.
- Put long or structured route content in a typed `content.ts` file beside the route.
- Introduce a shared type or rendering template only when multiple pages repeat a stable structure.
- Use one route-local content file per editorial event, with bespoke TSX sections allowed when an approved event design needs them.
- Keep route title, description, canonical URL, and social-image metadata with the corresponding route content.
- Store static assets under predictable route- or slug-based repository paths.
- Do not create a global copy registry or abstract isolated text merely to make it data-driven.

Update workflow:

1. the designer supplies an approved mock, final copy, and required assets;
2. the developer or coding agent updates the relevant TSX and typed content modules;
3. the change receives code review and manual browser review at the required responsive sizes;
4. code and content ship in the same deployment.

## Page-Local Navigation Patterns

## Homepage

Page spec:

- [[ascent-rivals/initiatives/website-v2/pages/homepage]]

Homepage role:

- primary game-marketing and conversion landing page
- clear bridge into competition through `/gauntlets`
- selected current competition, recent event, partner, or community proof only where it strengthens the marketing story
- light logged-in personalization without a separate homepage layout

Working V1 content categories:

- game proposition and primary Steam conversion action
- gameplay footage and differentiating features
- ship customization or other game-system proof
- gallery or media proof
- partners and community
- compact competition bridge or teaser where useful

Possible logged-in additions:

- current or upcoming gauntlet participation context
- career and team links through the account menu
- compact personal result or course-placement context

## Gauntlets Index

Page spec:

- [[ascent-rivals/initiatives/website-v2/pages/gauntlets-index]]

Visibility contract:

- every successfully created Eventun gauntlet is public in the initial release;
- `Current & Upcoming` and `Past` are discovery scopes, not publication states;
- Past gauntlets retain public detail routes and remain available to search;
- future draft, embargo, cancellation, or suppression behavior requires an explicit lifecycle contract and is not inferred from timing.

Page-local sections:

- `Gauntlets` and `Schedule` view control
- unique `Current & Upcoming` gauntlet list, sorted by active or nearest future occurrence
- URL-backed `Past` entity scope
- repeated-occurrence chronological Schedule agenda

Permissioned actions:

- `Create Gauntlet` for gauntlet creators/admins

## Gauntlet Detail

Page spec:

- [[ascent-rivals/initiatives/website-v2/pages/gauntlet-detail]]

Page-local sections:

- overview / briefing
- qualifiers when present
- stages, finals, or a published bracket when present
- standings and results supported by the actual gauntlet composition
- approved sponsor identity when an explicit relationship exists; direct billboard artwork alone does not create this section
- schedule
- history / past winners, later

Composition guardrail:

- qualifiers and stages are independent optional parts of a gauntlet;
- never render an empty qualifier, stage, final, or bracket section merely to preserve a universal template;
- prioritize the next or active component that actually exists, then show the authoritative completed result for the structure that ran;
- keep section labels and local navigation stable where possible without implying a missing phase.

Terminology guardrail:

- use `Qualifier` only for qualification windows;
- use `Stage` for a general scheduled non-bracket competition unit;
- use `Final` only when the competition explicitly marks a stage as the deciding final;
- use `Bracket` only when a published bracket graph exists, not merely because stages have win/loss prerequisites.

Personalized logged-in overlays:

- current rank
- qualification status
- eligible finals/stage status

Permissioned actions:

- `Edit Gauntlet` for creator/admin
- non-blockchain gauntlet edit/delete actions for authorized users

Terminology guardrail:

- qualifiers are gauntlet/tournament windows
- heats are match-internal runtime rounds
- do not use these terms interchangeably

## Players

Page specs:

- [[ascent-rivals/initiatives/website-v2/pages/player-directory]]
- [[ascent-rivals/initiatives/website-v2/pages/player-profile]]

Directory contract:

- include every real pilot with a usable public identity, including new or inactive pilots;
- exclude bots, test accounts, or internal identities only through explicit source-system classification;
- default to alphabetical order with client-side name/team search, sorting, filtering, and progressive display over one compact collection response;
- keep full profiles and histories out of the directory collection;
- show `[TAG] Team Name` when space permits, tag-only identity on compact cards, and `Independent` for unaffiliated pilots;
- keep the pilot avatar as the ordinary directory card's only image and use neutral team-tag styling with at most a restrained accessible team-color accent;
- reconsider server pagination only after measured query, transfer, parsing, memory, or interaction cost becomes material.

Page-local sections:

- Overview
- Course Stats
- Recent Races
- Gauntlets, containing the `Gauntlet History` section
- Achievements & Medals

`Gauntlet History` includes active public participation before completed history, then sorts by the pilot's latest real activity. It adapts each entry to qualifier, accepted stage, or general participation facts; it does not expose invitations or other private participation state and does not label qualifier rank as a tournament finish.

`Achievements & Medals` shows completed public Eventun achievements/masteries and known gameplay-medal totals. It does not expose active or incomplete progress, challenges, raw progression counters, reward data, or inferred trophies. A later self-only progression destination requires a separate approval.

Personalized own-profile overlays:

- private or more detailed rank context where appropriate
- team/account action links

Public privacy guardrail:

- the initial profile has no generic global rank tier or rank history;
- exact AccelByte MMR is omitted, including on the current player's profile;
- exact course leaderboard positions and gauntlet standings remain public in their scoped contexts;
- any future named division is Eventun-owned and requires a separate stateful rank-system design rather than a Website mapping.
- Recent Races contains only published/archived-course multiplayer results and does not expose hidden course codes, client versions, replay keys, or raw match/session identifiers.
- Time trials, Career Cup, and other single-player activity are not presented as recent-race history; retained best lap and best finish records remain on course/career surfaces.

## Course Leaderboards

Page spec:

- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]

Page-local sections:

- production-ready course directory and selector
- explicit archived-course filter
- selected course briefing
- category filter
- leaderboard table
- logged-in personal placement strip
- cross-course overview
- related context, later

Route behavior:

- `/courses` is the discovery and cross-course overview;
- `/courses/[code]` is the canonical detail route;
- the leaderboard category remains explicit shareable query state on the detail route.

Course visibility guardrails:

- AccelByte Cloud Save `Courses` is authoritative for course configuration and feature state;
- the server classifies a production-ready course as `published` when its AccelByte feature state matches the configured enabled state and it is not marked archived;
- the public directory shows `published` courses by default;
- a course is `archived` only through an explicit AccelByte metadata marker asserting that it was previously public and deliberately retired;
- alpha, internal, and otherwise unreleased courses remain absent from public routes, search, metadata, and sitemaps;
- unknown, incomplete, or conflicting metadata fails closed to hidden;
- Website-facing APIs expose only `published` and `archived`; hidden/unreleased detail requests behave as not found;
- do not infer archive eligibility from Eventun's derived `active` boolean alone.

Personalized logged-in overlays:

- current user's placement for the selected course/category where available

Public privacy guardrail:

- public leaderboard time/rank is allowed
- internal AccelByte MMR is absent from and unrelated to course leaderboard display

## Teams

Flow spec:

- [[flows/team-lifecycle]]

Page specs:

- [[ascent-rivals/initiatives/website-v2/pages/teams-index]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]

Page-local sections:

- Overview
- public membership mode: `Open`, `Request to Join`, or `Invite Only`
- Roster
- Individual Pilot Results
- Team Stats, secondary and provisional until post-implementation review
- Gauntlet Results when team-result semantics exist
- Trophies and Medals
- Manage, if authorized

Permissioned actions:

- request to join
- leave team
- manage invites/requests
- edit team media
- promote/demote/kick

Membership-mode guardrail:

- show the same public membership label to anonymous and logged-in visitors;
- authentication, current-team state, and invitations determine which action appears, not whether the team mode is disclosed;
- treat the three public concepts as stable while mapping them to the reviewed backend enum after the new team implementation.

Team-statistics guardrail:

- team history and aggregate performance require Eventun fact-backed event-time membership attribution;
- do not sum current roster pilot careers to approximate historical team results;
- Website V2 follows the team feature work and may assume that data is available by launch;
- finalize the exact team page modules only after reviewing the implemented contracts described in [[initial-release-scope]].
- keep pilots, pilot profiles, and the roster more prominent than aggregate team claims until the team feature has been implemented and iterated on;
- distinguish pilot results earned while representing a team from competition-defined team standings or wins.

Management guardrail:

- `/teams/[id]` owns the public profile and ordinary join/request/leave actions;
- `/teams/[id]/manage` owns metadata, media, roster administration, invitations, join requests, ownership transfer, and disbanding;
- a permission-aware `Manage Team` action links from the public profile;
- the management route retains team identity and a clear return path so it does not feel like a disconnected admin product.

## Sponsors

Sponsor administration handoff:

- [[sponsor-administration-handoff]]

Website V2 has no sponsor registry, detail, create, edit, delete, or sponsor-media administration pages. Those workflows move to the Eventun Extend App before cutover.

Gauntlet-authoring boundary:

- direct gauntlet-owned `Billboard` uploads are the primary advertising workflow, with an explicit `Tileable` metadata control and a lightweight three-copy preview for ribbon-style placements;
- creators do not need general sponsor-registry access;
- retain an optional existing-sponsor picker scoped to the gauntlet form for the less common reusable-entity case;
- direct billboard artwork does not imply a public sponsor identity or Website sponsor module.

Other configured media purposes receive generic labeled upload and thumbnail handling at launch. Their names are compatibility labels rather than commitments to purpose-specific Website modules. Dimension-derived slot matching and other billboard-system improvements are deferred with the broader advertising redesign.

Terminology boundary:

- `Sponsor` remains the Eventun-backed competition entity, but its registry and administration exist only in the Eventun Extend App;
- public gauntlet pages may show an approved sponsor name or mark in that gauntlet's context but do not link to the registry or expose relationship tier;
- code-authored marketing content may use `Partner` for a broader verified relationship that does not imply gauntlet sponsorship;
- do not introduce `/partners` until there is enough distinct content and ownership to justify a separate route.

Permissioned actions:

- upload gauntlet-owned billboard media for gauntlet creators
- optionally select an existing sponsor through a form-scoped advanced control without granting registry access

## Page State Matrix

This is the initial phase-1 state matrix. It should be expanded during page-spec work.

| Route | Anonymous View | Logged-In View | Authorized/Admin View |
|---|---|---|---|
| `/` | marketing homepage with game proposition, conversion CTA, feature/media proof, and competition bridge | same, with optional compact gauntlet, career, team, or result context | same as logged-in; no global admin controls |
| `/gauntlets` | unique current/upcoming gauntlets, Past scope, and repeated-occurrence Schedule agenda | same layout plus personalized participation context when available | `Create Gauntlet` for creator/admin |
| `/gauntlets/[id]` | briefing, qualifiers, finals/brackets, standings, sponsors, and factual public result context; no Accountun-driven prize/reward data | same plus personal rank/qualification/eligibility context | ordinary non-prize edit/delete actions; administrator-only bracket and runtime-repair tooling remains in the Eventun Extend App UI |
| `/players` | player directory and search/filter | same | same, possible admin-only moderation/actions later |
| `/players/[id]` | public profile, course stats, course placements, Recent Races, structure-aware Gauntlet History, completed public achievements/masteries, and known gameplay-medal totals; no generic rank tier/history | own profile may show team/account actions; exact MMR and active progression remain omitted | admin-only actions later if needed |
| `/courses` | production-ready course selector, explicit archived filter, course metadata, selected leaderboard, player profile links | same plus personal placement strip when available | no V1 admin actions unless course administration is added later |
| `/courses/[code]` | public or explicitly archived course briefing, selected category records and leaderboard, pilot links; unreleased courses are not exposed | same plus personal placement when available | no initial admin actions unless course administration is later approved |
| `/teams` | team directory, search/filter, membership-mode context | same plus create team when eligible and `My Team` context if useful | admin may see broader moderation affordances later |
| `/teams/[id]` | public team briefing, roster, membership mode, and fact-backed team analytics when available | join/request/leave actions based on membership and current team state | manage roster, invites, requests, media, colors, membership mode, ownership/disband for owner/manager/admin |
| `/teams/[id]/manage` | not publicly navigable | unavailable unless authorized for the selected team | metadata, media, roster roles, invitations, join requests, ownership transfer, and disbanding |
| login | Steam login entry | redirect or show already logged-in state | same |
| team management | login required | only visible if authorized by team role | admin override if supported |
| gauntlet management | login required | only visible to creator role where applicable | admin override |

## Search Architecture

Search should group results by entity type.

Initial delivery uses the persistent top-bar `SearchCommand` as an accessible dialog or mobile sheet rather than adding a separate `/search` destination. The catalog is lazy-loaded on first search interaction, searched locally, and cached in browser query state with bounded staleness and mutation invalidation. Each group can route to its normal directory with `q` preserved for the complete local result set.

Initial groups:

- Gauntlets
- Players
- Teams
- Courses

Sponsor discovery and administration remain in the Eventun Extend App and do not become a Website global-search group. Public search responses and general creator search never include sponsor registry records. A gauntlet form may provide a narrower authorized relationship picker.

Future groups:

- Planets
- Ship parts
- Manufacturers
- News/media

General lore should not be the first search priority. Lore should mostly be reached through editorial pages or entity relationships.

## Open Questions

- Which pages need admin-only action affordances in phase 1 versus later?
- What brand guideline content can be migrated as-is versus rewritten after the new design direction lands?

## Next Steps

- Use page specs to drive the next Pencil pass.
- Create user-flow specs for authenticated and admin workflows.
