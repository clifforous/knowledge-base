# Ascent Rivals - Cardano

## Related
- [[overview]]
- [[website]]
- [[eventun/overview|eventun]]
- [[midnight]]

## Role
Community-facing identity and entitlement domain.

## Current Proof-of-Concept Exception

Cardanoun is a separate Cardano proof-of-concept reward service for Ascent Rivals event data. It is intentionally not part of the normal public wallet-linking model.

Cardanoun receives filtered accepted Eventun event batches, creates backend-managed player wallets, mints/distributes an experimental native asset named `tokun`, and simulates entry-fee transactions. These wallets are not user-linked website wallets, are not visible to players, and do not change public wallet-linking copy or recovery expectations.

As of 2026-05-14, the Cardanoun POC uses:

- Blockfrost for initial Preprod provider access.
- Cardanoun-managed service wallets for mint authority, reserve, collection, and worker lanes.
- UTXOS developer-controlled wallets for deployed managed player wallets, with one UTXOS project and Entity Secret per deployment.
- SQLite on durable storage for POC job state.
- Separate Eventun-ingestion and operator bearer tokens.

Do not generalize Cardanoun's managed wallets into the production Cardano identity model without a separate product and custody review.

## Responsibilities
- wallet-linked identity context
- entitlement eligibility based on token ownership
- social participation constraints informed by token context

## Boundary
Cardano and Midnight remain distinct:
- Cardano emphasizes community identity and eligibility
- Midnight emphasizes accounting lifecycle and payout commitments

## Open Questions
- Which eligibility checks are mandatory versus optional?
- What fallback behavior is required when entitlement data is temporarily stale?
- What recovery flows are required for wallet changes and account continuity?
