# kb Tool System Design

Status: proposed design baseline

Last revised: 2026-07-22

## Purpose And Boundary

Describe an implementable architecture for the local `kb` tool. The
[requirements](requirements.md) are normative. The
[workflow design](federated-personal-and-canonical-knowledge-workflow.md) defines contributor
behavior, knowledge lifecycle, and rationale. This document owns process boundaries,
components, local state, synchronization, indexing, MCP behavior, client adapters, packaging,
and verification.

Self-only implementation may begin in bounded slices. The remaining parallel task-log and
grooming cases are now personal dogfood gates rather than prerequisites for the executable
foundation, retrieval, status, receipts, and direct capture path. Do not freeze those provisional
schemas, extract the template, or begin coworker or canon rollout until the cases are complete and
their structural friction is recorded in the
[Pass 3 governance ledger](../repository-restructure/pass-3-governance-ledger.md).

## Architectural Decisions

### On-demand process, no daemon

Each agent client starts `kb mcp` as a local standard-input/output MCP server. The process lives
for that client connection and exits with it. Multiple clients may start independent processes;
cross-process repository locks protect mutations.

There is no required daemon, service, tray process, or scheduler. Work normally associated with
a background process is moved to safe invocation boundaries:

| Work | Invocation boundary |
|---|---|
| Validate identity and recover interrupted local operations | MCP startup and `kb doctor` |
| Report unsynchronized personal changes | Mutation results, `kb_status`, explicit `kb sync`, and reliable boundary hooks |
| Retry automatic-mode unpushed commits | MCP startup, `kb_status`, explicit `kb sync`, and eligible checkpoints |
| Refresh a stale read-only source | First relevant search/read within a bounded timeout |
| Refresh the local index | Lazily before a query or immediately after a local mutation |
| Surface grooming backlog | `kb_status`, context retrieval for a related subject, or explicit `kb_groom` |
| Semantic incorporation or grooming | The already-active agent task or explicit human review |

Process exit never discards work. The personal Git clone retains authored working-tree changes or
local commits, while a small local state database retains index, reminder throttle, and recovery
information between invocations.

### Deterministic core, no autonomous model

The `kb` executable never calls a model or embedding API. It performs deterministic repository,
Markdown, schema, search, validation, and synchronization operations. The active Codex, Claude
Code, or Cursor agent performs semantic classification and writes proposed prose using context it
already has.

This affects several tool names that otherwise sound model-powered:

- `kb_groom` selects, groups, and returns candidate evidence; it does not decide semantic
  compatibility.
- `kb_incorporate` validates and applies explicit agent- or human-supplied document updates; it
  does not invent the update.
- `kb_prepare_canon` assembles a source-attributed review bundle; it does not resolve conflicts.
- `kb_search` performs attributed lexical retrieval; the calling agent synthesizes an answer.

### Proposed implementation baseline

The initial implementation should use:

- Rust for native Linux and Windows executables, using the official MCP Rust SDK (`rmcp`);
- the installed Git command-line client for repository transport and history;
- a local SQLite database with FTS5 for derived search and operational state, using `rusqlite`
  with bundled SQLite so contributors do not need a database installation or C toolchain;
- YAML for managed configuration and repository manifests;
- Markdown plus the current `ORGANIZATION.md` schema for durable content; and
- standard-input/output MCP transport for every supported client.

Rust, the official MCP SDK, bundled SQLite through `rusqlite`, and FTS5 are selected design
directions. The cross-platform spike verifies those choices rather than reopening them. The
external Git client is intentional for the pilot: it uses existing GitHub authentication and
avoids building a second Git implementation.

SQLite fits this workload better than RocksDB. The corpus is small, reads need structured
filters and full-text ranking, and the database is local rebuildable state rather than the
durable knowledge store. RocksDB would add a C++ key-value engine and require `kb` to build its
own document-query and full-text-index abstractions for write throughput and scale the pilot
does not need. The SQLite file, write-ahead log when enabled, and other derived files remain
outside Git and may be rebuilt from Markdown.

## System Context

~~~text
Product workspace                         Private application data

Codex --------\                           +-----------------------------+
Claude Code ---+--> stdio MCP --> kb ---->| personal clone (read/write) |
Cursor --------/                  |        | canon clone (read-only)     |
                                  |        | peer clones (read-only)     |
                                  |        | index and local state       |
                                  |        +-----------------------------+
                                  |
                                  +------> installed Git + credential provider
                                  +------> optional client-owned Notion MCP
~~~

The product workspace contains only shared tool-independent instructions and client
configuration where appropriate. The `kb` process is the portable capability boundary.

### MCP baseline and optional direct reads

MCP is the required cross-client interface and the only supported mutation path. It provides one
contract for source attribution, personal/canon/peer authority, applicability, pending-state
filters, locking, validation, and Git synchronization. `kb_search` returns attributed excerpts
and logical handles; `kb_read` returns the complete raw Markdown so MCP retrieval does not force
agents to work from summaries.

A contributor may additionally enable native read-only filesystem access to the configured
Markdown clones when a client and sandbox make that convenient. This is an optional local
optimization for browsing with ordinary file and search tools, not a separate workflow. It does
not grant writes, replace MCP retrieval in the compatibility contract, or make direct edits a
supported capture path. Strict or centrally managed installations may use MCP-only access.

The agent does not choose or grant either permission. The contributor or administrator selects
an MCP-only or hybrid-read setup profile, and the client enforces the resulting capability. A
hybrid profile should expose only read-only clones or mirrors where operating-system permissions
can express that distinction; instructions alone are not a security boundary for a writable
personal clone.

