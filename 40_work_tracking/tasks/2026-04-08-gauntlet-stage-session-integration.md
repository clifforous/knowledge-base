# 2026-04-08 Gauntlet Stage Session Integration

**Status:** Planned / In Progress
**Project:** Ascent Rivals / Eventun / Dedicated Server / Game Client / Admin Web
**Primary repository:** `github.com/ikigai-github/eventun`
**References:**
- `30_designs/ascent-rivals/gauntlet-stage-orchestration-improvements.md`
- `50_knowledge/ascent-rivals/eventun/gauntlet-stage-runtime-contract.md`
- `50_knowledge/ascent-rivals/eventun/api.md`

---

## Eventun Backend

### Completed

- [x] Upgrade Go and AccelByte SDK to the current working baseline
- [x] Pass `RequestedRegions` to AccelByte session creation
- [x] Stop using display-stage values for stage allocation scheduling
- [x] Add durable `gauntlet_stage_session` attempt tracking
- [x] Add DB-backed create/reconcile flow for stage session ownership
- [x] Add minute-based sweep for recovery and deadline-based failure of stuck attempts

### Remaining

- [ ] Add `GetGauntletStageEligibility` for trusted dedicated-server reads
- [ ] Define the eligibility snapshot payload returned by `StageSessionId`
- [ ] Freeze eligibility per attempt so the DS can cache once and enforce locally
- [ ] Add `ReportGauntletStageStatus` for trusted dedicated-server updates
- [ ] Define and enforce allowed stage status transitions
- [ ] Persist dedicated-server-driven timestamps such as claimed, started, finished, and last heartbeat
- [ ] Update `ReportGauntletStageResults` to be stage-attempt aware and idempotent
- [ ] Consume participation only when Eventun accepts a completed stage attempt after race start
- [ ] Add `stage_session_id` support to accepted stage placements
- [ ] Add explicit cleanup behavior for failed attempts that already have an AccelByte session
- [ ] Add admin operations for retry / hold / defer / cancel / replace
- [ ] Add better observability for attempt state and repeated failure reasons

## Dedicated Server

- [ ] Read and validate gauntlet stage session attributes:
  - [ ] `GauntletId`
  - [ ] `GauntletStage`
  - [ ] `StageSessionId`
  - [ ] `StageSessionAttempt`
  - [ ] `StageSessionShardKey`
  - [ ] stage rule fields such as `EntryRequirement`, `AllowedTeams`, `MinCompetitors`, `MinLobbySize`, and `Circuit`
- [ ] Call `GetGauntletStageEligibility` on claim or startup and cache the response for the attempt
- [ ] Enforce gauntlet-stage admission rules for every join attempt using the cached eligibility snapshot
- [ ] Reject or kick unauthorized players immediately
- [ ] Ensure rejected players do not count toward lobby readiness or final standings
- [ ] Disable bot backfill for gauntlet stages unless the backend contract changes
- [ ] Require at least one human player or shut down the session cleanly
- [ ] Gate match start on valid qualified human thresholds
- [ ] Treat lobby join or pre-start presence as non-participation
- [ ] Treat mid-race disconnect as participation if the stage completes successfully
- [ ] Report `aborted(insufficient_players)` when the stage cannot validly start
- [ ] Report runtime failure conditions to Eventun once the status API exists
- [ ] Publish final standings through the stage-attempt-aware results API once it exists
- [ ] Keep sending trusted gameplay telemetry through `Server.Event`
- [ ] Define shutdown behavior after abort, failure, or successful completion

## Game Client

- [ ] Show gauntlet-stage join UI only when Eventun-backed qualification says the player is eligible
- [ ] Do not use public-session visibility as join permission
- [ ] Handle dedicated-server rejection with clear gauntlet-specific messaging
- [ ] Handle dedicated-server kick during admission or pre-start cleanly
- [ ] Refresh Eventun-backed gauntlet state after rejection, abort, completion, or failure
- [ ] Treat Eventun standings as authoritative after the stage ends
- [ ] Define UX copy for:
  - [ ] not qualified
  - [ ] stage already full / invalid for player
  - [ ] insufficient players
  - [ ] server failure / stage failed

## Admin Web Client

- [ ] Add stage-attempt views for gauntlet stages
- [ ] Show current attempt status and failure reason
- [ ] Show region, `StageSessionId`, attempt number, and AccelByte `session_id`
- [ ] Add manual retry control
- [ ] Add manual hold / resume control
- [ ] Add defer and cancel controls if backend support lands
- [ ] Show attempt history for a stage
- [ ] Surface timeout-driven failures clearly for live operations

## Decisions Still Needed

- [ ] Exact dedicated-server authentication model for `GetGauntletStageEligibility`, stage status, and final result calls
- [ ] Exact eligibility snapshot payload shape for the first production version
- [ ] Whether `deferred` should be manual-only or schedule-driven in the first production version
- [ ] Whether failed attempts should trigger immediate AccelByte session deletion
- [ ] Whether the first admin surface needs full controls or read-only visibility first

## Suggested Execution Order

1. Eventun: add `GetGauntletStageEligibility`.
2. Eventun: add dedicated-server status and final-results APIs.
3. Dedicated server: consume the eligibility snapshot and enforce allow or kick rules.
4. Game client: align gauntlet join UX and rejection handling with the runtime rules.
5. Admin web: expose attempt visibility and manual recovery controls.
