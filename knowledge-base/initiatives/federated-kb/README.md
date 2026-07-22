# Federated Knowledge Base Initiative

Status: in-progress
Status detail: Requirements, workflow, and system design are being refined during manual
repository validation; tool implementation remains deferred until that checkpoint closes.

Last consolidated: 2026-07-21

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
| Manual repository workflow | `implemented` | [Organization policy](../../../ORGANIZATION.md), [Pass 3 ledger](../repository-restructure/pass-3-governance-ledger.md), [coordinated feature use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-coordinator-guided-feature-delivery), [cross-chat design use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-iterative-design-coordination-across-chats-and-a-live-artifact), and [direct implementation use case](federated-personal-and-canonical-knowledge-workflow.md#observed-use-case-analysis-gated-direct-feature-implementation) | In use in Cliff's personal repository; the coordinated Eventun/teams, Windows-originated Website V2 design, and direct Ascent Rivals implementation cases are recorded | Complete the remaining parallel task-log and grooming validation cases |
| Requirements and workflow design | `designing` | [Requirements](requirements.md) and [workflow design](federated-personal-and-canonical-knowledge-workflow.md) | `not-applicable` | Owner review and further ordinary-work observations |
| Tool system design | `designing` | [System design](system-design.md) | `not-applicable` | Resolve pilot-blocking technical decisions and validate with platform/client spikes |
| Reusable repository template | `not-started` | No template repository exists | `not-applicable` | Close the manual repository checkpoint and remove personal assumptions |
| Personal `kb` pilot implementation | `not-started` | No implementation repository or revision exists | `not-deployed` | Approve the personal-pilot requirement/design baseline after manual validation |

## Documents

- [Requirements](requirements.md)
- [Federated personal and canonical knowledge workflow](federated-personal-and-canonical-knowledge-workflow.md)
- [System design](system-design.md)

## Authoritative Current System

- [Knowledge-base organization policy](../../../ORGANIZATION.md)
- [Repository agent policy](../../../AGENTS.md)
- [Current repository support tools](../../../tools/README.md)

## Remaining Before Closure

- Complete and evaluate the manual-use cases recorded in the Pass 3 ledger.
- Review the proposed requirements and system design and resolve personal-pilot blockers.
- Extract and exercise a reusable repository template without machine or owner assumptions.
- Implement and validate the personal, coworker, and canon pilots in sequence.
- Incorporate accepted tool behavior into `knowledge-base/system/` before archiving this
  initiative.
