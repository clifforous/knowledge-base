# Knowledge Base

## Purpose

This repository is a personal, project-first knowledge base. It preserves current system
understanding, proposed initiatives, decisions and rationale, and supporting sources in
portable Markdown.

## Projects

- [Ascent Rivals](ascent-rivals/README.md)
  - Current gameplay, client, backend, website, platform, and integration knowledge.
  - Proposed product and engineering initiatives.
- [Knowledge Base](knowledge-base/README.md)
  - Repository organization, migration, and the proposed federated kb workflow.

## Reading Order

For a current-state question:

1. Open the relevant project index.
2. Read the applicable `system/` document.
3. Consult decisions for rationale and sources for evidence when needed.
4. Read initiatives only for proposed or in-progress behavior.
5. Read archive only for historical questions.

## Repository Roles

Each project may contain:

- `system/`: accepted current behavior for the document's stated applicability
- `initiatives/`: intended changes not yet fully incorporated into current truth
- `decisions/`: concise decision history and task-owned decision evidence
- `sources/`: durable references, observations, and supporting analyses
- `archive/`: inactive historical material excluded from default retrieval

Temporary local material belongs in ignored `scratch/` and must not be cited as a durable
source.

The durable placement, lifecycle, metadata, indexing, and decision-log rules are defined in
[ORGANIZATION.md](ORGANIZATION.md).
