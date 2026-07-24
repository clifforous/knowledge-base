# Ascent Rivals Website V2 Route and API Matrix

Date: 2026-07-17
Status: Initial route groups, integration boundaries, and shared support contracts approved; implementation contract gaps remain tracked by route group
Last reviewed: 2026-07-23

## Related

- [[unified-design]]
- [[initial-release-scope]]
- [[information-architecture]]
- [[non-functional-baseline]]
- [[delivery-plan]]
- [[ascent-rivals/initiatives/website-v2/pages/homepage]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlets-index]]
- [[ascent-rivals/initiatives/website-v2/pages/gauntlet-detail]]
- [[ascent-rivals/initiatives/website-v2/pages/player-directory]]
- [[ascent-rivals/initiatives/website-v2/pages/player-profile]]
- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]
- [[ascent-rivals/initiatives/website-v2/pages/teams-index]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]
- [[flows/authentication]]
- [[flows/gauntlet-authoring]]
- [[flows/team-lifecycle]]
- [[ascent-rivals/system/eventun/api|eventun-api]]

## Purpose

Map each approved Website V2 route to its authoritative source, server-side integration, browser-visible data, authorization behavior, and required contract work.

This is a product and integration map, not a frozen endpoint-name or TypeScript-interface specification. Exact operation names and generated types must be verified against the implementation revision used by each slice.

## Approved Integration Boundary

- the browser does not receive Eventun or AccelByte service credentials, player access/refresh tokens, or generated clients configured to call those services directly;
- server-only Next.js data functions use generated Eventun gateway clients and controlled AccelByte integrations;
- Server Components obtain initial public or authenticated data and pass explicit browser view models only to the client components that need interaction;
- cached public reads, private request-time reads, and mutation invalidation follow [[non-functional-baseline]];
- same-origin Server Actions or route handlers own authenticated refreshes and mutations that originate in the Website;
- Eventun remains authoritative for metrics, historical attribution, visibility, ownership, domain authorization, and mutation validation;
- the Next.js layer may authenticate, cache, compose a bounded number of authoritative reads, remove unrendered fields, normalize transport failures, and map domain responses into page presentation;
- do not copy backend domain rules into React components or treat a rendered control as authorization evidence;
- direct browser upload is allowed only through a bounded signed URL or equivalent upload contract; the Website server obtains the authorization and attachment intent without proxying large media bodies unnecessarily;
- AccelByte course metadata reaches the browser through a Website server integration or an approved Eventun projection, never through browser-held AccelByte service credentials;
- prefer domain-neutral Eventun read models where other trusted consumers may reasonably reuse the semantics; keep route-only composition and display labels in Website V2.

## Transport and Type Rules

- keep generated gateway clients and raw transport models in a server-only integration package;
- do not pass a complete generated record to the browser merely because it is available;
- define explicit public, private-overlay, form-prefill, and mutation-input projections according to the route contract;
- preserve null, absent, zero, false, timestamp, unit, and enum semantics during projection;
- prevent secrets, internal ids, raw event evidence, replay/session keys, client versions, permission internals, and unrendered configuration from crossing the browser boundary;
- use route templates and normalized failure categories in logs rather than request bodies or entity/player identifiers;
- normalize dependency errors into deliberate unavailable, retryable, validation, authorization, conflict, and unexpected-failure states;
- keep initial compact collections in one response for client-side search/filter/sort/display pagination until measured limits justify a different contract.

## Repository-Authored Route Group

| Route | Authoritative source | Server behavior | Browser behavior | Contract status |
|---|---|---|---|---|
| `/` | Repository-authored typed content and approved media; optional Eventun gauntlet discovery read | Static marketing page; independently cache an optional bounded race-network item; authenticated ownership/personal context must not block the page | Marketing interaction and optional client enhancement only | Repository content convention approved; optional gauntlet teaser reuses the discovery contract |
| `/about` | Repository-authored verified studio, mission, team, and recognition content | Static by deployment | No product-data client fetch required | Approved; content accuracy review required during migration |
| `/brand` | Repository-authored brand guidance and downloadable assets | Static by deployment; serve approved assets with stable URLs | Download interactions only | Approved; visual guidance must be refreshed after the design system is finalized |
| `/events` | Repository-authored typed editorial event collection | Static by deployment; sort and render current/historical editorial entries | Optional local filtering only if event volume justifies it | Approved; no CMS or Eventun gauntlet substitution |
| `/events/[slug]` | Repository-authored typed event detail and approved media/video links | Static by deployment; generate factual metadata/social card | Ordinary media/link interaction | Approved; verified promotional prize copy may exist here without data-driven Accountun integration |
| `/game` | None approved beyond homepage content | No route in the initial release | None | Explicitly deferred until distinct material content exists |

### Homepage Data Boundary

The homepage may consume at most one optional race-network module backed by the same compact public gauntlet discovery response as `/gauntlets`. Selection uses the approved deterministic current/upcoming/recent fallback or code-authored editorial fallback. Failure or absence omits the module and never blocks the marketing shell.

Do not add independent homepage leaderboard, telemetry, system-log, or multi-entity dashboard contracts.

## Gauntlet Route Group

