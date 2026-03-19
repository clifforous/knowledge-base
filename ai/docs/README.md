# AI Docs

Purpose:
- Store procedural guidance intended specifically for AI agents working in this repository.
- Keep `AGENTS.md` as the top-level policy file and move lower-level workflow details here.

Current documents:
- `ai/docs/inbox-processing.md`: how to ingest `00_Inbox/notes.md` into durable repository artifacts.
- `ai/docs/work-tracking.md`: how to maintain daily notes, summaries, and task drafts.

Usage:
- Read `AGENTS.md` first for repository-wide rules.
- Read the relevant `ai/docs/*.md` file when the task depends on repository workflow details.

Documentation constraints:
- Generated durable notes must not include conversation-thread-specific notes or assistant/user exchange artifacts.
- `00_Inbox/` content may inform synthesis, but inbox files must not be cited as durable sources.
- When referencing repositories from `/home/cgarvis/projects/genun/`, cite the GitHub repository rather than the local path.
