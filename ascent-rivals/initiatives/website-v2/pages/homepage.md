# Ascent Rivals Homepage Page Spec

Date: 2026-04-14
Status: Approved content hierarchy; copy, assets, and visual design open
Last reviewed: 2026-07-19

## Related

- [[../unified-design]]
- [[../information-architecture]]
- [[../terminal-ops-design-system]]
- [[ascent-rivals/initiatives/website-v2/design-language-v0.2]]
- [[../tone-and-voice]]
- [[gauntlets-index]]
- [[gauntlet-detail]]
- [[player-directory]]
- [[player-profile]]
- [[course-leaderboards]]
- [[teams-index]]
- [[ascent-rivals/system/eventun/interface-architecture|eventun-interface-architecture]]
- [[ascent-rivals/system/accelbyte-platform|AccelByte platform]]

## Purpose

Define the content hierarchy, behavior, and acceptance requirements for the Website V2 root route.

The homepage is a marketing and conversion page first. It should explain Ascent Rivals, demonstrate the game through real footage and factual systems, establish the revised Terminal Ops sci-fi atmosphere, and give visitors clear next actions.

The page may include one restrained module drawn from current competition or recent editorial event content. That module supports the marketing story; it does not turn the homepage into a dashboard.

## Approved Decisions

- Keep `/` as the primary marketing and conversion homepage.
- Use `Play Now` as the default primary conversion action.
- Keep the same section order, module placement, responsive composition, and primary layout for anonymous and authenticated visitors.
- Authentication may change copy, actions, and player-specific data inside an existing slot, but it must not insert, remove, reorder, or resize homepage sections merely because the visitor signed in.
- If a signed-in player's ownership is reliably confirmed, replace the repetitive primary conversion emphasis with a more useful `Explore Gauntlets` action and retain a smaller Steam play/launch action where appropriate.
- Do not treat sign-in alone as proof of ownership and do not claim to know whether the game is installed.
- Allow one compact, optional `From the Race Network` module after the core gameplay and ship explanation.
- Prefer a current or upcoming public gauntlet for that module; fall back to a recent verified competition or code-authored event recap; omit the module when no strong content exists.
- Keep global entity search in the shared top bar rather than recreating a large homepage search console.
- Do not add homepage status telemetry, a generated system log, multiple leaderboard panels, or a sequence of data widgets.
- Build the content hierarchy so the page remains complete when all dynamic competition content is unavailable or intentionally omitted.

## Route

- Canonical route: `/`
- Current source reference: the `ascent-website` root page
- Primary competition destination: `/gauntlets`
- Editorial event destination: `/events`

The current marketing implementation is a content, media, and conversion reference only. Website V2 should rebuild the layout and components from scratch.

## Audience

Primary:

- new visitors discovering the game;
- prospective players deciding whether to play;
- press, creators, partners, and community members seeking a concise product overview.

Secondary:

- returning players looking for current competition;
- followers seeking recent races, tournaments, teams, pilots, or records;
- signed-in players re-entering the Website experience.

## Page Goals

- communicate the core game proposition quickly;
- give `Play Now` a clear and trustworthy destination;
- explain the combination of high-speed racing, combat, and Ascension Mode;
- demonstrate ships and customization with current approved game media;
- introduce the industrial-planet and outlaw-race atmosphere without presenting exploratory lore as settled canon;
- show that organized competition exists when credible content is available;
- route interested visitors to gauntlets, events, courses, community channels, and deeper public pages;
- remain readable, responsive, and persuasive without custom planet paintings or illustrated course maps.

## Non-Goals

- a logged-in player dashboard;
- a real-time race-control display;
- a comprehensive gauntlet directory;
- player, team, or course leaderboards;
- an activity feed generated to create false motion;
- a news CMS or editorial publishing system;
- wallet, token, prize, reward, or betting functionality;
- detailed lore claims that have not been approved elsewhere.

## Approved Content Hierarchy

