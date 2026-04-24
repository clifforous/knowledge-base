# Ascent Rivals Team Profile Page Spec

Date: 2026-04-13
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[teams-index]]
- [[sponsors-index]]
- [[player-profile]]
- [[gauntlet-detail]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

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

- use plural route groups in the Nuxt site
- keep management affordances attached to the team context
- implementation can use a sub-route such as `/teams/[id]/manage`, but the public page should expose the entry point when authorized

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
- leave room for future team stats, trophies, medals, and gauntlet history
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
- gate token policy ids

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

Current designation names:

- `Prime`
- `Nexus`
- `Vector`
- `Echo`

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
- update token gate policies

Sources:

- `PUT /v1/team/{teamId}`
- `POST /v1/team/{teamId}/gate/token`
- `DELETE /v1/team/{teamId}/gate/token/{policyId}`

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
2. roster
3. relevant join/leave/manage action for the current user
4. future stats/gauntlet/trophy sections only if supported

## 1. Team Briefing

Purpose:

- establish team identity and current public state

Content:

- team hero/avatar
- team name
- team tag
- member count
- membership mode
- team colors as accent, not full-page takeover
- token-gated indicator if relevant

Tone examples:

- `Crew profile`
- `Roster signal acquired`
- `Membership gate active`

Terminal Ops components:

- `HeroBriefing`
- `TeamTag`
- `StatusTelemetryBar`
- `CommandAction`

## 2. Membership Status and Actions

Purpose:

- show what the current user can do

Anonymous:

- show `Sign in with Steam` or `Login to Join` if joining is plausible

Logged-in player without team:

- `Join Team` for open teams
- `Request to Join` for request teams
- wallet/token guidance for token-gated teams
- no join action for invite-only teams unless invited state is available and applicable

Logged-in player on this team:

- show own team status
- `Leave Team` if not Prime
- management entry if manager/owner/admin

Logged-in player on another team:

- show already-on-team state
- do not show join/request action

Admin/manager:

- show `Manage Team`

Design guidance:

- membership actions should live near the team briefing
- destructive actions such as leave/disband should be visually separated and confirmed

## 3. Token Gate Notice

Only for token-gated teams.

Purpose:

- explain wallet/token requirements clearly

Content:

- required token policy ids
- token names/images if token metadata is available
- wallet connection status for logged-in users
- link to wallet connection

Tone examples:

- `Wallet token required`
- `Gate token not detected`

Guardrail:

- do not make token-gated membership look like pay-to-win
- describe it as access control, not competitive advantage

## 4. Roster

Purpose:

- make the crew visible and navigable

Content:

- player avatar
- player name
- designation
- rank
- link to player profile

Interaction:

- sort by name
- sort by designation
- sort by rank

Design guidance:

- roster should be the primary public data section in V1
- designations can use in-world labels, but should remain understandable

Terminal Ops components:

- `DataTable`
- `PilotIdentityCell`
- `TeamDesignationPill`

## 5. Team Stats

V1 status:

- placeholder or omitted unless supported by reliable data

Reason:

- current team responses include roster and metadata, not team aggregate performance
- deriving team stats by fetching every player career would be expensive and potentially misleading

V2 candidate content:

- team gauntlet standings
- aggregate medals
- trophies from team-based finals
- course strengths across members
- team podiums
- team recent match/event history

Design guidance:

- leave room for this section in mocks
- do not invent numbers for V1 implementation specs

## 6. Gauntlet Results

V1 status:

- optional only if existing gauntlet data can associate team results safely

V2:

- team gauntlet history
- team finals placements
- invite-only/team tournament results
- trophy case

## 7. Trophies and Medals

V1 status:

- optional/empty unless reliable backend data exists

V2:

- team trophies for team finals
- event medals
- historical prize placements

Guardrail:

- do not fake official trophies or medals from incomplete data

## 8. Manage Team

Visible when:

- logged-in user is admin
- logged-in user is on this team with manager/owner designation

Current manager/owner model:

- `Prime` and `Nexus` are management roles in current UI logic
- admins can manage regardless of membership

Management areas:

- team info
- media
- roster
- invites
- join requests
- token gates
- ownership transfer
- disband/delete

Implementation note:

- management can be a page-local section, modal workflow, or `/teams/[id]/manage` sub-route
- it should remain visibly attached to the team profile, not treated as a separate admin product

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

- member designation
- member rank
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

- owner/Prime-only actions must be clearly separated from routine roster management
- disband is destructive and must require strong confirmation

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view public team briefing and roster; can sign in to join if relevant |
| Logged-in player without team | can join open teams, request request-based teams, or see wallet/token guidance for token-gated teams |
| Logged-in player on another team | can view team but cannot join until leaving current team |
| Logged-in member | can view own team state and leave if not Prime |
| Manager/Prime | can manage roster, invites, requests, media, membership mode, colors, and ownership/disband where allowed |
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
- token metadata unavailable

Tone:

- `Team profile not found.`
- `Roster empty.`
- `Pending queue clear.`
- `Team registry sync failed.`
- `Gate token metadata unavailable.`

Guardrail:

- do not expose private invite/request errors to anonymous users

## Responsive Behavior

Desktop:

- hero/status area with action rail
- roster table
- management sections as tabs or panels

Tablet:

- stack hero/media and action rail
- preserve roster name/designation/rank

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

- Should management be a page-local section or a dedicated `/teams/[id]/manage` route in the Nuxt app?
- Should the public page show membership mode for all teams, or only if the user can act on it?
- Should team rank mean in-team ordering, competitive team ranking, or both?
- Should `Prime`, `Nexus`, `Vector`, and `Echo` remain public labels, or should we add plain-language helper text?
- What is the first source of truth for team trophies and team gauntlet standings?

## Next Steps

- Ask Pencil for one public team profile mock and one authorized management state mock.
- Create companion sponsor page spec.
- Create user-flow specs for team join request, invite accept/deny, roster management, and ownership/disband flows.
