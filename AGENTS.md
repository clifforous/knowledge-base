# AGENTS

## Purpose
This repository is the canonical knowledge base for:
- Obsidian notes
- research and references
- architecture and design artifacts
- work tracking and execution planning

## Scope
- Knowledge, decisions, rationale, and references
- Work logs, daily summaries, and task planning
- AI prompts and skills for repository workflows
- No product implementation code except supporting local tooling

## Collaboration Rules
- Use a formal, technical tone.
- Be direct and concise.
- Do not be agreeable by default.
- Explicitly call out incorrect, risky, or low-quality proposals.
- Separate facts from assumptions.
- Explain tradeoffs when proposing alternatives.

## Preferred Workflow
1. Plan
2. Review
3. Iterate
4. Implement

Workflow guidance:
- Default to this sequence unless explicitly asked to skip it.
- For non-trivial changes, provide `Goal`, `Assumptions`, `Plan`, and `Review checkpoint` before implementation.
- Surface risks and weak assumptions during review, not after implementation.

## Engineering Standards
- Favor durable, reviewable notes over ad-hoc conversation artifacts.
- Keep changes minimal and verifiable.
- Prefer Rust for custom tools and skill-backed automation.
- Validate tooling outputs with concrete commands when possible.

## Repository Structure
- `00_Inbox/` quick capture and triage
- `10_Research/` exploratory analysis and findings
- `20_References/` durable reference material
- `30_Designs/` architecture and solution design docs
- `40_Work_Tracking/Daily/` daily journal notes
- `40_Work_Tracking/Summaries/` generated next-day summaries
- `40_Work_Tracking/Tasks/` active and planned task lists
- `90_Templates/` reusable note templates
- `ai/prompts/` reusable AI prompt snippets
- `ai/skills/` repository-local skills
- `ai/tools/` Rust tools used by skills

## Daily Workflow
1. Journal work in `40_Work_Tracking/Daily/YYYY-MM-DD.md`.
2. Generate next-day summary and task draft from recent daily notes.
3. Review and edit task priority before execution.

## Next-Day Summary Tool (Rust)
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

## External Integrations
- Notion data may be linked via MCP.
- Store external references as links with concise context and rationale.