MCP Resources may expose logical documents in clients that support them well, but the baseline
must not depend on resource browsing because client support and presentation vary. Tools remain
the interoperable search/read surface.

Local stdio MCP must also not be described as universally bypassing a client sandbox. The
effective boundary depends on the client, its MCP approval configuration, the operating system,
and how the server process is launched. The client smoke matrix must verify read/write behavior
for MCP-only and hybrid-read profiles on every supported platform.

## Executable Surface

One executable supports both human/setup commands and the MCP server:

| Command | Purpose |
|---|---|
| `kb mcp` | Run the stdio MCP server for one client connection. |
| `kb setup` | Detect the environment, configure sources and selected clients, and initialize clones and index. |
| `kb doctor` | Run non-mutating integration, repository, auth, sync, lock, index, and client checks. |
| `kb status` | Print the same core health model exposed by `kb_status`. |
| `kb sync` | Refresh selected read-only sources and report personal sync state; only automatic mode performs personal commit/push retries. |
| `kb validate` | Run repository-structure and content validation. |
| `kb uninstall` | Remove client integration and derived local state while preserving unsynchronized knowledge. |

Normal contributors should interact through their agent after setup. These commands exist for
installation, support, and recovery, not as a recurring workflow.

## Internal Components

### MCP boundary

- Registers only tools allowed by the configured capability mode.
- Parses and validates structured inputs before accessing repositories.
- Converts internal errors into stable, actionable MCP errors without leaking credentials or
  arbitrary paths.
- Attaches source identity, freshness, and applicability to read results.

### Configuration and identity

- Loads machine-local contributor, device, source, client, workflow, and environment settings.
- Resolves logical source ids to fixed local clones.
- Validates each repository's root manifest, remote identity, and allowed role.
- Exposes no operation that replaces a configured root with a caller-supplied path.

### Repository manager

- Owns clone creation, fetch, safe integration, validated natural-message commits, pushes, and
  recovery according to the selected synchronization profile.
- Acquires a cross-process write lock before personal mutations or local history rewrites.
- Treats canon and peer clones as read-only even when the operating-system account could write
  them.
- Maps Git failures into explicit synchronization states.

### Knowledge document service

- Parses Markdown, frontmatter, indexes, task logs, stable ids, applicability, links, and
  dispositions.
- Reuses or ports the existing `tools/validate_kb.py` behavior as conformance fixtures.
- Restricts destination updates to roles permitted by the organization contract.
- Enforces expected document hashes for incorporation and other multi-document writes.

### Capture service

- Creates or resumes the one task-owned log selected by a stable work handle.
- Appends one validated entry with a stable identifier.
- Updates only that log during capture.
- Maintains no authored shared task index.

### Search service

- Builds a derived local lexical index over permitted source repositories.
- Stores document identity, project, role, source kind, owner, applicability, verification,
  initiative status, archive state, and task-entry disposition with searchable text.
- Applies authority, role, applicability, and archive filters before ranking.
- Returns excerpts and stable document/entry handles, not generated summaries.

### Workflow service

- Stores the machine-local workflow profile and work-handle audit state.
- Prepares bounded grooming batches.
- Applies explicit incorporation updates and entry dispositions transactionally.
- Tracks no-capture acknowledgements locally without creating repository artifacts.

### Canon and deployment service

- Is absent from normal contributor capability mode except for reads.
- In maintainer mode, prepares review bundles and applies an exact explicitly approved revision.
- Maintains source attribution, canon dispositions, feature adoption, and component-level
  deployment events.

### Client adapters

- Write supported MCP configuration.
- Install or update the small shared/global instruction block.
- Optionally translate reliable client lifecycle events into a throttled audit request.
- Never implement repository, capture, or synchronization semantics themselves.

## Local Files And State

### Default locations

Linux follows XDG locations:

~~~text
$XDG_CONFIG_HOME/kb/config.yaml        # fallback ~/.config/kb/config.yaml
$XDG_DATA_HOME/kb/repos/               # fallback ~/.local/share/kb/repos/
$XDG_STATE_HOME/kb/state.db            # fallback ~/.local/state/kb/state.db
$XDG_STATE_HOME/kb/logs/
~~~

Windows uses:

~~~text
%LOCALAPPDATA%\kb\config.yaml
%LOCALAPPDATA%\kb\repos\
%LOCALAPPDATA%\kb\state.db
%LOCALAPPDATA%\kb\logs\
~~~

For Cliff's pilot, the existing WSL personal clone remains the only writable clone. Windows
clients launch the configured WSL `kb mcp` command. The Windows installation therefore does not
create a second personal clone.

Repositories and SQLite state live on the native local filesystem of the process that owns them:
the WSL filesystem for the WSL installation and a local Windows filesystem for a native Windows
installation. Windows clients may invoke the WSL process, but they do not relocate its database
to a UNC or other network filesystem.

### Configuration model

A conceptual local configuration is:

~~~yaml
schema: 1
identity:
  contributor: cliff
  device: cliff-main
workflow:
  style: mixed
  acceptance: explicit-or-source-control
  parallelism: frequent
access:
  profile: hybrid-read
git:
  transport: ssh
  ssh_host: ikigai-github
  signing: inherit
sync:
  mode: manual-remind
  reminder: meaningful-boundary
  automatic_trigger: checkpoint
  read_refresh:
    freshness_seconds: 300
    wait_milliseconds: 2000
    explicit_timeout_seconds: 30
