# Pass 1 Migration Manifest

## Status

Structural migration complete and awaiting owner review.

Date: 2026-07-19

## Constraints

- Preserve document content except for mechanical path, link, index, and active instruction
  changes required by the new structure.
- Preserve existing unstaged edits.
- Do not stage or commit migration changes.
- Do not infer implementation, production, abandonment, or archival status from age alone.
- Do not consolidate or delete substantive knowledge during this pass.
- Remove only obsolete empty-directory placeholder files.

## Deterministic Directory Mappings

Every file below the source prefix moves to the same relative path below the destination
prefix unless an exception is listed later.

| Source prefix | Destination prefix |
|---|---|
| `50_knowledge/ascent-rivals/` | `ascent-rivals/system/` |
| `10_research/ascent-rivals/` | `ascent-rivals/sources/analysis/` |
| `10_research/midnight/` | `ascent-rivals/sources/analysis/` |
| `20_references/ascent-rivals/website-concepts/` | `ascent-rivals/sources/website-concepts/` |
| `40_work_tracking/` | `ascent-rivals/archive/work-tracking/` |
| `90_templates/` | `knowledge-base/archive/templates/` |
| `ai/docs/` | `knowledge-base/archive/legacy-workflows/ai-docs/` |
| `ai/skills/` | `knowledge-base/archive/legacy-automation/skills/` |
| `ai/tools/` | `knowledge-base/archive/legacy-automation/tools/` |

## Project System and Source Exceptions

| Source | Destination |
|---|---|
| `20_references/ascent-rivals/SOURCE_INDEX.md` | `ascent-rivals/sources/SOURCE_INDEX.md` |
| `20_references/local-repo-paths.md` | `knowledge-base/system/local-repo-paths.md` |
| `00_inbox/.gitkeep` | `scratch/.gitkeep` |

## Ascent Rivals Initiative Mappings

### Eventun progression

Destination: `ascent-rivals/initiatives/eventun-progression/`

