# Ascent Rivals Sponsor Registry Spec

Date: 2026-04-14
Updated: 2026-07-15
Status: Draft

## Related

- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[gauntlets-index]]
- [[gauntlet-detail]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]
- [[../../../../50_knowledge/ascent-rivals/game-client|game-client]]
- [[../flows/gauntlet-authoring]]

## Purpose

Define the administrator-facing Website V2 registry used to inspect and maintain Eventun sponsor records, plus its limited relationship to gauntlet authoring.

The sponsor catalog is an administrative surface, not a public entity directory or the default gauntlet advertising workflow. It should help administrators answer:

- which approved media, colors, and links belong to a sponsor;
- which sponsor records an administrator can create, edit, or delete.

Gauntlet creators currently tend to upload tournament-specific billboard artwork directly to the gauntlet. Sponsor-entity association remains an optional advanced capability because the same sponsor and artwork are not necessarily reusable across tournaments.

Public visitors may see approved sponsor branding in the context of a gauntlet or code-authored marketing content. They do not receive a general sponsor index or sponsor profile route.

## Sponsor and Partner Terminology

- `Sponsor` is the Eventun-backed competition entity used by gauntlet authoring, sponsor relationships, and sponsor administration;
- `Partner` is a broader manually verified marketing relationship and does not imply Eventun sponsorship or a gauntlet association;
- code-authored marketing sections may use `Partners` when that broader relationship is accurate;
- do not merge code-authored partner content into the Eventun sponsor catalog;
- do not add a public `/partners` route until distinct partner content and ownership justify it.

## Routes and Visibility

Working routes:

- `/sponsors` — administrator-only registry;
- `/sponsors/[id]` — administrator-only sponsor record detail;
- sponsor create/edit routes or equivalent in-page flows — administrators only.

Current app route equivalents:

- `/sponsor`;
- `/sponsor/[id]`;
- `/sponsor/create`;
- `/sponsor/[id]/edit`.

Required direction:

- preserve sponsor list/detail capability for operational replacement parity;
- do not expose either route in public navigation, public entity search, sitemaps, or anonymous metadata;
- require server-side authorization rather than relying on hidden links or client-only checks;
- gauntlet creators do not receive general registry/detail access;
- gauntlet authoring leads with direct gauntlet-owned advertising uploads and retains a scoped advanced picker for associating an existing sponsor entity;
- administrators retain create, edit, delete, media, color, description, and social-link management;
- preserve existing sponsor records, media, gauntlet relationships, and relationship tiers without flattening them into gauntlet-owned media;
- exact create/edit route naming can be chosen with the other operational routes;
- preserve legacy redirects only inside the equivalent authorized flow; do not turn old singular URLs into public sponsor pages.

## Audience

Primary:

- administrators maintaining sponsor records.

Not an audience for the registry:

- anonymous visitors;
- ordinary logged-in players;
- gauntlet creators outside the scoped gauntlet-authoring relationship control;
- press or community viewers;
- marketing partners without an explicitly designed operational identity and permission model.

## Page Goals

- make approved sponsor identity, media, colors, and external links easy to verify;
- preserve sponsor CRUD/admin workflows from Ascentun;
- keep reusable sponsor records secondary to gauntlet-owned campaign artwork;
- show relationship context without treating tier as a global sponsor rank;
- keep private or operational sponsor fields out of public responses and metadata.

## Current V1 Data Availability

### Sponsor List

Available:

- sponsor id;
- name;
- description;
- primary color;
- secondary color;
- website URL;
- Discord URL;
- X URL;
- Twitch URL;
- media.

Source:

- `GET /v1/sponsor`.

### Sponsor Detail

Available:

- the same sponsor fields as the list, by sponsor id.

Source:

- `GET /v1/sponsor/{sponsorId}`.

### Sponsor Administration

Available:

- create sponsor;
- update sponsor;
- delete sponsor.

Sources:

- `POST /v1/admin/sponsor`;
- `PUT /v1/admin/sponsor/{sponsorId}`;
- `DELETE /v1/admin/sponsor/{sponsorId}`.

Admin-editable fields:

- name;
- description;
- primary color;
- secondary color;
- website URL;
- Discord URL;
- X URL;
- Twitch URL;
- media.

### Gauntlet Sponsor Relationship

Available from gauntlet data:

- sponsor id;
- relationship tier.

Source:

- gauntlet `sponsors` field.

### Gauntlet-Owned Advertising Media

Current behavior:

- gauntlet media supports direct `Billboard` assets independently of sponsor entities; `Tileable` metadata makes a normal billboard compatible with ribbon-style placements;
- `WideBillboard` still exists as a media purpose, but the reviewed client has no identified consumer for its separate collection;
- the current gauntlet create/edit form uploads those assets through the ordinary gauntlet media workflow;
- practical organizer use commonly stores tournament-specific sponsor artwork this way;
- the game client treats direct gauntlet media as the synthetic `Gauntlet` source at tier `0` when populating course billboards.

Initial Website direction:

- make direct gauntlet billboard upload the primary creator workflow;
- preserve preview, replacement, ordering, validation, and removal through the gauntlet media form;
- assume the currently used square creative, show a square thumbnail, and render three adjacent copies when `Tileable` is enabled;
- do not extract dimensions or attempt to match uploads to billboard aspect ratios or physical slots in the initial release;
- do not require sponsor name, reusable identity, or sponsor relationship tier merely to place campaign artwork;
- retain sponsor-entity association only as an optional advanced path until the sponsor model has responsibilities beyond reusable advertising media.

Sponsor, gauntlet, and team media-purpose catalogs include anticipated use cases that do not necessarily have active consumers. Preserve their generic attachment management where required for parity, but do not build bespoke previews or placement rules solely because a purpose value exists.

Contract caution:

- the current API authorization must be reviewed against the administrator-only registry boundary and any narrower form-scoped lookup retained for gauntlet authors;
- public gauntlet reads should return only the approved sponsor display projection needed for that gauntlet, not unrestricted registry records;
- Eventun does not appear to provide a dedicated sponsor-to-gauntlets aggregate endpoint;
- do not make full sponsor history a launch dependency.

## V1 Registry Structure

Default priority:

1. operational registry header and permission-aware actions;
2. compact sponsor search and sort;
3. sponsor records with approved identity/media cues;
4. selected sponsor detail and optional gauntlet relationship context;
5. mutation controls.

## 1. Registry Header

Content:

- `Sponsors` or `Sponsor Registry` title;
- concise operational description;
- sponsor count if useful;
- `Create Sponsor`.

The page should feel like part of gauntlet operations, not a public partner showcase.

## 2. Search and Sort

Required controls:

- search by sponsor name;
- search by description;
- sort A–Z;
- sort Z–A.

Do not add a global tier filter. Tier belongs to a specific sponsor–gauntlet relationship, not the sponsor record.

## 3. Sponsor Records

Record content:

- sponsor logo or approved media;
- name;
- short description when present;
- website/social-link indicators;
- color accents;
- view/edit action for administrators.

Design guidance:

- use sponsor colors as restrained accents;
- do not let sponsor styling override the Website V2 operational shell;
- omit absent fields rather than generating promotional claims;
- do not expose sponsor records through public entity cards or public search results.

## 4. Sponsor Detail

The permissioned detail capability is required for replacement parity.

Content:

- available approved media;
- sponsor name;
- description when present;
- website/social links;
- colors;
- relationship context when cheaply derivable;
- admin edit/delete affordances when authorized.

Sparse records use a compact factual layout. The route does not need public-profile SEO, sharing, or marketing modules.

## 5. Sponsor Relationships and Tier

Tier is specific to the sponsor's relationship with one gauntlet.

Rules:

- do not store or present tier as a global sponsor rank;
- do not show tier in public gauntlet or marketing presentation or use it to imply prestige;
- when relationship context is useful to an authorized user, label the tier beside the relevant gauntlet;
- treat tier as gauntlet-specific operational input currently used in deciding in-game advertising placement;
- do not over-specify public Website behavior from the current tier model because the game-client billboard system is expected to change.

