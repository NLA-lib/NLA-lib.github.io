# nla-lib.org

The website for NLA-lib, served as static files from GitHub Pages.

## Writing

Pages are written in markdown. Each page is a folder holding an `index.md`
with a YAML header (`title`, `author`, `date`, `tldr`, ...) followed by the
text. Footnotes (`[^1]`) become sidenotes; a line holding only `-.-` becomes a
section divider. The landing page lists posts from a `::: posts` block
naming their folders.

## Building

The HTML is generated and committed, so GitHub Pages serves the repository
as is. After editing a markdown file, rebuild its page (pandoc is required):

    python3 md2html.py index.md hello-world/index.md

Pass every `.md` file whose page should be regenerated.

## Layout

- `css/landing.css`: the stylesheet (Source Sans 3, served from `font/`)
- `css/print.css`: print styles, loaded for print only
- `md2html.py`: markdown to HTML converter
- `.github/workflows/static.yml`: deploys the repository to GitHub Pages on
  every push to `main`
