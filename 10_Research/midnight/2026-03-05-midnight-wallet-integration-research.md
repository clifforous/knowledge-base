# Midnight Wallet Integration Research (from ChatGPT Share)

## Source
- Shared conversation: https://chatgpt.com/share/69a90a86-41e8-800d-8c57-b11a1182c5e2
- Topic/title detected: `Crypto Wallet Integration`
- Extraction date: 2026-03-05

## Scope of This Note
This document summarizes key technical and product conclusions extracted from the shared conversation regarding wallet onboarding and custody tradeoffs for a game context (Ascent: Rivals), comparing Midnight vs Cardano approaches.

## Executive Summary
- Midnight provides stronger privacy properties and better long-term architecture for private accounting, but current user onboarding friction is higher because proving infrastructure is still a practical dependency.
- If mainstream user onboarding friction is the primary KPI right now, Cardano-like flows are easier operationally.
- The most practical near-term strategy is walletless-by-default with opt-in claim flows, while using Midnight selectively for privacy-sensitive accounting.

## Key Findings
1. Midnight value proposition is strong for private state and selective disclosure.
2. Proof generation is the gating constraint for frictionless consumer UX today.
3. Requiring users to run or configure proving infrastructure is a non-starter for mainstream game audiences.
4. Server-side proving can reduce user friction but increases trust/custody and privacy-risk exposure.
5. A two-capability model (management vs ownership rights) is feasible conceptually, but does not eliminate the proving/user-control handoff problem.
6. Gas/fee abstraction (batchers, sponsored fees) can materially improve UX, but does not remove proving requirements.

## Candidate Integration Patterns (from the conversation)
### Pattern A: Walletless-by-default, claim later (recommended baseline)
- Keep accrual/entitlements without forcing wallet setup.
- Require wallet only when user explicitly opts in to claim.
- Pros: lowest default friction, avoids forced crypto UX.
- Cons: opt-in claim still hits proving/tooling friction.

### Pattern B: Sponsored transactions + relayed actions
- Backend/batcher pays fees and relays user-authorized actions.
- Pros: better fee UX.
- Cons: still needs signing/proving path; custody boundary must be explicit.

### Pattern C: Embedded self-custody in client
- Generate/store keys client-side and hide complexity.
- Pros: can feel seamless if mature.
- Cons: highest engineering and security complexity; proving/tooling maturity uncertain.

### Pattern D: Shared wallet with limited management capability
- Service can spend only specific game token; user retains broader ownership capability.
- Pros: better than full custody.
- Cons: regulatory/custody interpretation risk remains; proving still required for true user takeover.

## Architecture Implications for Ascent: Rivals
- Use Midnight where privacy and auditability matter most (tournament accounting, receipts, selective disclosure).
- Do not require blockchain interaction for core gameplay participation.
- Design explicit lifecycle transitions:
  - `off-chain accrual` -> `optional wallet link` -> `on-chain claim`.
- Separate product tracks:
  - mainstream path (minimal wallet/proving burden),
  - advanced path (full Midnight control features).

## Risks and Constraints
- Proving dependency and setup complexity remain the primary UX risk.
- Partial custody patterns can still be interpreted as custody in some legal regimes.
- Privacy can be weakened if proving/witness handling moves to centralized infrastructure.
- Documentation/SDK maturity may shift quickly; decisions must be revisited with current vendor docs.

## Research Questions to Resolve Next
1. Can proving be packaged without Docker for end users (native binary, embedded runtime, or wallet-managed flow)?
2. What exact data leaves the client during remote proving, and what privacy guarantees remain?
3. What fee sponsorship patterns are production-ready for your target transaction volume?
4. Which custody model is acceptable for legal/compliance posture in your target jurisdictions?
5. What are the user-dropoff rates at each onboarding stage in a staged rollout?

## Suggested Next Experiments
1. Build a minimal opt-in claim prototype with no wallet requirement at account creation.
2. Time and instrument the end-user claim flow (wallet connect, proving, submission).
3. Validate custody/compliance assumptions on the management-capability model.
4. Run a UX A/B test:
   - Path A: walletless accrual + later claim,
   - Path B: immediate wallet setup.

## Confidence and Limitations
- Confidence: medium.
- Reason: content was extracted from embedded streamed payload in a shared page, not via a clean export format.
- Action: treat this as a working synthesis and validate assumptions against current Midnight/Lace official docs before locking architecture decisions.
