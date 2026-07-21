# Ascent Rivals Website V2 Initial Release Scope

Date: 2026-07-15
Status: Approved scope baseline
Last reviewed: 2026-07-20

## Related

- [[unified-design]]
- [[information-architecture]]
- [[non-functional-baseline]]
- [[delivery-plan]]
- [[route-api-matrix]]
- [[terminal-ops-design-system]]
- [[ascent-rivals/initiatives/website-v2/pages/player-profile]]
- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]
- [[flows/gauntlet-authoring]]
- [[ascent-rivals/initiatives/website-v2/README|Website V2 initiative index]]
- [[ascent-rivals/system/eventun/api|eventun-api]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]

## Goal

Ship one greenfield Next.js/React website that becomes the primary destination for both game discovery and player activity. The release replaces the current marketing site and Ascentun for approved public/player non-blockchain behavior, while administrator-only sponsor operations move to the Eventun Extend App. It then improves the public pilot, course, and team statistics experience.

This is a replacement release, not a read-only companion to the existing sites.

## Release Boundary

### Required

- current marketing content and conversion behavior selected for migration;
- public gauntlet, pilot, team, course, and search experiences, plus approved sponsor branding in gauntlet context and separately verified code-authored partner branding;
- Steam authentication, session refresh, logout, permission-aware actions, and personalized context;
- Ascentun's approved public/player non-blockchain workflows, with sponsor administration preserved through the Eventun Extend App handoff;
- better pilot, course, and team statistics using both exact tables and purposeful visualizations;
- canonical routes, SEO metadata, cutover, rollback, and deliberate legacy retirement for replaced behavior; a legacy redirect layer is not required at the current traffic level.

### Explicitly excluded

- wallet linking, verification, or management;
- Cardano or Midnight wallet support;
- token-gated teams or token catalogs;
- all Accountun-related prize and reward data, including public presentation, configuration, funding, claims, payouts, wallet requirements, and legacy workflow links;
- rebuilding the legacy sites or sharing their component implementations;
- a CMS, MDX pipeline, or custom art-production dependency.

Legacy prize/reward workflows may continue independently, but Website V2 does not expose or link them during the initial release. A manually maintained `/events/[slug]` page may include verified promotional prize copy, as the MSI tournament page does today; that editorial content is not an Accountun integration and must not imply live funding, eligibility, claim, or payout state.

## Ascentun Parity Matrix

The current implementation is the behavioral reference, not the target information architecture or visual design.

| Area | Current Ascentun behavior | Website V2 initial disposition |
|---|---|---|
| Discovery | Home search across gauntlets, teams, pilots, and admin-visible sponsors | Preserve grouped public search for gauntlets, teams, pilots, and courses; move sponsor discovery to the Eventun Extend App and keep only a form-scoped selector in gauntlet authoring |
| Pilot directory | Fuzzy search, team search context, sort, lazy loading, summary stats | Preserve and redesign |
| Pilot profile | Identity, team, career totals, per-course career totals | Preserve public identity, team, scoped competitive outcomes, and per-course records; add recent races and three-entry gauntlet history; treat broad cumulative totals and recognition as reversible own-profile candidates rather than anonymous-public parity |
| Course records | Eventun course and leaderboard APIs exist, but Ascentun has no dedicated public course route | Add `/courses` discovery and canonical `/courses/[code]` detail routes as required launch functionality |
| Team directory/profile | Search, identity, roster, membership mode, join/request, leave | Preserve and redesign |
| Team creation/management | Create; edit metadata, colors, membership, and media; invite; accept/deny requests; rank/designation changes; remove; transfer ownership; disband | Required launch parity, updated to the implemented team-feature contracts |
| Gauntlet directory/detail | Search/sort, schedule, qualifiers, stages/circuits, standings, sponsors, and media | Preserve and redesign |
| Gauntlet authoring | Create, edit, delete, qualifier and stage configuration, colors, media, direct `Billboard` upload with `Tileable` metadata, and existing sponsor association | Required launch parity for non-prize behavior; make gauntlet-owned campaign artwork primary, keep sponsor-entity selection optional/advanced, and exclude every prize/reward field and action |
| Sponsor operations | Admin list/detail, create, edit, colors, social links, and media | Explicit Website parity exception: move the complete administrator workflow to the Eventun Extend App before cutover; Website V2 has no sponsor registry routes and creators retain only a scoped existing-sponsor picker inside gauntlet authoring |
| Authentication | Steam login/callback, token refresh, session-aware permissions, logout | Required at launch |
| Media | Purpose lookup, signed upload URLs, previews, metadata, and entity media attachment | Required launch parity for Website team/gauntlet workflows; sponsor-owned media moves with sponsor administration to the Eventun Extend App and requires its own authorized upload boundary |
| Prizes and rewards | Accountun-related prize setup, presentation, funding, reward results, claim status, claims, wallet requirements, and payout planning | Entirely deferred; Website V2 neither consumes nor links these workflows |
| Wallets and token gates | Wallet integration remnants and retired token-gating artifacts | Excluded; do not migrate dormant artifacts |
| Theme test | Internal component/theme demonstration route | Retire; not product parity |

