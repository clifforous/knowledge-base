# Ascent Rivals - Eventun API

## Related
- [[../overview]]
- [[overview]]
- [[data-model]]
- [[gauntlet-stage-runtime-contract]]
- [[../game-client]]
- [[../website]]
- [[../accountun]]
- [[../../../30_designs/ascent-rivals/teams-solution-design|teams-solution-design]]
- [[../../../30_designs/ascent-rivals/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]]
- [[../../../30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]]
- [[../../../10_research/ascent-rivals/eventun-team-postgresql-derivation-review|eventun-team-postgresql-derivation-review]]
- [[../../../10_research/ascent-rivals/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]]

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

## Observability Transport
- The deployed AccelByte Eventun configuration advertises Zipkin ingestion through `OTEL_EXPORTER_ZIPKIN_ENDPOINT` and does not advertise or document OTLP ingress.
- Eventun retains the deprecated OpenTelemetry Zipkin exporter until AccelByte changes the injected configuration or documents a supported OTLP endpoint. Replacing it earlier would break deployed tracing.
- Eventun uses OpenTelemetry `v1.44.0` semantic conventions from `semconv/v1.41.0` while preserving the existing one-second batch timeout, `AlwaysSample`, service identity, `environment`, and `ID` attributes.
- OTLP migration is vendor-dependent deferred work and must be coordinated with the deployed receiver contract.

## API Compatibility
- Eventun consumers use generated HTTP gateway APIs rather than direct protobuf/gRPC transport.
- Removed protobuf fields do not need `reserved` declarations unless Eventun later exposes direct protobuf/gRPC clients.
- Treat protobuf definitions as the source for generated gateway shapes, not as a long-lived wire contract for external direct protobuf callers.
- Current code registers 69 ClientService RPCs, 60 AdminService RPCs, and 4 ServerService RPCs, producing 133 merged HTTP operations across 115 paths and 291 definitions. The ten dedicated-server reads and two shared writes are existing Client operations with alternate effective Server policies, not additional RPC declarations.
- The retired token catalog, manual token registration/sync, team gate-token methods, and their generated gateway operations have been removed. Token gating is unsupported until a provider-neutral asset-source contract is separately designed.
- Mandatory unary and stream auth interceptors require a non-empty JWT `client_id` and place claims, access token, client id, and player subject when present in request context. ClientService authenticates without a blanket Eventun permission; its ten shared reads apply Server `READ` and its two shared writes apply Server `CREATE` only for subjectless callers, while the other Client methods require a player subject. ServerService and AdminService validate their annotated Eventun permissions. Stream handlers receive the enriched context through the wrapped `grpc.ServerStream`, and event ingestion rejects a missing client identity instead of persisting a zero UUID.
- Eventun uses only the coarse Server and Admin custom resources above; it does not define Client, endpoint-, or domain-specific IAM permissions. Client authorization below the transport boundary remains in Eventun's domain rules.
- Every `apiAction` variant acquires a database connection before handler execution, including handlers that perform external calls or do not use PostgreSQL.
- Eventun continues serving the complete merged Swagger v2 document for the Extend contract and Admin UI. The four dedicated-server gauntlet runtime methods live only on ServerService. The ten dedicated-server reads and two shared writes remain single ClientService operations usable by their documented player and authorized subjectless service principals.
- Unreal Client is a byte-for-byte copy of the 69-operation Client specification with 148 definitions. Models is the deterministic full Client+Server union at 73 operations and 156 definitions; conflicting duplicate paths, definitions, or top-level metadata fail generation. GameServer reuses that union's metadata and definitions but selects only the ten reviewed Client reads, the two shared Client writes, and all four Server operations, producing 16 paths, 16 operations, and 156 definitions. No Admin or merged specification is an Unreal input.
- See [[../../../10_research/ascent-rivals/eventun-foundation-api-simplification-review|eventun-foundation-api-simplification-review]] for the recommended bounded foundation slice.

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
- `AddTeamMember` deterministically interprets actor, target, the supported `open`, `invite`, and `request` membership modes, pending invitation, and join-request context for open join, request, invite, invite acceptance, and request approval. The next contract should keep one operation but return a typed transition outcome and apply audit/notification intent atomically.
- Existing team mutation APIs return no updated team/player snapshot. A client integration must explicitly refresh or invalidate `PlayerMe`, team detail, and team-list caches after a mutation.
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
- Match delivery remains at most once from the producer, but the implemented shared `ClientService.IngestMatch` contract uses a client-generated batch id, event ids, producer sequence, canonical payload hash, and idempotent acceptance. Automatic sender retry remains a separate behavior change.
- Player and dedicated-server producers call the same ingest operation. Eventun classifies a namespaced player subject as self-reported `client` data and an exactly subjectless Server-authorized token as higher-trust `server` data; the producer does not choose source kind. Both remain necessary because time trials and some local/career modes have no dedicated server. Facts, serving projections, and product policies preserve this provenance.
- Replay association now uses the separate shared `ClientService.CreateMatchArtifact` operation rather than a late authored `ReplaySaved` telemetry event.
- Identified ingest transactionally derives one current narrow match/heat/player/progression fact graph per batch. Detailed laps and checkpoints remain in source/event-type partitions. Current reads stay unchanged until fresh incremental record/career/gauntlet projections prove parity and replace hourly native materialized-view refreshes.
- `gauntlet_stage_placement` includes `stage_run_id` but its current primary key is not stage-run scoped, which blocks independent accepted placements across multiple bracket runs in one logical stage.

## Open Questions
- Which admin controls should ship first for live gauntlet operations?
- Which runtime failures should trigger immediate AccelByte cleanup versus age-based cleanup?
- What exact DS-side kick/replacement tie-breakers should be used for equal-priority players?
- Should admission/preflight distinguish normal joins, reconnects, replacements, and spectator/shoutcaster joins?
- Detailed team API decisions are tracked in [[../../../30_designs/ascent-rivals/team-experience-and-progression-solution-design|team-experience-and-progression-solution-design]].
- Detailed slot, admission, result, and bracket decisions are tracked in [[../../../30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design|team-gauntlets-and-brackets-solution-design]].
