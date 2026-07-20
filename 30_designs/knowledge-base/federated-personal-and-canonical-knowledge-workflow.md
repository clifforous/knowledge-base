# Federated Personal and Canonical Knowledge Workflow

## Status

Proposed.

The repository restructuring and a period of normal use under the new structure should
precede implementation of the kb tool. This document defines the intended direction so
the restructuring can preserve the boundaries and metadata the future tool will require.

## Problem Statement

Project knowledge currently accumulates primarily in one personal Markdown repository.
That repository is effective for AI-assisted work because it is local, searchable,
reviewable, and stored in a simple format. It is not yet designed for:

- multiple contributors maintaining independently authored knowledge
- agents consulting other contributors' knowledge without gaining write access
- explicit promotion of reviewed knowledge into a shared canonical source
- consistent use from Codex, Claude Code, and Cursor
- automatic capture and synchronization without requiring contributors to remember a
  separate documentation or Git workflow

Most intended contributors use Perforce for product development and do not otherwise need
Git in their daily workflow. Any solution that makes contributors manage clones, branches,
commits, pushes, or merge conflicts directly is unlikely to be adopted consistently.

## Context

The expected initial environment is heterogeneous:

| Contributor profile | Primary environment | Secondary environment | Primary agent |
|---|---|---|---|
| Knowledge-base owner | Arch Linux under WSL | Windows for Unreal Editor and general Unreal work | Codex and Cursor |
| Initial pilot coworker | Linux with Nix tooling | Dual-boot Windows | Claude Code |
| Additional coworkers | Windows | Unknown | Primarily Cursor |

The game-client workspace is distributed through Perforce. The personal and canonical
knowledge repositories are expected to use Git. Initial onboarding may require Git to be
installed, but routine Git use must be hidden behind the proposed tooling.

## Workflow Variability

The collaboration model must not assume that contributors organize agent work in the same
way.

The knowledge-base owner commonly uses a coordinated feature workflow:

1. Describe a problem or feature and request guidance.
2. For larger work, perform questions and answers and produce a small design.
3. Derive a high-level implementation plan when the design requires one.
4. Keep a main coordinating task that generates task prompts for coder agents.
5. Reuse one coder task per affected project so that task accumulates project and feature
   context.
6. Review each implementation increment in the main task or through a review-team
   workflow.
7. Generate feedback for the coder and repeat implementation and review until acceptable.
8. Manually test and inspect the result.
9. Commit or submit the accepted feature.
10. Update durable knowledge before deployment and development-environment testing.

Smaller fixes, cleanup, and simple features may instead be completed in one task within
the affected project. Other contributors may primarily use a single conversation in which
they describe a problem and iteratively work through it.

The kb workflow must support all of these shapes:

| Workflow shape | Capture behavior |
|---|---|
| Coordinated multi-agent feature | Each worker, reviewer, and coordinating task appends to its own decision/delta log. The coordinating task may incorporate accepted entries after review, validation, and commit; unresolved logs remain for grooming. |
| Single-session iterative work | The same agent records meaningful decisions and deltas in one task log. Current-system incorporation may happen in that task when acceptance is explicit or during later grooming. |
| Small direct task | The project task records only the durable decision or behavioral delta. It may incorporate it immediately when completion is clear. |
| Large design with multiple features | Related task logs share a parent feature identifier and can be groomed or incorporated independently as features become real. |

The invariant is not a prescribed task sequence. The invariant is that potential knowledge
is first recorded in a task-owned log, current-system documents change only through
explicit incorporation or grooming, and every durable update retains its evidence and
authorship.

## Goals

1. Preserve durable decisions, current system understanding, constraints, terminology,
   and corrections in a contributor-owned personal knowledge base.
2. Allow agents and people to consult canonical knowledge and other contributors'
   knowledge while designing, implementing, reviewing, or investigating work.
3. Allow an authorized leader to explicitly review candidate knowledge, resolve
   conflicts, and promote accepted results into a shared canonical knowledge base.
4. Keep personal and canonical repositories human-readable as ordinary Markdown.
5. Make normal capture, commit, push, pull, and indexing behavior require no recurring
   human action.
6. Support Codex, Claude Code, and Cursor through a common integration boundary.
7. Preserve the same content structure in personal and canonical repositories so canon
   can seed a new personal repository and personal material can be promoted without a
   format conversion.
8. Adapt capture, incorporation, and grooming behavior to single-session, coordinated
   multi-agent, and mixed contributor workflows without requiring contributors to adopt
   a standard agent process.
9. Distinguish a contributor's local-development understanding from shared development,
   staging, and production truth.
10. Track multi-project feature rollout explicitly so partial deployments and rollbacks do
    not make the shared knowledge base overstate what is live.

## Non-Goals

- Replacing Perforce for product source control.
- Introducing project-management, ticketing, approval-board, or meeting workflows.
- Making every implementation step, task list, prompt, transcript, or investigation log
  durable.
- Treating any agent vendor's private memory feature as the shared system of record.
- Automatically promoting personal knowledge into canon.
- Allowing leaders or agents to silently rewrite another contributor's personal
  knowledge.
- Implementing the kb tool before the reorganized repository has been exercised in
  normal work.
- Providing cryptographic protection from organization administrators. Repository
  ownership and role configuration provide the intended collaboration boundary.
- Standardizing how contributors plan, delegate, review, test, or commit product work.
- Storing every task prompt or agent transcript as knowledge.
- Inferring production state merely because code was committed, submitted, merged,
  reviewed, or incorporated into canon.

## Design Principles

### Personal authorship is preserved

Each contributor has a distinct personal repository. It represents that contributor's
current understanding and decisions, including material that has not been accepted into
canon.

Other contributors and their agents may read it but do not write it. Canon review may
produce a correction request or rejection record, but the origin contributor remains
responsible for changing the personal source.

### Canon is explicit