## Statistics Product Rule

Do not replace every table with a chart. Select the representation based on the question:

- use tables for exact rank, time, roster, designation, schedule, and match-row lookup;
- use charts for change over time, comparison across a bounded set, contribution composition, or distance between values;
- pair charts with exact values, accessible labels, and an equivalent reduced-motion/nonvisual reading path;
- never infer population percentiles from a top-N response;
- never compare raw course times across different courses as if they share one scale;
- never derive historical team performance from current roster membership;
- do not add decorative gauges, radar charts with incompatible axes, or fabricated live telemetry.

## Website API Contract Policy

The existing game-client reads are candidates for reuse, not a constraint that Website V2 must inherit every current response shape.

- reuse current Eventun or AccelByte-backed reads when their semantics, authorization, payload, and query behavior fit the page;
- add or revise server-side contracts when the Website needs different authoritative aggregation, chart-ready bounded series, public visibility, or page-level composition; ordinary directory filtering or display pagination alone does not justify a new contract;
- prefer domain-neutral Eventun read models that can be evaluated for game-client reuse over endpoint names and shapes coupled to one Website component, while allowing specialized runtime, operator, or authenticated contracts to remain separate;
- compute authoritative metrics and historical attribution in the owning backend, not in React components or from unrelated summary fields;
- allow the Next.js server layer to handle authentication, caching, and composition without making it a new statistics or configuration source of truth;
- avoid N+1 page loading and client-side joins when a bounded Website read model can return one internally consistent response;
- default all initial collection experiences, including players and collection-style histories, to a complete compact response with client-side search, filtering, sorting, and UI pagination or progressive reveal;
- keep collection projections shallow rather than transferring every entity's nested detail;
- do not make server pagination an initial-release requirement; add it only when measured query, response, parsing/hydration, memory, or interaction costs justify it, with histories and feeds expected to reach that point first;
- keep generated Eventun gateway clients, AccelByte service credentials, and player tokens in the Next.js server boundary rather than calling those services directly from browser components;
- use Server Components and server-only data functions for initial reads, and use same-origin Server Actions or route handlers for authenticated refreshes and mutations;
- project explicit browser view models rather than transferring complete generated transport records;
- allow direct browser media transfer only through bounded signed upload URLs obtained through an authorized server flow;
- see [[route-api-matrix]] for the per-route source, composition, browser, overlay, and contract-gap map.
- require explicit units, metric definitions, population/scope, time windows, freshness, and null/no-data semantics, plus pagination semantics only where server pagination is actually used;
- enforce hidden/internal content and permission filtering before data reaches the browser.

Approved gauntlet-discovery application:

- add one compact, unpaginated Eventun collection with server time, shallow public gauntlet presentation fields, normalized occurrences, and server-derived active/next/latest occurrence summaries;
- use it for `/gauntlets`, the repeated-occurrence Schedule view, the optional homepage teaser, and public gauntlet search without transferring full authoring/detail records;
- keep personalized participation as an optional authorized overlay so the base collection remains public and cacheable;
- make the contract domain-neutral for possible later game-client reuse, but defer game-client migration and retain current reads until their consumers are reviewed.

## Initial Analytics Surfaces

### Pilot

Required baseline:

- lead with pilot identity and a bounded career summary so the profile remains useful without recent gauntlet participation;
- use Matches, Podiums, Podium Rate, and Ascension Rate as the public headline career measures;
- define Ascension Rate over eligible Ascension-mode heats, with a success when the player
  either ascends or takes a podium place, counted at most once per heat;
- show exact numerators and denominators for both rates; use `Rate` consistently in headline
  and comparison labels;
- keep overall total and average Circuit Points, play time, credits/economy, detailed combat/objective
  totals, achievements, and medals out of the anonymous public response by default; they remain
  reversible own-profile candidates rather than approved public fields;
- make visualization optional in the headline summary; compact Podium Rate and Ascension Rate
  rails are valid when paired with their exact counts;
