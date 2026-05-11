# Ascent Rivals Pencil Terminal Ops Follow-Up Prompt

Date: 2026-05-11
Status: Draft

## Related
- [[unified-design]]
- [[information-architecture]]
- [[terminal-ops-design-system]]
- [[tone-and-voice]]
- [[shell-concepts]]
- [[pencil-design-brief]]
- [[design-doc-roadmap]]
- [[pages/player-profile]]
- [[pages/course-leaderboards]]
- [[pages/gauntlet-detail]]
- [[../../../20_references/ascent-rivals/website-concepts/terminal-concept|terminal-concept]]

## Purpose

This prompt is for the next Pencil design pass.

It replaces the first broad shell exploration prompt for this iteration. The goal is not to generate more unrelated shell concepts. The goal is to validate the current Terminal Ops direction against dense data pages and mobile behavior.

## Design Pass Goal

Create a focused static mock pass for the unified Ascent Rivals website using Terminal Ops as the baseline design direction.

The pass should test whether Terminal Ops can support:

- dense player statistics
- course leaderboard filtering
- gauntlet detail hierarchy
- contextual page navigation
- mobile shell behavior
- the marketing-to-competition bridge in a compact global top bar

## Required Outputs

Produce four static mocks:

1. Desktop player profile page
2. Desktop course leaderboard page
3. Desktop gauntlet detail page refinement
4. Mobile shell state, preferably showing either player profile or gauntlet detail

Optional if time allows:

- one quick desktop homepage refinement showing the current top-bar bridge behavior

## Prompt To Paste Into Pencil

