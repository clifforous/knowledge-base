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

### KB-2026-006 — kb is an on-demand deterministic MCP tool without a daemon

- **Date:** 2026-07-20
- **Status:** Adopted design direction; implementation has not started.
- **Changed:** From leaving background retry, indexing, and scheduled knowledge work as possible
  operating modes to one on-demand stdio MCP process per client connection, with persistent Git
  and local derived state carrying recoverable work between invocations.
- **Why:** The knowledge workflow should not require a resident process, create another service
  contributors must understand, or autonomously consume Codex, Claude, Cursor, embedding, or
  other model tokens. Semantic work belongs to the agent already active in the user's task;
  deterministic retry and indexing can run at safe invocation boundaries.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-007 — Implement kb in Rust

- **Date:** 2026-07-20
- **Status:** Adopted design direction; implementation has not started.
- **Changed:** From Go as the proposed implementation language to Rust using the official MCP
  Rust SDK for native Linux and Windows executables.
- **Why:** Rust is the owner's preferred systems language, has maintained MCP protocol support,
  and meets the cross-platform single-binary design without giving up a capability required from
  the earlier Go proposal. Cross-platform build and packaging complexity will be tested in the
  implementation spike.
- **Affected knowledge:** [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-008 — Use manually provisioned GitHub repositories for the pilot

- **Date:** 2026-07-20
- **Status:** Adopted for the personal and first-coworker pilots.
- **Changed:** From an unselected Git host and possible provisioning API to owner-created GitHub
  repositories with permissions managed in GitHub and access verified through installed Git.
- **Why:** The team already uses GitHub for this purpose, the owner can manage the small initial
  repository set, and avoiding provisioning automation removes credentials and onboarding logic
  that the pilot does not yet need. GitHub access uses the installed Git client's SSH
  configuration and agent; Cliff's machine-local baseline is the `ikigai-github` SSH host alias,
  while other contributors may use `github.com` or their own local alias.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-009 — Use bundled SQLite FTS5 for kb derived state and lexical search

- **Date:** 2026-07-20
- **Status:** Adopted design direction; implementation has not started.
- **Changed:** From SQLite as a proposed choice still competing with other embedded stores to
  bundled SQLite through `rusqlite`, with FTS5 for the initial attributed lexical index.
- **Why:** The expected corpus is small, the tool needs transactions, structured filters, and
  full-text ranking, and the database is rebuildable local state rather than durable knowledge.
  A RocksDB-style key-value engine would require additional query and full-text abstractions for
  scale and write throughput the pilot does not need.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md) and
  [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-010 — MCP is the portable boundary with optional contributor-enabled native reads

- **Date:** 2026-07-20
- **Status:** Adopted design direction; client-specific enforcement remains to be validated.
- **Changed:** From requiring MCP-only access on every installation to retaining MCP as the
  universal retrieval and sole mutation contract while permitting a hybrid profile with native
  read-only Markdown browsing.
- **Why:** Direct file search can be smoother for hands-on contributors, while MCP preserves a
  consistent attributed interface and controlled mutations across Codex, Claude Code, and
  Cursor. The contributor or administrator grants the profile; an agent cannot grant itself
  broader access.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-011 — kb setup keeps access, synchronization, and workflow profiles independent

- **Date:** 2026-07-20
- **Status:** Adopted for the pilot design.
- **Changed:** From one implied contributor setup to independent MCP-only/hybrid-read access,
  manual-remind/automatic Git synchronization, and inferred work-style profiles.
- **Why:** Filesystem capability, credential behavior, and the way a contributor works are
  separate choices. Keeping them separate lets Cliff browse directly and retain his manual Git
  workflow without imposing either choice on a coworker using one continuing Claude session.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-012 — Durable kb schemas remain human-readable Markdown

- **Date:** 2026-07-20
- **Status:** Adopted for the pilot design; exact fields await implementation fixtures.
- **Changed:** From leaving all record encodings open to using Markdown with minimal versioned
  YAML frontmatter for task, canon, adoption, and deployment knowledge. Pure YAML is limited to
  local configuration and small repository manifests.
- **Why:** The repository must remain useful to people and agents without the executable or its
  SQLite index. Fixtures can refine field-level schemas without replacing readable knowledge
  with an opaque tool-owned database.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md) and
  [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-013 — Personal Git persistence defaults to manual reminders

- **Date:** 2026-07-20
- **Status:** Adopted for Cliff's pilot; automatic mode remains an opt-in contributor profile.
- **Changed:** From committing and pushing every personal mutation by default to saving,
  validating, and indexing Markdown while leaving Cliff's staging, natural commit description,
  signing, and push workflow untouched. `kb` provides a throttled unsynchronized-change reminder.
- **Why:** Cliff already curates commits and uses passphrase-protected signing and GitHub keys.
  Contributors who want hidden Git may opt into automatic synchronization only with a confirmed
  non-passphrase SSH identity and verified non-interactive GitHub and signing behavior.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  and [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-014 — Adopt the pilot interoperability and canon-feedback defaults

- **Date:** 2026-07-20
- **Status:** Adopted design direction; Windows-to-WSL stdio remains to be proven by a spike.
- **Changed:** To logical `kb://` handles with expected-hash full-document replacement,
  capability-tested client floors and optional hooks, direct machine-local `wsl.exe` MCP launch,
  and canon-hosted correction outcomes without email, Slack, or issue integrations.
- **Why:** These choices keep the first implementation small, portable, attributable, and
  reversible while leaving client-specific behavior behind tested adapters.
- **Affected knowledge:** [system design](../initiatives/federated-kb/system-design.md).

### KB-2026-015 — Derive deployment truth from explicit observed-state events

- **Date:** 2026-07-20
- **Status:** Adopted for the design; initial capture remains manual and implementation has not
  started.
- **Changed:** From an unresolved deployment-certainty model to append-oriented verification,
  deployment, failure, rollback, and removal events with a rebuildable current view per component
  and named environment.
- **Why:** Knowledge adoption, source-control availability, deployment attempts, successful
  deployment, and runtime health are independent facts. The event model preserves evidence,
  represents partial and failed rollouts without erasing an older deployed revision, and allows
  future GitHub, CI, CDEvents, or Perforce-aware adapters without making any adapter mandatory.
- **Affected knowledge:** [requirements](../initiatives/federated-kb/requirements.md) and
  [system design KBTD-010](../initiatives/federated-kb/system-design.md#kbtd-010--deployment-evidence-integration).

### KB-2026-016 — Treat direction to the next step as bounded checkpoint acceptance

- **Date:** 2026-07-20
- **Status:** Applied to repository policy.
- **Changed:** From recognizing only explicit approval or source-control completion as reliable
  incorporation signals to also recognizing owner-directed progression after a bounded result as
  acceptance of that immediately preceding checkpoint.
- **Why:** Existing long-running agent tasks advanced correctly when the owner asked for the next
  step but did not consistently update initiative gates or record the material decisions that had
  just become the working baseline. Bounded progression acceptance captures that ordinary
  conversational signal without treating silence, unrelated continuation, implementation, or
  deployment as approved.
- **Affected knowledge:** [organization policy](../../ORGANIZATION.md), [agent policy](../../AGENTS.md),
  and the [Pass 3 governance ledger](../initiatives/repository-restructure/pass-3-governance-ledger.md).

### KB-2026-017 — Start the self-only kb pilot before the remaining empirical cases

- **Date:** 2026-07-22
- **Status:** Adopted delivery order; implementation has not started.
- **Changed:** From deferring all `kb` implementation until manual parallel-capture and grooming
  cases were complete to building the bounded self-only foundation, retrieval, status, visible
  receipts, and direct capture path first, then using that tool during those remaining cases.
- **Why:** Three distinct live workflows already validate direct, coordinator-guided, and
  cross-environment knowledge updates. Building the small personal surface now lets the remaining
  cases evaluate the intended contributor experience while retaining explicit gates against
  premature schema compatibility, template extraction, coworker onboarding, or canon work.
- **Affected knowledge:** [federated initiative](../initiatives/federated-kb/README.md),
  [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  [system design](../initiatives/federated-kb/system-design.md), and the
  [Pass 3 governance ledger](../initiatives/repository-restructure/pass-3-governance-ledger.md).

### KB-2026-018 — Structure capture destinations and separate work titles from receipt prose

- **Date:** 2026-07-23
- **Status:** Adopted from initial personal capture dogfood; implementation pending.
- **Changed:** From one delimiter-bearing destination string and an H1 derived from the first
  change description to independently validated destination values and a stable work title
  supplied separately from operation-receipt prose.
- **Why:** A live Website capture accepted semicolon-separated documents as one path-like value,
  while its first finding produced a task title narrower than the continuing coder task. Typed
  destinations remove ambiguous parsing, and a separate title keeps a reused task readable
  without making later receipt descriptions part of resume identity.
- **Affected knowledge:** [workflow design](../initiatives/federated-kb/federated-personal-and-canonical-knowledge-workflow.md),
  [system design](../initiatives/federated-kb/system-design.md), the
  [Website capture log](../../ascent-rivals/decisions/tasks/2026/2026-07-24-website-v2-coder-20260723.md),
  and the [teams capture log](../../ascent-rivals/decisions/tasks/2026/2026-07-23-teams-coder-20260723.md).
