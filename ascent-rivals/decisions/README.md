# Ascent Rivals Decision Log

## Purpose

Record concise, durable changes in direction without duplicating the current system
description.

Entries record the decision and its disposition. Linked current-system documents remain the
authority for how the system works now; linked archived designs preserve deeper rationale.

## Entry Shape

Each future entry should include a stable identifier and date, what changed from X to Y,
the rationale, affected documents, supporting evidence or task-log entries, and any later
superseding decision.

Future task-owned decision and delta logs may live under `tasks/`. Pending entries are
evidence and must not be presented as current truth before incorporation.

## Decisions

### AR-2026-001 — One identified complete-match ingest contract

- **Date:** 2026-07-13
- **Status:** Implemented in the known local-development state; production cutover remains
  separately gated.
- **Changed:** From fragmented or source-specific event submission toward one identified
  complete-match envelope submitted through shared `ClientService.IngestMatch` by both player
  and dedicated-server producers.
- **Why:** Stable batch/event identity, canonical hashing, producer ordering, derived source
  trust, and equal-content idempotency provide one repairable contract without duplicating
  APIs for authorization classes.
- **Affected knowledge:** [identified match ingestion](../system/eventun/identified-match-ingestion.md),
  [Eventun API](../system/eventun/api.md), [game client](../system/game-client.md), and
  [gauntlet runtime](../system/eventun/gauntlet-stage-runtime-contract.md).
- **Evidence:** [foundation/API review](../sources/analysis/eventun-foundation-api-simplification-review.md).

### AR-2026-002 — Product seasons are separate from telemetry storage lifecycle

- **Date:** 2026-07-17
- **Status:** Season catalog and season-aware serving implemented locally; retention and
  archive choices remain open.
- **Changed:** From a proposed general competition-period/storage concept to explicit
  Eventun-owned product seasons while storage segments, retention tiers, game builds, Season
  Pass, and MMR ownership remain independent concepts.
- **Why:** Product comparison windows and physical data lifecycle have different owners and
  change at different rates.
- **Affected knowledge:** [identified match ingestion](../system/eventun/identified-match-ingestion.md),
  [data model](../system/eventun/data-model.md), and the active
  [telemetry lifecycle plan](../initiatives/eventun-foundation/eventun-telemetry-lifecycle-plan.md).
- **Evidence:** [insights/progression/seasons review](../sources/analysis/eventun-insights-progression-seasons-review.md).

### AR-2026-003 — Progression runtime uses immutable published snapshots

- **Date:** 2026-06-16
- **Status:** Incorporated into the known local-development state; operator UI follow-through
  remains active.
- **Changed:** From goal-version activation and row-level active flags as the runtime model to
  editable drafts plus immutable published goal and challenge-pool snapshots.
- **Why:** Later authoring edits must not rewrite assignments, completion history, or reward
  semantics already presented to players.
- **Affected knowledge:** [progression](../system/eventun/progression.md),
  [data model](../system/eventun/data-model.md), and the active
  [progression initiative](../initiatives/eventun-progression/README.md).
- **Evidence:** [archived progression design set](../archive/initiatives/eventun-progression/README.md).

### AR-2026-004 — Recommendations became backend-owned Insights

- **Date:** 2026-04-03
- **Status:** Backend and manual game-client integration implemented locally; automatic
  pre-summary presentation remains open.
- **Changed:** From recommendation endpoints and a recommendation-only player concept to typed
  Insights that can return coaching, kudos, no insight, pending, unavailable, or failed.
- **Why:** The system needs to praise strong play, suppress low-credibility advice, and expose
  readiness explicitly while keeping selection policy in Eventun and localization in the
  client.
- **Affected knowledge:** [post-match insights](../system/eventun/post-match-insights-rollout.md)
  and [automatic presentation](../initiatives/post-match-insights/automatic-pre-summary-presentation.md).
- **Evidence:** [archived Insights designs](../archive/initiatives/post-match-insights/README.md).

### AR-2026-005 — Gauntlet stages use durable runs and explicit match acceptance

- **Date:** 2026-05-06
- **Status:** Eventun orchestration and first game-server pass implemented locally; runtime
  validation and listed gaps remain open.
- **Changed:** From implicit stage/session lifecycle assumptions to durable stage-run identity,
  per-match acceptance, and explicit aggregate run completion.
- **Why:** Multi-match stages, recovery, idempotency, participation, and final standings require
  Eventun-owned durable state rather than session presence or admission rows.
- **Affected knowledge:** [gauntlet runtime contract](../system/eventun/gauntlet-stage-runtime-contract.md)
  and [team gauntlet current state](../system/team-gauntlet-current-state.md).
- **Evidence:** [archived orchestration and server plans](../archive/initiatives/gauntlet-runtime/README.md).

### AR-2026-006 — Provider-specific team token gating was removed

- **Date:** 2026-07-13
- **Status:** Implemented in the known local-development state.
- **Changed:** From the TapTools-shaped token catalog, team gate relations, and `token_gated`
  membership mode to no token-gated mode; existing gated teams transition to invite-only.
- **Why:** A provider-specific asset contract should not be embedded in the foundational team
  model. A provider-neutral asset-source design is required before reintroduction.
- **Affected knowledge:** [Eventun API](../system/eventun/api.md),
  [data model](../system/eventun/data-model.md), [game client](../system/game-client.md), and
  [team current state](../system/team-gauntlet-current-state.md).
- **Evidence:** [foundation/API review](../sources/analysis/eventun-foundation-api-simplification-review.md).
