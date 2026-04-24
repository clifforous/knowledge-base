# Ascent Rivals Homepage Page Spec

Date: 2026-04-14
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[gauntlets-index]]
- [[player-directory]]
- [[player-profile]]
- [[course-leaderboards]]
- [[teams-index]]
- [[sponsors-index]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for the unified site's root route.

The homepage should be the competition/player-side command center for Ascent Rivals while still providing a clear bridge into the marketing/game-discovery side of the site.

It should help players and followers answer:

- what is happening now
- which gauntlets are active or upcoming
- who and what is worth checking
- where to search for a player, team, course, sponsor, or gauntlet
- how to reach the game/marketing overview if they are new

## Route

Working route:

- `/`

Current app route equivalent:

- current `ascentun` root page

Current app behavior:

- shows Ascent Rivals branding
- provides search-everywhere for gauntlets, teams, players, and admin-only sponsors
- prefetches courses but does not include courses in the current search command

Final route direction:

- keep `/` as the adaptive homepage
- bias the page toward competition utility for returning users
- retain enough brand context that anonymous visitors understand where they are
- use top-bar navigation to bridge to the marketing/game side, likely `/game`

## Audience

Primary:

- returning players
- followers tracking players, teams, gauntlets, and course records
- logged-in players looking for quick re-entry

Secondary:

- new visitors who landed on the player-side surface first
- sponsors
- press/community viewers
- admins checking public state

## Page Goals

- preserve the current search-first utility of `ascentun`
- make the page feel less empty than a single search box
- provide a high-signal snapshot of active Ascent Rivals competition state
- introduce the game brand without replacing the dedicated marketing pages
- surface current and upcoming gauntlets as the primary player action path
- surface course records and pilot highlights as lightweight stat entry points
- avoid promising live presence, real-time feeds, or season systems before APIs exist
- keep admin tooling out of the homepage unless there is a critical public-state issue

## Page Positioning

The homepage is not the full marketing landing page.

It is closer to:

- race-control dashboard
- pilot command center
- competition operations lobby
- public status console

The marketing bridge should remain visible in the global top bar.

Possible bridge labels:

- `Game`
- `About Ascent`
- `Marketing`
- `Learn the Game`

The exact label should be finalized during navigation mock review.

## Current V1 Data Availability

### Search entities

Available from current app integrations:

- gauntlets
- teams
- players
- sponsors
- courses

V1 direction:

- include gauntlets, teams, players, sponsors, and courses in the new homepage search
- group results by entity type
- use public sponsor results if sponsor pages are public in the new site
- avoid admin-only sponsor visibility unless sponsor data truly remains private

Current implementation gap:

- current `HomeSearchCommand` does not include courses even though courses are prefetched
- current `HomeSearchCommand` only includes sponsors for admins

### Gauntlets

Available:

- gauntlet id
- title
- subtitle
- media
- sponsors
- qualifier and stage timing
- first and final event times
- region
- colors and ticker

Source:

- `GET /v1/gauntlet`

Homepage usage:

- active gauntlet cards
- upcoming gauntlet cards
- current/upcoming/past counts
- system-log entries derived from start/end timing

### Courses and leaderboards

Available:

- course metadata
- top leaderboard entries by course/category
- player id/name/avatar
- rank
- time in milliseconds
- loadout value

Sources:

- `GET /v1/course`
- `GET /v1/leaderboard?limit={n}`

Homepage usage:

- course record cards
- fastest finish and fastest lap highlights
- link to `/courses`
- link to player profiles from record holders

### Players

Available:

- player id
- name
- avatar URL
- team summary
- podium finishes
- matches played
- average circuit points
- public aggregate stats

Source:

- `GET /v1/player`

Homepage usage:

- pilot highlights
- top podium pilots
- high average circuit point pilots
- new/recently active pilots only if supported by timestamps or activity data

Guardrail:

- label rankings by the visible metric instead of claiming an overall best player

### Teams

Available:

- team id
- name
- tag
- colors
- media
- roster context where exposed
- public aggregate stats where available

Source:

- `GET /v1/team`

Homepage usage:

- search result grouping
- optional team spotlight
- high-level team count

### Sponsors

Available:

- sponsor list and sponsor detail data
- sponsor media
- sponsor links
- related gauntlet context where modeled

Sources:

- `GET /v1/sponsor`
- `GET /v1/sponsor/{sponsorId}`

Homepage usage:

- optional sponsor strip
- sponsor-backed gauntlet badges
- search result grouping

### High-level status counts

V1-safe counts:

- registered players
- teams
- active or upcoming gauntlets
- active courses
- sponsors

Do not show in V1 unless backed by a real source:

- players online
- live races in progress
- live viewers
- current season standings
- real-time system events

## V1 Page Structure

Default first-view priority:

1. hero / command briefing
2. search everywhere
3. active and upcoming gauntlets
4. high-level status strip
5. course records
6. pilot highlights
7. generated system log

## 1. Command Hero

Purpose:

- establish the Ascent Rivals identity
- make the page feel branded without turning it into a full marketing page
- direct visitors to the most important next actions

Content:

- Ascent Rivals logo or wordmark
- cinematic or illustrated background art if available
- concise command-style headline
- short game/competition descriptor
- primary CTA to `Gauntlets`
- secondary CTA to `Search`
- tertiary bridge CTA to `/game` or equivalent marketing overview

Tone examples:

- `Race control online`
- `Competition signal acquired`
- `Find pilots, gauntlets, teams, and course records`

Design guidance:

- use `BrandGold` and `BrandDarkBlue` as anchors
- background art can be atmospheric and gritty, but must not overpower search and competition state
- avoid relying on a large bespoke cinematic image as the only way the page works
- support a later current-season module without requiring it in V1

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `CommandAction`

## 2. Search Everywhere

Purpose:

- preserve the current homepage's strongest utility
- make entity lookup fast for returning users

Required V1 entity groups:

- Gauntlets
- Players
- Teams
- Courses
- Sponsors

Search behavior:

- grouped result sections
- fast keyboard-first interaction
- clear empty state
- route to entity detail pages
- top-bar search and homepage search should use the same search model where practical

Design guidance:

- search should feel like a command console, not a generic site search box
- placeholder copy should name the entities users can search
- result rows should show avatars/media where available
- result rows should use plural Nuxt routes such as `/players/[id]`, `/teams/[id]`, `/gauntlets/[id]`, `/sponsors/[id]`

Tone examples:

- `Search pilot, team, gauntlet, course, sponsor`
- `No matching signal`
- `Entity index synced`

## 3. Active and Upcoming Gauntlets

Purpose:

- make the homepage useful immediately for competition-aware visitors
- route players toward the most important current activity

Content:

- current gauntlets
- upcoming gauntlets
- status chip
- next relevant time
- sponsor strip when present
- prize indicator when available
- route to `/gauntlets/[id]`
- link to `/gauntlets`

Logged-in overlays:

- user's current rank where available
- qualification status where available
- finals eligibility where available
- reward/claim indicator where available

Guardrails:

- do not split the homepage into many empty gauntlet sections if there are few active events
- do not imply a gauntlet is live unless derived from real timing/state
- use `qualifier` only for gauntlet-level qualification windows, not match heats

## 4. High-Level Status Strip

Purpose:

- give the page a quick read on the state of the game ecosystem

V1-safe telemetry:

- player count
- team count
- active/upcoming gauntlet count
- active course count
- sponsor count
- latest leaderboard sync timestamp if available

Later telemetry:

- players online
- live race count
- live tournament status
- current season state
- concurrent viewers

Design guidance:

- use compact status tiles or a telemetry bar
- do not create fake real-time numbers
- if data is snapshot-based, label it as snapshot or latest sync

Tone examples:

- `Pilot registry`
- `Active gauntlets`
- `Courses indexed`
- `Leaderboard sync`

## 5. Course Records

Purpose:

- expose competitive stats without requiring users to know which course page to open
- route time-focused players to `/courses`

Content:

- fastest finish record
- fastest lap record
- selected featured courses or top courses with records
- player avatar/name for record holder
- course name
- time
- category label
- link to course leaderboard
- link to player profile

Design guidance:

- keep this as highlights, not a full leaderboard
- do not show all leaderboard categories at once
- if records are missing, show a useful link to the course leaderboard page instead of an empty table

## 6. Pilot Highlights

Purpose:

- give player-focused visitors another reason to browse
- showcase players through positive, data-backed metrics

V1 highlight types:

- top podium pilots
- high average circuit point pilots
- fastest course record holders
- best finish or best lap specialists

Avoid:

- deaths, crashes, or other negative callouts
- total kills as a strength module
- playtime as a strength module
- claims that are not supported by the available data

Design guidance:

- label each list by metric
- keep highlight cards small enough that gauntlets and search remain dominant
- route all player highlights to `/players/[id]`

## 7. Generated System Log

Purpose:

- create the sense of a live operations console using real site data
- provide a compact recent-activity feed before a true event-feed API exists

V1 model:

- generated from current snapshot data
- not a real-time feed
- labeled as latest sync or operations log

V1-safe log entry sources:

- gauntlet started based on start time
- qualifier window opened or closed based on timing
- finals scheduled based on stage/final time
- sponsor attached to a gauntlet if data exists
- course leaderboard updated if sync timestamp exists
- new gauntlet created if created timestamp exists

Example entries:

- `Starforge Tournament 02: qualifier window open`
- `MSI Circuit Cup: final stage scheduled`
- `Course records synced: Aztlan Run`
- `Sponsor signal attached: NovaForge`

Guardrails:

- do not fabricate events for ambience
- do not say `live` unless there is live state
- do not describe a heat as a qualifier

Terminal Ops components:

- `SystemLog`
- `TimestampLabel`
- `StatusChip`

## 8. Sponsor / Partner Strip

Purpose:

- acknowledge sponsors without making the homepage feel like an ad wall

V1 status:

- optional
- useful if sponsor data is public and media is present

Content:

- sponsor logo/name
- link to sponsor detail
- relationship to current gauntlets where available

Design guidance:

- keep sponsor presence secondary to player utility
- avoid generic ad-card treatment

## Logged-In Variant

Logged-in users should see personal context layered into the same public homepage.

Recommended V1 additions:

- avatar menu remains visible in the top bar and never collapses away
- link to `My Career`
- link to wallet state if wallet linking is required or incomplete
- link to `My Team` or team request/invite status where available
- personal status on active gauntlet cards where available
- personal placement on course record modules where available

Guardrail:

- avoid creating a separate private dashboard unless a workflow truly requires privacy

## Admin / Creator Variant

Admin and creator affordances should be restrained.

Allowed V1 additions:

- `Create Gauntlet` entry point if user has gauntlet creator/admin permission
- critical admin alert if public data is broken or pending moderation
- admin actions in the avatar/admin menu

Avoid:

- turning the homepage into an operations dashboard
- showing sponsor CRUD, team moderation, or prize-admin controls globally

## Empty States

No gauntlets:

- show search, course records, player directory, and game bridge
- copy example: `No active gauntlets detected`

No leaderboard data:

- show course entry point and explain that records will appear after timing data syncs
- copy example: `Course timing board awaiting records`

No players:

- show search empty state and game bridge
- copy example: `Pilot registry awaiting first signal`

No sponsor media:

- hide sponsor strip instead of showing broken or placeholder-heavy sponsor cards

## Loading States

Use skeletons or terminal-style loading states for:

- search index
- gauntlet cards
- course record cards
- status telemetry
- system log

Copy guidance:

- prefer precise loading labels such as `Syncing gauntlet index`
- avoid fake terminal noise

## Error States

Search index error:

- keep the rest of the page usable
- provide retry if practical

Gauntlet feed error:

- show a compact panel with route to `/gauntlets`

Leaderboard error:

- hide course records or show a compact retry state

Global error guardrail:

- never let one failed module blank the entire homepage

## Responsive Notes

Desktop:

- primary design target
- can use hero plus two-column or modular grid composition
- search should remain prominent above the fold

Tablet:

- collapse dense modules into stacked panels
- preserve top-bar bridge and login/avatar visibility

Mobile:

- marketing-quality hero must still work
- search remains near the top
- gauntlet cards stack before secondary stats
- login/avatar should not collapse away
- secondary top-bar links can collapse into a menu

## SEO Requirements

The homepage should support:

- clear title and description for Ascent Rivals
- Open Graph image using the strongest available brand art
- links to core public entity routes
- crawlable text describing the game and competition surface

V1 meta direction:

- title: `Ascent Rivals`
- description should mention players, gauntlets, teams, and course records

## V2 / Later Enhancements

Later homepage modules:

- current season or circuit overview
- player online count from presence/telemetry API
- live races or matches in progress
- true event/activity feed API
- live stream or watch CTA
- personalized recommended gauntlets
- news/announcements if an authoring model exists
- public social/live-stream signals for players
- richer sponsor/event campaign modules

## Open Questions

- Should the root homepage always be competition-first, or should anonymous first-time visitors get a more marketing-heavy order?
- Should `/game` become the canonical marketing landing route, or should a future `/marketing` or `/about` route own that bridge?
- What source, if any, should power homepage news/announcements without adding a CMS?
- Which data field should define a gauntlet as `featured`?
- Should the system log be purely generated in the frontend, generated by Eventun, or eventually replaced by a real event-feed endpoint?
