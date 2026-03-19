# Inbox Processing Workflow

## Purpose
- Define how agents should convert transient inbox notes into durable work-tracking or knowledge-base artifacts.
- Prevent inbox notes from becoming a second unmanaged task system.

## Scope
- Primary source: `00_Inbox/notes.md`
- Optional future extension: other files placed under `00_Inbox/`

## Workflow
1. Review the inbox content and identify whether each item is:
   - completed work
   - an active task
   - secondary backlog
   - knowledge to record elsewhere in the repository
2. Review the most relevant current files before editing:
   - today's daily note in `40_Work_Tracking/Daily/`
   - today's or current task draft in `40_Work_Tracking/Tasks/`
   - related summaries if the inbox content fills a tracking gap
3. Convert the inbox content into durable notes:
   - completed work belongs in the daily journal and, when appropriate, the next summary cycle
   - active work belongs in a dated task file
   - backlog items belong in task notes or durable design/research notes, not in the inbox
4. Verify the destination files reflect the inbox content accurately and without duplication.
5. Clear the processed inbox file only after the user has explicitly approved that action.

## Rules
- Treat `00_Inbox/notes.md` as transient intake, not durable storage.
- Do not clear or delete inbox content until it has been ingested into the correct durable files.
- Do not update older dated task files with unrelated new work when a new dated task file is more accurate.
- Prefer creating a new dated task file when the work has shifted materially.
- Preserve facts separately from assumptions when rewriting inbox notes into durable documents.
- Do not include inbox files in a durable document's source list; use durable upstream sources or repository references instead.
- Do not copy conversation-thread-specific commentary into durable notes when ingesting inbox content.

## Source Referencing
- Use inbox content as transient intake to guide what should be captured, not as a durable citation target.
- When the inbox points to a source repository under `/home/cgarvis/projects/genun/`, cite the corresponding GitHub repository instead of the local path.
- Current canonical repository references:
  - `eventun`: `github.com/ikigai-github/eventun`
  - `accountun`: `github.com/ikigai-github/accountun`
  - `ascent-website`: `github.com/ikigai-github/ascent-website`
  - `ascentun`: `github.com/ikigai-github/ascentun`
  - `betun`: `github.com/ikigai-github/betun`
  - `handlun`: `github.com/ikigai-github/handlun`
  - `mintun`: `github.com/ikigai-github/mintun`
  - `website`: `github.com/ikigai-github/genun-website`

## Expected Outputs
- `40_Work_Tracking/Daily/YYYY-MM-DD.md`
- `40_Work_Tracking/Tasks/YYYY-MM-DD-tasks.md`
- optionally `40_Work_Tracking/Summaries/YYYY-MM-DD-summary.md`
- optionally research, design, or reference notes elsewhere in the repository

## Clearing Policy
- Clearing the inbox is permitted after:
  - the inbox items have been transferred into durable files
  - the user has given explicit permission to clear the processed file
- Clearing means leaving the intake file empty and ready for the next round of incoming notes.