sources:
  - id: personal
    kind: personal
    owner: cliff
    path: /machine/local/path
    remote: organization/knowledge-cliff
    access: read-write
  - id: canon
    kind: canon
    path: /machine/local/path
    remote: organization/knowledge-canon
    access: read-only
clients:
  codex:
    enabled: true
    audit_adapter: true
environments:
  - shared-development
  - production
~~~

Configuration contains logical remote identities, not credentials. Git or platform credential
facilities own authentication. Setup writes configuration atomically and retains a recoverable
previous version during upgrades.

`ikigai-github` is Cliff's machine-local SSH host alias and pilot baseline, not a value for the
future repository template. Other installations may use `github.com` or their own local alias.
The tool inherits Git author, signing, SSH, and agent configuration instead of copying private-key
paths or passphrases into `kb` configuration.

Access, synchronization, and workflow profiles are independent. Cliff's initial profile is
`hybrid-read`, `manual-remind`, and coordinated/mixed. A contributor may opt into automatic Git
synchronization only after confirming a non-passphrase SSH identity and passing setup's
non-interactive GitHub access and configured-signing checks.

### Repository manifest

Each managed repository has a small tracked root manifest named `.kb-repository.yaml`, for
example:

~~~yaml
schema: 1
kind: personal
owner: cliff
organization_contract: 1
~~~

Canon uses `kind: canon`; template uses `kind: template` without a concrete owner. A source whose
manifest, configured remote, or role disagrees with local configuration is unhealthy and cannot
be mutated or pushed.

### Operational state

The local state database contains only derived or operational data:

- schema and application version;
- source HEADs, fetch times, freshness, and health;
- indexed document hashes and FTS rows;
- pending local commits and last push result;
- interrupted-operation recovery markers;
- work handles and no-capture/audit-throttle state;
- client adapter versions; and
- bounded diagnostic history.

Deleting the database may lose convenience state but not durable knowledge. `kb doctor` and an
index rebuild restore it from configuration and repositories.

## On-demand Process Lifecycle

1. The client launches `kb mcp`.
2. `kb` loads configuration and validates its version.
3. It checks repository manifests and interrupted-operation markers without taking a long-lived
   write lock.
4. It inspects personal working-tree and local-ahead state. Automatic mode may make one bounded,
   non-interactive push retry; manual-remind mode records status without changing Git.
5. It opens or repairs the derived index metadata.
6. It exposes the capability-appropriate MCP tools.
7. Individual tools refresh only the sources they need and acquire locks only around mutation or
   local history integration.
8. On client disconnect, the process finishes the active atomic local step, records recoverable
   remote work, and exits. It does not remain resident to finish network retries.

Startup must be bounded. Authentication prompts, slow fetches, and full index rebuilds occur only
through a relevant operation or explicit setup/doctor flow, not before the MCP handshake.

## Synchronization Design

### Source health states

| State | Meaning | Allowed behavior |
|---|---|---|
| `healthy` | Local and configured remote identity are valid; no known unsynchronized state. | Read and permitted writes. |
| `working-tree-pending` | Valid authored Markdown has not been committed. | Read and permitted capture; remind in manual mode or retry automatic commit. |
| `local-ahead` | Valid local commits have not reached the remote. | Read, append new task logs when safe, and retry push. |
| `remote-ahead` | The remote has non-conflicting changes not yet integrated locally. | Read cached state; integrate under lock before mutation. |
| `diverged` | Local and remote histories require integration. | Attempt non-conflicting rebase; stop on conflict. |
| `offline` | Network is unavailable or timed out. | Read local sources and permit recoverable personal capture. |
| `authentication-error` | Remote credentials or access failed. | Read local data; retain commits; block uncertain pushes. |
| `conflict` | Automatic Git integration encountered a textual conflict. | Preserve both histories, stop mutation, and report recovery. |
| `indeterminate` | Repository identity and the local snapshot are valid, but local tracking data cannot determine synchronization state. | Read validated local state; block synchronization-sensitive mutation until tracking state is known. |
| `invalid-identity` | Manifest, owner, remote, or configured role disagrees. | Read only when safe; no mutation or push. |
| `corrupt` | Git or knowledge validation cannot establish a safe baseline. | No mutation; diagnostic/recovery only. |

### Mutation transaction

Every capture or incorporation uses this pipeline:

1. Resolve the fixed personal source and requested logical document handles.
2. Acquire the personal repository cross-process write lock with a bounded timeout.
3. Revalidate manifest, owner, remote, and working-tree assumptions.
4. Abort without editing if unexpected authored changes overlap the requested mutation.
5. Apply the file changes through a temporary/atomic write strategy.
6. Run scoped schema, link, identifier, and organization validation.
7. Update the local index transactionally.
8. In manual-remind mode, record `working-tree-pending` without staging or changing Git.
9. In automatic mode, record the pending validated paths and, when the operation reaches the
   configured checkpoint trigger, create a signed commit using the agent-supplied natural
   sentence, fetch and safely integrate remote history, and attempt a bounded non-interactive
   push.
10. Record `healthy`, `working-tree-pending`, `local-ahead`, or a more specific recovery state.
11. Release the lock.

The authored working tree is the manual profile's durable outbox; the local commit is the
automatic profile's push outbox. A separate queue does not duplicate Markdown contents. The
state database records expected file hashes, reminder throttles, and commits needing remote
confirmation.

