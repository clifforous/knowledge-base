# Ascent Rivals Cardano Reward Service Proof of Concept

Status: initial proof-of-concept implementation in progress
Date: 2026-05-07
Last updated: 2026-05-19

## Goal

Design a proof-of-concept Cardano service for Ascent: Rivals that receives filtered trusted match events from Eventun, creates service-managed player wallets when needed, mints or distributes a Cardano native reward token, and simulates player-wallet entry-fee transactions.

This is a one-off Cardano ecosystem proof of concept, not a long-term Ascent Rivals product integration. The goal is to demonstrate feasibility, transaction throughput, and service orchestration using Ascent Rivals match data as the source of realistic gameplay events. Players do not interact with, see, recover, link, or manage these proof-of-concept wallets.

This began as a research-backed proposal. As of 2026-05-15, the `cardanoun` proof-of-concept service has an initial Bun/TypeScript implementation with PostgreSQL state, Hono/Zod APIs, Blockfrost provider integration, Mesh transaction builders, UTXOS developer-controlled player wallet support, CLI setup/operations commands, and Azure-oriented readiness checks.

The proof of concept still should not be treated as a production economy launch. `tokun` remains an experimental native asset with a deliberately simple hot-key minting policy.

## Knowledge Base Context

Facts from the existing Ascent Rivals knowledge base:

- Ascent: Rivals is a competitive sci-fi combat racing game with high-speed racing, combat eliminations, modular hover ships, gauntlets, laps, heats, matches, and ARC as the in-game currency.
- The runtime hierarchy is `Session -> Match -> Heat -> Lap -> Checkpoint`. A qualifier is a competition-structure concept and must not be confused with a heat.
- Eventun is the authoritative owner of operational competition state, match summaries, player identity, wallet linkage, and accepted outcomes.
- Accountun is the existing accounting execution service for Midnight-backed tournament economics. Eventun delegates accounting transition execution to Accountun rather than owning chain execution itself.
- Current Cardano knowledge-base positioning is identity and entitlement oriented, while Midnight is accounting and payout oriented.
- Current wallet-linking design says Eventun is the website source of truth for linked wallet state and warns product copy not to imply that Ascent Rivals can custody a user's wallet.

Scope clarification:

- This proof of concept introduces service-created custodial or developer-controlled wallets, but they are intentionally separate from website-linked wallets and from the long-term Ascent Rivals wallet model.
- There is no required change to the public wallet-linking product guidance as long as this remains an internal/demo-only service and the wallets are not exposed to players.
- If these wallets are ever exposed to users, the product guidance must be updated before that exposure.

## External Research Summary

Cardano native tokens are the right starting point for the reward currency. Cardano supports user-defined native assets without requiring an ERC-20-style smart contract for basic ownership and transfer. Minting is controlled by a minting policy, and every asset is permanently associated with exactly one policy.

Important Cardano constraints:

- Ada remains required for fees and deposits. Native tokens cannot pay Cardano transaction fees by themselves.
- A UTxO cannot contain only custom tokens. Sending native tokens to a wallet requires an ADA amount in the same output, at least enough to satisfy minimum-ADA rules.
- The EUTXO model consumes whole UTxOs. Each UTxO can be spent once, so high-throughput designs need multiple UTxO lanes rather than a single shared state/output.
- Cardano smart contracts are validators, not actors. They cannot initiate payments, minting, collection, or callbacks; the off-chain service must build and submit every transaction.
- Plutus/Aiken script transactions need collateral UTxOs and careful budgeting. For this proof of concept, use Plutus only where the demonstration value is clear.

Mesh research:

- Mesh `MeshCardanoHeadlessWallet` supports server-side wallet creation from mnemonic or BIP32 roots, signing transactions, signing data, submitting transactions, fetching account UTxOs, and selecting collateral.
- Mesh `MeshTxBuilder` supports native-asset minting and burning with native scripts, Plutus minting policies, transaction metadata, required signers, manual UTxO input selection, custom change address handling, and partial multi-signature flows.
- Mesh's Aiken integration can compile Aiken validators, apply parameters, resolve script addresses, and build lock/redeem transactions from TypeScript.
- I did not find a Mesh-native sponsored-transaction service API in the current Mesh docs. Mesh appears sufficient for constructing a transaction that spends both a player-wallet UTxO and a service-wallet ADA UTxO, then signs with both wallets. That is a practical service-sponsored fee pattern when the backend controls the involved wallets.

UTXOS.dev research:

- UTXOS markets wallet-as-a-service, developer-controlled wallets, and transaction sponsorship for Cardano.
- Developer-controlled wallets are a good fit for this proof of concept's backend-managed player wallets. UTXOS creates project wallets, stores encrypted key material, and requires the backend-held Entity Secret private key for signing.
- UTXOS developer-controlled wallet APIs run on the backend only. The Entity Secret and API key must never be exposed to game clients or browser code.
- Losing the Entity Secret means losing access to all wallets created under that Entity Secret. Use a separate UTXOS project and separate Entity Secret per Cardanoun deployment, even for two Preprod deployments.
- UTXOS Cardano examples initialize the SDK with a provider such as Blockfrost and use `network: "testnet"` for test networks or `network: "mainnet"` for mainnet.
- UTXOS beta pricing currently lists dev-controlled wallet quotas by tier. Treat quota and rate-limit confirmation as a pre-mainnet and pre-load-test checklist item because pricing and limits may change.
- UTXOS transaction sponsorship is separate from the developer-controlled wallet custody path. It remains deferred unless the POC needs UTXOS to sponsor externally controlled user wallets.

