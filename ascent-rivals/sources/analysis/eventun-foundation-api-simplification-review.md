# Eventun Foundation And API Surface Simplification Review

Status: Architecture recommendation revised for task planning
Date: 2026-07-10
Last updated: 2026-07-13
Reviewed repository: [Eventun](https://github.com/ikigai-github/eventun) at `34b42861f2a698be50b0d7de134881544d072658`

## Related

- [[eventun-team-postgresql-derivation-review]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/teams-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design]]
- [[ascent-rivals/system/eventun/interface-architecture|eventun-interface-architecture]]
- [[ascent-rivals/system/eventun/data-model|eventun-data-model]]
- [[ascent-rivals/decisions/README|Ascent Rivals decision log]]

## Purpose

Reassess Eventun as if its current event ingestion, progression, insights, gauntlets, teams, and optional blockchain integrations were being designed together today. Determine which foundation changes should precede the teams iteration, with a bias toward correctness, fewer concepts, fewer dependencies, and simpler request paths.

This is an architecture decision and research document, not the execution checklist. It distinguishes:

- confirmed defects;
- accepted operating policies;
- cleanup that should reduce code or cognitive load;
- optional defense in depth;
- architecture that would add more machinery than value;
- changes that are justified only because Eventun's product scope has grown beyond its original telemetry template.

## Production Baseline Supersession

On 2026-07-13 the owner deployed and removed the former `t0_migration.sql`. The former `t1_migration.sql` became stable `migration/migration.sql`, the sole current pending one-time delta against the deployed production baseline. Development fixtures now use the independent `t0_seed_courses.sql` through `t3_seed_teams.sql` sequence. Canonical `d3_schedule_refresh_views.sql` safely no-ops without pg_cron and is reapplied by guarded operational setup after provisioning. Current disposable-delta verification uses `production-delta --confirm-disposable-production-baseline=<target-fingerprint>`. References below to the former `t0_migration.sql`, `t1_migration.sql`, or `t2`-`t5` fixture names are retained only as dated review and implementation-history evidence; they are not current instructions.

## Accepted Operating Context

- Eventun is deployed as an AccelByte Extend Service Extension in AccelByte Shared Cloud.
- One backend maintainer manually builds, uploads, and deploys infrequent releases. CI and automated deployment are not current requirements.
- Match submission remains at most once from the producer, while the implemented replacement acceptance contract is idempotent so bounded retry can be enabled separately without another schema change.
- A submitted match batch receives a stable client-generated batch id. Every event receives a stable client-generated event id and producer sequence.
- Match telemetry payloads do not carry independent schema-version fields. Historical payloads and facts are rewritten when their shape changes materially.
- The gameplay client working tree submits a complete match batch and uses the dedicated match-artifact operation; the authored `ReplaySaved` telemetry event has been removed.
- PostgreSQL 16.14 on a one-core Azure B1ms-class deployment is the current performance baseline.
- The `a*` through `d*` SQL files are the canonical clean-slate schema. Stable `migration/migration.sql` is the current pending one-time delta against the deployed production baseline; development fixtures have a separate `t0`-`t3` sequence.
- Pre-alpha compatibility is not required by default. Obsolete code and disposable state should be removed instead of preserved behind compatibility branches.
- The complete merged Swagger v2 document must continue to be generated and served for the Extend app.
- The merged Swagger remains the input to the Extend App UI and the complete administrative contract. Its current use for Unreal GameServer and Models generation is a transitional defect, not a target constraint.
- The Unreal project is one source tree shared by player-client and dedicated-server targets. The generated boundary is nevertheless consumer-specific: Client wrappers come from ClientService, GameServer is a reviewed selection of the ten Client reads and five Server operations used by the dedicated server, and shared Models use the full Client+Server union.
- Eventun uses coarse custom permissions for dedicated-server and administrative callers. Player calls do not need a blanket Client permission; the Server resource also authorizes subjectless access to the exact shared Client reads.
- Local insecure operation is no longer required. Every runtime request path must install authentication and authorization interceptors.
- Accountun and Cardanoun are optional proof-of-concept integrations, not core game dependencies. Disabled integrations must not construct clients, start jobs, or appear in core domain constructors.
- Breaking API, package, and schema changes are acceptable during this pre-alpha reset. Compatibility branches and dead schema should be deleted after the coordinated cutover.
- A recommendation should either fix a demonstrated defect, remove meaningful duplication, or make a frequently modified path materially easier to follow.

## Revisions To The Initial Review

| Earlier conclusion | Revised conclusion | Reason |
|---|---|---|
| `pgx.Batch` commands can partially commit without an explicit transaction | Incorrect. `pgx/v5` `SendBatch` is implicitly transactional unless explicit transaction-control statements are queued | Eventun pins pgx v5.7.6, whose documented and implemented contract is explicit on this point |
| Every multi-statement command needs `DBTX`, `InTx`, and an explicit transaction | Check `BatchResults.Close()` for pure batched writes; use a real transaction only for read-decide-write or locking workflows | This fixes the actual error path without adding a store framework |
| Keep the current broad service/admin trust policy | Require authenticated player tokens for Client, and replace borrowed administrator-role checks with coarse Server and Admin Eventun permissions | Shared Cloud supports custom Extend permissions, but a Client permission granted to every player adds no authorization distinction; Server and Admin grants still separate trusted principals |
| Add an ordered migration runner and durable migration ledger | Keep the canonical clean slate plus one deliberate production diff; make their execution paths unambiguous and manually verifiable | The maintainer has deliberately rejected deployment-coupled migration runners |
| Add CI generation and migration checks | Provide one documented local verification/release command and a short manual deployment checklist | The project has one deployer and infrequent manual releases |
| Keep the 154-file `internal/eventun` package and root bootstrap | Move the executable to `cmd/eventun`, remove `internal/`, and extract domain packages incrementally as each subsystem is changed | The current package contains about 45,000 lines across unrelated domains; package boundaries now remove real coupling and make optional integrations detachable |
| Keep at-most-once rows without stable identity | Add a stable match-batch id, event id, and producer sequence now; retain retry as a separate sender behavior | Progression, insights, gauntlets, and future final-stage reliability all need reproducible source identity and idempotent derivation |
| Preserve separate `server_event` and `client_event` logical models | Use one source-tagged logical `game_event` parent while retaining client/server and event-type physical partition pruning initially | The current logical duplication is costly, but the existing leaf partitions and targeted indexes have demonstrated query-performance value |
| Leave the merged Swagger as the Unreal GameServer and Models input until team-gauntlet work | Separate Unreal consumers during foundation work immediately after coarse permissions; move the true dedicated-server runtime RPCs together, select existing Client reads without duplicating them, and construct Models only from Client/Server definitions | Admin operations and Admin-only models are not game-runtime contracts, and authorization differences do not justify duplicate network APIs |
| Copy every lap and checkpoint into a universal typed fact layer | Keep narrow match, heat, player-result, and progression contribution facts; aggregate lap totals and records at heat/player scope; retain detailed checkpoint and experimental telemetry in source/event-type partitions | One-to-one wide lap/checkpoint copies add synchronous write, WAL, index, and storage cost without bounding career, leaderboard, gauntlet, or match-local insight reads |
| Retain multiple complete fact revisions online | Keep one current fact set per accepted batch and rewrite it transactionally; retain only batch-level operational derivation metadata needed for repair | The original global revision integer was not bound to immutable projector semantics and could duplicate downstream contributions |
| Treat rebuildable projections as an optional last resort and retain hourly materialized views for delayed presentation | Use incrementally maintained serving projections for fresh unbounded reads such as records, career summaries, and gauntlet sequences; retire native materialized views after parity | Native refresh replaces the materialized result and introduces avoidable staleness and repeated full-history work |