- exact per-course record and career table;
- exact recent-races table covering at most the newest 100 public-course multiplayer matches;
- compact `Gauntlet History` limited to the three gauntlets with the pilot's latest actual
  activity, regardless of lifecycle state;
- structure-aware gauntlet facts that keep qualifier rank, accepted stage placement, and general participation distinct;
- current course/category ranks where a player record exists.

Candidate launch visualizations supported by bounded data:

- raw per-match circuit points across the bounded recent Ascent Mode cohort, with an optional local course filter, no initial race-mode selector, and no rolling/improvement trend;
- a cross-course gap-to-record view for one explicit leaderboard category, normalized within each course and paired with exact pilot time, record time, and ordinal rank;
- an exact sortable per-course table as the canonical representation;
- compact composition bars for clearly related counts only when the denominator and interpretation are explicit.

Not supported without additional contracts:

- lifetime performance timelines from aggregate rollups;
- reliable population percentiles or distributions;
- record-progression history when only the current winning record is retained;
- checkpoint or segment analysis when website-safe geometry/detail is not exported.
- improvement or form trends from raw match circuit points without backend-derived comparable values or sufficient heat/rules/scoring context.
- one aggregate gauntlet-performance chart across unlike qualifier-only, staged, playtest, and future bracket structures.

Gauntlet-history contract requirement:

- use one compact Website-oriented player history read rather than an all-gauntlet join followed by per-gauntlet event requests;
- include only canonical public participation evidence, not invitations, eligibility, admission state, or a status row by itself;
- return gauntlet presentation metadata, active/completed state, latest player-activity time, applicable qualifier facts, accepted stage placements, and a small aggregate fallback;
- use `Final` only when the gauntlet contract explicitly marks a deciding final.
- return at most the three most recent entries for the public profile and do not add public
  pagination or progressive reveal.

Own-profile detail boundary:

- do not send candidate private career detail or recognition in the shared public response and
  then hide it in the browser;
- if approved later, compose an authorized own-profile response or overlay that is never placed
  in the shared public cache;
- keep the public/private calibration reversible until the implemented contracts and product
  value of the additional fields are reviewed.

### Course

Required baseline:

- course directory and selected-course briefing;
- category-specific leaderboard table;
- logged-in or selected pilot placement where available;
- clear Race/Time Trial and finish/lap player-facing category labeling without exposing ingestion or trust implementation details.

Candidate launch visualizations:

- top-N time-gap bars for one course and category, anchored to the winning time and paired with the exact leaderboard table;
- cross-category record summary for one course, without visually equating unlike finish and lap measures;
- generated checkpoint trace only when approved checkpoint geometry is exported through a stable website contract.

Not supported without additional contracts:

- whole-population time distributions or percentiles;
- historical record progression;
- checkpoint-sector comparisons from compact serving facts alone.

### Team

Required product outcome:

- prominent roster and individual pilot links;
- a concise fact-backed team performance summary that remains secondary to individual results;
- course strengths and recent team performance only where the implemented contracts support an approved metric;
- member contribution context attributed at performance time;
- exact roster and competition result tables.

Candidate visualizations after the required Eventun contracts exist:

- recent team placement or score trend;
- course-strength small multiples based on an approved team metric;
- bounded contributing-member bars for a selected competition or period;
- team-versus-field comparison where the comparison population and statistic are explicit.

Sequencing dependency:

The current Eventun foundation does not implement fact-backed team statistics, team leaderboards, or membership-at-performance-time attribution. The [teams delivery plan](../teams-and-team-gauntlets/delivery-plan.md) assigns those reads to T03 after the shared-development cutover and T00 design checkpoint. Website V2 is sequenced after that team feature work and may assume the resulting data is available for launch planning. The exact team-statistics modules must still be reviewed against the implemented contracts; Website V2 must not approximate missing behavior by summing the current roster's lifetime pilot totals.

Product-priority checkpoint:

- individual pilots and their exact results remain more prominent than team aggregates during the current design phase;
- re-evaluate team-stat prominence and visualization only after the team implementation has been exercised and iterated on;
- do not label team-represented individual results as team wins, placements, or standings unless the competition rules calculate those outcomes at team scope.

## Eventun Readiness Matrix

