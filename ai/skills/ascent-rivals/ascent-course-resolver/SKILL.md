---
name: ascent-course-resolver
description: Use when an Ascent Rivals request names a course, map, level, course code, screenshot, minimap, old alias, internal Unreal asset path, sublevel, or derived map and the canonical playable course identity must be resolved before analysis or changes.
---

# Ascent Course Resolver

## Purpose
Resolve a human course prompt into canonical Ascent Rivals course facts before optimization, validation, hygiene, or content changes.

## References
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/README.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-catalog.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-brief.md`

## Workflow
1. Check `course-catalog.md` first.
2. If the course is present, use it as a reviewed cache and spot-check current `UHGCourseDefinition` and level references before proposing changes.
3. If missing, stale, ambiguous, or structurally changed, re-resolve from `CourseDefinition` primary assets.
4. Match prompt terms against course code, planet, display name, full display name, level path, media asset names, localization source paths, and known aliases.
5. Classify aliases as `canonical`, `corroborating`, `stale`, `prototype`, or `unresolved`.
6. Record level relationships: canonical map, streaming sublevels, world partition/external actor notes, derived map variants, and related course definitions.
7. Identify presentation assets: thumbnail, hero image, and minimap.
8. Identify project-owned course roots and vendor/import roots.
9. Output facts, assumptions, unresolved questions, and recommended next work.

## MCP-Unavailable Fallback
If Unreal MCP/editor property access is unavailable:
- state that limitation explicitly
- if the request depends on live editor evidence, ask the human whether to pause for MCP/editor availability or continue with provisional non-MCP evidence
- use source-controlled text directly when it is faster, cleaner, and more authoritative than MCP, such as C++ source, config, localization, and existing KB docs
- use config, source, localization, package map lists, filesystem paths, and binary string-table scans only as provisional evidence
- mark editor-owned properties unresolved when exact property mapping matters
- do not infer absence of assets from unavailable MCP results
- do not claim a dirty package check was completed

## Authority Order
- Current `UHGCourseDefinition` primary asset fields are canonical.
- Current map actor references, package map lists, localization paths, screenshots, minimaps, and source references are corroborating unless they conflict with the course definition.
- Legacy config, stale localization, missing assets, and `/Game/Developers/**` content are not canonical unless current course definitions point there.

## Rules
- Preserve exact Unreal package paths, including typo-bearing asset names.
- Normalize player-facing names only from current course definition fields, localization, or approved design notes.
- Treat internal map names and sublevels as aliases or relationships, not as canonical course identity by themselves.
- Treat binary `.uasset` string matches as hints. They may support candidate object paths, text values, enum names, and dependency roots, but they do not prove exact property ownership.
- Use editor/MCP property reads for numeric gameplay fields and exact property mappings, or mark them unresolved.
- Treat planet/code naming mismatches as identity findings, not automatic errors. For example, a current course definition may have player-facing `Planet`/`Name` fields that differ from an older code prefix; record both and ask whether the code should remain stable.
- Keep MCP work bounded: exact course-definition search first, then exact map/media searches, then narrow alias searches. Avoid broad all-course property scans unless the task is explicitly catalog-wide.
- Do not mutate Unreal content, source control state, or KB catalog entries unless the user requested persistence.

## Output Shape
```text
Facts
- 

Assumptions
- 

Unresolved Questions
- 

Recommended Next Work
- 
```
