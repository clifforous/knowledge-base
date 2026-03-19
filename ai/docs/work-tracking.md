# Work Tracking Workflow

## Purpose
- Standardize how work is recorded in daily journals, summaries, and task drafts.

## Daily Workflow
1. Journal work in `40_Work_Tracking/Daily/YYYY-MM-DD.md`.
2. Generate the next-day summary and task draft from recent daily notes.
3. Review and edit task priority before execution.

## Task File Guidance
- Prefer a new dated task file when priorities or assigned work have changed.
- Keep the active tasks short, reviewable, and specific enough to execute.
- Move low-priority or speculative work into a secondary section instead of mixing it into the priority list.

## Summary Generation Tool
Preferred command:

```bash
cargo run --manifest-path ai/tools/next-day-summary/Cargo.toml -- --date YYYY-MM-DD
```

Optional lookback:

```bash
cargo run --manifest-path ai/tools/next-day-summary/Cargo.toml -- --date YYYY-MM-DD --lookback-days N
```

Outputs:
- `40_Work_Tracking/Summaries/YYYY-MM-DD-summary.md`
- `40_Work_Tracking/Tasks/YYYY-MM-DD-tasks.md`

## Validation
- Review generated summaries and task drafts before treating them as final.
- Correct obvious omissions or stale priorities manually.
- Prefer dated notes over ad-hoc conversation history as the source of truth.
- Keep generated work-tracking notes free of conversation-thread-specific commentary.