Normal capture updates only the contributor's personal repository. Canon changes occur
only through an explicit review initiated by an authorized maintainer.

### Markdown is the durable representation

Markdown files, links, small indexes, and minimal machine-readable front matter remain the
portable source format. Search indexes, caches, and embeddings are derived artifacts and
can be rebuilt.

### Current truth is glanceable and evidence remains traceable

High-value system documents and indexes should reveal information in attention layers:
applicability and verification status, a concise current-state summary, detailed behavior,
then links to decisions, task logs, and sources. The current synthesis is rewritten when
accepted evidence changes; its supporting evidence remains append-oriented and addressable.

This is a selective convention, not a requirement to decorate or repeatedly summarize
every file. It should be applied where a reader or agent needs a fast, reliable answer while
retaining a path to the history and evidence behind it.

### Git is storage infrastructure, not a contributor workflow

Git provides history, transport, review, and recovery. The kb integration performs
ordinary synchronization and commit operations. Contributors should not need to learn or
remember Git commands for normal use.

### Agents receive capabilities, not broad filesystem access

Agents do not directly edit a knowledge repository outside their product workspace. They
use narrowly scoped kb tools that enforce source identity and write boundaries.

### Capture and promotion are separate operations

Durable personal capture should be automatic during normal work. Canon promotion remains
deliberate because it requires comparison, conflict resolution, and accountable judgment.

### Task decision logs and current truth are separate

Parallel tasks may discover useful facts before their implementations are accepted.
Those facts should be recorded in task-scoped decision/delta logs rather than immediately
rewriting current-system documents.

Task logs are durable evidence and history, not assertions of current truth. An explicit
incorporation or grooming step consolidates applicable entries into current knowledge. A
proposed design may be saved earlier as an explicitly proposed artifact, but it must not
be presented as implemented behavior.

### Workflow adaptation is configuration, not policy duplication

Onboarding records a small workflow profile that determines when capture checks,
incorporation suggestions, and grooming reminders occur. Knowledge categories, source
roles, and acceptance rules remain common across profiles.

### Canonicality and deployment are separate

Canonical knowledge is team-reviewed and shared. Production knowledge describes what is
actually deployed to a production environment. A feature can be canonical while still
being limited to local development, integrated source, a shared development environment,
or staging.

Production status requires an explicit deployment record. Source-control state, personal
knowledge, and canon adoption do not imply production.

### Personal knowledge defaults to local-development applicability

A personal knowledge base primarily reflects the contributor's current local-development
understanding. It may be ahead of shared development and production and may contain work
that is later abandoned.

Personal documents and task logs should therefore default to local-development
applicability unless they cite a shared environment or production deployment record.

## Repository Model

The initial hosted topology should use organization-owned private repositories:

~~~text
knowledge-template
knowledge-cliff
knowledge-<contributor>
knowledge-canon
knowledge-tooling
~~~

knowledge-template defines the common repository structure, schemas, indexes, and agent
guidance. A new personal repository should be created from the template rather than as a
fork of canon. Fork relationships add upstream and branch semantics that are unnecessary
for this workflow.

The current personal knowledge base should become the source used to create
knowledge-template only after:

1. the repository has been reorganized
2. the new boundaries and indexes have been used during normal work
3. personal or machine-specific material has been separated from reusable structure
4. generated, transient, and obsolete material has been excluded

Personal and canonical repositories should carry a small root manifest:

~~~yaml
schema: 1
kind: personal
owner: cliff
~~~

Canon uses the same schema with kind: canon. Template repositories use kind: template and
omit a concrete owner.

## Access Model

Expected repository roles:

| Repository | Repository owner | Knowledge readers | Canon maintainers |
|---|---|---|---|
| Personal | Write | Read | Read |
| Canon | Read | Read | Write |
| Template | Maintainer-controlled | Read | Maintainer-controlled |
| Tooling | Maintainer-controlled | Read | Maintainer-controlled |

Normal kb tools must additionally enforce these boundaries:

- Personal capture writes only to the configured personal repository.
- Peer, canon, Notion, and other imported sources are read-only.
- No normal MCP tool accepts an arbitrary repository path.
- Canon write operations are absent from the normal contributor tool set.
- Canon preparation and canon publication are separate operations.

## Agent Integration Architecture

The common integration boundary is a local kb program that exposes Model Context Protocol
tools. Codex, Claude Code, and Cursor use client-specific configuration but call the same
logical API.

~~~text
Codex --------\
Claude Code ---+--> kb MCP interface --> personal repository (read/write)
Cursor --------/           |
                           +-----------> canon and peer repositories (read-only)
                           +-----------> optional Notion source (read-only)
                           +-----------> local search index and synchronization state
~~~

The kb process, rather than the agent's general shell or filesystem tools, owns access to
the knowledge repositories. This provides a narrow exception to agent workspace
sandboxing without granting arbitrary access outside the product workspace.

The initial implementation may use a local stdio MCP process. An always-running local
service is not required for the first version. Repository operations should use a lock so
multiple clients on one machine cannot mutate the same clone concurrently.

## Proposed Tool Surface

### Normal contributor tools

| Tool | Behavior |
|---|---|
| kb_status | Reports identity, source roles, synchronization state, configured hooks, and pending operations. |
| kb_search | Searches personal, canonical, peer, and optional external sources with source attribution. |
| kb_read | Reads a specific indexed document or decision record. |
| kb_begin_work | Creates or resumes a task-owned decision/delta log and associates it with an optional parent feature. |
| kb_capture | Appends a structured decision, delta, finding, correction, or open question to the calling task's log. |
| kb_close_work | Optionally marks a task log completed, abandoned, or superseded when that state is known. |
| kb_incorporate | Incorporates selected accepted log entries into durable current-system or design documents. |
| kb_groom | Reviews open and stale task logs and proposes incorporation, continued activity, rejection, supersession, or archival. |
| kb_no_capture | Records that the agent completed the end-of-turn knowledge check and found no durable change. |