Sources:

Local knowledge-base sources:

- `ascent-rivals/system/overview.md`
- `ascent-rivals/system/game-design.md`
- `ascent-rivals/system/competition-runtime-terms.md`
- `ascent-rivals/system/cardano.md`
- `ascent-rivals/system/accountun.md`
- `ascent-rivals/system/eventun/overview.md`
- `ascent-rivals/system/eventun/api.md`
- `ascent-rivals/system/eventun/data-model.md`
- `ascent-rivals/system/eventun/events.md`
- `ascent-rivals/initiatives/website-v2/flows/wallet-linking.md`
- `ascent-rivals/initiatives/midnight-tournament-accounting/ascent-rivals-midnight-tournament-accounting-design.md`

External sources:

- Cardano native tokens: https://docs.cardano.org/developer-resources/native-tokens
- Cardano EUTXO model: https://docs.cardano.org/about-cardano/learn/eutxo-explainer
- Cardano transaction costs and determinism: https://docs.cardano.org/about-cardano/learn/transaction-costs-determinism
- Cardano confirmation concepts: https://docs.cardano.org/about-cardano/learn/chain-confirmation-versus-transaction-confirmation
- Cardano testnet environments: https://docs.cardano.org/cardano-testnets/environments
- Cardano developer smart contracts overview: https://developers.cardano.org/docs/build/smart-contracts/overview/
- Mesh headless wallet: https://meshjs.dev/apis/wallets/meshwallet
- Mesh transaction builder: https://meshjs.dev/apis/txbuilder
- Mesh minting and burning: https://meshjs.dev/apis/txbuilder/minting
- Mesh multi-signature transactions: https://meshjs.dev/apis/txbuilder/multisig
- Mesh Aiken integration: https://meshjs.dev/aiken
- Aiken validators: https://aiken-lang.org/language-tour/validators
- UTXOS introduction: https://docs.utxos.dev/
- UTXOS developer-controlled wallets: https://docs.utxos.dev/wallet/developer-controlled
- UTXOS Cardano developer-controlled wallet usage: https://docs.utxos.dev/wallet/developer-controlled/usage/cardano
- UTXOS pricing: https://docs.utxos.dev/project/pricing
- UTXOS Cardano sponsorship: https://docs.utxos.dev/sponsor/usage/cardano
- UTXOS sponsorship flow: https://docs.utxos.dev/sponsor/how-it-works
- Azure Container Apps storage mounts: https://learn.microsoft.com/en-us/azure/container-apps/storage-mounts
- Azure Cosmos DB free tier: https://learn.microsoft.com/en-us/azure/cosmos-db/free-tier
- Azure SQL Database free offer: https://learn.microsoft.com/en-us/azure/azure-sql/database/free-offer

## Assumptions

- The new service is separate from Accountun and Eventun. Working name: `cardanoun`.
- `cardanoun` will be a TypeScript/Bun service because Mesh is TypeScript-first and Accountun already uses a Bun package layout, Dockerfiles, and Azure Container Registry publishing. Use Node.js only if a Mesh dependency has an incompatible Bun runtime requirement.
- Eventun remains the authoritative source for trusted gameplay facts. `cardanoun` does not ingest raw game events directly from game servers.
- Initial deployment target is Cardano Preprod, not Preview, because Preprod is closer to mainnet behavior.
- Mainnet deployment is a controlled test, not a public economy launch.
- The proof-of-concept reward token is `tokun`. It is unrelated to ARC and must not be described as an Ascent Rivals economy token.
- Each rewardable event produces an individual Cardano transaction. Batch transport from Eventun is allowed, but `cardanoun` must expand the request into one transaction job per reward.
- No Ascent Rivals game client or dedicated-server event changes are planned for this proof of concept. The intended game-side integration is limited to Eventun calling `cardanoun` when an end-of-match event batch arrives.
- Eventun should not know or send Cardano network, wallet, asset, or chain data for this proof of concept. `cardanoun` owns chain configuration, managed-wallet lookup, and wallet creation.
- Mainnet test funding is expected to be limited, roughly USD 1,000 to USD 2,000 converted into ADA. The mainnet test runs until the allocated funds are spent.
- Blockfrost is the selected provider for the initial Preprod deployment.
- UTXOS developer-controlled wallets are the selected player-wallet custody provider for deployed tests. Local HD player wallets remain a development fallback.
- Service wallets remain Cardanoun-managed HD wallets for mint authority, reserve, and collection. The reserve wallet owns the reward-lane UTxOs; there are no separate worker subwallets in the current POC model.
- Each Cardanoun deployment should use its own PostgreSQL database, service wallet secret, Blockfrost project, UTXOS project, UTXOS Entity Secret, Eventun bearer token, and operator bearer token.
- Each Cardanoun deployment owns exactly one Cardano network. Switching networks means creating a separate deployment and database rather than reusing one database with different network configuration.
- The Cardanoun database does not use `network` columns for relational scoping. Network-prefixed ids may remain as human/debug labels, but deployment/database isolation is the network boundary.
- Newly built real transactions should include a configured `invalidHereafter` validity window so ambiguous submission failures have a deterministic expiry point.
- The proof-of-concept should include a lightweight dashboard package for demos and operator visibility. The dashboard should be read-only, separately deployed from the API, and should not expose privileged operator controls or signing/submission capabilities.

