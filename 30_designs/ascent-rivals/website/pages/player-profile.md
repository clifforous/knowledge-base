# Ascent Rivals Player Profile Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../design-doc-roadmap]]
- [[player-directory]]
- [[course-leaderboards]]
- [[team-profile]]
- [[../../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the first page-level specification for the public player profile route.

This spec is intentionally V1/V2-aware:

- V1 should use data that Eventun/OpenAPI and the current `ascentun` implementation already expose or strongly imply.
- V2 ideas can be captured but should not block the first Nuxt build.

## Route

Working route:

- `/players/[id]`

Current app route equivalent:

- `/player/[id]`

Final naming should align with the new IA, which favors plural route groups.

## Audience

Primary:

- the player whose profile it is
- other players comparing themselves
- team managers or teammates
- followers watching a player's performance

Secondary:

- tournament organizers
- press/community viewers
- sponsors

## Page Goals

- make a player feel identifiable and worth following
- show what the player is good at, not only their raw rank
- expose public career stats and per-course performance
- support comparison and discovery without requiring login
- layer private/user-specific actions only when relevant
- establish a reusable data-page pattern for Terminal Ops

## Core Product Principle

The player profile should not only reward the fastest or highest-ranked players.

It should help each player understand their strengths.

Examples:

- best course by finish time
- best course by lap time
- notable course leaderboard placement
- podium frequency, if it is presented as a rate rather than a raw count
- strong circuit point generation, if it is normalized enough to avoid rewarding only volume

V1 can infer some strengths from available aggregate stats. V2 can add richer strengths once Eventun exposes deeper breakdowns.

Guardrail:

- avoid strength modules that are mostly volume counters, such as total kills, total play time, or total races
- avoid negative or joke-framed stats, such as most deaths or most crashes
- do not present combat style, loadout style, consistency, survival, or improvement trends until the data model can support those claims cleanly

## Current V1 Data Availability

This section is based on the current `ascentun` code and OpenAPI data.

### Player identity

Available:

- player id
- name
- avatar URL
- team summary

Source:

- `GET /v1/player/{playerId}/career`
- `GET /v1/player`

### Overall career stats

Available:

- podium finishes
- matches played
- total play time
- total circuit points
- average circuit points
- total kills
- average kills
- total deaths
- average deaths
- total crashes
- average crashes
- total obelisks
- average obelisks
- total credits
- average credits

Source:

- `GET /v1/player/{playerId}/career`
- `GET /v1/player`

### Per-course career stats

Available per course code:

- podium finishes
- matches played
- total kills
- average kills
- total deaths
- average deaths
- total crashes
- average crashes
- total obelisks
- average obelisks
- best lap time
- average lap time
- best finish time
- average finish time
- total play time
- average weight
- total circuit points
- average circuit points
- total credits
- average credits

Source:

- `GET /v1/player/{playerId}/career`

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

- course metadata may include default/known heats and laps for the course/ruleset, but heats remain match-internal runtime units.

### Leaderboard data

Available:

- top leaderboard entries grouped by course
- player-specific leaderboard rank/time by course
- client/server finish and lap categories
- low-cost/high-cost variants
- loadout value on leaderboard ranks

Sources:

- `GET /v1/leaderboard`
- `GET /v1/leaderboard/player/{playerId}`

### Match history

Available:

- player match history
- course code
- match id
- race mode
- start time
- match stats

Match stats include:

- placement
- podium finish
- best lap time
- best finish time
- circuit points
- kills
- deaths
- crashes
- credits
- obelisks

Source:

- `GET /v1/match/history/{playerId}`

### Match summary / heat breakdown

Available for specific match summary contexts:

- match standings
- heat array
- per-heat standings
- per-heat stats
- loadout object on heat standings

Sources:

- `GET /v1/match/summary/{sessionId}/{matchId}`
- `GET /v1/match/summary/gauntlet/{gauntletId}/recent`

V1 caution:

- generic public player profile should show a match-history overview if the endpoint is available.
- detailed match-summary drill-in and heat breakdown views are out of V1 scope for the player profile.

### AccelByte medals and badges

Available conceptually:

- in-game medals
- in-game badges

Source:

- AccelByte, using the logged-in player's token where supported

V1 caution:

- Eventun does not currently appear to own medals or badges.
- The site can potentially show medals and badges for the logged-in user's own profile if AccelByte exposes them through that user's token.
- Do not assume public medal or badge counts are available for other players unless AccelByte or Eventun exposes a safe public lookup.

## V1 Page Structure

Default first-view priority:

1. identity and career context
2. career totals
3. course stats and course placements
4. optional strengths, only if they can be derived cleanly from best lap or best finish data

## 1. Player Header / Briefing

Purpose:

- establish identity and context

Content:

- avatar
- player name
- team name/tag if present
- public rank tier if available
- profile status labels if useful

V1 supported:

- avatar
- name
- team summary

V1 conditional:

- public rank tier only if Eventun/AccelByte-backed public rank tier is available

V2:

- richer player banner media
- social links
- current ship/loadout identity

Social-link note:

- player-owned public social links are a future profile feature, not a V1 dependency
- likely links include Twitch, YouTube, X, Discord, and website
- players should control whether each link is public
- product must decide whether social URLs can be unverified player-provided links or require provider/ownership verification before being displayed as official

Terminal Ops component:

- `HeroBriefing`
- `PathBar`
- optional `StatusTelemetryBar`

## 2. Career Overview

Purpose:

- show high-level public career totals

Recommended V1 stats:

- matches played
- podium finishes
- average circuit points
- total circuit points
- kills, if combat contribution belongs in the public overview
- obelisks
- total play time
- total credits

Display guidance:

- use grouped stat cards rather than one flat grid of every value
- group by `Results`, `Course Objectives`, `Economy`, `Time`
- avoid foregrounding deaths, crashes, or other negative-interesting stats in the default overview

Terminal Ops component:

- `BracketPanel`
- stat cards

## 3. Course Stats

Purpose:

- show where the player performs well

V1 content per course:

- course media
- course name
- planet
- public leaderboard placement where available
- matches played
- best lap
- average lap
- best finish
- average finish
- average circuit points
- podium finishes

Interaction:

- sort by leaderboard placement, best finish, best lap, matches played, average circuit points, podiums
- filter active courses if needed

Terminal Ops component:

- `DataTable`
- `EntityCard`
- optional card/table hybrid

## 4. Optional Strength Snapshot

Purpose:

- answer "what is this player good at?" only when the data supports a defensible positive claim

V1 possible modules:

- Best Course by best finish time
- Best Course by best lap time

V1 derivation rules:

- derive from career and per-course aggregate stats
- do not imply loadout-specific claims unless leaderboard loadout values or future detailed data supports them
- avoid overclaiming causality
- do not use total kills, total play time, total races, or similar always-increasing counters as strengths
- do not use deaths, crashes, or other negative stats as strength modules

Deferred/candidate modules:

- podium rate
- best average circuit points course
- consistency
- improvement trend
- survival rate by mode
- loadout-specific strength

V2 modules:

- best loadout context
- strongest ship-part/course pairing
- improvement trend
- consistency over time
- survival rate by mode
- teammate contribution profile

Terminal Ops component:

- `PlayerStrengthModule`
- `BracketPanel`

## 5. Leaderboard Placement

Purpose:

- show public rank placement in course leaderboards

V1 decision:

- include the player's placements across the various courses where leaderboard data is available

V1 content:

- per-course personal leaderboard rank and time
- category variants:
  - client finish
  - client lap
  - client low-cost finish/lap
  - client high-cost finish/lap
  - server finish
  - server lap

Design caution:

- do not overwhelm first view with every category
- start with most meaningful categories and allow expansion

Terminal Ops component:

- `DataTable`
- `LocalSectionNav` or segmented category filter

## 6. Match History

Purpose:

- show recent play history and link toward deeper analysis later

V1 decision:

- include a match-history overview
- do not include a dedicated match-detail route or heat-breakdown drill-in in V1

V1 content:

- recent match list
- course
- race mode
- start time
- placement
- circuit points
- best lap
- best finish
- kills and obelisks where useful
- deaths and crashes only if the row has a detailed/expanded mode and the product wants complete stat parity

V1 caution:

- if current frontend does not yet consume this endpoint, treat it as a page-spec requirement but not a preserved UI feature.

V2:

- match detail pages
- heat breakdown drill-ins
- loadout comparison
- player-vs-winner comparison

Terminology:

- use `Match History` for match list
- use `Heat Breakdown` only inside match detail/drill-in views
- do not call qualifiers heats

## 7. Gauntlet Results

Purpose:

- show tournament/gauntlet performance history

V1 possible:

- player gauntlet stats if `GET /v1/gauntlet/stats/player/{playerId}` is available and usable
- player-specific gauntlet leaderboards if available

V1 caution:

- exact presentation depends on the current shape of gauntlet stats and standings responses

V2:

- trophies
- finals placements
- historical event highlights
- qualification progression over time

## 8. Trophies and Medals

Purpose:

- support recognition beyond raw leaderboard rank

V1 possible:

- show real medals and badges for the logged-in user's own profile if AccelByte exposes them through the user's token
- show tournament/gauntlet trophies only if Eventun exposes reliable winner/placement data

V1 caution:

- if medals are real game achievements, do not fake them as official achievements without backend support
- do not show generated/computed medals as if they are official game medals
- do not assume public medal counts for other players are available in V1

V2:

- backend-owned public trophy and medal summaries
- gauntlet winner trophies
- event medals
- achievement history

## 9. Own-Profile Overlay

Only when the viewed player is the logged-in user.

V1 possible:

- wallet link
- team invite/request state
- link to team management or team page
- profile/account actions if supported
- AccelByte medals and badges for the logged-in user if available

Placement decision:

- own-profile wallet and team actions should appear on the public profile page when the logged-in user is viewing their own profile
- these actions can also remain reachable from the avatar/account menu, but the profile page should not require users to hunt through global account navigation

V1 not currently primary:

- owned items
- battle pass
- private ELO

V2:

- AccelByte item ownership
- battle pass progress
- private rating detail
- recommendation cards

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view public profile, public stats, course stats, leaderboards, public match history if enabled |
| Logged-in other player | same as anonymous plus account/avatar top bar and comparison affordances if available |
| Logged-in own profile | public profile plus wallet/team/account action overlays and own AccelByte medals/badges if available |
| Admin | same as logged-in, plus admin-only moderation/actions only if product decides they are needed |

## Empty / Loading / Error States

Required states:

- player not found
- no course stats
- no leaderboard placements
- no match history
- no team
- failed career fetch
- failed leaderboard fetch
- failed match history fetch

Tone:

- empty states should be direct and in-world where tasteful
- do not hide missing data by implying zero performance

## Responsive Behavior

Desktop:

- full Terminal Ops shell
- profile header plus career overview and course stats
- two-column layout where useful
- tables for course stats and leaderboards

Tablet:

- reduce secondary columns
- keep key stats visible
- allow leaderboard/category filters to wrap

Mobile:

- maintain top bar with login/avatar visible
- stack profile modules
- use cards or horizontally scrollable tables for dense stats
- preserve key values:
  - course
  - rank/time
  - matches played
  - best lap / best finish

Mobile is not the primary player-side use case, but the profile must remain usable.

## SEO and Sharing

Public player pages should support:

- title: `{Player Name} - Ascent Rivals Career`
- description using team and key stats where available
- Open Graph image from avatar or generated profile card
- canonical URL

Guardrail:

- do not expose private rating/ELO in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1 if unsupported:

- exact public rank tier history
- private exact ELO display on own profile
- public trophy and medal counts for other players
- player-owned public social links
- social-link verification state
- ship/loadout-specific strength analysis
- ship-part/course pairing analysis
- improvement trends over time
- consistency metrics
- survival rate by mode
- detailed match pages with heat drill-ins
- recommendation cards
- AccelByte owned items and battle pass progress

## Resolved Product Decisions

1. V1 should include a match-history overview, but not a match-detail page.
2. V1 should include course leaderboard placements using player-specific leaderboard data where available.
3. Medals and badges are real in-game systems owned by AccelByte. Do not fake them from Eventun aggregate stats.
4. V1 strength modules should be limited to best finish and best lap unless richer normalized data becomes available.
5. Avoid negative or joke-framed stats for now.
6. The default layout should prioritize identity and career totals first, then course stats. Strength modules are welcome only where the data supports them cleanly.
7. Own-profile wallet and team actions should appear on the public profile page for the logged-in user.

## Next Steps

- Ask the design AI/Pencil for a player profile mock using this spec and Terminal Ops.
- Create companion specs for course leaderboard and gauntlet detail.
