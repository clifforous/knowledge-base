# Eventun Post-Match Insights Next-Phase Ideation Notes

Status: Ideation notes for post-current implementation review
Date: 2026-07-03
Related solution design: `ascent-rivals/archive/initiatives/post-match-insights/eventun-post-match-insights-solution-design.md`
Related implementation plan: `ascent-rivals/archive/initiatives/post-match-insights/eventun-post-match-insights-implementation-plan.md`
Related progression design: `ascent-rivals/archive/initiatives/eventun-progression/eventun-medals-progression-goals-challenges-rewards-solution-design.md`

## Purpose

Capture post-current-phase insight ideas that are useful but should not distract the active
Eventun backend implementation. This document is not an implementation plan. It is a review
queue for the next design iteration.

## Current Feasibility Summary

| Idea | Current feasibility | Recommendation |
|---|---|---|
| Damage-done kudo | Needs new telemetry. Eventun does not currently expose damage done as an insight metric or heat/match summary field. | V2 candidate after adding aggregate damage dealt/taken telemetry. |
| Air/lift insight | Partially instrumented. Eventun has `timeInAirMs`, but not low-to-ground versus high-air distribution. | V2 candidate after adding distance-to-ground or lift-band aggregates. |
| Heat-specific insights | Contract already supports location heat/lap/checkpoint, but multi-heat narrative advice can become noisy. | Use sparingly. Do not build multi-heat narrative insights until UI/product value is proven. |
| Medal standout kudo | Medal heat counts exist. Medal importance/rank is missing from Eventun's medal definition API/model. | V2 candidate after adding medal kudo eligibility and importance metadata. |
| Course checkpoint graph export | Game client has rich checkpoint graph data, edge tags, distances, and inferred turn-angle tags. Backend analysis cost is non-trivial. | Prefer human-authored course-level insight weights first; export graph only if coarse weights are insufficient. |

## Damage-Done Kudo

Candidate insight:

- `damage_standout_kudo`

Player value:

- Praises combat contribution even when kills alone understate the player's impact.
- Helps avoid shallow combat coaching when the player had meaningful pressure but did not
  secure final blows.

Current state:

- Game code has damage-related combat callbacks and projectile damage values.
- Eventun insight metrics currently include kills, deaths, shots, combat mode time, and
  category scores, but not damage dealt or damage taken.
- Existing post-match and heat-end payloads do not appear to include aggregate damage done.

Likely implementation direction:

- Add aggregate combat telemetry at heat or match level:
  - `damageDealt`
  - `damageTaken`
  - optionally `damageDealtToPlayers`, `damageDealtToObjectives`, and `damageTakenFromPlayers`
- Add insight metric ids for damage dealt/taken.
- Generate `damage_standout_kudo` only when damage dealt is top or near-top in lobby, or
  materially above lobby average, with enough combat-enabled context.
- Suppress or reduce `combat_pressure_gap` when damage dealt is strong but kills are low.

Open questions:

- Should objective damage count, or only player damage?
- Does damage during non-combat phases matter?
- Should damage taken ever be a kudo, or only survivability/coaching context?

## Air/Lift Insights

Candidate insights:

- `air_lift_control_gap`
- `lowline_control_kudo`

Player value:

- Explains lift and hover control in a way that maps to Ascent Rivals' movement model. Lower
  to ground usually means more speed, but also more collision risk.

Current state:

- Segment telemetry includes `timeInAirMs` on lap/checkpoint events.
- Game control code can determine whether the ship is in midair and can query exact distance
  to ground.
- Current Eventun telemetry does not distinguish near-ground hover, high air time, jump time,
  or risky lowline time.

Likely implementation direction:

- Add compact segment aggregates rather than raw per-frame samples:
  - `timeNearGroundMs`
  - `timeMidLiftMs`
  - `timeHighAirMs`
  - optional `averageDistanceToGroundCm`
  - optional `lowlineSpeedTimeMs`
- Compare against course/segment context. A lowline insight only makes sense where the course
  geometry rewards it and the player also shows pace loss or crash risk.
- Keep broad `hover_speed_control_gap` disabled until those aggregates exist.

Open questions:

- Which height bands are stable across ship sizes and courses?
- Should thresholds be absolute centimeters, normalized by ship lift capability, or both?
- Should this ever appear as primary, or stay secondary unless very strong?

## Heat-Specific Insights

Candidate direction:

- Use existing `InsightLocation.heat` when a selected insight is clearly tied to one heat.
- Defer multi-heat narrative insights such as "Heat 1 you were slow on corners, but Heat 2
  you ignored shortcuts."

Current state:

- The insight response already supports heat, lap, checkpoint range, segment tags, and
  location key.
- Some current economy/loadout candidates already attach a heat number.
- The UI can format a single localized location if the client has copy for it.

Guidance:

- V1/current work may set `location.heat` for an otherwise normal insight.
- Do not add multi-heat comparison logic until there is a clear UI design and evidence that
  players benefit from the added specificity.
