# Eventun Foundation F06A Coding Worker

Use this prompt from the existing VS Code session attached directly to the Eventun WSL workspace.

---

You are continuing the Ascent Rivals Eventun foundation reset in the native WSL checkout. Implement only `F06A: Simplify The Player Authentication Boundary`, verify it, update durable documentation and task evidence, and stop for review. Do not begin F06B's service-method moves or Unreal consumer split, F07's package reorganization, or any teams feature work.

## Read First

Read and follow Eventun's `AGENTS.md`. Inspect the current branch, index, worktree, recent commits, and every existing diff before editing. Then read these knowledge-base documents as accepted decisions:

- `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`, especially F06, F06A, and F06B
- `50_knowledge/ascent-rivals/eventun/api.md`, especially Authentication And Permission Model
- `10_research/ascent-rivals/eventun-foundation-api-simplification-review.md`, especially Shared Cloud IAM

At prompt preparation time, the accepted F06 implementation is still an uncommitted Eventun working-tree diff. F06A intentionally revises part of that implementation. Work on top of it; do not reset, discard, stage, commit, or rewrite unrelated owner changes.

## Validated Context And Fixed Decisions

- Live Shared Cloud testing confirmed that the current player permission works after adding `CUSTOM:NAMESPACE:{namespace}:EVENTUN` to the game namespace's Default User Role Override.
- Eventun's confidential client already has IAM Roles Read and Basic Namespace Read.
- The working mechanism is nevertheless the wrong product boundary: every player receives all Client actions, so the custom permission adds no authorization distinction beyond a valid user token.
- ClientService must instead require mandatory AccelByte authentication against `AB_NAMESPACE`, a non-empty `client_id`, and a non-empty user `sub`. It must not perform an Eventun IAM permission lookup.
- A subjectless service token must be rejected by ClientService. A Studio Admin user token may have a `sub`, but it receives no ClientService domain bypass; ordinary ownership and role checks still apply.
- ServerService retains `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN:SERVER` and per-method actions.
- AdminService retains `CUSTOM:ADMIN:NAMESPACE:{namespace}:EVENTUN` and per-method actions. Shared Cloud Studio Admin tokens are expected to satisfy this resource without modifying the built-in role. Trusted service clients still need explicit client grants.
- Eventun's own confidential client retains IAM Roles Read and Basic Namespace Read because Admin user permission resolution still needs them.
- Authentication remains unconditional. Health and reflection remain the only explicit gRPC bypasses.
- Keep the accepted global Swagger Bearer security and all current service ownership and routes.
- Keep all Eventun domain authorization: self, wallet ownership, team owner/manager/hierarchy, gauntlet creator, and other non-admin roles. Do not restore the deleted local `admin` bypass or remote role-status authorizer.
- Breaking pre-alpha cleanup is allowed. Delete obsolete Client permission metadata and tests rather than retaining compatibility behavior.

## Required Implementation

### 1. Make Authentication Policy Explicit Per Service

- Refactor the current method-permission lookup into the smallest clear service policy:
  - ClientService authenticates with `validator.Validate(token, nil, &namespace, nil)` and requires `sub`.
  - ServerService and AdminService continue resolving and validating their annotated permission.
  - Unknown product services and malformed Server/Admin permission metadata fail closed as Internal.
  - Health and reflection retain their explicit bypass.
- Preserve Bearer and Admin Portal `access_token` cookie extraction, `cookie` and `grpcgateway-cookie`, Authorization precedence, unary/stream parity, claims context, raw token context, and client-id context.
- Require non-empty `client_id` on all product surfaces.
- Treat a valid ClientService token without `sub` as an authenticated but disallowed principal and return PermissionDenied before the handler.
- Do not add a replacement role lookup, client allowlist, local player role, or endpoint-specific IAM policy for ClientService.

### 2. Remove Only The Client Permission Contract

- Remove the Client resource/action options from all ClientService methods and remove the permission proto import from `client.proto` if no longer used there.
- Remove `ClientPermissionResource`, Client descriptor/action inventories, and tests that require Client permission annotations.
- Retain `permission.proto`, its generated Go artifacts, and all AdminService and ServerService annotations because those two surfaces still enforce permissions.
- Descriptor tests must prove that ClientService methods have no permission metadata and that every Server/Admin method has exactly one valid expected resource and action.
- Preserve all RPCs, HTTP routes, operation ids, messages, schemas, top-level Bearer security, and service ownership.

### 3. Improve Validation Failure Observability

- Preserve token-safe structured logs for the original SDK validation failure. Include the gRPC method/service and required resource/action when applicable, but never log the token, cookie, complete claims, client secret, or other credentials.
- Invalid or unverifiable tokens return Unauthenticated.
- A token that authenticates but lacks a required Server/Admin permission returns PermissionDenied.
- Do not expose internal IAM dependency details to callers. Make them visible in server logs so lookup failures are distinguishable from genuine denied permissions.
- Keep the implementation direct. Do not introduce a generic policy framework, dependency-injection container, or parallel claims model.

