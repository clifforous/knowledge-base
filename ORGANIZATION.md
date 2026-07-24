---
id: knowledge-base:organization
status: current
applicability: environment-independent
adopted: 2026-07-19
---
# Knowledge Base Organization

## Purpose And Authority

This repository stores durable, project-first knowledge in portable Markdown. It is intended
to remain understandable without Obsidian, a database, a generated site, or the future `kb`
tool.

This document defines placement, lifecycle, metadata, indexing, decision-log, and validation
rules. `AGENTS.md` contains the smaller enforceable agent policy and links here for detail.
When they conflict, the explicit operational rule in `AGENTS.md` controls agent behavior and
this document should be corrected.

Repository identity carries source authority:

- this repository is Cliff's personal knowledge source;
- a future contributor repository is that contributor's personal source;
- a future canon repository contains explicitly reviewed team knowledge;
- Notion and peer repositories are attributed sources, not implicit canon.

Authority and deployment are independent. Personal knowledge, canon adoption, an approved
design, a commit, a merge, or a Perforce submit does not prove production deployment.

## Default Reading Order

For a normal current-state question:

1. Read the root `README.md` and select the owning project.
2. Read that project's `README.md`.
3. Read the most relevant `system/` index or subject document.
4. Follow `decisions/` when rationale or a transition matters.
5. Consult `sources/` when evidence, provenance, or a known conflict matters.
6. Read `initiatives/` only for intended or in-progress behavior.
7. Read `archive/` only for a historical question or a clearly labeled evidence link.

Search results must preserve project, role, source repository, applicability, and known gaps.
A generated index may accelerate this order but must not redefine it.

## Repository Shape

~~~text
/
├── README.md
├── ORGANIZATION.md
├── AGENTS.md
├── CLAUDE.md
├── scratch/                         # ignored local-only work
├── tools/                           # small repository support tools only
├── knowledge-base/                  # this repository and future kb workflow
│   ├── README.md
│   ├── system/
│   ├── initiatives/
│   ├── decisions/
│   ├── sources/                     # only when content exists
│   └── archive/                     # only when content exists
├── ascent-rivals/
│   ├── README.md
│   ├── system/
│   ├── initiatives/
│   ├── decisions/
│   ├── sources/
│   └── archive/
└── <unrelated-project>/
    └── ...same semantic roles as needed
~~~

Only roles containing durable material need to exist. Do not create empty directory trees to
make projects look uniform.

A top-level project represents an independently understandable product, system, or body of
work. Route by the subject of the knowledge, not the vendor, protocol, implementation
repository, or file format. Cardano and Midnight notes about Ascent Rivals therefore remain
under `ascent-rivals/`; create a separate project only for independently scoped work.

## Project Roles

| Role | Question answered | Contains | Must not be treated as |
|---|---|---|---|
| `system/` | How does the project currently work for the stated applicability? | Cohesive domain, product, gameplay, API, architecture, terminology, and visual-system knowledge | Proof of production unless deployment evidence says so |
| `initiatives/` | What change is proposed, approved, or in progress? | Requirements, solution designs, specifications, experiments, and useful active implementation plans | Current behavior merely because it is approved or implemented somewhere |
| `decisions/` | Why did direction or current knowledge change? | Concise material decision history and task-owned decision/delta evidence | A second copy of current-system prose or a task manager |
| `sources/` | What evidence or reference supports another document? | Independently reusable external references, repository analyses, observations, provenance, and durable assets | Accepted current truth by itself or the default home for an initiative-specific working artifact |
| `archive/` | What inactive material remains useful for history, recovery, or audit? | Superseded designs and incorporated implementation history | A default retrieval source |
| `scratch/` | What is temporary and local? | Uncommitted working notes and disposable files | A citable or indexed knowledge source |

Executable product code belongs in its implementation repository. `tools/` is limited to
small support utilities that validate or maintain this knowledge repository.

## Placement Procedure

Apply these questions in order:

1. Which project owns the subject?
2. Is the statement accepted current behavior for a known applicability? Incorporate it into
   `system/`.
