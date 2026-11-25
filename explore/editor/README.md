# Local collaborative editor

This is an opt-in prototype over the existing Explorer. It edits a local SQLite
workspace, not the Markdown checkout, Lean repository, Git branches, or live site.
The normal static build does not load the editor or depend on this server.
No new Python or JavaScript runtime dependency is required.

## Start

First build the Explorer using the usual instructions in `../README.md`, with an
extraction compatible with this checkout. Then, from the website repository root:

```sh
python3 explore/editor_server.py --site /absolute/path/to/built/explorer
```

Open the printed `http://127.0.0.1:8082/explore/` URL on the computer running the
server. Both the printed origin and `http://localhost:8082` are accepted (use the selected port). The server binds only to
loopback and does not expose a remote or public service. `--port` changes the port.
For a build at `_site/explore`, pass `--site _site/explore`, not `_site`.

The default database is `~/.local/share/nlalib-editor/prototype.sqlite3`.
Override it with `--database /path/outside/the/built/site/workspace.sqlite3`.
Back up the database to preserve local work. Separate databases provide separate
workspaces; no AWS setup is involved.

## Browser workflow

The main Explorer is an overview. The disclosure beside a theorem title expands its readable statement. The title itself opens a stable `/explore/statements/{uid}/`
page holding the full statement, Lean details, shared references, reactions, discussion,
and editing/history controls in the **⋯** page menu. Emoji reactions stay available on collapsed overview entries. Inline revisions in overview lists are deferred.
The static build emits these theorem pages as well, so mathematics remains readable
without the collaboration server.


- **Edit page** in the **⋯** menu opens one textarea with the full Markdown source, including
  YAML metadata and readable statement imports. This includes Theory pages. There
  is no per-paragraph or per-statement layout inside the page editor.
- **Edit statement** in the theorem page’s **⋯** menu opens its mathematical text and references. The
  Library remains populated from the Lean extraction; its pages expose discussion
  and reactions without an edit control.
- **Add new result** creates a result, conjecture, or definition with optional
  external proof references. Each reference includes an HTTPS URL and a version /
  location. This does not assert a checked proof or completed expert review.
- **Preview** uses the existing Python renderer and KaTeX, with debounced live
  updates while editing beside the preview. **Changes** shows a
  line-oriented diff. An explanation is required to save a local revision.
- **Save draft** persists unfinished text without adding a revision. **Save local
  revision** creates an immutable local revision. Neither creates a Git commit.
- **History** lists the source baseline and local revisions, with revision URLs.
  Restoring opens the old content against the current head; save it as a new
  revision. Page history pins the statement versions used at the time of saving.
  Current pages intentionally show the latest local statement revisions.
- A **discussion icon and count** summarize activity beside overview entries.
  The theorem page contains the discussion directly, with inline replies and a Markdown/LaTeX preview.
  Discussions support suggestions, potential errors,
  reference requests, formalization requests, and generalizations. Feedback records
  the object and revision it concerns. Emoji reactions appear directly on pages and statements as compact count chips.
  Use the smile/plus picker to add an emoji, or click a selected chip to remove it.
  Multiple emoji are allowed. Counts currently reflect the local prototype user.
- **Research feedback** in the footer collects feedback across pages and statements. Export
  loaded feedback as JSON for periodic research / Lean developer review. Load older
  feedback before exporting if the queue spans more than one page.

All activity is attributed to **Local researcher**, a clearly labelled prototype
identity. Reloading preserves drafts, revisions, feedback, and reactions.
The published source and extracted formal evidence remain unchanged. Mathematical
prose edits display a reassessment notice. External proof references are explicitly
unverified. Changing an existing Lean-linked object's kind is rejected.

File-backed imports share their committed UUID across all placements. Theorems are
stored individually under `content/statements/`; see `../content/statements/README.md`.
Inline authored blocks remain distinct editorial formulations; generated occurrences
of the same result share a local object. Inserting an existing statement references
that same object. Editing it updates all local placements. Removing a card does not
delete the statement or its discussion. Unsourced explanatory definitions also work.

## Structured agent API (local v1)

Base URL: `http://127.0.0.1:8082/explore/editor-api/`.
`GET bootstrap` returns an ephemeral session key. Mutations require JSON and
`X-Editor-Session: <key>`. This is a local browser/agent boundary, not production
account authentication. Cross-origin requests, unexpected Host headers, and writes
without a session key are rejected. Do not expose this server publicly.

