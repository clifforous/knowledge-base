# Battle Pass — Server-Side Data Model & XP Award Flow

Ascent Rivals · Season 1 · companion to *Battle Pass Progression Design*

This document specifies the persistent data, the post-match award flow, and the
correctness constraints for awarding Battle Pass XP server-side. It assumes the
match-result authority runs server-side and the client is display-only.

---

## 0. AccelByte Season Pass review note

This document describes a custom Ascent-owned server-side Battle Pass XP ledger
and progression model. It is not simply a wrapper around AccelByte Season Pass.

Current AccelByte Season Pass documentation also supports a platform-owned pass
model: the game can query the current season and player season state, a server
API can grant XP to a user, XP can advance tiers, and the client can claim season
pass rewards. If Ascent Rivals chooses AccelByte Season Pass as the source of
truth, the local tables in this document should either be replaced by AccelByte
Season Pass state or narrowed to an Eventun audit/idempotency ledger that records
why Eventun granted XP before calling AccelByte.

Eventun challenge rewards can reasonably award Battle Pass XP under that model.
The reward fulfillment path should call the AccelByte Season Pass XP grant API,
not the Platform item/currency fulfillment API. Current public docs show XP
grant as an amount-based server operation and do not show a caller-provided
transaction id, so Eventun should keep a local reward/grant ledger to prevent
duplicate XP grants before invoking AccelByte.

Relevant AccelByte docs:

- Season Pass overview: https://docs.accelbyte.io/gaming-services/modules/online/season-pass/
- Season Pass integration and server XP grant: https://docs.accelbyte.io/gaming-services/modules/online/season-pass/integrating-season-pass-to-your-game/
- Season Pass configuration: https://docs.accelbyte.io/gaming-services/modules/online/season-pass/configuring-season-pass/

---

## 1. Curve constants

A single source of truth, loaded once. Keep this server-authoritative; the client
may cache a copy for UI but never computes awards from it.

```cpp
// HGBattlePassConfig — data asset, one per season
struct FHGBattlePassTier
{
    int32 FirstLevel;     // inclusive
    int32 LastLevel;      // inclusive
    int32 XPPerLevel;
};

// Season 1 values
// Tier 1: levels  1-10  @ 1000  -> 10000
// Tier 2: levels 11-20  @ 1250  -> 12500
// Tier 3: levels 21-30  @ 1500  -> 15000
// Total pass cost: 37500 XP, 30 levels
```

Two helpers everything else is built on. Both are pure functions of the curve —
no I/O, trivially unit-testable.

```cpp
// Total XP required to be AT the start of a given level (level 1 == 0 XP).
int32 HGBattlePass::XPToReachLevel(int32 Level);

// Given a cumulative XP total, returns {Level, XPIntoLevel, XPForThisLevel}.
FHGBattlePassProgress HGBattlePass::ProgressFromTotalXP(int64 TotalXP);
```

Store **cumulative XP** as the source of truth, not level. Level is always derived.
This makes curve re-tuning safe: change the tiers, every player's level
recomputes correctly from their stored total.

---

## 2. Persistent data model

Three tables. The design goal is that the **per-source breakdown** survives, so
telemetry and anti-abuse work later, and that **every award is idempotent**.

### 2.1 `battlepass_progress` — one row per player per season

| Column            | Type     | Notes                                              |
|-------------------|----------|----------------------------------------------------|
| `player_id`       | uuid     | PK part 1                                          |
| `season_id`       | int      | PK part 2                                          |
| `total_xp`        | int64    | Cumulative. Source of truth. Level is derived.     |
| `xp_from_base`    | int64    | Running total — match participation                |
| `xp_from_perf`    | int64    | Running total — podium + circuit points            |
| `xp_from_daily`   | int64    | Running total — daily challenges                   |
| `xp_from_weekly`  | int64    | Running total — weekly challenges                  |
| `updated_at`      | timestamp|                                                    |

`total_xp` must always equal the sum of the four `xp_from_*` columns. Assert this
on every write — a mismatch means a bug in the award path.

### 2.2 `battlepass_xp_ledger` — append-only, one row per award event

This is what makes awards idempotent and auditable. Never updated, only inserted.

| Column          | Type      | Notes                                                  |
|-----------------|-----------|--------------------------------------------------------|
| `award_id`      | uuid      | PK                                                     |
| `idempotency_key`| string   | **UNIQUE**. See §3.1 for how it is constructed.        |
| `player_id`     | uuid      |                                                        |
| `season_id`     | int       |                                                        |
| `source`        | enum      | `base` / `perf` / `daily` / `weekly`                   |
| `amount`        | int       | XP granted by this event                               |
| `match_id`      | uuid?     | Set for base/perf; null for challenge claims           |
| `detail`        | json      | e.g. `{placement:1, circuit_points:48, capped:true}`   |
| `created_at`    | timestamp |                                                        |

The `UNIQUE` constraint on `idempotency_key` is the entire idempotency mechanism.
A duplicate insert fails at the DB layer; the award path catches that and treats
it as "already awarded, no-op."

### 2.3 `battlepass_challenge_state` — challenge progress & claims

