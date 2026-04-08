# Match Summary and Time Trial — Improvement Recommendation Design

## What This Screen Must Do

After every run, the player should leave with one clear answer to: **"What should I do differently next time?"**

That answer is not a stat dump. It is a single, visually expressed recommendation — something like "use more warps on the shortcut segments," "your light-engine swap did not increase speed," or "you bled 4 seconds to energy starvation." Everything else on the screen exists to support that one takeaway with evidence.

The screen succeeds when a player can glance at it, understand what held them back, and know what to change before queuing again.

---

## What This Screen Must Not Be

- A generic delta board showing time changes and rank shifts with no direction attached.
- An analytics dashboard the player has to interpret themselves.
- A coaching essay. No prose. All improvement guidance is expressed visually.
- A screen that optimises only for lap time when the player is in match mode, where circuit points — not pace — are the real success metric.

---

## Scope for This Round of Mocks

These are the two screens to mock. Design both, but keep them clearly separated — they have different success axes and different supporting evidence.

### Post-Match (v1)

| Component | Content |
|---|---|
| Outcome strip | Final placement, circuit points, credits, best lap, best finish, kills / deaths / crashes |
| What changed | Finish delta, lap delta, placement or CP delta vs historical same-heat baseline |
| Where it changed | Weakest heat relative to historical same heat; weakest lap; weakest tagged segment type inside current match |
| Why it changed | Part-change delta, crashes / deaths, execution burden, kill and objective contribution, spend efficiency; use pre-ascension racing data for race-phase recommendations |
| **Primary recommendation card** | **One category, one player metric vs benchmark, where it showed up** |
| Heat progression strip | Per-heat: placement, finish time, best lap, circuit points, credits, loadout summary, loadout delta from prior heat |
| Match relative comparison | Your same-heat result vs match winner's; your best lap vs match best; your loadout vs top finisher's |

### Time Trial (v1)

| Component | Content |
|---|---|
| Outcome strip | Personal best finish, personal best lap, course rank, delta to rank 1, delta to next rank |
| Self-progress block | Delta vs previous attempt, delta vs personal average, last 3–5 attempts as a trend list, current build vs personal-best build |
| Execution snapshot | Slowest lap or tagged segment type, average speed, warps used, stall time, time out of energy, lap consistency, build change payoff |
| **Primary recommendation card** | **One category, one player metric vs benchmark, where it showed up** |
| Cost-bracket context | Overall client best finish rank, low-cost finish rank, high-cost finish rank, overall best lap rank |

---

## The Primary Recommendation Card

This is the most important component on both screens. It should be visually prominent — not buried in a list.

### What it contains

| Field | Purpose |
|---|---|
| Category label | Names the focus area (see categories below) |
| Player metric | What the player actually did |
| Benchmark metric | What the reference achieves |
| Location | Which heat, lap, or segment the loss showed up |
| Confidence indicator | Optional — show when evidence is thin |

### How it reads

The card does not use sentence-based coaching. It uses icon + label + metric pair. Examples:

| Category | Visual expression |
|---|---|
| Warp drive utilization | `Bought warp drive, 2 / 7 warp opportunities used` |
| Engine swap payoff | `Light engine swap, +1 kph / +6 kph benchmark` |
| Weapon spend payoff | `900c spent, 0 kills gained` |
| Corner speed | `142 kph / 158 kph benchmark` |
| Route choice | `0 / 2 shortcut opportunities taken` |
| Energy uptime | `4.1s empty / 0.8s target` |
| Slotted handling | `5 strafes / 11 benchmark in slotted segments` |
| Canyon control | `118 kph / 131 kph in canyon segments` |
| Engine class | `Medium class / Heavy benchmark` |
| Objective focus | `1 / 3 obelisks captured` |
| Crash avoidance | `3 crashes / 0.8 average` |
| Purchase timing | `Bought after heat 2 / benchmark buys after heat 1` |

### How the category is chosen

The system scores each candidate category by opportunity score:

```
opportunity score = impact × confidence × actionability
```

- **Impact** — estimated time loss (time trial) or estimated circuit point loss (match)
- **Confidence** — how strongly the evidence supports this category as the cause
- **Actionability** — whether the player can clearly change it next run

The highest-scoring category becomes the primary recommendation. Up to two additional categories can appear as secondary recommendations if the evidence is strong enough and the layout can support them cleanly.

This matters because the right lesson changes from run to run. One run is a corner-speed problem. Another is an energy-management problem. Another is a loadout mismatch. Another is a weapon-spend problem that did not convert into kills, credits, or placement. The card should reflect that, not repeat the same generic advice.

### Recommendation stack

The recommendation area should support:
- exactly 1 primary recommendation
- up to 2 secondary recommendations

