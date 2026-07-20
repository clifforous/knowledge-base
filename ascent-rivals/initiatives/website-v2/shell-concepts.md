# Ascent Rivals Website Shell Concepts

Date: 2026-04-11
Status: Draft

## Related
- [[unified-design]]
- [[ascent-rivals/archive/initiatives/website-v2/pencil-design-brief]]
- [[README|Website V2 initiative index]]
- [[terminal-ops-design-system]]
- [[ascent-rivals/system/design-language|design-language]]
- [[ascent-rivals/system/competition-runtime-terms|competition-runtime-terms]]

## Purpose

This note captures reviewed shell concept work for the unified Ascent Rivals website.

It should be used to preserve visual decisions and rejected ideas from design exploration, not as an implementation spec.

## Source Assets

Concept set:

- [[ascent-rivals/sources/website-concepts/terminal-concept|Terminal Ops design summary]]

Images:

- ![[ascent-rivals/sources/website-concepts/terminal-concept-homepage.png]]
- ![[ascent-rivals/sources/website-concepts/terminal-concept-gauntlet-detail.png]]
- ![[ascent-rivals/sources/website-concepts/terminal-concept-marketing-landing.png]]

Image dimensions:

- `terminal-concept-homepage.png`: 1440 x 900
- `terminal-concept-gauntlet-detail.png`: 1440 x 900
- `terminal-concept-marketing-landing.png`: 1440 x 3102

## Review Update: 2026-07-15

The concept set was reviewed again after approving a marketing-first root route, reserving `/gauntlets` for Eventun-backed competition, and deferring `/game` from the initial route map.

Current assessment:

- The marketing landing is the strongest of the three concepts and is the best structural reference for the new homepage.
- Its hero, feature proof, ship schematic, partner strip, community section, and media treatment align with the approved homepage content categories.
- The original homepage concept no longer describes the root route. Its gauntlet, standing, and activity modules are references for competition pages only.
- The gauntlet-detail concept visually resembles a live match or heat view more than a gauntlet overview.
- `Qualifier Standings` combined with `Heat 1`, `Heat 2`, and `Heat 3` tabs incorrectly mixes gauntlet-level qualification with match-internal heats.
- Unverified live counts, season state, system-log events, rewards, and timing must not be reproduced as factual UI without supporting contracts.

Visual strengths to carry into the next review:

- strong cinematic hero hierarchy
- near-black and dark-navy foundation with warm off-white text and restrained gold emphasis
- heavy display headlines paired with technical supporting type
- technical schematics and ship-construction imagery
- thin rails, status markers, restrained telemetry, and compact data alignment
- a shared visual family that can vary between editorial and data-heavy pages

Visual weaknesses to address:

- repeated flat rectangular panels make the player concepts resemble a generic dark dashboard
- literal shell commands and box-drawing labels are overused
- small, low-contrast monospace text reduces readability
- the two 1440 x 900 data concepts leave excessive unused space while compressing useful information
- the concepts lack a distinctive Ascent Rivals shape language beyond the terminal metaphor
- surface depth and physical material cues are too weak for the intended industrial tone
- generated or illustrative imagery cannot substitute automatically for current approved game captures and art

Direction implication:

Terminal Ops remains a viable base, but the next pass should be treated as an evolution rather than a cleanup. It needs stronger spacecraft, racing, mechanical, and world-specific interface cues while replacing present-day shell imitation with a distinct in-world terminal language.

### Direction clarification

The terminal metaphor remains central.

The target is not a Linux terminal applied as a visual skin. It is an information terminal that could plausibly exist inside the Ascent Rivals setting and be used to inspect gauntlets, teams, pilots, planets, courses, ships, and related systems.

The terminal should combine:

- a futuristic information and navigation system
- race-control and vehicle-diagnostic precision
- salvaged hardware assembled from scrapyard machinery
- rusted hard metal, repaired plates, exposed fasteners, abrasion, heat, and age
- emissive display technology and status feedback that clearly belong to a more advanced future

The physical and digital layers should reinforce each other. Framing, seams, access panels, damage, and material transitions imply the terminal's rugged hardware; typography, scans, targeting marks, telemetry, maps, and entity indexing imply its advanced information system.

Present-day Linux conventions such as `$ cd`, `$ cat`, filesystem paths, and box-drawing syntax are references only. The revised system should develop its own readable Ascent Rivals command and indexing vocabulary without requiring users to understand a real shell.

The static exploded diagram based on an old ship model is not a canonical motif. Ship schematics remain viable only when they use current approved game models or data and present useful information through stronger diagnostic, modular, or interactive treatment.

### Working world context

The terminal can be framed as a receiver for a distributed underground race network. A short-lived gauntlet signal reaches crews and viewers; orbital support, racer-drone deployment, planet hazards, team and manufacturer information, and results can all appear as parts of the same information environment.

This is a visual narrative premise rather than locked lore. The exact authorities, communications system, deployment logistics, audience behavior, and betting culture remain undefined. Betting is not a Website V2 feature commitment.

Approved interaction direction:

- preserve ordinary clickable and touch navigation
- add a global entity-query console as a useful enhancement
- allow optional readable in-world commands such as `FIND`, `OPEN`, `SCAN`, and `TRACK`
- use race-network or registry hierarchy instead of Linux filesystem paths
- never require command knowledge to use the site

## Concept: Terminal Ops

Terminal Ops uses a command-line and spaceship-operations metaphor for the website shell.

Core traits:

- command prompt navigation
- terminal-style path bars
- bracket-framed panel headers
- monospace-heavy UI voice
- pipe-separated status and telemetry bars
- dark layered surfaces
- gold used as active command/accent language
- marketing pages and player utility pages share the same shell metaphor but vary density

