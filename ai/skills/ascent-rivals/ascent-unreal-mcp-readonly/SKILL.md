---
name: ascent-unreal-mcp-readonly
description: Use when inspecting Ascent Rivals Unreal assets, maps, CourseDefinition assets, texture details, dependency roots, dirty package state, editor state, or Unreal MCP results without making content, code, Blueprint, material, map, or source-control changes.
---

# Ascent Unreal MCP Readonly

## Purpose
Use Unreal MCP as a read-only inspection channel for Ascent Rivals evidence gathering.

## References
- `../../../../30_designs/ascent-rivals/ai-assisted-unreal-improvement/README.md`

## Workspace Context
Unreal MCP availability is thread/workspace specific. Use this skill from an Ascent Rivals project thread where the `mcp__unreal_engine` tool namespace is exposed. A knowledge-base thread may maintain docs and skills without having live editor tools.

## Safety Rules
- Default to read-only inspection.
- Do not save packages, move assets, rename assets, delete assets, compile Blueprints, check out files, add files to source control, or change maps without explicit approval.
- If an MCP command might mutate state, stop and ask before running it.
- After editor inspection, check dirty content and map packages before claiming no mutation occurred.

## Preferred MCP Pattern
1. Check MCP/editor connection and enabled tool categories.
2. Use asset search for `CourseDefinition` assets, screenshots, minimaps, maps, materials, textures, and near-match aliases.
3. Use asset metadata to confirm primary asset type, primary asset name, native class, package path, and asset registry tags.
4. For `UHGCourseDefinition` and other custom data assets, prefer a small Unreal Editor Python helper through MCP that loads the asset and reads explicit editor properties.
5. For texture dimensions/settings, prefer an Unreal Editor Python helper through MCP when native texture inspection returns package-level data.
6. For dependency roots, query the Asset Registry with explicit dependency options and summarize by root with samples.
7. Avoid currently loaded-world object listing for content discovery; use it only when inspecting actors in the loaded world.

## Bounded Query Rules
- Prefer exact asset search, then near-exact alias search, then narrow package-path searches.
- Avoid repository-wide or `/Game`-wide property scans during smoke tests, forward tests, and course resolution.
- Do not load every course definition unless the user explicitly asked for a catalog-wide pass and the risk is acceptable.
- If a broad MCP/Python query times out, run at most one `manage_tools.get_status` recovery check. If that fails, stop MCP calls and report the remaining checks as unresolved.
- If `inspect_object` returns `Package` or generic package metadata for a custom data asset, do not treat it as authoritative. Switch to selected editor-property reads.

## Selected Property Helper Pattern
Use this pattern through `system_control.execute_python` for targeted data-asset reads. Keep the asset list and property list small.

```python
import unreal, json

def value(v):
    if v is None:
        return None
    if hasattr(v, "get_path_name"):
        return v.get_path_name()
    if isinstance(v, (list, tuple, set)):
        return [value(x) for x in v]
    if isinstance(v, dict):
        return {str(k): value(x) for k, x in v.items()}
    return str(v)

asset = unreal.EditorAssetLibrary.load_asset("/Game/Courses/Definitions/Example_CD")
props = ["code", "level", "thumbnail_image", "hero_image", "minimap_image", "planet", "name"]
print(json.dumps({p: value(asset.get_editor_property(p)) for p in props}, indent=2))
```

## MCP-Unavailable Fallback
If the editor appears to be running but no Unreal MCP tools are available in the current assistant environment:
1. Report `MCP/editor property inspection unavailable`.
2. If the request depends on live editor evidence, ask the human whether to pause for MCP/editor availability or continue with provisional non-MCP evidence.
3. Use source-controlled text directly when it is faster, cleaner, and more authoritative than MCP, such as C++ source, config, localization, or KB docs.
4. Do not infer absence of assets, dependencies, texture settings, or dirty packages.
5. Limit fallback findings to source, config, localization, package map lists, filesystem paths, source-control status, and binary string-table hints.
6. Mark exact `UObject` property values, dependency graph details, texture settings, and dirty package state as unresolved.
7. Separate evidence levels: `confirmed by editor/MCP`, `corroborated by source-controlled text`, and `hinted by binary string scan`.
8. Recommend the smallest read-only MCP/editor property query needed next.

## Data Asset Fields
For course identity, read these fields when relevant:
- `Code`
- `StatCode`
- `Level`
- `ThumbnailImage`
- `HeroImage`
- `MinimapImage`
- `Planet`
- `Name`
- `FeatureState`
- `bInternalOnly`
- `Difficulty`
- `Laps`
- `TargetLapTime`
- `MaxAscensionZones`

## Evidence Rules
- Report the exact asset path inspected.
- Separate facts from assumptions.
- Treat empty or suspicious native MCP results as inconclusive, not proof of absence.
- Mark fields unresolved when they cannot be read authoritatively.
- Include whether editor packages were dirty after inspection.
- Do not require repository-local Python scripts or system Python. Any Python mentioned here means Unreal Editor Python executed through MCP.
- Treat binary `.uasset` or `.umap` strings as provisional. String order does not prove field ownership.

## Output Shape
```text
Facts
- 

MCP/Editor Evidence
- 

Assumptions
- 

Unresolved Questions
- 

Dirty Package Check
- 
```