| Column          | Type      | Notes                                                       |
|-----------------|-----------|-------------------------------------------------------------|
| `player_id`     | uuid      | PK part 1                                                   |
| `challenge_id`  | string    | PK part 2 — e.g. `daily_2026-05-25_finish3races`            |
| `season_id`     | int       |                                                             |
| `kind`          | enum      | `daily` / `weekly`                                          |
| `progress`      | int       | Current count toward the goal                               |
| `goal`          | int       | Target count                                                |
| `claimed`       | bool      | True once XP has been awarded for completion                |
| `expires_at`    | timestamp | Daily: end of UTC day. Weekly: end of the offered week.     |

`challenge_id` embeds the date/week so it is globally unique and naturally forms
a clean idempotency key when the challenge is claimed.

---

## 3. Post-match XP award flow

### 3.1 Idempotency keys

Every award event has a deterministic key. Re-running the same award produces the
same key, so the `UNIQUE` constraint absorbs duplicates.

```
base award:    "base:{match_id}:{player_id}"
perf award:    "perf:{match_id}:{player_id}"
daily claim:   "daily:{challenge_id}:{player_id}"
weekly claim:  "weekly:{challenge_id}:{player_id}"
```

Note `base` and `perf` are **separate** keys even though they come from the same
match. This lets them be awarded, retried, and audited independently.

### 3.2 The flow

The match-result authority hands the award service a result payload when a match
finishes. The award service does NOT trust any XP figure from the payload — it
receives only facts (placement, points, completion state) and computes XP itself.

```
ServerMatchAuthority
        |
        |  FHGMatchResult { match_id, season_id,
        |                   per-player: { completion, placement, circuit_points },
        |                   challenge_deltas: [ {player_id, challenge_id, +count} ] }
        v
HGBattlePassAwardService::ProcessMatchResult(result)
        |
        +--> for each player in result:
        |       1. Compute base XP   from completion state   (125 / 30 / 0)
        |       2. Compute perf XP   from placement + points (podium + 2.5/pt, capped)
        |       3. AwardXP(base)  with key base:{match}:{player}
        |       4. AwardXP(perf)  with key perf:{match}:{player}
        |
        +--> for each challenge_delta:
                5. Increment battlepass_challenge_state.progress
                6. If progress >= goal AND not claimed AND not expired:
                       AwardXP(challenge payout) with key {kind}:{challenge_id}:{player}
                       set claimed = true
```

### 3.3 `AwardXP` — the single choke point

Every XP grant in the game goes through exactly one function. One place to get
the transaction, the idempotency check, and the invariant assertion right.

```cpp
// Returns the player's new progress. Safe to call repeatedly with the same key.
FHGBattlePassProgress HGBattlePassAwardService::AwardXP(
    const FGuid& PlayerId,
    int32 SeasonId,
    EHGBattlePassSource Source,
    int32 Amount,
    const FString& IdempotencyKey,
    const FHGAwardDetail& Detail)
{
    // BEGIN TRANSACTION
    //
    // 1. INSERT into battlepass_xp_ledger with IdempotencyKey.
    //      - On UNIQUE violation: this award already happened.
    //        ROLLBACK, load current progress, return it. No-op. Not an error.
    //
    // 2. UPDATE battlepass_progress:
    //        total_xp        += Amount
    //        xp_from_<source> += Amount
    //
    // 3. ASSERT total_xp == xp_from_base + xp_from_perf
    //                       + xp_from_daily + xp_from_weekly
    //      - On failure: ROLLBACK, log loudly, alert. This is a code bug.
    //
    // COMMIT
    //
    // 4. Derive new level via ProgressFromTotalXP(total_xp).
    //    If level increased, enqueue reward-unlock events for the
    //    crossed levels (cosmetics, etc.) — also idempotent by level.
    //
    // 5. Return FHGBattlePassProgress to caller for client display.
}
```

Steps 1–3 are one transaction. Either the ledger row and the totals both land, or
neither does. The ledger insert happening *first* is deliberate: it is the lock.

---

## 4. Correctness constraints (the checklist)

- **Client never computes XP.** The payload carries facts (placement, points,
  completion), never an XP amount. The server is the only authority.
- **Every award is idempotent.** Duplicate match-result submissions, network
  retries, and reprocessing are all safe — the `idempotency_key` UNIQUE
  constraint makes a repeat a silent no-op.
- **No-show = 0 XP.** A race never entered awards nothing. This is what kills
  AFK-farming; enforce it in the base-XP computation, not the client.
- **Cumulative XP is the source of truth.** Level is always derived. Re-tuning
  the curve never corrupts stored progress.
- **Per-source totals always sum to total_xp.** Asserted inside the AwardXP
  transaction; a mismatch fails the write.
- **Challenge claims check `expires_at`.** A weekly cleared after its week must
  not pay out. The claim is gated on `not expired AND not claimed`.
- **Reward unlocks are idempotent by level.** Crossing level N enqueues the
  level-N unlock once, even if AwardXP is replayed.

---

## 5. Telemetry hooks

Emit these from `AwardXP` and a nightly job, from launch — not after:

- Per award event: `{player_id, source, amount, new_total, new_level}` — the
  ledger already is this; make sure it is queryable.
- Nightly snapshot: per-player `{level, total_xp, xp_from_*}` keyed by date.
- Headline dashboard metric: **distribution of player level at season day 30.**
  Target median is level 16–17. A median well below 16 means the pass is
  mistuned — trigger the global XP multiplier (see design doc §4.2) as the
  correction lever.