| Route | Authoritative source | Server behavior | Browser behavior | Private/authorized overlay | Contract status |
|---|---|---|---|---|---|
| `/gauntlets` | Eventun `GET /v1/public/gauntlet/discovery`, using identity and complete occurrence facts; accept the preceding response and deployed `0e4d656` replacement while ignoring transport time and redundant presentation fields | Cache only the normalized factual collection with ordinary source-data TTL/invalidation; after the cached read resolves, obtain one fresh Website-server timestamp outside the shared cache and derive the initial presentation snapshot | Hydrate from the exact server presentation timestamp, advance time monotonically with suspension recovery, and recalculate Current/Upcoming/Past, active/next/latest, ordering, scope, and Schedule locally at the nearest boundary, bounded fallback, visibility recovery, and replacement data; never refetch only because time passed | Optional participation summaries compose separately and must not make the public collection private | Eventun removal is deployed in shared development through `0f2a1de`; the compatible Website consumer is reviewed, verified, and committed as `ar-web` `7d1d00c` but not deployed |
| `/gauntlets/[id]` | A compact domain-neutral Eventun public detail projection for stable identity, approved media, normalized scoring configuration, occurrence facts, qualifiers, and stage/circuit structure; current/exact fields, factual StageRuns, standings/results, and optional sponsor display remain independent reads | Resolve canonical existence before streaming; cache stable detail separately from short-cache field, StageRun, standings, and result modules; omit prize/reward data and unavailable optional modules independently | Derive schedule-relative presentation from occurrence facts and the Website clock; use factual StageRun status only; expose explicit standings/result refresh and bounded local presentation | Personal rank/qualification/participation and ordinary edit/delete permissions compose request-time; admin-only bracket/runtime mutation remains outside Website V2 | Primary detail plus factual StageRun timeline are implemented, fixture-verified, and committed as `ar-web` `f06bc6d3f093cfabb0c77b9c8b4e951d5369d602`; standings, fields, and accepted results remain typed deferrals. The Website revision is not deployed |
| `/gauntlets/create` | Eventun player-facing core gauntlet mutation, media-purpose lookup, signed upload, scoped sponsor lookup | Authenticate server-side; obtain form options and signed upload intent; submit one authoritative create mutation; invalidate collection/entity tags after success | Form state, client validation, direct signed media transfer, retry, and unsaved-change handling | Route requires `gauntlet_creator` or administrator according to Eventun; ordinary players cannot render protected form data | Existing mutation/upload contracts require final post-team field and failure-model review |
| `/gauntlets/[id]/edit` | Eventun authorized full core-edit record, mutation, delete, media, and scoped sponsor reads | Enforce creator ownership/role or administrator access before prefill; recheck in Eventun; invalidate detail/collection/dependent tags after success | Prefilled form, direct signed uploads, preservation of existing ids/media/relationships, conflict and retry handling | Owning creator with current role or administrator | Existing contracts require optimistic-concurrency and post-team field review; bracket graph mutation excluded |

### Gauntlet Detail Read Decomposition

Do not force every gauntlet module into one cache and refresh lifecycle.

Use these logical read classes even if implementation later combines compatible operations internally:

1. Public detail/configuration
   - identity, title/subtitle/ticker, colors, region, approved media, bounded scoring model,
     qualifiers, stages/circuits, and normalized occurrence schedule;
   - do not include current published field-owner count or racer-slot count; obtain current values
     from the current-field projection and historical values from the exact StageRun-field
     projection;
   - tagged entity cache with ordinary source-data TTL and mutation invalidation; derive
     time-relative presentation from cached occurrences rather than refetching at a boundary.
2. Standings and accepted results
   - existing overall and qualifier standings only for a supported player-owned qualification
     model and a recognized bounded public scoring metric;
   - team-owned qualification requires an owner-aware public standings projection; omit the module
     when that projection or a supported scoring configuration is unavailable;
   - accepted result summaries use an explicit player-or-team owner variant;
   - exact StageRun identity selected by the public timeline rather than an empty or browser-inferred
     run id;
   - StageRun status is a factual bounded projection such as pending/not-started, in progress,
     completed, cancelled, failed, or deferred; it never derives `Upcoming` or `Open` from the
     current clock;
   - short public cache and explicit refresh where useful.
3. Optional sponsor display
   - a relationship-scoped public sponsor identity projection may be added after the core detail
     route;
   - its absence does not block the primary detail implementation or canonical page existence;
   - never consume the public sponsor registry, relationship tier, or billboard-placement data.
4. Published bracket and public match state
   - published graph, seeds/byes only when public, match state, and accepted results;
   - new contract tied to the bracket implementation; no mutation controls or repair evidence.
5. Private player overlay
   - personal participation, qualification, placement, invitation/eligibility facts only when approved, and permissioned core actions;
   - request-time player-authenticated read, never shared cached.

An unavailable standings, bracket, sponsor, or personal module must fail independently where the remaining public detail is still meaningful.

### Approved Public Detail Contract Direction

Add a compact domain-neutral `GET /v1/public/gauntlet/{gauntlet_id}` read rather than consuming the
legacy `GET /v1/gauntlet/{gauntlet_id}` response. The primary projection contains:

- stable public identity, title/subtitle/ticker, region, validated optional colors, and bounded
  approved gauntlet media;
- complete qualifier and stage occurrence facts with exact identity, deterministic display order,
  start/end timestamps, and explicit timing basis;
- stage race mode, visitor-facing entry category, and ordered circuit rows with course-code
  fallback plus presence-aware positive lap/heat settings;
- a presence-aware qualification model with explicit player/team ownership and a bounded public
  scoring-metric enum. The initial enum may support only deliberately verified metrics; unknown or
  unsupported source configuration remains unspecified and prevents standings consumption.

The primary projection excludes creator identity, generic participant count, field-owner/slot
capacity, raw authoring/admission/runtime configuration, sponsor relationships, prize/reward data,
and arbitrary media metadata.

Current field composition and counts come from
`GET /v1/public/gauntlet/{gauntlet_id}/stage/{stage}/field`. Historical field composition and
counts come from the exact StageRun-field read. The StageRun collection retains scheduled start,
presence-aware actual start/end, and explicit result availability, but replaces clock-derived
`UPCOMING`/`OPEN` lifecycle values with a bounded status mapped only from persisted runtime facts.
Website V2 derives Current/Upcoming/Past and other schedule-relative emphasis from occurrence facts
and its own request/hydration clock.

The new detail RPC and every existing specific public-gauntlet route require dispatch tests at the
generated gateway boundary. Tests must prove that the parameterized `/{gauntlet_id}` route cannot
capture `/v1/public/gauntlet/discovery`, current-field, exact StageRun-field, StageRun-list, or
exact-result routes, and must assert the intended operation for both valid specific paths and an
ordinary detail UUID.

Malformed identifiers remain sanitized `InvalidArgument`; an absent public gauntlet is `NotFound`;
infrastructure failures retain sanitized `Internal` or `Unavailable`. The legacy detail handler's
conversion of every database error to `NotFound` is tracked as a separate cleanup and is not a
reason to consume that endpoint.

Eventun T03D implements the approved public-detail contract and factual StageRun lifecycle from the
G03 baseline and is reviewed and committed as `0f2a1de`. Generated route-order tests prove the
parameterized detail route does not capture the specific public-gauntlet routes. The unsafe legacy
detail error mapping remains a separate cleanup. The owner reports the Eventun dependency and
ordered post-development delta deployed in shared development; this does not implement or deploy the
Website route.

