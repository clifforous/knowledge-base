# AI-Assisted Unreal Improvement Workflows

## Status
Draft standard for Ascent Rivals Unreal project improvement work.

This document is authored in the personal knowledge base as a portable draft. It is not yet the shared team source of truth. If it proves useful, move or adapt it into the Unreal project documentation without carrying over local machine paths or knowledge-base-specific assumptions.

## Purpose
Define a human-reviewed, AI-assisted workflow for improving the Unreal game project in small, verifiable passes.

The first fully specified workflow is the **course/map improvement pass**. Other target areas are included as lightweight shells so future standards and skills can use the same operating model.

## Portable Packet
This folder is the portable AI-assisted improvement packet. Keep the workflow standard, working formats, and durable course catalog together so the folder can later move into the Ascent Rivals project without reconstructing cross-repository links.

Current documents:
- [Course Brief](course-brief.md)
- [Course Catalog](course-catalog.md)

Repository-local draft skills currently live under `ai/skills/ascent-rivals/`. If this packet moves into the game project, move those skills with it or adapt them into the target AI tooling location.

## Goals
- Route vague human prompts into concrete work targets and pass types.
- Keep AI work bounded to small slices that can be reviewed before mutation.
- Improve course performance, visual quality, level validity, naming clarity, and content/package hygiene together when they affect the same target.
- Preserve project-owned design intent while reducing avoidable technical cost.
- Build standards that humans can review and AI agents can execute without inventing process.

## Non-Goals
- Do not ask an agent to "make the game faster" or "fix the project structure" as a single implementation task.
- Do not mass-move Marketplace, Fab, Megascans, Wwise, plugin, or other vendor content without explicit higher-level approval.
- Do not treat one visual diagnostic value as a universal budget. For example, Unreal's shader complexity view is useful, but its color scale depends on instruction-count configuration and does not alone prove runtime cost.
- Do not optimize by visibly degrading course identity, player readability, or gameplay clarity.
- Do not delete assets only because an automated scan cannot prove they are used.

## Core Concepts

### Target Brief
A Target Brief is the resolved thing being investigated or improved.

The brief starts from the human prompt and is normalized into concrete project facts before changes are proposed. The brief should include known aliases and unresolved identity questions.

Examples:
- `fix the lava material on Dunes 7` should resolve to a course target plus a material concern.
- `the ship camera swings too far out` should resolve to a player-view or camera-behavior target, not a performance pass.
- `clean up Alluvial Basin assets` should resolve to a course target plus a content/package hygiene pass.

### Pass Type
A Pass Type is the kind of work being performed against the target.

Initial pass types:
- analysis only
- performance investigation
- performance optimization
- content/package hygiene
- level validation
- visual readability
- code or Blueprint simplification
- audio investigation
- server runtime investigation

One pass may include secondary hygiene work when it directly affects the target. For example, a course performance pass may identify an oversized lava texture, a confusing material instance location, and a level alias mismatch in the same review packet.

## Prompt Routing
Every AI-assisted pass starts by routing the request:

```text
human prompt
-> resolve Target Brief
-> classify Pass Type
-> gather evidence
-> propose a small slice
-> human approval
-> apply changes
-> verify
-> summarize results and remaining risks
```

Routing examples:

| Prompt | Target Brief | Pass Type |
|---|---|---|
| `Why is Tefri 7 - Dunes slow?` | Course target | performance investigation |
| `Fix my lava material on Dunes 7` | Course target plus material concern | visual/material analysis or performance pass, depending on symptoms |
| `Clean up assets for Alluvial Basin` | Course target | content/package hygiene |
| `The ship camera is swinging too far out` | Player-view/camera target | gameplay/camera analysis |
| `The HUD is hard to read during combat` | UI/HUD target | visual readability |
| `Dedicated server tick is spiking in races` | Server runtime target | server runtime investigation |

If the target cannot be safely resolved, the agent asks a targeted clarification before proposing changes.

## Review Gates

