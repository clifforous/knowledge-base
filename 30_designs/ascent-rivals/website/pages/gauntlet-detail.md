# Ascent Rivals Gauntlet Detail Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[gauntlets-index]]
- [[sponsors-index]]
- [[../../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]
- [[../../../../50_knowledge/ascent-rivals/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]

## Purpose

Define the IA and page requirements for a single gauntlet.

The page should behave like an event operations console: it explains the gauntlet, shows what phase is active, exposes standings and qualification state, and keeps prizes/sponsors visible without making the page feel like an admin form.

## Route

Working route:

- `/gauntlets/[id]`

Current app route equivalent:

- `/gauntlet/[id]`

Final route direction:

- use plural route groups in the Nuxt site
- preserve redirects from old singular routes if public links already exist

## Audience

Primary:

- players trying to qualify or track their status
- followers tracking standings and finals
- gauntlet creators/admins

Secondary:

- sponsors
- tournament organizers
- press/community viewers

## Page Goals

- make qualifier and finals/stage status clear
- keep personal logged-in status visible when relevant
- preserve standings, stats, sponsor display, prize flows, and admin actions from the current site
- support multiple gauntlet models without making early pages feel empty
- protect qualifier-versus-heat terminology
- provide a future landing surface for stream embeds when a tournament is broadcast

## Supported Gauntlet Models

The underlying model is generic. Presentation can adapt by type.

V1 should support:

- qualifier-only gauntlets that behave like matchmaking windows
- stage-only or bracket-only events
- traditional gauntlets with qualifiers plus finals/stages
- sponsored prize events

Later:

- invite-only events
- team tournaments
- richer bracket visualization
- season/circuit rollups

Design guardrail:

- avoid showing empty sections just because the generic model supports them
- show only the sections that apply, but keep the page-local nav stable enough that users can learn the page

## Current V1 Data Availability

### Gauntlet detail

Available:

- gauntlet id
- creator id
- title
- subtitle
- ticker
- primary and secondary colors
- scoring stat
- stat window
- stat top K
- first event time
- final event time
- region code
- qualifiers
- media
- sponsors
- stages

Source:

- `GET /v1/gauntlet/{gauntletId}`

### Overall standings

Available:

- ranking
- qualification points
- qualifiers played
- qualifiers counted
- matches played
- total and average circuit points
- player identity summary

Sources:

- `GET /v1/gauntlet/{gauntletId}/standings`
- `GET /v1/gauntlet/{gauntletId}/standings/player/{playerId}`

### Qualifier standings

Available:

- ranking
- best sequence points
- best sequence time
- matches played
- total and average circuit points
- player identity summary

Sources:

- `GET /v1/gauntlet/{gauntletId}/qualifier/{qualifierId}/standings`
- `GET /v1/gauntlet/{gauntletId}/qualifier/{qualifierId}/standings/player/{playerId}`

### Gauntlet stats

Available:

- player stats across the gauntlet
- kills/deaths/crashes/obelisks
- podiums
- matches
- circuit points
- credits
- stage wins/losses
- qualifier counts

Source:

- `GET /v1/gauntlet/{gauntletId}/stats`

### Recent gauntlet match summary

Available:

- most recent gauntlet match summary
- match standings
- heat array
- per-heat standings
- loadout objects on heat standings

Source:

- `GET /v1/match/summary/gauntlet/{gauntletId}/recent`

V1 caution:

- use recent match summary as a supporting module if useful
- do not confuse match-internal heats with gauntlet qualifiers

### Prize data

Available:

- prize configuration
- funding
- participation rewards
- distribution rows
- results
- payouts
- dust claim status and claim action

Sources:

- `GET /v1/admin/gauntlet/{gauntletId}/prize`
- `GET /v1/gauntlet/{gauntletId}/prize/dust/claim/status`
- `POST /v1/gauntlet/{gauntletId}/prize/dust/claim`

V1 caution:

- current prize model is mostly currency/item oriented
- presentation should leave room for future sponsored physical prizes without pretending the API already supports every prize type

### Stage operations

Available/admin-oriented:

- create stage session
- report stage results
- stage attempt concepts in the runtime contract

Sources:

- `POST /v1/admin/gauntlet/{gauntletId}/stage/{stage}/session`
- `POST /v1/admin/gauntlet/{gauntletId}/stage/{stage}/results`

V1 caution:

- stage operations are admin/creator surfaces, not public page clutter

## V1 Page Structure

Default first-view priority:

1. event identity and current operational status
2. active/upcoming qualifier or finals/stage state
3. logged-in personal status
4. standings entry points
5. sponsors and prizes

This respects the product priority that qualifiers and finals matter most while still giving the page enough identity to orient the user.

## 1. Gauntlet Briefing

Purpose:

- identify the event and summarize the current operational state

Content:

- title
- subtitle/ticker
- banner or square media
- status chip
- region
- first/final event time
- scoring summary
- sponsor strip
- prize indicator
- primary action to view active standings or qualifier

Tone examples:

- `Gauntlet Briefing`
- `Qualifier Window Open`
- `Final Stage Scheduled`
- `Event Concluded`

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `SponsorStrip`
- `CommandAction`

## 2. Personal Status Overlay

Only when the user is logged in.

Purpose:

- make the gauntlet personally actionable

V1 possible content:

- current overall rank
- current qualifier rank
- qualification points
- qualifiers played/counted
- qualification/final eligibility if endpoint/state supports it
- dust claim status if prize data supports it
- wallet-required warning for claims if needed

Sources:

- `GET /v1/gauntlet/{gauntletId}/standings/player/{playerId}`
- `GET /v1/gauntlet/{gauntletId}/qualifier/{qualifierId}/standings/player/{playerId}`
- `GET /v1/gauntlet/{gauntletId}/prize/dust/claim/status`

Design guidance:

- keep this near the top, but visually secondary to the event status
- do not expose another player's private status

## 3. Qualifier Windows

Purpose:

- show how qualification works and when players can make progress

Content:

- qualifier list
- start/end times
- active/upcoming/concluded state
- scoring rule summary
- best-sequence explanation if applicable
- link or local jump to qualifier standings

Terminology:

- use `Qualifier Window`
- do not call qualifiers heats
- a qualifier can span many sessions and many matches

## 4. Finals / Stages / Brackets

Purpose:

- show what happens after qualification

Content:

- stage/final list
- match time
- race mode
- entry requirement
- min/max competitors
- team/group constraints where available
- circuit courses
- laps and heats only as match runtime settings inside stages

Terminology:

- use `Stage`, `Final Stage`, or `Bracket` depending on data and product language
- use `Heat` only for match-internal runtime rounds in a stage match

V1 visual model:

- stage cards are acceptable
- bracket visualization is optional unless the stage model includes enough bracket data

## 5. Standings

Purpose:

- show current competitive order

Required views:

- overall standings
- qualifier standings

Useful columns:

- rank
- player
- points
- qualifiers counted
- qualifiers played
- matches

Qualifier-specific columns:

- rank
- player
- best sequence points
- matches played

Design guidance:

- standings should be easy to scan
- standings can live inside qualifier/final sections or behind page-local navigation
- do not make standings the only page identity

## 6. Sponsors

Purpose:

- make sponsor relationships visible and valuable

Content:

- sponsor logos/names
- sponsor tier if available
- sponsor profile links
- sponsor-specific prize callouts if supported

Placement:

- sponsor strip in briefing
- richer sponsor module lower on the page if there is enough content

## 7. Prize Manifest

Purpose:

- show rewards and claim/admin state

Public content:

- prize pool or reward summary
- distribution/placement rows
- participation rewards where public
- funding summary if public
- result/payout summary after completion if public

Logged-in content:

- claim eligibility
- claim action
- wallet requirement

Admin/creator content:

- setup prize
- add funding
- report results
- mark payouts planned/paid

Guardrail:

- do not overfit the design to only currency prizes
- leave room for sponsored hardware or showcase rewards as future presentation data

## 8. Watch / Broadcast

V1:

- optional module only if a YouTube/Twitch/VOD link exists

Later:

- embedded Twitch or YouTube stream
- live chat or lightweight interaction if product scope expands
- bounties/betting are future concepts, not V1 requirements

Placement:

- near finals/stages when live
- lower on the page or behind `Watch` section when only VODs exist

## 9. History / Past Winners

V1:

- optional if winner/result data exists

Later:

- past winners
- finals bracket archive
- VOD links
- event recap
- season/circuit context

## Permissioned Actions

### Edit Gauntlet

Visible when:

- user is the gauntlet creator and has the creator role, or
- user is an admin

Placement:

- in the gauntlet briefing action area
- not in global top navigation

### Delete Gauntlet

Visible only for authorized users.

Design guardrail:

- destructive actions should not be visually adjacent to primary public actions
- require confirmation

### Prize/Admin Actions

Visible only to authorized users.

Actions:

- setup prize
- add funding
- report results
- mark payout planned
- mark payout paid
- create stage session
- report stage results

Guardrail:

- keep admin actions near their relevant object
- do not turn the public page into an operations dashboard for anonymous users

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view briefing, qualifiers, stages/finals, standings, sponsors, public prizes, media |
| Logged-in player | same plus personal rank, qualification context, claim status, wallet warnings where supported |
| Gauntlet creator/admin | same plus edit, delete, prize, stage-session, and result actions |

## Empty / Loading / Error States

Required states:

- gauntlet not found
- no qualifiers
- no stages/finals
- no standings yet
- no sponsors
- no prize data
- failed standings fetch
- failed qualifier standings fetch
- failed prize fetch
- media missing

Tone:

- `No qualifier windows published.`
- `No final stage scheduled.`
- `Standings sync pending.`
- `Prize manifest unavailable.`

## Responsive Behavior

Desktop:

- briefing/status header
- local section navigation
- standings table with pagination
- stages and qualifiers as structured panels

Tablet:

- reduce metadata columns
- preserve event status, next time, and personal status

Mobile:

- stack modules
- keep login/avatar visible in top bar
- use compact cards for qualifier and stage details
- allow standings tables to horizontal-scroll or transform into rank cards
- keep destructive/admin actions behind menus

## SEO and Sharing

Public gauntlet pages should support:

- title: `{Gauntlet Title} - Ascent Rivals Gauntlet`
- description using subtitle/ticker and event timing
- Open Graph image from gauntlet media if available
- canonical URL

Do not expose private player-specific eligibility or claim data in metadata.

## Open Questions

- What data should determine whether a gauntlet is qualifier-only, stage-only, traditional, invite-only, or team-based in the UI?
- Should stage/final presentation use the word `Stage`, `Final`, or `Bracket` by default?
- Should prize details be public by default or partially hidden until results/claims are active?
- Should watch embeds appear directly on gauntlet detail pages before the dedicated `/watch` page ships?
- Which stage operations are phase-1 web requirements versus admin-only future tooling?

## Next Steps

- Ask Pencil for one active gauntlet detail mock and one sparse/upcoming gauntlet detail mock.
- Create a companion course leaderboard page spec.
- Decide how much stage/final bracket data Eventun must expose before bracket visualization becomes a V1 requirement.
