# 2026-07-10 Eventun Foundation And Initial Teams Tasks

**Status:** Active
**Project:** Ascent Rivals / Eventun / Ascentun / Game Client
**Primary repository:** `github.com/ikigai-github/eventun`
**References:**
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`
- `10_research/ascent-rivals/eventun-team-postgresql-derivation-review.md`
- `30_designs/ascent-rivals/team-experience-and-progression-solution-design.md`
- `30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design.md`
- `50_knowledge/ascent-rivals/eventun/data-model.md`
- `50_knowledge/ascent-rivals/team-gauntlet-current-state.md`

---

## Goal

Simplify and harden Eventun before adding teams features, then refresh and implement the initial team experience and team-gauntlet slices on the resulting foundation.

## Accepted Direction

- Breaking pre-alpha API, schema, and package changes are acceptable.
- Keep the three external service surfaces: Client, Server, and Admin.
- Keep the complete merged Swagger for the served Extend contract and Admin UI. Generate Unreal Client from ClientService, derive GameServer from the exact reviewed ten Client reads plus five Server runtime operations, and build shared Models from the full Client+Server union. Do not duplicate network APIs solely to express caller authorization.
- Require mandatory AccelByte authentication on all three surfaces. ClientService ordinarily requires a namespaced player token with `sub` and relies on Eventun domain authorization rather than a blanket player permission; exactly ten shared reads also accept a subjectless token with Server `READ`. ServerService and AdminService use coarse Eventun custom permissions.
- Remove local insecure runtime operation; authentication is always installed.
- Keep the canonical clean schema and one manually applied production delta. The owner confirmed the former `t0_migration.sql` was deployed on 2026-07-13 and removed it from source. Current pending transitions use stable `migration/migration.sql` against the deployed production baseline; verify it with `production-delta --confirm-disposable-production-baseline=<target-fingerprint>` against an authentic disposable production copy. Optional fixtures use the independent `t0_seed_courses.sql` through `t3_seed_teams.sql` sequence. Canonical `d3_schedule_refresh_views.sql` safely no-ops without pg_cron and is reapplied by guarded operational setup after provisioning. Do not add a migration runner, numbered production migration files, or a CI service.
- Move the executable to `cmd/eventun`, remove `internal/`, and extract domains incrementally.
- Keep pgx and PostgreSQL-first bounded aggregation. Do not add an ORM or generic repository layer.
- Introduce client-generated batch ids, event ids, and producer sequence. Do not add payload schema-version branches.
- Preserve the source/event-type `game_event` partitions as immutable detailed telemetry. Derive only narrow semantic facts that collapse lifecycle rows or establish idempotent contributions; do not copy every lap or checkpoint into a second wide relation.
- Prefer incrementally maintained ordinary projection tables for fresh leaderboard, career, progression, and gauntlet reads whose cost grows with retained history. Existing native materialized views are transitional and should be retired after output, freshness, and query-plan parity.
- Retain one current derived fact set per accepted batch. Rewrite it transactionally during repair or payload migration instead of keeping parallel global fact revisions online.
- Remove the retired TapTools integration and the complete disabled Koios/token-gating slice. Reintroduce gating later only through a newly designed provider-neutral asset source.
- After that removal reduces the module graph, move Eventun from Go 1.26.1 to Go 1.26.5, remove every unused Go dependency, and update every remaining Go module and tool dependency to its latest stable release.
- Resolve dependency and generated-code compatibility before changing package boundaries, auth, event ingestion, or other foundation architecture.
- Isolate Accountun and Cardanoun as optional proof-of-concept integrations during the later package extraction.
- Finish foundation work before re-approving the team solution designs.

**Production-baseline supersession:** completed-task evidence below preserves the filenames and verification claims that were true when each task ran. Any reference in that historical evidence to frozen `t0_migration.sql`, active `t1_migration.sql`, or `t2`-`t5` fixtures is superseded by the current convention above and must not be reused as worker instruction.

## Sequencing Rules

- Work one task at a time unless a task explicitly names a coordinated Eventun/game-client cutover.
- Complete R01 through R03 before starting or resuming any F-series foundation task.
- Remove dead integrations before updating modules so obsolete dependencies do not enlarge the compatibility pass.
- Keep each task buildable and reviewable. Additive transition schema may exist temporarily, but remove obsolete paths in the final cutover task.
- Do not combine dependency major-version migrations with protobuf contract changes.
- Use the currently available checks during R01 and each R02 dependency group. Run the complete local verification command after every Eventun task once F01 provides it.
- Update the knowledge base whenever an implementation decision changes these tasks or either team solution design.

## Mandatory Pre-Foundation Reset

### R01: Remove The Retired Token Integration Slice

- [x] Capture the existing Eventun build and test result using the current commands so pre-existing failures are distinguished from removal regressions.
- [x] Delete the TapTools OpenAPI source and generated client, `TAPTOOLS_API_KEY` configuration, startup construction, scheduled sync, admin sync RPC, and collection metadata ingestion.
- [x] Delete the Koios OpenAPI source and generated client, startup construction, wallet asset lookup, and token-ownership admission logic.
- [x] Delete Eventun token catalog, token registration/list APIs, team gate-token APIs, handlers, models, and `token_gated` membership behavior.
- [x] Historical R01 execution: remove `token_meta`, `team_gate_token`, and related schema objects from the canonical clean schema and add explicit removal to the then-active `migration/t1_migration.sql` without modifying the then-frozen `migration/t0_migration.sql`. Both names are superseded by the production-baseline convention above.
- [x] Delete integration-only IPFS/media helpers that have no remaining caller and remove retired configuration from deployment examples and documentation.
- [x] Remove Ascentun `token_gated` types, constants, and dormant handling.
- [x] Regenerate Eventun, Ascentun, and Unreal API outputs affected by the removed protobuf methods, and confirm no authored game-client code depended on them.
- [x] Record the future boundary: token gating is unsupported until a provider-neutral asset-source contract is separately designed.

**Done when:** no Eventun runtime, schema, protobuf, generated client, Ascentun source, or authored game-client source references TapTools, Koios, token catalogs, gate tokens, or `token_gated`; the remaining service builds and its available tests pass.

### R02: Reset The Go Toolchain And Module Graph

**Depends on:** R01

**Status:** Complete (2026-07-10)

- [x] Run `go mod tidy` immediately after R01 and review every removed direct and transitive module.
- [x] Set the `go` directive, local verification requirement, and service build image to Go 1.26.5.
- [x] Run `go list -m -u all` against the reduced graph and inventory direct, indirect, replacement, and `tool` dependencies.
- [x] Update every direct application module and Go tool dependency to its latest stable release on its current module path. Do not force unrelated upstream or tool-only transitive modules beyond their owners' tested graphs.
- [x] Remove unused direct requirements, unnecessary indirect requirements, and obsolete `replace` directives; retain a replacement only with a recorded reason.
- [x] Run available tests and an Eventun build after each family and record source-compatibility findings for R03.
- [x] Run final `go mod tidy`, confirm stable `go.mod` and `go.sum`, and run `govulncheck ./...`.
- [x] Record dependencies that require later source migration instead of silently downgrading them.

**Done when:** Eventun declares and builds from Go 1.26.5, the reduced graph contains no known unused direct requirement, direct application and Go tool dependencies are current, no reachable vulnerability is unreviewed, and remaining source migrations or build failures are recorded as concrete R03 inputs.

### R03: Resolve Upgrade Compatibility And Prove The New Baseline

**Depends on:** R02

**Status:** Complete (2026-07-10)

**Telemetry decision (2026-07-10): retain Zipkin.** The deployed AccelByte Eventun configuration explicitly advertises Zipkin ingestion through `OTEL_EXPORTER_ZIPKIN_ENDPOINT` and does not advertise or document an OTLP endpoint. Eventun will retain the deprecated Zipkin exporter until AccelByte changes the injected configuration or documents supported OTLP ingress. R03 preserves the one-second batch timeout, `AlwaysSample`, B3/W3C propagation, and the existing `environment` and `ID` resource attributes while updating semantic conventions and testing delivery through the supported Zipkin transport. OTLP migration is deferred vendor-dependent work, not an R03 requirement.

**R03 completion evidence (2026-07-10):** No source adaptations were required for the updated AccelByte, pgx, scheduler, gRPC/Gateway/protobuf, MinIO, OpenAPI, or other retained packages. The ignored Accountun client was regenerated with oapi-codegen `v2.7.2`; reviewed changes were generator-only, and a second full generation was stable with no protobuf, Gateway, or Swagger difference. The implementation worker reported that Go 1.26.5 tidies were byte-stable and formatting, generation, tests, normal and explicit Linux builds, vet, and govulncheck passed. The repository owner explicitly waived the service-image build for this pass because Docker is intentionally not running; image verification remains part of a later manual release check.

- [x] Resolve Eventun source compatibility with updated AccelByte, pgx, scheduler, gRPC/Gateway/protobuf, OpenTelemetry, MinIO, OpenAPI, and other retained packages one family at a time.
- [x] Complete approved major-version import-path migrations or package replacements identified by R02, then run final `go mod tidy`. No additional major-path migration was required; Zipkin is retained by the accepted deployment constraint.
- [x] Retain the Zipkin exporter required by the deployed AccelByte configuration and record the deprecation and future vendor-triggered migration boundary.
- [x] Move `internal/common/trace.go` from `semconv/v1.12.0` to the current semantic conventions shipped with OpenTelemetry `v1.44.0` (`semconv/v1.41.0`). Preserve or deliberately rename the existing service and custom resource attributes, and record any sampling or batching behavior change. Existing custom attributes, sampling, and batching were preserved.
- [x] Add focused tracer-provider verification for supported Zipkin construction, JSON delivery, service identity, and custom resource attributes.
- [x] Regenerate protobuf, Gateway, Swagger, and retained external clients where their updated generators or runtimes require it. Only the upgraded oapi-codegen tool required a retained-client change; protobuf, Gateway, and Swagger regeneration was difference-free.
- [x] Prefer deleting obsolete adaptation code or using the maintained package API directly; do not introduce generic wrappers solely to preserve old call shapes. No adaptation layer was required.
- [x] Record behavior changes caused by upgraded packages, especially auth interception, scheduler lifecycle, telemetry, storage, and generated-client error handling. No application behavior change was identified; Accountun generated helpers were additive/current-runtime changes.
- [x] Run formatting, generation, `go test ./...`, `go vet ./...`, `govulncheck ./...`, and Eventun builds with Go 1.26.5. The service-image build was explicitly waived for this pass and deferred to manual release verification.
- [x] Keep this task limited to compatibility and necessary deletion; defer package reorganization and product contract changes to the existing foundation tasks.

**Done when:** the reduced and fully upgraded Eventun source and generated code compile cleanly, telemetry continues exporting through AccelByte's supported Zipkin ingress with current semantic conventions, all required non-container checks pass, and intentional behavior and deferred vendor-dependent work are documented before architecture work resumes.

## Foundation Tasks

### F01: Establish The Reproducible Local Verification Baseline

**Depends on:** R03

**Status:** Complete and reviewed (2026-07-11; corrected Buf 1.71.0 baseline)

**Corrected F01 verification evidence (2026-07-10):** `./scripts/verify.sh` passed from a disposable clean WSL workspace with Buf `1.71.0`. It installed the frozen root tool lockfile, enforced the exact tool version, checked canonical protobuf formatting, ran `buf build` and STANDARD lint, generated protobuf/Gateway/Swagger/Accountun output from an empty `gen/` tree, and compared all 38 generated files with the reviewed SHA-256 manifest. It then checked `gofmt` and `go mod tidy -diff`, passed `go test -count=1 ./...`, `go vet ./...`, and a CGO-disabled `linux/amd64` Eventun build, and ran govulncheck `v1.6.0` with zero reachable or imported-package vulnerabilities. The known module-only `golang.org/x/crypto/openpgp` advisory remains unreachable. Generated completeness remains exact at 133 authored RPC declarations, 133 generated gRPC full-method constants, and 68 Client + 64 Admin + 1 Server = 133 merged Swagger operations. The command operates only on non-ignored source copied to a temporary tree, so local ignored generated output, environment files, and credentials are not trusted or modified.

The corrected baseline pins Go `1.26.5`, Bun `1.3.9`, Node.js `24.4.0`, npm `11.4.2`, Buf CLI `1.71.0`, oapi-codegen `2.7.2`, AccelByte App UI codegen `4.2.1`, govulncheck `1.6.0`, and AccelByte Unreal codegen/templates `2026.3.0`. The `bufbuild/buf:1.71.0` generator image is pinned to immutable index digest `sha256:7f3e3dfb8650f39878625bbc9f2016a51a781693b209165671d5a61d11c74992`. Every remote plugin was rechecked and is pinned by stable version and rebuild revision: Gateway `v2.29.0` revision 1, protobuf Go `v1.36.11` revision 1, gRPC Go `v1.6.2` revision 1, and openapiv2 `v2.29.0` revision 1. Only openapiv2 required a plugin-version change from the provisional F01 baseline.

The Buf configuration and output changes were reviewed rather than carried forward automatically. Both configuration files were already v2 and required no structural migration. `buf dep update` refreshed the locked Google APIs and grpc-gateway module commits, and subsequent update/prune checks were stable. The deprecated `DEFAULT` lint category was changed to `STANDARD`; legacy request/response naming, non-empty request/response reuse, and the one unused import are now grandfathered only by rule and affected path. The explicit Google Protobuf `Empty` request/response allowances remain because existing Admin RPCs use them. Buf `1.71.0` canonical formatting sorted imports in `admin.proto` and `client.proto`, added the final newline in `event.proto`, and removed whitespace in `gauntlet.proto`; `buf breaking . --against '.git#ref=HEAD'` passed. Regeneration changed only the dependency order embedded in `admin.pb.go` and `client.pb.go` and their corresponding init-call order. Gateway, Swagger, Accountun, messages, fields, RPCs, and routes were unchanged. The reviewed manifest contains exactly the resulting 38 files.

`./scripts/verify.sh appui` also passed with Buf `1.71.0`: the service output matched the same manifest and two App UI generation passes produced identical 338-file clients. The locked install retained the existing 35 npm audit findings and peer-dependency warnings assigned to F04, and AccelByte codegen retained its existing missing-`x-version` warning. `./scripts/verify.sh unreal` was exercised and stopped at its intentional Docker-daemon preflight without deleting the existing 18-file ignored output or changing its archive. Actual Unreal generation, generated-plugin integration/compilation, and the service-image build remain manual Docker prerequisites; Docker was intentionally not started and is not an F01 blocker. A Buf login is optional for an ordinary verification run but is a remaining prerequisite for repeated runs that would exceed the public BSR anonymous generation limit. No CI service was added.

**Review disposition (2026-07-11):** accepted with no blocking findings after read-only inspection of the implementation diff, generated-output contract, and recorded worker evidence. The review did not rerun generation, compilation, tests, lint, vulnerability scans, or image builds. The waived Docker-dependent Unreal generation and service-image build remain manual release checks, not unfinished F01 scope. The PostgreSQL image's inclusion of temporary migration and seed SQL remains assigned to F03.

- [x] Pin the Buf CLI, every remote Buf plugin, and the Buf Docker generator image.
- [x] Provide one local command that runs protobuf and external-client generation from a clean checkout.
- [x] Include `gofmt`/generated-diff checks, `go test ./...`, `go vet ./...`, `govulncheck ./...`, and an Eventun build.
- [x] Keep Extend App UI and Unreal generation as explicit optional subcommands, and exercise both once to establish the baseline. Unreal stopped at the required Docker preflight because the daemon is intentionally unavailable.
- [x] Update stale README paths and manual release prerequisites.
- [x] Record the exact Go, Buf, plugin, AccelByte codegen, Node/Bun, and Unreal generator versions.

**Done when:** one documented command succeeds from a clean generated-output state, generated service methods are complete, and the baseline results are recorded. No CI service is added.

### F02: Correct Existing Error And Source-Identity Paths

**Depends on:** F01

**Status:** Complete (2026-07-11)

**Completion evidence (2026-07-11):** Unary and stream claims interceptors now use one validation/enrichment path that rejects an empty `client_id`, stores claims, access token, client id, and an optional player subject, and supplies streaming handlers with a real context-overriding `grpc.ServerStream`. `GetClientID` no longer fabricates a zero UUID; event mapping returns an explicit Internal error when the interceptor invariant is absent. Focused tests cover unary and stream propagation, missing-client rejection without handler invocation, the optional service-token subject, authenticated interceptor-to-`EventRecord.ClientId` mapping, and missing event source identity.

All 32 original production `SendBatch` sites were audited. Four structurally fixed one-command prize updates now use `Exec`; the remaining 28 sites are 21 genuine multi-write batches and seven query batches. Six standings query batches, two team write batches, and the course-catalog scan-error path now handle `BatchResults.Close()` on every return. When an earlier operation and completion both fail, both remain in the error chain and completion failure takes Internal precedence over domain NotFound mapping. A production-path fake proves `insertTeamMember` cannot report success when its first queued write succeeds but a later statement fails during `Close`; no database or mocking dependency was added.

`gofmt` and `git diff --check` passed. `go test -count=1 ./internal/common ./internal/eventun` passed. The complete `./scripts/verify.sh` clean-room workflow passed with Go `1.26.5` and Buf `1.71.0`: protobuf formatting/build/lint, clean protobuf/Gateway/Swagger/Accountun generation and 38-file manifest comparison, Go formatting and `go mod tidy -diff`, all tests, vet, govulncheck `v1.6.0` with zero reachable or imported-package vulnerabilities, and the CGO-disabled `linux/amd64` Eventun build. Docker was not required or started.

- [x] Propagate validated `client_id` through unary and stream request contexts.
- [x] Add interceptor-to-event mapping tests.
- [x] Check every `BatchResults.Close()` result and remove deferred close errors that can report false success.
- [x] Replace one-statement batches with `Exec`.
- [x] Add a focused later-statement-failure test.

**Done when:** persisted source identity is nonzero for valid tokens and no audited batch helper can return success after rollback.

### F03: Separate Clean Schema, Production Delta, And Development Data

**Depends on:** F01

**Status:** Complete with owner-approved production-delta verification waiver (2026-07-11)

**Static implementation evidence (2026-07-11):** All SQL files were inventoried in dependency order. The pinned PostgreSQL image now selects the 21 canonical `a*` through `d*` files; frozen `t0_migration.sql`, active `t1_migration.sql`, development fixtures `t2` through `t5`, and optional operational SQL remain outside automatic initialization. Canonical data/configuration files are sequential: `d0_data_media_purpose.sql`, `d1_data_progression.sql`, and `d2_insight_policy.sql`. A definition-level audit found 21 exact duplicate indexes: five table indexes repeated between `a0` and the former `d2_indexes.sql`, plus 16 rank-materialized-view indexes repeated between `b2` and that file. The duplicates were removed, the 29 remaining table/partition indexes were moved beside their tables in `a0`, and the former index file was deleted. All 50 original index names now occur exactly once across canonical SQL: 34 in `a0` and 16 materialized-view indexes in `b2`; every unique index required by concurrent refresh remains. Actual PostgreSQL execution exposed and corrected the missing expression parentheses in `server_event_active_qualifiers_idx`, the only semantic definition change among those indexes.

The former `d0_data_course.sql` is now `t2_seed_courses.sql`: AccelByte Cloud Save `Courses` is the documented course source of truth, and the existing sync transaction can populate an empty cache. The scheduled sync is not immediate at startup and source records may omit public fields, so deployment documentation now requires manual course sync before course-dependent authoring and records possible fallback values. The former `d3_sponsors.sql` is now `t3_seed_sponsors.sql`: its named companies and billboard assets are mutable product content managed by existing admin CRUD, not required reference data. No production delta deletes existing course or sponsor content. The development helper applies `t2_seed_courses.sql`, `t3_seed_sponsors.sql`, `t4_seed_gauntlets.sql`, and `t5_seed_teams.sql` in dependency order and one transaction.

Twelve drop-only legacy `insight_*` preambles with no current definition or consumer were removed from `c5` through `c7`; no created view, function, procedure, trigger, or required reference/configuration row was removed. The misplaced pg_cron call and commented examples were removed from canonical `c4`; the procedure remains canonical and the semantically unchanged named hourly schedule is now explicit optional operational setup. The gauntlet development fixture was updated from removed stage columns to the current `region_code`, `entry_requirement`, and `players_per_team` schema and remains destructive, optional data.

`scripts/database.sh` provides explicit, guarded canonical, production-delta, development-seed, and operational modes. It remains necessary because a common `t*` prefix does not make production deltas, development fixtures, and operational setup one valid execution path. The helper requires explicit single-target `PGHOST`, `PGPORT`, `PGUSER`, and plain-name `PGDATABASE` settings, PostgreSQL 16, a mode-specific SHA-256 confirmation bound to the configured and live server identity, `psql --no-psqlrc`, `ON_ERROR_STOP`, and one transaction. It logs and fingerprints the configured endpoint plus server address/port, database/OID, authenticated/effective roles, version, and server start time. The applying psql process rechecks that identity, the mode precondition, every guarded SQL file, and the postcondition on the same connection; guarded files may not contain a backslash, which excludes psql meta-commands. Canonical mode checks for a normal empty-schema target and absence of optional course, sponsor, team, and gauntlet rows; delta mode checks characteristic post-`t0_migration.sql` objects before applying `t1_migration.sql`; no mode creates or drops a database. README commands document the two-step confirmation, frozen baseline, destructive seed order, pg_cron provisioning and job-owner requirements, and repeatable PostgreSQL 16.14 schema-only dump comparison.

Static verification passed: `bash -n scripts/database.sh`; explicit-target and target-bound-confirmation failure-path checks; `git diff --check`; cached diff check; byte-identical comparison of `t0_migration.sql` with `HEAD:migration/temp_migration.sql`; SQL-body comparison of `t1_migration.sql` with `HEAD:migration/temp_migration_2.sql` after its filename/header-only update; exact 21-file Docker selection; all 50 former `d2` index names retained exactly once with no unintended effective-definition change; and no pg_cron reference in canonical SQL. After the data/index reclassification, final sequential rename, and target-confirmation hardening, `./scripts/verify.sh` passed again from its disposable clean WSL workspace with Go `1.26.5` and Buf `1.71.0`, including protobuf formatting/build/lint and clean generation comparison, Go formatting and module stability, all tests, vet, govulncheck `v1.6.0` with zero reachable or imported-package vulnerabilities, and the CGO-disabled `linux/amd64` Eventun build. ShellCheck was unavailable.

**PostgreSQL 16.14 verification evidence (2026-07-11):** Docker Engine 27.2.0 built `postgres.Dockerfile` from the pinned `postgres:16@sha256:be01cf...a95c` base, which resolved to PostgreSQL `16.14` (`server_version_num 160014`). After the final sequential rename, a fresh tmpfs-backed container initialized all 21 and only the 21 canonical files with no log errors. The final database contained zero course, sponsor, team, and gauntlet rows; retained required media-purpose, progression, medal, and insight-policy rows; contained every former `d2` index; contained neither retired token table; retained the canonical refresh procedure; and contained no pg_cron extension/schema. `scripts/database.sh canonical --confirm-empty-database=<target-fingerprint>` constructed a second empty database in one transaction. PostgreSQL 16.14 schema-only dumps of the automatic and helper-built databases remained byte-identical at SHA-256 `c2a86ee328e606dfb28c9e0e82b9fba4fccf675241106789919849c3454bc393`. Calling `refresh_leaderboard_materialized_views()` succeeded. The four-file development-seed mode succeeded transactionally and produced 17 courses, 14 sponsors with 16 media rows, 10 teams, five gauntlets, and five current-shape stages; the course fixtures had complete positive public fields and stages had no missing/invalid region, entry-requirement, or players-per-team values. Negative tests proved the helper refuses a nonempty canonical target, a canonical database as a production-delta baseline, and operational scheduling without pg_cron. Two PostgreSQL containers with identical database and role names proved a confirmation from target A cannot authorize target B; the rejected target remained unchanged. A deliberate connection redirection between discovery and execution was rejected by the live in-session guard before fixture SQL, and a server restart invalidated its prior confirmation. The exact target-bound canonical and development-seed paths succeeded.

**Owner verification decision (2026-07-11):** Do not create or obtain an authentic disposable post-`t0_migration.sql` production copy solely to test `t1_migration.sql`, and do not require clean/delta schema-dump convergence for F03 completion. `t1_migration.sql` remains statically reviewed but unexecuted against the production-derived baseline. This explicitly accepts the residual risk that production may retain one of the 12 removed legacy `insight_*` signatures or lack the corrected `server_event_active_qualifiers_idx`; inspect and address those differences when the production delta is applied manually. Optional pg_cron setup was not executed because the standard image intentionally does not provision it; its guard and the canonical refresh procedure were verified.

**Review hardening completed (2026-07-11):** Destructive `database.sh` confirmations are now action- and target-bound, with the configured endpoint and complete live identity revalidated inside the applying transaction. Cross-target, changed-connection, restarted-server, TCP, and Unix-socket cases were exercised as described above.

- [x] Move or select SQL so the PostgreSQL image applies only the canonical clean schema.
- [x] Keep frozen `t0_migration.sql`, active `t1_migration.sql`, and `t2` through `t5` development fixtures outside automatic initialization.
- [x] Remove confirmed duplicate indexes, stale drop-only SQL, and commented executable SQL; review and repair optional seed compatibility without deleting unconfirmed records.
- [x] Add a stop-on-error command for empty-schema verification and disposable production-delta verification.

**Done when:** an empty PostgreSQL 16 database reaches the canonical schema without production deltas or development fixtures, the execution roles remain explicit and guarded, and the owner has accepted the documented waiver and residual risk for production-derived `t1_migration.sql` convergence.

### F04: Update Extend App UI Dependencies

**Depends on:** F01

- [x] Update compatible AccelByte SDK/codegen, React, query, Ant Design, Axios, lint, formatting, and build packages.
- [x] Upgrade React Router 8, Vite 8, TypeScript 7, and Zod 4 one major family at a time only after reviewing their official migration requirements.
- [x] Preserve the tracked package lockfile and run install, audit, lint, codegen, and production build after each family.
- [x] Record any major upgrade deliberately deferred because the current AccelByte App UI toolchain is not compatible.

**Done when:** root and App UI dependencies are at the latest compatible approved versions, all newer majors are either migrated or explicitly blocked by a documented incompatibility, and audit/build output is clean.

**Completed (2026-07-11):** The App UI is on the latest verified compatible graph under Node 24.4.0 and npm 11.4.2. React Router 8.2.0, TypeScript 6.0.3, ESLint 10.7.0, and all compatible patch/minor families passed isolated lint, deterministic codegen, and production-build checkpoints. `./scripts/verify.sh appui` now performs the promised frozen install, two-generation diff, lint, production build, and production-dependency audit in a clean workspace; the final run passed with 338 generated files and zero production audit findings.

| Direct package or override | Before | Final | Latest stable checked | Decision |
| --- | --- | --- | --- | --- |
| `@accelbyte/sdk` | 4.3.0 | 4.3.2 | 4.3.2 | Updated |
| `@accelbyte/sdk-extend-app-ui` | 0.2.0 | 0.2.2 | 0.2.2 | Updated |
| `@accelbyte/sdk-iam` | 6.3.3 | 6.3.5 | 6.3.5 | Updated |
| `@accelbyte/validator` | 0.2.30 direct | Removed direct | 0.3.1 | No authored import; 0.3.1 remains through current AccelByte packages |
| `@module-federation/vite` | 1.11.1 | 1.16.16 | 1.16.16 | Updated |
| `@tanstack/react-query` | 5.90.21 | 5.101.2 | 5.101.2 | Updated |
| `antd` | 6.3.1 | 6.5.0 | 6.5.0 | Updated |
| `axios` | 1.13.6 | 1.18.1 | 1.18.1 | Updated |
| `react` | 19.2.0 | 19.2.7 | 19.2.7 | Updated |
| `react-dom` | 19.2.0 | 19.2.7 | 19.2.7 | Updated |
| `react-router` | 7.13.1 | 8.2.0 | 8.2.0 | Major migrated in existing Declarative mode |
| `@accelbyte/codegen` | 4.2.1 | 4.2.2 | 4.2.2 | Updated; missing-`x-version` warning remains upstream/expected |
| `@eslint/js` | 9.39.1 | 10.0.1 | 10.0.1 | Major migrated with ESLint 10 |
| `@tailwindcss/vite` | 4.2.1 | 4.3.2 | 4.3.2 | Updated |
| `@types/http-proxy` | 1.17.17 | 1.17.17 | 1.17.17 | Already current |
| `@types/node` | 24.10.1 | 24.13.3 | 26.1.1 | Latest Node 24 declarations retained for the pinned Node 24 runtime |
| `@types/react` | 19.2.7 | 19.2.17 | 19.2.17 | Updated |
| `@types/react-dom` | 19.2.3 | 19.2.3 | 19.2.3 | Already current |
| `@vitejs/plugin-react` | 5.1.1 | 5.2.0 | 6.0.3 | Latest Vite 7-compatible release; 6.x requires Vite 8 |
| `eslint` | 9.39.1 | 10.7.0 | 10.7.0 | Major migrated |
| `eslint-plugin-react-hooks` | 7.0.1 | 7.1.1 | 7.1.1 | Updated; lifecycle findings corrected without suppressions |
| `eslint-plugin-react-refresh` | 0.4.24 | 0.5.3 | 0.5.3 | Updated |
| `globals` | 16.5.0 | 17.7.0 | 17.7.0 | Updated |
| `http-proxy` | 1.18.1 | 1.18.1 | 1.18.1 | Already current |
| `prettier` | 3.8.1 | 3.9.5 | 3.9.5 | Updated |
| `prettier-plugin-organize-imports` | 4.3.0 | 4.3.0 | 4.3.0 | Already current |
| `rimraf` | 6.1.3 | 6.1.3 | 6.1.3 | Already current |
| `tailwindcss` | 4.2.1 | 4.3.2 | 4.3.2 | Updated |
| `typescript` | ~5.9.3 | 6.0.3 | 7.0.2 | TypeScript 6 bridge migrated; 7 deferred below |
| `typescript-eslint` | 8.48.0 | 8.63.0 | 8.63.0 | Updated |
| `vite` | 7.1.7 | 7.3.6 | 8.1.4 | Latest compatible Vite 7; 8 deferred below |
| `zod` | 3.25.76 dev dependency | 3.25.76 application dependency | 4.4.3 | Generated runtime modules import it directly; latest Zod 3 retained and 4 deferred below |
| Axios override | 1.13.6 | 1.18.1 | 1.18.1 | Retained: removal restored vulnerable Axios 1.15.0/1.16.0 copies in AccelByte codegen/SDKs and raised the audit |
| Zod override | 3.25.76 | 3.25.76 | 4.4.3 | Retained: removal split generated schemas and SDK validation across Zod copies; the TypeScript check exceeded 74 seconds and 2.7 GB without completing, versus a 15-second/855-MB passing build after restoration |

Deferred majors have concrete toolchain blockers:

- Vite 8.1.4 is incompatible with `@accelbyte/sdk-extend-app-ui` 0.2.2's `vite: ^7.3.5` peer; `@vitejs/plugin-react` 6 is therefore also deferred.
- TypeScript 7.0.2 is outside `typescript-eslint` 8.63.0's `<6.1.0` peer and removes the compiler API used by `prettier-plugin-organize-imports` 4.3.0. A trial left unused imports and logged a `fileExists` failure, so TypeScript 6.0.3 is the verified bridge.
- Zod 4.4.3 is outside `@accelbyte/validator` 0.3.1's Zod 3 peer, while AccelByte codegen 4.2.2 pins Zod 3.23.8 and generates 32 one-argument `z.record` calls whose overload was removed in Zod 4.

Final evidence:

- `./scripts/verify.sh appui`: passed frozen installation, Buf format/lint and reviewed generation manifest, two identical 338-file App UI generations, lint, TypeScript/Vite production build, and `npm audit --omit=dev` with zero findings.
- `npm audit`: reduced from 35 baseline findings to 9 development-only findings (3 low, 6 high). All nine are owned by AccelByte codegen 4.2.2's hard-pinned ESLint 9.26.0 / TypeScript-ESLint 6 subtree; that tooling processes repository-controlled Swagger, config, and file paths and is not shipped in the App UI bundle. npm offers no compatible current-codegen fix. No production finding remains.
- `npm ls --all`: exits 1 only for the same upstream codegen ESLint peer mismatch and npm's missing optional WASM dependencies under Tailwind's cross-platform optional package. The installed direct/runtime graph is valid; `npm ci`, lint, codegen, and build pass.
- Vite emits a module-federation warning because TanStack Query has no default export and the output remains above the 500-KB chunk advisory. The emitted TanStack shared chunk imported successfully in Node, and `remoteEntry.js`, `remoteEntry.ssr.js`, `mf-manifest.json`, `mf-stats.json`, and the Vite manifest were all produced.
- No generated App UI output is tracked. Backend contracts, Go code, F03 database work, and product behavior were not changed.

**Review hardening (2026-07-11):** Zod 3.25.76 was moved from `devDependencies` to `dependencies` because the generated client imports and bundles it at runtime. The override remains 3.25.76. A frozen install, production-only Zod tree, lint, build, and production audit all passed; the deployed graph no longer relies on an AccelByte SDK transitive dependency to retain Zod.

### F05: Remove Or Replace Avoidable Runtime Dependencies

**Depends on:** F01

**Status:** Complete (2026-07-11)

**Completion evidence (2026-07-11):** All handwritten logging formerly using zerolog now uses one process-default `log/slog` JSON logger with debug enabled. The gRPC middleware adapter is the upstream v2.3.3 `logging.LoggerFunc` pattern and preserves level, gRPC fields, and trace id; the HTTP request middleware preserves method, path, and duration, and `http.Server.ErrorLog` uses `slog.NewLogLogger` at error level. Context-aware calls are used where request or job contexts already exist. The small `common.Fatal` helper logs a structured error and exits with status 1, preserving actual prior fatal-call behavior; a subprocess test verifies both the JSON event and exit status. Focused tests also verify the gRPC adapter and HTTP middleware/error-log bridge.

The pgx connection callback and `pgx-gofrs-uuid` were removed, leaving `google/uuid` as the application UUID type. The team designation query explicitly binds its slice parameter as `UUID[]`. A focused pgx default-type-map test passes scalar Google UUID encode/scan and `[]uuid.UUID` UUID-array encode/scan in binary format, covering the `ANY($n)` boundary without adding database orchestration.

The hidden `godotenv/autoload` import was removed. README local-run instructions now require an explicit, reviewed `.env`, export it with `set -a; . ./.env; set +a`, and run `go run .`; Compose and scripts remain environment-driven. `.env.template` passed `bash -n` and a clean-subshell export assertion without printing values.

Swagger serving now deterministically reads `gen/0_eventun.swagger.json` with the standard library and patches only top-level `basePath` through `map[string]json.RawMessage`, because runtime `BASE_PATH` is configurable while generated protobuf options remain `/eventun`. The existing UI and JSON routes remain, successful responses are explicitly `application/json`, and missing or malformed/non-object documents remain 500 responses. The handler test deep-compares the complete served document with the generated source after changing only `basePath`, ignores a lexically earlier decoy file, and verifies 115 paths, 133 Client/Server/Admin operations, 286 definitions, representative models, and Bearer metadata.

`go mod tidy` removed direct requirements for zerolog, `pgx-gofrs-uuid`, godotenv, and `go-openapi/loads`. `gofrs/uuid/v5`, `mattn/go-colorable`, and `mattn/go-isatty` became unreachable and were removed. `go-openapi/loads` necessarily remains an indirect module because the retained AccelByte Cloud Save models import `go-openapi/validate`, which imports `loads`; Eventun no longer imports or uses it for Swagger. The directly imported `go-openapi/runtime` and `strfmt` remain for current authorization code.

Focused `go test` and `go vet` runs passed for the root, common, and Eventun packages; `go test -race . ./internal/common ./internal/eventun`, `go mod tidy -diff`, `bash -n .env.template`, clean-subshell environment loading, and `git diff --check` passed. The complete `./scripts/verify.sh` disposable-workspace workflow passed with Go `1.26.5`: pinned protobuf formatting/build/lint and clean generation manifest comparison, Go formatting and module stability, all tests, vet, govulncheck `v1.6.0` with zero reachable vulnerabilities, and the CGO-disabled `linux/amd64` Eventun build. Generated output, App UI, protobuf/API contracts, auth behavior, SQL, migrations, schema, and product behavior were not changed.

- [x] Replace zerolog with standard `log/slog` and the current Extend interceptor adapter pattern.
- [x] Remove `pgx-gofrs-uuid`; use one application UUID type with pgx v5 scanning and values.
- [x] Remove `godotenv/autoload`; make local configuration explicit.
- [x] Serve or minimally patch generated Swagger with the standard library if `go-openapi/loads` is unnecessary.

**Done when:** each removed dependency has a verified replacement, logging remains structured, UUID handling and explicit configuration still work, and Swagger still serves the complete spec.

### F06: Adopt Mandatory Auth And Eventun Permissions

**Depends on:** F01, F04

**Status:** Complete (2026-07-11)

**Completion evidence (2026-07-11):** `proto/ikigai/eventun/v1/permission.proto` is a local STANDARD-lint-compatible adaptation of the AccelByte Extend Service Extension permission contract at commit `3d200c8f568f5820643c28905b5474f8d49b235c`. It preserves extension field numbers 50001/50002 and action wire values CREATE=1, READ=2, UPDATE=4, and DELETE=8. Descriptor tests prove all 68 ClientService methods use `CUSTOM:NAMESPACE:{namespace}:EVENTUN`, all 64 AdminService methods use `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN`, and the one ServerService method uses `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER`. The reviewed semantic inventory is Client 8 CREATE / 46 READ / 7 UPDATE / 7 DELETE, Admin 13 CREATE / 24 READ / 19 UPDATE / 8 DELETE, and Server 1 CREATE, for 133 annotated methods and totals of 22 CREATE / 70 READ / 26 UPDATE / 15 DELETE. Missing, empty, wrong-service, or unknown-action metadata fails closed as Internal before a product handler runs; only health and gRPC reflection bypass product permission lookup.

One unary and one stream interceptor now extract Authorization or Admin Portal cookies, resolve the annotated method permission, validate authenticity and that permission through AccelByte SDK v0.89.0 against `AB_NAMESPACE`, and propagate claims, the raw token, non-empty client id, and optional player subject. Authorization wins over cookies, and both `cookie` and `grpcgateway-cookie` remain supported. Startup constructs one concrete `iam.TokenValidator`, enables its local JWT/revocation validation, disables the OAuth repository's separate auto-refresh scheduler, and treats `Initialize` failure as fatal before server construction. The SDK validator owns client-token, JWKS, and revocation refresh; Eventun does not create a second validator. Interceptor order is metrics, structured logging, then mandatory auth for both unary and stream calls. Tests cover player Bearer, dedicated-server service token, Studio Admin cookie, header precedence, unary and stream context propagation, invalid/malformed/missing tokens, missing client id even when permission is also denied, denied permission, malformed descriptors, and operational-service bypass. The denied and misconfigured cases never call their handlers.

The optional auth branch, `PLUGIN_GRPC_SERVER_AUTH_ENABLED`, `AB_IAM_BASE_URL`, remote role-status authorizer, `iam.RolesService` constructor dependency, scheduled manual login, local `admin` shortcut, and admin-specific wrappers were removed. `internal/eventun/admin_authorization.go` and its tests were deleted. All 64 AdminService handlers now rely on the transport-level Admin permission and use the ordinary action wrappers without a role network call or local `player_role` query. `go mod tidy` moved `go-openapi/runtime` and `go-openapi/strfmt` from direct to indirect requirements because the retained AccelByte SDK still imports them. Client domain checks remain narrower than IAM: subjectless Client tokens are denied before ownership callbacks; team create/self, manager, hierarchy, and owner checks remain; DeleteTeam requires designation 0; `gauntlet_creator` and gauntlet creator ownership remain; and a local `player_role = admin` grants no bypass. The four dedicated-server gauntlet run methods remain together on AdminService with Claim=CREATE and admission/accept/complete=UPDATE, as required for the later coordinated service move.

The global Swagger prototype was accepted. Each service now declares one top-level Bearer requirement and all 132 redundant operation-level blocks were removed. The previously omitted Courses operation now inherits Bearer, and tests walk all 133 merged operations and validate effective security. The Client, Admin, Server, and merged specifications, after recursively removing only `security`, are byte-identical to the captured baseline; their normalized SHA-256 values are respectively `89953e8bf4eb79a8194baece3aebd28b9de42586cfe6fbf3fec6cb8a7b937480`, `0a950c726902866f1e7afad29604063c5c9b0b03a779cb5267df08242aad99ce`, `60b552083d109edfd63268067fca3e8d29f89a6432c959a3d10c829f3c05d952`, and `168e6ead3450fa4b8b0db50557477677fac781caba17de5d95845d937bb20b0f`. The merged contract remains 115 paths, 133 operations, and 286 definitions. App UI generation remained exactly 338 files and equivalent to baseline, with deterministic regeneration, lint, production build, and zero production audit findings. The pinned Unreal `2026.3.0@sha256:15f77da4a61f131940e30bf692a917e648d40eb6ba44c6023234707af05dccf1` generator remained exactly 18 files; non-spec output is byte-identical to baseline and normalized specs match. No Unreal script, service ownership, route, or game-client integration changed.

README and `.env.template` now require real Eventun IAM credentials and authenticated local calls, with no insecure switch. The grant-before-deploy checklist assigns Default User Client CREATE/READ/UPDATE/DELETE; dedicated-server Server CREATE plus temporary Admin CREATE/UPDATE only; Studio Admin and explicitly trusted operator/backend Admin CREATE/READ/UPDATE/DELETE; and Eventun's own `AB_CLIENT_ID` IAM Roles READ, Basic Namespace READ, plus existing downstream-service grants. It records that the temporary Admin grant remains only while the four runtime methods stay on AdminService and that the current App UI custom-permission path supports Studio Admin while Game Admin and View Only receive 403.

The reviewed generated manifest now contains 40 files, including `permission.pb.go` and its generated Swagger file. `./scripts/verify.sh` passed Buf format/build/STANDARD lint, clean protobuf/Gateway/Swagger/Accountun generation and manifest comparison, Go formatting and module stability, all tests, vet, govulncheck v1.6.0 with zero reachable or imported-package vulnerabilities, and the CGO-disabled linux/amd64 build under Go 1.26.5. `./scripts/verify.sh appui`, `./scripts/verify.sh unreal`, focused race tests, `.env.template` syntax/clean-shell assertions, legacy-reference scans, and both repository diff checks passed. No SQL, migration, event contract, team schema, service-method ownership, package layout, or game-client source changed.

**Review disposition (2026-07-11):** accepted with no blocking findings after read-only inspection of the implementation diff, permission and actor-context boundaries, domain-authorization cleanup, generated-contract changes, and recorded worker evidence. The review did not rerun generation, compilation, tests, lint, vulnerability scans, or consumer builds. Real Shared Cloud player, dedicated-server, and Studio Admin permission checks remain a mandatory grant-before-deploy release gate. Until F06B moves the four runtime methods, the dedicated-server's temporary Admin `CREATE` and `UPDATE` grant also authorizes every other AdminService operation using those action bits; that deliberately broad transitional access must not be treated as the final permission boundary.

**Shared Cloud validation and correction (2026-07-11):** the owner confirmed that Eventun's confidential client has IAM Roles Read and Basic Namespace Read, activated the game namespace's default user role override, obtained a fresh player token, and successfully called the protected player endpoint after restarting Eventun. This proves the AccelByte Shared Cloud mechanism is feasible. It also confirms that the Client permission is a redundant blanket grant when every player receives it. F06A therefore removes the Client custom-permission requirement while retaining mandatory token, namespace, client-id, and player-subject validation plus all Eventun domain authorization. Dedicated-server and Studio Admin smoke tests remain release gates for their meaningful custom-permission boundaries.

- [x] Import the current Extend permission proto and authorization-interceptor behavior.
- [x] Define `CUSTOM:NAMESPACE:{namespace}:EVENTUN` for ClientService.
- [x] Define `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER` for ServerService.
- [x] Define `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN` for AdminService.
- [x] Add method action/resource annotations without creating domain-specific permission resources.
- [x] Prototype Swagger-level Bearer security and remove repeated operation blocks after App UI and Unreal comparison.
- [x] Delete the `PLUGIN_GRPC_SERVER_AUTH_ENABLED` branch and documentation.
- [x] Remove remote role-admin-status authorization and Eventun-local player-role authorization from network admin access.
- [x] Document the default user role and confidential IAM-client grants in the manual deployment checklist.

**Done when:** player, dedicated-server, Studio Admin, and denied-principal tests pass and no runtime path can disable product API authentication.

### F06A: Simplify The Player Authentication Boundary

**Depends on:** F06

**Status:** Complete (2026-07-11)

**Implementation evidence (2026-07-11):** The mandatory unary and stream interceptor now selects an explicit policy by service. ClientService calls AccelByte SDK v0.89.0 `Validate(token, nil, &AB_NAMESPACE, nil)` exactly once, performs no Eventun permission lookup, requires a non-empty `client_id`, requires either the JWT namespace or Extend target namespace to match `AB_NAMESPACE`, and rejects an empty or whitespace-only player `sub` with PermissionDenied before context propagation or handler execution. The explicit namespace claim check closes the SDK's nil-permission gap where v0.89.0 validates a populated `extend_namespace` but does not otherwise compare the ordinary JWT namespace. ServerService and AdminService retain descriptor-based validation of their exact annotated resource/action. A failed privileged permission check is revalidated without a permission to distinguish an invalid token (Unauthenticated) from an authenticated principal lacking the grant (PermissionDenied). Health and both reflection services remain the only bypasses; unknown services and missing or malformed privileged descriptors fail closed as Internal.

All 68 ClientService RPCs are annotation-free and `client.proto` no longer imports the permission contract. Descriptor tests assert both permission extensions are absent from every Client method and that the generated Client file has no permission import. The retained privileged inventory remains exact: 64 Admin methods and one Server method, with 14 CREATE / 24 READ / 19 UPDATE / 8 DELETE actions. `permission.proto`, Admin and Server annotations, service ownership, routes, messages, schemas, and global Swagger Bearer security remain unchanged. Client domain authorization remains in force: subjectless Client tokens are rejected at transport, the local `admin` role grants no bypass, team ownership/manager/hierarchy checks remain, DeleteTeam remains owner-only, and `gauntlet_creator` plus gauntlet creator ownership remain enforced.

SDK failures are emitted as one token-safe structured warning with `grpc.service`, `grpc.method`, `auth.outcome`, and the sanitized original validation error. Privileged failures also record required resource/action and, when nil-permission revalidation fails, the sanitized authentication error. Exact access-token values are replaced with `[REDACTED]`; cookies, claims, client secrets, and internal IAM errors are not returned to callers. Tests cover Client player Bearer unary and stream success with nil permission, Extend-targeted user tokens, unrelated-namespace rejection, subjectless Client rejection, missing metadata/token/client id, malformed and invalid tokens, Admin cookie success, Server service-token success, Authorization precedence, privileged allow/deny/invalid two-pass behavior, error redaction, malformed descriptors, operational bypass, actor context, and the retained domain boundaries.

Regeneration changed only `gen/ikigai/eventun/v1/client.pb.go`, whose reviewed manifest hash moved from `43996c84733abb3e05d1a5e7d2154209db98fda4b76dafb45dc0df54d2445932` to `8cd8f079c8798d6b6d8b7151d214de8fdceac3712ea5a70fcf8acf72768559ea`; the other 39 generated hashes are unchanged. Client, Admin, Server, and merged Swagger files are byte-identical to the accepted F06 baseline. The merged contract remains 115 paths, 133 operations, and 286 definitions, with one global Bearer requirement and effective Bearer security on every operation. App UI generation remains byte-identical at 338 API files plus one Swagger file and passed deterministic generation, lint, production build, and a zero-finding production audit. Docker was already running and was not started; the pinned Unreal generator produced two identical 18-file outputs that are byte-identical to baseline.

`./scripts/verify.sh` passed the final clean-room generation/manifest check, Buf format/build/STANDARD lint, Go formatting and module stability, all tests, vet, govulncheck v1.6.0 with no reachable or imported-package vulnerabilities, and the CGO-disabled linux/amd64 build under Go 1.26.5. `./scripts/verify.sh appui`, `./scripts/verify.sh unreal`, focused tests and vet, race tests for the root/common/Eventun packages, generated-spec comparisons, stale Client-permission/grant searches, environment/run-wrapper checks, and repository diff checks passed. README removes the player grant requirement and instructs operators to remove only the temporary Eventun entry from the Default User Role Override without disturbing unrelated permissions. Durable API knowledge now describes the implemented player-subject boundary. No F06B service move or Unreal split, F07 package work, SQL, migration, event/team contract, downstream integration, or game-client change was made.

**Owner validation evidence (2026-07-11):** The owner removed only the temporary Eventun entry from the game namespace's Default User Role Override, restarted or redeployed Eventun, and confirmed that every Shared Cloud smoke result matched the documented boundary: a fresh normal player token reached ClientService, a subjectless service token was rejected there, a fresh Studio Admin token reached a read-only AdminService endpoint without modifying the built-in role, and the retained dedicated-server permission boundary behaved as expected. A separate valid confidential-client token without the requested AdminService permission returned PermissionDenied with `required permission is missing`, confirming the privileged missing-grant path remains enforced. README deployment guidance now distinguishes Shared Cloud's automatic built-in Studio Admin custom-permission access from custom grants that operators must assign to confidential IAM clients.

- [x] Stop requiring the retired Client custom permission and remove its default-user-role-override grant from deployment instructions.
- [x] Validate ClientService access tokens without an IAM permission lookup while retaining signature, expiry, revocation, configured namespace, and non-empty `client_id` validation.
- [x] Require a non-empty player `sub` for every ClientService RPC at the transport boundary; reject service tokens instead of treating any authenticated token as a player.
- [x] Preserve all self, team ownership/management, gauntlet creator, wallet, and other domain authorization checks after transport authentication.
- [x] Remove ClientService resource/action annotations, constants, descriptor assertions, and generated permission artifacts that no longer describe enforced behavior; retain the permission contract for ServerService and AdminService.
- [x] Preserve the underlying SDK validation failure in token-safe structured logs so an IAM dependency failure is distinguishable from a genuine missing permission; return Unauthenticated for invalid tokens and PermissionDenied for an authenticated principal lacking a required Server/Admin permission.
- [x] Update README, environment guidance, grant checklists, and API knowledge to describe authentication for ClientService and authorization for ServerService/AdminService.
- [x] Record coder-owned verification evidence.
- [x] Complete the owner-controlled Shared Cloud smoke checks for a normal player without the Eventun override, subjectless Client rejection, Studio Admin access without role modification, and the retained dedicated-server permission boundary.

**Done when:** every valid namespaced player can use ClientService without a custom role override, non-player tokens cannot use ClientService, Server/Admin permission behavior is unchanged, and no Client permission metadata or deployment grant remains.

### F06B: Separate Unreal Consumer Surfaces

**Depends on:** F06A

**Status:** Complete; implementation and game-client integration review passed (2026-07-12)

**Corrected Eventun implementation evidence (2026-07-12):** ClientService remains 68 annotation-free methods. The four dedicated-server stage-run methods moved without compatibility copies from AdminService to ServerService. No read method was copied: the ten reads proven by the Ascent Rivals caller audit remain their single existing ClientService definitions. AdminService is 60 methods with CREATE=12, READ=24, UPDATE=16, DELETE=8. ServerService is five true runtime methods with CREATE=2 for event ingestion and claim and UPDATE=3 for admission, match acceptance, and completion. The privileged descriptor inventory is therefore 65 methods with CREATE=14, READ=24, UPDATE=19, DELETE=8; the ten effective Server `READ` policies on ClientService are asserted separately rather than represented as Server RPC annotations.

The Client auth policy authenticates every call without a blanket Client permission. A nonblank player `sub` follows normal Client behavior. An exactly subjectless principal is eligible only on `Player`, `Sponsors`, `Gauntlets`, `Gauntlet`, `GauntletStats`, `PlayerGauntletStats`, `GauntletLeaderboards`, `GauntletPlayerLeaderboards`, `GauntletCalendar`, and `GauntletCalendarCompleted`, and must then pass a second validation for `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER` `READ`. The other 58 Client methods reject subjectless tokens after authentication, and a whitespace-only `sub` is neither a player nor a service principal. All five ServerService methods continue to require their annotated Server permission and an exactly subjectless principal. The moved adapters reuse the existing gauntlet runtime functions, leaving validation, transactions, idempotency, admission, and result behavior unchanged.

Generated specifications prove Client 59 paths / 68 operations / 143 definitions, Admin 51 / 60 / 162, Server 5 / 5 / 24, and the complete served contract 115 / 133 / 286. Unreal Client remains a byte-for-byte copy of `client.swagger.json`. Models is a recursively canonicalized structural union of the full Client and Server paths and definitions; duplicate paths, definitions, or top-level metadata must be structurally equal or generation fails. GameServer reuses the union metadata and 151 definitions but selects the ten reviewed `ClientService` operation ids plus all five `ServerService` operation ids at the HTTP-method level. Real-spec structural verification proves GameServer 15 / 15 / 151 and Models 64 / 73 / 151, with no Admin or merged specification as an Unreal input. This consumer view does not add network APIs.

`./scripts/verify.sh`, `./scripts/verify.sh appui`, and `./scripts/verify.sh unreal` pass after the correction. The default workflow passed the corrected Bun contract tests and structural checks, clean generation and reviewed manifest, Go formatting and module stability, all Go tests, vet, govulncheck, and the linux/amd64 build. App UI generation remained deterministic and passed its lint, build, and production audit checks. The pinned Unreal generator produced deterministic output and verified the exact Client, GameServer, and Models inventories above. The superseded 68/60/15 and 125-path evidence from the rejected duplicate-RPC implementation is not retained as completion evidence.

**Ascent Rivals integration evidence (2026-07-12):** After the owner refreshed the Perforce ticket, Windows-native `p4 login -s` confirmed a valid ticket before editing. The supplied regenerated package was inspected against the checked-in customization, then its five generated Eventun wrapper/model files and three Client/GameServer/Models specifications were integrated without hand-editing generated content; only CRLF normalization was applied for the Windows Perforce workspace. The obsolete tracked `spec/eventun.json` merged input was opened for delete, and the three obsolete plugin-local Eventun spec additions in junk changelist 5719 were abandoned and removed without touching the changelist's unrelated files. `HGEventunServerSubsystem.cpp` changes only the four requested `AdminService...` runtime call prefixes to `ServerService...`; the ten existing dedicated-server reads remain `ClientService` calls across that subsystem and `HGGauntletSubsystem.cpp`.

The integrated GameServer specification and wrapper each expose exactly ten selected `ClientService` reads and five `ServerService` runtime operations. Searches across the generated Eventun wrappers/models and the three retained specifications find no `AdminService` or `/v1/admin`. Final-state builds both passed with `Result: Succeeded`: `& 'D:\perforce\ascent\UE\Engine\Build\BatchFiles\Build.bat' AscentRivals Win64 Development '-Project=D:\perforce\ascent\UE\AscentRivals\AscentRivals.uproject' -WaitMutex` in 87.74 seconds, and the same command with target `AscentRivalsServer` in 86.49 seconds. Five generated Eventun files were already open in the default changelist and retained the owner's earlier token-surface removals through regeneration; this task additionally opened the three root split specs, the four-call source file, and the obsolete merged-spec delete. All unrelated changelist 5719 editor, cache, DLSS, NIS, Streamline, and Wwise files remain untouched. Nothing was submitted or shelved.

**Review evidence (2026-07-12):** Read-only review found no implementation issues. The default changelist contains the five generated Eventun wrapper/model files, the three split specifications, the four-call subsystem edit, and the obsolete merged-spec delete. The four source changes are limited to the required `AdminService...` to `ServerService...` prefixes. All eight integrated generated/specification files match the reviewed Eventun package after CRLF normalization. The GameServer wrapper and specification expose the same ten Client and five Server operations with no Admin symbol or route, the ten dedicated-server Client call sites remain intact, the merged spec is absent and opened for delete, and no plugin-local Eventun specification file remains. The review relied on the implementation worker's recorded successful client and dedicated-server builds and did not rerun them.

- [x] Record the pre-cutover caller inventory: the dedicated server used `ServerService.Event`, four gauntlet runtime operations then owned by AdminService, and ten read operations defined on ClientService through the merged GameServer wrapper.
- [x] Move `ClaimGauntletStageRun`, `CheckGauntletStageRunAdmission`, `AcceptGauntletStageRunMatch`, and `CompleteGauntletStageRun` together from `AdminService` to `ServerService` in one breaking contract change.
- [x] Delete the old Admin methods, routes, generated wrappers, and compatibility aliases; keep `CreateGauntletStageRuns` and `LaunchGauntletStageNow` in Admin.
- [x] Keep the ten existing dedicated-server reads defined once on ClientService. Permit an exactly subjectless caller only after Server `READ` validation; keep the other 58 Client methods player-only and do not add auth-only Server counterparts.
- [x] Require a subjectless service principal for every ServerService method and for the alternate path through the ten shared Client reads. The dedicated-server IAM client needs only the Server resource with CREATE, READ, and UPDATE after this cutover; remove its temporary Admin grant.
- [x] Generate Unreal Client only from `client.swagger.json`; derive GameServer by selecting the ten reviewed Client reads plus all five Server operations from the Client+Server inputs.
- [x] Build Unreal Models through a deterministic full structural union of the Client and Server specifications, failing on conflicting duplicate paths, definitions, or metadata; do not filter the merged Admin specification or include Admin-only models.
- [x] Continue generating and serving the complete merged Swagger for `/eventun/apidocs`, the Extend contract, and the Admin Extend App UI.
- [x] Update `scripts/make_unreal.sh` and the template inputs so the consumer boundary is explicit and reproducible.
- [x] Regenerate and integrate the Ascent Rivals Eventun plugin. Update only the four Admin runtime calls to their ServerService operations; retain the ten dedicated-server reads as ClientService calls.
- [x] Remove obsolete merged/Admin Unreal spec inputs and verify that no Admin operation, Admin route, or Admin-only model symbol remains in the generated or checked-in Unreal surface.
- [x] Refresh Ascentun's checked-in merged `api.json` contract snapshot without changing website behavior; preserve its accepted unrelated working-tree changes.
- [x] Correct the carried F06A README grant table so Studio Admin explicitly requires no role modification and trusted confidential clients carry the explicit Admin grant.
- [x] Rerun and record the complete corrected Eventun, App UI, and Unreal verification workflows and review the generation manifest.
- [x] Record coder-owned generated-plugin integration and client/dedicated-server compilation evidence; game-client behavior remains manually tested.

**Expected post-cutover inventory:** 68 Client methods, 60 Admin methods, and 5 Server methods for 133 merged operations across 115 paths and 286 definitions. The ten shared Client reads add an effective Server `READ` authorization path without adding operations. The derived GameServer view contains 15 selected operations, but it is a generator input rather than another served API.

**Done when:** the served full contract and Admin UI remain complete; Unreal exposes the Client API, the selected 15-operation GameServer consumer view, and the full Client+Server model union; the four true runtime calls use ServerService while the ten shared reads remain ClientService; the old Admin runtime operations and temporary Admin grant are gone; and no compatibility alias, duplicated read API, or merged/Admin Unreal input remains.

### F07: Extract Bootstrap, Transport, And Auth Packages

**Depends on:** F02, F05, F06B

**Status:** Complete; implementation review passed and changes remain uncommitted (2026-07-12)

**Implementation evidence (2026-07-12):** The previous 489-line root executable and 11-file `internal/common` catch-all were replaced by a 16-line `cmd/eventun/main.go` process boundary and packages with explicit ownership. The entry point only calls `internal/app.Run` and performs the final process exit; lower packages return errors. `internal/app` owns environment configuration and validation, AccelByte and PostgreSQL dependency construction, registration of all six scheduled jobs with immediate error checks, gRPC/Gateway HTTP/metrics servers, Zipkin tracing with B3 and W3C propagation, health, reflection, generated Swagger serving, and graceful concurrent shutdown of the scheduler, servers, tracer, and pool. The existing top-level `app` directory remains exclusively the separately built Extend App UI. Existing ports, routes, schedules, telemetry, and deployment behavior are retained.

`auth` now owns verified JWT claims, actor and access-token context, Client/Server/Admin authorization policies and interceptors, permission-descriptor validation, and the moved tests. The F06B boundary is unchanged: the ten reviewed Client reads accept an exactly subjectless principal only after Server `READ` validation, while the other 58 Client methods remain player-only. `api` owns explicit construction and registration of ClientService, ServerService, and AdminService plus the transport boundary. The 133 concrete RPC implementations deliberately remain in `internal/eventun` because moving them would require pass-through boilerplate or broadening its unexported domain API; this is a transitional boundary, not an API copy. `pb.Unimplemented*Server` embeddings were removed and compile-time generated-service interface assertions now make missing RPC implementations fail compilation. Pgx transaction ownership remains in the existing domain commands, and no container, command bus, repository framework, replacement catch-all, or domain import of `internal/app` was introduced.

The root `main.go` and `main_test.go` and all of `internal/common` were deleted, with tests relocated to their owning packages. Dockerfile, `run.sh`, `scripts/verify.sh`, and relevant README instructions now build or run `./cmd/eventun`. Every handwritten Go file is below 1,200 lines; the maximum is 1,149, after two oversized legacy files were mechanically split without behavior changes. `./scripts/verify.sh`, focused race tests and vet for `auth`, `internal/app`, `api`, and affected legacy packages, layout/import/`os.Exit` scans, entry-point inspection, and repository diff checks passed. Docker was already available and the service image build passed as `eventun:f07-verify` (`sha256:d2a0ce7f1c5176c72ed824d9c965da98937c37ab9f6cb34aa6ea0470f2dd1fce`). No protobuf contract, SQL, migration, generated API, dependency, authorization, scheduling, telemetry, or product behavior changed. F08 was not started.

**Review evidence (2026-07-12):** Read-only review found no implementation issues. `internal/app` is the accepted composition package because the top-level `app` directory is the TypeScript Extend App UI; only `cmd/eventun` imports it. Startup resources are acquired with corresponding deferred cleanup, service and Gateway registration remain complete, all six jobs are registered with immediate error checks, and shutdown orders scheduler/server draining before tracer and pool cleanup. The relocated auth policy retains the exact F06B Client, Server, and Admin boundaries, while compile-time assertions cover all 133 concrete RPC methods without unimplemented embeddings or pass-through copies. The moved transport tests retain the merged Swagger and operation-inventory checks. The gauntlet and insight file splits preserve their complete pre-split function inventories. Review relied on the implementation worker's recorded canonical verification, focused race/vet results, and successful Docker service-image build and did not rerun them. A live AccelByte/PostgreSQL startup smoke test remains part of deployment verification rather than F07 review.

- [x] Move the executable entry point to `cmd/eventun` and keep final process exit there.
- [x] Move configuration, dependency construction, server lifecycle, all six jobs, telemetry, and shutdown to `internal/app`, keeping top-level `app` exclusively for the Extend App UI.
- [x] Make `api` the explicit generated-service construction, registration, and transport boundary while retaining tightly coupled concrete RPC implementations in `internal/eventun`.
- [x] Move claims, actor context, access-token context, permission enforcement, interceptors, and their tests to `auth`.
- [x] Remove `Unimplemented*Server` embedding and add compile-time generated-service interface assertions.
- [x] Delete the root bootstrap and `internal/common`; update executable references to `./cmd/eventun`.
- [x] Keep pgx transaction ownership in domain commands; do not add a container, command bus, repository framework, or new catch-all package.
- [x] Keep every handwritten Go file below 1,200 lines.

**Done when:** `cmd/eventun/main.go` only invokes application startup, all existing API behavior still verifies, and old bootstrap/common files are deleted.

### F08: Isolate Optional And External Integrations

**Depends on:** F07

**Status:** Complete; implementation review passed and changes remain uncommitted (2026-07-12)

**Implementation evidence (2026-07-12):** Added focused `integration/accelbyte`, `integration/steam`, `integration/r2`, `integration/accountun`, and `integration/cardanoun` packages without a generic provider framework. `internal/app` remains the direct composition owner. It always constructs the mandatory AccelByte services and one configured Steam player-summary client, leaves the consumerless R2 client uninitialized, and conditionally constructs Accountun/Cardanoun only after their explicit enable flags and configuration validate. `ACCOUNTUN_ENABLED` and retained `CARDANOUN_FORWARDING_ENABLED` default to false. Injectable factory tests prove both disabled paths make zero constructor calls and produce no settlement or sink; invalid booleans, missing enabled settings, invalid URLs, and nonpositive adapter timeouts fail configuration or startup rather than silently disabling an enabled integration.

Accountun's OpenAPI source and generated client moved from `api/accountun` and `gen/api/accountun` to `integration/accountun` and `gen/integration/accountun`; the reviewed generated hash is byte-identical and only its manifest path changed. The adapter owns generated models, authentication, HTTP transport, timeouts, minor-unit/UUID/timestamp mapping, response checks, and representative register/funding payload tests. Core prize commands depend only on the domain-owned `GauntletPrizeSettlement` contract and domain inputs. All settlement-required commands return `FailedPrecondition` before any database mutation when settlement is absent, while prize and dust-status reads remain independent. `apiActionWithAccountun` and every generated Accountun import outside the adapter were deleted.

Cardanoun configuration, HTTP payload mapping, and tests moved into its adapter. Dedicated-server ingestion now iterates domain-owned `EventPostIngestSink` values only after successful persistence; app composition registers the Cardanoun sink only when enabled. Delivery remains asynchronous and best effort, with no outbox, retry, persistence, or synchronous failure coupling. Steam implements the domain-owned `PlayerSummarySource` and is injected once rather than constructed per sync. R2 has an explicit validating constructor and no startup consumer. AccelByte client/service construction moved from `internal/app` to its integration package, and reward consumers now receive the domain-owned `RewardGrantService` interface. Concrete IAM, CloudSave, Session, Platform, and Season Pass SDK pointers remain only at documented legacy boundaries where wrappers would duplicate the SDK.

`./scripts/verify.sh`, focused race tests and vet for all integration packages, `internal/app`, `api`, and `internal/eventun`, module-tidy and diff checks, optional-boundary scans, and the linux/amd64 build passed. Generated Eventun inventories remain 68 Client, 60 Admin, and 5 Server operations; all 13 Unreal contract tests passed. `govulncheck` found no called or imported vulnerabilities and one module-only finding. Docker was already available and `eventun:f08-verify` built as `sha256:4d973fbfcacffe99ba73764f5e40bcc3ac47a0362c621888662ea71ac8131af3`. No protobuf, SQL, migration, module dependency, App UI, authorization, telemetry, scheduling, Swagger, Unreal, or product behavior changed. F09 was not started.

**Review evidence (2026-07-12):** Read-only review found no implementation issues. Accountun and Cardanoun are disabled by default and their factories are not called when disabled; enabled invalid configuration fails startup. All settlement-required prize commands check the domain-owned settlement dependency before acquiring or mutating database state, while prize and dust-status reads remain available without Accountun. Dedicated-server Cardanoun delivery occurs only after the event transaction commits and remains asynchronous and best effort. The generated Accountun client is confined to its adapter, the old generated paths and provider-specific action wrapper are removed, Steam is constructed once and injected through `PlayerSummarySource`, and R2 has no startup consumer. The remaining concrete AccelByte SDK pointers are the documented transitional legacy boundaries; reward consumers receive `RewardGrantService`. Review relied on the implementation worker's recorded verification, race/vet, generated-inventory, vulnerability-scan, and Docker-build evidence and did not rerun those commands.

- [x] Move supported AccelByte, Steam, and R2 adapters and optional Accountun/Cardanoun adapters under `integration`.
- [x] Make Accountun and Cardanoun disabled by default and construct nothing when disabled.
- [x] Register Cardanoun as an optional best-effort post-ingest sink rather than an event-service field.
- [x] Put Accountun behind a gauntlet-prize settlement interface or a separate experimental API surface.
- [x] Do not reintroduce provider-specific token metadata or ownership dependencies while extracting supported and proof-of-concept integrations.
- [x] Ensure no domain imports generated optional-integration models.

**Done when:** core Client/Admin/Server constructors contain no Accountun or Cardanoun parameters, disabled PoCs start no clients, jobs, or goroutines, and supported integrations have explicit domain-owned boundaries.

### F09: Define Identified Match Ingestion

**Depends on:** F03, F06, F08

**Status:** Complete; amended implementation review passed and changes remain uncommitted (2026-07-12)

**Checkpoint evidence (2026-07-12):** Repository inspection found no authoritative competition-period source shared by dedicated-server, client-hosted, and local matches. The current request and game event buffer carry no period field; build information appears only inside `SessionStart.event_data`; Eventun exposes no active competition configuration; and no universal AccelByte session metadata contract is documented. The proposed shared `GetActiveCompetitionPeriod` operation would therefore create a new API, authorization exception, generated Unreal operation, and runtime dependency before the product has defined season ownership or lifecycle. The owner declined that implementation.

**Owner clarification:** A player-facing season, a statistics comparability scope, a retention-oriented telemetry storage segment, and a retention tier are distinct concepts. Their cadence, ownership, historical-detail policy, archive format, and relationships are unresolved. Do not add an active-period API, producer-supplied period id, Eventun period catalog, placeholder legacy period, or period-based partition. This does not remove source/event-type partitioning: the owner reports material query-performance gains from the existing client/server event trees partitioned by event name. The provisional direction is documented in [[../../30_designs/ascent-rivals/eventun-telemetry-lifecycle-plan|eventun-telemetry-lifecycle-plan]].

**Schema and migration evidence (2026-07-12):** The canonical schema and additive post-`t0` production delta now contain one byte-identical marked identified-ingestion DDL block. `event_ingest_batch` records the stable non-nil batch UUID, Eventun-derived client/server source, OAuth client and submitting-player provenance, session/match, bounded nonblank game build, server receipt time, event and match time bounds, a `BIGINT` count of at least two events, and a 32-byte canonical SHA-256. Actor constraints match the accepted authorization boundary: Client submissions require a player and Server submissions are subjectless. `game_event` is one logical relation partitioned first into client/server source subtrees and then into 17 retained non-replay event-type leaves plus a default leaf per source. The canonical tree therefore has 39 relations including both partitioned levels, and predicates prune to one source/type leaf, two same-type leaves when source is absent, or one source subtree. Existing generated payload columns and the useful source-tree/leaf access paths are retained in equivalent batch-oriented indexes without exact duplicate indexes.

PostgreSQL 16 cannot enforce a global event UUID or global `(batch_id, producer_sequence)` key directly on that hierarchy without including every partition key. A compact unpartitioned `game_event_identity` constraint ledger provides the global event primary key and batch-sequence unique key, fixes each event to one batch/source/type/sequence/hash tuple, and is referenced by the partition-compatible payload key. The unpartitioned batch ledger additionally has partial unique indexes for one server observation per `(session_id, match_id)` and one client observation per `(submitting_player_id, session_id, match_id)`. Distinct authenticated client observers may retain separate self-reported views of the same match, but a new batch id cannot create a second accepted observation for the same source identity. `match_artifact` separately records stable artifact identity, optional accepted-batch association, source/actor provenance, session/match, kind, external object key, producer creation and server receipt times, canonical hash, and both artifact-id and external-key conflict constraints. `ReplaySaved` is rejected from `game_event`. Legacy `client_event`, `server_event`, their replay leaves, views, functions, indexes, and runtime queries remain intact. Frozen `migration/t0_migration.sql` remains byte-identical at SHA-256 `82878c3893ed2385c19b1188e4a0e93f7c644e16d51adc7991436fb1281da5ed`; no migration runner or deployment migration was added.

**Contract and behavior decisions (2026-07-12):** Additive, currently unreferenced `MatchIngestEvent`, `MatchIngestRequest/Response`, `MatchArtifactRequest/Response`, kind, and outcome definitions make the future contract reviewable without changing either Event RPC. A batch is one complete match of at least two events with a common session/match, required nonnegative match-id presence even when zero, bounded diagnostic `game_build`, stable non-nil event UUIDs, and required producer sequence exactly `0..N-1` in list order and no greater than PostgreSQL `INTEGER` maximum. It has exactly one `MatchStart` followed by one terminal `MatchEnd`; required producer timestamps are JCS-safe integer Unix milliseconds, timestamps may tie and never reorder sequence; `ReplaySaved` uses the artifact contract. No producer message contains source, trust, period, season, statistics scope, retention segment, or schema version.

F10 will replace `ClientService.Event` with one shared `ClientService.IngestMatch` operation at `POST /v1/match/ingest`, add one shared `ClientService.CreateMatchArtifact` operation at `POST /v1/match/artifact`, and remove `ServerService.Event` without a compatibility copy. Both operations accept either a valid namespaced player subject without a custom permission or an exactly subjectless token with Eventun Server `CREATE`. Eventun derives source from that verified actor class: a player subject is always `client`, even if the principal also has Server permission; only the subjectless Server-authorized mode is `server`; whitespace subjects are rejected. F09 adds no route, RPC, auth rule, or runtime handler. F11 consumes these same ClientService operations in both generated Client and selected GameServer surfaces rather than generating server-specific copies.

Canonical content is SHA-256 over the UTF-8 RFC 8785 JSON Canonicalization Scheme encoding documented in `docs/identified-match-ingestion.md`. The batch projection includes canonical lowercase session UUID, present match id, exact game build, and the ordered complete event projections including stable event id, present sequence, present occurred milliseconds in the exact-integer range 0 through 9,007,199,254,740,991, type, and every present optional field. It excludes the batch idempotency key and all receipt, source/actor, derived-bound/count/status, database-generated, and hash fields. Absent optionals are omitted; explicitly present defaults are retained; structured payloads are recursively canonicalized without Unicode normalization; unknown protobuf fields and non-finite numbers are rejected. Artifact hashing analogously includes present batch association, session/match, numeric kind, bounded external key, and present producer creation time in the same range while excluding artifact id and server-derived metadata. Numeric replay kind 1 maps to exact stored text `replay`.

A new batch returns gRPC success/HTTP 200 with `ACCEPTED`. The same batch id, canonical hash, and exact derived source/client/player provenance returns success/200 with `ALREADY_ACCEPTED`, without another insert or derivation. A different batch id for the same logical-match key also returns `ALREADY_ACCEPTED` and the existing canonical batch id/hash only when content and provenance are equal; differing content or provenance returns gRPC `AlreadyExists`/HTTP 409. Accepted payloads are immutable and the initial API has no producer correction or last-write-wins behavior. A future correction requires a separately approved audited supersession that retains the original acceptance and transactionally rebuilds the one current fact and projection set. Reused persisted event or sequence identity with different ownership or content also returns `AlreadyExists`/409. Malformed or internally duplicated identities, missing presence, sequence gaps, unknown fields, or invalid complete-match shape return `InvalidArgument`/HTTP 400. Acceptance is atomic with no partial merge.

Artifact idempotency resolves both stable artifact id and `(artifact_kind, external_record_key)`. The same kind/key and canonical content/provenance under a different artifact id returns `MATCH_ARTIFACT_OUTCOME_ALREADY_ACCEPTED` with the existing canonical artifact id/hash and performs no insert. A reused artifact id or kind/key with different content or provenance returns `AlreadyExists`/409. These are contract decisions only; the current sender remains at most once and runtime validation/persistence is deferred to F10.

**Legacy conversion decision (2026-07-12):** F15 will exclude replay rows, group server rows by source/session/match, and group client rows by source/submitting-player observer/session/match after proving consistent producer and client-player attribution. The legacy batch UUID projection includes nullable submitting-player identity so deterministic backfill preserves the same logical-match policy as new acceptance. It will derive a pinned UUIDv5 root from the exact standard URL namespace, deterministic batch identities from an exact RFC 8785 projection of that group key, zero-based order by exact Unix millisecond, pinned lifecycle rank, UTF-8 event type, and exact RFC 8785 tie-projection bytes with explicit SQL-null handling, and event identities from an exact batch/sequence/lowercase-content-hash projection. Equal-time order is explicitly reconstructed rather than authoritative. The first usable ordered `SessionStart.clientVersion`, or literal `legacy-unknown`, supplies game build. One manifest-recorded backfill execution timestamp supplies otherwise-unavailable legacy receipt time and is excluded from identities/hashes. Missing/invalid session or match identity, inconsistent attribution, ambiguous lifecycle, non-millisecond timestamp, or replay rows without external keys are quarantined for explicit operator disposition; no synthetic session or period is invented. Replay rows are grouped by artifact kind/external key: equal mapped content and source/client/player provenance coalesce to one deterministic artifact, while conflicting ownership or content quarantines the entire key group to honor the unique external-key constraint. The artifact links to a reconstructed batch when available. F09 performs no production backfill or old-table deletion.

**Verification evidence (2026-07-12):** `./scripts/verify_schema.sh` passed against the immutable pinned PostgreSQL image reporting exact `server_version_num=160014`. It built the complete canonical `a*` through `d*` schema in a networkless, no-published-port, tmpfs-backed disposable container; proved the canonical/t1 marked blocks byte-identical; checked the frozen t0 hash; retained legacy relations; exercised known/default routing, source/type and type-only partition pruning, reviewed leaf/source index ownership, access methods, keys, predicates and definition fragments, rejection of equivalent partition-tree indexes, source/actor/hash/UUID/count/time/sequence constraints, global cross-source event identity, cross-type batch-sequence identity, payload/identity and batch/source foreign keys, replay rejection, nil-player rejection, 2,048-byte accepted and 2,050-byte rejected UTF-8 artifact keys, and artifact identity/external-key/provenance conflicts; then rolled the data tests back and removed its temporary container/image. The owner-approved lack of an authentic disposable post-t0 production baseline remains explicit: `t1_migration.sql` was not executed, and clean/delta dump convergence was not claimed.

`./scripts/verify.sh` passed from its clean temporary workspace with Go 1.26.5, Bun 1.3.9, Node 24.4.0/npm 11.4.2, Buf 1.71.0, oapi-codegen 2.7.2, AccelByte App UI codegen 4.2.2, and the pinned Unreal generator 2026.3.0. Evidence includes protobuf format/build/lint and clean generation/manifest comparison, four identified-ingest descriptor tests, all Go tests, vet, govulncheck 1.6.0 with zero called/imported vulnerabilities and one module-only finding, and the linux/amd64 service build. Current Event RPC types and generated inventories remain Client 68, Admin 60, Server 5, GameServer 15, and Models 73 operations; all 13 Unreal contract tests passed and Swagger output was unchanged. Focused `go test -race -count=1 ./api ./internal/eventun`, shell syntax checks, and `git diff --check` passed. A service-image build passed before the final timestamp-presence correction, but its digest is deliberately not retained as final evidence. The corrective rebuild was in flight when the WSL connection was lost; after reconnection the Docker daemon was unavailable, and the owner explicitly asked to skip further Docker build/run checks to avoid the memory cost. The final linux/amd64 Go build remains covered by the canonical verifier.

**Contract-gap correction evidence (2026-07-12):** The canonical and production-delta DDL blocks remain byte-identical after adding the server and client-observer logical-match unique indexes, and the guarded production-delta postcondition requires both indexes. Focused SQL cases now require equal and conflicting second server batches to hit `event_ingest_batch_server_logical_match_key`, require an equal second batch from the same client observer to hit `event_ingest_batch_client_observer_logical_match_key`, permit a distinct client observer for the same session/match, and require equal artifact content with a different artifact id to hit the external-key identity. The descriptor test additionally proves that the current two Event RPCs remain unchanged and neither future shared operation is exposed before the runtime cutover. `MatchIngestResponse.batch_id` and `MatchArtifactResponse.artifact_id` document that equal logical-key duplicates return the retained canonical identity.

The corrected `./scripts/verify.sh` passed with the same pinned versions and unchanged Client 68, Admin 60, Server 5, GameServer 15, and Models 73 operation inventories. Protobuf format/build/lint, clean generation and manifest comparison, four identified-ingest descriptor tests, 13 Unreal composition tests, all Go tests, module-tidy stability, vet, govulncheck with zero called/imported findings and one module-only finding, and the linux/amd64 build passed. Focused `go test -race -count=1 ./api ./auth ./internal/eventun`, repeated descriptor tests, shell syntax checks, canonical/t1 block comparison, frozen-t0 SHA-256 verification, and staged/unstaged `git diff --check` passed. `./scripts/verify_schema.sh` stopped at its intentional preflight because Docker is not running; it was not started under the owner's standing memory constraint. The new PostgreSQL constraints and focused cases therefore have static parity evidence but still require execution in the pinned PostgreSQL 16.14 disposable container when Docker is next available.

**Review result (2026-07-12):** Read-only follow-up review found no remaining implementation findings. The server and client-observer partial unique indexes close the logical-match duplication gap while preserving separate client observations; the actor constraint makes the nullable client-observer index key effective. The documented future shared ClientService operations provide one network operation per behavior, define player-versus-subjectless-server authorization and source derivation, and leave the current RPC surface unchanged until F10. Artifact external-key collisions now have deterministic equal-content and conflicting-content behavior even when the submitted artifact id differs. The owner-deferred PostgreSQL execution noted above remains residual verification evidence to collect before applying the new delta or cutting over runtime ingestion; it does not block approval of the F09 contract and schema design.

**Changed files:** `README.md`; `docs/identified-match-ingestion.md`; `migration/a0_create_init.sql`; `migration/t1_migration.sql`; `proto/ikigai/eventun/v1/event.proto`; `scripts/README.md`; `scripts/database.sh`; `scripts/generated.sha256`; `scripts/identified_ingest_contract.test.ts`; `scripts/schema_contract.sql`; `scripts/verify.sh`; `scripts/verify_schema.sh`; the foundation/API simplification review; and this task record. There are no runtime Go, service signature, route, dependency, legacy query, product behavior, authorization, game-client, App UI, Unreal, Ascentun, SQL seed, or frozen-t0 changes.

Implemented period-neutral identified ingestion:

- [x] Inspect current Eventun and game-client period/configuration sources and stop rather than inventing one.
- [x] Separate product season, statistics scope, storage segment, and retention-tier terminology.
- [x] Approve resuming the period-neutral identified-ingest reset while preserving source/event-type partition pruning.
- [x] Add `event_ingest_batch`, one logical source-tagged `game_event` hierarchy that preserves client/server and event-type partition pruning, and `match_artifact` schema.
- [x] Include stable batch id, event id, contiguous sequence, source, game build, canonical payload hash, actor attribution, and receipt metadata.
- [x] Derive immutable source from the verified player-versus-subjectless-Server actor class on one shared operation; never accept a producer-selected trust classification or duplicate an operation for auth differences.
- [x] Reconcile global event identity with PostgreSQL 16 partitioned-table uniqueness requirements without discarding the useful partition keys.
- [x] Enforce one server logical-match observation and one client observation per authenticated player, while permitting distinct client observers of the same match.
- [x] Define same-content duplicate and conflicting-content responses.
- [x] Define equal-content artifact-key behavior when the submitted artifact id differs from the retained artifact id.
- [x] Define synthetic legacy batch/event identity and replay-artifact backfill rules without payload schema versions or a synthetic period.

**Done when:** after explicit approval to resume, the period-neutral schema and API contract are reviewed together and support idempotent acceptance, deterministic ordering, source attribution, later statistics classification, and later storage segmentation.

### F10: Implement The Match-Batch API And Event Domain

**Depends on:** F09

**Status:** Complete; implementation review passed and changes remain uncommitted (2026-07-12)

- [x] Replace `ClientService.Event` with the one shared `ClientService.IngestMatch` operation at `POST /v1/match/ingest`; remove `ServerService.Event` without a compatibility copy.
- [x] Add the one shared `ClientService.CreateMatchArtifact` operation at `POST /v1/match/artifact`; do not add a ServerService counterpart.
- [x] Authorize both shared writes for either a namespaced player subject or an exactly subjectless token with Server `CREATE`; derive immutable client/server source from that verified actor class.
- [x] Validate one start, one end, envelope identity, ids, contiguous order, and supported event shapes.
- [x] Insert batch and events atomically; resolve batch-id and logical-match uniqueness races; return the retained batch id for equal content under a different id.
- [x] Resolve artifact-id and kind/external-key uniqueness races; return the retained artifact id for equal content under a different id.
- [x] Reject conflicting batch, logical-match, event, sequence, artifact, or external-key identity; do not add producer correction or last-write-wins behavior.
- [x] Move event code into the `event` package and delete the old implementation.
- [x] Keep automatic sender retry disabled until the contract is deployed and verified.

**Done when:** shared-operation auth/source, ingest, logical-match duplicate/conflict, artifact duplicate/conflict, malformed-envelope, and rollback tests pass without auth-only API copies.

**Completion evidence (2026-07-12):** `ClientService` now exposes `IngestMatch` at `POST /v1/match/ingest` and `CreateMatchArtifact` at `POST /v1/match/artifact`; the two legacy Event RPC declarations and messages are removed and `ServerService` has no ingestion or artifact copy. The total served inventory remains 133 operations, redistributed as Client 69, Admin 60, and Server 4. Authorization tests prove a namespaced nonblank player uses the client source without a custom permission, an exactly subjectless caller requires Server `CREATE` and uses the server source, a player is never upgraded to server source, and whitespace subjects fail closed. The generated GameServer consumer contract selects the ten shared reads and these two shared writes alongside all four Server operations; no Ascent Rivals game-client file was changed.

The new top-level `event` package validates required presence, nil/malformed and request-duplicate UUIDs, exact contiguous sequence, JCS-safe time bounds, one ordered start and terminal end, replay exclusion, finite structured data, typed generated-field inputs, and unknown protobuf fields before opening a transaction. It uses the pinned Cyberphone RFC 8785 reference implementation for the documented projections and SHA-256 vectors. One explicitly owned transaction inserts the batch, global identity ledger, and partitioned payload rows; uniqueness failures roll back before reading the committed batch-id or logical-match winner. Exact canonical content and source/client/player provenance returns the retained identity and `ALREADY_ACCEPTED`; conflicting batch, logical-match, event, sequence, artifact-id, or artifact-key identity returns `AlreadyExists`. Artifact insertion applies the same rollback-then-resolve pattern and maps an invalid accepted-batch association to `FailedPrecondition`. Only newly committed server matches reach the existing asynchronous best-effort post-ingest sinks. Automatic sender retry, fact derivation, producer changes, legacy conversion, and old-table removal remain deferred.

`./scripts/verify.sh` passed with Go 1.26.5, Bun 1.3.9, Node 24.4.0/npm 11.4.2, Buf 1.71.0, oapi-codegen 2.7.2, AccelByte App UI codegen 4.2.2, and Unreal codegen 2026.3.0. Evidence includes protobuf formatting/build/lint, clean protobuf/Gateway/Swagger and integration generation with manifest parity, four identified-ingest descriptor tests, 13 Unreal composition tests, all Go tests, module-tidy stability, vet, govulncheck 1.6.0 with zero called/imported findings and one module-only finding, and the linux/amd64 Eventun build. Focused `go test -race -count=1 ./event ./auth ./api ./integration/cardanoun ./internal/app ./internal/eventun`, focused vet, shell syntax checks, frozen-t0 SHA-256 verification, canonical/t1 ingestion-block parity, and staged/unstaged `git diff --check` also passed. The canonical contract reports Client 69 operations/148 definitions, Server 4/19, GameServer 16/156, and Models 73/156. Docker was not started under the owner's memory constraint, so the PostgreSQL 16.14 schema contract and service-image build were deliberately not rerun; the F09 executable-schema evidence gap remains. No file was staged or committed.

**Unreal SDK prerequisite follow-up (2026-07-12):** After the owner started Docker, `scripts/make_unreal.sh` regenerated the ignored `eventun-unreal/` tree and `eventun-unreal.zip` with the pinned `accelbyte/extend-codegen-cli:2026.3.0@sha256:15f77da4a61f131940e30bf692a917e648d40eb6ba44c6023234707af05dccf1` image. `verify-generated`, direct byte comparisons, and consumer-spec verification passed with the same Client 69/148, Server 4/19, GameServer 16/156, and Models 73/156 inventories. Both Client and GameServer wrappers contain `ClientServiceIngestMatch` and `ClientServiceCreateMatchArtifact`; generated files contain no `ClientServiceEvent`, `ServerServiceEvent`, legacy event request, or `AEvent` model. The archive SHA-256 is `9fd3083b3479f7184ad735d7d53884f978ff6ce8746e001e46adee20ca89721b`. Exactly five generated wrapper/model files and three split specifications were copied byte-for-byte into the existing Ascent Rivals default changelist. No authored game-client file was edited and no Unreal compile was attempted; those remain F11 coder work. PostgreSQL schema execution and the service-image build were not part of this follow-up.

**Unreal optional-presence correction (2026-07-12):** Game-client review found that the generated wrappers serialize absent artifact `batch_id` and per-event `player_id` as empty strings. A temporary field-name-specific Unreal operation-template workaround was rejected because it would fork third-party generator behavior and could silently become stale when either the contract or template changes. The generic pinned template is restored. Eventun now applies one narrow request-boundary normalization before validation, canonical hashing, and persistence: only `MatchIngestEvent.player_id == ""` and `MatchArtifactRequest.batch_id == ""` map to absence. Focused tests prove each empty form produces nil stored identity and exactly the same canonical hash as omission; whitespace, malformed UUIDs, and nil UUIDs remain invalid. Required numeric zero values such as `match_id`, `sequence`, and timestamps retain normal presence semantics. `./scripts/verify.sh` passed with all Go tests, vet, govulncheck, clean generation/manifest comparison, and the linux/amd64 build. `./scripts/verify.sh unreal` passed 13 composition tests, two deterministic pinned-image generation runs, generated-output verification, and byte comparison. The generic-template archive supersedes both earlier artifacts at SHA-256 `061ad1bc4f75f29ef50c0ce05c11558797831ca188ebe0025bfbac2e25902eb4`. The two raw-UStruct generated implementation files and three description-updated consumer specifications were copied byte-for-byte into the existing Ascent Rivals default changelist; the generated headers and model file were already identical and left untouched. No authored game file was edited and no Unreal compile was attempted during this correction.

**Review result (2026-07-12):** Read-only implementation review found no remaining findings. The shared authorization policy derives client versus server provenance from verified player versus exactly subjectless Server-`CREATE` actors; request validation and canonical hashing match the approved contract; batch, identity-ledger, payload, and artifact writes have explicit transaction ownership; and uniqueness failures roll back before resolving retained identities and equal-versus-conflicting provenance. Generated Client, Server, GameServer, Models, Gateway, and Swagger inventories match the intended nonduplicated API placement. The review relied on the worker's reported verification and did not rerun builds, generation, tests, linters, vulnerability checks, or Docker.

**Deployment boundary:** F10 is an intermediate coordinated-cutover state, not a standalone product release. It removes both legacy Event RPCs and writes only the replacement relations, while current progression job creation and existing career, leaderboard, match-history, insight, and gauntlet reads still depend on legacy event storage. Do not deploy the new producer/backend cutover as production behavior until F11 through F15 have supplied the producer update, facts, current-domain migration, representative output comparison, and final cleanup. No compatibility dual-write is required.

### F11: Update The Game Client Event Producer And Replay Association

**Depends on:** F06B, F10

- [x] Consume the regenerated Eventun Client, GameServer, and Client/Server Models surfaces in the Ascent Rivals game-client repository; keep the same shared ClientService ingest and artifact operation ids rather than generating ServerService copies.
- [x] Generate and retain a batch id per active match.
- [x] Generate an event id at record time and stable producer sequence for every event.
- [x] Populate game-build context; do not add a season or statistics-scope field until its ownership and distribution are approved.
- [x] Retain the same request identity if bounded retry is enabled later.
- [x] Replace the late one-event `ReplaySaved` submission with `ClientService.CreateMatchArtifact` at `POST /v1/match/artifact`.
- [ ] Manually test dedicated-server and local/client submission paths.

**Implementation status (2026-07-12):** Ascent Rivals now records one complete-match envelope from `MatchStart` through terminal `MatchEnd`, assigns stable batch/event identities and zero-based sequences at record time, omits invalid player UUIDs, and uses `UHGGameInstance::GetBuildVersion()` for game-build context. Both local/client and dedicated-server surfaces call the shared `ClientServiceIngestMatch` and `ClientServiceCreateMatchArtifact` operations. Accepted batch ids are retained by session/match and linked to finalized replay artifacts only after `ACCEPTED` or `ALREADY_ACCEPTED`; otherwise the optional batch link is omitted. The generated Unreal transport represents either omitted optional UUID string as `""`; Eventun's documented request-boundary normalization maps only event `player_id` and artifact `batch_id` empty strings to absence, so the game code does not use nil-UUID or negative-number sentinels, while required `match_id = 0` and `sequence = 0` remain valid. The legacy Event RPC models/calls and authored `ReplaySaved` event were removed. Win64 Development builds succeeded for `AscentRivalsEditor`, `AscentRivals`, and `AscentRivalsServer`. Backend-dependent manual submission and acceptance testing remains pending; no Docker or backend smoke environment was started.

**Canonical response identity:** `ACCEPTED` and `ALREADY_ACCEPTED` success is determined from the outcome plus a valid response UUID, not equality with the submitted UUID. Eventun may return a previously retained canonical batch or artifact id for an equal logical request; Ascent Rivals retains the canonical response batch id for replay linkage and logs both submitted and canonical identities.

**Done when:** Eventun accepts complete matches from both paths, replay records associate independently, and no legacy request is emitted.

### F12: Rework Narrow Facts And Projection Inputs

**Depends on:** F10

**Status:** Complete; corrected revised implementation is uncommitted and awaiting review (2026-07-13)

- [x] Retain `event_ingest_batch`, `game_event_identity`, the source/event-type `game_event` partition tree, and `match_artifact` as the immutable identified telemetry layer.
- [x] Keep and narrow `match_fact`, `heat_fact`, `match_player_fact`, and `heat_player_fact` to stable context, terminal results, proven loadout dimensions, and values required by current career, record, progression, qualification, and team work.
- [x] Remove the one-row-per-event wide `lap_fact` and `checkpoint_fact`. Add lap count, total valid lap time, best valid lap time, and winning source event identity at heat/player scope; leave detailed lap/checkpoint segment metrics, coordinates, and tags in raw partitions.
- [x] Keep `progression_metric_fact` as an idempotent semantic contribution ledger. Retain bounded JSONB dimensions where they remove sparse columns, but remove the dimensions GIN unless F13 demonstrates an implemented containment query that needs it.
- [x] Derive the narrow facts through bounded PostgreSQL functions in the accepted-batch transaction and preserve explicit client-reported versus dedicated-server provenance.
- [x] Retain one current fact set per batch. Remove parallel fact revisions and selected-revision joins; a rebuild transaction replaces the batch's current facts. Batch-level status or current-projector metadata may remain only where it materially supports repair.
- [x] Keep `single_player_mode` nullable and store only a nonblank canonical game enum name of at most 64 bytes, such as `None` or `TimeTrial`; do not infer it from `race_mode` or add boolean compatibility.
- [x] Use `MatchStart` as authoritative course context because a course cannot change between heats; reject conflicting present heat course metadata rather than allowing one match to derive multiple courses.
- [x] Reconcile fact extraction with the actual Unreal payload shape. The emitted per-player `PlayerHeatStart` is the sole loadout snapshot for that player/heat; retain its nested item-ID slots/augment slots and do not duplicate it onto PlayerKill, PlayerDied, or other events. Defer item ID versus SKU changes. Preserve medal-count and weapon-specific fields used for their own purposes.
- [x] Preserve reported podium state separately from placement-derived policy. Missing optional placement and podium values must not produce null for a non-null fact or roll back an otherwise valid batch.
- [x] Validate every selected typed payload field before persistence. Projection functions raise private SQLSTATE `P2001` only for deliberate producer-data rejection; map only that state to `InvalidArgument`, leaving class 22, ordinary constraints, and unexpected projector/storage failures as `Internal`.
- [x] Treat a supplied nonnegative `heat` as retained ambient context unless its event type is explicitly heat-scoped. Derive boundaries only from HeatStart/HeatEnd; require the approved heat-scoped events to fall within the matching nonoverlapping pair, while allowing global MatchStart/PlayerMatchEnd/MatchEnd heat context outside the interval without creating or counting a heat. Missing, duplicate, misordered, overlapping, and escaped boundaries cannot produce the current/canonical fact graph.
- [x] Enforce or contract-test that every retained source event identity belongs to the fact's batch, source, and expected event type.
- [x] Replace the 18-event fixture with three-heat 5-human/11-bot and maximum-normal 16-human matches at 4,681 events, plus a separately labeled 32-human/9,362-event synthetic stress case. Alternate raw-only and projected runs and report insertion, projection, commit, query, WAL, heap/TOAST/index, buffers, and row ratios on PostgreSQL 16.14 with one CPU and 2 GiB RAM. Treat the sample's 3.09 heats/match only as workload evidence.

**Rejected implementation checkpoint (2026-07-12):** The first F12 implementation added revision-keyed `match_fact`, `heat_fact`, `match_player_fact`, `heat_player_fact`, wide one-to-one `lap_fact` and `checkpoint_fact`, and `progression_metric_fact`. Its disposable 18-event/two-player contract passed and reported a 7.605 ms rebuild, but production currently averages approximately 4,681 server events per match. A three-reviewer database, product-query, and architecture review on 2026-07-13 rejected the universal fact shape: it duplicated high-cardinality telemetry synchronously, did not bound the measured leaderboard/career/gauntlet reads, retained revisions without immutable projector ownership, lost time-trial classification, and contained podium and validation defects. The rejected uncommitted machinery was replaced by the revised implementation below.

**Revised implementation evidence (2026-07-13):** Identified ingestion and its client/server plus event-type partitions remain intact. The accepted transaction now calls `derive_match_facts(batch_id)` and retains exactly one current graph: one `match_fact` per batch, one `heat_fact` per batch/zero-based heat, one `match_player_fact` per batch/player, one `heat_player_fact` per batch/heat/player, and idempotent `progression_metric_fact` contributions keyed by batch/source event/metric/dimensions. `rebuild_match_facts(batch_id)` deletes the match root and cascading children and recreates them in one transaction; two consecutive rebuilds matched the original five-relation row/fingerprint set. All fact and batch revision/status/error fields, revision arguments/joins, wide `lap_fact`/`checkpoint_fact`, progression-dimensions GIN, synthetic weapon/part SKU extraction, and typed speed/agility/combat/segment copies were removed.

`MatchStart` now owns course context, and defensive SQL rejects any present conflicting heat unique code/code/version/lap value. Nullable `single_player_mode` is bounded text copied only as the explicit canonical enum name; no boolean compatibility or race-mode inference remains. Match-player facts preserve nullable `reported_podium_finish`; explicit false and missing remain distinct even for placements 1-3, while only explicit true contributes `podium.count`. Heat-player facts read the one emitted per-player `PlayerHeatStart` loadout snapshot (existing item-ID key/slot/augment-slot/version plus weight/value fields) and retain positive-lap count, total, best time, and deterministic winning PlayerLap identity ordered by time/sequence/event id. Later events do not carry copied loadout state; item ID versus SKU work remains deferred. Medal contributions read the actual `medalCounts` name/parent/count shape and derive augment state from the parent; kill contributions retain emitted `weaponItemId` for their separate purpose.

Go now distinguishes retained ambient heat from heat-scoped semantics before persistence. HeatStart/HeatEnd alone discover the complete, nonoverlapping intervals. HeatStart, HeatEnd, AscensionStart, PlayerHeatStart, PlayerHeatEnd, PlayerCheckpoint, PlayerLap, PlayerDied, PlayerRespawn, PlayerKill, PlayerGate, and SlalomGate require a nonnegative heat; every listed non-boundary event must be strictly inside its matching pair. Global events may retain nonnegative heat outside that interval without creating, counting, or requiring a boundary. PostgreSQL repeats the same exact list and interval rules for rebuild/direct-maintenance safety, makes heat-fact end boundaries required, and filters every raw projector query by the accepted batch's `source_kind` so the other partition subtree can be pruned. The projector uses private SQLSTATE `P2001` for deliberate producer-validation failures; only that state maps to `InvalidArgument`. Class 22 errors, ordinary `23514` constraints, and unexpected projector/storage defects map to `Internal`. Focused Go and PostgreSQL tests cover the actual Unreal MatchStart heat-0 and terminal final-heat shape, retained global heat, AscensionStart missing/negative/escaped heat, expected and unexpected error classifications, missing/duplicate/misordered/escaped/overlapping boundaries, loadout ownership, server/client source isolation, zero values, optional results, explicit true/false/missing podium, two same-course heats, conflict rollback, loadout/medal shapes, lap aggregate/tie behavior, exact source event batch/source/type provenance, bounded dimensions, current-graph rebuild, and full atomic rollback.

The corrected PostgreSQL 16.14 harness uses one CPU, 2 GiB RAM, and ten alternating raw-only/projected samples per workload. The provided 100,000-row sample supplied workload evidence only: 108 HeatStart rows across 35 observed matches (3.09/match), median 16 participants per heat, and 900 bot versus 528 human PlayerHeatStart rows. The representative 5-human/11-bot case (bots omit `player_id`) and maximum-normal 16-human case each contain three heats and 4,681 events; the explicitly synthetic 32-human stress case contains three heats and 9,362 events. They include realistic core/augment item-ID arrays, medal entries, lifecycle rows, and production-weighted checkpoint/death/respawn/kill counts.

The corrected harness runs diagnostic fact-row counts only after the measured commit interval and compares equivalent raw/fact per-player/per-heat valid-lap count, total, and best-time results. Mixed raw-only/projected p50/p95 raw insertion was 131.169/164.758 versus 129.782/163.955 ms; projected derivation was 42.018/55.465 ms and projected committed time was 231.129/282.180 ms. It produced 122 facts (2.606%) with 8,201,928 median WAL bytes. Sixteen-human insertion was 124.773/151.001 versus 126.568/167.887 ms; derivation was 62.024/75.876 ms and projected committed time was 276.690/348.895 ms. It produced 375 facts (8.011%) with 8,438,796 median WAL bytes. Synthetic 32-human insertion was 403.599/764.522 versus 433.660/654.676 ms; derivation was 104.120/183.690 ms and projected committed time was 615.083/813.962 ms. It produced 743 facts (7.936%) with 16,971,032 median WAL bytes. Warm raw/fact query p50 was 0.038/0.009 ms mixed, 0.071/0.016 ms normal-16, and 0.138/0.029 ms synthetic-32.

Per projected match, fact heap/index allocation was about 27,853/27,034 bytes mixed, 90,112/72,909 bytes normal-16, and 181,043/150,733 bytes synthetic-32, with no fact TOAST. Across 60 measured matches, peak raw heap/index growth was 269,164,544/171,835,392 bytes and fact heap/index growth was 2,990,080/2,506,752 bytes. Representative normal-16 raw-only versus projected shared hit/read/dirtied/written buffers were 127,631/19/682/1,094 versus 168,524/15/689/960, with 8,127,119 versus 8,374,772 WAL bytes. Synthetic-32 was 255,096/44/1,396/1,895 versus 321,161/32/1,400/2,519, with 16,328,838 versus 16,758,881 WAL bytes. The disposable Docker filesystem was not capacity- or IOPS-shaped to the Azure tier's 32 GiB storage, so these are local latency, buffer, WAL, and allocated-size measurements rather than durable Azure latency evidence.

`./scripts/verify.sh` passed with Go 1.26.5, Bun 1.3.9, Node 24.4.0/npm 11.4.2, Buf 1.71.0, oapi-codegen 2.7.2, AccelByte App UI codegen 4.2.2, Unreal codegen 2026.3.0, all Go tests, generation/manifest parity, formatting, tidy stability, vet, govulncheck 1.6.0 (zero called/imported findings; one module-only finding), and the linux/amd64 Eventun build. `go test -race -count=1 ./event`, `go vet ./event`, shell syntax, and `git diff --check` passed. `./scripts/verify_schema.sh` passed with the frozen `t0_migration.sql` SHA-256 `82878c3893ed2385c19b1188e4a0e93f7c644e16d51adc7991436fb1281da5ed`, exact canonical/`t1_migration.sql` marked-block parity, PostgreSQL 16.14 initialization, source/provenance and rebuild contracts, expected `P2001` versus unexpected `23514` behavior, actual generated-Unreal ambient/global heat acceptance, explicit `P2001` rejection of negative ambient heat, the aligned AscensionStart and other heat-scoped boundary cases, raw/fact lap-summary equality, and all 60 interleaved benchmark samples. The owner-provided `production-sample.csv` remained byte-identical at SHA-256 `ecb34ea9ed573fb77d978b8004de695df24faa25c82c7330f6041019c2e8ecd0` and remains outside this change. Current product reads, materialized views, and separately owned game-client production work were not changed; F13, F14, F15, teams, and unrelated refactors were not started. All changes remain unstaged and uncommitted.

**Production-baseline advancement (2026-07-13):** The owner confirmed the frozen `t0_migration.sql` was deployed to production, so it was removed. The pending former `t1_migration.sql` is now stable `migration/migration.sql`, based directly on current production. Development fixtures were independently renumbered `t0_seed_courses.sql` through `t3_seed_teams.sql`, and the pg_cron schedule is now `d3_schedule_refresh_views.sql`. The canonical `d3` file safely no-ops without pg_cron, while the guarded operational mode reapplies it after provisioning. Production-delta confirmation is `--confirm-disposable-production-baseline=<target-fingerprint>`. Repository instructions, guarded database commands, README guidance, and schema verification use the new names; historical evidence above records the names that existed when those earlier checks ran.

**Projection boundary:** F12 supplies narrow, replayable contributions. It does not yet replace the current leaderboard, career, gauntlet, or insight consumers and does not remove the existing materialized views. F14 adds incremental serving projections and removes materialized-view dependencies only after parity.

**Done when:** one accepted batch and one rebuild produce the same current narrow facts without parallel revisions; detailed lap/checkpoint data remains queryable from raw partitions; malformed selected fields return the documented client error; and production-shaped measurements demonstrate an acceptable synchronous ingest budget.

### F12G: Add Explicit Play Context To The Game Producer

**Owner:** Ascent Rivals game-client coder

**Depends on:** F12 accepting nullable `MatchStart` play context

- [x] Add single-player mode or an equivalent explicit play-context field to the authored `MatchStart` event shape.
- [x] Populate it from the authoritative session entity for local/client and dedicated-server recording paths while preserving the separate race-mode field.
- [x] Verify time trial emits `singlePlayerMode = TimeTrial` even though `raceMode = Classic`; cover other current single-player modes and ordinary multiplayer `None` behavior.
- [x] Preserve the complete-match envelope, canonical request hashing behavior, generated Eventun transport, and current artifact association.

**Game-client implementation evidence (2026-07-13):** Authored `FHGMatchStart_EventData` now serializes `singlePlayerMode`, and the shared race-server producer constructs both `raceMode` and `singlePlayerMode` from the authoritative session entity through the existing `SG::EnumToString` utility. The focused `AscentRivals.Eventun.MatchStart.SinglePlayerMode` automation test passed for `None`, `Simulator`, `Training`, `CareerCup`, `TimeTrial`, `Scrimmage`, and `Slalom`, with `raceMode = Classic` held independently; this proves ordinary multiplayer emits the explicit string `None` and time trial emits `TimeTrial`. Win64 Development builds passed for `AscentRivalsEditor`, `AscentRivals`, and `AscentRivalsServer`. The change is confined to the authored event shape/conversion, the MatchStart producer, and its focused test; generated Eventun transport, complete-match identity/hash/sequence handling, artifact association, HeatStart loadout shape, and weapon-specific event fields remain unchanged.

**Done when:** newly recorded complete-match batches let Eventun distinguish time trial, career/local modes, and ordinary multiplayer without `SessionStart` or race-mode inference.

### F13: Harden Progression Work And Move It To Facts

**Depends on:** F12

- [x] Replace raw-event rereads with normalized progression metric facts.
- [x] Make contributions idempotent by source fact.
- [x] Keep direct SQL aggregates only where their input is explicitly bounded; otherwise maintain current counters as idempotent incremental projections from the contribution ledger. Do not introduce periodic full refresh.
- [x] Add row leases, `SKIP LOCKED`, bounded backoff, maximum attempts, and terminal/dead-letter state to progression jobs.
- [x] Keep expensive goal evaluation and external reward delivery in workers.

**Eventun implementation evidence (2026-07-13):** Identified server ingestion now enqueues one career `match_ingest` job per distinct eligible fact player after `derive_match_facts` and inside the same acceptance transaction. Jobs carry `source_batch_id` and use batch/player/scope/trigger identity; client facts never enqueue progression. `player_progression_counter_contribution` records the exact batch, source event, metric, JSONB dimensions, player, scope, policy, value, and occurrence time. Its exact primary key plus `ON CONFLICT DO NOTHING` means only newly inserted facts increment exact-JSONB counters, including under concurrent application. The deferred, non-cascading source-fact foreign key now covers the complete copied source tuple, including player, value, and occurrence time. Deterministic rebuilds retain equal ledger identity, while repairs that change any contributed attribution/value/time fail until the derived contribution is deliberately reconciled.

Every claimed job fences its own row and then locks the durable player row before applying facts, rebuilding challenge scopes, evaluating goals, or creating completion/reward records. Career processing selects only that job's server `source_batch_id`; challenge reconstruction deletes and rebuilds one player/scope atomically from server facts in the explicit half-open period window. The occurrence-window query uses `(source_kind, player_id, occurred_at)` so metric is filtered after PostgreSQL reaches the bounded player history. The legacy `server_event`, `server_heat_start`, and `server_player_heat_start` progression readers, loadout/SKU inference, dimensions hash, JSONB GIN index, and dedicated raw-progression indexes were deleted.

Active definitions exactly match emitted fact dimensions and use `weapon_item_id` without SKU inference. The Extend App UI now enables the weapon selector for `weapon_item_id` and persists the selected catalog `itemId`; it no longer authors `weapon_sku` or `part_sku`. The production delta retires a pre-alpha source goal when its latest published snapshot still uses either legacy SKU dimension. It expires every active assignment from that retired source, including assignments to older compatible snapshots, and also expires active assignments to any other incompatible snapshot. Ordinary Admin goal archival now establishes the same invariant transactionally by retiring the source and expiring every active assignment across all of its published snapshots. Assignment candidate selection holds a source-goal row lock through materialization, so concurrent archival either observes and expires the new assignment or makes the source ineligible before selection completes. Assigned-challenge evaluation holds the same source-goal lock through completion, reward creation, and worker commit, so archival waits for a worker that already selected the assignment. The assignment completion update additionally requires `status = 'active'` and exactly one affected row; failure aborts the worker transaction and rolls back completion and reward writes. Immutable published snapshots, completed assignments, completions, and reward records are retained. The deployment explicitly requires Eventun and its schedulers to be quiescent and takes transaction-scoped exclusive locks before clearing jobs, counters, and incomplete progress. Completed progress is retained, excluded from career reevaluation, and protected by immutable upserts.

Progression workers claim one due or lease-expired job immediately before each execution in a short `FOR UPDATE SKIP LOCKED` transaction, issue a fresh UUID lock token, lease for two minutes, and increment attempts once. Exhausted candidates use their own `FOR UPDATE SKIP LOCKED` selection, so a locked terminal row cannot block unrelated claims. Success and retry/dead-letter transitions are token-fenced. Retries use exponential backoff from five seconds capped at five minutes, with a five-attempt terminal `dead_letter`; public match-progression summaries report terminal jobs as `failed`. Goal evaluation and reward-record creation remain in the database worker transaction, while external reward fulfillment remains in its existing separate prepare/call/finalize flow with no database transaction held across the external call.

**Eventun verification evidence (2026-07-13):** `go test -count=1 ./event ./internal/eventun`, `go test -race -count=1 ./event ./internal/eventun`, and `go vet ./event ./internal/eventun` passed. Focused archive tests prove all active assignments are selected by source goal, expiration failure prevents success, and both assignment creation and completion selection hold the archival row lock. Completion tests prove the assignment update is active-only and treats a zero-row result as `FailedPrecondition`. `bun test scripts/progression_contract.test.ts` passed seven review-focused source/migration/UI contracts, including the single-transaction Admin archive boundary and guarded challenge completion. `./scripts/verify.sh` passed formatting, pinned generation/diff checks, all Go and Bun tests, vet, govulncheck (zero reachable or imported-package vulnerabilities; one module-only finding), and the linux/amd64 Eventun build. `./scripts/verify.sh appui` passed deterministic regeneration of 343 files, lint, production build, and production dependency audit with zero vulnerabilities.

`./scripts/verify_schema.sh` passed canonical/production-delta DDL and function parity, PostgreSQL 16.14 schema contracts, compact-fact rebuild contracts, fact-progression idempotency/server-only/distinct-scope/bounded-rebuild contracts, repair rejection for a changed contributed fact tuple, a two-session same-batch contribution race, and a real two-session/two-job race using distinct source batches. The distinct jobs produced three source contributions, a combined `match.completed=2` counter, exactly one completion, exactly one reward bundle, two succeeded jobs, and completed progress at `2/2`. A separate two-session worker/archive regression observed archival blocked on the selected challenge's shared source-goal lock; the worker committed one completion and reward, then archival retired the source while leaving the assignment completed. It also extracted and executed the exact marked legacy-dimension cutover from `migration.sql`: a source with an older compatible assigned snapshot and a latest incompatible snapshot became retired, its active older assignment became expired, and both published snapshots remained. The existing 1-vCPU/2-GiB three-heat benchmark also passed. `git diff --check` and shell syntax passed, progression-source searches found no legacy raw event/heat/loadout reads, and all handwritten Go files remain below 1,200 lines. All work remains unstaged and uncommitted; F14 was not started.

**Done when:** retries cannot double-count, permanently failing jobs do not retry hot, and existing progression tests pass against fact-backed inputs.

### F14: Add Incremental Serving Projections And Cut Over Reads

**Depends on:** F12, F12G, F13

- [ ] Add one incrementally maintained player/course record row per source, record category, course, and player, retaining the winning source fact/event identity and using a B-tree order that serves top-N reads directly.
- [ ] Add player and player/course career rollups containing mergeable sums, counts, and minima; derive averages at read time.
- [ ] Add one gauntlet match contribution per player/match/qualifier plus a retained best-sequence projection with the selected source match identities. New in-order matches evaluate only the new trailing window; late or rewritten input triggers targeted player/qualifier recomputation.
- [ ] Update simple projections transactionally with accepted facts when representative ingest measurements permit. Otherwise use one idempotent immediately queued projector with an explicit freshness target, watermark, retry, and repair path; do not use periodic full refresh as the normal update mechanism.
- [ ] Move career and leaderboard reads to their projections. Move match-history lists to narrow facts, but retain batch-local raw reads or a purpose-built snapshot for full match summaries, player discovery, bot rows, and detailed insights.
- [ ] Preserve `single_player_mode` semantics before moving time-trial records or insights. Do not infer time trial from `race_mode`.
- [ ] Move gauntlet qualifier scoring to incremental contributions and retained best sequences, then publish immutable cutoff snapshots.
- [ ] Preserve and apply each product surface's explicit accepted-source policy; do not silently merge client-reported and dedicated-server facts as equally authoritative.
- [ ] Apply an approved statistics scope to comparisons and public records only if that separate lifecycle decision has been completed; do not introduce `competition_period_id` by default.
- [ ] Compare representative old and new outputs, query plans, cold/warm latency, and update freshness; explain intentional differences.
- [ ] Remove the eight leaderboard and four gauntlet native materialized views and their hourly refresh procedure only after incremental replacements pass parity.

**Done when:** player-facing records, career summaries, and gauntlet standings update incrementally without hourly refresh delay; authoritative cutoff remains immutable; and each remaining raw-event read is deliberately batch-local or diagnostic rather than an accidental lifetime scan.

### F15: Complete Event Cutover And Foundation Cleanup

**Depends on:** F11, F14

- [ ] Backfill production rows with synthetic batch, event, sequence, artifact, narrow fact, and serving-projection data; classify historical statistics only if an approved scope model exists.
- [ ] Validate counts, source coverage, and representative outputs before destructive cleanup.
- [ ] Remove the duplicated legacy `server_event`/`client_event` logical APIs and obsolete SQL only after the replacement parent and equivalent source/event-type partitions are populated, representative query plans are compared, and no material regression is found.
- [ ] Finish extracting touched race, progression, insight, and gauntlet code and remove the remaining `internal` tree.
- [ ] Run the full manual release and smoke-test checklist.

**Done when:** the canonical schema contains only the replacement model, Eventun and the game client use only the new contract, and rollback/recovery steps for the manual deployment are recorded.

### F16: Define Seasons, Statistics Scopes, And Telemetry Retention

**Status:** Deferred product and operations decision; not a prerequisite for teams

**Depends on:** defined historical product requirements and representative telemetry volume

- [ ] Decide player-facing season cadence and system of record.
- [ ] Decide which statistic families share comparability scopes and how matches are assigned.
- [ ] Decide historical API/UI detail for recent and older play.
- [ ] Measure raw-event volume, index size, hot-query predicates, and expected archive cadence.
- [ ] Select physical PostgreSQL storage segments independently from gameplay semantics.
- [ ] Define hot, warm, and cold retention tiers, archive format/location, manifests, checksums, restore, and reprocessing.
- [ ] Validate restore and reconciliation before the first destructive telemetry removal.

**Done when:** each lifecycle has an explicit owner and rollover process, historical product behavior is defined, and raw telemetry can be archived and restored before relational data is dropped.

### F17: Investigate Lightweight Client-Event Validation

**Status:** Deferred long-term investigation; not a prerequisite for initial teams

**Depends on:** identified client event batches, retained source provenance, and representative client telemetry

- [ ] Define the threat model and which competitive, progression, insight, leaderboard, and reward surfaces may accept client-reported facts.
- [ ] Measure deterministic sequence, timing, checkpoint/lap, movement, and other low-cost plausibility checks against representative valid telemetry.
- [ ] Evaluate binding submissions to authoritative session context or server-issued nonces where those mechanisms work for local/time-trial play.
- [ ] Evaluate lightweight replay/ghost checksums, platform or anti-cheat signals, anomaly scoring, selective audit, and quarantine workflows.
- [ ] Define confidence and operator-review behavior without representing authenticated client data as server-authoritative.
- [ ] Reject full dedicated-server replay as the default unless a later cost/benefit review finds a narrowly targeted use worthwhile.

**Done when:** client-derived records have a measured, affordable validation policy appropriate to each product surface, with false-positive handling and no requirement to replay every match on dedicated-server infrastructure.

## Team Design Checkpoint

### T00: Refresh And Re-Approve The Team Solution Designs

**Depends on:** F15, F04

- [ ] Update both team solution designs to the implemented auth, package, event, fact, and integration boundaries plus the explicitly deferred telemetry-lifecycle decisions.
- [ ] Resolve remaining team progression, notification, cosmetic, wildcard, and competition-slot decisions.
- [ ] Capture current game-client routes, component hierarchy, navigation graph, and screenshots in the Ascent Rivals project.
- [ ] Produce controller-first Pencil designs before adding game-client team routes.
- [ ] Keep website work minimal and admin/progression configuration in the Eventun Extend App UI.

**Done when:** the initial team experience and later team-gauntlet slices have approved contracts, UI flows, and explicit exclusions.

## Initial Team Experience Tasks

These remain planned until T00 re-approval.

### T01: Replace Team State And Membership

- [ ] Generate team identity and derive owner from the authenticated creator.
- [ ] Enforce one active team per player.
- [ ] Store membership validity intervals instead of deleting history.
- [ ] Separate visible title, management capability, and competition rank.
- [ ] Keep create, disband, capability management, and roster administration on the website initially.

### T02: Add Team Read And Membership APIs

- [ ] Add browse/list, team detail, active roster, current-player team, open join, leave, invite, accept, decline, and typed transition outcomes.
- [ ] Keep one deterministic `AddTeamMember` command rather than separate endpoints for every transition.
- [ ] Expose team region, time zone, recruiting status, and approved Twitch or Discord watch links; keep editing on the website.
- [ ] Defer pagination and put text search last because controller text entry is poor and teams remain small.
- [ ] Do not add token-gated joins.

### T03: Add Fact-Backed Team Views

- [ ] Add public team-filtered roster stats and internal roster comparison.
- [ ] Add public team leaderboard queries using approved top-performer metrics.
- [ ] Attribute historical results by membership at performance time.
- [ ] Avoid mutable team aggregate tables until measured query cost requires a projection.

### T04: Add Initial Team Presentation And Cosmetics

- [ ] Implement the approved first cosmetics, likely card border/effect and decal choices.
- [ ] Let members choose whether and where to display team affiliation and entitled shared cosmetics.
- [ ] Keep media upload on the website and fixed cosmetic entitlements in Eventun.
- [ ] Keep course flags, holograms, and broader Discord-profile-style decoration behind later design approval.

### T05: Add Game-Client Team Views And Membership Flow

- [ ] Implement controller-first browse, team detail, roster, current-team, open join, leave, and invite-response flows.
- [ ] Do not add in-game team creation, disbanding, promote/demote, capability management, or token gates.
- [ ] Reuse existing routes and controls where the UI inventory supports it.
- [ ] Add closed-team join requests only if T00 confirms an approval workflow is required.
- [ ] Add a team-roster party invite only if it is a thin call to the unchanged existing invite path and T00 includes it.

### T06: Add Team Awareness In Lobbies And Matches

- [ ] Show clearer team identity in lobby, profile, player card, and pre-heat presentation.
- [ ] Show teammates with a green minimap treatment.
- [ ] Optionally give teammate bounty beams a distinct green treatment after visual testing.
- [ ] Keep team markers visible by default initially and allow affiliation hiding where approved.
- [ ] Leave party-member marker treatment out of scope.

### T07: Integrate Team Inbox Notifications

- [ ] Inventory the current AccelByte-backed toast, persistent inbox, and actionable invitation behavior.
- [ ] Persist actionable invites or requests until expiry or response.
- [ ] Define which team events are toast-only, inbox actions, or omitted.
- [ ] Do not add chat or a separate team activity feed.

### T08: Define Team Progression Before Building It

- [ ] Define team XP sources, member caps, active-participation scaling, season/permanent scope, levels, and cosmetic unlocks.
- [ ] Decide how team challenges reuse Eventun goals and normalized progression facts.
- [ ] Validate economy impact before granting member rewards.
- [ ] Implement team progression only after this definition is approved.

## Initial Team Gauntlet Tasks

These form a second, mostly parallel implementation slice after the team experience contract is stable.

### G01: Replace Qualification With Competition Slots

- [ ] Model stage entries as configurable slots owned by an individual, team, sponsor/community selection, or wildcard rule.
- [ ] Allow a team-owned slot to be occupied by one or more racers according to stage configuration.
- [ ] Snapshot top-N team qualification contributors at cutoff.
- [ ] Keep individual and team tournaments on one cohesive gauntlet model.

### G02: Add Frozen Team Qualification And Roster Control

- [ ] Attribute qualification performances to membership at performance time.
- [ ] Configure top-N team contributors and fixed racers per team.
- [ ] Let a manager control eligible racers or select an alternate admission rule.
- [ ] Support configurable qualification points, team rank, first-come, or threshold admission where approved.

### G03: Extend Dedicated-Server Team Runtime Contracts

- [ ] Extend the existing `ServerService` claim, admission, match acceptance, and completion contracts with slot, team, occupancy, and lock context.
- [ ] Regenerate the already service-specific Unreal GameServer and Client/Server Models surfaces for the team runtime changes.
- [ ] Make accepted matches and results stage-run scoped and idempotent.
- [ ] Enforce Eventun Server permission on every runtime operation.

### G04: Implement Pre-Start Slot Replacement

- [ ] Resolve concrete slot occupancy through a point read against the frozen field.
- [ ] Support `replace_lowest_prestart` when a higher-priority eligible racer arrives.
- [ ] Lock occupancy at the configured start point and never eject after lock.
- [ ] Give the dedicated server explicit allow, replace, reject, and reason responses.

### G05: Implement Durable Bracket State

- [ ] Add bracket entries, seeds, matches, sides, byes, results, and advancement references.
- [ ] Support high-versus-low seeding and manual setup/repair.
- [ ] Publish the bracket graph once the initial field is settled.
- [ ] Keep results and advancement stage-run scoped.

### G06: Define And Add Wildcard Slot Policies

- [ ] Define unaffiliated-individual fill behavior and sponsored/community team-owned slots.
- [ ] Decide whether community CP selection is one policy for a team-owned slot or a separate qualification source.
- [ ] Keep slot counts and wildcard policy configurable per gauntlet.
- [ ] Do not implement voting or rooting persistence as part of this slice.

### G07: Add Minimal Admin Website And Extend App Support

- [ ] Update Ascentun only for required team/gauntlet API changes and basic create/edit flows.
- [ ] Add manual bracket setup, repair, slot ownership, and roster controls with minimal styling.
- [ ] Put progression configuration and operational diagnostics in the Eventun Extend App UI.
- [ ] Do not add server-side pagination to existing small team views.

## Explicitly Deferred

- OTLP trace export until AccelByte changes the deployed Eventun configuration or documents a supported OTLP endpoint.
- The R03 service-image build while Docker is intentionally stopped; perform it during a later manual release verification when a container builder is available.
- Event-level rooting or persistent fan state.
- Team-specific custom-game modes.
- Asymmetric racer/supporter gameplay.
- Spectator, shoutcaster, or coach slots.
- Team activity feed or chat.
- Token-gated team joins.
- Party-system changes; a team-roster convenience invite remains conditional on requiring no party changes.
- In-game team creation, disbanding, capability management, or roster promotion/demotion.
- Full website redesign or v2 visual work.
- Automatic sender retry until identified ingestion is proven.
- Team progression implementation until T08 is approved.

## Review Checkpoints

- After R01: confirm the complete dormant token-gating slice is absent across Eventun, Ascentun, schema, and generated game-client APIs.
- After R03: approved on 2026-07-10; Go 1.26.5 and the compatibility baseline may proceed to F01.
- After F01: accepted on 2026-07-11 with no blocking review findings; Docker-dependent Unreal generation and service-image verification remain owner-waived manual release checks.
- After F06: code review accepted on 2026-07-11 with no blocking findings. Shared Cloud player custom-permission resolution was manually confirmed, then deliberately superseded by F06A because a grant assigned to every player adds no useful authorization boundary. Dedicated-server and Studio Admin permission checks remain outstanding. The intentionally broad temporary dedicated-server Admin grant remains until F06B.
- After F06A: read-only review found no implementation defects, and owner-controlled Shared Cloud smoke checks passed for the player, subjectless-service rejection, Studio Admin, dedicated-server, and denied confidential-client paths. The remaining Studio Admin grant-table wording is carried explicitly into F06B.
- After F06B: confirm the complete served/Admin specification contains no auth-only read duplicates, while generated Unreal code contains the exact ten selected Client reads plus five Server operations and no Admin operations or Admin-only model types.
- After F08: confirm disabled PoC integrations have zero core-runtime coupling.
- After F12: compare fact derivation cost against the one-core PostgreSQL tier.
- After F15: stop and re-review both team designs before team implementation.
- After T00: select the exact initial team and gauntlet delivery cutoffs.