### 1. Target Resolution Gate
The agent must identify the real level, asset, Blueprint, subsystem, or data asset before making claims.

For a course, this includes:
- planet
- display name
- course code
- level asset path
- course definition primary asset
- legacy config or registry entry, if still present
- known aliases, old names, and alias classifications
- related content roots
- likely vendor-content roots

### 2. Evidence Gate
The agent gathers enough evidence to distinguish facts from assumptions.

Acceptable evidence includes:
- Knowledge-base notes and design docs
- Unreal project config and course registry entries
- Asset Manager and Asset Registry results
- Unreal MCP/editor observations
- screenshots or viewport captures
- Reference Viewer, Size Map, dependency, or cook information
- Unreal Insights traces, `stat` captures, GPU captures, logs, or command output
- source code or Blueprint structure relevant to the target

### 3. Proposal Gate
Before mutation, the agent produces a short review packet:

```text
Target Brief
- resolved target
- aliases found
- unresolved identity questions

Evidence
- files/assets inspected
- editor observations
- screenshots/captures/logs/profiles
- dependency findings

Proposed Slice
- 1-5 focused changes
- expected benefit
- risk
- verification method

Approval Request
- exact changes the agent wants permission to make
```

### 4. Approval Gate
The human approves the slice before the agent changes content, code, Blueprints, materials, maps, validation rules, or source-control state.

Read-only inspection does not require approval unless the requested tooling is unusually expensive or invasive.

### 5. Verification Gate
The agent reruns the relevant checks after changes and compares before/after evidence. If verification cannot be run, the summary must say why.

### 6. Knowledge Gate
Durable discoveries should be recorded where they can be reused.

Examples:
- course display name to level-path aliases
- course code changes
- vendor-content exceptions
- material or VFX budget decisions
- validation rules added or deferred
- unresolved questions that blocked safe mutation

## Course/Map Improvement Pass

### Scope
Use this workflow to improve one playable course or map in a bounded pass.

The pass may include:
- render performance
- visual readability
- level playability requirements
- naming and identity cleanup
- content/package hygiene
- project-owned asset locality
- course-specific code or Blueprint simplification
- validation rules that protect the same course or content pattern

### Required Course Brief
A resolved course brief should contain:

```text
Course Brief
- planet
- display_name
- course_code
- level_asset_path
- course_definition_primary_asset
- legacy_config_or_registry_entry
- known_aliases
- alias_classifications
- level_relationships
- screenshots_or_reference_captures
- related_content_roots
- vendor_content_exceptions
- known_performance_or_hygiene_notes
```

The alias field is required. Course prompts often use names that differ from the internal level asset. A prompt like `Tefri 7 - Dunes`, `Dunes 7`, `DesertTest_0`, or `Illus - Alluvial Basin` must resolve to the same course facts before the agent acts.

Aliases are not all equally authoritative. Classify each alias or near match as canonical, corroborating, stale, prototype, or unresolved so a current course definition is not confused with an old config entry, localization remnant, developer prototype, or map package name.

For production-facing courses, `ThumbnailImage`, `HeroImage`, and `MinimapImage` should be treated as required presentation assets unless product direction says otherwise. If any of those fields are missing, stale, or still pointing at legacy config-era assets, flag that as a course identity or presentation hygiene finding.

### Course Resolution Procedure
1. Inspect `CourseDefinition` primary assets first. A valid playable course should be discoverable as a `UHGCourseDefinition` primary data asset.
2. Match the human prompt against course code, planet, display name, level path, and known aliases from the course definition assets.
3. Use legacy Unreal course settings, registry entries, primary asset settings, and durable notes to cross-check or fill missing fields.
4. Resolve the level asset path and the course definition asset that owns gameplay metadata.
5. Inspect level relationships for the resolved level: streaming sublevels, world partition/external actor structure, related map variants, reverse/reflection/night/event copies, and maps that appear to derive from or depend on the canonical course level.
6. Search for folders and assets that appear course-specific.
7. Identify vendor-content roots referenced by the course.
8. Ask for clarification if no matching valid course definition exists, multiple course definitions match, or the prompt uses an alias that cannot be verified.