3. Is it a proposed or unfinished change? Put it under one named initiative.
4. Is its lasting value the change in direction or rationale? Record it in `decisions/` and
   link the affected document.
5. Is it independently useful evidence or reused across subjects? Put it in shared `sources/`.
   If it exists only for one initiative, keep it inside that initiative and label whether it is
   live, external, or a preserved snapshot.
6. Is it inactive but historically useful? Archive it with a reason and replacement.
7. Is it temporary, a prompt, transcript, task list, build output, or routine review detail?
   Keep it in `scratch/`, the agent task, or the implementation repository; do not add it as
   durable knowledge.
8. Is it about this repository or the future knowledge workflow? Route it to the
   `knowledge-base/` project or a root policy file.

If status remains uncertain, preserve the evidence and state the uncertainty. Do not infer
that old work is completed, abandoned, deployed, or safe to delete from age alone.

## Current-System Documents

`system/` is the default answer surface. A current-system document should:

- state the current behavior before history or implementation detail;
- be self-sufficient for normal questions;
- read as a reference chapter, not as a chronological implementation log;
- distinguish implemented facts, known gaps, and future direction;
- identify applicability when it differs from the project default;
- link evidence or decisions without requiring those files for basic comprehension;
- replace contradicted prose instead of accumulating incompatible statements;
- preserve rationale in decisions or sources rather than as an inline chronological diary.

Use stable domain language in the main explanation. Internal task labels, delivery-slice codes,
commit hashes, changelist numbers, test counts, and step-by-step implementation history belong in
task logs, initiative delivery evidence, source records, or Git history. Include them in a system
chapter only when a reader needs the identifier to understand or operate the current system.

Prefer a small number of cohesive sections and tables over a long undifferentiated notes list.
When detailed behavior already has an authoritative chapter, summarize the boundary and link that
chapter instead of repeating its implementation history.

Write for a technically curious teammate who does not have the recent task conversation in mind.
Introduce the mental model before edge cases, explain specialized terms when they first matter, and
use a small concrete example when it makes a boundary easier to understand. Concise means removing
repetition and irrelevant history; it does not mean compressing every idea into the fewest words.

AI friendliness comes from descriptive headings, explicit terminology, stable identifiers, and
clear applicability—not from dense shorthand. Natural explanatory prose is preferred when it helps
a person learn the system without making the facts ambiguous.

### Subject boundaries

A current-system chapter should have one primary kind of question:

| Chapter kind | Owns | Does not own |
|---|---|---|
| Overview | Mental model, responsibilities, boundaries, and reading path | Detailed contracts or a running change history |
| Interface architecture | How requests enter, gain identity and authority, are validated, execute, and return | Endpoint-by-endpoint reference or unrelated domain rules |
| Domain behavior | Product and game rules, lifecycle, invariants, and interactions | Transport boilerplate or table-by-table storage notes |
| Data model | Durable meaning, entities, relationships, facts, projections, and retention | Handler catalogs or user-flow narration |
| Operational behavior | Runtime limits, failure handling, observability, jobs, and environment behavior | Product roadmap or implementation transcript |
| Deployment view | What is active in each named environment and the evidence for that claim | A replacement for the conceptual system chapters |

Generated Swagger, protobuf comments, code documentation, and equivalent references own exhaustive
operation and field catalogs. The knowledge base should explain how those interfaces are designed
and used, then link the generated reference when exact shapes matter.

When information does not fit the owning chapter without changing its main question, move it to the
chapter that owns the subject. Create a new focused chapter only when the subject will remain useful
independently; do not create one merely to avoid editing an existing explanation.

The default applicability for this personal repository is `local-development`. Stronger
environment claims require explicit evidence. When part of a system differs by environment,
state that boundary close to the affected claim or use a dedicated environment/deployment
document; do not label the entire personal repository production.

Lead with runtime-active behavior. Accepted implementation that exists only in a working copy,
branch, commit, Perforce shelf, or other non-running artifact may be useful current knowledge,
but it must be labeled with that source-control boundary. A shelved or committed implementation
does not become active runtime behavior merely because its code exists.

