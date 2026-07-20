# Ascent Rivals Gauntlet Detail Page Spec

Date: 2026-04-13
Status: Draft
Last reviewed: 2026-07-20

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../flows/gauntlet-authoring]]
- [[gauntlets-index]]
- [[../sponsor-administration-handoff]]
- [[ascent-rivals/system/competition-runtime-terms|competition-runtime-terms]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[ascent-rivals/system/eventun/gauntlet-stage-runtime-contract|gauntlet-stage-runtime-contract]]

## Purpose

Define the IA and page requirements for a single gauntlet.

The page should behave like an event operations console: it explains the gauntlet, shows what phase is active, exposes standings and qualification state, and keeps sponsors visible without making the page feel like an admin form.

## Route

Working route:

- `/gauntlets/[id]`

Current app route equivalent:

- `/gauntlet/[id]`

Final route direction:

- use plural route groups in Website V2
- allow old singular routes to retire without redirects unless later measured inbound use justifies an exact mapping

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
- preserve standings, stats, sponsor display, and approved non-prize admin actions from the current site
- support multiple gauntlet models without making early pages feel empty
- protect qualifier-versus-heat terminology

## Supported Gauntlet Models

The underlying model is generic. Presentation can adapt by type.

V1 should support:

- qualifier-only gauntlets that behave like matchmaking windows
- stage-only or bracket-only events
- traditional gauntlets with qualifiers plus finals/stages
- sponsored events

Later:

- invite-only events
- team tournaments
- richer bracket visualization
- season/circuit rollups

Design guardrail:

- avoid showing empty sections just because the generic model supports them
- show only the sections that apply, but keep the page-local nav stable enough that users can learn the page

### Prize and Reward Boundary

Prize and reward data is Accountun-related and is entirely deferred from Website V2.

- do not request or display prize pools, reward descriptions, distribution rows, funding, claims, payouts, or wallet requirements;
- do not expose prize or reward state in public metadata, personalized overlays, gauntlet administration, or sponsor modules;
- do not add Website V2 links into legacy prize/reward workflows during the initial release;
- a related code-authored `/events/[slug]` page may contain verified promotional prize copy, but `/gauntlets/[id]` remains free of Accountun-driven prize modules and state;
- revisit the complete product and system boundary later rather than preserving a partial presentation.

### Composition and State Rules

Qualifiers and stages are independent optional parts of a gauntlet. The page must derive its composition from the actual gauntlet data rather than assume a fixed qualifier-to-final funnel.

- a qualifier-only gauntlet shows qualifier scheduling, scoring, standings, and its concluded result without an empty finals section;
- a stage-only gauntlet leads with the next or current stage and never invents qualification status;
- a gauntlet with both follows the currently relevant qualifier, between-phase, or stage state;
- a bracket-backed gauntlet shows the published graph and match state when the bracket read contract exists;
- if neither qualifiers nor stages exist, render only the factual briefing and available actions or results, and treat the missing competition structure as a sparse/data-quality state rather than fabricating sections.

State-specific priority means changing emphasis, not creating separate page types:

- upcoming: show the next applicable qualifier or stage schedule, entry requirements, and format;
- active qualifier: show that qualifier's remaining time, standings, and personal position where available;
- between qualification and a stage: show the resolved or provisional field and the next scheduled stage where supported;
- active stage or bracket: show the current stage/match, current results, and advancement state;
- completed: show the authoritative final result for the composition that actually ran.

Website contract guidance:

- a server-provided current phase/component is preferable once bracket and stage-run state becomes richer;
- if Website V2 derives state from timestamps and arrays initially, keep the algorithm centralized and test qualifier-only, stage-only, combined, sparse, and exact-boundary cases;
- do not use `live` unless a reliable backend state supports it.

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

### Stage operations

Available/admin-oriented:

- create stage session
- report stage results
- stage attempt concepts in the runtime contract

Sources:

- `POST /v1/admin/gauntlet/{gauntletId}/stage/{stage}/session`
- `POST /v1/admin/gauntlet/{gauntletId}/stage/{stage}/results`

V1 caution:

- stage operations are operator surfaces, not public page clutter;
- defer the hosting and permission boundary for stage-session creation, result submission/repair, and related runtime controls until the initial bracket implementation clarifies the operator workflow;
- this deferral does not change the Website V2 requirement to preserve ordinary non-prize gauntlet creation, editing, and deletion.

## V1 Page Structure

Default first-view priority:

1. event identity and current operational status
2. the active or next applicable qualifier, stage, or bracket state
3. logged-in personal status
4. standings or results that exist for the gauntlet's actual composition
5. sponsors and media

This respects the product priority that qualifiers and finals matter most while still giving the page enough identity to orient the user.

Use readable in-page anchors for the gauntlet's long public document. `Overview` is always present; add `Qualifiers`, `Stages`, `Bracket`, `Standings` or `Results`, and `Sponsors` only when the corresponding structure or approved identity actually exists. Do not render empty navigation destinations to preserve a universal template. On compact layouts, use a labeled section jump menu. Command-like Terminal Ops copy may accompany the controls visually but cannot replace these plain-language labels.

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

Sources:

- `GET /v1/gauntlet/{gauntletId}/standings/player/{playerId}`
- `GET /v1/gauntlet/{gauntletId}/qualifier/{qualifierId}/standings/player/{playerId}`

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

- use `Stage` as the general label for a scheduled non-bracket competition unit;
- use `Final` or `Final Stage` only when the competition explicitly identifies that stage as the deciding final;
- use `Bracket` only when a published bracket graph exists;
- do not infer a bracket merely from stage win/loss prerequisites;
- use `Heat` only for match-internal runtime rounds in a stage match

V1 visual model:

- stage cards are acceptable
- bracket visualization is optional unless the stage model includes enough bracket data

## 5. Standings

Purpose:

- show current competitive order

Required when applicable:

- overall standings when the competition read returns them
- qualifier standings only when qualifiers exist

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

- approved sponsor logos/names for this gauntlet
- no public relationship-tier or billboard-placement data
- no links to Eventun Extend App sponsor operations or any nonexistent Website sponsor profile route

Placement:

- sponsor strip in briefing
- richer sponsor module lower on the page if there is enough content

Data boundary:

- use the approved sponsor display projection embedded in or composed for the public gauntlet response;
- do not fetch unrestricted sponsor records through public list/detail endpoints;
- tier remains gauntlet-specific operational data that may influence in-game advertising placement;
- direct gauntlet `Billboard` media, including tileable artwork, does not establish a named sponsor relationship and must not generate this module by itself;
- omit the sponsor section when there is no explicit approved sponsor identity to present.

## Deferred Watch / Broadcast

Current operational reality:

- a shoutcaster launches the game, joins as a spectator, and streams the running client through their own Twitch channel;
- Eventun and Website V2 do not currently own a canonical broadcaster assignment, stream URL, or trustworthy live-status signal;
- this is a user-operated broadcast workflow, not a first-party gauntlet stream service.

Initial Website V2 boundary:

- do not add a gauntlet broadcast module or `/watch` route;
- do not discover, embed, or label personal streams automatically;
- a code-authored editorial event page may include a manually verified Twitch, YouTube, or later VOD link when organizers deliberately provide one;
- revisit gauntlet streaming only after broadcaster authorization, spectator admission, stream registration, status, moderation, and ownership are designed.

## 7. History / Past Winners

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

### Stage/Admin Actions

Initial hosting boundary: administrator-only bracket mutation and runtime repair actions live in the Eventun Extend App UI. Website V2 renders the published bracket graph and public match state when those contracts ship, but ordinary core gauntlet creators do not receive AdminService access through the public page.

Candidate operations:

- create stage session
- submit or repair stage results
- resolve runtime failures where an explicit operator action exists

Guardrail:

- these controls remain restricted operator tooling in the initial Extend App UI boundary;
- do not assume they belong on Website V2 merely because the public gauntlet page displays stage state;
- do not turn the public page into an operations dashboard.

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view briefing, qualifiers, stages/finals, standings, sponsors, and media |
| Logged-in player | same plus personal rank and qualification context where supported |
| Gauntlet creator/admin | same plus ordinary non-prize edit/delete actions; administrator-only bracket and runtime-repair tooling remains in the Eventun Extend App UI |

## Empty / Loading / Error States

Required states:

- gauntlet not found
- no qualifiers
- no stages/finals
- no standings yet
- no sponsors
- failed standings fetch
- failed qualifier standings fetch
- media missing

Tone:

- `No qualifier windows published.`
- `No final stage scheduled.`
- `Standings sync pending.`

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

Do not expose private player-specific eligibility data in metadata.

## Next Steps

- Review the active-gauntlet desktop calibration already created in the live Pencil workfile.
- Create one sparse/upcoming calibration after the active composition is accepted.
- Decide how much stage/final bracket data Eventun must expose before bracket visualization becomes a V1 requirement.
