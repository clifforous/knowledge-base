# Pass 2 Consolidation Ledger

Status: Complete

Date: 2026-07-19

## Purpose

Record content judgments made during consolidation so archive and deletion operations are
reviewable. This is a migration record, not permanent organization policy.

## Consolidation Decisions

| Cluster | Durable current replacement | Active remainder | Historical disposition |
|---|---|---|---|
| Eventun progression | `ascent-rivals/system/eventun/progression.md` plus the API, data-model, and ingest documents | Extend App authoring and post-V1 ideas | Requirements, solution, draft/publish plan, and completed client-integration plan archived |
| Post-match Insights | `ascent-rivals/system/eventun/post-match-insights-rollout.md` | Automatic pre-summary presentation and later ideation | Implemented design/plan and recommendation/metric predecessors archived |
| Gauntlet runtime | `ascent-rivals/system/eventun/gauntlet-stage-runtime-contract.md` | Client entry, runtime validation, and later finals/bracket direction | Implemented orchestration and first server-pass plan archived |
| Eventun foundation | Identified-ingestion, API, data-model, and game-client current-system documents | Physical retention, archive/restore, and client-confidence policy | Shared analyses retained as sources; task/prompt execution artifacts removed |
| Teams and team gauntlets | `team-gauntlet-current-state.md` for existing behavior | All three solution designs remain proposed | No consolidation beyond status/index clarification |
| Website V2 | `system/website.md` remains the deployed/current boundary | Approved and draft V2 design set remains active | Superseded Pencil brief retained; prompt and redundant design roadmap removed |
| MMR v2, Cardano POC, Midnight accounting | Existing current-system documents state present boundaries | Initiative documents remain active | No archive action |

## Decision Extraction

Material implementation and product changes were summarized in
`ascent-rivals/decisions/README.md`. Repository-organization choices were summarized in
`knowledge-base/decisions/README.md`. These concise entries replace reliance on task logs and
coder prompts as a rationale index.

## Deleted As No Longer Durable

- daily notes, task lists, generated summaries, and coder prompts under the former work
  workflow;
- the unused inbox-processing, work-tracking, prompt-store, skill, and next-day-summary
  automation;
- unused document templates;
- root Obsidian workspace configuration;
- the Website V2 design-document roadmap after its reading order and live status were
  incorporated into the initiative index.

The pass 1 migration manifest intentionally retains the temporary destinations of these
files as historical migration evidence.

## Validation

- 113 Markdown files were checked for relative Markdown links and Obsidian wiki links: zero
  missing or ambiguous targets.
- Active content has no references to the removed work-tracking, prompt, legacy automation,
  template, or Website V2 roadmap files. Their old paths remain only in the pass 1 manifest
  and migration-plan mapping as historical evidence.
- No current-system document is labeled draft or proposed. Initiative indexes state their
  lifecycle status and identify the authoritative current-system replacement where one exists.
- The repository root contains only Git metadata, root instructions/indexes, `ascent-rivals/`,
  `knowledge-base/`, and ignored `scratch/`.
- `scratch/*` and `.obsidian/` are ignored; `scratch/.gitkeep` remains explicitly retained.
- Git whitespace validation passed and the index remains unstaged. No commit was created.

## Outcome

Pass 2 removed 56 tracked workflow, application-configuration, template, prompt, and redundant
roadmap artifacts from the original layout. It added concise current progression and Insights
knowledge, extracted stable project/repository decisions, reduced three active initiative
clusters to unfinished work, and retained their implementation history under archive.

Pass 3 may now define `ORGANIZATION.md`, final placement rules, task-log grooming policy,
metadata vocabulary, and lightweight automated validation using the boundaries observed here.
