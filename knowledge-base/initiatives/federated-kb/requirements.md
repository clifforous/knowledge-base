# kb Tool Requirements

Status: proposed

Last revised: 2026-07-22

## Purpose

Define the normative requirements for the proposed `kb` tool and federated personal/canonical
knowledge workflow. The [workflow design](federated-personal-and-canonical-knowledge-workflow.md)
owns contributor behavior and rationale. The [system design](system-design.md) owns the proposed
implementation.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## Product Boundary

`kb` is a local, on-demand MCP and command-line tool that makes durable Markdown knowledge
available to agents working in otherwise sandboxed project workspaces. It manages the owner's
personal knowledge repository, reads permitted canon and peer repositories, and hides routine
Git mechanics when automatic synchronization is selected or reports outstanding work without
changing Git when manual-remind is selected.

It is not a project manager, agent framework, autonomous researcher, transcript archive, or
replacement for product source control.

## Supported Environments And Clients

### Platforms

- **KB-PLAT-001:** The initial tool MUST run on 64-bit Linux and native 64-bit Windows.
- **KB-PLAT-002:** The Linux distribution MUST work in Arch WSL and on an ordinary Linux/Nix
  workstation without depending on a desktop environment.
- **KB-PLAT-003:** Windows agents MUST be able to invoke either a native Windows installation or
  an explicitly configured WSL installation.
- **KB-PLAT-004:** One simultaneously active machine or operating-system installation MUST have
  only one writable clone of a personal repository.
- **KB-PLAT-005:** A dual-boot contributor MAY maintain one clone per operating system because
  the installations cannot run concurrently; setup MUST detect unsynchronized local work before
  treating a second installation as healthy.
- **KB-PLAT-006:** Shared repositories and instructions MUST NOT contain contributor-specific
  absolute paths. Setup MUST keep machine paths in local configuration.

### Agent clients

- **KB-CLIENT-001:** The supported client set MUST include Codex, Claude Code, and Cursor.
- **KB-CLIENT-002:** All clients MUST use the same core MCP tool contract.
- **KB-CLIENT-003:** Client-specific code MUST be limited to configuration, instruction, and
  optional lifecycle-hook adapters.
- **KB-CLIENT-004:** Search, read, capture, and synchronization MUST remain usable when a client
  lacks a reliable lifecycle hook.
- **KB-CLIENT-005:** Setup MUST detect supported installed clients where practical and MUST
  configure only clients selected by the contributor.
- **KB-CLIENT-006:** Client adapters MUST be versioned and compatibility-tested independently
  from the core repository and knowledge rules.
- **KB-CLIENT-007:** The contributor or administrator MUST select and authorize the client access
  profile. An agent MUST NOT grant itself MCP access, filesystem access, or broader source
  permissions.

## Execution And Token Use

- **KB-EXEC-001:** Normal operation MUST use an on-demand local MCP process, initially over
  standard input/output.
- **KB-EXEC-002:** `kb` MUST NOT require an always-running daemon, operating-system service,
  tray application, or scheduled task.
- **KB-EXEC-003:** The MCP process MUST be safe to start per client session and exit when its
  client closes it.
- **KB-EXEC-004:** Retryable synchronization, index refresh, and health work MUST run on a
  relevant command or MCP invocation. They MUST NOT depend on a background process.
- **KB-COST-001:** The `kb` executable MUST NOT call an LLM API, launch an autonomous agent, or
  consume a contributor's model subscription independently.
- **KB-COST-002:** Search, validation, indexing, Git operations, task-log writes, and status
  checks MUST be deterministic local operations except for configured repository or source
  network access.
- **KB-COST-003:** Semantic classification, synthesis, incorporation prose, and conflict
  resolution MUST use the agent already active in the contributor's task or explicit human
  review.
- **KB-COST-004:** A lifecycle adapter MAY request at most one capture audit at a meaningful
  work boundary. It MUST throttle by work stream, prevent loops, and prefer a missed audit over
  repeated token-consuming turns.
- **KB-COST-005:** Routine progress, questions, plans, review feedback, and intermediate coding
  turns MUST NOT trigger a visible capture audit.
- **KB-COST-006:** The contributor MUST be able to inspect and disable lifecycle adapters without
  disabling the core MCP tools.

## Repository And Authority Model

- **KB-REPO-001:** Durable knowledge MUST remain ordinary Markdown plus minimal portable
  metadata and links.
- **KB-REPO-002:** Search indexes, caches, locks, synchronization state, and credentials MUST be
  local derived state and MUST NOT be required to understand the repository.
