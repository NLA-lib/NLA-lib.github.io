# Explorer

The Explorer is an ordinary Markdown website backed by a generic Lean extraction.
[Algorithms, method families, implementations, and theory](content/README.md) are
editable pages under `content/`. The generated Library contains every extracted
module, declaration, and named result, with exact Lean signatures and source links.

## Build

From the website repository root:

```sh
python3 -m pip install -r explore/requirements.txt
python3 explore/build.py --data /path/to/explore-data.json \
  --src /path/to/matching/library --bib /path/to/references.bib --out /tmp/explorer-site
```

`--src` accepts a checkout or an archive at the extraction's revision. Source hashes
must cover every extracted module and match before definition bodies are loaded.
Theorems expose their signatures, never source proof bodies. Matching Ops sources
supply CG implementation fragments automatically; `--core-src` explicitly previews
a different working core. A file receives a pinned GitHub link only when its bytes
match the published snapshot or a published checkout revision.

Use `--content` for a different Markdown directory, `--renames` for declaration
rename maps, and `--module-map` for explicit mathematical module relocations.
Relocation landing pages do not restore retired execution APIs. Rendering existing metadata again only needs:

```sh
python3 explore/content_pages.py --site /path/to/built/explorer
```

For result placement and review, see [choosing where a guarantee belongs](content/README.md#choosing-where-a-guarantee-belongs).

## Metadata contract

The input is schema 1: `commit`, `date`, `decls`, `modules`, and `sourceHashes`.
Declarations preserve `name`, `module`, `kind`, `signature`, `statement`, `doc`,
`line`, `endLine`, `typeDeps`, `valueDeps`, and `sorry`. Module records preserve
names, paths, docstrings, and imports. The extraction file hash identifies the
snapshot across the rendered pages, records, and browser search.

Unpublished extractions may set `dirty: true` and `base_commit`. A dirty extraction
is always a working-tree preview: the rendered snapshot clears `commit` and `date`,
keeps the parent revision only as `base_commit`, and does not create source links
to new paths under that parent revision. Prefer emitting `commit: null` directly
for such artifacts. Source fingerprints still verify the actual local file bytes.

`Result:` tags group named mathematical results. `Algorithm:` tags and statement
dependencies supply discovery associations only. Families, tasks, implementations,
and theory relationships are authored in Markdown. `results.toml` contains optional
mathematical result titles, aliases, primary declarations, and merge aliases;
`synonyms.toml` adds keyword search aliases. Page headers can name `source_guides`
under `docs/algorithms/`: available guides receive a separate Library page and API
record, their actual file fingerprint, and a source Markdown download. Their bodies
are not merged into mathematical method pages. Unpublished Lean links resolve to
current module references; no base-revision source links are invented. Neither file describes an execution
certificate. Result prefixes and source module selectors live in page headers.

There is no program emitter, old program/target registry, inferred resource ladder,
Rates table, or old single-page app in the build. The website does not need NumPy
emission or any old execution namespace to exist. The optional independent
[lemma-retrieval tools](search/README.md) are not code emitters or part of the
website build; their lexical/documentation modes use the standard library.

## API and compatibility

`api/v1/index.json` lists declaration, result, algorithm, task, module, and curated guide records.
Every record has an immutable identity, snapshot provenance, and a canonical URL.
Declaration records distinguish statement dependencies from proof/value dependencies,
retain exact signature fingerprints and admission flags, and link to pinned sources.
Tags and dependencies never establish execution, success, or resource guarantees.

A docstring may end with a notes block: one or more paragraphs, the first starting
with the literal `Note:` at the start of a line, before the tag lines. The pages show
the part before it as the statement and the notes as a collapsed "Notes" disclosure.
Declaration records keep `docstring` whole and add `docstring_statement` (the
docstring without the notes block), `docstring_notes` (the block, empty when there is
none) and `index_typed_sizes` (the signature mentions `Fintype.card` or `[Nonempty …]`).
`summary` is the first paragraph of the statement. The search text still contains the
notes, so the Lean names they mention remain searchable. Result records add
`primary_explicit`: whether `primary` was chosen in `results.toml` or is the fallback,
the first theorem by name. Result pages show the primary first, marked "Headline"
("provisional" for a fallback among several declarations), then the other forms.

`search-index.json` and its gzip copy use those same records plus the Markdown
pages. `manifest.json` reports snapshot identity and counts; `schema.json` describes
the envelope. The retired implementation/target/bound/guarantee API collections are
not generated. Formal implementation evidence is displayed through authored,
source-backed statements and Ops-specific adapters.

Old declaration/result/module URLs, result aliases, `#d/` and related hash links,
and library rename maps resolve to the current Library. The old catalogue and Rates
URLs redirect to module and result indexes. Removed source/dependency-graph views
are not recreated. A rename never transfers an old statement silently: the generic
record retains the maps reporting a changed statement.

## Headline audit

```sh
python3 explore/audit_primaries.py --site /path/to/built/explorer [--report FILE] [--strict]
```

This lists every result with several declarations and no explicit `primary`, with its
members, and every result whose primary carries a size as an index type. Choosing a
primary is a mathematical decision recorded in `results.toml`; the audit never chooses.

## Validate

```sh
cd explore
python3 -m unittest discover -s tests
```

The tests cover extraction provenance, fail-closed source hashes, exact signatures,
proof separation, operator-name URLs, aliases and renames, removal of old execution
records, Markdown relationships, statement links, and documentation/search tools.
Browser scripts under `tests/check_*_browser.py` accept a separately served preview
and a Chromium path. See [architecture](docs/design/explorer-architecture.md) and
[the legacy retirement notes](docs/design/legacy-retirement.md).