### Remote integration

Automatic mode may use fetch plus rebase for non-conflicting personal history while under lock.
If Git reports a conflict, `kb` aborts the rebase, restores the pre-attempt working state, records
both commit tips, and asks the owner or an active agent to resolve it. It never chooses
last-write-wins or silently commits conflict markers. Manual-remind mode may fetch remote status
for diagnostics but never integrates or rewrites personal history.

Task-owned filenames make ordinary parallel capture unlikely to conflict. Incorporation is more
likely to overlap and therefore always verifies expected destination hashes after synchronization.

### Read-only refresh

Canon and peer clones refresh lazily when their configurable freshness threshold has elapsed. The
default lease is five minutes. The first relevant query then attempts a non-interactive fetch
within a configurable two-second default wait budget. If a new valid tip exists, `kb` performs an
explicit fast-forward rather than inheriting user `git pull` behavior. Timeout, offline, or
authentication failure returns the last valid index with its revision and a stale warning. An
explicit sync uses a separately configurable longer timeout. A state-database refresh lease
prevents concurrent MCP processes from duplicating the fetch.

## Search And Index Design

The first version uses lexical search rather than embeddings. Markdown is parsed into document
and addressable-entry records. Each record carries:

- source id, source kind, owner, and source revision;
- project and repository role;
- document path, title, headings, and stable id where present;
- initiative and archive state;
- applicability and verification metadata;
- task-entry state and parent feature; and
- text plus outbound links.

The index stores no source the current configuration cannot read. Removing permission or a
source configuration removes its rows before the next query returns results.

Index freshness is derived from source HEAD plus a fingerprint of permitted authored working
changes. After a `kb` mutation, affected records update immediately. After an external repository
change, the next query performs an incremental scan. A missing or incompatible index triggers a
rebuild without changing the source repositories.

Default search filtering follows the repository reading order:

1. current-system documents for the requested applicability;
2. relevant initiative documents when future/in-progress material is requested;
3. decisions and incorporated task evidence;
4. pending task entries only for explicit local/in-progress queries; and
5. sources and archives only when requested or needed as labeled evidence.

Ranking may use title, heading, exact stable id, subject terms, curated-index membership, and
role. It must not collapse results from different authority or environment states into one row.

The initial cross-source comparison boundary is mechanical and limited to authority-filtered
whole-document rows actually returned by one search. When distinct logical sources share project,
non-null stable document id, and applicability but have different content hashes, `kb` preserves
every attributed row and rank, marks each `comparison-required`, and emits one deterministic
redacted warning. Matching hashes, missing stable ids, different applicability or projects,
single-source evidence, and evidence excluded by query limits remain `not-assessed`. Task-entry
fragments are excluded because their hashes cover only an entry while their document metadata
identifies the parent log. This boundary requests active-agent comparison; it does not infer a
semantic contradiction, deduplicate evidence, or choose an authority winner.

### Candidate shared vocabulary

A small vocabulary registry is worth evaluating but is not an initial requirement. It would map
stable domain ids to a preferred label and scoped aliases, for example mapping `game client`,
`the game client`, and `Unreal client` to a canonical Ascent Rivals client component id without
requiring every contributor to use identical prose.

The registry should remain versioned, human-readable knowledge rather than hidden search state.
Canon would own shared terms; personal repositories could propose additional aliases. Search
could apply deterministic alias expansion while preserving the original query and reporting the
canonical id it matched. Ambiguous aliases such as `Ascent Rivals` would not be silently forced to
one component without scope or corroborating terms.

## MCP Tool Contract

### Normal contributor tools

| Tool | Mutation | Core behavior |
|---|---|---|
| `kb_status` | Local state only | Report identity, configured sources, revisions, sync/index health, workflow profile, grooming counts, and client adapter status. |
| `kb_search` | Optional read-only refresh | Return ranked attributed excerpts with filters and freshness. |
| `kb_read` | Optional read-only refresh | Read a fixed document or task-entry handle from a configured source. |
| `kb_begin_work` | Personal repository when a new log is needed | Create or resume a task-owned log and return a stable work handle. |
| `kb_capture` | Personal repository | Append one structured entry to the work handle's log, validate, index, and report synchronization state; automatic per-mutation mode may also commit and attempt push. |
| `kb_close_work` | Personal repository | Record completed, abandoned, superseded, or unknown only when explicitly supplied. |
| `kb_no_capture` | Local state only | Mark the work handle audited without creating a Markdown file or commit. |
| `kb_checkpoint` | Git only in automatic mode | Report outstanding knowledge changes; automatic mode commits eligible validated paths using the supplied natural sentence and retries push, while manual-remind mode only returns the reminder state. |
| `kb_groom` | None | Return a bounded grouped batch of pending evidence and current destinations for active-agent review. |
| `kb_dispose` | Personal repository | Apply explicit non-incorporation dispositions such as already-represented, rejected, or needs-owner. |
| `kb_incorporate` | Personal repository | Apply explicit expected-revision document updates and source dispositions as one transaction. |

All tools accept logical source, project, document, task, feature, or entry identifiers. They do
not accept arbitrary filesystem paths.

Personal mutating tools accept a natural one-sentence change description from the active agent.
Automatic mode uses that sentence unchanged as the visible commit message after basic one-line
validation. It adds no conventional prefix, work id, tool identity, trailer, or model name.
Manual-remind mode ignores it for Git because the contributor authors their own commits.

### Incorporation input