Level relationship discovery belongs in the course resolver, not in a separate first-priority skill. The resolver should report these relationships so later performance, validation, and hygiene passes know whether they are working on the base course, a sublevel, or a derived course variant.

### Alias Classification
Course identity work should classify every alias and near match by source quality.

Use these classifications:
- `canonical`: current `CourseDefinition` primary asset identity and fields, including `Code`, `Planet`, `Name`, and the current `Level` reference
- `corroborating`: current map actor references, localization source paths, screenshot or minimap names, cook/package map lists, or UI/source references that support the canonical identity
- `stale`: legacy config rows, localization entries, screenshots, minimaps, or asset paths that refer to missing, renamed, or superseded course definitions or levels
- `prototype`: `/Game/Developers/**`, whitebox, AlphaCourses, experiment, or other non-production content that shares a name or theme with the course
- `unresolved`: human prompt text or asset matches that cannot yet be tied to a current valid course definition

Rules:
- Preserve exact Unreal package and asset names in evidence, even when they contain typos or old naming. Do not silently "correct" a package path in documentation or proposed work.
- Normalize player-facing names only when the current course definition, localization source, or approved design note supports the normalized name.
- Treat internal level names as aliases until the course definition confirms the level reference. A map package can be the backing level without being the canonical course identity.
- Treat sublevels and derived map variants as relationships to document, not as proof of canonical course identity. A sublevel may be shared implementation detail; a derived map may have its own course definition.
- Treat localization as supporting evidence for display text and historical aliases, not as proof that the referenced asset still exists.
- Treat binary `.uasset` string matches as useful hints, not as complete property reads. Numeric fields such as laps, target times, difficulty, and feature state should come from editor inspection, Unreal MCP Python helpers, source-controlled text data, or be marked unresolved.
- Treat binary `.uasset` string matches for object paths, text values, and enum names as provisional evidence unless editor property inspection confirms the property mapping. String order in a package does not prove which field owns a value.

### Unreal MCP Notes For Course Identity
For course identity work, prefer this MCP pattern:
- use native asset search early to find `CourseDefinition` assets, screenshots, minimaps, and near-match aliases
- use asset metadata to confirm primary asset type, primary asset name, native class, and package identity
- use a small Unreal Editor Python helper through MCP for authoritative `UHGCourseDefinition` fields such as `Code`, `Level`, `ThumbnailImage`, `HeroImage`, `MinimapImage`, `Planet`, `Name`, `FeatureState`, `Difficulty`, `Laps`, and target times
- use Unreal Editor Python Asset Registry dependency queries through MCP with explicit dependency options when native dependency helpers return empty or suspiciously shallow results
- avoid currently loaded-world object listing for asset discovery; it is useful for world actors, not content registry search
- after read-only editor inspection, check dirty content and map packages before claiming no mutation occurred

These Python references are Unreal Editor/MCP execution paths, not requirements for developers to install system Python or for repository-local skills to ship code.

Unreal MCP availability is thread/workspace specific. Live MCP-backed tests should run from an Ascent Rivals project thread where the `mcp__unreal_engine` tool namespace is exposed. Knowledge-base threads can maintain these docs and skills, but should not be assumed to have editor access.

Keep MCP queries bounded. Prefer exact asset searches, near-exact alias searches, and selected property reads over broad `/Game` scans or loading every course definition. A broad scan that times out can destabilize the MCP transport and prevent a dirty-package check.

If MCP transport fails after a timeout, run at most one status retry. If the retry fails, stop MCP calls, report the transport failure, and mark any remaining editor checks unresolved.

If `inspect_object` returns a package or generic metadata for a custom data asset, do not treat it as an authoritative property read. Use the Unreal Editor Python property helper path instead.

