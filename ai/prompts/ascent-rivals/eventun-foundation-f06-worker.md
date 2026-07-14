# Eventun Foundation F06 Coding Worker

Use this prompt from the existing VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset in the native WSL checkout. Implement only `F06: Adopt Mandatory Auth And Eventun Permissions`, verify it, update durable documentation and task evidence, and stop for review. Do not begin F06B's service-method moves or Unreal consumer split, F07's package reorganization, or any teams feature work.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the current branch, index, worktree, recent commits, and all existing diffs before editing. Then read these knowledge-base documents as accepted decisions rather than redoing completed analysis:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F06 and F06B
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially Shared Cloud IAM, the production-authentication finding, OpenAPI security, and the target request shape
- `50_knowledge/ascent-rivals/eventun/api.md`

The workspace project map identifies the Knowledge Base if it is not mounted in the VS Code workspace.

At prompt preparation time, the accepted F05 changes were staged but not committed and F06 overlaps `main.go`, `README.md`, `go.mod`, and tests. Prefer starting only after the owner commits F05. If F05 is still staged, do not reset, unstage, amend, or mix ownership silently; preserve the index exactly and keep F06 changes unstaged and clearly attributable.

## Accepted Baseline And Fixed Decisions

- R01 through R03 and F01 through F05 are accepted for their scoped behavior. Do not reopen dependency, migration, logging, UUID, dotenv, or Swagger-serving decisions.
- Eventun is an AccelByte Extend Service Extension in Shared Cloud. Protobuf, gRPC-Gateway, generated Swagger v2, and the complete `/eventun/apidocs/api.json` contract remain required.
- Local insecure product APIs are no longer supported. Delete the runtime auth-disable path; every Eventun Client, Server, and Admin RPC must authenticate and authorize.
- Use exactly three coarse resources, with the literal `{namespace}` placeholder:
  - Client: `CUSTOM:NAMESPACE:{namespace}:EVENTUN`
  - Server: `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER`
  - Admin: `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN`
- Use only the standard CREATE, READ, UPDATE, and DELETE action bits. Do not create endpoint-, domain-, team-, progression-, or gauntlet-specific IAM resources.
- Client, Server, and Admin service ownership does not change in F06. In particular, the four dedicated-server gauntlet runtime methods remain temporarily on AdminService until F06B.
- The Admin permission is authoritative for AdminService. Delete the remote AccelByte role-admin-status lookup and the Eventun-local `player_role = admin` network shortcut.
- Preserve non-admin domain roles such as `gauntlet_creator`, the `player_role` table, and player role data returned by existing APIs. This task removes the special `admin` bypass; it does not delete all domain roles.
- A token without a player subject is not implicitly an administrator. ClientService ownership, self, manager, and creator checks must not be bypassed merely because the caller used a service token.
- An already authorized AdminService caller must not repeat a database role check or make an IAM role-status network call. Both Studio Admin user tokens and trusted confidential clients with the Admin resource are accepted.
- Health, reflection, metrics, Swagger UI, and Swagger JSON remain non-product operational/documentation surfaces. Product RPCs must fail closed if their permission annotation is missing or malformed.
- Breaking pre-alpha cleanup is allowed. Delete obsolete branches, tests, configuration, and dependencies rather than retaining compatibility code.

## Current External Reference

Review the current official behavior before implementation. At prompt preparation on 2026-07-11, AccelByte's Go template `main` was commit `3d200c8f568f5820643c28905b5474f8d49b235c`:

- template: `https://github.com/AccelByte/extend-service-extension-go`
- permission proto: `https://github.com/AccelByte/extend-service-extension-go/blob/main/pkg/proto/permission.proto`
- auth interceptor: `https://github.com/AccelByte/extend-service-extension-go/blob/main/pkg/common/authServerInterceptor.go`
- customization guide: `https://docs.accelbyte.io/gaming-services/modules/foundations/extend/service-extension/customize-service-extension-app/`
- Shared Cloud custom permissions: `https://docs.accelbyte.io/gaming-services/modules/foundations/identity-access/authorization/master-permissions/custom-permissions/`
- App UI cookie/auth troubleshooting: `https://docs.accelbyte.io/gaming-services/modules/foundations/extend/extend-app-ui/extend-app-ui-troubleshooting/`
- App UI Swagger generation: `https://docs.accelbyte.io/gaming-services/modules/foundations/extend/extend-app-ui/codegen-specs/`

