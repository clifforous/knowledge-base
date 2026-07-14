# ai/prompts

Reusable prompt templates and snippets.

## Current Eventun SQL Baseline

- Canonical empty-database schema files are `migration/a*.sql` through `migration/d*.sql`.
- `migration/migration.sql` is the stable filename for the sole current pending one-time delta against the deployed production baseline. Do not create numbered production migration files.
- Optional development fixtures use their own sequence: `t0_seed_courses.sql`, `t1_seed_sponsors.sql`, `t2_seed_gauntlets.sql`, and `t3_seed_teams.sql`.
- Canonical `d3_schedule_refresh_views.sql` safely no-ops when pg_cron is unavailable; guarded operational setup reapplies it after pg_cron provisioning.
- Disposable production-delta verification uses `production-delta --confirm-disposable-production-baseline=<target-fingerprint>` against an authentic disposable copy of current production.
- Completed foundation prompts are archived execution records. Their references to former `temp_migration*.sql`, `t0_migration.sql`, `t1_migration.sql`, or `t2`-`t5` fixture names are historical and must not be copied into a new worker prompt.

- `ascent-rivals/eventun-foundation-worker.md`: archived R01 token-integration removal worker prompt.
- `ascent-rivals/eventun-foundation-r02-worker.md`: archived WSL-native R02 Go toolchain and module-graph reset prompt.
- `ascent-rivals/eventun-foundation-f04-worker.md`: archived WSL-native F04 Extend App UI dependency-update prompt.
- `ascent-rivals/eventun-foundation-f05-worker.md`: WSL-native F05 avoidable runtime-dependency removal prompt.
- `ascent-rivals/eventun-foundation-f06-worker.md`: WSL-native F06 mandatory auth and coarse Eventun permission prompt.
- `ascent-rivals/eventun-foundation-f06a-worker.md`: WSL-native F06A player-authentication boundary simplification prompt.
- `ascent-rivals/eventun-foundation-f06b-worker.md`: coordinated Eventun/Unreal F06B service ownership and generated-consumer split prompt.
- `ascent-rivals/eventun-foundation-f12-rework-worker.md`: archived WSL-native F12 narrow-fact replacement and representative measurement prompt.