| Method / route | Purpose |
| --- | --- |
| `GET schema` | Machine-readable proposal JSON Schema |
| `GET objects?type=statement&q=bound&limit=100&cursor=0` | Search titles; `next_cursor` paginates |
| `GET objects/{id}` | Current fields, revision, draft, preview, known placements |
| `GET objects/{id}?revision={revision}` | Immutable revision and pinned preview |
| `GET objects/{id}/history` | Baseline and local revision metadata |
| `POST objects/{id}/preview` | Validate `fields`, return rendered HTML and diff |
| `POST preview` | Preview fields of a new external result |
| `POST objects/{id}/draft` | Save `base_revision`, editable `fields`, and `draft_revision` from a previous draft |
| `POST proposals` | Atomically save 1–20 explicit object changes |
| `GET proposals?cursor=0` | Export/recover saved proposals, including after upstream conflicts |
| `GET/POST objects/{id}/feedback` | Read / add version-associated feedback and replies |
| `GET objects/{id}/feedback?summary=1` | Message count, including replies |
| `POST feedback/preview` | Render safe Markdown/LaTeX from `{ "body": "..." }` |
| `GET references?q=term` | Search the shared bibliography |
| `GET/POST objects/{id}/reaction` | Read reactions or set `{ "emoji": "👍", "active": true }` |
| `GET feedback?cursor=0` | Feedback handoff queue, including source evidence and revision IDs |

Example proposal (get real IDs and revision tokens from `GET objects/{id}`):

```json
{
  "idempotency_key": "unique-key-for-this-exact-request",
  "explanation": "Make the positive-definiteness hypothesis explicit.",
  "changes": [{
    "operation": "update_statement",
    "id": "object-uuid-from-the-api",
    "base_revision": "revision-token-from-the-api",
    "fields": {"body_markdown": "Let $A$ be symmetric positive definite..."}
  }]
}
```

Supported operations are `update_page`, `update_statement`, and
`create_statement`. New statements use a fresh UUID and `base_revision: null`.
The page editor submits `document_markdown` containing the complete source file.
The API also retains structured page fields `title`, `summary`, and `body_markdown`
for agents; do not mix these with `document_markdown` in one change. Statement fields are
`title`, `body_markdown`, `statement_kind`, and `proofs`. Formal evidence and source
paths are not writable. Page bodies reference statements with a standalone line:

```text
{{ statement:<statement-uuid> }}
```

One proposal can create a statement and place it on a page atomically. Changes to
the same object must be combined into one operation. The service renders and
validates all changes before committing the SQLite transaction.

A stale revision returns HTTP 409; the service does not overwrite the current
head. Draft saves also check `draft_revision` (null for a new draft) so two open
editors cannot silently replace each other's draft. Retrying the same proposal
with the same idempotency key returns the same
result. Reusing a key with different content returns 409. Invalid content returns
400; unknown objects/revisions return 404; oversized requests return 413. Request
bodies are limited to 500 KB; individual Markdown bodies to 120 KB (UTF-8).

Feedback POST bodies contain `kind`, `body`, and `parent_id` (null for a root).
The accepted kinds are listed in the browser workflow above; API spellings use
hyphens, e.g. `mathematical-error` and `formalization-request`.

## Verification

From `explore/`:

```sh
python3 -m unittest discover -s tests
node --check editor/editor.js
```

The HTTP integration test needs permission to bind a loopback socket. Browser QA
uses the existing optional Playwright setup; do not add it to runtime requirements:

```sh
python3 tests/check_editor_browser.py --site /path/to/built/explorer \
  --chromium /path/to/chromium
```

## Boundaries before production

This deliberately does not implement ORCID, multi-user authorization, editorial
approval, GitHub publication, Git history import, source-file migration, or automatic
Lean changes. Exported proposals describe the local prototype schema; they are not
already accepted changes in a live service. Revision URLs require the same database.
Page metadata edits use the existing schema and relationship validation. Identity
fields (`kind`, `id`, `algorithm`) remain fixed during ordinary editing.

Shared statement IDs are committed UUIDs and survive source-file renames. Page IDs
and legacy inline-block IDs are still derived from current identities / explicit
anchors. Renaming a page or unanchored inline block can change those IDs. Before
production, commit permanent page IDs and migrate remaining inline statements
where appropriate. Do not silently equate distinct formulations of one theorem.

