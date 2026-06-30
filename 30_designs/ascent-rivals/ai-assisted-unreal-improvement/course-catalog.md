# Course Catalog

## Purpose
Record reviewed course identity facts so agents and developers do not need to re-resolve stable courses on every pass.

This catalog is a reviewed cache, not the source of truth. The authoritative sources remain current `UHGCourseDefinition` assets, referenced levels, project config, and Unreal asset state.

## Use
1. Check this catalog before resolving a course from scratch.
2. Spot-check the course definition and level path before proposing changes.
3. Re-resolve the course if the course definition, level path, folder structure, media assets, or alias evidence changed significantly.
4. Update the catalog after a reviewed resolution pass finds durable new facts.

## Course Entry Format

```text
## <Planet> - <Display Name>
- Course code:
- Course definition:
- Canonical level:
- Feature state:
- Difficulty:
- Thumbnail:
- Hero image:
- Minimap:
- Last verified:
- Verification method:

### Aliases
| Alias | Classification | Source | Confidence | Notes |
|---|---|---|---|---|

### Level Relationships
- Persistent or canonical map:
- Streaming sublevels:
- World partition or external actor notes:
- Derived map variants:
- Other course definitions that reference related maps:

### Content Roots
- Project-owned:
- Vendor/import:

### Known Stale Or Prototype References
- 

### Unresolved Questions
- 
```

## Tefri 7 - Dunes
- Course code: `tefri-7-dunes`
- Course definition: `/Game/Courses/Definitions/Tefri_7_Dunes_CD.Tefri_7_Dunes_CD`
- Canonical level: `/Game/Courses/Desert/DesertTest_0_Relit.DesertTest_0_Relit`
- Feature state: `Prod`
- Difficulty: `Easy`
- Laps: `4`
- Target lap time: `27.0`
- Max ascension zones: `2`
- Thumbnail: `/Game/Courses/Screenshots/4kCineShots/SS_Dunes_small.SS_Dunes_small`
- Hero image: `/Game/Courses/Screenshots/4kCineShots/SS_Dunes_4k.SS_Dunes_4k`
- Minimap: `/Game/Courses/Minimaps/tefri_7_dunes_minimap.tefri_7_dunes_minimap`
- Last verified: 2026-06-26
- Verification method: Read-only Unreal MCP property read of `Tefri_7_Dunes_CD`, MCP asset search, texture detail read, dependency-root scan, source/config cross-check, and dirty package check in an Ascent Rivals project thread.

### Aliases
| Alias | Classification | Source | Confidence | Notes |
|---|---|---|---|---|
| `Tefri 7 - Dunes` | canonical | `UHGCourseDefinition` planet/name fields | High | Full display name. |
| `Tefri 7 Dunes` | corroborating | Human shorthand / composed display name | Medium | Useful prompt alias. |
| `Dunes` | canonical | `UHGCourseDefinition` name field | High | Ambiguous without planet. |
| `tefri-7-dunes` | canonical | `UHGCourseDefinition` code field | High | Also used as stat code when `StatCode` is empty. |
| `Tefri_7_Dunes_CD` | canonical | Course definition asset | High | Primary asset name. |
| `DesertTest_0_Relit` | corroborating | `UHGCourseDefinition` level field | High | Current backing level. |
| `DesertTest_0` | stale | Legacy `DefaultGame.ini` course rows | High | Legacy config maps `tefri-7-dunes` to this older level. |
| `SS_Dunes_4k` | corroborating | `UHGCourseDefinition` hero image field | High | Current hero image. |
| `SS_Dunes_small` | corroborating | `UHGCourseDefinition` thumbnail field | High | Current thumbnail. |
| `course_thumbnail_tefri_7_dunes` | stale | Legacy `DefaultGame.ini` course rows | High | Older thumbnail asset still referenced by legacy config. |
| `course_highres_tefri_7_dunes` | stale | Legacy `DefaultGame.ini` course rows | High | Older hero/high-res asset still referenced by legacy config. |
| `Dunes REDUX` / `tefri-7-dunes-2` | prototype | MCP alias search | Medium | Related but distinct course/variant. |
| `Dunes - Reflect` / `tefri-7-dunes-reverse` | prototype | MCP alias search | Medium | Related reverse/reflect variant. |
| `Spooky Dunes` / `tefri-7-dunes-dark` | prototype | MCP alias search | Medium | Related dark variant. |
| `Dunes (PAX)` / `Tefri_7_Dunes_OG_CD` | stale | Localization reference | Medium | Historical/missing reference; asset not found in current content tree during prior pass. |

