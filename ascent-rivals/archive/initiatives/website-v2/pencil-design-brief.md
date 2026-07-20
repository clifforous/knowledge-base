# Ascent Rivals Pencil Design Brief

Date: 2026-04-10
Status: Superseded exploratory brief

Do not use this file as the active Pencil prompt. It preserves the initial shell exploration,
including decisions that have since changed. Use
[[ascent-rivals/initiatives/website-v2/information-architecture]],
[[ascent-rivals/initiatives/website-v2/terminal-ops-design-system]], and the
[[ascent-rivals/initiatives/website-v2/README|Website V2 initiative index]] for current
direction. The follow-up prompt was removed after its durable results were incorporated.

## Related
- [[unified-design]]
- [[shell-concepts]]
- [[ascent-rivals/initiatives/website-v2/README|Website V2 initiative index]]
- [[terminal-ops-design-system]]
- [[tone-and-voice]]
- [[ascent-rivals/initiatives/website-v2/pages/homepage]]
- [[ascent-rivals/initiatives/website-v2/pages/player-directory]]
- [[ascent-rivals/initiatives/website-v2/pages/course-leaderboards]]
- [[ascent-rivals/initiatives/website-v2/pages/teams-index]]
- [[ascent-rivals/initiatives/website-v2/pages/team-profile]]
- [[ascent-rivals/initiatives/website-v2/sponsor-administration-handoff]]
- [[ascent-rivals/system/design-language|design-language]]
- [[ascent-rivals/system/game-design|game-design]]
- [[ascent-rivals/system/lore|lore]]

## Purpose

This note is a design brief for exploratory work in Pencil.

It is intentionally not a final layout specification.

The immediate goal is to give Pencil enough product, visual, and asset context to generate strong mocks for a unified Ascent Rivals website without prematurely freezing:

- homepage composition
- navigation pattern
- exact page layouts
- final component library details

## Current Iteration Goal

This iteration is specifically for shell and navigation exploration.

The output should be a small set of static concept mocks that help decide:

- the shell direction
- the navigation direction
- how marketing and competition content coexist

This is not a request to design or generate the full site.

## Hard Constraints for Pencil

For this round, Pencil should:

- produce 2 to 4 distinct shell concepts
- focus primarily on navigation, chrome, framing, and overall page structure
- show homepage framing for anonymous and logged-in states at a high level
- optionally show one interior-page shell check per concept

For this round, Pencil should not:

- generate the entire website
- generate every page in the sitemap
- overproduce detailed components
- treat the brief like a production build request

## Design Task

Design a unified public-facing Ascent Rivals website that combines:

- branded game-marketing surfaces
- public competition browsing
- public player, team, and gauntlet stats
- lightweight logged-in personalization

The site should feel like one product, not a marketing site bolted onto an admin tool.

The design work should explore the bridge between:

- discovery for new visitors
- repeat-use utility for players and followers

## What Pencil Should Optimize For

- a strong Ascent Rivals brand feel tied to the in-game palette
- a cohesive experience across marketing and competition pages
- a dark, cinematic, competitive visual system that still supports dense stats and standings
- fast scanning for returning users
- strong first impression for visitors who do not know the game yet
- flexible structure that can support both public and logged-in states
- a materially grittier sci-fi tone than the first mock achieved

## What Pencil Should Not Lock Yet

- final nav placement between side nav, top nav, or hybrid
- exact homepage adaptation rules for first-time versus returning users
- final information hierarchy between marketing and competition blocks on the home page
- final component styling for admin-heavy internal workflows

Pencil should explore alternatives rather than collapsing immediately into a single safe layout.

It should also avoid interpreting the prompt as permission to build the full product.

## Core Product Context

The new site is a single Nuxt application that must eventually support:

- marketing and game overview
- players
- teams
- gauntlets and events
- public stats
- contextual sponsor branding and permissioned sponsor operations
- Steam-authenticated user context
- wallet linking after login
- later lore and watch surfaces

The site has two public-use modes:

1. Marketing public
   - visitors learning what Ascent Rivals is
   - needs strong branding, game footage, and call-to-action surfaces

2. Competition public
   - visitors who already know the game and want players, teams, gauntlets, standings, and stats

Logged-in users should often see additional personal context layered into public pages rather than being pushed into a disconnected internal app.

## Split Inspiration Model

The current reference set is mostly marketing-heavy.

Pencil should use those references primarily to shape:

- shell language
- navigation mood
- material treatment
- hero composition
- CTA shape language

It should not directly apply full-bleed cinematic-marketing patterns to every interior page.

The player-facing and gauntlet-facing parts of the site should be:

- calmer
- more structured
- more scan-friendly
- more data-forward

The goal is a shared brand shell with different content density modes, not one identical treatment across every page.

There is now a second reference set for player-focused and data-heavy surfaces.

Pencil should use those references to shape:

- leaderboards
- player profiles
- stat modules
- match-history treatment
- comparison and breakdown patterns

Those references should not override the Ascent Rivals brand shell.

## Implementation Context

The likely implementation stack is now:

- Nuxt
- Reka UI

This should not drive the visual style toward generic library defaults.

The new site should feel custom to Ascent Rivals rather than like a reskinned starter kit.

## Design Exploration Request

Pencil should produce 2 to 3 distinct directions for the shared shell and homepage.

Useful variation axes:

- navigation pattern
  - side-nav dominant
  - top-nav dominant
  - hybrid
- homepage emphasis
  - brand/editorial-first
  - competition-first
  - adaptive hybrid
- page density
  - cinematic/editorial
  - balanced
  - data-forward

Each direction should still feel like the same product family.

Each direction should be presented as a shell concept, not a full-site execution.

Useful output per concept:

- one homepage shell mock
- one interior-page shell mock
- a short rationale for the direction

## Brand and Mood

### Mandatory palette anchors

The design should anchor to the in-game brand palette.

Primary required colors:

- `BrandGold`: `#F2A900`
- `BrandDarkBlue`: `#11111F`

These two colors should define the site feel.

### Supporting colors

Use the rest of the game palette as optional support rather than equal peers.

| Token | Hex | Intended Use |
|---|---|---|
| `White` | `#E8E4D8` | primary text on dark surfaces |
| `Black` | `#121216` | dark text or deep surfaces |
| `Red` | `#C95644` | warnings, destructive, high-risk states |
| `Orange` | `#D98226` | warm highlight or accent |
| `Yellow` | `#C9B13F` | secondary highlight |
| `Green` | `#4F9A68` | positive state |
| `Blue` | `#3F74C2` | utility accent |
| `LightBlue` | `#63B8E8` | info accent |
| `Purple` | `#7157A8` | rare tertiary accent only |

Text guidance:

- `LightPrimaryText`: `#E8E4D8`
- `LightSecondaryText`: `#B9B3A6`
- `DarkPrimaryText`: `#121216`
- `DarkSecondaryText`: `#35353D`

### Palette usage guidance

- dark-first visual system
- gold should feel like a brand accent and warm metal, not a constant flood fill
- use off-white rather than pure white on dark backgrounds
- use auxiliary colors primarily for rank, states, charts, badges, and category accents
- avoid drifting into purple-dominant cyberpunk or generic black-and-gold luxury branding

### Desired emotional tone

- industrial sci-fi
- high-speed competition
- brutal but premium
- salvage-built and engineered, not clean utopian futurism
- cinematic without becoming vague
- esports-adjacent without looking like a template esports site

### Concrete visual cues to push harder

The first mock was not gritty enough.

Pencil should push harder into:

- armored or plated panel language
- machinery-inspired framing lines
- telemetry and race-instrument cues
- subtle wear, abrasion, grime, or heat-stained material treatment
- stenciled or engineered labels
- modular, bolted, or welded construction language
- premium-but-brutal surfaces that feel built for impact

This should stay readable and intentional. The goal is not random grunge textures everywhere.

### Avoid

