# Ascent Rivals - Website

## Related
- [[overview]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[accountun]]
- [[cardano]]
- [[midnight]]
- [[team-gauntlet-current-state]]

## Role
Primary web application surface for player-facing and operations-facing workflows.

## Responsibilities
- player identity and profile experiences
- competition discovery and context views
- team and social participation workflows
- sponsor and administrative operations
- entitlement and wallet-linked interaction flows

## Current Implementation Notes

Ascentun currently implements the core team lifecycle: team list/profile/create, open join, request-to-join, invite acceptance, token-gated join checks, owner/manager/admin team management, roster rank/designation edits, pending invites, pending join requests, owner transfer, and disband.

Ascentun gauntlet authoring currently carries `playersPerTeam`, `allowedTeams`, `requiredStageWins`, `requiredStageLosses`, and `groups` in TypeScript/schema state, but the visible create/edit UI does not expose team-stage or bracket authoring controls. The visible stage form is limited to stage type, start time, race mode, competitor/lobby counts, and circuit configuration. The stage detail view does not show allowed teams, per-team caps, bracket filters, overflow policy, admission priority rule, roster lock point, or join status.

For team gauntlet iteration planning, see [[team-gauntlet-current-state]].

## Domain Boundary
- competition domain data is owned by [[eventun/overview|eventun]]
- accounting transitions are owned by [[accountun]] / [[midnight]]
- wallet/community identity context intersects with [[cardano]]

## Open Questions
- Which data requires strict real-time freshness versus eventual consistency?
- Which operations belong in public web workflows versus restricted operations tooling?
- Which views should expose private-versus-public distinction explicitly?