kb_capture should append structured entries rather than arbitrary prose or file writes.
Expected fields include:

- project or domain
- parent feature and work-stream identifiers
- contributing task or session identifier
- agent role, such as coordinator, coder, reviewer, or direct worker
- capture type
- stable subject key
- current truth or decision
- rationale
- evidence and affected code or project paths
- intended applicability, defaulting to local development
- implementation references such as Git commits or Perforce changelists
- related documents
- superseded knowledge, when applicable

Capture types should initially be limited to:

- decision
- current-system delta
- durable finding
- contract or terminology change
- durable constraint
- correction
- open question that materially blocks or qualifies a decision
- durable external-source adoption

### Task decision-log model

Each agent task owns one append-oriented log. A coordinating task, a coder task reused for
a project, and a review task therefore write different files even when they contribute to
the same parent feature.

A conceptual log contains:

~~~yaml
task_id: stable-client-or-kb-task-id
parent_feature: optional-feature-id
project: ascent-rivals
agent_role: coordinator
status: open
applicability: local-development
last_activity: 2026-07-19
~~~

Each entry should have its own stable identifier, timestamp, type, state, concise statement,
rationale, evidence, and related projects or documents. An entry should normally express
one decision, delta, correction, or material open question so another document can address
it directly. Atomicity applies to the entry, not the file: keeping all entries for one task
in its task-owned log avoids a file-per-fact explosion and preserves parallel write
ownership. Entry states should include:

- pending
- incorporated
- rejected
- superseded
- informational

Task status should include:

- open
- completed
- abandoned
- superseded
- unknown

Unknown and stale are not equivalent to abandoned. Staleness is only a reason to include
the log in a grooming review.

The log is not a task diary. It excludes prompts, full transcripts, detailed execution
steps, routine review feedback, and build output. It records only decisions and deltas
that may matter after the task context disappears.

### Canon tools

Canon capabilities should be exposed only to authorized maintainers:

| Tool | Behavior |
|---|---|
| kb_prepare_canon | Compares selected personal changes with current canon and produces a review proposal. |
| kb_publish_canon | Applies an approved proposal through the configured canon review mechanism. |
| kb_record_canon_disposition | Records acceptance, rejection, deferral, or a required origin correction. |
| kb_record_deployment | Records component versions deployed to a named environment and updates the shared feature ledger. |
| kb_record_rollback | Records a rollback or removal and restores the correct environment view. |

kb_publish_canon must require explicit invocation. It must not be called by an automatic
end-of-turn hook. Deployment and rollback tools must likewise require an authenticated
release context or an explicit authorized invocation.

## Knowledge Capture Lifecycle

### Context retrieval

Before making a product, gameplay, API, architecture, terminology, or design decision, the
agent should search:

1. canon
2. the contributor's personal knowledge
3. relevant peer knowledge
4. optional external sources such as Notion

Results must retain source identity. Personal or peer knowledge does not become canonical
merely because it was returned by a search.

### Capture during work

The active agent has the best context for determining what became durable. Project
instructions should require it to call kb_capture when work may establish or change:

- user-visible behavior
- gameplay rules
- API or data contracts
- architectural ownership
- stable terminology
- an approved design decision
- an important correction to existing knowledge

Worker and reviewer tasks may contribute log entries throughout a feature without editing
the destination documents. Each contribution appends to the calling task's own log. Tasks
must submit concise facts and evidence, not their prompts, reasoning transcripts, task
lists, or complete implementation histories.

The agent should call kb_no_capture when the session contains no durable knowledge.
Examples that normally do not warrant capture include:

- implementation plans
- task tracking
- build or test output
- routine mechanical refactoring
- prompts and transcripts
- speculative investigation that reached no durable conclusion

### Optional completion and direct incorporation

An entry in a task decision log does not assert that product behavior has changed. When
completion and acceptance are explicit, the coordinating or direct task may incorporate
selected entries immediately.

Supported completion signals should include:

- explicit completion: the user or coordinating task says the work is accepted
- source-control completion: the relevant commit, changelist, or submit is confirmed
- explicit abandonment or supersession
- no reliable signal: leave the log open for later grooming

The coordinated feature profile should incorporate only after explicit or source-control
completion. The coordinating task gathers applicable entries after implementation review,
feedback iterations, manual testing, and code inspection. Rejected iterations remain in
the audit log as rejected or superseded rather than becoming current behavior.

The single-session profile may incorporate entries in the same task when the agent has
clear evidence that the result was accepted. If acceptance is unclear, the log remains
open. The system must not require a task to declare itself complete because users may
leave a line of work dormant or abandon it without an explicit closing action.

Direct incorporation should:

1. select accepted entries from the relevant task logs
2. discard duplicates and identify contradictions
3. re-read the latest destination documents
4. update decisions, proposed designs, or current-system knowledge according to their
   actual status
5. record evidence and affected projects
6. mark each entry as incorporated, rejected, superseded, informational, or still pending

### Grooming

Grooming is the normal recovery path for work that was never explicitly completed,
incorporated, or abandoned.

A grooming pass should:

1. collect open logs, stale logs, and entries not yet dispositioned
2. group them by project, parent feature, subject, and likely destination document
3. compare entries with current personal knowledge and, when needed, current
   implementation evidence
4. identify duplicates and conflicts across parallel tasks
5. propose one disposition per entry
6. update current-system or design documents only after the proposed disposition is
   accepted
7. update log entry states and task status without deleting the audit trail

Useful dispositions are:

- incorporate into named documents
- already represented
- keep open
- informational only
- rejected
- superseded
- abandoned with confirmation
- needs contributor judgment

Grooming may be invoked explicitly after a large feature, when beginning related work, or
on a low-frequency cadence. Automatic scheduling may prepare a grooming report, but it
must not infer that stale work was completed or abandoned and must not silently rewrite
current-system knowledge.

