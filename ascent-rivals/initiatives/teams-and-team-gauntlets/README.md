# Teams and Team Gauntlets Initiative

Status: proposed
Status detail: Program and solution designs are retained, but T00 reapproval waits for the
coordinated Eventun shared-development cutover and implementation waits for runtime hardening.

Last consolidated: 2026-07-20

## Outcome And Boundary

Deliver useful team identity, membership, presentation, and fact-backed views before extending
the same foundation into team qualification, concrete racer slots, runtime roster enforcement,
and brackets. Proposed behavior is not current system state, and production deployment is not
authorized by this initiative.

## Delivery Snapshot

| Surface | Work state | Source or artifact evidence | Runtime evidence | Next gate |
|---|---|---|---|---|
| Existing Eventun and Ascentun team identity/lifecycle baseline | `implemented` | [Current team and gauntlet state](../../system/team-gauntlet-current-state.md) plus linked repository evidence | Known local-development code state; shared-development and production use are unproven | Revalidate the live repositories during T00 |
| Eventun match, fact, cutoff, and season data foundation used by future team work | `verified` | [Foundation delivery snapshot](../eventun-foundation/README.md#delivery-snapshot) | Verified locally; shared-development deployment remains pending | Coordinated cutover |
| Runtime resource and service-boundary hardening | `approved` | [Cutover and hardening plan](../eventun-foundation/development-cutover-and-runtime-hardening.md) | `not-deployed` | Implement and verify before team implementation |
| T00 team design refresh and delivery cutoff | `not-started` | Current solution designs and [delivery plan](delivery-plan.md) | `not-applicable` | Successful shared-development cutover |
| Team experience implementation | `not-started` | No selected implementation slice | `not-deployed` | T00 approval and completed runtime hardening |
| Team gauntlet and bracket implementation | `not-started` | Existing partial behavior is documented in [current state](../../system/team-gauntlet-current-state.md), not as this initiative's implementation | `not-deployed` | T00 cutoff, team identity foundation, and selected gauntlet gates |

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

## Remaining Before Closure

- Complete the coordinated Eventun shared-development cutover.
- Refresh and reapprove the designs through T00 against the implemented schema and client UI.
- Complete runtime hardening before starting implementation.
- Select and deliver the first team-experience cutoff, then the approved team-gauntlet slices.
- Incorporate accepted behavior into `system/` and archive or supersede completed planning.