### MCP-Unavailable Fallback
If the Unreal editor is running but MCP tools are not exposed to the current agent session:
1. State that MCP/editor property inspection is unavailable.
2. If the requested task depends on live editor evidence, ask the human whether to pause for MCP/editor availability or continue with provisional non-MCP evidence.
3. Use source-controlled text directly when it is faster, cleaner, and more authoritative than MCP, such as C++ source, config, localization files, or existing KB docs.
4. Use source, config, localization, package lists, filesystem paths, and binary string-table scans only as provisional evidence for Unreal asset properties that normally require editor reads.
5. Do not infer absence of assets from missing MCP results.
6. Mark editor-owned properties unresolved when they require property reads, dependency queries, texture settings, or dirty package state.
7. Distinguish `confirmed by editor/MCP`, `corroborated by source-controlled text`, and `hinted by binary string scan` in the evidence summary.
8. Do not claim a dirty package check was completed unless editor tooling actually reported dirty packages.

### Baseline Evidence
For a course pass, gather only the evidence needed for the requested slice.

Common baseline checks:
- level opens successfully in the editor
- course registry entry points to the resolved level
- map check or equivalent level validation output
- lit viewport screenshot for visual reference
- shader complexity or material complexity captures when material cost is in scope
- `stat unit`, `stat gpu`, `profilegpu`, or Unreal Insights evidence when runtime performance is in scope
- texture size and texture group scan for course-referenced textures
- material and material-instance scan for course-referenced materials
- static mesh, skeletal mesh, Niagara, and particle dependency scan when relevant
- Reference Viewer or Size Map evidence for unexpected dependencies
- cook/package ownership evidence when package hygiene is in scope

### Performance Investigation
The first performance pass should identify the dominant constraint before proposing fixes.

Classify the problem as one or more of:
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

Do not propose texture downsizing, material simplification, LOD work, VFX changes, or code changes as root-cause fixes until the evidence supports that category.

### Render And Content Signals
Use these as signals, not automatic failures:
- 4k or larger textures referenced by the course
- textures with inappropriate texture groups, compression settings, or no mip strategy
- high shader complexity in large screen-space areas
- many translucent or overdraw-heavy effects in racing sightlines
- expensive materials on frequently visible surfaces
- high instance counts or high triangle count meshes without appropriate LOD strategy
- runtime virtual texture, landscape, water, sky, volumetric, or fog cost that affects frame pacing
- repeated references to heavy vendor assets through small course-specific objects
- unexpected hard references from course content into unrelated game areas

Any numeric budget must state its target context, such as platform, scalability level, resolution, camera view, and gameplay scenario.

### Content/Package Hygiene
Prefer existing project domain patterns over a new universal folder scheme.

Observed project-owned patterns:
- course definitions live under `Courses/Definitions`
- course presentation assets are centralized under `Courses/Screenshots` and `Courses/Minimaps`
- course levels currently live under map-family or environment folders such as `Courses/Desert`, `Courses/Volcanic`, `Courses/WetDarkRock`, `Courses/Beach`, and `Courses/Sky`
- ship parts use `Ship/Parts/<slot>/<weight-class>/<part-id>` where practical
- part-specific runtime assets commonly colocate `*_BP`, `*_MIN_BP`, and `*_SPD` assets with the part
- weapons commonly use `Weapons/<weapon-name>` for weapon definitions, Blueprints, skins, VFX, widgets, and textures
- UI content is grouped by UI role under `UserInterface/Routes`, `UserInterface/Widgets`, `UserInterface/Textures`, `UserInterface/Materials`, and related support folders
- runtime and build-support roots such as `CookLabels`, `PreloadedItems`, `Perf`, `Generated`, and `DataTable` have special ownership and should not be treated as ordinary feature folders

The strongest divergence from the preferred long-term model is course layout. Current course level folders are often internal environment or prototype names rather than canonical player-facing course identity. A future course layout may be better expressed as:

```text
Courses/<Planet>/<Course>/
- Level
- Course definition or local metadata
- Course-specific material instances
- Course-specific textures
- Course-specific meshes or Blueprint wrappers
- Course-specific VFX instances
```