Each incorporated entry should retain a backlink to the task log and disposition that
produced it. Grooming should likewise update the source entry with the destination
document. This bidirectional traceability makes it possible to audit both coverage and
origin without preserving task transcripts.

Grooming should run as a bounded scan:

1. define the task-log scope and date or subject range
2. process entries in manageable batches
3. deduplicate against current documents and the running proposal
4. identify contradictions and unresolved applicability
5. verify that every proposed knowledge change cites at least one source entry
6. stop when the in-scope entries have dispositions, two passes find nothing new, or the
   configured time or iteration limit is reached
7. escalate remaining judgment calls rather than forcing completeness

The mechanical checks are coverage, backlinks, required metadata, duplicate identifiers,
and disposition state. Whether two statements are semantically compatible remains a
judgment call and must retain evidence.

### Knowledge hygiene

Grooming incorporates new task-log material. Knowledge hygiene separately checks whether
existing durable claims have drifted.

Environment-dependent claims should carry:

- last verified date
- verification source or method
- applicability
- verification result: verified, unverifiable-cheaply, drifted, or obsolete

Cheap deterministic evidence should be preferred, including repository paths, Git
references, Perforce changelists, build identifiers, deployment records, API contracts,
and live environment queries. An agent's recollection is not verification.

Unverifiable does not mean false, and stale does not mean obsolete. Verified corrections
may update factual text directly with an audit entry. Archival and deletion remain
proposal-only. Generic confidence scores must not override explicit deployment evidence
or applicability.

### End-of-turn audit

Client-specific lifecycle hooks should verify that relevant work ended with either
kb_capture, kb_close_work, kb_incorporate, or kb_no_capture as appropriate for the task
role and workflow profile.

A client Stop event is only the end of an agent response. It is not necessarily a task,
handoff, feature, or acceptance boundary. Hooks must not create a visible knowledge
bookkeeping turn after every response in a persistent coder, reviewer, or coordinator
task.

The hook should remain silent for ordinary progress reports, questions, plans, review
findings, and feedback iterations. It should audit when one or more of these conditions
apply:

- the agent claims its assigned work unit is complete
- the agent is handing results back to a coordinator
- the user accepts or rejects the work
- a configured commit, changelist, or submit boundary is confirmed
- the task or session is actually closing and contains uncaptured durable decisions or
  deltas

When an audit condition applies and no knowledge operation occurred, the hook may resume
the agent once with a concise knowledge check. A coder task should normally be reminded to
append its meaningful decisions or deltas, while a coordinator or direct task may also be
reminded that accepted entries can be incorporated. The hook must not require a completion
decision. Loop-prevention and per-work-stream throttling are required.

The hook is an audit and recovery mechanism; knowledge classification remains the active
agent's responsibility. When the client does not expose enough reliable lifecycle state,
the adapter should prefer a missed automatic audit over repeatedly interrupting normal
work.

Hook implementations are adapters because Codex, Claude Code, and Cursor use different
event schemas. Core capture and repository behavior must remain in kb.

### Persistence and synchronization

Task-log capture should be append-oriented and uniquely identified. It must not rewrite a
shared destination document. Logs are committed and synchronized so they survive across
the sessions that make up a work stream, but pending log entries must not be indexed or
presented as current truth.

After a successful log append, kb should validate the log, create a deterministic commit,
and attempt to push. After a successful incorporation or grooming application, kb should:

1. validate repository identity and write scope
2. update or create the appropriate Markdown artifact
3. update the source log entries with their dispositions
4. update affected indexes
5. validate required metadata and links
6. create a local Git commit with a deterministic message
7. attempt to push immediately

If the network is unavailable, the committed change remains in a local outbox and is
retried on the next invocation. Search operations refresh read-only sources when their
configured staleness threshold has elapsed.

Scheduled tasks are optional for retry, health reporting, and index maintenance. They are
not the primary mechanism for semantic capture.

Synchronization must fail safely:

- do not discard local commits
- do not silently resolve content conflicts
- do not push when repository identity or authorization is uncertain
- surface a concise unhealthy status while preserving a recoverable local state

### Parallel work and document coordination

Every capture should carry a stable work identifier and a unique entry identifier.
Parallel coder or reviewer tasks append entries to their own task logs. Because each task
owns a different file, normal capture does not produce document-level conflicts and tasks
do not open and rewrite the same current-system knowledge file.

kb_incorporate and application of an accepted grooming proposal are serialization points:

1. acquire the personal-repository write lock
2. refresh the current personal repository
3. load all selected entries from relevant task logs
4. re-read every affected destination document
5. consolidate and validate the update
6. update the entry dispositions
7. commit and push
8. release the lock

If another incorporation changed a destination document first, the later operation must
recompute against the new document. It must not use last-write-wins behavior. An unresolved
semantic conflict remains pending for the contributor, coordinator, or next grooming pass
to resolve.

This model permits immediate parallel commits to independent decision logs while
serializing the less frequent operation that changes actual knowledge. It also avoids
storing every task prompt or transcript in the knowledge base.

## Canon Review Lifecycle

Canon review begins only when a leader explicitly requests it.

1. Select one or more personal changes since the last reviewed watermark.
2. Compare the candidate facts and decisions with current canon.
3. Identify additions, compatible refinements, superseded canon, and conflicts.
4. Produce a reviewable proposal with source attribution.
5. Record a disposition for every candidate.
6. Publish accepted changes to canon.
7. Notify origin owners of rejected or conflicting personal material.

The review process may recommend cleanup in a personal repository but does not directly
perform that cleanup. The origin contributor or their agent applies the correction.

A person may seed a new personal knowledge base from canon, but subsequent personal
knowledge remains independently authored until promoted.

## Environment and Release Truth

### Independent state dimensions

The system must represent knowledge authority and deployment applicability independently.