## Delivery, Deployment, And Artifact State

An initiative's controlled `status` describes the lifecycle of the initiative as a whole. It
does not prove that every component has the same design, implementation, source-control, or
deployment state.

When a material initiative spans multiple implementation repositories, environments, or live
design artifacts and those states differ, its `README.md` must include a concise `Delivery
Snapshot`. Track only meaningful surfaces and gates, not every task or commit:

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Named component or artifact | Controlled state | Location or revision | Environment and evidence | State-changing condition |

Keep the dimensions independent:

- work state is `not-started`, `designing`, `approved`, `implementing`, `implemented`,
  `verified`, or `superseded`;
- `implemented` means an implementation artifact exists; it does not mean merged, submitted,
  deployed, or verified in a running environment;
- a Perforce shelf is recoverable implementation evidence, not mainline or deployment;
- a Git commit or submitted changelist is source history, not deployment evidence;
- deployment claims name the environment and cite a release, revision, observation, or other
  stable evidence when available;
- local, shared-development, staging, and production states may differ; never promote one from
  another by inference;
- a live design artifact can be ahead of its reviewed Markdown checkpoint and must be labeled as
  such.

Update the snapshot when a meaningful gate changes: design approval, implementation creation,
shelving, merge or submit, deployment, rollback, runtime verification, or an external design
checkpoint. Detailed execution still belongs in the agent task or implementation repository.

## Initiative Lifecycle

Every material initiative has its own directory and `README.md`. The index must state:

- controlled status;
- intended outcome and boundary;
- affected projects or implementation repositories when useful;
- authoritative current-system documents;
- active requirements, designs, specifications, and plans;
- relevant decisions and sources;
- a delivery snapshot when component or artifact states materially differ;
- what remains before incorporation or closure.

Use these initiative statuses:

| Status | Meaning |
|---|---|
| `proposed` | Direction is still under review or not approved for implementation. |
| `approved` | Direction is accepted, but implementation has not materially started. |
| `in-progress` | Design, implementation, validation, or incorporation is active. |
| `blocked` | Progress requires a named external decision or condition. |
| `completed` | Accepted effects are incorporated and the initiative is ready to archive. |
| `superseded` | Another named initiative or decision replaced it. |
| `rejected` | The direction was explicitly declined. |

`completed` is transitional. Once current effects and material decisions are incorporated,
move the inactive initiative material to `archive/initiatives/<initiative>/` and remove it
from the active initiative index. Preserve an archive README that states date, reason,
current replacement, and any active successor.

An implementation plan remains active only while it still guides work. After execution,
promote durable behavior to `system/`, extract useful rationale, then archive or delete the
plan. Unchecked boxes in a historical plan are not a completion ledger.

## Decision Records

### Curated project log

`<project>/decisions/README.md` is the concise human and AI entry point. Record only material
decisions whose rationale will help future work. Normal entries include:

- stable identifier in `<PROJECT>-YYYY-NNN` form;
- decision date and disposition;
- what changed from X to Y;
- concise rationale;
- affected current-system or initiative documents;
- evidence or originating task-log entries;
- superseding decision when applicable.

Do not duplicate the full current behavior in the decision log. The affected `system/` or
initiative document remains authoritative.

### Task-owned decision and delta logs

When manual capture is useful before the future `kb` tool exists, use one append-oriented
file per agent task:

~~~text
<project>/decisions/tasks/<year>/<YYYY-MM-DD>-<task-id>.md
~~~

The task id must be stable for the agent task and sanitized for a filename. A reused coder or
coordinator task continues appending to its existing file. Parallel tasks never append to the
same file and never update a shared task-log index during capture.

Required task-log frontmatter:

~~~yaml
---
id: ascent-rivals:task:<task-id>
task_id: <stable-client-or-generated-id>
parent_feature: <optional-stable-feature-id>
project: ascent-rivals
agent_role: coordinator
status: open
applicability: local-development
opened: 2026-07-19
last_activity: 2026-07-19
---
~~~

