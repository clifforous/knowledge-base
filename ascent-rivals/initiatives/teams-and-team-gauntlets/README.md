# Teams and Team Gauntlets Initiative

Status: in-progress
Status detail: T00 is approved against the committed local Eventun foundation, with Team Core
selected as the first implementation cutoff. The Eventun implementation based on `9213feb` passed
local verification and implementation review and is committed as `c4260f3`. The Ascentun working
tree implementation based on `a0a40ad` is coder-verified and awaiting implementation review.
Coordinated Eventun and Ascentun deployment remains blocked on that review, the
shared-development cutover, and combined runtime smoke. The local G01 explicit-team runtime
pre-edit checkpoint is now active; this does not establish G01 implementation or runtime evidence.

Last consolidated: 2026-07-21

## Outcome And Boundary

Deliver useful team identity, membership, presentation, and fact-backed views before extending
the same foundation into team qualification, concrete racer slots, runtime roster enforcement,
and brackets. Proposed behavior is not current system state, and production deployment is not
authorized by this initiative.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Existing Eventun and Ascentun team identity/lifecycle baseline | `implemented` | [Current team and gauntlet state](../../system/team-gauntlet-current-state.md) plus linked repository evidence | Revalidated during T00; shared-development and production use are unproven | Replace through accepted Team Core behavior at the coordinated shared-development gate |
| Eventun match, fact, cutoff, and season data foundation used by future team work | `verified` | [Foundation delivery snapshot](../eventun-foundation/README.md#delivery-snapshot) | Verified locally; shared-development deployment remains pending | Coordinated cutover |
| Runtime resource and service-boundary hardening | `verified` | Eventun commit `9213feb`; [cutover and hardening plan](../eventun-foundation/development-cutover-and-runtime-hardening.md) | Code-verified for local development; not deployed to shared development | Reconfirm during coordinated shared-development smoke |
| T00 team design refresh and delivery cutoff | `approved` | Approved solution designs and [delivery plan](delivery-plan.md) | Revalidated against the committed local foundation and retained migrated database | Narrow contract/runtime reconfirmation after shared-development cutover |
| Eventun Team Core implementation | `verified` | Eventun commit `c4260f3`; current-system API and data-model records | Coder-reported repository, schema, Unreal-contract, race, and PostgreSQL smoke verification; independent implementation review accepted; not deployed | Focused authentic-baseline runner rehearsal before deployment, then coordinated shared-development cutover |
| Ascentun Team Core implementation | `verified` | Uncommitted Ascentun working tree based on `a0a40ad`; exact generated Swagger copy plus focused contract, authorization, action, cache, and session tests | Type check, lint, production build, and focused tests passed locally. A fresh local PostgreSQL/Eventun smoke verified the empty compact list, missing detail, authentication boundaries, Ascentun proxies, and rendered empty directory; player-authenticated mutations remain unexecuted because no player fixture exists | Implementation review, then coordinated shared-development cutover and combined runtime smoke |
| G01 explicit-team runtime vertical | `designing` | Approved G01 boundary and 2026-07-21 local pre-edit checkpoint; existing partial behavior remains documented in [current state](../../system/team-gauntlet-current-state.md) | No G01 runtime evidence; `not-deployed` | Accept the exact schema, API, locking, migration, and verification checkpoint before implementation |
| Later team qualification, roster policy, mixed-owner, and bracket slices | `not-started` | G02-G07 remain defined in the delivery plan | `not-deployed` | Verified G01 owner-to-slot-to-result path and each slice's named design gate |

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

- Accept the coder-verified Ascentun Team Core implementation through implementation review.
- Complete the coordinated Eventun shared-development cutover and combined runtime smoke before
  enabling Team Core in a shared environment.
- Deliver the approved team-gauntlet slices after the Team Core deployment unit is proven.
- After coordinated deployment, reconcile environment applicability and archive or supersede
  completed Team Core planning.
