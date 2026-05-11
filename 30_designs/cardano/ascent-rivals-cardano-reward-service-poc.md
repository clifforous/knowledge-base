# Ascent Rivals Cardano Reward Service Proof of Concept

Status: draft for review
Date: 2026-05-07

## Goal

Design a proof-of-concept Cardano service for Ascent: Rivals that receives filtered trusted match events from Eventun, creates service-managed player wallets when needed, mints or distributes a Cardano native reward token, and simulates player-wallet entry-fee transactions.

This is a one-off Cardano ecosystem proof of concept, not a long-term Ascent Rivals product integration. The goal is to demonstrate feasibility, transaction throughput, and service orchestration using Ascent Rivals match data as the source of realistic gameplay events. Players do not interact with, see, recover, link, or manage these proof-of-concept wallets.

This is not an approved implementation plan. It is a research-backed proposal intended to drive review questions before service scaffolding begins.

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
- Their sponsorship flow replaces static placeholder UTxOs with real sponsor UTxOs server-side, signs with a developer-controlled wallet, then returns a transaction for the user wallet to sign.
- UTXOS.dev is a separate third-party service outside Mesh. It is relevant if Mesh is insufficient or if the proof of concept shifts toward passkey/social/non-custodial wallets, but it should not be part of the preferred path.

Sources:

Local knowledge-base sources:

- `50_knowledge/ascent-rivals/overview.md`
- `50_knowledge/ascent-rivals/game-design.md`
- `50_knowledge/ascent-rivals/competition-runtime-terms.md`
- `50_knowledge/ascent-rivals/cardano.md`
- `50_knowledge/ascent-rivals/accountun.md`
- `50_knowledge/ascent-rivals/eventun/overview.md`
- `50_knowledge/ascent-rivals/eventun/api.md`
- `50_knowledge/ascent-rivals/eventun/data-model.md`
- `50_knowledge/ascent-rivals/eventun/events.md`
- `30_designs/ascent-rivals/website/flows/wallet-linking.md`
- `30_designs/midnight/ascent-rivals-midnight-tournament-accounting-design.md`

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
- Eventun should not know or send Cardano wallet addresses for this proof of concept. `cardanoun` owns managed-wallet lookup and creation.
- Mainnet test funding is expected to be limited, roughly USD 1,000 to USD 2,000 converted into ADA. The mainnet test runs until the allocated funds are spent.

## Recommended Approach

Build `cardanoun` as an asynchronous Cardano transaction orchestration service.

Eventun calls `cardanoun` after accepting an end-of-match event batch. Eventun should filter and forward the relevant accepted events, not derive a special reward contract and not include wallet data. `cardanoun` derives proof-of-concept entry-fee and reward transactions from that event input, persists transaction jobs, assigns jobs across funded HD subwallet lanes, submits transactions, and tracks block inclusion and confirmation.

Use a Cardano native fungible token for the proof-of-concept currency:

- Asset name: `tokun`.
- Policy: native script requiring a service mint authority signature.
- Supply model: mint an initial reserve to the main service wallet, then distribute funds across HD child subwallet lanes. If any lane falls below its threshold, top it up from the main wallet.
- Mainnet test hardening: use a separate mainnet-test policy, separate keys, explicit supply caps or operator approval, and clear product copy that the asset is experimental.

Do not include an Aiken entry-fee contract in the first version. Use direct wallet transactions with metadata for the simulated entry fee.

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
- own HD subwallet lane funding, top-ups, and rebalancing
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
  "network": "preprod",
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

- Main HD service wallet: derives child subwallets and can refill them.
- Mint authority wallet: signs minting transactions under the token policy. This may be the main HD wallet in the proof of concept but should be modeled as a distinct role.
- Reserve wallet: holds the main `tokun` reserve and ADA reserve for top-ups.
- Worker subwallets: HD child wallets used as independent transaction lanes. Each holds enough ADA and `tokun` to build reward and simulated entry-fee transactions without blocking on one shared UTxO.
- Sponsor wallet or sponsor lanes: fund fees/min-ADA outputs if separated from reserve.
- Collection wallet: receives entry fees collected from the optional contract.

