# Ascent Rivals Team Profile Page Spec

Date: 2026-04-13
Status: Approved public T03 read/presentation contract; management details remain draft;
desktop/mobile visual calibration pending
Last reviewed: 2026-07-22
Analytics priority confirmed: 2026-07-15 — individual pilots, their profiles, and the roster remain more prominent than team aggregates until the implemented team feature has been reviewed through real iteration.

Membership direction confirmed: 2026-07-15. The stable public concepts are `Open`, `Request to Join`, and `Invite Only`. Exact backend enum names remain subject to the new team implementation. Token-gated membership is not part of Website V2.

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../route-api-matrix]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../flows/team-lifecycle]]
- [[teams-index]]
- [[../sponsor-administration-handoff]]
- [[player-profile]]
- [[gauntlet-detail]]
- [[ascent-rivals/system/eventun/interface-architecture|eventun-interface-architecture]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for a public team profile with authenticated team-management overlays.

The team profile should be both:

- a public destination for a team/crew
- the natural home for join, leave, invite, request, roster, media, role, and ownership workflows

The page should not feel like a hidden admin console, but it must preserve all current team workflows.

## Route

Working route:

- `/teams/[id]`

Current app route equivalent:

- `/team/[id]`
- `/team/[id]/manage`

Final route direction:

- use plural route groups in Website V2;
- use `/teams/[id]` for the public profile, roster, membership state, join/request/leave actions, and public performance context;
- use `/teams/[id]/manage` for metadata, media, roster administration, invitations, join requests, ownership transfer, and disbanding;
- expose a contextual `Manage Team` action on the public profile when the current user is authorized.

## Audience

Primary:

- team members
- team managers/owners
- players looking to join
- followers of a team

Secondary:

- sponsors
- tournament organizers
- press/community viewers

## Page Goals

- make a team identifiable and worth following
- show roster clearly
- preserve current join, leave, invite, request, and management flows
- expose membership rules without confusing players
- keep management actions near the relevant team object
- include the approved T03 performance modules at Website V2 launch after implementation review,
  while keeping their visual prominence provisional and secondary
- do not invent browser-side team aggregates
- keep individual pilots and links to their profiles prominent
- avoid presenting represented individual performance as a team win, podium, rating, trophy, or medal

## Current-System Reference

The following legacy operations explain the current Ascentun surface but are not the Website V2
public contract. The committed local Team Core replacement separates compact list, team detail,
exact membership action, and management data; coordinated deployment remains unfinished. See
[[ascent-rivals/system/team-gauntlet-current-state|current team and gauntlet behavior]].

### Team detail

Available:

- team id
- name
- tag
- membership mode
- media
- players
- primary and secondary colors

Source:

- `GET /v1/team/{teamId}`

### Roster

Available per player:

- player id
- name
- avatar URL
- designation
- rank

Source:

- included in `GET /v1/team/{teamId}`

Legacy reference designation names:

- `Prime`
- `Nexus`
- `Vector`
- `Echo`

Replacement-contract direction:

- explicit ownership, public title, effective capability, and competition rank are distinct;
- the approved public roster exposes identity, name, avatar, explicit owner treatment, approved
  public title, and optional competition rank;
- visible titles and rank never authorize Website actions.

### Pending invites and requests

Available:

- invited players
- requesting players
- pending player id
- name
- avatar URL
- expiration time

Source:

- `GET /v1/team/{teamId}/pending`

V1 caution:

- pending invite/request state is permissioned management data
- do not show pending users publicly unless product decides those queues are public, which is not the current direction

### Membership actions

Available:

- join team
- request to join team
- leave team
- cancel/deny pending invite or request
- accept join request

Sources:

- `POST /v1/team/{teamId}/player/{playerId}`
- `DELETE /v1/team/{teamId}/player/{playerId}`
- `DELETE /v1/team/{teamId}/player/{playerId}/pending`

### Roster management

Available:

- update member rank
- update member designation
- remove member

Sources:

- `PUT /v1/team/{teamId}/player/{playerId}/rank`
- `PUT /v1/team/{teamId}/player/{playerId}/designation/{designation}`
- `DELETE /v1/team/{teamId}/player/{playerId}`

### Team metadata management

Available:

- update name
- update tag
- update membership mode
- update primary/secondary colors
- update media

Sources:

- `PUT /v1/team/{teamId}`

### Ownership / disband

Available:

- Prime abdication
- ownership transfer
- disband if no replacement is specified
- team delete

Sources:

- `POST /v1/team/{teamId}/abdicate`
- `DELETE /v1/team/{teamId}`

## Approved T03 Public Read Contract

Website V2 designs against reusable Eventun projections, not the broad management response.

### Public identity and active roster

The public detail contains team identity, public name/tag, membership mode, colors, bounded media,
status, and the complete active roster at the expected maximum of 16 members. Each roster row may
contain only:

- player identity;
- public player name;
- public avatar;
- explicit owner treatment;
- approved public presentation title;
- optional competition rank.

The public response excludes management capabilities, membership-interval identities, roster
revisions, pending-action versions, and audit/correction evidence. A player may hide optional team
badges or cosmetics on other presentation surfaces, but the canonical roster on the team's own
profile remains complete.

### Authenticated viewer state

One private Eventun response supplies the viewer's relationship, exact applicable unexpired action
reference, and explicit allowed transition. The page renders only the returned state:

- join;
- request to join;
- cancel request;
- accept invitation;
- decline invitation;
- leave;
- manage;
- already on another team;
- no available action.

Membership mode remains a public description and is never sufficient to infer one of these actions.
Management capabilities and pending queues use separate authorized reads.

### Independent performance modules

The public profile may compose four independent modules below the roster:

1. represented-performance summary;
2. current-roster leaderboard comparison;
3. recent represented results;
4. team gauntlet history.

Each module has its own loading, empty, unavailable, and freshness state. One failed module does not
replace the public identity or roster.

## V1 Page Structure

Default first-view priority:

1. team identity and membership status
2. relevant join/leave/manage action for the current user
3. roster and individual pilot profile links
4. represented-performance and current-roster comparison
5. recent represented results and team-owned gauntlet history when available

The public profile uses readable anchors for `Overview`, `Roster`, `Performance`, and `Gauntlets`,
omitting destinations whose module is unavailable or inapplicable. Do not add a `Trophies` anchor
without explicit trophy semantics. The dedicated management route uses a section index for Team
Info, Media, Roster, Invites, Join Requests, and Ownership/Disband. Do not use tabs to hide one long
unsaved form; tabs are acceptable later only if the panels have independent loading, validation,
and save behavior. Compact layouts use a labeled section jump menu.

## 1. Team Briefing

Purpose:

- establish team identity and current public state

Content:

- team hero/avatar
- team name
- team tag
- active member count
- public membership mode: `Open`, `Request to Join`, or `Invite Only`
- team colors as accent, not full-page takeover

Tone examples:

- `Crew profile`
- `Roster signal acquired`
- `Membership: Invite Only`

Terminal Ops components:

- `HeroBriefing`
- `TeamTag`
- `StatusTelemetryBar`
- `CommandAction`

## 2. Membership Status and Actions

Purpose:

- show what the current user can do

Anonymous:

- always show the public membership mode;
- use the shared `Sign In` control without promising a join outcome before Eventun evaluates the
  authenticated viewer.

Authenticated viewer:

- render only the authoritative viewer state returned by Eventun: `Join Team`, `Request to Join`,
  `Cancel Request`, `Accept Invitation`, `Decline Invitation`, `Leave Team`, `Manage Team`, already
  on another team, or no available action;
- preserve an explicit no-action state rather than manufacturing a disabled action;
- use the exact pending-action reference supplied by the private response for cancellation or
  invitation resolution;
- confirm destructive actions such as leaving.

Design guidance:

- show the same membership label to every audience; authentication and team state change the action, not the public description
- membership actions should live near the team briefing
- destructive actions such as leave/disband should be visually separated and confirmed
- do not infer an action from membership mode, roster membership, owner styling, public title,
  competition rank, or cached browser assumptions

## 3. Roster

Purpose:

- make the crew visible and navigable

Content:

- player avatar
- player name
- explicit owner marker/treatment for the owner row
- approved public title
- optional competition rank when present
- link to player profile

Interaction:

- keep the complete active roster visible, including members without competition rank;
- default to the authoritative roster order if Eventun supplies one, otherwise use a stable
  presentation order with the owner clearly identified;
- optional local sorting must not hide unranked members or imply management precedence.

Design guidance:

- roster should be the primary public data section in V1
- public titles can use in-world labels, but should remain understandable and must not imply authorization
- do not expose capability, membership-interval, revision, pending-action, audit, or correction data

Terminal Ops components:

- `DataTable`
- `PilotIdentityCell`
- `TeamDesignationPill`

## 4. Team Stats

Website V2 initial-release direction:

- include the approved concise fact-backed team performance section after T03 is implemented and
  reviewed;
- keep the section below the roster and subordinate to individual pilot identity and performance;
- treat visualization and prominence as provisional even though the response semantics are fixed;
- omit unsupported modules rather than approximating them from current-roster lifetime totals.

Reason:

- current team responses include roster and metadata, not team aggregate performance
- deriving team stats by fetching every current player career would misattribute historical results as well as create inefficient Website reads

### 4.1 Represented-Performance Summary

Show:

- distinct matches represented;
- player-match results;
- individual podium finishes;
- individual ascensions;
- latest represented result time.

These facts count individual results earned while a player represented the team at canonical
MatchStart. Label them `Represented Performance` or equally explicit copy. Do not label them team
wins, team podiums, a team rating, trophies, or medals.

### 4.2 Current-Roster Leaderboard Comparison

Show:

- selected published course and record category;
- the complete current roster;
- each ranked player's global rank and exact result;
- an explicit `Unranked` state for every roster member without a qualifying result;
- optional loadout value only when it belongs to the selected public leaderboard category.

This is a roster comparison over individual global records. It does not create an aggregate team
rank, score, course strength, or average. The course/category selection is local, shareable only if
the route contract deliberately adopts query state, and must not drop unranked rows.

### 4.3 Recent Represented Results

Show a bounded newest-first collection containing, where present:

- player;
- course;
- race mode;
- result time;
- placement;
- circuit points;
- podium;
- ascension.

Every row was earned while that player represented this team at MatchStart. Missing placement,
circuit points, podium, or ascension remains different from zero or false.

### 4.4 Team Gauntlet History

Show only qualification or accepted-result evidence whose typed owner is the team. Member
participation by itself does not create a team result. When a player occupies a team-owned racer
slot, show the player's participation and the team's owned result as separate facts.

Use `Stage NN` or another factual competition label. Use `Final`, win, trophy, or medal only when
explicit competition semantics provide that meaning.

Course strengths, trend charts, team ratings, aggregate medals, and trophies remain deferred until
their metric or ownership semantics are approved.

Design guidance:

- do not let a speculative team score outrank the exact roster or individual pilot links
- distinguish `results earned while representing this team` from true team-format standings or wins
- re-evaluate placement and prominence after the team implementation has undergone product iteration

## 5. Gauntlet Results

Initial status:

- use the owner-aware team gauntlet history defined above;
- present an explicit no-team-result state when members participated but no qualification or
  accepted result is owned by the team;
- omit the module when the read is unavailable without suppressing the identity, roster, or other
  performance modules.

## 6. Trophies and Medals

Deferred. Do not derive trophies or medals from represented podiums, stage placement, member
participation, or generic accepted results. Add the section only after a competition contract owns
the exact meaning.

## 7. Manage Team

Visible when:

- the authenticated Eventun action-state response allows team management for this user and team

Current manager/owner model:

- `Prime` and `Nexus` are legacy presentation/designation inputs in the current UI logic;
- the replacement model uses explicit ownership and effective capabilities from Eventun;
- administrators may override only where the implemented Eventun policy allows it.

Authorization guardrail:

- use Eventun's explicit allowed action/effective capability response to render management entry and controls;
- do not infer permission from public title, competition rank, roster order, or a legacy numeric designation;
- every mutation is authorized again by Eventun.

Management areas:

- team info
- media
- roster
- invites
- join requests
- ownership transfer
- disband/delete

Route decision:

- use the dedicated `/teams/[id]/manage` route;
- keep ordinary join, request, leave, and membership-status actions on `/teams/[id]`;
- link back to the public profile and preserve the team identity/chassis so management does not feel like a disconnected admin product;
- do not expose management navigation to unauthorized or anonymous users;
- use explicit confirmation for ownership transfer, disband, and other destructive operations.

## Team Management Details

### Team Info

Editable:

- name
- tag
- membership mode
- primary color
- secondary color

### Media

Editable:

- team avatar
- square hero
- banner hero
- other configured media purposes

### Roster Management

Editable:

- member public title where permitted
- member competition rank where permitted
- delegated capabilities where permitted
- remove member
- promote member
- demote member

Guardrail:

- managers should only see actions they are allowed to perform
- destructive member removal should require confirmation or clear affordance

### Invites

Actions:

- invite player
- cancel pending invite

Data:

- invited player
- expiration

### Join Requests

Actions:

- accept request
- deny request

Data:

- requesting player
- expiration

### Ownership / Disband

Actions:

- transfer ownership
- abdicate
- disband

Guardrail:

- owner-only actions must be clearly separated from routine roster management
- disband is destructive and must require strong confirmation

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | Can view public identity, complete active roster, and available public performance modules. |
| Authenticated viewer | Receives one authoritative relationship/action state from Eventun; the page renders no inferred transition. |
| Already on another team | Can view the full public profile; receives the explicit relationship state without join/request controls. |
| Current member | Can view the full public profile; leave or manage appears only when explicitly allowed. |
| Authorized manager/owner/admin | Can enter management only when Eventun returns `manage`; management reads and mutations reauthorize separately. |

## Empty / Loading / Error States

Required states:

- team not found
- sparse but complete roster
- failed public team/roster fetch
- represented-performance summary unavailable
- current-roster comparison unavailable
- current-roster comparison with ranked and explicit unranked members
- recent represented results unavailable or empty
- team gauntlet history unavailable
- no team-owned gauntlet result despite member participation
- viewer state unavailable without leaking relationship or pending-action detail
- failed pending invites/requests fetch
- no pending invites
- no pending join requests
- media missing

Tone:

- `Team profile not found.`
- `No represented results yet.`
- `No team-owned gauntlet result recorded.`
- `Pending queue clear.`
- `Team registry sync failed.`

Guardrail:

- do not expose private invite/request errors to anonymous users
- optional performance failure does not replace the public team identity or roster

## Responsive Behavior

Desktop:

- hero/status area with action rail
- roster table
- dedicated management route with sections or tabs for authorized users

Tablet:

- stack hero/media and action rail
- preserve roster name and any approved public-title/competition-rank fields

Mobile:

- stack modules
- keep login/avatar visible in top bar
- convert roster table to compact player rows if needed
- keep join/manage actions visible near top
- retain explicit owner treatment and unranked leaderboard rows
- allow independently unavailable performance modules to collapse without residual gaps
- keep destructive actions behind menus or confirmation flows

## SEO and Sharing

Public team pages should support:

- title: `{Team Name} [{Tag}] - Ascent Rivals Team`
- description using roster size and membership mode where appropriate
- Open Graph image from team media
- canonical URL

Do not expose pending invites, join requests, or private management state in metadata.

## Deferred Data Needs

These ideas are valuable but should not block V1:

- explicit team-format score or standings beyond the approved owner-aware history
- team trophies and medals
- aggregate team course strengths
- team sponsor relationships
- recruiting message or team bio
- public social links
- region/time-zone fields
- explicit team activity status
- richer public role presentation

## Open Questions

- Which approved public titles and competition-rank values should appear in the initial roster
  presentation rather than remain optional response fields?
- Should the initial represented-performance summary use only numeric facts or one restrained
  visualization after populated data can be reviewed?

## Next Steps

- Update the desktop and mobile public-profile specimens against the approved T03 semantics.
- Include populated, sparse-roster, unranked-comparison, independently unavailable-module, and
  no-team-result states.
- Keep the management design separate; this checkpoint does not redesign forms or management
  contracts.
- Revalidate exact fields, populated values, and failure behavior after T03 implementation.
