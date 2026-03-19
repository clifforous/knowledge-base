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
- Prefer lowercase folder names unless a mixed-case name is intentionally required for Obsidian presentation or a comparable concrete reason.
- Do not copy conversation-thread-specific notes into generated durable documents.
- Do not cite `00_Inbox/` files as sources in durable documents; inbox files are transient intake only.
- When citing source repositories under `/home/cgarvis/projects/genun/`, prefer the canonical GitHub repository reference over a local filesystem path.

## Repository Structure
- `00_Inbox/` quick capture and triage
- `10_Research/` exploratory analysis and findings
- `20_References/` durable reference material
- `30_Designs/` architecture and solution design docs
- `40_Work_Tracking/Daily/` daily journal notes
- `40_Work_Tracking/Summaries/` generated next-day summaries
- `40_Work_Tracking/Tasks/` active and planned task lists
- `50_Knowledge/` durable domain knowledge derived from research and execution
- `90_Templates/` reusable note templates
- `ai/docs/` AI-agent workflow and repository procedure docs
- `ai/prompts/` reusable AI prompt snippets
- `ai/skills/` repository-local skills
- `ai/tools/` Rust tools used by skills

## Additional Agent Context
- Read `ai/docs/README.md` for AI-agent-specific workflow docs.
- Use `ai/docs/inbox-processing.md` for ingesting transient inbox notes into durable repository artifacts.
- Use `ai/docs/work-tracking.md` for daily journal, summary, and task-draft workflow details.

## External Integrations
- Notion data may be linked via MCP.
- Store external references as links with concise context and rationale.
