# nla-lib.org

The NLA-lib website, deployed to GitHub Pages by `.github/workflows/deploy.yml`.

- **Homepage** (`index.md`) and **Design page** (`design/index.md`, how NLA-lib defines things):
  Markdown converted by `python3 md2html.py index.md design/index.md` (needs pandoc). Commit the
  `.md` and the `.html`. A page's menu is the `menu:` list in its front matter; a page with
  mathematics loads KaTeX.
- **Explorer** (`explore/`, served at nla-lib.org/explore/): the static viewer of the NLAlib
  library, built from NLAlib's extracted data at every deploy. See `explore/README.md`. It was
  the repository `NLA-lib/explore` until 2026-11-06; its history is kept here.
- **Shared** by both halves, one copy each: `css/site.css` (fonts, links, the reading column, the
  title and the menu, so the header does not move between pages), `font/` and `vendor/katex/`.
  The explorer's build copies them into its output.

Every menu must list the same pages; `explore/tests/test_menu.py` checks it. Run the explorer's
tests with `cd explore && python3 -m unittest discover -s tests`.

## Explorer preview

The Explorer opens with a regular list of narrow subject tags. Each category contains its algorithms, bounds and
mathematical building blocks; implementation details expand on demand. Structured records remain
available without adding agent-specific navigation. See
[the Explorer design](explore/docs/design/explore-pages.md).

Build the Explorer into `_site/explore` using `explore/build.py` and matching published data,
then add the homepage and shared assets as in the deployment workflow. Run `python3 preview.py`
from this repository root to serve the combined site at `http://127.0.0.1:8000/explore/`.