### Level Relationships
- Persistent or canonical map: `/Game/Courses/Desert/DesertTest_0_Relit.DesertTest_0_Relit`
- Streaming sublevels: unresolved.
- World partition or external actor notes: unresolved.
- Derived map variants: `DesertTest_0`, `DesertTest_0_Pools`, `DesertTest_0_Tour_Neuvo`, `DesertTest_Reverse`, `DesertTest_Dark_A1`, `DesertTest_SandyDunes`; exact production status not cataloged.
- Other course definitions that reference related maps: `tefri-7-dunes-cardano` appears in legacy config; current `CourseDefinition` relationship not cataloged.

### Content Roots
- Project-owned: `/Game/Courses/Definitions`, `/Game/Courses/Desert`, `/Game/Courses/Minimaps`, `/Game/Courses/Screenshots/4kCineShots`
- Game/system: `/Game/Environment`, `/Game/UI/MiniMap`, `/Game/Race`, `/Game/Entities`, `/Game/Server`
- Vendor/import: `/Game/Brushify`, `/Game/Megascans`, `/Game/heavymetal`, `/Game/Cargo/kb3d_scifiindustrial`, `/Game/Shield_FX_Responsive`, `/Game/DarkSnowLandscape`, `/Game/WhiteSandsLandscape`
- Legacy presentation: `/Game/Courses/Screenshots/HighRes`, `/Game/Courses/Screenshots/Thumbnails`

### Known Stale Or Prototype References
- Legacy `DefaultGame.ini` course rows still point at `/Game/Courses/Desert/DesertTest_0.DesertTest_0` and older screenshot assets.
- Localization references `Tefri_7_Dunes_OG_CD` / `Dunes (PAX)`, but that asset was not found in the current content tree during the prior pass.
- Developer/prototype Dunes variants exist and should not be treated as canonical without a specific course definition check.

### Unresolved Questions
- Is the stale `DefaultGame.ini` course-array data intentionally retained for migration/backcompat, or should it be retired later?
- Is `Dunes (PAX)` intentionally removed, or should it remain as a historical alias?
- Supported modes are not `UHGCourseDefinition` fields and should be resolved from route/session systems when needed.
- Streaming/sublevel relationships were not fully cataloged.

## Galphus - Alluvial Basin
- Course code: `illus-0`
- Stat code: `illus-0`
- Course definition: `/Game/Courses/Definitions/Galphus_Allivual_Basin_CD.Galphus_Allivual_Basin_CD`
- Canonical level: `/Game/Courses/WetDarkRock/WetDarkRock_0.WetDarkRock_0`
- Feature state: `Prod`
- Difficulty: `Hard`
- Laps: `2`
- Target lap time: `3600.0`
- Max ascension zones: `3`
- Thumbnail: `/Game/Courses/Screenshots/4kCineShots/SS_Illus_small.SS_Illus_small`
- Hero image: `/Game/Courses/Screenshots/4kCineShots/SS_Illus_0_4k.SS_Illus_0_4k`
- Minimap: `/Game/Courses/Minimaps/galphus_alluvial_basin_minimap.galphus_alluvial_basin_minimap`
- Last verified: 2026-06-26
- Verification method: Live read-only Unreal MCP forward test in an Ascent Rivals project thread, including MCP asset search and selected `UHGCourseDefinition` property reads. Dirty package check was not completed because MCP transport failed after a broad read-only scan timed out.