For the proof of concept, these roles can derive from one mnemonic or root key, but the database and configuration should store role, account index, address index, and network explicitly.

### Player wallets

Initial proof of concept:

- If Eventun includes a player without a proof-of-concept managed wallet, `cardanoun` creates a service-managed custodial wallet.
- Store only encrypted key material or a secret reference. Do not log mnemonic words, private keys, signatures, or full payloads.
- Send the first reward token output with required minimum ADA to the wallet address.

Important constraint:

- A player wallet that holds Cardano native tokens will also hold some ADA in the token UTxO. Sponsorship can avoid requiring the player to acquire ADA for fees, but it cannot make native-token UTxOs ADA-free.

Product guardrail:

- A service-managed proof-of-concept wallet is not the same as a user-linked Cardano wallet.
- Because players will not interact with these wallets, no public UI copy is required for the proof of concept.
- If these wallets are ever shown to users, use separate language such as `Managed reward wallet` and define export/recovery policy first.

## Fee Funding Model

Cardano does not have an Ethereum-style separate gas payer field. Transaction fees are paid by the transaction's input set. A service-sponsored fee pattern can still be built by including one or more service-wallet ADA UTxOs in the transaction, directing change appropriately, and signing with every required wallet.

Recommended proof-of-concept fee model:

- Reward payout transactions spend service reserve UTxOs only. The service wallet supplies reward tokens, minimum ADA for the player token output, and transaction fees.
- Simulated entry-fee transactions spend the player's managed wallet UTxO for the entry-fee token and a service-wallet ADA UTxO for fees and any ADA delta needed by outputs.
- If the simulated entry-fee transaction spends a player wallet UTxO, sign with both the player managed wallet and the service fee subwallet. Mesh multi-signature and partial-signing support should be enough for this, but it must be validated with a local or Preprod integration test before the design is considered implementation-ready.
- Avoid relying on UTXOS.dev sponsorship unless Mesh alone proves insufficient.

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
4. Assign jobs to available worker subwallet lanes.
5. Submit as many independent transactions as reasonable without intentionally clogging blocks.

Recommended worker model:

1. Normalize and persist event-derived transaction jobs.
2. Ensure the player has a Cardano address.
3. Select a funded worker subwallet with enough `tokun`, ADA, and available UTxOs.
4. Build a transaction that either pays a simulated entry fee or transfers one reward amount to the player address.
5. Include minimum ADA in the player output.
6. Attach compact transaction metadata containing a reward reference, not raw personal data.
7. Sign with the required service and/or managed player wallet.
8. Submit through the configured provider.
9. Mark the job `submitted` with transaction hash.
10. Watch for block inclusion and confirmation depth.
11. Mark the job `confirmed` when the confirmation policy is satisfied.

Statuses:

```text
accepted
wallet_required
wallet_created
ready
building
signed
submitted
in_block
confirmed
failed_retryable
failed_terminal
reconciled
```

No batching:

- Do not combine multiple reward facts into one Cardano transaction.
- Throughput comes from multiple UTxO lanes and workers, not from batching reward outputs.
- The throughput goal is to fit many independent transactions in a block without intentionally filling blocks or congesting the network.

Transaction chaining:

- Maintain an internal pending-UTxO ledger for outputs created by submitted transactions.
- Conservative mode waits for block inclusion before spending a newly created change output.
- Chained mode may build child transactions against pending outputs to improve throughput, but it must track parent-child dependencies and fail the whole chain if a parent transaction fails.
- Validate chained-mode behavior against the chosen provider/node. Do not assume every provider exposes mempool state or accepts dependent submissions the same way.

UTxO lane strategy:

- Derive multiple HD child subwallets from the main service wallet and treat each as an independent transaction lane.
- Pre-fund each worker subwallet with enough ADA and `tokun` for a configured number of transactions.
- Pre-split each worker subwallet into many UTxOs sized for expected reward and entry-fee transactions.
- Keep separate lanes for token reserve and ADA fee/min-ADA funding.
- Monitor lane count, pending ratio, reserve balance, and failed submissions.