Screenshots, thumbnails, and minimaps may remain centralized if that continues to fit player-facing presentation workflows. The guide should not force course media into per-course folders until the team chooses a presentation-asset convention.

Treat this as a migration direction, not a requirement for immediate broad restructuring. Course pass agents should document alias mismatches and propose small safe moves only when the current layout blocks the pass.

Vendor content should usually stay in its original vendor root. When a course uses vendor content, prefer project-owned wrappers, material instances, or data assets that reference vendor assets rather than moving the vendor assets themselves.

Allowed hygiene recommendations:
- document or add aliases for confusing level names
- create or update a course identity note
- propose a canonical course folder only after resolving course identity and dependencies
- move project-owned orphaned course assets into a course-owned root after dependency review
- replace broad hard references with narrower course-owned references
- consolidate duplicate material instances when dependency review shows they are equivalent
- add validation rules for repeated naming, size, or dependency issues
- fix redirectors after approved asset moves

Not allowed without explicit broader approval:
- moving vendor roots
- mass-migrating current course folders into `Courses/<Planet>/<Course>` as part of a single course pass
- renaming widely shared assets used by multiple courses
- deleting assets based only on a single automated unused-assets scan
- changing shared master materials without reviewing all dependent instances
- changing packaging rules for unrelated game areas

### Level Validation
A playable course should eventually have explicit validation criteria.

V1 validation should check for:
- course registry and display metadata consistency
- level asset exists and opens
- required gameplay actors and course flow objects are present
- player, spectator, and bot entry points are valid for supported modes
- checkpoint/lap/race flow data is internally consistent
- no required runtime asset is editor-only or in a never-cook root
- no development-only content remains in production course paths
- screenshots/thumbnails exist for player-facing course presentation when required
- map check has no pass-blocking errors

The exact actor and data requirements should be refined from the current Ascent Rivals race/course implementation before these checks become hard validators.

### Course Media Tooling
Course media appears to have at least two relevant tooling paths:
- `AHGCourse::CaptureMinimapImage` is an editor-callable course method for generating a minimap image from course splines.
- `UHGThumbnailGeneratorWidget` and the `ThumbnailGenerator` content map support primary-data-asset thumbnail capture and assignment.

Do not assume those tools fully cover course thumbnail, hero image, and minimap workflows until a focused media-generation pass verifies the intended usage. A course media pass should inspect existing tools first, then propose whether to reuse, extend, or replace them.

### Course Pass Output
A completed pass should end with:
- changes made
- evidence before and after
- verification commands or editor checks run
- remaining risks
- next recommended slice
- knowledge updates made or recommended

## Other Target Brief Shells

### Player View Target
Use for driver-visible ship, cockpit, camera, boost, weapon, first-person particles, and near-camera readability.

Common pass types:
- visual readability
- camera behavior analysis
- render performance
- VFX/material cleanup
- input or gameplay feel analysis

Required evidence should include camera context, screenshots/video when possible, relevant ship/camera assets, and affected gameplay states.

### External Ship View Target
Use for third-person, spectator, and other-racer ship visuals.

Common pass types:
- silhouette/readability
- replicated VFX performance
- spectator clarity
- LOD and material review

Required evidence should include observer distance bands, multiplayer/spectator context, and whether the effect is locally predicted, replicated, or cosmetic only.

### UI Target
Use for HUD, in-race overlays, menus, hangar, match summary, and other UMG/CommonUI surfaces.

Common pass types:
- visual readability
- layout consistency
- Slate/UMG performance
- asset reference cleanup
- code or Blueprint simplification

Required evidence should include route/widget identity, screenshots, viewport size, input mode, and relevant user flow.

### Server Runtime Target
Use for dedicated server performance, gameplay subsystem cost, SnapNet/rollback cost, session flow, and server logs.

Common pass types:
- performance investigation
- code simplification
- log/debug analysis
- subsystem boundary review

Required evidence should include logs, server scenario, player/bot count, tick or trace evidence, and affected subsystem boundaries.