### 4. Update Deployment And Durable Documentation

- Remove the Default User Role Override Eventun grant from README and deployment instructions. Do not require disabling the entire override if it contains unrelated permissions.
- Retain the dedicated-server Server grant, temporary dedicated-server Admin grant required until F06B, Studio Admin behavior, trusted backend Admin grants, and Eventun service-client IAM Roles Read and Basic Namespace Read.
- Update `50_knowledge/ascent-rivals/eventun/api.md` from the pending F06A target to implemented current behavior.
- Update F06A status and implementation evidence in `40_work_tracking/tasks/2026-07-10-eventun-foundation-and-teams.md`. Do not mark the live Shared Cloud smoke criterion complete unless the owner supplies that evidence.
- Do not rewrite F06's historical completion evidence; add F06A evidence separately.

## Required Tests

Use the existing injected validator interface and fakes. Tests must not require live IAM.

At minimum prove:

- ClientService calls validation with a nil permission and a valid user token reaches unary and stream handlers with complete actor context.
- A valid ClientService token without `sub` returns PermissionDenied and never reaches the handler.
- Invalid token, missing token, missing metadata, and missing `client_id` remain rejected before the handler.
- ClientService methods require no permission descriptor metadata.
- Every AdminService and ServerService method still has the expected resource and a valid action; missing or malformed metadata still fails closed.
- Server/Admin allowed and denied permission behavior is unchanged, including Bearer/cookie precedence and stream context behavior.
- Client domain authorization remains in force and a local `player_role = admin` or service token cannot bypass it.
- Swagger still has 115 paths, 133 operations, the accepted definitions inventory, and effective top-level Bearer security on every product operation unless generation demonstrates a legitimate metadata-only inventory change.
- Generated App UI and Unreal API shapes do not gain or lose operations because Client permission annotations were removed.

## Verification

1. Run focused auth, descriptor, authorization-boundary, and Swagger tests while iterating.
2. Regenerate through the existing scripts and update `scripts/generated.sha256` only for accepted deterministic output changes.
3. Run `go mod tidy` only if imports changed, and confirm the module graph has no unrelated churn.
4. Run the complete coder-owned `./scripts/verify.sh` workflow.
5. Run `./scripts/verify.sh appui` because protobuf metadata and generated specifications changed.
6. Do not start Docker. If Docker is already running, run `./scripts/verify.sh unreal`; otherwise record the Unreal verification gap and compare generated specifications using the available deterministic checks.
7. Run `git diff --check` and targeted searches proving no Client resource, Client permission annotation, or default-user Eventun grant remains outside F06's historical task evidence.
8. Inspect the final diff for accidental F06B, F07, SQL, migration, event-contract, team, or game-client changes.

The owner-controlled post-deployment smoke test is:

1. Remove only the Eventun Client custom permission from the Default User Role Override.
2. Restart/redeploy Eventun and obtain a fresh normal player token.
3. Confirm a ClientService read such as PlayerMe succeeds.
4. Confirm a subjectless service token is rejected by ClientService.
5. Separately confirm a fresh Studio Admin token reaches a read-only AdminService endpoint without any role modification.

Do not perform Shared Cloud configuration changes unless the owner explicitly asks you to do so and provides the authenticated environment.

## Constraints

- Do not begin F06B: no method or route moves, Unreal Client/GameServer/Models split, or game-client plugin integration.
- Do not begin F07: do not create `cmd/eventun`, `app`, `api`, or `auth` packages and do not remove `internal/`.
- Do not change SQL, migrations, event schemas, team schemas, product behavior, or downstream integrations.
- Do not remove Server/Admin permissions or weaken mandatory authentication.
- Do not restore insecure operation, borrowed AccelByte admin-role checks, or Eventun-local admin bypasses.
- Do not stage, commit, amend, reset, or discard owner changes.

## Completion Report

Before stopping, report:

- the final Client, Server, and Admin authentication/authorization policy;
- all removed Client permission annotations, constants, grants, generated metadata, and tests;
- proof that all Client methods are annotation-free and all Server/Admin methods remain correctly annotated;
- player-subject, subjectless-service-token, invalid-token, Server/Admin permission, unary/stream, and domain-authorization test evidence;
- safe validation-error logging behavior;
- generated Swagger/App UI/Unreal comparison evidence;
- default, App UI, Unreal-or-gap, module, generation, and diff-check results;
- documentation and task-status changes;
- the exact owner-controlled Shared Cloud smoke checks still pending;
- confirmation that F06B, F07, SQL, migrations, event contracts, teams, and game-client integration were not started.

Stop for review after F06A. Do not continue to F06B or F07.