Allowed `agent_role` values are `direct`, `coordinator`, `coder`, `reviewer`, and `researcher`.
Allowed task statuses are `open`, `completed`, `abandoned`, `superseded`, and `unknown`.
Staleness is derived from `last_activity`; it is never a task status and never proves
abandonment.

Each entry uses a stable id and records one durable fact:

~~~md
## <task-id>:D001 — decision

- Timestamp: 2026-07-19T18:30:00Z
- Type: decision
- State: pending
- Statement: Changed X to Y.
- Rationale: Why the change matters after this task ends.
- Evidence: Commit, changelist, code path, source document, or explicit acceptance.
- Destinations: Candidate system, initiative, or decision documents.
- Disposition note: Empty while pending; required when state changes.
~~~

Allowed entry types are `decision`, `current-delta`, `finding`, `contract-change`,
`terminology-change`, `constraint`, `correction`, `blocking-question`, and
`source-adoption`.

Allowed entry states are:

- `pending`
- `incorporated`
- `already-represented`
- `informational`
- `rejected`
- `superseded`
- `abandoned`
- `needs-owner`

Task logs exclude prompts, transcripts, execution steps, routine review feedback, build/test
output, and ordinary task tracking. A task log is evidence; pending entries are never current
truth.

### Task-log indexing

Normal capture does not edit `decisions/README.md` or a shared task index. Discovery scans the
task-log directory or uses a derived local index. A future generated `decisions/tasks/INDEX.md`
must be reproducible from task frontmatter and entries and must not be treated as authored
knowledge.

Add a curated decision-log entry only when the incorporated change is materially useful
history. Routine deltas may link directly between the destination document and task entry.

## Incorporation And Grooming

Direct incorporation is allowed when acceptance is explicit or reliable source-control
completion is confirmed. Otherwise leave entries pending.

Incorporation must:

1. select accepted entries;
2. re-read the latest destination documents;
3. deduplicate and identify contradictions;
4. update current-system, initiative, or decision documents according to actual status;
5. add a destination backlink to each source entry;
6. add a source-task link in the destination's evidence or decision-history section when the
   origin is useful;
7. set a final entry state and disposition note;
8. update affected curated indexes.

Grooming handles work that ended without clear incorporation. Review logs by bounded project,
feature, subject, or date scope. Every reviewed entry receives one of the allowed states or
remains `pending` with a concrete reason. Useful grooming outcomes are incorporation,
already represented, informational, rejected, superseded, abandoned with confirmation, or
needs owner judgment.

Never infer completion or abandonment from age. Stop a grooming pass when the selected scope
has dispositions, two passes produce no new changes, or the chosen time/iteration bound is
reached. Escalate semantic conflicts instead of manufacturing agreement.

## Sources

Shared sources should identify origin, observation or retrieval date when relevant, and known
limitations. Prefer canonical repository URLs, commit hashes, Perforce changelists, official
documentation, Notion page identity, or another stable reference over machine-local paths.

A mutable working artifact may remain outside the repository when its authoring tool or storage
boundary makes repository use unreliable. The owning initiative must then record the artifact's
owner, tool and durable identity when one exists, why it is external, the last reviewed
checkpoint, and which Markdown documents capture accepted direction. Do not publish a
machine-specific path as a shared identifier. Import a repository snapshot only at an explicit
preservation or review checkpoint, label it as a snapshot, and do not maintain two nominally
live copies.

Source conclusions do not become current truth until incorporated into `system/`, an active
initiative, or a decision. A stale or contradictory source may remain unchanged when its
provenance is still useful.

## Archive And Deletion

Archive material must be excluded from default current retrieval. Each archived initiative
or collection has an index or notice containing:

- archive date;
- reason;
- current replacement when known;
- active successor when one exists;
- any limitation such as unverified runtime behavior.

Delete prompts, transcripts, redundant task logs, templates, generated summaries, and
obsolete automation when they have no remaining historical, recovery, or audit value and
their durable decisions are preserved. Record non-obvious bulk deletion in a migration or
consolidation ledger.

