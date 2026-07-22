# Federated Personal And Canonical Knowledge Workflow

Status: proposed workflow design

Last revised: 2026-07-21

## Document Role And Status

This document defines the intended contributor experience, knowledge lifecycle, canon model,
and design rationale for the future `kb` workflow.

- [Requirements](requirements.md) define what the tool must do and how it is accepted.
- [System design](system-design.md) defines how the local executable, MCP interface, repositories,
  search, synchronization, client adapters, and packaging should work.
- [ORGANIZATION.md](../../../ORGANIZATION.md) remains authoritative for the current manual
  repository structure, placement, task-log, lifecycle, and validation rules.

Repository restructuring and governance are implemented. Manual workflow validation is still
active, so this initiative may change as ordinary design, implementation, review, and testing
work exposes friction. Tool implementation remains deferred until that checkpoint closes.

## Problem Statement

Project knowledge currently accumulates primarily in one personal Markdown repository. It works
well for AI-assisted development because it is local, searchable, reviewable, portable, and
readable without a special application. It does not yet provide a simple team workflow for:

- independently authored personal knowledge;
- read-only consultation of coworkers' knowledge;
- explicit review and promotion into shared canon;
- consistent access from Codex, Claude Code, and Cursor;
- capture from sandboxed project workspaces; or
- routine Git persistence without requiring contributors to remember a documentation or Git
  ritual.

Most intended contributors use Perforce for product development and do not otherwise need Git.
Automatic synchronization must therefore hide clones, branches, commits, pushes, pulls, and
ordinary recovery. A hands-on contributor may instead select manual-remind and keep ownership of
their normal Git workflow without making that the team onboarding default.

## Initial Contributor Context

| Contributor profile | Primary environment | Secondary environment | Primary agent |
|---|---|---|---|
| Knowledge-base owner | Arch Linux under WSL | Windows for Unreal Editor and general Unreal work | Codex and Cursor |
| Initial pilot coworker | Linux with Nix tooling | Dual-boot Windows | Claude Code |
| Additional coworkers | Windows | Unknown | Primarily Cursor |

The game-client workspace remains in Perforce. Personal and canonical knowledge use Git as hidden
storage infrastructure. Initial onboarding may require Git installation, but routine use should
not require Git knowledge.

## Workflow Variability

The collaboration model must not assume that contributors organize agent work alike.

The knowledge-base owner commonly uses a coordinated feature workflow:

1. Describe a problem or feature and request guidance.
2. For larger work, answer design questions and produce a small solution design.
3. Produce a high-level implementation plan only when the design needs one.
4. Keep a coordinating agent task and reuse one coder task per affected implementation project.
5. Review each increment in the coordinating task or through an independent review workflow.
6. Return feedback to the coder and repeat until the increment is acceptable.
7. Manually test and inspect the result.
8. Commit or submit the accepted feature.
9. Incorporate durable changes into the personal knowledge base.
10. Deploy and test separately in a shared environment.

Small fixes, cleanup, and simple features may instead use one agent task within the affected
project. Other contributors may use one continuing conversation for nearly all work.

The workflow supports these shapes without prescribing their task sequence:

| Workflow shape | Capture behavior |
|---|---|
| Coordinated multi-agent feature | Each worker, reviewer, and coordinator writes its own task decision/delta log. The coordinator may incorporate accepted entries after review and acceptance; unresolved entries remain for grooming. |
| Single-session iterative work | One agent records meaningful decisions and deltas in its task log. It may incorporate them when acceptance is clear or leave them for grooming. |
| Small direct task | The project task records only the durable decision or behavioral delta and may incorporate it directly when completion is clear. |
| Large design with multiple features | Related task logs share a parent feature id and can be incorporated independently as individual features become real. |

The invariant is that parallel potential knowledge enters task-owned evidence, accepted current
documents change only through a serialized incorporation or grooming step, and every durable
update retains source and authorship.

## Desired Contributor Experience

After one-time setup, a contributor should be able to work normally in a product repository:

1. Their agent automatically has access to the configured `kb` MCP tools.
2. The agent searches relevant canon, personal, and permitted peer knowledge before making
   material assumptions.
3. The active task records only durable decisions and deltas as they become clear.
4. `kb` reports personal synchronization state. Automatic mode commits and attempts to push;
   manual-remind mode leaves Git untouched and provides a throttled reminder.
5. The contributor is interrupted only when a meaningful work boundary appears to have missed a
   knowledge check or when synchronization needs human recovery.
6. When the agent client closes, no knowledge service remains running in the background.
7. A later invocation retries recoverable Git or index work without requiring a daily routine.

