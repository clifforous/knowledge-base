# Ascent Rivals - Eventun API

Status: current

Applicability: committed local-development behavior unless a section explicitly identifies a
deployed AccelByte contract. This document does not imply shared-development or production
deployment.

Last consolidated: 2026-07-20

## Related
- [[../overview]]
- [[overview]]
- [[data-model]]
- [[identified-match-ingestion]]
- [[gauntlet-stage-runtime-contract]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/teams-solution-design|teams-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]
- [[ascent-rivals/sources/analysis/eventun-team-postgresql-derivation-review|eventun-team-postgresql-derivation-review]]
- [[ascent-rivals/sources/analysis/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]]

## Interface Domains

### Client-facing domain
Supports product-facing interaction flows:
- player profile and progression views
- team lifecycle actions
- gauntlet browsing and standings
- advisory gauntlet stage join preflight through `GetGauntletStageJoinStatus`
- history and summary retrieval
- wallet and eligibility interactions

### Match-ingest domain
Accepts complete-match telemetry from both player/local producers and dedicated servers through the single shared `ClientService.IngestMatch` operation. Replay association uses the separate shared `ClientService.CreateMatchArtifact` operation. Eventun derives client versus server source from the verified player or subjectless Server-authorized actor; producers do not select their own trust classification.

ServerService owns four dedicated-server gauntlet runtime operations: stage-run claim, admission, match acceptance, and completion. Dedicated servers obtain player/team presentation context, sponsors, gauntlet lists and details, stats, leaderboards, and calendars through ten existing ClientService reads; Eventun authorizes the subjectless caller with Server `READ` on those methods instead of duplicating the APIs under ServerService.

Gauntlet stage run match acceptance depends on trusted server events being present before Eventun derives `match_summary(session_id, match_id)`.

### Admin/operations domain
Supports privileged controls for:
- operational corrections and maintenance tasks
- sponsor and prize administration
- synchronization and cleanup operations
- gauntlet stage run inspection and intervention
- individual qualification cutoff preview, publication, and audited replacement

`PreviewGauntletQualificationCutoff` is a read-authorized Admin operation for pure individual `circuit_points` qualification stages. It takes the gauntlet/stage lock and returns a consistent projection revision, projection schema version, projector version, source/canonical/bot policies, entry limit, configuration hash, resolution hash, deterministic candidates, qualifier tie values, and exact source-match evidence. `PublishGauntletQualificationCutoff` and `ReplaceGauntletQualificationCutoff` require Admin `CREATE` and `UPDATE` respectively. Both require an idempotency key plus the previewed revision/schema/projector and hashes; stale input fails rather than sealing mixed state. Publish creates immutable version one. Replace requires the latest sealed snapshot id and a reason, creates a linked new version, and is rejected after a stage run has bound a cutoff.

## Authentication And Permission Model

Authentication is mandatory for every ClientService, ServerService, and AdminService RPC. Health and gRPC reflection are explicit non-product exceptions.

The implemented boundary is:

| Surface | Transport authorization | Intended principal |
| --- | --- | --- |
| ClientService | Valid AccelByte access token for the configured game namespace. The ten shared reads accept either a non-empty player `sub` or a subjectless client-credentials token with Server `READ`. `IngestMatch` and `CreateMatchArtifact` accept either a player subject or a subjectless token with Server `CREATE`. The other 57 methods require the player subject. | Players, plus dedicated servers for the twelve reviewed shared operations |
| ServerService | Subjectless client-credentials token plus `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER` with the method's semantic action | Dedicated-server confidential IAM clients |
| AdminService | `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN` with the method's semantic action | Studio Admin users and explicitly trusted confidential clients |

Shared Cloud validation proved that a blanket Eventun player permission can be granted through the default user role override when Eventun's confidential client has IAM Roles Read and Basic Namespace Read. It is not part of the implemented boundary: granting the same permission to every player expresses no authorization distinction, duplicates player-token authentication, and adds role-override configuration, lookup, and cache dependencies to every ClientService request. Server and Admin custom permissions remain because they distinguish trusted principals from ordinary authenticated players and unrelated service clients.

