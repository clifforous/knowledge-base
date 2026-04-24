# Ascent Rivals Player Directory Page Spec

Date: 2026-04-14
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[player-profile]]
- [[team-profile]]
- [[course-leaderboards]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for the public player directory.

The directory should help players and followers answer:

- which players exist
- what team a player belongs to
- which player profile to open
- who has meaningful public activity
- how to search and sort the pilot registry without requiring login

## Route

Working route:

- `/players`

Current app route equivalent:

- `/player`

Final route direction:

- use plural route groups in the Nuxt site
- preserve redirects from old singular routes if public links already exist

## Audience

Primary:

- players looking for other players
- followers tracking a pilot
- team managers looking at potential recruits

Secondary:

- tournament organizers
- sponsors
- press/community viewers

## Page Goals

- preserve the current simple directory behavior
- make players feel like public entities, not database rows
- show enough context to distinguish similarly named players
- support search by player and team
- support lightweight sorting using data already exposed by Eventun
- avoid overloading the directory with deep stats that belong on player profiles
- leave room for future public social links without making them a V1 dependency

## Current V1 Data Availability

### Player list

Available:

- player id
- player name
- avatar URL
- team summary
- total kills
- average kills
- total deaths
- average deaths
- total crashes
- average crashes
- total obelisks
- average obelisks
- podium finishes
- matches played
- total play time
- total circuit points
- average circuit points
- total credits
- average credits

Source:

- `GET /v1/player`

### Team summary

Available on player rows:

- team id
- team name
- team tag
- team avatar URL
- designation
- rank
- team colors
- team media

Source:

- `GET /v1/player`

### Current UI behavior

Current app already supports:

- player card grid
- player avatar
- player name
- team name or `No Team`
- podium count
- matches played
- average circuit points
- search by player or team
- sort by name
- sort by podium finishes
- sort by matches played
- sort by average circuit points
- lazy loading / incremental display

## V1 Page Structure

Default first-view priority:

1. directory header and search
2. player cards/list
3. sort controls
4. lightweight player context

## 1. Pilot Registry Header

Purpose:

- establish this as the player discovery surface

Content:

- title such as `Players`
- short operational description
- player count if useful
- optional link to logged-in user's own career profile

Tone examples:

- `Pilot registry online`
- `Search pilot signal`
- `No pilots detected`

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `CommandSearch`

## 2. Search and Sort

Purpose:

- let users find a player quickly

V1 controls:

- search by player name
- search by team name
- sort A-Z
- sort Z-A
- sort by podium finishes
- sort by matches played
- sort by average circuit points

Design guidance:

- keep filters compact
- do not make stats filters feel like a full analytics page
- player directory is for discovery; player profile is for depth

## 3. Player Cards

Purpose:

- show enough identity to choose a profile

V1 card content:

- avatar
- player name
- team name/tag if available
- podium finishes
- matches played
- average circuit points
- link to `/players/[id]`

Optional V1 card content:

- small public rank tier if available from supported public rank data
- team accent color, if visually useful and not noisy

Do not include in V1 cards by default:

- deaths
- crashes
- exact ELO
- wallet state
- private team invite/request state
- owned items or battle pass data

Terminal Ops components:

- `EntityCard`
- `PilotIdentityCell`
- `TeamTag`
- `TelemetryValue`

## 4. Public Activity Signals

Purpose:

- help users distinguish inactive/empty players from active public profiles

V1-safe signals:

- matches played
- podium finishes
- average circuit points
- team membership

Guardrail:

- do not present volume-only stats as strengths
- do not frame low or negative stats as jokes
- avoid making the directory a leaderboard replacement

## 5. Player Social Links

V1 status:

- not currently supported by the Eventun player list/profile model
- do not block the V1 player directory on socials

Future direction:

- allow players to add public social links on their own profile
- likely fields include Twitch, YouTube, X, Discord, website, and possibly live-stream URL
- player should control whether each link is public

Verification question:

- Twitch/YouTube/X profile URLs could be unverified user-provided links, or the site could require account verification/ownership proof before showing them as official
- unverified links are simpler and may be acceptable if clearly treated as player-provided links
- verified links are safer for impersonation risk but require additional auth/provider integration

Directory usage:

- if socials exist later, show only small public icons on cards
- do not let social links dominate the directory
- Twitch/live indicator can be a later enhancement if stream status integration exists

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can browse/search/sort players and open public profiles |
| Logged-in player | same plus optional `My Career` shortcut and own-profile context |
| Admin | same as logged-in; no V1 admin actions unless moderation tools are added later |

## Empty / Loading / Error States

Required states:

- no players
- no players matching search
- failed player list fetch
- avatar missing
- team summary missing

Tone:

- `No pilots detected.`
- `No pilot signal matches this query.`
- `Pilot registry unavailable.`

Guardrail:

- missing stats should not be rendered as zero unless the backend explicitly returns zero

## Responsive Behavior

Desktop:

- command header
- search/sort row
- responsive card grid

Tablet:

- reduce card columns
- keep search and sort visible

Mobile:

- stack search and sort controls
- use compact player cards
- preserve avatar, name, team, and one or two key stats
- keep login/avatar visible in top bar

## SEO and Sharing

The player directory should support:

- title: `Players - Ascent Rivals`
- description focused on public pilot profiles, teams, and career stats
- canonical URL

Do not expose private ELO, wallet state, private account state, or invite/request state in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- player-owned public social links
- social-link verification state
- public Twitch/live status
- rank tier filters
- team filters
- course specialty filters
- gauntlet participation filters
- region filters
- season filters
- recently active sorting
- public profile badges if backend/AccelByte exposes them safely

## Open Questions

- Should the V1 card show podiums/matches/average circuit points, or stay closer to avatar/name/team only?
- Should player social links be unverified user-provided URLs, verified provider links, or both with a visible trust state?
- Should a logged-in player manage public socials on their own profile page, an account menu/settings page, or both?
- Should the directory support a `live now` Twitch indicator later, or should that live only on `/watch`?
- Should player cards include team tag instead of team name when space is constrained?

## Next Steps

- Ask Pencil for one player directory mock using this spec and Terminal Ops.
- Update [[player-profile]] when player-owned social-link fields become a real feature.
- Keep homepage search result requirements aligned with this directory's public player-card fields.