- **KB-REPO-003:** Personal, canon, template, and tooling repositories MUST have explicit
  identities. Personal repositories MUST identify their owner.
- **KB-REPO-004:** Normal contributor tools MUST write only the configured personal repository.
- **KB-REPO-005:** Canon, peer, Notion, and other external sources MUST be read-only through the
  normal contributor tool surface.
- **KB-REPO-006:** Normal MCP tools MUST NOT accept arbitrary repository roots, filesystem paths,
  Git commands, or shell commands.
- **KB-REPO-007:** Canon publication MUST use a separate maintainer capability and explicit
  authorization.
- **KB-REPO-008:** Canon maintainers MUST NOT directly rewrite another contributor's personal
  repository through `kb`.
- **KB-REPO-009:** Repository structure, placement, metadata, task-log, and validation behavior
  MUST follow the template's versioned organization contract.
- **KB-REPO-010:** The initial personal and canon repositories MUST be hosted on GitHub and MAY
  be provisioned manually by the owner or organization administrator.
- **KB-REPO-011:** Durable task entries, canon proposals, adoption records, deployment events,
  and other authored knowledge MUST remain human-readable Markdown with minimal versioned YAML
  frontmatter. Pure YAML MAY be used for machine-local configuration and small repository
  manifests, but MUST NOT replace readable durable knowledge documents.

## Retrieval

- **KB-READ-001:** Agents MUST be able to search the configured personal, canon, and permitted
  peer sources from an unrelated product workspace.
- **KB-READ-002:** Notion MAY be configured as an attributed read-only source.
- **KB-READ-003:** Every result MUST retain source identity, repository role, project role,
  applicability, and known verification or conflict state.
- **KB-READ-004:** Search MUST prefer current-system documents and curated indexes over raw task
  logs and archives for ordinary current-state questions.
- **KB-READ-005:** Pending task-log entries MUST NOT be presented as accepted current truth.
- **KB-READ-006:** Archive results MUST be excluded from default current retrieval unless the
  query requests history or follows an explicitly labeled evidence link.
- **KB-READ-007:** Retrieval MUST support raw document reads so humans and agents can inspect
  underlying evidence rather than relying on synthesized answers.
- **KB-READ-008:** The first implementation MUST provide lexical/local full-text retrieval. It
  MUST NOT require remote embeddings or a model-powered search service.
- **KB-READ-009:** If sources disagree, `kb` MUST return the contradiction and source boundaries;
  it MUST NOT manufacture one answer.
- **KB-READ-010:** An installation MAY grant agents native read-only filesystem access to
  configured Markdown clones as a local browsing optimization. MCP MUST remain the portable
  retrieval contract and the only supported mutation path.
- **KB-READ-011:** Raw MCP reads MUST be able to return the complete Markdown document, subject
  to client transport limits, rather than requiring the agent to rely on synthesized summaries.

## Capture And Task Logs

- **KB-CAP-001:** Each agent task MUST write only its own append-oriented task decision/delta
  log during normal parallel capture.
- **KB-CAP-002:** Captures MUST use stable task and entry identifiers.
- **KB-CAP-003:** Capture types, task states, entry dispositions, paths, and required metadata
  MUST follow `ORGANIZATION.md` until a reviewed schema version replaces them.
- **KB-CAP-004:** A capture MUST contain a concise durable statement, rationale when material,
  evidence, intended applicability, and candidate destinations when known.
- **KB-CAP-005:** Prompts, transcripts, task lists, detailed execution steps, routine review
  feedback, and build output MUST NOT be stored as durable captures.
- **KB-CAP-006:** Capture MUST default to personal local-development applicability unless
  stronger environment evidence is supplied.
- **KB-CAP-007:** A no-capture acknowledgement MUST be local task/session state. It MUST NOT
  create a knowledge document or Git commit solely to record that no durable knowledge existed.
- **KB-CAP-008:** The tool MUST NOT require a task to declare itself complete. Unknown and stale
  MUST remain distinct from abandoned.
- **KB-CAP-009:** Parallel capture MUST NOT edit a shared task index or current-system document.

## Operation Transparency

- **KB-OBS-001:** Every mutating operation MUST return a compact receipt identifying what durable
  knowledge changed, why it changed, the affected document or task-entry identifiers, any accepted
  lifecycle transition, validation outcome, and current synchronization state.
