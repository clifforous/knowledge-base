# Ascent Rivals Authentication User Flow

Date: 2026-04-14
Status: Draft

## Related
- [[../unified-design]]
- [[../information-architecture]]
- [[../design-doc-roadmap]]
- [[../terminal-ops-design-system]]
- [[../tone-and-voice]]
- [[../pages/homepage]]
- [[../pages/player-profile]]
- [[wallet-linking]]

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

This flow does not cover wallet linking in detail. Wallet linking is specified in [[wallet-linking]].

## Product Decision

V1 authentication is Steam-only.

The UI may still use a provider picker if the team wants to leave room for future providers, but the simplest V1 experience can be a direct `Sign in with Steam` action.

Steam remains the account authority for initial website login.

Wallets are linked only after Steam login.

## Implementation Target

The new implementation target is a separate Nuxt/Vue/Reka UI project.

The current `ascentun` app is a behavior and API reference only.

Do not copy Next.js/shadcn implementation details directly unless the behavior still makes sense in the new Nuxt site.

## Current Ascentun Implementation Notes

Current implementation files:

- `/home/cgarvis/projects/genun/ascentun/components/nav/nav-login.tsx`
- `/home/cgarvis/projects/genun/ascentun/components/nav/nav-steam-login.tsx`
- `/home/cgarvis/projects/genun/ascentun/components/nav/nav-user.tsx`
- `/home/cgarvis/projects/genun/ascentun/app/api/auth/steam/login/route.ts`
- `/home/cgarvis/projects/genun/ascentun/app/api/auth/steam/callback/route.ts`
- `/home/cgarvis/projects/genun/ascentun/app/api/logout/route.ts`
- `/home/cgarvis/projects/genun/ascentun/lib/session/server.ts`
- `/home/cgarvis/projects/genun/ascentun/components/auth/token-refresh.tsx`

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

V1 Nuxt should implement the desired behavior below rather than copying those gaps.

## Desired V1 Flow Summary

1. Anonymous user clicks `Sign in` or `Sign in with Steam`.
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

- global top-bar `Sign in` or `Sign in with Steam`

Secondary entry points:

- login-required action prompts
- protected-route redirects
- wallet linking page
- team join/request actions
- gauntlet create/edit actions
- prize claim actions

Global navigation rule:

- login/avatar control must never collapse away on mobile
- secondary nav links can collapse before login/avatar does

## Anonymous Navigation State

When not logged in:

- show a sign-in action in the top bar
- do not show wallet, career, team, or admin account options
- public entity pages remain browseable
- login-required actions should be visible only when useful and should explain that Steam sign-in is required

Provider picker rule:

- if Steam is the only supported provider, a direct `Sign in with Steam` button is acceptable
- if using a provider picker, the UI should not imply other providers are currently available

Recommended copy:

- `Sign in with Steam`
- `Steam sign-in required`
- `Connect Steam to continue`

Avoid:

- `Choose login provider` if there is only one visible option and no near-term provider expansion
- language implying wallet-only auth exists in V1

## Return Path Handling

Desired behavior:

- login should attempt to return the user to the page they were on before signing in
- only safe relative paths should be accepted as return destinations
- missing, invalid, external, or unsafe return paths should fall back to `/`

Recommended Nuxt shape:

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
- linked wallets summary
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

Required V1 avatar menu items:

- `Career`
- `Wallets`
- `Sign out`

Recommended routes:

- `Career` should link to the logged-in player's public career/profile route
- `Wallets` should link to the wallet management route
- `Sign out` should trigger logout without requiring a separate confirmation

Route naming is still final-implementation dependent.

Preferred Nuxt route direction:

- `Career`: `/players/[currentPlayerId]` or a stable alias such as `/players/me`
- `Wallets`: `/wallets` or `/players/me/wallets`

Guardrail:

- the account menu should not become a full admin nav
- admin shortcuts can appear later, but public identity actions should remain clear

## Sign-Out Flow

User action:

- logged-in user opens avatar/account menu
- user clicks `Sign out`

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
- sign out from `/players/me/wallets` redirects to `/`
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

- unauthenticated `/players/me/wallets` should route to sign-in and return to wallets after successful login
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
- team, wallet, role, and player-specific overlays may be absent until Eventun data is available

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
- provider menu, if used, must use accessible menu primitives
- avatar menu must have an accessible label such as `Account menu`
- sign-out must be a real button/menu item, not only an icon
- loading and error states must be announced or visible as text
- mobile top bar must preserve login/avatar access

## Analytics Events

Potential non-sensitive events:

- login started
- login provider selected
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
- wallet addresses from this flow unless explicitly covered by wallet analytics policy

## Acceptance Criteria

- anonymous users can start Steam login from the top bar
- if only Steam is supported, the UI does not imply multiple active providers
- login from a public page returns to that page after Steam callback
- login from a protected route returns to that route after successful login when the user is authorized
- unsafe return paths fall back to `/`
- successful login replaces sign-in control with avatar/account menu
- avatar/account menu includes Career, Wallets, and Sign out
- Career menu item is a working link
- Wallets menu item is a working link
- sign-out from public pages keeps the user on the current public page
- sign-out from fully private pages redirects to `/`
- sign-out clears server cookies and client session state
- expired sessions prompt re-login without exposing private content

## Open Questions

- Should the final V1 UI use a direct `Sign in with Steam` button or keep a provider picker for future providers?
- Should the logged-in career link be `/players/[id]`, `/players/me`, or another stable alias?
- Should expired protected routes show `/login?expired=true&returnTo=...` or trigger Steam login directly?
- Should admin shortcuts appear in the avatar menu in V1, or stay only as in-page actions?
- Should logout from authorized management routes prefer public parent routes or always return to `/`?
