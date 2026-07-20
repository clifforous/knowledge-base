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
| Eventun foundation | Identified-ingestion, API, data-model, and game-client current-system documents | Shared-development cutover, runtime resource hardening, physical retention, archive/restore, and client-confidence policy | Shared analyses retained as sources; task/prompt execution artifacts removed after active gates were extracted |
| Teams and team gauntlets | `team-gauntlet-current-state.md` for existing behavior | All three solution designs and their concise delivery plan remain proposed | Active T00–T08 and G01–G07 sequencing retained without the former execution diary |
| Website V2 | `system/website.md` describes the two current sites and separates future direction | Approved and draft V2 design set plus the sponsor-administration handoff remain active | Superseded Pencil and wallet flows retained; live Pencil workfile, prompt, and redundant design roadmap removed |
| MMR v2, Cardano POC, Midnight accounting | Existing current-system documents state present boundaries | Initiative documents remain active | No archive action |

## Decision Extraction

Material implementation and product changes were summarized in
`ascent-rivals/decisions/README.md`. Repository-organization choices were summarized in
`knowledge-base/decisions/README.md`. These concise entries replace reliance on task logs and
coder prompts as a rationale index.

## Post-Review Correction

The 2026-07-20 continuity review found that deleting the combined foundation/teams tracker also
removed the only definitions of the pending shared-development cutover, runtime-hardening gate,
production boundary, and T00–T08/G01–G07 work sequence. The implementation diary remains deleted,
but those active remainders are now represented by:

- `ascent-rivals/initiatives/eventun-foundation/development-cutover-and-runtime-hardening.md`;
- `ascent-rivals/initiatives/teams-and-team-gauntlets/delivery-plan.md`; and
- decision `AR-2026-007` in the Ascent Rivals decision log.

The three team solution designs retained their substantive capability, qualification, slot,
disconnect, and bracket decisions; their foundation status and cross-initiative links were
corrected without treating proposed behavior as current system state.

The same continuity review corrected Website V2 lifecycle drift:

- `system/website.md` now distinguishes the current marketing site and Ascentun from the
  proposed replacement;
- the excluded wallet-linking flow moved to archive, while sponsor administration became an
  active cutover handoff rather than a nonexistent public page;
- the accepted compact gauntlet-discovery contract no longer remains listed as an open choice;
- the initiative and design documents now record the completed homepage and gauntlet-directory
  calibrations plus the remaining detail, pilot, course, and team validation; and
- the repository Pencil copy was removed so the external live workfile remains the only
  actively edited copy until an explicit preservation checkpoint.

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
- The 2026-07-20 post-review strict validator pass checked 125 files with zero errors or
  warnings after the foundation/team continuity and Website V2 corrections.
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