- generic crypto or web3 luxury aesthetic
- default esports purple neon
- sterile SaaS dashboard language
- overly rounded toy-like UI
- flat generic blog layouts disconnected from the game mood
- smooth glossy sci-fi that feels too clean
- generic dark dashboards with gold accents pasted on top

## Typography Direction

Known current references:

- game client primary font direction: Opinion Pro Condensed
- current sites also use display-heavy fonts, but those should not be treated as fixed requirements

Design guidance:

- use a condensed, assertive headline voice
- support data-heavy surfaces with a readable secondary typeface
- make numerals, ranks, standings, and stat values feel intentional
- preserve enough restraint that dense pages remain usable

If Pencil supports custom font uploads, `Opinion Pro Condensed` should be treated as a strong reference for headings, labels, or brand moments.

## Product Screens Pencil Should Mock First

These are the highest-value exploration screens.

### Screen set A: shell exploration

- concept 1 shell
- concept 2 shell
- concept 3 shell if possible

Each shell concept should include:

- homepage shell framing
- one interior-page shell framing

### Screen set B: homepage exploration

- anonymous homepage
- logged-in homepage variant or logged-in state module treatment

### Screen set C: optional interior page check

- gauntlets list
- gauntlet detail
- player detail
- team detail

### Screen set D: optional marketing/editorial support

- `/game`
- code-authored partner strip treatment

If Pencil can only produce a smaller set first, prioritize:

1. homepage
2. interior-page shell check
3. gauntlet detail
4. player detail

## Phase-1 Must-Have Pages

- `/`
- `/game`
- `/gauntlets`
- `/gauntlets/[id]`
- `/players`
- `/players/[id]`
- `/teams`
- `/teams/[id]`

Sponsor registry/detail screens belong to the Eventun Extend App rather than Website V2 or its Pencil page set. Gauntlet creators use direct billboard uploads first and may receive a scoped advanced sponsor picker.

## Nice-to-Have Phase-1 Pages

- `/features`
- `/media`
- `/courses`
- `/press`

## Later Pages

- `/watch`
- `/lore`
- `/faq`

## Homepage Guidance

The root homepage is now better defined in [[ascent-rivals/initiatives/website-v2/pages/homepage]].

It should be explored as the primary marketing and conversion page, with the gritty sci-fi Terminal Ops system framing a readable product narrative rather than a dashboard.

Approved content order:

1. hero and primary conversion
2. gameplay and Ascension Mode
3. ships and customization
4. one optional bounded race-network proof module
5. worlds, planets, and courses
6. events and community
7. final conversion and next actions

Use `Play Now` as the default conversion label when accurate for the release state. Reliable confirmed ownership may promote `Explore Gauntlets` inside the same CTA region. Sign-in alone does not prove ownership or installation.

Anonymous, authenticated, and confirmed-owner states use the same section order, module placement, and responsive composition. Personalization may change content or actions only inside an existing slot.

Do not add a homepage telemetry strip, generated system log, leaderboard grid, or separate logged-in command-center layout. Keep global entity search in the shared top bar.

The optional race-network module may feature one meaningful current/upcoming gauntlet, a recent gauntlet, or an explicitly labeled code-authored event recap. Omit it when no strong content exists.

The output should establish the hierarchy, material system, readable typography, media treatment, CTA region, optional competition proof, and consistent anonymous/authenticated composition without fully designing every implementation state.

## Entity Page Guidance

## Player Data Product Principle

The career and player-stat surfaces should not only reward the fastest or highest-ranked players.

A good Ascent Rivals player profile should help each player understand what they are good at, even if they are not top-tier in traditional rankings.

Examples of useful positive framing:

- strong performance on a specific course
- best finish time on a specific course
- best lap time on a specific course
- notable course leaderboard placement

Avoid using these as V1 player-strength modules:

- total kills, total playtime, total races, or other counters that mainly increase with volume
- deaths, crashes, or other negative or joke-framed stats
- combat style, consistency, improvement, survival, ship-part, or loadout claims unless the implementation data can support them cleanly
- generated medals/badges that could be confused with real in-game AccelByte medals or badges