The initial homepage uses the following seven-part hierarchy. Sections may overlap visually in a final design, but the narrative order should remain recognizable.

1. Hero and primary conversion
2. Gameplay and Ascension Mode
3. Ships and customization
4. Optional race-network proof
5. Worlds, planets, and courses
6. Events and community
7. Final conversion and next actions

## 1. Hero and Primary Conversion

### Purpose

- identify Ascent Rivals immediately;
- communicate high-speed sci-fi racing and combat;
- provide the primary conversion action without requiring the visitor to understand gauntlets or the competition system first.

### Required Content

- Ascent Rivals logo or wordmark;
- one concise headline;
- one short explanatory statement;
- current approved gameplay footage, cinematic capture, or a strong non-image fallback;
- primary CTA;
- one secondary action when it improves the decision rather than competing with it.

### Default CTA State

For anonymous visitors, signed-in users without a reliable ownership result, and confirmed non-owners:

- primary: `Play Now`;
- destination: the current approved Steam store, access, or install destination;
- optional secondary: `Explore Gauntlets`.

If the product's actual Steam availability requires different wording at implementation time, replace `Play Now` with an accurate conversion label such as `Wishlist on Steam` or `Request Access`. Do not use conversion copy that contradicts the current release state.

### Confirmed-Owner CTA State

When all of the following are true:

- the visitor is authenticated;
- the account is linked to the relevant Steam identity;
- ownership of the intended Ascent Rivals Steam application is confirmed through an approved server-side source;

then the hero may use:

- primary: `Explore Gauntlets`;
- secondary: `Play on Steam` or another accurate Steam action.

Ownership personalization changes the actions, not the hero narrative or overall page structure. If ownership lookup fails, times out, is unavailable in Shared Cloud, or cannot distinguish the relevant application, render the default state without an error panel.

The personalized actions must occupy the same CTA region and follow the same responsive rules as the default actions. Do not create an owner-specific hero layout.

The implementation must not claim that the game is installed or that a browser action can launch it unless the final Steam integration actually supports that behavior.

### Design Guidance

- use the revised race-control Terminal Ops visual language without making the hero resemble a modern Linux terminal;
- let industrial grit come primarily from approved game imagery, atmosphere, and world context rather than distressed foreground components;
- prioritize readable copy and gameplay proof over decorative diagnostic text;
- avoid a long boot sequence, typing effect, or delayed CTA;
- preserve immediate CTA access on mobile.

### Provisional Implementation Background Direction

The approved image-neutral mock validates composition and hierarchy without committing to a final background asset. During implementation, test one large atmospheric background behind the open homepage composition. Leading candidates are:

- an oversized Ascent Rivals logo treatment similar in role to the MSI tournament page composition;
- an approved environmental capture from the current game, similar in role to the current marketing homepage background.

Whichever treatment is selected must be dimmed or covered by a deliberate scrim so headings, body copy, navigation, and CTAs retain verified contrast. Use responsive art direction and crop review rather than relying on one desktop image at every breakpoint. The neutral graphite/atmospheric field remains the fallback when no approved asset works. Do not add background art to the current calibration mock solely to settle this implementation choice.

## 2. Gameplay and Ascension Mode

### Purpose

- explain what the player does;
- distinguish Ascent Rivals from a conventional racing game;
- foreground the mode that represents almost all current racing activity.

### Required Ideas

- high-speed circuit racing;
- combat and survival pressure during the race;
- podium placement as the first competitive objective;
- the post-podium Ascension challenge, where remaining racers attempt to reach the designated zone without being destroyed.

Classic and Deathmatch race modes may be acknowledged later where relevant, but they should not dilute the homepage's initial Ascension Mode explanation.

### Presentation

- use one concise narrative sequence rather than a dense rules document;
- pair the explanation with current gameplay footage or stills;
- make the transition from race to Ascension visually understandable;
- do not expose client/server authority details, event-validation behavior, or other anti-cheat-sensitive implementation information.

## 3. Ships and Customization