| Dimension | Example states | Meaning |
|---|---|---|
| Knowledge authority | personal, canon | Who maintains the statement and whether it has passed shared review. |
| Work state | proposed, active, completed, abandoned, superseded, unknown | What is known about the task or feature lifecycle. |
| Deployment applicability | local-development, integrated, development, staging, production, retired, unknown | Where the behavior is known to apply. |

These states must not be collapsed into one status. In particular:

- personal does not mean unimplemented
- canon does not mean production
- completed does not mean deployed
- deployed to development does not mean deployed to production
- stale does not mean abandoned

Environment names should be configurable. The initial vocabulary may use development,
staging, and production, but the schema should not require every project to use all three.

### Default knowledge views

The default applicability of personal knowledge is local development. It describes the
contributor's working understanding, including accepted local changes that may not yet be
shared.

The shared canonical repository should provide distinct views:

- production system knowledge: the default authoritative answer for live behavior
- shared-development knowledge: accepted or observed behavior deployed to the common
  development environment
- adopted but not deployed features: reviewed knowledge pulled from personal repositories
  that has not reached a shared environment
- future initiatives and proposed designs: intentionally non-current material
- deployment history: an audit trail of environment transitions and rollbacks

A current-system document should either describe production or declare its environment
applicability prominently. Search and agent instructions must not silently combine local,
development, and production facts into one answer.

### Feature adoption

When canon review accepts relevant material from a personal repository, the shared
knowledge base should create or update a feature-adoption record. Adoption preserves:

- stable feature identifier
- originating personal repositories and task-log entries
- affected projects or deployable components
- accepted decisions and expected behavior
- implementation references known at adoption time
- current applicability per component
- destination canonical documents

Adoption initially means shared and reviewed. It does not mark any environment as
deployed.

### Component-level deployment ledger

Features may span multiple repositories and may be deployed at different times. Deployment
state must therefore be recorded per component rather than as one feature-wide boolean.

A conceptual shared feature record may contain:

~~~yaml
feature_id: post-match-insights
knowledge_state: canon
components:
  eventun:
    implementation: git-commit
    development: deployment-id
    production: deployment-id
  game-client:
    implementation: perforce-changelist
    development: build-id
    production: null
overall_production_state: partial
~~~

The overall feature state is derived from the required component matrix. A feature is
fully production only when every required component is recorded at the compatible
production version. Optional components and compatibility constraints must be explicit.

This prevents a backend deployment from making canon claim that an unreleased game client
feature is available, or the reverse.

### Deployment transition

A release or deployment task should explicitly notify the shared knowledge base:

1. identify the environment
2. identify the feature and affected components
3. record the deployed Git commits, Perforce changelists, build identifiers, configuration
   versions, or other release evidence
4. record deployment time and responsible release context
5. update the component-level ledger
6. update the applicable environment view
7. update production current-system documents only when production evidence is complete

The notification may eventually be called by release automation, but the first workflow
may use an explicit leader or release-agent command. A merge, commit, Perforce submit, or
canon incorporation is insufficient production evidence.

### Rollback and retirement

Rollback is also an explicit deployment event. It must:

- identify the environment and components rolled back
- restore the prior compatible environment view
- mark affected feature versions rolled back or retired
- retain the deployment and rollback history
- prevent superseded production knowledge from remaining the default answer

### Query behavior

Knowledge retrieval should respect the requested applicability:

- "How does this work?" defaults to canonical production knowledge when canon exists.
- "What am I currently building?" prefers the contributor's personal local-development
  knowledge and active task logs.
- "What is in development?" uses the shared-development view and deployment ledger.
- "What is coming next?" uses adopted-not-deployed features and proposed initiatives.
- "Why did this change?" uses decision logs, canon dispositions, and deployment history.

When the environment is unspecified and sources disagree, search results must label the
applicability rather than synthesizing one ambiguous answer.

Within the chosen applicability, the default lookup order should be:

1. the relevant current-system synthesis or index
2. linked decisions and incorporated task-log entries when rationale or corroboration is
   needed
3. unresolved task logs for explicitly local or in-progress questions
4. raw external sources when the knowledge base has a gap or the claim needs re-verification

A synthesized answer should cite the documents or entries it relies on and explicitly note
material gaps, stale evidence, and contradictions. Raw retrieval remains available when an
agent or human wants the underlying material rather than a synthesized answer.

## Notion Integration

Notion remains an optional source, not the canonical storage format for this workflow.

Expected behavior:

- search selected Notion content through an authenticated integration
- retain Notion page identity and retrieval time in citations
- allow an agent to explicitly adopt durable Notion content into its personal knowledge
- do not perform unrestricted bidirectional synchronization
- do not silently overwrite Markdown from a changed Notion page

Canon review may incorporate Notion evidence alongside personal repositories, but accepted
canon remains Markdown in the canonical repository.

## Instruction Distribution

The game-client Perforce workspace should carry a short tool-independent knowledge policy
in its root AGENTS.md. Cursor and Codex can consume that file directly. A root CLAUDE.md
should import it:

~~~md
@AGENTS.md
~~~

The shared policy should state:

- use kb rather than editing the knowledge repository directly
- search relevant knowledge before material decisions
- capture durable decisions and current-system changes
- exclude plans, tasks, prompts, transcripts, and routine logs
- complete an end-of-turn capture check
- append task-scoped decision/delta entries instead of directly rewriting knowledge from
  parallel worker tasks
- incorporate current-system knowledge only when acceptance is clear or a grooming
  proposal is approved
- treat personal knowledge as local-development knowledge unless stronger environment
  evidence is recorded
- never infer production from a commit, submit, merge, review, or canon incorporation
- record production deployments and rollbacks in the shared knowledge base
- require explicit authorization for canon promotion

User-global instruction files should contain only a small generated fallback for
configured projects that do not carry the shared policy. kb setup should install and
update that block rather than asking contributors to edit multiple global files manually.

## Platform Strategy

### Knowledge-base owner

The existing WSL repository should remain the single local writable clone during the
initial personal pilot.

