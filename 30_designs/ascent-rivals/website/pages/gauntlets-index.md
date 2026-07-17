# Ascent Rivals Gauntlets Index Page Spec

Date: 2026-04-13
Status: Approved discovery model; visual design and Website API projection open
Last reviewed: 2026-07-16

## Related

- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../flows/gauntlet-authoring]]
- [[gauntlet-detail]]
- [[sponsors-index]]
- [[../../../../50_knowledge/ascent-rivals/competition-runtime-terms|competition-runtime-terms]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the information architecture, ordering, state model, and page requirements for public gauntlet discovery.

The page must support two related but different browsing needs:

1. finding a gauntlet as a durable competition entity;
2. finding the next qualifier or stage occurrence on the schedule.

Do not force one list to satisfy both. The default `Gauntlets` view lists each gauntlet once. The alternate `Schedule` view lists occurrences chronologically and may repeat the same gauntlet for multiple qualifier or stage windows.

## Route and URL State

- canonical route: `/gauntlets`;
- current legacy route: `/gauntlet`;
- permanently redirect public legacy singular routes to their plural equivalents at cutover.

Initial URL-backed state:

- `/gauntlets` — unique gauntlets with current/upcoming occurrences;
- `/gauntlets?scope=past` — unique past gauntlets;
- `/gauntlets?view=schedule` — chronological current/upcoming occurrence agenda;
- search and any later filters should remain shareable in query state where practical.

Do not add `/calendar` or `/gauntlets/calendar` until a distinct route provides value beyond the responsive schedule agenda.

## Audience

Primary:

- players seeking the next opportunity to participate;
- followers tracking active and upcoming competition;
- returning visitors entering from the marketing homepage;
- gauntlet creators and administrators.

Secondary:

- teams, sponsors, tournament organizers, press, and community viewers;
- visitors researching prior gauntlets and results.

## Approved Discovery Decisions

- Use `Gauntlets` as the default view and list each gauntlet once.
- Use `Schedule` as an alternate chronological agenda and allow repeated gauntlet entries for separate occurrences.
- Default the entity scope to `Current & Upcoming`.
- Keep `Past` as a secondary entity scope rather than rendering a permanent history section below the default list.
- Keep every successfully created Eventun gauntlet public, including gauntlets in the `Past` scope.
- Determine directory relevance from an active occurrence or the nearest future occurrence, not from the full span between a gauntlet's first and final event.
- Sort active gauntlets first, then upcoming gauntlets by their next occurrence.
- Do not classify a long-running gauntlet as current during gaps between its qualifier or stage windows.
- Use `Past` as the general historical label even when final scores could establish stronger completion semantics.
- Reserve `Live` for a future trustworthy runtime or broadcast state; schedule overlap alone is insufficient.
- Avoid separate empty `Current` and `Upcoming` bands.
- Keep creation and management actions permission-aware and contextual.

## Important Product Cases

### Long-Lived Gauntlets

A gauntlet may span months or longer while containing only occasional qualifier or stage windows. Its broad `first_event_time` to `final_event_time` span is therefore not a useful directory status.

Between event windows:

- if another qualifier or stage is scheduled, classify the gauntlet as upcoming and sort it by that next occurrence;
- if no future occurrence exists, remove it from the default scope and place it in `Past`;
- do not keep it at the top merely because the current time falls between its first and final historical event.

### Ad Hoc Playtest Gauntlets

A durable playtest gauntlet may have no stages and receive qualifier-style time windows as playtests are arranged.

Behavior:

- a currently open playtest window makes it current;
- a future window makes it upcoming;
- after the last window ends, with no future window scheduled, it moves to `Past`;
- adding a new future window returns the same gauntlet to the default scope automatically;
- absence of stages is valid and must not create empty stage labels or block discovery.

### Optional Competition Structure

Gauntlets may omit qualifiers or stages, but the current Eventun authoring contract requires at least one of the two. Directory and schedule presentation must derive from occurrences that actually exist.

A public gauntlet with no current or future occurrence has no basis for default schedule discovery. If unscheduled public gauntlets later need a holding state, add an explicit `Unscheduled` or announcement contract rather than inferring one from missing data.

## Current Eventun Contract

### Unique Gauntlet Reads

Current endpoints:

- `GET /v1/gauntlet` returns unique gauntlet records whose broad final event time is after the request boundary;
- `GET /v1/gauntlet/completed` returns unique gauntlet records whose broad final event time has passed.

Current gauntlet fields include:

- id and creator id;
- title, subtitle, and ticker;
- colors and region;
- qualifiers and stages;
- first and final event times;
- media and sponsor relationships;
- participant count and scoring configuration.

Limitation:

The current list contract exposes broad first/final times but no explicit directory lifecycle, cancellation, delay, publication, or actual-completion state.

### Public Visibility Contract

The current Eventun model has no draft, private, hidden, archived, or publication field for gauntlets. The client API exposes public gauntlet reads, and the separate completed read is a time-based listing convenience rather than an access-control boundary.

Website V2 therefore preserves the current product model:

- every successfully created gauntlet is publicly readable and discoverable;
- a gauntlet remains public after its final occurrence moves it into `Past`;
- exclusion from the default `Current & Upcoming` scope does not hide its detail route, search result, metadata, or appropriate sitemap entry;
- timing, missing future occurrences, completion, and absence from the game-client calendar must never be interpreted as private or unpublished;
- create, edit, delete, runtime, and other management actions remain permission-gated even though the entity is publicly readable.

Successful creation is therefore immediate publication in the initial Website V2 authoring flow. If organizers later need private drafts, embargoed announcements, cancellations, or administrative suppression, add an explicit lifecycle and authorization contract rather than overloading schedule fields.

### Occurrence Reads

Current endpoints:

- `GET /v1/gauntlet/calendar` returns current/future qualifier and stage occurrences, ordered by occurrence start, plus server time;
- `GET /v1/gauntlet/calendar/completed` returns cursor-paginated past gauntlet calendar groups and optional player summaries.

Each current/future occurrence includes:

- gauntlet id;
- event type;
- start and end time;
- qualifier duration or stage timing window;
- stage id where applicable;
- region;
- occurrence index and count within its type.

The occurrence contract is the correct basis for nearest-event ordering and the Schedule view.

### Timing Limitation

Qualifier end time is derived from its authored duration. Current stage calendar end time is estimated as two hours after the scheduled start. Schedule-derived state can therefore support `Current`, `Upcoming`, and `Past`, but it is not enough to claim that a stage is actually live, completed successfully, cancelled, or delayed.

Accepted final stage scores or a completed stage run may support stronger result-state labels later, but the index does not need that distinction to use `Past` accurately.

## Directory State and Ordering Contract

For each unique gauntlet, derive two occurrence candidates relative to one server time:

- `active_occurrence`: an occurrence where `start_time <= server_time < end_time`;
- `next_occurrence`: the earliest occurrence whose `start_time > server_time`.

If multiple occurrences are active, select the one ending soonest as the primary active occurrence and retain the others as supporting schedule context.

Directory inclusion:

- `Current` when an active occurrence exists;
- `Upcoming` when no active occurrence exists and a next occurrence exists;
- `Past` when neither exists and at least one historical occurrence exists;
- invalid for the current directory contract when it has no occurrence at all; current authoring requires at least one qualifier or stage, so an unscheduled holding state would require an explicit future contract.

Default sort:

1. current gauntlets before upcoming gauntlets;
2. current gauntlets by active occurrence end ascending, then active occurrence start ascending;
3. upcoming gauntlets by next occurrence start ascending;
4. stable tie-break by normalized title, then gauntlet id.

Past sort:

1. most recently ended occurrence descending;
2. stable tie-break by normalized title, then gauntlet id.

Do not use absolute distance from now without first prioritizing active occurrences. A future event a minute away should not displace a qualifier that is currently open.

## Schedule Ordering Contract

The Schedule view lists occurrences rather than unique gauntlets.

Rules:

- one row or card per qualifier or stage occurrence;
- the same gauntlet may appear multiple times;
- active occurrences first, ordered by ending soonest;
- future occurrences next, ordered by start time ascending;
- group by local calendar day only as a presentation aid;
- preserve exact timestamps and timezone clarity;
- link every occurrence to its canonical `/gauntlets/[id]` detail page;
- include enough gauntlet identity on every row that repeated entries remain understandable.

Initial Schedule presentation should be a responsive chronological agenda, not a month grid. A month grid consumes space poorly on mobile and does not improve a schedule with relatively few irregular events.

## Page Structure

## 1. Competition Header

Content:

- `Gauntlets` title;
- one concise explanation;
- permission-aware `Create Gauntlet` action;
- no fabricated network status or live count.

The header should be compact. The first relevant occurrence should not be pushed below a large decorative hero.

## 2. Discovery Controls

Primary view control:

- `Gauntlets`;
- `Schedule`.

Entity scope control in `Gauntlets` view:

- `Current & Upcoming`;
- `Past`.

Shared controls:

- title search;
- later filters only when event volume and supported metadata justify them.

Use segmented controls for the two small view/scope choices. Keep their state in the URL. Do not use content tabs that depend on client-only state and cannot be shared.

## 3. Unique Gauntlet List

Each card should prioritize:

- gauntlet title and verified media;
- `Current`, `Upcoming`, or `Past` timing label;
- active or nearest future occurrence type and time;
- concise qualifier or stage position such as `Qualifier 2 of 4` or `Stage 1 of 3` when meaningful;
- region;
- participant count only when its meaning is clear;
- approved sponsor branding only when supplied through the public gauntlet context;
- route to `/gauntlets/[id]`.

Optional supporting context:

- next occurrence after the primary one;
- count such as `3 more scheduled`;
- signed-in participation, qualification, or join context when a bounded Website projection supplies it.

Do not render:

- empty qualifier or stage rows;
- a broad year-long date range as the primary status;
- full standings or leaderboard tables;
- sponsor tier;
- prize or reward content;
- `Live` based only on the clock.

### Card Media Composition

Reuse gauntlet imagery without copying the game-client composition directly.

- Ordinary directory cards use a fixed-ratio media bay beside the information region on wider screens and above it on narrow screens.
- Keep titles, timing, and actions on an opaque or near-opaque terminal surface. Do not make variable uploaded artwork responsible for text contrast.
- A gauntlet `Background` image may be cropped into that media bay when it is the best verified asset, but it is not the default full-card background.
- Reserve full-bleed or atmospheric `Background` treatment for the gauntlet-detail summary or one deliberately featured module. Those uses require a strong scrim, crop review at each breakpoint, and verified text contrast.
- Treat the existing media-purpose labels as selection hints until the media-consumer audit establishes a reliable Website priority and aspect-ratio contract.
- Preserve the card dimensions and information hierarchy when no usable media exists; render the terminal-native fallback in the same bay.

## 4. Schedule Agenda

Each occurrence row should include:

- local date and time with timezone access;
- gauntlet title;
- `Qualifier` or `Stage` label;
- occurrence index/count when meaningful;
- region;
- current/upcoming timing treatment;
- canonical gauntlet link.

Keep the agenda image-light. An optional small identity thumbnail may aid repeated-gauntlet recognition, but do not use per-row background art or allow media to displace the occurrence time and type.

Use exact competition semantics:

- `Qualifier` only for actual qualifier windows;
- `Stage` for scheduled stage occurrences;
- `Final` only when the stage is explicitly the deciding final;
- `Bracket` only for an actual published bracket graph, not for any multi-stage gauntlet.

The current calendar contract does not identify an explicitly deciding final. Add that fact to the Website projection before using `Final` in the agenda.

## 5. Past Scope

Past gauntlets remain unique entities rather than repeated occurrence history.

Card content:

- title and verified media;
- most recent occurrence date;
- result or winner summary only when supported by accepted result data;
- participant count where meaningful;
- canonical detail link.

Use `Past` when only schedule history is known. A card may say `Completed` inside result context only when an explicit completion/result contract supports it.

## Permissions and Authenticated Overlays

Anonymous visitors can browse both views and both entity scopes.

Authenticated players may receive concise overlays inside the same card or row layout:

- participation or qualification context;
- join/request context where relevant;
- personal result summary in Past when supported.

Gauntlet creators and administrators may receive:

- `Create Gauntlet` in the page header;
- contextual edit/manage actions on gauntlets they can manage.

Do not expose operations controls globally or change the discovery layout by role. Authorization must be enforced by protected routes and APIs as well as presentation.

## Website API Projection Requirement

Website V2 may initially join current gauntlet and calendar reads server-side. If a dedicated Website-oriented projection is useful, it should return one compact, complete collection of public gauntlet summaries rather than a server-paginated directory. Each summary provides:

- authoritative server time;
- unique public gauntlet summary;
- active occurrence, if any;
- next occurrence, if any;
- latest ended occurrence for Past sorting;
- additional scheduled-occurrence count;
- public timing state;
- optional explicit runtime/result state when available;
- bounded public media and sponsor context;
- optional signed-in participation overlay;
- no nested detail data that the index does not render.

The server should derive timing state and occurrence candidates once. Do not let browser clocks independently classify the same gauntlet differently around time boundaries. The browser then performs the approved stable ordering, title search, scope filtering, and any later supported filters over the returned collection.

Initial directory presentation is client-side:

- fetch the compact collection once;
- filter and search without network round trips;
- use ordinary page controls, progressive reveal, infinite-style loading, or list virtualization as interchangeable rendering choices over the same local collection;
- do not add server pagination until measured collection size, transfer cost, parsing cost, or memory use demonstrates a real problem.

Client-side progressive reveal reduces rendered DOM work but does not reduce the initial response size. Keep the collection payload compact and cacheable rather than confusing UI lazy loading with data pagination.

The Schedule projection should include the bounded gauntlet identity needed for each occurrence so the Website does not issue one detail fetch per repeated gauntlet.

## Empty, Loading, and Error States

No current/upcoming gauntlets:

- show one compact message and offer `Past` or `Schedule` only if those destinations contain useful content;
- do not render separate empty Current and Upcoming sections;
- keep `Create Gauntlet` visible when authorized.

No schedule occurrences:

- state that no qualifier or stage windows are currently scheduled;
- link to Past when available.

No past gauntlets:

- show one compact historical empty state.

Fetch failure:

- preserve the page header and controls;
- provide a retry path;
- do not substitute cached-looking fabricated items.

Missing media:

- use a consistent terminal-native gauntlet fallback;
- do not render broken image slots.

## Responsive Requirements

Desktop:

- use a compact header and clear view/scope controls;
- cards use a fixed-ratio media bay plus a structured, independently readable content region;
- the agenda may group occurrences by date.

Tablet:

- reduce columns without dropping occurrence type, date, or state;
- allow controls to wrap in a predictable order.

Mobile:

- use one-column cards and agenda rows;
- place the fixed-ratio card media bay above its content when shown, rather than moving text over the image;
- keep current/next occurrence and primary detail action visible before secondary metadata;
- retain URL-backed `Gauntlets`/`Schedule` and `Current & Upcoming`/`Past` controls;
- do not use a month-grid calendar as the initial mobile experience.

## Accessibility Requirements

- timing labels must include text and not rely on color alone;
- local time presentation must expose an unambiguous date, time, and timezone;
- search and segmented controls must be keyboard accessible;
- card actions must have explicit accessible names;
- repeated schedule entries must name both the gauntlet and occurrence type;
- motion or countdown treatment must respect reduced-motion preferences and must not be required to understand timing.

## SEO and Sharing

- title: `Gauntlets - Ascent Rivals`;
- description focused on finding current and upcoming Ascent Rivals competitions;
- canonical default URL: `/gauntlets`;
- query-state variants should use deliberate canonical handling so Past and Schedule filters do not create uncontrolled duplicate indexing;
- private participation overlays must never appear in metadata.

## Acceptance Criteria

- the default view lists every gauntlet at most once;
- the Schedule view may list a gauntlet once per qualifier or stage occurrence;
- a long-lived gauntlet is current only during an actual occurrence window;
- between windows, a gauntlet is sorted by its nearest future occurrence;
- an ad hoc playtest gauntlet with no stages works using its authored qualifier-style windows;
- adding a new future window returns a previously Past gauntlet to the default scope;
- current gauntlets sort before upcoming gauntlets;
- upcoming gauntlets sort by next occurrence ascending;
- Past gauntlets sort by latest ended occurrence descending;
- browser clock differences do not independently determine list classification;
- schedule overlap is never labeled `Live` without a trustworthy runtime or broadcast state;
- empty Current and Upcoming bands are not rendered;
- missing optional qualifiers or stages do not produce empty labels;
- anonymous and authenticated visitors retain the same discovery layout;
- creation and management actions appear only when authorized;
- public cards contain no sponsor tier, prize, reward, wallet, or token-gating content;
- Past gauntlets remain publicly readable, searchable, and linked through the Past scope;
- the Website does not infer private, hidden, or unpublished state from schedule timing;
- the initial directory fetches one compact public collection and searches, filters, sorts, and incrementally presents it client-side;
- ordinary directory cards do not place essential text directly over gauntlet artwork;
- the Schedule agenda does not use per-row background images;
- the schedule agenda remains usable on mobile without a month grid.

## Open Implementation Questions

- Should the first Website API projection extend the existing gauntlet/calendar responses or add one purpose-built discovery endpoint?
- What runtime/result fields should distinguish scheduled overlap, an active stage run, accepted final results, cancellation, and delay?
- How should overlapping qualifier and stage occurrences choose their one primary directory occurrence beyond the approved soonest-ending rule?
- Which media-purpose priority and crop metadata should the Website adopt after the media-consumer audit?

## Review Checkpoint

The unique-gauntlet directory, repeated-occurrence Schedule agenda, `Current & Upcoming` and `Past` scopes, all-gauntlets-public visibility, client-side collection interaction, occurrence-based inclusion, nearest-event ordering, long-lived/playtest behavior, schedule-derived terminology guardrails, and constrained media composition are approved. Detailed styling, explicit runtime/result lifecycle, media-purpose priority, and whether a dedicated compact Website API projection is worthwhile remain open.
