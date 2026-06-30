---
name: ascent-course-content-hygiene
description: Use when reviewing Ascent Rivals course or map content organization, package hygiene, aliases, stale config/media references, project-owned versus vendor asset roots, texture/material locality, dependency roots, safe asset moves, or cleanup recommendations.
---

# Ascent Course Content Hygiene

## Purpose
Review one Ascent Rivals course for content/package hygiene risks and propose small, reviewable cleanup slices.

This skill does not authorize mutation. Do not move, rename, delete, save, check out, or fix redirectors unless the human approves a separate implementation slice.

## References
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/README.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-catalog.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-brief.md`

## Required Sub-Skills
- Use `ascent-course-resolver` first when course identity is not already resolved.
- Use `ascent-unreal-mcp-readonly` for live editor/MCP evidence when available and useful.

## Workflow
1. Resolve course identity and check the course catalog.
2. Identify canonical course definition, canonical level, media assets, aliases, and level relationships.
3. Separate project-owned roots from vendor/import/plugin/Wwise roots.
4. Identify stale, prototype, confusing, or conflicting references.
5. Inspect dependency roots narrowly; avoid broad `/Game` scans.
6. Identify hygiene findings by risk and blast radius.
7. Recommend small cleanup slices with exact approval boundaries.

## Evidence Priority
- Use source-controlled text directly when it is faster, cleaner, and more authoritative than MCP, such as config, localization, C++ source, and existing KB docs.
- Use MCP/editor evidence for asset registry identity, property reads, dependency roots, texture settings, and dirty package state.
- If MCP/editor evidence is unavailable and the hygiene question depends on it, ask whether to pause for MCP/editor availability or continue with provisional non-MCP evidence.

## Hygiene Signals
Look for:
- course definition, level path, media, and config disagreements
- player-facing name differs from internal level or folder names
- typo-bearing canonical assets that must be preserved exactly
- stale localization or legacy config references
- developer/prototype content that resembles production content
- course-specific project-owned assets outside an obvious course/domain root
- project-owned material instances, textures, meshes, Blueprints, or VFX with unclear ownership
- course assets hard-referencing unrelated systems
- 4k or oversized textures where the course use does not justify them
- old screenshots, thumbnails, minimaps, or presentation assets not used by current course definitions

## Vendor And Shared Content
- Vendor/import/plugin/Wwise roots are exempt from locality cleanup by default.
- Prefer project-owned wrappers, material instances, data assets, or documentation over moving vendor assets.
- Do not rename or move shared master materials, shared meshes, shared VFX, or shared UI assets from a single-course hygiene pass.
- Do not delete assets based only on an unused-assets scan.

## Recommended Actions
Allowed as recommendations:
- document alias relationships in the course catalog
- document stale config/media/localization refs
- propose project-owned course folders for future migration
- propose moving narrowly scoped project-owned orphan assets after dependency review
- propose redirector cleanup after approved moves
- propose validation rules for repeated problems
- propose explicit vendor-root exceptions

Not allowed without explicit approval:
- moving assets
- renaming assets
- deleting assets
- saving packages
- checking out or adding files in source control
- fixing redirectors
- changing packaging/cook rules
- changing shared master materials or shared content

## Bounded MCP Rules
- Start with exact course definition, exact level, exact media, and narrow alias searches.
- Use selected property reads and dependency-root summaries.
- Avoid broad all-course or `/Game` scans unless the task is explicitly catalog-wide.
- If MCP transport fails after a timeout, stop after one status retry and report unresolved editor checks.

## Output Shape
```text
Facts
- 

Assumptions
- 

Hygiene Findings
- 

Vendor/Shared Content Exceptions
- 

Unresolved Questions
- 

Recommended Cleanup Slices
- 
```