Import the current behavior, not the template's project layout or all of its code. Eventun already has stronger actor-context propagation and tests. Do not copy a second token extractor, a second claims context, obsolete exported validator fields, or the template's optional auth-disable branch.

## Current Eventun Auth Shape

Confirm these against the current tree before editing:

- `internal/common/claims.go` extracts Bearer metadata plus `access_token` from both `cookie` and `grpcgateway-cookie`, parses claims, requires non-empty `client_id`, wraps stream contexts, and stores claims, access token, client id, and optional player subject.
- The current claims interceptor validates token authenticity but does not validate the RPC's required Eventun permission.
- `main.go` conditionally installs claims interceptors through `PLUGIN_GRPC_SERVER_AUTH_ENABLED`.
- Client, Admin, and Server protos repeat operation-level Bearer blocks; `Courses` is the known omission. No permission extension is currently imported.
- `apiActionWithPermission` treats any service token or Eventun-local `admin` role as an administrator and skips domain checks.
- AdminService repeats authorization through `accelByteAdminRoleAuthorizer`, `iam.RolesService`, `AB_IAM_BASE_URL`, and `g.checkIsAdmin` on nearly every method.
- AdminService currently contains four dedicated-server gauntlet runtime methods. Their callers must temporarily retain the Admin grant until F06B moves all four together.
- The current generated inventory is 68 ClientService RPCs, 64 AdminService RPCs, one ServerService RPC, and 133 merged operations.

## Required Implementation

### 1. Add Permission Annotations To Every Product RPC

- Add a local, lint-compliant copy of the current Extend permission proto and generate its Go extension definitions through the existing Buf pipeline. Keep the four action values compatible with AccelByte: CREATE=1, READ=2, UPDATE=4, DELETE=8.
- Import it into `client.proto`, `server.proto`, and `admin.proto`.
- Give every ClientService method the Client resource, every ServerService method the Server resource, and every AdminService method the Admin resource. Do not move any method in this task.
- Assign one semantic action to every RPC:
  - READ for side-effect-free get/list/status/history/preview/validate/explain/export operations;
  - CREATE for submission, creation, add/invite/claim, and event-ingest operations;
  - UPDATE for mutation, publish/apply/sync/retry/launch/accept/complete operations;
  - DELETE for delete/remove/leave/cancel/deny/archive/purge/unlink operations.
- Resolve ambiguous methods by their actual behavior, not only their HTTP verb. Record the final action inventory in test output or task evidence.
- Add descriptor-level coverage that fails unless all 133 Eventun methods have exactly one non-empty expected service resource and one nonzero known action. An omitted annotation must not silently make a product method public.

### 2. Build One Mandatory Auth And Actor-Context Interceptor

- Adapt Eventun's existing claims interceptor so one unary and one stream path perform token extraction, method-permission lookup, AccelByte token/permission validation, and actor-context enrichment without parsing unrelated metadata twice.
- Preserve both Bearer and Admin Portal cookie authentication. Authorization metadata takes precedence over cookies. Preserve `cookie` and `grpcgateway-cookie` support.
- Preserve claims, raw access token, non-empty client id, and optional player id in the handler context. Preserve the wrapped stream context behavior.
- Validate the method's annotated permission against `AB_NAMESPACE` through the current AccelByte SDK. Do not hand-roll wildcard, namespace, role, revocation, or action-bit matching.
- Inspect AccelByte Go SDK v0.89.0's current `iam.TokenValidator`, `OAuth20Service`, and validator interfaces before choosing construction. Use the smallest path that validates the required method permission and provides claims while handling initialization failure explicitly. Do not blindly copy the template's compatibility wrapper or create duplicate long-lived validators/background refresh loops without proving they are required.
- Missing metadata, missing token, malformed/invalid/expired token, and missing `client_id` must be rejected before the handler. A valid token without the required resource/action must return PermissionDenied. Keep error details useful without leaking token contents.
- Product service descriptors with missing or malformed permission annotations must fail closed as server misconfiguration. Explicitly allow only intended non-product gRPC services such as health and reflection to bypass product permission lookup.
- Install unary and stream auth interceptors unconditionally in `main.go`. Delete every `PLUGIN_GRPC_SERVER_AUTH_ENABLED` branch and lookup.
- Initialization failure for the mandatory validator must stop startup or otherwise leave no serving path; do not log and continue with unprotected APIs.
- Keep interceptor logic in the current common package for F06. Moving it to `auth` belongs to F07.

