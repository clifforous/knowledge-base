# Course Brief

## Purpose
Resolve a human course prompt into concrete Ascent Rivals project facts before analysis, optimization, validation, or content hygiene work begins.

Use this format when a request names a course by display name, planet, code, internal level name, old prototype name, screenshot label, or ambiguous alias.

For valid playable courses, start from `CourseDefinition` primary assets. Use legacy config, registry entries, primary asset settings, durable notes, and content search to cross-check or fill gaps.

## Course Identity
- Planet:
- Display name:
- Course code:
- Feature state:
- Difficulty:
- Supported modes:

## Asset Identity
- Level asset path:
- Course definition primary asset:
- Legacy config or registry entry:
- Thumbnail asset:
- Hero image asset:
- Minimap asset:

## Level Relationships
- Persistent or canonical map:
- Streaming sublevels:
- World partition or external actor notes:
- Derived map variants:
- Other course definitions that reference related maps:

## Known Aliases
Record every name that appears to refer to the same course.

| Alias | Classification | Source | Confidence | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

Alias sources may include human prompt text, course definitions, config entries, level asset names, screenshots, minimaps, old design notes, or editor labels.

Classifications:
- `canonical`: current course definition primary asset identity or fields
- `corroborating`: current references that support the canonical identity
- `stale`: legacy or superseded references that should not override the course definition
- `prototype`: developer, whitebox, or experiment content that shares a name or theme
- `unresolved`: candidate alias that needs more evidence

## Content Roots
Project-owned roots directly associated with this course:
- 

Vendor, Marketplace, Fab, Megascans, plugin, Wwise, or other third-party roots referenced by the course:
- 

## Current Structure Notes
Describe how the current folder layout maps to course identity.

Examples of issues to capture:
- course lives in an internal environment folder rather than a planet/course folder
- canonical asset path contains a typo that must be preserved exactly in Unreal references
- screenshots or minimaps are centralized instead of colocated
- course-specific material instances live outside the course root
- old prototype names remain in level, sublevel, or asset names

## Relevant Systems
- Course registry:
- Asset Manager primary asset type:
- Cook labels or packaging rules:
- Level streaming, sublevels, or derived maps:
- Race/checkpoint/lap flow assets:
- Bot, spectator, or lobby requirements:

## Evidence Collected
List the evidence used to resolve the course.

- 

Do not infer numeric gameplay fields from binary asset string matches. Use editor/MCP property inspection, source-controlled text data, or mark the field unresolved.

If MCP/editor property inspection is unavailable, label binary asset string evidence as provisional. It may support candidate paths, text, enum names, and related roots, but it does not prove exact property ownership or dirty package state.

## Unresolved Questions
List questions that must be answered before safe mutation.

- 

## Recommended Next Work
State the smallest useful next slice.

- 