## Recommended Approach

Build `cardanoun` as an asynchronous Cardano transaction orchestration service.

Eventun calls `cardanoun` after accepting an end-of-match event batch. Eventun should filter and forward the relevant accepted events, not derive a special reward contract and not include wallet data. `cardanoun` derives proof-of-concept entry-fee and reward transactions from that event input, persists transaction jobs, provisions managed player wallets through UTXOS when configured, reserves reward-lane UTxOs from the reserve wallet, submits transactions, and tracks block inclusion and confirmation.

Use a Cardano native fungible token for the proof-of-concept currency:

- Asset name: `tokun`.
- Policy: native script requiring a service mint authority signature.
- Supply model: mint an initial reserve to the `reserve` service wallet, then split reserve funds into reward-lane UTxOs held by the reserve address. Treat `reserve` as the main operating wallet; `mint_authority` signs the policy and only keeps a small ADA operating float for mint transaction fees and minimum-ADA mint outputs. Reconciliation should top up `mint_authority` from `reserve` when active mint jobs need that float, and move mint-authority ADA above the float back to `reserve`; `mint_authority` should not behave as the backing reserve for the reserve wallet.
- Mainnet test hardening: use a separate mainnet-test policy, separate keys, explicit supply caps or operator approval, and clear product copy that the asset is experimental.

Do not include an Aiken entry-fee contract in the first version. Use direct wallet transactions with metadata for the simulated entry fee.

Use scoped bearer tokens:

- `CARDANOUN_EVENTUN_BEARER_TOKEN` only authorizes `/v1/eventun/*` ingestion.
- `CARDANOUN_OPERATOR_BEARER_TOKEN` authorizes privileged operations routes such as mint queueing, funding movement, signing, submission, observation, and runner controls.
- The API should refuse startup if the route tokens are missing or identical.

## Service Boundaries

### Eventun

Eventun should:

- own match acceptance, match summaries, and player identity
- call `cardanoun` after accepting an end-of-match server event batch
- filter out bots and forward only the accepted `PlayerMatchEnd`, `PlayerLap`, `PlayerKill`, and `PlayerHeatEnd` events needed for the proof of concept
- store a bridge status if product surfaces need reward progress
- avoid submitting Cardano transactions directly
- avoid storing or sending proof-of-concept Cardano wallet addresses

### Cardanoun

`cardanoun` should:

- own Cardano network configuration, providers, wallet signing, minting policy metadata, transaction building, transaction submission, confirmation tracking, and chain reconciliation
- own service-managed wallet records and encrypted key references for custodial wallets
- derive entry-fee and reward jobs from Eventun's filtered accepted events
- own managed-wallet lookup and creation by Eventun player id
- own reserve reward-lane funding, reservation, and rebalancing
- expose idempotent APIs for Eventun
- expose operations APIs for reserve balance, stuck transactions, failed jobs, and chain sync health

### Accountun

Accountun should stay focused on Midnight tournament accounting unless a later design intentionally unifies chain execution patterns. This proof of concept should not add Cardano concerns to Accountun.

## Eventun to Cardanoun API Shape

Suggested initial endpoint:

```text
POST /v1/eventun/matches/{session_id}/{match_id}/event-batches
```

Request shape, conceptually:

```json
{
  "requestId": "eventun:session:match:events-v1",
  "sessionId": "accelbyte-session-id",
  "matchId": 0,
  "submittedAt": "2026-05-07T00:00:00Z",
  "events": [
    {
      "eventId": "stable-event-id-or-derived-id",
      "name": "PlayerLap",
      "time": "2026-05-07T00:00:00Z",
      "sessionId": "accelbyte-session-id",
      "matchId": 0,
      "heat": 1,
      "playerId": "uuid",
      "progress": { "placement": 2, "lap": 2, "checkpoint": 4 },
      "eventData": {
        "timeMs": 62412,
        "shotsHit": 1,
        "shotsFired": 4
      }
    }
  ]
}
```

Response:

```json
{
  "eventBatchId": "uuid",
  "acceptedEvents": 42,
  "entryFeeJobs": 8,
  "rewardJobs": 67,
  "createdWallets": 3,
  "transactionJobs": 75
}
```

Idempotency:

- `requestId` must be unique and stable per Eventun filtered event batch submission.
- Each forwarded event should have a stable `eventId` if Eventun can provide one.
- If Eventun does not expose stable event ids, derive event ids from `session_id`, `match_id`, `event_name`, `player_id`, `heat`, top-level progress fields, event time, and a deterministic ordinal inside the filtered batch.
- `cardanoun` derives deterministic job ids from `eventBatchId`, event id, job kind, and ordinal. This makes retries safe even when a batch is resubmitted.

## Reward Event Model

Supported proof-of-concept rewards:

| Gameplay fact | Eventun source | Reward transaction |
| --- | --- | --- |
| Completing a lap | `PlayerLap` | transfer reward token to player wallet |
| Completing a match | `PlayerMatchEnd` | transfer reward token to player wallet |
| Killing another player | `PlayerKill` | transfer reward token to killer wallet |
| Shooting an obelisk | `PlayerHeatEnd.obelisks` aggregate count | one transfer reward token transaction per counted obelisk |

Obelisk mismatch:

- Current Eventun knowledge records `obelisks` as aggregate fields on `PlayerHeatEnd` and `PlayerMatchEnd`.
- For this proof of concept, `PlayerHeatEnd.obelisks` is acceptable. If a heat end has `obelisks: 3`, `cardanoun` creates three obelisk reward transaction jobs for that player and heat.
- This proves the transaction flow and approximate gameplay mapping without requiring Ascent Rivals gameplay changes.

Bot and abuse policy:

- Reward only human players unless an explicit test mode includes bots.
- Eventun should reject or omit forwarded events where `player_id` is missing, bot-prefixed, or not associated with an accepted human participant.
- `cardanoun` should defensively reject forwarded events that still look like bot events, even if Eventun is expected to filter them first.
- Kill and obelisk awards need anti-farming rules before any valuable mainnet test.

## Wallet Model

Use two wallet classes:

### Service wallets

- Main HD service root: derives the service roles.
- Mint authority wallet: signs minting transactions under the token policy. This may be the main HD wallet in the proof of concept but should be modeled as a distinct role.
- Reserve wallet: holds the main `tokun` and ADA reserve, owns reward-lane UTxOs, funds reward payouts, and sponsors entry-fee transactions.
- Collection wallet: receives entry fees collected from the optional contract.

For the proof of concept, these roles can derive from one mnemonic or one HD root private key. A mnemonic is a human-friendly representation of wallet seed material, while an HD root private key/xprv can preserve child-key derivation without storing words. Storing only a single payment private key is not equivalent because it cannot derive role keys. The database and configuration should store role, account index, and address index; deployment/database isolation, not a database `network` column, is the network boundary.

### Player wallets

Initial proof of concept:

- If Eventun includes a player without a proof-of-concept managed wallet, `cardanoun` creates a service-managed player wallet. For deployed tests, use UTXOS developer-controlled wallets and store the UTXOS wallet id/provider reference.
- Store only encrypted key material or a secret reference. Do not log mnemonic words, private keys, UTXOS Entity Secrets, signatures, or full payloads.
- Send the first reward token output with required minimum ADA to the wallet address.

Important constraint:

- A player wallet that holds Cardano native tokens will also hold some ADA in the token UTxO. Sponsorship can avoid requiring the player to acquire ADA for fees, but it cannot make native-token UTxOs ADA-free.

Product guardrail:

- A service-managed proof-of-concept wallet is not the same as a user-linked Cardano wallet.
- Because players will not interact with these wallets, no public UI copy is required for the proof of concept.
- If these wallets are ever shown to users, use separate language such as `Managed reward wallet` and define export/recovery policy first.
- UTXOS developer-controlled player wallets are not the same as website-linked Cardano wallets and are not player-recoverable through the current public product flow.

## Fee Funding Model

Cardano does not have an Ethereum-style separate gas payer field. Transaction fees are paid by the transaction's input set. A service-sponsored fee pattern can still be built by including one or more service-wallet ADA UTxOs in the transaction, directing change appropriately, and signing with every required wallet.

Recommended proof-of-concept fee model:

- Reward payout transactions spend service reserve UTxOs only. The service wallet supplies reward tokens, minimum ADA for the player token output, and transaction fees.
- Simulated entry-fee transactions spend the player's managed wallet UTxO for the entry-fee token and a reserve ADA UTxO for fees and any ADA delta needed by outputs.
- If the simulated entry-fee transaction spends a player wallet UTxO, sign with both the player managed wallet and the reserve wallet. For UTXOS developer-controlled player wallets, Cardanoun loads the UTXOS Cardano wallet through the backend SDK and uses it as the player signer.
- Avoid relying on UTXOS transaction sponsorship for this POC unless an externally controlled user wallet flow is introduced later.

Operational implication:

- Player managed wallets still hold ADA inside token UTxOs because Cardano requires minimum ADA in native-token outputs.
- The service can avoid routine player ADA top-offs by supplying service ADA inputs whenever it constructs transactions that spend from player wallets.
- Some player-wallet UTxO reshaping may still be needed if a player wallet accumulates fragmented token outputs.

## Transaction Execution Model

Every simulated entry-fee payment and every reward fact becomes one transaction job.

For each new filtered event batch:

1. Create managed player wallets for unseen human player ids.
2. Create simulated entry-fee jobs for the batch's human players. These jobs run before reward jobs.
3. Create reward jobs from `PlayerLap`, `PlayerKill`, `PlayerMatchEnd`, and `PlayerHeatEnd.obelisks`.
4. Reserve available reserve reward-lane UTxOs for reward jobs.
5. Submit as many independent transactions as reasonable without intentionally clogging blocks.

Recommended execution model:

1. Normalize and persist event-derived transaction jobs.
2. Ensure the player has a Cardano address.
3. For reward jobs, reserve one available reserve reward-lane UTxO with enough `tokun` and ADA.
4. Build a transaction that either pays a simulated entry fee or transfers one reward amount to the player address.
5. Include minimum ADA in the player output.
6. Attach compact transaction metadata containing a reward reference, not raw personal data.
7. Add an `invalidHereafter` validity upper slot using the configured transaction validity window.
8. Sign with the required service and/or managed player wallet.
9. Submit through the configured provider.
10. Mark the job `submitted` with transaction hash.
11. Watch for block inclusion and confirmation depth.
12. Mark the job `confirmed` when the confirmation policy is satisfied.