### 3. Remove Duplicate And Borrowed Admin Authorization

- Delete `internal/eventun/admin_authorization.go`, its tests, the role-status service, referer workaround, `AB_IAM_BASE_URL`, and `adminRoleConfigRepository`.
- Remove `iam.RolesService` from AdminService construction and remove now-unreachable direct dependencies with `go mod tidy`.
- AdminService handlers should rely on the already validated Admin resource and proceed through their ordinary action wrapper without `g.checkIsAdmin` or a local role query. Simplify existing wrappers directly; do not introduce a second Admin wrapper family.
- Remove the Eventun-local `admin` bypass from `apiActionWithPermission`, team mutation internals, and any other ClientService domain path. A service token on ClientService cannot bypass player ownership checks.
- Preserve `gauntlet_creator` and any other non-admin domain role checks. Do not drop the `player_role` schema or role data from player responses.
- Do not leave ClientService `DeleteTeam` permanently unusable after deleting `checkIsAdmin`. Align it with the accepted current rule that a team owner may disband the team, reusing the narrow existing owner/designation check rather than redesigning the team contract.
- Keep the dedicated-server gauntlet runtime methods on AdminService for this task. Their authorization is the Admin resource until F06B moves them.

### 4. Prototype Global Swagger Bearer Security

- Before changing security metadata, capture the generated Client, Server, Admin, and merged Swagger documents plus App UI and available Unreal generated outputs as comparison baselines.
- Prototype one top-level Bearer security requirement in each service Swagger option. Permission annotations remain the runtime authority.
- Remove repeated operation-level Bearer blocks only if all of the following hold:
  - every Client, Server, Admin, and merged operation still has effective Bearer security;
  - routes, operation ids, parameters, request/response schemas, definitions, and service inventories are unchanged;
  - the Extend App UI generated client remains equivalent for authentication and passes deterministic generation, lint, and build;
  - the pinned Unreal generator remains equivalent for authentication and API shape.
- Update F05's Swagger tests to validate effective top-level security and complete-spec preservation without incorrectly requiring a redundant operation-level block.
- If global security is not honored by either generator, retain the operation-level blocks and document the concrete blocker. Do not weaken a consumer merely to reduce protobuf lines.
- Do not change `scripts/make_unreal.sh`, move runtime methods, split Unreal inputs, or modify the Ascent Rivals Perforce tree. Those changes belong to F06B.

### 5. Update Manual Shared Cloud Configuration

- Remove `PLUGIN_GRPC_SERVER_AUTH_ENABLED` and `AB_IAM_BASE_URL` from `.env.template`, README instructions, code, and tests. Do not retain a replacement insecure switch.
- Update local instructions to require real AccelByte credentials and authenticated test calls.
- Add a concise manual permission-cutover checklist. At minimum document:
  - Default User Role Override: Client resource with the action bits used by ClientService;
  - dedicated-server confidential IAM client: Server resource, plus the temporary Admin resource needed by the four gauntlet runtime methods until F06B;
  - Studio Admin and trusted operator/backend principals: Admin resource;
  - Eventun's own `AB_CLIENT_ID`: the IAM Roles Read and Basic Namespace Read grants required by the validator, plus its existing downstream service grants; do not confuse these with caller-facing Eventun resources.
- Document grant-before-deploy ordering so the mandatory-auth release does not create an avoidable outage. Keep deployment manual; do not add IAM automation, CI, or migration tooling.
- Record the Shared Cloud limitation that the current Extend App UI custom-permission path supports Studio Admin, while Game Admin and View Only users receive 403.

## Required Tests

Use injected narrow interfaces and fakes for auth behavior; unit tests must not require live AccelByte IAM.

At minimum cover:

- all 68 Client, 64 Admin, and one Server descriptors have the correct resource and a valid action;
- a player Bearer token with Client permission reaches a Client handler and receives complete actor context;
- a dedicated-server service token with Server permission reaches ServerService with client id and no player id;
- a Studio Admin `access_token` cookie with Admin permission reaches AdminService and receives actor context;
- Authorization metadata wins when both header and cookie exist;
- missing/malformed token, parser failure, missing client id, and denied resource/action never call the handler and return the intended status;
- unary and stream paths enforce the same rules and enrich the stream context;
- an Eventun product method without permission metadata fails closed, while explicitly allowed health/reflection behavior remains available;
- a local `player_role = admin` or subject-less Client token no longer bypasses ClientService ownership checks;
- non-admin domain role behavior such as `gauntlet_creator` remains intact;
- AdminService no longer invokes remote role status or queries local admin role state;
- complete merged Swagger still has 115 paths, 133 operations, 286 current domain definitions unless generated permission metadata legitimately changes the definition inventory, and effective Bearer security covers all product operations.

## Implementation And Verification Sequence

1. Record the accepted F05 baseline, generated manifests, proto/RPC/security inventory, auth code paths, dependency reasons, and generated App UI/Unreal baselines before editing.
2. Add and generate the permission extension, annotate all methods, and add descriptor-inventory tests.
3. Implement the combined mandatory auth/actor interceptor and focused unary/stream tests. Make main installation unconditional.
4. Remove remote Admin authorization and local admin bypasses, simplify Admin wrappers, and add focused domain-boundary tests.
5. Prototype global Swagger security and compare structured specs and generated consumers before deleting operation-level blocks.
6. Update README, `.env.template`, durable API knowledge, and the manual permission-cutover checklist.
7. Run `go mod tidy`, regenerate, inspect all generated diffs, and update `scripts/generated.sha256` with the explicit manifest command after the API metadata change is accepted.
8. Run focused Go tests and vet while iterating, then the complete default `./scripts/verify.sh` workflow.
9. Run `./scripts/verify.sh appui` because Swagger security metadata changed.
10. If Docker is already running, run `./scripts/verify.sh unreal` and compare against the captured baseline. Do not start Docker without owner direction. If Docker is unavailable, do not claim Unreal equivalence or delete operation-level security based only on assumption; retain the blocks or obtain an explicit owner waiver and record the gap.
11. Run `git diff --check`, confirm no auth-disable or legacy admin-authorizer references remain, update F06 task status/evidence only after its done criteria pass, and stop for review.

## Constraints

- Do not begin F06B: no service-method moves, route moves, Unreal Client/GameServer/Models split, or generated plugin integration into the game client.
- Do not begin F07: do not create `cmd/eventun`, `app`, `api`, or `auth` packages and do not remove `internal/`.
- Do not change SQL, migrations, event schemas, team schemas, or product data.
- Do not create endpoint-specific permission resources, a custom IAM policy engine, a generic interceptor framework, or parallel actor contexts.
- Do not preserve the insecure environment branch or old role-authorizer code behind compatibility flags.
- Do not remove non-admin domain roles or broaden ClientService service-token privileges.
- Do not stage, commit, amend, reset, or modify the owner's accepted F05 index state.

## Completion Report

Before stopping, report:

- the permission proto source/path and exact Client, Server, and Admin resources;
- action counts by service and proof that all 133 methods are annotated;
- the real validator/parser construction, initialization behavior, and unary/stream interceptor order;
- player, dedicated-server, Studio Admin cookie, denied-principal, missing-annotation, and actor-context test evidence;
- every deleted legacy auth/configuration file, constructor dependency, environment variable, direct module, and local admin bypass;
- how ClientService owner/self/domain roles behave after removal of the admin shortcut;
- whether global Swagger security was accepted or retained operation-level blocks, with structured App UI and Unreal comparison evidence;
- the final manual Shared Cloud grant matrix, including the temporary dedicated-server Admin grant until F06B;
- generated manifest, focused tests, default verification, App UI verification, Unreal verification or explicit gap, and `git diff --check` results;
- all changed files and confirmation that F06B, F07, SQL, event contracts, team schema, and game-client integration were not started.

Stop for review after F06. Do not begin F06B or F07.