- **KB-OBS-002:** Supported client instructions MUST tell the active agent to summarize that receipt
  for the contributor at meaningful checkpoints. A contributor MUST NOT need to ask separately
  whether the knowledge base changed or remember a knowledge-maintenance command.
- **KB-OBS-003:** A receipt MUST distinguish capture, incorporation, lifecycle acceptance,
  source-control state, verification, and deployment. Reporting one of these MUST NOT imply the
  others.

## Incorporation, Grooming, And Hygiene

- **KB-INC-001:** Pending task entries MUST become accepted current or initiative knowledge only
  through explicit incorporation or an accepted grooming disposition.
- **KB-INC-002:** The active agent or human MUST supply semantic document changes. `kb` MUST NOT
  generate or approve incorporation prose autonomously.
- **KB-INC-003:** Incorporation MUST re-read the latest destinations, detect changed expected
  revisions, update source dispositions, preserve evidence, update affected indexes, and
  validate the result atomically under a repository write lock.
- **KB-INC-004:** Incorporated destinations and source entries SHOULD link to one another when
  the origin remains useful.
- **KB-GROOM-001:** Grooming MUST be a bounded, explicitly initiated review of a selected scope.
- **KB-GROOM-002:** Mechanical grooming MAY group entries and detect identifiers, backlinks,
  metadata gaps, or exact duplicates. Semantic compatibility and conflict resolution MUST remain
  with the active agent or owner.
- **KB-GROOM-003:** Grooming MUST permit pending and needs-owner outcomes and MUST NOT force
  completion, abandonment, or consensus.
- **KB-HYG-001:** Hygiene checks MUST distinguish stale, unverifiable, drifted, obsolete, and
  still-valid knowledge.
- **KB-HYG-002:** Archive and deletion changes MUST remain proposal-only until explicitly
  accepted.

## Git Synchronization And Durability

- **KB-SYNC-001:** Setup MUST support a `manual-remind` synchronization profile and an explicit
  opt-in `automatic` profile. Each installation MUST select one profile independently of its
  access and workflow profiles.
- **KB-SYNC-002:** After a valid personal mutation, `kb` MUST atomically save and validate the
  Markdown, update its derived index, and expose whether the working tree, local history, and
  remote are synchronized. Local knowledge durability MUST NOT depend on remote authentication.
- **KB-SYNC-003:** An unavailable network or remote MUST NOT prevent local capture when the local
  repository identity and write scope are valid.
- **KB-SYNC-004:** In `manual-remind` mode, `kb` MUST NOT stage, commit, rewrite, pull, or push the
  personal repository. It MUST preserve authored working-tree changes and provide a concise,
  throttled reminder that the contributor's normal Git synchronization is still required.
- **KB-SYNC-005:** In `automatic` mode, `kb` MUST stage only its validated paths, create a local
  commit, and attempt a push at a configured checkpoint. Failed commits or pushes MUST remain
  recoverable and be retried on a later relevant invocation without a daemon. The default
  automatic trigger SHOULD be a meaningful work checkpoint; per-mutation synchronization MAY be
  selected explicitly.
- **KB-SYNC-006:** In automatic mode, non-conflicting remote changes MAY be integrated under the
  repository lock. A semantic or textual conflict MUST stop the mutation or synchronization and
  surface actionable status while preserving both sides. Manual-remind mode MUST NOT integrate
  personal history.
- **KB-SYNC-007:** Multiple local client processes MUST coordinate writes through a cross-process
  lock.
- **KB-SYNC-008:** Read-only sources MAY be refreshed lazily according to configurable freshness,
  bounded-wait, and explicit-sync timeout settings. Failure MUST fall back to the last valid local
  copy with an explicit freshness warning.
- **KB-SYNC-009:** Repository identity, owner, configured remote, and authorization MUST be
  checked before pushing.
- **KB-SYNC-010:** Automatic mode MUST be opt-in and MUST require a contributor-confirmed
  non-passphrase SSH identity plus successful non-interactive GitHub access and configured-signing
  checks. `kb` MUST NOT inspect, copy, or store private-key material.
- **KB-SYNC-011:** Git, SSH, and commit-signing processes invoked through MCP or lifecycle hooks
  MUST be non-interactive and bounded. They MUST NOT prompt on MCP standard input/output or open
  an askpass interaction.
- **KB-SYNC-012:** Automatic commits MUST inherit the contributor's Git author and signing policy.
  The active agent MUST supply a natural one-sentence description of the committed change; `kb`
  MUST NOT add standardized prefixes, work ids, tool names, or model names to the visible commit
  message.
