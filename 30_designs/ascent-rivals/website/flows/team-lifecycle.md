# Ascent Rivals Team Lifecycle User Flows

Date: 2026-04-21
Status: Draft

## Related
- [[authentication]]
- [[wallet-linking]]
- [[../unified-design]]
- [[../information-architecture]]
- [[../design-doc-roadmap]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../pages/teams-index]]
- [[../pages/team-profile]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the V1 team lifecycle flows for the unified Ascent Rivals website.

This note covers:

- team creation
- public team discovery and action states
- join team
- request to join
- cancel join request
- invite player
- accept or decline invite
- leave team
- manage team
- update team identity and membership mode
- token-gated team eligibility
- roster management
- ownership transfer
- disband team

This is a combined domain flow spec because team creation, membership, invites, and management all converge on the same public team profile and management context.

## Implementation Target

The new implementation target is a separate Nuxt/Vue/Reka UI project.

The current `ascentun` app is a behavior and API reference only.

Do not copy Next.js/shadcn implementation details directly unless the behavior still makes sense in the new Nuxt site.

## Product Decisions

Teams are public entities.

Team workflows should stay attached to the public team context rather than feeling like a disconnected admin tool.

V1 team lifecycle should support:

- discovering teams publicly
- creating a team when eligible
- joining or requesting to join from the team profile
- invite-only teams through explicit invite acceptance
- token-gated teams through wallet-aware eligibility
- manager and owner actions on the team profile or a team-scoped manage route

Private team state should be layered into the team experience, not moved into a separate product shell.

## Current Ascentun Reference Notes

Current implementation files are spread across:

- public team pages under `/team` and `/team/[id]`
- protected team pages under `/team/create` and `/team/[id]/manage`
- team actions in `/lib/team/actions.ts`
- team pending queries in `/lib/team/hooks.ts`
- team creation form in `/components/team/form/*`

Current reference behavior:

- team directory is public
- team detail is public
- `Create Team` is shown only when logged in and either not on a team or admin
- admins can create a team for another eligible player
- non-admin users create a team for themselves
- team creation currently redirects to the manage view after success
- public team detail shows login prompt, wallet prompt, join/request button, leave button, and manage button depending on user state
- `open`, `request`, `invite`, and `token_gated` membership modes exist
- self-join, join request, manager invite, and request acceptance all currently flow through the same backend add-member endpoint
- managers can see pending invites and join requests
- managers can cancel invites
- managers can accept or deny join requests
- managers can promote, demote, rank, and remove lower-designation members
- owners and admins can transfer ownership or disband the team

Current reference gaps:

- there is no clear player-facing invite inbox or invite acceptance UI in the current app
- there is no clear player-facing cancel-request UI after a join request is sent
- token-gated teams currently mix two concepts:
  - management copy says eligibility is based on linked wallets
  - public join button checks assets from the currently connected browser wallet

The new Nuxt project should resolve those gaps explicitly instead of copying them.

## Role Model

Current designation model:

- `Prime`: owner
- `Nexus`: manager
- `Vector`
- `Echo`

Operational permissions:

- owner can manage all team settings and members, transfer ownership, and disband
- manager can manage lower-designation members and team settings allowed by backend policy
- standard members can leave the team but not manage it
- admin can override most team management permissions

## Membership Modes

V1 membership modes:

- `open`
- `request`
- `invite`
- `token_gated`

Meaning:

- `open`: eligible player joins immediately
- `request`: eligible player submits a join request; manager or owner accepts or denies
- `invite`: team invites a player; player must accept or decline
- `token_gated`: player must satisfy token gate eligibility before joining

## Working Route Direction

Preferred Nuxt route set:

- `/teams`
- `/teams/create`
- `/teams/[id]`
- `/teams/[id]/manage`

Implementation guardrail:

- management may also be surfaced as in-page sections on `/teams/[id]`
- if a sub-route is used, it should still feel team-scoped, not like a separate admin app

## Entry Points

Primary team entry points:

- `/teams`
- `/teams/[id]`
- top-bar `Teams`
- top-bar or page-local `Create Team`
- contextual `Manage Team`

Secondary entry points:

- player profile team link
- account menu `My Team`, if added later
- gauntlet or sponsor context linking to team profiles

## Team Creation Flow

### Eligibility

Desired V1 rule:

- logged-in player can create a team only when not already on a team
- admin can create a team regardless of team membership

Current reference rule matches this.

### Default behavior

Non-admin creator:

- owner is fixed to the logged-in player
- default membership mode is `open`

Admin creator:

- can choose an eligible player without a team as owner
- can create on behalf of that player

### User flow

1. Logged-in eligible user selects `Create Team`.
2. Site opens `/teams/create`.
3. User enters:
   - team name
   - team tag
   - membership mode
   - primary and secondary colors
   - media
   - owner, if admin
4. Site validates the form.
5. Media uploads resolve before final create submission.
6. Site sends create request.
7. Backend creates the team.
8. Session refresh updates current team state if needed.
9. Site routes to the new team's management context.

Recommended success route:

- `/teams/[id]/manage`

Validation rules from current reference:

- team name length 4-16
- team tag length 2-4
- tag alphanumeric only
- tag uppercased
- valid hex colors

Error states:

- unauthorized
- already on a team
- chosen owner no longer eligible
- name or tag conflict
- media upload failure
- backend validation failure

## Public Team Action-State Model

The team profile should compute action state from:

- auth state
- whether the user is already on a team
- whether the user is on this team
- whether the user is owner or manager
- membership mode
- whether the user has a pending join request
- whether the user has a pending invite
- whether the user satisfies token-gate requirements

Recommended public-state matrix:

- anonymous:
  - `Sign in to Join`
- logged in, on another team:
  - no join action
  - explanatory state such as `Already on another team`
- logged in, on this team, non-owner:
  - `Leave Team`
- logged in, on this team, manager/owner/admin:
  - `Manage Team`
- logged in, no team, `open` team:
  - `Join Team`
- logged in, no team, `request` team:
  - `Request to Join`
  - if request pending: `Cancel Request`
- logged in, no team, `invite` team:
  - if invite exists: notification routes to the team page, where `Accept Invite` and `Decline Invite` are shown
  - if no invite exists: informational `Invite Only`
- logged in, no team, `token_gated` team:
  - if eligibility satisfied: `Join Team`
  - if wallet link required: `Connect Wallet`
  - if wrong wallet/token state: `Wallet does not satisfy gate`

## Open Join Flow

1. Logged-in player opens team profile.
2. Team membership mode is `open`.
3. Player is not currently on another team.
4. Player clicks `Join Team`.
5. Site submits join request.
6. Backend adds the player immediately.
7. Session refresh updates player's team state.
8. Team page updates to show member state and `Leave Team` or `Manage Team`.

Success copy:

- `Joined team`

Error states:

- unauthorized
- already on another team
- roster full, if backend introduces limits later
- backend rejection

## Request-to-Join Flow

1. Logged-in player opens team profile.
2. Team membership mode is `request`.
3. Player is not currently on another team.
4. Player clicks `Request to Join`.
5. Site submits request.
6. Backend records pending request.
7. Team page updates to pending state.
8. Player sees `Request Pending` and `Cancel Request`.

Current reference note:

- current app shows `Request to Join` but does not clearly show a dedicated post-request cancel state

Desired V1 behavior:

- the team profile should show pending request state for the requester
- requester should be able to cancel from the same team page

## Cancel Join Request Flow

1. Logged-in player has a pending request for a team.
2. Player reopens team profile or sees request status in a personal queue.
3. Player clicks `Cancel Request`.
4. Site removes the pending request.
5. Team page returns to normal `Request to Join` state.

Implementation note:

- current backend route shape suggests the pending-delete pattern already exists
- the new site should expose it cleanly

## Invite Player Flow

1. Manager, owner, or admin opens team manage view.
2. User opens `Invite Player`.
3. Site shows eligible players with no team.
4. User selects a player.
5. Site submits invite action.
6. Backend records pending invite.
7. Manage view refreshes pending invites list.

Current reference note:

- current app reuses the same add-member action used for self-join and request acceptance

Guardrail:

- the user-facing flow should still describe this as an invite, not a silent membership add

Post-send behavior:

- after an invite is sent, it should appear immediately in the same team management context under pending invites
- team members with permission to manage invites should be able to cancel it from that pending state while it remains unresolved

## Invite Notification Flow

Desired V1 behavior:

1. Team manager, owner, or admin sends an invite to a player.
2. The invited player receives a lightweight in-product notification or pending-team indicator.
3. That notification links the player to the relevant `/teams/[id]` page.
4. The team page opens in an invited state and shows `Accept Invite` and `Decline Invite`.

Notification guidance:

- the notification does not need to be a full notifications product in V1
- a lightweight badge or account/team-status indicator is sufficient
- the notification should direct the player to the team page rather than trying to complete invite acceptance entirely from a detached popup

Acceptable V1 surfaces:

- avatar menu badge or team-status entry
- homepage personal-status module
- team-related banner on `/teams`

Guardrail:

- the team page remains the authoritative place where the player reviews and responds to the invite
- notification is a routing aid, not a separate invite-management application

## Invite Acceptance / Decline Flow

Desired V1 behavior:

1. Invited player signs in.
2. Site surfaces a pending invite notification or team-status indicator.
3. Player follows that notification to `/teams/[id]`.
4. Team page shows invited-state actions in the primary action area.
5. Player chooses `Accept Invite` or `Decline Invite`.
6. Accept adds the player to the team.
7. Decline removes the pending invite.
8. Session and team data refresh.

Direct-navigation rule:

- if the player lands on `/teams/[id]` by other means and has a pending invite for that team, the same accept/decline actions should still appear

Desired team-page state:

- invited player sees team briefing and roster as normal
- primary action block swaps from generic `Invite Only` copy to explicit `Accept Invite` and `Decline Invite`
- after acceptance, page updates to member state
- after decline, page returns to the standard non-member state

Current reference gap:

- current app has manager-side invite creation and cancelation, but no clear player-side invite acceptance UI
- `populateServerSession` even carries a TODO for invites/requests in session context

Required V1 data need:

- player-scoped pending invite state must be queryable for the logged-in player

Recommendation:

- if player-scoped invite state is not ready for initial launch, do not expose `invite` membership mode as a primary user-facing mode until acceptance is practical

## Join Request Review Flow

1. Manager, owner, or admin opens team manage view.
2. User opens `Requests`.
3. Site lists pending join requests with expiry metadata if available.
4. Manager chooses `Accept` or `Deny`.
5. Accept adds player to team.
6. Deny removes pending request.
7. Team data and pending queue refresh.

## Cancel Pending Invite Flow

1. Manager, owner, or admin opens team manage view.
2. User opens `Invites`.
3. Site lists pending invites with expiry metadata if available.
4. User sees the newly sent invite in that pending list.
5. Manager, owner, or admin clicks `Cancel`.
6. Site removes the pending invite.
7. Pending list refreshes.

Context rule:

- pending invite cancelation should stay team-scoped
- authorized team members should not need a separate global invite-admin screen to cancel invites
- the `Invites` tab or equivalent team-page management section is the right place for this action

## Token-Gated Join Flow

Desired V1 source of truth:

- token-gated eligibility should be based on linked wallets recognized by Eventun

Optional UX enhancement:

- currently connected browser wallet can be used for preflight messaging or token preview
- it should not replace server-side eligibility checks

Desired user flow:

1. Logged-in player opens a token-gated team profile.
2. Team page explains the gate and required token collection.
3. If user has no linked eligible wallet, show `Connect Wallet`.
4. User links a wallet through [[wallet-linking]].
5. Site returns user to the team page.
6. Team page reevaluates eligibility.
7. If eligible, player can `Join Team`.
8. Backend confirms eligibility and adds player.

Current reference gap:

- current public join button checks policy IDs from the locally connected browser wallet
- management copy says linked wallets determine eligibility

Nuxt V1 should resolve this by treating linked-wallet eligibility as authoritative.

## Leave Team Flow

1. Logged-in player opens their own team profile.
2. Player is a normal member, not owner.
3. Player clicks `Leave Team`.
4. Site shows destructive confirmation.
5. Player confirms.
6. Backend removes player from team.
7. Session refresh updates team state.
8. Team profile updates to non-member state.

Current reference rule:

- owner cannot use normal leave flow
- owner must transfer ownership or disband

## Manage Team Flow

### Access rule

Manage route or manage section is visible only to:

- owner
- manager
- admin

Standard members and outsiders should not access team management.

### Management zones

Recommended V1 management zones:

- team identity
- team media
- membership mode and gate tokens
- roster
- invites
- requests
- ownership/disband actions

## Team Identity Editing Flow

Manager, owner, or admin can update:

- team name
- team tag
- primary color
- secondary color
- membership mode

Media management can update:

- hero/avatar/banner media as supported

Mutation behavior:

- update team
- refresh team view
- refresh session if current team changed

## Membership Mode and Gate Token Management Flow

Manager, owner, or admin can:

- switch between `open`, `request`, `invite`, and `token_gated`
- add gate token policies
- remove gate token policies

Desired V1 behavior:

- changing mode updates the public team page immediately
- token-gated teams should explain that players must satisfy at least one required token policy
- if gate token list is empty while mode is `token_gated`, show setup guidance instead of a broken gate

Current reference behavior:

- token list can be selected from known tokens or entered manually by policy id

## Roster Management Flow

Manager, owner, or admin opens roster tab.

Allowed actions on lower-designation players:

- promote
- demote
- set or clear rank
- remove from team

Permission rule from current reference:

- manager can only manage players with a numerically lower privilege than their own designation
- admin can override this

Desired V1 UX:

- show unavailable actions as disabled or hidden based on clarity
- avoid ambiguous failures caused by hidden permission rules

## Ownership Transfer Flow

1. Owner or admin opens manage view.
2. Team has more than one member.
3. User clicks `Transfer Ownership`.
4. Site opens member picker excluding current owner.
5. User selects successor.
6. Site shows confirmation.
7. Backend transfers ownership and demotes prior owner appropriately.
8. Team and session state refresh.

Current reference behavior:

- payload uses `successorId`
- prior owner is reassigned designation `1`

## Disband Team Flow

1. Owner or admin opens manage view.
2. User clicks `Disband Team`.
3. Site shows destructive confirmation.
4. User confirms.
5. Backend disbands team.
6. Members are removed from the team.
7. Session refresh updates current user.
8. Site routes to `/teams`.

Guardrail:

- disband is irreversible
- prefer clear explicit warning copy

## Team Data Refresh and Session Interaction

After any of these actions, the site should invalidate and refresh:

- team detail
- team list
- pending team queues when relevant
- logged-in session if current user's team state changed

Actions that should refresh session:

- team creation
- self-join
- request acceptance when it affects the current user
- leaving team
- ownership transfer affecting current user
- disband affecting current user
- membership mode or gate-token edits when session exposes current-team fields that changed

## Public Messaging Guidance

Good copy:

- `Join Team`
- `Request to Join`
- `Request Pending`
- `Accept Invite`
- `Decline Invite`
- `Invite Only`
- `Team management`
- `Transfer ownership`
- `Token-gated crew`

Avoid:

- vague labels like `Proceed`
- hidden request states
- making invite-only teams feel broken when the user simply lacks an invite

## Accessibility Requirements

- team action buttons must be keyboard reachable
- destructive actions require clear confirmation dialogs
- pending states must be visible as text, not color alone
- roster-management controls must have accessible labels
- token-gate explanations must be readable without relying on token imagery
- mobile layouts must keep primary team actions visible without forcing horizontal scroll

## Acceptance Criteria

- eligible logged-in players can create a team
- non-admin users cannot create a second team while already on a team
- admins can create a team on behalf of an eligible player
- team creation routes to the new team's management context
- open teams can be joined directly by eligible players
- request-mode teams create a pending request state
- requester can cancel a pending request
- managers can accept or deny join requests
- managers can invite eligible players
- invited players receive a notification or status indicator that routes them to the team page
- invited players have a visible way to accept or decline invites on the team page
- managers, owners, and admins can cancel pending invites from the team management context
- non-owner members can leave their team
- owners cannot leave without transfer or disband handling
- manage route is limited to manager, owner, or admin
- managers can manage lower-designation members only
- owners or admins can transfer ownership
- owners or admins can disband the team with confirmation
- token-gated teams rely on linked-wallet eligibility as the authoritative rule
- team and session state refresh after mutations

## Open Questions

- Should invite notification appear in the avatar menu, homepage personal-status area, `/teams`, or more than one of those surfaces?
- Should the team page action area show invite-specific controls above the standard membership-mode copy when a pending invite exists?
- Should invite-only teams be allowed in V1 if player-side invite acceptance is not ready?
- Should managers be allowed to edit all team identity settings, or should some remain owner-only?
- Should token-gated teams require linked-wallet eligibility only, or linked wallet plus current wallet connection for better UX?
- Should players on another team see a clear `Leave current team first` message on joinable teams?
- Should `/teams/create` remain a separate route, or can creation be a modal/sheet launched from `/teams`?