- If implemented later, prefer a single insight focused on one heat or one repeated pattern.
  Avoid returning three unrelated heat-specific diagnoses.

Open questions:

- Should heat-specific copy be visible in the card title, body, metric row, or location line?
- Does heat-specific advice help players in four-heat matches, or does it feel too granular
  after the match is already over?

## Medal Standout Kudos

Candidate insight:

- `medal_standout_kudo`

Player value:

- Uses already-authored gameplay recognition as positive post-match feedback.
- Can praise specialized play without inventing new backend semantics.

Current state:

- `PlayerHeatEnd.event_data.medalCounts` provides per-player heat medal counts.
- Eventun normalizes those facts through `server_player_medal_fact`.
- Game medal definitions include `ImpactWeight`, tags, display data, and category.
- Eventun `medal_definition` has `metadata`, but the public/admin medal definition model
  currently exposes only code, display name, description, kind, and status.

Likely implementation direction:

- Add medal metadata fields for insight use:
  - `kudoEligible`
  - `kudoPriority` or `impactWeight`
  - optional `kudoGroup`, such as combat, objective, piloting, comeback, or style
- Import or sync the game medal `ImpactWeight` into Eventun medal metadata, or author the
  Eventun kudo priority directly if that is easier to tune.
- Generate a kudo when the player has the most or near-most count for a high-priority medal
  in the lobby, or when they earn a rare/special medal.
- Avoid praising negative medals unless explicitly marked kudo-eligible.

Open questions:

- Should augment medals compete directly with primary medals?
- Should "most medals of type" be per heat or whole match?
- Should medal display/localization remain client-owned, with Eventun returning only medal
  code and kudo context?

## Course Checkpoint Graph Export

Candidate direction:

- Export course checkpoint graph data from the game client/editor into Eventun course tables
  so backend insights can understand map topology beyond run telemetry tags.

Current game-client facts:

- `AHGCheckpoint` owns next checkpoint links, previous checkpoint links, checkpoint ids,
  checkpoint type, linked spline, neighbor distances, and edge telemetry tags.
- `FHGCheckpointEdgeTags` stores authored tags and inferred tags per outgoing edge.
- Current course code defines edge tags such as `shortcut`, `straight`, `bend`, and `corner`.
- Current course code can infer edge tags from branch splines and total turn angle over an
  edge.

Possible Eventun shape:

- `course_checkpoint`
  - `course_code`
  - `course_version`
  - `checkpoint_id`
  - `checkpoint_name`
  - `checkpoint_type`
  - `sector_label_key` or display key if needed
  - optional position for diagnostics
- `course_checkpoint_edge`
  - `course_code`
  - `course_version`
  - `from_checkpoint_id`
  - `to_checkpoint_id`
  - `distance_cm`
  - `authored_tags`
  - `inferred_tags`
  - `turn_angle_deg`
  - `spline_name`
  - optional spline start/end distance

Potential backend uses:

- Understand whether a shortcut materially reduces path distance.
- Boost shortcut coaching only on maps where shortcut choice is strategically important.
- Distinguish mild bends from sharp corners when evaluating corner-speed gaps.
- Compare player segment choices against graph alternatives once path choice is reliably
  reconstructed.

Risks:

- Requires export tooling, schema, validation, versioning, and sync/reimport behavior.
- Backend analysis becomes more graph-oriented and can grow quickly.
- A precise graph may still need human judgment to decide whether shortcut usage should be
  recommended for a given map and build.
- Spline export provides richer geometry but increases payload size and analysis complexity.

Recommended next step:

- Start with human-authored course insight metadata on the Eventun course table:
  - `shortcutImportance`
  - `speedImportance`
  - `agilityImportance`
  - `combatImportance`
  - optional `shortcutDistanceImpact`, such as none, low, medium, high
  - optional `courseInsightNotes` for admin/debug context
- Use these authored weights the same way current Phase 7 uses course role weights: as
  confidence/salience modifiers, never as standalone insight facts.
- Revisit graph export only if the authored metadata fails to explain real map differences
  or if shortcut/path-choice insights become a major product direction.

Open questions:

- Should authored course insight metadata live in AccelByte `Courses`, Eventun-only course
  metadata, or both with one source of truth?
- If graph export happens, should it be editor-generated JSON, an AccelByte game record
  extension, or an Eventun admin import?
- How should Eventun detect that a graph belongs to the same course version as the submitted
  match events?

## Review Priority

Recommended ordering for next design work:

1. Human-authored course insight metadata, because it is low complexity and directly supports
   shortcut/build-shape salience.
2. Damage-done kudo, because it adds a strong positive combat insight once telemetry exists.
3. Medal standout kudo, because medal facts already exist but need kudo priority metadata.
4. Air/lift insights, because they need careful telemetry and tuning.
5. Full checkpoint graph export, only if coarse course metadata and segment telemetry are not
   enough.