Statuses:

```text
accepted
wallet_required
wallet_created
ready
building
signed
submission_unknown
submitted
in_block
confirmed
failed_retryable
failed_terminal
reconciled
```

Submission uncertainty:

- Blockfrost can return `404` for a transaction hash shortly after submission, before its indexing path sees the transaction. Treat that as pending, not proof of failure.
- If signed CBOR submission fails after the service already has a signed transaction hash, move the job to `submission_unknown` rather than immediately rebuilding.
- `submission_unknown` jobs should be observed by hash. If the transaction appears on-chain, move to `in_block` or `confirmed`.
- If the latest provider tip passes `invalid_hereafter_slot + tx_expiry_grace_slots` and the transaction is still not observed, it can no longer validly appear in a later block. Clear stale CBOR and move the job back to `failed_retryable` for rebuilding.
- Keep the validity window configurable. The initial implementation default is 300 slots, with an additional 60-slot expiry grace window.

No batching:

- Do not combine multiple reward facts into one Cardano transaction.
- Throughput comes from multiple reserve-owned reward-lane UTxOs, not from batching reward outputs.
- The throughput goal is to fit many independent transactions in a block without intentionally filling blocks or congesting the network.

Transaction chaining:

- Maintain an internal pending-UTxO ledger for outputs created by submitted transactions.
- Conservative mode waits for block inclusion before spending a newly created change output.
- Chained mode may build child transactions against pending outputs to improve throughput, but it must track parent-child dependencies and fail the whole chain if a parent transaction fails.
- Validate chained-mode behavior against the chosen provider/node. Do not assume every provider exposes mempool state or accepts dependent submissions the same way.

UTxO lane strategy:

- Treat individual reserve UTxOs as independent reward lanes.
- Pre-split reserve funds into many UTxOs sized for one expected reward transaction.
- Keep each reward-lane UTxO above the player output's minimum ADA and with enough `tokun` for the configured reward amount.
- Size reward-lane ADA with fee/change headroom. The current implementation uses `CARDANOUN_REWARD_LANE_ADA_LOVELACE`, defaulting to twice `CARDANOUN_MIN_ADA_LOVELACE`; token-bearing outputs are built with the protocol-calculated minimum ADA from Blockfrost protocol parameters.
- Monitor lane count, pending ratio, reserve balance, and failed submissions.

## Reserve Lane Management

The reserve service wallet is both the operating reserve and the source of reward-lane UTxOs. This intentionally removes the earlier worker-subwallet layer, which created extra funding, fan-out, and reconciliation complexity without improving the first POC enough to justify it.

Balance targets:

- `minAda`: fallback/conservative local ADA floor used for reserve-lane defaults and offline helper logic.
- `rewardLaneAda`: the ADA expected in each reserve reward-lane UTxO, including fee/change headroom.
- `rewardTokun`: the token amount expected in each reward-lane UTxO.
- `maxInFlightTransactions`: the target number of reserve reward lanes to keep available for concurrent reward signing/submission.

Lane refill flow:

1. Chain sync records reserve UTxOs as available, reserved, spent, or recycle reward lanes.
2. Reward job claiming atomically reserves an available reward lane before signing.
3. Confirmed reward observations mark the consumed lane spent.
4. Reconciliation queues a reserve-to-reserve funding transaction with one output per missing lane.
5. After the refill transaction confirms and the provider indexes it, chain sync records those outputs as available lanes.

This model is simpler than worker wallets while still allowing multiple reward transactions to be built from independent UTxOs. It also makes reconfiguration simpler: if reward size changes, reconciliation can classify old lane sizes as recycle candidates and create new reserve lanes with the new target shape.

## Entry Fee Simulation

Use direct payment with metadata for the first version. Do not include a smart contract.

The player custodial wallet pays the entry fee token to a service collection wallet. This is not user-facing and does not affect match admission; it exists only to make the managed player wallet transact before rewards in each new event batch.

The entry-fee transaction includes metadata with:

- match identifier or stage-run identifier
- player id hash
- entry fee amount
- Eventun event batch id

Advantages:

- cheapest and simplest
- no Plutus collateral
- lower operational risk
- enough for proving "player wallet paid fee for match" in a demo

Disadvantages:

- no script address
- collection is just a wallet transfer
- refund/collection rules are entirely off-chain

Ordering:

- For each event batch, submit simulated entry-fee jobs first for new or participating player wallets.
- Submit reward jobs after the entry-fee jobs are accepted for processing. Confirmation does not need to block reward submission unless the player wallet lacks enough token/ADA for the simulated entry fee.

## Data Store

Use PostgreSQL for deployed proof-of-concept state. Neon is the initial managed PostgreSQL target for Azure deployment.

Preferred deployment:

- Use one PostgreSQL database per Cardanoun deployment/network.
- Run SQL migrations automatically on API/CLI startup under a PostgreSQL advisory lock.
- Treat transaction job state as the source of truth for retry/reconciliation.
- Scale service replicas conservatively until Postgres job locking and Cardano UTxO lane behavior have been revalidated under the intended deployment topology.

