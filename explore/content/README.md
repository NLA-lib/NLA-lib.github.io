# Editing the explorer

These Markdown files are the editable source of the new explorer. The old topic
navigation is replaced. HTML, relationship lists, theorem signatures, and the full
Library reference are generated at build time.

Start with `tasks/eigenvalues.md` for task-specific organization,
`algorithms/lanczos/index.md` for a shared algorithm, or
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

- **Task pages own placement.** The Algorithms entry point lists tasks. Each task
  defines its own ordered `groups` in front matter and renders them with
  `{{ generated:task-groups }}`. Group names, depth, and descriptions need not be
  uniform across tasks. The same algorithm can belong to differently named groups
  in different tasks, using the same canonical URL.
- `algorithms` inside a group lists canonical method IDs in display order.
  Optional `summaries` overrides a card's description for this task without
  changing the method page. Optional `family` links a shared conceptual reference;
  it does not automatically insert every member of that family into the task.
- Algorithm task-membership backlinks are derived from these groups. Do not
  duplicate `tasks` lists on canonical algorithms. Legacy explicit task membership
  remains supported for tasks without groups.
- An algorithm's `families` list links shared conceptual family pages. These
  global references are independent of task-local grouping.
- Its `theory` list supplies background links and each theory page's reverse
  "Used by algorithms" list.
- `uses` names component algorithms. A composed method has its own canonical page;
  the component's applications list is generated automatically.
- Theory pages use `parents` for overlapping subjects and `prerequisites` for
  mathematical dependencies. Neither creates a duplicate page.
- `library_algorithm: lanczos` identifies the extracted algorithm and collects its result IDs.
  Set `library_results: false` to keep that identity while selecting only explicit
  `result_ids` for this method, rather than collecting related methods' results.
- `module_prefixes: [NLAlib.Matrix.Norms]` selects extracted definitions and result
  groups from matching modules. `result_ids` adds exact named results; `result_prefixes`
  selects result-ID prefixes. `search_aliases` adds discoverable method names.

Generated sections are single lines of `{{ generated:<name> }}`. Available names:
`entry-points`, `tasks`, `task-groups`, `families`, `algorithms`, `implementations`, `mathematical-method`, `theory`, `theory-topics`,
`subtopics`, `parent-topics`, `prerequisites`, `used-by`, `components`, `applications`,
`task-membership`, `results`, `definitions`, `library-counts`, `library-index`.

For example, one task can use:

```yaml
groups:
- id: krylov
  title: Krylov methods
  summary: Compress the operator and extract Ritz approximations.
  algorithms: [lanczos, arnoldi]
  summaries:
    lanczos: Build a tridiagonal compression for a Hermitian operator.
```

Another task can place `lanczos` under `Shared recurrence`, with a quadrature-specific
description. No second Lanczos page is created. Unknown method IDs, duplicate group
IDs, and dependency cycles reject the build.

Theory subject hubs should navigate to subtopics rather than import every theorem
under a broad module directory. Leaf pages select the modules or results that match
their mathematical scope. Algorithm tags can include relatives: use
`library_results: false` and explicit `result_ids` when necessary to keep a method's
results distinct from compositions and arithmetic-specific implementations.

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

`generated:results` presents the remaining selected results as expandable theorem
or definition rows. Opening a row shows its source documentation; a second
disclosure contains the exact Lean statement and GitHub source information. The
renderer omits results already explained in an authored statement block and merges
rows with the same primary declaration. Admission-reported declarations are labeled
as statements rather than theorems. These rows have stable copyable links.

Use authored blocks for the main results and their reader-facing explanations.
Use the generated rows for additional results whose complete documented hypotheses
should remain available in place. Formal definition indexes start collapsed.

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
Appears under these tasks, Family, and Broader topics start collapsed; the other sections start expanded. Empty generated sections are omitted. Put
Implementations near the top of a method page, before its detailed analysis.
Every theorem and definition has a Copy link action alongside its Lean/source details. Source-backed statement anchors
use their result/declaration identity; set `id=your-stable-anchor` to choose one.
Implementation links to arithmetic-specific statements preserve the selected model.
Opening a statement link expands its containing sections.

## Curated implementation guides

Use `source_guides: [docs/algorithms/Conjugate-Gradient.md]` in a family or method
header and `{{ generated:source-guides }}` in its body. Available guides appear in
a closed disclosure and retain their own Library pages, source Markdown, and
fingerprints. An older source snapshot may not yet contain a guide; it is omitted
until available. Dirty source guides never acquire a GitHub URL under a base SHA.

## Reviewing organization

Run `python3 explore/audit_organization.py --site /path/to/built/explore` to check
task reachability and source selectors. Add `--report explore/docs/design/organization-audit.md`
to refresh the per-page review inventory. This complements relationship validation;
it does not prove the equivalence of editorial prose and Lean statements.

For a complete named-mathematics inventory, run:

```sh
python3 explore/audit_math.py --site /path/to/built/explore \
  --source /path/to/matching/NLAlib --extraction /path/to/explore-data.json \
  --baseline /path/to/previous-extraction.json \
  --published-baseline _site/explore \
  --renames /path/to/matching/NLAlib/docs/renames \
  --report explore/docs/design/mathematical-coverage-audit.md
```

This checks every source module and fingerprint, public declaration record,
`Result:` ID, rendered theorem signature, and tagged method placement. Baseline
comparisons require explicit rename mappings for removed declarations and report
changed signatures. A result selector with no generated results slot does not count
as a visible placement. Unplaced named results or methods fail the audit.
