# Eventun Progression

Status: current

Applicability: local-development

Scope: Eventun and the Ascent Rivals game client. This document does not imply production
deployment.

Last consolidated: 2026-07-19

## Purpose

Eventun owns player progression derived from accepted Ascent Rivals gameplay facts. The
current domain covers authored goals, achievements and challenges, immutable published
snapshots, player assignments and progress, completions, rewards, and AccelByte-backed
fulfillment.

Use this document for the current product and ownership model. Detailed ingestion and schema
mechanics remain in [identified match ingestion](identified-match-ingestion.md) and the
[data model](data-model.md).

## Runtime Model

- Operators edit draft goal and challenge-pool definitions.
- Player-facing runtime behavior reads immutable published goal and pool snapshots.
- Player progress, completion, assignment, and reward records retain the published snapshot
  that produced the outcome.
- Source-goal identity prevents duplicate completion of a non-repeatable goal across later
  publications.
- Challenge availability comes from membership in a published challenge-pool snapshot, not
  merely from a goal being marked as a challenge.
- Publishing validates requirements, rewards, pool membership, and assignment eligibility
  and creates the complete snapshot atomically.
- Goal title and description are localized presentation data. Requirement rules, metric
  codes, dimensions, and reward identities are not localized.

## Gameplay Input And Evaluation

- Progression consumes trusted server-derived narrow facts from the shared identified-match
  ingestion path. Client-reported facts are excluded from progression.
- Accepted server batches enqueue per-player career work in the same transaction.
- The worker serializes work per player, applies fact contributions, reconstructs applicable
  challenge windows, evaluates goals, and creates completion and reward records.
- Contributions retain the source batch, event, metric, dimensions, player, value, and
  occurrence time so repair cannot silently change already-derived outcomes.
- Current counter-style metrics include medal, kill, completed-heat, completed-match, and
  podium counts where their counter builders are implemented. Unsupported metric or counting
  policy combinations must not become publishable runtime content.
- The production cutover deliberately starts the replacement contribution ledger empty while
  retaining completed progress, completion records, published snapshots, and reward history.

## Challenges And Client Surface

- Assignments are player-scoped and may be daily, weekly, monthly, or seasonal.
- Current-period completed assignments remain part of the active challenge response until
  their period expires.
- The game client's `UHGChallengesSubsystem` consumes Eventun `MyActiveChallenges` and exposes
  assignment, lane, progress, and reward-preview view models to the existing challenge UI.
- AccelByte Challenges and Achievements are not dependencies for this product model.

## Rewards

- A completed published goal may create one reward bundle containing multiple entries;
  intentionally rewardless goals create no bundle.
- Eventun records completion durably before external reward delivery and tracks fulfillment
  attempts independently.
- Current external fulfillment can grant configured player items, ARC/currency, and Battle
  Pass XP through AccelByte.
- Eventun owns validation and fulfillment policy. Operator UIs should use Eventun's normalized
  catalog and reward APIs rather than call AccelByte catalog services directly.
- Team XP, team contribution, and team cosmetic entitlement are not part of the current
  player-scoped progression implementation.

## Authoring And Administration

- Eventun's Extend App UI is the intended operator surface for progression authoring and
  support workflows.
- The current authoring direction uses editable drafts and explicit publish operations rather
  than treating row-level active flags or goal-version activation as the durable runtime
  invariant.
- Goal and challenge-pool administration, validation, preview, import/export, localization,
  reward inspection, and retry remain at different implementation stages. Consult the active
  [progression initiative](../../initiatives/eventun-progression/README.md) before assuming an
  operator workflow is complete.

## Current Boundaries

- Progression is player-scoped. Proposed team progression belongs to the
  [teams and team gauntlets initiative](../../initiatives/teams-and-team-gauntlets/README.md).
- Published snapshots are durable history; ordinary draft edits must not rewrite prior player
  outcomes.
- Item-specific requirements must use the facts actually emitted by the current producer.
  Historical source goals whose published requirements use incompatible part or weapon
  dimensions are retired during cutover rather than guessed or remapped.
- Sender retry, full historical recomputation, and broad telemetry-retention policy are
  separate decisions from progression evaluation.

## Evidence And History

- [Identified match ingestion](identified-match-ingestion.md)
- [Eventun API](api.md)
- [Eventun data model](data-model.md)
- [Game client](../game-client.md)
- [Progression design archive](../../archive/initiatives/eventun-progression/README.md)
