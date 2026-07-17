# Ascent Rivals Pencil Terminal Ops Follow-Up Prompt

Date: 2026-05-11
Status: Draft
Navigation contract reviewed: 2026-07-16

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
- the approved shared destination model in a compact responsive top bar

## Required Outputs

Produce four static mocks:

1. Desktop player profile page
2. Desktop course leaderboard page
3. Desktop gauntlet detail page refinement
4. Mobile shell state, preferably showing either player profile or gauntlet detail

Optional if time allows:

- one quick desktop homepage refinement showing the current top-bar collapse behavior

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
- Gold is an accent, command, active, and CTA color. Do not turn the whole site into black-and-gold luxury styling.
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
- Keep the semantic destination order stable across every page: Gauntlets, Pilots, Teams, Courses, Events.
- Always keep brand/home, search, and login/avatar directly accessible. Show a `More` or menu trigger whenever a destination is hidden.
- On wide desktop, show all five destinations only when they fit cleanly without wrapping or compressed labels.
- As width decreases, move Events and then other destinations from the right side of the ordered list into `More`.
- Keep About and Brand in `More` and the footer. Put authorized sponsor operations in the account/admin menu.
- Do not add a separate marketing/competition bridge label; brand/home and Gauntlets provide that continuity.
- Show a direct `Sign in with Steam` action for anonymous users, not a provider dropdown. Compact layouts may shorten the visible label to `Sign In` beside the Steam icon while preserving the full accessible meaning.
- Page-local navigation should handle deep sections. Do not use a permanent global side nav.
- Contextual side panels are allowed inside data-heavy pages when they help scanning.
- Default long entity pages and forms to readable section anchors; use true tabs only for mutually exclusive panels and segmented controls only for small module-level filters.
- On mobile, replace long section rows with a labeled jump menu. Do not rely on hidden horizontal scrolling.
- Command-like text may add visual character but cannot replace ordinary visible labels or accessible names.

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
  - avatar, player name, and team tag/name; no generic global rank tier or rank-history module
  - career overview
  - course stats
  - leaderboard placement module
  - `Recent Races` overview: an exact newest-first table for bounded public-course multiplayer results and an optional discrete raw circuit-points plot for recent Ascent Mode matches
  - no rolling/improvement trend and no match-detail page
  - `Gauntlet History`: a compact responsive list with active public participation first, then completed entries ordered by latest pilot activity; adapt each entry to qualifier facts, accepted stage placement, or a general participation summary without forcing one rigid result schema
  - no aggregate cross-gauntlet chart, no qualifier rank presented as a tournament finish, and no invitation or eligibility state
  - `Achievements & Medals`: completed public Eventun achievements/masteries first and known gameplay-medal totals second, using a text-first treatment that does not require custom icon art
  - no inferred trophies, active/incomplete progress, challenges, raw counters, or reward UI
  - own-profile overlay area for approved team/account actions; no wallet module
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
  - schedule
- Preserve standings, stats, sponsor display, and non-prize admin action affordances.
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
- Put the complete primary destination list in the opened menu, beginning with Gauntlets and preserving the approved order.
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
- Does the stable top bar make the unified site feel connected without overcrowding wide or compact layouts?
- Can the player profile show strengths without inventing unsupported stats?
- Does the leaderboard page remain scannable?
- Does the gauntlet detail page correctly distinguish qualifiers from heats?
- Does mobile preserve brand/home, search, account access, and the complete destination path?
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