`kb_incorporate` receives:

- selected source entry ids;
- intended applicability;
- destination logical ids and expected content hashes;
- complete proposed Markdown content for each destination;
- the final disposition and backlink for each entry; and
- an optional curated decision/index update; and
- a natural one-sentence change description used only when automatic mode creates a commit.

The active agent generates this proposal. `kb` verifies current hashes, roles, links, metadata,
entry coverage, and repository policy. A stale destination returns a recompute-required error
with the new document handles; it does not merge prose automatically.

The initial pilot intentionally omits a custom patch language. Full-document replacement is
guarded by the expected content SHA-256 and validated diff scope. Section-level structured edits
may be added later only if fixtures show material token or reliability costs.

### Maintainer tools

| Tool | Behavior |
|---|---|
| `kb_prepare_canon` | Assemble attributed candidate changes, current canon, conflicts, and a proposal revision. |
| `kb_record_canon_disposition` | Record explicit acceptance, rejection, deferral, or origin-correction requests. |
| `kb_publish_canon` | Apply only the fully dispositioned approved proposal revision under the canon write lock. |
| `kb_record_deployment` | Append a component/environment deployment event with release evidence. |
| `kb_record_rollback` | Append rollback/retirement evidence and update the derived environment view. |

Maintainer tools should be delivered after the personal pilot. Their schemas must prevent a
normal end-of-turn audit from invoking publication or deployment mutations.

## Work Handles And Client Sessions

`kb_begin_work` returns a stable opaque work handle bound to owner, project, task id, agent role,
and optional parent feature. When a client exposes a stable task/thread identifier, its adapter
supplies it. Otherwise `kb` generates an id and the active agent retains the handle in task
context.

Reused coder or coordinator tasks resume the same handle. Separate parallel agents receive
different handles and therefore different log files. A lost handle can be recovered by owner,
project, client task id, and recent activity without guessing task completion.

No-capture and lifecycle-audit state is stored locally against the handle and current activity
marker. It is operational state, not knowledge history.

## Lifecycle Audit Adapters

Lifecycle hooks are optional recovery aids, not the primary capture mechanism. Each supported
client requires a small adapter verified against that client's current documented event model.

An adapter may request one active-agent audit only when it has a reliable material boundary such
as a handoff, explicit completion/acceptance, confirmed source-control boundary, or actual task
closure. It records a throttle marker before requesting the audit and recognizes `kb_capture`,
`kb_close_work`, `kb_incorporate`, or `kb_no_capture` as resolution.

If the event model exposes only ordinary response completion, the adapter remains disabled and
shared instructions ask the active agent to perform the check at meaningful boundaries. Client
support therefore does not depend on hook parity.

Adapters may also run deterministic `kb checkpoint --non-interactive` at a reliable boundary.
This consumes no model turn: manual-remind mode emits at most one throttled unsynchronized-change
notice, and automatic mode retries only operations already eligible for non-interactive Git.

## Instruction Distribution

Product repositories should carry one short tool-independent knowledge policy in `AGENTS.md`.
Where supported, `CLAUDE.md` imports that shared policy. Setup installs only a small generated
fallback in user-global instructions for configured projects lacking repository policy.

The generated block contains no paths. It tells agents to:

- search `kb` before material product or design assumptions;
- use task-owned capture for durable decisions and deltas;
- exclude prompts, plans, transcripts, routine execution, and build logs;
- incorporate only with acceptance evidence;
- preserve authority and applicability; and
- never infer deployment from source control or canon.

Adapter installation records a managed-block version so setup can update its own block without
rewriting unrelated user instructions.

## Setup And Platform Packaging

### Setup flow

`kb setup` performs these ordered steps:

1. Detect operating system, architecture, Git, supported clients, and existing installations.
2. Verify access to the configured GitHub repositories using existing Git credentials.
3. Identify contributor and device and validate the configured repository grants.
4. Clone or validate the personal, canon, and permitted peer repositories.
5. Select MCP-only or hybrid-read access and manual-remind or automatic synchronization.
6. If automatic synchronization is requested, confirm the dedicated SSH identity has no
   passphrase and verify non-interactive GitHub access and configured commit signing without
   reading the key.
7. Ask for a natural-language workflow description and infer the small workflow profile.
8. Write machine-local configuration.
9. Configure selected MCP clients and optional compatible audit adapters.
10. Install/update the managed instruction block.
11. Build the local index.
12. Run `kb doctor` and the non-mutating bootstrap verification.

Setup is idempotent. Re-running it reports proposed configuration changes and preserves healthy
clones and unrelated client configuration.

### GitHub repository provisioning

GitHub is the selected repository host. For the personal and first-coworker pilots, the owner or
organization administrator creates the personal, canon, template, and tooling repositories and
manages permissions in GitHub. `kb setup` accepts repository identities, verifies access through
the installed Git client, and clones them; it does not call a GitHub provisioning API or ask the
contributor to create forks, remotes, branches, commits, or pushes.

The authentication baseline is GitHub over SSH using the contributor's existing SSH client and
agent. Cliff's pilot uses the local `ikigai-github` host alias. Setup treats the SSH hostname and
remote URL as machine-local configuration so coworkers can use `github.com`, another alias, an
unencrypted key, or a differently managed SSH agent without changing shared knowledge files.

