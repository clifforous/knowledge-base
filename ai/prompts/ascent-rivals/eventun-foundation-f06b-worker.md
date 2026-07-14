# Eventun Foundation F06B Coding Worker

Use this prompt from the existing VS Code session attached directly to the Eventun WSL workspace. This task also has a coordinated Windows/Perforce Ascent Rivals portion.

---

You are continuing the Ascent Rivals Eventun foundation reset. Implement only `F06B: Separate Unreal Consumer Surfaces`, verify the Eventun, generated-contract, and game-client cutover, update durable documentation and task evidence, and stop for review. Do not begin F07 package reorganization, event-ingestion redesign, database work, or teams features.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the Eventun branch, index, worktree, recent commits, and every diff before editing. Then read:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F06 through F07
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially Full Spec Versus Consumer Specs and the F06B caller-audit correction
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/game-client.md`
- `30_designs/ascent-rivals/team-gauntlets-and-brackets-solution-design.md` only for the foundation boundary this task establishes

Before touching Ascent Rivals, read its root `AGENTS.md`. Use Windows-native PowerShell and Perforce commands for that tree, preserve CRLF/encoding, open files with `p4 edit` or reconcile generated files appropriately, and never submit. At prompt preparation time the Perforce ticket was expired and `HGEventunServerSubsystem.cpp` remained read-only. Do not bypass Perforce with `chmod` or attribute changes; ask the owner to refresh `p4 login` if needed. If Perforce access cannot be restored, complete only independently reviewable Eventun work, leave F06B incomplete, and report the game-client blocker.

The accepted F06/F06A Eventun changes and accepted R01 Ascentun changes are still uncommitted working-tree state. Work on top of them. Do not reset, discard, stage, commit, amend, or overwrite unrelated changes.

## Corrected Current Caller Inventory

Do not preserve the earlier assumption that the dedicated server consumes only `ServerService.Event` plus four Admin gauntlet methods. Current Ascent Rivals source proves the dedicated server uses:

- `ServerService.Event`;
- four AdminService runtime operations: `ClaimGauntletStageRun`, `CheckGauntletStageRunAdmission`, `AcceptGauntletStageRunMatch`, and `CompleteGauntletStageRun`;
- ten ClientService reads through the currently merged GameServer wrapper: `Player`, `Sponsors`, `Gauntlets`, `Gauntlet`, `GauntletStats`, `PlayerGauntletStats`, `GauntletLeaderboards`, `GauntletPlayerLeaderboards`, `GauntletCalendar`, and `GauntletCalendarCompleted`.

F06A correctly rejects subjectless service tokens on ClientService. Generating GameServer solely from `server.swagger.json` therefore requires ServerService counterparts for all ten read calls. Preserve ClientService versions for authenticated player and non-dedicated/listen-server contexts.

## Fixed Decisions

- ClientService remains 68 methods, annotation-free, and authenticated by namespaced user subject.
- Move the four runtime methods from AdminService to ServerService. Delete the old Admin RPCs, `/v1/admin/gauntlet/stage-run/...` routes, handlers, generated wrappers, and aliases.
- Keep `CreateGauntletStageRuns`, `LaunchGauntletStageNow`, and all other authoring/operator operations in AdminService.
- Add ServerService READ counterparts for exactly the ten current dedicated-server reads above. Reuse existing request/response messages and query functions; do not invent a bulk bootstrap contract in this task.
- Use `/v1/server/...` HTTP routes for every ServerService operation. Preserve specific-before-generic gateway ordering where the calendar routes require it.
- ServerService uses only `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER`: CREATE for event ingestion and claim, READ for the ten query operations, and UPDATE for admission, match acceptance, and completion.
- Require a subjectless service principal for every ServerService RPC. Studio Admin or ordinary user tokens must not become GameServer callers merely because they can satisfy a custom Admin-format permission.
- After cutover, the dedicated-server IAM client needs Server CREATE, READ, and UPDATE and no Eventun Admin grant.
- Expected contract inventory is 68 Client methods, 60 Admin methods, and 15 Server methods: 143 merged operations, 125 paths, and the current 286 definitions unless structured generation proves a concrete difference.
- Continue serving the complete merged Swagger for `/eventun/apidocs`, the Extend contract, and the Extend App UI.
- Unreal Client input is `client.swagger.json`. Unreal GameServer input is `server.swagger.json`. Unreal Models input is a deterministic structured Client+Server merge. No merged/Admin specification is an Unreal input.
- Breaking pre-alpha cleanup is intended. Do not retain compatibility routes, wrapper aliases, copied Admin models, or stale merged specs.

## Required Implementation

### 1. Correct Service Ownership And Authorization

- Remove the four runtime RPC declarations from `admin.proto` and their methods from `AdminServiceServerImpl`.
- Add them to `server.proto` with Server resource annotations, existing CREATE/UPDATE semantics, and `/v1/server/gauntlet/stage-run/...` routes.
- Add the ten Server READ RPCs using the existing message types and the corresponding `/v1/server/...` routes. Keep the original Client RPCs unchanged.
- Add thin ServerService adapter methods that reuse the existing Eventun query/runtime functions. Do not duplicate database logic.
- Enforce subjectless service-token identity consistently for all 15 Server methods, using the smallest clear shared guard or transport policy. Retain mandatory permission validation and fail before product work.
- Preserve all four runtime methods' validation, transaction, idempotency, admission, and result behavior. This is a service/route/consumer move, not a gauntlet redesign.

### 2. Update Permission And Contract Tests

- Assert the exact 68/60/15 descriptor inventory.
- Assert every Client method remains annotation-free, every Admin method uses the Admin resource, and every Server method uses the Server resource with the intended action.
- Expected privileged action totals are CREATE=14, READ=34, UPDATE=19, DELETE=8 across 75 Admin+Server methods.
- Prove the four runtime methods are absent from AdminService and present only on ServerService.
- Prove all Server methods reject a token with a user subject even when permission validation succeeds, and accept the intended subjectless service actor path.
- Update merged Swagger assertions for the intentional ten-operation expansion and route moves. Preserve global Bearer security and the current definition set.

### 3. Make Unreal Inputs Structurally Correct

- Change `scripts/make_unreal.sh` so Client copies `client.swagger.json` and GameServer copies `server.swagger.json` directly.
- Add the smallest maintainable structured JSON composition step for Models using the already pinned Bun/Node toolchain or an equally existing project dependency. Do not concatenate JSON, regex-filter the merged spec, or depend on an unpinned global utility.
- Compose only Client and Server paths/definitions. Sort output deterministically. If the same path or definition appears in both inputs, require structural equality or fail with a useful error.
- Do not copy `gen/0_eventun.swagger.json` anywhere under the Unreal generation package. It remains the served/Admin/App UI contract only.
- Add non-Docker structural checks proving the Models definition set equals the Client+Server union and no Admin operation is present in Client, GameServer, Models, or packaged Unreal specs.
- Extend `./scripts/verify.sh unreal` to assert the generated GameServer wrapper exposes exactly the 15 Server operations, no `AdminService` operation identifier exists, and generated models come only from the reviewed union. Preserve deterministic double generation.

### 4. Integrate The Coordinated Ascent Rivals Cutover

- Regenerate with the pinned Unreal image and compare output before integration.
- In `HGEventunServerSubsystem`, change the four runtime calls from `AdminService...` to `ServerService...` and change the dedicated-server player lookup to `ServerServicePlayer`.
- In `HGGauntletSubsystem`, change the ten dedicated-server branches from `ClientService...` on `EventunServerApi` to the matching `ServerService...` calls. Leave `EventunClientApi->ClientService...` branches intact for authenticated player/listen-server execution.
- Do not remove the `ClientServiceEvent` non-dedicated fallback: `OnCreated` initializes Server and Client APIs exclusively, so that branch is the listen-server path rather than a dedicated-server authorization bypass.
- Integrate only reviewed generated plugin changes. The Client wrapper should remain behaviorally unchanged; the GameServer wrapper should shrink to actual ServerService operations; the shared Models header must retain every Client/Server type and remove Admin-only types.
- Reconcile the checked-in Ascent Rivals `spec/Client`, `spec/GameServer`, and `spec/Models` inputs to the new three-way boundary. Remove obsolete root merged/Admin input and duplicate plugin-local spec files if repository/tool searches confirm they are no longer consumed. Do not leave an Admin operation in any Unreal generation input.
- Preserve existing C++ style, CRLF, encoding, gameplay behavior, callbacks, and model types. This task explicitly authorizes compilation of the affected client and dedicated-server targets after integration; it does not authorize unrelated game tests or refactors.

### 5. Keep Other Consumers And Deployment Guidance Current

- The Ascentun source has no runtime caller for the moved methods, but its currently modified `api.json` is a checked-in merged Eventun contract snapshot. Refresh it from the accepted merged specification without overwriting unrelated R01 website changes. Do not add website behavior or regenerate a nonexistent client layer.
- Fix the carried README ambiguity: list Studio Admin users separately as requiring no manual role modification, and list trusted confidential clients separately with the explicit Admin CREATE/READ/UPDATE/DELETE grant.
- Update the dedicated-server grant matrix to Server CREATE/READ/UPDATE only and remove the temporary Admin grant.
- Update `50_knowledge/ascent-rivals/eventun/api.md`, `50_knowledge/ascent-rivals/game-client.md`, relevant F06B foundation notes, and the F06B task evidence to the implemented service counts and consumer boundary.
- Preserve the completed F06A Shared Cloud evidence. Record the new F06B dedicated-server Server READ/UPDATE grant and runtime smoke checks as pending unless the owner supplies them.

## Verification

1. Run focused descriptor, auth-boundary, service-adapter, gauntlet runtime, Swagger, and structured-model-composition tests while iterating.
2. Regenerate Eventun from a clean ignored-output state and update `scripts/generated.sha256` only through the established manifest command.
3. Run the complete coder-owned `./scripts/verify.sh` and `./scripts/verify.sh appui` workflows.
4. Do not start Docker. F06B cannot be marked complete without reviewed Unreal output; if Docker is already running, run `./scripts/verify.sh unreal`, otherwise report the blocker and stop before game-client integration.
5. With a valid Perforce ticket, open/reconcile only the generated plugin/spec files and the two affected game source files. Inspect `p4 diff` and `p4 opened`; never submit.
6. Compile the affected Ascent Rivals client and dedicated-server targets using the repository's established Windows workflow. Record commands and results. Automated gameplay tests remain out of scope; record the manual runtime checks still needed.
7. Run `git diff --check` in Eventun, Ascentun, and the Knowledge Base where applicable. Inspect all cross-repository diffs and preserve unrelated owner changes.
8. Search final Eventun and Ascent Rivals Unreal surfaces for old Admin runtime routes/wrappers, `EventunServerApi->ClientService`, `AdminService` generated operations, Admin-only model definitions, merged Unreal spec inputs, and stale temporary Admin-grant instructions.

## Constraints

- Do not begin F07 or move packages out of `internal/`.
- Do not change SQL, migrations, event payloads, team schemas, gauntlet rules, admission behavior, progression, or website UI.
- Do not add compatibility copies of the four moved runtime methods.
- Do not expose all ClientService methods to ServerService; add only the ten reads proven by current dedicated-server call sites.
- Do not hand-edit generated Go, App UI, or Unreal API/model output as the source of truth.
- Do not modify the AccelByte generator templates unless the separate-spec inputs cannot work without a narrowly demonstrated template defect.
- Do not start Docker, bypass an expired Perforce ticket, change read-only attributes manually, submit Perforce changes, or stage/commit/reset Git changes.

## Completion Report

Before stopping, report:

- final Client/Admin/Server method, route, and permission-action inventories;
- the four moved runtime operations and ten added Server read counterparts;
- service-token principal enforcement and focused test evidence;
- merged Swagger path/operation/definition counts and App UI generation evidence;
- the deterministic Models composition algorithm and conflict behavior;
- generated Unreal Client/GameServer/Models inventories proving no Admin surface remains;
- every Ascent Rivals generated/spec and C++ call-site change, plus Perforce state;
- client and dedicated-server compilation evidence and remaining manual runtime checks;
- Ascentun contract-snapshot and README/grant corrections;
- default, App UI, Unreal, generation-manifest, formatting, and diff verification;
- confirmation that F07, SQL, migrations, event contracts, gauntlet behavior, teams, progression, and website UI were not started.

Stop for review after F06B. Do not continue to F07.
