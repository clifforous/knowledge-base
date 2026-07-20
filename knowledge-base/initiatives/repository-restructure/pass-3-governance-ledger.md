# Pass 3 Governance Ledger

Status: Governance implementation complete; empirical workflow validation pending

Date: 2026-07-19

## Purpose

Record the governance artifacts adopted after structural migration and content consolidation,
and make the remaining manual-use checkpoint explicit before template extraction or `kb`
implementation.

## Adopted Governance

- Root `ORGANIZATION.md` now defines project roles, placement, lifecycle, applicability,
  controlled initiative states, selective metadata, indexes, linking, and validation.
- Root `AGENTS.md` is reduced to enforceable retrieval, placement, updating, lifecycle,
  source-control, and validation rules linked to the full policy.
- Project-specific boundaries remain in `ORGANIZATION.md`; no nested `AGENTS.md` was added
  because neither current project needs a conflicting or narrower operational policy.
- New durable links prefer relative Markdown. Valid legacy wiki links remain supported.
- Minimal document patterns are embedded in policy rather than recreating a template folder
  the owner does not use.

## Decision And Task-Log Model

- Curated project decisions use stable `<PROJECT>-YYYY-NNN` identifiers.
- Optional pre-tool task logs use one file per agent task under
  `<project>/decisions/tasks/<year>/`.
- Capture does not update a shared task index, avoiding conflicts between parallel tasks.
- Pending task entries remain evidence until direct incorporation or grooming gives them a
  disposition.
- Incorporation updates both the destination and source entry, with bidirectional links when
  the origin is useful.
- Staleness never implies completion or abandonment.

## Validation

The zero-dependency `tools/validate_kb.py` checker validates:

- required root, project, role, active-initiative, and archived-initiative indexes;
- invalid project-root roles;
- controlled initiative status;
- task-log metadata and entry dispositions;
- duplicate stable identifiers;
- relative Markdown and Obsidian wiki links;
- verification dates and stale current-system claims when dates exist;
- direct archive links from default current reading indexes.

Strict validation on 2026-07-19 checked 122 Markdown files across two projects with zero
errors and zero warnings. Git whitespace validation also passed. No files were staged or
committed.

## Remaining Empirical Checkpoint

Do not extract the reusable template or begin the `kb` implementation solely from this pass.
First exercise the policy during ordinary work:

1. one small direct task that produces either a direct durable update or an explicit
   no-capture result;
2. one coordinated feature with implementation and review contributions;
3. one feature with at least two parallel task-owned logs and serialized incorporation;
4. one grooming pass containing an unresolved, abandoned, or already-represented entry;
5. one Windows-originated agent interaction against the WSL-hosted personal repository.

After these cases, review classification friction, capture noise, missing retrieval links,
task-log ownership, and whether the validator reports useful failures. Amend policy before
extracting a baseline repository.

## Closure Condition

The repository-restructure initiative remains `in-progress` only for this empirical checkpoint.
Once the cases above have been exercised and any policy corrections are incorporated, mark the
initiative `completed`, move this directory to
`knowledge-base/archive/initiatives/repository-restructure/`, and begin template extraction as
a separate explicit task.
