# nla-lib.org

The NLA-lib website, deployed to GitHub Pages by `.github/workflows/deploy.yml`.

- **About page** (`about/index.md`) and **Design page** (`design/index.md`, how NLA-lib defines things):
  Markdown converted by `python3 md2html.py about/index.md design/index.md` (needs pandoc). Commit the
  `.md` and the `.html`. A page's menu is the `menu:` list in its front matter; a page with
  mathematics loads KaTeX. A citation `[@Key]` becomes a sidenote with the reference of that
  key in NLAlib's `docs/references.bib`, found in a checkout at `../nlalib` or given with `--bib`.
- **Explorer homepage** (`explore/`, served at nla-lib.org/): the static viewer of the NLAlib
  library, built from NLAlib's extracted data at every deploy. See `explore/README.md`. It was
  the repository `NLA-lib/explore` until 2026-11-06; its history is kept here.
- **Shared** by both halves, one copy each: `css/site.css` (fonts, links, the reading column, the
  title and the menu, so the header does not move between pages), `font/` and `vendor/katex/`.
  The explorer's build copies them into its output.

After copying the root assets and built Explorer into `_site/explore`, run
`python3 explore/assemble_site.py --site _site` to publish the Explorer homepage at
`/` and a query/fragment-preserving redirect from `/explore/`. Existing nested
Explorer page and API URLs stay accessible. The former homepage is at `/about/`.

Every menu must list the same pages; `explore/tests/test_menu.py` checks it. Run the explorer's
tests with `cd explore && python3 -m unittest discover -s tests`.

## Explorer preview

The Explorer is authored in [Markdown files](explore/content/README.md), with YAML
metadata and generated sections. It opens with Algorithms, Theory, and the full
Library reference. Tasks and method families are discovery pages; mathematical algorithms, implementations,
and theory topics have canonical identities. See [the architecture](explore/docs/design/explorer-architecture.md).

Install the page-rendering dependencies with
`python3 -m pip install -r explore/requirements.txt`. The regular build turns the generic extraction into library records and Markdown pages,
without the retired program/target pipeline. Matching published core sources
automatically fill the CG implementation pages. Use `--core-src <NLAlib>` to preview
a newer working core; unfinished pages elsewhere remain placeholders.

Build the Explorer into `_site/explore` using `explore/build.py` and matching published data,
then add the homepage and shared assets as in the deployment workflow. Run `python3 preview.py`
from this repository root (with `--port 8081` for the current demo).

## Local collaborative editor prototype

The opt-in [editor prototype](explore/editor/README.md) adds page and individual
statement editing, mathematical preview, diffs, local drafts and revision history,
discussion, reactions, and a research feedback queue. Start it with
`python3 explore/editor_server.py --site /path/to/built/explorer`. It stores work in
a separate local database and never commits, publishes, or changes Lean sources.

The [notation standard](explore/docs/notation.md) describes source conventions and
validation. The [authentication and hosting plan](explore/docs/authentication-and-hosting.md)
sets out the next AWS/ORCID slice while retaining GitHub Pages.

## Analytics

All content pages load the asynchronous GoatCounter script for
`https://nlalib.goatcounter.com`. The Markdown page generator (`md2html.py`) and
Explorer shell (`explore/web/template.html`) supply it to generated pages. The
standalone lemma-search page also includes it. Keep the committed homepage and
Design HTML in sync with the Markdown generator.

## Collaborative research platform

The Explorer build publishes the shared statement pages, minimalist discussion
interface, source snapshots and editing assets. The optional AWS backend supplies
ORCID identities, private drafts, review, reactions and discussions. Accepted
mathematical content stays in Git; a restricted GitHub App publishes through
checked pull requests. See [setup and publication](explore/backend/COLLABORATION.md).
The loopback-only [local editor](explore/editor/README.md) remains available for
preview without AWS and never publishes its SQLite workspace.

The shared website bibliography is maintained in
[`explore/content/references/`](explore/content/references/README.md). The References
page offers BibTeX downloads and reviewed entry editing. The Lean repository
retains its separate bibliography for its own docstrings.

The [Luna editorial cleanup playbook](explore/docs/luna-editorial-cleanup.md) defines
bounded, reviewed batches for consistent natural-language statements, citations
and definition links. Preparing the guide does not start a cleanup run.
