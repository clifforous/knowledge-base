# Ascent Rivals Website Design Language v0.2

Date: 2026-07-21
Status: Approved implementation baseline
Last reviewed: 2026-07-21

## Related

- [[unified-design]]
- [[terminal-ops-design-system]]
- [[information-architecture]]
- [[tone-and-voice]]
- [[ascent-rivals/initiatives/website-v2/pages/homepage]]
- [[ascent-rivals/system/design-language|game-client design language]]
- [[ascent-rivals/decisions/README#ar-2026-011--website-v2-uses-a-purpose-built-race-control-language|race-control visual direction decision]]

## Purpose

This document consolidates the accepted Website V2 desktop/mobile calibrations and reviewed v0.2
reference board into a reusable visual, interaction, and responsive implementation contract. It
supersedes Design Language v0.1 without claiming that the website is implemented, verified, or
deployed.

Source calibration frames:

- `Ascent V2 — Homepage Composition Calibration`
- `Ascent V2 — Homepage Mobile Calibration`
- `Homepage Composition — Interaction Notes`
- `Ascent V2 — Gauntlets Index Calibration`
- `Ascent V2 — Gauntlets Schedule Calibration`
- `Ascent V2 — Gauntlets Index Mobile Calibration`
- `Ascent V2 — Gauntlets Schedule Mobile Calibration`
- `Ascent V2 — Gauntlet Detail Active Calibration`
- `Ascent V2 — Gauntlet Detail Sparse Upcoming Calibration`
- `Ascent V2 — Gauntlet Detail Active Mobile Calibration`
- `Ascent V2 — Pilot Profile Career Calibration`
- reviewed mobile companion to the pilot-profile career calibration
- `Ascent V2 — Pilot Directory Calibration`
- `Ascent V2 — Pilot Directory Mobile Calibration`
- `Ascent V2 — Course Detail Leaderboard Calibration`
- `Ascent V2 — Course Directory Calibration`
- `Ascent V2 — Course Detail Leaderboard Mobile Calibration`
- `Ascent V2 — Course Directory Mobile Calibration`
- `Ascent V2 — Course Category Faceted Selection Study`
- `Ascent V2 — Global Search Command Calibration`
- `Ascent V2 — Global Search Command Mobile Calibration`
- `Ascent V2 — Global Search Command State Study`
- `Ascent V2 — Shared Page States Calibration`
- `Ascent V2 — Shared Page States Mobile Calibration`

This baseline has been validated on marketing, gauntlet
discovery/detail, pilot-profile and directory, and course directory/detail compositions at desktop
and mobile widths. The reviewed frames cover local search where a directory needs it, URL-backed
view/scope controls, self-explanatory faceted category paths, entity cards and rows, a
repeated-occurrence agenda, conditional detail sections, ordered stage circuits, desktop qualifier
standings, mobile rank-list translation, bounded charts, client-side progressive reveal, and a
dense responsive course leaderboard, plus the shared global-search command with representative
loading, no-match, partial-availability, and keyboard-focus states. The shared page-state frames
also cover route loading, valid empty collections, essential-route unavailability, non-revealing
not-found handling, local optional-module failure, and safe stale refresh. Forms and team surfaces
remain unvalidated.

## Design Thesis

Website V2 is a purpose-built interface into the Ascent Rivals race network.

It should feel like a futuristic race-control terminal used to inspect gauntlets, pilots, teams, courses, vehicles, and race signals. It is not a present-day Linux terminal, a generic esports dashboard, or a collection of faux-metal sci-fi cards.

The working character is:

- cinematic but readable;
- operational rather than ornamental;
- matte graphite with selective signal illumination;
- asymmetric only where geometry communicates direction, hierarchy, or attachment;
- gritty through imagery and atmosphere rather than distressed component chrome;
- conventional and accessible beneath the in-world presentation.

## Core Principles

### One interface field

Treat the page as one continuous race-control display. Use open composition, broad tonal sections, spacing, and thin structural rules before introducing another card.

Do not make every paragraph, statistic, destination, or action a separate device.

### Geometry must have a role

Use cuts and directional marks to express:

- forward motion;
- selection or action;
- progression;
- a media or module boundary;
- a relationship between adjacent regions.

Do not vary silhouettes only to make repeated content look more futuristic.

### Readability carries the interface

Use a proportional body face for reading. Reserve condensed display and monospace treatments for roles that benefit from them. Technical notation is a supporting voice, not the primary information layer.

### Grit belongs to the world

Use approved gameplay imagery, atmospheric backgrounds, restrained texture, and occasional major-shell details to imply an industrial frontier environment.

Do not distribute rust, scratches, rivets, repair plates, or simulated metal gradients across ordinary UI components.

### State must be factual

Do not invent live signals, viewer counts, shutdown pressure, telemetry, or urgency. Display state, freshness, qualification, and timing only when an authoritative source supports them.

## Color System

### Canonical semantic tokens

| Token | Value | Role |
|---|---:|---|
| `canvas` | `#090A0F` | primary page field |
| `surface-deep` | `#07090D` | footer and deepest recesses |
| `surface-nav` | `#080B10E8` | navigation and translucent shell bands |
| `surface-section` | `#0B0E14` | broad section bands |
| `surface-panel` | `#111318` | calm panel surface |
| `surface-raised` | `#181B22` | destination cards and raised information |
| `surface-selected` | `#18232E` | selected control field |
| `surface-display` | `#101721` | media, scan, and received-signal display |
| `rule` | `#303641` | seams, dividers, and low-emphasis structure |
| `rule-strong` | `#46505C` | faceted-shell outlines and emphasized boundaries |
| `brand-dark` | `#11111F` | canonical dark-blue brand anchor |
| `brand-gold` | `#F2A900` | primary action, selection, and brand signal |
| `brand-gold-dim` | `#F2A90055` | quiet emphasized rule or secondary control |
| `text-primary` | `#E8E4D8` | primary text |
| `text-secondary` | `#B9B3A6` | body and secondary text |
| `text-dim` | `#6A6A7A` | nonessential metadata |
| `signal-info` | `#63B8E8` | course scans and informational state |
| `signal-success` | `#4F9A68` | confirmed success or qualified state |
| `signal-danger` | `#C95644` | destructive, eliminated, or error state |

Alpha variants are allowed for atmospheric illumination, subdued rules, and state backgrounds. They should not lower text contrast.

These tokens are extracted from the reviewed frames. The Pencil file also retains exploratory
variables such as `metal-*`, `metal-rust`, `terminal-green`, `terminal-bg`, and older
`surface-*` values. They are not part of v0.2 and must not be exported into the application merely
because they still exist in the workfile. The reviewed v0.2 reference board identifies them as
legacy rather than presenting them as usable palette choices. They may be removed after Cliff
preserves any useful history.

### Color rules

- Gold is scarce. Use it for primary action, active state, key progression, and small index marks.
- Off-white replaces pure white.
- Cyan supports scans and information; it is not a second brand accent.
- Green and red remain state colors.
- Broad surfaces remain near-black, graphite, or dark blue.
- Avoid purple-neon esports palettes and black-and-gold luxury or crypto styling.
- Gradients are for atmosphere, readability scrims, and display illumination—not simulated metal.

## Typography

### Working families

| Role | Family | Use |
|---|---|---|
| Display | Saira Semi Condensed | hero and section headings |
| Reading and general UI | IBM Plex Sans | body copy, navigation, descriptions, and ordinary labels |
| Operational | IBM Plex Mono | commands, actions, short eyebrow labels, data, and technical notation |

These are the v0.2 implementation families. Opinion Pro Condensed remains a brand reference but
is not an implementation dependency.

### Working type range

- desktop hero: approximately `74px`, tightly led;
- mobile hero: approximately `52px`, tightly led;
- section headings: approximately `34–44px`;
- card headings: approximately `25–32px`;
- prominent body copy: approximately `17–19px`;
- ordinary body and data descriptions: approximately `15–16px`;
- actions and operational labels: approximately `11–14px`;
- nonessential metadata: `10px` minimum in normal use.

Nine-pixel labels in the calibration are not a general production target. Do not place required information at that size.

### Typography rules

- Keep long-form copy in IBM Plex Sans with a comfortable line height and measure.
- Use uppercase and wider tracking only for short labels, actions, status, and display headings.
- Do not use monospace for paragraphs.
- Test names, timestamps, ranks, and identifiers for `0/O`, `1/I/l`, and truncation ambiguity.
- Preserve heading hierarchy without relying on gold alone.

### Numeric notation

- Do not add leading zeros to ordinary user-facing values merely to make them look technical.
- Use natural forms for ranks, placements, counts, stage and qualifier numbers, collection status, and progressive-reveal actions: `#4`, `3rd`, `Stage 2`, `Qualifier 2`, `6 of 24 shown`, and `Show 6 more`.
- A zero-padded structural display index such as `01 / Overview` is allowed when it identifies a fixed editorial sequence. Treat it as optional notation and reduce or omit repeated indices on mobile.
- Preserve required padding inside conventional formatted values such as `01:39.840`, calendar dates, and canonical codes or identifiers where a leading zero is meaningful.
- Never change an authoritative identifier's formatting to satisfy the display convention.

## Spacing and Sizing

Use a 4px base grid.

Working values:

- micro: `4`, `6`, `8`, `10`, `12`;
- component: `16`, `20`, `24`, `32`;
- section: `40`, `48`, `60`, `64`, `80`.

Applied baselines:

- desktop calibration viewport: `1440px` with a `64px` outer gutter and `1312px` content field;
- mobile calibration viewport: `390px` with a `20px` outer gutter and `350px` content field;
- common panel inset: `24px`;
- desktop navigation height: `80px`;
- mobile navigation height: `72px`;
- desktop footer height: `200px`;
- mobile footer height: `212px`;
- primary and secondary CTA height: `56px`;
- minimum compact touch target: `44 × 44px`.

Internal spacing should be balanced visually. Body or action text must not crowd the lower edge of a panel.

The `1440px` and `390px` values are calibration widths, not fixed application breakpoints. The
implementation should preserve the gutter and content relationships fluidly, introduce an
intermediate layout where the desktop shell no longer fits, and avoid a sudden desktop-to-mobile
collapse tied only to those two example widths.

## Composition and Surface Hierarchy

### Open cinematic field

Use for:

- homepage hero;
- major gameplay capture;
- received race signal;
- future major course, vehicle, or event visualization.

Characteristics:

- full-width or full-bleed atmospheric field;
- left-weighted readable copy when appropriate;
- optional approved imagery or factual scan fallback;
- sparse rules, labels, and acquisition marks;
- no visible card enclosing the primary copy by default.

### Broad section band

Use a subtle tonal shift and one or two structural rules to establish a new section. A large background field may carry several related modules so that cards float within one system rather than becoming isolated boxes.

### Information surface

Use a panel only when content needs a shared boundary, selection surface, media viewport, or grouped interaction. Tables, prose, metadata, and repeated rows may remain open or use a calm rectangular surface.

### Major framed module

Reserve stronger geometry for one important module within a region, such as a featured gauntlet, gameplay viewport, course scan, or primary briefing. Repetition weakens the motif.

## Shape Grammar

### Angle and scale

Use a consistent 45-degree angle system. Working cut scales are approximately:

- `10px` for compact controls;
- `20px` for ordinary modules;
- `32px` for major media or featured surfaces.

Exact values may be adjusted after data-heavy page validation, but a component must use a named token rather than an arbitrary cut size.

### Corner cuts

Approved corner topologies:

- zero cuts;
- one intentional cut;
- two diagonally opposed cuts;
- four cuts for rare, large, self-contained displays.

The default repeated-card treatment is zero cuts or a consistent pair of diagonally opposed cuts. Do not alternate shapes solely for visual variety.

Avoid:

- three cut corners;
- two adjacent cuts on one side;
- a different corner pattern for every sibling;
- generic hexagons as identity markers.

### Mid-edge cutouts

Mid-edge cutouts are not part of the default card system. The homepage composition showed that repeated cutouts become gimmicky and make grouped cards visually restless.

Allowed exceptions:

- one shallow top cut that clearly behaves like a header or tab attachment;
- one shallow left or right cut that expresses a relationship to adjacent open content;
- a bespoke major media or hero frame where the cut has an explicit structural role.

Do not apply the earlier zero-through-four cutout study as a production complexity ladder. Do not use multiple cutouts on repeated destination cards without a new composition-level review.

### Border and rail rules

- Prefer one continuous structural edge or rule over detached fragments.
- Border accents must attach to a real edge, state, or relationship.
- Use subdued `rule` strokes by default and gold only for emphasis.
- Do not place decorative gray and gold fragments around every panel.
- Circuit-trace forms are allowed only when they communicate a connector, path, or data relationship.

## Signature Motifs

### Compact `//` notation

Use `//` as a concise race-network prefix for eyebrows, section labels, scan identifiers, and operational annotations.

Do not expand it into fake source code, filesystem paths, or decorative noise on every line.

### Paired forward chevrons

Use on the primary CTA and selected high-value progression actions. They communicate acceleration and forward intent.

### Directional termination

Use one short angled endpoint on secondary CTAs or an occasional state rail. It should read as an endpoint or action cue, not a random circuit trace.

### Diamond progression nodes

Use diamonds for ordered Ascension or race-state diagrams:

- outlined diamond: ordinary step;
- gold filled diamond: current or emphasized step;
- straight rail: relationship and sequence.

Desktop may use a horizontal progression; mobile converts the same structure into a vertical rail. Do not replace diamonds with generic hexagonal badges.

### Course-scan trace

Use a cyan checkpoint trajectory as the preferred factual non-image fallback when approved checkpoint data exists. In conceptual mocks it must be labeled as a temporary fallback rather than gameplay.

## Components

### Canonical component inventory

| Component family | Canonical role | Responsive rule |
|---|---|---|
| Global shell | Brand, primary destinations, search, and account access | Keep the desktop destinations while they fit; use borderless Search, Menu, and account controls on mobile |
| Global footer | Brand and stable secondary destinations | Use the `200px` desktop footer and `212px` mobile two-row footer |
| Primary and secondary action | High-value forward action and lower-emphasis companion action | Stack at full content width when horizontal actions no longer fit |
| Standard segmented control | A small mutually exclusive page view such as Gauntlets/Schedule | Preserve one connected `44px` shell; keep its state in the URL where it changes the view |
| Faceted radio group | A compact, closely related category path such as Race/Time Trial and Finish Time/Best Lap | Use one shared opposing-cut shell per group; stack full-width groups on mobile |
| Directory item | Scan-and-compare identity or event summary | Preserve the leading identity and primary status; move secondary data below or omit it |
| Data table / rank list | Exact competitive comparison | Use semantic tables on wide layouts and an open ranked list on mobile rather than horizontal scrolling |
| Global search command | Shallow public entity discovery | Use a modal dialog on desktop and a full-width sheet within the mobile shell |
| Rate and chart module | At-a-glance comparison or bounded history | Preserve labels, values, and accessible summaries when reducing chart detail |
| Shared page-state surface | Route, collection, entity, module, or freshness state | Preserve the global shell; keep optional failures local to their module |
| Media or scan viewport | Approved gameplay, event imagery, or factual fallback | Change crop and overlay density by width; do not change the represented fact |

The implementation should compose these families rather than create page-specific copies with
slightly different measurements. Page components may add content structure without redefining the
global shell, footer, action, selector, focus, or state language.

### Primary CTA

- gold filled surface;
- dark label;
- paired forward chevrons;
- `56px` high in the homepage calibration;
- full-width on narrow mobile layouts when needed.

### Secondary CTA

- transparent or deep surface;
- subdued gold outline;
- light label;
- one directional termination;
- equal height to the primary CTA.

### Standard segmented control

- use one rectangular connected shell with shared seams;
- each option retains a minimum `44px` interaction height;
- selected state uses a quiet tonal field and a `2px` amber index;
- hover, focus, and selected state remain visually distinct;
- do not use the faceted selector merely to make an ordinary two-view switch look more technical;
- when the control changes the page view, make the URL the state source.

### Faceted radio group

- use a single shell with top-right and bottom-left cuts around the whole group;
- keep internal options rectangular and separated by ordinary seams;
- use `56px` desktop and `52px` mobile group heights in the reviewed category path;
- selected state uses `surface-selected`, stronger label weight, and one `3px` amber rail inset
  approximately `11px` from the group edge;
- keyboard focus uses a separate `2px` cyan, shape-aware inset outline over the full interaction
  target; it may coexist with selection on another option;
- expose the group legend to assistive technology without adding vague visible labels such as
  `Context` or `Measure`;
- keep shareable category state in the URL.

### Destination card group

- one shared silhouette grammar for siblings;
- consistent internal padding and content baseline;
- one featured destination may be wider or stronger than the others;
- do not change corners or cutouts card by card;
- preserve an even visual rhythm when stacked on mobile.

### Navigation shell

Desktop:

- actual Ascent Rivals logo and wordmark;
- visible primary destinations when space permits;
- search and account actions remain directly available;
- direct `Sign in` action that starts the only implemented provider flow without opening a provider picker.

Mobile:

- `72px` high with `20px` side padding;
- actual logo lockup remains the visual anchor;
- search, menu, and login/account use equal `44 × 44px` targets;
- default icons are borderless and have no persistent boxed background;
- search and menu are muted; login/account may use a restrained gold icon;
- hover, focus, and pressed surfaces appear only as interaction states;
- the login control has the accessible name `Sign in` and becomes the avatar/account control after authentication.

### Media and scan viewport

- use approved gameplay captures or video when available;
- use the course-scan fallback only when clearly identified;
- one or two diagonal corner cuts are sufficient;
- keep overlays sparse enough that imagery remains legible.

### Global search command

- open from the stable global shell without navigating to an intermediate search page;
- group shallow results by public entity type and link directly to canonical entity routes;
- preserve deterministic keyboard focus and distinguish focus from activation;
- report no matches separately from dependency failure;
- allow one unavailable group while valid groups remain usable;
- do not imply analytics-based relevance, popularity, or command latency unless implemented.

### Shared page-state surfaces

- route loading preserves the global shell and reserves the expected content structure;
- a valid empty collection states that the request succeeded and offers a safe next action;
- essential-route failure offers Retry first and a safe route second without exposing provider or
  infrastructure detail;
- not-found and not-public use one non-revealing entity response;
- optional-module failure preserves valid surrounding content and retries only that module;
- stale refresh keeps the last safe content visible, labels it neutrally, and uses a polite status
  announcement without inventing a timestamp;
- loading, empty, unavailable, not-found, and stale are different states and must not share one
  generic error component with interchangeable copy.

## Motion

Motion should confirm interaction or factual state change.

Approved baseline:

- primary chevrons advance approximately `4px` once on hover or focus, then settle;
- the secondary termination uses the same brief directional response;
- course traces may draw once when acquired or selected;
- menus and panels may use short mechanical shifts or stepped reveals;
- actual data changes may receive one brief highlight.

Avoid:

- continuous CTA or rail animation;
- persistent flicker or CRT noise;
- long typewriter sequences;
- repeated boot or acquisition effects;
- decorative interference on healthy content;
- delaying content for atmosphere.

Reduced motion must replace drawing, scanning, and mechanical movement with an immediate state change or simple fade.

### Implementation calibration

The reference board defines stable component states and transition intent; it is not an animation
storyboard. The first implementation may choose reasonable short transitions for button feedback,
expand/collapse, segmented-view changes, faceted selection, menus, dialogs, and sheets, then review
them in the browser with representative content.

Initial motion choices remain provisional. They must:

- make interaction feel responsive rather than delay content;
- preserve a clear distinction among hover, focus-visible, selected, expanded, and activated;
- avoid moving surrounding layout merely to animate a state marker;
- use one coherent timing and easing family instead of page-specific effects;
- disable nonessential movement and remove animated height travel under reduced motion.

## Imagery and Atmosphere

Priority order:

1. approved gameplay capture or video;
2. approved render or promotional composition derived from the current game;
3. terminal-native visualization generated from real data;
4. restrained atmospheric field or clearly labeled temporary fallback.

Rules:

- do not present stock or generated concept art as gameplay;
- do not expose raw Fab assets;
- use gradients for background atmosphere, display illumination, vignette, and readability scrims;
- use scan lines sparingly;
- allow a strong page-level background to carry a section, but preserve contrast behind text and controls;
- do not make bespoke planet paintings or course illustrations a launch dependency.

### Provisional implementation background direction

The image-neutral calibration frames establish layout and information hierarchy; they do not require production pages to remain visually empty.

- The homepage may use one large approved environmental game capture or an oversized Ascent Rivals logo composition behind the open page field.
- Gauntlet directory items may use their uploaded `Background` media as a dimmed row underlay when representative asset testing confirms the treatment.
- Apply a deliberate scrim, vignette, gradient, or opaque information surface so content contrast does not depend on the source image.
- Preserve the same dimensions, hierarchy, and terminal-native fallback when imagery is missing or unsuitable.
- Review crops and focal points independently at desktop, tablet, and mobile widths.
- Use responsive image delivery and avoid loading unnecessary full-resolution backgrounds below the fold.
- Keep dense schedule rows, tables, and similar scan-and-compare surfaces image-light.

These are implementation-art candidates, not instructions to add placeholder imagery to every design mock.

## Responsive Reduction

Mobile is a deliberate recomposition, not a scaled desktop terminal.

Preserve:

- brand identity;
- content hierarchy;
- primary actions;
- factual media or fallback;
- Ascension explanation;
- all core destinations.

Reduce or remove:

- repeated section indices;
- nonessential metadata;
- excess scan lines and telemetry labels;
- ornamental rails;
- multi-column relationships that do not survive stacking.

Applied patterns:

- stack primary and secondary CTAs;
- convert long or narrative progression, such as the Ascension sequence, to one vertical rail;
- allow a short bounded sequence, such as a four-node qualifier rail, to remain horizontal when it fits without scrolling or compressed labels;
- use one-column destination cards with consistent shapes and gaps;
- keep mobile body text at approximately `16–17px`;
- maintain 44px touch targets without requiring visible borders.

### Canonical responsive transformations

| Desktop pattern | Narrow/mobile transformation |
|---|---|
| Full destination navigation | Stable brand lockup plus Search, Menu, and account controls |
| Side-by-side actions | Full-width vertical action stack |
| Horizontal Ascension progression | Straight vertical diamond rail |
| Multi-column destination or identity collection | One-column cards or open rows with reduced metadata |
| Wide standings or leaderboard table | Open ranked list preserving rank, identity, and primary value |
| Adjacent faceted category groups | Full-width stacked groups separated by `16px` |
| Search modal | Mobile sheet under the stable `72px` shell |
| Dense chart annotations | Reduced visual detail with unchanged value labels and accessible summary |
| Page-local anchor row | Compact labeled section-jump control |
| Multi-column footer links | Two centered link rows beneath left-aligned branding |

Responsive reduction changes composition, not product meaning. Route, selected filters, primary
facts, status, and action semantics must remain equivalent across widths.

### Operational detail composition

- Let one current qualifier, stage, or bracket surface carry the operational focus instead of nesting several equally strong cards.
- Treat personal status as a removable inset or adjacent layer; its absence must not leave a structural hole.
- Omit qualifier, stage, standings, sponsor, and navigation destinations when their factual content does not exist.
- Use a compact labeled section-jump control on mobile rather than squeezing desktop anchors into the header.

### Stage circuits

- Present each stage as one coherent panel with its state, identity, entry summary, and ordered match circuit.
- Show circuit matches as open rows within the stage surface rather than a grid of nested cards.
- Let mobile stage panels stack and grow to their content; do not equalize heights across different circuit lengths.
- When a stage has an authored title, pair a small stage number with the prominent title. When it does not, promote the stage number and remove the empty title region.

### Standings translation

- Use a scan-friendly table or open row system on desktop.
- Translate standings to an open ranked list on mobile instead of preserving a wide table through horizontal scrolling.
- Preserve rank, pilot identity, the leading competitive value, and signed-in-player emphasis before secondary columns.
- Keep pagination and local view controls visually distinct from page navigation; initial collection controls remain client-side.

### Branded media fallback

- Use a quiet, logo-derived signal field when approved gameplay or event media is absent.
- Label a fallback as a display or capture fallback where ambiguity is possible.
- Do not fabricate course maps, planet art, race telemetry, or live media.

## Accessibility and Implementation

- Build the visual system from semantic HTML and accessible interaction primitives.
- Use CSS custom properties for semantic tokens.
- Use CSS `clip-path` or masks for simple filled corner-cut surfaces.
- Use inline SVG for chevrons, diamonds, checkpoint traces, and sparse perimeter geometry.
- Do not rasterize ordinary panel chrome or text.
- Keep content inside a geometry-safe inset without drawing a second rectangular safe-area border.
- Ensure clipped components retain an unclipped, visible focus indicator through an appropriate wrapper or focus treatment.
- Do not encode meaning through color, motion, or decorative geometry alone.
- Meet WCAG AA contrast for core text and controls.
- Keep the design usable with motion disabled and terminal notation removed from screen-reader labels where it adds no meaning.

### Artifact and handoff boundary

- The external Pencil workfile is reviewed design evidence, not generated application source.
- The Markdown contract controls when exploratory variables, hidden notes, and superseded study
  frames disagree with a canonical visible frame.
- Ignore the immutable, nonvisual desktop pilot-profile root metadata value `RACE FINISH`; visible
  copy, control metadata, accessibility labels, and this contract use `RACE / FINISH TIME`.
- Ignore the superseded labeled course-category study in favor of the faceted-selection study.
- Do not export every Pencil variable into CSS. Export only the canonical token set shown on the
  reviewed v0.2 reference board.
- Preserve one reviewed `.pen` snapshot only at an explicit checkpoint; the Windows workfile
  remains the live artifact during iteration.

## Rejected Patterns

- faux scrap-metal panels;
- smooth gray gradients used as metal;
- rust, heat staining, repair plates, scratches, and rivets on ordinary cards;
- generic Linux shell imitation;
- all-monospace content;
- arbitrary hexagons;
- random border fragments;
- decorative circuit traces;
- a unique polygon for every card;
- repeated mid-edge cutouts across card grids;
- boxed default-state mobile header icons;
- constant CRT noise, flicker, or typewriter effects;
- fake live-state and telemetry claims;
- generic purple-neon esports treatment;
- black-and-gold luxury or crypto styling.

## Validation Boundary

Version 0.2 consolidates the marketing shell, responsive visual thesis, gauntlet directory and
Schedule composition, active and sparse gauntlet-detail behavior, the public pilot-profile
desktop/mobile composition, the course directory/detail compositions, and the global-search
command at desktop/mobile widths. It validates
ordered stage circuits, conditional section omission, desktop qualifier standings, a mobile
rank-list translation, client-side progressive reveal, bounded career-rate comparisons,
responsive pilot course-record summaries, recent-race visualization, a three-entry gauntlet
history, one exact course leaderboard with a top-five gap view, grouped shallow search results,
local search-command recovery states, and representative route-, collection-, entity-, module-,
and stale-data states. The 2026-07-21 alignment pass also confirms common desktop/mobile shell and
footer measurements, generic sign-in language, search identity, natural user-facing numbers, and
the accepted faceted and segmented controls across the current canonical frames. It does not yet
finalize:

- broader leaderboard and very dense table behavior beyond the reviewed course board;
- complex filters, sorting, and pagination beyond the reviewed collection controls;
- broader chart behavior beyond the reviewed career-rate and recent-race examples;
- gauntlet bracket graphs, stage-run detail, and completed-result composition;
- team identity modules and authorized management states;
- forms and permissioned workflows;
- final font loading and licensing decisions;
- final dark-token consolidation for implementation.

The bounded Pencil reference board has been reviewed across canonical tokens, typography,
geometry, shells, footers, actions, selectors, rows, shared states, focus treatment, and responsive
transformations. It establishes static states and intent rather than final transition timing.
Team, form, and in-browser motion validation may revise this baseline later.