### Purpose

- show the player's vehicle fantasy;
- demonstrate meaningful visual and loadout variation;
- retain one of the strongest content categories from the current marketing site.

### Content

- current approved ship models or gameplay captures;
- concise customization or loadout explanation;
- factual manufacturer, class, performance, or equipment context only where supported by current game content;
- optional terminal-native comparison or diagnostic graphics derived from real ship data.

### Guardrails

- do not reuse the current static exploded-ship image as a primary Website V2 feature;
- do not expose Fab source assets or present marketplace assets as bespoke website art;
- do not invent manufacturer lore merely to fill the module;
- avoid implying that loadout value alone determines competitive strength.

## 4. Optional Race-Network Proof

### Purpose

- show that Ascent Rivals has a real competitive ecosystem;
- give returning or already-convinced visitors a direct path to current activity;
- add timely proof without making the page depend on a constant event schedule.

### Placement and Scale

Place this module after the game and ship proposition. It should be one bounded feature area, not a dashboard section followed by additional gauntlet, leaderboard, pilot, and telemetry panels.

Recommended maximum:

- one featured item;
- up to two compact supporting links when the design remains clean at desktop and mobile widths;
- one clear route to either `/gauntlets` or `/events` based on the featured content.

### Selection Priority

Select the strongest available item in this order:

1. an active public gauntlet with a reliable active state and useful current context;
2. an upcoming public gauntlet with a meaningful schedule or entry state;
3. a recently completed public gauntlet with verified final context or results;
4. a recent code-authored `/events` tournament, showcase, LAN, or recap;
5. no module.

The fallback is not an empty gauntlet card or fabricated network status. The marketing page must close the gap cleanly when the section is absent.

### Terminology

Use a broad section label such as `From the Race Network` only if the final tone review approves it.

Within the module, label the content type explicitly:

- `Gauntlet` for Eventun-backed competition;
- `Event Recap`, `Tournament`, `Showcase`, or another accurate editorial label for code-authored `/events` content.

Do not call an editorial event a live gauntlet, and do not label a scheduled gauntlet `Live` based solely on its planned start and end timestamps.

### Dynamic Gauntlet Content

Allowed fields include:

- title and verified media;
- current public state;
- next relevant time;
- qualifier, stage, final, or bracket context only when that structure exists;
- concise participation context for a signed-in player when supported;
- approved sponsor branding provided in the public gauntlet context;
- link to `/gauntlets/[id]` and the broader `/gauntlets` route.

Gauntlets may omit qualifiers or stages. The teaser must use the same state- and composition-aware rules as the gauntlet-detail page rather than rendering empty phases.

### Editorial Fallback

A recent tournament or event recap may be used when it tells a stronger story than current gauntlet data. Editorial content remains code-authored and must link to `/events/[slug]`.

Use verified copy, media, dates, and outcomes. A sponsored event may contain manually approved promotional content, but the homepage must not recreate deferred data-driven prize or reward functionality.

### Failure and Empty Behavior

- omit the module if the query fails and no approved editorial fallback is available;
- do not show a large error panel on the marketing homepage;
- do not block rendering of any other section;
- do not reserve a visually obvious empty space;
- log the operational error through the Website observability path once that baseline is defined.

## 5. Worlds, Planets, and Courses

### Purpose

- give the races a sense of place;
- introduce industrial planets, improvised competition, and scrapyard construction as atmosphere;
- lead interested visitors toward the public course experience.

### Initial Content Strategy

The team does not currently have a dedicated planet-art or course-map pipeline. Initial presentation should therefore prioritize:

1. current gameplay captures and video;
2. factual environment and course descriptions;
3. terminal-native procedural graphics generated from approved data;
4. checkpoint-derived course traces if a Website data contract becomes available;
5. strong material and typographic composition when no suitable image exists.

Planet paintings and bespoke course illustrations are later enhancements, not launch dependencies.

### Lore Boundary