No contributor should have to remember to open a knowledge repository, edit an index, or run a
scheduled consolidation. Automatic-mode contributors also do not need to remember Git. A
manual-remind contributor deliberately retains Git ownership and receives an unsynchronized-change
reminder rather than hidden staging, commits, or pushes. All contributors remain responsible for
semantic acceptance, genuine conflicts, and explicit canon or deployment actions.

Setup may offer a hybrid-read profile for contributors who prefer agents to browse the raw
Markdown clones with native file and search tools. The contributor enables that capability; the
agent does not. MCP remains available for attributed retrieval and is the only supported capture,
incorporation, and canon mutation path. Personal Git persistence follows the selected
synchronization profile, so using hybrid reads does not fork the knowledge workflow.

## Design Principles

### Personal authorship is preserved

Each contributor owns a distinct personal repository representing that contributor's current
understanding and decisions, including material not accepted into canon. Others may read it but
do not write it. A canon review may request a correction; the origin owner applies it.

### Canon is explicit

Normal capture updates only personal knowledge. Canon changes only through an explicit review
initiated and published by an authorized maintainer.

### Markdown is durable; tooling state is derived

Markdown files, links, curated indexes, and minimal metadata remain the durable representation.
Search indexes, caches, operational state, and client configuration may be rebuilt and must not
be required to read the knowledge.

### Current truth is glanceable and evidence remains traceable

High-value documents should reveal information in attention layers: applicability and status, a
concise current-state summary, detailed behavior, then linked decisions and evidence. Accepted
current synthesis is rewritten when truth changes; supporting decision and task evidence remains
append-oriented and addressable.

This is selective. It does not require repeated summaries or dense metadata in every file.

### Git is infrastructure, not contributor workflow

Git provides history, transport, recovery, and review. Automatic mode performs routine operations
for contributors who do not use Git. Manual-remind mode exists for hands-on contributors who
already prefer to stage, describe, commit, and push their own changes.

### Agents receive explicit capabilities

Every installation provides fixed, narrowly scoped MCP tools. A contributor may additionally
authorize native read-only access to the Markdown clones when that is smoother in their client.
Personal mutations and source boundaries still pass through `kb`; direct folder access is not a
supported write path. Strict installations can remain MCP-only.

### Capture and promotion are separate

Personal capture should be cheap during ordinary work. Canon promotion remains deliberate because
it requires comparison, conflict resolution, and accountable judgment.

### Task evidence and current truth are separate

Parallel tasks may discover useful facts before implementation is accepted. They append those
facts to task-owned decision/delta logs rather than immediately rewriting current-system
documents. Pending evidence is not current truth.

### Workflow adaptation is configuration, not policy duplication

A small workflow profile changes audit timing, role defaults, direct-incorporation suggestions,
and grooming presentation. It does not create different knowledge categories or acceptance rules
for each contributor.

### Authority, source control, and deployment are independent

Personal or canonical authority does not establish implementation. A working copy, Git commit,
Perforce shelf, submit, or merge does not establish deployment. Development deployment does not
establish production. Retrieval preserves all of these boundaries.

### No autonomous semantic process

The local executable performs deterministic storage, retrieval, validation, and synchronization.
It does not run its own model or scheduled semantic process. Classification, incorporation prose,
conflict resolution, and canon judgment use the active agent task or a human review.

## Knowledge Topology

The expected hosted topology is:

~~~text
knowledge-template
knowledge-cliff
knowledge-<contributor>
knowledge-canon
knowledge-tooling
~~~

`knowledge-template` defines common repository shape, schemas, indexes, and agent policy. New
personal repositories should start from the template rather than fork canon; a fork relationship
adds upstream semantics the workflow does not need.

The current repository may become the source for the template only after:

1. the reorganized boundaries have been used in ordinary work;
2. manual capture and incorporation have exercised direct and parallel workflows;
3. personal and machine-local material is separated from reusable structure; and
4. obsolete, transient, and generated material is excluded.

Repository identity and access are conceptually:

| Repository | Owner writes | Contributors read | Canon maintainers write |
|---|---|---|---|
| Personal | Yes, through its owner's tools | When granted | No |
| Canon | No | Yes | Explicit review only |
| Template | Maintainer controlled | Yes | Maintainer controlled |
| Tooling | Maintainer controlled | Yes | Maintainer controlled |

Notion and peer repositories remain attributed sources, never implicit canon.

## Knowledge Lifecycle

### Context retrieval

Before making a material product, gameplay, API, architecture, terminology, lore, or design
decision, the agent searches:

1. canon for shared authoritative knowledge;
2. the contributor's personal repository for local-development understanding;
3. relevant peer repositories for attributed alternate knowledge; and
4. optional external sources such as Notion when a gap remains.

Results retain source identity. Search does not promote personal or repeated knowledge into
canon. Ordinary current-state questions prefer current-system documents; initiative, pending,
source, and archive material appears only with its role clearly labeled.

### Capture during work

The active agent has the best context for deciding what may remain useful after the task. It
captures when work establishes or changes:

- user-visible behavior or gameplay rules;
- an API, data, save, or deployment contract;
- architectural ownership or a durable constraint;
- stable terminology;
- an approved product or solution decision;
- a correction to existing knowledge; or
- a material blocking question that qualifies other conclusions.

Each agent task writes one append-oriented log. Coordinators, coders, reviewers, researchers, and
direct tasks therefore do not contend for the same file even when they share a parent feature.

The log is not a diary. It excludes prompts, transcripts, task lists, detailed execution,
routine review feedback, test/build output, and speculation that reached no durable conclusion.

When no durable knowledge exists, the agent acknowledges no-capture in task-local state. That
acknowledgement does not deserve a document or Git commit.

### Completion and direct incorporation

A task-log entry does not assert that behavior changed. Direct incorporation is appropriate only
when acceptance is explicit or reliable source-control completion is confirmed.

Useful signals are:

- explicit owner or coordinator acceptance;
- a confirmed commit, changelist, or submit for the accepted implementation;
- explicit abandonment or supersession; or
- no reliable signal, in which case the entry stays pending.

In a coordinated feature, the coordinator normally incorporates after implementation review,
feedback, manual testing, and code inspection. In a single-session or small task, the same agent
may incorporate when acceptance is unambiguous. Neither profile must declare work complete when
the user simply stops returning to it.

Incorporation selects accepted entries, re-reads current destinations, identifies duplicates and
contradictions, applies the explicit update, preserves evidence, updates dispositions, and
validates all affected files as one serialized operation.

### Grooming

Grooming is the recovery path for work never explicitly incorporated, rejected, or abandoned.
It is an explicit bounded activity, not an always-running consolidation loop.

A grooming pass:

1. selects a project, feature, subject, or date scope;
2. groups pending and stale entries with likely destinations;
3. compares them with current knowledge and implementation evidence when necessary;
4. identifies duplicates, contradictions, and uncertain applicability;
5. lets the active agent propose a disposition;
6. applies only accepted document changes; and
7. stops with pending or needs-owner entries when evidence is insufficient.

Useful dispositions remain incorporation, already represented, informational, rejected,
superseded, confirmed abandonment, and needs-owner. Staleness never proves abandonment.

The tool may assemble the batch and check ids, backlinks, metadata, and exact duplicates. It does
not supply semantic judgment independently of the active agent.

### Knowledge hygiene

Hygiene checks existing durable claims rather than new task entries. Environment-dependent claims
may record applicability, verification date, source, and result. Cheap deterministic evidence—
repository revisions, Perforce changelists, build ids, deployment records, API contracts, and
live observations—outranks recollection.

Unverifiable does not mean false; stale does not mean obsolete. Verified corrections may update
current facts with evidence. Archival and deletion remain explicit proposals.

### Lifecycle audit

The active agent should complete a capture-or-no-capture check at meaningful boundaries. Optional
client adapters may recover a missed check when the client exposes a reliable handoff,
acceptance, source-control, or task-closing event.

An ordinary assistant response ending is not a task boundary. The adapter must stay silent during
progress reports, questions, planning, code/review iterations, and feedback. It may request only
one throttled audit for a material boundary and should prefer a missed audit over a noisy or
looping extra turn.

Lifecycle parity is not required across clients. Shared instructions and normal MCP tools remain
the fallback when a client lacks reliable hooks.

### Persistence and synchronization experience

After every valid personal mutation, `kb` atomically saves and validates Markdown and updates the
derived index. Manual-remind mode stops there: it does not stage, commit, integrate, or push, and
it returns a concise throttled reminder until the contributor's normal Git workflow restores a
clean synchronized state. This is Cliff's selected profile.

Automatic mode is opt-in only after setup confirms a dedicated non-passphrase SSH identity and
verifies that GitHub access and configured signing work non-interactively. It stages only
validated paths, uses the active agent's natural one-sentence change description as the commit
message, and attempts a push at meaningful checkpoints by default. A contributor may explicitly
select per-mutation synchronization. Offline or failed pushes remain recoverable and retry later.

No Git or signing process launched through MCP or a hook may prompt, and no daemon is required.

