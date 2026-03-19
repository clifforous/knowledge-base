# Ascent-Rivals Source Index

## Goal
Track authoritative source locations for ingesting project knowledge into Obsidian markdown.

## Sources
| Source | Type | Canonical Path | Access Status | Notes |
|---|---|---|---|---|
| eventun | Repository | `github.com/ikigai-github/eventun` | Reachable | Backend event and stats service |
| accountun | Repository | `github.com/ikigai-github/accountun` | Reachable | Game dev UI |
| AscentRivals UE | Repository checkout | Local workspace checkout | Reachable | Unreal Engine 5.7 game project; see `20_references/local-repo-paths.md` if machine-specific path mapping becomes necessary |
| Notion workspace | Notion via MCP | `notion` MCP server (`https://mcp.notion.com/mcp`) | Configured | Use MCP tools to pull page/database content and write markdown snapshots under `20_references/ascent-rivals/notion/` |

## Path Notes
- Prefer GitHub repository references over machine-specific local clone paths in durable notes.
- Keep machine-specific local checkout paths in `20_references/local-repo-paths.md` when they are operationally necessary.

## Ingest Targets
- Repository snapshots: `20_references/ascent-rivals/repos/<repo-name>/...`
- Notion snapshots: `20_references/ascent-rivals/notion/<workspace-or-database>/...`
- Cross-source synthesis and durable knowledge notes: `50_knowledge/ascent-rivals/`
- Finalized decisions/designs: `30_designs/ascent-rivals/`

## Operating Rules
1. Keep raw source extracts in `20_references`; avoid mixing interpretation into raw snapshots.
2. Add source provenance to each generated markdown note (source URL/path, commit hash or page ID, retrieved date).
3. Regenerate snapshots instead of manually editing generated files.