ClientService first validates token authenticity, expiry, revocation, and configured namespace through the AccelByte SDK without requesting a blanket Eventun player permission, requires either the token namespace or Extend target namespace to match `AB_NAMESPACE`, and requires a non-empty `client_id`. A nonblank `sub` follows normal player behavior. An exactly subjectless token is accepted on `Player`, `Sponsors`, `Gauntlets`, `Gauntlet`, `GauntletStats`, `PlayerGauntletStats`, `GauntletLeaderboards`, `GauntletPlayerLeaderboards`, `GauntletCalendar`, and `GauntletCalendarCompleted` after Server `READ` validation, and on `IngestMatch` and `CreateMatchArtifact` after Server `CREATE` validation. A whitespace-only subject is neither a player nor a service principal and is rejected. ServerService and AdminService methods declare a coarse Eventun resource and one semantic `CREATE`, `READ`, `UPDATE`, or `DELETE` action; missing, empty, or unknown permission metadata fails closed as a server configuration error. ServerService additionally rejects every token carrying a `sub`, even if that user can satisfy the Server permission, so only a subjectless service principal reaches product work.

- Bearer metadata and the Admin Portal `access_token` cookie are supported; Authorization metadata takes precedence when both are present.
- Successful validation propagates claims, raw access token, non-empty client id, and optional player subject through one request context for unary and stream handlers.
- The Admin resource is authoritative for AdminService. AccelByte role-admin-status lookup and Eventun-local `player_role = admin` are not network authorization paths.
- ClientService requires a player subject at the transport boundary except for the exact ten shared reads authorized with Server `READ` and the two shared writes authorized with Server `CREATE`. Self, ownership, manager, creator, and other domain checks remain authoritative for player calls after authentication; non-admin domain roles such as `gauntlet_creator` remain in force.
- The dedicated-server confidential client needs the Server resource with `CREATE`, `READ`, and `UPDATE`; it needs no Eventun Admin-resource grant. Shared match ingestion/artifact creation and stage-run claim use `CREATE`, the ten current query operations use `READ`, and admission, match acceptance, and completion use `UPDATE`.

## Integration Boundary
Eventun orchestrates competition flow and delegates accounting transition execution to [[../accountun]].

## Current Public Course API Gap

The current course response derives an `active` boolean and returns inactive rows as well as
active rows. It does not expose the complete AccelByte feature state or distinguish deliberately
retired courses from alpha, internal, or otherwise unreleased courses. It therefore is not a
public-visibility contract and is not safe for Website V2 to consume unchanged.

The unfinished server-side projection and fail-closed visibility behavior remain in the
[[ascent-rivals/initiatives/website-v2/pages/course-leaderboards|Website V2 course specification]].

## Observability Transport

- The deployed AccelByte Eventun configuration advertises Zipkin ingestion through `OTEL_EXPORTER_ZIPKIN_ENDPOINT` and does not advertise or document OTLP ingress.
- Eventun retains the deprecated OpenTelemetry Zipkin exporter until AccelByte changes the injected configuration or documents a supported OTLP endpoint. Replacing it earlier would break deployed tracing.
- Eventun uses OpenTelemetry `v1.44.0` semantic conventions from `semconv/v1.41.0` while preserving the existing one-second batch timeout, `AlwaysSample`, service identity, `environment`, and `ID` attributes.
- OTLP migration is vendor-dependent deferred work and must be coordinated with the deployed receiver contract.
- Structured logging defaults to `info`; `debug` is explicit opt-in. Unary and stream access records are metadata-only: method, final status, duration, request/response message counts, protobuf wire sizes, and sampled trace id. Request/response bodies, authentication metadata, cookies, tokens, and player payloads are excluded.
- The unary and stream interceptor boundary is metrics, access logging, error sanitization, then authorization and handler execution. This ordering makes metrics and access records observe the final client-visible status while the sanitizer covers authorization and handler failures.
- Deliberate non-`Unknown`, non-`Internal` gRPC statuses retain their code and public details. Bare or wrapped Go context cancellation and deadline errors retain `Canceled` or `DeadlineExceeded` with canonical `context canceled` or `context deadline exceeded` text, so wrapper diagnostics cannot cross the transport boundary.
- Raw errors and gRPC `Unknown` or `Internal` failures are logged internally with the original diagnostic and returned as `Internal` with the stable client message `internal server error`. This contract applies to both unary and stream RPCs.

