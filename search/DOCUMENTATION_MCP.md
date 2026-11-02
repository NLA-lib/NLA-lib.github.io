# Mathematical documentation MCP

This server gives an LLM agent bounded access to the library's mathematical interface. The agent
can browse topics, read original docstrings and complete Lean signatures, inspect definitions and
callers, and keep a persistent reading session. Default readings omit theorem proofs. It
complements Lean LSP MCP's goal, hover, navigation and proof-checking tools.

The host agent supplies the reasoning: for example, recognizing that “generalized inverse twice”
belongs in the pseudoinverse API, or that two existing lemmas can be composed. This server does
not call an LLM, require an API key, load embeddings, or start Lean. It supplies source material
and navigation, not generated mathematical assertions.

## Install and connect

From the explorer checkout:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r search/requirements-docs.txt
.venv/bin/python -m search.docs_server \
  --data data/explore-data.json --src data/src --print-client-config
```

The last command prints a standard `mcpServers` JSON configuration with absolute paths, suitable
for merging into a compatible MCP client's existing configuration. Keep your existing Lean MCP
entry. It does not install or modify global client settings. Clients with a different config
schema can use the printed `command` and `args`. Restart/reconnect the client after configuring it.

The data is the existing schema-1 explorer extraction. `--src` is optional for prose, signatures,
and navigation. To inspect definition bodies, supply a source archive or checkout matching the
extraction: each requested source file's SHA-256 must match `sourceHashes` before any source slice
is returned. A matching archive is already available locally in this prototype's `data/src`.

Agents with a shell can use the same reader immediately, without configuring an MCP client or
installing the SDK (Python 3.11+):

```sh
python3 -m search.docs --data data/explore-data.json --tool read_module \
  --args '{"module":"NLAlib.Matrix.Pseudoinverse.Pinv","view":"prose"}'
```

The CLI also accepts `catalog`, `read_declaration`, `search`, `related`, `context` and `session`,
with the same arguments and paged JSON responses as their MCP counterparts.

Without `--print-client-config`, this command runs the MCP server over **stdio**. Standard output
is reserved for protocol messages. It does not bind a port, expose a public HTTP endpoint, or
change any Lean/library files. The only write operation saves reading sessions under
`.docs-state/sessions.sqlite3`, configurable with `--state-dir`.

## Tools

| Tool | Purpose |
|---|---|
| `docs_info` | Snapshot, coverage, and reading instructions |
| `docs_catalog` | One level of topic/module discovery, starting at `NLAlib.Matrix` |
| `docs_read_module` | Original overview, prose-only documentation, or docstrings and signatures |
| `docs_read_declaration` | Exact declaration API, prose-only view, or hash-verified definition body |
| `docs_search` | Candidate discovery by names, prose, statements and existing vocabulary aliases |
| `docs_related` | Direct statement dependencies, proof/value dependencies, or callers |
| `docs_context` | A selected bundle of 1–20 declarations' docstrings and complete signatures |
| `docs_session` | Create, update, list or resume a persistent, snapshot-pinned reading session |

Discovery/search initially cover 2,394 proved Matrix and matrix-related ForMathlib declarations
in 158 modules. Exact reads, explicit module reads, and related declarations may cross into the
other public library topics present in the extraction, so downstream usage remains available.
Declarations flagged as admitted are excluded. This is not a Mathlib-wide documentation index.
Use module `view="prose"` to read just the human documentation and declaration names;
`view="api"` adds all extracted signatures. Module/bundle pages share provenance instead of
repeating long source/resource links for every declaration.

All tools return **one text JSON page**, without duplicating it as structured content. The
`content` field is readable Markdown/Lean. `max_chars` bounds the entire decoded text page,
including provenance and continuation metadata: default 8,000, permitted 1,500–20,000. This is a
character budget, not an exact token estimate. MCP transport framing is additional.

Every page includes the library commit, extraction SHA-256, character range, total content size,
`complete`, and `next_cursor`. Pagination can split a signature; finish its continuation or read
that declaration separately before drawing conclusions about its hypotheses. Continue with the
same tool and arguments plus the returned cursor. Cursors reject another document, extraction,
or updated session revision. Pages never silently drop the remaining declarations.

Resources provide additional entry points:

- `nlalib-docs://catalog`
- `nlalib-docs://<extraction-sha256>/module/<module>`
- `nlalib-docs://<extraction-sha256>/declaration/<name>`

Names in resource links are URL-encoded. The `find_existing_lemma` MCP prompt supplies a browsing
and validation workflow; it does not run a hidden model.

## Example agent workflow

For “does applying the generalized inverse twice recover the matrix?”:

1. `docs_catalog(prefix="NLAlib.Matrix")` → locate Pseudoinverse.
2. `docs_catalog(prefix="NLAlib.Matrix.Pseudoinverse")` → locate the pseudoinverse definition/API.
3. `docs_read_module(module="NLAlib.Matrix.Pseudoinverse.Pinv")` → scan the main results.
   Use `view="prose"` or `view="api"` if the overview does not identify a suitable declaration.
4. `docs_read_declaration(name="NLAlib.pinv_pinv")` → confirm the exact statement and assumptions.
5. For a concrete proof goal, use the existing Lean MCP to check its application.
6. Save the question and selected names with `docs_session(action="create", ...)`.

Prefer concept-based browsing when keyword search misses. Reading an API is useful even when no
single theorem matches the final goal: inspect bridges and compose simpler results.

## Context recovery

`docs_session(action="create", goal=..., bookmarks=[...], notes=..., open_questions=[...])`
returns a session id. After a context reset or process restart, use `action="list"` to recover
ids for this extraction, then `action="get"` with that id. Reopen only selected bookmarked APIs
with `docs_context`. Notes are explicitly agent-authored and unverified; saving a statement does
not certify it. The reader does not infer verification from dependency edges or prior prose.

`action="update"` replaces supplied fields and preserves omitted ones. Sessions refuse a
different extraction, even when its commit label is identical. Restore the matching extraction
to reopen one; snapshot migration is deliberately not automatic. Session data is local SQLite,
not a multi-user access-controlled service.

## Verification and limits

```sh
python3 -m unittest discover -s tests -p 'test_docs.py'
.venv/bin/python -m unittest discover -s tests -p 'test_docs*.py'
```

Tests cover exact-budget continuation, proof-body omission, source hash failures, cross-snapshot
cursor rejection, cross-topic callers, resource links, real MCP stdio discovery/calls, and session
recovery after a server restart. These establish tool behavior, not LLM search quality.

The documentation is the library's original prose: it can contain mistakes such as the ones found
in the mathematical audit. Signatures remain authoritative about formal assumptions. Reading
documentation, inspecting source, and checking a Lean proof are separate evidence levels. The
server does not attempt theorem unification, prove applicability, or guarantee that the best
available lemma has been found. Evaluate actual agent tasks separately before making reuse a gate.

Run the deterministic browsing/restart walkthrough against real data:

```sh
.venv/bin/python -m search.docs_demo --data data/explore-data.json --src data/src
```

It traverses the pseudoinverse API, reads `pinv_pinv`, saves a candidate reading session, restarts
the server, and reopens selected context. It is a protocol/workflow smoke test, not evidence of
LLM retrieval quality. [Documentation size measurements](documentation_sizes.json) compare source,
prose-only and proof-free API characters in three modules; these are not tokenizer measurements.
