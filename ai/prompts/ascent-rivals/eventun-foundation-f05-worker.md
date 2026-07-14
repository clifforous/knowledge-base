# Eventun Foundation F05 Coding Worker

Use this prompt from the existing VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset in the native WSL checkout. Implement only `F05: Remove Or Replace Avoidable Runtime Dependencies`, verify it, update its task evidence, and stop for review. Do not begin F06 authorization, F07 package reorganization, the event/fact reset, or any teams feature work.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the current branch, `git status`, recent commits, and all existing diffs before editing. Preserve user and prior-worker changes. Then read these knowledge-base documents as current decisions rather than redoing completed analysis:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F05
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially the dependency audit and accepted foundation constraints
- `50_knowledge/ascent-rivals/eventun/api.md`

The workspace project map identifies the Knowledge Base if it is not mounted in the VS Code workspace.

## Accepted Baseline

- R01 through R03 and F01 through F04 are complete for their accepted scopes. Treat them as the baseline and do not reopen their decisions.
- F04 updated and verified the Extend App UI dependencies. Do not modify `app/`, its lockfile, its generated output, or its verification behavior in F05.
- Go 1.26.5 and the current F01 verification workflow are the accepted toolchain baseline.
- The deployed tracing contract still requires Zipkin. Do not replace or remove it.
- Migration organization and schema behavior are out of scope. Do not change SQL or add a migration.
- Backward compatibility is not required unless a current Eventun consumer demonstrably depends on the behavior, but this task is dependency simplification rather than an API redesign. Preserve protobufs, HTTP/gRPC routes, generated contracts, auth behavior, database semantics, and product behavior.
- The owner values direct, idiomatic code and fewer lines. Do not replace dependencies with a home-grown logging framework, UUID abstraction, configuration framework, or Swagger model layer.

## Current Runtime Seams

Confirm these against the current tree before acting:

- `github.com/rs/zerolog` is used throughout `main.go`, `internal/common`, and Eventun handlers. `internal/common/logging.go` contains the gRPC adapter and an HTTP standard-log bridge.
- Eventun domain code already uses `github.com/google/uuid`. `github.com/jackc/pgx-gofrs-uuid` is registered only through `pgxuuid.Register` after each connection; no second application UUID type is intended.
- `github.com/joho/godotenv/autoload` is a blank import in `main.go`. Docker Compose already loads `.env`, and scripts explicitly load their own environment files.
- `github.com/go-openapi/loads` is used only to read the generated merged Swagger, replace `basePath`, marshal it again, and serve it. Other `go-openapi` modules may remain reachable through AccelByte authorization code and must not be removed merely because `loads` is removed.
- The generated merged Swagger currently contains Client, Server, and Admin operations and already advertises `/eventun` as its base path. Verify the generator source and current output before deciding whether runtime patching is still needed.

## Required Implementation

### 1. Replace zerolog with `log/slog`

- Create one process logger using the standard library JSON handler and install it as the default logger once during bootstrap.
- Migrate every direct zerolog import and call in handwritten Go code. Preserve useful structured fields, errors, levels, request method/path/duration, gRPC fields, and trace IDs; do not flatten fields into formatted message strings when a structured attribute is clearer.
- Use context-aware `slog` calls where a meaningful request or job context is already available. Do not thread a logger through every service solely for this task.
- Replace the gRPC adapter with the current upstream `slog` pattern: a small `logging.LoggerFunc` that calls `logger.Log(ctx, slog.Level(level), message, fields...)`. The authoritative v2.3.3 example is `https://github.com/grpc-ecosystem/go-grpc-middleware/blob/v2.3.3/interceptors/logging/examples/slog/example_test.go`.
- Replace the custom HTTP `ZeroLogWrapper` with the standard-library bridge, such as `slog.NewLogLogger`, and retain structured HTTP request logging.
- Preserve fail-fast behavior where zerolog `Fatal` currently terminates the process. Since `slog` has no fatal API, make termination explicit. One small process-exit helper is acceptable if it reduces repetition; do not create a general logging facade.
- Delete obsolete zerolog adapter/bridge code. Keep `internal/common/logging.go` only if the small gRPC adapter still belongs there.

### 2. Remove `pgx-gofrs-uuid`