## Runtime Resource And Failure Boundaries

- Ordinary RPC database work uses `pgxpool.Pool` with query-, batch-, or transaction-scoped
  acquisition. Database-free endpoints acquire no connection, and Eventun releases PostgreSQL
  capacity before player, Steam, course, replay, gauntlet-session, reward, or optional Accountun
  dependency calls.
- The single-instance pool defaults to eight maximum and one minimum connection, a five-second
  connect and startup-ping bound, fifteen-minute idle lifetime, one-hour maximum lifetime plus
  ten-minute jitter, and one-minute health checks. Existing Prometheus output exposes
  low-cardinality pool gauges and counters.
- Generated ordinary and catalog calls have thirty-second bounds, reward grants forty-five
  seconds, Steam fifteen seconds, and the supported Accountun settlement operation five minutes.
  An otherwise unbounded unary RPC receives a six-minute-thirty-second service deadline; a
  shorter caller deadline remains authoritative.
- Gateway HTTP bounds are five seconds for headers, two minutes for reads, seven minutes for
  writes, and two minutes idle. Metrics HTTP bounds are five seconds for headers, ten seconds for
  reads and writes, and one minute idle.
- Scheduled jobs use singleton rescheduling and bounded run contexts; progression retains its
  lease and lock-token fencing. The validated AccelByte namespace is constructor-injected and
  immutable per application instance.
- Only `pgx.ErrNoRows` represents database absence. Touched handlers preserve cancellation,
  deadlines, and deliberate gRPC statuses, while scan, iteration, infrastructure, and provider
  failures retain stable sanitized transport mappings.
- Shutdown stops new work, gives serving and reward finalization separate ten-second phases inside
  one twenty-second bound, and keeps the database pool open through reward finalization. A timeout
  does not close the pool underneath unfinished finalization.

## Uncommitted Team Replacement Under Review

An Eventun working-tree artifact based on `9213feb` replaces the pre-alpha team contract and has
coder-reported isolated verification. This section records that artifact for review; it is not part
of the committed baseline above and is not deployed to shared development or production.

The artifact removes legacy delete/abdicate, numeric designation, rank, and split pending-request
RPCs. It provides `Team`, `Teams`, `CreateTeam`, presence-aware `UpdateTeam`,
`TransferTeamOwnership`, `DisbandTeam`, `AddTeamMember`, `LeaveTeam`, `RemoveTeamMember`,
`ResolveTeamMembershipAction`, three title/capability/competition-rank updates,
`MyPendingTeamInvitations`, and `TeamPendingJoinRequests`; `PlayerMe` remains the authenticated
current-team read. The generated artifact contains 73 ClientService operations, 67 AdminService
operations, and 4 ServerService operations. Its merged Swagger has 144 operations across 125 paths
and 331 definitions. Unreal Client has 73 operations/173 definitions, Models has 77
operations/181 definitions, and GameServer remains limited to 16 operations/181 definitions.

All team classifications use fully prefixed protobuf enums because top-level enum values share
package scope: membership mode, team lifecycle status, presentation title, capability, action
kind/state, resolution, and membership outcome follow names such as
`TEAM_MEMBERSHIP_MODE_OPEN`, `TEAM_STATUS_ACTIVE`, `TEAM_CAPABILITY_MANAGE_MEMBERS`, and
`TEAM_MEMBERSHIP_OUTCOME_JOINED`. Externally returned action and lifecycle timestamps are signed
64-bit Unix milliseconds.

`CreateTeam` accepts no caller-selected team or owner UUID. Eventun generates the team identity,
derives the owner from the authenticated subject, and ensures an ID-only player row before locking
the creator. Names are trimmed to 4–16 characters, tags are normalized to 2–4 uppercase ASCII
alphanumeric characters, and colors are normalized uppercase `#RRGGBB`. `UpdateTeam` is an HTTP
`PATCH` and protobuf presence-aware patch: profile/media authorization applies only to fields that
actually change, while member-management authorization applies only to an actual membership-mode
change. A mode change cancels effective pending actions; ownership transfer preserves them.

