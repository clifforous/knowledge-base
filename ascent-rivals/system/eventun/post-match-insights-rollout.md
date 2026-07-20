# Post-Match Insights Rollout Notes

Status: current
Status detail: Automatic pre-summary presentation remains an approved client follow-on.

Applicability: local-development

Scope: Eventun and the Ascent Rivals game client. This document does not imply production
deployment.

Last consolidated: 2026-07-19

## Current Product Contract

- **Insights** is the product and public API term. The public recommendation RPCs and
  `RunRecommendation*` models have been removed.
- Eventun selects a primary insight and up to two secondary insights. It may return coaching,
  a kudo, or an explicit non-ready/no-insight state; the client does not promote a secondary
  result into the primary slot.
- Eventun owns candidate generation, comparator selection, confidence gates, salience,
  suppression, policy, and readiness status. The client owns localized copy, units, layout,
  timing, and navigation.
- Player APIs return only selected insight slots and their presentation inputs. Admin explain
  may expose rejected candidates, score components, policy state, and readiness diagnostics.
- The current submitted client enters Insights manually from the match summary. The active
  follow-on is [automatic pre-summary presentation](../../initiatives/post-match-insights/automatic-pre-summary-presentation.md).

## Analysis States

- `READY`: a valid primary insight exists; up to two secondary slots may also exist.
- `PENDING`: required ingestion or analysis may still complete; the client uses a bounded
  retry window.
- `NO_INSIGHT`: analysis completed but no credible candidate cleared the low salience floor.
- `UNAVAILABLE`: the run or mode is outside the supported analysis contract.
- `FAILED`: evaluation failed after a valid run context was available.

Client timeout and transport failure are client outcomes, not aliases for backend
`NO_INSIGHT`.

## Data And Ownership

- Eventun derives insights from current match, heat, lap, checkpoint, loadout, course, and
  historical comparator data.
- Narrow facts provide terminal and selection context during the identified-telemetry
  cutover. Detailed lap and checkpoint inputs remain bounded reads from their source/event
  partitions rather than duplicated one-for-one into compact facts.
- Time-trial classification uses explicit single-player mode. It must not be inferred from
  Classic race mode.
- AccelByte `Courses` game-record data is authoritative course context. Eventun maintains a
  transactional cache and marks absent courses inactive instead of deleting referenced
  history.
- Speed, Agility, and Combat are current presentation scores, not versioned physical
  capability metrics.

## Implementation Deltas

- Public legacy recommendation RPCs and `RunRecommendation*` models have been removed from the Eventun client API. The public flow uses `GetPostMatchInsights` and `GetTimeTrialInsights`.
- Internal Go and SQL snapshot helpers still use `recommendation_*` names. They are internal insight input loaders retained for migration stability until a dedicated DB/function rename pass.
- Insight policy schema lives in `migration/a0_create_init.sql`. Durable default policy rows live in `migration/d2_insight_policy.sql`. The former frozen delta was deployed and removed on 2026-07-13; pending one-time production transitions use `migration/migration.sql` against the current deployed baseline.
- Admin tuning is the normal product path for policy changes. Direct DB edits are trusted-operator escape hatches.
- Admin explain includes selected and rejected candidates, score components, policy-disabled candidates, and readiness notes. Player endpoints never return rejected candidates or raw scores.
- Unexpected evaluator failures after a valid run context return `FAILED` with `EVALUATION_FAILED`. Data-loading failures still return transport errors.
- Economy insights compare against the current-match high-CP/top-placement cohort and use `CURRENT_MATCH_HIGH_CP_COHORT` as the benchmark type.
- Confidence and salience are separate decisions. Confidence gates decide whether a candidate is credible; priority/salience ranks credible candidates and applies only a low floor to avoid junk filler.
- AccelByte `Courses` game-record data is authoritative course context. Eventun mirrors it as a transactional cache, upserts current rows, and marks absent courses inactive rather than deleting rows that may be referenced by historical data.
- Speed, Agility, Combat, and efficient-low-loadout insight IDs are implemented and seeded disabled/conservatively until explain output and runtime data justify enabling them.

## QA Scenario Matrix

- Post-match Ascent match complete with placement 1: expect `READY` with a primary kudo possible.
- Post-match Ascent match complete with a strong coaching gap and no stronger kudo: expect `READY` with a primary coaching insight.
- Run with multiple qualifying candidates from different suppression groups: expect one primary and at most two secondary insights.
- Complete run with no eligible candidate clearing credibility gates or the low salience floor: expect `NO_INSIGHT` and no primary/secondary insights.
- Complete time-trial run with a credible medium-confidence pace gap above the salience floor but below the old high primary threshold: expect `READY` with a primary insight, not `NO_INSIGHT`.
- Run where match/heat ingestion is not complete: expect `PENDING` and bounded client retry behavior.
- Unsupported post-match race mode: expect `UNAVAILABLE` with `UNSUPPORTED_MODE`.
- Evaluator panic/unexpected evaluator failure after run context loads: expect `FAILED` with `EVALUATION_FAILED`.
- Disabled policy row for an otherwise qualifying insight: player endpoint must not return it; admin explain should show it as rejected with `policy_disabled`.
- Admin policy page: operator can update known returned policy rows only; no unknown insight IDs or template keys can be created.
- Admin policy page: operator can filter policies by `Coaching` versus `Kudo`, see type
  without relying on raw insight enum IDs, and sort by current base weight descending.
- Admin audit page: recent policy changes show previous and next policy JSON.
- Admin explain should distinguish insufficient confidence/sample gates, below-salience-floor rejection, and suppression/diversity rejection. Candidate rows should support type filtering and show `Coaching`/`Kudo` as the prominent type label while keeping raw insight IDs secondary/debug-only.

## Client Contract Checks

- The currently submitted client enters the insights route through the manual Insights button.
- The approved next client change moves Insights before the normal match summary. It prefetches after accepted submission, shows ready insight content, and advances directly to summary for every non-ready outcome.
- Dedicated-server flow inserts Insights after player results; standalone/time-trial flow may enter the same decision directly after the finish delay. Non-final heat summaries are unchanged.
- The client renders `primary_insight` as primary and up to the first two `secondary_insights` as secondary. It must not promote secondary insights.
- Client timeout or network/API failure is distinct from backend `NO_INSIGHT`.
- Player-facing copy is client-localized from insight IDs/template keys. Eventun returns keys and metrics, not rendered player-facing text.

## Evidence And History

- [Archived solution design](../../archive/initiatives/post-match-insights/eventun-post-match-insights-solution-design.md)
- [Archived implementation plan](../../archive/initiatives/post-match-insights/eventun-post-match-insights-implementation-plan.md)
- [Current identified ingestion](identified-match-ingestion.md)