## Executive Recommendation

Use an incremental foundation reset, not a big-bang rewrite:

1. establish one repeatable local generation, test, vulnerability, and build command;
2. update dependencies in isolated, verified passes and remove dependencies that standard library or existing platform code can replace;
3. make authentication unconditional, require a namespaced player subject for ordinary ClientService calls, allow only the reviewed shared reads to use a subjectless principal with Server `READ`, and adopt coarse Eventun Server and Admin permissions using the current Extend authorization model;
4. move all true dedicated-server gauntlet runtime RPCs to ServerService and generate Unreal Client, selected GameServer, and Client+Server Models surfaces independently from the complete served/Admin specification;
5. extract bootstrap, transport, domain, and integration packages as touched code moves out of `internal/`;
6. isolate Accountun, Cardanoun, and other chain proof-of-concept adapters behind explicit optional registration;
7. replace duplicated event tables with a stable match-batch envelope, one source-tagged event store, explicit producer ordering, and a dedicated replay-artifact operation;
8. derive narrow match, heat, player-result, and progression contribution facts synchronously with accepted batches; aggregate lap count, total time, and best records without copying every lap or checkpoint;
9. add incrementally maintained record, career, and gauntlet serving projections while retaining batch-local raw reads for detailed summaries and insights;
10. remove the legacy duplicated `server_event`/`client_event` trees, stale SQL, native materialized-view dependencies, and compatibility code after output, freshness, and query-plan parity is established while preserving the replacement source/event-type partitions;
11. revisit the two teams solution designs against the completed foundation before implementing team APIs or UI.

Do not add a migration runner, CI service, ORM, generic repository layer, command bus, dependency-injection framework, or payload schema-version branching.

## Review Method

The review traced:

- every protobuf service and generated HTTP operation;
- gRPC and HTTP server registration;
- authentication, AccelByte admin verification, and request-context construction;
- representative client, admin, server, team, progression, and gauntlet endpoints;
- all Eventun `SendBatch` call sites relevant to team and gauntlet work;
- database acquisition and external-call lifetimes;
- schema initialization and the temporary production migration convention;
- Go, OpenAPI, Extend App UI, and Unreal generation workflows;
- current manual publish scripts and test organization.
- every direct Go dependency and the tracked Bun/npm dependency sets;
- current package ownership across the 154 files in `internal/eventun`;
- game-client event recording, complete-match submission, and post-match replay submission;
- raw-event consumers in progression, career, leaderboards, gauntlets, match history, recommendations, and insights;
- the Accountun/Cardanoun proof-of-concept coupling and the Koios/TapTools coupling subsequently removed by R01.

No Eventun source files were changed. The local WSL environment did not have Go on `PATH`, so the Go test suite was not run.

## Platform And Generation Constraints

### Extend Service Extension

AccelByte documents Service Extension as a gRPC service exposed through gRPC-Gateway, with the OpenAPI document generated from the protobuf service definition. Deployed apps expose Swagger UI and the specification used by SDK and App UI code generation.

Consequences for Eventun:

- protobuf, gateway, and Swagger generation remain the external API foundation;
- `/eventun/apidocs` and `/eventun/apidocs/api.json` must remain complete and usable;
- replacing gRPC-Gateway to reduce adapter code would work against the hosting model;
- a locally generated spec must preserve the deployed `/eventun` base path.

### Shared Cloud IAM

Shared Cloud permits custom permissions for Extend APIs. The platform constraints reinforce a coarse service-boundary scheme rather than endpoint- or domain-specific resources:

- custom resources must use Shared Cloud's prescribed `CUSTOM:NAMESPACE:{namespace}:...` or `CUSTOM:ADMIN:NAMESPACE:{namespace}:...` shape;
- one IAM client can have at most 10 custom permissions without AccelByte Support involvement;
- the current App UI documentation states that custom-permission endpoints are available to Studio Admin users, while Game Admin and View Only users receive `403` for that path;
- target audience is available as another IAM-client boundary, but an empty target-audience field does not narrow access.

The initial recommendation adopted three resource names, with ordinary Create, Read, Update, and Delete action bits assigned to RPCs as appropriate:

| Surface | Resource | Intended principal |
|---|---|---|
| Client | `CUSTOM:NAMESPACE:{namespace}:EVENTUN` | Default user role and player access tokens |
| Server | `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER` | Dedicated-server confidential IAM client |
| Admin | `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN` | Studio administrators and trusted service clients |

Shared Cloud testing later confirmed that the Client resource works when added to the default user role override and Eventun's confidential client has IAM Roles Read plus Basic Namespace Read. The result also invalidated the need for that resource: every player would receive every Client action, so it duplicates authentication while adding role-override lookup and cache dependencies. The approved correction removes the Client resource, ordinarily requires a valid game-namespace player token with `sub` for ClientService, and retains only the meaningful Server and Admin custom permissions. Exactly ten shared Client reads also accept a subjectless caller after Server `READ` validation.

The remaining two resources are service boundaries, not one permission per endpoint. A trusted principal may receive the appropriate action bits for its resource. The Admin resource replaces the current remote role-admin-status lookup and the Eventun-local `player_role = admin` shortcut for network authorization.

Use the current Extend template pattern for ServerService and AdminService: method `permission.resource` and `permission.action` annotations plus an authorization interceptor. ClientService uses the same mandatory authentication interceptor without permission annotations. Its ten shared reads apply an effective Server `READ` check only for an exactly subjectless caller; the other 58 methods reject tokens without a player subject. At the same time, move Bearer security to the Swagger-level default if generated App UI and Unreal consumers remain equivalent.

Authentication is always installed. Delete `PLUGIN_GRPC_SERVER_AUTH_ENABLED` runtime branching and its local-insecure documentation. Health and metrics remain on their existing non-product surfaces.

### Full Spec Versus Consumer Specs

The required full Swagger and generated consumer surfaces are separate concerns:

- `gen/0_eventun.swagger.json` is the complete served, Extend-contract, and Admin App UI specification;
- `gen/ikigai/eventun/v1/client.swagger.json` drives the Unreal Client API generation;
- `gen/ikigai/eventun/v1/server.swagger.json` contains only the five true dedicated-server runtime operations;
- Models is the deterministic full Client+Server union;
- GameServer is a deterministic consumer view selecting the ten reviewed Client reads and all five Server operations from those two specifications.

Dedicated-server claim, admission, match acceptance, and completion move together to `ServerService`. A deterministic structured merge of the generated Client and Server specifications supplies the Models input and must fail if duplicate paths, definitions, or top-level metadata conflict. GameServer reuses that union's definitions but filters HTTP methods by an exact operation-id inventory. Admin paths and definitions are not inputs to any Unreal surface.

A later game-client caller audit corrected one inherited assumption in that recommendation. The dedicated server also calls ten ClientService reads through the merged GameServer wrapper: `Player`, `Sponsors`, `Gauntlets`, `Gauntlet`, `GauntletStats`, `PlayerGauntletStats`, `GauntletLeaderboards`, `GauntletPlayerLeaderboards`, `GauntletCalendar`, and `GauntletCalendarCompleted`. An initial correction proposed ServerService counterparts solely because subjectless tokens were rejected on ClientService. That would duplicate stable read APIs only to express a caller-auth difference and was rejected. The accepted boundary keeps each read defined once on ClientService: player tokens retain normal behavior, while an exactly subjectless token must also satisfy Server `READ` on those ten methods. The other 58 Client methods remain player-only.