This should influence visual design.

The player profile should support:

- optional headline strengths
- contextual comparisons
- real trophies, medals, or badges only where supported by backend or AccelByte data
- stat cards that explain why a player is interesting, not only where they rank

### Player page

Default content structure:

- Overview
- Course Stats
- Match History
- Gauntlet Results
- Trophies and Medals

Default first-view priority should be identity and career totals first, course stats and course placements second, and optional best-lap/best-finish strength highlights only when the data supports them.

Key design challenge:

- combine aspirational profile identity with dense competitive information

### Team page

Default content structure:

- Overview
- Roster
- Gauntlet Results
- Team Stats
- Trophies and Medals
- Manage for authorized users

Key design challenge:

- support both public team fandom and authenticated team-management affordances

### Gauntlet list

Current preferred structure:

- default `Gauntlets` view lists each entity once in a combined `Current & Upcoming` scope;
- current occurrence windows sort first, then remaining gauntlets by nearest future occurrence;
- `Past` is a URL-backed secondary scope;
- alternate `Schedule` view is a chronological agenda that may repeat one gauntlet for multiple qualifier or stage occurrences;
- a long-lived gauntlet is not current during gaps between its actual occurrences;
- avoid separate empty Current and Upcoming bands.

Use a responsive agenda rather than a month grid initially. Schedule timing does not justify a `Live` label without an explicit runtime or broadcast state.

For ordinary gauntlet-directory cards, place verified artwork in a fixed-ratio media bay beside the information panel on wider layouts and above it on narrow layouts. Keep essential text on an opaque or near-opaque surface rather than overlaying variable uploaded art. The existing gauntlet `Background` media may be used as cropped source art, but reserve full-bleed atmospheric treatment for gauntlet detail or one deliberately featured module with a strong scrim and contrast review. Keep Schedule rows image-light and never use per-row background art.

### Gauntlet detail

Current content priority:

1. qualifiers
2. finals or brackets
3. personal logged-in status
4. hero and branding
5. sponsors
6. watch stream
7. past winners or history

Standings are still required, but they do not need to dominate the whole page if qualification and finals presentation are stronger organizing structures.

### Qualifier vs heat terminology

Do not confuse qualifiers with heats.

- A qualifier is a gauntlet/tournament time window or qualification structure.
- A qualifier can span multiple sessions and multiple matches.
- A heat is a runtime round inside a match.
- A match can have one or more heats.
- A heat can have one or more laps.
- A lap is composed of checkpoints used for progress tracking and respawns.

Design copy should use:

- `Qualifier Standings` for tournament qualification
- `Heat Breakdown` for match-internal rounds
- `Lap Times` and `Checkpoint Splits` for course execution details

## Shared UX Elements to Explore

- search-everywhere interaction
- shell and navigation
- player/team/gauntlet cards
- standings tables
- trophy and medal displays
- scoped leaderboard and gauntlet-standing treatments; no global rank-tier badge
- sponsor strip or sponsor module
- CTA treatments for wishlist, play, or follow
- account/avatar state in global navigation

## Responsive Expectations

Pencil should show desktop first, but the concepts must be viable on mobile.

At minimum, the mock set should imply how these adapt:

- homepage hero and CTA stack
- dense stats modules
- standings tables
- navigation
- profile and gauntlet sub-navigation

## Asset Pack for Pencil

Pencil should be given access to existing site assets as reference material.

These are not final layout instructions. They are inputs for mood, branding, and visual continuity.

### Brand marks

- `projects/genun/ascentun/public/ascent-logo.png`
- `projects/genun/website/public/ascent-header-logo.svg`
- `projects/genun/website/public/ascent-banner-logo.png`
- `projects/genun/website/public/ascent-banner-logo-black.png`
- `projects/genun/website/public/ascent-icon.png`
- `projects/genun/website/public/ascent-logo-banner-gray.png`

### Hero and atmosphere imagery

