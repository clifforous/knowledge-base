# Teams and Team Gauntlets Initiative

Status: in-progress
Status detail: T00 is approved against the committed local Eventun foundation, with Team Core
selected as the first implementation cutoff. An uncommitted Eventun implementation artifact based
on `9213feb` exists and has coder-reported isolated verification, but implementation review and the
Ascentun half remain unfinished. Coordinated Eventun and Ascentun deployment remains blocked on
the shared-development cutover and combined runtime smoke.

Last consolidated: 2026-07-20

## Outcome And Boundary

Deliver useful team identity, membership, presentation, and fact-backed views before extending
the same foundation into team qualification, concrete racer slots, runtime roster enforcement,
and brackets. Proposed behavior is not current system state, and production deployment is not
authorized by this initiative.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Existing Eventun and Ascentun team identity/lifecycle baseline | `implemented` | [Current team and gauntlet state](../../system/team-gauntlet-current-state.md) plus linked repository evidence | Revalidated during T00; shared-development and production use are unproven | Replace through accepted Team Core behavior after implementation review and the shared-development gate |
| Eventun match, fact, cutoff, and season data foundation used by future team work | `verified` | [Foundation delivery snapshot](../eventun-foundation/README.md#delivery-snapshot) | Verified locally; shared-development deployment remains pending | Coordinated cutover |
| Runtime resource and service-boundary hardening | `verified` | Eventun commit `9213feb`; [cutover and hardening plan](../eventun-foundation/development-cutover-and-runtime-hardening.md) | Code-verified for local development; not deployed to shared development | Reconfirm during coordinated shared-development smoke |
| T00 team design refresh and delivery cutoff | `approved` | Approved solution designs and [delivery plan](delivery-plan.md) | Revalidated against the committed local foundation and retained migrated database | Narrow contract/runtime reconfirmation after shared-development cutover |
| Team experience implementation | `implementing` | Uncommitted Eventun working tree based on `9213feb`; implementation review pending and Ascentun unchanged | Coder-reported focused schema, migration, transaction, authorization, and query-plan verification in an isolated local environment; not independently accepted and not deployed | Review the Eventun artifact, implement Ascentun, then perform the coordinated shared-development cutover and combined runtime smoke |
| Team gauntlet and bracket implementation | `not-started` | G01 explicit-team runtime vertical selected; existing partial behavior remains documented in [current state](../../system/team-gauntlet-current-state.md) | `not-deployed` | Team Core identity foundation and G01 implementation gate |

## Documents

- [Delivery plan and gates](delivery-plan.md)
- [Teams program design](teams-solution-design.md)
- [Team experience and progression design](team-experience-and-progression-solution-design.md)
- [Team gauntlets and brackets design](team-gauntlets-and-brackets-solution-design.md)

## Related Current System and Evidence

- [Team gauntlet current state](../../system/team-gauntlet-current-state.md)
- [Eventun API](../../system/eventun/api.md)
- [Eventun data model](../../system/eventun/data-model.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
- [Foundation and API simplification review](../../sources/analysis/eventun-foundation-api-simplification-review.md)
- [Team PostgreSQL derivation review](../../sources/analysis/eventun-team-postgresql-derivation-review.md)
- [Team Core replacement decision](../../decisions/README.md#ar-2026-014--team-core-replaces-the-pre-alpha-team-model)
- [Team Core sequencing decision](../../decisions/README.md#ar-2026-015--local-team-core-implementation-may-precede-shared-development-cutover)

## Remaining Before Closure

- Complete the Ascentun half of the breaking Team Core contract.
- Complete the coordinated Eventun shared-development cutover and combined runtime smoke before
  enabling Team Core in a shared environment.
- Deliver the approved team-gauntlet slices after the Team Core deployment unit is proven.
- Incorporate accepted behavior into `system/` and archive or supersede completed planning.
