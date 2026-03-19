---
name: next-day-summary
description: Generate a next-day work summary and task draft from Obsidian daily journal notes using the repository Rust tool.
---

# Next-Day Summary Skill

Use this skill when the user asks for:
- a next-day summary
- a daily work recap
- a task list draft based on recent daily notes

## Preconditions
- Daily notes exist at `40_work_tracking/daily/YYYY-MM-DD.md`.
- Notes should contain bullet lists under headings such as:
  - `## Work Completed`
  - `## Decisions`
  - `## Risks / Blockers`
  - `## Open Questions`
  - `## Candidate Next Tasks`

## Execution
Run:

```bash
cargo run --manifest-path ai/tools/next-day-summary/Cargo.toml -- --date YYYY-MM-DD
```

Optional lookback window:

```bash
cargo run --manifest-path ai/tools/next-day-summary/Cargo.toml -- --date YYYY-MM-DD --lookback-days N
```

## Outputs
- Summary: `40_work_tracking/summaries/YYYY-MM-DD-summary.md`
- Tasks: `40_work_tracking/tasks/YYYY-MM-DD-tasks.md`

## Review Step
After generation, review with the user and refine:
- priority order
- task scope
- owner and deadline annotations
