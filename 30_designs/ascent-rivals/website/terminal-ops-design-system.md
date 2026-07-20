# Ascent Rivals Terminal Ops Design System

Date: 2026-04-13
Last reviewed: 2026-07-18
Status: Draft

## Related
- [[unified-design]]
- [[design-language-v0.1]]
- [[information-architecture]]
- [[design-doc-roadmap]]
- [[tone-and-voice]]
- [[pages/homepage]]
- [[pages/player-directory]]
- [[pages/player-profile]]
- [[pages/gauntlets-index]]
- [[pages/gauntlet-detail]]
- [[pages/course-leaderboards]]
- [[pages/teams-index]]
- [[pages/team-profile]]
- [[pages/sponsors-index]]
- [[shell-concepts]]
- [[pencil-design-brief]]
- [[../../../20_references/ascent-rivals/website-concepts/terminal-concept|terminal-concept]]
- [[../../../50_knowledge/ascent-rivals/design-language|design-language]]

## Purpose

This note defines the working Terminal Ops design system direction for the unified Ascent Rivals website.

[[design-language-v0.1]] is the current applied visual baseline. This document retains the broader rationale, component inventory, and unresolved design-system requirements; where its earlier exploratory geometry conflicts with v0.1, the applied v0.1 rule takes precedence.

It should guide:

- Pencil follow-up prompts
- Next.js/React implementation planning
- accessible primitive and component styling
- page specifications
- responsive behavior

It is not a final pixel-perfect visual specification.

## Working Design Decision

Adopt Terminal Ops as the primary working design direction.

Direction refined: 2026-07-15

Terminal Ops should represent an in-world Ascent Rivals information terminal rather than a contemporary Linux terminal. It is the interface through which visitors inspect gauntlets, teams, pilots, planets, courses, ships, and other world or competition entities.

The terminal has two coordinated layers:

1. purpose-built race-control interface
   - matte graphite panels and flat tonal surfaces
   - crisp seams, selective edge cuts, restrained inset depth, and sparse signal lighting
   - a consistent fabricated-panel grammar rather than arbitrary card silhouettes
   - conventional readable information architecture beneath the in-world presentation
2. advanced information display
   - entity indexing and scanning
   - telemetry, maps, diagnostics, and system state
   - emissive status light and display behavior
   - an original, readable in-world command vocabulary rather than Linux shell syntax

Scrapyard material and physical wear remain optional atmospheric cues, not the foreground component system. Do not simulate metal through smooth gray gradients, rust colors, repair plates, scratches, or decorative rivets on ordinary UI panels. When grit is useful, prefer approved background art, gameplay imagery, restrained texture, or a small number of physical shell details.

The terminal metaphor is a product and worldbuilding decision, not a decorative layer to remove when pages become editorial or data-heavy.

## Working Narrative Premise

The terminal is an access point into an underground race-information network.

Working scene-setting premise for design exploration:

- an improvised gauntlet signal announces a short race window on a hazardous industrial or frontier planet
- crews, teams, and manufacturers discover the event through distributed race-network terminals
- orbital support ships may deploy remotely operated racer drones and equipment to the surface
- the network carries planet hazards, course data, team and pilot registries, vehicle diagnostics, qualification state, and race results
- viewers follow the same signal as the event forms and unfolds
- the race operates under pressure before an external corporate, security, or regulatory response can shut it down

This premise aligns with [[../../../50_knowledge/ascent-rivals/lore|lore]], but it is not a final lore contract. The exact authority, communications network, deployment sequence, role of manufacturers, spectator culture, and legality remain open.

Betting may inform the rough outlaw-sport atmosphere, but Website V2 must not present wagering as a committed product feature or invent betting mechanics, balances, odds, or transactions.

Design implication:

- the UI should feel like it is receiving a contested, time-sensitive race signal rather than browsing a clean institutional league database
- advanced scans, maps, telemetry, and registries sit inside a modern race-control surface whose surrounding atmosphere may carry industrial wear
- information can show source, freshness, signal quality, verification, and event-window state where real data supports those concepts
- avoid fake live state or fabricated urgency when the product has no authoritative source for it

Core decisions:

- global navigation uses a top-bar command/prompt-inspired shell
- marketing and player/competition contexts share the same shell family
- top-bar nav links may change by site context
- page-local navigation handles deep page sections
- permissioned actions appear in-page, near the relevant entity
- contextual side panels are allowed inside data-heavy pages but are not the global nav model

Terminal Ops remains a working direction until it is validated against:

- player profile
- course leaderboard
- gauntlet detail
- mobile shell state

## Voice Direction

The interface should sound like a shipboard computer, race-control terminal, or team telemetry desk.

It should be precise, operational, and lightly in-world.

It should not become vague sci-fi roleplay.

See [[tone-and-voice]] for detailed copy rules.

## Implementation Context

Approved baseline:

- Next.js
- React
- TypeScript
- custom Ascent Rivals components built over unstyled accessible primitives

Design implication:

- use well-supported accessible primitives for interaction behavior where they fit the approved component design
- style primitives into a custom Ascent Rivals shell
- avoid default starter-kit aesthetics
- avoid re-creating inaccessible custom primitives when a suitable unstyled primitive exists

## Core Visual Language

## Brand Anchors

Required brand colors:

| Token | Hex | Role |
|---|---|---|
| `brand-gold` | `#F2A900` | primary accent, active states, CTA highlights, warm metal |
| `brand-dark-blue` | `#11111F` | primary dark brand anchor |
| `text-primary` | `#E8E4D8` | primary text on dark surfaces |
| `text-secondary` | `#B9B3A6` | secondary text on dark surfaces |

## Terminal Ops Surface Tokens

Working token set from the Terminal Ops concept:

| Token | Hex | Usage |
|---|---|---|
| `terminal-bg` | `#0A0A12` | page background |
| `surface-deep` | `#080810` | nav bars and deep sections |
| `surface-panel` | `#0F0F1A` | panel/card bodies |
| `surface-raised` | `#161625` | panel headers and raised sections |
| `surface-border` | `#1E1E30` | dividers and low-emphasis strokes |
| `brand-gold` | `#F2A900` | primary accent |
| `gold-border` | `#F2A90055` | emphasized dividers |
| `gold-dim` | `#F2A90033` | subtle gold wash |
| `text-primary` | `#E8E4D8` | primary text |
| `text-secondary` | `#B9B3A6` | secondary text |
| `text-dim` | `#6A6A7A` | metadata and low-emphasis text |
| `accent-green` | `#4F9A68` | live, online, qualified, success |
| `accent-red` | `#C95644` | eliminated, error, destructive |
| `accent-lightblue` | `#63B8E8` | in-progress, racing, info |

## Palette Guardrails

- Gold is a command and brand-accent color, not a full-page fill.
- Dark blue and near-black surfaces should carry most of the page.
- Off-white text should replace pure white.
- Auxiliary colors should mostly appear in statuses, charts, ranks, badges, and alerts.
- Avoid purple-neon esports drift.
- Avoid black-and-gold luxury/crypto aesthetics.

## Display and Light Direction

The advanced display should feel integrated into a purpose-built race-control terminal.

- Use amber or gold as the dominant emissive display color.
- Reserve green, cyan, and red primarily for functional state, confirmation, information, warning, or failure.
- Present selected information through dark illuminated display surfaces without reducing text contrast.
- Allow localized bloom, scan acquisition, signal breakup, and brief interference as state or transition effects.
- Present current approved game imagery in full color where it represents received race footage, a scan, or an entity image.
- Let display light catch nearby panel edges or the surrounding scene where imagery supports that treatment.

Avoid constant CRT noise, persistent flicker, rainbow-neon color, and decorative typewriter animation.

## Grit and Material Direction

The foreground UI should remain clean enough to read as advanced equipment rather than faux-metal decoration.

Preferred material treatment:

- matte graphite and dark-blue panel surfaces
- flat tonal separation with crisp seams and restrained inset depth
- localized display illumination and atmospheric gradients
- sparse stenciled labels, telemetry marks, and physical-shell cues
- approved background art, gameplay captures, or low-contrast texture when a scene needs more grit

Avoid:

- smooth gray gradients presented as metal
- rust, heat staining, scratches, repair plates, or rivets distributed across ordinary components
- random gray and gold border fragments with no structural or state role
- texture that reduces text or data contrast

