# Ascent Rivals Player Directory Page Spec

Date: 2026-04-14
Status: Approved desktop/mobile public-directory calibration; implementation states and contract
verification remain open
Last reviewed: 2026-07-21

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[player-profile]]
- [[team-profile]]
- [[course-leaderboards]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

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

- use plural route groups in the Next.js site
- allow old singular routes to retire without redirects unless later measured inbound use justifies an exact mapping

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

## Approved Initial Decisions

- Treat `/players` as a public pilot registry rather than a leaderboard.
- Include every real pilot with a usable public identity, including new or inactive pilots with no matches.
- Exclude only records explicitly classified by the source system as bots, test accounts, or internal identities; do not infer exclusion from a name pattern or zero activity.
- Default to alphabetical ordering and make name/team search the primary interaction.
- Keep podium finishes and matches played as secondary card context and optional sorts rather
  than the directory's primary ranking. Overall Total and Average Circuit Points remain outside
  the anonymous public surface under the later bounded-profile decision.
- Present team identity as `[TAG] Team Name` when space permits, reduce it to the tag on compact cards, and use `Independent` for an unaffiliated pilot.
- Keep the pilot avatar as the card's only image; do not add the team avatar to ordinary player-directory cards.
- Fetch one compact, unpaginated directory collection and perform search, filtering, sorting, and progressive display in the browser.
- Reconsider server pagination only when measured query time, response transfer, parsing/hydration cost, memory use, or interaction latency becomes material.

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

### Initial Website Collection Contract

The current `GET /v1/player` response exposes substantially more data than the directory needs. Reuse it while the measured response remains inexpensive; otherwise add a compact unpaginated Website projection containing only fields rendered, searched, or sorted by the directory:

- player id and public display name;
- avatar URL;
- public team id, name, and tag when present;
- podium finishes and matches played while those remain approved card/sort fields.

Do not include full career groups, match history, course history, nested team media, private account state, exact AccelByte MMR, wallet data, or other profile-detail payloads in the directory collection.

Do not add current AccelByte MMR or a derived rank field to the directory. If a future Eventun-owned named-division system is approved, revisit the collection only after its public contract exists; the browser must never derive divisions from raw MMR.

Client collection behavior:

- fetch the complete compact directory collection once;
- normalize searchable player/team text once and search locally without network round trips;
- apply all initial sorts and filters locally;
- use incremental card reveal or virtualization when useful to limit DOM work;
- remember that rendering fewer local cards does not reduce the original transfer size;
- use measured compressed bytes, fetch/query latency, parse and hydration cost, memory, and input responsiveness as the scale signals rather than a fixed row-count threshold.

The initial release does not require server pagination for the player directory. Large theoretical counts such as 10,000 or 100,000 records are not themselves acceptance claims: compact records may remain practical, but long names and avatar URLs can still create a multi-megabyte response that must be evaluated on representative mobile hardware and networks.

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
- sort A-Z as the default
- sort Z-A
- sort by podium finishes
- sort by matches played

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
- `[TAG] Team Name` when space permits
- team tag alone on compact cards when available
- `Independent` when the pilot has no team
- podium finishes
- matches played
- link to `/players/[id]`

Optional V1 card content:

- one restrained team-color accent, such as a narrow rule or small marker, only when the supplied color remains legible in the Website palette

Team identity styling:

- use a neutral Website-controlled surface and text treatment for the team tag by default;
- do not apply arbitrary team foreground and background colors as the full tag treatment;
- never rely on a team color to communicate identity or membership;
- do not render a separate team logo/avatar beside the pilot avatar in the ordinary card;
- reserve richer team color and media treatment for `/teams/[id]` and other team-primary contexts.

Do not include in V1 cards by default:

- deaths
- crashes
- exact MMR
- team avatar or logo
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
- preserve pilot avatar, name, team tag or `Independent`, and one or two key stats
- keep login/avatar visible in top bar

## SEO and Sharing

The player directory should support:

- title: `Players - Ascent Rivals`
- description focused on public pilot profiles, teams, and career stats
- canonical URL

Do not expose exact AccelByte MMR, wallet state, private account state, or invite/request state in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- player-owned public social links
- social-link verification state
- public Twitch/live status
- future named-division filters only after an Eventun public-rank design and contract are approved
- team filters
- course specialty filters
- gauntlet participation filters
- region filters
- season filters
- recently active sorting
- public profile badges if backend/AccelByte exposes them safely

## Acceptance Criteria

- every source-classified real pilot with a usable public identity can appear regardless of match count or recency;
- only explicitly classified bot, test, or internal identities are excluded;
- the default directory order is alphabetical;
- name and team search, supported sorts, and display pagination/progressive reveal do not require additional network requests;
- the collection response contains only identity, search, card, and approved sort fields rather than full profile/history payloads;
- podium finishes and matches played remain secondary context rather than an implied player
  ranking;
- exact AccelByte MMR, any Website-derived division, wallet state, private team state, and account data never enter the public directory payload;
- a future public named division appears only after Eventun owns an explicitly approved stateful rank contract;
- team identity uses `[TAG] Team Name` where space permits, tag-only compact treatment, and `Independent` when unaffiliated;
- the pilot avatar is the card's only image, and arbitrary team foreground/background colors do not control tag legibility;
- missing avatars and teams use stable fallbacks without excluding the pilot;
- server pagination is not an initial requirement and is reconsidered from measured performance evidence.

## Open Questions

- Should player social links be unverified user-provided URLs, verified provider links, or both with a visible trust state?
- Should a logged-in player manage public socials on their own profile page, an account menu/settings page, or both?
- Should the directory support a `live now` Twitch indicator later, or should that live only on `/watch`?

## Next Steps

- Treat the reviewed desktop/mobile pilot-directory frames as the responsive implementation
  baseline.
- Review implementation-facing loading, empty, unavailable, search-empty, and partial-data states
  in the shared utility-state pass.
- Update [[player-profile]] when player-owned social-link fields become a real feature.
- Keep homepage search result requirements aligned with this directory's public player-card fields.