| Data need | Current status | Website implication |
|---|---|---|
| Pilot career totals | Implemented locally through `player_career_rollup` and accepted retained-data smoke | Usable in shared environments after their coordinated cutover; Website launch still depends on deployed production behavior |
| Pilot-course career totals | Implemented locally through `player_course_career_rollup` | Supports per-course profiles after the coordinated cutover |
| Current course records and ranks | Implemented locally through `player_course_record` and set-based leaderboard reads | Supports exact leaderboards and current placement after the coordinated cutover |
| Recent pilot match history | Uses player-selective narrow facts with keyed match/artifact lookup; response remains bounded | Supports the Recent Races table and raw result plot after the coordinated cutover; improvement trends require a later comparable backend value or richer rules context |
| Gauntlet stats and standings | Uses incremental contributions/projections and revisioned cutoff evidence | Supports refreshed gauntlet pages after the coordinated cutover |
| Course metadata | AccelByte Cloud Save `Courses`, optionally delivered through a controlled Eventun cache | Use the approved server-side projection: configured production-ready state maps to `published`, an explicit AccelByte retirement marker maps a previously public course to `archived`, and every other or invalid state remains hidden |
| Team metadata and current roster | Existing Eventun APIs | Supports directory, profile, roster, and management parity |
| Historical team attribution and team statistics | Planned [T03](../teams-and-team-gauntlets/delivery-plan.md#t03--add-fact-backed-team-views) work; not implemented at this review point | Website V2 follows this work and assumes the implemented reads are available by launch; finalize presentation after contract review |
| Course checkpoint geometry | Generated in the game; no approved website contract recorded | Optional enhancement with factual fallback |

The identified-match, projection, season, historical-rehearsal, and retained-data performance work is implemented and reviewed locally. The coordinated shared-development cutover remains pending, and production remains an independent owner-scheduled release. Website implementation may design against reviewed contracts, but launch acceptance must depend on deployed behavior rather than local worktree or rehearsal evidence.

## Launch Acceptance

Website V2 is ready to replace the two current sites only when:

- every approved non-blockchain Ascentun workflow has a tested Website V2 or Eventun Extend App destination or an explicitly approved retirement;
- all required marketing routes and content have migrated under the approved canonical routes;
- pilot and course analytics use production-cut-over Eventun reads;
- team analytics use fact-backed event-time attribution rather than current-roster inference;
- no Accountun-related prize/reward data or legacy workflow links are exposed by Website V2;
- Steam auth, permission checks, uploads, empty/error states, responsive layouts, accessibility, SEO, safe runtime logging, cutover, and rollback are verified; external analytics, insight, and error-observability services are not launch requirements.

## Confirmed Operational Scope

Approved non-blockchain operational workflows have an explicit launch destination:

- team creation/management and delegated gauntlet creation/editing/deletion remain in Website V2;
- team and gauntlet media upload/attachment remain in Website V2;
- sponsor administration and sponsor-owned media upload/attachment move to the Eventun Extend App;
- administrator-only bracket and runtime repair remain in the Eventun Extend App.

For gauntlet advertising, direct gauntlet-owned `Billboard` media are the default initial workflow. A purpose-specific control writes `Tileable = true` when the artwork can repeat across a ribbon-style placement. Reusable sponsor records remain administrator-owned, and their relationship picker stays optional and scoped to gauntlet authoring.

Keep initial media handling deliberately shallow. Existing media-purpose catalogs largely describe anticipated places an upload might be used; they are not evidence that every purpose has a current Website or game-client consumer. Preserve the configured attachment workflows for compatibility, but use shared labeled thumbnails and controls unless a verified consumer requires purpose-specific behavior. Billboard is the narrow initial exception: assume the current predominantly square artwork, show a normal square preview, and show three adjacent copies when `Tileable` is enabled. Do not make uploaded-dimension extraction, automatic aspect-ratio classification, or billboard-slot matching a launch requirement.

Gauntlet create/edit uses one sectioned form with Core Details, Competition Structure, Branding and Advertising, and Review and Save. It is not a wizard, does not imply a persisted draft or autosave, and keeps bracket authoring in a separate workspace.

Compatibility decision:

- retain existing sponsor records, sponsor media, gauntlet–sponsor relationships, and relationship tiers in Eventun and the Extend App workflow;
- keep existing relationships readable and editable through the advanced association control;
- do not flatten existing sponsor-associated media into gauntlet-owned media or delete relationships during Website V2 cutover;
- preserve direct gauntlet advertising media independently of sponsor-associated media.
- preserve existing `WideBillboard` records as legacy data without offering the unused purpose for new uploads; audit live data before coordinated backend/client removal.

Legacy prize/reward workflows remain independent and unlinked from Website V2. Team analytics are required for launch, but their exact page modules remain a later design checkpoint after the preceding team feature work is implemented.
