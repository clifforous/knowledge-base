# Ascent Rivals Teams Index Page Spec

Date: 2026-04-13
Status: Approved public directory contract; desktop/mobile visual calibration pending
Last reviewed: 2026-07-22

The approved T03 public-read checkpoint defines this page's data boundary. The stable public
membership labels are `Open`, `Request to Join`, and `Invite Only`. Token-gated membership is not
part of Website V2.

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../route-api-matrix]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[team-profile]]
- [[player-profile]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/delivery-plan|teams delivery plan]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA, public-data boundary, and page requirements for the public team directory.

The teams index should help players and followers answer:

- which active teams exist;
- how each team identifies itself;
- how many active members it has;
- which public membership mode it uses;
- which team profile they want to inspect.

Creation eligibility and the authenticated player's current-team context are private overlays, not
fields in the public directory collection.

## Route

Working route:

- `/teams`

Current app route equivalent:

- `/team`

Final route direction:

- use plural route groups in Website V2;
- allow old singular routes to retire without redirects unless later measured inbound use justifies
  an exact mapping.

## Audience

Primary:

- players looking for a team;
- followers browsing crews;
- team managers checking team presentation.

Secondary:

- sponsors;
- tournament organizers;
- press/community viewers.

## Page Goals

- make teams feel like first-class public entities;
- preserve fast client-side search and filtering over the compact complete collection;
- show enough identity and membership context to choose a team profile;
- expose `Create Team` only from a separate authoritative eligibility overlay;
- avoid turning the directory into a roster or management table;
- avoid introducing speculative team statistics or activity claims.

## Current-System Reference

The committed local Team Core API exposes compact active-team summaries without rosters and a
complete roster through the per-team detail read. Shared development and production retain the
legacy contract until coordinated cutover. See [[ascent-rivals/system/eventun/api#Committed Local Team Core API|Eventun API]].

Website V2 does not consume the legacy every-team-plus-roster shape as its target contract.

## Approved T03 Public Directory Projection

Return one compact summary per active team containing only:

- stable team identity;
- public name;
- public tag;
- public membership mode;
- primary and secondary colors;
- bounded approved public media;
- active member count.

Normal browse omits disbanded teams. A future direct historical lookup may return a compact
tombstone, but it does not enter this directory.

The directory projection does not include:

- complete or preview rosters;
- management capabilities;
- pending invitations or join requests;
- relationship/action state;
- performance summaries or statistics;
- membership intervals, roster revisions, audit, or correction evidence.

Use the same compact public identity in global search. Do not make internal identifiers, raw enum
values, or private metadata searchable merely because they exist in Eventun.

## Membership Labels

Map the implemented Eventun values to these player-facing labels:

- `Open`;
- `Request to Join`;
- `Invite Only`.

Membership mode is descriptive. It does not authorize or predict an action for the authenticated
viewer. Join/request/invitation decisions belong to the authoritative viewer-state response on the
team profile.

## Page Structure

Default first-view priority:

1. directory header;
2. local name/tag search and optional membership-mode filter;
3. compact team collection;
4. eligible create-team affordance.

## 1. Directory Header

Purpose:

- establish the team directory as a crew registry.

Content:

- title such as `Teams`;
- short operational description;
- `Create Team` only when the separate authenticated eligibility response allows it.

Do not require a total count in the visual header. If the complete collection length is useful to
assistive status text, derive it locally from the returned collection.

Terminal Ops components:

- `HeroBriefing`;
- `CommandAction`.

## 2. Search and Filters

Initial controls:

- local search by team name or tag;
- membership-mode filter only if it improves the reviewed composition.

The expected compact collection remains client-side for search, filtering, sorting, and display
pagination/progressive reveal. Add server pagination or server search only after measured payload or
interaction cost justifies changing that contract.

Do not add an active/inactive filter: normal browse already contains active teams only. Recruiting,
region, recent-activity, and competitive-focus filters require separately approved public fields.

## 3. Team Cards

Required card content:

- approved team avatar or bounded media fallback;
- team name;
- team tag;
- active member count;
- public membership label;
- restrained accent derived from approved team colors;
- canonical link to `/teams/[id]`.

Do not add roster previews. Do not place management actions, pending-state indicators, statistics,
trophies, or audit-shaped metadata on directory cards.

Terminal Ops components:

- `EntityCard`;
- `TeamTag`;
- `StatusChip`.

## 4. Create Team CTA

Visible when:

- the user is authenticated; and
- the separate authoritative session/current-player response says team creation is available.

Placement:

- directory header or command-action area;
- not global top navigation.

Design guidance:

- if the user is already on a team, use `My Team` context rather than foregrounding creation;
- if the user is anonymous, ordinary `Sign In` remains in the shared shell; do not add a disabled
  create button;
- do not derive eligibility from absence in the public team collection.

## Required Collection States

The desktop/mobile calibration must include:

- populated collection;
- sparse collection;
- no public teams available;
- no local search matches;
- public directory unavailable;
- missing or invalid optional media.

Tone:

- `No teams registered.`;
- `No crews match this query.`;
- `Team registry unavailable.`

Guardrail:

- a sparse directory should use deliberate spacing and stronger identity presentation rather than
  fabricated activity or statistics.

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | Browse/search teams and open public team profiles. |
| Authenticated player without a team | Same public collection plus separate create eligibility when available. |
| Authenticated player on a team | Same public collection plus `My Team` context from private session state. |
| Admin | Same public collection; administration does not enter directory cards. |

## Responsive Behavior

Desktop:

- command header;
- compact local controls;
- responsive card grid.

Tablet:

- reduce card columns;
- keep search and any accepted membership filter reachable.

Mobile:

- stack or collapse local controls without imitating page tabs;
- use compact team rows/cards;
- preserve team name, tag, active member count, and membership label;
- keep the shared sign-in/account control in the top bar.

## SEO and Sharing

The team directory should support:

- title: `Teams - Ascent Rivals`;
- description focused on public teams, crews, and roster discovery;
- canonical URL.

Do not expose private viewer, invitation, request, or capability state in metadata.

## Deferred Directory Ideas

These ideas require separate product and public-field decisions and do not block the initial route:

- explicit recruiting flag separate from membership mode;
- region or time-zone;
- public social/watch links;
- featured/manual ordering;
- search by member name;
- team performance, trophies, medals, or recent activity on directory cards.

## Open Questions

- Should the default order be alphabetical or an explicitly authored featured order?
- Does the reviewed composition benefit from a membership-mode filter at the expected team count?

## Next Steps

- Update the desktop and mobile Pencil specimens against this exact compact projection.
- Review populated, sparse, no-result, unavailable, and missing-media states without adding roster
  or statistics fields.
- Revalidate compressed payload size and local search responsiveness after T03 implementation.