`AddTeamMember` owns open join, join-request creation, invitation creation, exact UUID/version
invitation acceptance, and exact UUID/version request approval. `ResolveTeamMembershipAction`
owns only decline, deny, or cancel and also requires the exact action UUID/version. Neither method
infers a current action by team/player pair. Action state plus typed outcomes cover successful
join/create/accept/approve/decline/deny/cancel, capacity, expiry, supersession, and already-handled
delivery. Deliberate domain failures use stable gRPC statuses; cancellation/deadline mappings are
preserved and database diagnostics remain private.

The artifact adds only `Team` and `Teams` to the subjectless ClientService allowlist with Eventun
Server `READ`; every team mutation remains subject-bearing and uses Eventun domain authorization
without a custom player permission. These two Ascentun reads are not added to GameServer. The
Ascentun confidential IAM client therefore needs Server `READ` in each deployed environment, with
no dedicated-server or Studio Admin grant change. `TEAM_MAX_ACTIVE_MEMBERS` defaults to 16 and is
validated through normal configuration before constructor injection into membership transactions.

## API Compatibility
- Eventun consumers use generated HTTP gateway APIs rather than direct protobuf/gRPC transport.
- Removed protobuf fields do not need `reserved` declarations unless Eventun later exposes direct protobuf/gRPC clients.
- Treat protobuf definitions as the source for generated gateway shapes, not as a long-lived wire contract for external direct protobuf callers.
- Current committed code registers 70 ClientService RPCs, 67 AdminService RPCs, and 4 ServerService RPCs, producing 141 merged HTTP operations across 121 paths and 310 definitions. The ten dedicated-server reads and two shared writes are existing Client operations with alternate effective Server policies, not additional RPC declarations. The three qualification-cutoff operations and four season mutations are Admin-only; season listing is public through ClientService.
- The retired token catalog, manual token registration/sync, team gate-token methods, and their generated gateway operations have been removed. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.
- Mandatory unary and stream auth interceptors require a non-empty JWT `client_id` and place claims, access token, client id, and player subject when present in request context. ClientService authenticates without a blanket Eventun permission; its ten shared reads apply Server `READ` and its two shared writes apply Server `CREATE` only for subjectless callers, while the other Client methods require a player subject. ServerService and AdminService validate their annotated Eventun permissions. Stream handlers receive the enriched context through the wrapped `grpc.ServerStream`, and event ingestion rejects a missing client identity instead of persisting a zero UUID.
- Eventun uses only the coarse Server and Admin custom resources above; it does not define Client, endpoint-, or domain-specific IAM permissions. Client authorization below the transport boundary remains in Eventun's domain rules.
- API actions acquire a database connection only for the query, batch, or explicit transaction
  that needs it; handler execution and external dependency latency do not own a whole-RPC
  connection.
- Eventun continues serving the complete merged Swagger v2 document for the Extend contract and Admin UI. The four dedicated-server gauntlet runtime methods live only on ServerService. The ten dedicated-server reads and two shared writes remain single ClientService operations usable by their documented player and authorized subjectless service principals.
- Unreal Client is a byte-for-byte copy of the 70-operation Client specification across 61 paths with 152 definitions. Models is the deterministic full Client+Server union at 74 operations across 65 paths and 160 definitions; conflicting duplicate paths, definitions, or top-level metadata fail generation. GameServer reuses that union's metadata and definitions but selects only the ten reviewed Client reads, the two shared Client writes, and all four Server operations, producing 16 paths, 16 operations, and 160 definitions. No Admin or merged specification is an Unreal input.
- `ListSeasons` defaults to all past/current/upcoming regular seasons. `include_off_seasons = true` includes both kinds, ordered by `starts_at` then UUID. Admin create, full-replacement update, conditional title-only update, and delete route catalog mutation through the schedule-locking database functions. A semantic full replacement racing title-only mutation intentionally uses last-writer-wins for title; a failed title-only condition maps to NotFound if the row disappeared and Aborted if its semantics changed. Match History exposes only optional `season_id`, while clients resolve current title and kind through `ListSeasons`. The Extend editor accepts and round-trips explicitly labelled UTC timestamps.
- See [[ascent-rivals/sources/analysis/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]] for the recommended bounded foundation slice.

