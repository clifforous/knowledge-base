# Knowledge Base Decision Log

## Purpose

Record durable changes to this repository and the proposed personal/canonical knowledge
workflow. Current policy remains in root instructions or `../system/`; initiatives remain
proposals until adopted.

## Decisions

### KB-2026-001 — Organize by project, then document role

- **Date:** 2026-07-19
- **Status:** Applied by structural pass 1 and refined by consolidation pass 2.
- **Changed:** From numbered activity/type roots to independent project roots containing
  `system`, `initiatives`, `decisions`, `sources`, and `archive` as needed.
- **Why:** A human or agent should find a project's current truth without reconstructing which
  activity originally created a file.
- **Affected knowledge:** [repository restructuring plan](../initiatives/repository-restructure/repository-organization-and-restructuring-plan.md)
  and [pass 1 manifest](../initiatives/repository-restructure/pass-1-migration-manifest.md).

### KB-2026-002 — Current truth and proposed design are lifecycle states

- **Date:** 2026-07-19
- **Status:** Applied during consolidation.
- **Changed:** From permanent competing `knowledge` and `design` categories to current behavior
  under `system/`, proposed or in-progress behavior under `initiatives/`, concise rationale in
  `decisions/`, evidence in `sources/`, and inactive material in `archive/`.
- **Why:** Implemented designs must become the default current answer, while unfinished designs
  must remain visibly non-current.
- **Affected knowledge:** [restructuring plan](../initiatives/repository-restructure/repository-organization-and-restructuring-plan.md)
  and [pass 2 consolidation ledger](../initiatives/repository-restructure/pass-2-consolidation-ledger.md).

### KB-2026-003 — Remove abandoned workflow artifacts after extraction

- **Date:** 2026-07-19
- **Status:** Applied during consolidation.
- **Changed:** From retaining unused daily notes, task lists, generated summaries, coder
  prompts, templates, Obsidian configuration, and dormant automation to deleting them once
  surviving decisions and current facts have durable replacements.
- **Why:** These artifacts added retrieval noise and implied workflows the repository owner no
  longer follows.
- **Affected knowledge:** [pass 2 consolidation ledger](../initiatives/repository-restructure/pass-2-consolidation-ledger.md).

### KB-2026-004 — Use selective metadata with path-derived project and role

- **Date:** 2026-07-19
- **Status:** Applied by pass 3 governance.
- **Changed:** From an undecided uniform frontmatter schema to path-derived project/role plus
  selective metadata for task logs, machine-queried applicability, verification, and durable
  identifiers.
- **Why:** Mandatory frontmatter on every legacy note would create maintenance noise without
  improving ordinary retrieval. Applicability and verification still need controlled values
  where agents or tools make decisions from them.
- **Affected knowledge:** [ORGANIZATION.md](../../ORGANIZATION.md) and the
  [pass 3 governance ledger](../initiatives/repository-restructure/pass-3-governance-ledger.md).

### KB-2026-005 — Parallel capture uses one append-only log per agent task

- **Date:** 2026-07-19
- **Status:** Adopted as the manual and future-tool task-log contract; empirical validation
  remains.
- **Changed:** From agents writing shared current documents or a shared task index during work
  to independent task-owned logs followed by serialized incorporation or grooming.
- **Why:** File ownership follows the agent task, which avoids normal parallel conflicts while
  keeping pending evidence separate from current truth.
- **Affected knowledge:** [ORGANIZATION.md](../../ORGANIZATION.md), the
  [federated workflow](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and the [pass 3 governance ledger](../initiatives/repository-restructure/pass-3-governance-ledger.md).
