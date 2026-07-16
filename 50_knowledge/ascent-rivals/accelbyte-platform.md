# Ascent Rivals - AccelByte Platform

Date: 2026-07-16
Status: Current deployment constraint
Last reviewed: 2026-07-16

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

## Architecture Rule

Every new or materially changed AccelByte integration must be checked against all three of the following before it becomes an approved implementation dependency:

1. current official Shared Cloud documentation and feature-coverage notes;
2. the APIs, configuration, roles, and permissions actually exposed in the Ascent Rivals Shared Cloud namespace;
3. a non-destructive integration smoke test using the intended client and authorization boundary.

If public documentation is ambiguous or conflicts with observed behavior, record the integration as provisional and obtain clarification from AccelByte. A feature working incidentally does not by itself establish that AccelByte supports it as a durable Shared Cloud contract.

Do not design a Shared Cloud dependency around Private Cloud-only capabilities without an explicit replacement, an approved migration to Private Cloud, or a deliberate decision to own an unsupported integration.

## Website Steam Authentication Boundary

Current facts as of 2026-07-16:

- Steam still documents OpenID 2.0 as its browser-based method for a third-party website to obtain and verify a SteamID.
- Steam also documents OAuth 2.0, but that program is for approved partner applications performing scoped Steam API operations on a user's behalf. Valve states that it generally does not issue an OAuth client solely for ordinary website identity login.
- AccelByte's current IAM OpenAPI contract still includes `steamopenid` and the V4 platform-token grant at `POST /iam/v4/oauth/platforms/{platformId}/token`. For `steamopenid`, the platform token is the URL returned by Steam's web authentication flow.
- AccelByte's current authentication coverage table lists Steam in-game login as supported in Shared Cloud and Steam web login as not supported in Shared Cloud.
- AccelByte's Steam setup guide describes its web-login integration as an AGS Player Portal flow configured in a publisher namespace. That is not the exact architecture used by Ascentun.
- Ascentun performs Steam OpenID in the custom website, then sends the returned assertion to the AccelByte V4 `steamopenid` platform-token endpoint using a server-side confidential IAM client.

The exact Shared Cloud support boundary for Ascentun's custom platform-token flow is therefore not established by the public documentation. The existing architecture remains the provisional Website V2 baseline because both the Steam browser protocol and the AccelByte platform-token contract remain current, but it is not an approved launch dependency until the Shared Cloud verification gate below is complete.

### Verification Gate

Before Website V2 authentication implementation is frozen:

- smoke-test the existing Ascentun flow against the intended Shared Cloud environment with a known linked player;
- verify first-login or account-linking behavior without creating duplicate production identities;
- verify refresh, logout, cancellation, invalid assertion, replay rejection, and Login Queue behavior relevant to the deployed namespace;
- confirm that the intended confidential IAM client and `steamopenid` V4 grant are supported for a custom website in Shared Cloud, preferably through an explicit AccelByte support response or equivalent durable documentation;
- record the environment, client boundary, endpoint version, observed responses, and support conclusion in this note or the implementation plan.

If AccelByte confirms that the custom grant is unsupported, select a different website identity architecture before implementation. Potential alternatives require separate design because AccelByte credential login, website-owned Steam sessions with a backend-for-frontend authorization boundary, and game-assisted website login have materially different identity, authorization, and account-linking behavior.

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
