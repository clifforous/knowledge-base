---
name: ascent-rivals-kb-research
description: Ground Ascent-Rivals product and technical requests in this repository knowledge base before proposing solutions. Use when the user mentions Ascent-Rivals or asks about game features, stats, websites, architecture, or integrations.
---

# Ascent-Rivals KB Research Skill

Use this skill when the user asks for:
- Ascent-Rivals research, planning, or architecture help
- website or dashboard proposals for game stats
- feature design that depends on existing game context
- integration decisions across game client, backend services, and documentation

## Primary Sources
- `20_references/ascent-rivals/` for source captures and indexing
- `10_research/` for synthesized findings
- `30_designs/` for architecture and decision docs
- `40_work_tracking/daily/` only when recent execution state matters

Start with `20_references/ascent-rivals/SOURCE_INDEX.md` when present.

## Workflow
1. Scope the request.
- Identify requested output and relevant domain areas (gameplay, stats, backend, client, UI).

2. Collect evidence.
- Use `rg` over the primary source paths with domain-specific keywords.
- Read only relevant files and prefer most recent dated notes when conflicts exist.

3. Build context summary.
- List confirmed facts with file evidence.
- List assumptions and missing information separately.

4. Produce the response or proposal.
- Tie recommendations directly to evidence.
- For new website/stats requests, include candidate metrics/entities, likely source systems, and integration boundaries.
- Call out risks and unresolved unknowns.

5. Persist artifacts when requested.
- Analysis and durable knowledge notes -> `50_knowledge/ascent-rivals/`
- Design decisions -> `30_designs/ascent-rivals/`
- Raw imported material -> `20_references/ascent-rivals/`

## Quality Bar
- Separate facts from assumptions explicitly.
- Flag weak or stale evidence.
- Do not invent gameplay or data-model details not supported by sources.
- Keep outputs concise, reviewable, and verifiable.
