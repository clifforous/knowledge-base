# Eventun Foundation Initiative

Status: in-progress
Status detail: Local implementation, rehearsal, and populated smoke are complete. The
runtime resource and service-boundary hardening is committed and verified for local development.
The coordinated shared-development cutover and physical lifecycle decisions remain open;
production release is unscheduled.

Last consolidated: 2026-07-20

## Outcome And Boundary

Finish the coordinated Eventun foundation transition without treating local implementation or
rehearsal as shared-environment deployment. This initiative owns two active remainders:

- the coordinated shared-development cutover and validation; and
- physical retention, archive, restore, and long-term client-confidence policy.

Current ingest and season behavior is authoritative under `system/`. Production migration is a
separate owner-scheduled action and is not implied by this initiative's local evidence.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Eventun identified-match, fact, projection, cutoff, and season foundation | `verified` | Accepted Eventun implementation and linked rehearsal evidence | Production-scale local rehearsal and populated smoke passed; not deployed to shared development | Coordinated shared-development cutover |
| Game-client producer contract required by the cutover | `implemented` | Perforce shelf; changelist identity is not recorded in this knowledge base | Not in the shared-development mainline and not deployed | Copy accepted changes to main and refresh generated contracts |
| Shared-development Eventun cutover | `approved` | [Cutover and hardening plan](development-cutover-and-runtime-hardening.md) | `not-deployed` | Game-client mainline precondition, backup, coordinated migration, and smoke |
| Runtime resource and service-boundary hardening | `verified` | Eventun commit `9213feb`; [cutover and hardening plan](development-cutover-and-runtime-hardening.md) | Code-verified for local development; not deployed to shared development | Reconfirm during coordinated shared-development smoke |
| Production foundation release | `not-started` | No release revision or window selected | `not-deployed` | Shared-development soak and explicit owner-selected window |

## Documents

- [Development cutover and runtime hardening](development-cutover-and-runtime-hardening.md)
- [Telemetry lifecycle plan](eventun-telemetry-lifecycle-plan.md)
- [Eventun historical cutover runbook](https://github.com/ikigai-github/eventun/blob/main/docs/historical-cutover-runbook.md)
  — implementation-owned shared-development and production procedure

## Related Sources

- [Foundation and API simplification review](../../sources/analysis/eventun-foundation-api-simplification-review.md)
- [Team PostgreSQL derivation review](../../sources/analysis/eventun-team-postgresql-derivation-review.md)
- [Insights, progression, and seasons review](../../sources/analysis/eventun-insights-progression-seasons-review.md)

## Authoritative Current System

- [Identified match ingestion](../../system/eventun/identified-match-ingestion.md)
- [Eventun API](../../system/eventun/api.md)
- [Eventun data model](../../system/eventun/data-model.md)
- [Eventun progression](../../system/eventun/progression.md)
- [Gauntlet stage runtime contract](../../system/eventun/gauntlet-stage-runtime-contract.md)

## Remaining Before Closure

- Wait for the accepted game-client API changes to complete their next copy to main.
- Apply and validate the coordinated Eventun database/service transition in shared development.
- After a development soak period, leave production release pending until the owner selects a
  window and accepts any required rehearsal refresh.
- Separately decide retention tiers, storage segmentation, archive format, and restore proof
  before any destructive telemetry lifecycle change.