The GameServer operation inventory is explicit because it is a consumer contract, not a second network service definition. The complete merged specification remains unchanged in purpose, and server-side authorization remains the security boundary.

## API Surface Inventory

### Network Services

| Surface | Current shape | Consumers |
|---|---|---|
| gRPC `ClientService` | 69 RPCs; ten reads accept subjectless Server `READ`, while match ingest and artifact creation accept subjectless Server `CREATE` | Game client, Ascentun, authenticated players, and the bounded dedicated-server operations |
| gRPC `AdminService` | 60 RPCs | Extend App UI and operators |
| gRPC `ServerService` | 4 RPCs for stage-run runtime | Dedicated game servers |
| gRPC health and reflection | Registered on the same server | Platform health and development tooling |
| gRPC-Gateway HTTP | 133 operations | Unreal, website, Extend App UI, and diagnostics |
| Swagger UI and merged JSON | `/eventun/apidocs` and `/eventun/apidocs/api.json` | Extend contract, development, and code generation |
| Prometheus metrics | Separate HTTP server on port 8080 | Platform monitoring |

The corrected service boundary retains 133 authored RPC declarations and merged Swagger operations: 69 Client + 60 Admin + 4 Server. No additional handwritten product HTTP API was found. The ten effective Server `READ` policies and two Server `CREATE` policies on ClientService do not add operations.

### Internal And External Entry Points

`main.go` registers token refresh, player and Steam sync, gauntlet stage-run sweep, progression polling, automatic reward fulfillment, old-session cleanup, and course metadata sync. PostgreSQL runs the hourly materialized-view refresh through `pg_cron`.

Eventun also calls AccelByte IAM, Cloud Save, Session, Platform/Fulfillment, Entitlements, Catalog, Season Pass, and Chat-adjacent services, plus Accountun, Cardanoun, Cloudflare R2, and Steam. R01 removed the retired TapTools/Koios path. Database connection ownership should not extend across remaining network latency unless a specific operation requires it.

## Ground-Up Foundation Direction

### Why The Original Shape No Longer Fits

Eventun began as an event collector but now owns or supports:

- player identity and synchronization;
- career and public leaderboard reads;
- complete match history and replay association;
- gauntlet qualification, stage allocation, admission, results, and prizes;
- progression goals, challenges, counters, completion, and reward delivery;
- post-match insight input, scoring, policy, and snapshots;
- teams and upcoming team qualification;
- media and several optional blockchain integrations.

The original two event tables are therefore functioning as an implicit shared domain model. At least 12 schema files and 11 Go query files read raw `server_*` or `client_*` event relations directly. `c6_func_insight_metrics.sql` contains parallel client and server extraction paths, progression reloads selected raw events after ingestion, and hourly gauntlet materialized views parse match payloads again. The resulting complexity is not inherent to those features; it comes from repeatedly rediscovering match facts from unkeyed JSON rows.

### Replacement Match-Batch Contract

Replace `EventRequest` with a complete-match envelope shared by Client and Server services:

| Field | Requirement |
|---|---|
| `batch_id` | Required client-generated UUID; retained unchanged for any later retry |
| `session_id`, `match_id` | Required common match identity; removed from every individual event |
| `game_build` or equivalent ruleset identifier | Required diagnostic context; not a payload schema version |
| `events` | Ordered complete-match events |
| `event_id` | Required client-generated UUID on every event |
| `sequence` | Required contiguous producer order within the batch |
| `occurred_at` and event type | Required on every event |
| heat, player, progress, coordinate, payload | Optional event-specific data |

Validation rules:

1. `batch_id`, every `event_id`, and every sequence are unique within the request.
2. Sequence is contiguous and determines order when timestamps are equal.
3. The envelope contains exactly one `MatchStart` and one `MatchEnd` in valid order.
4. Every event belongs to the envelope's session and match by construction.
5. A repeated `batch_id` with the same canonical payload hash returns an already-accepted result without re-deriving facts.
6. A repeated id with different content returns `AlreadyExists` or `FailedPrecondition`; it is never silently merged.
7. `ReplaySaved` is rejected from a complete-match batch and written through a dedicated match-artifact operation.

The generated Unreal models cannot express optional-string presence: an
unset `MatchIngestEvent.player_id` or `MatchArtifactRequest.batch_id` is sent
as an empty string. Eventun therefore applies one narrow request-boundary
normalization before validation, canonical hashing, and persistence: those two
fields map `""` to absence. Empty and omitted forms have the same canonical
hash. This is not a general default-value policy; whitespace, malformed UUIDs,
and nil UUIDs are rejected, while required numeric zero values such as
`match_id`, `sequence`, and timestamps remain present and valid. Keeping this
compatibility rule in the contract avoids a field-name-specific fork of the
pinned third-party Unreal generator template.

The sender may remain at most once immediately after this cutover. Idempotent acceptance is foundation work; enabling bounded sender retry is a separate behavior change.

The envelope deliberately does not require a season or `competition_period_id` yet. Product seasons, statistics comparability scopes, physical storage segments, and retention tiers are separate unresolved concepts. Stable match identity, timestamps, source, and `game_build` allow retained matches to be classified after those policies are defined.

### Replacement Event Schema

Use one batch relation and one event relation:

| Relation | Core columns and constraints |
|---|---|
| `event_ingest_batch` | `batch_id` primary key; source kind; producer client id; submitting player id; session and match; game build; received and occurred bounds; event count; canonical payload hash; current derivation status and repair metadata |
| `game_event` | logical source-tagged parent with event id, batch id, producer sequence, occurred time, event type, heat, player, progress, coordinate, and payload; physically partitioned by source and event type unless reviewed benchmarks justify another layout |
| `match_artifact` | session and match; artifact kind; external record key; created time; source batch or request id when applicable |

`source_kind` preserves the current client/server distinction without duplicating the logical event contract. The replacement operations are defined once on ClientService and accept either a namespaced player subject or an exactly subjectless caller with Eventun Server `CREATE`. Eventun derives source from that verified actor class, not from a producer field or separate client/server route: a player subject is always `client`, even if it also has Server permission, while only the subjectless Server-authorized mode is `server`. Dedicated-server events are the higher-trust source; authenticated client events remain self-reported and potentially alterable, but are required for time trials and other modes without dedicated servers. The replacement should retain physical source/event-type partition pruning and equivalent targeted indexes beneath one parent. Facts and product queries must preserve this provenance and apply explicit source policies rather than silently treating the sources as equally authoritative.

Logical match acceptance is source-aware. Server identity is `(server, session_id, match_id)`. Client identity is observer-scoped as `(client, submitting_player_id, session_id, match_id)`, allowing distinct authenticated players to retain separate self-reported observations without allowing one observer to create multiple accepted batches for the same match. Equal canonical content submitted with a different batch id returns the existing accepted identity; differing content or provenance returns `AlreadyExists`. Accepted payloads are immutable. Producer correction remains blocked until an explicit audited supersession model preserves the original acceptance and transactionally rebuilds the one current fact and projection set.

The runtime replaces `ClientService.Event` with the one shared `ClientService.IngestMatch` operation at `POST /v1/match/ingest`, adds the one shared `ClientService.CreateMatchArtifact` operation at `POST /v1/match/artifact`, and removes `ServerService.Event` without a compatibility copy. Both shared writes use the actor-class authorization above. The game client selects those same ClientService operation ids into the generated GameServer consumer surface rather than adding server-specific APIs.

Do not replace the current source/event-type partition layout with one unpartitioned payload table by assumption. Many hot queries address event-type leaves and rely on leaf-specific indexes. F09 must preserve equivalent pruning in the new logical model and document how global event identity is enforced under PostgreSQL 16 partitioned-table uniqueness rules. Any additional retention-oriented partition dimension requires representative query plans, measured latency, and partition-count analysis. A future storage segment need not align with a product season or statistics scope. `event_ingest_batch` remains compact and useful after detailed events move to another retention tier.