The contributor sees concise health such as healthy, working changes awaiting a manual commit,
local commits awaiting push, offline, authentication failure, or conflict. `kb` never discards
working changes or commits and never silently resolves content conflicts. A genuine conflict
returns to the owner or active agent.

## Canon Review Lifecycle

Canon review begins only when an authorized leader explicitly requests it:

1. Select personal changes since a known review watermark or by project/feature scope.
2. Compare candidate decisions and facts with current canon.
3. Identify additions, compatible refinements, superseded canon, and conflicts.
4. Produce a reviewable proposal with source attribution.
5. Record a disposition for every candidate.
6. Publish the accepted proposal revision.
7. Notify origin owners of rejected or conflicting personal material.

The review may recommend personal cleanup but does not perform it. Canon publication does not
mark a feature deployed.

A contributor may seed a new personal repository from canon. Subsequent personal knowledge
remains independently authored until explicitly promoted.

## Environment And Release Truth

Knowledge authority, work state, source-control state, and runtime applicability must remain
independent. Useful shared views include:

- production system knowledge;
- shared-development knowledge;
- adopted but not deployed features;
- future initiatives and proposed designs; and
- deployment and rollback history.

Personal knowledge defaults to local-development understanding. Canon provides the authoritative
team view but may contain adopted features not deployed anywhere. Production status requires an
explicit deployment event.

Features may span Eventun, Accountun, Ascentun, Cardanoun, the game client, Website V2, content,
and configuration. Deployment is therefore recorded per required component. A backend deployment
cannot make canon claim that an unreleased game client feature is production, or the reverse.

An explicit deployment or rollback action records:

- feature, environment, and affected components;
- Git revisions, Perforce changelists, build ids, configuration versions, or equivalent evidence;
- time and responsible release context;
- compatibility between required component versions; and
- the resulting environment-specific view.

When a query does not name an environment, canon production is the default shared answer. Local
work, development, proposed direction, rationale, and history are separately queryable. Material
disagreement is labeled rather than blended.

## Notion Boundary

Notion remains optional evidence rather than the canonical storage format. An agent may search
selected Notion content through an authenticated integration, cite page identity and retrieval
time, and explicitly adopt durable conclusions into personal knowledge.

There is no unrestricted bidirectional synchronization and no silent Markdown overwrite from a
changed Notion page. Canon review may consider Notion evidence, but accepted canon remains
Markdown.

## Instruction Distribution

Product repositories should contain one short, tool-independent knowledge policy in root
`AGENTS.md`. Cursor and Codex can consume that shared policy. Where supported, root `CLAUDE.md`
imports or mirrors the same policy rather than inventing a second workflow.

The shared policy should tell agents to:

- search relevant knowledge before material decisions;
- use `kb` rather than directly editing an external knowledge clone;
- capture durable decisions, corrections, contracts, and behavioral deltas;
- exclude plans, prompts, transcripts, tasks, routine execution, and build output;
- keep parallel task evidence separate from accepted current truth;
- incorporate only with acceptance evidence;
- preserve source authority and environment applicability; and
- require explicit canon and deployment actions.

Setup may install a small managed fallback in user-global instructions for configured projects
without repository policy. Machine paths stay in local configuration.

## Onboarding Experience

### Administrator preparation

1. Create a personal GitHub repository from `knowledge-template`.
2. Grant the contributor write access and approved readers read access in GitHub.
3. Grant GitHub read access to canon and selected peer repositories.
4. Configure shared environments and deployable component identities.
5. Publish the supported `kb` package for the contributor's platform.

### Workflow bootstrap

Setup first asks the contributor to describe how they normally work with agents. It infers and
confirms only fields that materially affect capture suggestions:

1. single continuing conversation, coordinated tasks, or a mixture;
2. explicit acceptance, source-control completion, or usually-unclear completion; and
3. rare, occasional, or frequent parallel agent work.

Client and operating-system details should be detected where practical. These choices change
audit and incorporation behavior, not repository permissions or the definition of durable
knowledge.

Recommended starting profiles are:

| Contributor style | Work profile | Incorporation default |
|---|---|---|
| Coordinated owner | Mixed coordinator and worker roles | Incorporate after explicit or source-control acceptance; groom unfinished logs. |
| Single-conversation coworker | Single session | Capture in that task; incorporate only with a clear acceptance signal. |
| Unknown | Mixed and conservative | Capture task evidence and rely on grooming for current updates. |

### Contributor steps

The intended one-time flow is:

1. Install Git if setup reports it missing.
2. Install `kb`.
3. Run `kb setup`.
4. Select MCP-only or hybrid-read access and manual-remind or automatic synchronization.
5. Authenticate for repository setup; automatic mode additionally verifies a confirmed
   non-passphrase SSH identity without prompting through MCP.
6. Accept selected client MCP and optional hook configuration.
7. Run a non-mutating bootstrap verification.

The bootstrap proves writable personal identity, read-only sources, workflow profile, source
search, synchronization health, environment defaults, and client integration. It does not create
a harmless fake fact that later needs cleanup.

No onboarding step asks the contributor to fork, add a remote, create a branch, commit, or push.

## Rollout

### Stage 1: Repository restructuring

Status: complete on 2026-07-19.

The personal repository has project/current-system/initiative/decision/source/archive boundaries,
root governance, indexes, and mechanical validation.

### Stage 2: Manual workflow validation

Status: active.

Use the structure during ordinary product work and during `kb` requirements/design work. Observe
retrieval, placement, index usefulness, delivery snapshots, direct updates, parallel ownership,
and grooming without implementing the tool prematurely.

### Stage 3: Personal tool pilot

Implement the smallest on-demand read, capture, validation, synchronization, and incorporation
surface for the knowledge-base owner. Exercise WSL plus Windows-client access and offline recovery.

### Stage 4: One-coworker pilot

Onboard the willing Claude Code coworker on Linux/Nix. Add their dual-boot Windows installation
only when needed. Evaluate setup time, capture quality, hook noise, and Git invisibility.

### Stage 5: Canon pilot

Use two personal repositories to review one multi-component feature. Exercise conflict,
disposition, adoption without deployment, partial deployment, and rollback.

### Stage 6: Broader rollout

Package native Windows onboarding for additional Cursor users only after normal use requires no
Git knowledge or recurring manual reminders.

## Workflow Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Agents capture transient noise | Restrict capture types and preserve strong negative examples. |
| Agents omit durable knowledge | Shared instructions plus one-shot boundary audits where reliable. |
| Audit hooks consume attention or tokens | Disable on weak events, throttle by work handle, and prefer missed audits. |
| Parallel tasks rewrite current documents | Task-owned logs during capture; serialized incorporation. |
| Rejected implementation becomes current truth | Pending evidence requires explicit disposition and incorporation. |
| Open logs accumulate | Surface bounded grooming batches by subject and age without inferring abandonment. |
| Grooming invents coherence | Require source-linked proposals and allow pending/needs-owner outcomes. |
| Personal or canon is mistaken for production | Preserve authority, source-control, and deployment as independent dimensions. |
| A feature is only partly deployed | Track required components and compatible versions per environment. |
| Git failures leak into normal work | Preserve working changes and local commits, respect the selected sync profile, and report concise actionable health. |
| Personal repositories become de facto canon | Label source kind and prefer canon for authoritative shared questions. |
| MCP or folder access defeats sandbox intent | User-selected access profiles, fixed source registry, capability-specific tools, no arbitrary MCP paths, and client/platform verification. |
| Notion and Markdown drift | Read-only attributed Notion evidence and explicit adoption. |
| The template preserves personal assumptions | Extract only after ordinary use identifies reusable structure. |

## Manual-Use Observations To Collect

During design, implementation, review, and eventual testing of `kb`, record:

- whether agents find the correct current, initiative, decision, and source documents;
- whether requirements, system design, workflow design, and implementation evidence remain
  distinct without excessive navigation;
- whether initiative delivery snapshots stay useful or become status busywork;
- which durable decisions deserve the curated decision log versus direct document updates;
- whether one task-owned log per agent actually avoids parallel contention;
- whether no-capture checks are frequent enough without becoming ritual;
- when a design becomes sufficiently accepted to drive implementation while remaining
  initiative material;
- whether implementation and testing evidence belongs in the tool repository, task logs,
  initiative documents, or current-system knowledge;
- what closure and archive steps are easy to forget; and
- which checks the repository validator can enforce mechanically without pretending to make
  semantic judgments.

Observations that change repository-wide policy belong in the repository-restructure governance
ledger and `ORGANIZATION.md`. Observations specific to `kb` belong in this initiative. Accepted
material design changes also receive a concise knowledge-base decision entry.

### Observed Use Case: Coordinator-Guided Feature Delivery

The Eventun foundation and teams work provides one sustained coordinated-feature case. The owner
uses a long-running coordinator conversation to retain product direction, review implementation
checkpoints, decide what should happen next, and prepare bounded prompts for separate Eventun,
Ascentun, and Ascent Rivals coder conversations. Independent review conversations may also inspect
the same foundation. The owner brings proposals and completion reports back to the coordinator,
which compares them with the repositories and accepted knowledge before approving, narrowing, or
returning corrections.