### Gauntlet Contract Gaps

- verify the compatible Website discovery consumer against the deployed `0e4d656`-and-later
  development response and representative media; it ignores transport time plus redundant
  snapshot-derived timing fields when reading an older response;
- review and deploy the compatible Website discovery consumer;
- review and live-verify the locally implemented Website detail consumer against deployed Eventun
  T03D `0f2a1de`; it does not consume or normalize the broad legacy response;
- constrain legacy overall/qualifier standings to recognized player-owned qualification models,
  and add a separate owner-aware public projection before showing team-owned qualification;
- keep current and historical field capacity in their respective field projections; never conflate
  owners, slots, occupants, admissions, or generic participants;
- retain typed player/team accepted results; do not label a represented team's placement as the
  occupant's individual finish;
- treat relationship-scoped sponsor display as an optional follow-on after core detail;
- define the public published-bracket graph and match-state read when bracket contracts ship;
- verify a bounded personal-overlay read instead of making the browser join several player-gauntlet calls;
- review post-team allocation, field-publication, and stage fields before freezing create/edit projections;
- determine optimistic-concurrency/version behavior for edits;
- accept occasional unreferenced uploads at the initial traffic level, use auditable server-generated keys, and revisit cleanup only if measured growth or cost warrants it;
- keep sponsor lookup scoped to authorized gauntlet authoring without exposing the administrator sponsor registry;
- verify mutation-driven invalidation signals for detail, discovery, standings, and dependent player/team histories.

## Pilot Route Group

| Route | Authoritative source | Server behavior | Browser behavior | Private/authorized overlay | Contract status |
|---|---|---|---|---|---|
| `/players` | Eventun public pilot identity, team summary, and approved shallow career context | Return one cached compact collection; exclude only source-classified bot, test, and internal identities; strip profile-detail and private fields before serialization | Client-side name/team search, approved sorts, and display pagination/progressive reveal over the complete collection | None required; an own-profile link is ordinary navigation | Existing `GET /v1/player` is a candidate while measured payload cost remains acceptable; otherwise add a compact domain-neutral directory projection |
| `/players/[id]` | Eventun pilot career and pilot-course career projections, current records/ranks, bounded match history, and gauntlet participation/results; public course metadata originates in AccelByte through the approved Eventun projection | Compose independently cached public modules; expose only the approved public headline career fields; filter history through the public course projection; preserve missing-value semantics; remove raw evidence and unrendered identifiers; return not found for an unusable public identity | Section navigation, local table/chart controls, and exact-value accessible alternatives; no browser N+1 joins | Request-time own-profile team/account actions and any later approved private career-detail overlay; no wallet, exact MMR, or rank history | Serving reads are implemented and locally rehearsed; shared use waits for the coordinated environment cutovers. Compact three-entry gauntlet history and an Ascension Rate aggregate remain required, and the own-profile contract depends on the implemented team model |

### Pilot Profile Read Decomposition

Keep these as logical read classes even if compatible operations are combined internally:

1. Identity and career summary
   - public pilot identity, current public team summary, Matches, Podiums, Podium Rate, and
     Ascension Rate with exact numerator and denominator counts;
   - ordinary tagged public cache.
2. Course career and placements
   - public-course career rows, current record context, exact category rank/time, and the values needed for an optional normalized gap-to-record view;
   - public cache aligned with course-record freshness.
3. Recent races
   - newest 100 server-backed multiplayer races on `published` or `archived` courses;
   - short public cache; omit session/match ids, replay keys, client versions, hidden-course rows, and unrendered fields before the browser boundary.
4. Gauntlet history
   - the three gauntlets with the player's latest real public participation, derived from real
     qualifier, match, or accepted-stage evidence;
   - no invitations, eligibility, group assignment, or status-only rows.
5. Own-profile overlay
   - request-time team and account actions for the viewed authenticated pilot;
   - overall total and average Circuit Points, play time, credits/economy, detailed combat/objective
     totals, achievements, and medals only if that reversible private-detail boundary is later
     approved and supported by a purpose-built authorized response;
   - unavailable or unauthorized state must not alter the shared public profile response.

Identity/career, course performance, recent races, gauntlet history, and the private overlay may fail independently where the remaining profile still has factual value. The server may execute bounded compatible reads in parallel; the browser must not reproduce their joins.

### Pilot Contract Gaps

- finalize the reviewed Eventun career, pilot-course, current-record/rank, and bounded-history contracts, then require deployed production behavior before launch use;
- verify that the directory source supplies explicit public identity classification; do not infer bots, test accounts, or internal identities from naming or activity;
- add a compact directory projection when the measured `GET /v1/player` response is no longer appropriate for a full client-side collection;
- define a public recent-races projection that applies course visibility, maps race-mode labels, preserves missing versus zero/false, and strips internal identifiers before serialization;
- add the compact player-gauntlet-history read defined in [[ascent-rivals/initiatives/website-v2/pages/player-profile]] instead of issuing one request per gauntlet;
- add an Eventun-owned Ascension Rate aggregate over eligible Ascension-mode heats; count
  `Ascended` and podium `Placed` outcomes once per heat and return the exact successful/eligible
  counts with the rate;
- finalize the own-profile team/action overlay only after the team implementation is reviewed;
- if private career detail or recognition is approved later, use a purpose-built authorized
  response rather than forwarding broad progression, medal, or economy responses or hiding
  fields in the browser;
- define invalidation or bounded freshness for career, records, recent races, gauntlet results, and team identity changes.

## Course Route Group

AccelByte Cloud Save remains authoritative for course configuration and publication state. Eventun should own the reusable controlled cache and public-safe projection because course visibility also governs leaderboards, recent races, player-course statistics, search, metadata, and game-facing reads. Website V2 consumes that Eventun projection server-side rather than implementing a separate publication classifier in Next.js.