- **KB-SYNC-013:** `kb` MUST never discard authored working-tree changes or local commits, bypass
  a required signature, or silently resolve a content conflict.

## Canon And Peer Knowledge

- **KB-CANON-001:** Canon review MUST begin only through an explicit maintainer action.
- **KB-CANON-002:** A canon proposal MUST preserve originating repositories, task entries,
  candidate changes, conflicts, and a disposition for every reviewed item.
- **KB-CANON-003:** Canon publication MUST apply only the reviewed proposal revision and MUST
  reject stale approval if canon changed meanwhile.
- **KB-CANON-004:** Rejected or conflicting personal material MAY produce an owner notification
  or correction request but MUST NOT be silently removed from its origin.
- **KB-CANON-005:** Peer repositories MUST remain attributed sources and MUST NOT become canon by
  retrieval, popularity, or repetition.
- **KB-CANON-006:** A contributor MAY seed a personal repository from canon, after which personal
  authorship and promotion rules apply normally.

## Environment And Deployment Truth

- **KB-ENV-001:** Knowledge authority, work state, source-control state, and runtime/deployment
  applicability MUST remain independent dimensions.
- **KB-ENV-002:** A commit, merge, Perforce shelf, Perforce submit, review, or canon adoption MUST
  NOT establish deployment.
- **KB-ENV-003:** Deployment MUST be recorded per required feature component and named
  environment with stable release evidence when available.
- **KB-ENV-004:** A feature MUST be reported as fully deployed only when all required components
  have compatible deployment evidence in that environment.
- **KB-ENV-005:** Partial deployments, rollbacks, retirements, and unknown components MUST be
  represented explicitly.
- **KB-ENV-006:** Production knowledge MUST cite explicit production evidence and MUST NOT be
  inferred from shared development or staging.
- **KB-ENV-007:** Environment names and deployable-component identities MUST be configurable.
- **KB-ENV-008:** Durable deployment history MUST be append-oriented. Corrections, rollbacks,
  removals, and later observations MUST preserve the prior evidence rather than rewriting it.
- **KB-ENV-009:** The last attempted revision, last successfully deployed revision, observed
  runtime state, and runtime health MUST remain independent when those signals are available.
  A failed attempt MUST NOT erase evidence for an older revision that remains deployed.

## Setup And Contributor Experience

- **KB-SETUP-001:** Initial contributor onboarding SHOULD complete in approximately ten minutes
  after required accounts and repository access exist.
- **KB-SETUP-002:** Setup MUST detect Git, supported clients, operating system, repository health,
  and existing configuration where practical.
- **KB-SETUP-003:** Setup MUST fail with a clear remediation when a required Git client or access
  grant is missing.
- **KB-SETUP-004:** Setup MUST configure selected MCP clients and the selected MCP-only or
  hybrid-read profile, clone or validate repositories, install the shared instruction block,
  and run a non-mutating verification.
- **KB-SETUP-005:** Setup SHOULD infer the contributor's workflow profile from one natural-language
  description and ask only materially necessary follow-up questions.
- **KB-SETUP-006:** No normal onboarding step may require the contributor to create a fork, add a
  remote, create a branch, commit, or push manually.
- **KB-SETUP-007:** `kb doctor` MUST report identity, source permissions, client integration,
  synchronization health, pending local commits, index health, workflow profile, and optional
  hook status without making durable knowledge changes.
- **KB-SETUP-008:** Uninstallation MUST remove client integration and local derived state without
  deleting a personal repository containing authored working-tree changes or unpushed commits
  unless the contributor explicitly confirms a safe disposition.
- **KB-SETUP-009:** Setup MUST keep access, synchronization, and workflow profiles independent.
  It MUST verify automatic-mode prerequisites before enabling automatic Git mutations and MUST
  otherwise select or fall back to `manual-remind`.

## Security And Privacy

- **KB-SEC-001:** Repository credentials MUST use platform or Git credential facilities and MUST
  NOT be stored in shared Markdown or plaintext `kb` configuration.
- **KB-SEC-002:** Tool responses MUST avoid exposing credentials, access tokens, arbitrary local
  files, or unrelated repository content.
- **KB-SEC-003:** Source authorization MUST be enforced before retrieval and before indexing
  content for a client.
- **KB-SEC-004:** Mutating tools MUST validate repository kind, owner, operation capability, and
  expected document revision.
- **KB-SEC-005:** Logs and diagnostics MUST redact secrets and SHOULD contain only operational
  metadata needed to diagnose `kb`.
