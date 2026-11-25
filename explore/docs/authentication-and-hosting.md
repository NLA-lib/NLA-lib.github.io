# Authentication and hosting: next implementation slice

The existing deployment is GitHub Pages, not AWS static hosting. The repository's
`.github/workflows/deploy.yml` builds the Explorer together with the homepage and
publishes them to nla-lib.org. Preserve that pipeline and the independent static
mathematical library. The current collaboration server is loopback-only and SQLite
is a local prototype; it must not be exposed as the production backend.

## Proposed first hosted slice

Keep the frontend on GitHub Pages. Add an AWS HTTP API and Lambda backend on a
proposed `api.nla-lib.org` subdomain, with DynamoDB for profiles, sessions, drafts,
discussions and notifications. Keep published content in Git. Store provider/app
secrets in Secrets Manager and define resources using SAM. These are proposals;
no AWS resources, DNS records or credentials have been created or changed.

Start with ORCID sign-in, public profiles and read-only published content. Enable
comments and reactions after permission and abuse checks pass. Then port private
drafts and revision proposals. Publication remains a later GitHub App integration
with branch protections and editorial review; a login does not grant editor trust.

## ORCID versus Cognito

ORCID supports both OAuth authorization-code authentication and OpenID Connect. It
can return an ID token with the `openid` scope. This makes an OIDC integration a
real alternative, not an unsupported-provider workaround.
[ORCID authentication tutorial](https://info.orcid.org/documentation/api-tutorials/api-tutorial-get-and-authenticated-orcid-id/)

On 2026-11-25, the production and sandbox discovery documents both advertised
`client_secret_post` and authorization-code responses. Cognito's OIDC requirements
include `client_secret_post`, HTTPS endpoints and claim mapping. This establishes
prerequisite compatibility; it is not an end-to-end Cognito sign-in test.
[ORCID discovery](https://orcid.org/.well-known/openid-configuration),
[AWS OIDC requirements](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-oidc-idp.html)

| Option | Benefits | Work and tradeoffs |
| --- | --- | --- |
| Direct ORCID | Fewer services; fits the required Lambda/API/DynamoDB stack | We own application sessions, logout and provider-flow integration; use a vetted OAuth/OIDC library |
| Cognito with ORCID OIDC | Managed provider federation and standardized Cognito tokens; room for other sign-in methods | Adds a user pool, app client and domain; must test scopes, subject mapping, and accounts without email |

Recommendation for the first slice: direct ORCID through the backend. The user
has chosen to register a production client using their own ORCID account. Keep Cognito as a viable option if other
identity providers or managed authentication features become requirements. Neither
option supplies academic trust, library roles or responsible-person attribution.
Do not require email for an ORCID account or link accounts by a supplied email/iD.

## Browser flow and endpoints

1. The user chooses Sign in with ORCID. `GET /auth/login` records short-lived,
   random, browser-bound OAuth state and redirects to ORCID.
2. ORCID redirects to the registered HTTPS `GET /auth/callback`. Lambda verifies
   state, expiry and single use, exchanges the code server-side, and validates
   the returned identity (including issuer, audience and nonce if using OIDC).
3. The backend maps the authenticated provider subject to an internal person ID.
   New people receive contributor permissions. Typed profile ORCID text is not
   evidence of authentication.
4. Issue an opaque application session in a `Secure`, `HttpOnly`, `SameSite=Lax`
   host-only cookie scoped to the API. Store only its hash and expiry in DynamoDB.
   Provider credentials and tokens stay off the frontend.
5. `GET /me` supplies profile and permissions; `POST /auth/logout` revokes the
   session. Every mutation checks the current account status, effective role,
   allowed origin and a session-bound CSRF token.

The static frontend needs a small public runtime configuration for the API origin
and feature flag. Requests use `credentials: include`; API CORS permits the exact
frontend origin with credentials. Never use wildcard origins for private data.
Different subdomains require deliberate cookie/CORS tests. Private API responses
must not enter shared caches.

## DynamoDB and authorization changes

Use stable internal actor/person IDs, with a unique external identity lookup from
provider issuer + subject. Use the profile/activity/follow/notification model in
`editor/README.md`, with per-person drafts and sessions. Enforce expiry in code;
TTL deletion is cleanup, not an authorization decision. Add conditional writes for
revision conflicts and idempotent contribution events. Migrate the store interface
and account resolver rather than translating arbitrary SQLite queries at runtime.

Bots retain their own actor IDs and immutable responsible-person IDs. Issue scoped,
expiring, revocable tokens to authenticated owners; derive the owner server-side.
Effective capabilities are the intersection of the grant and the owner's current
permissions. Suspension disables their sessions and bots. Bot tokens cannot manage
other bots, read a person's inbox/drafts or elevate editorial roles.

Before enabling public writes, test account isolation, CSRF/state replay, expiry,
role revocation, bot ownership and scopes, safe rendering, conflict handling,
rate limits, quotas and audit attribution. Use HTTP API throttles and bounded
Lambda concurrency; alerts and quotas supplement, rather than replace, authorization.

## Current registration and next setup steps

The user registered a production Public API application using their own ORCID
account. Its public client ID is `APP-3ZETXC93IST3V94T`. The client secret has not
been shared with the agent or stored in this repository.

Proposed exact redirect URI: `https://api.nla-lib.org/auth/callback`.
This endpoint still needs its AWS backend, certificate and DNS configuration.
`/explore/` remains the frontend destination after the callback completes sign-in;
it is not the code-exchange endpoint. Register the complete HTTPS callback URL.
[ORCID redirect URI requirements](https://info.orcid.org/ufaqs/how-do-redirect-uris-work/)

Next confirm access to the AWS account, its chosen region, and the DNS provider for
nla-lib.org. Prepare a reviewable SAM template before creating infrastructure.
Enter the client secret directly into Secrets Manager, never chat or source. The
application requests sign-in permissions, not permission to modify ORCID records.
The Public API registration alone does not mean the backend is deployed or login
is working. A sandbox application remains an optional separate testing setup.