The useful durable output is not the conversation transcript or the generated coder prompts. It is:

- accepted design rules and owner decisions that survive the individual conversation;
- current-system corrections after implementation review accepts local behavior;
- initiative checkpoints for approved, implementing, verified, committed or submitted, and
  deployed states;
- unresolved risks and the next meaningful gate;
- enough source and revision identity to resume after a client crash, lost conversation, coder
  replacement, or context compaction; and
- a compact basis for constructing the next coder prompt without replaying all prior discussions.

This case also demonstrates why lifecycle dimensions must remain independent. Eventun changes may
be committed and locally verified while Ascentun remains uncommitted, an Ascent Rivals Perforce
changelist remains intentionally unsubmitted during release-fix work, and no component is deployed
to shared development. Review acceptance and successful tests must not silently promote any of
those states.

The manual workflow uses the knowledge base as the shared memory between conversations:

1. The coordinator retrieves current-system and active-initiative context before selecting work.
2. A coder receives a bounded pre-edit prompt and returns a proposal rather than editing
   immediately.
3. The coordinator reviews the proposal, preserving accepted decisions while identifying only
   material corrections and genuine owner choices.
4. The coder implements and reports source-control state plus verification evidence separately
   from deployment.
5. The coordinator performs implementation review and incorporates accepted behavior or delivery
   status into the appropriate documents.
6. The next coder conversation is bootstrapped from that durable state rather than from copied chat
   history.

Implications for the proposed `kb` tool are:

- one feature or workstream needs a stable handle across multiple conversations and repositories;
- each conversation needs isolated capture ownership while incorporation into shared documents is
  serialized;
- retrieval should return current behavior, active initiative decisions, pending deltas, and
  delivery state without treating them as one authority level;
- capture should prefer decisions, contract changes, corrections, blockers, and lifecycle gates
  over prompts, review chatter, command output, and repeated verification summaries;
- explicit owner acceptance and implementation-review outcomes should be usable incorporation
  evidence, while silence and ordinary conversation endings should not;
- source-control and environment state must represent Git commits, uncommitted work, Perforce
  changelists, submission, and deployment independently; and
- status and grooming should expose unincorporated decisions or stale checkpoints without turning
  the knowledge tool into a task manager.

This use case satisfies the coordinated-feature portion of the manual repository checkpoint. It
does not yet prove the separate parallel task-log, unresolved grooming, or reusable-template cases.

### Observed Use Case: Iterative Design Coordination Across Chats And A Live Artifact

[Website V2](../../../ascent-rivals/initiatives/website-v2/README.md) provides a distinct
design-to-implementation-preparation case. The owner uses one
long-running coordinator conversation to review current product knowledge, resolve scope and
architecture, develop route and data requirements, decide the visual direction, review design
checkpoints, and select the next bounded task. A separate designer conversation operates the live
Pencil workfile on Windows from prompts prepared in the coordinator. The owner reviews the result,
adds subjective visual feedback, and returns the designer's summary to the coordinator; the
coordinator can also inspect the actual Pencil frames through MCP before accepting or returning a
revision. Adjacent Eventun and team conversations may change contracts that Website V2 will later
consume.

This case crosses an important storage boundary. The personal knowledge repository remains in WSL,
while the mutable Pencil artifact remains on a Windows drive because live authoring against the WSL
filesystem proved unreliable. The workfile can advance through several experiments before one
reviewed checkpoint is incorporated into Markdown. It is evidence for the design, not accepted
knowledge merely because a frame exists, and it is not implementation or deployment evidence. The
greenfield Website V2 application remains unimplemented at the time of this observation.

The observed loop is:

1. The coordinator retrieves current-system facts and the active Website V2 initiative rather than
   reconstructing context from old chat history.
2. The owner and coordinator resolve one bounded product, architecture, content, or visual question.
3. The coordinator prepares a focused designer prompt that names the accepted baseline and protects
   unrelated frames.
4. The designer changes the external workfile and reports the affected frames and layout checks.
5. The owner supplies visual judgment, while the coordinator inspects the artifact and checks it
   against product contracts and prior decisions.
6. Revisions repeat until the owner accepts the checkpoint. Ordinary progression language such as
   `looks good`, `continue`, or `what is next` accepts only the immediately preceding bounded result
   when it is not qualified.
7. The coordinator directly incorporates material decisions, page rules, artifact checkpoint state,
   and the next gate because it owns the serialized documentation step. Routine prompts, rejected
   compositions, tool output, and review chatter remain outside durable knowledge.
