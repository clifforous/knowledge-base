# Eventun Foundation Initiative

Status: in-progress
Status detail: Local implementation, rehearsal, and populated smoke are complete. The coordinated
shared-development database cutover completed successfully, and the Eventun, Ascentun, and game
client changes are deployed in shared development. Development soak and combined runtime validation
remain active. Physical lifecycle decisions remain open and production release is unscheduled.

Last consolidated: 2026-07-23

## Outcome And Boundary

Finish the coordinated Eventun foundation transition without treating successful development
deployment as production acceptance. This initiative owns three active remainders:

- shared-development soak and combined runtime validation;
- the separately scheduled production cutover and post-release transition cleanup; and
- physical retention, archive, restore, and long-term client-confidence policy.

Current ingest and season behavior is authoritative under `system/`. Production migration is a
separate owner-scheduled action and is not implied by this initiative's local evidence.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Eventun identified-match, fact, projection, cutoff, and season foundation | `deployed-dev` | Accepted Eventun implementation and linked rehearsal evidence | Production-scale local rehearsal and populated smoke passed; owner reports successful shared-development migration and deployment | Development soak and combined runtime validation |
| Game-client producer contract required by the cutover | `deployed-dev` | Accepted Perforce implementation; submitted changelist identity is not recorded in this knowledge base | Owner reports the coordinated game client is deployed in shared development | Exercise identified ingestion and artifact association during development soak |
| Shared-development Eventun cutover | `deployed-dev` | [Cutover and hardening plan](development-cutover-and-runtime-hardening.md); exact pre-cutover-dump schema transition and complete schema verification passed after rollback corrections | Owner reports the guarded database migration completed successfully and Eventun, Ascentun, and the game client are deployed | Record combined smoke/soak outcomes and any production-delta corrections |
| Runtime resource and service-boundary hardening | `deployed-dev` | Eventun commit `9213feb`; [cutover and hardening plan](development-cutover-and-runtime-hardening.md) | Included in the owner-reported shared-development deployment; focused runtime reconfirmation remains part of soak | Reconfirm under normal development traffic |
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

- Complete and record shared-development API, ingestion, team, gauntlet, and runtime smoke/soak.
- Keep the accepted historical production delta frozen. Put any later database changes in the
  separately ordered post-development delta so production can apply both baselines in sequence.
- Leave production release pending until the owner selects a window and accepts any required
  rehearsal refresh.
- After successful production migration and observation, remove the consumed historical conversion
  machinery and return to the normal single-delta workflow.
- Separately decide retention tiers, storage segmentation, archive format, and restore proof
  before any destructive telemetry lifecycle change.