## Metadata

Paths provide project and role, so frontmatter is selective. Do not add metadata that merely
repeats a stable path or invent dates to satisfy a template.

Frontmatter is required for task logs. It is recommended for new long-lived system documents,
standalone source records, and documents whose applicability or verification will be queried
mechanically. Existing documents may adopt it when substantively revised; do not create a
large mechanical rewrite solely for metadata uniformity.

When controlled metadata is present, put it in YAML frontmatter before the title. Do not create a
body preamble made only of `Date:`, `Status:`, `Last reviewed:`, or `Last consolidated:` labels.
Dates describe actual observation, acceptance, verification, or deployment evidence; they are not
document-maintenance bookkeeping. Initiative indexes may explain their current boundary in the
opening paragraph after the title. Existing body-label preambles may remain until the document is
substantively revised; convert them as part of that revision rather than through a repository-wide
metadata-only pass.

Controlled fields:

| Field | Rule |
|---|---|
| `id` | Stable lowercase identifier, normally `<project>:<subject>`; required for task logs and standalone records that need durable backlinks. |
| `status` | Use the role-specific controlled vocabulary; do not encode source authority or deployment here. |
| `applicability` | `local-development`, `shared-development`, `staging`, `production`, `environment-independent`, `unknown`, or `environment:<slug>`. |
| `last_verified` | ISO date of an actual verification; omit when not verified. |
| `verification` | `verified`, `unverified`, `unverifiable-cheaply`, `drifted`, `obsolete`, or `not-required`. |
| `verification_source` | Stable evidence for `verified`, `drifted`, or `obsolete`. |
| `superseded_by` | Stable id or relative link to the replacing record. |

`verified` requires `last_verified` and `verification_source`. A verification date becoming
old makes a claim stale for review; it does not make the claim false. `drifted` and `obsolete`
require a corrective disposition. Generic confidence scores are not a replacement for
applicability and evidence.

Initiative frontmatter `status` uses the controlled initiative value. The opening paragraph
explains the real boundary in ordinary prose.

## Minimal Document Patterns

These are patterns, not mandatory fill-in-the-blank templates.

### System subject

~~~md
---
id: project:subject
status: current
applicability: local-development
---
# Subject

## Current State
## Known Gaps
## Evidence And Decisions
~~~

### Initiative index

~~~md
---
id: project:initiative-name
status: proposed
applicability: environment-independent
---
# Initiative

One sentence explaining the real boundary.

## Outcome
## Active Documents
## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|

## Authoritative Current System
## Remaining Before Closure
~~~

### Source record

~~~md
---
id: project:source-name
applicability: environment-independent
---
# Source Or Analysis

Observed: YYYY-MM-DD
Origin: stable URL, repository revision, page id, or changelist
Limitations: what this evidence cannot establish

## Findings
## Adopted Conclusions
~~~

### Archive notice

~~~md
Archive notice: Archived YYYY-MM-DD because <reason>. Use <replacement> for current behavior.
~~~

## Index And Linking Rules

- Root `README.md` lists projects and the default reading order.
- Every project has `README.md` linking its active semantic roles.
- Every existing role directory has a role index (`README.md` or, for a cohesive system
  domain, an explicitly linked `overview.md`).
- Every material initiative has its own `README.md`.
- Nested page, flow, or specification collections need an index when the parent links the
  collection as a unit.
- Prefer relative Markdown links in new documents. Existing Obsidian wiki links may remain
  while valid, but new links should not depend on basename ambiguity.
- Link to the authoritative current document first; label source, initiative, and archive
  links by role.
- A default current-system index must not route readers directly to an individual archive
  artifact. A project index may link its archive index, and a subject document may link
  clearly labeled historical evidence.
- Human indexes are curated reading paths, not exhaustive filesystem listings. Derived AI
  indexes may be exhaustive when they preserve role and status.

## Updating Knowledge During Work