## What Works

### Strong shell identity

The concept creates a recognizable website shell that feels more specific than a generic game landing page or generic dark dashboard.

The command prompt navigation is especially strong because it can support:

- direct route access
- search-everywhere language
- logged-in user identity
- a bridge between marketing and competition usage

### Good fit for returning-user utility

The homepage concept supports a returning-player mode well:

- gauntlet list
- standings sidebar
- system log
- status strip
- search/command affordance

This aligns with the product goal of not forcing known users back through pure marketing content.

### Strong data-surface compatibility

The terminal metaphor is compatible with:

- standings
- leaderboards
- qualifier status
- match history
- system logs
- player stats
- telemetry-style comparisons

This makes it a plausible shared shell for both public pages and logged-in overlays.

### Distinct from current app defaults

The concept moves away from the current Next.js/shadcn feel and gives the new Nuxt/Reka UI site a stronger custom visual identity.

## What Needs Caution

### Risk: terminal metaphor overuse

The command-line metaphor is strong but can become gimmicky if every label becomes shell syntax.

Use it for:

- primary nav
- search
- path/breadcrumb bars
- status strips
- select section labels

Avoid forcing it into:

- all body copy
- every CTA
- every table label
- all marketing headlines

### Risk: box-drawing character dependency

Bracket-framed headers are visually distinctive, but box-drawing characters may create accessibility, rendering, and localization issues if overused.

Implementation should prefer CSS-driven framing for production components where possible, with text characters reserved for lightweight accents.

### Risk: insufficient grit without imagery/material treatment

Terminal Ops feels operational and sci-fi, but not automatically gritty.

The production direction should combine the terminal shell with:

- worn or armored panel surfaces
- course/ship imagery
- subtle grime or abrasion textures
- bolder industrial framing
- more physical material cues

The concept should not collapse into a clean terminal dashboard.

### Risk: marketing page length and image dependence

The marketing landing concept is strong but image-heavy.

The final site should avoid assuming a continuous supply of high-quality full-bleed background art.

Use large imagery where it exists, but keep the shell strong enough to work with:

- smaller crops
- generated stills
- game screenshots
- abstracted UI/telemetry panels

## Adopted Direction Candidates

These are candidates to carry forward into the unified website design.

### 1. Command prompt nav

Adopt as a serious shell candidate.

Reason:

- supports search-everywhere
- fits the returning-player workflow
- visually distinguishes the site
- can work as top-nav or hybrid-nav

Open question:

- whether the final shell should be prompt-top-nav only or combine prompt-top-nav with contextual side panels.

### 2. Terminal path bar

Adopt for interior pages as a breadcrumb alternative.

Examples:

- `$ cd /gauntlets/orbital-blitz`
- `$ open /players/pilot-id`
- `$ list /courses`

Guardrail:

- path labels must still be understandable to non-technical visitors.

### 3. Status/telemetry strip

Adopt as a recurring website primitive.

Potential use:

- active season
- pilots online
- next gauntlet
- live event state
- user's qualification state
- system/news highlights

### 4. Bracket/framed panel headers

Adopt as a visual pattern, but implement carefully.

Production recommendation:

- use CSS framing first
- use box-drawing glyphs only where they improve the brand voice and do not harm accessibility

### 5. System log module

Adopt as an optional content primitive.

Potential use:

- homepage activity feed
- gauntlet activity
- recent records
- recent qualifications
- event operations feed

## Rejected or Constrained Ideas

### Full terminal UI everywhere

Do not make every interaction look like a literal terminal.

The site still needs to serve:

- new game visitors
- press
- sponsors
- non-technical followers

### Pure monospace for all text

The all-monospace direction is distinctive, but the final site should test readability carefully.

Likely direction:

- monospace for nav, labels, data, status, and system modules
- stronger display face for brand headlines
- readable proportional body font where long-form editorial content needs it

### Global navigation decision

Terminal Ops has no side navigation.

Website V2 now adopts one responsive command-inspired top bar without a persistent global side navigation. The stable primary destinations are `Gauntlets`, `Pilots`, `Teams`, `Courses`, and `Events`; search and login/account remain direct utilities. Available width determines which destination links remain visible and which move into `More` or the mobile drawer.

The site may still use:

- contextual side panels on data-heavy pages
- local navigation within player/team/gauntlet sections
- collapsible page-local utility navigation on logged-in views

These are page composition tools, not alternate global shells.

## Impact on Unified Website Design

Terminal Ops suggests the strongest current shell direction is:

- top-level command nav
- dark operational shell
- entity/content surfaces inside framed panels
- telemetry/status strips as navigation and context aids
- player-facing utility pages with a calmer data-forward interior

This does not eliminate the need for other shell concepts, but it gives a credible candidate direction for the design system.

## Follow-Up Design Questions

- How much monospace is acceptable before readability suffers?
- Should the search-everywhere interaction literally behave like command input?
- Can the terminal shell be made gritty enough without overwhelming player stat pages?
- How should this style adapt to mobile without becoming novelty terminal UI?
- Which page should be used for the next deeper mock: player detail, gauntlet detail, or course leaderboard?

## Next Recommended Mock Pass

Run one focused follow-up pass using Terminal Ops as the base direction.

Request:

- one player profile page
- one course leaderboard page
- one gauntlet detail refinement
- one mobile shell state

Design goals:

- test data density
- test accessibility/readability
- test prompt navigation with real routes
- test player-strength modules
- test qualifier-vs-heat terminology correctness