- Remove the import, per-connection registration, and module dependency.
- Keep `github.com/google/uuid` as the single application UUID type. Do not introduce `pgtype.UUID`, `gofrs/uuid`, string-only UUID handling, or conversion wrappers unless a concrete pgx boundary requires one.
- Verify the actual database shapes Eventun uses, including scalar UUID scan/value behavior and the `[]uuid.UUID` array passed to `ANY($n)` in team permission queries. Do not assume scalar coverage proves the array path.

### 3. Remove hidden dotenv autoloading

- Remove the blank `godotenv/autoload` import and module dependency.
- Keep production, Docker Compose, and script configuration environment-driven. Do not add another runtime dotenv package or custom parser.
- Update local-run documentation so direct `go run .` use explicitly exports or sources the repository `.env` before startup. Keep `.env.template`; Compose still uses it. Ensure the documented command matches the template's actual shell compatibility and does not expose credentials.

### 4. Remove `go-openapi/loads` from Swagger serving

- First determine whether the generated merged Swagger's `basePath` is already guaranteed to equal `common.BasePath`. If so, serve the generated JSON directly with the standard library. If runtime patching is still necessary, decode and replace only the top-level `basePath` with `encoding/json` while preserving the rest of the document.
- Preserve the existing Swagger UI route, JSON route, status handling, JSON content type, and complete merged specification. Do not reduce the served document to only one service surface.
- Keep file selection deterministic. Do not add a generic OpenAPI abstraction or switch generators in this task.
- Add focused coverage that parses the served JSON and proves the base path and representative Client, Server, and Admin operations, definitions, and security metadata survive unchanged. Cover missing or invalid input behavior if the handler still performs runtime file discovery/parsing.

## Implementation Sequence

1. Record the baseline tree and module graph. Inventory all imports and usages of the four target dependencies, including transitive reasons for related modules.
2. Migrate logging first. Add focused adapter/middleware coverage where useful, then format and run focused tests.
3. Remove the pgx UUID adapter and verify representative scalar and array behavior through the narrowest reliable test available. Use a database integration test only if the existing test conventions and local environment make it appropriate; do not add Docker orchestration to F05.
4. Remove dotenv autoloading and correct local-run documentation.
5. Simplify Swagger serving and add focused handler/spec-preservation tests.
6. Run `go mod tidy` only after code changes are complete. Confirm `go.mod` and `go.sum` no longer contain zerolog, `pgx-gofrs-uuid`, `gofrs/uuid` when no longer transitively reachable, godotenv, or `go-openapi/loads`. Retain any `go-openapi` runtime/format modules still required by current auth code.
7. Run the complete default `./scripts/verify.sh` workflow and `git diff --check`. Docker, Unreal SDK generation, and App UI verification are not required because this task does not change those surfaces.
8. Mark F05 complete and add concise implementation and verification evidence to `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md` only after all done criteria pass.

## Constraints

- Keep changes tightly scoped to F05. Do not move `main.go`, remove `internal/`, introduce `cmd/eventun`, split domain packages, or otherwise begin F07.
- Do not change auth enablement, permissions, role checks, service ownership, or Swagger security declarations; those belong to F06.
- Do not change protobufs, regenerate contracts unnecessarily, update unrelated dependencies, or alter database schema/query behavior.
- Do not add a migration runner, CI workflow, logger facade, configuration object graph, UUID repository abstraction, or OpenAPI framework.
- Do not weaken verification or delete useful structured log fields merely to reduce line count.
- Do not stage or commit changes.

## Completion Report

Before stopping, report:

- each removed direct dependency and any newly unreachable transitive modules removed by `go mod tidy`;
- the final logger construction, gRPC adapter, HTTP error-log bridge, and explicit fatal behavior;
- UUID scalar and array verification evidence;
- the explicit local configuration workflow now documented;
- how Swagger is served, whether runtime base-path patching remains, and evidence that the complete merged spec is preserved;
- focused test results, full `./scripts/verify.sh` result, `git diff --check`, and any warnings;
- all changed files and confirmation that F06, F07, API contracts, SQL, generated output, App UI, and product behavior were not changed.

Stop for review after F05. Do not begin F06 or F07.
