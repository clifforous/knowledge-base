# Eventun Foundation F04 Coding Worker

> **Archived prompt:** This records the completed F04 worker instructions and must not be executed as current guidance. The former `t0_migration.sql` was deployed and removed; current pending production SQL uses stable `migration/migration.sql`. Fixtures use `t0_seed_courses.sql` through `t3_seed_teams.sql`, canonical scheduling uses `d3_schedule_refresh_views.sql`, and disposable delta confirmation is `--confirm-disposable-production-baseline=<target-fingerprint>`. The old baseline waiver below is historical.

This prompt was used from the existing VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset in the native WSL checkout. Implement only `F04: Update Extend App UI Dependencies`, verify it, update its task evidence, and stop for review. Do not begin F05, F06, or any teams feature work.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the current working tree before editing and preserve all existing changes. Then read these knowledge-base documents as current decisions rather than redoing completed analysis:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F01 and F04
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially the dependency audit and F04 delivery guidance
- `50_knowledge/ascent-rivals/eventun/api.md`

The workspace project map identifies the Knowledge Base if it is not mounted in the VS Code workspace.

## Accepted Baseline

- R01 through R03 and F01 through F03 are complete for their accepted scopes.
- F03's authentic disposable post-`t0_migration.sql` execution and schema-convergence check was explicitly waived by the owner. Do not reopen SQL organization, migrations, PostgreSQL verification, pg_cron, or `scripts/database.sh` in F04.
- F03 may still be uncommitted when this task begins. Treat every existing F03 file as a read-only baseline, do not stage or revert it, and keep F04 changes clearly distinguishable in the final report.
- The root uses Bun only for pinned service-generation tools. The Extend App UI under `app/` uses npm and the tracked `app/package-lock.json`. Do not replace either package manager.
- The verified runtime baseline is Bun 1.3.9, Node.js 24.4.0, and npm 11.4.2. Do not change runtime baselines unless a selected dependency has a documented minimum that requires an explicit owner decision.
- F01's `./scripts/verify.sh appui` workflow performs a frozen install, regenerates the App UI client twice, compares both generated outputs, lints, builds, and audits. Its accepted baseline had 35 npm audit findings, peer-dependency warnings, and the AccelByte codegen missing-`x-version` warning.
- Preserve the complete merged Swagger and existing App UI generated-client contract. Do not change protobufs, routes, API behavior, auth, Go code, Unreal generation, or product UI behavior in this task.

## Current Dependency Shape

Start from the current files rather than assuming these versions remain unchanged:

- `app/package.json`
- `app/package-lock.json`
- `app/vite.config.ts`
- `app/eslint.config.js`
- `app/tsconfig*.json`
- `app/abcodegen.config.ts`
- `app/swaggers.json`
- `scripts/verify.sh`
- root and App UI dependency/tooling documentation

The current application is React 19 with React Router 7, Vite 7, TypeScript 5.9, Zod 3, Ant Design 6, TanStack Query 5, AccelByte SDK packages, AccelByte codegen, module federation, Tailwind, ESLint, and Prettier. Exact versions and transitive constraints must come from the current package and lock files.

## Required Research

Use `npm view`, `npm outdated`, package peer metadata, release notes, and official migration documentation available at execution time. Record the exact latest stable version and compatibility decision for every direct dependency and override. Do not rely on a stale version list in the task document.

At minimum, review these official migration sources:

- React Router v7 to v8: `https://reactrouter.com/upgrading/v7`
- Vite v7 to v8: `https://vite.dev/guide/migration.html`
- TypeScript 7: `https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/`
- Zod 4: `https://zod.dev/v4/changelog`
- AccelByte Extend App UI codegen: `https://docs.accelbyte.io/gaming-services/modules/foundations/extend/extend-app-ui/codegen-specs/`

Do not assume that a package being published makes the complete AccelByte App UI toolchain compatible with it. An incompatible latest major must be documented with concrete peer, build, codegen, or official-support evidence rather than forced into the graph.

