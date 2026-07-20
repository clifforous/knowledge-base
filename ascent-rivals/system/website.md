# Ascent Rivals - Website

## Related
- [[overview]]
- [[eventun/overview|eventun]]
- [[eventun/api|eventun-api]]
- [[accountun]]
- [[cardano]]
- [[midnight]]
- [[team-gauntlet-current-state]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/teams-solution-design|teams-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]

## Role
Primary web application surface for player-facing and operations-facing workflows.

## Responsibilities
- player identity and profile experiences
- competition discovery and context views
- team and social participation workflows
- sponsor and administrative operations
- entitlement and wallet-linked interaction flows

## Current Implementation Notes

Ascentun is hosted on the existing Vercel Pro plan with a two-environment deployment split: `ascentun` for production and `ascentundev` for development. Each deployment connects to Eventun in the corresponding AccelByte production or development game environment. Website V2 is expected to preserve the same two-environment boundary. Reuse of `ascentrivals.com` is the working production-domain assumption pending final cutover confirmation.

Ascentun currently implements the core team lifecycle: team list/profile/create, open join, request-to-join, invite acceptance, owner/manager/admin team management, roster rank/designation edits, pending invites, pending join requests, owner transfer, and disband.

The retired Eventun token catalog and team gate API consumers have been removed from Ascentun. The website supports only open, invite-only, and request-to-join membership modes. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.

For the next teams iteration, Ascentun remains the minimal administration surface for team creation/disband, ownership transfer, title and capability assignment, member administration, recruiting metadata, watch/community links, the website-uploaded team avatar, and fixed team-cosmetic management. The game client focuses on browsing, viewing, joining, invitations, leave, and member presentation preferences. Text search comes after controller browsing, and pagination is deferred for the current expected roster scale.

Ascentun gauntlet authoring currently carries `playersPerTeam`, `allowedTeams`, `requiredStageWins`, `requiredStageLosses`, and `groups` in TypeScript/schema state, but the visible create/edit UI does not expose team-stage or bracket authoring controls. The visible stage form is limited to stage type, start time, race mode, competitor/lobby counts, and circuit configuration. The stage detail view does not show allowed teams, per-team caps, bracket filters, overflow policy, admission priority rule, roster lock point, or join status.

Required core gauntlet changes should extend the create/detail flows to author allocation rules, top-N team scoring, racer slots per owner, roster admission policy, and field publication. Bracket setup/repair remains a separate administrator operation in the Eventun Extend App UI. The future v2 website remains the target for the polished public competition experience and delegated core authoring.

Website V2 remains the intended core gauntlet create/edit/delete surface because Eventun's player-facing domain authorization supports delegated `gauntlet_creator` users as well as administrators. The Eventun Extend App UI is the initial surface for deliberately administrator-only bracket generation/publication/repair and runtime result or stage-operation repair. Public Website rendering of published bracket/match state remains separate from mutation permission. Do not duplicate the core authoring form across both applications.

Administrator-only sponsor list/detail, CRUD, and sponsor-owned media administration also belong in the Eventun Extend App rather than Website V2. Website V2 has no sponsor registry routes; it retains only bounded gauntlet-context sponsor display, an optional form-scoped existing-sponsor selector, and direct gauntlet-owned billboard upload. The Extend App sponsor workflow and an administrator-authorized sponsor media upload boundary must be working before Ascentun's sponsor pages are retired.

Website V2 team and gauntlet media retain direct browser-to-R2 transfer through a same-origin upload-intent route. Intents require the corresponding Eventun-backed create/manage permission, accept no more than 10 JPEG/PNG/WebP images of no more than 10 MB each per submission, use ten-minute signed URLs and server-generated keys, and exclude sponsor/course uploads and new `WideBillboard` records. Occasional unreferenced objects from abandoned forms are an accepted initial low-volume tradeoff rather than a reason to add a pending-upload service.

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
