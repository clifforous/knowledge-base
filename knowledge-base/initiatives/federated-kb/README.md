# Federated Knowledge Base Initiative

Status: in-progress
Status detail: The self-only personal tool pilot is approved to begin. Parallel task-log and
grooming behavior remain provisional dogfood gates before template extraction and coworker use.

Last consolidated: 2026-07-23

## Outcome And Boundary

Deliver a local, on-demand MCP tool that lets Codex, Claude Code, and Cursor search attributed
personal, canon, peer, and optional external knowledge through MCP or an optional native-read
profile; capture durable personal decisions only through controlled tool operations; either hide
Git synchronization or leave it to the contributor with reminders; and preserve explicit canon
and deployment boundaries.

The tool does not prescribe how contributors plan or delegate work, run a background semantic
service, autonomously consume model tokens, replace Perforce, or add project-management features.

## Reading Order

1. [Requirements](requirements.md) for normative behavior and acceptance.
2. [Workflow design](federated-personal-and-canonical-knowledge-workflow.md) for contributor
   experience, knowledge lifecycle, canon, and rationale.
3. [System design](system-design.md) for process architecture, components, local state, MCP,
   synchronization, indexing, setup, packaging, and verification.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Manual repository workflow | `implemented` | [Organization policy](../../../ORGANIZATION.md), [Pass 3 ledger](../repository-restructure/pass-3-governance-ledger.md), [coordinated feature use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-coordinator-guided-feature-delivery), [cross-chat design use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-iterative-design-coordination-across-chats-and-a-live-artifact), and [direct implementation use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-analysis-gated-direct-feature-implementation) | In use in Cliff's personal repository; the coordinated Eventun/teams, Windows-originated Website V2 design, and direct Ascent Rivals implementation cases are recorded | Exercise the remaining parallel task-log and grooming cases during personal `kb` dogfood |
| Requirements and workflow design | `designing` | [Requirements](requirements.md) and [workflow design](federated-personal-and-canonical-knowledge-workflow.md) | `not-applicable` | Owner review and further ordinary-work observations |
| Tool system design | `approved` | [System design](system-design.md) and adopted KBTD register | The Arch WSL personal pilot has verified configuration, repository identity, attributed retrieval, and Codex MCP approval behavior; remaining retrieval and mutation behavior is unproven | Refine the design from personal dogfood while completing the accepted self-only slices |
| Reusable repository template | `not-started` | No template repository exists | `not-applicable` | Complete personal parallel-capture and grooming dogfood, then remove personal assumptions |
| Personal `kb` pilot implementation | `implementing` | Separate `kb` repository revision `ac5dba3` implements configuration, repository identity, status/doctor, attributed retrieval, rebuildable SQLite/FTS5 indexing, operation receipts, bounded lazy peer/canon refresh, mechanical cross-source comparison, and direct task-owned personal capture | Arch WSL: 87 reported tests plus formatting, strict Clippy, and diff checks; real stdio trials verified retrieval, refresh, source-owner safety, no-prompt annotated reads, and begin/capture/read/search behavior; capture uses caller-supplied task ids, repository-keyed locking, existing project boundaries, recoverable post-write receipts, and manual-remind without Git or network mutation | Install and dogfood capture in existing work, then implement expected-hash personal incorporation |

## Documents

- [Requirements](requirements.md)
- [Federated personal and canonical knowledge workflow](federated-personal-and-canonical-knowledge-workflow.md)
- [System design](system-design.md)

## Authoritative Current System

- [Knowledge-base organization policy](../../../ORGANIZATION.md)
- [Repository agent policy](../../../AGENTS.md)
- [Current repository support tools](../../../tools/README.md)

## Remaining Before Closure

- Implement and personally dogfood the bounded self-only slices in the accepted delivery order.
- Complete and evaluate the parallel task-log and grooming cases recorded in the Pass 3 ledger.
- Refine provisional schemas and policy from that evidence.
- Extract and exercise a reusable repository template without machine or owner assumptions.
- Validate the coworker and canon pilots in sequence.
- Incorporate accepted tool behavior into `knowledge-base/system/` before archiving this
  initiative.