```text
Design a focused follow-up mock pass for the unified Ascent Rivals website.

This is not a broad concept exploration and not a full-site generation request. Use the existing Terminal Ops concept as the baseline design direction and test whether it works for dense player, leaderboard, gauntlet, and mobile states.

Product context:
- Ascent Rivals is a sci-fi competitive racing/combat game.
- The new website combines the current marketing website and current player/admin portal into one Nuxt application.
- The site has three experience modes:
  1. marketing public, for visitors learning the game
  2. competition public, for players/followers browsing gauntlets, players, teams, sponsors, and stats
  3. logged-in overlays, for account, wallet, team, participation, and admin actions
- Most entity pages should be public. Private and admin actions should layer into the relevant public page instead of feeling like a separate admin product.

Use Terminal Ops as the working visual direction:
- command prompt-inspired top navigation
- dark operational shell
- gold accent language
- terminal-style path/breadcrumb bars
- framed panels for entity and data surfaces
- telemetry/status strips
- system-log style activity modules where useful
- contextual page-local navigation for dense pages
- permissioned actions near the object they affect

Required brand palette:
- brand gold: #F2A900
- brand dark blue: #11111F
- primary text: #E8E4D8
- secondary text: #B9B3A6
- success/live: #4F9A68
- destructive/error: #C95644
- in-progress/info: #63B8E8

Palette guardrails:
- Gold is an accent, command, active, CTA, and reward color. Do not turn the whole site into black-and-gold luxury styling.
- Avoid purple-neon esports drift.
- Use off-white text instead of pure white.
- Keep auxiliary colors mostly in statuses, alerts, charts, ranks, badges, and telemetry.

Voice direction:
- precise
- tactical
- compressed
- operational
- lightly in-world
- clear before clever

Avoid:
- faux-hacker copy
- jokey error states
- vague lore-only labels for critical UI
- turning every label into shell syntax
- body text that is too monospaced or too dense to read

Global navigation requirement:
- Use top-bar-based global navigation.
- Always include brand/prompt identity, search, login/avatar, and a visible bridge between marketing and competition/player areas.
- On competition/player pages, include a bridge label such as Game, Marketing, or About Ascent.
- On marketing pages, include a bridge label such as Competition, Pilot Portal, or Gauntlets.
- The label is still open; propose a practical visual treatment.
- Page-local navigation should handle deep sections. Do not use a permanent global side nav.
- Contextual side panels are allowed inside data-heavy pages when they help scanning.

Mock 1: desktop player profile
- Route: /players/[id]
- Purpose: public pilot/career page with logged-in own-profile overlays where relevant.
- First-view priority:
  1. identity and career context
  2. career totals
  3. course stats and course placements
  4. optional strengths only when supported by best finish or best lap data
- Include:
  - player header/briefing
  - avatar, player name, team tag/name, public rank tier if available
  - career overview
  - course stats
  - leaderboard placement module
  - match-history overview, but no match-detail page
  - gauntlet results
  - trophies/medals only if clearly marked as backend-provided
  - own-profile overlay area for wallet/team actions
- Player principle:
  - The profile should not only reward the fastest or highest-ranked players.
  - It should help each player understand what they are good at.
  - Strength modules may show best course by finish time or best course by lap time.
  - Do not invent combat style, loadout style, consistency, survival, or improvement claims unless the data shown clearly supports them.
  - Do not include negative or joke-framed stats.

Mock 2: desktop course leaderboard
- Route direction: /courses, with selected course and category state visible.
- Purpose: public course leaderboard and course-performance discovery.
- Include:
  - leaderboard command header
  - course selector
  - selected course briefing
  - category filter
  - leaderboard table
  - personal placement strip for logged-in users
  - cross-course overview if space allows
- Preserve scan clarity over lore styling.
- Test whether course selection works better as a rail, strip, grid, or dropdown-first pattern.
- Preserve rank, player, time, and category at useful widths.
- Do not imply missing data means zero or poor performance.

Mock 3: desktop gauntlet detail refinement
- Route: /gauntlets/[id]
- Purpose: public gauntlet detail with logged-in personal status and authorized/admin actions near the relevant entity.
- Include:
  - gauntlet briefing
  - personal status overlay
  - qualifier windows
  - finals/stages/brackets area
  - standings
  - sponsors
  - prize manifest
  - schedule
  - watch/broadcast placeholder only if it does not dominate V1
- Preserve standings, stats, sponsor display, prize context, and admin action affordances.
- Permissioned actions should appear in-page, not as permanent global nav.
- Test both a rich active gauntlet and a sparse/upcoming gauntlet treatment if possible.

Terminology guardrail:
- Qualifiers are not heats.
- Qualifiers are gauntlet/tournament windows that can span many sessions and matches.
- Heats are match-internal rounds.
- Matches contain heats.
- Heats contain laps.
- Laps contain checkpoints.
- Do not label qualifier windows as heats.

Mock 4: mobile shell state
- Show how the top bar collapses.
- Required visible mobile top-bar items:
  - brand/prompt
  - search
  - menu
  - login/avatar
- If the marketing/competition bridge cannot stay visible, it must be the first item in the opened menu.
- Mobile does not need desktop density, but it must remain usable.
- Test data-table handling, two-column collapse, local section navigation, and touch target sizing.

Accessibility and implementation guardrails:
- Use semantic page structure in the implied layout: nav, main, sections, tables, headings.
- Do not rely on box-drawing characters as the only semantic frame.
- CSS-style framing should carry important structure.
- Search and nav should be keyboard-accessible in the implied interaction model.
- Color contrast should remain readable against dark surfaces.
- Motion should be subtle and optional; do not depend on terminal type-on effects for comprehension.

Design quality bar:
- This should feel like Ascent Rivals, not a generic esports site, generic SaaS dashboard, clean terminal dashboard, or crypto-luxury black-and-gold page.
- Make the shell more physical and gritty than a pure terminal UI through armored surfaces, worn panel texture, industrial framing, ship/course imagery, and restrained operational detail.
- Dense pages should remain calm, scannable, and useful.
- Marketing personality should not overwhelm player utility.

Deliver the pass as static mocks with short rationale notes for each screen:
- what layout decision it tests
- what works
- what remains risky
- whether Terminal Ops still looks viable after this page
```

## Review Criteria

Review the Pencil output against these questions:

- Does Terminal Ops still work when the page is data-dense?
- Does the top-bar bridge make the unified site feel connected rather than split?
- Can the player profile show strengths without inventing unsupported stats?
- Does the leaderboard page remain scannable?
- Does the gauntlet detail page correctly distinguish qualifiers from heats?
- Does mobile preserve search, account access, and the bridge path?
- Is the style gritty and physical enough without becoming unreadable?

## Follow-Up After Pencil Output

Create a short review note that records:

- strongest screen
- weakest screen
- Terminal Ops viability decision
- component patterns to carry forward
- route or IA changes implied by the mocks
- design-system changes needed before implementation
- remaining questions for user review
