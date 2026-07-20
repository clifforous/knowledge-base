# 2026-07-15 Website V2 Design Restart

**Status:** Active
**Project:** Ascent Rivals Website V2
**References:**
- `30_designs/ascent-rivals/website/unified-design.md`
- `30_designs/ascent-rivals/website/design-doc-roadmap.md`
- `30_designs/ascent-rivals/website/information-architecture.md`
- `30_designs/ascent-rivals/website/initial-release-scope.md`
- `30_designs/ascent-rivals/website/delivery-plan.md`
- `30_designs/ascent-rivals/website/route-api-matrix.md`
- `30_designs/ascent-rivals/website/terminal-ops-design-system.md`
- `30_designs/ascent-rivals/website/design-language-v0.1.md`
- [Ascent Website](https://github.com/ikigai-github/ascent-website)
- [Ascentun](https://github.com/ikigai-github/ascentun)

---

## Goal

Resume Website V2 design work, validate the technical and product direction one decision at a time, and update the existing design set before implementation planning begins.

## Confirmed Scope Decisions

- Website V2 combines the marketing and player-facing public experiences.
- Website V2 is intended to replace both the current marketing site and Ascentun, rather than launch as a read-only companion.
- The initial release must provide at least Ascentun's current non-blockchain functionality and add a stronger public statistics experience for pilots, courses, and teams.
- Current non-blockchain operational workflows receive explicit launch destinations: team and delegated gauntlet workflows remain in Website V2, while administrator-only sponsor administration/media move to the Eventun Extend App.
- Website V2 follows the planned team feature work. Initial planning may assume fact-backed team data will be available by Website V2 launch, but the exact team-statistics modules remain provisional until the implemented team contracts can be reviewed.
- Website V2 will be implemented as a greenfield project rather than by extending `ascent-website` or `ascentun`.
- The existing websites are content, behavior, asset, and migration references only.
- Token-gated teams are not part of Website V2.
- Wallet linking and wallet management are not part of the initial Website V2 release.
- All Accountun-related prize and reward data is deferred. Website V2 does not display, link, configure, fund, claim, pay out, or administer data-driven prizes/rewards in the initial release; verified code-authored promotional prize copy remains allowed on editorial event pages.
- Marketing content remains code-authored from approved design mocks; no CMS is planned for the initial release.
- Terminal Ops remains the visual starting point, but the next design pass should push it toward a stronger sci-fi identity while retaining industrial material cues and data readability.

## Current Technical Facts

- As of 2026-07-15, both `ascent-website` and `ascentun` use Next.js 16.2, React 19.2, TypeScript 6, Tailwind CSS 4, and Radix-based UI primitives.
- `ascent-website` already owns the actively maintained marketing homepage, about, brand, tournament, and event content.
- `ascentun` remains the reference for player, team, gauntlet, sponsor, and authentication behavior; its prize/reward behavior is explicitly outside Website V2 reference parity.
- Eventun remains the primary website data service; Website V2 does not need to become a new domain backend.
- Existing game-client API shapes are reusable but not frozen Website contracts. New or revised Website-oriented reads are allowed where authoritative aggregation, chart series, visibility, or response composition differ; ordinary directory filtering and UI pagination remain client-side by default.
- Eventun F14 implements incremental pilot career, pilot-course career, course-record, leaderboard, match-history, and gauntlet serving paths in the current worktree. These are not production-ready until F14 review and the F15 historical backfill and cutover complete.
- Fact-backed team statistics, team leaderboards, and event-time membership attribution are not implemented by F14. They remain planned Eventun T03 work after the F15/T00 checkpoint and are a backend dependency for credible launch team analytics.
- Ascent Rivals uses AGS Shared Cloud, which exposes a subset of Private Cloud features and configuration. AccelByte-dependent Website designs are checked against current documentation and the actual namespace; the existing working Ascentun Steam exchange is explicitly accepted as sufficient architecture evidence despite the public documentation ambiguity.
- The existing Vercel Pro plan hosts `ascentun` for production and `ascentundev` for development, each paired with Eventun in the corresponding AccelByte game environment; Website V2 should retain this two-environment model, with `ascentrivals.com` as the working production-domain assumption pending cutover confirmation.

## Ordered Review Queue

### 1. Framework and Repository Direction

- [x] Use Next.js with React and TypeScript for Website V2.
- [x] Use a new greenfield project rather than extending `ascent-website` or `ascentun`.
- [x] Record the decision and rationale in the canonical unified design document.
- [ ] Reconcile remaining superseded Nuxt/Vue/Reka references in active Website V2 page, flow, shell, Pencil-prompt, and roadmap documents; preserve original concept briefs only when they are clearly labeled as historical inputs.

Recorded decision:

- use a new greenfield Next.js/React/TypeScript project;
- treat `ascent-website` and Ascentun as reference and migration sources only;
- create custom Ascent Rivals components over unstyled accessible primitives rather than adopting starter-kit styling wholesale;
- use code review and manual browser review as the default design-iteration loop;
- add Storybook, automated screenshots, or visual-regression tooling only when repeated state coverage or regression risk justifies the added maintenance and AI-token cost.

Decision criteria:

- migration cost and reusable code;
- developer familiarity and maintenance burden;
- compatibility with designer handoff and generated component output;
- correctness and observability support for AI coding agents;
- component-isolation and visual-regression workflow;
- public-page SEO and rendering;
- Steam authentication and Eventun integration;
- data-heavy interactive pages;
- deployment portability;
- visual-system freedom;
- testing and operational complexity.

Candidate UI libraries, styling conventions, and test tools remain separate implementation decisions. The framework decision does not require adopting a pre-styled component kit.

### 2. Marketing Content and Information Architecture

- [x] Inventory the current `ascent-website` routes and content against the proposed Website V2 route map.
- [x] Keep `/` as the primary marketing landing page; use `/gauntlets` as the primary competition and player entry.
- [x] Reserve `/gauntlets` for Eventun-backed competition and migrate code-authored tournament/editorial content to `/events`.
- [x] Keep `/about` as a concise studio, mission, current-team, and verified-recognition page.
- [x] Retain `/brand` as a public, repository-managed brand-kit route and revise its visual guidance after the Website V2 design system is approved.
- [x] Decide the final relationship between `/`, `/game`, `/about`, `/brand`, `/tournaments` or `/events`, and the player/competition routes.
- [x] Identify content to preserve, rewrite, merge, redirect, or retire.
- [x] Define the code-authored content update convention without introducing a CMS.
- [x] Record canonical URLs, deliberate legacy-route retirement, metadata, and historical-event handling.

Recorded direction:

- retain the homepage's marketing and conversion purpose;
- allow real gauntlet, player, record, partner, and community proof as supporting content without turning `/` into a dashboard;
- use light additive personalization for logged-in visitors rather than a different homepage;
- defer `/game` from the initial route map and create it later only if deeper game modes, systems, ships, courses, or worldbuilding provide material content beyond `/`;
- use `/events` and `/events/[slug]` for code-authored LAN, showcase, sponsored-tournament, historical, and recorded-event content;
- retire `/tournaments` and its MSI Grand Prix detail route without an initial redirect layer at the current negligible external traffic level;
- keep Eventun-backed competition under `/gauntlets` and omit all prize/reward content and legacy workflow links from Website V2;
- keep `/about` concise; move event appearances and recaps to `/events`, associate useful videos with event details, and link to YouTube for the broader vlog archive;
- verify team, role, mission, and recognition content before migration;
- retain `/brand` for verified logo downloads and usage rules; revalidate spacing and replace visual-system guidance only after the revised Terminal Ops direction is approved;
- keep brand assets repository-managed and allow a future `/press` page to link to, rather than replace, `/brand`;
- use plain TypeScript and TSX for initial marketing content, with short copy beside its component and long or structured content in route-local typed `content.ts` files;
- use shared typed models only for genuinely repeated structures such as editorial events, keep metadata with route content, and allow bespoke sections when approved designs require them;
- continue the approved mock and assets to implementation, code review, and manual responsive browser review workflow without adding CMS or MDX machinery;
- preserve the current homepage's content categories but rewrite or verify its copy and media, and rebuild its layout and components from scratch;
- treat the current homepage implementation, backgrounds, clipping treatments, and styling as references only, and add a restrained `/gauntlets` bridge for Website V2;
- treat the current homepage, about, brand, tournament history, and MSI Grand Prix content as migration inputs requiring accuracy and route review.

### 3. Terminal Ops Sci-Fi Design Review

- [x] Review the existing homepage, gauntlet-detail, and marketing concept images against current product requirements.
- [x] Define which industrial Terminal Ops elements remain canonical.
- [x] Specify the stronger sci-fi additions through shape language, materials, imagery, light, typography, motion, and world-specific interface motifs.
- [x] Avoid generic terminal, generic esports, crypto-luxury, and unreadable all-monospace outcomes.
- [x] Calibrate the visual direction through clean HUD Overlay, race-control terminal, reference-grounded panel, balanced-corner, and cutout-placement Pencil studies.
- [x] Reject faux scrap-metal component styling, smooth gray metal gradients, arbitrary hexagons, random border fragments, and per-card polygon randomization.
- [x] Establish a provisional directional-panel grammar for corners, mid-edge cutouts, signal rails, CTA motion, and framed-versus-open information.
- [x] Apply the provisional grammar to one complete desktop homepage composition and review it at normal viewing size.
- [x] Create and refine the corresponding mobile homepage composition after desktop approval.
- [x] Extract Design Language v0.1 from the approved applied composition.
- [ ] Produce or commission revised mocks for marketing, a data-heavy player page, gauntlet detail, and mobile.
- [ ] Approve, revise, or replace Terminal Ops after reviewing those mocks.

Recorded visual foundation:

- keep the terminal as the core in-world interface metaphor;
- replace present-day Linux and filesystem imitation with an original, readable Ascent Rivals information and command language;
- make the terminal a plausible source for gauntlet, team, pilot, planet, course, ship, and world information;
- use a modern race-control surface built from matte graphite panels, flat tonal separation, crisp seams, restrained inset depth, and selective signal lighting;
- keep scrapyard wear as optional atmosphere, background art, gameplay imagery, or occasional shell detail rather than simulating rusted metal across ordinary UI components;
- treat the existing static exploded diagram based on an old ship model as reference-only; use schematics later only with current approved game models or data and a stronger diagnostic, modular, or interactive purpose.
- use a hybrid terminal interaction model: conventional navigation remains primary and accessible, while a global entity-query console supports optional readable commands such as `FIND`, `OPEN`, `SCAN`, and `TRACK`;
- frame the interface as an access point into a distributed underground race-information network, while keeping exact authorities, orbital deployment, manufacturer roles, spectator culture, and betting as exploratory lore rather than Website V2 requirements;
- use outlaw-race urgency as atmosphere only where supported by real timing or state, and do not fabricate live signals, shutdown pressure, viewer activity, or wagering data.
- use amber/gold as the dominant emissive display color, with restrained green, cyan, and red for functional state; place it behind worn display glass with localized scan, bloom, and signal effects rather than constant CRT noise;
- prioritize readability through a proportional body face and reserve condensed display or monospace typography for shorter roles;
- compare Saira Semi Condensed plus IBM Plex Sans/Mono against an all-IBM Plex system, use Atkinson Hyperlegible Next as a readability benchmark, and retain Opinion Pro Condensed only if webfont licensing is verified;
- validate typography using real marketing copy, a data table, terminal search results, ambiguous identifiers, and mobile labels before selecting a final system.
- treat each page as one terminal system; establish a restrained persistent shell, reserve stronger framing for major modules, and use lighter rails, open composition, or unframed regions for ordinary information;
- allow marketing pages more cinematic depth and atmospheric material while keeping player and competition pages calmer and data-forward;
- derive cuts, seams, latches, recesses, and asymmetry from plausible fabricated construction rather than generic sci-fi decoration.
- do not depend on bespoke planet art, illustrated course maps, or an ongoing custom-art pipeline;
- prioritize current gameplay captures and video, then terminal-native graphics generated from real data, with material and signal treatments carrying pages that have limited imagery;
- present planets through factual environment context, available in-game captures, and clearly procedural scan graphics rather than invented planet paintings;
- treat the game's checkpoint-generated course trace as a strong terminal graphic when an approved export or website data contract exists, with course stills and factual metadata as the fallback;
- treat Fab source assets as game-production inputs rather than standalone website art, and never expose raw source assets through the public site.
- allow bespoke planet and course artwork later, but give initial components optional media slots and strong non-image fallbacks so art production cannot block functional routes;
- use restrained functional motion for signal acquisition, actual data changes, course-trace drawing, and mechanical response; avoid constant flicker, repeated boot effects, long typing, or delayed content, and provide full reduced-motion behavior.

Pencil calibration findings recorded on 2026-07-18:

- the clean HUD Overlay direction is the strongest composition base: open cinematic field, left-weighted hero content, sparse scan treatment, thin rules, and compact `//` notation;
- the homepage should not return to a boxed Linux-terminal simulation or a heavily plated scrap-metal chassis;
- paired forward chevrons and a short directional termination are the preferred CTA motifs; hover/focus may use a subtle one-time approximately 4px advance rather than continuous animation;
- diamond nodes are the preferred Ascension progression marker;
- a reusable panel family must use named variants rather than random cuts per card, and ordinary tables, metadata, and long-form regions may remain unframed;
- valid corner topologies are zero, one, two diagonally opposed, or all four cuts; avoid three cuts or two adjacent cuts on the same side;
- mid-edge cutouts count any inward removal from the rectangular envelope, including continuing shoulders; no side is mandatory and positions or dimensions need not be symmetric;
- the cutout-placement studies informed balance, but the complete homepage showed that repeated mid-edge cutouts become gimmicky in composition;
- default repeated cards to zero mid-edge cutouts, allowing a single shallow top cut for a header/tab relationship, a single side cut beside related open content, or a bespoke cut on a major media/hero frame with a structural reason;
- a short neutral signal rail with a smaller gold termination is optional state geometry, not default decoration; generic hex identity marks and randomly placed gray/gold fragments are rejected;
- implementation remains feasible with CSS clip paths or masks for filled surfaces, inline SVG for sparse edge geometry, and semantic HTML for content; raster assets are reserved for atmosphere and imagery rather than panel construction.

Visual-design progress:

1. [x] desktop homepage composition calibration;
2. [x] desktop review and iteration at normal viewing size;
3. [x] mobile homepage companion and compact-header refinement;
4. [x] Design Language v0.1 extraction into durable design-system documentation;
5. [ ] representative page mocks for gauntlet listing/calendar, gauntlet detail, player profile, course detail/leaderboard, and later team pages;
6. [ ] continued design-language revision as those page archetypes expose missing table, chart, filter, state, or responsive rules.

### 4. Initial Replacement Product Scope

- [x] Set replacement parity, rather than a read-only public companion, as the initial release target.
- [x] Require at least Ascentun's current non-blockchain functionality.
- [x] Include gauntlets, players, teams, courses, and grouped public entity search in the phase-one route model; keep the Eventun sponsor registry out of public routes and public search.
- [x] Include Steam authentication, session handling, logout, and personalized overlays in the initial release.
- [x] Make better pilot, course, and team statistics part of the initial release definition, using visualizations only where they communicate a relationship or trend more clearly than a table.
- [x] Keep exact rankings, rosters, Recent Races, and other scan-and-compare data in tables where tables are the clearer representation.
- [x] Remove wallet, token-gating, and every Accountun-related prize/reward dependency, presentation module, action, and legacy link from initial Website V2 acceptance criteria.
- [x] Confirm the split operational boundary: Website V2 owns team and delegated gauntlet workflows/media; the Eventun Extend App owns administrator sponsor CRUD/media plus administrator-only bracket/runtime repair.
- [x] Approve the detailed parity and analytics matrix in `30_designs/ascent-rivals/website/initial-release-scope.md`.
- [x] Sequence Website V2 after the team feature work and assume its fact-backed team reads will be available by launch; defer exact team-statistics presentation until those implemented contracts can be reviewed.
- [x] Lead the pilot profile with identity and career summary rather than recent gauntlet results.
- [x] Use Matches, Podiums, Podium Rate, and Average Circuit Points as the primary career-summary measures, with Results, Objectives, Combat, Activity, and Economy detail groups.
- [x] Keep career-summary visualization optional; permit a compact podium-share graphic only when paired with exact counts and do not fabricate trends from aggregate totals.
- [x] Use an exact newest-first `Recent Races` table for at most 100 public-course multiplayer matches; optionally show discrete raw Circuit Points for recent Ascent Mode matches, allow local course filtering, and do not claim or draw an improvement trend without a backend-derived comparable value or sufficient rules context.
- [x] Use a structure-aware player `Gauntlet History`: active public participation first, completed entries by latest actual player activity, and distinct qualifier, accepted-stage, and general-participation summaries without an aggregate cross-gauntlet chart.
- [x] Exclude gauntlet invitations, eligibility, admission, group assignment, and status-only rows from another player's public history; never present qualifier rank as a tournament finish or infer `Final` from stage order.
- [x] Use `Achievements & Medals` for public recognition: completed public Eventun achievements/masteries first, known gameplay-medal totals second, and no inferred trophies, public incomplete progress, active challenges, or reward UI.
- [x] Remove generic global rank tiers and `Rank History` from the initial profile and directory; keep exact course leaderboard positions and gauntlet standings in their scoped contexts and omit exact AccelByte MMR even for the current user.
- [x] Treat a future Eventun-owned named-division layer with stateful promotion thresholds or delayed promotion as a separate design, not as a Website-derived mapping from current MMR or item-recommender bands.
- [x] Use an exact sortable course table plus an optional normalized gap-to-record view for one explicit leaderboard category; do not compare raw times across courses or imply percentile.
- [x] Use `/courses` for discovery and `/courses/[code]` for canonical shareable detail, with leaderboard category preserved in query state.
- [x] Default course leaderboards to `Race Finish`, followed by `Race Lap`, `Time Trial Finish`, `Time Trial Lap`, and loadout-challenge variants; keep source validation internal and do not use `Official`, `Server`, `Client`, or authority language in public labels.
- [x] Name the inclusive low- and high-cost time-trial categories `3K Class` and `10K Class`, with concise help text stating the 3,000-or-less and 10,000-or-less loadout-value caps.
- [x] Use `Race` as the mode-neutral public leaderboard context and foreground Ascent Mode in gameplay explanation because nearly all current races use it.
- [ ] Add a race-mode leaderboard selector only after Eventun exposes mode-scoped records and ranks; preserve Classic and Deathmatch as future filter values.
- [x] Treat AccelByte Cloud Save `Courses` as the course metadata and feature-state source of truth; use production-ready courses by default and expose only explicitly retired, previously public courses through an `Archived` filter.
- [x] Define a server-side Website course-visibility contract: configured production-ready state maps to `published`, an explicit AccelByte retirement marker maps a previously public course to `archived`, all other or invalid states fail closed to hidden, and public reads expose only published/archived records.
- [x] Show loadout value as a compact secondary leaderboard column on desktop; retain it in the primary mobile row for 3K/10K Class boards and move it into row details for ordinary Race and Time Trial boards.
- [x] Allow purpose-built Website API requirements rather than forcing every page to consume the simpler game-client response shapes.
- [x] Keep individual pilots, pilot profiles, and roster results more prominent than aggregate team analytics; retain fact-backed team stats in launch scope but re-evaluate their exact modules after the team implementation has been exercised and iterated on.
- [x] Keep ordinary membership actions on `/teams/[id]` and use `/teams/[id]/manage` for metadata, media, roster administration, invitations, join requests, ownership transfer, and disbanding, reached through a permission-aware team-profile action.
- [x] Show the public team membership mode to every audience using `Open`, `Request to Join`, and `Invite Only`; map the final new-team enum values to these stable labels after implementation review.
- [x] Make gauntlet-detail priority state- and composition-aware: qualifiers and stages are independently optional, empty phases are omitted, and the next/current/result module is selected from the competition structure that actually exists.
- [x] Use `Qualifier`, `Stage`, `Final`, and `Bracket` according to actual competition semantics; reserve `Final` for an explicitly deciding stage and `Bracket` for a published bracket graph.
- [x] Defer a gauntlet broadcast module and `/watch`: current shoutcasting is a user launching the game as a spectator and streaming through a personal Twitch channel, with no canonical broadcaster, URL, or live-status contract. Allow only manually verified links on code-authored event pages.
- [x] Keep ordinary non-prize gauntlet creation/editing/deletion in Website V2 and place initially administrator-only bracket mutation, runtime stage-session, and result-repair controls in the Eventun Extend App UI.
- [x] Use `Sponsor` for the Eventun-backed competition entity; reserve `Partner` for broader verified code-authored marketing relationships and defer `/partners` until distinct content justifies it.
- [x] Remove sponsor registry/detail/CRUD routes from Website V2 and move the complete administrator workflow to the Eventun Extend App before cutover; ordinary visitors see only approved sponsorship branding in gauntlet or code-authored marketing context.
- [x] Treat sponsor tier as gauntlet-specific operational data that may influence in-game advertising placement, not as a global or public sponsor rank.
- [x] Make direct gauntlet-owned `Billboard` upload the primary creator workflow and expose `Tileable` metadata for ribbon-style placements; retain reusable sponsor-entity association only as an optional advanced control scoped to gauntlet authoring.
- [x] Keep initial media UI shallow: use generic labeled thumbnails for configured media purposes, assume square billboard creative, show three copies for the tileable preview, and defer dimension-derived aspect-ratio or slot matching.
- [x] Preserve existing sponsor records, sponsor media, gauntlet–sponsor relationships, and tiers at Website V2 cutover rather than flattening them into direct gauntlet media.
- [ ] Revisit game-client billboard placement separately: consider authored course slots, manual organizer or future sponsor selection, multiple shapes/aspect ratios, trackside and vehicle placements, and holographic variants.
- [ ] If sponsorship expands beyond direct billboard uploads, evaluate a sponsor–gauntlet campaign model that separates stable sponsor identity from tournament-specific creative and placement.
- [ ] Audit live `WideBillboard` media, then coordinate retirement of the unused purpose and game-client collection if no required data or consumer is found; preserve existing records until that decision.
- [ ] Audit actual consumers of sponsor, gauntlet, and team media-purpose values and metadata before adding custom UI or retiring unused types.
- [ ] Implement and verify Eventun Extend App sponsor list/detail/create/update/delete-or-block behavior, including atomic writes and correction of the stale `gauntlet_media.sponsor_id` delete statement.
- [ ] Implement or deliberately reuse an Eventun-admin-authorized sponsor media upload-intent flow for the Extend App; verify upload, preview, attach, replace, remove, and retained media consumption before Ascentun cutover.

### 5. Knowledge-Base Reconciliation

- [ ] Update the unified design, information architecture, page specs, and flow specs with confirmed scope decisions.
- [ ] Remove retired token-gating branches instead of relying only on supersession warnings.
- [x] Remove wallet requirements from the initial-release route and state matrices.
- [x] Exclude legacy Ascentun prize/reward behavior entirely from Website V2 feature parity and defer the Accountun boundary for later redesign.
- [x] Resolve the top-navigation contradiction: use one responsive top bar with stable `Gauntlets`, `Pilots`, `Teams`, `Courses`, and `Events` destinations, direct search/account utilities, priority-based `More` disclosure, and no persistent global side navigation or separate cross-site bridge control.
- [x] Define page-local navigation: readable anchors for long pages and forms, tabs only for mutually exclusive panels, segmented controls for small filters, URL-backed shareable state, compact mobile jump menus, and no command syntax as the only label.
- [x] Define the initial account menu as `My Career`, `My Team` with concise pending invitation/request status, conditional `Admin / Operations`, and a separated `Sign Out`; keep object creation/editing contextual and exclude wallets.
- [x] Use a direct `Sign in with Steam` action with no one-option provider picker; treat Epic, Discord, and other providers as future identity/linking designs only after a concrete use case is approved.
- [x] Approve grouped global search over the compact public gauntlet, pilot, team, and course collections with client-side matching and directory-query fallbacks.
- [ ] Create a consolidated decision and open-question register.

### 6. Page and Flow Specification Completion

- [x] Rewrite the homepage page specification for the approved marketing-first direction.
- [x] Use `Play Now` as the default hero conversion, allow reliable confirmed ownership to promote `Explore Gauntlets`, and never infer ownership or installation from sign-in alone.
- [x] Keep homepage section order, module placement, responsive composition, and CTA region consistent across anonymous and authenticated states; limit personalization to content or actions inside existing slots.
- [x] Allow one bounded optional race-network module: prefer meaningful active/upcoming gauntlet data, fall back to a recent verified gauntlet or code-authored event recap, and omit it rather than rendering stale, empty, or fabricated activity.
- [ ] Create a `/game` page specification only if the route is later approved based on distinct content.
- [ ] Update public page specifications against current Eventun contracts.
- [x] Reconcile the `/gauntlets` discovery specification with current gauntlet and calendar contracts: unique entity directory, repeated-occurrence Schedule agenda, occurrence-based inclusion, nearest-event ordering, and Past history scope.
- [x] Constrain gauntlet media composition: fixed media bays for ordinary directory cards, opaque information surfaces, image-light Schedule rows, and full-bleed `Background` treatment only for detail or a deliberately featured module with contrast review.
- [x] Preserve Eventun's all-public gauntlet model: successful creation publishes immediately, Past remains public and searchable, and Website V2 does not infer hidden state from timing or game-client list omission.
- [x] Add a compact, unpaginated, domain-neutral Eventun gauntlet-discovery collection with shallow presentation fields, normalized occurrences, server time, and server-derived active/next/latest occurrence data rather than joining the four current list/calendar reads in Website V2.
- [ ] After Website contract design, review game-client gauntlet list/calendar consumers for migration to the shared discovery read; retain current client reads until generated Unreal types, auth, caching, timing, and specialized runtime needs are evaluated.
- [x] Define `/players` as a public pilot registry: include every real usable identity, exclude bot/test/internal records only through explicit classification, default to alphabetical local search/sort, and use a compact unpaginated directory collection with only card/search fields.
- [x] Keep player-directory team identity quiet: `[TAG] Team Name` where space permits, tag-only on compact cards, `Independent` when unaffiliated, no second team avatar, and only restrained accessible team-color accents.
- [x] Exclude time trials, Career Cup, and other single-player activity from profile `Recent Races`; keep their retained best lap and best finish records on course/career surfaces.
- [x] Use the newest 100 races as the initial recent-history bound and treat Eventun seasons as the later grouping/boundary; defer exact season navigation and unseasoned-history treatment until the implemented F16A contract is reviewed.
- [ ] Preserve missing-versus-zero match-stat semantics through generated Go, gateway/TypeScript, and selected Unreal models; prefer protobuf optional fields when verified, otherwise add explicit availability metadata, and never use zero-as-missing where zero/false is valid.
- [ ] Filter public Recent Races to published/archived courses and strip client version, replay key, session id, match id, and other unrendered implementation fields before the payload reaches the browser.
- [ ] Add a compact Website-oriented player-gauntlet-history read with presentation metadata, lifecycle state, latest real activity time, qualifier facts, accepted stage placements, aggregate fallback facts, and explicit missing-value semantics; avoid per-gauntlet browser requests.
- [ ] Add a compact public player-recognition read with authored goal and medal presentation fields, explicit historical coverage, and no raw counters/dimensions, source ids, active/incomplete progress, private/hidden goals, or reward data.
- [x] Update the Steam authentication flow specification for the confirmed initial scope.
- [x] Record AGS Shared Cloud as a cross-project platform constraint and identify the ambiguity between AccelByte's unsupported Shared Cloud web-login classification and Ascentun's custom `steamopenid` V4 platform-token flow.
- [x] Draft the Website V2 authentication/session route group, including trusted-origin callback construction, one-time login transactions, Login Queue continuation, explicit browser session projection, serialized refresh, best-effort token revocation, and safe logout destinations.
- [x] Prohibit Ascentun's browser-readable user-info cookie from serving as a Website V2 server authorization, role, or team-state source; keep browser identity display as an explicit output projection.
- [x] Review and approve the authentication/session route group.
- [x] Accept the deployed Ascentun Steam OpenID to AccelByte V4 exchange as sufficient architecture evidence; do not require a separate vendor-support answer or duplicate pre-implementation smoke-test gate.
- [ ] During Website V2 implementation, verify successful login, refresh, logout, cancellation, invalid/replayed assertion, linking, and documented Login Queue behavior in the matching development environment as ordinary release acceptance.
- [ ] Specify any remaining approved team, gauntlet, or personalized flows; sponsor administration is assigned to the Eventun Extend App handoff specification.
- [ ] Reconcile Website V2 gauntlet create/edit authoring with the post-team bracket work, including allocation rules, field publication, single-elimination generation, seeds, byes, versioned publication, and audited repair.
- [x] Keep core gauntlet creation separate from bracket authoring rather than expanding the current single-page form into one combined operator form.
- [x] Use one sectioned create/edit form rather than a wizard: Core Details, Competition Structure, Branding and Advertising, and Review and Save; do not imply draft persistence or autosave without a backend contract.
- [x] Add a dedicated core gauntlet-authoring flow covering section navigation, validation, media-upload state, responsive behavior, failure handling, and the separation from brackets/runtime operations.
- [x] Route successful gauntlet create and edit to a freshly revalidated `/gauntlets/[id]` detail page as the canonical manual-review checkpoint.
- [x] Keep delegated core gauntlet create/edit/delete in Website V2; use the Eventun Extend App UI as the initial boundary for administrator-only bracket generation/publication/repair and runtime repair, without duplicating the core form.
- [ ] Require Website V2 to render the published bracket graph and public match state when bracket contracts ship, without assuming that public-site gauntlet creators can mutate the graph.
- [ ] Keep deferred legacy workflows out of Website V2 acceptance criteria.

### 7. Non-Functional Baseline

- [x] Default every initial collection experience to one compact fetch with client-side search, filtering, sorting, and display pagination/progressive reveal; add server pagination only after measured query, transfer, parsing/hydration, memory, or interaction costs justify it.
- [x] Define rendering and caching rules: static repository-authored marketing, tagged stale-while-revalidate public data, boundary-aware schedule freshness, short-cache standings/results, request-time private overlays, and mutation-driven entity/collection invalidation.
- [x] Define WCAG 2.2 AA accessibility acceptance requirements, including semantic terminal UI, keyboard/focus behavior, contrast, target sizing, reflow, data-visualization alternatives, reduced motion, and a representative manual verification matrix.
- [x] Define responsive behavior plus image, font, motion, and performance budgets, including fluid layouts, representative review widths, optimized optional media, controlled font loading, route-local heavy libraries, transfer review thresholds, and Core Web Vitals targets.
- [x] Define lightweight SEO metadata, indexing, structured-data, canonical URL, sitemap, legacy-route retirement, and social-sharing rules without adding a separate content-growth system.
- [x] Record the existing Vercel Pro plan and matching `ascentun` production / `ascentundev` development model while retaining standard Next.js primitives and keeping private state out of shared caches.
- [x] Confirm the hosting/deployment baseline: existing Vercel Pro plan, two fixed Website environments paired to the matching AccelByte/Eventun environments, protected non-indexable previews using development only, Node.js runtime, and an initial single region near the backends.
- [ ] Provision the final Vercel projects/environments, select the measured function region, confirm hostnames and branch promotion, and execute DNS/cutover and rollback setup during implementation.
- [x] Defer Vercel Analytics/Speed Insights, Sentry, and all other external analytics/error-observability services from launch; retain safe short-lived runtime logging, accessible error states, and manual performance verification.
- [ ] Later evaluate a free privacy-respecting aggregate page-analytics tool if route, visit, or referrer data gains a concrete product or marketing use.

### 8. Migration and Delivery Plan

- [x] Choose an incremental greenfield route-slice sequence that keeps the current marketing site and Ascentun available until their replacement responsibilities are verified.
- [x] Define the Website integration boundary: generated Eventun/AccelByte clients and credentials remain server-only, initial reads use server data functions, authenticated refreshes/mutations use same-origin actions or handlers, browser models are explicit projections, and direct transfer is limited to signed media uploads.
- [x] Map approved routes to source systems and existing or required Website APIs, then identify contract changes and new read models.
- [x] Review and approve the repository-authored marketing/editorial and gauntlet route groups in the route/API matrix, including the separate stable-detail, standings/results, published-bracket, and private-overlay read classes.
- [x] Draft the pilot and course route groups, including independently cached profile modules, public-safe course visibility, leaderboards, recent races, recognition, and private personal overlays.
- [x] Review and approve the pilot and course route groups in the route/API matrix.
- [x] Draft the provisional team route group, including compact discovery, public detail/roster, fact-backed T03 statistics, current-player action state, capability-based management, and typed membership mutations.
- [x] Review and approve the provisional team route group in the route/API matrix, including omission of administrator create-on-behalf unless T01/T02 deliberately preserves it.
- [x] Draft the grouped global-search utility boundary, including a lazy public catalog, four initial entity groups, directory query handoff, local matching, and explicit exclusion of sponsor administration/search from Website V2.
- [x] Review and approve the grouped global-search utility boundary in the route/API matrix.
- [x] Review and approve shared not-found/unavailable behavior, metadata, sitemap generation, legacy-route retirement, and the bounded team/gauntlet upload-intent contract.
- [x] Define visual-system and shared-component implementation slices before marketing, public data, authenticated, management, and administrator route slices.
- [ ] Define route-level acceptance criteria and verification evidence.
- [x] Define the cutover strategy, temporary rollback-compatibility boundary, and distinct legacy disposition: retire the marketing site after stabilization while retaining Ascentun only for the explicitly deferred Midnight/blockchain workflow.
- [ ] Produce the Vercel/DNS cutover runbook, stabilization duration, rollback ownership, retained Midnight-host boundary, and cleanup criteria during implementation planning.

## Review Checkpoint

Framework, marketing information architecture, replacement-release scope, product-statistics baseline, course visibility, navigation, non-functional requirements, delivery sequencing, the complete initial route/API matrix, and shared support contracts are approved. Sponsor administration/media is assigned to the Eventun Extend App as a pre-cutover dependency, with no Website V2 sponsor pages. External analytics/observability are deferred, legacy redirects are omitted at the current traffic level, and team presentation remains provisional until the preceding team feature work is implemented. Focused Pencil studies and the approved desktop/mobile homepage calibration have established a provisional clean race-control/HUD direction while rejecting faux scrap-metal component styling and repeated decorative cutouts. Design Language v0.1 now records the applied baseline. The next checkpoint is the gauntlet listing/calendar mock, followed by representative interior-page validation and design-language revision.

## Risks

- Rewriting two current React applications into another framework creates cost without automatically improving the product.
- Using the phrase "Ascentun parity" without an explicit exclusions list can accidentally reintroduce wallet, Accountun prize/reward, and retired token-gating behavior.
- Treating team analytics as a frontend-only task would misattribute historical performance to current rosters and produce incorrect team results.
- Requiring every analytics idea at launch could delay replacement indefinitely; the launch set must be limited to visualizations supported by bounded, production-cut-over Eventun reads.
- Treating Design Language v0.1 as final before data-heavy-page validation could lock in table, chart, filter, state, or geometry rules that have not yet been applied.
- Changing the root-route purpose without a migration and SEO decision can damage the current marketing funnel and historical links.
- Website V2 deliberately relies on the working Ascentun `steamopenid` exchange despite ambiguous managed-cloud documentation. If AccelByte removes or changes that behavior, authentication will require a replacement architecture; that compatibility risk is accepted rather than treated as a launch blocker.
