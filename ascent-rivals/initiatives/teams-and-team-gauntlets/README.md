# Teams and Team Gauntlets Initiative

Status: in-progress
Status detail: T00 through T03B and the G01 dedicated-server integration passed their local
implementation and review gates. The coordinated shared-development database cutover completed
successfully, and the Eventun, Ascentun, and game-client changes are deployed in shared development.
The T03C Eventun correction, corrected G03 priority replacement and roster policy, and bounded T03D
Website public-gauntlet detail projection are deployed in shared development through Eventun commit
`0f2a1de`. The ordered post-development database delta was applied there. The compatible Website
consumer and dedicated-server G03 consumer remain separate unfinished work. G04 may now begin.
Combined
player/team/gauntlet runtime smoke and soak remain active; production deployment is not implied or
scheduled.

Last consolidated: 2026-07-23

## Outcome And Boundary

Deliver useful team identity, membership, presentation, and fact-backed views before extending
the same foundation into team qualification, concrete racer slots, runtime roster enforcement,
and brackets. Proposed behavior is not current system state, and production deployment is not
authorized by this initiative.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Existing Eventun and Ascentun team identity/lifecycle baseline | `superseded-dev` | [Current team and gauntlet state](../../system/team-gauntlet-current-state.md) plus linked repository evidence | Replaced by Team Core in the owner-reported shared-development deployment; production retains the old baseline | Validate Team Core under development traffic |
| Eventun match, fact, cutoff, and season data foundation used by future team work | `deployed-dev` | [Foundation delivery snapshot](../eventun-foundation/README.md#delivery-snapshot) | Owner reports successful shared-development migration and deployment | Development soak and combined runtime validation |
| Runtime resource and service-boundary hardening | `deployed-dev` | Eventun commit `9213feb`; [cutover and hardening plan](../eventun-foundation/development-cutover-and-runtime-hardening.md) | Included in the shared-development deployment; runtime reconfirmation remains part of soak | Reconfirm during combined smoke |
| T00 team design refresh and delivery cutoff | `approved` | Approved solution designs and [delivery plan](delivery-plan.md) | Revalidated against the committed local foundation and retained migrated database | Narrow contract/runtime reconfirmation after shared-development cutover |
| Eventun Team Core implementation | `deployed-dev` | Eventun commit `c4260f3`; current-system API and data-model records | Local verification/review accepted and included in the shared-development deployment | Player-authenticated lifecycle and concurrency smoke |
| Ascentun Team Core implementation | `deployed-dev` | Accepted Ascentun Team Core implementation and exact generated Swagger copy | Local verification/review accepted and owner reports Ascentun deployed in shared development; player-authenticated mutation smoke remains outstanding | Combined player-authenticated Team Core smoke |
| G01 Eventun field/slot/roster/result foundation | `deployed-dev` | Eventun commit `6343438`; [delivery checkpoint](delivery-plan.md#g01-implementation-review-checkpoint) | Local verification/review accepted and included in the shared-development Eventun deployment | Combined field/admission/roster/result smoke |
| G01 dedicated-server runtime integration | `deployed-dev` | Accepted Ascent Rivals implementation; [runtime verification checkpoint](delivery-plan.md#g01-dedicated-server-runtime-verification-checkpoint) | Local focused verification passed and owner reports the game client deployed in shared development | Player-connected combined smoke |
| G02 closed-membership-correction pass | `deployed-dev` | Eventun commit `3e1606c`; [Pass 1 checkpoint](delivery-plan.md#g02-pass-1-implementation-review-checkpoint) | Local verification/review accepted and included in the shared-development Eventun deployment | Validate correction and membership serialization under development traffic |
| G02 frozen team qualification pass | `deployed-dev` | Eventun commit `1e3b76e`; [Pass 2 checkpoint](delivery-plan.md#g02-pass-2-implementation-review-checkpoint) | Local verification/review accepted and included in the shared-development Eventun deployment | Exercise cutoff publication, qualified field, and claim flow in development |
| T03A reusable public team and gauntlet reads | `deployed-dev` | Eventun commit `efcedcd`; [T03A checkpoint](delivery-plan.md#t03a-implementation-review-checkpoint) | Local verification/review accepted and included in the shared-development Eventun deployment | Combined consumer smoke |
| T03B fact-backed performance and history reads | `deployed-dev` | Eventun commit `a96d6b4`; [T03B checkpoint](delivery-plan.md#t03b-implementation-review-checkpoint) | Local verification/review accepted and included in the shared-development Eventun deployment | Populated shared-development consumer and latency smoke |
| T03C public gauntlet occurrence-fact correction | `partial-dev` | Eventun commit `0e4d656`; compatible Website correction implemented locally from `ar-web` `481c47b`; [implementation-review checkpoint](delivery-plan.md#t03c-implementation-review-checkpoint) | Eventun correction is deployed in shared development through `0f2a1de`; the compatible Website consumer is not deployed | Review and deploy the Website consumer, then run combined consumer smoke |
| T03D Website public-gauntlet detail projection | `deployed-dev` | Eventun commit `0f2a1de`; [implementation-review checkpoint](delivery-plan.md#t03d-implementation-review-checkpoint) and Website detail contract | Owner reports Eventun deployment and successful application of the ordered post-development delta in shared development; Website fetching and rendering remain unimplemented | Implement the Website consumer separately; G04 may begin from the deployed Eventun baseline |
| G03 priority replacement and roster policy | `deployed-dev` | Eventun commit `cb79df3`; [implementation-review checkpoint](delivery-plan.md#g03-implementation-review-checkpoint) | Eventun behavior and its guarded occupancy constraint are deployed in shared development through `0f2a1de`; the dedicated-server occupancy/replacement consumer is not implemented | Implement and verify the dedicated-server occupancy/replacement consumer |
| Later mixed-owner, bracket, fallback, and administration slices | `approved` | G04-G07 remain defined in the delivery plan | `not-deployed` | Begin G04 from committed Eventun baseline `0f2a1de` |
| Post-teams simplification and technical-debt cleanup | `approved` | [G08 cleanup boundary](delivery-plan.md#g08--post-teams-simplification-and-technical-debt-cleanup) and AR-2026-020 | `not-started` | Begin after the teams delivery slices are complete enough for one cross-layer audit |

## Documents

- [Delivery plan and gates](delivery-plan.md)
- [Teams program design](teams-solution-design.md)
- [Team experience and progression design](team-experience-and-progression-solution-design.md)
- [Team gauntlets and brackets design](team-gauntlets-and-brackets-solution-design.md)

## Related Current System and Evidence

- [Team gauntlet current state](../../system/team-gauntlet-current-state.md)
- [Eventun interface architecture](../../system/eventun/interface-architecture.md)
- [Eventun data model](../../system/eventun/data-model.md)
- [Eventun development cutover and runtime hardening](../eventun-foundation/development-cutover-and-runtime-hardening.md)
- [Foundation and API simplification review](../../sources/analysis/eventun-foundation-api-simplification-review.md)
- [Team PostgreSQL derivation review](../../sources/analysis/eventun-team-postgresql-derivation-review.md)
- [Team Core replacement decision](../../decisions/README.md#ar-2026-014--team-core-replaces-the-pre-alpha-team-model)
- [Team Core sequencing decision](../../decisions/README.md#ar-2026-015--local-team-core-implementation-may-precede-shared-development-cutover)

## Remaining Before Closure

- Complete and record the combined player-authenticated Team Core, G01 roster/runtime, G02
  qualification, and T03 consumer smoke in shared development.
- Soak the coordinated deployment before any production decision.
- Keep production migration and deployment as a separate owner-scheduled gate.
- Deliver the approved team-gauntlet slices after the Team Core deployment unit is proven.
- Run the G08 simplification pass after the team slices, with a measured reduction in redundant
  compatibility and validation code.
- After production deployment, reconcile final environment applicability and archive or supersede
  completed Team Core planning.
