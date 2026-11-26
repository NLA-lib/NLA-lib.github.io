# Install collaborative editing

This updates the existing `nla-lib-auth` stack in Oregon. It reuses the current
ORCID secret, hostname, certificate and DynamoDB table. It adds no servers, queues,
new databases or new hosting service. Published content stays in the public Git
repository; discussions, drafts and account data stay in DynamoDB.

## 1. Update the existing AWS service

Download `nla-lib-collaboration-setup.zip`, upload it using **Actions → Upload
file** in AWS CloudShell, and run:

```sh
unzip -o nla-lib-collaboration-setup.zip -d nla-lib-collaboration-setup
cd nla-lib-collaboration-setup
bash deploy.sh
```

The script checks the account and existing resources, uploads the hashed Lambda
package to the existing private artifact bucket, then updates CloudFormation.
The table and all existing sign-ins/profiles are preserved. No secret value is
printed. Keep the old setup directory as a deployment rollback artifact.

After deployment, `https://api.nla-lib.org/health` should list `editing`,
`discussions` and `reactions`. Reload the Explorer. Sign in with ORCID to save
private drafts, propose edits, comment and react. Anonymous visitors can read the
published mathematics, discussions and counts. Full Markdown editing includes
Theory pages. Statements shared across pages retain their committed UUIDs.

## 2. Give your authenticated account editorial access

While still in that directory:

```sh
bash bootstrap-admin.sh
```

Enter **your ORCID iD from your NLA-lib profile**, not the ORCID application client
ID. You must have signed in first. This command runs under your existing AWS
administrator access and cannot create an account from an unverified typed iD.
It grants your account the admin role and writes an audit record. Ordinary ORCID
sign-in always creates contributors, never trusted editors.

Reload the Explorer. **My contributions** and **Review contributions** appear in
the footer. Reviewers can inspect previews and source diffs, approve, reject or
request changes. Approved edits remain safely stored even before GitHub is linked.
Do not run `recover.sh` on the healthy stack.

## 3. Connect a restricted GitHub App for publication

A deploy key used by a developer is separate from the website's publishing App.
Create an organization-owned GitHub App in **NLA-lib → Settings → Developer
settings → GitHub Apps → New GitHub App**:

- Name: a unique name such as **NLA-lib Explorer Editor**.
- Homepage: `https://nla-lib.org/explore/`.
- Disable webhooks; this first version checks publication status when an editor
  chooses **Check and publish**.
- Repository permissions: **Contents: Read and write**, **Pull requests: Read and
  write**, **Checks: Read-only**, **Commit statuses: Read-only**. Metadata read is
  automatic. No Actions-write, administration, organization or account permissions.
- Install it only on `NLA-lib/NLA-lib.github.io`.
- Generate its private key. Keep that file out of Git and chat.

Keep branch protections on `main`, require the `test` and **Published content
build** checks, and do not add the App to any protection-bypass list. Enable squash
merging in repository settings. If the repository requires GitHub review approvals,
an eligible GitHub reviewer must also supply them; the App cannot override them.

In AWS Secrets Manager, in **us-west-2**, create **Other type of secret**, named
`nla-lib/production/github-app`, with a JSON value containing:

```json
{
  "app_id": "numeric App ID from the App's settings",
  "installation_id": "numeric ID at the end of its installation settings URL",
  "private_key": "the complete PEM private key, with newlines escaped as \\n in JSON"
}
```

Use the Secrets Manager JSON editor to preserve the PEM newlines. Do not use the
GitHub OAuth Client ID here. Share only its **ARN**, never the JSON/private key.
Then in CloudShell, set the ARN and rerun deployment:

```sh
export NLA_GITHUB_APP_SECRET_ARN='paste-the-secret-ARN-here'
bash deploy.sh
```

The optional ARN parameter adds permission to read only that one secret. Omitting
it on future updates preserves the existing stack parameter. The backend generates
short-lived installation tokens and does not retain them in DynamoDB.

## Publication

1. A contributor saves drafts privately and submits a change with an explanation.
2. An editor reviews the preview and source diff and approves it.
3. **Start publication** creates one contribution branch and pull request.
4. The repository runs unit tests, notation checks and a full content build.
5. **Check and publish** performs a guarded squash merge after successful checks.
6. The existing Pages workflow rebuilds the site. A failed deployment does not
   remove Git history or DynamoDB revisions.

The App only writes `explore/content/**/*.md` and individual bibliography `.bib` entries. It refuses stale source blobs,
never force-pushes, and cannot edit workflows or Lean source through this API.
Each accepted contribution becomes one commit on main. Commit messages preserve
ORCID, revision ID, reviewer and contributor/coauthor attribution. Researchers do
not need email addresses or GitHub accounts. GitHub may display the App as the
squash-commit author; explicit researcher attribution is preserved in its message.

Statement changes mark mathematical review and formalization links for
reassessment. They do not change Lean proofs or assert that a revised informal
statement was proved. New results, conjectures and definitions can link versioned
external proofs. Shared bibliography keys remain source-controlled in this release.

## API and storage

