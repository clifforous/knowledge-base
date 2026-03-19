# Ascent Rivals Midnight Tournament Accounting Design
## Executive Summary
## Problem
Ascent: Rivals must award tournament prizes in a way that is both auditable and privacy-preserving. Prize pools are funded by sponsors and the community. To build trust, the system should provide transparent, verifiable accounting while keeping sensitive amounts and participant identities confidential.
## Solution
Introduce a Midnight-backed accounting layer. Each prize-bearing tournament is registered on-chain through an intermediary service operated by the game backend. On-chain state is intentionally minimal: a tournament identifier and Merkle roots for sponsor funding, payout plan, entitlements, and receipts. Human-readable public details are hosted off-chain and can be discovered via the tournament ID (e.g., a URL on our site).
## Scope
On-chain, we will register tournaments, record sponsor prize contributions, commit the payout plan, declare the outcome, and record payment receipts. Tournament winners may optionally link a Midnight wallet to their game account to claim a small bonus in Dust.
Off-chain, we will disburse prizes and host public tournament information, along with the supporting data and metrics needed for audits.
## Out of Scope
This solution does not include custody or distribution of prize pools on-chain, public disclosure of individual sponsor or winner amounts, comprehensive KYC, or cross-chain asset bridging. Only a minimal identity check for bonus claims is included.
## Competition Model and Lifecycle
A tournament is a competitive racing event where racers aim for a podium finish. Points are earned through racing performance and combat actions. After all heats conclude, the points are totaled and the top three competitors are considered the podium finishers.
A tournament may include an optional qualifier window, during which results from eligible races count toward qualification or seeding, or it may be run by invitation only. The main competition is the finals. Finals are composed of one or more stages, although most events use a single stage. Each stage consists of one or more heats, and a heat is a race on a specific course with one or more laps.
Tournaments can be funded by sponsors or other contributors. Sponsors may contribute to a shared prize pool or provide non-monetary awards, and they may choose to remain anonymous or be credited publicly.
## Requirements
These requirements are limited to the interaction between the game backend service and the Midnight chain, which is the focus of this solution.
## Create tournament
The game backend registers each tournament on-chain with a unique identifier. Public, human-readable details (e.g., schedule, courses) are hosted off-chain and discovered via this identifier. Only the game backend submits these transactions.
## Record sponsor donations
The game backend adds sponsors and their contributions on-chain. Sponsors may remain anonymous or be credited publicly. The sponsor on-chain records are shielded and do not reveal amounts.
## Commit payout plan
Prior to the finals concluding, the game backend compiles the prize distribution into a shielded plan and writes its Merkle root on-chain. The plan must be bounded by recorded funding and can be proven in a later phase via a zero-knowledge proof.
## Declare outcome and payout plan
After competition concludes, the game backend publishes the placements of the racers by their salted ids on-chain.
## Record payment receipts
As prizes are disbursed off-chain, the game backend updates the receipts Merkle root on-chain. Receipts cover both cash and item prizes; bonus Dust uses the same receipts tree but is marked as a bonus category.
## Collect bonus address and award bonus
Winners may link a Midnight wallet by signing a message that proves control of an address. The game backend sends the Dust bonus to that address during distribution and records a matching bonus receipt on-chain. No direct user interaction with the contract is required.
## Architecture Overview
This solution centralizes all blockchain interaction in the game backend. The backend records public tournament facts on-chain and writes shielded commitments for sensitive items. Verification is enforced by proof circuits that the backend runs off-chain; the contract verifies those zero-knowledge proofs on-chain. Players never need a wallet; winners may optionally link a Midnight wallet to claim a bonus prize of Dust.
## System Context
### Game Backend
The game backend consists of multiple services, including an intermediary responsible for all interaction with the Midnight chain. This intermediary is the sole on-chain writer. Through it, the backend registers tournaments, records shielded sponsor funding contributions, commits a compiled payout plan, declares the outcome, and records shielded payment receipts. It also maintains the off-chain Merkle trees and salts that can be used to produce proofs for sponsors, auditors, and players. Unless inter-service details matter, these services are referred to collectively as the game backend.
### Tournament Ledger
A single smart contract on Midnight that serves all tournaments. It maintains minimal public state and accepts privacy-preserving updates from the game backend.
### External Roles & Participants
Organizers create and configure tournaments through a web portal. Players compete via the game client and may optionally link a Midnight wallet to claim a bonus prize if they win. Sponsors provide funding and may be credited publicly or remain anonymous. Auditors review public on-chain records and, when permitted, off-chain disclosures.
## Data Classification
### Public State
Minimal tournament facts recorded on-chain for discoverability and accountability. This includes the tournament’s identity and status, and a high-level outcome summary.
### Shielded State
Privacy-preserving on-chain records that reference sensitive information such as donation amounts, payout details, and bonus eligibility. These entries support proof-based checks and allow selective disclosure to authorized parties when needed.
### Off-Chain Records
Operational data maintained outside the chain includes sponsor prize contribution and payout receipt salts and hashes as needed to produce proofs for auditors, sponsors, and players.
## Contract Surface
The contract exposes endpoints sufficient to meet the functional requirements. Only the game-backend intermediary will call these endpoints.
### Create Tournament
Registers a new tournament on-chain with a unique identifier and initializes lifecycle state.
### Record Funding
Writes or updates the funding Merkle-root for the tournament. Individual contributions remain off-chain; only the aggregate root is stored on-chain.
### Commit Payout Plan
Commits the Merkle root of the prize distribution plan. This freezes the distribution prior to seeing results and may be accompanied by a proof that plan cash is bounded by recorded funding.
### Declare Outcome
Publishes an ordered top-N placement salted player ids and advances tournament lifecycle state.
### Record Payment Receipts
Updates the receipts Merkle-root as disbursements occur. Receipts cover both cash and item prizes; optional Dust bonuses are included in the same tree and marked as bonus.
### Cancel Tournament
Cancels a tournament that is still in the Created state with no funding recorded. In future implementation may extend to allow cancelling of a funding tournament as long as proof of refunding sponsors is recorded.
## Typical Flow
1. An organizer creates a tournament in the web interface.
2. One or more sponsors contribute funding to the prize pool.
3. The game backend registers the tournament on-chain and records sponsor funding.
4. The game backend registers the payout distribution plan on-chain.
5. The final tournament concludes.
6. The game backend declares the outcome on-chain.
7. Prizes are paid off-chain.
8. The organizer reports each disbursement in the web interface.
9. The game backend records a matching payment receipt on-chain.
10. Optionally, if a winner confirms a Midnight wallet address the game backend sends a Dust bonus to the verified address, and records the receipt on-chain.
## Tournament Accounting Contract
A single Midnight smart contract serves all tournaments. It records tournament ids publicly while using Merkle roots to shield private data such as funding contributions, the payout plan, and payment receipts.
## State Flow
The contract state progresses in a strict sequence. A tournament starts out in the created state where funding can be recorded. When all funding has been recorded the game backend submits the payout plan and the tournament enters the payout planned state. After the tournament is held the outcome is declared which is the next formal state. Next receipts are recorded as prizes are disbursed. The tournament accounting state transitions to complete after all payments in the payment plan can be shown to have been made. The Cancelled state is allowed only while the tournament is newly created and no funding has been recorded.
## Merkle Roots & Leaf Construction
There are four Merkle trees that are maintained for each tournament. Those trees represent sponsor funding, payment plan, entitlements, and receipts. Each leaf hash is created from a tuple composed of a scope, entity, value, and meta.
Scope is the domain and tournament id as well as a unique identifier in all cases. Entity is the party or reference the record is about such as a sponsor id or a recipient id. It may also include some salt to keep the hash unique. Value is the thing being stored often the cash amount but could be an item identifier or tag. Meta is any other necessary bits of information that must be included.
### Funding
Each funding leaf represents one sponsor funding contribution into the prize pool for a given tournament. The leaves are ordered primarily by a timestamp and secondarily by an identifier.
For funding the entity is the sponsor identifier combined with a salt if a pseudonym is preferred. The value is the type of reward and the quantity. If the type of reward is currency it will also include the currency type. Meta may include additional item information if needed for the reward such as its cash value.
### Payout Plan
The payout plan defines how payment will be distributed by placement. It is declared before the outcome to lock in the planned reward distribution.
For the payout plan the entity is the placement position the payout will be awarded to. It will also include a reward index to support multiple rewards by position. The value is the type of reward and the quantity. If the type of reward is currency it will also include the currency type. Meta may include the item specific identifiers or estimated cash values.
### Entitlements
Entitlements is a mapping of the placements to winners. It has the same scope and value of the payout plan. The entity is a salted player id or if the outcome doesn’t include enough players it can be to another entity such as sponsor.
### Receipts
A receipt entry fulfills exactly one entitlement with its scope, entity, and value being the same. The meta includes an identifier linking to one or more transactions. Those transactions can be on-chain or off-chain, with Dust initially being the only on-chain case.
## Proofs
The design leaves room for formal proofs without changing the contract’s interface. At plan time, the backend can prove that the total in the plan equals the total funding for cash prizes. At completion, it can prove that recorded cash receipts equal the plan. Non-monetary prizes are handled by evidence of issuance and matching, rather than by sums.
For sponsors we can give them information to self prove their funds are recorded and distributed. Similarly for players we can give information to prove they are included in the entitlements and receipt of funds.
## Bonus Handling
Players can link a Midnight wallet anytime before the payout plan is declared to receive a bonus Dust distribution. The link is not a full vetting of identity, just a simple proof by a user who is logged into their game account that they can sign transactions with the wallet.
### Wallet Linking Flow
1. The player signs in to their game account and requests to link a Midnight wallet.
2. The backend returns a message including a nonce for the player to sign.
3. The player signs the message and returns the signed message to the backend.
4. The backend verifies the signature and records the players payment address.
5. When entitlements are declared a line item for the Dust payout is included.
6. A receipt for the Dust payout is recorded with the payout transaction.
## Off-Chain Records
This section describes the off-chain records used to compute the Merkle roots and proofs using the information stored on-chain. The game backend will store this data to support producing proofs and updating roots.
## Sponsor Funding
We will record the following information about sponsor funding in our internal database to support proving inclusion in the prize pool.
* **Tournament Id** - The internal id of the tournament the sponsor is funding
* **Sponsor Id** - Our internal system identifier for the sponsor
* **Sponsor Salt** - Salt used to create the sponsor pseudonym for the tournament
* **Contribution Type** - Currency or Item
* **Contribution Quantity** - The amount of currency or for an item the quantity of the item
* **Contribution Salt** - Salt to protect leaking the contribution amount
* **Meta** - Any transaction identifiers or item specific values like a sku number.
## Payment Plan
The payout plan will be compiled into line items from a general payout plan. For example the web tool might indicate a participation prize of $10 and a distribution of 50% / 30% / 20% of the remainder of the prize pool to the top three winners. The plan would just be the exact amounts for each placement position given those rules. We will record the following information about the payment plan in our internal database.
* **Tournament Id** - The internal id of the tournament the sponsor is funding
* **Placement** - The placement which the payment will be linked to
* **Reward Index** - Usually 0 but if for example first place also gets a new car then that would warrant its own separate index
* **Reward Type** - Either the currency or an “item”
* **Reward Amount** - The amount to be awarded
* **Reward Salt** - Salt used to prevent leaking reward amount.
## Outcome & Entitlements
The outcome will have already been stored in the database at part of the normal competition game flow. Entitlements will be a mapping of the payment plan to the outcome. The only additional data needed is the optional salt for player ids.
* **Tournament Id** - The internal id of the tournament the sponsor is funding
* **Player Id** - The internal id of the player that is entitled to a reward
* **Player Salt** - The salt used to prevent leaking the internal player id.
## Receipts
Receipts will be recorded as rewards are distributed to players. A web form will be used to record the receipts.
* **Tournament Id** - The internal id of the tournament the receipt is being made for
* **Player Id** - The internal id of the player
* **Receipt Amount** - The amount of funds distributed to the player
* **Receipt Type** - The type of funds distributed to the player
* **Receipt Salt** - Salt used to prevent linking receipt amount
## Merkle Tree
To make indexing simple and reduce the need to rehash we will store some information about transactions made to update the different Merkle trees.
* **Id** - Just an increasing value to order the updates and provide a reference for the leaf hashes
* **Tournament Id** - The internal id of the tournament the transaction relates to
* **Kind** - Which tree was updated or initialized
* **Root** - Current root of the tree after the update
* **Leaf Count** - How many leaves are in the tree
* **Transaction Hash** - The transaction hash for the updated tree
* **Block Number** - The block number the transaction ended up in
Notes
* Submit proofs that all prizes are paid on-chain so anyone can see
* Could give them a token to represent their donation. 
