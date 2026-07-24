# Ascent Rivals - Overview

## Purpose
This folder is the knowledge hub for Ascent: Rivals domain understanding.

## Core Knowledge Areas
- [[game-client]]
- [[accelbyte-platform]]
- [[accelbyte-game-records]]
- [[website]]
- [[eventun/overview|eventun]]
- [[eventun/events|eventun-events]]
- [[eventun/interface-architecture|eventun-interface-architecture]]
- [[eventun/data-model|eventun-data-model]]
- [[accountun]]
- [[midnight]]
- [[cardano]]
- [[game-design]]
- [[competition-runtime-terms]]
- [[team-gauntlet-current-state]]
- [[hangar]]
- [[lore]]
- [[design-language]]

## Working Rule
Use these notes as the conceptual source of truth. Use implementation repositories only when executing project-specific work.

## Coordinated Deployment And Compatibility

Eventun, the Ascent Rivals game client, Ascentun, Website V2, and their generated first-party
contracts are normally changed and deployed as one coordinated unit. Backward compatibility
between those controlled components is not a default requirement. Prefer direct contract
replacement plus explicit data migration over parallel APIs, compatibility branches, runtime
version negotiation, or matrices of supported schema/algorithm combinations.

Do not add a schema-version column to each table or message. A version discriminator is justified
only when retained immutable history genuinely needs it to be interpreted or reproduced, or when an
external protocol outside the project's coordinated deployment control requires it. Such a version
is historical provenance, not a general compatibility mechanism. Any exception must identify the
specific independently deployed consumer or retained data that makes migration insufficient.

## Validation Ownership And Simplicity

Validate and normalize untrusted input at the boundary that first owns it, then pass a typed,
validated representation inward. Internal layers should rely on that contract rather than repeat
the same presence, range, enum, UUID, and shape checks in every function. A repeated check is
justified only when the later layer introduces a distinct risk or is independently reachable.

Keep validation where trust or state can actually change:

- authentication and authorization boundaries;
- Website, game-client, provider, generated-transport, and other external input;
- transaction-time checks whose truth may change under concurrency;
- database constraints that protect durable integrity independently of application execution;
- decoding retained or external data that may be corrupt or from a historically distinct format;
- irreversible administrative and financial operations.

Prefer one authoritative validation path, straightforward control flow, and fewer production-code
branches. Tests should exercise the owned boundary and durable invariants. Defensive checks without
a distinct failure model, obsolete fallbacks, and repeated semantic fingerprints are technical debt
rather than a default form of safety.
