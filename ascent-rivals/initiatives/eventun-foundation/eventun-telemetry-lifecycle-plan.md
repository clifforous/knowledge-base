# Eventun Telemetry Lifecycle Plan

**Status:** Initial season implementation, the single combined local historical-and-season rehearsal, and retained-data API/performance smoke are complete. Physical retention and archive decisions remain deferred.

**2026-07-17 implementation:** Eventun owns explicit finite regular/off-season windows managed through its Extend App UI. Non-overlapping half-open windows may have gaps; uncovered matches are unseasoned and still contribute to lifetime behavior. Server facts resolve nullable season identity from MatchStart. Client facts are season-eligible only when MatchStart and trusted batch receipt resolve to the same non-null season; this deliberately replaces the earlier occurrence-time-only statement. Seasons remain separate from PostgreSQL storage segments, retention tiers, game builds, AccelByte Season Pass, and MMR ownership. The accepted checkpoint is recorded in [[ascent-rivals/sources/analysis/eventun-insights-progression-seasons-review]].

## Related

- [Development cutover and runtime hardening](development-cutover-and-runtime-hardening.md)
- [[ascent-rivals/system/eventun/data-model|Eventun data model]]
- [[ascent-rivals/sources/analysis/eventun-foundation-api-simplification-review|Eventun foundation and API simplification review]]
- [[ascent-rivals/sources/analysis/eventun-team-postgresql-derivation-review|Eventun PostgreSQL derivation review]]
- [[ascent-rivals/decisions/README|Ascent Rivals decision log]]

## Decision Boundary

No current product decision yet defines:

- how much per-match detail remains queryable for older history;
- how long raw telemetry remains in PostgreSQL;
- the archive format, storage provider, or restore process; or
- any additional retention-oriented PostgreSQL partition key or segment boundary beyond the implemented source/event-type hierarchy.

The implemented logical model adds an Eventun season catalog and season-aware read/projection behavior without requiring producers to submit a period id or partitioning telemetry by season. The earlier `competition_period_id` proposal conflated product and storage responsibilities that have different lifecycles. This does not retire the existing client/server and event-type partitions, which are query-performance structures rather than season-retention policy.

## Delivery Sequencing

The one permitted production-scale combined local historical-and-season rehearsal completed successfully against the retained pre-cutover dump. It committed 3,219 reconstructed match facts, left converted history explicitly unseasoned, recorded match/player serving generation `2/2`, preserved gauntlet and sealed qualification generation `1/1`, and reconciled all 12 historical comparison rows as explained. The migrated isolated database and a resettable post-cutover dump were retained, and the API smoke matrix passed against ported history plus temporary season rows before restoring the catalog to empty. Production rehearsal is refreshed later against the final release delta and a current dump; this local run did not deploy or mutate a shared development or production database.

The retained-data performance pass also exercised the exact player-facing read shapes. Match History now starts from source/player-selective facts and uses keyed match/artifact lookup. Lifetime and seasonal leaderboards assemble all course/category groups set-wise and resolve `player_view` once per request rather than once per group. The authentic 11-course lifetime leaderboard measured 36.313 ms SQL p95 and 25.862 ms handler p95 with 730 shared-hit buffers; Match History remained below 3.4 ms handler p95 at limits 30 and 100. These are implementation and capacity observations, not durable product latency guarantees or a reason to couple seasons to physical storage.

Live production comparisons are optional sanity checks rather than equality gates: exact older match facts should remain stable, totals may increase, best times may improve, standings may move, and presentation may change after the dump cutoff.

## Terminology

| Concept | Meaning | Current decision |
|---|---|---|
| Product season | Eventun-owned finite regular/off-season product window | Non-overlapping half-open windows may have gaps; uncovered matches are unseasoned |
| Statistics scope | Comparability boundary for a particular record or leaderboard | Initial season scope covers best lap, best finish, and their ranks while lifetime records remain |
| Telemetry storage segment | Physical unit used to partition, detach, export, or delete raw events | Partition strategy is undecided and need not match seasons |
| Retention tier | Amount and location of retained detail over time | Exact tiers and durations are undecided |
| Game build | Producer build or release identifier used for diagnostics and later classification | Preserve independently of all four concepts above |

These concepts may eventually share boundaries, but that must be an explicit product and operations decision rather than a schema assumption.

## Stable Foundation

The implemented identified-ingestion foundation remains useful without a season model:

- stable batch and event ids;
- deterministic producer sequence;
- client/server source attribution;
- session and match identity;
- event occurrence and receipt timestamps;
- producer client and submitting-player attribution where available;
- `game_build` or equivalent diagnostic build context;
- canonical payload hashes and idempotent duplicate handling; and
- replay association through a separate match-artifact record.

This metadata permits an additive season implementation to classify matches without changing producer contracts. Historical conversion does not invent seasons; retained matches remain unseasoned unless a later reviewed repair classifies them.

