# Ascent-Rivals Source Index

## Goal
Track authoritative source locations and provenance for durable Ascent Rivals knowledge.

## Sources
| Source | Type | Canonical Path | Access Status | Notes |
|---|---|---|---|---|
| eventun | Repository | `github.com/ikigai-github/eventun` | Reachable | Backend event and stats service |
| accountun | Repository | `github.com/ikigai-github/accountun` | Reachable | Game dev UI |
| AscentRivals UE | Repository checkout | Local workspace checkout | Reachable | Unreal Engine game project; see `knowledge-base/system/local-repo-paths.md` for the durable path policy |
| Notion workspace | Notion via MCP | `notion` MCP server (`https://mcp.notion.com/mcp`) | Configured | Use MCP tools to read selected workspace content; explicitly adopt durable material into the appropriate project role |

## Path Notes
- Prefer GitHub repository references over machine-specific local clone paths in durable notes.
- Keep machine-specific local checkout paths in local agent configuration, as described by
  `knowledge-base/system/local-repo-paths.md`.

## Ingest Targets
- Independently useful or cross-subject repository and external evidence:
  `ascent-rivals/sources/`
- Current-system synthesis: `ascent-rivals/system/`
- Proposed designs and initiative-specific artifacts: `ascent-rivals/initiatives/<initiative>/`
- Durable decision history: `ascent-rivals/decisions/`

## Operating Rules
1. Keep raw source extracts in `sources/`; avoid mixing interpretation into raw snapshots.
2. Add source provenance to each generated markdown note (source URL/path, commit hash or page ID, retrieved date).
3. Regenerate snapshots instead of manually editing generated files.
