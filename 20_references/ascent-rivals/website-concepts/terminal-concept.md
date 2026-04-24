# Terminal Ops — Design Language Summary

## Typography

| Role | Font | Weight | Size Range | Tracking |
|------|------|--------|------------|----------|
| **Display / Headlines** | Inter | 900 (Black) | 28–72px | +2–4px |
| **Everything else** (nav, labels, body, data, status) | IBM Plex Mono | 400–700 | 9–16px | +1–2px |

The entire UI voice is monospaced except for headlines. This is the single biggest differentiator — it makes the site feel like a spaceship operating system, not a marketing page wearing a skin.

## Color System

| Token | Hex | Usage |
|-------|-----|-------|
| `terminal-bg` | `#0A0A12` | Page background — near-black with blue undertone |
| `surface-deep` | `#080810` | Section backgrounds, nav bars |
| `surface-panel` | `#0F0F1A` | Card/panel bodies |
| `surface-raised` | `#161625` | Panel headers, table headers |
| `surface-border` | `#1E1E30` | Subtle dividers, panel strokes |
| `brand-gold` | `#F2A900` | Primary accent — active states, section titles, CTAs, user identity |
| `gold-border` | `#F2A90055` | 33% opacity gold — major dividers (nav underline, footer top) |
| `gold-dim` | `#F2A90033` | Subtle gold wash |
| `text-primary` | `#E8E4D8` | Headlines, primary content — warm off-white |
| `text-secondary` | `#B9B3A6` | Body text, descriptions |
| `text-dim` | `#6A6A7A` | Metadata, timestamps, decorative brackets |
| `accent-green` | `#4F9A68` | Live/online/qualified states |
| `accent-red` | `#C95644` | Eliminated, errors |
| `accent-lightblue` | `#63B8E8` | In-progress/racing states |

## Layout Architecture

**Page-level:** Vertical flex stack. Every section is a full-width row. No side-nav — the terminal prompt IS the nav.

**Section pattern (repeating):**

```
[content section]
[1px divider — surface-border or gold-border]
[content section]
```

The gold-border divider (`#F2A90055`) is used sparingly for emphasis (below nav, above footer). Standard dividers use `surface-border`.

## Signature UI Patterns

### 1. Command Prompt Navigation

```
❯ ASCENT RIVALS    GAUNTLETS   PLAYERS   TEAMS   STANDINGS    /search   PILOT_07
```

- Gold `❯` prompt character as logo stand-in
- Nav items in monospace uppercase with letter-spacing
- `/search` styled as a command, not a search icon
- User identity shown as a terminal username

### 2. Bracket-Framed Headers

```
┤ ACTIVE GAUNTLETS ├
┤ TOP PILOTS ├
┤ SYSTEM LOG ├
```

Panel headers use box-drawing characters (`┤ ├`) around the title. Gold text, `surface-raised` background. This is the primary "component header" pattern.

### 3. Transmission Brackets (Hero sections)

```
┌─── INCOMING TRANSMISSION ─────────────────────┐
  RACE HARD.
  WIN HARDER.
└────────────────────────────────────────────────┘
```

Used for hero/splash content. Box-drawing top and bottom in `text-dim`, content between.

### 4. Terminal Command Labels

```
$ cat /features
$ ls /ship/components
$ join /community
$ cd /gauntlets/orbital-blitz-s3-07
```

Section headers use shell command syntax as a label above the display headline. These replace generic "Features" breadcrumbs with something that feels native to the terminal metaphor.

### 5. Status / Telemetry Bars

```
◆ SEASON 3 ACTIVE │ PILOTS ONLINE: 2,847 │ NEXT GAUNTLET: 03h 42m │ SYS STATUS: NOMINAL
```

Pipe-separated monospace data strips. Gold diamond for primary status. Green for system health. These sit between sections as transition elements.

### 6. Panel Cards

- Structure: `surface-panel` fill + 1px `surface-border` stroke
- Header: `surface-raised` background, bracket title
- Body: Monospace text with generous line-height (1.5)

### 7. System Log

```
[04:12:07] Gauntlet ORBITAL_BLITZ started        (green)
[04:11:41] NIGHTCRAWL course record: 1:23.07      (gold)
[04:11:12] IRONWAKE eliminated — heat 2            (red)
```

Timestamped monospace entries with color-coded severity. This is the "activity feed" pattern.

### 8. Data Tables

Horizontal flex rows with fixed-width columns (POS, PILOT, TIME, STATUS). Top border dividers between rows. Monospace throughout. Gold for rank #1 and current user.

## Per-Screen Breakdown

### Homepage (shell concept)

```
cmd-nav → gold-border divider → hero (360px, bg image + gradient overlay)
→ status bar → border → content-body (2-column: gauntlet list + right sidebar)
```

Right sidebar: standings table + system log. This is the "logged-in returning user" view.

### Interior — Gauntlet Detail

```
cmd-nav → gold-border → path bar ($ cd /gauntlets/...) → border
→ gauntlet-hero (200px, bracket-framed briefing + stats) → border
→ int-body (2-column: qualifier table + prize/schedule sidebar)
```

The path bar adds breadcrumb navigation in terminal syntax. Interior heroes are shorter (200px vs 360px).

### Landing Page (marketing)

```
cmd-nav (with WISHLIST CTA) → gold-border → hero (600px, big tagline)
→ partner strip → border → features (3-col cards with images)
→ border → status bar → border → ship customization (800px, bg image + 2x3 grid)
→ border → community (3-col cards) → border → gallery (bg + thumbs)
→ gold-border → footer
```

Marketing version uses larger heroes, image-heavy sections, and a CTA in the nav. The terminal metaphor stays consistent but the content density shifts from data to editorial.

## Converting to a Design System

### CSS Custom Properties

The 18 design tokens map directly to CSS variables. The surface hierarchy (`deep → panel → raised`) creates a consistent elevation model.

### Component Library (for Nuxt/Reka UI)

| Component | Description |
|-----------|-------------|
| `TerminalNav` | Prompt, nav items, search, user slot |
| `BracketPanel` | Header with `┤ TITLE ├`, body slot |
| `StatusBar` | Pipe-separated telemetry items |
| `DataTable` | Monospace rows with fixed columns |
| `SystemLog` | Timestamped color-coded entries |
| `HeroSection` | Background image + gradient overlay + bracket-framed content |
| `PathBar` | Terminal-style breadcrumb (`$ cd /path/to/page`) |
| `TerminalLabel` | `$ command /section` above a display headline |

### Spacing Scale

The design uses `6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 60, 80` consistently. This maps to a 4px base grid.

### Breakpoint Strategy

The monospace + vertical stack approach naturally degrades to mobile. Panels stack, tables scroll horizontally, bracket headers stay intact. The nav prompt `❯` could collapse to a hamburger with the prompt as the toggle label.
