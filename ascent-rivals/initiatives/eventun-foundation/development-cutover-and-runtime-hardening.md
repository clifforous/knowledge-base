# Eventun Development Cutover And Runtime Hardening

Status: in-progress
Status detail: The production-scale local rehearsal and populated API/performance smoke are
complete. Shared-development cutover is intentionally waiting for the next game-client main
integration. The schema-neutral runtime-hardening correction is committed at Eventun `9213feb`
and verified for local development. The coordinated shared-development cutover remains the
unfinished deployment gate before enabling Team Core in a shared environment or releasing to
production; T00 reapproval and isolated Team Core implementation work may proceed locally.

Last consolidated: 2026-07-20

## Outcome And Boundary

Move the accepted identified-match, serving-projection, season, and runtime-hardening foundation
into the shared development environment once the coordinated game-client contract is ready, then
validate the combined runtime before enabling Team Core there.

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
- The schema-neutral runtime-hardening correction is committed in Eventun at `9213feb`, including
  the follow-up review corrections. The complete ordinary verification gate,
  full Go tests, focused race tests, vet, generated-contract checks, and the linux/amd64 service
  build pass without a database rehearsal or shared-environment access.
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

This is the completed schema-neutral correction formerly tracked as H01. It remains deliberately
sized for one Eventun Extend instance and did not add repositories, distributed scheduler
ownership, durable delivery infrastructure, or broad package movement.

### Current-State Incorporation

Accepted runtime behavior is incorporated into the current-system documents rather than retained
as an initiative-only contract:

- database, dependency, HTTP, scheduling, configuration, shutdown, and typed-error boundaries are
  in [Eventun API](../../system/eventun/api.md#runtime-resource-and-failure-boundaries);
- publication and reward prepare/external/finalize behavior is in
  [Eventun progression](../../system/eventun/progression.md);
- ambiguous AccelByte session creation and same-identity reconciliation are in the
  [gauntlet stage runtime contract](../../system/eventun/gauntlet-stage-runtime-contract.md); and
- bounded best-effort post-ingest dispatch is in
  [identified match ingestion](../../system/eventun/identified-match-ingestion.md).

The verification evidence below remains initiative evidence and does not imply deployment.

### Local Verification

- Focused deterministic tests cover capacity-one connection release, reward cancellation and
  finalization states, shutdown admission and pool-close ordering, concurrent automatic grants,
  ambiguous gauntlet create/reconcile without a duplicate create, persisted same-identity reclaim
  after the allocation lease, production AccelByte response mapping, publication lock release and
  stale-snapshot rejection, singleton schedules, request deadlines, pool behavior and metrics,
  immutable namespace instances, team/gauntlet query failure mapping, enforced asynchronous
  post-ingest composition, and bounded post-ingest shutdown.
- `go test -count=1 ./...`, relevant `go test -race` packages, `go vet ./...`, generation and
  source-contract checks, Unreal specification composition, shell syntax, formatting, module
  stability, and the CGO-disabled linux/amd64 build passed locally.
- The guarded-database documentation contract now reads the durable Historical Cutover Runbook
  and checks stable structure rather than exact prose: repository links, quiescence/confirmation/
  apply headings, the guarded production-delta command, and its target-bound confirmation token.
  The obsolete disposable-baseline confirmation remains forbidden. The full `./scripts/verify.sh`
  gate passes. No schema verification or database rehearsal was run because this correction did
  not change SQL.

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

- The teams T00 design checkpoint is approved against the committed local foundation and retained
  migrated database. Reconfirm its implementation assumptions after the shared-development
  cutover rather than repeating the design checkpoint.
- Local T01/T02 implementation and isolated verification may proceed against the committed
  foundation. Enabling the combined implementation in shared development remains gated by the
  successful cutover and runtime smoke.
- Physical retention and archive choices are not prerequisites for teams.
- Production release requires shared-development acceptance and an explicit owner-selected
  window.

## Evidence And Related Knowledge

- [Identified Match Ingestion](../../system/eventun/identified-match-ingestion.md)
- [Eventun API](../../system/eventun/api.md)
- [Eventun data model](../../system/eventun/data-model.md)
- [Insights, progression, and seasons review](../../sources/analysis/eventun-insights-progression-seasons-review.md)
- [Teams delivery plan](../teams-and-team-gauntlets/delivery-plan.md)
- [Ascent Rivals decision log](../../decisions/README.md#ar-2026-007--coordinate-development-cutover-with-the-game-client-mainline)
- [Team Core sequencing decision](../../decisions/README.md#ar-2026-015--local-team-core-implementation-may-precede-shared-development-cutover)