## Implementation Sequence

1. Record `git status`, the existing non-F04 diff, runtime versions, direct dependency versions, `npm outdated`, `npm ls`, and `npm audit` before editing. Run the existing App UI verification baseline before changes when feasible; distinguish pre-existing failures and warnings from regressions.
2. Inventory every direct dependency, dev dependency, and override. Classify each as compatible patch/minor, isolated major migration, unchanged because already current, removable, or blocked by a documented incompatibility.
3. Update compatible patch/minor releases in coherent families first. Include AccelByte SDK/codegen, React and its types, query/UI/network packages, build plugins, lint/format packages, and supporting types where updates exist. Keep exact-version pinning consistent with the current project and let npm update the tracked lockfile.
4. Re-evaluate the existing Axios and Zod overrides. Retain an override only when the resolved graph demonstrably needs it; do not use overrides to hide incompatible peer requirements.
5. Migrate each major family independently and verify before starting the next:
   - React Router 8: first satisfy its current Node, React, and Vite baseline and review applicable v7 preparation/future behavior. Preserve the app's existing routing mode and behavior.
   - Zod 4: review authored schemas, AccelByte-generated client output, validator/codegen peer constraints, error handling, and changed inferred types. Update the direct dependency and any justified override together.
   - Vite 8: account for Rolldown/Oxc changes and verify the React, Tailwind, module-federation, custom proxy, build-manifest, and remote-entry behavior. Use an intermediate Rolldown-on-Vite-7 step only when it provides useful diagnostic isolation; do not retain it without a reason.
   - TypeScript: use TypeScript 6 as the compatibility bridge before TypeScript 7, because TypeScript 7 adopts TypeScript 6 behavior and removes deprecated constructs. TypeScript 7 uses the native compiler and does not yet provide every former programmatic API. Verify `typescript-eslint`, AccelByte codegen, Prettier organize-imports, Vite, and all build scripts. If one of those tools requires the unavailable API, retain the latest compatible TypeScript 6 release and document the exact blocker to TypeScript 7.
6. After each dependency family, run the focused install, dependency-tree, lint, codegen, and production-build checks needed to localize failures. Do not combine unrelated major upgrades before obtaining a passing checkpoint.
7. Run the complete `./scripts/verify.sh appui` workflow after the final dependency graph. Run `npm audit` explicitly and classify any remaining finding by owning package, available fix, reachability/relevance, and whether fixing it requires an incompatible upstream major.
8. Update only documentation whose versions, commands, warnings, or compatibility statements changed. Add concise F04 status and evidence to the foundation task list after verification.

## Constraints

- Do not use `npm audit fix --force`, a blind all-package update, or manual lockfile editing.
- Do not weaken lint, TypeScript, build, audit, or deterministic-generation checks merely to make an upgrade pass.
- Do not add compatibility wrappers for old package APIs when direct migration and deletion are clearer.
- Do not make product-facing UI redesigns or opportunistic component refactors.
- Do not check in generated `app/src/eventunapi`, `app/swaggers`, `app/dist`, `node_modules`, or temporary module-federation output if those paths remain generated/ignored.
- Do not stage, commit, or modify the pre-existing F03 baseline.
- If a major is blocked, preserve the latest verified compatible version, cite the concrete blocker, and continue with independent families rather than abandoning all compatible updates.

## Completion Report

Before stopping, report:

- every direct package's before/after version or documented reason for no change;
- changes to overrides and why each remaining override is necessary;
- each dependency family checkpoint and its command results;
- final `npm ls`, `npm audit`, lint, codegen determinism, production build, and `./scripts/verify.sh appui` outcomes;
- any remaining peer warning, audit finding, codegen warning, or deferred major with exact ownership and rationale;
- changed files and confirmation that F03, backend contracts, generated service output, and product behavior were not altered.

Stop for review after F04. Do not begin F05 or F06.
