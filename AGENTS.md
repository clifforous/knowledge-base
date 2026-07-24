# AGENTS

## Repository Contract

This is Cliff's personal durable knowledge base. Read and follow
[ORGANIZATION.md](ORGANIZATION.md) for the complete taxonomy, lifecycle, metadata,
decision-log, indexing, and validation rules.

This repository contains current system knowledge, initiatives, decisions, sources, and
selected history. It is not a general task manager, prompt archive, daily journal,
transcript store, or product-code repository.

## Retrieval

- Start with the root `README.md`, then the owning project `README.md` and relevant `system/`
  index.
- Treat `system/` as the default current answer for its stated applicability.
- Treat `initiatives/` as proposed or in progress; approval, implementation, merge, submit, or
  canon adoption does not prove production deployment.
- Use `decisions/` for rationale, `sources/` for evidence, and `archive/` only for history or
  a clearly labeled evidence link.
- Preserve project, role, source identity, applicability, contradictions, and known gaps when
  synthesizing results.

## Placement And Updates

- Route by owning project and durable role, not document format, vendor, protocol,
  implementation repository, or the activity that produced the information.
- Put accepted current behavior in `system/`; unfinished change in one named initiative;
  material rationale in `decisions/`; evidence in `sources/`; inactive useful history in
  `archive/`; temporary work in ignored `scratch/`.
- Search existing knowledge before adding a document. Prefer a concise update to the closest
  existing subject over a new fragmented note.
- Make current-system documents self-sufficient. Separate implemented facts, known gaps, and
  future direction, and write them as reference chapters rather than implementation logs.
- Write for a technically curious teammate without recent task context. Start with the mental
  model, explain specialized terms, and do not sacrifice useful teaching prose merely to minimize
  word count.
- Keep interface architecture, domain behavior, data meaning, operations, and deployment state in
  the chapter that owns that question. Swagger, protobuf comments, and code own exhaustive endpoint
  and field reference.
- Keep task IDs, delivery-slice labels, commit hashes, test counts, and routine execution history
  out of explanatory system prose unless the identifier is required to understand or operate the
  current system.
- Put controlled document metadata in YAML frontmatter when substantively revising a document;
  do not add a body preamble of maintenance dates and status labels.
- Keep an artifact used by only one initiative inside that initiative. Reserve shared `sources/`
  for independently useful or reused evidence, and distinguish live external artifacts from
  preserved repository snapshots.
- When behavior, terminology, contracts, gameplay rules, or accepted design changes, update
  the affected knowledge in the same work or record a task-owned decision/delta entry for
  later incorporation.
- After a bounded deliverable has been presented or reviewed, treat the owner's direction to
  proceed, continue, or start the next step as scoped acceptance of that checkpoint unless the
  owner qualifies it. Update material decisions and lifecycle gates accordingly, but do not
  infer acceptance from silence or infer implementation, verification, source-control, or
  deployment state from progression language alone.
- Parallel worker tasks append only to their own task log. They do not directly rewrite a
  shared current-system document unless they own the serialized incorporation step.
- Do not copy prompts, transcripts, routine task steps, review chatter, build output, or
  conversation-specific notes into durable documents.
- Do not cite `scratch/` files. Prefer canonical repository URLs, revisions, Perforce
  changelists, or other stable evidence over machine-local paths.
- If implementation and current knowledge conflict, report the mismatch before changing the
  described behavior.

## Lifecycle And Compatibility

- An initiative closes only after accepted effects are incorporated into `system/` and useful
  rationale has a durable disposition. Then archive or delete inactive artifacts.
- Do not preserve obsolete repository paths or duplicate documents for compatibility. Update
  internal links in the same change.
- Do not infer that stale task logs are completed or abandoned. Use the grooming dispositions
  defined in `ORGANIZATION.md`.
- Personal current knowledge defaults to local-development applicability. Production claims
  require explicit environment or deployment evidence.
- Notion, peer repositories, and future canon are attributed sources. Adoption into this
  repository must be explicit.

## Working Rules

- Use clear, approachable technical prose. Teach the mental model before compressing details, and
  separate facts from assumptions while explaining material tradeoffs.
- For non-trivial repository changes, plan, review the classification boundary, implement,
  and validate.
- Reviews are read-only by default. Inspect content, links, contracts, contradictions, and
  reported verification; do not run unrelated implementation builds or tests unless asked.
- Keep repository changes minimal and reviewable. Small support tools may live under `tools/`;
  product implementation belongs elsewhere.
- Run the validator described in `ORGANIZATION.md` after structural, indexing, metadata, or
  link changes.

## Source Control

- The repository owner normally owns commits.
- Do not stage or commit unless the user explicitly asks.
- Leave unrelated existing changes intact.