- WSL agents invoke the Linux kb program directly.
- Windows agents may invoke the same WSL-hosted program through wsl.exe.
- Windows and WSL must not maintain simultaneous writable clones of the same personal
  repository.
- Unreal Editor and Windows-native coding remain unaffected because the integration
  boundary is MCP rather than a product-repository path.

### Linux/Nix and Windows dual-boot coworker

The primary installation should be packaged for the contributor's Linux/Nix
environment. A Windows installation may use a second clone of the same personal
repository because only one operating system is active at a time.

Each operating system requires its own local agent configuration, hook installation,
authentication, and clone. Remote synchronization reconciles the two environments.
kb setup should verify that pending local commits are pushed before treating another
installation as healthy.

### Windows coworkers

Windows installations should use a native kb executable and an application-data
directory outside the Perforce workspace. Client configuration should refer to the
installed executable and not to a contributor-specific absolute path checked into
Perforce.

### Git dependency

The first version may require a supported Git client to be installed and available to
kb. Setup must detect the version and fail with a clear remediation message.

A later self-contained distribution may embed or bundle Git behavior if installation
friction justifies it. That is an optimization, not a prerequisite for the pilot.

## Onboarding Design

### Administrator preparation

1. Create a personal organization repository from knowledge-template.
2. Grant the contributor write access and the knowledge-readers group read access.
3. Grant read access to canon and any approved peer repositories.
4. Configure shared environment names, deployable component identifiers, and required
   feature-component rules.
5. Publish the supported kb installer or package for the contributor's platform.

### Workflow bootstrap

Setup should ask only the questions that materially change automatic capture behavior:

1. How do you usually work with agents?
   - one ongoing conversation
   - a coordinating conversation with separate coder or reviewer tasks
   - a mixture of both
2. When do you usually know work has been accepted?
   - when I or my coordinating task explicitly say it is complete
   - after a commit, changelist, or submit is confirmed
   - it is often unclear, so leave the log for later grooming
3. Do you commonly run multiple agent tasks against the same project in parallel?
   - rarely
   - sometimes
   - often

These are configuration fields, not a rigid questionnaire. Setup should first ask the
contributor to describe how they normally use agents, infer all three values from that
answer, and confirm the interpretation. It should ask one concise follow-up only when a
material field remains unclear.

Client and operating-system questions should be detected where possible rather than
asked. The resulting profile changes reminders, task roles, direct-incorporation behavior,
and grooming presentation; it does not change repository permissions or the definition of
durable knowledge.

The initial recommended profiles are:

| Contributor style | Work profile | Incorporation default |
|---|---|---|
| Coordinated owner workflow | mixed with coordinator and worker roles | incorporate after explicit or source-control completion; groom unfinished logs |
| Single-prompt coworker workflow | single-session | write the task log; incorporate only with a clear acceptance signal |
| Unknown workflow | mixed and conservative | write task logs and rely on grooming for current-system updates |

### Contributor experience

The intended contributor workflow is:

1. Install Git if setup reports that it is missing.
2. Install kb.
3. Run kb setup.
4. Authenticate in a browser.
5. Accept the agent client's one-time MCP and hook trust prompts.
6. Run a bootstrap verification prompt.

kb setup should:

- identify the contributor and device
- locate installed Codex, Claude Code, and Cursor clients
- configure only the detected or selected clients
- clone the personal repository into private application data
- configure canon and peers as read-only sources
- load the shared environment and deployable-component configuration
- install the appropriate lifecycle-hook adapters
- install or update the small global instruction block
- record the workflow profile and incorporation behavior
- configure low-frequency, non-blocking grooming reminders
- initialize the local search index
- run kb doctor

No normal onboarding step should ask the contributor to fork a repository, add a remote,
create a branch, commit, or push.

### Bootstrap verification

The standard verification prompt should make no durable changes:

~~~text
Validate my knowledge-base integration without changing product or knowledge files.

1. Call kb_status.
2. Search canon and my personal knowledge for "Ascent Rivals".
3. Perform a dry-run kb_capture for a harmless test fact.
4. Report:
   - which source is my writable personal knowledge base
   - which sources are read-only
   - my workflow profile and incorporation behavior
   - the number of task logs currently awaiting grooming
   - the configured shared environments
   - which source answers production questions by default
   - whether synchronization is healthy
   - whether the end-of-turn capture hook is active
~~~

## Rollout Sequence

### Stage 1: Repository restructuring

Reorganize the current personal knowledge base, establish clear current-system,
initiative, decision, source, archive, and transient-work boundaries, and add useful
human and AI indexes.

### Stage 2: Manual workflow validation

Use the new structure during normal work without implementing kb. Identify which
documents agents reliably find, which captures are valuable, and where classification
boundaries remain ambiguous. Exercise coordinated feature work, direct small tasks, and
at least one parallel-task feature so the future decision-log and grooming model reflects
actual practice.

### Stage 3: Personal kb pilot

Implement the smallest local tool surface for the knowledge-base owner. Validate WSL and
Windows agent access, automatic capture auditing, Git synchronization, and failure
recovery.

### Stage 4: One-coworker pilot

Onboard the willing Claude Code coworker on Nix/Linux. Add the Windows dual-boot
installation only when needed. Evaluate setup time, capture quality, and whether the
workflow remains unobtrusive.

### Stage 5: Canon review pilot

Run canon review with two personal repositories. Adopt one multi-project feature, record
its development deployment, and exercise a partial production deployment and rollback.
Establish practical conflict, disposition, and environment-transition rules before
onboarding more contributors.

### Stage 6: Broader rollout