Azure alternatives:

- Azure SQL Database remains a possible managed relational alternative if Neon does not fit the deployment.
- Azure Cosmos DB or Azure Table Storage are less direct fits because Cardanoun now relies on relational job claims, row locks, and SQL migrations.

Initial tables:

- `asset_policy`: policy id, asset name, script type, active flag.
- `service_wallet`: role, address, derivation path or account index, secret reference, status.
- `player_wallet`: player id, address, custody mode, provider wallet id, created at.
- `wallet_secret_ref`: wallet id, secret storage reference, key version, disabled flag.
- `event_batch`: Eventun request id, session id, match id, status.
- `forwarded_event`: event batch id, derived event id, name, player id, heat, progress, event data hash, raw event JSON.
- `reward_fact`: deterministic reward id, kind, player id, amount, source event reference, ordinal, status.
- `transaction_job`: job id, job type, reward id or entry fee id, source wallet id, reserved reward-lane id, status, tx hash, parent job id, attempts.
- `transaction_job` should also store signed CBOR only for internal submission, an `invalid_hereafter_slot` for real signed transactions, submission/build locks, and last error details. Operations APIs should not expose signed CBOR.
- `transaction_observation`: tx hash, block slot, block hash, confirmation depth, observed at.
- `entry_fee_payment`: event batch id, player id, amount, status, tx hash.
- `reward_lane`: reserve wallet id, tx hash, output index, amount summary, lane status, reserved job id, observed at.

## Deployment Shape

Follow Accountun's deployment style where practical:

- Bun workspace with packages for API, Cardano transaction library, and shared utilities.
- Hono or similar lightweight HTTP API with OpenAPI/Zod schemas.
- Docker image built from the service package.
- Azure Container Registry publish flow similar to Accountun.
- Azure-hosted service with environment-specific configuration for Preprod and Mainnet.
- Managed PostgreSQL database for durable state.
- Key Vault secret or equivalent mounted/managed secret for the service wallet root key material.
- Azure Key Vault for secrets; avoid `.env` secrets outside local development.
- Health endpoint and metrics endpoint.
- Operations endpoint for service wallet balances, reserve reward-lane status, job backlog, block inclusion rate, and remaining mainnet ADA budget.
- Deployment readiness gate that can fail startup when bearer tokens, durable paths, provider health, service wallets, tokun policy, or custody settings are not production-like.
- Background runner that wakes on Eventun ingestion or operator actions, processes queued work, submits signed jobs when enabled, observes pending jobs, reconciles funding after confirmations, and stops when no active work remains.

Azure resource shape:

- Mirroring Accountun with a separate `rg-cardanoun`, `cardanoun` container registry, `cardanoun-env` Container Apps environment, and `cardanoun-api` app is acceptable for the POC.
- Sharing an existing container registry is the most obvious small cost optimization, but separate resources are operationally cleaner and easier to tear down.
- Keep the Container App on the Consumption plan and start with conservative replica counts until Postgres job locking and Cardano UTxO lane behavior have been load-tested.
- Avoid dedicated workload profiles, min replicas greater than zero, or high log retention unless the test requires them.

Provider options:

- Start with Blockfrost for Preprod.
- Keep provider access behind `cardanoun` and never expose API keys to client code.
- Consider a self-hosted node/Ogmios/Kupo path only after the proof-of-concept transaction model stabilizes.

## Dashboard Package

Add a separate static dashboard package for demonstration and light operational visibility. Working package name:

```text
packages/dashboard
```

Primary goals:

- show the Cardanoun service is actively turning Eventun batches into chain transactions
- make transaction state transitions visible during demos
- show reserve, mint-authority, collection, and reward-lane health at a glance
- show job queue pressure, recent failures, and runner state without exposing privileged controls
- link on-chain transaction hashes to a public Cardano explorer after they are known

Recommended frontend shape:

- static SPA, not Next.js for the first dashboard
- Vite + TypeScript
- Tailwind CSS for layout and styling
- Solid + TanStack Router/Query is acceptable if the team wants to trial the Solid path; verify Solid/TanStack version compatibility at scaffold time
- Prefer a framework-agnostic charting library for Solid, such as Apache ECharts, Chart.js, or ApexCharts; Recharts and Tremor are React-oriented and should only be selected if the dashboard uses React instead of Solid

Recommended deployment:

- deploy as Azure Static Web Apps
- use `dashboard.cardanoun.com` as the stable custom domain
- keep the API at `api.cardanoun.com`
- prefer Azure Static Web Apps over Azure Storage static website hosting because Static Web Apps supports custom domains with managed SSL directly; Azure Storage static website custom-domain HTTPS typically requires Azure CDN or Front Door

Authentication and API scope:

- add a third bearer token for dashboard read-only APIs, tentatively `CARDANOUN_DASHBOARD_BEARER_TOKEN`
- dashboard token must not authorize minting, fund movement, signing, submission, queue mutation, runner controls, or secret-bearing endpoints
- if the static dashboard is public or broadly shared, do not bake the dashboard token into the bundle; use Static Web Apps auth or a tiny server/API proxy later
- for internal POC demos, a token entered into the UI and stored in memory/session storage is acceptable if the token has read-only scope
- dashboard local development should keep mock mode as the default. API mode should be enabled with `VITE_CARDANOUN_DASHBOARD_MODE=api`, point to `VITE_CARDANOUN_API_BASE_URL` such as `https://api.cardanoun.com`, and prompt for the read-only dashboard token in the browser session.

