# Federated Knowledge Base Initiative

Status: in-progress
Status detail: The self-only personal tool pilot is approved to begin. Parallel task-log and
grooming behavior remain provisional dogfood gates before template extraction and coworker use.

Last consolidated: 2026-07-22

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
| Tool system design | `approved` | [System design](system-design.md) and adopted KBTD register | Rust toolchain verified in Arch WSL; implementation and client behavior remain unproven | Create the separate implementation repository and complete the first self-only vertical slice |
| Reusable repository template | `not-started` | No template repository exists | `not-applicable` | Complete personal parallel-capture and grooming dogfood, then remove personal assumptions |
| Personal `kb` pilot implementation | `implementing` | Separate `kb` repository revision `244af1f` implements configuration, repository identity, local-only status/doctor, MCP `kb_status`, and the operation-receipt contract | Arch WSL: formatting, clippy with warnings denied, 21 tests, and real stdio MCP framing verified; not deployed | Implement and verify attributed read/search, then continue through the accepted self-only slices |

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
