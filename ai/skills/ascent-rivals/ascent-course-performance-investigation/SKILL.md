---
name: ascent-course-performance-investigation
description: Use when investigating Ascent Rivals course or map performance, render cost, frame pacing, GPU/render-thread/game-thread bottlenecks, streaming, memory pressure, shader complexity, texture cost, VFX cost, or course-specific runtime performance before proposing optimizations.
---

# Ascent Course Performance Investigation

## Purpose
Investigate one Ascent Rivals course performance concern in a bounded, evidence-first pass.

This skill is for analysis and proposal. Do not change assets, maps, materials, Blueprints, code, or source control state unless the human approves a separate mutation slice.

## References
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/README.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-catalog.md`
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/course-brief.md`

## Required Sub-Skills
- Use `ascent-course-resolver` first when course identity is not already resolved.
- Use `ascent-unreal-mcp-readonly` for live editor/MCP evidence when available and useful.

## Workflow
1. Resolve course identity and confirm the target level.
2. State the performance question and gameplay scenario: platform, resolution, scalability, camera/view, player count, route section, and symptom if known.
3. Gather the smallest useful baseline evidence.
4. Classify the likely bottleneck before proposing fixes.
5. Identify high-value suspects and separate confirmed costs from hypotheses.
6. Recommend a small next slice with expected benefit, risk, and verification method.

## Evidence Priority
- Use source-controlled text directly when it is the better authority, such as C++ source, config, existing profiling notes, and KB docs.
- Use MCP/editor evidence for asset properties, level state, texture settings, material references, dependency roots, and dirty package state.
- Use runtime profiling evidence for actual performance claims: Unreal Insights, `stat unit`, `stat gpu`, `profilegpu`, logs, captures, or reproducible editor/standalone observations.
- If MCP/editor evidence is unavailable and the task depends on it, ask whether to pause for MCP/editor availability or continue with provisional non-MCP evidence.
- Prefer source-controlled text over MCP when it is faster, cleaner, and more authoritative for the specific question.

## Bottleneck Classification
Classify the issue as one or more of:
- game thread
- render thread
- RHI thread
- GPU
- asset loading or streaming
- memory pressure
- shader compilation or PSO stutter
- network or dedicated server cost
- UI/Slate cost
- unknown due to insufficient evidence

Do not present texture downsizing, material simplification, LOD work, VFX reductions, or code changes as root-cause fixes until evidence supports that category.

## Bounded MCP Rules
- Start with exact course definition and level asset queries.
- Prefer selected property reads over broad asset scans.
- Avoid all-course, all-map, or `/Game`-wide scans during a course investigation.
- If an MCP query times out, run at most one status retry. If it fails, stop MCP calls and report unresolved editor checks.
- Do not claim a dirty package check unless editor tooling reported it.

## Common Signals
Treat these as investigation signals, not automatic failures:
- 4k or larger textures referenced by the course
- no mip strategy, inappropriate texture group, or unusual compression
- expensive materials in large screen-space areas
- high shader complexity or heavy translucent overdraw in racing sightlines
- high triangle or instance counts without LOD strategy
- heavy Niagara, fog, water, landscape, RVT, sky, or volumetric features
- unexpected hard references into unrelated gameplay/UI/vendor roots
- streaming hitches or memory spikes around a specific course section

## Output Shape
```text
Facts
- 

Assumptions
- 

Evidence Collected
- 

Bottleneck Classification
- 

Suspects
- 

Unresolved Questions
- 

Recommended Next Work
- 
```