Cliff retains his passphrase-protected signing and push setup in manual-remind mode and continues
to run his normal Git commands. Automatic mode is opt-in and intended for a dedicated
non-passphrase SSH identity with repository-scoped access where practical. Setup verifies that
GitHub access and configured signing complete without a terminal or askpass prompt; it never
reads or stores private-key material. A failure leaves or returns the installation to
manual-remind mode.

Automated organization provisioning may be considered only if manual administration becomes a
real rollout burden. Deferring it keeps GitHub tokens, organization policy, and another API out
of the first implementation.

### Packages

The pilot should publish:

- a Linux x86-64 archive containing the `kb` executable and checksums;
- a native Windows x86-64 archive containing `kb.exe` and checksums; and
- a Nix package or flake wrapper after the Linux binary is proven on the pilot coworker's setup.

Cliff's WSL installation uses the Linux package. Setup writes a machine-local Windows client
command that invokes the configured distribution and absolute WSL binary directly through
`wsl.exe`; it does not require a wrapper or place those paths in a repository. The MCP server and
writable repository both remain inside WSL. The platform spike must prove stdio framing and clean
shutdown before this adapter is considered supported.

Automatic self-update is not required initially. Setup/doctor may report a newer supported
version; upgrades remain explicit and must migrate configuration/state atomically.

## Notion Boundary

The initial design delegates Notion retrieval to the agent client's existing authenticated
Notion integration. An active agent may cite a page and use `kb_capture` or `kb_incorporate` to
adopt durable conclusions with page identity and retrieval time.

Direct Notion indexing inside `kb` is deferred. This avoids duplicating authentication and keeps
Notion optional. Canon remains Markdown even when Notion supplied evidence.

## Security Model

The local process runs with contributor operating-system permissions, so its strongest boundary
is capability restriction rather than protection from the contributor or administrators.

- Configured logical sources map to fixed validated clones.
- Normal mode has no canon mutation handlers.
- Read authorization is applied before indexing and retrieval.
- Mutations check manifest kind, owner, remote, role, and expected document revision.
- Git owns credentials; configuration and logs contain no tokens.
- Tool output uses logical ids and repository-relative paths, not arbitrary local paths.
- Diagnostics redact command environment and remote credential material.
- Canon publication requires a separately authenticated maintainer mode and explicit proposal
  revision.

The tool does not attempt cryptographic isolation from organization administrators or malware
running as the same operating-system user.

## Diagnostics And Recovery

`kb doctor` reports each layer independently:

- executable and configuration versions;
- contributor/device identity;
- source manifests, roles, remotes, and access;
- Git and credential readiness;
- local-ahead, remote-ahead, offline, conflict, and authentication states;
- lock ownership and stale-lock recovery safety;
- index revision and rebuildability;
- configured clients and adapter versions;
- workflow profile and unresolved local work; and
- strict knowledge validation.

Recovery commands must be explicit and non-destructive. `kb` may clear a demonstrably stale lock
or rebuild derived state automatically, but it must not delete clones, commits, task entries, or
conflicted branches as a repair shortcut.

## Verification Strategy

### Unit and contract tests

- configuration and manifest parsing/version migration;
- path and source capability enforcement;
- Markdown/frontmatter/task-entry parsing;
- stable ids and controlled vocabularies;
- search filters, ranking, and source attribution;
- synchronization state transitions and error mapping;
- natural one-sentence commit-message validation;
- expected-hash incorporation behavior; and
- secret redaction.

### Repository fixtures

- valid personal, canon, peer, and template repositories;
- pending versus incorporated task logs;
- archive and applicability retrieval boundaries;
- duplicate ids, broken links, invalid status, and malformed metadata;
- non-conflicting parallel captures;
- conflicting incorporation edits; and
- partial deployment and rollback records.

The existing Python validator remains the conformance oracle until equivalent Rust behavior passes
the same fixtures. It should not be deleted merely because a partial validator exists in `kb`.

### Git integration tests

Use disposable local bare remotes to test:

- initial clone and identity validation;
- manual-remind capture without Git mutation and later externally completed synchronization;
- automatic capture, signed commit, push, offline retry, and non-interactive credential failure;
- two client processes appending different task logs;
- remote-ahead integration;
- non-conflicting divergence;
- textual conflict preservation;
- authentication/remote rejection mapping; and
- crash recovery between file write, index update, commit, and push; and
- proof that MCP and hook invocations cannot open terminal or askpass credential prompts.

### Client smoke matrix

At implementation time, verify the then-current supported versions of:

- Codex with Linux/WSL `kb mcp`;
- Windows Codex or Cursor invoking the WSL-owned process;
- Claude Code on the pilot Linux/Nix workstation; and
- native Windows Cursor with `kb.exe`.

For each client, verify MCP startup, tool schemas, search/read, dry-run capture, real disposable
capture, error rendering, instruction discovery, and lifecycle audit behavior when enabled.

## Implementation Slices

Implementation and rollout use this evidence-gated order:

1. Build the executable foundation: configuration, repository manifests, status, doctor,
   validation, cross-process locking, and compact operation receipts.
2. Add read-only source management, lexical search, and complete attributed document reads.
3. Add direct personal capture and incorporation, manual-remind Git status, and offline recovery.
4. Dogfood those self-only paths during ordinary work before broadening the mutation model.
5. Add a provisional one-log-per-task parallel-capture surface.
6. Exercise one real feature with at least two parallel logs and serialized incorporation.
7. Add bounded grooming with pending, incorporated, already-represented, abandoned, and
   needs-owner outcomes without autonomous semantic decisions.
8. Groom one real mixed batch, then refine and version the task-log, receipt, and grooming schemas
   plus any affected organization rules.
