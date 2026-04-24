# Ascent Rivals Sponsors Page Spec

Date: 2026-04-14
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[gauntlets-index]]
- [[gauntlet-detail]]
- [[team-profile]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the IA and page requirements for sponsor and partner presentation.

The sponsors page should help players, followers, and partners answer:

- who supports Ascent Rivals
- what sponsors are connected to gauntlets and events
- where to find sponsor websites/socials
- which brands are active partners
- how admins create and maintain sponsor records

## Route

Working route:

- `/sponsors`

Current app route equivalent:

- `/sponsor`
- `/sponsor/[id]`
- `/sponsor/create`
- `/sponsor/[id]/edit`

Optional public detail route:

- `/sponsors/[id]`

Final route direction:

- `/sponsors` is the required public route
- `/sponsors/[id]` is optional in V1 and should only be first-class if sponsor content is rich enough to justify detail pages
- admin create/edit routes can exist as permissioned sub-routes or in-page admin flows, but should not dominate the public sponsor listing
- preserve redirects from old singular routes if public links already exist

## Audience

Primary:

- players and followers seeing who backs events
- sponsors and potential partners
- admins maintaining sponsor records

Secondary:

- press/community viewers
- tournament organizers
- teams

## Page Goals

- make sponsors feel like credible partners, not a buried admin list
- preserve public sponsor browsing
- preserve sponsor CRUD/admin workflows from the current site
- expose sponsor social/website links clearly
- connect sponsors to gauntlets where data supports it
- support sponsor media and brand colors without letting sponsor branding override Ascent Rivals visual identity

## Current V1 Data Availability

### Sponsor list

Available:

- sponsor id
- name
- description
- primary color
- secondary color
- website URL
- Discord URL
- X URL
- Twitch URL
- media

Source:

- `GET /v1/sponsor`

### Sponsor detail

Available:

- same sponsor fields as list, by sponsor id

Source:

- `GET /v1/sponsor/{sponsorId}`

### Sponsor admin

Available:

- create sponsor
- update sponsor
- delete sponsor

Sources:

- `POST /v1/admin/sponsor`
- `PUT /v1/admin/sponsor/{sponsorId}`
- `DELETE /v1/admin/sponsor/{sponsorId}`

Admin-editable fields:

- name
- description
- primary color
- secondary color
- website URL
- Discord URL
- X URL
- Twitch URL
- media

### Gauntlet sponsor relationship

Available from gauntlet data:

- sponsor id
- tier

Source:

- gauntlet `sponsors` field

V1 caution:

- Eventun exposes sponsor relationships from gauntlets, but there does not appear to be a dedicated sponsor-to-gauntlets aggregate endpoint.
- If the sponsor page shows sponsored gauntlets, it may need to derive the relationship from the gauntlet list/detail data.
- Do not make sponsored-gauntlet history a hard V1 dependency unless the implementation has a cheap data path.

## V1 Page Structure

Default first-view priority:

1. sponsor/partner identity and search
2. sponsor cards
3. featured/current partners if data or editorial curation exists
4. admin create/edit affordances for authorized users
5. optional sponsor detail or relationship modules

## 1. Partner Registry Header

Purpose:

- present sponsors as public partner entities

Content:

- title such as `Sponsors`
- short partner-oriented description
- sponsor count if useful
- `Create Sponsor` action for admins only

Tone examples:

- `Sponsor registry online`
- `Partner signal acquired`
- `No sponsors registered`

Terminal Ops components:

- `HeroBriefing`
- `StatusTelemetryBar`
- `CommandAction`

## 2. Search and Sort

Purpose:

- preserve fast sponsor discovery

V1 controls:

- search by sponsor name
- search by description
- sort A-Z
- sort Z-A

Optional later:

- filter by sponsor tier
- filter by active gauntlet relationship
- filter by event type or partner category

Design guidance:

- search/sort should be compact
- do not overbuild filters until sponsor volume requires them

## 3. Sponsor Cards

Purpose:

- make sponsor browsing visual and scannable

Card content:

- sponsor logo/media
- name
- short description if present
- website/social link indicators
- color accent using sponsor colors
- link to detail if `/sponsors/[id]` exists

Design guidance:

- use sponsor colors as accents, borders, or small metadata treatments
- do not let sponsor colors override the global Terminal Ops shell
- keep card layout consistent with player/team/gauntlet entity cards

Terminal Ops components:

- `EntityCard`
- `SponsorMark`
- `StatusChip`
- `ExternalLinkCluster`

## 4. Featured Sponsors

Purpose:

- optionally highlight important partners

V1 status:

- optional
- only show if manually curated data, sponsor tier data, or event context supports it

Guardrail:

- do not create a permanent empty featured section
- do not imply paid tiering unless the business/design team intends that presentation

## 5. Sponsor Detail

Optional V1.

Purpose:

- provide a richer public page for a sponsor when content exists

Possible route:

- `/sponsors/[id]`

Content:

- banner/hero media
- sponsor name
- description
- website/social links
- color accents
- related gauntlets if cheaply derivable

Current app equivalent:

- `/sponsor/[id]`

Design guidance:

- if sponsor content remains light, detail can be a modal/panel or expanded card instead of a full route
- if sponsors become more important to events, use dedicated detail pages

## 6. Sponsor Relationships

Purpose:

- connect sponsors to the events they support

Possible V1 surfaces:

- sponsor strip on gauntlet detail
- sponsor badges/cards in gauntlet listing
- optional related gauntlets on sponsor detail

Data:

- gauntlet sponsor id
- sponsor tier

V1 caution:

- sponsor tier is available on the gauntlet relationship, not necessarily on the sponsor itself
- avoid global sponsor tier displays unless the relationship context is clear

## 7. Admin Sponsor Management

Visible only to admins.

Actions:

- create sponsor
- edit sponsor
- delete sponsor
- update media
- update colors
- update description
- update social links

Placement:

- `Create Sponsor` in the sponsors header for admins
- `Edit Sponsor` on sponsor card/detail for admins
- destructive delete action separated from normal public actions

Guardrail:

- public users should not see disabled admin controls
- sponsor admin should feel integrated into the public sponsor context, not like a separate back-office product

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | can view sponsor list, public sponsor details, public external links, and sponsor appearances on gauntlets |
| Logged-in player | same as anonymous plus account/avatar state; no special sponsor actions |
| Admin | same plus create/edit/delete sponsor actions and media/social/color management |

## Empty / Loading / Error States

Required states:

- no sponsors
- no sponsors matching search
- sponsor not found, if detail route exists
- failed sponsor list fetch
- failed sponsor detail fetch
- media missing
- failed create/update/delete

Tone:

- `No sponsors registered.`
- `No sponsor signal matches this query.`
- `Sponsor profile not found.`
- `Sponsor registry unavailable.`

Guardrail:

- missing sponsor media should fall back to a branded placeholder
- failed admin writes should be explicit and recoverable

## Responsive Behavior

Desktop:

- partner registry header
- search/sort row
- sponsor card grid
- optional detail panel or route

Tablet:

- reduce card columns
- keep search and sort reachable

Mobile:

- stack search/sort controls
- use compact sponsor cards
- keep login/avatar visible in top bar
- preserve sponsor name, media, and external link affordances

## SEO and Sharing

The sponsors page should support:

- title: `Sponsors - Ascent Rivals`
- description focused on partners and event sponsors
- canonical URL

If sponsor detail routes are used:

- title: `{Sponsor Name} - Ascent Rivals Sponsor`
- description from sponsor description if present
- Open Graph image from sponsor media

Do not expose admin-only sponsor state in metadata.

## V2 Candidate Data Needs

These ideas are valuable but should not block V1:

- sponsor category/type
- explicit featured sponsor flag
- sponsor-to-gauntlet aggregate endpoint
- sponsor event history
- sponsor prize contribution history
- sponsor team relationships
- partner inquiry CTA
- partner media kit downloads
- public sponsor tiers independent of gauntlet relationship tiers

## Open Questions

- Should `/sponsors/[id]` be a required public route or optional until sponsor content becomes richer?
- Should sponsor tier be shown globally, or only in gauntlet/event context?
- Should partner inquiry content live on `/sponsors`, `/press`, or a future `/partners` page?
- Should sponsor admin live as `/sponsors/create` and `/sponsors/[id]/edit`, or as admin-only in-page controls?
- Which sponsor media purpose should be preferred for cards: avatar, square hero, or banner hero?

## Next Steps

- Ask Pencil for one sponsors page mock using this spec and Terminal Ops.
- Decide whether sponsor detail should be a full route or expandable card/panel in V1.
- Keep homepage sponsor strip and search behavior aligned with the public/private sponsor visibility decision.
