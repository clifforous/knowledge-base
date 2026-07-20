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

As of 2026-05-15, the Cardanoun POC uses:

- Blockfrost for initial Preprod provider access.
- Cardanoun-managed service wallets for mint authority, reserve, collection, and worker lanes.
- UTXOS developer-controlled wallets for deployed managed player wallets, with one UTXOS project and Entity Secret per deployment.
- PostgreSQL, initially Neon for Azure deployment, for POC job state.
- Separate Eventun-ingestion and operator bearer tokens.

Cardanoun deployment assumptions:

- Each Cardanoun deployment owns exactly one Cardano network and one database. Switching networks means creating a separate deployment/database rather than reusing the same database with different configuration.
- Eventun sends gameplay event data only. It does not send Cardano network, wallet, asset, or chain data.
- The Cardanoun database does not use `network` columns for scoping. Network-prefixed ids may remain as human/debug labels, but they are not the isolation model.

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
