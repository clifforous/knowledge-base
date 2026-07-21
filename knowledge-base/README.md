# Knowledge Base Project

## Purpose

This project contains current repository policy and proposed designs for the structure,
tooling, and collaboration model of the knowledge base itself.

The repository has completed structural migration and content consolidation and has adopted
root governance. Empirical workflow validation remains before template extraction or `kb`
implementation. Proposed future behavior stays under `initiatives/`; current repository
policy belongs under `system/` or the root policy and agent instructions.

## Current Policy

- [Local Repository Path Policy](system/local-repo-paths.md)
- [Repository decision log](decisions/README.md)

## Initiatives

- [Federated Knowledge Base Initiative](initiatives/federated-kb/README.md)
  - Status: design in progress; implementation deferred pending manual validation
  - Separates normative requirements, contributor workflow and rationale, and the proposed
    on-demand MCP system design.
- [Repository Organization and Restructuring Plan](initiatives/repository-restructure/repository-organization-and-restructuring-plan.md)
  - Status: approved for phased migration
  - Defines the project-first target structure, document placement rules, initial mapping,
    and three-pass migration sequence.
- [Pass 1 Migration Manifest](initiatives/repository-restructure/pass-1-migration-manifest.md)
  - Status: structural migration record
  - Maps the previous numbered roots and individual design clusters to their first-pass
    destinations.
- [Pass 2 Consolidation Ledger](initiatives/repository-restructure/pass-2-consolidation-ledger.md)
  - Status: complete
  - Records current-system consolidation, initiative/archive boundaries, extracted decisions,
    and deleted workflow artifacts.
- [Pass 3 Governance Ledger](initiatives/repository-restructure/pass-3-governance-ledger.md)
  - Status: governance implementation complete; empirical workflow validation pending
  - Records adopted policy, task-log conventions, validation, and the pre-template use cases.

## Boundaries

- Current product knowledge belongs under each project's `system/` tree.
- Proposed knowledge-base behavior belongs under this project's `initiatives/` tree.
- Removed legacy workflows and automation remain documented in the pass 2 ledger; they are no
  longer part of the repository's readable workflow surface.
- The reorganized knowledge base must be exercised before the kb tool design is treated as
  implementation-ready.