Package Windows onboarding for Cursor users and expand only after normal use requires no
Git knowledge or recurring reminders.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Agents capture transient implementation noise | Restrict capture types, provide negative examples, and audit early pilot commits. |
| Agents omit durable knowledge | Require capture-or-no-capture and use a one-shot Stop-hook audit. |
| Hooks differ or regress across clients | Keep small tested adapters and place core behavior in kb. |
| Parallel tasks rewrite the same document | Give each task its own append-oriented log and serialize incorporation under a repository lock. |
| Rejected implementation is recorded as current truth | Treat task logs as evidence, and require incorporation or approved grooming before updating current truth. |
| Open logs accumulate indefinitely | Surface a grouped grooming backlog by age and subject without treating staleness as abandonment. |
| Grooming invents coherence that the evidence does not support | Require source links for every incorporated claim, preserve contradictions, and escalate semantic uncertainty. |
| Environment-dependent facts become stale but continue to rank highly | Record verification metadata and run bounded hygiene checks against deterministic sources. |
| Canon adoption is mistaken for production | Track knowledge authority and deployment applicability independently. |
| A multi-project feature is only partially deployed | Record deployment per required component and derive an explicit partial state. |
| Production documentation drifts after deployment | Make deployment and rollback workflows update the shared environment ledger and affected production documents. |
| Workflow-specific automation annoys contributors | Ask three bootstrap questions and allow the workflow profile to be changed later. |
| Stop hooks interrupt every iterative response | Treat Stop as an audit opportunity, require a handoff or completion signal, and throttle by work stream. |
| Contributors must understand Git failures | Preserve an outbox, fail safely, and report actionable health status through kb_status. |
| Personal knowledge conflicts with canon | Preserve source identity and resolve only through explicit canon review. |
| Personal repositories become de facto canon | Search results label source kind and prefer canon when the user asks for authoritative behavior. |
| Dual-environment clones conflict | Prefer one writable clone per simultaneously active machine and verify synchronization during setup. |
| Broad MCP access bypasses sandbox intent | Expose narrow tools, fixed repositories, and no arbitrary path or Git command execution. |
| Notion and Markdown drift | Treat Notion as a cited read-only source and require explicit adoption. |
| The template preserves personal assumptions | Exercise the restructured personal repository before extracting the reusable template. |

## Validation Criteria

The design is ready for implementation planning when:

- the reorganized repository has been used successfully during ordinary work
- personal, canonical, initiative, decision, source, archive, and transient boundaries
  are unambiguous in practice
- the future template contains no machine-specific paths or personal-only content
- one contributor can be onboarded in approximately ten minutes
- onboarding requires no Git commands beyond installing Git when absent
- agents can search all permitted sources from a normal product workspace
- normal capture writes only the active contributor's personal repository
- parallel workers can commit independent task logs without editing the same destination
  files
- rejected work does not become current-system knowledge
- coordinated and single-session profiles both produce groomable decision logs and the
  same durable document model
- incorporated knowledge links back to its source task entries and those entries record
  their disposition
- grooming can stop with unresolved contradictions instead of manufacturing a conclusion
- environment-dependent claims distinguish verified, unverifiable, drifted, and obsolete
- stale or unknown task state does not cause automatic incorporation or abandonment
- personal knowledge defaults to local-development applicability
- canon adoption alone cannot mark a feature as production
- production status cites explicit deployment evidence for every required component
- partial deployments and rollbacks produce accurate environment-specific answers
- routine progress, review, and feedback turns do not trigger visible capture reminders
- commit and push occur without a recurring user action
- offline and conflict states preserve all local work
- canon cannot change without an explicit maintainer action
- the same bootstrap check works from supported Codex, Claude Code, and Cursor clients

## Open Decisions

- Exact root schema and index conventions after the knowledge-base restructuring.
- Exact task-log directory, filename scheme, front matter, and index structure.
- Grooming cadence and the least intrusive way to surface the backlog.
- Knowledge-hygiene cadence and which claim types justify live verification.
- Exact evidence required before source-control completion may permit direct
  incorporation.
- Shared environment names and the canonical location of their configuration.
- Feature and deployable-component identity across Git repositories, Perforce projects,
  builds, services, and configuration-only releases.
- How production deployment and rollback notifications integrate with existing release
  workflows.
- Whether production documents are materialized independently or generated as a view over
  base knowledge plus environment deltas.
- Whether the first kb version shells out to Git or uses an embedded Git library.
- Git hosting organization, authentication policy, and read-team membership.
- Canon proposal and approval representation: pull request, local review bundle, or both.
- How peer repositories are selected and refreshed when the number of contributors grows.
- Whether Notion retrieval is implemented directly by kb or delegated to each agent's
  existing Notion MCP integration.
- Packaging approach for Nix, native Windows, and WSL-to-Windows invocation.

## External Inspiration

### COG Second Brain

