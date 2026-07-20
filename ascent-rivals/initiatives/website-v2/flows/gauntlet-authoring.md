# Ascent Rivals Gauntlet Authoring Flow

Date: 2026-07-15
Last reviewed: 2026-07-17
Status: Core authoring and hosting-surface boundary approved; implementation contract review open

## Related

- [[../unified-design]]
- [[../initial-release-scope]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../pages/gauntlets-index]]
- [[../pages/gauntlet-detail]]
- [[../sponsor-administration-handoff]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

## Goal

Define the initial Website V2 create/edit experience for the core Eventun gauntlet record.

This flow covers ordinary non-prize gauntlet authoring. It does not own bracket authoring, runtime stage operations, Accountun prize/reward workflows, or the future spatial billboard-placement system.

## Confirmed Form Direction

- use one sectioned form for both create and edit;
- do not use a step-by-step wizard;
- do not imply draft persistence, autosave, or resumability because Eventun has no approved draft-gauntlet contract;
- keep all sections reachable through page-local navigation;
- validate the whole record before the final create/update request;
- keep bracket authoring in a separate workspace after a core gauntlet exists;
- exclude all prize, reward, wallet, funding, claim, and payout fields/actions.

The one-form model supports frequent editing better than a wizard and avoids holding an apparently saved multi-step draft that the backend does not own.

## Working Routes

- `/gauntlets/create`;
- `/gauntlets/[id]/edit`.

Exact route naming may change during implementation, but create and edit should share the same section model, validation vocabulary, and field components.

## Authorization

- a gauntlet creator or administrator can create when the current role contract permits it;
- the owning creator or administrator can edit an existing gauntlet when the current backend contract permits it;
- authorization must be enforced before protected data is rendered and again by Eventun on mutation;
- an ordinary logged-in player cannot enter the form merely by navigating directly to the route.

## Hosting Surface Boundary

Website V2 remains the single initial surface for ordinary core gauntlet creation, editing, deletion, scheduling, competition-structure configuration, and gauntlet-owned media. It uses Eventun's player-facing domain authorization so the non-admin `gauntlet_creator` role and creator ownership remain meaningful.

The Eventun Extend App UI is the initial surface for operations deliberately restricted to studio administrators, including bracket generation/publication/repair and runtime result or stage-operation repair when those workflows are implemented. Those operations use the AdminService permission boundary rather than treating the Eventun-local creator role as an administrator grant.

Do not implement duplicate core create/edit forms in Website V2 and Extend. Moving core authoring wholesale to Extend would intentionally retire delegated gauntlet creation and requires a separate product and permission-model decision. A later bracket design may revisit whether a bounded creator-facing bracket workflow is justified, but that does not move the approved core form.

## Form Shell

The form should provide:

- clear `Create Gauntlet` or `Edit Gauntlet` identity;
- selected gauntlet identity during edit;
- a return path to the gauntlet directory or detail page;
- page-local links to all four sections;
- unsaved-change protection when leaving a dirty form;
- a top-level validation summary after an attempted save;
- one primary final `Create Gauntlet` or `Save Changes` action.

Desktop can use a sticky anchor-based section index. Mobile should use a compact labeled jump menu rather than turning the sections into sequential screens. Do not use tabs that hide sections of the one-page form. Terminal-style prefixes may be decorative, but the visible and accessible labels remain `Core Details`, `Competition Structure`, `Branding and Advertising`, and `Review and Save`.

## Section 1: Core Details

Purpose: establish the competition identity and operating region.

Current fields:

- title;
- subtitle;
- ticker/announcement;
- region.

Guidance:

- use plain labels and concise help text;
- keep the region visible because it affects session operations;
- do not place branding colors in this section merely because the current form does.

## Section 2: Competition Structure

Purpose: define the qualifier and scheduled competition structure that actually exists.

Current concerns:

- qualifier scoring/stat configuration;
- zero or more qualifier windows;
- zero or more stages;
- stage schedule;
- entry requirement;
- race mode;
- competitor and lobby bounds;
- stage circuit matches, courses, laps, and heats;
- stage win/loss prerequisites where supported;
- team allocation fields after the team contracts ship.

Rules:

- qualifiers and stages are independently optional;
- do not insert empty placeholder phases into the saved record;
- require qualifiers only when a stage explicitly uses qualifier-based entry;
- keep cross-section scheduling and min/max validation visible near the affected fields;
- use `Qualifier`, `Stage`, `Final`, and `Bracket` according to the approved competition terminology;
- do not add bracket graph generation, seeding, byes, publication, or repair to this core form.

Repeated qualifiers, stages, and circuit entries should support explicit add/remove actions. Reordering must not be offered unless the backend semantics and identifiers safely support it.

## Section 3: Branding and Advertising

Purpose: configure the gauntlet's visual identity and campaign-specific media.

Structure:

1. primary and secondary colors;
2. general gauntlet media grouped by use;
3. direct advertising uploads;
4. advanced reusable sponsor association.

Treat the configured media-purpose values as attachment labels, not as proof that each value has a distinct active consumer. For the initial release, general gauntlet media uses a shared labeled thumbnail, upload, replacement, ordering, and removal treatment. Do not build purpose-specific presentation or metadata controls unless a current Website or game-client consumer requires them.

Direct advertising is the primary creator path:

- upload gauntlet-owned `Billboard` assets;
- expose an explicit `Tile across ribbon placements` control backed by media metadata `Tileable = true`;
- use a square-oriented single-panel preview and, when tileable, show three adjacent copies of the same artwork as a lightweight ribbon preview;
- show upload status, priority/order, replacement, and removal;
- request operation-scoped upload intents immediately before final save, allowing at most 10 JPEG/PNG/WebP images of at most 10 MB each per submission;
- upload directly to R2, verify each transfer, preserve form state on failure, and retry only failed files without adding dimension extraction, aspect-ratio classification, or billboard-slot matching;
- do not require a reusable sponsor record, sponsor name, or relationship tier.

`WideBillboard` is not a normal new-upload choice. Preserve an existing record without silently converting or deleting it, label it as legacy in edit mode, and defer its removal until live Eventun data and the unused game-client collection are reviewed together.

Advanced sponsor association:

- keep the existing sponsor-entity picker behind an `Advanced` disclosure;
- scope lookup to this form without granting access to the administrator sponsor registry;
- show selected sponsor identity and relationship tier;
- preserve existing sponsor associations and tiers during edit;
- explain that this path uses reusable sponsor-owned assets, while direct uploads belong only to this gauntlet.

The initial form assumes the current predominantly square billboard workflow and does not select physical billboard locations. Multiple shapes, uploaded-dimension metadata, aspect-ratio matching, trackside/vehicle placements, holograms, slot compatibility, and sponsor self-service remain part of the later game-client advertising design.

## Section 4: Review and Save

Purpose: expose blockers and provide one deliberate mutation point without becoming a separate wizard step.

Content:

- concise summary of core identity, qualifier/stage counts, schedule range, region, and media counts;
- warnings for unusual but allowed structures;
- linked validation errors grouped by section;
- final create/update action;
- explicit progress and success/failure state.

This section is part of the same page. It does not hide earlier fields, claim that an intermediate draft exists, or require a forward/back step sequence.

## Validation Behavior

- client validation provides immediate feedback, but Eventun remains authoritative;
- place field errors beside the field and also provide a linked error summary after save is attempted;
- section navigation should indicate which sections contain errors;
- do not keep a section collapsed while it contains an unresolved error;
- focus the first invalid field after a failed save while preserving access to the complete summary;
- preserve current cross-field rules such as qualifier overlap, qualifier-to-stage timing, qualifier-count scoring, required qualifier presence, and competitor/lobby bounds unless the backend contract changes;
- never expose or validate excluded prize/reward fields.

## Media Upload Behavior

The current workflow uploads media before the final gauntlet mutation. Website V2 must therefore show the difference between upload completion and gauntlet save completion.

Requirements:

- show per-file upload status and recoverable errors;
- disable final save while required uploads are unresolved;
- retain successfully uploaded media references in local form state after a gauntlet save failure;
- allow retry or removal without re-entering unrelated form data;
- do not claim the upload and gauntlet mutation are one atomic operation unless a later backend contract makes that true.

Orphan cleanup and upload expiration policy require an implementation-time contract review.

## Create and Edit Behavior

Create:

- initialize empty qualifier, stage, sponsor-association, and media collections;
- allow a structurally valid gauntlet with no qualifiers or no stages when Eventun accepts that composition;
- send one final create request after successful validation and uploads;
- on success, route to `/gauntlets/[id]` with a clear creation-success state.

Edit:

- prefill the complete editable core record;
- preserve stable ids and existing sponsor/media relationships;
- warn before leaving with unsaved changes;
- keep delete separate from the normal save action in a clearly labeled danger area;
- do not expose published bracket graph mutation in the core edit form;
- on success, route to `/gauntlets/[id]` with a clear update-success state.

The destination detail read must be revalidated or otherwise refreshed so the operator reviews the saved version rather than stale cached data. The detail page remains the canonical manual-review checkpoint and exposes the permission-aware `Edit Gauntlet` action when another change is needed.

## Failure States

Required handling:

- authentication expired;
- role or ownership no longer authorizes the action;
- source gauntlet not found;
- source record changed or mutation conflict, if Eventun can report it;
- validation rejected by Eventun;
- media purpose or upload failure;
- sponsor lookup unavailable while the advanced section is in use;
- create/update/delete failure.

Mutation failures must preserve entered form state wherever safe and provide a specific retry path.

## Responsive and Accessibility Requirements

- all sections remain keyboard reachable;
- the section index exposes current section and error state without color alone;
- repeated-item add/remove actions have specific accessible names;
- destructive removal is not adjacent to primary save without separation;
- date/time fields expose timezone and unambiguous formatted values;
- dense stage and circuit fields stack into labeled groups on mobile rather than relying on horizontal table context.

## Separate and Deferred Work

- administrator-only bracket generation, publication, seeding, byes, and audited repair in the Eventun Extend App UI;
- administrator-only runtime stage-session and result-repair operations in the Eventun Extend App UI;
- draft gauntlets, autosave, and resumable authoring;
- spatial billboard-slot selection and game-client preview;
- sponsor representative identity and self-service approval;
- all Accountun-related prizes and rewards.

## Open Questions

- Which existing media-purpose labels and metadata fields have active consumers, and which can be retired during a later media audit?
- Does Eventun need optimistic-concurrency/version support before multi-operator editing is safe?

Accepted upload tradeoff: an abandoned or failed form may leave an unreferenced object. Use auditable server-generated keys, but do not add an initial pending-object database or automated cleanup service at the current traffic level.

## Next Steps

- create a constrained desktop and mobile form mock using these four sections;
- review current Eventun mutation and media-upload contracts against the failure model;
- map implemented post-team allocation fields into Competition Structure;
- keep bracket authoring linked but structurally separate.