Backfill existing data as follows:

- group ordinary server events by source, session, and match and client events by source, submitting-player observer, session, and match into synthetic batches;
- generate event ids and sequences ordered by timestamp plus a deterministic migration tiebreaker;
- create separate artifact records for existing replay events;
- record that equal-timestamp historical order is reconstructed, not authoritative;
- rebuild narrow facts and incremental serving projections, then compare representative career, leaderboard, gauntlet, progression, and insight outputs before deleting old relations.

### Selective Fact And Serving Layers

Derive only stable semantic contributions that either collapse multiple lifecycle
events or provide an idempotent product input:

| Fact | Product use |
|---|---|
| `match_fact` | receipt/completion, mode, build, qualifier context, canonical status, and a future statistics-scope association when approved |
| `heat_fact` | circuit order, course, laps, canonical state, start and end |
| `match_player_fact` | placement, best finish/lap, circuit points, credits, kills, deaths, crashes, obelisks |
| `heat_player_fact` | heat placement and finish, proven loadout dimensions, lap count, total lap time, best lap, and best-lap source identity |
| `progression_metric_fact` | normalized idempotent contributions keyed to their source fact |

Do not create a one-to-one `lap_fact` or `checkpoint_fact` by default. Current
career and leaderboard needs are served by heat/player lap aggregates and retained
records. Current insight reads are bounded to one match and player and should use
the corresponding source/event-type partitions. Add a purpose-specific segment
projection only after a cross-match product query and representative measurement
justify it.

Keep stable, frequently filtered semantic fields in typed columns. Keep sparse or
experimental telemetry in raw JSONB. A bounded JSONB object remains reasonable
for variable progression dimensions, but do not add a blanket GIN index until an
implemented containment query demonstrates the need. The raw event tree has no
whole-document JSONB GIN index; its generated columns and targeted B-tree or
expression indexes are already stored write-time projections.

After `CopyFrom` inserts one accepted batch, call bounded PostgreSQL derivation
functions in the same transaction. The database should project terminal and
summary events into the narrow facts and enforce source uniqueness. One current
fact set is retained per batch; a rebuild transaction replaces it rather than
retaining parallel global revisions. Expensive insight scoring, external rewards,
notifications, and bulk repair/backfill remain worker responsibilities.

Fresh player-facing reads use incrementally maintained ordinary tables rather
than periodic native materialized-view refreshes:

| Projection | Bounded read served |
|---|---|
| `player_course_record` or equivalent | best lap and best finish per player/course/source/category, with the winning source identity |
| player and player-course career rollups | sums, counts, minima, and other mergeable values needed to calculate current career output |
| gauntlet match contribution and retained best sequence | one contribution per player/match/qualifier plus the currently selected sequence and source matches |

Simple projections should update transactionally with accepted facts when the
measured ingest budget permits. Otherwise they use an idempotent immediately
queued projector with an explicit freshness target, watermark, and repair path;
an hourly refresh is not the target. Authoritative qualifier cutoff remains an
immutable snapshot, not a mutable projection.

Consumer changes:

- career and leaderboards read incremental serving projections; match-history lists may read narrow facts while full match details retain bounded raw reads;
- gauntlet qualifier scoring incrementally records match-player contributions and the retained best sequence, then snapshots authoritative results at cutoff;
- progression workers read `progression_metric_fact` and evaluate goals; they no longer reread raw event JSON to increment counters;
- standard insight metrics read narrow result facts plus batch-local raw lap/checkpoint payloads; raw payloads also remain available for diagnostics and uncommon segment analysis;
- existing native materialized views are transitional and are removed after incremental projections demonstrate output, freshness, and query-plan parity.

### Package And Dependency Direction

The target package shape is intentionally small and follows dependency direction rather than creating a package per table:

```text
cmd/eventun/       executable entry point only
internal/app/      configuration, dependency construction, jobs, servers, shutdown
api/               ClientService, ServerService, and AdminService gRPC adapters
auth/              claims, Eventun permission enforcement, request actor context
event/             match ingestion, validation, facts, artifact association
race/              course, match, career, and leaderboard reads
player/            player identity and synchronization
team/              team state and membership commands/queries
gauntlet/          qualification, slots, stage runs, brackets, and core prizes
progression/       goals, challenges, contributions, completion, and rewards
insight/           insight policy, inputs, scoring, and snapshots
media/             media validation and storage-facing operations
integration/       AccelByte, Steam, R2, optional Accountun and Cardanoun
gen/               generated protobuf and OpenAPI clients
```

Rules:

- `internal/app` composes concrete dependencies but contains no product behavior; top-level `app` remains exclusively the Extend App UI.
- `api` maps protobuf requests and gRPC statuses but delegates domain behavior.
- domain packages may use pgx directly; do not introduce repository-per-table wrappers.
- a domain owns the smallest interface it needs from an external service; `integration/*` implements it.
- domains do not import optional integration packages.
- extraction is incremental: move one working domain at a time and delete its old `internal/eventun` files immediately.
- do not create a `pkg/` replacement for `internal/`; these are service packages, not a reusable library facade.

### Optional Integration Boundary

Accountun and Cardanoun currently leak into core constructors and event/prize paths. Replace that coupling with explicit registration:

- Cardanoun implements an optional post-ingest sink. When disabled, no client or goroutine is created and event ingestion has no Cardanoun branch beyond iterating registered sinks.
- Accountun implements an optional gauntlet-prize settlement interface or separate experimental API surface. Core gauntlet prize calculations do not import generated Accountun models.
- TapTools announced its wind-down in June 2026. Its main site now reports paused operations, and `openapi.taptools.io` no longer resolves. Remove the generated TapTools client, startup construction, daily top-collection job, manual sync RPC, and TapTools-specific token metadata code rather than wrapping a retired provider.
- The TapTools feed only populated collection names and logos. Team gate ownership checks use Koios separately, and current Ascentun create/edit flows hide `token_gated`. No active Ascentun or game-client caller of Eventun's token catalog APIs was found.
- Delete the complete dormant token-gating slice, including Koios, token catalog APIs/tables, gate-token tables/RPCs, and the `token_gated` membership mode. A future gate should begin with a provider-neutral asset-source contract rather than preserve TapTools-shaped metadata.
- Optional proof-of-concept delivery remains best effort unless separately promoted to a supported product capability. Do not add a durable outbox solely for a disabled PoC.

### Dependency Audit

Eventun currently declares Go 1.26.1. Go 1.26.5 was released on 2026-07-07 with standard-library security fixes and is the required toolchain, module directive, and service-build baseline. Remove the retired token integration slice and run `go mod tidy` before upgrading so dead provider dependencies do not enlarge the compatibility surface.

Registry checks on 2026-07-10 found several direct modules behind their current releases. Update every remaining module and Go tool dependency to its latest stable release, but perform the updates in coherent verified families rather than issuing one blind upgrade command. An incompatible current release is a blocking decision to record explicitly, not an implicit reason to leave a dependency stale.

