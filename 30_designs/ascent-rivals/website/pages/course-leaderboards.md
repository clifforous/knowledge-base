# Ascent Rivals Course Leaderboards Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[player-profile]]
- [[../../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for course-based leaderboards.

This page should help players and followers answer:

- which courses exist
- which players are fastest on each course
- who owns the best lap and best finish records
- where the logged-in player stands
- which leaderboard category is being viewed

## Route

Working route:

- `/courses`

Optional later route:

- `/courses/[code]`

V1 route direction:

- `/courses` can support course and category selection through query state or local page state
- do not require `/courses/[code]` until the product needs shareable course-detail URLs, lore-heavy course pages, or deeper per-course analytics

Possible query shape:

- `/courses?course={courseCode}&category={category}`

## Audience

Primary:

- players comparing best times
- players trying to improve on a specific course
- followers checking who owns course records

Secondary:

- gauntlet organizers
- teams
- sponsors
- press/community viewers

## Page Goals

- make course selection fast
- make leaderboard category selection clear
- foreground best lap and best finish records
- show personal placement for logged-in users where available
- connect course competition to player profiles
- keep course metadata and lore available without overwhelming the stat task
- avoid confusing course runtime heats/laps with gauntlet qualifiers

## Current V1 Data Availability

### Course metadata

Available:

- course code
- display name
- planet
- description
- difficulty
- heats
- laps
- active state
- media

Source:

- `GET /v1/course`

Terminology note:

- course `heats` and `laps` describe course/match runtime settings
- they are not gauntlet qualifiers

### Top leaderboard entries

Available:

- top leaderboard entries grouped by course
- category-specific arrays
- player id
- player name
- player avatar URL
- rank
- time in milliseconds
- loadout value

Source:

- `GET /v1/leaderboard?limit={n}`

Categories:

- `clientFinish`
- `clientLap`
- `clientLowCostFinish`
- `clientLowCostLap`
- `clientHighCostFinish`
- `clientHighCostLap`
- `serverFinish`
- `serverLap`

### Player-specific leaderboard placement

Available:

- player-specific leaderboard placement by course and category
- rank
- time in milliseconds

Source:

- `GET /v1/leaderboard/player/{playerId}`

V1 usage:

- show the logged-in user's placement when they are viewing course leaderboards
- show placements on player profiles when viewing a player

### Player profile linking

Available:

- leaderboard rows include player id/name/avatar

V1 usage:

- each row should link to `/players/[id]`

## Category Model

The raw API categories should be presented in player-readable groups.

Recommended V1 groups:

- `Finish Time`
- `Lap Time`
- `Low-Cost Finish`
- `Low-Cost Lap`
- `High-Cost Finish`
- `High-Cost Lap`
- `Server Finish`
- `Server Lap`

Default category:

- `Finish Time`

Default course:

- first active course with leaderboard data, or
- a featured/currently relevant course if product/config later supports it

Design guardrail:

- do not show all eight categories as eight full tables at once
- use tabs, segmented controls, or command-like filters
- keep the selected course and selected category obvious at all times

## V1 Page Structure

Default first-view priority:

1. course selector and selected course identity
2. active category leaderboard
3. logged-in personal placement
4. course metadata and related context
5. cross-course overview

## 1. Leaderboard Command Header

Purpose:

- establish the page as a course record console

Content:

- title such as `Course Leaderboards`
- selected course
- selected category
- search/filter affordance
- top-N limit if user-facing
- timestamp or sync label if useful

Tone examples:

- `Course records online`
- `Select course signal`
- `Timing board synced`

Terminal Ops components:

- `HeroBriefing`
- `PathBar`
- `StatusTelemetryBar`
- `CommandSearch`

## 2. Course Selector

Purpose:

- make switching courses fast and visual

Content per course:

- course image
- display name
- planet
- difficulty
- active/inactive state
- default laps/heats metadata
- best visible record summary if leaderboard data is available

Interaction:

- select course
- filter/search by course name or planet
- optionally hide inactive courses by default

Design guidance:

- desktop can use a side rail, horizontal card strip, or compact grid
- mobile should use a select/list pattern with visible selected course identity
- do not let course art dominate the leaderboard table

## 3. Selected Course Briefing

Purpose:

- orient the user before the table

Content:

- course name
- planet
- description
- difficulty
- media
- laps/heats metadata
- selected category record summary

Optional later:

- course lore excerpt
- planet link
- course hazards
- gauntlets currently using the course

## 4. Category Filter

Purpose:

- let users switch leaderboard types without losing course context

Recommended V1 categories:

- Finish
- Lap
- Low-Cost Finish
- Low-Cost Lap
- High-Cost Finish
- High-Cost Lap
- Server Finish
- Server Lap

Design guidance:

- use concise labels in the UI
- expose explanatory helper text for low/high-cost and server/client distinctions if needed
- preserve selected category in URL query if feasible

## 5. Leaderboard Table

Purpose:

- show the top performers for the selected course/category

Columns:

- rank
- player
- time
- loadout value, if meaningful to players
- team, if the row or related player data supports it later

Row actions:

- open player profile
- compare to logged-in player's time, later

Display guidance:

- time should be the visual anchor
- top ranks can receive stronger framing
- do not over-decorate every row
- preserve scan clarity over lore styling

Terminal Ops components:

- `DataTable`
- `RankPill`
- `PilotIdentityCell`
- `TelemetryValue`

## 6. Personal Placement Strip

Only when the user is logged in and player placement data is available.

Purpose:

- show "where am I?" without requiring the player to find themselves in the top-N table

Content:

- user's rank
- user's best time
- delta to top time if derivable client-side from table data
- selected course/category

Source:

- `GET /v1/leaderboard/player/{playerId}`

Tone examples:

- `Pilot placement acquired`
- `No registered time for this course/category`

Guardrail:

- do not expose private ELO or rating here

## 7. Cross-Course Overview

Purpose:

- help users discover which courses have active records

V1 content:

- course cards with best finish and best lap summary where available
- active/inactive state
- route/query link to selected course/category

Placement:

- below the selected leaderboard, or
- used as the default state before a course is selected

Design guidance:

- useful for returning players, but secondary to the selected leaderboard once a course/category is active

## 8. Related Context

Optional V1/later content:

- active/upcoming gauntlets using this course
- planet/lore link
- course media
- related VODs or watch links
- ship part/loadout notes later

V1 caution:

- keep this secondary
- do not block leaderboard usability on lore/content completeness

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view courses, selected leaderboard, course metadata, and player profile links |
| Logged-in player | same plus personal placement strip when player leaderboard data is available |
| Admin | same as logged-in; no special admin actions required for V1 unless course administration is added later |

## Empty / Loading / Error States

Required states:

- no courses
- no active courses
- no leaderboard entries for selected course/category
- logged-in player has no time for selected course/category
- failed course fetch
- failed leaderboard fetch
- failed player-placement fetch
- course media missing

Tone:

- `No course records detected.`
- `No registered time for this category.`
- `Course manifest unavailable.`
- `Timing board sync failed.`

Guardrail:

- missing data should not imply the player has a zero or poor result

## Responsive Behavior

Desktop:

- selected course briefing and leaderboard table should be visible without excessive scrolling
- course selector can be a side rail, compact grid, or horizontal strip
- category filter can be tabs or segmented controls

Tablet:

- collapse course selector into a scrollable strip or dropdown
- preserve rank, player, and time columns

Mobile:

- stack modules
- keep login/avatar visible in top bar
- use a course select/dropdown or compact cards
- table can horizontal-scroll or convert to rank cards
- preserve rank, player, time, and category

## SEO and Sharing

The course leaderboards page should support:

- title: `Course Leaderboards - Ascent Rivals`
- description focused on course records, lap times, and finish times
- canonical URL

If query-state pages are indexable later:

- title: `{Course Name} {Category} Leaderboard - Ascent Rivals`
- description using course, planet, and leaderboard category

Do not expose private player status in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- dedicated `/courses/[code]` route
- season filters
- gauntlet/event filters
- team filters
- ship part/loadout filters
- deltas between player and world record
- percentile placement
- checkpoint/split breakdowns
- course hazard/lore modules
- planet/manufacturer relationship modules
- VODs or run recaps

## Terminology Guardrails

- `Lap` is a course/match runtime concept.
- `Finish Time` is the total time for the relevant run/match category.
- `Heat` is a match-internal runtime round.
- `Qualifier` is a gauntlet/tournament window.
- Do not call leaderboard categories qualifiers.
- Do not call course heats qualifier rounds.

## Open Questions

- Should the route stay as one `/courses` page with query state, or should `/courses/[code]` be added for shareable course pages?
- Which category should be the default: client finish, server finish, or product-defined `Finish Time`?
- How should low-cost and high-cost categories be explained to new players?
- Should inactive courses be hidden by default or visible with an archived state?
- Is loadout value meaningful enough for V1 display, or should it be behind an expanded row?

## Next Steps

- Ask Pencil for one course leaderboard mock using this spec and Terminal Ops.
- Use the mock to decide whether course selection should be a rail, strip, grid, or dropdown-first pattern.
- Create companion spec for sponsors.
