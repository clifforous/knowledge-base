# Ascent Rivals Wallet Linking User Flow

Date: 2026-04-14
Status: Draft

## Related
- [[authentication]]
- [[../unified-design]]
- [[../information-architecture]]
- [[../design-doc-roadmap]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../pages/player-profile]]
- [[../pages/team-profile]]
- [[../pages/gauntlet-detail]]
- [[../../../../50_knowledge/ascent-rivals/eventun/api|eventun-api]]
- [[../../../../50_knowledge/ascent-rivals/eventun/data-model|eventun-data-model]]

## Purpose

Define the V1 wallet linking and wallet management flow for the unified Ascent Rivals website.

This flow covers:

- opening wallet management after Steam login
- viewing linked wallets
- detecting supported browser wallets
- connecting a browser wallet
- proving or associating wallet ownership
- naming a wallet
- linking wallet addresses to the logged-in player
- renaming a linked wallet
- unlinking a wallet
- contextual prompts from token-gated or prize-related surfaces

This flow assumes the user is already authenticated with Steam.

## Implementation Target

The new implementation target is a separate Nuxt/Vue/Reka UI project.

The current `ascentun` app is a behavior and API reference only.

Do not copy Next.js/shadcn implementation details directly unless the behavior still makes sense in the new Nuxt site.

## Product Decision

Wallet linking is a post-login account workflow.

V1 login remains Steam-first. Wallets do not replace Steam authentication in V1.

Wallet state is private account state by default.

Public pages can show wallet-related prompts only when they are contextual and necessary, such as:

- token-gated team join requirements
- prize claim requirements
- gauntlet reward eligibility requirements

Public pages should not expose a player's wallet addresses by default.

## Current Ascentun Implementation Notes

Current implementation files:

- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/page.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-verified-card.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-cardano-connect-card.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-midnight-connect-card.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-action-button.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-name-dialog.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/(logged-in)/player/me/wallets/wallet-forget-dialog.tsx`
- `/home/cgarvis/projects/genun/ascentun/lib/wallet/cardano/client.ts`
- `/home/cgarvis/projects/genun/ascentun/lib/wallet/cardano/hooks.ts`
- `/home/cgarvis/projects/genun/ascentun/lib/wallet/midnight/client.ts`
- `/home/cgarvis/projects/genun/ascentun/lib/wallet/midnight/hook.ts`
- `/home/cgarvis/projects/genun/ascentun/app/api/wallet/cardano/link/verify/route.ts`
- `/home/cgarvis/projects/genun/ascentun/app/api/wallet/midnight/link/verify/route.ts`
- `/home/cgarvis/projects/genun/ascentun/app/api/player/me/wallet/[address]/route.ts`

Current behavior:

- wallet management is a protected page under `/player/me/wallets`
- the page shows `Verified Wallets`
- the page shows `Browser Detected Wallets`
- current linked wallet shape is `address` and `name`
- Cardano browser wallets are detected through Mesh
- Cardano wallet install links mention Eternl, Lace, and Vespr
- Cardano connect flow reads a change address
- Cardano verify flow signs the CSRF token and posts address, signature, key, and name
- server verifies the Cardano data signature before linking the wallet
- Midnight Lace is shown only when `window.midnight.mnLace` exists
- Midnight connect flow gets one or more wallet addresses
- Midnight link flow currently posts wallet addresses and name without a Cardano-style signature challenge
- linked wallet changes refresh the session so the account menu and guards see current wallet state
- linked wallets can be renamed
- linked wallets can be unlinked with a confirmation dialog

Current implementation gaps / production cautions:

- the current route is tied to the old `/player/me/wallets` structure; the new project can choose a cleaner private route
- Cardano linking has a cryptographic signature proof
- Midnight linking currently behaves more like wallet-address association through the connector than signature verification
- production security should decide whether Midnight requires a stronger ownership proof before labeling it `verified`
- wallet management is visually account/admin-like in the current app and should be restyled into the Terminal Ops shell

## Working Route Direction

Preferred Nuxt route:

- `/wallets`

Acceptable aliases:

- `/players/me/wallets`
- `/account/wallets`

Recommendation:

- use `/wallets` as the primary private account route
- optionally redirect old/current links such as `/player/me/wallets` or `/players/me/wallets`

Entry points:

- avatar/account menu
- own player profile wallet action
- token-gated team join prompt
- prize claim prompt
- login redirect after attempting a wallet-required action

## Data Ownership

Eventun is the website source of truth for wallet state.

Wallet data appears in the session after login or refresh.

Current session wallet shape:

- wallet address
- wallet display name

Expected V1 server responsibilities:

- link wallet addresses to the logged-in player
- rename a linked wallet
- unlink wallet addresses from the logged-in player
- refresh session data after wallet mutations

Current Eventun-related endpoints used by `ascentun`:

- `GET /v1/player/me`
- `POST /v1/admin/player/{playerId}/wallet`
- `POST /v1/player/me/wallet/unlink`
- `PUT /v1/player/{playerId}/wallet/{address}`

Nuxt implementation may wrap these through server API routes for token security and CSRF handling.

## Default Wallet Page Structure

Default first-view priority:

1. wallet management header
2. linked wallets
3. detected browser wallets
4. contextual explanation for why wallets matter
5. error/help states

## 1. Wallet Management Header

Purpose:

- explain that wallets are linked to the Steam-authenticated player account
- make the workflow feel private and account-scoped
- avoid making wallet linking sound like V1 login

Content:

- title such as `Wallets`
- short explanation
- current account identity
- optional wallet requirement summary if the user arrived from a gated action

Tone examples:

- `Wallet link station`
- `Steam session required`
- `Wallets connect rewards, gates, and claim flows to your pilot account`

Avoid:

- `Sign in with wallet`
- `Primary identity`
- `Public wallet profile`

## 2. Linked Wallets

Purpose:

- show wallets already associated with the logged-in player
- allow users to manage linked wallet names
- allow users to unlink wallets

V1 display:

- wallet display name
- truncated address
- wallet network/type if available
- rename action
- unlink/forget action

Privacy guardrail:

- show full address only when intentionally expanded or copied
- do not show wallet addresses on public player profile by default

Empty state:

- `No wallets linked yet`
- explain the next step: connect a browser wallet, then verify/link it

## 3. Browser-Detected Wallets

Purpose:

- show wallet extensions the browser can detect
- make connect/verify/link state obvious

Supported V1 wallet families:

- Cardano browser wallets
- Midnight Lace, if available and production-approved

Cardano wallet examples:

- Eternl
- Lace
- Vespr

Wallet card states:

- `Connect`
- `Verify`
- `Linked`
- `Unavailable`
- `Error`

Design guidance:

- use clear action labels instead of only icon states
- do not hide install guidance when no wallet is detected
- keep wallet cards compact; this page is account utility, not a marketing surface

Terminal Ops copy examples:

- `Wallet detected`
- `Signature requested`
- `Wallet linked`
- `No compatible wallet detected`
- `Install a compatible wallet and refresh`

## 4. Contextual Explanation

Purpose:

- explain why linking a wallet matters without overwhelming users

V1 reasons:

- token-gated team eligibility
- gauntlet prize or reward claim flows
- future sponsor/reward mechanics

Guardrail:

- do not mention betting, bounties, or spectator wallet auth as committed V1 features

## Cardano Link Flow

User flow:

1. User opens wallet management while logged in.
2. Site detects installed Cardano wallets.
3. User selects `Connect` for a wallet.
4. Browser wallet extension prompts user to connect.
5. User approves wallet connection.
6. Site reads the change address.
7. If the address is already linked to this account, show `Linked`.
8. If the address is not linked, show `Verify`.
9. User clicks `Verify`.
10. Site asks user for a wallet display name.
11. Site requests a data signature from the wallet.
12. Wallet extension prompts user to sign a challenge.
13. User approves signature.
14. Site sends address, signature, key, and wallet name to the server.
15. Server verifies the signature.
16. Server links the wallet to the logged-in player in Eventun.
17. Server refreshes session wallet state.
18. UI shows the wallet in `Linked Wallets`.

Challenge guidance:

- use a short, opaque, server-issued challenge
- current `ascentun` signs the CSRF token
- production Nuxt can use a dedicated wallet-link challenge if preferred
- rotate the challenge after successful verification
- prevent replay where practical

Error states:

- wallet extension not installed
- user rejects connection
- user rejects signature
- address read fails
- invalid signature
- address already linked
- address linked to another player
- session expired
- Eventun link request fails

## Midnight Link Flow

User flow:

1. User opens wallet management while logged in.
2. Site checks for Midnight Lace connector.
3. If connector is missing, hide Midnight or show install guidance depending on product preference.
4. User selects `Connect`.
5. Browser wallet extension prompts user to connect.
6. User approves connection.
7. Site reads one or more Midnight addresses.
8. If all relevant addresses are already linked, show `Linked`.
9. If not linked, show `Verify` or `Link`.
10. User provides wallet display name.
11. Site sends wallet address list and wallet name to server.
12. Server links addresses to the logged-in player in Eventun.
13. Server refreshes session wallet state.
14. UI shows linked state.

Production caution:

- if Midnight cannot provide a cryptographic ownership proof, do not call the state `verified` without a security/product decision
- labels can distinguish `Linked` from `Verified` if necessary

Open security decision:

- should Midnight require a signed challenge, connector-level proof, or continue as address association?

## Rename Wallet Flow

User flow:

1. User opens linked wallets.
2. User clicks rename/edit on a wallet.
3. Site opens a dialog.
4. User enters a wallet display name.
5. Site validates non-empty name and max length.
6. Site sends rename request.
7. Server updates Eventun.
8. Server refreshes session wallet state.
9. UI shows updated name.

Validation:

- name is required
- max length should be short enough for account menu and compact cards
- current reference uses max length `40`

Error states:

- empty name
- session expired
- wallet no longer linked
- Eventun rename failure

## Unlink Wallet Flow

User flow:

1. User opens linked wallets.
2. User clicks unlink/forget.
3. Site shows confirmation dialog.
4. User confirms.
5. Site sends unlink request.
6. Server unlinks wallet from the logged-in player.
7. Server refreshes session wallet state.
8. UI removes wallet from linked list.

Confirmation copy should be clear:

- `Forget wallet?`
- `This removes the wallet from your Ascent Rivals account. It does not affect the wallet itself.`

Guardrails:

- unlinking should not require wallet extension access
- unlinking should require an authenticated session
- if unlinking affects eligibility, show a warning where possible

## Contextual Wallet Prompts

Wallet prompts can appear outside `/wallets` when a workflow requires wallet state.

Examples:

- token-gated team join
- prize claim
- sponsor/reward claim
- gauntlet payout or reward eligibility

Prompt behavior:

- explain why a wallet is required
- link to wallet management
- preserve return path where practical
- after wallet linking, route the user back to the source page if safe

Example:

- user opens token-gated team page
- team page says `Wallet link required`
- user clicks `Connect Wallet`
- user completes wallet link
- user returns to the team page and can retry join/request if eligible

## Auth and Session Interaction

Wallet page requires Steam login.

If anonymous user opens `/wallets`:

- redirect to login
- preserve `/wallets` as return path

If session expires while on wallet page:

- show expired-session state or redirect to login
- do not render linked wallets from stale state

After any wallet mutation:

- refresh session data
- invalidate client session cache
- update account menu state
- update contextual eligibility checks where applicable

## Privacy and Security Requirements

Do:

- keep access and refresh tokens HTTP-only
- use CSRF protection for wallet mutation endpoints
- validate all wallet mutation inputs on the server
- verify Cardano signatures server-side
- use HTTPS in production
- truncate addresses by default in UI
- avoid logging full wallet addresses unless required for audited backend logs
- avoid logging signatures, keys, token values, or raw wallet payloads in client analytics

Do not:

- ask for seed phrase or private key
- imply Ascent Rivals can custody the user's wallet
- show wallet addresses publicly by default
- treat wallet link as login replacement in V1
- call Midnight addresses `verified` unless the chosen proof model supports that wording

## Accessibility Requirements

- wallet cards must be keyboard reachable
- connect, verify, rename, and unlink actions must have visible text labels
- dialogs must trap focus and return focus correctly
- destructive unlink action must have a clear confirmation state
- wallet connection status must be text, not color alone
- loading states must be announced or visibly labeled

Reka UI primitives likely useful:

- Dialog / AlertDialog
- Toast or status region
- Button
- Tooltip
- Tabs or Accordion if wallet families expand

## Terminal Ops UX Guidance

Use operational language, but keep wallet security copy plain.

Good:

- `Wallet link station`
- `Wallet detected`
- `Signature requested`
- `Wallet linked`
- `Link failed`
- `Forget wallet`
- `Session required`

Avoid:

- `Inject wallet`
- `Hack wallet`
- `Bind cryptographic soul`
- any language that could make users nervous about custody or private keys

## Analytics Events

Potential non-sensitive events:

- wallet page viewed
- wallet family detected
- wallet connect started
- wallet connect succeeded
- wallet connect failed
- wallet verification started
- wallet verification succeeded
- wallet verification failed
- wallet renamed
- wallet unlink started
- wallet unlinked

Do not log:

- full wallet addresses in frontend analytics
- signatures
- verification keys
- access tokens
- refresh tokens
- raw connector payloads

## Acceptance Criteria

- unauthenticated users cannot access wallet management without logging in
- wallet management is reachable from the avatar/account menu
- linked wallets are visible after login when present in session state
- linked wallet addresses are truncated by default
- user can rename a linked wallet
- user can unlink a linked wallet after confirmation
- Cardano wallets can be detected when browser wallets are installed
- Cardano connect handles user rejection gracefully
- Cardano link requires a signature challenge and server-side signature verification
- successful Cardano link refreshes session wallet state
- no Cardano wallet detected state provides install guidance
- Midnight Lace only appears when supported by browser/environment, unless product chooses install guidance
- successful Midnight link refreshes session wallet state
- wallet-required contextual prompts link to wallet management and preserve return context where practical
- no public player profile exposes wallet addresses by default

## Open Questions

- Should the primary route be `/wallets`, `/account/wallets`, or `/players/me/wallets`?
- Should linked wallets be labeled `Linked Wallets` instead of `Verified Wallets` if Midnight remains address-association-only?
- Should Midnight require a signature/challenge proof before production?
- Should wallet type/network be stored and displayed, or inferred from address shape?
- Should wallet names be unique per player?
- Should unlinking a wallet warn if it affects team eligibility, prize claims, or pending rewards?
- Should wallet-required flows return users automatically to the source page after linking, or show an explicit `Return to Team/Gauntlet` action?
