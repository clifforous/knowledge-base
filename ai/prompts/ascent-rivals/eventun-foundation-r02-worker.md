# Eventun Foundation R02 Coding Worker

> **Archived prompt:** This records the completed R02 worker instructions and must not be executed as current guidance. The former production baseline delta was deployed and removed; current pending production SQL uses stable `migration/migration.sql`. Fixtures use `t0_seed_courses.sql` through `t3_seed_teams.sql`, canonical scheduling uses `d3_schedule_refresh_views.sql`, and disposable delta confirmation is `--confirm-disposable-production-baseline=<target-fingerprint>`. References below to temporary migration files are historical.

This prompt was used from a VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset in the native WSL checkout. Implement only `R02: Reset The Go Toolchain And Module Graph`, report the resulting R03 compatibility inputs, and stop for review. Do not begin R03 or any F-series task.

## Read First

Read and follow Eventun's `AGENTS.md`. Use the existing working tree as the source of truth and preserve every R01 change. Read these knowledge-base documents for current decisions instead of redoing completed analysis:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially R02 and R03
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially Dependency Audit and Suggested Delivery Order
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/eventun/data-model.md`

The workspace project map identifies the Knowledge Base if it is not already mounted in the VS Code workspace.

## Completed R01 Baseline

R01 is complete but intentionally uncommitted. The current Eventun R01 diff is staged in the index; treat that staged index as a read-only baseline. Do not unstage, restage, revert, rewrite, or regenerate it as part of R02. Keep every R02 edit unstaged so its diff remains distinguishable from R01.

- TapTools, Koios, token catalog/gate APIs and tables, and `token_gated` behavior were removed.
- Eventun, Ascentun, and Unreal generated API surfaces were updated.
- Before and after R01, Eventun `go test ./...`, `go build ./...`, and post-change `go vet ./...` passed with Go 1.26.1.
- Swagger generation passed with 68 Client, 64 Admin, 1 Server, and 133 merged operations.
- `go.mod` and `go.sum` were deliberately left unchanged for R02.
- `migration/temp_migration.sql` remained hash-identical to `HEAD`.
- Existing unrelated findings are deferred: Buf RPC naming/unused-import lint findings belong to F01, and Extend App UI dependency vulnerabilities belong to F04.

The Eventun working tree contains the R01 implementation plus the intentional migration-boundary setup. Ascentun, the Knowledge Base, and the Perforce game client also contain coordinated R01 changes. R02 is Eventun-only: do not modify those other workspaces.

## Fixed Decisions

- Upgrade the Go directive and service builder from Go 1.26.1 to exactly Go 1.26.5.
- Remove dependencies made unreachable by R01 before evaluating updates.
- Update every remaining Go module and Go `tool` dependency to the latest stable release available on its current module path.
- Inventory newer major versions and maintained replacements that require source/import migration, but leave those source changes for R03.
- Do not silently retain or downgrade an old version to keep current source compiling.
- Do not replace used dependencies scheduled for later architectural cleanup, such as zerolog, `pgx-gofrs-uuid`, `godotenv`, or `go-openapi/loads`; update their current module paths in R02 and leave replacement/removal to F05.
- Do not change the existing staged R01 index. Do not stage R02 changes or create a commit.

## Scope And Sequence

1. Inspect `git status`, `git diff --cached`, unstaged `git diff`, `go.mod`, `go.sum`, the Dockerfile, Go-related scripts/docs, and every applicable repository instruction. Record the staged R01 baseline and confirm there is no pre-existing unstaged Eventun change before editing.
2. Verify the native WSL shell is actually running Go 1.26.5. Record `go version`, `go env GOTOOLCHAIN`, and the executable path. Do not report verification performed with Go 1.26.1 as the R02 result.
3. Capture the current module graph and direct requirements before cleanup. Use `go mod why -m` where ownership is unclear.
4. Run `go mod tidy` against the completed R01 source before any upgrades. Review and record every removed requirement. `github.com/gabriel-vasile/mimetype` is expected to disappear because its only importer was removed; confirm rather than assume. Confirm whether the oapi-codegen runtime/tool remains required by retained generated integrations.
5. Change the `go` directive and every repository build/runtime declaration from 1.26.1 to 1.26.5, including the service Docker builder. Search the full Eventun tree for stale Go-version declarations.
6. Run `go list -m -u all` on the reduced graph. Inventory:
   - direct application modules;
   - indirect modules;
   - the oapi-codegen `tool` dependency;
   - the `github.com/willf/bitset` replacement and why it remains or can be removed;
   - newer major versions or maintained alternatives that require source migration.
7. Update current module paths in coherent families, with a separate `go mod tidy`, `go test ./...`, and `go build ./...` result after each family:
   - gRPC, Gateway, protobuf, middleware, and genproto;
   - OpenTelemetry core, contrib, propagators, and exporter;
   - pgx and database helpers;
   - AccelByte SDK;
   - scheduler;
   - MinIO/R2 and retained OpenAPI generation/runtime;
   - remaining logging, configuration, Swagger, metrics, and utility modules.
8. If a family compiles, record that. If it exposes a source or generated-code incompatibility, keep the selected dependency update, capture the exact compiler/test failure and affected API, and add it to the R03 handoff. Do not edit application or generated source to repair it in R02. Stop further grouping only if the failure prevents reliable module-graph analysis.
9. Remove unused requirements and obsolete replacements. Keep a `replace` only when `go mod why`, module-path history, or a reproducible failure demonstrates that it is still necessary; record that reason.
10. Run final `go mod tidy`, repeat `go list -m -u all`, and verify `go.mod` and `go.sum` are stable across a second tidy.
11. Attempt `go test ./...`, `go build ./...`, `go vet ./...`, and `govulncheck ./...` with Go 1.26.5. A compile-blocked check is an R03 input, not permission to downgrade or start source fixes.
12. Run `git diff --check` for both cached R01 and unstaged R02 changes. Confirm the staged R01 index is unchanged, no schema, protobuf, generated client, Ascentun, Knowledge Base, or game-client file changed during R02, and both temporary migration files are untouched.

## Constraints

- Use WSL-native commands and paths throughout this task.
- Do not run protobuf, Swagger, App UI, Ascentun, or Unreal generation in R02.
- Do not change application source, generated source, APIs, schema, migrations, auth, package layout, or product behavior.
- Do not add CI, a migration runner, dependency wrappers, or compatibility branches.
- Treat the dependency-version table in the foundation review as a dated starting point; query the current module registry rather than copying its versions blindly.
- Keep `go.mod` readable and let `go mod tidy` classify direct versus indirect requirements.

## Completion Report

Stop after R02 and report:

- Go executable/version and every changed toolchain declaration;
- requirements removed by the post-R01 tidy;
- old and selected version for every updated direct module and Go tool;
- remaining `go list -m -u all` results, with reasons;
- retained `replace` directives and evidence;
- test/build/vet/vulnerability results after each family and at the end;
- exact R03 source-compatibility, major-version migration, or vulnerability work items;
- changed files and `git diff --check` result;
- confirmation that R01 code, Ascentun, generated game-client files, and both temporary migration files were not modified;
- confirmation that the pre-existing staged R01 index was unchanged, all R02 changes remain unstaged, and nothing was committed.