## Source Trust

Dedicated-server and client submissions have intentionally different trust properties:

- `server` means the shared ingest operation accepted the batch from an exactly subjectless caller with Eventun Server `CREATE`, and is the higher-trust source for server-hosted competition;
- `client` means the batch was accepted from an authenticated player client, but the gameplay payload remains self-reported and potentially modifiable; and
- client events remain required for time trials and other play that does not use a dedicated server.

Eventun derives source from the verified actor class on the shared operation. Producers do not select or upgrade their own trust classification. Accepted events and all derived facts retain source provenance so each leaderboard, qualifier, progression rule, insight, or reward policy can explicitly choose which sources it accepts.

Long-term client-event validation should seek useful confidence without replaying every match on a dedicated server. Investigation candidates include deterministic event-sequence and physics/plausibility checks, binding batches to authoritative session context or server-issued nonces, lightweight replay or ghost checksums, anti-cheat/platform signals, anomaly detection, selective audit, and quarantining suspicious records. No mechanism is selected yet, and full dedicated-server replay is not the default plan because of its resource and implementation cost.

## Provisional Lifecycle

### 1. Preserve Detailed Source Data

Keep accepted raw telemetry and compact derived facts while the game is pre-alpha and data volume is low. Do not destructively roll up or discard source events before historical product requirements and restore tooling are defined.

Identified match ingestion now exposes one logical `game_event` relation while preserving physical pruning by client/server source and event type. The current schema has demonstrated query benefits from that layout, and many hot queries address event-type leaves directly. Do not replace it with an unpartitioned payload table without representative query-plan and latency evidence. Do not add a placeholder period id whose only value is effectively `current`.

### 2. Define Product History

Before the first deliberate season boundary, complete product decisions for:

- MMR rollover ownership and procedure.

Season splitting and reassignment between already attributed seasons are low-priority recovery considerations, not initial administration features. Invalid facts caused by gameplay or telemetry bugs require targeted fact/contribution repair and projection rebuilds rather than artificial season boundaries.

Historical API/UI availability is separate from whether raw telemetry still exists in an archive.

### 3. Define Statistics Classification

Implement nullable Eventun season attribution on compact match facts from the accepted batch MatchStart. Keep the existing lifetime record and career projections, and add explicit season projections only for the selected record families. Do not generalize the initial work into a universal statistics-scope or producer-supplied period contract.

Do not assign seasons to the initially converted retained matches. Validate representative leaderboard, career, gauntlet, progression, and insight outputs with those facts remaining unseasoned. A later reviewed repair may classify previously unseasoned facts from authoritative MatchStart time; ordinary season creation never performs that reassignment implicitly.

### 4. Measure And Select Storage Segments

Preserve source/event-type partitioning as the initial query-performance layout. Choose any additional retention-oriented storage segmentation only after measuring row volume, index size, ingest cost, hot-query predicates, partition count, and expected detach cadence. A time range, release boundary, season boundary, or a combination may be appropriate. Storage segmentation must optimize operations and query pruning; it must not define gameplay semantics.

### 5. Add Retention Tiers And Archive Recovery

A plausible future model is high-detail relational access for the current and recent history, durable compact summaries for older history, and compressed raw telemetry in lower-cost object storage. This is a hypothesis, not an approved duration or product promise.

Before deleting relational raw events, the archive process must provide:

- immutable manifests, row counts, checksums, source ranges, and build coverage;
- a documented payload transformation policy without permanent payload schema-version branches;
- a tested restore or reprocessing path into an isolated database;
- reconciliation against retained facts and historical outcomes; and
- confirmation that authoritative competition results and awarded progression are retained independently.

## Scale Planning Reference

The following scenario is an illustrative long-term scalability goal, not a forecast, launch requirement, or claim that the current PostgreSQL tier can sustain it:

- 200,000 concurrently playing users;
- 16 players per full lobby;
- one complete match every 180 seconds, including the full match cycle;
- exactly one accepted authoritative batch per match; and
- an illustrative 100 events per complete match.

At steady state those assumptions imply:

| Quantity | Approximate rate |
|---|---:|
| Simultaneous matches | 12,500 |
| Completed matches and accepted batches | 69.4/second; 6.0 million/day |
| Player-match outcomes | 1,111/second; 96 million/day |
| Events at 100 events/match | 6,944/second; 600 million/day |
| Identified-ingest base rows at 100 events/match | 1.206 billion/day: one batch row plus identity and payload rows |
| Broad event-index insertions at seven entries/event | 48,600/second before event-specific indexes |

The event count is the least certain assumption. Complete matches containing multiple heats, laps, players, and checkpoints may produce far more than 100 events. If every player independently submits the complete match instead of one authoritative producer doing so, batch and event rates increase by a factor of 16. Real capacity planning must measure occupancy, matchmaking and loading time, match duration, source mix, event-type distribution, events per match, retries or duplicates, and payload-size percentiles.