The API is `https://api.nla-lib.org/editor-api/`. `GET schema` documents the
structured proposal format. Browser writes use the existing HttpOnly cookie and
CSRF token; bot writes use a scoped Bearer token. No endpoint accepts an arbitrary
repository path, arbitrary actor, trusted role or formal proof status.

Drafts and proposals use optimistic version checks. Reusing an idempotency key
with the same proposal returns the original submission; different content returns
409. Proposed revision text is private to its responsible person and editors;
published revisions and Git source are public. Revision URLs use the entry ID and
revision token. Restoring a revision creates a new proposal, preserving history.

Discussions support threaded comments, suggestions, errors, formalization requests
and references. Reactions are idempotent per actor and emoji. Public activity
counts use batched reads. Moderators/admins can inspect reports and remove comments;
original text and attribution remain in a private audit record. Suspension of an
account disables its sessions and all owned bot tokens on their next request.
Account suspension/role changes other than initial admin setup are currently AWS
administrator operations, not public profile fields.

Bots have a distinct profile, immutable responsible-person attribution, selected
scopes, 90-day expiry and revocation. The token is returned only once and only a
hash is stored. Bots cannot inspect private drafts, notification inboxes or review
tools and cannot approve or publish. Their public contributions identify the bot
and the responsible researcher.

In-app notifications show recent activity on followed entries. Joining a discussion
or proposing an edit follows the entry automatically. This first release supports
50 follows per person, up to ten recent events per followed entry and 100 inbox
items; it is a bounded recent-activity inbox, not a permanent delivery archive.
It does not send email. Larger delivery workloads can use a queue later.

Hourly contribution/preview quotas and a global daily write quota complement the
existing API throttles. API GET traffic still has AWS costs; keep an AWS Budget
alert on the account. This release increases the existing Lambda's memory to 512 MB
and adds table query/batch-read permissions, without granting table or resource
administration. No fixed-cost always-on service is introduced.

## Verification and rollback

The release is tested with the real API handler and simulated AWS, GitHub and ORCID
adapters, and browser tests intercept all external requests. The live GitHub App
installation and actual AWS update must still be verified after configuration.

Restore the previous `auth.zip`, its hash file and template from the original setup
folder and run its deployment script to roll back application code. The DynamoDB
table is retained and auth records remain compatible. Published mathematical edits
are reverted through new reviewed commits; do not rewrite the repository history.

## Statement creation and proof requirements

Use **Add statement** in the Explorer header to create a standalone result,
conjecture or definition. A Lean link is optional. A result claiming to be proved
must have a complete linked Lean proof or at least one HTTPS link explicitly
entered under Proof references for a natural-language proof hosted elsewhere.
Bibliographic citations alone do not satisfy that requirement. Definitions and
conjectures are exempt. The API checks submissions, approval of older pending
contributions, and publication; bot credentials follow the same policy. Draft
validation does not require a proof link. Typed statements belong in shared files
rather than inline page blocks.

The Lean statement appears directly below the readable formulation in a collapsed
code section. Unlinked results, conjectures and definitions display **No linked
Lean statement** there. Admissions and changes requiring reassessment are explained
in the Lean section or editorial notice, without verification badges on cards.
A proof URL indicates a supplied source; editorial review must assess its argument.

The editor keeps its live preview visible while editing and viewing changes.
Sign-in links carry the current Explorer path, query and fragment. The backend
binds that destination to the browser's single-use OAuth state and accepts only
local Explorer destinations, including the canonical homepage `/`. For an existing deployment, the generated
`update-nla-editor.py` helper updates the affected Lambda modules, preserves the
original package and redeploys the existing stack without changing stored data.

## Frontend-owned bibliography

`explore/content/references/*.bib` is the website's canonical shared bibliography.
The initial entries were copied from the Lean repository; its bibliography remains
independent for Lean docstrings. Website builds use the frontend entries when that
directory exists. They do not overwrite these entries from Lean.

The References page provides a complete BibTeX download, per-entry copy dialogs,
formatted citations, and Add reference / Edit / History actions. BibTeX edits keep
existing citation keys fixed and use the same private drafts, source diffs, review
and checked publication workflow. New entries get stable IDs from their keys.
The API accepts only one entry per reference and validates citation links.
Publishing is restricted to individual `.bib` files under the references directory
in addition to the existing mathematical Markdown paths. No permission to write
Lean source or workflows is introduced.

New public references become available to the shared statement-reference picker
after publication. The raw entries retain extra BibTeX fields; formatting separates
authors, titles, publication information and identifiers. Peer-review attestations
for mathematical or external proofs remain deferred. Supplied external proof URLs
are labelled as sources, without an assertion that their contents were reviewed.

## Comment reactions

`GET` and `POST /editor-api/objects/{entry_id}/comments/{encoded_comment_id}/reaction`
read and toggle reactions on one comment. Encode the complete comment ID as a URL
path segment. A write supplies `{ "emoji": "👍", "active": true }`; reactions are
idempotent per actor and use the same session, bot scope and rate-limit checks as
entry reactions. Discussion responses include each comment's reaction counts and
the requesting actor's selection. These records remain separate from entry reactions.
Hidden comments cannot receive reactions. The frontend enables these controls only
when bootstrap advertises `comment-reactions`. No new AWS resources are required.