| Route | Authoritative source | Server behavior | Browser behavior | Private/authorized overlay | Contract status |
|---|---|---|---|---|---|
| `/courses` | AccelByte Cloud Save course configuration through Eventun's public-safe course projection | Return one cached compact collection of `published` courses; never serialize hidden classifications | Render the complete small directory and navigate each entry to `/courses/[code]`; no page-local search, result count, archive scope, sort, selection state, or pagination | None | Current `GET /v1/course` is not safe to consume unchanged because its derived `active` value collapses retired and unreleased states; revise it or add a purpose-built domain-neutral projection |
| `/courses/[code]` | AccelByte course metadata through Eventun; Eventun category leaderboard/current record; Eventun player-specific placement | Resolve the stable course code; return not found for hidden/unknown courses; cache stable metadata separately from short-cache selected-category records; preserve the category query in shareable state | Category switching, exact leaderboard table, bounded top-N gap visualization, accessible row detail, and public pilot links | Request-time logged-in pilot rank/time for the selected course/category, including placement outside the public top-N | Leaderboard reads are implemented and locally rehearsed; final public-board/private-placement presentation requires contract verification and deployed production behavior |

### Course Read Decomposition

1. Public course catalog/detail
   - stable code, display metadata, approved media, default laps, and only `published` or explicitly `archived` public lifecycle values;
   - tagged public cache with one visibility implementation shared by directory, detail, history filtering, search, metadata, and sitemap generation.
2. Public records and leaderboard
   - selected player-facing category, exact rank/time, public pilot identity/link, loadout value, record context, returned-population size, and as-of time where available;
   - short public cache or explicit refresh without implying live telemetry.
3. Personal placement
   - authenticated pilot rank and time for the selected course/category even when absent from the returned top rows;
   - request-time private overlay that does not make the public board private.

The initial course index does not include cross-course record summaries. Course metadata failure, leaderboard failure, and personal-placement failure require distinct page states on the routes that consume them.

### Course Contract Gaps

- revise `GET /v1/course` or add a purpose-built Eventun public projection that reads authoritative AccelByte feature metadata, returns only `published` courses to directory/search consumers, supports `archived` detail only if deliberately retained for historical links, and treats hidden detail as not found;
- ensure the same public projection filters player recent-race history, player-course rows, global search, route metadata, canonicals, and sitemaps;
- finalize current-record and player-rank serving contracts and require deployed production behavior before launch use;
- verify the public leaderboard projection exposes exact category, rank, time, public pilot identity, loadout value, bounded population context, and useful as-of metadata without raw source-policy or internal identifiers;
- verify a small authenticated personal-placement response for ranks outside the public top-N;
- preserve the approved player-facing Race, Time Trial, `3K Class`, and `10K Class` mappings while keeping server/client authority and validation terminology out of public copy;
- defer checkpoint geometry, sector comparison, whole-population distributions, percentiles, and record-history timelines until stable source contracts exist;
- define bounded record/cache freshness or invalidation from accepted Eventun result updates.

## Team Route Group

This route group is provisional until the Eventun [T00–T03 team work](../teams-and-team-gauntlets/delivery-plan.md) is implemented and reviewed. It fixes Website ownership, public/private separation, and required semantics without freezing legacy endpoint names, numeric designations, or speculative statistics fields.

| Route | Authoritative source | Server behavior | Browser behavior | Private/authorized overlay | Contract status |
|---|---|---|---|---|---|
| `/teams` | Eventun public team browse projection | Return one cached complete compact collection of active teams with stable identity, name/tag, membership mode, approved bounded media/colors, status, and active-member count; do not embed management queues, performance modules, or rosters | Client-side name/tag search, optional membership filter, approved sorts, and display pagination/progressive reveal over the complete collection | Request-time current-team and create-eligibility summary composes separately; it must not make the directory private | T03 reusable public summary contract approved; implementation pending |
| `/teams/create` | Eventun authenticated team creation, approved media-purpose lookup, and signed upload | Authenticate and obtain eligibility/form options server-side; submit one authoritative create mutation; refresh current-player state; invalidate team collection/detail tags; route to the new team management context | One form with local validation, direct signed media upload, retry, and unsaved-change handling | Eligible authenticated player; administrator create-on-behalf remains an explicit post-T01 contract decision | Final create fields, ownership rule, typed result, conflict behavior, and media attachment lifecycle require T01/T02 review |
| `/teams/[id]` | Eventun public team detail/active roster; T03 summary, current-roster comparison, represented-result history, and owner-aware gauntlet history | Cache identity/roster independently from each fact-backed module; compose authenticated viewer state request-time; execute membership mutations through same-origin actions and revalidate affected team/player collections | Local roster and leaderboard controls, exact pilot links, public membership label, and only the action returned for the current player state | Current relationship, exact pending action, and allowed actions; no public pending queues, capability internals, membership intervals, or audit evidence | T03 reusable reads approved; implementation and measured-data verification pending |
| `/teams/[id]/manage` | Eventun authorized management snapshot, pending queues, team mutation contracts, media-purpose lookup, and signed upload | Reject unauthorized access before prefill; recheck every mutation in Eventun; keep independently saveable management sections; invalidate team, player, pending, search, and relevant statistic tags after success | Team info/media forms, roster/capability controls, invite/request queues, direct signed uploads, confirmations, conflicts, and retries | Explicit effective capabilities and ownership from Eventun; numeric designation or a visible title is not authorization evidence | T01/T02 replacement contracts required; management fields and capabilities must be reviewed after implementation |

### Team Read and Mutation Decomposition

1. Public team directory
   - stable identity, name/tag, public membership mode, bounded media/colors, active status, and
     active-member count;
   - one cached collection for local search/filter/sort.
2. Public team detail and roster
   - identity plus the complete active roster at the expected small team scale;
   - player identity/name/avatar, explicit owner treatment, approved public title, and optional
     competition rank; never serialize management capabilities, membership intervals, roster
     revisions, pending-action versions, or audit evidence as public profile fields.
3. Fact-backed team performance
   - T03 represented-performance summary, current-roster leaderboard comparison, bounded represented-
     result history, and owner-aware team gauntlet history;
   - summary/history use membership at canonical MatchStart; roster comparison deliberately uses the
     current roster and preserves each player's global rank;
   - separate public cache and independent unavailable state; never sum current members' lifetime pilot careers as a substitute.
4. Current-player action state
   - current team, relationship to the viewed team, relevant unexpired exact invitation/request,
     and one explicit state: join, request, cancel, accept, decline, leave, manage, already on another
     team, or no available action;
   - request-time authenticated response; React does not reproduce the membership transition state machine.
5. Authorized management state
   - effective capabilities, editable public fields/media, active roster management facts, and pending invitation/request queues;
   - permissioned request-time reads split by management section when that improves independent loading and saving.