Storage sensitivity at 600 million events/day is:

| Assumed retained bytes per logical event | Approximate growth/day |
|---|---:|
| 100 bytes | 60 GB |
| 300 bytes | 180 GB |
| 500 bytes | 300 GB |
| 1,000 bytes | 600 GB |

These values are dimensional examples, not measured Eventun row sizes. Physical PostgreSQL consumption includes the identity and payload heaps, tuple and page overhead, indexes, free space and bloat, and derived facts. WAL, replicas, backups, and exported archives add further storage or transfer cost. The identified-ingest model creates two event rows and several index entries even when the JSON payload is small, so changing JSON format alone cannot remove the fixed relational and identity cost.

Detailed fact volume can also exceed raw match volume. With `H` heats, `L` laps per heat, and `C` checkpoints per lap, the scenario produces approximately `1,111 * H * L * C` player-checkpoint facts per second. For `H=3`, `L=3`, and `C=10`, that is approximately 100,000 checkpoint facts per second. Retention planning must therefore cover detailed facts and identity ledgers as well as raw payloads.

This scale remains compatible with sub-second product reads only if normal APIs use bounded typed facts and projections rather than scanning lifetime raw or fact history. Candidate read models include one current record per player, course, source policy, and statistics scope; current player and player-course statistic summaries; bounded recent match history; and rebuildable leaderboard or rank snapshots. Match-local insights can join facts for one identified batch. Raw telemetry and archived detail are evidence and reprocessing inputs, not the ordinary best-lap, career, leaderboard, or post-match query path.

Before treating this scenario as an engineering target, collect representative measurements for:

- `pg_column_size` distributions for each payload and event type;
- heap, TOAST, and index bytes per accepted event and batch;
- WAL bytes and transaction latency per accepted match;
- derived rows and derivation time per match;
- hot-query `EXPLAIN (ANALYZE, BUFFERS)` results and latency percentiles; and
- restore, reprocessing, and reconciliation throughput.

## Archive Format Evaluation

Reprocessing and offline analytics favor different physical formats. Do not select one format merely because it is best for the other workload.

| Need | Candidate direction | Benefits | Costs and proof required |
|---|---|---|---|
| Exact restore, audit, and deterministic reprocessing | Immutable complete-match envelopes grouped into compressed objects, using canonical JSON/JSONL plus Zstandard or another proven row-oriented batch encoding | Preserves batch identity, event order, source evidence, and a directly inspectable representation; repeated keys compress across many records | Less efficient for selective analytical scans; must prove canonical-hash preservation or documented rewriting, restore, and current-derivation compatibility |
| Compact replay-oriented recovery | Versioned protobuf or another binary match bundle with pinned descriptors and tooling | Compact and efficient to decode | Schema evolution, unknown-field behavior, canonical hashing, and long-term tool availability must be proven; do not introduce permanent producer payload-version branches |
| Offline analytical scans | Rebuildable Parquet datasets with columnar compression such as Zstandard, derived from typed facts and selected raw metadata | Column pruning and compression suit large scans and aggregate analysis | Not automatically an exact round-trip representation of accepted payloads; should not be the sole recovery copy unless reconstruction and reconciliation are demonstrated |

A plausible hybrid is a canonical compressed match archive for recovery and reprocessing plus rebuildable Parquet fact datasets for analytics. This is an evaluation direction, not an approved duplication policy, provider, encoding, compression setting, object layout, or retention duration.

Archive manifests should record at least object hashes, format and compression, batch and event counts, stable-id ranges or coverage, source and time coverage, game builds, export and rewrite tool revisions, the current fact/projection definition used for reconciliation, and expected reconciliation targets. Archive-level format and tool revisions belong in the manifest rather than requiring producers to carry permanent payload schema-version fields or retaining parallel fact revisions online.

The restore acceptance test should load selected objects into an isolated database, verify checksums and counts, apply any explicitly versioned rewrite to the retained payload shape, derive the one current narrow fact set and incremental projections, and reconcile retained facts, authoritative competition outcomes, and awarded progression. No source relation or partition should be deleted until this path succeeds on representative data.

## Deferred Decisions

| Decision | Required before |
|---|---|
| Season duration and system of record | First player-facing season configuration |
| Statistics-scope boundaries and ownership | Seasonal/reset leaderboard or record behavior |
| Historical match-detail product policy | Removing detailed history from normal APIs |
| PostgreSQL partition key and rollover process | Creating the second storage segment or when measured scale requires partitioning |
| Hot, warm, and cold retention durations | First destructive removal from PostgreSQL |
| Archive format, location, and restore tooling | First raw-event export or deletion |

These decisions are not prerequisites for teams. They become prerequisites only for features that promise seasonal comparison, historical detail, or destructive telemetry retention.