- Search the relevant project knowledge before making product, gameplay, API, architecture,
  terminology, lore, or design assumptions.
- Small accepted changes may update the destination document and decision log directly.
- Parallel workers append only to their own task logs; a coordinator or grooming pass
  serializes destination-document changes.
- Update current documents only after the behavior or decision is accepted for their stated
  applicability.
- Update an initiative's delivery snapshot when implementation, source-control availability,
  deployment, verification, or a live external artifact crosses a meaningful gate.
- Record what changed, why, affected projects or code paths, and evidence.
- If implementation and current knowledge disagree, report the mismatch before choosing
  which one to change.
- Before moving, consolidating, archiving, or deleting an active initiative, consult its active
  owner/task context and inspect linked implementation or source-control evidence. Repository
  contents alone cannot prove that off-repository design work, a branch, or a Perforce shelf is
  inactive or disposable.
- Explicitly record `no durable knowledge` in the agent/task context when no repository update
  is warranted; do not create a file solely to record that fact.

### Acceptance And Progression Signals

Acceptance is scoped to the immediately preceding bounded deliverable or checkpoint. Explicit
approval such as `approved`, `go with that`, or `looks good` is acceptance within that scope.
After the owner has been presented with or reviewed a bounded result, an instruction such as
`continue`, `proceed`, or `let's work on the next step` is progression acceptance: the current
result is good enough to become the baseline for the named next phase unless the owner qualifies
the instruction.

Progression acceptance may authorize an agent that owns incorporation to:

- update an initiative checkpoint or delivery gate;
- incorporate accepted design or current-state changes for the stated applicability;
- record a concise curated decision when direction changed materially; and
- begin the next approved design or implementation phase.

It does not by itself establish that:

- every open question or later initiative slice is approved;
- implementation exists or review and verification succeeded;
- a Git commit, merge, Perforce shelf, or submit exists; or
- any environment received a deployment.

Do not infer acceptance from silence, age, a topic change, an abandoned task, or an agent choosing
its own next action. If the bounded subject or consequence is materially ambiguous, preserve the
entry as pending or ask the owner. At an accepted phase transition, check whether current-system
knowledge, the initiative delivery snapshot, a material decision, or task-entry dispositions
actually changed. Do not create a decision entry merely because routine work continued.

## Project-Specific Boundaries

### Ascent Rivals

- `system/` defaults to Cliff's known local-development state.
- Eventun, Accountun, Ascentun, Cardanoun, and the Unreal client are implementation surfaces
  of the Ascent Rivals product; implementation-repository identity does not create separate
  top-level knowledge projects.
- Midnight and Cardano belong under Ascent Rivals while the subject is their game integration.
- Current game terminology, mechanics, and contracts in `system/` outrank unincorporated
  initiative drafts.
- Production claims require explicit deployment or live-environment evidence.

### Knowledge Base

- Root `ORGANIZATION.md` and `AGENTS.md` are current policy.
- `knowledge-base/system/` contains narrower current repository policy and machine-path
  boundaries.
- The federated personal/canonical workflow remains an initiative until the manual structure
  has been exercised and the `kb` tool is implemented.
- Completed migration plans and ledgers belong in the knowledge-base archive.

## Validation

Run the repository validator after structural, indexing, metadata, or link changes:

~~~sh
python tools/validate_kb.py
~~~

Use `python tools/validate_kb.py --strict` when warnings should fail validation. The validator checks
required indexes, project-role boundaries, initiative status, task-log metadata, duplicate
stable identifiers, internal Markdown/wiki links, stale verification metadata, and archive
links from default reading indexes.

Validation catches mechanical drift. It cannot determine whether two claims are semantically
compatible, whether an implementation is accepted, or whether a feature is deployed.

## Template Extraction Boundary

Do not extract the reusable contributor template merely because this policy exists. First use
the structure during ordinary direct work, coordinated feature work, and at least one
parallel-task feature. Record classification friction and change this policy before copying it
into a baseline template. Machine-local paths, personal project content, and repository-source
authority must not enter that template.