9. Extract the reusable repository template and prepare the contributor handoff only after those
   cases pass.
10. Host and validate the personal/template repositories, then onboard one willing coworker.
11. Add peer/canon review and deployment-event adapters only after two personal repositories
   provide useful evidence.

Detailed planning may proceed for steps 1 through 4 now. Field-level compatibility is not promised
for the provisional parallel and grooming schemas before step 8. Every mutating slice must expose
the paths and identifiers changed, the reason, any lifecycle transition, validation result, and
synchronization state so the client can keep knowledge maintenance visible without making it a
separate contributor chore.

## Technical References

- [Official MCP Rust SDK](https://github.com/modelcontextprotocol/rust-sdk)
- [MCP server resources](https://modelcontextprotocol.io/specification/2025-03-26/server/resources)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)
- [Codex sandboxing](https://learn.chatgpt.com/docs/sandboxing)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Claude Code MCP](https://code.claude.com/docs/en/mcp)
- [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Cursor MCP](https://docs.cursor.com/context/model-context-protocol)
- [Cursor permissions](https://docs.cursor.com/cli/reference/permissions)
- [Cursor hooks](https://cursor.com/docs/hooks)
- [GitHub SSH-agent setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub commit-signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [SQLite overview](https://sqlite.org/about.html)
- [SQLite FTS5](https://www.sqlite.org/fts5.html)
- [SQLite write-ahead logging](https://www.sqlite.org/wal.html)
- [`rusqlite`](https://github.com/rusqlite/rusqlite)
- [RocksDB overview](https://github.com/facebook/rocksdb/wiki/RocksDB-Overview)
- [Basic Memory](https://github.com/basicmachines-co/basic-memory)
- [`ai-memory` architecture](https://github.com/akitaonrails/ai-memory/blob/main/docs/ARCHITECTURE.md)
- [Graphiti temporal context graph](https://github.com/getzep/graphiti)
- [Argo CD sync and health example](https://github.com/argoproj/argo-cd/blob/master/docs/getting_started.md#7-sync-deploy-the-application)
- [Flux Kustomization status and reconciliation](https://fluxcd.io/flux/components/kustomize/kustomizations/)
- [GitHub deployments](https://docs.github.com/en/rest/deployments/deployments)
- [GitHub artifact deployment records](https://docs.github.com/en/rest/orgs/artifact-metadata)
- [CDEvents continuous deployment events](https://cdevents.dev/docs/continuous-deployment-pipeline-events/)

## Technical Decision Register

These stable ids retain the reviewed technical choices and distinguish the remaining deployment
question from implementation verification work.

### KBTD-001 — Setup profiles

**Status:** Adopted 2026-07-20.

Keep three orthogonal profiles rather than one bundle:

- **access:** `mcp-only` or `hybrid-read`;
- **synchronization:** `manual-remind` or opt-in `automatic`; and
- **workflow:** the existing inferred coordinator, single-session, or conservative behavior.

Setup always installs MCP. It asks whether native reads should be enabled and otherwise infers
the workflow profile from the contributor's description. Hybrid reads are enabled only where the
client can grant an acceptably narrow read capability; otherwise setup explains the limitation
and retains MCP-only access. Access grants and machine paths remain in user-local client
configuration.

### KBTD-002 — Schema depth and format

**Status:** Adopted 2026-07-20.

Use the current versioned envelopes, but defer a field-by-field schema freeze until
implementation slice 1 produces fixtures. Local configuration and repository manifests remain
YAML. Durable task entries, canon proposals, adoption records, and deployment events remain
Markdown with versioned YAML frontmatter rather than becoming opaque YAML databases. The Rust
binary embeds the accepted schemas, and readable schema files plus valid/invalid fixtures live in
the tooling repository. Unknown major versions fail closed; minor additive fields are preserved.

Sequential retrieval and rebuildable-index versions created during the private pilot are
implementation checkpoints, not a compatibility commitment to external consumers. Before the
template and coworker handoff, review whether obsolete pilot schemas should be removed and the
surviving contracts renumbered as one deliberate baseline. Preserve multiple versions only when a
real supported consumer or durable migration boundary requires them.

### KBTD-003 — Read-only source refresh

**Status:** Adopted 2026-07-20, with configurable timing.

Use configurable freshness, bounded-wait, and explicit-sync timeouts with defaults of five
minutes, two seconds, and thirty seconds. The first relevant search or read after freshness expiry
attempts a non-interactive `git fetch`. For canon and peer clones, `kb` verifies the fetched tip
and performs an explicit fast-forward update rather than relying on user `git pull` configuration.
Timeout, offline, or authentication failure returns the last valid index with its revision and a
stale warning. A shared refresh lease prevents concurrent MCP processes from repeating the fetch.

### KBTD-004 — Credential-aware Git persistence

**Status:** Adopted 2026-07-20 with manual-remind as Cliff's default and automatic Git as opt-in.

Separate four observable states: authored changes saved locally, signed local commit created,
commit awaiting push, and remote synchronized. Never permit Git, SSH, or the signer to prompt on
MCP standard input/output or from a lifecycle hook.

`manual-remind` writes, validates, and indexes Markdown immediately but never stages, commits,
pulls, rebases, or pushes the personal repository. `kb_status`, mutation results, and reliable
boundary hooks may emit a concise throttled reminder until the contributor's own Git operations
restore a clean synchronized state. This is Cliff's profile.

`automatic` is explicit opt-in for a contributor-confirmed non-passphrase SSH identity that
passes non-interactive GitHub access and configured-signing checks. Its default trigger is a
meaningful checkpoint supplied by the active agent; a contributor may explicitly select
per-mutation synchronization. It retries recoverable local-ahead work later. Failure preserves
the working changes or local commits and produces a reminder; it never falls back to prompting.

### KBTD-005 — Git identity and commit messages

**Status:** Adopted 2026-07-20 with natural agent-supplied messages.

Inherit the contributor's repository or global Git `user.name`, `user.email`, signing format,
signing key, and `commit.gpgSign` policy. Do not invent a shared bot identity and do not bypass
required signing. Missing identity or unavailable signing is a recoverable automatic-sync state.

The active agent supplies one natural sentence describing what the commit contains, for example,
`Document how team invitations and membership work.` The tool validates that it is one line and
uses it unchanged. It adds no formal prefix, identifier trailer, machine path, or model name.

### KBTD-006 — Logical handles and edit representation

**Status:** Adopted 2026-07-20.

Use resource-shaped logical handles such as `kb://personal/ascent-rivals/system/teams.md#entry-id`
without exposing local absolute paths. Reads return a source revision and content SHA-256.
Initial incorporation accepts a complete replacement Markdown document plus the expected hash,
source entries, and dispositions. This is simpler and safer than inventing a patch language for
the pilot; validation can reject unintended scope changes. Add section-level structured edits
later only if full-document replacement proves materially wasteful.

### KBTD-007 — Client support and lifecycle adapters

**Status:** Adopted 2026-07-20.

Set the version floor at implementation time by capability tests, not hard-coded product version
numbers in this design. Required support is user-local stdio MCP and ordinary tool invocation.
Per-tool approval controls, external read grants, and lifecycle hooks are adapter capabilities,
not core requirements.

Codex and Claude currently expose usable lifecycle hooks, while Cursor's hook surface is evolving.
Use hooks only for deterministic `kb checkpoint --non-interactive` and a carefully throttled
missed-capture audit. Core search, capture, and recovery must remain functional without them.
Test the latest stable client and the immediately preceding supported release where practical.

### KBTD-008 — Windows clients using the WSL-owned installation

**Status:** Adopted 2026-07-20, subject to the platform spike.

For Cliff's machine, have setup write a user-local Windows client command that launches
`wsl.exe -d <configured-distribution> --exec <absolute-wsl-kb-path> mcp`. Do not place that
distribution or path in shared repositories. Avoid a shell wrapper so startup output cannot
corrupt MCP framing. A native Windows `kb.exe` is used only when Windows owns a separate native
clone, as in a native-Windows coworker installation.

### KBTD-009 — Canon rejection and correction feedback

**Status:** Adopted 2026-07-20.

Store adopted, deferred, excluded, conflict, and correction-request dispositions in the canon
review outcome. A contributor's next canon refresh lets `kb_status` surface outcomes addressed to
that owner. The owner or their agent may then correct, supersede, or explicitly retain the
personal material. Do not add email, Slack, GitHub issues, or direct writes to personal
repositories in the pilot.

### KBTD-010 — Deployment evidence integration

**Status:** Adopted 2026-07-20.

Keep verification, canon adoption, and deployment to a named environment distinct; source-control
work state remains a fourth independent dimension. Moving knowledge into canon indicates team
adoption, not runtime deployment. Canon `synced_at` reports knowledge freshness; a separate
deployment `last_observed_at` reports runtime-evidence freshness. Neither timestamp upgrades an
unknown environment to deployed.

Use append-oriented deployment evidence plus a compiled current view. This adapts GBrain's
current-synthesis-plus-timeline pattern and the observed-state separation used by Argo CD and
Flux without importing their infrastructure. Durable events remain readable Markdown with
versioned YAML frontmatter; SQLite stores only the rebuildable current view and indexes.

The pilot event vocabulary is:

- `verification-succeeded`;
- `deployment-attempted`;
- `deployment-succeeded`;
- `deployment-failed`;
- `deployment-rolled-back`; and
- `deployment-removed`.

Every event has a stable event id, schema version, component id, event type, occurrence time,
recording time, and stable evidence. Verification events identify their applicability or
environment. Deployment events also identify a configured environment and the strongest
available artifact identity: Git revision, artifact digest or version, Perforce changelist, or
another stable release identifier. A correction appends a replacement event linked to the
incorrect record; it does not edit the historical evidence in place.

For each component and environment, the compiled view keeps these fields independent when
evidence exists:

- latest attempted revision and result;
- last successfully deployed revision;
- observed presence state: `unknown`, `deployed`, or `removed`;
- last observation time and evidence; and
- runtime health, which remains separate and defaults to `unknown`.

A failed attempt does not erase an older successfully deployed revision. A rollback identifies
the restored revision when known. Evidence becoming old does not silently make the deployment
false or unknown; results say when the state was last observed and may label it stale. Only an
explicit deployment, rollback, removal, correction, or later observation changes the compiled
state.

Manual maintainer- or agent-recorded events are the baseline. After a canon refresh, `kb_status`
may surface a bounded optional checkup for adopted features whose required component state is
unknown or stale. Silence leaves the state unknown. GitHub deployment or artifact records,
CDEvents producers, CI/release systems, and Perforce-aware release tooling may become adapters
later, but they must emit the same evidence model and must not infer deployment from a commit,
merge, submit, shelf, or canon adoption.