### Audio Target
Use for Wwise events, spatial audio, mix, memory, streaming, concurrency, and course-specific soundscape issues.

This target needs domain research before hard standards are written. Until then, audio passes should be analysis-first and should avoid broad automated changes.

### System Target
Use for cross-cutting gameplay/client systems that are not tied to one course, UI route, or ship view.

Common pass types:
- code organization
- API or data-model cleanup
- performance investigation
- validation rule design

The pass must define the system boundary before proposing changes.

## AI Agent Operating Rules
- Start with target resolution; do not optimize an unidentified asset.
- Keep each pass small enough for a human to review.
- Separate facts, assumptions, and recommendations.
- Prefer read-only Unreal MCP/editor inspection before mutation.
- Prefer project-local conventions and existing systems over new abstractions.
- Treat Unreal MCP as an execution channel, not an authority. Verify results through editor state, files, captures, or logs.
- Avoid broad automated asset moves.
- Preserve vendor content roots unless a human explicitly approves otherwise.
- Use source control-aware operations for asset moves and renames.
- When changing behavior, update the relevant durable knowledge or standards note in the same pass.

## Future Skill Set
The workflow should eventually be split into small skills instead of one large prompt.

Current draft skills:
- `ascent-course-resolver`: resolve course identity, aliases, media, content roots, and level relationships.
- `ascent-unreal-mcp-readonly`: enforce safe read-only Unreal MCP inspection and evidence reporting.
- `ascent-course-brief`: create or update a reusable course brief from resolver, MCP, performance, validation, or hygiene evidence.
- `ascent-course-performance-investigation`: investigate one course performance concern and classify likely bottleneck before recommending fixes.
- `ascent-course-content-hygiene`: review one course for aliases, stale references, dependency roots, vendor exceptions, and approval-gated cleanup slices.

Candidate next skills:
- `ascent-prompt-router`: classify prompt into Target Brief and Pass Type.
- `ascent-level-validation`: validate playable course requirements.
- `ascent-player-view-analysis`: inspect camera, cockpit/ship surface, and driver-visible VFX concerns.
- `ascent-external-ship-view-analysis`: inspect third-person and spectator ship readability.
- `ascent-ui-readability-and-performance`: inspect HUD/menu routes, screenshots, layout, and Slate/UMG performance concerns.
- `ascent-server-runtime-investigation`: inspect dedicated server logs, traces, and subsystem costs.

## External References
- Epic Games, [Data Validation](https://dev.epicgames.com/documentation/unreal-engine/data-validation-in-unreal-engine): validates assets with custom rules, including naming, budget, and dependency checks; supports command-line validation.
- Epic Games, [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine): telemetry capture and analysis for CPU, GPU, memory, asset loading, cooking, networking, and Slate/UMG.
- Epic Games, [Asset Registry](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-registry-in-unreal-engine): editor subsystem for querying unloaded asset metadata.
- Epic Games, [Scripting the Unreal Editor Using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python): editor automation and asset pipeline scripting.
- Epic Games, [Viewport Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/viewport-modes-in-unreal-engine): includes shader complexity view mode and default `MaxPixelShaderAdditiveComplexityCount`.
- ChiR24, [Unreal Engine MCP Server](https://github.com/ChiR24/Unreal_mcp): MCP server and native automation bridge for controlling Unreal Engine from AI assistants.

## Open Questions
- Where should the canonical shared course alias registry live if this workflow moves into the Unreal project?
- Should future course folders use `Courses/<Planet>/<Course>` as the canonical project-owned layout, or should the project keep central media folders and map-family folders with a stronger alias registry?
- Which course metadata source should be authoritative when config, primary assets, and documentation disagree?
- What are the target hardware, resolution, scalability, and frame-time budgets for course performance passes?
- Which level-validation checks are hard blockers versus warnings?
- Which vendor roots are formally exempt from project-owned locality rules?
- Which MCP operations are safe enough for routine use, and which require explicit human approval every time?