The stack should follow these rules:
- The primary recommendation must be the highest-confidence, highest-impact action the player can take next run.
- Secondary recommendations can be broader and slightly less specific, but they still need to point at a real change opportunity.
- If the evidence is weak, do not force all three recommendation slots to appear.
- It is better to show 1 strong recommendation than 1 weak recommendation plus 2 filler cards.

Good secondary recommendation patterns:
- `Build investment`: loadout value increased but same-heat result stayed flat
- `Part payoff`: a part swap changed the build but did not improve the segment type it should help
- `Objective share`: circuit point composition leaned too little on objectives
- `Kill economy`: kill pressure was low even though the player invested in combat parts
- `Consistency`: laps varied more than the player's normal spread
- `Route opportunity`: faster runs used a different checkpoint path

Bad secondary recommendation patterns:
- repeating the primary recommendation with different wording
- generic deltas with no implied action
- categories whose evidence does not meet the confidence threshold

### Which categories apply to which mode

| Category | Post-Match | Time Trial | Notes |
|---|---|---|---|
| Warp drive utilization | Yes | Yes | Stronger now that part changes and tagged opportunities are available |
| Engine swap payoff | Yes | Yes | Compare speed change after engine swaps against similar runs |
| Weapon spend payoff | Yes | No | Match only — combat investment should be tied to kills, credits, and placement impact |
| Corner speed | Yes | Yes | Cleaner signal in time trial |
| Route choice | Yes | Yes | Shortcut-tagged segments make this more direct |
| Energy uptime | Yes | Yes | Direct from lap/checkpoint telemetry |
| Slotted handling | Yes | Yes | Best when the next segment is tagged `slotted` |
| Canyon control | Yes | Yes | Best when the next segment is tagged `canyon` |
| Crash avoidance | Yes | Secondary | Deaths and crashes are directly available |
| Objective focus | Yes | No | Match only — obelisks are the signal |
| Engine or build class | Yes | Yes | Stronger when tied to actual part-change events |
| Purchase timing | Yes | No | Supported when part-change events include buy or sell action and credits-after state |

---

## How the Supporting Evidence Is Organised: What, Where, Why, How

Every surface on the screen maps to one of four questions. The recommendation card is the "How." The rest of the screen answers the other three.

### What changed
- Total finish delta
- Lap delta
- Placement delta
- Circuit points delta (match only)
- CP composition shift across placement, kills, and objectives (match only)
- spend delta and part-change delta (when relevant)

### Where it changed
- Which heat was weakest relative to historical same-heat results
- Which lap was slowest inside the current match
- Which tagged segment type lost the most time
- Whether the player took or missed a route shortcut

### Why it likely changed
- Loadout difference from historical same-heat baseline
- part changes and their payoff against the segment types they should improve
- Crashes, deaths, respawn interruptions
- Stall time and time out of energy as execution discipline signals
- Combat efficiency: hit rate, shots fired, shots hit
- kill conversion, because kills influence credits and can improve placement in match mode
- Economy difference through part-change cost and remaining credits

### How to improve next run
- The primary recommendation card (see above)
- Up to two secondary recommendation cards when evidence is strong enough
- One visual target metric
- One benchmark to beat

---

## Benchmark Hierarchy

Each recommendation category needs a benchmark to compare against, and the right source of truth differs by category. Use this priority order:
- same player, same course, same heat number
- same player personal best run on the course
- current course-record best lap run
- current course-record best finish run
- winner or top performer in the same match
- top comparable cohort such as similar loadout class or cost bracket

Guidance:
- Time trial recommendations should prefer self-best and current course-record baselines.
- Match recommendations should prefer same-heat historical baselines and same-match top-performer baselines.
- Build and economy recommendations should prefer comparable cohorts and comparable part-change decisions, not absolute world-best runs.
- If the benchmark source is weak or unavailable, demote that category to secondary or suppress it.

---

## Post-Match Screen — Design Notes

**Success axis: circuit points, not just lap time.**

The match advice should not over-optimize for pace if a better recommendation is to focus on objectives, convert more kills, or make a different economy decision between heats. A player who finishes first every heat but ignores obelisks may still be losing circuit points to someone who reads the objective better.

Kills matter in match mode for three reasons:
- they contribute directly to circuit points
- they generate money for between-heat upgrades
- they can disrupt another player's placement and improve your own result indirectly

**Ascension is a recommendation cutoff for racing guidance.**

Once ascension starts, the player objective changes. The priority is no longer pure racing execution. It becomes surviving and reaching a point of interest on the map.

That means:
- racing recommendations should ignore racing telemetry after ascension starts
- post-ascension movement should not be used to explain corner speed, straightaway speed, warp usage, or similar race-phase guidance

Current gameplay rule:
- ascension starts when the first 3 racers finish their final lap

**Heat comparisons should be same-heat-index only.**

Heat 3 naturally has stronger parts because of earned credits. Do not compare heat 1 to heat 3. Compare heat 1 to the player's historical heat 1 results on the same course or ruleset. This is the honest comparison.

