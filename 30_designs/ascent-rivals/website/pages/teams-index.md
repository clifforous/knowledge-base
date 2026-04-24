# Ascent Rivals Teams Index Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[team-profile]]
- [[player-profile]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for the public team directory.

The teams index should help players and followers answer:

- which teams exist
- which teams are active or recruiting
- how large each roster is
- which team a player might want to inspect or join
- whether the logged-in player can create a team

## Route

Working route:

- `/teams`

Current app route equivalent:

- `/team`

Final route direction:

- use plural route groups in the Nuxt site
- preserve redirects from old singular routes if public links already exist

## Audience

Primary:

- players looking for a team
- followers browsing crews
- team managers checking team presentation

Secondary:

- sponsors
- tournament organizers
- press/community viewers

## Page Goals

- make teams feel like first-class public entities
- preserve fast search/filter behavior from the current app
- show enough roster and membership context to decide whether to open a team
- expose `Create Team` only when relevant
- avoid turning the directory into a management table
- leave room for future team stats without inventing unsupported aggregate data

## Current V1 Data Availability

### Team list

Available:

- team id
- name
- tag
- membership mode
- media
- players
- primary and secondary colors
- gate token policy ids

Source:

- `GET /v1/team`

### Team player summary

Available per team player:

- player id
- name
- avatar URL
- designation
- rank

Source:

- included in team list/detail responses

### Membership modes

Available:

- `open`
- `invite`
- `request`
- `token_gated`

Current labels:

- `Open To Join`
- `Invite Only`
- `Request To Join`
- `Token Gated`

### Create team

Available:

- create team metadata
- name
- tag
- membership mode
- primary/secondary colors
- media
- owner id

Source:

- `POST /v1/team`

V1 caution:

- eligibility to create a team is user/session dependent
- the directory should show the action only when the user is logged in and eligible

## V1 Page Structure

Default first-view priority:

1. directory header and search
2. team cards/list
3. logged-in create-team affordance
4. membership/recruiting filters

## 1. Directory Header

Purpose:

- establish the team directory as a crew registry

Content:

- title such as `Teams`
- short operational description
- total team count if useful
- `Create Team` action for eligible logged-in users

Tone examples:

- `Crew registry online`
- `Team signal acquired`
- `No crews registered`

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `CommandAction`

## 2. Search and Filters

Purpose:

- help users find teams quickly

V1 controls:

- search by team name
- optional search by tag
- membership mode filter
- active/inactive filter only if active state exists later

V1 caution:

- current UI supports fuzzy team-name search
- do not require advanced filters until the data supports them

## 3. Team Cards

Purpose:

- give enough identity to choose a team

Card content:

- team image/avatar
- team name
- team tag
- member count
- membership mode
- color accent from team colors
- token-gated indicator if relevant

Optional V1:

- small roster preview from first few members

V2:

- team trophies
- team gauntlet standings summary
- team medals
- recruiting status
- recent activity

Terminal Ops components:

- `EntityCard`
- `TeamTag`
- `RosterPreview`
- `StatusChip`

## 4. Create Team CTA

Visible when:

- user is logged in
- user is eligible to create a team

Placement:

- directory header or command action area
- not global top navigation

Design guidance:

- if the user is already on a team, do not foreground create-team actions
- if the user is anonymous, prefer `Sign in with Steam` over a disabled create button

## 5. Empty and Sparse States

Required states:

- no teams
- no teams matching search
- failed team list fetch
- media missing

Tone:

- `No teams registered.`
- `No crews match this query.`
- `Team registry unavailable.`

Guardrail:

- do not make a sparse team directory feel like a dead product
- if the list is small, cards can be larger and more identity-focused

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can browse/search teams and open public team profiles |
| Logged-in player without team | same plus create-team CTA if eligible and join/request actions after opening a team |
| Logged-in player on a team | same plus `My Team` context and no create-team emphasis |
| Admin | same plus future moderation/admin affordances only if needed |

## Responsive Behavior

Desktop:

- command header
- search/filter row
- responsive card grid

Tablet:

- reduce card columns
- keep search and membership filter reachable

Mobile:

- stack filters
- show compact team cards
- keep login/avatar visible in top bar
- preserve team name, tag, member count, and membership mode

## SEO and Sharing

The team directory should support:

- title: `Teams - Ascent Rivals`
- description focused on public teams, crews, and competitive roster discovery
- canonical URL

Do not expose private invite/request state in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- explicit recruiting/open roster flag separate from membership mode
- team stats aggregate
- team gauntlet standings
- team trophies and medals
- team recent activity
- sponsor relationships
- team search by member name
- team filters by region or competitive focus

## Open Questions

- Should anonymous users see a `Sign in to create team` CTA, or should create-team actions appear only after login?
- Should token-gated teams show token policy names/images in the directory, or only on the detail page?
- Should teams be sorted alphabetically, by member count, by recent activity, or by featured/manual ordering?
- Should `/teams` eventually include a `My Team` panel for logged-in users?

## Next Steps

- Use this spec with [[team-profile]] for the next team design pass.
- Decide whether the directory mock should show a sparse catalog or a fuller production-like catalog.
