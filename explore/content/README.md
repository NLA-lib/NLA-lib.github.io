# Editing the explorer

These Markdown files are the editable source of the new explorer. The old topic
navigation is replaced. HTML, relationship lists, theorem signatures, and the full
Library reference are generated at build time.

Start with `algorithms/lanczos/index.md` for a placeholder algorithm, or
`theory/matrix-polynomials.md` for a theory page belonging to two subjects.
`algorithms/conjugate-gradient/index.md` shows editable theorem prose backed by
extracted Lean statements.

## A page

```markdown
---
kind: algorithm
id: my-method
title: My method
summary: The question this method answers.
status: placeholder
tasks: [linear-systems, eigenvalues]
theory: [spectral-theory, krylov-spaces]
---

Write an introduction here. Ordinary Markdown lists, links, code, and $math$ work.

## Implementations

{{ generated:implementations }}

## Mathematical background

{{ generated:theory }}
```

Add a mathematical algorithm under `algorithms/<id>/index.md`; add an implementation under
`algorithms/<algorithm>/implementations/<id>.md`, with `kind: implementation` and
`algorithm: <algorithm>` in its header. File locations are for contributors;
identities in the header determine canonical URLs. Family pages use `kind: family`
and live under `families/<id>.md`; algorithms name their `families` in the header.
Implementation pages link to their mathematical method with
`{{ generated:mathematical-method }}`; its prose and theorems are authored once.

Kinds: `family`, `algorithm`, `implementation`, `task`, `theory`, `index`, `home`.
Statuses: `ready`, `outline`, `placeholder`.
Status describes the curated page,
not whether an algorithm or theorem exists in the library.

## Relationships and generated metadata

- A family's `tasks` list places it on task pages. An algorithm's `families` list
  generates the family's methods and the algorithm's family links. Algorithms without
  a family appear directly under their tasks; each method keeps its own canonical URL.
- Its `theory` list supplies background links and each theory page's reverse
  "Used by algorithms" list.
- `uses` names component algorithms. A composed method has its own canonical page;
  the component's applications list is generated automatically.
- Theory pages use `parents` for overlapping subjects and `prerequisites` for
  mathematical dependencies. Neither creates a duplicate page.
- `library_algorithm: lanczos` identifies the extracted algorithm and collects its result IDs.
  Set `library_results: false` to keep that identity while selecting only explicit
  `result_ids` for this method, rather than collecting related methods' results.
- `library_topics: [matrix-norms]` collects definitions and results from an indexed
  subject. `result_ids` adds specific result IDs; `module_prefixes` selects source modules.

Generated sections are single lines of `{{ generated:<name> }}`. Available names:
`entry-points`, `tasks`, `families`, `algorithms`, `implementations`, `mathematical-method`, `theory`, `theory-topics`,
`subtopics`, `prerequisites`, `used-by`, `components`, `applications`,
`task-membership`, `results`, `definitions`, `library-counts`, `library-index`.

The CG adapter additionally supplies `cg-definition`, `cg-resources`, and
`cg-accuracy`. These preserve the current program/model demo using matching core
source metadata; the surrounding prose, headings, and placement are Markdown-owned.

## Editable statements with generated Lean details

```markdown
::: theorem result:cg-chebyshev-bound name="Chebyshev convergence"
Write the readable statement here, including its hypotheses and $math$.
:::
```

The result ID supplies its primary Lean declaration, exact signature, and GitHub
source link. `decl:<full-name>` selects a declaration directly. The `name` option
is optional when the library record has a useful title. An optional `id=anchor`
adds a stable link target. The body is editorial prose;
editing it does not change the formal theorem.

An explanatory definition can omit a source:

```markdown
::: definition name="A useful concept"
An authored mathematical definition.
:::
```

An unsourced theorem is rejected. Unknown result/declaration names, wrong statement
kinds, missing relationships, duplicate routes, and unknown generated markers reject
the build. Metadata associations never establish an execution or accuracy guarantee.

## Rendering and rebuilding

Install `python3 -m pip install -r explore/requirements.txt` from the website root.
The regular `explore/build.py` CLI builds the reference data and then these pages.
It fills CG implementation pages automatically when matching published sources
contain the new core. GitHub source links use the extraction's commit and verified
source fingerprints. Use the optional `--core-src /path/to/NLAlib` to preview a
newer working core; unpublished file bytes remain explicitly labeled.

To re-render Markdown without repeating extraction or the source build:

```sh
python3 explore/content_pages.py --site _site/explore
```

Source metadata stays in `api/v1/`; `editorial-pages.json` records the Markdown
identities, relationships, paths, statuses, and content fingerprints. Editorial
pages also enter the same search index as the library statements.

## Sections and statement links

Second-level headings become collapsible sections. Mathematical background,
Appears under these tasks, and Family start collapsed; the other sections start expanded. Put
Implementations near the top of a method page, before its detailed analysis.
Every theorem and definition has a Copy link action alongside its Lean/source details. Source-backed statement anchors
use their result/declaration identity; set `id=your-stable-anchor` to choose one.
Implementation links to arithmetic-specific statements preserve the selected model.
Opening a statement link expands its containing sections.
