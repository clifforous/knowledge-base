# Ascent Rivals Sponsor Administration Handoff

Date: 2026-04-14
Updated: 2026-07-20
Status: Approved boundary; Eventun Extend App implementation required before Website V2 cutover

## Related

- [[unified-design]]
- [[information-architecture]]
- [[initial-release-scope]]
- [[delivery-plan]]
- [[route-api-matrix]]
- [[pages/gauntlet-detail]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[flows/gauntlet-authoring]]

## Decision

Website V2 has no sponsor registry, sponsor detail, sponsor create/edit/delete, or sponsor-media administration routes.

All sponsor identity and media administration moves to the Eventun Extend App UI before Website V2 replaces Ascentun. This is an approved parity exception: the capability is preserved, but its destination is the administrator operations application rather than the public/player website.

This boundary is appropriate because sponsor CRUD is administrator-only operational work. It does not need the public Website shell, Steam player navigation, public metadata, or responsive marketing presentation.

## Website V2 Boundary

Website V2 retains only sponsor behavior required in a gauntlet context:

- public gauntlet detail may render an approved sponsor name or mark from a bounded gauntlet display projection;
- public pages do not expose relationship tier, placement rules, registry fields, or a sponsor profile link;
- authorized gauntlet creators may use a form-scoped existing-sponsor selector in the optional advanced association section;
- the selector returns only stable id, name, one optional preview, and fields required to preserve the selected relationship;
- direct gauntlet-owned `Billboard` upload remains the primary advertising workflow and does not require a sponsor record;
- no Sponsor group appears in Website global search, navigation, metadata, sitemap, or account routes.

Legacy `/sponsor`, `/sponsor/[id]`, create, and edit URLs do not become Website V2 pages. Do not redirect public traffic to an authenticated AccelByte Admin Portal surface. Administrators enter sponsor operations through the normal Eventun Extend App/Admin Portal navigation.

## Eventun Extend App Scope

The Eventun Extend App must support:

- administrator-authorized sponsor list and detail;
- create, edit, and delete or dependency-blocked retirement behavior;
- optional description, primary/secondary colors, website, Discord, X, and Twitch links;
- media list, upload, preview, purpose, priority/order, replacement, and removal;
- preservation of existing media ids, metadata, URLs, gauntlet relationships, relationship tiers, and legacy `WideBillboard` records;
- explicit loading, empty, validation, authorization, conflict, dependency, and retry states;
- generated Admin API clients and the existing Eventun Admin permission boundary.

The initial UI should remain operational and compact. It does not need the Website V2 Terminal Ops visual system, sponsor marketing pages, spatial billboard placement, sponsor self-service, or campaign management.

## Required Eventun Contract Work

Before exposing sponsor administration in the Extend App:

- add administrator-authorized sponsor list and detail operations or an equivalent reviewed Admin projection; retain the existing client/game reads until their consumers are separately reviewed;
- make create, update, and delete atomic rather than issuing an untransactional batch of independent statements;
- correct the current delete path, which references a nonexistent `gauntlet_media.sponsor_id` column;
- define deletion behavior for gauntlet relationships and historical Accountun/prize references. Do not partially delete media or relationships and then return failure;
- return typed validation, conflict, not-found, dependency, and authorization failures without raw database details;
- return an empty media collection for a sponsor with no media rather than a synthetic null media item;
- validate and normalize sponsor name, optional colors, URLs, media purposes, priorities, and supported metadata at the authoritative boundary;
- preserve unknown but valid existing media metadata during an edit even when the initial UI does not expose a generic JSON editor.

Sponsor delete is not a Website V2 requirement. If safe destructive behavior is not settled before cutover, the Extend App may block deletion for referenced sponsors and support create/update/media management first, provided existing records remain maintainable and the limitation is explicit.

## Sponsor Media Upload Dependency

The Eventun Extend App runs in the administrator browser and must not receive object-store credentials. Sponsor media therefore requires an administrator-authorized upload boundary before cutover.

Review these implementation choices in order:

1. reuse an existing media upload service only if it can issue bounded administrator-authorized upload intents without importing Accountun prize/wallet responsibilities;
2. otherwise add an Eventun Admin upload-intent operation backed by server-held object-store credentials;
3. do not retain an undocumented Ascentun upload-only dependency after Ascentun retirement.

The selected contract must:

- require Eventun Admin authorization;
- generate the object key server-side and bind the intent to sponsor ownership and an allowed media purpose;
- allow only reviewed image MIME types and file-size/count limits;
- use a short expiry and direct browser-to-object-store transfer;
- return the stable media URL and identifier required by the sponsor mutation;
- preserve existing externally hosted or legacy media URLs during edits;
- define best-effort cleanup or an auditable orphan-media process for abandoned uploads and removed assets;
- verify that uploaded media resolves in the matching development and production environments and remains usable by the game/public gauntlet projections.

For create, the simplest recoverable sequence is to create the base sponsor record first, then upload and attach media. An upload failure leaves an editable sponsor rather than losing all form work or requiring a client-owned provisional sponsor id.

## Advertising Boundary

Current advertising has two independent ownership paths:

- reusable `sponsor_media` administered in the Extend App;
- tournament-specific `gauntlet_media` administered in Website V2 gauntlet create/edit.

Do not flatten either path during cutover. `Billboard` remains the normal initial purpose, `Tileable` metadata indicates repeatable ribbon treatment, and existing `WideBillboard` records are preserved as legacy data without offering that purpose for new uploads until the game-client audit is complete.

Tier remains a sponsor–gauntlet relationship value used by current advertising placement logic. It is not a global sponsor rank and does not appear in public Website presentation.

## Cutover Acceptance

Website V2 and the current Ascentun sponsor pages may be retired only after the matching Eventun Extend App environment demonstrates:

- authorized list, detail, create, update, and the approved delete/block behavior;
- sponsor image upload, preview, attachment, replacement, and removal;
- preservation of existing sponsor records, media, metadata, gauntlet relationships, tiers, and legacy media purposes;
- correct generated-client behavior and Eventun Admin authorization;
- no partial database mutation on a failed write;
- successful consumption of retained sponsor relationships/media by gauntlet authoring, public gauntlet display, and the game client where applicable.

## Deferred

- sponsor self-service or sponsor representative accounts;
- sponsor–gauntlet campaign entities;
- public sponsor profiles or a `/partners` route;
- physical billboard-slot selection, shape matching, vehicle placements, and holographic treatments;
- dimension-derived placement and automatic creative approval;
- a complete sponsor-to-gauntlet history experience.