- `30_designs/ascent-rivals/eventun-challenges-game-client-integration-plan.md`
- `30_designs/ascent-rivals/eventun-extend-app-ui-progression-admin-design-plan.md`
- `30_designs/ascent-rivals/eventun-extend-app-ui-progression-authoring-design-plan.md`
- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-requirements.md`
- `30_designs/ascent-rivals/eventun-medals-progression-goals-challenges-rewards-solution-design.md`
- `30_designs/ascent-rivals/eventun-progression-draft-publish-implementation-plan.md`
- `30_designs/ascent-rivals/eventun-progression-next-phase-ideation-notes.md`

### Post-match insights

Destination: `ascent-rivals/initiatives/post-match-insights/`

- `30_designs/ascent-rivals/eventun-post-match-insights-implementation-plan.md`
- `30_designs/ascent-rivals/eventun-post-match-insights-next-phase-ideation-notes.md`
- `30_designs/ascent-rivals/eventun-post-match-insights-solution-design.md`
- `30_designs/ascent-rivals/match-summary-time-trial-improvement-metrics.md`
- `30_designs/ascent-rivals/recommendation-api-engineering-design.md`

### Eventun foundation

Destination: `ascent-rivals/initiatives/eventun-foundation/`

- `30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan.md`

### Gauntlet runtime

Destination: `ascent-rivals/initiatives/gauntlet-runtime/`

- `30_designs/ascent-rivals/gauntlet-finals-and-tournament-modes-design-review.md`
- `30_designs/ascent-rivals/gauntlet-stage-client-entry-plan-2026-05-07.md`
- `30_designs/ascent-rivals/gauntlet-stage-events-implementation-plan-2026-05-04.md`
- `30_designs/ascent-rivals/gauntlet-stage-orchestration-improvements.md`

### MMR v2

| Source | Destination |
|---|---|
| `30_designs/ascent-rivals/mmr-v2-design-and-implementation-plan.md` | `ascent-rivals/initiatives/mmr-v2/mmr-v2-design-and-implementation-plan.md` |

### Teams and team gauntlets

Destination: `ascent-rivals/initiatives/teams-and-team-gauntlets/`

- `30_designs/ascent-rivals/team-experience-and-progression-solution-design.md`
- `30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design.md`
- `30_designs/ascent-rivals/teams-solution-design.md`

### Website V2

All files under `30_designs/ascent-rivals/website/` move to
`ascent-rivals/initiatives/website-v2/` except:

| Source | Destination | Reason |
|---|---|---|
| `30_designs/ascent-rivals/website/pencil-design-brief.md` | `ascent-rivals/archive/initiatives/website-v2/pencil-design-brief.md` | Explicitly superseded. |
| `30_designs/ascent-rivals/website/pencil-terminal-ops-follow-up-prompt.md` | `ascent-rivals/archive/work-prompts/website-v2/pencil-terminal-ops-follow-up-prompt.md` | Prompt artifact, not durable design truth. |

### Cardano reward service proof of concept

Destination: `ascent-rivals/initiatives/cardano-reward-service-poc/`

- `30_designs/cardano/ascent-rivals-cardano-reward-service-poc.md`
- `30_designs/cardano/cardanoun-dashboard.pen`

### Midnight tournament accounting

Destination: `ascent-rivals/initiatives/midnight-tournament-accounting/`

- `30_designs/midnight/ascent-rivals-midnight-tournament-accounting-design.md`
- `30_designs/midnight/ascent-rivals-walletless-player-accounting-future-work.md`

## Ascent Rivals Archive Mappings

| Source | Destination | Reason |
|---|---|---|
| `30_designs/ascent-rivals/reconnect-state-restoration-initial-implementation-plan-2026-04-29.md` | `ascent-rivals/archive/initiatives/reconnect-state-restoration/reconnect-state-restoration-initial-implementation-plan-2026-04-29.md` | Explicitly historical; current policy is already linked. |
| `ai/prompts/ascent-rivals/*.md` | `ascent-rivals/archive/work-prompts/eventun-foundation/` | Completed coder prompt artifacts. |
| `ai/prompts/README.md` | `knowledge-base/archive/legacy-workflows/prompts/README.md` | Procedure for an inactive prompt store. |

## Knowledge-Base Project Mappings

| Source | Destination |
|---|---|
| `30_designs/knowledge-base/README.md` | `knowledge-base/README.md` |
| `30_designs/knowledge-base/federated-personal-and-canonical-knowledge-workflow.md` | `knowledge-base/initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md` |
| `30_designs/knowledge-base/repository-organization-and-restructuring-plan.md` | `knowledge-base/initiatives/repository-restructure/repository-organization-and-restructuring-plan.md` |
| `30_designs/knowledge-base/pass-1-migration-manifest.md` | `knowledge-base/initiatives/repository-restructure/pass-1-migration-manifest.md` |

## Root Files

| Path | Disposition |
|---|---|
| `AGENTS.md` | Remains at root and is updated to the active structure. |
| `CLAUDE.md` | Remains unchanged at root. |
| `.gitignore` | Remains at root and changes its transient path from `00_inbox/` to `scratch/`. |
| `.obsidian/` | Remains unchanged during pass 1 pending pass-2 removal review. |

New structural indexes:

- `README.md`
- `ascent-rivals/README.md`
- `ascent-rivals/system/README.md`
- `ascent-rivals/initiatives/README.md`
- `ascent-rivals/decisions/README.md`
- `ascent-rivals/sources/README.md`
- `ascent-rivals/archive/README.md`

## Removed Placeholders

The following empty files exist only to retain obsolete empty directories and are removed:

- `10_research/.gitkeep`
- `20_references/.gitkeep`
- `30_designs/.gitkeep`
- redundant `.gitkeep` files inside moved non-empty work-tracking directories

## Validation Contract

- All mapped source files exist before movement and all target paths are collision-free.
- All mapped target files exist after movement.
- The old numbered roots and `ai/` contain no remaining files.
- Active documents contain no unresolved path reference to a removed numbered root.
- Relative Markdown and path-qualified wiki links resolve after mechanical rewriting.
- Root and project indexes link to the new locations.
- Git reports no staged changes and no content loss.

## Pass 1 Outcome

- The pre-migration index contained 150 tracked files.
- 137 tracked files were mapped to new project-first paths.
- Seven root policy, client-adapter, ignore, and Obsidian configuration files remained at
  their existing paths.
- Six empty-directory placeholder files were removed.
- The previously untracked restructuring plan and this manifest were preserved under the
  knowledge-base restructuring initiative.
- Twenty-one root, project, role, and initiative indexes were added.
- The resulting working tree contains 167 non-Git files.
- Every tracked pre-migration file is either present at its mapped target, intentionally
  unchanged at root, or listed as a removed placeholder.
- The retired numbered roots and `ai/` directory no longer exist.
- Active content has no remaining references to the retired roots. Historical path names
  remain only where required by this plan, this manifest, or archived workflow history.
- A repository-local link audit reported zero broken and zero ambiguous Markdown or wiki
  links after accounting for same-directory resolution.
- Scratch content is ignored while `scratch/.gitkeep` remains tracked.
- No migration change is staged or committed.
