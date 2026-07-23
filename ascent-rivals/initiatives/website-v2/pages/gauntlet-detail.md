# Ascent Rivals Gauntlet Detail Page Spec

Date: 2026-04-13
Status: Approved public layout and public-detail contract direction; implementation remains open
Last reviewed: 2026-07-23
Design checkpoint: Active combined, sparse/upcoming, and active mobile calibrations reviewed
Contract alignment: T03 owner/slot terminology approved; affected visual annotations remain to be
revalidated

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

The page should behave like an event operations console: it explains the gauntlet, shows what phase
is active, exposes supported standings and qualification state, and can surface approved sponsor
identity when the optional projection exists without making the page feel like an admin form.

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
- preserve standings only through the approved owner-aware and scoring-aware public boundary;
  defer broad stats, sponsor display, and approved non-prize admin actions until their own
  projections or workflows are reviewed
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
- never collapse field owners, racer slots, occupied slots, admissions, and participants into one
  generic participant count.

## Current V1 Data Availability

### Public-detail contract checkpoint

The 2026-07-23 read-only audit rejects the broad legacy
`GET /v1/gauntlet/{gauntletId}` response as the Website V2 public boundary. It mixes visitor-facing
identity and structure with creator identity, raw scoring/authoring values, admission and runtime
policy, allowed-team configuration, arbitrary media metadata, sponsor tier, and an ambiguous
individual qualification count. Its handler also maps every database failure to `NotFound`;
sanitized `InvalidArgument`, `NotFound`, `Internal`, and `Unavailable` behavior is required, while
repairing the legacy mapping remains separate cleanup.

The approved direction is a compact domain-neutral
`GET /v1/public/gauntlet/{gauntlet_id}` projection containing:

- stable public identity, region, validated optional colors, and approved bounded gauntlet media;
- complete qualifier and stage occurrence facts;
- a presence-aware qualification model with explicit player/team ownership and a bounded scoring
  metric enum;
- visitor-facing stage race mode and entry category plus ordered circuit rows.

It explicitly excludes:

- current published field-owner count and racer-slot count;
- creator identity, generic participant count, raw authoring/admission/runtime fields, arbitrary
  media metadata, sponsor relationships, prize/reward data, and administrative evidence.

Resolve current field composition and counts from the current-field public read. Resolve historical
composition and counts only from the exact StageRun-field read. The public StageRun timeline must
replace clock-derived `Upcoming` and `Open` with a bounded factual status derived from persisted run
state. Website V2 derives schedule-relative presentation from occurrence facts and its own clock.

Existing overall and qualifier standings support only verified player-owned qualification models.
The Website may request them only when the public detail projection identifies player ownership and
a supported scoring metric. Team-owned qualification requires an owner-aware public standings
projection; otherwise omit standings. Do not assume `Circuit Points` for an unknown or unsupported
gauntlet configuration.

Sponsor display is optional follow-on work. The core detail route ships without sponsors when no
relationship-scoped public sponsor projection exists; it never reads the broad sponsor registry.

Eventun G03 field/runtime work was reviewed and committed as `cb79df3`, so the public-detail
implementation may proceed from that clean baseline. Generated-gateway route tests must prove that
the parameterized detail path cannot capture `/v1/public/gauntlet/discovery` or the more specific
field, StageRun, and result routes.

### Gauntlet detail

Legacy response fields currently available, but not approved as one public Website response:

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

Public-use boundary:

- the collection endpoint is suitable only when the public detail projection identifies a supported
  player-owned qualification model and recognized scoring metric;
- team-owned overall standings require an owner-aware public projection and remain omitted until
  that contract exists;
- an unspecified or unsupported scoring metric prevents the standings module from rendering rather
  than defaulting to Circuit Points.

### Stage configuration

Currently available on each gauntlet stage:

- numeric stage id and scheduled match time;
- entry requirement, required prior stage wins/losses, and group constraints;
- stage-level race mode;
- minimum and maximum competitors plus lobby bounds;
- ordered circuit matches;
- player/team allocation and allowed-team configuration;
- overflow, admission-priority, and roster-lock policy values.

Each circuit match currently contains a numeric match id, `course_code`, and optional lap and
heat counts. Resolve `course_code` against the published AccelByte course catalogue for public
display and retain the code as a fallback when no public display name is available.

Legacy source:

- `GET /v1/gauntlet/{gauntletId}`

Presentation and model dependencies:

- Eventun does not currently expose an authored stage title. A title is a planned model
  addition; until it exists, the numeric `Stage NN` label is the primary heading and the UI
  must not reserve an empty title region.
- Eventun currently exposes race mode on stages, not as a gauntlet-level default. Show a
  gauntlet-level mode only if that separate optional field is deliberately added; otherwise
  omit it rather than infer it from stages or qualifiers.
- A qualifier currently contains only its id, start time, and duration. It does not author a
  qualifier-specific race mode or participation type, so public qualifier modules omit those
  fields.
- Lobby bounds, overflow policy, admission priority, roster-lock rules, and raw allowed-team
  configuration are operator details unless a later public requirement gives them a clear
  player-facing meaning.
- Published field-owner count and racer-slot count are not stable stage-configuration fields. Read
  them from current-field or exact StageRun-field projections and preserve their distinct meanings.

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

