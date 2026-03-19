# Ascent Rivals - Game Design

## Related
- [[overview]]
- [[lore]]
- [[game-client]]
- [[eventun/overview|eventun]]

## Overview

This note is a game design domain dump for **Ascent: Rivals**, based on the long-running project context. It covers the playable structure, modes, progression concepts, ship design, tournament framing, and the major systemic pillars that define the game.

Ascent: Rivals is a competitive sci-fi racing/combat game built around modular hover ships, dangerous courses, gauntlet-style competitive events, and a blend of speed, destruction, engineering, and extraction pressure.

---

## Core genre identity

The game is not purely a racing game and not purely a vehicular combat game. Its identity comes from the combination of:

- high-speed racing
- combat and eliminations
- modular ship customization
- event/tournament structures
- risk management under pressure

The result is something closer to a **combat racing gauntlet game** than a conventional lap racer.

---

## Primary level / flow types

The current game structure has three main level and flow types.

### 1. Headquarters

The primary hub experience is functionally the **menu system**, but thematically it is framed as the player’s **Headquarters** rather than as the hangar itself.

Functions include:

- reading news or event information
- checking stats
- entering matchmaking through a queue action
- entering custom games or tournament stages when those flows are available

For standard matchmaking, the player queues from this menu layer and then transitions directly to the course once the session is filled on the server.

The hangar is part of Headquarters rather than a primary level in its own right.

Within Headquarters, the **Hangar** is a more specific ship-management space.

Functions include:

- viewing ship parts
- inspecting the current ship configuration
- making cosmetic changes to ship parts

The hangar is no longer the place where pre-race gameplay loadout changes are made.

### 2. Lobby

The **Lobby** is a pre-race waiting and setup area, but it is not part of the default matchmaking flow. It is only reached from custom games or tournament stages.

Functions include:

- player assembly before a custom match or tournament stage
- ready-up flow
- racer vs spectator entry distinction
- bot backfill support

For custom games, the lobby leader can change the course, heats, bots, and bot difficulty. Tournament/event lobbies can auto-start when their stage conditions are met.

### 3. Race Courses

The **Race Course** is the actual competitive arena. This is where the driving, flying, combat, and race-start loadout adjustment flow occur.

The project currently emphasizes two primary game modes on race courses:

- Classic Race
- Ascent Mode

---

## Core modes

### Classic Race

Classic Race is structured around multiple heats and laps. Players earn points based on placement and eliminations.

Key ideas:

- you are rewarded for both finishing performance and offensive success
- points earned can be spent between heats
- between-heat adaptation matters

This gives the mode a metagame layer across the event rather than making each race a totally isolated sprint.

### Ascent Mode

Ascent Mode adds extraction pressure. After the top finishers cross the line, the remaining players must reach a safety zone to preserve their points.

If they fail to extract, they lose those points.

Why this matters:

- finishing well is not the only success condition
- survival and route control matter
- late-race tension stays high even after podium spots are settled
- the mode has a strong lore justification tied to authorities/corporate shutdown pressure

This is one of the game’s most distinctive designs.

---

## Gauntlets and multi-match competition

The game includes **gauntlets**, which are multi-match tournament structures.

A key redesign in the project context is that gauntlets are no longer thought of only as heats on different maps. They are now better understood as broader multi-match tournaments with qualifiers, optional stages, and potentially finals/brackets.

Important gauntlet design concepts from current project work include:

- qualifiers are time windows
- qualification is based primarily on **Circuit Points**
- best-sequence logic can be used within a qualifier
- overall rollup can sum a player’s **Top K qualifiers**
- finals/stages may be optional rather than mandatory
- top ranks may receive guaranteed slots rather than exclusive eligibility

This makes gauntlets a serious competitive backbone, not just a cosmetic playlist wrapper.

---

## Ranking and qualification concepts

The game’s competitive design includes nuanced ranking logic rather than simplistic cumulative totals.

### Circuit Points

Circuit Points are a central competition metric used for qualification and standings.

### Best Sequence

Within a qualifier, scoring can be based on the player’s **best rolling window of N matches**. This rewards consistency across a sequence without forcing every match in a large window to count equally.

### Top K qualifiers

Across multiple qualifiers, the gauntlet rollup can sum the player’s **Top K** qualifier performances. This allows players to recover from weaker qualifier windows and emphasizes peak performance within a season/event structure.

### Guaranteed spots vs total eligibility

The project context distinguishes between:

- top players receiving **guaranteed slots**
- lower-ranked players potentially still being able to join unless displaced by higher-qualified players