[COG Second Brain](https://github.com/huytieu/COG-second-brain) is a useful reference for
selected capture, consolidation, and verification patterns. It is not a candidate
dependency or baseline for this design.

Patterns worth adapting:

| COG pattern | Adaptation for this design |
|---|---|
| Captured sources are marked consolidated and backlink to the consolidation result. | Task-log entries receive explicit dispositions and bidirectional links to incorporated knowledge. |
| Consolidation scans a defined corpus, detects repetition and contradictions, deduplicates existing frameworks, and preserves evidence links. | Grooming scans scoped task logs, groups by subject, detects contradictions, and produces source-linked document updates. |
| Derived knowledge distinguishes emerging, working, and stable understanding. | Proposed or derived material may carry maturity, but maturity remains separate from deployment applicability and canonical authority. |
| Memory hygiene re-verifies environment-dependent claims and records last verification. | Existing paths, versions, contracts, and deployment claims are periodically checked against deterministic evidence. |
| Unverifiable claims are not automatically treated as wrong, and archival is proposed rather than silently performed. | Unknown, stale, and unverifiable states remain explicit and require evidence or confirmation before removal. |
| Iterative skills define verifiers, no-progress detection, hard caps, and human escalation. | Grooming and hygiene use bounded scans with mechanical coverage checks and explicit escalation for semantic judgments. |
| Onboarding infers settings from a natural workflow description and asks only for missing material information. | The kb bootstrap infers workflow profile, acceptance signals, and parallelism before asking a follow-up. |

Patterns intentionally excluded:

- general-purpose braindumps and daily journaling
- people CRM and progressive people profiles
- task, issue, release-note, and product-management workflows
- role packs, competitive watchlists, and news intelligence
- large collections of vendor-specific skills and worker agents
- broad integration and publishing automation
- a single vault that mixes raw personal intake, task management, and trusted product
  knowledge
- model-assigned confidence as a substitute for source, environment, or deployment
  evidence

COG's consolidation model is oriented toward finding personal patterns and producing
general frameworks. This design instead consolidates engineering decisions and observed
system deltas into environment-aware product knowledge. The reusable idea is the
source-to-consolidation lifecycle and its verification discipline, not COG's information
architecture or operating rituals.

### GBrain

[GBrain](https://github.com/garrytan/gbrain) contributes the clearest additional knowledge
model. Its Compiled Truth + Timeline pattern separates a rewritten current synthesis from
an append-only, cited evidence trail and weights the synthesis more heavily during search.
That maps directly to current-system documents plus decision and task-log evidence. The
design adopts the distinction without requiring both zones to live in one file.

GBrain also distinguishes raw retrieval from a synthesized, cited answer that identifies
staleness, contradictions, and missing knowledge. The query behavior above adopts that
contract and combines it with this design's environment and authority filters. Its
brain-first lookup protocol is useful as a default agent instruction, provided it does not
prevent code, deployment records, or external sources from re-verifying a claim.

Two further boundaries are useful: world knowledge should outlive any particular agent
configuration, and permission filtering must occur before retrieval or synthesis. This
supports a portable Markdown knowledge repository, machine-local agent instructions, and
read-only peer access. GBrain's database, vector and graph infrastructure, broad ingestion,
CRM-oriented schemas, daemon, and large skill surface are not required for the initial kb
workflow.

### GStack

[GStack](https://github.com/garrytan/gstack) is primarily a workflow and skill-distribution
reference, not a knowledge architecture. Explicit specialist modes and repo-local skill
packaging may inform later cross-client onboarding. Its automatic project-specific
operational learnings also suggest keeping agent/tooling lessons separate from product
truth. The specialist role pack and prescribed development lifecycle are intentionally not
adopted because contributors may use very different workflows.

### Zettelkasten

The useful Zettelkasten principles are stable addresses, small independently referenceable
ideas, explicit source references, and structure notes that act as curated entry points.
They support stable task-entry identifiers, concise single-purpose decisions, contextual
links, and human/AI indexes. The method's insistence that a Zettelkasten is personal also
supports keeping individual knowledge bases distinct from deliberately reviewed canon.

This design does not adopt one file per thought, graph-first navigation, or atomicity as a
rigid storage law. Product knowledge is often most understandable as a cohesive system
description; atomic entries serve as evidence that can be incorporated into that larger
description.

### PARA and Progressive Summarization

PARA's most relevant ideas are organizing active material close to the work it supports and
moving inactive material to an archive. The planned project-root structure, initiative
areas, and archive boundary obtain those benefits without importing a personal productivity
taxonomy or treating the knowledge base as a project manager.

Progressive Summarization contributes a stronger idea: preserve detail while making the
highest-value material progressively easier to scan, and add summarization only when the
material earns further attention. For this design that means concise current-state sections
and useful indexes above linked detail and evidence, not layers of bold and highlighted text
in every document.

### Getting Things Done

GTD's capture, clarify, organize, and reflect stages describe a useful hygiene loop for task
decision logs: capture durable deltas cheaply, clarify their meaning during incorporation,
place accepted knowledge in the correct system document, and periodically review the open
backlog. The knowledge workflow stops there. It does not adopt GTD action lists, calendars,
projects, or the instruction to capture everything; prompts, routine execution, and transient
tasks remain outside the durable knowledge base.

## References

- [COG Second Brain repository](https://github.com/huytieu/COG-second-brain)
- [COG knowledge-consolidation skill](https://github.com/huytieu/COG-second-brain/blob/main/.claude/skills/knowledge-consolidation/SKILL.md)
- [COG memory-hygiene skill](https://github.com/huytieu/COG-second-brain/blob/main/.claude/skills/memory-hygiene/SKILL.md)
- [COG loop-engineering reference](https://github.com/huytieu/COG-second-brain/blob/main/.claude/skills/loop-engineering/SKILL.md)
- [COG onboarding skill](https://github.com/huytieu/COG-second-brain/blob/main/.claude/skills/onboarding/SKILL.md)
- [GBrain repository](https://github.com/garrytan/gbrain)
- [GBrain Compiled Truth + Timeline guide](https://github.com/garrytan/gbrain/blob/master/docs/guides/compiled-truth.md)
- [GBrain agent-repository versus brain-repository guide](https://github.com/garrytan/gbrain/blob/master/docs/guides/repo-architecture.md)
- [GStack repository](https://github.com/garrytan/gstack)
- [GStack skill guides](https://github.com/garrytan/gstack/blob/main/docs/skills.md)
- [Zettelkasten Method introduction](https://zettelkasten.de/introduction/)
- [Forte Labs PARA method](https://fortelabs.com/blog/para/)
- [Forte Labs Progressive Summarization](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- [Getting Things Done fundamentals](https://gettingthingsdone.com/what-is-gtd/)
- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Claude Code Model Context Protocol](https://code.claude.com/docs/en/mcp)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Cursor rules and AGENTS.md](https://docs.cursor.com/context/rules-for-ai)
- [Cursor Model Context Protocol](https://docs.cursor.com/context/model-context-protocol)
- [Cursor agent hook example](https://cursor.com/blog/agent-best-practices)
- [GitHub repository roles for organizations](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)
- [GitHub repository templates](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [Notion Model Context Protocol](https://developers.notion.com/guides/mcp/overview)