Public-use boundary:

- the collection endpoint is suitable only when the public detail projection identifies a supported
  player-owned qualification model and recognized scoring metric;
- `best_sequence_time_seconds` is an achievement timestamp used in deterministic ordering, not a
  race-duration value;
- team-owned qualifier standings require an owner-aware public projection and remain omitted until
  that contract exists.

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

V1 caution:

- defer this broad response from the initial public detail implementation;
- do not expose credits, raw combat/objective totals, or unsupported scoring values through the
  public page merely because the legacy response contains them.

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

- defer the recent match summary from the initial public detail implementation
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
5. media, plus sponsor identity only when the optional follow-on projection exists

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
- optional sponsor strip only when the relationship-scoped follow-on projection exists
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
- optional authored stage title when the planned API field exists
- match time
- race mode
- entry requirement
- min/max competitors
- team/group constraints where available
- qualified player/team owner count or field-owner count only when the public projection supplies
  that exact meaning through the current-field or exact StageRun-field read
- racer-slot count separately when useful
- ordered circuit matches with a published course name or course-code fallback
- laps and heats only as optional match runtime settings inside stages

Terminology:

- use `Stage` as the general label for a scheduled non-bracket competition unit;
- use `Final` or `Final Stage` only when the competition explicitly identifies that stage as the deciding final;
- use `Bracket` only when a published bracket graph exists;
- do not infer a bracket merely from stage win/loss prerequisites;
- use `Heat` only for match-internal runtime rounds in a stage match
- label owner counts as `Qualified Players`, `Qualified Teams`, or `Field Owners` according to the
  returned owner composition; label capacity as `Racer Slots`

V1 visual model:

- use one consistent stage-panel grammar and label each stage's factual state separately;
- show the complete ordered circuit as open match rows within the stage panel rather than as nested cards;
- when a title exists, use a small `Stage NN` label and the title as the heading; otherwise promote `Stage NN` and collapse the unused title space;
- stack stage panels at natural height on mobile so different circuit lengths do not create artificial empty space;
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

### Accepted Result Ownership

Every accepted gauntlet result used by Website V2 has an explicit owner variant: player or team.

- render a player-owned result as an individual result;
- render a team-owned result as the team's result;
- when a player occupied a team-owned racer slot, keep personal participation and the team-owned
  result visually separate;
- do not label the team's placement as the occupying player's individual finish;
- preserve exact StageRun identity from the public projection rather than selecting or inferring a
  run in the browser;
- use `Final`, win, trophy, or medal only when explicit competition semantics provide that meaning.

Member participation without team-owned qualification or accepted-result evidence is a
`No team result` state, not a team placement.

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

- use a relationship-scoped public sponsor display projection only when the optional follow-on
  contract exists;
- sponsor display is not a dependency of canonical detail identity or the core route;
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
| Anonymous | can view briefing, qualifiers, stages/finals, supported standings, media, and optional approved sponsor identity |
| Logged-in player | same plus personal rank and qualification context where supported |
| Gauntlet creator/admin | same plus ordinary non-prize edit/delete actions; administrator-only bracket and runtime-repair tooling remains in the Eventun Extend App UI |

## Empty / Loading / Error States

Required states:

- gauntlet not found
- no qualifiers
- no stages/finals
- no standings yet
- no team-owned result despite member participation
- typed result module unavailable while schedule/detail remains available
- failed standings fetch
- failed qualifier standings fetch
- media missing

Tone:

- `No qualifier windows published.`
- `No final stage scheduled.`
- `Standings sync pending.`
- `No team result recorded.`

## Responsive Behavior

Desktop:

- briefing/status header
- local section navigation
- standings table or open rows with client-side pagination
- qualifiers as structured open rows and stages as consistent circuit panels

Tablet:

- reduce metadata columns
- preserve event status, next time, and personal status

Mobile:

- stack modules
- keep login/avatar visible in top bar
- use a labeled 44px section-jump control for the sections that exist
- consolidate the current qualifier into one operational module and use compact open rows for other qualifier windows
- stack variable-height stage panels and keep each ordered circuit legible
- transform qualifier standings into an open rank list rather than horizontal-scroll the desktop table; show a bounded first page and client-side pagination
- treat the signed-in personal-status inset as optional without leaving a gap
- retain a short four-node qualifier sequence horizontally when it fits at 390px; stack or simplify it at narrower widths rather than forcing overflow
- keep destructive/admin actions behind menus

## SEO and Sharing

Public gauntlet pages should support:

- title: `{Gauntlet Title} - Ascent Rivals Gauntlet`
- description using subtitle/ticker and event timing
- Open Graph image from gauntlet media if available
- canonical URL

Do not expose private player-specific eligibility data in metadata.

## Next Steps

- Use the reviewed active desktop, sparse/upcoming desktop, and active mobile frames as the gauntlet-detail implementation baseline.
- Add the planned stage-title field and decide whether an optional gauntlet/default race-mode field belongs in Eventun before relying on either value in implementation.
- Decide how much stage/final bracket data Eventun must expose before bracket visualization becomes a V1 requirement.
- Revalidate affected desktop/mobile field-count and accepted-result annotations against the typed
  owner contract; do not redesign the reviewed overall composition.