- `projects/genun/website/public/ascent-banner.jpg`
- `projects/genun/website/public/ascent-oria.jpg`
- `projects/genun/website/public/ascent-nuelo-top.jpg`
- `projects/genun/website/public/ascent-ships-aerial-view.png`
- `projects/genun/website/public/ascent-section-background.jpg`
- `projects/genun/website/public/ascent-features-background.jpg`
- `projects/genun/website/public/ascent-trailer-background.jpg`
- `projects/genun/website/public/moon-ship-banner.png`
- `projects/genun/website/public/ship-setting.png`
- `projects/genun/website/public/ascent-oria-4.png`
- `projects/genun/website/public/ascent-playtest.jpg`

### Competition and gameplay imagery

- `projects/genun/website/public/features-competition.gif`
- `projects/genun/website/public/features-drive-to-survive.gif`
- `projects/genun/website/public/features-dual-engines.gif`
- `projects/genun/website/public/ascent-competition-brackets.png`
- `projects/genun/website/public/rival-match-banner.png`
- `projects/genun/website/public/ascent-dual-ship.png`
- `projects/genun/website/public/ascent-ship.png`

### CTA and social assets

- `projects/genun/website/public/steam-wishlist.png`
- `projects/genun/website/public/watch-now-icon.svg`
- `projects/genun/website/public/play-icon.svg`
- `projects/genun/website/public/discord-logo.svg`
- `projects/genun/website/public/x-logo.svg`
- `projects/genun/website/public/youtube-block-icon.svg`

### Fallback placeholders from current app

- `projects/genun/ascentun/public/player-placeholder.png`
- `projects/genun/ascentun/public/team-placeholder.png`
- `projects/genun/ascentun/public/gauntlet-placeholder.png`
- `projects/genun/ascentun/public/course-placeholder.png`

### Fonts if Pencil supports upload

- `projects/genun/ascentun/app/opinion-pro-condensed-medium.otf`

## Recommended First Upload Pack

If the initial Pencil pass should stay small, upload these first:

- `ascent-logo.png`
- `ascent-header-logo.svg`
- `ascent-banner-logo.png`
- `ascent-banner.jpg`
- `ascent-oria.jpg`
- `ascent-ships-aerial-view.png`
- `ascent-section-background.jpg`
- `ascent-trailer-background.jpg`
- `ascent-competition-brackets.png`
- `rival-match-banner.png`
- `steam-wishlist.png`
- `opinion-pro-condensed-medium.otf` if supported

## Prompt Seed for Pencil

Use this as a starting prompt and adjust after the first mock round.

```text
Design a shell exploration pass for a unified public-facing website for Ascent Rivals, a sci-fi competitive racing/combat game.

This is not a request to build the full site.
Do not generate a complete site, exhaustive page system, or production implementation.
Produce 2-4 distinct high-level mock directions focused on shell, navigation, and homepage framing only.

Each direction should show:
- a homepage shell
- one interior-page shell state
- a short rationale

Use the in-game brand palette as the foundation:
- Brand gold: #F2A900
- Brand dark blue: #11111F
- Light text: #E8E4D8
- Secondary light text: #B9B3A6

The tone should feel industrial, gritty, high-speed, competitive, and cinematic. It should not look like a generic esports template, a SaaS dashboard, or a crypto-luxury black-and-gold site. Keep the overall mood dark-first, with gold used as a brand accent and warm metal rather than everywhere.

Push harder into gritty sci-fi cues:
- armored panels
- telemetry
- engineered framing
- subtle wear and impact
- salvage-built premium machinery

Avoid:
- clean glossy sci-fi
- generic dark dashboards
- purple-neon esports styling
- smooth generic gaming landing-page aesthetics

Do not lock the design to a single obvious layout too early. Explore 2-3 directions for:
- navigation pattern
- homepage composition
- density of competition/stats surfaces

The likely implementation stack is Nuxt plus Reka UI, but do not let that collapse into library-default styling.

For this pass, prioritize:
- anonymous homepage shell
- logged-in homepage shell variation
- one interior-page shell check such as gauntlet detail or player detail

The homepage must work for both:
- new visitors learning what the game is
- returning players/followers who want quick access to gauntlets, stats, and search

Anonymous homepage priorities:
1. hero trailer/banner
2. play or wishlist CTA
3. news/announcements
4. game features
5. social/community links
6. lore/world hook

Logged-in homepage priorities:
- search everywhere
- gauntlets with my rank or participation status
- course leaderboards

Use the uploaded image and logo assets as reference material for composition, mood, and reference.

Use marketing-heavy reference sites mainly for shell language, navigation mood, and hero composition.
For player-facing and gauntlet-facing interior pages, simplify the composition and increase scan clarity.

Use player-stat reference sites for leaderboard and profile information architecture.
Player pages should help players understand their strengths, not only whether they are fastest or highest-ranked.
Show room for highlight modules such as best course by lap time or best course by finish time.
Do not invent medals, badges, negative stat jokes, or playtime/dedication modules for the first player-profile mock.

Terminology guardrail:
- qualifiers are not heats
- qualifiers are gauntlet/tournament windows that can span many sessions and matches
- heats are match-internal rounds
- matches contain heats, heats contain laps, laps contain checkpoints

Important:
- shell concepts only
- static mock exploration only
- no full-site generation
- no exhaustive component system yet
```