The scrapyard influence should be felt primarily through atmosphere, imagery, world context, and occasional shell details. It is not a requirement for every panel.

## Typography

## Roles

The current Terminal Ops concept uses:

- display/headlines: heavy display face
- nav, labels, data, status: monospace

Working direction:

| Role | Guidance |
|---|---|
| Display / hero headings | condensed or heavy display face; can reference Opinion Pro Condensed or the current concept's heavy headline treatment |
| Nav / commands / labels | monospace, uppercase or command-like where useful |
| Data / tables / telemetry | monospace for scan precision |
| Body / editorial | readable proportional face is allowed, especially for marketing and long-form copy |

## Typography Guardrails

- Do not use monospace everywhere by default.
- Keep long-form editorial readable.
- Use monospace where it reinforces command, data, status, or system tone.
- Make numerals, standings, and stat values feel deliberate.
- Set long-form body copy at a comfortable default size and line height, with an approximate 60–75 character measure where layout allows.
- Avoid the 9–12px low-contrast text used extensively in the original concepts; small technical labels are accents, not the primary reading layer.
- Restrict uppercase and wide tracking to short headings, commands, labels, and status text.

## Font Research Shortlist

Status: comparison candidates, not a final font decision.

### Recommended first comparison

- Display and section headings: [Saira Semi Condensed](https://fonts.google.com/specimen/Saira+Semi+Condensed), primarily semibold through extrabold.
- Body and general UI: [IBM Plex Sans](https://github.com/IBM/plex), primarily regular/text through semibold.
- Terminal commands, data, numerals, and telemetry: [IBM Plex Mono](https://github.com/IBM/plex), primarily regular through semibold.

Rationale:

- Saira was designed for headlines and short text and draws on industrial, engineering, automotive, and scientific forms.
- IBM Plex was designed for UI use and provides related Sans, Sans Condensed, and Mono families under the Open Font License.
- The combination puts the stronger futuristic-industrial character in short display text while keeping reading and data work in a restrained, legible family.

### Conservative single-superfamily comparison

- IBM Plex Sans Condensed for display and compact headings.
- IBM Plex Sans for body and general UI.
- IBM Plex Mono for commands, data, and telemetry.

This option is less distinctive but reduces visual mismatch and font-loading complexity.

### Accessibility stress-test

[Atkinson Hyperlegible Next](https://www.brailleinstitute.org/freefont/) and its monospace companion should be included in a body/data comparison. The family prioritizes character distinction, provides seven weights and variable versions, and supports a broad language set. It may be used as the final body family or as a benchmark the selected design must perform against.

### Existing Opinion Pro reference

Opinion Pro Condensed remains a strong display candidate because it connects the website to the current game-client typography and has a technical, wayfinding-oriented structure.

However, the local `.otf` file does not establish website embedding rights. [Opinion Pro licensing](https://www.myfonts.com/collections/opinion-pro-font-mint-type/) separates desktop and webfont use. Confirm that the project owns an appropriate webfont license before including it in Website V2; otherwise use an open-source display candidate.

The current marketing site's five-family mixture of Opinion Pro, Sansation, Square, Chakra Petch, and Thuner should not migrate as a system. Individual faces may remain visual references during comparison, but Website V2 should target one readable proportional family, one related mono, and at most one distinct display face.

Required specimen test:

- homepage hero and feature heading
- long-form About copy
- gauntlet table with names, times, ranks, and statuses
- terminal query and result list
- mobile navigation and compact labels
- ambiguous character strings such as `0/O`, `1/I/l`, player handles, timestamps, and identifiers

## Layout System

## Page Architecture

Default page structure:

```text
TopCommandNav
Optional StatusTelemetryBar
Main page body
Footer
```

Interior page structure:

```text
TopCommandNav
PathBar
PageHeader / HeroBriefing
LocalSectionNav or page-local anchors
Primary content grid
Optional contextual side panel
Footer
```

## Surface Hierarchy

Recommended hierarchy:

- `terminal-bg`: page
- `surface-deep`: nav/footer/deep bands
- `surface-panel`: content panels
- `surface-raised`: panel headers, selected/raised regions
- `surface-border`: default dividers
- `gold-border`: major context separators

## Background and Material Treatment

Default direction:

- use dark textural backgrounds rather than flat single-color canvases
- prefer subtle material noise, faint grid marks, restrained scan treatment, or atmospheric gradients
- keep texture low-contrast enough that tables and copy remain readable
- do not require a giant bespoke background illustration for every page

Marketing/editorial pages can use stronger texture and art layering than player utility pages.

Player, stats, gauntlet, and admin pages should use restrained texture so dense data remains scannable.

## Imagery and Generated Graphics Strategy

Website V2 must not depend on bespoke planet paintings, illustrated course maps, or a continuing custom-art pipeline. The team does not currently have dedicated artists, and much of the game's environment art is assembled from Fab marketplace assets.

Bespoke planet and course artwork remains a valid later enhancement. Initial components should provide optional media slots and strong non-image fallbacks so future art can be added without redesigning the route or blocking the functional site.

Priority order:

1. current approved gameplay captures and video
2. current approved renders or promotional compositions derived from the actual game
3. terminal-native graphics generated from real game or website data
4. restrained material, signal, grid, and atmospheric treatments when no canonical image exists

Planet presentation:

- do not assume unique planet key art exists
- use factual planet name, environment description, hazard or condition data, and course relationships
- use current in-game environment captures where a course provides an honest visual reference
- use restrained procedural scan fields, coordinate grids, orbital markers, or classification graphics as terminal presentation rather than pretending they are literal planet imagery

Course presentation:

- the game currently generates course-map geometry from checkpoints rather than relying on authored map illustrations
- treat a generated checkpoint trace as a strong candidate for the Website V2 terminal language
- render the trace as a route scan, navigation plot, or timing diagram rather than a decorative fantasy map
- do not require the graphic until checkpoint geometry is available to the website through an approved export or data contract
- fall back to a course still, identity panel, and factual metadata when route geometry is unavailable

Asset guardrails:

- use the actual game's assembled environments as the primary source of visual truth
- do not present generic generated concept art as a current planet, course, ship, or production asset
- treat Fab source assets as game-production inputs, not as a ready-made collection of standalone website illustrations
- do not redistribute or expose raw source assets through the website
- build the visual system so strong typography, materials, layout, and generated information graphics can carry pages with limited imagery
- reserve full-bleed imagery for moments where a strong current capture exists

## Shape and Border Language

Status: refined through the approved desktop and mobile homepage calibration frames on 2026-07-18. It must still be tested on a data-heavy interior page.

Approved motifs:

- cut-corner panels
- angled CTA edges
- paired forward chevrons and short directional terminations for interactive controls
- restrained bracket-like section frames
- thin technical border accents attached to a real edge or state
- inset image boxes
- compact `//` notation and ASCII-adjacent labels inherited from the clean HUD Overlay direction
- diamond nodes for Ascension progression and related ordered race-state diagrams
- Ascent icon/logo marks as section header identifiers
- physical chassis seams or access details when a major shell or media module justifies them
- advanced scan, targeting, map, diagnostic, and entity-index overlays

Rejected or restricted motifs:

- generic hexagons used as unexplained identity markers
- evenly dashed one-pixel borders around a rectangular safe-area panel
- detached gray or gold border fragments with no structural or state role
- circuit traces used as general decoration rather than a specific connector or relationship
- a different arbitrary polygon silhouette for every card

### Corner grammar

Treat corner cuts separately from mid-edge cutouts. Valid corner topologies are:

- zero cut corners
- one intentional cut corner
- two diagonally opposed cut corners
- all four cut corners

Do not use three cut corners or two adjacent cuts on the same side. The current directional-panel calibration uses top-right and bottom-left cuts as its default two-corner configuration. Other valid configurations remain available when a component role gives them a consistent reason.

### Mid-edge cutout grammar

The focused studies established how to balance mid-edge cutouts, but the complete homepage showed that repeated cutouts become gimmicky when several cards compose together. They are therefore restricted rather than graduated by component importance.

Allowed exceptions:

- one shallow top cut that behaves as a header or tab attachment
- one shallow left or right cut that expresses a relationship to adjacent open content
- a bespoke major media or hero frame with a clear structural reason

Do not use the earlier zero-through-four cutout study as a production complexity ladder. Default repeated cards to zero mid-edge cutouts and a consistent corner grammar. Ordinary tables, lists, metadata regions, and long-form copy may remain unframed or use calm rectangular surfaces.

### Signal rails and interaction geometry

A short neutral rail with a smaller gold termination is an optional state treatment, not required perimeter decoration. Default gold remains subdued; hover or focus may advance the termination approximately 4px once and return on blur; selected or active state may retain restrained gold at the endpoint. Do not use continuous motion.

Primary and secondary CTAs may use the approved paired-chevron and directional-termination motifs with the same short, one-time mechanical response. Critical control meaning must remain available without motion.

The current static exploded ship image is not an approved reusable motif. A future schematic treatment must use current approved models or data and provide meaningful diagnostic, modular, or interactive information.

## Framing Hierarchy

Treat each page as one terminal system rather than a stack of unrelated physical devices.

### Level 1: terminal chassis

The page shell establishes the persistent hardware context through:

- top and edge rails
- major seams or repaired joins
- restrained material transitions
- navigation, query, and system-state regions
- occasional exposed fasteners, vents, handles, or access details

This layer should be recognizable without placing a thick metal border around the entire viewport.

### Level 2: major hardware modules

Reserve the strongest physical construction for important modules such as:

- primary hero or incoming race signal
- terminal query and entity result surface
- current gauntlet briefing
- planet or course scan
- featured vehicle diagnostic
- major video or received-footage display

These modules may use layered armor, repaired seams, latches, clamps, deeper recesses, heavier cut corners, and visibly inset display glass.

### Level 3: information surfaces

Tables, lists, cards, long-form copy, and secondary metadata should use calmer construction:

- thin rails
- inset dark or smoked-glass surfaces
- restrained corner cuts
- compact section markers
- spacing and typography as the primary hierarchy

Do not render every row or content block as a separate ornate metal panel.

Context variation:

- marketing pages may expose more machinery, material depth, cinematic lighting, and large received imagery
- player and competition pages use the same terminal hardware more quietly so tables, rankings, and records remain readable
- mobile preserves the hierarchy but removes nonessential chassis detail rather than shrinking desktop ornament

Shape guardrails:

- derive asymmetry and corner cuts from plausible fabricated panel construction
- avoid generic hexagon grids, arbitrary cyberpunk angles, and decorative brackets with no structural role
- maintain consistent attachment, seam, recess, and corner logic across components

Use heavier decorative framing for:

- `/game` feature sections
- video modules
- screenshot/media groupings
- major homepage hero or brand modules

Use calmer framing for:

- standings
- leaderboards
- player stat modules
- match history
- team management
- authenticated and admin workflows

Implementation guidance:

- prefer CSS `clip-path` or masks for the filled panel surface and tokenized corner/cutout geometry
- use inline SVG for sparse perimeter rails, broad edge pieces, or geometry that CSS pseudo-elements cannot express cleanly
- keep text and interactive content as ordinary semantic HTML inside an invisible safe area; do not render a visible rectangular safe-area panel inside the silhouette
- image-based borders are acceptable for marketing accents, but should not become the default component border system
- decorative borders must not carry required semantic meaning
- avoid placing ornate tech borders around every card or the interface will become noisy

## Spacing

Use a 4px base grid.

Working spacing values:

- 6
- 8
- 10
- 12
- 16
- 20
- 24
- 32
- 40
- 48
- 60
- 80

## Top-Bar Navigation

## Terminal Interaction Model

Use a hybrid interaction model.

- All routes and actions remain available through conventional links, buttons, menus, and touch targets.
- A global query console provides universal entity search and a faster keyboard path.
- Optional readable commands may use an original in-world vocabulary such as `FIND PILOT`, `OPEN GAUNTLET`, `SCAN PLANET`, or `TRACK TEAM`.
- Typing a command is never required to complete a task.
- Breadcrumbs and location context should use readable network or registry hierarchy, such as `RACE NETWORK › GAUNTLETS › ORBITAL BLITZ`, rather than filesystem paths.
- Command results should map to the same accessible routes and grouped search results as conventional navigation.
- Mobile uses the same information model through touch-first controls; it should not simulate a miniature desktop command line.

Guardrails:

- do not require visitors to learn syntax
- do not use present-day shell error messages
- do not add fake typing delays
- do not hide ordinary navigation for the sake of the metaphor
- keep command language concise enough that it still works as clear interface copy

## Required Behavior

Top-bar global navigation is the working shell model.

The top bar must always include:

- brand/prompt identity
- search entry
- login/avatar area
- a `More` or menu trigger whenever any destination is hidden

The login/avatar area should never collapse out of the top bar.

It may become visually compact, but it should remain directly accessible at every viewport width.

## Desktop Top Bar

Desktop should show:

- brand/prompt
- `Gauntlets`, `Pilots`, `Teams`, `Courses`, and `Events` in that order when measured space permits
- search
- login/avatar

## Tablet Top Bar

As width decreases:

- keep brand/prompt visible
- keep search visible
- keep login/avatar visible
- move `Events`, then other destination links from the right side of the ordered list, into `More` before the bar wraps or compresses labels

## Mobile Top Bar

Mobile should use a compact top bar.

Required visible items:

- brand/prompt
- search
- menu
- login/avatar

The three compact action controls use equal 44px touch targets. Their default visual state is borderless: search and menu use muted icons, while login/account may use a restrained gold icon. A visible surface may appear for hover, focus, or pressed state but should not persist at rest.

The drawer contains the complete destination list in stable order, beginning with `Gauntlets`, followed by the secondary `About` and `Brand` destinations.

Mobile is not the primary player-side use case, but it must remain usable.

Marketing mobile should remain close to desktop feature parity because new visitors may arrive from social links or search.

## Responsive Collapse Model

Use measured available width rather than assuming that one device breakpoint guarantees enough space:

```text
wide
  Brand, Gauntlets, Pilots, Teams, Courses, Events, search, login/account.

compact
  Brand, highest-priority destinations that fit, More, search, login/account.
  Hidden destinations retain their stable order inside More.

mobile
  Compact prompt bar:
  [brand/prompt] [search] [menu] [login/avatar]
  Complete destination list is available in the drawer.
```

## Navigation Priority Rules

Brand, search, and login/account remain directly accessible independently of destination-collapse ordering. Show or collapse destination links in this priority order:

1. `Gauntlets`;
2. `Pilots`;
3. `Teams`;
4. `Courses`;
5. `Events`.

`About` and `Brand` remain in `More` and the footer rather than consuming primary-row width. The marketing hero owns the primary Steam conversion action; a top-bar conversion CTA is not required.

## Account Menu

The login/avatar area opens a dropdown menu.

Anonymous state uses a direct `Sign in with Steam` control. Do not use a one-option provider menu. Wide layouts use the full label; compact layouts use a generic login/account icon while preserving `Sign in with Steam` as the accessible name and tooltip. Do not create or approximate a Steam logo; use approved Valve artwork if Steam branding is displayed.

Approved initial items:

- My Career
- My Team, with one concise pending invitation/request status when relevant
- Admin / Operations, if authorized
- Sign Out

`My Career` links to the canonical authenticated pilot profile. `My Team` links to the current team or the personalized `/teams` state when the player has no team. `Admin / Operations` appears only when an approved Website or external operations destination exists; it does not imply a Website sponsor route. Keep team/gauntlet creation and entity editing on their relevant pages. Visually separate `Sign Out` from navigation entries. The menu should use accessible menu primitives and behavior, including an accessible pending-status label rather than a visual-only badge.

## Core Components

## TopCommandNav

Purpose:

- global shell navigation
- stable navigation across marketing and competition pages

Slots:

- brand/prompt
- primary nav links
- search entry
- login/avatar slot
- more/menu slot

States:

- default
- active route
- compact
- mobile menu open
- authenticated
- unauthenticated

## MobileCommandNav

Purpose:

- compact mobile shell

Required visible controls:

- brand/prompt
- search
- menu
- login/avatar

Menu contents:

- complete primary destination list in stable order
- secondary `About` and `Brand` links
- any authenticated account destinations that are not already available through the account control

## SearchCommand

Purpose:

- search-everywhere interaction

Behavior:

- reachable from top bar
- groups results by entity type
- supports keyboard interaction

Initial groups:

- Gauntlets
- Players
- Teams
- Courses

Sponsors do not enter Website global search. Sponsor discovery and administration belong to the Eventun Extend App; gauntlet authoring uses a separate form-scoped selector when needed.

Future groups:

- Planets
- Ship parts
- Manufacturers
- News/media

## PathBar

Purpose:

- interior breadcrumb/path context

Examples:

- `$ cd /gauntlets/orbital-blitz`
- `$ open /players/pilot-id`
- `$ list /courses`

Guardrail:

- path labels must still be understandable to non-technical users
- do not make path text the only accessible navigation label

## StatusTelemetryBar

Purpose:

- compact operational context strip

Potential uses:

- active season
- pilots online
- next gauntlet
- live event
- user's qualification status
- system/news highlight

Responsive behavior:

- desktop: pipe-separated inline strip
- tablet: wrap or reduce item count
- mobile: horizontal scroll or compact stacked summary

## BracketPanel

Purpose:

- framed content block for data and entity modules

Use for:

- standings
- leaderboards
- profile modules
- sponsor modules
- system log
- gauntlet sections

Guardrail:

- production framing should prefer CSS borders/shapes over meaningful box-drawing characters
- decorative glyphs can be used if not required for comprehension

## DataTable

Purpose:

- standings, leaderboards, results, history

Required states:

- default
- loading
- empty
- error
- current user highlighted
- selected row

Responsive behavior:

- desktop: table
- tablet: table with reduced columns or horizontal scroll
- mobile: horizontal scroll or stacked ranking cards depending on density

## EntityCard

Purpose:

- compact links to public players, teams, gauntlets, and courses, plus sponsors only inside administrator surfaces

Variants:

- player
- team
- gauntlet
- sponsor
- course

## SystemLog

Purpose:

- event/activity feed

Potential uses:

- homepage activity
- recent records
- gauntlet updates
- system/news highlights

Guardrail:

- should not become the only way to read important announcements

## HeroBriefing

Purpose:

- marketing or entity hero with Terminal Ops framing

Variants:

- homepage marketing hero
- logged-in utility hero
- gauntlet briefing
- game page hero

## LocalSectionNav

Purpose:

- page-local section navigation

Use for:

- player profile sections
- team profile sections
- gauntlet detail sections
- course leaderboard filters

Possible forms:

- readable section anchors for long entity pages and forms;
- accessible tabs for mutually exclusive content panels;
- segmented controls for a small set of module-level filters;
- a compact labeled jump menu when the anchor list does not fit on mobile.

Selection rules:

- default to anchors when the content remains part of one scrollable document;
- do not use tabs merely as a visual treatment for ordinary page headings;
- preserve selected tab or filter state in the URL when it changes a shareable data view;
- use conventional visible labels and accessible names; command-style text may be secondary decoration but never the only navigation language;
- omit structurally unavailable destinations, especially optional gauntlet qualifiers, stages, brackets, standings, or sponsor sections;
- on mobile, prefer a jump menu or disclosure over an overflowing tab strip that requires an undisclosed horizontal gesture;
- account for the persistent global bar when making local navigation sticky, and avoid consuming excessive vertical space with two stacked sticky bars.

The exact visual form can vary by page, but it should remain visibly connected to Terminal Ops through material, active-state, and focus treatments.

## PermissionActionBar

Purpose:

- actions available due to role/ownership

Examples:

- Create Gauntlet
- Edit Gauntlet
- Manage Team
- Create Sponsor

Guardrail:

- permissioned actions should be near the relevant object
- they should not become permanent global nav clutter

## PlayerStrengthModule

Purpose:

- show what a player is good at, not only their rank

Examples:

- best course by finish time
- best course by lap time
- notable course leaderboard placement

V1 guardrails:

- do not use total kills, total play time, total races, or similar volume counters as strength modules
- do not use deaths, crashes, or other negative stats as joke-framed strengths
- do not claim combat style, consistency, survival, improvement, ship-part, or loadout strengths unless supporting data exists
- do not invent medals or badges; official medals and badges are AccelByte-owned

## Motion and Interaction

## Motion Principle

Default to accessible interaction behavior from the chosen primitives where possible.

Terminal-inspired animation should be used selectively.

Good uses:

- command/search opening
- entity or signal acquisition on first open
- status telemetry updates
- section transitions
- lightweight text-entry effect for very short labels
- one-time course-trace drawing when a course is selected
- brief highlight or pulse when data actually changes

Avoid:

- typing long paragraphs
- delaying critical content
- constant blinking or distracting terminal effects
- animations that make data tables harder to scan
- replaying acquisition effects on every minor interaction
- using interference to decorate healthy, stable content

## Suggested Motion Language

Allowed motifs:

- quick scanline or wipe reveal for panels
- subtle terminal cursor on search/command input
- short type-on effect for concise status or query labels
- hard-cut or stepped transitions rather than soft SaaS easing
- short mechanical shifts for menus, latches, and panel controls
- a one-time approximately 4px advance and return for paired chevrons, directional terminations, or signal-rail endpoints on hover/focus
- localized signal breakup for genuine loading, stale, disconnected, or error state

Guardrail:

- motion should reinforce responsiveness and system mood
- motion should not become a novelty layer
- critical text and controls should be available without waiting for an animation
- reduced-motion mode should replace drawing, scanning, stepping, and interference with immediate state changes or simple fades

## Component States

Every interactive component should define:

- default
- hover
- focus-visible
- active/current
- disabled
- loading
- error
- empty

Data-specific components should also define:

- current user row
- qualified state
- eliminated state
- live state
- completed state
- upcoming state

## Data-Dense Rules

## Leaderboards and Standings

Rules:

- preserve rank, entity name, and primary metric at all widths
- secondary metrics can collapse or move behind expansion affordances
- current user should be visually findable
- sorting/filtering must stay clear

Potential filters:

- course
- mode/ruleset
- region
- season
- team/solo context
- rating/stat type

## Player Profiles

Rules:

- do not make the profile only a leaderboard/rank page
- include optional strength modules only when they can be derived cleanly from best lap or best finish data
- do not show a generic global rank tier, rank history, or exact MMR until a separate Eventun public-division design is approved
- keep match history deeper in the page or behind a section
- expose course stats clearly

## Gauntlet Pages

Rules:

- qualifiers and heats must not be conflated
- qualifier sections show tournament qualification windows/standings
- heat breakdowns belong to match details/history
- logged-in personal status should be visible but not dominate the public page

## Accessibility Guardrails

- Use semantic HTML for nav, main, sections, tables, and headings.
- Use accessible primitives where appropriate.
- Do not rely on box-drawing characters as the only semantic frame.
- CSS framing should carry critical visual structure.
- Top nav and menus must be keyboard accessible.
- SearchCommand must support keyboard operation and screen reader labeling.
- Login/avatar menu must remain visible at all breakpoints.
- Color contrast should meet WCAG AA for core text and controls.
- Motion should respect reduced-motion preferences.

## SEO and Public Page Guardrails

Public pages should use the appropriate Next.js server-rendering or static-rendering path for their freshness and personalization requirements.

Priority SEO surfaces:

- homepage
- game page
- gauntlet detail
- player profile
- team profile
- course pages
- historical event pages

Each public entity page should support:

- meaningful title
- meta description
- Open Graph image where available
- canonical URL
- share-friendly preview

## Open Questions

- Does Saira Semi Condensed with IBM Plex Sans and Mono pass data-table, form, and ambiguous-identifier testing?
- How much atmospheric grit can interior pages carry without weakening the clean race-control surface?
- Which calm panel and table variants remain coherent in dense data layouts and at mobile sizes?
- Should terminal type-on motion be used at all outside search/path labels?

## Next Steps

1. Use [[design-language-v0.1]] to create the gauntlet listing and calendar calibration.
2. Extend the applied language through gauntlet detail, player profile, and course detail/leaderboard mocks.
3. Add dense-data, filter, table, chart, form, and state rules only after those compositions are reviewed.
4. Validate team pages after the team model is stable enough.
5. Promote the applied language to v0.2 when the representative interior archetypes are coherent at desktop and mobile widths.
