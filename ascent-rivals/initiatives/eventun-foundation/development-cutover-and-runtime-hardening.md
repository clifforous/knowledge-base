# Eventun Development Cutover And Runtime Hardening

Status: in-progress
Status detail: The production-scale local rehearsal and populated API/performance smoke are
complete. Shared-development cutover is intentionally waiting for the next game-client main
integration; runtime hardening remains required before team implementation or production
release.

Last consolidated: 2026-07-20

## Outcome And Boundary

Move the accepted identified-match, serving-projection, and season foundation into the shared
development environment once the coordinated game-client contract is ready, then close the
remaining runtime resource boundaries before beginning team implementation.

This plan does not authorize a production migration or release. Physical telemetry retention,
archive, and restore policy remain in the separate
[telemetry lifecycle plan](eventun-telemetry-lifecycle-plan.md).

## Current Position

- The identified-ingestion, compact-fact, serving-projection, qualification-cutoff, and season
  implementations are accepted in local-development state.
- One full production-scale local historical-and-season cutover committed successfully. A
  resettable migrated snapshot is retained, and populated API plus representative query-plan
  smoke passed.
- No shared development or production database was changed by that rehearsal.
- Applying the accepted transition to shared development, removing the legacy runtime paths,
  and validating the coordinated service/game-client behavior remain unfinished.
- The one-time conversion machinery remains temporary but must stay available until the
  production cutover succeeds.

## Owner Sequencing Decision

Do not migrate the shared development Eventun database or release the coordinated Eventun
service contract until the pending game-client API changes have completed their next copy to
main. This avoids creating a shared-development service/client mismatch and gives the combined
foundation time to run in development before any production decision.

When that condition is met, update the generated contracts and apply the Eventun service and
database transition as one coordinated development change. Production remains unscheduled and
may follow only after a deliberate soak period and an owner-selected release window.

## Shared-Development Cutover

This is the durable remainder formerly tracked as F15B.

### Preconditions

- Confirm the game-client mainline contains the accepted identified-match and artifact producer
  contract needed by the replacement Eventun service.
- Select the reviewed Eventun revision and verify that its pending delta and temporary backfill
  machinery match the accepted rehearsal assumptions.
- Take a current development backup and record the target identity required by Eventun's guarded
  database command.
- Stop the single Eventun Extend instance and every Eventun worker or scheduler for the complete
  maintenance window. Online compatibility and concurrent ingestion are not requirements.
- Recheck the available database capacity against the recorded 32 GiB ceiling if the development
  data size or migration changed materially since rehearsal.

### Execution And Acceptance

- The owner runs the reviewed manual offline transition using Eventun's
  [Historical Cutover Runbook](https://github.com/ikigai-github/eventun/blob/main/docs/historical-cutover-runbook.md).
  The implementation repository owns exact commands, rollback checkpoints, smoke steps, and
  post-production transition cleanup. Do not create a general migration service or online
  cutover protocol.
- Require complete source accounting, nonzero fact and serving output, explained reconciliation,
  and successful destructive-suffix completion before commit.
- Validate replacement relation counts, source coverage, converted batches, facts, serving
  projections, season integrity, and the compact accepted-execution marker.
- Smoke the coordinated game client and service paths for client and dedicated-server match
  ingestion, artifact association, Match History, records, career views, lifetime and seasonal
  leaderboards, progression, gauntlet reads, cutoff-bound admission, and administrative season
  operations.
- Capture representative query plans for Match History, leaderboards, and gauntlet reads and
  compare them with the accepted local evidence. Live totals need not equal an older dump.

### Post-Cutover Cleanup

- Remove remaining runtime consumers of the legacy `client_event` and `server_event` model only
  after shared-development validation succeeds.
- Refresh Eventun, Ascentun, and game-client generated contracts together, including removal of
  dormant Ascentun token-gating contract artifacts. Do not restore token-gating behavior.
- Keep production rollback instructions reviewable and keep the one-time conversion machinery
  until production cutover has succeeded.
- Record shared-development evidence before declaring this gate complete.

## Runtime Resource And Service-Boundary Hardening

This is the durable remainder formerly tracked as H01. It may proceed while the team design
checkpoint runs, but it must complete before team implementation or any production release.

- Replace whole-RPC database connection ownership with query- or transaction-scoped acquisition.
  Database-free endpoints must not acquire a connection, and external service latency must not
  retain one.
- Revalidate manual and automatic reward fulfillment as short prepare and finalize transactions
  with no pool connection held during the external grant call.
- Configure explicit PostgreSQL pool limits, acquisition behavior, and pool telemetry from
  measured concurrency rather than an arbitrary large default.
- Add header, read, write, and idle bounds to gateway and metrics HTTP servers.
- Give progression and reward schedules an explicit singleton/reschedule or bounded-concurrency
  policy. Preserve progression lease/token fencing and replace any ineffective autocommit reward
  preselection lock with a durable short claim or remove it.
- Replace the mutable process-global AccelByte namespace with constructor-injected immutable
  configuration.
- Introduce typed domain errors and stable transport mapping incrementally as affected packages
  are touched. Distinguish absence, conflicts, authorization denial, and infrastructure failure
  without exposing raw database errors.
- Keep this work behavior-focused. Relocate packages only when establishing one of these
  boundaries requires it.

Completion requires evidence that external latency cannot pin database capacity, scheduled work
has a measured concurrency budget, HTTP resources are bounded, configuration is immutable after
construction, and client-visible failures are stable.

## Production Release Boundary

The production cutover formerly tracked as F15P is deferred and unscheduled. Shared-development
completion does not authorize it.

- Select an explicit release window after the coordinated changes have soaked in development.
- Refresh the authentic rehearsal only if schema, data scale, migration contents, or the accepted
  maintenance/storage budget changed materially.
- Execute the reviewed manual migration, service release, rollback checkpoints, and smoke matrix
  against the quiesced production environment using Eventun's
  [Historical Cutover Runbook](https://github.com/ikigai-github/eventun/blob/main/docs/historical-cutover-runbook.md).
- Remove the consumed production delta, historical conversion command/package, transition-only
  verification artifacts, and resolved quarantine state only after successful production use.

## Dependencies

- The teams T00 design checkpoint starts after the shared-development cutover succeeds.
- Runtime hardening may overlap T00 but must finish before T01/T02 or any other team
  implementation begins.
- Physical retention and archive choices are not prerequisites for teams.
- Production release requires shared-development acceptance, runtime hardening, and an explicit
  owner-selected window.

## Evidence And Related Knowledge

- [Identified Match Ingestion](../../system/eventun/identified-match-ingestion.md)
- [Eventun API](../../system/eventun/api.md)
- [Eventun data model](../../system/eventun/data-model.md)
- [Insights, progression, and seasons review](../../sources/analysis/eventun-insights-progression-seasons-review.md)
- [Teams delivery plan](../teams-and-team-gauntlets/delivery-plan.md)
- [Ascent Rivals decision log](../../decisions/README.md#ar-2026-007--coordinate-development-cutover-with-the-game-client-mainline)