## Reference Site Input

Additional reference sites should be added before the next Pencil pass.

They should be used to sharpen:

- shell language
- material treatment
- gritty sci-fi tone
- motion and editorial drama

They should not be copied literally.

## Current Reference Sites

These references are useful, but mostly as marketing-shell inspiration rather than direct templates for player-utility pages.

### MechWarrior 5 Mercenaries

Reference:

- https://mw5mercs.com

Borrow:

- gritty sci-fi impression built through imagery
- strong type presence
- acceptable semi-transparent surface language as a reference only

Avoid:

- image stacking that makes the page feel too busy
- heavy reliance on layered visuals that reduce hierarchy clarity
- semi-transparent buttons as a direct UI carryover, since that does not match the current game UI language

Translation for Ascent Rivals:

- use imagery and typography to create grit
- keep the composition cleaner and less overloaded

### Dune Awakening

Reference:

- https://duneawakening.com

Borrow:

- line work and structural framing that makes the page feel more engineered and sci-fi

Avoid:

- over-reliance on image-heavy composition if it overwhelms the content structure

Translation for Ascent Rivals:

- explore subtle line systems, dividers, grid marks, and structural overlays for shell framing

### Cyberpunk 2077: Phantom Liberty

Reference:

- https://www.cyberpunk.net/us/en/phantom-liberty

Borrow:

- more interesting button shapes
- stronger shape vocabulary than default rectangles
- more controlled image composition

Avoid:

- assuming access to extremely high-end custom background art at the same scale

Translation for Ascent Rivals:

- push CTA shapes, panel cuts, and framing geometry beyond generic rounded buttons

### Marathon

Reference:

- https://marathonthegame.com

Borrow:

- tighter command-line-like top-nav feeling
- variation in typography treatment
- use of orientation and placement to create brand tension, such as vertical type or edge labeling

Avoid:

- over-large cinematic treatment that crowds out utility
- interior layout choices that feel less resolved than the shell mood

Translation for Ascent Rivals:

- explore a sharper, more instrument-like nav treatment
- consider edge typography or secondary type orientation as a shell accent, not as decoration everywhere

### PRAGMATA

Reference:

- https://www.capcom-games.com/pragmata

Borrow:

- cut-corner box layout language
- half-page editorial chunks for features, videos, screenshots, and related marketing content
- textural full-page background treatment that does not depend on one giant hero artwork
- techy border details as a material reference
- animated GIF or short-motion content blocks where they clarify gameplay
- section headers that use a small icon/logo mark as part of the identity system
- small graphic markers and inset image treatments for editorial detail

Avoid:

- overusing ornate tech-border frames on every section
- making the page busier than the content requires
- copying the PRAGMATA identity, color world, or exact border assets
- relying on image borders that cannot be maintained or adapted cleanly in Nuxt
- applying marketing-page ornament density to player stats, leaderboards, or admin workflows

