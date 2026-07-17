# Ascent Rivals - AccelByte Platform

Date: 2026-07-17
Status: Current deployment constraint
Last reviewed: 2026-07-17

## Related

- [[overview]]
- [[game-client]]
- [[accelbyte-game-records]]
- [[eventun/overview|eventun]]
- [[website]]
- [[../../30_designs/ascent-rivals/website/flows/authentication|Website authentication]]

## Deployment Model

Ascent Rivals uses AccelByte Gaming Services Shared Cloud rather than Private Cloud.

Shared Cloud provides a private namespace in a shared managed environment and exposes only a subset of the features and configuration options available in Private Cloud. A feature documented for AGS in general, or for Private Cloud specifically, must not be assumed available to Ascent Rivals.

Current AccelByte authentication documentation labels the managed tier `Public Cloud`. This knowledge base retains `Shared Cloud` when referring to the Ascent Rivals deployment and configuration, while treating current `Public Cloud` feature-coverage statements as the relevant managed-tier constraint unless AccelByte confirms otherwise.

## Architecture Rule

Every new or materially changed AccelByte integration must be checked against all three of the following before it becomes an approved implementation dependency:

1. current official managed-tier (`Shared Cloud`/`Public Cloud`) documentation and feature-coverage notes;
2. the APIs, configuration, roles, and permissions actually exposed in the Ascent Rivals Shared Cloud namespace;
3. a non-destructive integration smoke test using the intended client and authorization boundary.

If public documentation is ambiguous or conflicts with observed behavior, record the mismatch and normally obtain clarification from AccelByte. A project may deliberately accept reliance on observed deployed behavior when the compatibility risk and fallback consequence are explicit. Website authentication below is one such exception.

Do not design a Shared Cloud dependency around Private Cloud-only capabilities without an explicit replacement, an approved migration to Private Cloud, or a deliberate decision to own an unsupported integration.

## Website Steam Authentication Boundary

Current facts as of 2026-07-17:

- Steam still documents OpenID 2.0 as its browser-based method for a third-party website to obtain and verify a SteamID.
- Steam also documents OAuth 2.0, but that program is for approved partner applications performing scoped Steam API operations on a user's behalf. Valve states that it generally does not issue an OAuth client solely for ordinary website identity login.
- AccelByte's current IAM OpenAPI contract still includes `steamopenid` and the V4 platform-token grant at `POST /iam/v4/oauth/platforms/{platformId}/token`. For `steamopenid`, the platform token is the URL returned by Steam's web authentication flow.
- AccelByte's current authentication coverage table lists Steam in-game login as supported in Public Cloud and Steam web login as not supported in Public Cloud.
- AccelByte's Steam setup guide describes its web-login integration as an AGS Player Portal flow configured in a publisher namespace. That is not the exact architecture used by Ascentun.
- Ascentun performs Steam OpenID in the custom website, then sends the returned assertion to the AccelByte V4 `steamopenid` platform-token endpoint using a server-side confidential IAM client.

The exact Shared Cloud support boundary for Ascentun's custom platform-token flow is therefore not established by the public documentation. The exchange nevertheless works in the deployed Ascentun application, and the project accepts that observed behavior as sufficient evidence for Website V2. The architecture is approved with an explicit vendor-compatibility risk rather than blocked on a separate support response.

### Project Decision and Implementation Verification

The current Ascentun behavior satisfies the architecture-level smoke-test decision. Website V2 implementation should still verify its own behavior as normal release acceptance:

- verify successful sign-in with a known linked player in the matching development environment;
- verify first-login or account-linking behavior without creating duplicate production identities;
- verify refresh, logout, cancellation, invalid assertion, replay rejection, and Login Queue behavior relevant to the deployed namespace;
- record the environment, client boundary, endpoint version, and observed responses in the implementation evidence.

No additional vendor-support answer is required to begin or launch Website V2. If the endpoint stops working or AccelByte gives a concrete removal timeline, select and design a replacement identity architecture at that point.

## General Shared Cloud Review Checklist

For each AccelByte-dependent design:

- identify the owning namespace and whether it is game or publisher scoped;
- identify whether the client is public, confidential, game-server, Extend, Admin Portal, or player-facing;
- verify feature availability for Shared Cloud rather than inferring it from a Private Cloud guide;
- verify the required IAM roles and permissions in the actual namespace;
- check documented Shared Cloud limits, unavailable configuration, quotas, and add-on requirements;
- prefer currently versioned APIs and record any vendor deprecation or compatibility risk;
- retain a release smoke test for the real Shared Cloud boundary.

## Sources

- [AccelByte Shared Cloud introduction](https://docs.accelbyte.io/gaming-services/getting-started/shared-cloud/shared-cloud-intro/)
- [AccelByte authentication coverage](https://docs.accelbyte.io/gaming-services/modules/foundations/identity-access/authentication/)
- [AccelByte Steam identity-provider setup](https://docs.accelbyte.io/gaming-services/modules/foundations/identity-access/authentication/steam-identity/)
- [AccelByte developer FAQ](https://docs.accelbyte.io/gaming-services/knowledge-base/developer-faq/)
- [AccelByte IAM OpenAPI specification](https://github.com/AccelByte/accelbyte-go-sdk/blob/main/spec/iam.json)
- [Steam browser authentication with OpenID](https://partner.steamgames.com/doc/features/auth)
- [Steam OAuth](https://partner.steamgames.com/doc/webapi_overview/OAuth)
