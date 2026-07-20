# Ascent Rivals Team Profile Page Spec

Date: 2026-04-13
Status: Draft
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
- [[ascent-rivals/system/eventun/api|eventun-api]]
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
- include fact-backed team stats at Website V2 launch when the preceding team contracts support them, but keep them secondary and provisional
- keep individual pilots and links to their profiles prominent
- avoid presenting unsupported team aggregates as if they exist

## Current V1 Data Availability

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
- final roster presentation fields must be reviewed after T01/T02 implementation;
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

## V1 Page Structure

Default first-view priority:

1. team identity and membership status
2. relevant join/leave/manage action for the current user
3. roster and individual pilot profile links
4. fact-backed team performance context after the implemented contracts have been reviewed
5. gauntlet/trophy sections only when their ownership and result semantics are supported

The public profile uses readable section anchors, initially `Overview` and `Roster`, with `Stats`, `Gauntlets`, and `Trophies` added only when the post-team implementation supports those sections. The dedicated management route uses a section index for Team Info, Media, Roster, Invites, Join Requests, and Ownership/Disband. Do not use tabs to hide one long unsaved form; tabs are acceptable later only if the panels have independent loading, validation, and save behavior. Compact layouts use a labeled section jump menu.

## 1. Team Briefing

Purpose:

- establish team identity and current public state

Content:

- team hero/avatar
- team name
- team tag
- member count
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
- show `Sign in with Steam` or `Login to Join` when an open or request-based action becomes available after authentication.

Logged-in player without team:

- `Join Team` for `Open` teams;
- `Request to Join` for `Request to Join` teams;
- show `Invite Only` without a join/request action unless a valid invitation provides an `Accept Invite` action.

Logged-in player on this team:

- show own team status
- `Leave Team` if not the explicit owner
- management entry if manager/owner/admin

Logged-in player on another team:

- show already-on-team state
- do not show join/request action

Admin/manager:

- show `Manage Team`

Design guidance:

- show the same membership label to every audience; authentication and team state change the action, not the public description
- membership actions should live near the team briefing
- destructive actions such as leave/disband should be visually separated and confirmed

## 3. Roster

Purpose:

- make the crew visible and navigable

Content:

- player avatar
- player name
- approved public title after the replacement contract is reviewed
- competition rank when its implemented meaning is useful to viewers
- link to player profile

Interaction:

- sort by name
- sort by approved public title when useful
- sort by competition rank when available

Design guidance:

- roster should be the primary public data section in V1
- public titles can use in-world labels, but should remain understandable and must not imply authorization

Terminal Ops components:

- `DataTable`
- `PilotIdentityCell`
- `TeamDesignationPill`

## 4. Team Stats

Website V2 initial-release direction:

- include a concise fact-backed team performance section after the preceding Eventun team work is implemented and reviewed;
- keep the section below the roster and subordinate to individual pilot identity and performance;
- treat the exact metrics and visualization as provisional until the team feature has been used and iterated on;
- omit unsupported modules rather than approximating them from current-roster lifetime totals.

Reason:

- current team responses include roster and metadata, not team aggregate performance
- deriving team stats by fetching every current player career would misattribute historical results as well as create inefficient Website reads

Candidate content after contract review:

- pilot results attributed to the team at performance time
- current-roster leaderboard comparison that preserves each pilot's individual result
- team gauntlet standings only when the competition computes team results
- course strengths based on an approved team metric
- recent team-represented match/event history
- aggregate medals or trophies only when their team ownership semantics exist

Design guidance:

- do not let a speculative team score outrank the exact roster or individual pilot links
- distinguish `results earned while representing this team` from true team-format standings or wins
- re-evaluate placement and prominence after the team implementation has undergone product iteration

## 5. Gauntlet Results

V1 status:

- optional only if existing gauntlet data can associate team results safely

V2:

- team gauntlet history
- team finals placements
- invite-only/team tournament results
- trophy case

## 6. Trophies and Medals

V1 status:

- optional/empty unless reliable backend data exists

V2:

- team trophies for team finals
- event medals

Guardrail:

- do not fake official trophies or medals from incomplete data

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
| Anonymous | can view public team briefing and roster; can sign in to join if relevant |
| Logged-in player without team | can join `Open` teams, request `Request to Join` teams, or accept a valid invitation; `Invite Only` otherwise has no direct membership action |
| Logged-in player on another team | can view team but cannot join until leaving current team |
| Logged-in member | can view own team state and leave if not the explicit owner |
| Authorized manager/owner | can perform only the roster, invite, request, media, membership, capability, transfer, or disband actions explicitly allowed by Eventun |
| Admin | can access management actions where supported |

## Empty / Loading / Error States

Required states:

- team not found
- no roster members
- failed team fetch
- failed pending invites/requests fetch
- no pending invites
- no pending join requests
- media missing

Tone:

- `Team profile not found.`
- `Roster empty.`
- `Pending queue clear.`
- `Team registry sync failed.`

Guardrail:

- do not expose private invite/request errors to anonymous users

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
- keep destructive actions behind menus or confirmation flows

## SEO and Sharing

Public team pages should support:

- title: `{Team Name} [{Tag}] - Ascent Rivals Team`
- description using roster size and membership mode where appropriate
- Open Graph image from team media
- canonical URL

Do not expose pending invites, join requests, or private management state in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- team stats aggregate
- team gauntlet standings
- team trophies and medals
- team match history
- team course strengths
- team sponsor relationships
- recruiting message or team bio
- public social links
- region/time-zone fields
- explicit team activity status
- richer role permissions

## Open Questions

- Which implemented public titles and competition-rank fields should be shown after T01/T02 replaces the legacy designation model?
- What is the first source of truth for team trophies and team gauntlet standings?

## Next Steps

- Ask Pencil for one public team profile mock and one authorized management state mock.
- Reconcile the mock and exact statistics modules against the implemented T01-T03 contracts.