**The heat progression strip is context, not the focus.**

The per-heat loadout and outcome strip exists to show the arc of the match — how the player adapted (or didn't) between heats. It should not dominate the screen. It is supporting evidence.

**The match relative comparison answers "what are other players doing that I am not?"**

Side-by-side evidence against the top finisher is more useful than a generic rank delta. Show their loadout, their objective contribution, their lap time — not just that they placed higher.

---

## Time Trial Screen — Design Notes

**Success axis: finish time and lap time.**

Economy is absent in time trial. The player selects their build before the run. This makes the recommendation cleaner and more directly tied to execution and route.

**Time trial is the cleaner place to make segment-level recommendations.**

Without heat economy to complicate comparisons, the screen can lean harder on execution: where in the lap did the player lose time, how did their warp usage compare to a reference run, where did energy run out, and whether a part swap actually improved the tagged segment types it should help.

**The self-progress block shows trajectory, not just the last result.**

Show the last 3–5 attempts as a simple trend list — not a chart. This lets the player see whether they are improving consistently or bouncing around.

**Cost-bracket context is a clean fairness signal.**

The existing leaderboard variants (low-cost and high-cost rank) let the player understand whether they are slow because of execution or because of build cost. This is one of the clearest pieces of context the screen can offer without any new data.

---

## UI Handoff Notes

The UI designer should assume:
- the screen has one dominant recommendation area
- the dominant area may optionally include up to two smaller secondary cards
- recommendation categories are dynamic and will change from run to run
- recommendation cards need a consistent visual structure even when the category changes
- confidence and benchmark source may need a subtle visual treatment, especially for heuristic categories

The UI should not assume:
- every run has three equally strong recommendations
- every recommendation can name a precise segment on day one
- every build or economy recommendation is ready at the same level of certainty as crash or energy signals

---

## Appendix: Data Availability Reference

This section is for the engineering team, not for mock design decisions.

### What already exists

- `PlayerHeatStart` — loadout, loadout value, weight, weight class per heat
- `PlayerPartChange` — buy, sell, or swap action; part identity; part cost; credits after change
- `PlayerHeatEnd` and `PlayerMatchEnd` — placement, finish time, best lap, credits, circuit points, kills, deaths, crashes, obelisks
- `PlayerLap` and `PlayerCheckpoint` — time, warps, shots hit, shots fired, energy spent, time in air, average speed, stall time, active strafes, time out of energy
- `PlayerCheckpoint` segment tags for the next segment, including `corner`, `canyon`, `slotted`, and `shortcut`
- Career overview — per-course averages and personal bests for finish and lap time
- Leaderboards — course best finish and best lap, low-cost and high-cost variants

### What is partially available

- Previous-attempt comparison: raw events support it, but no dedicated summary endpoint exists yet
- Same-heat-number historical baseline: events support it, but no dedicated query view exists
- Segment-vs-best-run: raw checkpoint data exists, but best-run views do not preserve a run identity needed to retrieve the exact baseline run's checkpoint sequence
- Comparable part-change cohorts: possible now, but needs dedicated query shapes to compare similar swaps on the same course and heat index
- Open-area and straight classification: mostly implied by missing restrictive tags, so some recommendation types will still use derived grouping rather than explicit tags

### What is missing

- Run identity on best-finish and best-lap materialized views
- A derived summary that attributes post-change performance to recent part changes over the following heat or run

### Recommendation confidence rules

These rules should constrain both engineering and UI:
- A primary recommendation should only appear when the category has strong enough evidence to survive comparison against alternatives.
- A secondary recommendation can tolerate lower confidence, but it still needs a real benchmark and a real action implication.
- `Purchase timing` should only be primary when the observed buy or sell window and its payoff are stronger than the available pace, objective, or combat recommendations.
- `Engine or build class` should only be primary when part taxonomy and comparison cohorts are reliable.
- `Warp drive utilization`, `Corner speed`, `Slotted handling`, and `Canyon control` should show a heuristic or confidence state when the underlying segment grouping is derived rather than explicit.
- `Weapon spend payoff` should only be primary when the link between combat investment and kill or placement outcome is stronger than the available pace or objective recommendations.

### High-value additions if this becomes a full feature

- Heat-indexed historical summary view keyed by course, player, heat number, mode
- Run-comparison function returning outcome deltas, part-change deltas, loadout deltas, lap deltas, tagged segment deltas, checkpoint group deltas
- CP breakdown summary making placement, kill, and objective contribution explicit per heat
- Course segment metadata classifying track sections as straight, corner, jump-heavy, hazard-heavy
- A part taxonomy mapping that groups engines, warp drives, weapons, and handling parts into recommendation-ready cohorts

### Defer from v1

- Exact segment-by-segment compare against canonical best run (missing run identity on best-run views)
- Text-based coaching of any kind