The interface may imply a distributed underground race-information network and improvised races on industrial worlds. Orbital arrival, manufacturers, authorities, spectators, and betting remain exploratory context until separately approved as canon. Do not state invented political, economic, or wagering facts as established lore.

## 6. Events and Community

### Purpose

- demonstrate real-world participation and community activity;
- preserve useful event, video, partner, and social content from the current marketing site;
- give visitors ways to follow the project beyond the game client.

### Content

- selected recent or historically important `/events` entries;
- useful videos associated with those events;
- a link to the broader YouTube archive where appropriate;
- verified community and social destinations;
- optional code-authored partner recognition;
- approved awards, press, showcase, or event proof only after accuracy review.

If Section 4 already uses a code-authored event as its fallback, avoid repeating the same event in this section. Section 6 may then emphasize community channels, video, or a different historical proof point.

### Sponsor and Partner Boundary

- `Sponsor` refers to an Eventun-backed gauntlet relationship and appears only in its approved gauntlet context;
- `Partner` refers to a broader manually verified marketing relationship;
- the homepage must not expose Eventun Extend App sponsor operations, operational tier, or sponsor-management controls.

## 7. Final Conversion and Next Actions

### Purpose

- close the marketing narrative;
- repeat the primary action after the visitor has seen the product proof;
- offer a concise choice for visitors who are interested but not ready to play.

### Actions

Default:

- `Play Now`;
- `Explore Gauntlets`;
- one appropriate community or follow action.

Confirmed owner:

- `Explore Gauntlets`;
- optional `View My Career` or `View My Team` when the session supplies a valid destination;
- a smaller accurate Steam play/launch action.

Do not turn the final CTA into a grid of every site destination.

## Logged-In Personalization

Personalization is additive and compact.

Allowed initial behavior:

- ownership-aware hero and final CTA changes when ownership is reliably confirmed;
- participation context inside the selected gauntlet teaser;
- direct `My Career` or `My Team` re-entry through the approved account menu;
- one concise invitation, join-request, or relevant competition status where an existing module naturally supports it.

Do not:

- replace the marketing homepage with a private dashboard;
- insert, remove, reorder, or resize sections based only on authentication state;
- move team or gauntlet management controls into the page;
- infer ownership from login alone;
- infer game installation;
- create a personalized empty state when public content would work.

## Data and Content Ownership

### Repository-Authored Content

Use code-authored typed content for:

- hero and feature copy;
- gameplay, ship, world, and course explanations;
- editorial events and recaps;
- verified partners, community links, and videos;
- CTA labels and destinations that depend on release state.

No CMS is required for the initial release.

### Eventun Content

Use public Website-oriented Eventun reads for a selected gauntlet and authenticated overlays. The homepage should not assemble its teaser by issuing many client-side entity requests.

A purpose-built projection may be added if it materially improves:

- public visibility filtering;
- composition-aware current state;
- featured-item selection;
- bounded media and sponsor context;
- signed-in participation overlay;
- cache behavior.

### AccelByte Content

AccelByte Cloud Save `Courses` remains the course metadata source of truth. Only the approved server-side `published` projection may reach ordinary homepage presentation. Hidden, alpha, internal, malformed, or otherwise unreleased course configurations must not be exposed.

Any ownership check used for CTA personalization must be verified as available and supported in the Ascent Rivals Shared Cloud deployment. Keep publisher credentials or Web API keys server-side and fail back to the anonymous conversion state.

## Loading, Failure, and Content-Absence Rules

- render repository-authored marketing content without waiting for optional live data;
- do not delay the hero CTA on authentication or ownership checks;
- allow ownership-aware CTA enhancement after the base hero is available without causing disruptive layout movement;
- keep a compact stable skeleton only where the optional race-network module is expected to render;
- omit optional content cleanly after a bounded failure or empty response;
- do not use fake terminal noise as a loading state;
- one failed optional integration must never blank the homepage.

## Responsive Requirements

Desktop:

- support cinematic depth and wider media while retaining a clear reading order;
- keep the optional race-network module bounded rather than expanding into a dashboard grid;
- prevent CTA, metadata, or supporting links from consuming excessive horizontal space.

Tablet:

- stack narrative and media regions without reversing their semantic order;
- reduce decorative chassis and material layers before reducing content readability.

Mobile:

- keep the hero proposition and primary CTA visible without a long ornamental preamble;
- use one-column section flow;
- make the race-network feature work as one card with supporting links below it;
- retain global login/account and navigation access;
- avoid horizontal data tables and dense status strips.

## Accessibility Requirements

- use a proportional, readable body font and reserve display or monospace faces for short labels;
- maintain semantic heading order matching the narrative hierarchy;
- provide captions or equivalent context for essential video information;
- provide useful poster images and non-video fallbacks;
- ensure every CTA has an explicit accessible name and destination;
- do not communicate gauntlet state, ownership, or availability through color alone;
- respect reduced-motion preferences and never gate content behind animation;
- keep text legible over gameplay media and textured industrial surfaces.

## SEO and Sharing

Required:

- canonical `/` URL;
- accurate page title and description centered on the game proposition;
- crawlable text explaining racing, combat, and Ascension Mode;
- approved Open Graph image and social description;
- crawlable links to `/gauntlets`, `/events`, `/courses`, and other relevant public destinations;
- structured data only where it truthfully matches the product and visible content.

Do not make frequently changing gauntlet content the only meaningful text in the page title, description, or social preview.

## Acceptance Criteria

- the first view identifies Ascent Rivals, communicates the game proposition, and exposes an accurate primary conversion action;
- the default primary CTA is `Play Now` while the game is currently available through that action;
- signed-in state alone never changes the CTA as though ownership were known;
- confirmed ownership may change the primary CTA to `Explore Gauntlets` without creating a separate homepage;
- anonymous, authenticated, and confirmed-owner states preserve the same section order and responsive layout;
- ownership lookup failure falls back silently to the default state;
- the page explains racing, combat, podium placement, and the Ascension challenge accurately;
- current approved gameplay and ship media are used instead of the obsolete exploded-ship treatment;
- the page works without custom planet art or illustrated course maps;
- at most one bounded race-network proof module appears;
- current/upcoming gauntlet data is preferred only when it is meaningful and reliably classified;
- recent verified competition or `/events` content may replace gauntlet data without being mislabeled;
- the optional module disappears cleanly when no strong content is available;
- no fake live state, viewer state, system activity, wagering, or authority pressure is presented;
- global search remains available through the shared shell without dominating the homepage;
- all core narrative and conversion content remains usable when Eventun, AccelByte, or authentication personalization is unavailable;
- mobile preserves the narrative order, CTA access, readable content, and global account control.

## Deferred Enhancements

- bespoke planet and course art;
- richer checkpoint-derived course visualization after a data contract exists;
- live race or broadcast modules after a canonical stream and live-state contract exists;
- deeper personalized recommendations;
- presence, current player count, viewer count, or real-time activity feeds;
- a `/game` route when distinct deeper content justifies it;
- CMS-backed news or editorial authoring.

## Open Implementation Questions

- Which supported server-side source, if any, can reliably confirm Steam ownership in the Shared Cloud architecture?
- What is the accurate Steam conversion label and destination at Website V2 launch?
- Should the selected race-network item be chosen through explicit code-authored curation, an Eventun feature marker, or a deterministic state/recency rule?
- What bounded Website API projection best supplies the optional gauntlet teaser and signed-in overlay?
- Which current gameplay captures, videos, ship images, event media, partner approvals, and community links survive the migration audit?

## Review Checkpoint

The marketing-first purpose, seven-part narrative hierarchy, default `Play Now` conversion, confirmed-owner CTA variation, and bounded optional race-network module are approved. Exact copy, media, ownership source, content-selection mechanism, API projection, responsive composition, and revised visual mock remain implementation-planning or design-production work.
