# Pass 3 Governance Ledger

Status: Governance implementation complete; empirical workflow validation pending

Date: 2026-07-19

Last updated: 2026-07-21

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

## First Live-Use Corrections

Reviews by the active Website V2 and teams/foundation tasks on 2026-07-20 exposed information
that repository-only consolidation did not preserve reliably:

- the Eventun foundation can be implemented and rehearsed locally while shared-development
  deployment remains pending;
- related game-client implementation can exist as a Perforce shelf awaiting mainline
  integration and therefore is neither absent nor deployed;
- the live Website V2 Pencil workfile is intentionally external because Pencil and the WSL
  filesystem do not provide a reliable live-authoring workflow; and
- a single initiative status cannot safely summarize components with different implementation,
  source-control, runtime, and design-artifact states.

`ORGANIZATION.md` now requires a small delivery snapshot for materially mixed initiatives,
keeps implementation, source-control, and runtime evidence independent, defines how to
reference mutable external artifacts, and requires active owner/task and source-control review
before consolidating active work. These corrections are evidence from real use, but they do not
by themselves complete the remaining task-log and cross-environment workflow cases below.

The Eventun foundation, teams, and Website V2 indexes received initial delivery snapshots.
Strict validation after these corrections checked 125 Markdown files across two projects with
zero errors and zero warnings.

## Second Live-Use Corrections

Refining the federated `kb` initiative on 2026-07-20 exposed a document-boundary problem: one
large design mixed normative requirements, contributor workflow and rationale, executable
architecture, rollout, validation, and open implementation choices. It was difficult to answer
whether the initiative had requirements or a design, and later edits could easily make one
section contradict another.

The initiative now keeps three linked documents in one initiative directory:

- `requirements.md` owns numbered normative constraints and acceptance;
- the workflow design owns contributor behavior, knowledge lifecycle, canon, and rationale; and
- `system-design.md` owns the executable/process architecture and technical verification.

This confirms that project-first lifecycle placement does not require a repository-wide folder
for every document type. Requirements and designs remain together under the change they govern,
while the initiative index provides reading order, role boundaries, status, and delivery state.
Each document also declares what it owns so a later agent can update one source of truth rather
than copy the same rule across all three.

The same work reconciled a smaller policy mismatch: `no durable knowledge` remains task-local
operational state and does not create a Markdown artifact or empty Git commit. This direct design
task updated initiative documents and a curated material decision without creating a task log.
It provides useful ordinary-work evidence, but it does not exercise parallel capture,
incorporation from task entries, or grooming and therefore does not close those remaining cases.

Strict validation after the design split checked 127 Markdown files across two projects with
zero errors and zero warnings.

## Third Live-Use Correction

Continuing Website V2 and teams work after the reorganization exposed an acceptance-signal gap.
The owner commonly accepts a reviewed checkpoint by asking to continue or begin the next step.
Existing long-running agent tasks advanced the work but did not consistently treat that ordinary
progression language as a reason to update initiative gates or record a material decision. This
left a few checkpoint summaries behind the detailed design even though the underlying work was
correctly separated by initiative and deployment state.

`ORGANIZATION.md` now defines scoped progression acceptance. Direction to proceed after a bounded
result accepts that immediately preceding checkpoint unless qualified; it may authorize
incorporation, a lifecycle update, or a material decision entry. It does not approve unrelated
open scope or establish implementation, verification, source-control, or deployment state.
Silence, age, topic changes, abandoned tasks, and agent-selected next actions remain
non-acceptance.

The compact operational rule is mirrored in `AGENTS.md` so existing and newly bootstrapped agents
apply it during normal work. This correction improves direct incorporation, but the two active
tasks mostly owned disjoint initiative documents and therefore still do not exercise the planned
parallel task-log and serialized-incorporation case.

## Fourth Live-Use Observation

The Website V2 design workflow now records a Windows-originated interaction against the WSL-hosted
personal repository. One long-running coordinator conversation owns product and design decisions,
prepares prompts for a separate Pencil designer conversation, inspects the Windows-hosted live
artifact through MCP, and incorporates accepted checkpoints into the Website V2 initiative. The
live artifact can advance beyond the reviewed Markdown checkpoint without becoming accepted
knowledge, implementation, or deployment evidence.

This case confirms the existing cross-environment and scoped-acceptance policies without requiring
a repository-wide correction. It also shows why prompts, copied completion reports, experimental
frames, and routine visual feedback should remain transient while accepted design rules, artifact
checkpoint state, contract gaps, and the next gate remain durable. The complete observation and
tool implications are recorded in the
[cross-chat design use case](../federated-kb/federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-iterative-design-coordination-across-chats-and-a-live-artifact).

This satisfies the Windows-originated manual-use case. It does not satisfy parallel task-owned
capture because the designer conversation did not write to the knowledge repository.

## Fifth Live-Use Observation

The Ascent Rivals Play-menu matchmaking-window change records the small-direct-task case. One
conversation performed an explicitly read-only ownership trace, proposed a bounded UI and calendar
freshness slice, received owner approval, paused when Perforce authentication was unavailable,
resumed after login, implemented the accepted change in an opened local working copy, and updated
the owning Gauntlet client-entry initiative.

The case confirms that a small feature can move from analysis to implementation and direct durable
incorporation without a coordinator/coder split or a task log. Scoped approval, local implementation,
Perforce submission, deployment, and runtime verification remained independent. Transient prompts,
command output, authentication recovery, and formatting checks stayed outside durable knowledge.
The complete observation and tool implications are recorded in the
[direct implementation use case](../federated-kb/federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-analysis-gated-direct-feature-implementation).

This satisfies the small-direct-task manual-use case. It does not satisfy parallel task-owned
capture or grooming.

## Remaining Empirical Checkpoint

Do not extract the reusable template or begin the `kb` implementation solely from this pass.
The small-direct, coordinated-feature, and Windows-originated cases are now recorded. Two cases
remain:

1. one feature with at least two parallel task-owned logs and serialized incorporation; and
2. one grooming pass containing an unresolved, abandoned, or already-represented entry.

After these cases, review classification friction, capture noise, missing retrieval links,
task-log ownership, and whether the validator reports useful failures. Amend policy before
extracting a baseline repository.

## Closure Condition

The repository-restructure initiative remains `in-progress` only for this empirical checkpoint.
Once the cases above have been exercised and any policy corrections are incorporated, mark the
initiative `completed`, move this directory to
`knowledge-base/archive/initiatives/repository-restructure/`, and begin template extraction as
a separate explicit task.
