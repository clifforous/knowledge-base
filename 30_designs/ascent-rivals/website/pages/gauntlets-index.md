# Ascent Rivals Gauntlets Index Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[sponsors-index]]
- [[../../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for the gauntlet discovery route.

The index should help players and followers answer:

- what is active now
- what is coming next
- what has concluded
- which gauntlets are sponsored or prize-backed
- where to go for details, standings, finals, and rewards

## Route

Working route:

- `/gauntlets`

Current app route equivalent:

- `/gauntlet`

Final route direction:

- use plural route groups in the Nuxt site
- preserve redirects from old singular routes if public links already exist

## Audience

Primary:

- returning players
- followers tracking active competitions
- gauntlet creators/admins

Secondary:

- sponsors
- tournament organizers
- press/community viewers

## Page Goals

- make active and upcoming gauntlets obvious
- avoid a sparse page when there are only a few events
- preserve access to past gauntlets without making past events dominate
- expose create/manage affordances only to authorized users
- establish the main competition-side landing surface if the marketing bridge lands here
- keep calendar support available without making calendar-first discovery a V1 dependency

## Current V1 Data Availability

### Gauntlet list

Available:

- gauntlet id
- creator id
- title
- subtitle
- ticker
- primary and secondary colors
- stat/scoring configuration
- first event time
- final event time
- region code
- qualifiers
- media
- sponsors
- stages

Source:

- `GET /v1/gauntlet`

### Calendar

Available:

- gauntlet calendar items

Source:

- `GET /v1/gauntlet/calendar`

V1 caution:

- calendar can be linked from this page, but does not need to be the primary discovery view.

### Sponsors

Available:

- sponsor ids and names
- sponsor details

Sources:

- `GET /v1/sponsor`
- `GET /v1/sponsor/{sponsorId}`

### Auth and role state

Available through current app/auth context:

- logged-in state
- roles such as gauntlet creator/admin where supported
- creator ownership checks for edit/delete behavior

## Classification Model

The index should group gauntlets by state.

Recommended V1 groups:

- `Current`
- `Upcoming`
- `Past`

Optional group:

- `Featured`

Current means:

- a qualifier window is active, or
- the gauntlet is between its first and final event time, or
- a stage/final is imminent enough to be operationally relevant

Upcoming means:

- the gauntlet has not started yet and has a future qualifier or stage.

Past means:

- the final event time has passed and there are no active/relevant pending stages.

Design guardrail:

- do not split gauntlets into too many separate top-level buckets if the catalog is sparse
- prefer one unified page with filters/status chips over multiple empty sections

## V1 Page Structure

## 1. Operations Header

Purpose:

- establish that this is the competition operations hub

Content:

- title such as `Gauntlets`
- short status copy
- count of active/upcoming gauntlets if available
- top-level CTA to create a gauntlet for authorized users
- link to past gauntlets
- link to calendar if available

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `CommandAction`

Tone examples:

- `Competition feed active`
- `No active gauntlets detected`
- `Qualifier windows online`

## 2. Current Gauntlets

Purpose:

- prioritize events players can act on now

Card content:

- gauntlet title
- subtitle/ticker
- media thumbnail
- status chip
- active qualifier window or next stage time
- sponsor strip if present
- prize indicator if prize data is available or known
- region
- entry/team/invite constraints if available
- link to detail

Logged-in overlays:

- player's current rank if available
- qualification status if available
- claim/reward indicator if available

## 3. Upcoming Gauntlets

Purpose:

- show what players should plan for

Card content:

- next qualifier start
- first event time
- final event time
- sponsor and prize indicators
- route to detail

Design guidance:

- cards can be slightly more compact than current gauntlets
- emphasize time-to-start and event identity

## 4. Featured Events

Purpose:

- optionally highlight sponsored or high-priority gauntlets

V1 status:

- optional
- only show if the data or manual curation supports it

Guardrail:

- do not create a permanent empty featured section

## 5. Past Gauntlets Entry Point

Purpose:

- preserve access to concluded events without letting history bury current action

V1 options:

- collapsed section
- filter tab
- route link such as `/gauntlets?status=past`
- future dedicated route

Past card content:

- gauntlet title
- winner/placement summary if available
- final date
- sponsor/prize summary if available
- link to detail

## 6. Calendar Link

Purpose:

- provide schedule-oriented browsing without making it the default page

V1:

- link or lightweight teaser

Later:

- `/gauntlets/calendar` or `/calendar`
- full schedule view for qualifiers, stages/finals, streams, and showcase events

## Permissioned Actions

### Create Gauntlet

Visible when:

- logged-in user has gauntlet creator role, or
- logged-in user is an admin

Placement:

- in the operations header
- not in the global top bar

### Admin/Operations

Avoid global admin clutter.

Admin-only links can appear in contextual menus or cards only when they apply to a specific gauntlet.

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can browse current/upcoming gauntlets, past entry point, sponsors/prizes where public |
| Logged-in player | same plus personal status overlays where endpoints support them |
| Gauntlet creator/admin | same plus `Create Gauntlet` and contextual manage links |

## Empty / Loading / Error States

Required states:

- no current gauntlets
- no upcoming gauntlets
- no past gauntlets
- failed gauntlet list fetch
- failed sponsor fetch
- partial media missing

Tone:

- `No active gauntlets detected.`
- `Upcoming schedule not yet published.`
- `Sponsor signal unavailable.`

## Responsive Behavior

Desktop:

- hero/status header
- current gauntlets as prominent cards
- upcoming/past as list or compact cards

Tablet:

- reduce columns
- keep status and next time visible

Mobile:

- stack cards
- keep login/avatar visible in top bar
- make time/status and primary action visible before secondary metadata

## SEO and Sharing

The gauntlet index should support:

- title: `Gauntlets - Ascent Rivals`
- description focused on current and upcoming competitions
- canonical URL

Do not expose private player rank or qualification state in metadata.

## Open Questions

- Should the marketing-to-competition bridge land on `/gauntlets` or a future competition landing page?
- Should past gauntlets be a filter state, collapsed section, or standalone route?
- What data marks a gauntlet as featured?
- Should calendar live at `/gauntlets/calendar` or `/calendar`?

## Next Steps

- Use this spec with [[gauntlet-detail]] for the next gauntlet design pass.
- Decide whether the first Pencil gauntlet pass should mock current/upcoming/past states or focus only on active/upcoming.