- **KB-SEC-006:** Optional native filesystem reads MUST NOT make canon or peer clones writable
  and MUST NOT make direct writes to the personal clone a supported agent workflow.
- **KB-SEC-007:** The implementation MUST verify effective MCP and native-folder access under
  each supported client's sandbox and permission model; it MUST NOT assume that starting a local
  MCP process universally bypasses or inherits a particular sandbox boundary.

## Reliability And Performance

- **KB-NFR-001:** Ordinary status, read, and lexical-search operations SHOULD respond within two
  seconds against the expected small-team corpus when no network refresh is required.
- **KB-NFR-002:** Capture SHOULD complete locally within two seconds before any optional remote
  synchronization wait.
- **KB-NFR-003:** Network timeouts MUST be bounded and MUST not leave the repository lock held
  indefinitely.
- **KB-NFR-004:** Derived indexes MUST be rebuildable from permitted source repositories.
- **KB-NFR-005:** All mutations MUST be crash-recoverable through Git history or explicit local
  transaction state.
- **KB-NFR-006:** The initial distribution SHOULD be a self-contained executable per supported
  platform, excluding the allowed external Git dependency.
- **KB-NFR-007:** Repository clones and the SQLite state database MUST remain on a local native
  filesystem for the process that owns them; cross-environment clients MAY invoke that process
  but MUST NOT relocate its mutable state to a network or UNC filesystem.

## Initial Acceptance Matrix

Before the personal pilot is considered usable:

1. Codex in WSL can start the MCP server and search, read, capture, and synchronize Cliff's
   personal repository.
2. A Windows-hosted Codex or Cursor session can reach the same WSL-owned writable clone without
   creating a competing Windows clone.
3. A Linux/Nix Claude Code installation can complete setup against a separate personal
   repository.
4. Native Windows Cursor can complete setup and use a native `kb` binary.
5. An offline capture remains recoverable locally; automatic mode creates or later retries its
   commit and push, while manual-remind mode reports the outstanding working-tree change.
6. Two simultaneous client processes cannot corrupt or interleave a personal mutation.
7. Search preserves source, authority, role, applicability, and stale/conflict labels.
8. A pending task entry is not returned as current truth.
9. A one-shot lifecycle audit cannot loop or trigger on routine iterative turns.
10. No `kb` process makes an LLM or embedding-service request.
11. A failed pull, push, authentication, or index refresh preserves all previously valid local
    knowledge and reports a useful recovery state.
12. Strict knowledge-repository validation passes after capture and incorporation fixtures.
13. MCP-only and hybrid-read profiles enforce their intended read/write boundaries in the
    supported client/platform matrix.
14. Manual-remind mode leaves Git staging, commits, integration, and pushes unchanged while
    surfacing a throttled unsynchronized-change reminder.
15. Automatic mode cannot be enabled without its non-interactive SSH and configured-signing
    checks, and no MCP or hook test can produce a credential prompt.

Before the canon pilot is considered usable:

1. A maintainer can prepare a proposal from two attributed personal repositories.
2. Conflicts remain explicit and every candidate receives a disposition.
3. Canon cannot change through the normal contributor tool surface.
4. A stale canon proposal cannot be published after canon changes.
5. A multi-component feature can be adopted without being marked deployed.
6. Partial development deployment, partial production deployment, rollback, and retirement all
   produce correct environment-specific retrieval.

## Deferred Capabilities

The initial personal pilot does not require:

- an always-running daemon or background scheduler;
- model-generated embeddings, graph storage, or a vector database;
- autonomous grooming, synthesis, or canon review;
- embedded Git implementation;
- direct Notion ingestion inside `kb`;
- broad project-management, task-management, CRM, or agent-team features;
- release-system automation; or
- cryptographic isolation from organization administrators.

## Requirement Open Questions

- Which exact client versions and lifecycle-hook facilities form the supported compatibility
  floor at implementation time?
- Which repository-scoped non-passphrase SSH-key pattern should automatic-mode onboarding
  document for contributors who opt into hidden Git synchronization?
- Is native Windows Claude Code required for the first coworker pilot or only for broader
  rollout?
- Which performance corpus size should be used for the two-second local retrieval target?
- Which contributor actions, beyond explicit acceptance and source-control completion, are
  reliable enough to permit direct incorporation?
- Should canon refresh offer an optional checkup for adopted features with unknown or stale
  deployment evidence, without inferring deployment from canon freshness?