Translation for Ascent Rivals:

- use cut corners, technical border accents, and icon-backed section headers mostly on `/game`, `/features`, `/media`, and branded homepage modules
- prefer textural background layers, subtle material noise, grid marks, and angled panel cuts over huge bespoke background art
- reserve heavier decorative frames for major feature blocks, video modules, and screenshot groupings
- keep the competition/player side calmer and more scan-friendly than the marketing side

## Player and Stats Reference Sites

These references are for data-heavy player and competition surfaces.

They should inform the interior pages after the shell direction is selected.

### U.GG Leaderboards

Reference:

- https://u.gg/lol/leaderboards/ranking?region=na1-

Borrow:

- clean leaderboard presentation
- side-navigation precedent
- tabular hierarchy that stays readable
- player-overview structure as a useful baseline

Avoid:

- copying the League-specific information model
- letting the data page become visually detached from the Ascent Rivals shell

Translation for Ascent Rivals:

- use as a reference for players, team leaderboards, course leaderboards, and gauntlet standings

### HLTV Stats

Reference:

- https://www.hltv.org/stats?csVersion=CS2

Borrow:

- game-stat and player-stat breakdown patterns
- examples of stats grouped by domain such as player performance and equipment/weapon usage

Avoid:

- the overly compact visual density
- the older table-heavy feeling as a direct style reference

Translation for Ascent Rivals:

- use the information architecture idea, not the visual density
- useful analogy for ship parts, course performance, and player performance breakdowns

### Blitz Valorant Profile

Reference:

- https://blitz.gg/valorant/profile/QOR%20Notexxd-amru

Borrow:

- profile page with components that have enough room to breathe
- match-history section as a deeper scroll area rather than forcing every detail above the fold
- balanced module spacing

Avoid:

- advertisement-driven layout disruptions

Translation for Ascent Rivals:

- use as a reference for player career pages that mix overview, strengths, recent matches, and detailed sections without feeling cramped

### Lolalytics Champion Build Page

Reference:

- https://lolalytics.com/lol/kayle/build/

Borrow:

- depth of statistical breakdown
- many ways to segment and compare performance
- evidence that very deep player-facing stats can be valuable

Avoid:

- visual busyness
- overwhelming the first view
- presenting advanced breakdowns before the user understands the primary story

Translation for Ascent Rivals:

- use as a long-term reference for deep stats, not as the first-pass visual density
- useful model for showing how course, ship part, loadout, map, and match context affect performance

### Rocket League Tracker Leaderboards

Reference:

- https://rocketleague.tracker.network/rocket-league/leaderboards/playlist/all

Borrow:

- leaderboard model for another track-based competitive game
- playlist/mode-oriented leaderboard filtering
- global and regional filter pattern
- clean ranking table structure for skill rating and related competitive metrics

Avoid:

- generic tracker-network visual language as a direct style reference
- ad or app-promo layout distractions
- leaderboard-only framing that ignores player strengths outside top rank

Translation for Ascent Rivals:

- use as a reference for course leaderboards, gauntlet standings, and ranked competitive views
- support filters such as course, mode/ruleset, region, season, team/solo context, and rating/stat type
- keep room for both rank-based leaderboards and strength-based player profile highlights

## Review Criteria

The first Pencil round should be reviewed against these questions:

- Does it feel like Ascent Rivals rather than a generic gaming site?
- Does the gold and dark-blue relationship feel authentic to the game palette?
- Does the design bridge marketing and competition utility credibly?
- Is the homepage flexible enough to support both anonymous and logged-in audiences?
- Can the system handle dense standings and stats without collapsing aesthetically?
- Do player, team, and gauntlet pages feel like first-class public destinations?
- Does the design still leave room for later lore and watch surfaces?

## Next Step After First Mock Round

After the first Pencil output, create a follow-up note capturing:

- which shell direction is strongest
- which homepage strategy is strongest
- which page patterns should converge into a design system
- what data-dense components need a second pass
- which routes need additional mock coverage
