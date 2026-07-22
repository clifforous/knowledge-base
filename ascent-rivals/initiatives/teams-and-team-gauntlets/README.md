# Teams and Team Gauntlets Initiative

Status: in-progress
Status detail: T00 is approved against the committed local Eventun foundation, with Team Core
selected as the first implementation cutoff. The Eventun implementation based on `9213feb` passed
local verification and implementation review and is committed as `c4260f3`. The staged Ascentun
Team Core implementation based on `a0a40ad` passed implementation review but remains uncommitted.
The Eventun G01 field, slot, roster-lock, and result foundation passed implementation review and is
committed as `6343438`. The unsubmitted Ascent Rivals default changelist now contains the G01
dedicated-server integration; it passed a Development Editor build, all five focused roster
automations, the Eventun PostgreSQL smoke, and implementation review. None of the G01 work is
deployed. Coordinated deployment remains gated by source-control completion, the shared-development
cutover, and combined runtime smoke.
Eventun G02 Pass 1 closed-membership correction passed implementation review and is committed as
`3e1606c`. G02 Pass 2 frozen team qualification passed coder verification and implementation review
and is committed as `1e3b76e`; it is not deployed. The T03 reusable public-team and fact-backed
performance-read contract is approved for implementation from that clean source baseline.

Last consolidated: 2026-07-22

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
| Ascentun Team Core implementation | `verified` | Staged, uncommitted Ascentun working tree based on `a0a40ad`; exact generated Swagger copy plus focused contract, authorization, action, cache, and session tests | Type check, lint, production build, focused tests, and implementation review passed locally. A fresh local PostgreSQL/Eventun smoke verified the empty compact list, missing detail, authentication boundaries, Ascentun proxies, and rendered empty directory; player-authenticated mutations remain unexecuted because no player fixture exists | Owner source-control decision, then coordinated shared-development cutover and combined runtime smoke |
| G01 Eventun field/slot/roster/result foundation | `verified` | Eventun commit `6343438`; [delivery checkpoint](delivery-plan.md#g01-implementation-review-checkpoint) | Full repository verification, disposable PostgreSQL schema/runtime suite, and implementation review passed locally; no authentic-data reconstruction or shared-environment deployment was run | Coordinated shared-development cutover and combined runtime smoke |
| G01 dedicated-server runtime integration | `verified` | Unsubmitted Ascent Rivals default changelist; [runtime verification checkpoint](delivery-plan.md#g01-dedicated-server-runtime-verification-checkpoint) | Development Editor build, five focused roster automations, and Eventun PostgreSQL smoke passed locally; no shared-environment deployment or player-connected combined smoke | Owner source-control decision, then coordinated shared-development cutover and combined runtime smoke |
| G02 closed-membership-correction pass | `verified` | Eventun commit `3e1606c`; [Pass 1 checkpoint](delivery-plan.md#g02-pass-1-implementation-review-checkpoint) | Full repository verification, isolated PostgreSQL correction/identity/timestamp/migration/access-plan/race/benchmark suite, and implementation review passed locally; not deployed | Use the committed correction and serialization boundary in Pass 2 |
| G02 frozen team qualification pass | `verified` | Eventun commit `1e3b76e`; [Pass 2 checkpoint](delivery-plan.md#g02-pass-2-implementation-review-checkpoint) | Full repository verification and isolated PostgreSQL migration, individual-rule reuse, full-population and complete contributor-tuple ranking, membership-semantic revisioning, effective field capacity, immutable cutoff/field evidence, sealed-cutoff fact repair and authoring replacement, qualified-field publication/claim, field-history deletion protection, race, access-plan, rebuild suites, and independent implementation review passed locally; not deployed | Coordinated shared-development cutover and combined runtime smoke |
| T03 reusable public team and performance reads | `approved` | [T03 contract checkpoint](delivery-plan.md#t03-public-read-contract-checkpoint); clean Eventun baseline `1e3b76e` | `not-implemented`; no runtime evidence | Eventun pre-edit implementation checkpoint |
| Later roster policy, mixed-owner, and bracket slices | `approved` | G03-G07 remain defined in the delivery plan | `not-deployed` | Complete the selected next implementation slice |

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

- Commit the accepted staged Ascentun Team Core implementation when the owner is ready.
- Submit the reviewed G01 dedicated-server integration when the owner is ready.
- Complete the coordinated Eventun shared-development cutover and combined runtime smoke before
  enabling Team Core in a shared environment.
- Deliver the approved team-gauntlet slices after the Team Core deployment unit is proven.
- After coordinated deployment, reconcile environment applicability and archive or supersede
  completed Team Core planning.