| Area | Current baseline | Checked current release | Direction |
|---|---|---|---|
| AccelByte Go SDK | `v0.88.0` | `v0.89.0` | Keep and update; validate auth and generated service calls |
| pgx | `v5.7.6` | `v5.10.0` | Keep and update; it remains the correct PostgreSQL-native driver |
| gocron | `v2.18.2` | `v2.22.0` | Keep and update; active, testable, and already matches scheduler needs |
| gRPC-Gateway | `v2.27.3` | `v2.29.0` | Keep and update with generated plugins and gRPC as one set |
| gRPC | `v1.77.0` | `v1.82.0` | Keep and update with protobuf and middleware verification |
| OpenTelemetry | `v1.39.0` / contrib `v0.64.0` | `v1.44.0` / contrib `v0.69.0` | Keep and update as one family; retain Zipkin while AccelByte advertises only Zipkin ingress, update semantic conventions, and revisit OTLP when the deployed contract changes |
| MinIO Go | `v7.0.97` | `v7.2.1` | Keep; a smaller fit for R2 than adopting AWS SDK v2 |
| oapi-codegen runtime | `v1.1.2` | `v1.4.2` | Keep only for generated optional integration clients |
| `pgx-gofrs-uuid` | 2023 pseudo-version | unchanged | Remove; standardize on `google/uuid` and pgx v5's native scanner/valuer support |
| zerolog | `v1.34.0` | `v1.35.1` | Replace with standard `log/slog`, matching the current AccelByte Go template |
| `godotenv/autoload` | `v1.5.1` | `v1.5.1` | Remove hidden runtime loading; Compose and explicit shell environments already provide configuration |
| `go-openapi/loads` | `v0.23.2` | `v0.24.0` | Remove if the generated spec can be served directly or patched with `encoding/json` |
| `mimetype` | `v1.4.11` | `v1.4.13` | Remove with TapTools collection-logo ingestion; no other current importer exists |

The root Buf CLI is `^1.34.0` while npm reports `1.71.0`, and the first three remote Buf plugins are unpinned. Pin the CLI, every remote plugin revision, and the Docker generator image to one recorded baseline.

The Extend App UI dependencies are mostly recent but several latest releases are major changes, including React Router 8, Vite 8, TypeScript 7, and Zod 4. Upgrade the App UI in its own task, one major family at a time, preserving the tracked lockfile and building after each family. Do not combine those migrations with protobuf contract changes.

Run `go list -m -u all`, `go mod tidy`, `go test ./...`, `go vet ./...`, and `govulncheck ./...` in the dependency task. A reported vulnerability must be classified by reachable code, not only module presence. No CI service is required; these commands belong in the local release verification script.

### Accepted Constraint: Retain Zipkin Until AccelByte Supports OTLP

R02 updated the retained OpenTelemetry modules to current releases. OpenTelemetry has deprecated its Zipkin exporter and plans to remove it in early 2027, but the deployed AccelByte Eventun configuration explicitly advertises Zipkin ingestion and does not advertise or document OTLP ingress.

Replacing the exporter before AccelByte changes that contract would disable deployed tracing. Eventun therefore retains `OTEL_EXPORTER_ZIPKIN_ENDPOINT` and the Zipkin JSON exporter despite the upstream deprecation. R03 updated resources to `semconv/v1.41.0`, preserved existing sampling, batching, service identity, and custom attributes, and added focused Zipkin construction and delivery coverage.

Future OTLP migration begins only when AccelByte changes the injected configuration or documents a supported endpoint. That future task must:

- replace the direct Zipkin exporter dependency and constructor with the supported OTLP trace exporter;
- replace the Zipkin-only endpoint configuration with the selected standard OTLP configuration and document the deployment cutover;
- preserve or deliberately rename `service.name`, `environment`, and `ID`, and record any sampling or batch-processing behavior change;
- verify exporter construction, resource attributes, and actual span delivery against a local OTLP receiver or Collector;
- remove the Zipkin exporter module only after the deployment contract and source migration are proven together.

## Confirmed Correctness Findings

### P1: Authenticated Client ID Is Not Propagated

The claims interceptor rejects an empty JWT `ClientID` but never calls `SetClientID`. Both client and server event ingestion read `common.GetClientID(ctx)`, whose fallback is the zero UUID.

Impact:

- event source identity is recorded as `00000000-0000-0000-0000-000000000000` on the reviewed path;
- source-specific diagnostics cannot rely on persisted `client_id`;
- future complete-match reliability policy cannot distinguish producers from stored data.

Fix:

- call `SetClientID(ctx, parsed.claims.ClientID)` in unary and stream interceptors;
- apply the same non-empty validation in both interceptors;
- add an interceptor-to-event-mapping test.

Do not add a general principal object for this fix. Existing typed context accessors are sufficient.

### P1: Some Batch Helpers Ignore The Only Error That Covers Later Statements

