---
name: ascent-course-brief
description: Use when drafting or updating an Ascent Rivals course brief from a course prompt, course resolver output, Unreal MCP observations, dependency scan, optimization investigation, validation pass, or content/package hygiene pass.
---

# Ascent Course Brief

## Purpose
Create or update a concise course brief that turns course identity evidence into a reusable working note.

## References
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-brief.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-catalog.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/README.md`

## Workflow
1. Resolve course identity first. Use `ascent-course-resolver` when available.
2. Use `course-brief.md` as the target format.
3. Fill only fields supported by evidence.
4. Record aliases with classification, source, confidence, and notes.
5. Record level relationships separately from canonical course identity.
6. Record project-owned and vendor/import content roots separately.
7. List evidence collected with enough detail for another agent or developer to reproduce the finding.
8. Put weak or missing evidence in `Unresolved Questions`, not in facts.
9. End with the smallest useful next work slice.

## MCP-Unavailable Fallback
If MCP/editor property inspection is unavailable:
- state that no editor property reads or dirty package checks were possible
- if the brief depends on live editor evidence, ask the human whether to pause for MCP/editor availability or continue with provisional non-MCP evidence
- use source-controlled text directly when it is faster, cleaner, and more authoritative than MCP, such as C++ source, config, localization, and existing KB docs
- use filesystem, config, localization, source, package map lists, and binary asset string scans only as provisional evidence
- label candidate media assets, level paths, numeric fields, and exact property mappings according to evidence strength
- put fields needing editor confirmation in `Unresolved Questions`

## Course Catalog Updates
Update `course-catalog.md` only when the user asked to persist durable resolution facts or the task is explicitly a cataloging pass.

When updating the catalog:
- preserve exact asset paths
- include last verified date
- include verification method
- keep stale/prototype references separate from canonical identity
- do not add conversation-only notes

## Quality Bar
- Facts, assumptions, and unresolved questions must be separable.
- Do not infer numeric gameplay fields from binary `.uasset` string matches.
- Do not treat binary string order as proof that a path belongs to `Level`, `ThumbnailImage`, `HeroImage`, `MinimapImage`, or another exact property.
- Do not flatten aliases into one list without classification.
- Do not treat vendor/import roots as project-owned cleanup targets.
- Do not propose Unreal content mutation from the brief alone; produce a reviewable next slice.

## Output Shape
```text
Updated
- 

Not Updated
- 

Unresolved
- 

Recommended Next Work
- 
```