That is a more flexible and realistic tournament admission model than a hard binary cutoff.

---

## Ship design

Ships in Ascent: Rivals are modular. That is one of the most important design pillars.

The current ship structure includes components such as:

- engines
- stabilizers
- cockpit
- battery
- boosters / warp systems
- pilot-wielded weapon
- Ion Thrusters (formerly PRS)

### Ion Thrusters

The older PRS concept has been renamed to **Ion Thrusters**. These allow quick lateral movement / dashes using ion bursts.

This implies the game is not just about raw forward velocity. Reactive movement and short-burst repositioning matter.

### Engines

Engines are the major propulsion units, described as large turbine-like side structures.

### Stabilizers

Stabilizers control hovering behavior. A particularly important design idea is that flying closer to the ground increases speed but also danger.

That creates a meaningful skill curve around terrain proximity and route precision.

### Warp Drive

The warp drive charges a warping boost when engines are off. This implies a deliberate timing/risk tradeoff rather than a permanently available boost button.

### Weapon

The drone/pilot can wield a weapon, but cannot both fully pilot and hold a weapon simultaneously. This tension is important because it prevents combat from becoming a costless overlay on top of driving.

---

## Part classes and tradeoffs

Ship parts can be categorized as:

- light
- medium
- heavy

These classes influence:

- speed
- durability
- maneuverability

This creates a readable build language and supports specialized archetypes without needing every individual part to be completely bespoke.

---

## Progression and between-race adaptation

Progression in the project context works at multiple timescales.

### In-event progression

In Classic-style multi-heat formats, players can spend earned **ARC** between heats to upgrade or replace ship parts. This creates an event-internal economy and supports adaptation mid-competition.

### Long-term progression

Outside the event, players can use ARC in the broader store/progression ecosystem to unlock:

- new parts
- skins
- visual/structural improvements

Parts can also be improved slightly through upgrades that affect both stats and visuals, such as making equipment appear less rusted.

---

## ARC and economy

**ARC** is the in-game currency. It is an important economy pillar and should always be described clearly as such.

ARC is used for things like:

- unlocking parts
- purchasing or enabling cosmetic/progression options
- between-heat upgrades in some modes

Thematically, the store is framed as part of an underground trade network rather than a generic polished storefront.

The project also has longer-term exploration around making Arc backed by a blockchain representation, but game design wise ARC is first and foremost the game’s internal monetary resource.

---

## Cosmetic economy and anti-pay-to-win stance

The project context makes clear that the team wants to avoid pay-to-win mechanics.

That implies a design split such as:

- gameplay-relevant upgrades earned through play and competitive systems
- premium or special-currency purchases focused on structural/material cosmetics

Examples include cosmetic skins such as cleaner materials or cobalt-blue finishes rather than direct performance purchases.

This is important to the game’s competitive credibility.

---

## Frequent crashes and replacement logic

Crashing is frequent in the game. That is a feature, not an edge case. This affects multiple design decisions:

- players need rebuild/repair/replacement framing
- races must remain fun despite high destruction rates
- the fiction needs to explain fast replacement of drones/parts
- damage and elimination must be integrated into the event economy

This also supports the junkyard ethos: machines are valuable, but damage is expected.

---

## Player skill expression

The current design supports multiple skill axes rather than only “drive the shortest line.”

### Mechanical skill

- terrain-following precision
- low-hover risk management
- dash timing with Ion Thrusters
- boost/warp timing
- combat execution

### Strategic skill

- build choice
- upgrade spending between heats
- qualification planning across event windows
- map/mode adaptation

### Survival skill

- extracting in Ascent mode
- deciding when to engage vs disengage
- preserving points under pressure

That combination gives the game more depth than a conventional arcade racer.

---

## Spectators and bots

Custom-game and tournament-stage lobbies support:

- spectators
- bot backfill

This matters because it means the game is being designed not just for perfectly full player-only sessions, but for resilient event operation and potentially watchable competition.

---

## Competitive audience

The project context repeatedly points to a competitive audience. This has implications for design priorities:

- ranking clarity matters
- fairness and anti-pay-to-win matter
- gauntlet scoring needs to be explainable
- team and sponsor structures matter
- vehicle handling must reward mastery, not randomness

The design is trying to support a real competitive scene rather than only casual spectacle.

---

## Best single-sentence design summary

Ascent: Rivals is a competitive sci-fi combat racing game where players build modular hover ships, fight and race across hazardous courses, earn and spend ARC to adapt and progress, and compete in multi-match gauntlets whose standout mode forces not just a finish, but extraction under pressure.
