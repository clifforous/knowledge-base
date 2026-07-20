# Repository Organization and Restructuring Plan

## Status

Approved for phased migration and executed through pass 2. Pass 1 established project-first
paths and indexes. Pass 2 consolidated current truth, separated active work from implementation
history, extracted decision logs, and removed obsolete workflow artifacts on 2026-07-19.

Pass 3 governance and mechanical validation are implemented. The empirical workflow cases in
the [pass 3 governance ledger](pass-3-governance-ledger.md) remain before final archival and
template extraction.

Date: 2026-07-19

## Goal

Reorganize the repository so a human or agent can answer four questions without knowing
its history:

1. Which project does this information describe?
2. Does it describe the current system, a proposed change, decision history, supporting
   evidence, or inactive material?
3. What should be read first for a reliable answer?
4. Where should new knowledge be written and how should it be incorporated later?

The resulting structure should work manually before it becomes the baseline for a template
repository or the proposed `kb` tool.

## Assumptions

- This remains a personal knowledge repository during the restructuring and manual-use
  period.
- Personal repositories and a future canonical repository should use the same durable
  document structure.
- The repository is primarily about Ascent Rivals today, but unrelated projects may be
  added as independent top-level directories.
- Markdown and ordinary links remain the durable representation. Search indexes and other
  retrieval structures are derived.
- Implementation repositories remain the source of executable code. This repository stores
  system understanding, design intent, rationale, evidence, and limited workflow support.
- The current work-tracking, prompt, research, and template workflows are not presumed to
  remain active merely because their files exist.

## Review of the Earlier Direction

The earlier project-first direction remains correct, but the future `kb` workflow sharpens
several boundaries.

### Project identity is the primary path axis

The current numbered roots organize files by activity or document format. This scatters one
project across research, reference, design, work-tracking, knowledge, template, and AI
trees. Project identity should instead be established at the repository root, followed by
the durable role the document serves.

The subject of the knowledge determines the project, not the implementation repository,
vendor, protocol, or technology mentioned. The existing Midnight and Cardano documents
describe Ascent Rivals integrations and therefore belong under `ascent-rivals/`. A new
top-level `midnight/` should be created only when documents describe an independent Midnight
project rather than Midnight's role in Ascent Rivals.

### Design and knowledge are lifecycle-relative

`design` and `knowledge` should not remain competing permanent categories:

- A proposed design belongs to an initiative.
- An accepted and implemented design is incorporated into the current system description.
- A superseded or rejected design becomes archive evidence.
- A design may remain linked from current knowledge as rationale, but it must not compete
  with the current system description as the default answer.

Website design follows the same rule. A proposed Website V2 page or visual system belongs
to its initiative. Once it describes the accepted, deployed website, the durable result
belongs under the website portion of `system/`.

### Research is an activity, not a durable destination

Research output should be classified by what survives the research:

- external material or bounded analysis used as evidence belongs in `sources/`
- an accepted conclusion belongs in `system/` or `decisions/`
- a speculative solution belongs in an initiative
- an obsolete or abandoned investigation belongs in `archive/`

This removes the need for a permanent top-level research bucket while preserving useful
evidence.

### Implementation plans and prompts are not current truth

An implementation plan may remain inside an active initiative when agents still use it.
After execution, its durable effects belong in system documents and decision records. The
plan can then be archived or removed after review.

Coder prompts, transcripts, task checklists, daily journals, and generated summaries do not
belong in the durable knowledge path. Valuable decisions and deltas should be extracted;
the original workflow artifacts should normally be archived or deleted. Future task-owned
decision logs are a separate evidence mechanism, not a replacement personal task manager.

## Target Repository Structure

~~~text
/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── ORGANIZATION.md
├── .gitignore
├── scratch/                         # local-only, ignored, never indexed or cited
├── knowledge-base/                  # this repository and the future kb workflow
│   ├── README.md
│   ├── system/
│   ├── initiatives/
│   ├── decisions/
│   ├── sources/
│   └── archive/
├── ascent-rivals/
│   ├── README.md
│   ├── system/
│   ├── initiatives/
│   ├── decisions/
│   ├── sources/
│   └── archive/
└── <unrelated-project>/
    ├── README.md
    ├── system/
    ├── initiatives/
    ├── decisions/
    ├── sources/
    └── archive/
~~~

Only directories that have content need to exist. The common names define semantic roles,
not a requirement to pre-create empty folder trees.

### Root files and reserved directories

| Path | Purpose |
|---|---|
| `README.md` | Human and AI entry point listing projects, repository role, and reading order. |
| `ORGANIZATION.md` | Tool-independent placement, lifecycle, metadata, linking, and indexing rules. |
| `AGENTS.md` | Short enforceable agent policy that links to `ORGANIZATION.md`; it should not duplicate the full taxonomy. |
| `CLAUDE.md` | Minimal client adapter importing the shared agent policy. |
| `scratch/` | Temporary local files that must not be committed, indexed, cited, or automatically consolidated. |
| `knowledge-base/` | Durable knowledge about this repository's organization and the proposed kb workflow. |
| `<project>/` | One independently understandable product or project knowledge base. |