## Subwallet Balance Management

The main service wallet acts as the reserve. Worker subwallets are treated as consumable transaction lanes.

Balance targets:

- `minAda`: the ADA threshold below which a worker subwallet is paused for top-up.
- `targetAda`: the ADA balance a worker subwallet should have after top-up.
- `minTokun`: the `tokun` threshold below which a worker subwallet is paused for top-up.
- `targetTokun`: the `tokun` balance a worker subwallet should have after top-up.
- `minSpendableUtxos`: the minimum number of independent UTxOs a worker subwallet should have available for parallel job assignment.

Top-up flow:

1. A balance monitor watches each worker subwallet.
2. If a worker falls below threshold, mark it `refill_pending` and stop assigning new jobs to it.
3. Build a refill transaction from the main reserve wallet to the worker subwallet.
4. After the refill is included, optionally fan out the refill output into multiple smaller UTxOs for that worker.
5. Mark the worker `active` once it has enough ADA, `tokun`, and spendable UTxOs.

This model is more important than transaction chaining for the first throughput demo. Independent funded subwallets make it plausible to submit many transactions that can land in the same block without every transaction contending for the same wallet state.

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

Use SQLite for the proof of concept unless the deployment requires multiple active replicas. This avoids standing up a full database while still giving the worker a durable transaction queue.

Preferred deployment:

- SQLite is only durable in Azure if the database file is on persistent storage, such as a mounted Azure Files share or another configured persistent volume. A database file stored only inside an ordinary container filesystem can be lost on restart, redeploy, or reschedule.
- Use a single writer process or a single active service replica for the proof of concept. If multiple replicas are required, move to Postgres or another central store.
- Run SQLite in WAL mode and treat transaction job state as the source of truth for retry/reconciliation.

Azure alternatives:

- Azure Cosmos DB free tier is the best managed durable-store candidate if SQLite-on-Azure-Files is not acceptable. It offers a lifetime free tier for one account with 1000 RU/s and 25 GB storage when enabled at account creation. Use the NoSQL or Table API and model records as schemaless documents. This avoids migration management but adds RU budgeting and a less relational query model.
- Azure SQL Database has a free offer, but it is still a relational database. It is not preferred here because it brings schema migrations back into the project.
- Azure Table Storage is cheap and schemaless, but the free-tier story is less clear than Cosmos DB free tier. Use it only if the Azure subscription already standardizes on Storage Tables.

Initial tables:

- `cardano_network`: network name, provider config, confirmation depth.
- `asset_policy`: policy id, asset name, script type, network, active flag.
- `service_wallet`: role, address, network, derivation path or account index, secret reference, status.
- `worker_subwallet`: service wallet id, derivation index, address, status, min/target ADA, min/target `tokun`, current lane count.
- `player_wallet`: player id, address, network, custody mode, provider wallet id, created at.
- `wallet_secret_ref`: wallet id, secret storage reference, key version, disabled flag.
- `event_batch`: Eventun request id, session id, match id, status.
- `forwarded_event`: event batch id, derived event id, name, player id, heat, progress, event data hash, raw event JSON.
- `reward_fact`: deterministic reward id, kind, player id, amount, source event reference, ordinal, status.
- `transaction_job`: job id, job type, reward id or entry fee id, assigned subwallet id, status, tx hash, parent job id, attempts.
- `transaction_observation`: tx hash, block slot, block hash, confirmation depth, observed at.
- `entry_fee_payment`: event batch id, player id, amount, status, tx hash.
- `utxo_lane`: wallet role, tx hash, output index, amount summary, lane status, reserved job id.

## Deployment Shape

Follow Accountun's deployment style where practical:

- Bun workspace with packages for API, Cardano transaction library, and shared utilities.
- Hono or similar lightweight HTTP API with OpenAPI/Zod schemas.
- Docker image built from the service package.
- Azure Container Registry publish flow similar to Accountun.
- Azure-hosted service with environment-specific configuration for Preprod and Mainnet.
- Persistent storage mount for the SQLite database file.
- Azure Key Vault for secrets; avoid `.env` secrets outside local development.
- Health endpoint and metrics endpoint.
- Operations endpoint for worker subwallet balances, refill status, job backlog, block inclusion rate, and remaining mainnet ADA budget.

Provider options:

- Start with Blockfrost or another Mesh-compatible provider for Preprod.
- Keep provider access behind `cardanoun` and never expose API keys to client code.
- Consider a self-hosted node/Ogmios/Kupo path only after the proof-of-concept transaction model stabilizes.

## Security and Compliance Risks

Custody:

- If Ascent creates wallets and holds keys, it is operating a custodial wallet service for those assets.
- The proof of concept needs a written export/recovery/loss policy before it is exposed to real users.
- Key custody should use Key Vault or a wallet provider designed for delegated custody. Plain encrypted mnemonics in a database are a weak mainnet posture.

Mint authority:

- A hot mint key can inflate supply if compromised.
- Mainnet tests should use separate keys and supply controls, even if the POC uses a simple single-signature policy.

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

Use Mesh headless wallets, native-script minting, worker subwallet reserve transfers, and direct simulated entry-fee payments with metadata.

This proves the core chain loop fastest:

- wallet creation
- minting
- per-event transactions
- chain confirmation
- Eventun bridge
- reserve, worker subwallet, and UTxO lane operations

Tradeoff:

- It does not showcase an Aiken script. That is acceptable for the first grant-provider demonstration because the requested goal is transaction feasibility and throughput.

### Deferred Alternative: Aiken entry-fee script

Add a small Aiken validator for entry fees only if grant-provider feedback specifically asks for a script-address demo.

Tradeoff:

- Better smart-contract demo, but it adds collateral, script debugging, and more failure modes before the basic reward pipeline is proven.

### Wallet-provider POC: UTXOS.dev sponsorship and managed/non-custodial wallets

Use UTXOS for wallet creation and sponsorship.

Tradeoff:

- Could reduce custom wallet infrastructure and enable user-controlled passkey/social wallets, but it introduces an external vendor, a different custody model, pricing/availability dependency, and integration surface that is not yet represented in existing Ascent services.
- This is not recommended for the preferred path because the requested dependency boundary is Mesh first, with other SDKs or services only if Mesh is insufficient.

## Review Questions

1. Which Azure store should be used for the first deployment: SQLite on Azure Files, or Cosmos DB free tier?
2. How many worker subwallet lanes should be pre-funded for the initial Preprod throughput test?
3. What per-worker ADA and `tokun` thresholds should define top-up behavior?
4. Which match modes are eligible: public matchmaking only, gauntlets only, custom games, local/scrimmage, or a dedicated blockchain test queue?
5. What throughput measurement should be shown to grant providers: submitted transactions per minute, block-included transactions per minute, confirmed transactions per minute, cost per transaction, or all of these?
6. What safety limit should stop the mainnet test: remaining ADA reserve, submitted transaction count, block fullness threshold, or elapsed duration?

## Proposed Next Plan

After review, produce an implementation plan with these phases:

1. Define reward facts and Eventun bridge contract.
2. Scaffold `cardanoun` Bun service.
3. Implement Preprod wallet/provider configuration.
4. Implement native token policy and reserve minting CLI.
5. Implement main HD service wallet and worker subwallet derivation.
6. Implement custodial player wallet creation and storage.
7. Implement Eventun filtered-event ingestion.
8. Implement entry-fee and reward job derivation.
9. Implement subwallet balance management, top-ups, and UTxO fan-out.
10. Implement transaction workers, confirmation watcher, and reconciliation.
11. Implement throughput and budget reporting.

## Review Checkpoint

The first decision should be persistence: SQLite on Azure Files or Cosmos DB free tier. My default recommendation is SQLite on Azure Files for the fastest Accountun-like service structure, unless the deployment environment makes file mounts inconvenient. The second decision is how many worker subwallet lanes to pre-fund for the first Preprod throughput test.
