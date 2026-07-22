# Ascent Rivals Website Surfaces

Applicability: Known current behavior and deployment boundaries; production statements are
limited to the explicitly described hosted sites.

## Current State

Ascent Rivals currently uses two separate web applications.

### Marketing website

The `ascent-website` application is the current public marketing surface. Its known content
includes:

- `/` for the game proposition, Steam conversion, partner proof, gameplay features, video,
  ship customization, gallery, and community links;
- `/about` for studio mission, team, recognition, appearances, and development/event video;
- `/brand` for downloadable brand assets and usage guidance;
- `/tournaments` and `/tournaments/msi-grand-prix-2026` for code-authored current and
  historical tournament material.

Marketing changes use the existing designer-to-code workflow: an approved mock, copy, and
assets are implemented directly in the repository and shipped with the application. There is
no current CMS requirement.

The MSI Grand Prix hero uses the approved MSI tournament crest with a separate “Sponsored by
MSI” lockup immediately above it. Both are repository-owned static assets derived from the
approved Idemax mock rather than hotlinked media. The `/tournaments` upcoming promotion uses
the same tournament crest over the event race artwork without repeating the sponsor lockup.

### Ascentun

Ascentun is the current player-facing and operations-facing web application. It is hosted on
the existing Vercel Pro plan as `ascentun` for production and `ascentundev` for development.
Each deployment connects to Eventun in the corresponding AccelByte production or development
game environment.

Current responsibilities include:

- public player, team, gauntlet, standing, and competition views;
- Steam OpenID login followed by the AccelByte `steamopenid` platform-token exchange,
  session refresh, permission-aware navigation, and logout;
- team list/profile/create, open join, request-to-join, invite acceptance, owner/manager/admin
  management, roster rank/designation edits, pending invitations and requests, ownership
  transfer, and disband;
- gauntlet list/detail/create/edit/delete, qualifier and stage configuration, standings,
  media, and sponsor association;
- administrator sponsor list/detail and sponsor/media management;
- the explicitly retained Midnight/blockchain sponsored-tournament workflow that prevents
  describing Ascentun as fully retired at Website V2 cutover.

The retired Eventun token catalog and team-gate consumers have been removed. Current team
membership supports open, invite-only, and request-to-join behavior; token gating is not a
current capability.

Ascentun has no current end-user wallet-management page. Some wallet-related components and
routes remain as inactive implementation remnants, and Website V2 must not treat them as a
working parity requirement.

## Known Gaps

- Ascentun gauntlet state carries `playersPerTeam`, `allowedTeams`, `requiredStageWins`,
  `requiredStageLosses`, and `groups`, but the visible create/edit UI does not expose the
  complete team-stage or bracket model.
- The visible stage form is limited to stage type, start time, race mode,
  competitor/lobby counts, and circuit configuration. Stage detail omits allocation,
  bracket, roster-lock, admission, and join-state information.
- The current Steam callback/session implementation works in the Ascent Rivals environment,
  but the Website V2 authentication specification records callback validation, browser-cookie
  trust, Login Queue, refresh serialization, revocation, and safe-logging gaps that should not
  be copied into the replacement.
- Sponsor media administration depends on the existing web workflow; the Eventun Extend App
  does not yet provide the complete replacement and authorized upload boundary required for
  cutover.

## System Boundaries

- Eventun owns competition, player, team, gauntlet, standing, and related domain behavior.
- AccelByte owns platform identity and authoritative course configuration.
- Accountun and Midnight own accounting and blockchain-related prize/reward transitions.
- The marketing repository owns code-authored public/editorial content and static brand
  assets for the current marketing application.

## Future Direction

[Website V2](../initiatives/website-v2/README.md) is an active initiative, not current or
deployed behavior. It is intended to:

- replace the marketing website and approved public/player non-blockchain Ascentun behavior
  with one greenfield Next.js/React application;
- retain the current two-environment website-to-AccelByte/Eventun boundary, with
  `ascentrivals.com` as the working production-domain assumption pending cutover;
- keep delegated team and core gauntlet workflows in Website V2 while assigning
  administrator-only sponsor administration, bracket mutation, and runtime repair to the
  Eventun Extend App;
- exclude wallet linking, token gating, and Accountun-related prize/reward data or workflow
  links from the initial release;
- preserve the legacy Ascentun host only for the explicitly deferred Midnight/blockchain
  workflow until that dependency is retired or relocated.

Future Website V2 media limits, cache policy, route composition, and permission boundaries
are authoritative only within that initiative until implemented and incorporated here.

## Evidence And Decisions

- [Website V2 initial-release scope](../initiatives/website-v2/initial-release-scope.md)
- [Website V2 delivery plan](../initiatives/website-v2/delivery-plan.md)
- [Authentication flow and current Ascentun observations](../initiatives/website-v2/flows/authentication.md)
- [Sponsor-administration handoff](../initiatives/website-v2/sponsor-administration-handoff.md)
- [Team and gauntlet current state](team-gauntlet-current-state.md)
- [Ascent Rivals decision log](../decisions/README.md)
