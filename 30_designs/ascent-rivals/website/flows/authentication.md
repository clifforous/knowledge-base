# Ascent Rivals Authentication User Flow

Date: 2026-04-14
Status: Approved scope baseline; implementation details open
Last reviewed: 2026-07-16

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../design-doc-roadmap]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../pages/homepage]]
- [[../pages/player-profile]]
- [[../../../../50_knowledge/ascent-rivals/accelbyte-platform|AccelByte platform]]

## Purpose

Define the V1 authentication flow for the unified Ascent Rivals website.

This flow covers:

- anonymous login entry points
- Steam OpenID redirect
- callback/session creation
- post-login navigation state
- avatar/account menu
- sign-out behavior
- expired-session handling

Wallet linking and wallet-derived account state are outside the initial Website V2 scope.

## Product Decision

V1 authentication is Steam-only.

Use a direct `Sign in with Steam` action. Do not show a provider picker when Steam is the only implemented provider.

Steam remains the account authority for initial website login.

Epic or Discord authentication may be reconsidered if a concrete player or viewer account use case is approved. That future work requires explicit decisions about canonical identity, account linking and merging, duplicate accounts, roles, profile ownership, and recovery. A speculative dropdown does not solve those problems, so Website V2 should not prebuild provider-selection UI or a provider registry solely for hypothetical expansion.

## Implementation Target

The implementation target is the greenfield Next.js/React/TypeScript Website V2 project.

The current `ascentun` app is a behavior and API reference only.

Do not copy current Ascentun components or implementation gaps directly; preserve only behavior that remains part of the approved scope.

## Protocol and Shared Cloud Assessment

As of 2026-07-16, Steam OpenID 2.0 remains Steam's documented browser-authentication method for third-party websites. Steam's separate OAuth 2.0 program is intended for approved partner applications that need scoped access to Steam APIs; it is not a generally available replacement for identity-only website login.

AccelByte's current IAM OpenAPI contract still documents `steamopenid` and the V4 platform-token grant used by Ascentun. No Steam or AccelByte deprecation notice was found for that core exchange.

However, Ascent Rivals runs on AGS Shared Cloud. AccelByte's current authentication coverage table marks Steam in-game login as supported in Shared Cloud and Steam web login as unsupported. The detailed Steam guide describes the unsupported web integration as an AGS Player Portal flow in a publisher namespace, while Ascentun instead performs OpenID in the custom website and submits the returned assertion to the V4 platform-token endpoint with a confidential client. Public documentation does not explicitly confirm whether this custom flow is a supported Shared Cloud contract.

Decision:

- retain `Steam OpenID callback -> server-side AccelByte V4 steamopenid grant -> AccelByte website session` as the provisional Website V2 implementation baseline;
- do not replace it with Steam OAuth 2.0 or a native Steam auth ticket flow, because neither is the documented general browser-login replacement;
- do not treat the baseline as launch-approved until the Shared Cloud verification gate in [[../../../../50_knowledge/ascent-rivals/accelbyte-platform|AccelByte platform]] is complete;
- if AccelByte confirms the custom grant is unsupported, stop and choose a different identity and authorization architecture before implementing Website V2 authentication.

Required hardening when the flow is implemented:

- construct the OpenID realm and callback from one trusted configured public origin, not the request `Host` header;
- store a signed, time-limited login transaction containing a nonce and validated relative return path;
- reject protocol-relative, external, expired, replayed, or otherwise invalid return state;
- require the expected OpenID mode, provider endpoint, claimed-identity shape, callback target, and signed response fields before exchange;
- submit only the required OpenID assertion fields to AccelByte and do not request unused AX/SREG profile attributes;
- keep the AccelByte client secret, access token, and refresh token server-only and use secure HTTP-only cookies;
- handle cancellation, AccelByte linking responses, Login Queue responses, refresh failure, and retry without logging raw assertions or tokens.

## Current Ascentun Implementation Notes

Current implementation files:

- [navigation login](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/components/nav/nav-login.tsx)
- [Steam navigation login](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/components/nav/nav-steam-login.tsx)
- [user navigation](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/components/nav/nav-user.tsx)
- [Steam login route](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/app/api/auth/steam/login/route.ts)
- [Steam callback route](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/app/api/auth/steam/callback/route.ts)
- [logout route](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/app/api/logout/route.ts)
- [session server](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/lib/session/server.ts)
- [token refresh component](https://github.com/ikigai-github/ascentun/blob/589d0e2ecb9a6c1153c4e7a259c6ee5fe0bdea57/components/auth/token-refresh.tsx)

Current behavior:

- anonymous users see a login button in the navigation
- login opens a provider dropdown
- the only available provider is Steam
- Steam login links to `/api/auth/steam/login`
- the server redirects to `https://steamcommunity.com/openid/login`
- Steam prompts for username/password and external-site consent
- Steam redirects back to `/api/auth/steam/callback`
- the callback exchanges the Steam OpenID platform token through AccelByte
- the session is populated from Eventun `/v1/player/me` when available
- if Eventun player data is unavailable, the session falls back to AccelByte public user data
- access token and refresh token are stored in HTTP-only cookies
- display-safe user info is stored in a readable user-info cookie for client navigation state
- a CSRF cookie/header pattern is used for mutating requests
- after login, the login button is replaced by the user's avatar/name menu
- the avatar menu currently exposes `Career`, `Wallets`, and `Log out`

Current implementation gap:

- `/api/auth/steam/login` currently sets the callback `state` to `/`, so it does not preserve the current page.
- the current `Career` dropdown item is present visually but is not linked in `nav-user.tsx`.
- `/api/logout` redirects to `/`, but the client logout handler only refreshes the current route after the fetch; protected-route guards may then decide where the user lands.

Website V2 should implement the desired behavior below rather than copying those gaps.

## Desired V1 Flow Summary

1. Anonymous user clicks `Sign in with Steam`.
2. Site records the user's current safe return path.
3. Site redirects the user to Steam OpenID.
4. User enters Steam credentials on Steam.
5. Steam shows an external-site consent screen.
6. User accepts.
7. Steam redirects back to the Ascent Rivals auth callback.
8. Site exchanges the Steam identity through AccelByte.
9. Site populates the website session.
10. Site redirects the user back to the original page when safe and valid.
11. Top-bar login is replaced by avatar/account menu.

## Entry Points

Primary entry point:

- global top-bar `Sign in with Steam`

Secondary entry points:

- login-required action prompts
- protected-route redirects
- team join/request actions
- gauntlet create/edit actions

Global navigation rule:

- login/avatar control must never collapse away on mobile
- secondary nav links can collapse before login/avatar does

## Anonymous Navigation State

When not logged in:

- show a sign-in action in the top bar
- do not show career, team, or admin account options
- public entity pages remain browseable
- login-required actions should be visible only when useful and should explain that Steam sign-in is required

Direct Steam action:

- wide layouts should use the explicit label `Sign in with Steam`;
- compact layouts may use the Steam icon with `Sign In` when necessary, while retaining the accessible name `Sign in with Steam`;
- activating the control starts the Steam flow directly rather than opening an intermediate menu;
- add a provider picker only after another provider and its identity/linking contract are approved and implemented.

Recommended copy:

- `Sign in with Steam`
- `Steam sign-in required`
- `Connect Steam to continue`

Avoid:

- `Choose login provider` while Steam is the only implemented option
- language implying another login provider is active when Steam is the only supported provider

## Return Path Handling

Desired behavior:

- login should attempt to return the user to the page they were on before signing in
- only safe relative paths should be accepted as return destinations
- missing, invalid, external, or unsafe return paths should fall back to `/`

Recommended implementation shape:

- login action calls an auth endpoint with `returnTo={currentPathAndQuery}`
- auth endpoint stores or signs that value into the OpenID `state`
- callback validates the state and redirects to the safe return path

Examples:

- user starts at `/gauntlets/starforge-02`
- user clicks `Sign in with Steam`
- callback returns to `/gauntlets/starforge-02`

- user starts at `/teams/abc`
- user clicks `Request to Join`
- login completes
- callback returns to `/teams/abc`, where the join/request action can be resumed or made visible

Security guardrail:

- never redirect to arbitrary external URLs from auth `state`
- prefer relative paths beginning with `/`
- reject protocol-relative paths such as `//example.com`
- reject full URLs unless they match an explicit allowlist

## Steam Redirect

The site redirects to Steam OpenID.

External Steam steps:

- user enters Steam username/password
- Steam may require Steam Guard or other account checks
- Steam shows a page explaining that the target website is not affiliated with Steam
- user chooses whether to continue

UX expectation:

- Ascent Rivals should not attempt to restyle or frame the Steam credential pages
- Ascent Rivals should make it clear before redirect that the next screen is Steam-owned

Recommended pre-redirect copy:

- `Redirecting to Steam`
- `Steam will verify your account. Ascent Rivals will not see your Steam password.`

## Callback and Session Creation

Callback responsibilities:

- validate Steam OpenID callback parameters
- exchange Steam identity through AccelByte
- receive AccelByte access and refresh tokens
- fetch website session context
- set session cookies
- set CSRF token/cookie state
- redirect to safe return path

Session population priority:

1. Eventun `/v1/player/me`
2. AccelByte public user data fallback

Session user info should include:

- user id
- display name
- avatar
- roles
- team summary, if available
- pending team invitation/join-request summary, if available
- access token expiry timestamp
- refresh token expiry timestamp

Display-safe user info can be available to the client for shell rendering.

Access and refresh tokens must remain HTTP-only.

## Post-Login Navigation State

After login:

- replace `Sign in` with the avatar/account menu
- show player avatar if available
- fall back to initials or a branded pilot placeholder if no avatar exists
- keep the avatar/account menu visible at all breakpoints

Approved initial avatar menu items:

- `My Career` links to the authenticated pilot's canonical `/players/[id]` profile;
- `My Team` links to the authenticated team when one exists, otherwise to `/teams` with the user's no-team or pending-request context;
- `My Team` may carry one concise, accessible count/status for pending invitations and join requests rather than creating separate menu items;
- `Admin / Operations` appears only when the authenticated account is authorized and at least one administrative destination is available;
- `Sign Out` triggers logout without a confirmation dialog.

Guardrail:

- do not add team creation, gauntlet creation/editing, or ordinary entity actions to the account menu; keep those actions on their relevant pages;
- do not render a disabled or dead `Admin / Operations` entry;
- authorization is enforced before rendering the admin entry and again by every protected route/API;
- visually separate `Sign Out` from navigation items and keep it easy to find;
- the account menu should remain a compact account switchboard rather than a full administrative navigation tree.

## Sign-Out Flow

User action:

- logged-in user opens avatar/account menu
- user clicks `Sign Out`

System behavior:

- clear access token cookie
- clear refresh token cookie
- clear user-info cookie
- clear CSRF cookie or rotate CSRF state
- invalidate client session cache
- refresh or redirect the current view

Desired route behavior:

- if the user is on a public page, keep them on that page and remove private overlays
- if the user is on a fully private account page, redirect them to `/`
- if the user is on an authorized management page, prefer redirecting to the public parent object if it is clear
- if no safe public parent is clear, redirect to `/`

Examples:

- sign out from `/gauntlets/starforge-02` stays on `/gauntlets/starforge-02`
- sign out from `/players/some-player` stays on `/players/some-player`
- sign out from `/teams/team-id/manage` redirects to `/teams/team-id` if available, otherwise `/`
- sign out from `/gauntlets/gauntlet-id/edit` redirects to `/gauntlets/gauntlet-id` if available, otherwise `/`

Design note:

- the user should not be stranded on a blank protected page after sign-out

## Protected Route Handling

Protected pages should not render private content to anonymous users.

If anonymous user opens a protected route:

- redirect to login page or trigger login prompt
- preserve the attempted route as the post-login return path when appropriate

If session is expired:

- show login with an expired-session message
- preserve the attempted route when safe

If user is logged in but lacks authorization:

- redirect to the nearest public page when possible
- otherwise redirect to `/`
- use a clear message if the redirect would otherwise feel surprising

Examples:

- unauthenticated `/teams/[id]/manage` should route to sign-in and return to the management route after successful login only when the user is authorized
- unauthorized `/gauntlets/[id]/edit` should route to `/gauntlets/[id]`
- unauthorized `/teams/[id]/manage` should route to `/teams/[id]`

## Token Refresh and Expiration

V1 should preserve the current refresh model:

- refresh access tokens before expiry when refresh token is still valid
- update session cookies after refresh
- rotate or update CSRF state as needed
- if refresh fails, mark session expired and require login

Expired state behavior:

- public pages remain usable
- private overlays disappear
- protected pages redirect to login with an expired-session message

Copy examples:

- `Session expired`
- `Reconnect Steam to continue`
- `Authentication refresh failed`

## Error and Cancellation States

Steam login canceled:

- return to the original page if practical
- show a non-blocking message or login page state

Steam or AccelByte token exchange failed:

- show login failure state
- allow retry
- preserve safe return path when practical

Eventun player lookup failed but AccelByte user lookup succeeds:

- allow login with reduced profile context
- avatar/name can come from AccelByte
- team and player-specific overlays may be absent until Eventun data is available

No session after callback:

- route to `/login?failed=true` or equivalent
- avoid dumping users onto a generic error page without a retry path

Security error in return path:

- drop return path
- redirect to `/`

## Terminal Ops UX Guidance

The auth UI should feel integrated with Terminal Ops, but it should remain plain and trustworthy.

Good labels:

- `Steam Link Required`
- `Redirecting to Steam`
- `Session Established`
- `Session Expired`
- `Reconnect Steam`
- `Sign Out`

Avoid:

- fake hacking language
- unclear labels like `Authorize Signal` for the main login button
- making Steam's external consent step sound like an Ascent Rivals-branded permission

## Accessibility Requirements

- sign-in action must be reachable by keyboard
- compact sign-in treatment must retain the accessible name `Sign in with Steam`
- avatar menu must have an accessible label such as `Account menu`
- sign-out must be a real button/menu item, not only an icon
- loading and error states must be announced or visible as text
- mobile top bar must preserve login/avatar access

## Analytics Events

Potential non-sensitive events:

- login started
- login succeeded
- login failed
- login canceled, if detectable
- logout clicked
- logout completed
- token refresh failed

Do not log:

- Steam credentials
- access tokens
- refresh tokens
- raw OpenID payloads

## Acceptance Criteria

- anonymous users can start Steam login from the top bar
- the direct sign-in control starts Steam authentication without an intermediate provider picker
- compact sign-in treatment retains the accessible name `Sign in with Steam`
- login from a public page returns to that page after Steam callback
- login from a protected route returns to that route after successful login when the user is authorized
- unsafe return paths fall back to `/`
- the custom `steamopenid` V4 grant is verified and confirmed as an accepted Shared Cloud dependency before launch
- OpenID realm and callback URLs use a trusted configured public origin rather than a request-supplied host
- login transaction state is signed, time-limited, nonce-bound, replay-resistant, and restricted to safe relative return paths
- successful login replaces sign-in control with avatar/account menu
- avatar/account menu includes working `My Career`, `My Team`, and `Sign Out` items
- `My Team` exposes pending invitation/request status concisely when available
- `Admin / Operations` is absent unless the account is authorized and an administrative destination exists
- creator and entity-management actions remain on their relevant pages rather than in the account menu
- sign-out from public pages keeps the user on the current public page
- sign-out from fully private pages redirects to `/`
- sign-out clears server cookies and client session state
- expired sessions prompt re-login without exposing private content

## Open Questions

- Should expired protected routes show `/login?expired=true&returnTo=...` or trigger Steam login directly?
- Should logout from authorized management routes prefer public parent routes or always return to `/`?
