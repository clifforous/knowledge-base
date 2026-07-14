# Ascent Rivals - Website

## Related
- [[overview]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[accountun]]
- [[cardano]]
- [[midnight]]
- [[team-gauntlet-current-state]]
- [[../../30_designs/ascent-rivals/teams-solution-design|teams-solution-design]]
- [[../../30_designs/ascent-rivals/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[../../30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]

## Role
Primary web application surface for player-facing and operations-facing workflows.

## Responsibilities
- player identity and profile experiences
- competition discovery and context views
- team and social participation workflows
- sponsor and administrative operations
- entitlement and wallet-linked interaction flows

## Current Implementation Notes

Ascentun currently implements the core team lifecycle: team list/profile/create, open join, request-to-join, invite acceptance, owner/manager/admin team management, roster rank/designation edits, pending invites, pending join requests, owner transfer, and disband.

The retired Eventun token catalog and team gate API consumers have been removed from Ascentun. The website supports only open, invite-only, and request-to-join membership modes. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.

For the next teams iteration, Ascentun remains the minimal administration surface for team creation/disband, ownership transfer, title and capability assignment, member administration, recruiting metadata, watch/community links, the website-uploaded team avatar, and fixed team-cosmetic management. The game client focuses on browsing, viewing, joining, invitations, leave, and member presentation preferences. Text search comes after controller browsing, and pagination is deferred for the current expected roster scale.

Ascentun gauntlet authoring currently carries `playersPerTeam`, `allowedTeams`, `requiredStageWins`, `requiredStageLosses`, and `groups` in TypeScript/schema state, but the visible create/edit UI does not expose team-stage or bracket authoring controls. The visible stage form is limited to stage type, start time, race mode, competitor/lobby counts, and circuit configuration. The stage detail view does not show allowed teams, per-team caps, bracket filters, overflow policy, admission priority rule, roster lock point, or join status.

Required gauntlet changes should extend the existing create/detail flows only enough to author allocation rules, top-N team scoring, racer slots per owner, roster admission policy, field publication, and bracket setup/repair. The future v2 website remains the target for a polished competition experience.

Team progression definitions, caps, level thresholds, unlock mappings, diagnostics, and projection repair belong in Eventun's existing AccelByte Extend App UI rather than Ascentun.

For team gauntlet iteration planning, see [[team-gauntlet-current-state]].

## Domain Boundary
- competition domain data is owned by [[eventun/overview|eventun]]
- accounting transitions are owned by [[accountun]] / [[midnight]]
- wallet/community identity context intersects with [[cardano]]

## Open Questions
- Which data requires strict real-time freshness versus eventual consistency?
- Which operations belong in public web workflows versus restricted operations tooling?
- Which views should expose private-versus-public distinction explicitly?
