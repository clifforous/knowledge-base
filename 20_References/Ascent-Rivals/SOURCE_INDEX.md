# Ascent-Rivals Source Index

## Goal
Track authoritative source locations for ingesting project knowledge into Obsidian markdown.

## Sources
| Source | Type | Canonical Path | Access Status | Notes |
|---|---|---|---|---|
| eventun | Repository | `/home/cgarvis/projects/genun/eventun` | Reachable | Backend event and stats service |
| accountun | Repository | `/home/cgarvis/projects/genun/accountun` | Reachable | Game dev UI |
| AscentRivals UE | Repository (Windows via WSL mount) | `/mnt/d/perforce/ascent/UE/AscentRivals` | Reachable | Unreal Engine 5.7 game project |
| Notion workspace | Notion via MCP | `notion` MCP server (`https://mcp.notion.com/mcp`) | Configured | Use MCP tools to pull page/database content and write markdown snapshots under `20_References/Ascent-Rivals/Notion/` |

## Path Notes
- Provided paths `/home/cliff/projects/genun/eventun` and `/home/cliff/projects/genun/accountun` are not present in this runtime.
- Equivalent reachable paths in this environment are under `/home/cgarvis/projects/genun/`.

## Ingest Targets
- Repository snapshots: `20_References/Ascent-Rivals/Repos/<repo-name>/...`
- Notion snapshots: `20_References/Ascent-Rivals/Notion/<workspace-or-database>/...`
- Cross-source synthesis and durable knowledge notes: `50_Knowledge/Ascent-Rivals/`
- Finalized decisions/designs: `30_Designs/Ascent-Rivals/`

## Operating Rules
1. Keep raw source extracts in `20_References`; avoid mixing interpretation into raw snapshots.
2. Add source provenance to each generated markdown note (source URL/path, commit hash or page ID, retrieved date).
3. Regenerate snapshots instead of manually editing generated files.
