# Ascent Rivals Website Design Language v0.1

Date: 2026-07-18
Status: Provisional applied baseline
Last reviewed: 2026-07-19

## Related

- [[unified-design]]
- [[terminal-ops-design-system]]
- [[information-architecture]]
- [[tone-and-voice]]
- [[pages/homepage]]
- [[../../../50_knowledge/ascent-rivals/design-language|game-client design language]]

## Purpose

This document is the first applied visual-language baseline for Website V2. It translates the approved homepage desktop and mobile calibration frames into rules that can guide Pencil mocks and the Next.js/React implementation.

Source calibration frames:

- `Ascent V2 — Homepage Composition Calibration`
- `Ascent V2 — Homepage Mobile Calibration`
- `Homepage Composition — Interaction Notes`

This version is intentionally provisional. It has been validated on one marketing composition at desktop and mobile widths, but not yet on data tables, filters, charts, forms, or dense entity pages.

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

### Working semantic tokens

| Token | Value | Role |
|---|---:|---|
| `canvas` | `#090A0F` | primary page field |
| `surface-deep` | `#07090D` | footer and deepest recesses |
| `surface-nav` | `#080B10` | navigation and shell bands |
| `surface-section` | `#0B0E14` | broad section bands |
| `surface-panel` | `#111318` | calm panel surface |
| `surface-raised` | `#161A21` | destination cards and raised information |
| `surface-display` | `#101721` | media, scan, and received-signal display |
| `rule` | `#303641` | seams, dividers, and low-emphasis structure |
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

These are the v0.1 implementation candidates. Opinion Pro Condensed remains a brand reference but requires confirmed webfont licensing before use.

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

## Spacing and Sizing

Use a 4px base grid.

Working values:

- micro: `4`, `6`, `8`, `10`, `12`;
- component: `16`, `20`, `24`, `32`;
- section: `40`, `48`, `60`, `64`, `80`.

Applied baselines:

- desktop section gutter: `64–80px`;
- mobile page gutter: `20px`;
- common panel inset: `24px`;
- desktop navigation height: `80px`;
- mobile navigation height: `72px`;
- primary and secondary CTA height: `56px`;
- minimum compact touch target: `44 × 44px`.

Internal spacing should be balanced visually. Body or action text must not crowd the lower edge of a panel.

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
- direct `Sign in with Steam` action while Steam is the only provider.

Mobile:

- `72px` high with `20px` side padding;
- actual logo lockup remains the visual anchor;
- search, menu, and login/account use equal `44 × 44px` targets;
- default icons are borderless and have no persistent boxed background;
- search and menu are muted; login/account may use a restrained gold icon;
- hover, focus, and pressed surfaces appear only as interaction states;
- the login control has the accessible name `Sign in with Steam` and becomes the avatar/account control after authentication.

### Media and scan viewport

- use approved gameplay captures or video when available;
- use the course-scan fallback only when clearly identified;
- one or two diagonal corner cuts are sufficient;
- keep overlays sparse enough that imagery remains legible.

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
- convert horizontal progression to one vertical rail;
- use one-column destination cards with consistent shapes and gaps;
- keep mobile body text at approximately `16–17px`;
- maintain 44px touch targets without requiring visible borders.

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

Version 0.1 confirms the marketing shell and responsive visual thesis. It does not yet finalize:

- leaderboard and table density;
- filters, sorting, pagination, and search-result presentation;
- charts and career-summary visualization;
- gauntlet schedule, stage, qualifier, and bracket composition;
- player and team identity modules;
- forms and permissioned workflows;
- loading, empty, error, stale, and partial-data visuals;
- final font loading and licensing decisions;
- final dark-token consolidation for implementation.

Revise this language through representative page mocks in this order:

1. gauntlet listing and calendar;
2. gauntlet detail;
3. player profile;
4. course detail and leaderboard;
5. team pages after the team model is stable enough.

Promote the document to v0.2 only after the interior mocks establish reusable rules for dense data, controls, charts, and responsive entity layouts.
