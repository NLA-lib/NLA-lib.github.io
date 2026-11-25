# First hosted authentication slice

This package creates ORCID sign-in, secure application sessions, public researcher
profiles and private profile editing. Comments, content editing, notifications and
bots remain in the local prototype; this first service grants no GitHub or Lean
access. The existing static site stays on GitHub Pages.

Deployment is not yet performed. The CloudFormation template uses SAM for the
Lambda package and native HTTP API resources. It references the existing Secrets
Manager ARN and ACM certificate ARN in account 432197736886, region us-west-2.
No secret value belongs in the bundle. Lambda reads it from Secrets Manager.

## Deploy from AWS CloudShell

Download the prepared setup archive, open AWS CloudShell in the AWS console, choose
Actions → Upload file, and upload the archive. Then run:

```sh
unzip nla-lib-auth-setup.zip -d nla-lib-auth-setup
cd nla-lib-auth-setup
bash deploy.sh
```

The script verifies the AWS account, checks certificate issuance and references the
existing secret. It creates a private deployment-artifact S3 bucket and deploys the
stack `nla-lib-auth`: one Lambda, its limited execution role and 14-day log group,
one DynamoDB table, an HTTP API, and the API custom-domain mapping. API Gateway
throttles requests; Lambda uses the account’s unreserved concurrency pool; no reservation is requested. The application permits at
most 20 login starts per IP/hour and 1,000 per day in total. These limits bound
activity; they are not a billing guarantee or a substitute for account budget alerts.

IAM acknowledgement permits the stack to create the Lambda execution role. That
role can only read the specified ORCID secret, read/write this stack's table and
write its log streams. It cannot publish content, manage other AWS resources,
change roles, modify DNS, or retrieve other secrets. The deployment command itself
runs under the user's existing CloudShell permissions.

If CloudFormation fails, inspect Events on the `nla-lib-auth` stack and share the
failed resource and reason, not credentials. The template does not reserve Lambda concurrency, so it can deploy in accounts
with a low concurrency quota. Do not keep retrying a rolled-back stack
without resolving its failed resource.

## DNS and sign-in verification

After deployment, the `ApiDnsName` output is the Squarespace `api` CNAME target.
Keep the previously added ACM validation CNAME. After DNS resolves:

1. Open `https://api.nla-lib.org/health` and confirm `ok: true`.
2. Open `https://api.nla-lib.org/account` and choose Sign in with ORCID.
3. Sign in using the production ORCID account. The callback returns to
   `https://nla-lib.org/explore/?auth=complete`.
4. Reopen `/account`; verify the authenticated ORCID iD and profile editing.
5. Sign out and verify that `/me` returns 401.

The user confirmed real ORCID sign-in on the account page, and the deployed
preflight fix was verified with HTTP 204. Explorer account controls are enabled
in `web/collaboration-config.json`; publishing the focused frontend change through
GitHub Pages exposes those controls. The local preview has a separate session adapter.

## Security and data

Authlib handles the confidential OAuth authorization-code exchange against the fixed
production ORCID endpoint with `/authenticate` only. Browser-bound random state is
hashed in DynamoDB, expires in 10 minutes and is atomically consumed. The provider's
authenticated ORCID identifier is checksum validated. Provider access/refresh tokens
are discarded; no ORCID record-writing permission is requested.

Opaque, host-only `__Host-` session cookies are Secure, HttpOnly and SameSite=Lax.
Session tokens are stored only as hashes and expire after 12 hours. The app checks
expiry and current account status on every private request; DynamoDB TTL is only
cleanup. Profile writes require the allowed Origin, a session-bound CSRF token,
JSON content type and a strict field allowlist. Public profiles omit private session
and account fields. The default role is contributor; users cannot change role,
status or authenticated ORCID. Session IDs and provider callbacks are never logged.
HTTP API access logging is intentionally not enabled because raw callback query
strings contain authorization codes. Structured app errors include request ID and
error category only. Sign-in and profile changes have separate DynamoDB audit rows.

DynamoDB deletion and replacement retain the table and point-in-time recovery is
enabled. Deleting the stack does not delete that retained data or the separate S3
artifact bucket. Existing AWS secret, certificate and website records are external
resources and remain under the user's management.

## Build and checks

`requirements.in` records the new direct dependencies: Authlib for OAuth, requests
for its transport, and boto3 bundled to avoid SDK/urllib3 version mismatch with the
Lambda runtime. `requirements.lock` pins all deployment wheels with hashes. These
are isolated from the existing static renderer and local prototype.

The release script builds CPython 3.12 x86_64 Linux wheels, includes dependency
license metadata, and packages only this backend. Tests mock the provider and data
store; they do not replace a real AWS deployment and ORCID end-to-end test.


## Recovery from the first failed deployment

The initial attempt failed because a reservation of five Lambda executions would
leave fewer than the account's required ten unreserved executions. The corrected
template omits the reservation, preserving API throttles and application quotas.

The small `nla-lib-auth-recovery.zip` contains updated scripts and template only;
it uses the already uploaded `auth.zip`. Extract it over the existing setup folder
and run `recover.sh`. It checks the exact failed stack ID and retained table,
records the table name locally, deletes only that rolled-back stack, and deploys
with `ExistingDataTableName` set. It never deletes the table. A new managed table is
not created in this recovery. The existing table is referenced as an external
resource; keep `.existing-data-table` with future deployments. Without that marker,
updates that omit the parameter retain the stack's previous parameter value.
