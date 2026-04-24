# Ascent Rivals Website Tone and Voice

Date: 2026-04-13
Status: Draft

## Related
- [[unified-design]]
- [[information-architecture]]
- [[terminal-ops-design-system]]
- [[pencil-design-brief]]
- [[pages/homepage]]

## Purpose

Define the voice layer for the unified Ascent Rivals website.

The site should feel like a shipboard computer, pit-wall terminal, or race operations system presenting live competition intelligence.

This supports the Terminal Ops visual direction without turning the UI into parody or making important information harder to read.

## Core Voice

The voice should be:

- precise
- tactical
- compressed
- operational
- lightly in-world
- clear before clever

The voice should not be:

- jokey
- overly military
- faux-hacker
- verbose sci-fi prose
- full of fake diagnostics that obscure real actions
- so in-world that users cannot tell what a button does

## Voice Model

The site is not a narrator.

It is a race operations interface.

Useful mental models:

- ship computer
- team telemetry desk
- orbital race-control terminal
- gauntlet operations console
- sponsor-backed underground broadcast system

The UI should report state as if it is helping pilots, followers, and organizers understand what is happening now and what to do next.

## Copy Patterns

Use short operational labels.

Good:

- `Qualifier Window Open`
- `Final Stage Scheduled`
- `Pilot Status`
- `Current Rank`
- `Prize Pool`
- `Standings Sync`
- `Wallet Link Required`
- `Team Invite Pending`
- `Signal Acquired`

Avoid:

- `Welcome to the ultimate future racing experience`
- `Hack the mainframe`
- `You have entered the cyber-zone`
- `Oopsie, something went wrong`
- `Amazing job, racer`

## Empty and Error States

Empty and error copy should remain direct.

Good:

- `No qualifier standings available yet.`
- `No active gauntlets detected.`
- `Pilot profile not found.`
- `Unable to sync standings. Retry.`
- `Wallet link required before claiming rewards.`

Avoid:

- vague lore-only explanations
- blamey language
- jokes about user failure
- implying zero performance when data is missing

## Entity Voice

### Players

Use pilot/career framing where it clarifies the experience.

Good:

- `Career Overview`
- `Course Performance`
- `Best Lap Signal`
- `Match History`
- `Gauntlet Record`

Avoid:

- negative callouts as entertainment
- fake strengths from weak data
- exposing private rating/ELO in public copy

### Gauntlets

Use competition-operations framing.

Good:

- `Gauntlet Briefing`
- `Qualifier Windows`
- `Final Stage`
- `Overall Standings`
- `Prize Manifest`
- `Sponsor Signal`
- `Pilot Eligibility`

Avoid:

- calling qualifiers heats
- calling match heats qualifiers
- hiding whether something is a real tournament structure or a match-internal runtime unit

### Teams

Use crew and roster language carefully.

Good:

- `Crew Roster`
- `Join Request`
- `Invite Pending`
- `Manage Roster`

Avoid:

- replacing clear team-management actions with lore-only labels

### Marketing

Marketing pages can be more cinematic, but they should still feel tied to the same race-control system.

Good:

- world hook
- game footage
- feature calls
- Steam wishlist CTA
- social and community links

Avoid:

- disconnected corporate marketing tone
- generic esports website phrasing

## Button and Action Rules

Primary actions should stay plain enough to be understood immediately.

Good:

- `View Gauntlet`
- `Create Gauntlet`
- `Edit Gauntlet`
- `Claim Reward`
- `Link Wallet`
- `Join Team`
- `Accept Invite`
- `Sign in with Steam`

Optional terminal treatment can appear around the action, but the action label should remain clear.

Example:

- visual label: `$ claim reward`
- accessible label: `Claim reward`

## Motion and Terminal Text

Terminal-style text animation can be used for:

- section reveal
- status updates
- loading diagnostics
- command prompt accents

Do not use typing animation for:

- long paragraphs
- primary navigation
- repeated table content
- critical errors
- frequently changing data

Motion should serve orientation, not delay comprehension.

## Accessibility Guardrails

- Do not rely on in-world terminology alone for critical state.
- Pair labels like `Signal Lost` with clear meaning, such as `Unable to load standings`.
- Keep action labels understandable to screen readers.
- Do not use terminal animation in a way that blocks keyboard or assistive technology usage.
- Avoid excessive all-caps text in long content.

## Design Implications

The visual design should support the voice through:

- status strips
- command-like section labels
- compact operational headers
- framed panels
- telemetry rows
- timestamped updates
- restrained in-world labels

The copy should not carry the entire sci-fi mood by itself.

The gritty sci-fi feel should come from the combination of palette, typography, imagery, framing, spacing, motion, and precise operational language.