Dashboard API surface:

- add read-only routes under `/v1/dashboard/*` or equivalent, protected by the dashboard token
- initial implementation can use a single `/v1/dashboard/snapshot` endpoint that summarizes existing data rather than exposing privileged operations responses directly
- keep a separate paginated transaction-history endpoint as a likely follow-up once the recent transaction list grows beyond what the snapshot should carry
- useful first endpoints:
  - summary: runner state, active jobs, recent confirmations, recent failures
  - transactions over time: counts by job type and status, grouped into time buckets
  - job queue: recent and active jobs with type, status, attempts, tx hash, updated time
  - wallets: service wallet ADA/`tokun` balances and reward-lane counts
  - failures: recent retryable and terminal errors grouped by message and job type

Dashboard persistence/read model:

- persist transaction job status transitions in a small history table so charts are not limited to the current mutable `transaction_job.status`
- include `job_id` on transaction observations, or otherwise make latest observation joins unambiguous
- snapshot responses can aggregate from the status history, current jobs, service wallet balances, and reward lanes
- if lane/job time-series charts need more accurate historical snapshots later, add a lightweight metric snapshot table written by the runner cycle

Live update behavior:

- use polling/long-polling style updates first; do not add WebSockets or SSE until the dashboard proves it needs them
- when active jobs exist, refresh high-volatility panels every 3 to 5 seconds
- when the queue is quiet, back off to 30 to 60 seconds
- allow manual refresh and a visible last-updated timestamp
- TanStack Query's refetch intervals and stale-time behavior are a good fit for this model
- avoid hammering Blockfrost from the browser; the dashboard should read Cardanoun's database/API summaries, not call chain providers directly
- graph bucket size should be adaptive or configurable. Preprod may have short bursts of activity a few times per week, so 10-minute buckets are useful during a live test but hourly or daily buckets are more useful when reviewing quiet/off-day history.

Recommended dashboard views:

- Overview: current runner state, active job counts, confirmed transaction count, failed job count, reserve available lanes, reserve ADA/`tokun`
- Transactions: time-series chart of submitted, in-block, and confirmed transactions by job type (`reward`, `entry_fee`, `fund_move`, `mint_reserve`)
- Queue: filterable table of active and recent transaction jobs
- Wallets/Lanes: service wallet balances, reward-lane availability, recycle lanes, reserved lanes
- Recent Chain Activity: latest known tx hashes, status, confirmation depth, block slot, explorer link

Initial graph set:

- Transactions over time by status: submitted, in-block, confirmed, failed. This is the primary "work is happening on-chain" demo graph.
- Transactions over time by type: `entry_fee`, `reward`, `fund_move`, and `mint_reserve`. If useful, reward transactions can later be split by reward kind.
- Job state pipeline over time: ready, signed, submitted, in-block, confirmed, failed-retryable, and failed-terminal counts. This should make backlog and stuck-state behavior visible.
- Confirmation latency: time from submitted to confirmed, shown as a line, histogram, or compact distribution summary.
- Reward lane availability over time: available, reserved, recycle, and spent lane counts. This shows current transaction throughput capacity.

Use table/list views rather than graphs for:

- active job queue
- recent transactions
- recent Eventun batches
- service wallet balances
- recent failures

Dashboard metric dimensions:

- Keep `jobType` separate from gameplay reward reason.
- `jobType` examples: `entry_fee`, `reward`, `fund_move`, `mint_reserve`.
- `rewardKind` examples: `lap`, `kill`, `match_end`, `obelisk`.
- Charts should use `jobType` for operational flow and `rewardKind` only when showing gameplay-derived reward mix.

Deferred player-wallet view:

- A later dashboard page may show managed player wallets, player ids, balances, provider wallet ids, and recent wallet transactions.
- Treat this as privacy-sensitive even though chain transactions are public. Player ids, wallet addresses, provider ids, and balances should not be casually exposed in a public demo view.
- If added, prefer an operator-only route or explicit "debug/private" dashboard mode, and consider masking player ids by default.

Explorer links:

- Use a network-aware helper for public transaction links.
- Cardanoscan URL pattern:
  - Preprod: `https://preprod.cardanoscan.io/transaction/{txHash}`
  - Mainnet: `https://cardanoscan.io/transaction/{txHash}`
- Cexplorer URL pattern:
  - Mainnet: `https://cexplorer.io/tx/{txHash}`
  - Preprod/testnet support should be verified before making it the default
- Pick one default explorer in configuration, but keep the helper easy to swap.

Non-goals for the first dashboard:

- no wallet creation or key handling in the browser
- no mint/fund/sign/submit buttons
- no direct Blockfrost or UTXOS API calls from the browser
- no player-facing wallet UI
- no public claims that `tokun` is a production currency

## Security and Compliance Risks

Custody:

