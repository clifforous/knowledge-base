# Ascent Rivals Website V2 Non-Functional Baseline

Date: 2026-07-17
Status: Rendering, caching, hosting/deployment, accessibility, responsive behavior, performance, and SEO approved; external analytics/observability deferred; provisioning/cutover setup remains

## Related

- [[unified-design]]
- [[initial-release-scope]]
- [[information-architecture]]
- [[design-doc-roadmap]]
- [[flows/authentication]]

## Purpose

Define the cross-route quality and operational rules that page specifications should not repeat independently.

The initial approved slice covers:

- rendering boundaries;
- public and private caching;
- mutation invalidation;
- the preferred deployment target;
- accessibility acceptance requirements;
- responsive, asset, motion, and performance requirements;
- lightweight search-discovery and link-sharing requirements.

## Platform Direction

- use the Next.js App Router;
- enable Next.js 16 Cache Components;
- apply shared caching deliberately at public data-function or component boundaries rather than marking an entire mixed public/private route cacheable by default;
- read cookies and other request-specific state outside shared cached scopes;
- keep domain rules and authoritative data in Eventun or AccelByte rather than in the Next.js cache layer.

References:

- [Next.js `use cache`](https://nextjs.org/docs/app/api-reference/directives/use-cache)
- [Next.js revalidation](https://nextjs.org/docs/app/getting-started/revalidating)

## Rendering and Cache Classes

### 1. Repository-Authored Marketing Content

Applies to:

- homepage marketing sections;
- `/about`;
- `/brand`;
- code-authored `/events` content;
- other repository-owned copy and media manifests.

Policy:

- render statically from the deployed revision;
- update through the approved design/content change and deployment workflow;
- do not add a runtime CMS cache or polling layer;
- do not block the static marketing shell on optional Eventun, authentication, or ownership reads.

### 2. Public Entity and Directory Data

Applies to public gauntlets, pilots, teams, courses, career summaries, records, and other non-user-specific reads.

Policy:

- render through cached server reads with explicit domain tags;
- use stale-while-revalidate behavior where brief staleness is acceptable;
- keep collection responses shallow and complete according to the approved client-side filtering policy;
- invalidate the affected entity and collection tags after successful mutations or controlled backend updates;
- allow an unavailable optional module to fail independently rather than making a whole public page unavailable.

### 3. Schedule-Sensitive Gauntlet Data

Policy:

- use the approved Eventun server time and server-derived active/next/latest occurrence summaries;
- use short or occurrence-boundary-aware freshness so cached `Current`, `Upcoming`, and `Past` state does not remain stale across a known start or end boundary;
- do not upgrade schedule overlap to `Live` without an explicit runtime-state contract;
- use the same cached public discovery collection for the gauntlet directory, Schedule view, homepage teaser, and public search where applicable.

Exact cache duration and boundary-refresh mechanics remain implementation choices. They must be tested around an occurrence start and end rather than selected as an arbitrary long global TTL.

### 4. Standings and Recent Results

Policy:

- use a short public cache appropriate to the actual update frequency;
- offer an explicit refresh action where users reasonably expect updated standings or recently submitted results;
- invalidate relevant tags when Website-owned mutations or result workflows provide a reliable completion signal;
- do not describe polling or briefly cached data as real-time or live.

### 5. Authenticated and Permissioned State

Applies to:

- login/session state;
- team invitations and join requests;
- personal participation and qualification overlays;
- management permissions;
- admin and operational data.

Policy:

- render request-time from authenticated state;
- never place tokens, cookies, permission results, invitations, private progress, or personalized payloads in a shared public cache;
- keep public shells and public entity data independently cacheable;
- compose optional authenticated overlays separately, using private/request-scoped behavior only where it is actually useful;
- recheck authorization at the protected mutation or read boundary regardless of rendered controls.

### 6. Authoring and Administrative Routes

Policy:

- keep forms, permissions, uploads, and operational reads dynamic;
- after a successful mutation, invalidate the affected public entity and collection tags;
- route to or refresh the canonical public detail page only after the mutation succeeds and its public reads have been invalidated;
- never use a stale public cache entry as evidence that an authorization-sensitive mutation succeeded.

## Invalidation Direction

Prefer domain/entity tags over path-only invalidation so one mutation can refresh every page and module that consumes the same data.

Expected tag families include:

- collection and entity tags for gauntlets;
- collection and entity tags for pilots;
- collection and entity tags for teams;
- collection and entity tags for courses;
- dependent leaderboard, career, standings, or recognition tags where their update lifecycle differs.

The final tag names and dependency graph belong to implementation planning. Avoid one global tag that invalidates the whole application for ordinary entity edits.

## Response and Failure-State Baseline

- resolve the primary identity and public visibility of an entity before optional streamed modules so an unknown, hidden, or unpublished entity uses the shared not-found state rather than an indexable partial shell;
- return the same branded not-found state for unknown, hidden, and unpublished public entities so the response does not reveal which classification caused the failure;
- verify the actual production status of representative entity not-found responses because a Next.js `notFound()` raised after streaming begins may render the not-found UI with a `200` status; restructure the route if that occurs;
- use one root `app/not-found.tsx` unless a route group demonstrates a materially different recovery action; do not adopt the experimental global-not-found convention for the initial single-root-layout application;
- treat a failure of data essential to the whole page as an unavailable 5xx state with a retry action; do not misclassify a dependency outage as not found;
- keep optional standings, recognition, sponsor display, personal-placement, and similar module failures local while the remaining factual page stays available;
- send an anonymous visitor requesting a protected page to `/login` with one validated relative return path;
- send an authenticated visitor without page-management permission to the closest safe public parent with a clear status message, while same-origin mutation endpoints return a typed `403` response;
- use the nearest `app/error.tsx` boundary for unexpected route failures and a minimal `app/global-error.tsx` fallback for failures that escape the root layout;
- return `404` for retired content; do not add an initial `410` or redirect inventory for the current negligible external traffic;
- provide recovery actions without exposing exception details, vendor payloads, internal identifiers, authorization rules, or hidden entity state.

## Media Upload Baseline

- retain direct browser-to-R2 `PUT` transfer through short-lived Website-issued upload intents; do not proxy image bodies through a Next.js function;
- restrict Website V2 upload intents to authorized team and gauntlet create/edit workflows; sponsor upload belongs to the Eventun Extend App and course upload is excluded;
- enforce same-origin CSRF/Origin checks, current Eventun-backed create/manage permission, a maximum of 10 new files per submission, and a maximum of 10 MB per file before issuing intents;
- allow JPEG, PNG, and WebP only; client-side content inspection is useful validation feedback but does not replace server authorization and bounded signing;
- derive safe extensions and random auditable object keys server-side rather than accepting a client-selected storage key or raw filename;
- use ten-minute signed URLs and configure R2 CORS for only the fixed production and development Website origins required by direct transfer;
- provide media-purpose options through the server-rendered form projection; reject purposes not approved for that entity/form and prevent new `WideBillboard` uploads while preserving existing legacy records during edit;
- require the browser to inspect every upload response, preserve form state, distinguish upload failure from mutation failure, and retry only failed transfers where practical;
- reauthorize the final Eventun create/update mutation and validate newly uploaded URLs against the configured environment media base before attachment; a successful upload is not mutation authorization;
- never log object-store credentials, signed upload URLs, authorization headers, file bodies, or mutation bodies;
- accept occasional unreferenced objects from abandoned or failed forms at the initial traffic level; use auditable keys and defer a pending-object store, promotion workflow, or automated cleanup until measured growth or cost justifies it;
- do not add initial dimension extraction, resizing, aspect-ratio classification, billboard-slot matching, spatial preview, or media-processing infrastructure.

## Accessibility Baseline

Website V2 targets WCAG 2.2 Level AA for the initial release. This is an implementation and acceptance baseline, not a commitment to third-party certification before launch.

### Structure and Meaning

- use semantic HTML landmarks, headings, lists, forms, buttons, links, and tables before adding ARIA;
- implement terminal panels, paths, separators, and frames through CSS and ordinary document structure;
- hide purely decorative glyphs, scan lines, status noise, and repeated terminal chrome from assistive technology;
- keep ordinary visible labels and accessible names even when optional command-like text adds visual character;
- preserve a logical reading order when layouts collapse or rearrange.

### Keyboard and Focus

- make every navigation, search, filter, authentication, dialog, menu, disclosure, and permissioned action operable without a pointer;
- provide a skip link, logical focus order, no keyboard traps, and conventional dismissal such as `Escape` where applicable;
- provide a strong visible focus treatment and ensure sticky bars, drawers, notifications, and other overlays do not obscure the focused control;
- do not expose essential information or actions only on hover;
- make hover- or focus-triggered supplemental content dismissible, hoverable, and persistent when WCAG requires it.

### Contrast, Sizing, Zoom, and Reflow

- meet at least 4.5:1 contrast for normal text and 3:1 for large text;
- meet at least 3:1 contrast for meaningful control boundaries, state indicators, focus treatments, and chart elements where WCAG non-text contrast applies;
- never distinguish status, rank, team, course category, or chart series by color alone;
- provide pointer targets at least 24 by 24 CSS pixels or qualifying spacing, and prefer approximately 44 by 44 CSS pixels for primary touch actions;
- support text zoom to 200 percent without losing content or functionality;
- support reflow at 320 CSS pixels, corresponding to a 1280-pixel viewport at 400 percent zoom, without two-dimensional page scrolling;
- allow a deliberately labeled scroll region or equivalent alternate presentation for a table, chart, course trace, or other component whose meaning genuinely requires two-dimensional layout.

### Data Visualizations and Tables

- give each meaningful chart a clear title, plain-language summary, and programmatically associated context;
- keep exact values available through an accessible table, list, detail view, or equivalent text representation when the chart is not itself sufficient;
- distinguish series and states with labels, shapes, patterns, or line styles in addition to color;
- use real table semantics for tabular comparisons and leaderboards;
- if a table becomes cards on narrow screens, preserve every field label, reading order, and relationship needed to interpret the row;
- do not announce passive telemetry or frequent data refreshes continuously through live regions.

### Forms, Status, and Motion

- associate labels, instructions, validation messages, and error summaries with their controls; placeholders are not labels;
- announce consequential asynchronous results and errors without unexpectedly moving focus;
- preserve entered values after recoverable validation or service errors;
- honor `prefers-reduced-motion` and provide a complete reduced-motion treatment for terminal acquisition, scan, trace-drawing, parallax, and mechanical effects;
- do not require animation, type-on sequences, flicker, or timed visual effects to understand content or complete a task;
- avoid flashing content that could exceed WCAG thresholds.

### Acceptance Verification

Use automated accessibility checks as a regression aid, not as the sole acceptance method. Before launch, manually verify representative marketing, directory/filter, entity-detail, chart/table, authentication, permissioned-form, error, empty, and mobile-shell states with:

- keyboard-only navigation;
- NVDA with Chrome or Firefox on Windows;
- VoiceOver with Safari on a mobile Apple device;
- 200-percent text zoom and 400-percent browser zoom/reflow;
- forced-colors or comparable high-contrast behavior;
- reduced-motion preferences;
- pointer and touch interaction at narrow widths.

Accessibility failures that prevent understanding or completing a core public, authentication, or authorized-management flow block initial release. Cosmetic differences that preserve meaning and operation may be triaged normally.

References:

- [Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)
- [WCAG 2.2 target size (minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- [WCAG 2.2 focus not obscured (minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum)

## Responsive, Asset, Motion, and Performance Baseline

### Responsive Behavior

- use one fluid component and content system rather than separate desktop and mobile implementations;
- choose component breakpoints from measured available space and content pressure rather than device labels alone;
- verify representative layouts at 320, 768, 1024, and 1440 CSS pixels and inspect intermediate widths for accidental overflow or unusable transitions;
- preserve full marketing information and actions on mobile because visitors may arrive there directly from search, social links, or shared event pages;
- preserve identity, rank, entity name, and the primary metric on dense narrow layouts; move secondary facts into labeled details, cards, or a deliberately scrollable region when needed;
- replace overflowing local navigation with a labeled jump menu or disclosure rather than an undisclosed horizontal gesture;
- collapse multi-column panels in a logical reading order and remove nonessential chassis ornament rather than shrinking desktop decoration into the content area;
- use the approved measured top-bar collapse model: brand, search, menu when required, and login/account remain directly accessible.

The test widths are review samples, not a requirement to encode exactly four media queries.

### Images and Video

- use the Next.js image pipeline for ordinary raster content, with correct intrinsic dimensions or aspect-ratio reservation and accurate responsive `sizes` values;
- request an appropriate source size and modern encoded format rather than sending one desktop source to every viewport;
- load only a genuine initial-view image eagerly; lazy-load below-the-fold media;
- prefer CSS and SVG for reusable framing, dividers, masks, grids, course traces, and terminal graphics where raster texture is unnecessary;
- keep material textures small, reusable, and low contrast; do not ship large images solely to create grit;
- use full-bleed gameplay imagery only where a strong current capture exists, and keep components functional when optional media is absent;
- show a lightweight poster before video and load playback resources on interaction or only when video is a genuinely prominent initial-view feature;
- reserve video dimensions before load and avoid autoplay behavior that competes with reading, data scanning, bandwidth, or reduced-motion preferences.

### Fonts

- use `next/font` and WOFF2 assets so font loading remains controlled and self-hosted with the deployed application;
- prefer variable fonts or a deliberately small weight/style set;
- preload only the primary reading face needed in the initial viewport, not every display and monospace variant;
- retain the approved role model of one readable proportional family, one related monospace face, and at most one distinct display face;
- target no more than approximately 200 KB of compressed initial font transfer and treat 300 KB as a hard initial-release ceiling;
- keep the selected typography usable under fallback and font-loading conditions without hiding text.

### Motion and Interactive Libraries

- use CSS transitions, CSS animations, or the Web Animations API for ordinary panel, menu, status, and terminal effects;
- do not add a site-wide JavaScript animation library for the initial implementation without a demonstrated interaction that needs it;
- animate compositor-friendly properties such as transform and opacity where possible and avoid layout-heavy continuous effects;
- keep critical content and controls available immediately rather than waiting for acquisition, scan, or type-on sequences;
- load charts, complex editors, and other substantial interactive libraries only on routes or modules that need them;
- preserve the complete reduced-motion behavior defined by the accessibility baseline.

### Transfer and Runtime Review Thresholds

Use the following compressed cold-load thresholds as investigation triggers:

- approximately 150 KB of client JavaScript for marketing and primarily server-rendered content routes;
- approximately 250 KB of client JavaScript for data-heavy interactive routes;
- approximately 1 MB for an initial compact collection response.

These are not automatic rejection or pagination thresholds. When a route exceeds them, inspect the dependency graph, projection, transfer time, parse/hydration cost, main-thread work, and memory on a representative lower-powered mobile device. Preserve the approved client-side collection model until measurements show that projection, deferred loading, or another bounded optimization is insufficient.

### User-Experience Targets and Verification

Target the current Core Web Vitals `good` thresholds at the 75th percentile, evaluated separately for mobile and desktop traffic:

- Largest Contentful Paint at or below 2.5 seconds;
- Interaction to Next Paint at or below 200 milliseconds;
- Cumulative Layout Shift at or below 0.1.

Before sufficient production traffic exists:

- run production-build bundle inspection on representative marketing, directory, entity-detail, chart-heavy, and authorized-form routes;
- use Lighthouse or equivalent lab measurements to identify regressions, not as the sole release verdict;
- test a cold load and meaningful interactions with network and CPU throttling;
- verify that images, fonts, authentication overlays, asynchronous results, and client-side filters do not introduce layout shifts or prolonged main-thread blocking;
- revisit real-user performance monitoring after launch only if traffic and operating needs justify an external tool; it is not an initial-release requirement.

References:

- [Web Vitals](https://web.dev/articles/vitals)
- [Next.js image optimization](https://nextjs.org/docs/app/getting-started/images)
- [Next.js font component](https://nextjs.org/docs/app/api-reference/components/font)
- [Next.js lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)

## SEO and Sharing Baseline

Treat SEO as low-cost technical hygiene, migration protection, and public-entity discoverability rather than a separate growth program. Use the standard Next.js metadata facilities; do not add a CMS, paid SEO platform, keyword-content program, or speculative structured-data system for the initial release.

### Metadata and Indexing

- set the metadata base from one trusted production-origin configuration value and never from request `Host` or forwarded-host headers;
- define one shared title template and give each indexable route a unique factual title and description;
- index the homepage, `/about`, `/brand`, code-authored public event pages, and public published gauntlet, pilot, team, and course index/detail pages;
- do not index site-search results, filter/sort result variants, authentication and callback routes, authorized management routes, administrative routes, preview deployments, or unpublished entities;
- derive dynamic entity metadata from the same public-safe projection that resolves the page, not a broader metadata-only read; optional statistics failure must not remove stable entity metadata;
- return the correct unavailable response for an unpublished or unknown public entity rather than serving an indexable empty shell;
- treat authentication and authorization as the security boundary; `robots.txt`, `noindex`, and hidden navigation are not access controls;
- apply a deployment-wide `X-Robots-Tag: noindex, nofollow` response or equivalent protection to development and preview environments so one route cannot accidentally opt into indexing;
- generate environment-aware `robots.txt` output: production advertises the canonical sitemap and may exclude protected/support paths, while development and preview disallow crawling and omit a production sitemap declaration.

### Canonical URLs and Query State

- select one HTTPS production origin before launch and use it consistently for metadata, sitemaps, structured data, social images, and internal absolute URLs;
- emit a self-referencing canonical URL for every indexable page;
- keep one canonical route for each entity and use stable route identifiers or slugs according to the approved route contract;
- keep client-side search, filtering, sorting, pagination, and section state out of the sitemap;
- when a directory query-result URL is shareable but is not intended as an independent search result, mark it `noindex` and canonicalize it to the base directory rather than creating an indexable page for each combination;
- normalize host, protocol, path casing, and trailing-slash behavior consistently.

### Sitemap and Legacy Retirement

- generate one cached sitemap containing repository-authored public routes/events, public current/upcoming/Past gauntlets, public pilots, public teams, and published or archived courses;
- exclude query variants, search, authentication, create/edit/manage/administrative routes, sponsor administration, wallet/prize routes, hidden/unpublished entities, and preview URLs;
- include a `lastModified` value only when it comes from a meaningful content or entity update timestamp;
- never replace a complete sitemap with a knowingly empty or partial successful result because Eventun or AccelByte is unavailable; retain the last complete cached result, or fail temporarily when no complete result exists;
- split the sitemap only when its measured size requires it;
- do not implement a legacy marketing or Ascentun redirect layer for the initial release at the current traffic level;
- update repository content, navigation, shared links, and the sitemap to use final canonical destinations directly;
- allow replaced or removed legacy routes to return `404`, while keeping the explicitly retained Midnight prize flow and its required Ascentun support reachable;
- add an exact redirect later only when a concrete inbound link or operational workflow demonstrates value.

### Social Sharing

- provide one branded 1200 by 630 default Open Graph image and a large-image social-card configuration;
- generate route-specific cards for entities and editorial events when factual names, categories, dates, and approved media make the result useful;
- provide a strong branded fallback when an entity has no suitable image;
- do not invent planet, course, sponsor, pilot, or team artwork solely for social metadata;
- keep important text within a safe central region and verify long names, missing media, and narrow platform crops.

### Structured Data

Start conservatively and emit JSON-LD only for facts visible on the page:

- use `Organization` and `WebSite` on the homepage;
- use `BreadcrumbList` on suitable public detail pages;
- use `Event` only on a unique editorial event page with verified event dates and physical or virtual location details;
- do not map a generic gauntlet to one `Event` while its qualifiers, stages, or ad hoc time windows cannot be represented accurately;
- do not describe pilot handles as `Person` or teams as conventional sports organizations without a later deliberate schema decision;
- do not add structured data merely because a schema type exists.

### Verification

Before cutover:

- inspect the rendered title, description, canonical URL, robots directives, and social metadata for each route class and relevant state;
- confirm the production sitemap contains every intended public canonical route and no private, query-result, preview, or unpublished route;
- test representative structured data and fix errors before enabling a type broadly;
- crawl the site anonymously to find broken internal links, incorrect response codes, and metadata fallbacks;
- verify that retired routes are absent from Website navigation and the sitemap and that the retained Midnight prize flow remains isolated on legacy Ascentun;
- add the final production origin to the selected search-console tooling and submit its sitemap after launch.

References:

- [Next.js metadata and Open Graph images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images)
- [Google canonical URL guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Google `noindex` guidance](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
- [Google event structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/event)
- [Google breadcrumb structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb)

## Hosting Direction

Vercel Pro is the confirmed hosting plan. The current Ascentun deployment uses two matching application/backend environments:

- `ascentun` for production, connected to Eventun in the production AccelByte game environment;
- `ascentundev` for development, connected to Eventun in the development AccelByte game environment.

Website V2 should preserve this two-environment operational model rather than inventing an independent website staging hierarchy. `ascentrivals.com` is the working production-domain assumption, subject to final DNS and cutover confirmation.

Approved deployment model:

- use two fixed Website environments connected only to the corresponding development or production Eventun deployment and AccelByte game environment;
- use protected branch previews only against the development environment; previews must never receive production Eventun or AccelByte credentials and must remain globally non-indexable;
- do not add a separate persistent staging backend or website environment for the initial release;
- use the Node.js runtime initially for Steam authentication, AccelByte integration, Eventun gateway access, and other server behavior;
- begin with one function region selected near the corresponding Eventun and AccelByte services; public cached content remains globally deliverable through Vercel's network;
- do not add multi-region functions until measured availability or latency requirements justify their consistency and operating cost;
- use standard Next.js rendering, cache, revalidation, image, and deployment primitives where they fit;
- do not design a custom multi-instance cache coordinator for the initial Vercel target;
- do not depend on process-local memory for correctness;
- avoid Vercel-specific domain logic when standard Next.js or HTTP behavior is sufficient;
- keep Eventun and AccelByte credentials, Steam verification material, and other secrets server-side and separated by environment.

Provisioning and cutover setup still must confirm:

- Website V2 Vercel project naming and team ownership;
- the exact development and production project/environment mapping and branch promotion rules;
- the selected function region after measuring Eventun/AccelByte latency;
- `ascentrivals.com`, the development hostname, the retained legacy Ascentun host, and DNS cutover ownership;
- image and bandwidth assumptions;
- default runtime-log handling and redaction;
- rollback and legacy-site coexistence behavior.

Reference:

- [Next.js self-hosting and cache coordination](https://nextjs.org/docs/app/guides/self-hosting)

## Analytics and Observability Deferral

Website V2 does not require Vercel Web Analytics, Vercel Speed Insights, Sentry, or another external analytics, insight, tracing, session-replay, or error-monitoring service for the initial release.

Initial requirements are limited to:

- accessible route and component error states with useful recovery actions;
- server logs sufficient to diagnose a recently reported failure while the platform retains them;
- structured log fields only where they materially help, such as environment, deployment, route template, operation, normalized failure category, duration, and a correlation/request id;
- redaction of cookies, authorization headers, tokens, Steam assertions, raw authentication payloads, request bodies, upload URLs, private Eventun responses, raw search text, and player identifiers;
- expected validation failures, cancellations, permission denials, and ordinary not-found responses handled as product states rather than logged as unexpected exceptions;
- manual and lab-based performance verification according to the approved performance baseline.

Accepted tradeoff: uncommon production failures may be discovered through user reports and may be harder to aggregate or diagnose after platform logs expire. This does not block initial release.

Later, evaluate a free, privacy-respecting aggregate page-analytics tool only if basic visit, referrer, or route-popularity information has a concrete use. Do not add advertising pixels, cross-site tracking, heatmaps, or session replay as part of that evaluation. Error aggregation, alerting, distributed tracing, and real-user performance monitoring remain separate future decisions rather than implied parts of basic page analytics.