6. Typed mutations
   - create/update, deterministic membership transition, decline/cancel/leave/remove, title/capability/rank changes, ownership transfer, and disband;
   - Eventun derives the actor, locks relevant state, authorizes one transition, commits audit/notification intent atomically, and returns an explicit outcome.

Public identity/roster and fact-backed statistics may fail independently. Private action-state or management failure must not leak pending state or disable the public profile. Successful mutations refresh or invalidate the team directory, team detail, current-player summary, pending queues, affected player profiles, global search, and any current-roster or historical-statistic projection whose facts changed.

### Team Contract Gaps

- implement and review the approved [T03 public-read checkpoint](../teams-and-team-gauntlets/delivery-plan.md#t03-public-read-contract-checkpoint); Website V2 launch requires those fact-backed reads and membership-at-performance-time attribution;
- add the compact reusable public team directory/detail projections rather than shipping Team Core's capability- and evidence-bearing roster response publicly;
- verify the approved public identity, bounded media, complete-roster, title, competition-rank, and
  affiliation-visibility behavior against the implementation; recruiting, region/time-zone, and
  watch/community fields remain separate future decisions;
- expose the approved bounded viewer-state response with unexpired exact pending state and explicit allowed actions; do not make the Website derive transition eligibility from membership mode alone;
- keep one deterministic add-member transition with typed outcomes where the reviewed Eventun design retains it; decline, cancel, leave, remove, transfer, and disband may remain explicit mutations;
- ensure the implemented T02 scope includes the approved `Open`, `Request to Join`, and `Invite Only` Website flows, including player-side invite acceptance/decline and requester cancellation;
- replace numeric designation authorization with explicit ownership and effective capabilities; visible titles remain presentation data;
- decide during T01/T02 review whether administrators can create a team for another player or whether ownership is always derived from the authenticated creator;
- define optimistic-concurrency/version behavior for independently saved management sections and destructive confirmations;
- reuse the approved signed-upload boundary and define cleanup/expiry for unattached team media;
- integrate actionable invite/request notification intent through the approved AccelByte Chat delivery path; Website V2 needs only a concise current-player indicator linking to the authoritative team page, not a second inbox;
- verify the approved T03 summary, full current-roster comparison, bounded represented-result
  history, and owner-aware gauntlet history without introducing a speculative aggregate team score;
- define mutation-driven invalidation for team identity, roster, current-player state, pending queues, public search, player team summaries, and fact-backed team views.

## Global Search Utility Group

Global search is a shared-shell utility rather than an initial destination route. Do not add a dedicated `/search` page merely to host the same grouped results. The accessible top-bar `SearchCommand` opens as a dialog or mobile sheet. Groups whose directory retains local search can link there with the query preserved, such as `/players?q={query}`; course matches link directly to their canonical detail routes.

The reviewed desktop/mobile command calibration and compact state study are the current visual
baseline. They keep the underlying shell stable, group shallow results by entity type, distinguish
no matches from partial group availability, and use a separate shape-aware focus overlay over the
full interaction target.

| Surface | Authoritative source | Server behavior | Browser behavior | Private/authorized overlay | Contract status |
|---|---|---|---|---|---|
| Top-bar `SearchCommand` | The approved Eventun public gauntlet, pilot, and team compact collections plus the AccelByte-authored course catalog through Eventun's public-safe projection | On first search interaction, compose the independently cached public collections into one explicit shallow Website catalog; return group availability independently; never expose service credentials or raw transport records | Cache the catalog in browser query state with bounded staleness and mutation invalidation; normalize once; perform grouped local matching; show at most a small result preview per group; support keyboard/touch navigation and direct entity links | None for the initial four public groups | No new Eventun cross-domain search endpoint is initially required if the approved compact reads remain suitably small; add one same-origin Website support handler/view model |
| `/gauntlets?q={query}` | Existing public gauntlet discovery collection | Render the ordinary directory and supply the initial query state; keep all public current, upcoming, and past gauntlets searchable | Apply the query through the directory's approved local search and controls | Existing participation overlay remains independent | Existing directory contract; query variant is `noindex` and canonicalizes to `/gauntlets` |
| `/players?q={query}` | Existing compact public pilot directory collection | Render the ordinary directory and supply the initial query state | Apply the query through local pilot/team matching | None | Existing directory contract; query variant is `noindex` and canonicalizes to `/players` |
| `/teams?q={query}` | Approved T03 compact public team browse collection | Render the ordinary directory and supply the initial query state | Apply the query through local team-name/tag matching | Current-team/create eligibility remains independent | Contract approved and implementation pending; query variant is `noindex` and canonicalizes to `/teams` |
| Course results in top-bar `SearchCommand` | Eventun public-safe projection of authoritative AccelByte course metadata | Include shallow `published` course identities in the grouped catalog; hidden and archived courses remain absent | Match course/planet labels locally and link each result directly to `/courses/[code]`; do not route through a `/courses?q=` variant | None | Requires the approved safe course projection |

### Search Catalog Contract

Return one full shallow collection for each initial group:

1. Gauntlets
   - stable id, title, ticker/subtitle where approved, canonical route, one optional small image,
     complete normalized occurrence facts sufficient for locally derived timing context, and public
     searchable labels;
   - include every public gauntlet regardless of whether it is current, upcoming, or past.
2. Players
   - stable id, display name, avatar, public team name/tag or `Independent`, canonical route, and public searchable labels;
   - apply the same explicit bot/test/internal classification used by `/players`.
3. Teams
   - stable id, name, tag, optional bounded avatar, public membership label, active-member count,
     canonical route, and public searchable labels;
   - do not include complete rosters, capabilities, or pending membership state.
4. Courses
   - stable code, display name, planet, optional approved image, canonical route, and public searchable labels for `published` courses;
   - never include hidden, alpha, internal, unknown, or conflicting records.

Common catalog rules:

- searchable aliases contain only deliberate public labels; do not make internal ids, raw enum values, or private metadata searchable merely because they exist;
- omit full statistics, schedules, rosters, media arrays, configuration, and management data;
- expose a stable group discriminator, canonical entity route, optional presentation fields, and per-group unavailable state rather than one ambiguous flat result list;
- return no personalized action state in the public catalog;
- reuse the same source cache tags and visibility projections as the entity directories so search cannot reveal a record that its public route rejects;
- invalidate or refresh the browser catalog after a same-session entity mutation that changes a searchable public label or lifecycle state.

### Search Interaction and Ranking

- lazy-load the catalog on the first explicit search interaction rather than prefetching every collection on every marketing page;
- use plain-text input; optional in-world verbs such as `FIND PILOT` remain presentation shortcuts and are never required syntax;
- rank deterministically within each group: exact normalized label/tag match, prefix match, then fuzzy or substring match with a stable alphabetical tie-break;
- do not create one opaque cross-entity relevance score or let a popular entity type crowd out the other groups;
- initially show up to five matches per group and provide `View all` navigation to the corresponding directory query;
- distinguish no matches from a temporarily unavailable group;
- preserve group headings, result counts, focus movement, Escape behavior, Enter activation, visible focus, screen-reader status, and touch targets according to [[non-functional-baseline]];
- do not add fake command latency, recent-query tracking, recommendation ranking, or analytics-dependent ordering.

### Search Permission Boundary

Sponsors do not enter the public catalog. Website V2 has no sponsor registry or administrator sponsor-search group; sponsor administration belongs to the Eventun Extend App. A gauntlet form may request a separate authorized form-scoped sponsor selector, but it never makes the shared public catalog session-dependent.

Team invitation player pickers, scoped sponsor pickers, gauntlet authoring selectors, and other mutation-specific choices are not global search. Each requires an authorized purpose-built lookup whose eligibility and returned fields match that workflow.

### Search Contract Gaps

- verify that the four approved compact collections expose the shallow labels and canonical identifiers needed by search without importing their broad legacy responses;
- add one same-origin Website catalog handler/view model that composes cached public source reads and reports per-group availability;
- ensure the gauntlet catalog includes Past entities, the pilot catalog applies explicit identity classification, the team catalog excludes private state, and the course catalog uses the fail-closed public visibility projection;
- accept and initialize the `q` query on each entity directory while keeping filtering client-side and query variants out of the sitemap/index;
- measure compressed catalog size, first-open fetch latency, parse/normalization time, memory, and input responsiveness on representative mobile hardware;
- if one group crosses measured limits, move only that group to a bounded server search contract before considering a separate all-entity search service;
- do not add Planets, Ship Parts, Manufacturers, Events/News, or a global Sponsor group until their route, visibility, and compact-result contracts justify inclusion.

## Authentication and Session Route Group

This route group is approved using the exchange already operating in Ascentun. Steam OpenID remains Steam's documented browser-login mechanism and AccelByte's current IAM contract still exposes the V4 `steamopenid` platform-token grant. AccelByte's managed-cloud coverage does not explicitly support this custom website architecture, but that documentation ambiguity is an accepted compatibility risk rather than a separate launch gate.

| Route | Authoritative source | Server behavior | Browser behavior | Security and contract status |
|---|---|---|---|---|
| `GET /api/auth/steam/login?returnTo=...` | Trusted environment configuration and Steam OpenID | Validate one safe relative return path; create a short-lived authenticated login transaction containing a nonce, issued time, and return path; construct realm/callback URLs from the configured public origin; redirect directly to Steam without unused AX/SREG claims | Follow the external redirect; no provider picker or browser-readable transaction contents are required | Approved; never derive realm, callback, or final redirect authority from `Host`/forwarded-host request values |
| `GET /api/auth/steam/callback` | Steam callback plus AccelByte V4 `steamopenid` platform-token exchange | Correlate and consume the login transaction; validate callback structure, expected provider/endpoint/mode/return target/claimed-id shape and required signed fields; submit only the allowed assertion fields to AccelByte; treat identity as established only after a successful exchange; handle cancel, linking/compliance, queue, and failure responses; establish the session and redirect safely | Receive only a final safe redirect or a deliberate login-status page | Required; raw assertions, platform tokens, AccelByte tokens, client secrets, and vendor response bodies must not be persisted in browser-accessible application state or ordinary logs |
| `/login` | Website-authored status copy; sanitized auth outcome | Render canceled, expired, failed, temporarily unavailable, linking-required, and retry states without exposing vendor payloads; preserve only a validated relative `returnTo` | Start or retry direct Steam sign-in | Required; `noindex`; expired protected routes should land here rather than silently starting an external redirect |
| `POST /api/auth/login-queue` | AccelByte Login Queue ticket grant | Read a sealed server-held queue ticket; enforce CSRF and Origin checks; exchange or poll through the documented V4 login-queue grant; establish a session when ready and discard the ticket on success/expiry/failure | Receive waiting, ready, expired, or retryable status without receiving the queue ticket | Implement when the platform-token exchange returns the documented V4 `202`; exact polling behavior is ordinary integration verification |
| `GET /api/auth/session` | Authenticated Website session; Eventun current-player context; display-only AccelByte fallback | Return a request-time, `no-store`, explicit `SessionView`; refresh authoritative context when required; fail closed for team/admin capabilities when Eventun context is unavailable | Render sign-in or the compact account menu and private overlays from display-safe fields only | Required; no access/refresh token, raw role/permission list, wallet state, or vendor payload crosses this boundary |
| `POST /api/auth/refresh` | HTTP-only AccelByte refresh-token cookie and reviewed IAM token endpoint | Enforce CSRF and Origin checks; serialize or deduplicate concurrent refresh for one session; rotate tokens, any cached session metadata, and CSRF state; clear private state on terminal failure | Receive success/expired status and refresh the explicit session view | Required; final V3-versus-V4 endpoint and token-rotation behavior must be verified against the deployed namespace |
| `POST /api/auth/logout` | Website session and AccelByte IAM token revocation | Enforce CSRF and Origin checks; best-effort revoke the refresh/access token through the supported confidential-client operation; always clear auth, transaction, queue, any metadata, and CSRF cookies; return a validated public-parent/current-public destination | Remove private overlays and navigate without a confirmation dialog | Required; local sign-out must succeed even when vendor revocation is unavailable |

### Session and Cookie Model

- do not add an external session database for the initial implementation unless cookie size, replay resistance, rotation, or Login Queue behavior demonstrates that one is required;
- use host-only production cookies with `Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/`, and `__Host-` names where applicable for access/refresh credentials and any cached authenticated session metadata;
- a readable CSRF value may exist for the double-submit pattern, but no browser-writable or unauthenticated cookie may become an identity, role, team, or authorization source;
- never copy Ascentun's readable user-info cookie pattern: a browser-facing `SessionView` is an output projection, not a credential or server authorization input;
- an AccelByte access token is different from that derived cookie: its claims are valid authentication input when the server verifies its signature, issuer, audience/client context, and expiry;
- keep access tokens, refresh tokens, Login Queue tickets, raw roles/permissions, client secrets, and OpenID assertions server-only;
- Eventun current-player context is primary for canonical pilot, team, pending membership, and operations destinations. AccelByte public user fallback may provide display identity only and must fail closed for Eventun-derived capabilities;
- private session reads are request-time and `no-store`; shared public page data remains independently cacheable;
- refresh authenticated context after team or identity mutations rather than relying on a long-lived browser copy;
- authorization controls may improve navigation, but Eventun must reauthorize every protected domain read and mutation.

The simplest initial implementation retains separate HTTP-only access/refresh cookies and derives `SessionView` server-side from the validated token and Eventun context. It does not require a second authentication framework, session database, or metadata cookie. If later performance work caches session metadata in another cookie, that cookie must be HTTP-only and cryptographically authenticated. Measure token-cookie size and rotation behavior before launch; move credentials behind an opaque server-session identifier only if those constraints are not safe or maintainable.

### Browser Session Projection

`SessionView` contains only fields needed by the shell and approved private overlays:

- authenticated/expired state;
- canonical pilot id, route, display name, and avatar;
- current team id, route, name/tag, or an explicit no-team state;
- one bounded pending invitation/join-request count or status;
- explicit authorized `Admin / Operations` destinations rather than raw roles or permissions;
- access-session expiry status sufficient to schedule refresh, without exposing either token.

The approved account menu remains `My Career`, `My Team`, conditional `Admin / Operations`, and separated `Sign Out`. Wallets, exact MMR, creation/edit actions, and speculative provider/linking controls remain excluded.

### Environment and Callback Boundary

- production and development each use one configured canonical public origin paired to the matching AccelByte/Eventun environment;
- arbitrary Vercel preview hosts must not become Steam realm, callback, or post-auth redirect authorities;
- previews should disable external Steam sign-in or hand off to the fixed development origin through a separately reviewed mechanism; they must not synthesize callbacks from request host headers;
- safe return paths begin with one `/`, remain same-origin, and exclude callback, logout, management, or other destinations that cannot safely resume;
- consume the login transaction once, enforce a short lifetime, and redact callback query strings and cookies from logs;
- return `Cache-Control: no-store` from authentication handlers and a restrictive referrer policy from the callback so the OpenID assertion URL is not retained or propagated by Website responses.

### Authentication Implementation Checks

- reuse the working Ascentun Steam OpenID to AccelByte V4 exchange; no separate vendor-support confirmation is required before implementation;
- verify successful login, refresh, and logout in the matching Website V2 development environment as ordinary release acceptance;
- verify linked-player, first-login/headless-account, duplicate-identity, `steam` versus `steamopenid` grouping, linking/compliance, cancellation, invalid assertion, replay, and Login Queue responses in the intended namespace;
- confirm the confidential client, exact V4 platform grant, refresh endpoint/version, token rotation, and V3 revocation operation available to Website V2;
- determine whether a sealed one-time login-transaction cookie plus provider/AccelByte validation supplies sufficient replay resistance or whether the flow requires a short-lived server-side nonce store;
- verify authenticated-cookie size, browser limits, expiry alignment, concurrent refresh behavior, multi-tab behavior, and terminal refresh cleanup;
- define or verify one bounded Eventun current-player/session-context read that supplies canonical pilot, team, pending membership, and explicit Website operations destinations without broad role disclosure;
- freeze the sanitized login outcome taxonomy and safe parent-route behavior for protected-route expiry and sign-out;
- test that Eventun unavailability cannot promote an AccelByte display fallback into team, creator, or administrator authority.

## Sponsor Administration Exclusion

Website V2 does not implement `/sponsors`, `/sponsors/[id]`, sponsor CRUD, or sponsor-owned media administration. Those operations move to the Eventun Extend App before cutover as specified in [[sponsor-administration-handoff]].

The Website route boundary retains only:

- optional approved sponsor display composed from a relationship-scoped public projection for one
  gauntlet; it is not part of or a prerequisite for the primary detail response;
- a narrow existing-sponsor option projection inside authorized gauntlet authoring;
- direct gauntlet-owned advertising upload, which remains independent of sponsor-owned media.

No unrestricted sponsor registry response, mutation, or upload credential crosses the Website browser boundary. Existing singular Ascentun sponsor URLs retire without becoming public Website V2 destinations.

## Shared Response-State Support

These are framework-level support behaviors, not independent public application routes or new backend APIs.

| Support surface | Trigger | Required behavior | Contract status |
|---|---|---|---|
| `app/not-found.tsx` | Unknown route; unknown, hidden, or unpublished public entity | Render one branded, non-revealing recovery state; entity routes resolve primary identity/visibility before optional modules; verify a real `404` response and `noindex` in the production build | Approved; duplicate entity-specific not-found pages are unnecessary unless recovery actions materially differ |
| Local unavailable state | Essential authoritative read is temporarily unavailable | Render the page shell with a retry action and a 5xx response; do not turn dependency failure into not found | Approved; exact 5xx behavior must be verified in the implemented Next.js route |
| Optional module unavailable state | Standings, recognition, sponsor display, personal placement, or another nonessential read fails | Keep the factual page available and isolate the failure to that module | Approved; each route contract identifies which modules are optional |
| `app/error.tsx` | Unexpected exception within the root route tree | Render a branded recovery state inside the normal shell and support retry without exposing exception details | Approved |
| `app/global-error.tsx` | Failure escapes the root layout or template | Render a minimal self-contained recovery document | Approved; expected to be rare |
| Protected-page recovery | Anonymous session or authenticated session without management permission | Anonymous visitors go to `/login` with a validated relative return path; authenticated unauthorized visitors return to the safe public parent with a clear message; mutation endpoints return typed `403` | Approved; Eventun still reauthorizes domain operations |
| Retired content | Replaced or removed legacy route | Return `404`; do not add an initial redirect or `410` inventory for the current negligible external traffic | Approved; exact redirects may be added later only for demonstrated inbound use |

Next.js can render a streamed `notFound()` result with a `200` response. Implementation acceptance must inspect the actual response status for unknown, hidden, and unpublished dynamic entities and move primary entity resolution ahead of optional streaming where necessary. Website V2 does not need the experimental `global-not-found` convention for its approved single-root-layout structure.

## Shared Metadata and Discovery Support

These use standard Next.js metadata facilities and the same public-safe projections as the rendered routes. Do not add parallel metadata or sitemap APIs.

| Support surface | Authoritative source | Server behavior | Indexing and browser behavior | Contract status |
|---|---|---|---|---|
| Root metadata configuration | Repository-authored brand defaults and one configured production origin | Set the title template, metadata base, default description, canonical-origin policy, icons, and default social image without deriving authority from request host headers | Supplies safe fallbacks; each indexable route still receives a factual title, description, and self-canonical URL | Approved; final production origin remains a cutover configuration item |
| Static route metadata | Repository-authored route content | Export static metadata for marketing, about, brand, event-index, and other repository-authored pages | Index approved public routes; no separate client fetch | Approved |
| Dynamic entity metadata | The same Eventun public-safe gauntlet, pilot, team, or course projection used by the page | Reuse the primary entity read; never perform a broader visibility-bypassing lookup; return not found for unknown/hidden/unpublished entities; remain useful when optional statistics fail | Render factual entity metadata and a self-canonical URL without private overlays or query-state variants | Approved; projection fields must include only the approved display identity and meaningful update timestamp |
| Query-state metadata | Directory route plus request query state | Recognize search/filter/sort/pagination variants on initial server render | Preserve useful shareable URLs, apply `noindex`, and canonicalize to the base directory; do not create an indexable variant for every combination | Approved |
| `app/robots.ts` and deployment headers | Trusted deployment environment and configured production origin | Production advertises the canonical sitemap and excludes protected/support paths; development and preview disallow crawling and receive deployment-wide `X-Robots-Tag: noindex, nofollow` | Robots directives are indexing guidance, never authorization | Approved |
| `app/sitemap.ts` | Repository-authored public routes/events plus complete cached public gauntlet, pilot, team, and course projections | Emit one sitemap containing canonical public routes, including Past gauntlets and published or archived courses; retain the last complete cached result across dependency failure and fail rather than publish a knowingly empty/partial replacement when no complete result exists | Exclude query variants, search, authentication, create/edit/manage/admin, sponsor, wallet/prize, hidden, unpublished, and preview URLs | Approved; split only after measured URL volume requires it |
| Social metadata | Repository-authored default card plus factual route/entity identity and approved media | Provide one branded 1200 by 630 fallback; generate route-specific cards only when approved names, dates/categories, and media make them useful | No invented planet, course, sponsor, pilot, or team artwork; missing media uses the fallback | Approved |

Sitemap `lastModified` values come only from meaningful source content/entity timestamps. Build time, request time, cache refresh time, and optional statistics refreshes do not qualify unless they represent a visible canonical-page change.

## Legacy Route Retirement

Website V2 does not implement a legacy marketing or Ascentun redirect layer for the initial release. The current audience is too small and internally concentrated to justify route mappings, host-specific redirect infrastructure, or a redirect manifest.

- all Website navigation, repository-authored content, shared links, metadata, and sitemap entries use the final canonical routes directly;
- replaced singular Ascentun routes and `/tournaments` marketing routes may return `404` after cutover;
- the legacy Ascentun gauntlet prize page, required authentication, and supporting APIs remain reachable only for the retained Midnight flow;
- sponsor routes retire after the Eventun Extend App handoff and do not redirect into Website V2 or an authenticated administrator surface;
- an exact redirect may be added later when a real inbound link or workflow demonstrates value; do not prebuild wildcard or host-wide mappings.

## Shared Media Upload Support

Website V2 retains Ascentun's direct browser-to-R2 transfer architecture but replaces its session-only signing endpoint with an operation-scoped upload-intent boundary. Website V2 owns only team and gauntlet uploads; sponsor uploads belong to the Eventun Extend App, and course uploads are excluded.

| Support surface | Authoritative source | Server behavior | Browser behavior | Contract status |
|---|---|---|---|---|
| Server-rendered media options | Eventun media-purpose configuration filtered by the approved Website form | Fetch with server credentials; return only the team or gauntlet purposes that the current form may create; exclude sponsor/course purposes and new `WideBillboard` uploads | Render labels and purpose-specific controls without a separate browser purpose API | Approved; preserve unrecognized or legacy media already attached during edit |
| `POST /api/media/upload-intents` | Authenticated session, Eventun create/manage capability, approved form-purpose projection, and Website R2 configuration | Enforce CSRF/Origin checks; authorize team create/manage or gauntlet create/edit; accept at most 10 JPEG/PNG/WebP images of at most 10 MB each; derive extensions from allowed types; generate random keys; issue ten-minute signed `PUT` URLs; return required headers, public URL, and expiry; never log credentials or signed URLs | Request intents immediately before save and retain form state on failure | Approved; no upload-session database or file-body proxy required |
| Direct R2 `PUT` | Short-lived upload intent and environment-specific R2 bucket | Keep object-store credentials server-only; configure CORS for the fixed production and development Website origins | Validate file type for user feedback, upload directly, inspect every response, and retry only failed files | Approved; direct transfer is not a Website API proxy |
| Team/gauntlet create or update mutation | Eventun authoritative mutation and authorization | Reauthorize the domain operation; accept newly uploaded URLs only from the configured environment media base while preserving reviewed existing/legacy media; attach purpose, priority, and approved metadata; invalidate affected entity/collection tags | Submit only after required uploads succeed; show upload and mutation failures separately | Approved; upload success alone never proves attachment or mutation authorization |

`Tileable = true` remains ordinary gauntlet `Billboard` metadata and may use the approved three-panel preview. New uploads do not perform dimension extraction, resizing, aspect-ratio classification, physical-slot matching, spatial preview, or content processing.

An upload followed by an abandoned or failed form can leave an unreferenced object. At the approved traffic level this is an accepted initial operational tradeoff: use auditable server-generated keys, but do not add a pending-object database, promotion workflow, or automated orphan-cleanup service. Revisit cleanup only if measured object growth or operating cost warrants it.

## Matrix Review Result

The initial route/API matrix is complete for planning. Remaining entries within individual route groups are implementation contract gaps, team/bracket dependencies, environment verification, and cutover work rather than unmapped Website route groups.