- If Ascent creates wallets and holds keys, it is operating a custodial wallet service for those assets.
- The proof of concept needs a written export/recovery/loss policy before it is exposed to real users.
- Service wallet custody should use Key Vault or an equivalent secret source for deployment. The preferred Cardanoun deployment secret is `CARDANOUN_SERVICE_ROOT_PRIVATE_KEY`, a bech32 HD root private key/xprv capable of deriving the configured service roles. A single address payment private key is not sufficient for this derivation model, and plain encrypted mnemonics in a database are a weak mainnet posture.
- UTXOS player wallets depend on the Entity Secret. Use one UTXOS project and Entity Secret per deployment, store the Entity Secret private key securely, and treat compromise as compromise of all wallets in that deployment.

Operations:

- Eventun ingestion and operator controls must not share bearer credentials.
- Signed transaction CBOR should remain internal to the build/submission path and should not be returned by operations APIs.
- Mainnet submission requires both normal transaction submission enablement and an explicit mainnet allow flag.

Mint authority:

- A hot mint key can inflate supply if compromised. For this POC, unlimited or repeated `tokun` minting is acceptable as long as operator access is controlled and product copy does not position the asset as a durable public currency.
- Mainnet tests should use separate keys, a separate policy id, small initial funding, and stable operator request ids for mint jobs.

Economy:

- Do not imply that the proof-of-concept token is the same as in-game ARC.
- Mainnet entry fees and reward payouts may raise legal, tax, gambling, contest, money-transmission, or consumer-protection questions. This needs legal review before value-bearing public use.

Privacy:

- On-chain addresses and transactions are public.
- Do not place raw player ids, Steam ids, display names, or full match payloads in metadata or datum.
- Use salted hashes or opaque Eventun/Cardanoun ids for on-chain references.

Abuse:

- Kill and obelisk rewards are farmable if match context is not constrained.
- Reward policy should distinguish competitive, custom, bot, local, and test server modes.

## Approach Comparison

### Recommended POC: Native token rewards plus direct entry fee metadata

Use Mesh transaction builders, Cardanoun-managed service wallets, UTXOS developer-controlled player wallets, native-script minting, reserve-owned reward lanes, and direct simulated entry-fee payments with metadata.

This proves the core chain loop fastest:

- wallet creation
- minting
- per-event transactions
- chain confirmation
- Eventun bridge
- reserve, reward-lane, and UTxO operations

Tradeoff:

- It does not showcase an Aiken script. It also introduces UTXOS as a third-party wallet dependency. That is acceptable for the first grant-provider demonstration because the requested goal is transaction feasibility, managed-wallet orchestration, and throughput.

### Deferred Alternative: Aiken entry-fee script

Add a small Aiken validator for entry fees only if grant-provider feedback specifically asks for a script-address demo.

Tradeoff:

- Better smart-contract demo, but it adds collateral, script debugging, and more failure modes before the basic reward pipeline is proven.

### Deferred Alternative: UTXOS sponsorship and non-custodial wallets

Use UTXOS transaction sponsorship for externally controlled user wallets.

Tradeoff:

- Could enable user-controlled passkey/social wallets later, but it adds a different custody and approval model. It is not needed while players do not interact with the POC wallets.

## Review Questions

1. Which match modes are eligible: public matchmaking only, gauntlets only, custom games, local/scrimmage, or a dedicated blockchain test queue?
2. What throughput measurement should be shown to grant providers: submitted transactions per minute, block-included transactions per minute, confirmed transactions per minute, cost per transaction, or all of these?
3. What safety limit should stop the mainnet test: remaining ADA reserve, submitted transaction count, block fullness threshold, or elapsed duration?
4. What UTXOS tier or custom quota is needed for the expected number of managed player wallets?
5. What Postgres/Neon sizing and connection-pool settings are needed for the intended transaction load test?

## Proposed Next Plan

Initial implementation status as of 2026-05-15:

- Bun workspace, API, CLI, and core packages are scaffolded.
- PostgreSQL durable state, service wallets, reserve reward lanes, player wallets, Eventun ingestion, reward derivation, entry-fee jobs, mint-reserve jobs, fund moves, chain balance sync, reconciliation, real Mesh builders/signing, signed-job submission, observation, `submission_unknown`, validity-window expiry, background runner, and Azure readiness checks are implemented.
- Preprod integration tests exist for build-submit-observe mint-reserve flow and an opt-in 50+ reward-job load pass. Both are gated behind explicit environment flags because they submit real Preprod transactions.
- A deployment runbook exists for bringing up a new chain/deployment.

Remaining near-term work:

1. Create Azure resources for `cardanoun`.
2. Publish and deploy the API container.
3. Configure Neon/PostgreSQL, bearer tokens, Blockfrost, UTXOS project credentials, `CARDANOUN_SERVICE_ROOT_PRIVATE_KEY`, and background worker settings.
4. Initialize the service wallet and tokun policy for the deployment.
5. Fund the `reserve` operating wallet, let reconciliation top up `mint_authority` for mint jobs, mint reserve `tokun`, and let reconciliation create reserve reward-lane UTxOs.
6. Run deployment readiness and one deployed Eventun smoke batch.
7. Decide whether any additional Preprod integration or load tests are required before mainnet.

## Review Checkpoint

PostgreSQL/Neon is the selected persistence path for the POC. The next checkpoint is deployment readiness in Azure, followed by a deployed Preprod smoke test using Eventun-shaped input and Blockfrost/UTXOS credentials for that deployment.