Machine-local paths, credentials, client configuration, search caches, and writable clones
remain outside this durable structure. A future tool may maintain private application state,
but that state is not a new knowledge category.

## Project Structure

### `README.md`

Each project has a curated entry point containing:

- a short project description and scope boundary
- the default current-system reading order
- active or material initiatives
- the decision-log entry point
- important source collections
- archive guidance
- any project-specific terminology or applicability warning needed before retrieval

The index should use stable relative links and one-line descriptions. It is not required to
enumerate every file when a subordinate index provides a better entry point.

### `system/`

`system/` answers how the project currently works for the applicability declared by the
document. It contains cohesive domain, architecture, product, gameplay, API, terminology,
and visual-system descriptions.

Rules:

- Prefer cohesive subject documents over atomic files for every fact.
- Put applicability and verification status near the top when they affect interpretation.
- Put a concise current-state summary before detailed behavior and linked evidence.
- Rewrite accepted current truth when evidence changes; retain history in linked decisions
  and task logs rather than appending contradictory paragraphs.
- Do not place a merely proposed behavior here.
- Do not infer production applicability from a personal repository, source-control state,
  or approved design.

Subdirectories are domain-oriented and introduced only when document volume warrants them.
For Ascent Rivals, likely subjects include gameplay, game client, services, website, platform,
and external integrations. Exact subject normalization belongs to the second pass because it
requires content consolidation rather than mechanical movement.

### `initiatives/`

`initiatives/` contains proposed or in-progress changes that are not yet fully incorporated
into the current system description.

Each material initiative should have its own directory and a `README.md` that states:

- lifecycle status
- problem and intended outcome
- affected projects and implementation repositories
- affected current-system documents
- approved design or requirements
- active implementation plan, if still useful
- relevant sources and decision/task logs
- incorporation or closure state

An initiative may contain requirements, solution designs, page specifications, implementation
plans, experiments, and initiative-specific evidence. Those are artifacts of one change, not
repository-wide document categories.

An initiative is complete only when accepted effects have been incorporated into `system/`
and material decisions have a durable disposition. Completed, rejected, abandoned, and
superseded initiative material moves to `archive/` when it no longer needs to appear in the
active project index.

### `decisions/`

`decisions/` preserves why current knowledge changed without becoming a second copy of the
system description.

The project `decisions/README.md` should provide a concise chronological log. A normal entry
records:

- stable decision identifier and date
- what changed from X to Y
- short rationale
- affected system or initiative documents
- source task log or evidence
- disposition or superseding decision when applicable

A separate decision document is warranted only when the alternatives and rationale need
more explanation than a concise log entry can provide.

The future kb workflow may also use `decisions/tasks/` for one append-oriented decision and
delta log per agent task. Pending task entries are evidence, not current truth. Incorporation
updates the relevant system or initiative document, records the entry disposition, and adds
or updates the concise project decision log when the change is materially useful history.

### `sources/`

`sources/` contains durable supporting material rather than assertions of current truth.
Examples include:

- summaries of external documentation or conversations
- codebase or database analyses used by several documents
- source indexes and provenance notes
- design references and image assets
- bounded research whose evidence remains useful

Every source should identify its origin, retrieval or observation date when relevant, and
limitations. A source may be stale or contradictory without being rewritten into agreement.
Accepted conclusions belong in system, initiative, or decision documents with links back to
the source.

Initiative-specific evidence may remain inside its initiative when it has no meaningful use
outside that change. Shared evidence belongs in the project-level `sources/` tree.

### `archive/`

`archive/` preserves inactive material that still has historical, recovery, or audit value.
It is excluded from default current-system retrieval unless a query asks for history.

Archive candidates include:

- superseded and rejected designs
- completed implementation plans after incorporation
- abandoned initiatives
- old daily notes, task lists, generated summaries, and coder prompts retained temporarily
  for extraction or audit
- unused repository automation and templates pending deletion review

Archiving is not evidence that a claim is false. Archived documents retain links and should
carry a reason, date, and replacement link when known. Material with no durable value may be
deleted in the second pass after review rather than preserved indefinitely.

## Placement Decision Procedure

Agents and the future kb tool should apply the following questions in order:

1. **What project owns the described knowledge?** Route by primary subject, not vendor,
   technology, file format, source repository, or author.
2. **Does it describe accepted current behavior?** Place or incorporate it in `system/` and
   declare applicability.
3. **Does it describe an intended change?** Place it under one named initiative.
4. **Is its durable value the rationale or transition itself?** Record it in `decisions/` and
   link the affected current document.