Eventun pins `github.com/jackc/pgx/v5 v5.7.6`. [`Conn.SendBatch`](https://pkg.go.dev/github.com/jackc/pgx/v5@v5.7.6#Conn.SendBatch) runs all queued queries in an implicit transaction unless explicit transaction-control statements are present. `pgxpool.Conn.SendBatch` delegates to that connection method.

Therefore:

- `createTeam`, `updateTeam`, `deleteTeam`, and the batched write portion of `abdicateTeam` are not partially committed merely because they omit `Begin`;
- a later statement failure aborts the implicit transaction;
- `BatchResults.Close()` must still be checked because it drains unread results and returns errors from later statements.

The concrete defect is in helpers such as `insertTeamMember` and `deleteTeamPlayerRequests`: they call `Exec()` for the first result, defer `Close()`, discard the deferred error, and then return success. If a later cleanup statement fails, the implicit transaction rolls back while the API reports success.

Fixes that reduce code:

- for a write-only batch whose per-statement command tags are not needed, return the checked result of `conn.SendBatch(ctx, batch).Close()`;
- use `conn.Exec` for one-statement operations such as adding or removing one team gate token;
- audit the remaining `defer br.Close()` sites and either consume every expected result or propagate the close error;
- do not wrap these calls in a new transaction abstraction.

### P1: Read-Decide-Write Team Transitions Still Need A Real Transaction

Implicit batch atomicity does not protect reads performed before `SendBatch`. Ownership transfer currently validates the replacement, reads the current owner, and then writes designations without locking those rows in one transaction. Membership transitions similarly perform authorization and state reads before selecting a write path.

As the team contract gains membership history, typed outcomes, audit, and notification intent, these state machines need one consistency boundary.

Recommendation:

- use `pgx.BeginFunc(ctx, pool, func(tx pgx.Tx) error { ... })` directly in the small number of read-decide-write commands;
- lock the team or active membership rows whose state determines the transition;
- write membership, request/invite cleanup, history, audit, and notification intent before commit;
- perform AccelByte or other remote calls outside the transaction;
- add a custom helper only if repeated direct `BeginFunc` usage is demonstrably longer or less clear.

This is command-specific transaction ownership, not a generic `DBTX` or repository layer.

### P1: The Clean-Slate Database Path Currently Runs Non-Clean-Slate SQL

At the reviewed baseline, `postgres.Dockerfile` copied every `migration/*.sql` file into `docker-entrypoint-initdb.d`. That included the canonical `a*` through `d*` files, both then-named temporary production deltas, and temporary development seeds.

The clean path has a confirmed conflict:

- `a0_create_init.sql` creates `team_player_team_id_idx` and `team_player_player_id_idx`;
- the then-named `d2_indexes.sql` creates the same indexes again without `IF NOT EXISTS`;
- automatic initialization would subsequently run the then-named `temp_migration.sql` and, as foundation work accumulates, `temp_migration_2.sql`; both are production deltas and may contain destructive/replacement work;
- temporary team and gauntlet seed scripts are also included automatically.

Historical accepted model at the reviewed baseline:

- `a*` through `d*` are the complete clean slate;
- `t0_migration.sql` is the manually applied, frozen production delta that defines the named production baseline;
- `t1_migration.sql` accumulates later foundation transitions from that post-`t0` baseline to the evolving clean slate;
- no migration runner or ledger is introduced.

Required cleanup:

1. remove duplicate and stale definitions from the clean slate;
2. make the PostgreSQL image copy only the clean-slate files;
3. keep both production deltas and all development fixtures in paths that are not copied automatically;
4. apply `t1_migration.sql` to a disposable production-schema copy that already includes `t0_migration.sql`, using `psql` error-stop behavior and, where supported by its statements, one transaction;
5. verify an empty database reaches the final schema before a release with schema changes;
6. do not modify or clear `t0_migration.sql`; advance the named baseline only through an explicit owner decision.

That explicit owner decision occurred on 2026-07-13. The current model supersedes the filenames above: the former `t0_migration.sql` is deployed and removed; `migration/migration.sql` is the stable pending production delta; fixtures are `t0_seed_courses.sql` through `t3_seed_teams.sql`; and canonical `d3_schedule_refresh_views.sql` owns the guarded pg_cron schedule definition. Do not introduce numbered production migration files.

A folder split such as `migration/clean`, `migration/production`, and `migration/development` is reasonable because it makes execution intent visible without adding runtime code. Keeping the existing filenames and using explicit Docker copy patterns is also valid.

### P1: Production Authentication Is A Hard Boundary

With authentication disabled, requests have no player id and the current policy treats them as service administrators. Insecure local operation is no longer required.

Required change:

- delete the `PLUGIN_GRPC_SERVER_AUTH_ENABLED` branch and environment variable;
- initialize the current Extend token validator and auth interceptor unconditionally;
- propagate claims, access token, player id, and client id through one actor context;
- enforce the three coarse Eventun permission resources described above;
- remove the remote AccelByte role-admin-status request once the Eventun Admin permission is authoritative;
- test player, dedicated-server, Studio Admin, and denied-token cases.

## Simplification Findings

### P1: API Wrappers Hold Database Connections Across External Calls

Every `apiAction` variant acquires a `pgxpool.Conn` before invoking the endpoint. This includes operations that do not use PostgreSQL and operations that call IAM, Cloud Save, Accountun, or reward services.

The issue is connection lifetime, not the existence of one small wrapper. On the current database tier, a leased connection should not wait through multi-second remote latency.

Incremental direction:

- keep `apiAction` for untouched database-only endpoints;
- new or modified handlers may call pool methods directly because `pgxpool.Pool` acquires and releases internally for each query;
- acquire an explicit transaction only for a local state transition;
- call external systems before or after that transaction according to the required semantics;
- use a durable outbox/work row only when an external effect must follow a committed local transition;
- delete `apiActionWithAccountun`; a closure can already capture the Accountun client, and touched Accountun flows should control their own database lifetime;
- do not add `apiActionWithoutDB` or a family of new wrappers.

### P1: The Team Contract Should Be Replaced While Touched

The current contract exposes caller-supplied team and owner ids, numeric designation and rank, current-only membership, and an `AddTeamMember` function that mixes transition selection, SQL, and permission checks.

The teams design already requires a direct pre-alpha replacement:

- Eventun generates team identity;
- owner is derived from the authenticated player at creation;
- ownership, visible title, capabilities, and competition rank are separate concepts;
- membership uses validity intervals;
- `AddTeamMember` remains one deterministic contextual operation and returns a typed transition outcome;
- remove token-gate behavior from the current contract; a future gate should use a provider-neutral asset source and does not shape the initial game-client flow;
- obsolete fields and designation-based authorization are deleted.

Implement the state machine in one clearly named team command function. Do not add command-bus, repository-per-table, or generic application-service frameworks.

### P1: Generation And Manual Release Steps Are Fragmented

Before F01, generation was split across Buf, `go generate`, the Extend App UI, and `scripts/make_unreal.sh`; paths and generator versions were inconsistent. F01 now provides the pinned reproducible baseline and optional App UI/Unreal entry points. The corrected Unreal boundary is implemented and verified: Client copies the Client specification, GameServer selects the exact ten shared Client reads plus five Server runtime operations, and Models uses the full Client+Server union. Only checked-in Ascent Rivals integration and compilation remain blocked by the expired Perforce ticket.

Buf already generates server interfaces with `require_unimplemented_servers=false`, but the three concrete Eventun service structs embed `Unimplemented*Server`. That embedding supplies default methods for future RPCs, so a newly added RPC can compile without a real handler. The reviewed 133 operations currently have handlers; this is a future-change risk.

The right scale is one local command, not CI:

```text
generate proto
generate external Go clients
generate Extend App UI client when requested
generate Unreal plugin when requested
build and test Eventun
build the service image
```

Recommendations:

- make `bun run gen` or one replacement script work from a clean checkout;
- pin the Buf CLI, Buf plugins, and Extend Codegen image versions;
- remove the three `Unimplemented*Server` embeddings so new RPCs require implementations at compile time;
- update README paths and the Shared Cloud manual upload/deploy steps;
- make the production publish script run or explicitly require the core generation/build verification first;
- keep App UI and Unreal generation optional subcommands because they are not needed for every backend-only release;
- consolidate near-identical dev/prod publish scripts only if one environment argument and one shared implementation reduce the total script surface.

No CI service is recommended.

### P1: OpenAPI Security Metadata Is High-Value Deletable Boilerplate

The service protos repeat operation-level Bearer security blocks across nearly the complete API even though authentication is global at runtime. The `Courses` operation already drifts by omitting the block while still passing through the claims interceptor.

Prototype one service-level Swagger security requirement. If generated output preserves the same effective Bearer requirement and the App UI and Unreal generators still succeed, delete the repeated blocks and keep only explicit public-operation overrides.

This is preferable to generating custom RPC handlers because it removes a large amount of declarative duplication without hiding Go control flow.

### P2: Dedicated-Server Runtime Methods Belong In `ServerService`

Claim, admission, match acceptance, and run completion are dedicated-server runtime operations. Move all four together from `AdminService` to `ServerService` immediately after the permission boundary. Keep the ten reads identified by the consumer audit on `ClientService`, authorize a subjectless caller with Server `READ`, and select them into the GameServer generated view instead of adding duplicate Server RPCs. This has four benefits:

- the external service name reflects the actual caller;
- `scripts/make_unreal.sh` can generate bounded GameServer wrappers from an explicit Client+Server operation selection instead of the merged admin specification;
- operator-only Admin methods no longer produce GameServer API hooks;
- Admin-only definitions no longer enter the shared Unreal Models surface.

Keep `CreateGauntletStageRuns`, `LaunchGauntletStageNow`, and other operator authoring/intervention methods in `AdminService`. Delete the old runtime routes rather than retaining compatibility aliases. This is an API-consumer and ownership cleanup; it does not require changing the accepted policy that validated service callers are broadly trusted administrators.

### P1: The Single Application Package Now Obscures Ownership

`main.go` is approximately 605 lines and owns configuration, client construction, servers, schedulers, and shutdown. More importantly, `internal/eventun` contains 154 Go files and approximately 45,000 lines spanning events, teams, gauntlets, progression, insights, prizes, media, players, and transport adapters.

`internal/` is valid Go, but validity is not the issue. The current package forces unrelated domain constructors to carry Accountun, R2, AccelByte, and Cardanoun dependencies, keeps all unexported names in one collision domain, and makes package-level logging and database helpers globally available to unrelated features.

Adopt the package layout in the ground-up direction section. Move the executable to `cmd/eventun`, put composition in `internal/app`, keep the three generated service implementations together in `api`, and extract one domain at a time. Do not perform a mechanical 154-file move with no ownership cleanup, and do not replace `internal/` with a generic `pkg/` folder.

The first extraction should be bootstrap, auth, and optional integrations. The event package follows with the new ingestion model. Progression, insights, teams, and gauntlets move when their raw-event dependencies or contracts are replaced. Each extraction deletes its former files so the transition does not leave duplicate implementations.

### P2: Validation And Error Cleanup Should Be Local To Touched APIs

Current code mixes manual validation, database failures as validation, gRPC errors inside DB helpers, broad `NotFound` conversion, and raw database errors. A service-wide domain-error framework would add another layer before teams deliver value.

For new team and gauntlet APIs:

- derive self player ids from authenticated context;
- validate structural request fields at the handler or command entry;
- return explicit `InvalidArgument`, `NotFound`, `AlreadyExists` or `FailedPrecondition`, `PermissionDenied`, and `Unavailable` statuses;
- keep SQL causes in logs rather than client responses;
- add shared validation or error helpers only after concrete repetition appears.

Complete-match envelope validation remains a small independent improvement: verify one consistent session/match identity and required start/end envelope before accepting a client batch.

### P3: Large Service Protos Do Not Justify Domain Service Proliferation

`client.proto` and `admin.proto` are visually large, but message definitions already live in domain files. Splitting TeamService, GauntletService, ProgressionService, and similar public services would add gateway registration and generated client churn without removing the per-RPC contract.

Retain ClientService, AdminService, and ServerService. Move operations only when caller type or generated-consumer ownership changes, as with dedicated-server gauntlet runtime.

## Target Request Shape

```text
validated JWT/cookie and Eventun service permission
  -> auth interceptor stores actor, player id, client id, token, and claims
  -> api adapter validates structural request fields and maps protobuf
  -> domain command or query owns behavior
  -> read-only work uses pgxpool.Pool directly
  -> read-decide-write command uses pgx.BeginFunc directly
  -> transaction commits local state, facts, history, audit, and required outbox intent
  -> external delivery occurs outside the transaction
  -> api adapter maps typed outcome to protobuf and gRPC status
```

There is no generic store layer, command bus, repository abstraction, or dependency-injection framework. The actor context and external interfaces remain small, concrete types owned by `auth` and the consuming domain.

## Prioritized Foundation Slice

### Required Before Team Contract Work

| Change | Why it precedes teams |
|---|---|
| Repeatable local generation and verification command | Every auth, proto, package, and event change depends on reproducible generated output |
| Retired token integration removal, Go 1.26.5, verified dependency updates, and vulnerability scan | Shrinks the module graph and resolves version compatibility before structural work makes failures harder to attribute |
| Mandatory auth and coarse Eventun permissions | Replaces the borrowed admin check and establishes the Client/Server/Admin trust boundary used by new APIs |
| Correct `client_id` propagation and checked batch completion | Fixes current source identity and false-success defects before code is moved |
| Clean schema / production delta / development seed separation | Makes the upcoming schema reset manually testable without a migration framework |
| Bootstrap and optional-integration extraction | Stops PoC clients from shaping event, team, and gauntlet constructors |
| Stable match-batch and event identity | Gives all later facts and state transitions reproducible source keys |
| Narrow shared facts keyed to identified matches | Prevents team qualification and progression from adding another raw-event aggregation path without duplicating high-cardinality telemetry; statistics scopes remain a separate deferred decision |
| Current-domain projection and bounded-read cutover | Proves the replacement model supports fresh career, leaderboard, progression, insight, and gauntlet reads before teams rely on it |

### Required Before Team Experience Implementation

| Change | Reason |
|---|---|
| Re-review the team experience design after foundation cutover | Update API and data assumptions to the implemented package and fact boundaries |
| Temporal team membership and one-team constraint | Required for historical attribution and deterministic team views |
| Replacement team command contract | Derive actor and owner from auth; separate visible title, permissions, and competition rank |
| Game-client browse/view/join design | Search is last; controller-first browsing and current route reuse need Pencil review |
| Public roster-stat and team-filtered leaderboard queries | Must use facts and current membership rather than new mutable aggregate tables |

### Required Before Team Gauntlets

| Change | Reason |
|---|---|
| Move runtime RPCs to ServerService | Gives the dedicated server the correct generated and authorized surface |
| Stage-run-scoped accepted results | Existing placement uniqueness cannot represent multiple bracket runs |
| Frozen qualification snapshots and concrete competition slots | Runtime admission must not recompute broad mutable standings |
| Team-at-performance membership attribution | Team top-N qualification must be reproducible after roster changes |
| Bracket entry, match, seed, bye, and advancement state | Brackets require durable graph state rather than stage metadata alone |

### Defer Or Reject

- migration runner or deployment-coupled schema ledger;
- CI or automated deployment infrastructure;
- generic `DBTX`, repository, command-bus, or dependency-injection frameworks;
- an ORM;
- payload schema-version branches;
- endpoint- or domain-specific IAM resource proliferation;
- durable delivery machinery for disabled proof-of-concept integrations;
- PostgreSQL major-version migration solely for teams;
- App UI major-version upgrades in the same change as protobuf contracts;
- automatic sender retry until idempotent batch acceptance is deployed and observed;
- compatibility branches after the coordinated pre-alpha cutover.

## Suggested Delivery Order

### R0: Retired Integration And Module Reset

- remove TapTools, Koios, token catalog and gate APIs/tables, and `token_gated` behavior across Eventun, Ascentun, and generated game-client APIs;
- tidy the reduced module graph and remove integration-only packages and requirements;
- move the module directive and service build to Go 1.26.5;
- update every remaining Go module and tool dependency to its latest stable release in verified families;
- resolve internal and generated-code compatibility without combining the upgrade with package reorganization or new product contracts.

### F0: Verification And Immediate Correctness

- pin generators and create one local verification command;
- propagate `client_id`, check every batch close, and replace one-statement batches;
- separate clean schema, production delta, and development seeds;
- remove stale SQL and verify empty-database creation.

### F1: Auth, Bootstrap, And Integrations

- remove runtime auth disable behavior;
- require a namespaced player subject for ClientService and add Eventun Server and Admin permission resources;
- remove borrowed role-admin authorization;
- move all four existing dedicated-server gauntlet runtime operations to ServerService, keep shared reads defined once on ClientService, and separate the generated Unreal Client, selected GameServer, and Client+Server Models inputs from the complete served/Admin specification;
- move the executable and composition into `cmd/eventun` and `internal/app`, leaving top-level `app` exclusively for the Extend App UI;
- move gRPC adapters into `api` and auth into `auth`;
- isolate optional Accountun/Cardanoun and give supported external systems explicit domain-owned boundaries;
- replace zerolog with `slog` and remove obsolete bootstrap dependencies.

### F2: Event And Fact Reset

- add ingest batches, unified game events, and match artifacts without presuming a season or storage-partition model;
- replace the protobuf event envelope and make acceptance idempotent;
- update the game client to generate batch ids, event ids, and sequence;
- derive narrow match, heat, player-result, lap-summary, and progression contribution facts in the ingest transaction;
- backfill legacy rows and validate representative outputs;
- move replay association to the artifact API.

### F3: Existing Domain Projection And Cutover

- move progression contributions and workers to facts, including queue leases/backoff;
- add incrementally maintained player/course records and career rollups, then move leaderboard and career reads to them;
- move match-history lists to narrow facts while retaining batch-local raw reads for full summaries and detailed insights;
- move gauntlet qualification to incremental match contributions, retained best sequences, and authoritative cutoff snapshots;
- remove the legacy duplicated client/server event trees, duplicated SQL, and obsolete materialized views while preserving the replacement source/event-type partitions;
- finish extracting the touched domains and remove `internal/`.

### F4: Team Design Refresh And Implementation

- revise the team experience/progression and team gauntlet/bracket designs against the implemented foundation;
- complete the game-client UI inventory and Pencil design phase;
- implement temporal membership, team views, controller-first browse/join flows, team presentation, roster stats, and teammate match indicators;
- implement team qualification, slots, roster control, admission replacement, brackets, and minimal website/admin changes in the later gauntlet slice.

## Manual Verification Plan

Use a local release check rather than CI:

- run the complete generation command from a clean ignored-output state;
- run `go test ./...`, `go vet ./...`, `govulncheck ./...`, and build Eventun;
- build the service image;
- start an empty PostgreSQL data directory and confirm all `a*` through `d*` files complete;
- apply `migration/migration.sql` with stop-on-error to an authentic disposable copy of the current deployed production schema, using `production-delta --confirm-disposable-production-baseline=<target-fingerprint>`;
- verify merged Swagger route and operation counts and Bearer metadata;
- verify Unreal Client and GameServer operation inventories and assert that the generated plugin contains no Admin operation or Admin-only model symbol;
- build the Extend App UI after its generated client changes;
- generate and compile the Unreal customization plugin when API contracts change;
- verify the Shared Cloud dedicated-server and operator IAM principals have the intended Server and Admin Eventun permissions; ClientService must work without a default-user-role override;
- manually smoke test a user call, Studio Admin call, dedicated-server call, denied call, idempotent event ingest, team transition, and affected gauntlet runtime call.

Focused backend tests should cover:

- unary and stream `client_id` context propagation;
- Client player-subject acceptance and service-token rejection, plus Server and Admin permission acceptance and rejection;
- later-statement batch failure returning an API error;
- rollback of a read-decide-write team transition;
- concurrent ownership or membership transitions;
- no database connection retained during a simulated slow external call;
- clean schema construction;
- duplicate batch with equal content returning already accepted;
- duplicate batch or event id with conflicting content being rejected;
- contiguous sequence and complete-match envelope validation;
- synchronous fact derivation rollback when any fact fails;
- representative old-versus-new career, leaderboard, progression, gauntlet, and insight output comparisons;
- disabled optional integrations constructing no client and starting no job;
- generated service method completeness where `Unimplemented*Server` embedding remains.

## Remaining Decisions

Resolved before implementation: all four current dedicated-server gauntlet runtime methods move together during foundation task F06B, before F11 and team-gauntlet work.

| ID | Decision | Working recommendation |
|---|---|---|
| FQ1 | Which IAM clients receive Eventun Server versus Eventun Admin? | Inventory and record them before permission cutover; do not add endpoint allowlists |
| FQ2 | Does global Swagger security preserve current App UI and Unreal generated output? | Prototype and compare before deleting repeated operation blocks |
| FQ3 | How are product seasons and statistics comparability scopes defined, owned, and associated with matches? | Deferred; do not add an active-period API or producer period field during identified-ingest work |
| FQ4 | What additional physical storage segments and retention tiers should telemetry use? | Deferred; preserve source/event-type pruning now and decide retention segmentation from measured scale and historical-product requirements before destructive retention |
| FQ5 | Which non-terminal metrics deserve typed fact columns in the first schema? | Promote fields already used by progression, leaderboards, qualification, and standard insights; keep experimental metrics in JSONB |
| FQ6 | Should bounded game-server retry ship with the idempotent contract or after observing it? | Keep it a separate task and enable it after idempotency tests pass |
| FQ9 | Which Extend App UI major dependency upgrades are required now? | Update security and compatible releases first; isolate React Router 8, Vite 8, TypeScript 7, and Zod 4 migrations |

## Source Index

Eventun:

- [Main bootstrap and scheduler](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/main.go)
- [Claims interceptor](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/common/claims.go)
- [Request context](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/common/context.go)
- [API action wrappers](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/action.go)
- [Requestor permissions](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/permissions.go)
- [AccelByte admin authorization](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/admin_authorization.go)
- [Team API](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/team_api.go)
- [Team database helpers](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/team_db.go)
- [Event protobuf contract](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/proto/ikigai/eventun/v1/event.proto)
- [Event ingestion](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/events.go)
- [Progression source-event queries](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/internal/eventun/progression_counter_db.go)
- [Gauntlet qualifier views](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/b4_view_gauntlet.sql)
- [Insight metric derivation](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/c6_func_insight_metrics.sql)
- [Canonical schema](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/a0_create_init.sql)
- [Go dependencies](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/go.mod)
- [Client service proto](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/proto/ikigai/eventun/v1/client.proto)
- [Admin service proto](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/proto/ikigai/eventun/v1/admin.proto)
- [Server service proto](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/proto/ikigai/eventun/v1/server.proto)
- [Buf generation](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/buf.gen.yaml)
- [Unreal generation script](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/scripts/make_unreal.sh)
- [Manual publish scripts](https://github.com/ikigai-github/eventun/tree/34b42861f2a698be50b0d7de134881544d072658/scripts)
- [Service image](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/Dockerfile)
- [Local PostgreSQL image](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/postgres.Dockerfile)
- [Temporary production migration](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/temp_migration.sql)
- [Duplicated index definitions](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/migration/d2_indexes.sql)
- [Repository README](https://github.com/ikigai-github/eventun/blob/34b42861f2a698be50b0d7de134881544d072658/README.md)

External primary references:

- [pgx v5.7.6 `SendBatch`](https://pkg.go.dev/github.com/jackc/pgx/v5@v5.7.6#Conn.SendBatch)
- [pgx v5.7.6 batch source](https://github.com/jackc/pgx/blob/v5.7.6/conn.go#L908-L914)
- [AccelByte Extend Service Extension](https://docs.accelbyte.io/gaming-services/modules/foundations/extend/service-extension/)
- [AccelByte Service Extension customization](https://docs.accelbyte.io/gaming-services/modules/foundations/extend/service-extension/customize-service-extension-app/)
- [Current AccelByte Go Service Extension template](https://github.com/AccelByte/extend-service-extension-go)
- [AccelByte Shared Cloud custom permissions](https://docs.accelbyte.io/gaming-services/modules/foundations/identity-access/authorization/master-permissions/custom-permissions/)
- [AccelByte Shared Cloud IAM client permissions](https://docs.accelbyte.io/gaming-services/modules/foundations/identity-access/authorization/manage-access-control-for-applications/)
- [AccelByte Extend App UI Swagger code generation](https://docs.accelbyte.io/gaming-services/modules/foundations/extend/extend-app-ui/codegen-specs/)
- [AccelByte Service Extension setup and production authentication](https://docs.accelbyte.io/gaming-services/modules/foundations/extend/service-extension/getting-started-service-extension/)
- [Go dependency management](https://go.dev/doc/modules/managing-dependencies)
- [Go release history](https://go.dev/doc/devel/release)
- [Go vulnerability checking](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [OpenTelemetry Go Zipkin exporter deprecation notice](https://pkg.go.dev/go.opentelemetry.io/otel/exporters/zipkin)
- [OpenTelemetry Zipkin exporter migration guidance](https://opentelemetry.io/blog/2025/deprecating-zipkin-exporters/)
- [pgx current module documentation](https://pkg.go.dev/github.com/jackc/pgx/v5)
- [gocron current module documentation](https://pkg.go.dev/github.com/go-co-op/gocron/v2)
- [PostgreSQL 16 declarative partitioning](https://www.postgresql.org/docs/16/ddl-partitioning.html)
- [PostgreSQL 16 materialized views](https://www.postgresql.org/docs/16/rules-materializedviews.html)
- [TapTools paused-operations page](https://www.taptools.io/)
