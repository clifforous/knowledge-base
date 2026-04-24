# Ascent Rivals Terminal Ops Design System

Date: 2026-04-13
Status: Draft

## Related
- [[unified-design]]
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

It should guide:

- Pencil follow-up prompts
- Nuxt implementation planning
- Reka UI component styling
- page specifications
- responsive behavior

It is not a final pixel-perfect visual specification.

## Working Design Decision

Adopt Terminal Ops as the primary working design direction.

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

Likely stack:

- Nuxt
- Reka UI

Design implication:

- use Reka UI for accessible primitives and interaction behavior
- style primitives into a custom Ascent Rivals shell
- avoid default starter-kit aesthetics
- avoid re-creating inaccessible custom primitives when Reka UI provides a good base

## Core Visual Language

## Brand Anchors

Required brand colors:

| Token | Hex | Role |
|---|---|---|
| `brand-gold` | `#F2A900` | primary accent, active states, CTA highlights, reward metal |
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

- Gold is a command/accent/reward color, not a full-page fill.
- Dark blue and near-black surfaces should carry most of the page.
- Off-white text should replace pure white.
- Auxiliary colors should mostly appear in statuses, charts, ranks, badges, and alerts.
- Avoid purple-neon esports drift.
- Avoid black-and-gold luxury/crypto aesthetics.

## Grit and Material Direction

Terminal Ops should not become a clean terminal dashboard.

Add grit through:

- armored or plated panel surfaces
- subtle scratches, abrasion, grime, or heat-stained overlays
- industrial framing lines
- restrained image overlays
- telemetry marks
- stenciled labels
- welded/bolted/modular construction cues

Guardrail:

- the UI must remain readable and premium
- grime should be subtle and systematic, not random decoration

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
- prefer subtle material noise, faint grid marks, scuffed metal, scanline texture, or atmospheric gradients
- keep texture low-contrast enough that tables and copy remain readable
- do not require a giant bespoke background illustration for every page

Marketing/editorial pages can use stronger texture and art layering than player utility pages.

Player, stats, gauntlet, and admin pages should use restrained texture so dense data remains scannable.

## Shape and Border Language

Approved motifs:

- cut-corner panels
- angled CTA edges
- bracket-like section frames
- thin technical border accents
- inset image boxes
- small marker glyphs near section headings
- Ascent icon/logo marks as section header identifiers

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
- wallet and admin workflows

Implementation guidance:

- prefer CSS borders, masks, clip-paths, pseudo-elements, and tokenized corner treatments
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

## Required Behavior

Top-bar global navigation is the working shell model.

The top bar must always include:

- brand/prompt identity
- marketing/player-side bridge link
- search entry
- login/avatar area

The login/avatar area should never collapse out of the top bar.

It may become visually compact, but it should remain directly accessible at every viewport width.

## Desktop Top Bar

Desktop should show:

- brand/prompt
- context-appropriate primary links
- cross-site bridge link
- search
- wishlist/play CTA where relevant
- login/avatar

## Tablet Top Bar

As width decreases:

- keep brand/prompt visible
- keep cross-site bridge visible if space allows
- keep search visible
- keep login/avatar visible
- move lower-priority links into `More`

## Mobile Top Bar

Mobile should use a compact top bar.

Required visible items:

- brand/prompt
- search
- menu
- login/avatar

If space allows, the cross-site bridge may remain visible.

If it does not fit, the bridge must be the first item inside the opened menu.

Mobile is not the primary player-side use case, but it must remain usable.

Marketing mobile should remain close to desktop feature parity because new visitors may arrive from social links or search.

## Responsive Collapse Model

Working model:

```text
>= 1200px
  Full top bar.

900-1199px
  Brand/prompt, bridge, primary context links, search, login/avatar.
  Secondary links move into More.

640-899px
  Brand/prompt, bridge if possible, search, login/avatar, More/Menu.
  Most nav links move into More/Menu.

< 640px
  Compact prompt bar:
  [brand/prompt] [search] [menu] [login/avatar]
  Bridge link is first item in menu if not visible.
```

## Navigation Priority Rules

Marketing context priority:

1. brand/prompt
2. player/competition bridge
3. wishlist/play CTA
4. Game
5. Media or Features
6. Events
7. Search
8. login/avatar
9. More

Competition context priority:

1. brand/prompt
2. marketing/game bridge
3. Gauntlets
4. Players
5. Teams
6. Courses
7. Search
8. login/avatar
9. More

Login/avatar remains visible independently of priority ordering.

## Account Menu

The login/avatar area can open a dropdown menu.

Likely items:

- My Career
- Wallets
- My Team or Team Requests
- Admin / Operations, if authorized
- Log out

The menu should use Reka UI menu primitives or equivalent accessible behavior.

## Core Components

## TopCommandNav

Purpose:

- global shell navigation
- context switch between marketing and competition/player site modes

Slots:

- brand/prompt
- primary nav links
- bridge link
- search entry
- CTA slot
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

- cross-site bridge first if not visible in bar
- context links
- secondary links
- CTA

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
- Sponsors
- Courses

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

- compact links to players, teams, gauntlets, sponsors, courses

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

- tabs
- anchor links
- command-like section links
- segmented controls

The exact form can vary by page, but it should remain visibly connected to Terminal Ops.

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

Default to Reka UI's accessible interaction behavior where possible.

Terminal-inspired animation should be used selectively.

Good uses:

- command/search opening
- path bar reveal
- status telemetry updates
- section transitions
- lightweight text-entry effect for very short labels

Avoid:

- typing long paragraphs
- delaying critical content
- constant blinking or distracting terminal effects
- animations that make data tables harder to scan

## Suggested Motion Language

Allowed motifs:

- quick scanline or wipe reveal for panels
- subtle terminal cursor on search/command input
- short type-on effect for path labels or status labels
- hard-cut or stepped transitions rather than soft SaaS easing

Guardrail:

- motion should reinforce responsiveness and system mood
- motion should not become a novelty layer

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
- show public rank tier but not exact private ELO
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
- Use Reka UI accessible primitives where appropriate.
- Do not rely on box-drawing characters as the only semantic frame.
- CSS framing should carry critical visual structure.
- Top nav and menus must be keyboard accessible.
- SearchCommand must support keyboard operation and screen reader labeling.
- Login/avatar menu must remain visible at all breakpoints.
- Color contrast should meet WCAG AA for core text and controls.
- Motion should respect reduced-motion preferences.

## SEO and Public Page Guardrails

Public pages should be SSR-friendly in Nuxt.

Priority SEO surfaces:

- homepage
- game page
- gauntlet detail
- player profile
- team profile
- sponsor pages
- course pages
- historical event pages

Each public entity page should support:

- meaningful title
- meta description
- Open Graph image where available
- canonical URL
- share-friendly preview

## Open Questions

- Which actual fonts should replace the concept placeholders?
- Should the bridge link use `Game`, `Marketing`, `Competition`, `Pilot Portal`, or another label?
- Should local page nav use tabs or command-like section links by default?
- How gritty should production surfaces become before readability suffers?
- Which component should receive the first implementation prototype?
- Should terminal type-on motion be used at all outside search/path labels?

## Next Steps

- Use this spec to create page specs for player profile, course leaderboard, and gauntlet detail.
- Ask the concept/design AI to refine exact font choices, component details, and color token tuning.
- Run another Pencil pass using this design system plus the IA spec, not the original broad prompt.