### Aliases
| Alias | Classification | Source | Confidence | Notes |
|---|---|---|---|---|
| `Galphus - Alluvial Basin` | canonical | `UHGCourseDefinition` planet/name fields | High | Current player-facing identity. |
| `Alluvial Basin` | canonical | `UHGCourseDefinition` name field and localization | High | Display name. |
| `Galphus` | canonical | `UHGCourseDefinition` planet field and localization | High | Current player-facing planet. |
| `illus-0` | canonical | `UHGCourseDefinition` code/stat code fields | High | Current technical code, despite `Galphus` player-facing planet. |
| `Galphus_Allivual_Basin_CD` | canonical | Course definition asset | High | Typo-bearing canonical asset path; preserve exact spelling. |
| `WetDarkRock_0` | corroborating | `UHGCourseDefinition` level field and package map list | High | Current backing level. |
| `Illus - Alluvial Basin` | stale | Prompt alias, course code/media naming, developer Illus assets | Medium | `Illus` appears retained as technical/stale terminology; current planet is `Galphus`. |
| `SS_Illus_small` | corroborating | `UHGCourseDefinition` thumbnail field | High | Current thumbnail keeps Illus naming. |
| `SS_Illus_0_4k` | corroborating | `UHGCourseDefinition` hero field | High | Current hero image keeps Illus naming. |
| `Illus_1_CD` | stale | Localization reference | Medium | Asset was not found by MCP in the current registry during live forward test. |
| `Illus_Extended_CD` | prototype | `/Game/Developers/sahsk/CDs` | Medium | Developer course definition. |
| `Illus_Raw_CD` | prototype | `/Game/Developers/sahsk/CDs` | Medium | Developer course definition. |
| `Illus_Raw_Mtn_CD` | prototype | `/Game/Developers/sahsk/CDs` | Medium | Developer course definition. |
| `WetDarkRock_1` | prototype | `/Game/Developers/sahsk/AlphaCourses` | Medium | Developer/alpha map. |

### Level Relationships
- Persistent or canonical map: `/Game/Courses/WetDarkRock/WetDarkRock_0.WetDarkRock_0`
- Streaming sublevels: unresolved.
- World partition or external actor notes: no confirmed World Partition or external actor relationship in the live forward test.
- Derived map variants: `Demo_02_Grassy_Raw`, `Demo_02_Raw_Hallow`, `Demo_02_Raw_Mountain`, `Demo_02_Raw_Mountain_Tutorial`, `Demo_02_Raw_Flat`, `Demo_02_Raw_Lava_2`, `Demo_02_Grassy_Raw_Dunes`, `Demo_02_Raw_Mountain_Mossy_Walls`; exact production relationships not cataloged.
- Other course definitions that reference related maps: likely multiple `WetDarkRock` map-family courses; a broad scan timed out, so this remains incomplete.

### Content Roots
- Project-owned: `/Game/Courses/Definitions`, `/Game/Courses/WetDarkRock`, `/Game/Courses/Minimaps`, `/Game/Courses/Screenshots/4kCineShots`
- Game/system: `/Game/Entities`, `/Game/Environment`, `/Game/Race`, `/Game/Server`, `/Game/UI/MiniMap`
- Vendor/import: `/Game/DarkRockLandscape`, `/Game/Cargo/kb3d_scifiindustrial`, `/Game/heavymetal`, `/Game/Megascans`, `/Game/SnappyRoads`, `/Game/SpaceStation`

### Known Stale Or Prototype References
- `Illus` remains in course code, media asset names, localization history, and developer prototypes, but current player-facing planet is `Galphus`.
- `Galphus_Allivual_Basin_CD` contains an asset-name typo; preserve exact path in Unreal references.
- Localization references `/Game/Courses/Definitions/Illus_1_CD` / `Tachyon Relay`, but live MCP did not find that asset in the current registry.
- Developer `Illus_*` course definitions under `/Game/Developers/sahsk/CDs` are prototype/history signals, not canonical course identity.

### Unresolved Questions
- Is `illus-0` intentionally retained as the stable course/stat code, or should the code eventually align with `Galphus - Alluvial Basin`?
- Is `TargetLapTime=3600.0` intentional placeholder data or a tuning issue?
- Should stale localization for `/Game/Courses/Definitions/Illus_1_CD` be retired?
- Are the `Illus_*` developer definitions still useful prototypes or historical leftovers?
- Does `WetDarkRock_0` use streaming sublevels or other level relationships not covered by the shallow pass?
- A dirty package check was not completed after the live MCP forward test because MCP transport failed following a broad read-only scan timeout.