Public gauntlet presentation may show an approved sponsor name or mark attached to that gauntlet. It should not link to the permissioned registry or expose operational tier/placement data.

Direct gauntlet billboard artwork does not by itself establish a reusable sponsor identity or a Website sponsor relationship. Do not infer a public sponsor name, profile, or sponsor strip from the image alone.

## 6. Sponsor Administration

Administrator actions:

- create sponsor;
- edit sponsor;
- delete sponsor;
- update media;
- update colors;
- update description;
- update social links.

Gauntlet creators do not gain registry or sponsor-record mutation rights. If the optional sponsor-association path remains in gauntlet authoring, expose only the scoped lookup and selection needed by that form.

Destructive actions must be separated from selection and ordinary editing. Failed writes must be explicit and recoverable.

## Game-Client Advertising Boundary

Current runtime data combines sponsor-owned assets carrying their relationship tier with gauntlet-owned assets assigned to the synthetic `Gauntlet` source at tier `0`. The resulting automatic placement behavior is not a stable Website V2 presentation contract.

A later game-client/content design pass should explore:

- authored sets of valid advertising locations per course;
- manual placement selection by organizers, or later by sponsors if a sponsor identity and approval workflow is designed;
- multiple billboard shapes and aspect ratios;
- trackside, vehicle-mounted, and holographic advertising treatments.

If sponsor identity later gains durable value beyond billboards, consider keeping the stable identity on `Sponsor` while owning tournament-specific creative and placement choices on the sponsor–gauntlet relationship. Do not assume one global sponsor billboard set fits every tournament.

Website V2 should not implement spatial placement authoring until that game-client model, asset rules, permissions, and preview/approval workflow are defined. The initial Website must preserve direct gauntlet `Billboard` upload with an explicit tileable control; sponsor-entity association is secondary. Preserve existing `WideBillboard` records as legacy data but do not offer that purpose for new uploads pending audit and coordinated cleanup.

## Auth and Permission States

| State | Behavior |
|---|---|
| Anonymous | no sponsor registry/detail navigation, search results, or route access; may see approved branding embedded in public gauntlet or marketing context |
| Logged-in player | same as anonymous unless the account is an administrator |
| Gauntlet creator | cannot browse the registry; can upload gauntlet-owned billboard assets and use the scoped optional existing-sponsor picker inside authorized gauntlet authoring |
| Administrator | can browse, inspect, create, edit, delete, and manage sponsor media/colors/links |

## Empty, Loading, and Error States

Required states:

- no sponsors;
- no sponsors matching search;
- sponsor not found;
- unauthorized or insufficient role;
- failed sponsor list/detail fetch;
- missing media;
- failed create/update/delete.

The unauthorized state must not leak record existence or sponsor fields.

## Responsive Behavior

Desktop may use a registry list/grid beside a selected-record panel. Tablet and mobile should stack the same administrative flow, preserve search and inspection, and keep destructive actions clearly separated.

## Indexing and Metadata

- exclude sponsor registry and detail routes from public sitemaps;
- emit no public sponsor-profile structured data or Open Graph identity pages;
- use authenticated application metadata and `noindex` behavior;
- do not leak sponsor descriptions, links, or media through unauthorized server rendering.

## Deferred Data and Workflow Questions

- whether sponsor-to-gauntlet history needs an aggregate endpoint;
- whether a future sponsor–gauntlet campaign record should own tournament-specific creative while `Sponsor` retains only stable identity/contact data;
- whether sponsor administration uses dedicated create/edit routes or in-page controls;
- which sponsor media purpose is preferred for registry rows and public gauntlet marks;
- whether a future sponsor representative can choose advertising locations directly;
- how billboard slot compatibility, asset approval, preview, and publication are modeled;
- whether a future public `/partners` route is justified by separately owned marketing content.

## Next Steps

- review Eventun list/detail authorization against the administrator-only registry boundary;
- design direct billboard upload in gauntlet create/edit as the primary advertising workflow;
- keep any sponsor-entity picker scoped to the gauntlet form and visually secondary;
- keep public gauntlet sponsor display limited to an approved relationship projection;
- defer billboard-placement design to a dedicated game-client/content pass.
