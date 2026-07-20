# Automatic Pre-Summary Insights Presentation

Status: approved
Status detail: Game-client follow-on; not yet implemented.

Applicability: local-development

Scope: Ascent Rivals game client

Last consolidated: 2026-07-19

## Outcome

For a completed final match, show Insights before the normal match summary only when a valid
`READY` response is available within the bounded wait policy. Every non-ready result advances
directly to the normal summary. Non-final heat summaries keep their current behavior.

## Required Behavior

- Route all final-match transitions through one Insights-or-summary controller entry point.
- Preserve the exact accepted submission `session_id` and `match_id`; do not reconstruct the
  completed match identity from session state that may already have advanced.
- Prefetch after Eventun accepts the submitted match so analysis can overlap the montage and
  player-results screen.
- Reuse the existing bounded request/retry state. Do not create a second independent retry
  machine in the player controller.
- Render only a valid `READY` result with a primary insight.
- Send `NO_INSIGHT`, `UNAVAILABLE`, `FAILED`, timeout, transport failure, rejected or absent
  submission, missing context, and malformed ready responses directly to match summary.
- Continue and Back have the same meaning in automatic Insights: remove the Insights route
  and open the normal summary without leaving Insights underneath it.
- Preserve the existing player-results route beneath summary when the old flow allowed Back.
- Remove the manual match-summary Insights button and its manual-only state after automatic
  entry is validated. Backward compatibility for that entry point is not required.

## Validation Evidence Required From The Implementer

- Dedicated-server ready and no-insight flows.
- Standalone/time-trial ready, no-insight, and timeout flows.
- Rejected or absent submission and backend transport-failure flows.
- Non-final heat behavior.
- Repeated Continue/Back input without duplicate routes.
- Existing summary Back behavior where player results remain on the stack.

The implementing coder owns compilation and runtime validation. Record final behavior in the
[current rollout document](../../system/eventun/post-match-insights-rollout.md) before closing
this follow-on.

## Historical Detail

The original task breakdown is retained in the
[archived implementation plan](../../archive/initiatives/post-match-insights/eventun-post-match-insights-implementation-plan.md#phase-8-automatic-pre-summary-presentation).
