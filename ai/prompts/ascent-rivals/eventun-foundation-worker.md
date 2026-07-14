# Eventun Foundation Coding Worker

> **Archived prompt:** This records the completed R01 worker instructions and must not be executed as current guidance. The former `temp_migration.sql` was deployed and removed; the former follow-up delta is now stable `migration/migration.sql`. Current fixtures are `t0_seed_courses.sql` through `t3_seed_teams.sql`, canonical scheduling is `d3_schedule_refresh_views.sql`, and disposable delta confirmation is `--confirm-disposable-production-baseline=<target-fingerprint>`. Every older migration filename below is historical.

This prompt started the completed R01 implementation worker for the Eventun foundation task list.

---

You are the coding worker for the Ascent Rivals Eventun foundation reset. Work one reviewed task at a time. Begin with `R01: Remove The Retired Token Integration Slice` and stop after R01 is implemented and verified. Do not begin R02 or update Go dependencies in this task.

## Required Context

Read and follow all repository `AGENTS.md` files before editing. Then read these knowledge-base documents as current decisions rather than redoing their completed analysis:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`
- `30_designs/ascent-rivals/teams-solution-design.md`
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/eventun/data-model.md`
- `50_knowledge/ascent-rivals/website.md`
- `50_knowledge/ascent-rivals/game-client.md`

Relevant repositories are the canonical Eventun, Ascentun, and Ascent Rivals game-client checkouts identified by the workspace project map. Inspect their current working-tree state before editing. Preserve existing changes and do not revert work you did not create.

## Accepted Decisions

- TapTools has ceased operation and its API is unavailable.
- Remove the complete dormant token-gating slice rather than retain provider-specific abstractions.
- Remove TapTools, Koios, token catalog APIs/tables, team gate-token APIs/tables, and `token_gated` membership behavior.
- Future token gating is unsupported until it is separately redesigned around a provider-neutral asset source.
- Pre-alpha backward compatibility is not required. Delete obsolete APIs, generated models, schema, and code instead of adding compatibility branches.
- Do not stage or commit changes.

## Migration Boundary

- `migration/temp_migration.sql` is frozen for the planned 2026-07-10 production deployment. Do not modify, clear, reorder, or copy foundation changes into it.
- Put every one-time production transition introduced by R01 in `migration/temp_migration_2.sql`.
- Treat production after `temp_migration.sql` as the baseline for `temp_migration_2.sql`.
- Also update the canonical clean-slate `a*` through `d*` SQL so a fresh database reaches the same final schema without either temporary migration.
- Do not add a migration runner or another numbered migration file.

## R01 Scope

1. Capture the available pre-change Eventun build and test result. Distinguish existing failures from regressions.
2. Delete the TapTools OpenAPI source/generated client, API-key configuration, startup construction, scheduled sync, admin sync RPC, and collection metadata ingestion.
3. Delete the Koios OpenAPI source/generated client, startup construction, wallet asset lookup, and token-ownership admission logic.
4. Delete Eventun token catalog and team gate-token protobuf methods, handlers, models, SQL, and `token_gated` transition behavior.
5. Remove `token_meta`, `team_gate_token`, and dependent schema objects from the canonical schema. Add only the required deployed-schema transition to `temp_migration_2.sql`.
6. Delete IPFS/media helpers used only by TapTools ingestion. Leave shared R2/media behavior used elsewhere intact.
7. Remove Ascentun's dormant `token_gated` types, constants, and handling. Do not redesign its team UI.
8. Regenerate affected Eventun protobuf, Gateway, Swagger, Ascentun, and Unreal outputs using the repository workflows. Confirm authored game-client code has no dependency before deleting generated types.
9. Remove retired environment/configuration documentation, but do not run `go mod tidy`, upgrade Go, or update dependencies; that belongs to R02 after review.

## Engineering Constraints

- Prefer direct deletion and clear package APIs over wrappers or generic abstractions.
- Keep the Client, Server, and Admin service surfaces, removing only retired token-related methods.
- Preserve complete served Swagger and the existing AccelByte Extend service requirements.
- Do not change auth, event ingestion, package layout, teams redesign, gauntlets, or unrelated website/game-client behavior.
- Keep SQL statements deterministic and safe to run once against the stated post-`temp_migration.sql` baseline.
- Use focused tests where practical. Game-client generated-code verification and manual evidence are acceptable when automated Unreal tests are unavailable.

## Completion And Report

Before stopping:

- search all three repositories for remaining TapTools, Koios, token-catalog, gate-token, and `token_gated` runtime/API/schema references;
- run available formatting, generation, tests, Eventun build, Ascentun checks, and relevant generated-client verification;
- run `git diff --check` in every modified Git repository;
- confirm `migration/temp_migration.sql` is unchanged;
- report changed files, commands and outcomes, remaining references with reasons, and any blocker;
- stop for review without beginning R02 and without staging or committing.