## Localization Contract
- Player-facing progression goal APIs should accept an optional requested locale, represented in HTTP as a `locale` query parameter and in protobuf request messages as an optional `locale` field.
- Supported locale tags should use BCP 47 style values such as `en-US`, `en`, `fr-FR`, or `fr`.
- Goal localization scope is limited to `title` and `description` for V1.
- Responses should return display-ready `title` and `description` resolved by requested locale, then language root, then English/default copy.
- Missing translations must not fail player-facing reads.
- Requirement JSON, metric codes, medal codes, SKUs, category values, visibility values, ids, and internal operator references are not localized API fields.
- Reward preview labels are fallback hints. For AccelByte catalog items, clients should prefer localized catalog names resolved from SKU when available.
- Admin localization export/import should be separate from goal definition CSV import. The localization workflow should export default copy for context, import one row per goal/locale, and sync published localization rows after source localization changes without requiring gameplay-rule publish.

## Current Notes
- Gauntlet stage AccelByte sessions are currently public for simplicity.
- Public session visibility is not authorization.
- The dedicated server is the final admission gate for gauntlet stages.
- Eventun is the authoritative owner of stage-run identity and accepted outcomes.
- `stage_run_id` is Eventun's durable run id.
- `session_id` is always the AccelByte/session-event id.
- `match_id` is a match index within the AccelByte/session-event context and can be `0`.
- Client preflight is advisory only.
- Dedicated servers should call stage-run admission for every human competitor join/rejoin; open stages return a cheap allow response after run/session/phase validation.
- Stage admission can return player team context (`team_id`, `team_name`, `team_tag`) when the player is on a team.
- `PlayerMe` returns the authenticated player's current Eventun team plus pending team invites and join requests. It is the appropriate initial source for a game-client team snapshot.
- `Teams` currently returns every team with its full roster and has no pagination, query, or lightweight summary response. That shape is retained for the expected current scale, with payload instrumentation used to decide when later search or pagination is justified.
- `AddTeamMember` deterministically interprets actor, target, the supported `open`, `invite`, and `request` membership modes, pending invitation, and join-request context for open join, request, invite, invite acceptance, and request approval. The approved replacement contract is maintained in the [team experience design](../../initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design.md) until its implementation review is accepted.
- Existing team mutation APIs return no updated team/player snapshot. A client integration must explicitly refresh or invalidate `PlayerMe`, team detail, and team-list caches after a mutation.
- Sponsor list/detail, CRUD, and sponsor-owned media administration are assigned to the Eventun Extend App before Website V2 cutover. The Admin surface needs reviewed list/detail reads and an administrator-authorized signed media-upload boundary. Existing sponsor create/update/delete handlers must become atomic, the stale delete reference to nonexistent `gauntlet_media.sponsor_id` must be removed, dependency behavior must be explicit, and sponsors with no media must return an empty collection before the controls are exposed.
- The current public leaderboard API returns global top N rows, and the player leaderboard API returns one player's ranks. Neither API accepts a team filter or returns complete roster-filtered leaderboard data.
- Team records do not currently include Twitch, Discord, or other external watch URLs. Sponsor records already provide a comparable URL pattern.
- Progression counters, goal progress/completions, challenge assignments, and active challenge APIs are player-scoped. Team XP and shared challenges require new authoritative team progress/contribution contracts rather than only a client presentation change.
- Existing reward fulfillment can grant player items, currency, and Battle Pass XP through AccelByte. It can be reused for configured activity-gated member rewards, but it does not own team XP or team cosmetic entitlements.
- AccelByte Challenges and Achievements are not product dependencies. Eventun progression evaluates detailed Eventun gameplay events rather than AccelByte stat-code requirements.
- AccelByte Chat persistent and transient system messages already back the game-client inbox and popups. Eventun should record notification intent in an outbox and deliver through Chat rather than add a second player read-state inbox, subject to a typed-payload prototype.
- Team progression administration belongs in Eventun's existing Extend App UI, not the interim Ascentun player website.
- Stage invite APIs exist for explicit player invites and explicit team invites.
- A stage's `allowed_teams` currently functions as a team membership eligibility filter, not as team scoring or team progression.
- Stage bracket fields currently function as required stage win/loss admission filters, not as a bracket graph or progression model.
- Sparse admission checks are on-demand audit/cache records, not participation or resolved racer slots.
- `gauntlet_stage_placement` is the participation record.
- Stages may have multiple configured `gauntlet_stage_circuit` rows, so agents must not assume one stage always equals one match.
- `gauntlet_stage_run_match` is the accepted-match ledger; `gauntlet_stage_circuit` is the configured match plan.
- Multi-match stage runs now use explicit per-match acceptance followed by aggregate run completion.
- Final stage placements are ordered by summed circuit points, then best placement, then placement sum, then player id.
- A first qualification stage-run claim locks the gauntlet before the run row and requires the latest sealed individual cutoff to match the locked live configuration hash, projection revision, schema version, and projector version. It binds the exact snapshot id and a complete rules snapshot. A same-session retry returns that stored binding without reapplying live freshness checks or overwriting the rules. Admission thereafter uses immutable cutoff membership, both rank fields, qualification points/counts, total circuit points, and the frozen stage circuit/match count; live run/session/phase, allowed-team/group, and prior-stage filters remain in force. Stage-run allocation uses the same gauntlet-before-stage lock order as full replacement. Gauntlet update preserves every stage parent with run/history rows, so open/invite configuration is edited in place without cascading away runs, admissions, matches, or results; omitting such a stage from this full-replacement API returns `FailedPrecondition` before mutation. Cutoff replacement and cutoff-relevant configuration changes are frozen only for qualification-bound stages.
- Match delivery remains at most once from the producer, but the implemented shared `ClientService.IngestMatch` contract uses a client-generated batch id, event ids, producer sequence, canonical payload hash, and idempotent acceptance. Automatic sender retry remains a separate behavior change.
- Player and dedicated-server producers call the same ingest operation. Eventun classifies a namespaced player subject as self-reported `client` data and an exactly subjectless Server-authorized token as higher-trust `server` data; the producer does not choose source kind. Both remain necessary because time trials and some local/career modes have no dedicated server. Facts, serving projections, and product policies preserve this provenance.
- Replay association now uses the separate shared `ClientService.CreateMatchArtifact` operation rather than a late authored `ReplaySaved` telemetry event.
- Identified ingest transactionally derives one current narrow match/heat/player/progression fact graph and applies idempotent record, career, and gauntlet serving projections before commit. Career and leaderboard/rank reads use ordinary projections; lifetime and seasonal leaderboard responses assemble all course/category groups set-wise and evaluate mutable `player_view` presentation once per request. Match History starts from source/player-selective server facts, performs keyed match/artifact lookup, orders by MatchStart, and preserves SessionStart version and replay association selected at the complete time/batch/sequence/event boundary. Gauntlet list/detail/stats/standings use ordinary projections and bounded views/functions. Time-trial history selects current candidates from facts, then fetches exact bounded PlayerHeatStart/End raw detail so the reported PlayerHeatEnd best-lap value remains authoritative. Full `match_summary` and current-match post-match insight baselines/metrics remain session/match-scoped raw reads for bot rows, loadouts, complete heat/standing presentation, and metrics absent from compact facts. Detailed post-match self-history selects current canonical server Ascent/placed candidates from facts, applies the ascension cutoff and per-heat limit, then fetches raw PlayerHeatStart/End detail only for those exact selected batch/event identities. Player discovery's one-day fallback, gauntlet runtime phase/match validation, most-recent-gauntlet lookup, replay purge, and fact repair/derivation are the other deliberate raw/legacy consumers. All twelve native materialized views, their refresh procedure, and the pg_cron schedule are retired.
- `gauntlet_stage_placement` includes `stage_run_id` but its current primary key is not stage-run scoped, which blocks independent accepted placements across multiple bracket runs in one logical stage.

## Open Questions
- Which admin controls should ship first for live gauntlet operations?
- Which runtime failures should trigger immediate AccelByte cleanup versus age-based cleanup?
- What exact DS-side kick/replacement tie-breakers should be used for equal-priority players?
- Should admission/preflight distinguish normal joins, reconnects, replacements, and spectator/shoutcaster joins?
- Detailed team API decisions are tracked in [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]].
- Detailed slot, admission, result, and bracket decisions are tracked in [[ascent-rivals/initiatives/teams-and-team-gauntlets/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]].