The source fingerprint is recorded with every revision. If source content changes
under a local object, reopening its old local head fails with a conflict instead of
silently applying it. Saved proposals remain available through `GET proposals` for
reconciliation. Historical source baselines are not archived independently yet;
Git-backed history and retained source snapshots are required for production.

The next phase replaces the local persistence/session adapters with AWS and ORCID,
adds an editorial review queue and an allowlisted GitHub publisher, and exports
accepted content/attribution to the public repository. Research feedback remains
separate from authoritative mathematics. Lean developers can periodically triage
that queue; checked library extraction continues to supply formal evidence.

## Emoji artwork

The picker bundles thirteen SVGs from [Twemoji](https://github.com/twitter/twemoji),
by Twitter, Inc. and other contributors, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The graphics license is included in `emoji/LICENSE-GRAPHICS`. No emoji package or
external runtime request is required.

## Shared bibliography

`api/v1/references.json` is keyed by stable bibliography identities. The build loads
the Lean repository's existing BibTeX bibliography; `content/references.json` can
supply additional keys without overriding the library's records. Statement files
can declare `references: [{key: HornJohnson2013, locator: "Section 5.6"}]` in their
front matter. The statement editor can also select shared keys and add locators.
References are rendered on theorem detail pages and cited Library records; the
complete shared bibliography is at `/explore/references/`.

New bibliography records are currently source-controlled; the local editor links
existing records rather than providing an unreviewed bibliography administration UI.
External proof URLs remain supported separately.

## Discussion component choice

The discussion uses [Primer React](https://primer.style/product/getting-started/react/)
for accessible buttons, textareas, segmented Write/Preview controls, selectors,
avatars and labels. A small custom thread layout keeps the existing Markdown/LaTeX
renderer and feedback API. Shadow DOM isolates the component styles from the legacy
Explorer stylesheet. All assets are served locally; no hosted discussion service or
GitHub login is required. Browser drafts and local SQLite feedback are preserved.

Source lives in `editor/discussion/`. The pinned npm lockfile includes React,
React DOM, Primer React, Primer design tokens, and esbuild. To rebuild:

```sh
cd explore/editor/discussion
npm ci
npm run build
```

The compiled `editor/discussion.js`, `editor/discussion.css`, and linked license
notices are checked in, so the Python preview and static renderer need no Node
installation at runtime. CI rebuilds the module. React and Primer are MIT licensed;
`discussion/THIRD_PARTY_LICENSES.txt` includes full license texts and the bundle's
adjacent `discussion.js.LEGAL.txt` preserves embedded dependency notices.

This provides the UI foundation while retaining the planned ORCID + Lambda/DynamoDB
backend. It does not add authentication or hosted multi-user storage to the local
prototype.

## Profiles, bots, and notifications

`/explore/people/{actor_id}/` is a public profile: biography, affiliation, research
interests, optional HTTPS website and ORCID iD, contributions, reactions, and owned
bots. ORCID text is explicitly unverified until real ORCID authentication is added.
The local session represents one person (`local-researcher`). Their own page also
shows private saved drafts, followed entries, and an inbox. Notifications are stored
in the database, not in Markdown or Git. Email delivery is not implemented.

Every new comment and revision has server-assigned `actor_id` and
`responsible_person_id`. A bot has its own profile and a fixed person owner; clients
cannot choose or impersonate an actor in a proposal. Ownership attribution survives
token revocation. Discussion messages and revision history link to both profiles.
Person activity includes their bots, while bot pages show only that bot's activity.
Existing local comments and revisions are attributed to the original local person.

**Manage bots** issues a token once, stores only its SHA-256 hash, and allows
revocation. Scopes are `proposals`, `feedback`, and `reactions`; each is optional and
at least one must be selected. Use `Authorization: Bearer <token>` in API requests.
Never put a token in a URL, public source, or browser storage. Tokens cannot access
private drafts, notifications, workspace state, session bootstrap, or bot management.
They do not grant editorial trust or publication permissions. All local proposals
still save only to the prototype database.

Joining a discussion or saving a revision follows the entry automatically. Follow /
Unfollow is also available in its page menu. Later comments and revisions notify
followers, excluding the acting person and their own bots. The inbox supports
unread state and pagination. It is an in-app inbox, with no polling or email service.

Additional API routes (browser session required for person management):

| Method | Route under `/explore/editor-api/` | Purpose |
| --- | --- | --- |
| GET | `profiles/{actor_id}?cursor=0` | Public profile, bots, contributions, reactions |
| POST | `me/profile` | Update person profile fields |
| GET | `me/workspace` | Private drafts and followed entries |
| GET / POST | `bots` | List owned bots / register bot and issue scoped token |
| POST | `bots/{token_id}/revoke` | Revoke an owned token |
| GET | `notifications?cursor=0` | Private inbox and unread count |
| POST | `notifications/read` | Mark an owned notification read (`id`) |
| GET / POST | `objects/{id}/follow` | Read / set follow state (`active`) |

## Storage path to AWS

Keep published statement and definition Markdown, stable IDs, references, and topic
relationships in Git. The current prototype uses the same local SQLite database for
profiles and interactions, with separate records for actors, immutable attribution,
revocable token hashes, follows, and notification deliveries. Draft text never becomes
public profile activity. Back up the database to preserve local work.

When moving to AWS, use DynamoDB for these records with direct queries by actor,
responsible person, entry, and notification recipient. A reasonable initial table
layout is:

| Partition key | Sort key examples | Data |
| --- | --- | --- |
| `ACTOR#{id}` | `PROFILE`, `ACTIVITY#{time}#{id}`, `BOT#{bot_id}` | Identity, public feed and owned bots |
| `PERSON#{id}` | `DRAFT#{entry_id}`, `FOLLOW#{entry_id}`, `NOTIFY#{time}#{id}` | Private workspace and inbox |
| `ENTRY#{id}` | `COMMENT#{time}#{id}`, `FOLLOWER#{person_id}`, `REACTION#{emoji}#{actor_id}` | Discussion, follower lookup and reactions |
| `TOKEN#{hash}` | `AUTH` | Bot identity, scopes, expiry and revocation state |

Activity feeds and notification deliveries are derived records, written from an
idempotent contribution event; keep the original contribution and its attribution
as the authority. For a small initial audience, bounded transactional writes can
create these records together. Move larger follower fan-out to a queue later, if
needed. Do not scan all users or comments to build a person's page. Private queries
must derive the person ID from the authenticated session, never from a submitted
owner ID. Production needs ORCID sessions, verified account linking, token expiry,
quotas and role checks before this local identity model becomes a multi-user service.
No AWS resources or new costs are introduced by this prototype.

## Theorem and definition pages

The overview heading includes emoji reactions, a comment count and a dedicated
expand/collapse button. Clicking the remaining card opens its stable statement page;
the title is also a normal keyboard-accessible link. Readable statements are boxed,
and Lean signatures use a code block. Rendering preserves authored LaTeX exactly:
letters are bold only when the source explicitly requests it.

Authored definitions already use shared statement files and receive the same stable
detail pages as theorems. Lean statement and Related results are collapsed by default. Definition names
in the Lean signature link to dedicated definition pages, using resolved statement
dependencies from the extraction. Ambiguous or locally shadowed names stay plain.
There is no separate Definitions list. Initial related-result discovery links are based on shared topic-page membership and are
labelled as contextual, not mathematical dependencies. Lean-only definitions link
to their generated declaration pages. Explicit reviewed dependencies can later
extend the statement schema without inferring them from discussion or prose.


## Preview loading behavior

The full search index loads when search is focused or used, rather than after every
navigation. Reactions and comment counts share a batched `GET activity?ids=...`
request (up to 200 entries). Topic relationships are indexed before the local server
accepts requests. This keeps browsing independent of the full search download.
On theorem and definition pages the discussion sits immediately after reactions;
Lean statement and Related results remain collapsed below it. Disclosure controls
use down/up arrows.


Overview reaction counts are read-only; adding or removing reactions happens on the
statement detail page. The whole overview card highlights on hover, rather than the
title text. Expand/collapse arrows have no button box and grow slightly on hover or
keyboard focus; Add reaction also has visible hover/focus feedback. Revision notices
sit below the readable statement box. Discussion waits for its styles, initial
messages and fonts before revealing the complete component, avoiding unstyled frames.

## Hosted collaboration

The same interface now has a hosted adapter for the ORCID/Lambda/DynamoDB service.
See [installation and review workflow](../backend/COLLABORATION.md). Hosted buttons
submit proposals and private drafts instead of changing this local SQLite workspace.
A static build remains readable if the service is unavailable; it does not expose
this loopback server publicly. The local prototype boundaries above still apply
to `editor_server.py`.
