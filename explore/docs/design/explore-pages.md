# Explorer categories and formal evidence

The Explorer is part of `NLA-lib.github.io`, under `/explore/`. It uses the same title-first
header, fonts, site menu and icon as the homepage and Design page. Reports remain removed.

## Navigation and category pages

The site menu contains Home, Explorer, Design and GitHub. Explore has one category index,
with a regular list of narrow, overlapping subject tags. There are no separate Bounds,
Algorithms, Theory, Search or For agents navigation tabs.

Each category has a canonical page at `/explore/<category>/`. It brings together an Algorithms
section, relevant bounds and their assumptions, related mathematical results and definitions.
Algorithm detail pages remain available from those sections.
Linear systems and least squares, eigenvalues and Krylov methods, and trace estimation and
spectral density are separate categories. Membership is many-to-many: a CG lower bound is
listed under Linear systems, Krylov methods and Lower bounds, with one canonical result page. Search is available through the
search field, without a navigation tab. Older bounds routes preserve their query and redirect
to the category page. Existing Rates links and the source catalogue remain compatible.

The page title precedes the site menu and search. Lists and implementation disclosures work
without JavaScript; JavaScript adds search and mathematical typesetting.

## Compact implementation presentation

Each program appears once with its definition link and access model. Its arithmetic models
are nested underneath, each with a Proof and assumptions control. Supplied services,
registered specifications, run models and complete scope are retained under that closed
disclosure, with named links and field labels. Multiple guarantees for one
program share an entry. A parameterized sparse family retains its target without pretending
to be one fixed tree.
Supplied-service phrases link to the shared semantics, interpretation or error-contract
definitions. The structured record retains those declaration identities in `service_definitions`.

The distinction between abstract mathematical analysis and an implementation guarantee is
preserved. A name, tag or dependency is only a discovery aid. Implementation entries require
registered target proofs or explicit reviewed theorem links in `explore.toml`. The additional
links pin complete signatures and require the theorem statements to mention the program and
run model. Missing components, admitted dependencies and changed signatures reject the build.
These are drift checks, not formal verification of an editorial interpretation.

## Human and agent access

Humans can browse by mathematical task, compare bounds, read precise assumptions and cite
literature or a versioned formalization. Every public declaration has its complete signature,
required import, original documentation, source location, statement dependencies and callers.
Definition bodies are accessible when matching source bytes have been supplied.
Reverse dependencies distinguish direct uses in statement types from direct uses in proof or
definition bodies. Both lists show counts and an explicit empty state; neither expands indirect
uses through other declarations. The API exposes `statement_callers` and `proof_or_value_callers`.

Structured records remain under `/explore/api/v1/`, linked from detail pages. They share the
same snapshot as the human pages and require no separate agent interface. The manifest records
the extraction digest, commit, source-hash validation and toolchain. Existing bounded CLI/MCP
readers remain available. Retrieval identifies candidates; Lean checks applicability.

## Validation and preview

Worked examples are the linear-systems category and CG, low-rank approximation and randomized
SVD, and reusable perturbation theory. Check desktop and narrow layouts, keyboard list navigation,
category navigation, closed/open implementation disclosures, old links, search,
shared navigation and readings without JavaScript.

Build from `explore/` with matching extracted data and sources into `../_site/explore`. Add the
homepage, Design, fonts and shared assets to `_site`, as in the deployment workflow. Start
`python3 preview.py` from the repository root and open `http://127.0.0.1:8000/explore/`.

Typography is shared in `css/site.css`: the title, heading spacing, native list bullets,
text line height and inline-math sizing. Explorer-specific styles do not reposition the
site heading or vertically center inline mathematics. Scrolling belongs on display equations
or enclosing resource blocks, since scrolling inline equations shifts their baselines. Browser
tab titles are NLA-lib · Explorer and NLA-lib · Design; the visible headings remain NLA-lib
Explorer and How NLA-lib defines things.
Page headings, list links and dynamic search-result titles all typeset inline title mathematics.

Category sections and guarantee groups use native disclosures, initially closed. Individual bounds
use compact disclosures with their resource summary visible, and assumptions, full statement and
source inside. Bounds have no text or dropdown filters; expansion controls sit on the right. Search indexes documentation,
module context and bibliography metadata as well as names and signatures; repeated terms are
deduplicated, and the local preview serves a compressed, content-versioned index.

Early- and late-truncated output links are derived from theorem output facets and direct
statement references to the algorithm definitions. They lead to the matching statements on the
algorithm page and do not introduce new programs or execution guarantees.
Composed methods such as RSI have their own algorithm pages at the same navigation level as
RSVD. Their pages link the composition's theorem statements and distinguish them from registered
program implementations. Comparison operands do not create output variants for the compared method.

Categories can use `bounds_layout = 'result_groups'` when a compact resource comparison would
omit important kinds of results. Trace estimation uses this layout: Girard–Hutchinson, Hutch++
and SLQ each collect their complete result groups, including variance, expectation and tail
statements where available. Algorithm coverage comes from library `Algorithm:` metadata;
theorem coverage comes from `Result:` metadata and collection membership.
