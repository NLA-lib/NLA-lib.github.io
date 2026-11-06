# nla-lib.org

The NLA-lib website, deployed to GitHub Pages by `.github/workflows/deploy.yml`.

- **Homepage**: `index.md`, converted to `index.html` by `python3 md2html.py index.md`. Commit
  both. Its menu is the `menu:` list in the front matter.
- **Explorer** (`explore/`, served at nla-lib.org/explore/): the static viewer of the NLAlib
  library, built from NLAlib's extracted data at every deploy. See `explore/README.md`. It was
  the repository `NLA-lib/explore` until 2026-11-06; its history is kept here.

The two menus must list the same pages; `explore/tests/test_menu.py` checks it. Run the
explorer's tests with `cd explore && python3 -m unittest discover -s tests`.