5. **Is it evidence consumed by another document?** Place it in shared `sources/` or the
   relevant initiative's evidence area.
6. **Is it inactive but worth retaining?** Place it under the project's `archive/` with a
   reason and replacement when known.
7. **Is it temporary working material?** Keep it in ignored `scratch/` or outside the
   repository. Do not cite or consolidate it directly.
8. **Is it about repository behavior rather than a product?** Route it to the
   `knowledge-base/` project or the root policy files.
9. **Is it executable product or tool implementation?** Put it in the appropriate code
   repository unless this repository deliberately retains a small support tool.

When classification remains uncertain, preserve the source and mark the state unknown. Do
not infer that old or inactive-looking material is abandoned, implemented, or safe to
archive solely from its date.

## Minimum Document Metadata

The migration should introduce metadata selectively rather than front-loading a large
schema. The proposed minimum is:

~~~yaml
---
id: ascent-rivals:eventun-api
status: current
applicability: local-development
last_verified: 2026-07-19
---
~~~

Rules:

- `id` is stable across renames and moves.
- `status` uses a vocabulary appropriate to the document role.
- `applicability` describes an environment or lifecycle view; it does not claim authority.
- `last_verified` is required only for claims that can drift and have actually been checked.
- `superseded_by` may be added when an archived or replaced document has a known successor.
- Repository source identity determines personal, peer, or canonical authority. Do not copy
  authority into every file where it can drift from repository permissions.
- Project and document role are normally derived from the path rather than repeated in
  front matter.
- Unknown values remain explicit; agents must not invent verification dates or status.

The exact schema and controlled vocabularies should be finalized during the third pass after
real classification problems have been observed.

## Reading and Retrieval Order

For a normal current-state question within one project:

1. read the project `README.md`
2. read the most relevant `system/` summary or domain index
3. follow linked decisions when rationale is needed
4. consult active initiatives and task logs only for in-progress or future-state questions
5. consult sources when evidence, verification, or a known gap requires them
6. consult archive only for historical queries

Search and synthesis must preserve repository source identity, applicability, citations,
contradictions, and known gaps. A machine-generated search index may accelerate this order
but must not redefine it.

## First-Pass Candidate Mapping

The first pass is structural. It creates the new directories and moves files to their best
candidate role without consolidating prose or deleting redundant information.

| Current path | First-pass candidate |
|---|---|
| `50_knowledge/ascent-rivals/**` | `ascent-rivals/system/**` with the existing relative shape initially preserved |
| `30_designs/ascent-rivals/website/**` | `ascent-rivals/initiatives/website-v2/**` until implemented portions are identified in pass two |
| loose `30_designs/ascent-rivals/**` | named Ascent Rivals initiative clusters such as progression, post-match insights, teams and team gauntlets, gauntlet runtime, MMR v2, and reconnect restoration |
| `30_designs/cardano/**` | Ascent Rivals Cardano initiative material, not a top-level Cardano project |
| `30_designs/midnight/**` | Ascent Rivals Midnight/tournament-accounting initiative material, not a top-level Midnight project |
| `10_research/ascent-rivals/**` | `ascent-rivals/sources/analysis/**` initially; tightly scoped evidence may later move into its initiative |
| `10_research/midnight/**` | Ascent Rivals Midnight source material because the current note's subject is the game integration |
| `20_references/ascent-rivals/**` | `ascent-rivals/sources/**` |
| `20_references/local-repo-paths.md` | `knowledge-base/system/` for consolidation into repository policy |
| `40_work_tracking/**` | `ascent-rivals/archive/work-tracking/**` pending extraction and deletion review |
| `ai/prompts/ascent-rivals/**` | `ascent-rivals/archive/work-prompts/**` pending extraction and deletion review |
| `30_designs/knowledge-base/**` | `knowledge-base/initiatives/**`, split between repository restructuring and federated-kb work |
| `ai/docs/**` | `knowledge-base/system/` or `knowledge-base/archive/`, based on whether the workflow remains active |
| `90_templates/**` | `knowledge-base/archive/templates/**` pending deletion review |
| `ai/skills/**` and `ai/tools/**` | `knowledge-base/archive/legacy-automation/**` unless an active workflow justifies retention |
| `00_inbox/` | ignored `scratch/`; it is not an intake workflow or durable source |
| `.obsidian/` | leave as root application configuration during pass one; remove in pass two if Obsidian is no longer used |
| `AGENTS.md`, `CLAUDE.md`, `.gitignore` | remain at the root and receive only changes required by the active structure |

For explicit historical or superseded designs, pass one may place them directly in the
project archive. When status is ambiguous, prefer the relevant initiative and defer archive
judgment to the second pass.

## Migration Passes

### Pass 0: Review and migration preparation

Outputs:

- approved target structure and placement rules
- current-to-target mapping manifest
- named initiative clusters
- list of ambiguous documents requiring owner judgment
- migration verification commands or scripts

Review checkpoint:

- confirm project-first organization
- confirm `system`, `initiatives`, `decisions`, `sources`, and `archive` as the common roles
- confirm `scratch/` replaces the unused inbox workflow
- confirm current Midnight and Cardano documents remain under Ascent Rivals
- confirm whether obsolete work-tracking, prompts, templates, and automation should first be
  archived or may be deleted directly in pass two

### Pass 1: Structural migration

Actions:

1. Start from a reviewed source-control snapshot so unrelated edits and content changes are
   distinguishable from moves.
2. Create root and project indexes plus the target directories.
3. Move files with history-preserving source-control operations.
4. Preserve filenames and internal document content unless a mechanical link or status-path
   correction is required.
5. Update relative Markdown links, Obsidian links with path components, and instruction paths.
6. Record ambiguous placements in the migration manifest rather than solving them through
   silent content rewrites.
7. Leave all changes uncommitted for owner review.

Validation:

- every durable file is under a project and one semantic role
- no active link resolves through a removed numbered root
- project and initiative indexes resolve
- source-control output shows moves rather than accidental delete/recreate churn where
  practical
- no current-system claim changed as a side effect of the move
- scratch content remains ignored

### Pass 2: Consolidation and content normalization

Actions:

1. Review each project and initiative cluster, beginning with current-system documents.
2. Merge duplicate or fragmented current descriptions into cohesive system documents.
3. Resolve contradictions only when evidence supports a conclusion; otherwise record the
   conflict explicitly.
4. Extract high-value decisions and deltas from designs, research, tasks, and prompts.
5. Incorporate implemented behavior into system documents and link the evidence.
6. Separate mixed current/proposed documents or label their sections clearly.
7. Add missing indexes, stable identifiers, applicability, status, and verification metadata.
8. Archive or delete redundant plans, prompts, work logs, templates, and automation after
   durable information has been preserved.
9. Normalize domain subdirectories and filenames after consolidation reduces unnecessary
   fragmentation.

Validation:

- a current-state query does not require reading old designs or task logs
- proposed behavior cannot be mistaken for implemented behavior
- important current claims link to their decision or evidence trail
- archived and deleted files have known replacements or an explicit no-durable-value
  disposition
- indexes identify the authoritative reading order rather than merely listing files

### Pass 3: Governance and kb-readiness

Actions:

1. Revise this proposal into root `ORGANIZATION.md` using issues observed during passes one
   and two.
2. Reduce `AGENTS.md` to enforceable placement, retrieval, updating, and compatibility rules
   linked to the full organization document.
3. Add project-specific rules only where the common rules are insufficient.
4. Finalize controlled metadata values and minimal document templates.
5. Define the task decision-log schema, decision-log index behavior, grooming dispositions,
   and incorporation backlink rules.
6. Add lightweight validation for required indexes, stale current-system metadata, broken
   links, invalid roles, and references to archived material from default indexes.
7. Use the structure during ordinary work before extracting the reusable template.

Validation:

- an unfamiliar agent can classify representative new documents consistently
- a small direct task and a multi-agent feature both produce compatible durable updates
- parallel task logs do not require concurrent edits to one current-system document
- the same structure can represent a personal source or canon without changing file roles
- machine-local configuration and source authority remain outside durable document content

## Known Ambiguities for the Migration Manifest

- Website V2 contains a mixture of approved baselines, provisional applied design language,
  draft page specifications, and open implementation work. Keep the cluster together in
  pass one and promote only verified current behavior during pass two.
- Some implementation plans contain the best available record of implemented behavior while
  also retaining obsolete checklists. They require extraction before archival.
- Eventun foundation research documents mix source analysis, accepted architecture, and work
  sequencing. Initial placement in sources preserves them without asserting that every
  recommendation is current.
- Existing knowledge documents link heavily to designs and research. Those links should
  remain evidence links, while the system document becomes self-sufficient enough to answer
  normal current-state questions.
- The current `.obsidian/` configuration and next-day-summary automation appear tied to a
  workflow that is no longer used. Their deletion should be deliberate but should not shape
  the new durable taxonomy.

## Non-Goals

- Implement the `kb` tool during restructuring.
- Convert the repository to a database, graph store, or generated documentation site.
- Preserve the numbered folder taxonomy for compatibility.
- Turn the knowledge base into a task manager, prompt archive, daily journal, or transcript
  store.
- Require every document to use an identical template or every decision to have its own file.
- Treat an approved design, merged change, or Perforce submit as proof of production
  deployment.

## Related Design

- [Federated Personal and Canonical Knowledge Workflow](../federated-kb/federated-personal-and-canonical-knowledge-workflow.md)
