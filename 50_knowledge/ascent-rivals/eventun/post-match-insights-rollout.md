# Post-Match Insights Rollout Notes

Last updated: 2026-06-27

## Implementation Deltas

- Public legacy recommendation RPCs and `RunRecommendation*` models have been removed from the Eventun client API. The public flow uses `GetPostMatchInsights` and `GetTimeTrialInsights`.
- Internal Go and SQL snapshot helpers still use `recommendation_*` names. They are internal insight input loaders retained for migration stability until a dedicated DB/function rename pass.
- Insight policy schema lives in `migration/a0_create_init.sql`. Durable default policy rows live in `migration/d5_insight_policy.sql`. One-time transition SQL for already-deployed environments lives in `migration/temp_migration.sql`.
- Admin tuning is the normal product path for policy changes. Direct DB edits are trusted-operator escape hatches.
- Admin explain includes selected and rejected candidates, score components, policy-disabled candidates, and readiness notes. Player endpoints never return rejected candidates or raw scores.
- Unexpected evaluator failures after a valid run context return `FAILED` with `EVALUATION_FAILED`. Data-loading failures still return transport errors.
- Economy insights compare against the current-match high-CP/top-placement cohort and use `CURRENT_MATCH_HIGH_CP_COHORT` as the benchmark type.

## QA Scenario Matrix

- Post-match Ascent match complete with placement 1: expect `READY` with a primary kudo possible.
- Post-match Ascent match complete with a strong coaching gap and no stronger kudo: expect `READY` with a primary coaching insight.
- Run with multiple qualifying candidates from different suppression groups: expect one primary and at most two secondary insights.
- Complete run with no candidate meeting primary threshold: expect `NO_INSIGHT` and no primary/secondary insights.
- Run where match/heat ingestion is not complete: expect `PENDING` and bounded client retry behavior.
- Unsupported post-match race mode: expect `UNAVAILABLE` with `UNSUPPORTED_MODE`.
- Evaluator panic/unexpected evaluator failure after run context loads: expect `FAILED` with `EVALUATION_FAILED`.
- Disabled policy row for an otherwise qualifying insight: player endpoint must not return it; admin explain should show it as rejected with `policy_disabled`.
- Admin policy page: operator can update known returned policy rows only; no unknown insight IDs or template keys can be created.
- Admin audit page: recent policy changes show previous and next policy JSON.

## Client Contract Checks

- The client enters the insights route through the manual Insights button, not automatic routing.
- The client renders `primary_insight` as primary and up to the first two `secondary_insights` as secondary. It must not promote secondary insights.
- Client timeout or network/API failure is distinct from backend `NO_INSIGHT`.
- Player-facing copy is client-localized from insight IDs/template keys. Eventun returns keys and metrics, not rendered player-facing text.