8. A later observation can reopen a previously accepted detail. The active specification is
   corrected or superseded rather than retaining contradictory layers merely to preserve chronology.
9. A future implementation conversation will bootstrap from the reviewed initiative, current-system
   facts, decisions, and selected design frames instead of replaying the coordinator and designer
   transcripts.

Durable outputs from this workflow include:

- accepted scope, architecture, route, data, interaction, responsive, and visual-language rules;
- current-system corrections discovered while evaluating the proposed site;
- material direction changes and their rationale;
- the latest reviewed design checkpoint and whether the live artifact may be ahead of it;
- unresolved backend contracts, deferred product choices, and the next meaningful gate; and
- delivery state that keeps design acceptance, implementation, verification, source control, and
  deployment independent.

The prompts sent to the designer, every experimental frame, copied designer completion reports,
raw MCP output, routine visual QA, and minor spacing corrections are not durable outputs. A frame
name or later preservation snapshot is useful only when it identifies evidence for an accepted
checkpoint.

Implications for the proposed `kb` tool are:

- one parent feature must relate coordinator, designer, reviewer, and future implementation work
  without forcing those conversations to share one writable log;
- retrieval for a handoff should return current facts, active specifications, material decisions,
  the latest accepted artifact checkpoint, and open gates without replaying conversation history;
- capture must support an attributed mutable external artifact and record the reviewed checkpoint
  separately from the artifact's live head, without copying machine-local paths into shared
  knowledge or treating artifact existence as acceptance;
- acceptance evidence must be scoped to the immediately preceding bounded result, while later owner
  corrections can supersede it cleanly;
- a coordinator that owns incorporation can update destinations directly, while independent worker
  conversations still require task-owned capture and serialized incorporation;
- routine design iterations need an inexpensive no-capture outcome so the tool does not turn every
  visual adjustment into repository noise; and
- Windows-hosted clients must be able to retrieve and mutate the WSL-owned personal repository while
  Windows-only design tools remain external evidence.

This use case satisfies the Windows-originated interaction portion of the manual repository
checkpoint and adds evidence for the mixed single-session/coordinated-design profile. The external
designer conversation did not write knowledge concurrently, so this case does not prove parallel
task-log capture, serialized incorporation of competing entries, or unresolved grooming.

### Observed Use Case: Analysis-Gated Direct Feature Implementation

The Ascent Rivals Play-menu matchmaking-window improvement provides a small direct-feature case.
The owner began with a concrete usability observation and tentative behavior: clarify that a
same-day match starts `today`, add a minute-updating countdown inside eight hours, and refresh
operator-adjusted matchmaking windows more frequently. The owner explicitly requested analysis
without edits because the Perforce session was not ready.

One conversation retained the full bounded lifecycle rather than handing work to separate
coordinator, coder, and reviewer chats. It retrieved the relevant Ascent Rivals knowledge and UI
workflow, inspected the Unreal client and Gauntlet subsystem, identified existing countdown
formatting support, and found an additional stale-data path: the Play menu listened for active
calendar transitions but not refreshed future-calendar data. The conversation returned a proposed
slice before mutation. After the owner approved it, an expired Perforce ticket stopped the change
without bypassing source control. The same conversation resumed after login, checked out the exact
files, implemented the accepted slice, preserved repository formatting, and directly updated the
Gauntlet client-entry initiative.

The implementation artifact remained an opened local Perforce working copy. The conversation did
not claim submit, deployment, or runtime UI verification. Related direct Ascent Rivals chats can use
the same pattern when one agent can own analysis, implementation, and durable incorporation without
parallel writers; a later review or QA chat should resume from product and source-control identity,
not from copied transcript history.

The observed loop is:

1. Retrieve current and initiative knowledge before interpreting the feature request.
2. Inspect source-controlled implementation and reusable project utilities while respecting an
   explicit analysis-only boundary.
3. Return a bounded proposal that separates requested behavior from additional defects discovered
   during the ownership trace.
4. Treat the owner's instruction to implement as scoped acceptance of that proposal.
5. Stop at a transient authorization boundary rather than modifying read-only Perforce files or
   treating the blocker as a product decision.
6. Resume in the same conversation after authorization, implement only the accepted slice, and
   preserve source-control and file-format conventions.
7. Incorporate the durable behavior and known limitation into the owning Ascent Rivals initiative,
   while reporting implementation, submission, deployment, and verification as independent states.

Durable outputs from this workflow include:

- the accepted same-day and eight-hour countdown behavior;
- the ownership relationship between the root Play-menu tile and Gauntlet calendar data;
- the separate five-minute calendar refresh and hourly broad Gauntlet sync;
- the requirement to react to full-calendar refreshes and select the earliest applicable window;
- the local Perforce implementation boundary and remaining runtime QA; and
- the product-knowledge update that lets a later review or related feature chat recover the result.

The original prompt, intermediate plan, source-search transcript, Perforce login exchange, command
output, and routine encoding checks are not durable knowledge. The login failure matters only as
evidence that a client must preserve task context across a pause and resume; it does not deserve a
task-log entry or product note by itself.

Implications for the proposed `kb` tool are:

- a direct task needs a lightweight stable handle even when no coordinator or parallel worker exists;
- retrieval should locate current behavior, the active initiative, and related prior decisions by
  product subject and feature identity rather than conversation identity;
- explicit analysis-only and mutation-approved phases should remain visible to the active agent,
  but routine phase transitions should not become durable records;
- lifecycle capture should be offered at meaningful gates such as accepted proposal, completed
  implementation, or incorporation, not after every progress turn;
- a single conversation that owns the serialized documentation step should be able to incorporate
  directly without first creating a redundant task log;
- transient authentication and tooling blockers should stay task-local unless they reveal a durable
  workflow constraint;
- later review or QA conversations should receive accepted behavior, changed ownership, source-control
  state, and unresolved verification rather than a transcript summary; and
- local implementation, Perforce submit, deployment, and runtime verification must remain separate
  fields even for a small feature.

This use case satisfies the small-direct-task portion of the manual repository checkpoint. It does
not exercise parallel task-owned capture, serialized incorporation of competing entries, or
grooming dispositions.

## Open Workflow Decisions

- Grooming cadence and the least intrusive way to surface the backlog.
- Which source-control signals are reliable enough to permit direct incorporation.
- How a contributor is notified of rejected or conflicting personal knowledge after canon review.
- Which shared environment names and component identities match the actual release workflow.
- Whether production documents are materialized separately or derived from base knowledge plus
  deployment state.
- How peers are selected and refreshed as the contributor count grows.
- Which Notion page sets, if any, should be standard shared evidence.

Technical choices such as language, Git integration, schemas, client version floors, packaging,
and patch representation are tracked in the [system design](system-design.md#open-technical-decisions).

## External Inspiration

### COG Second Brain

[COG Second Brain](https://github.com/huytieu/COG-second-brain) is a reference for selected
capture, consolidation, verification, bounded iteration, and onboarding patterns. It is not a
candidate dependency or repository baseline.

Useful adaptations are:

- source entries gain explicit dispositions and backlinks after incorporation;
- grooming scans a bounded corpus, groups by subject, detects repetition and contradiction, and
  retains evidence;
- unverifiable and stale claims remain explicit rather than being silently deleted;
- mechanical checks have stopping conditions while semantic conflicts escalate; and
- onboarding infers a workflow profile before asking focused follow-ups.

Excluded patterns include general braindumps, daily journaling, people CRM, task/project
management, role packs, competitive intelligence, broad publishing automation, and model-assigned
confidence as a substitute for evidence.

### GBrain

GBrain's Compiled Truth plus Timeline model cleanly separates rewritten current synthesis from an
append-only evidence trail. That maps to current-system documents plus decisions and task logs.
Its distinction between raw retrieval and a source-cited synthesized answer also informs `kb`
search: the local tool returns bounded attributed evidence and the active agent synthesizes.

World knowledge should outlive any agent configuration, and authorization should filter content
before retrieval. GBrain's database, graph/vector infrastructure, daemon, CRM schemas, and broad
ingestion surface are not required.

### GStack

GStack is useful mainly for tool-independent policy and client-local adapter distribution. Its
specialist role pack and prescribed development process are intentionally excluded because
contributors use different workflows.

### Zettelkasten

Stable addresses, small referenceable decisions, evidence links, and curated structure notes are
useful. One-file-per-thought and graph-first navigation are not. Cohesive product knowledge often
belongs in a single readable system description; atomic task entries serve as evidence.

### PARA, Progressive Summarization, And GTD

Project-first active placement and explicit archives gain PARA's useful boundary without turning
the repository into a productivity system. Progressive Summarization supports concise current
summaries above linked detail. GTD contributes capture, clarify, organize, and review as a hygiene
loop, but not action lists, calendars, or an instruction to capture everything.

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
- [GitHub repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)
- [GitHub repository templates](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [Notion Model Context Protocol](https://developers.notion.com/guides/mcp/overview)
