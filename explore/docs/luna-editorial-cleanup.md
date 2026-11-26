# Luna agent playbook: natural-language library cleanup

This is an editorial cleanup, not a mathematical audit or a formal-proof review.
Prepare proposals; do not run a library-wide rewrite or publish without an assigned
batch and the existing editorial approval process. No cleanup agents are started
by adding this guide.

## Current authorized scope

Clean research-facing statements and named results first: authored shared statements
and additional named-result entries. Raw extracted Lean helper descriptions are
queued for a later pass. Check possible authored/generated aliases before creating
files; the inventory tracks their distinct IDs rather than silently merging them.

## Assignment for each agent

You are a Luna editorial agent for NLA-lib. Clean the assigned natural-language
statements and definitions using the rules below. Preserve their mathematical
meaning, permanent identities, provenance and formal bindings. If an edit requires
mathematical judgment that the available sources do not settle, report the issue
instead of guessing.

The coordinator supplies:

- A batch ID and 3–5 canonical statement UUIDs, with their current revision tokens.
- The corresponding source paths or API object records, and the allowed write scope.
- Relevant surrounding exposition, linked Lean statements, references and definitions.
- A proposal/report destination and, if using the API, a scoped bot credential.

Do not add other entries to your batch. Report dependencies outside it. Do not edit
shared policy files, infrastructure, UI code, generated HTML/JSON, or Lean source.
Never put credentials in a report or source file.

Read these repository documents before editing:

- [Notation](notation.md).
- [Content architecture](../content/README.md).
- [Shared statements and stable identities](../content/statements/README.md).
- [Frontend bibliography](../content/references/README.md).
- [API and publication workflow](../backend/COLLABORATION.md).

## Inventory and source ownership

The coordinator inventories the public `/explore/api/v1/editor/index.json`, filters
statement objects, and deduplicates by canonical UUID. Include existing shared
Markdown and readable statements initially generated from Lean docstrings. Count
repeated placements and library aliases once. Do not assume the public API's
statement picker lists every generated entry.

Fetch the current object with `GET /editor-api/objects/{uuid}`. Record its revision,
formal evidence, inherited citations and editable source. A generated entry can be
materialized through its exported Markdown template with the same UUID and Lean
binding; do not patch its generated HTML/JSON or create a second identity. A blank
readable body is an inventory finding, not permission to invent a theorem summary.
Before materializing a generated entry, check whether an authored file already
uses the same result/declaration binding. Report possible aliases instead of
creating another formulation or merging their distinct IDs/discussions silently.

Keep `uid`, `id`, theorem/definition/result/conjecture kind, `result:` / `decl:`
bindings, relationships, imports and unrelated front matter intact. Do not rename
files, merge duplicates, delete entries or migrate discussions in this pass.

## 1. Preserve the mathematics

- Preserve quantifiers, hypotheses, domains, dimensions, parameter ranges, norms,
  constants, inequalities, probability statements and conclusions.
- Preserve distinctions between real and complex scalars, transpose and adjoint,
  exact and finite-precision arithmetic, deterministic and randomized guarantees,
  upper bounds and lower bounds, and algorithm-specific and general results.
- Resolve a symbol's role from the actual statement and its source. Capitalization
  alone is not evidence that a symbol is a matrix.
- Make the existing hypotheses and conclusion readable. Define a symbol locally
  when its meaning is already unambiguous in the supplied source. Flag genuinely
  missing hypotheses, undefined symbols, conflicting notation or unclear dimensions.
  Do not fill those gaps from mathematical intuition.
- Do not strengthen a claim, omit an inconvenient condition, turn a conjecture into
  a theorem, or infer that a readable formulation is Lean-verified because a Lean
  declaration is linked. Do not add peer-review attestations.
- Preserve existing review/reassessment metadata. The current workflow can flag
  readable-body edits for reassessment, including presentation changes; do not clear
  those flags to make a cleanup look finished.

## 2. Use explicit, consistent mathematical notation

Follow `explore/docs/notation.md`:

| Object | Write |
| --- | --- |
| Latin vector | `\mathbf{x}`, `\mathbf{r}_0` |
| Latin matrix | `\mathbf{A}`, `\mathbf{Q}_k` |
| Greek vector or matrix | `\boldsymbol{\omega}`, `\boldsymbol{\Omega}` |
| Transpose | `\mathbf{A}^{\mathsf{T}}` |
| Hermitian transpose | `\mathbf{A}^{\mathsf{H}}` |
| Scalar, dimension, index | `\alpha`, `n`, `k` |
| First-kind Chebyshev polynomial | `T_q` (a polynomial, not a bold matrix or a transpose) |

Keep indices outside bold font arguments: `\mathbf{x}_k`, not `\mathbf{x_k}`.
A matrix entry can be written `\mathbf{A}_{ij}`; the bold base symbol identifies
its matrix, while the indices remain ordinary. Do not globally replace `*` by
`\mathsf{H}`: scalar conjugation and other meanings require context.

Preserve norm types and subscripts. Do not interchange a vector norm, operator
norm, Frobenius norm or Schatten norm. Keep sets, fields, probability, expectation,
functions and operators in their appropriate existing fonts. Preserve formal Lean
identifiers verbatim inside Lean code.

Preserve existing mathematical expressions and their inline/display segmentation in
bulk cleanup; do not combine or split environments to redesign the layout. Report
layout issues separately so a source comparison can distinguish formatting from a
lost condition. Use supported math delimiters and braced font commands. Avoid display math inside
link labels, raw HTML, custom macros or layout tricks. Keep formulas as mathematical
text rather than images. Suggest reviewed symbol-role additions for
`explore/notation.json` in the batch report; the coordinator merges those proposals
rather than having parallel agents edit one global registry.

## 3. Move citations out of the statement box

"Into the page" means the References section of that statement's own page. The
citation association still belongs to the canonical shared statement so it survives
reuse on several topic pages. Do not transfer all sources to just one topic page.

- Remove bibliographic citation strings from readable theorem/definition prose and
  retain them as structured references rendered below the statement.
- `object.references` lists authored associations only. An empty list does not
  mean there are no inherited citations. Check `reference_links.inherited`; if that
  field is absent in an older snapshot, read the linked declaration's
  `/explore/api/v1/declarations/{declaration}.json` `record.references`. Record the
  actual key/locator pairs. Reuse those associations instead of duplicating them.
  Otherwise use an existing citation key from the shared frontend bibliography.
- Reread the whole sentence after removing a citation. Preserve author attribution
  or an exact-model qualification when needed to identify which subclaim the source
  supports. Do not leave a dangling “is” or a pronoun that now points to another proof.
- Preserve the edition/version and exact locator: theorem, section, equation or page.
  Preserve which claim a source supports when a statement has several parts. If that
  association cannot be represented clearly, flag it rather than dropping it.
- Do not add a citation from a related declaration as if it were already attached
  to this statement. Report that source as a separate candidate.
- Do not invent citation keys, DOI/arXiv IDs, theorem numbers or source metadata.
  Report missing bibliography entries for a separate reference proposal.
- Keep source attribution that is mathematically essential unless it can be replaced
  by a precise definition link or an unambiguous reference note. Flag unresolved cases.
- Keep proof sources distinct from bibliographic citations. A result without a
  complete Lean proof must retain an explicit external natural-language proof URL
  under `proofs`. Definitions and conjectures are exempt. Do not turn an ordinary
  citation into a claim that its linked document proves the result.

Example of structured references on a shared statement:

```yaml
references:
  - key: HornJohnson2013
    locator: Theorem 7.4.8.4
```

Keep the remainder of the file and its existing front matter. Through the API,
submit the corresponding `references` field rather than replacing the whole source
with this fragment.

## 4. Link mathematical concepts, not interface procedures

Use ordinary Markdown links to the existing permanent definition/result page:

```markdown
[Chebyshev polynomials $T_q$](/explore/statements/e7470c95-5c37-5fa0-94b3-ee795973f79d/)
```

The site supplies the hover preview. Do not add "click here," "hover to see," or
other procedural explanation to mathematical prose.

- Preserve the original prose when adding a link. Do not introduce a new clause
  or mathematical claim just to obtain another link.
- Verify the exact target and read its definition. Check its field, domain and
  hypotheses as well as its name. A real-only definition is not automatically an
  acceptable target for a statement allowing complex matrices; report the mismatch
  and leave the term unlinked until resolved. Similar names are insufficient:
  first-kind `T_q` and second-kind `U_q`, for example, must not be confused.
- Link the first useful occurrence in each independently readable statement or
  section. Avoid linking every occurrence, isolated generic symbols or already
  obvious repetitions. Preserve the original wording and formulas in the label.
- Prefer existing canonical definitions/results. Do not create a near-duplicate
  definition merely to obtain a link. Report missing or ambiguous targets.
- Preserve the existing stable UUID URL, even if the displayed title changes.
  The homepage is `/`; statement pages currently retain `/explore/statements/.../`.
- Related-result links must be mathematically relevant; a link does not establish
  that one theorem proves another or that a formal dependency exists.

## 5. Clean presentation without concealing gaps

Use concise descriptive titles, sentence punctuation and readable paragraphs.
Remove extraction residue such as duplicated bold headings or redundant `Result:`
labels when the interface already supplies them. Do not duplicate the title inside
an otherwise self-contained statement.

Statements should be understandable outside their original topic page. Prefer the
mathematical object and claim over unexplained "this," "above," or source-code
implementation names. Expand an abbreviation when its expansion is supported by
the source. Read the statement as a standalone page: bind its solution, initial
guess, iterate, index range and any nonstandard norm. When the exact linked Lean
signature/docstring supplies those definitions or hypotheses unambiguously, add
them and record the source location. Do not merely flag a gap that the exact source
already resolves. If self-containment requires new mathematical content or an
unclear translation of a source contract, flag the issue.

Keep theorem claims separate from proof sketches and connecting exposition. Useful
commentary can follow a blank line starting `Note:` at the end of the same statement
block. The site displays it below the statement box on the individual page and
omits it from list cards; it stays editable with the same statement and revision.
All conditions needed for the claim must precede `Note:`. Remove irrelevant UI or
implementation-navigation chatter rather than relabeling it as mathematics. Record
the exact removed/moved text. Algorithm definition steps remain part of a definition.
Semantic links to an algorithm are appropriate when defining its iterates, e.g.
`[conjugate gradient (CG)](/explore/algorithms/conjugate-gradient/)`.
Do not turn all algorithms into one generic
canonical procedure: model-specific guarantees and implementation assumptions matter.

Report duplicate entries, broken links, unsupported macros, empty prose, missing
proof URLs, incomplete definitions and conflicting sources. Do not hide them by
weakening a statement, inventing a proof or upgrading a page's readiness status.

## Workflow and validation

1. Read each assigned entry, its sources and neighboring definitions before editing.
2. Record the baseline revision and prepare the smallest editorial diff.
3. Preview each edited entry. Check math rendering, definition hover targets,
   references outside the statement box, and repeated placements of shared content.
4. Compare the assigned UUID set with the report and the staged source paths with
   the assigned paths. Derive both from the coordinator manifest, not a remembered
   group number. Compare parsed title/options and mathematical expressions to the
   pinned template, allowing only explicitly reviewed font/bracing changes. A
   parser or successful KaTeX render cannot detect a lost degree bound or a weight
   definition expressed in prose. Reread those definitions and conditions too.
5. Run the repository notation check (`node explore/tests/check_notation.cjs`) and
   relevant content validation when a workspace is provided. A successful render is
   not a mathematical correctness check. CI validates the complete published build.
6. Submit a proposal with a short explanation and an idempotency key, using the
   existing API schema and at most five changed entries. Keep drafts private. A
   stale-revision conflict requires rereading/comparison, never a silent overwrite.
7. Do not self-approve, publish, push to main, deploy, change permissions or modify
   Lean. A reviewer accepts the contribution through the normal workflow.

## Required batch report

For every assigned UUID, report:

- Baseline revision and source path.
- Outcome: `proposed`, `already-consistent`, `needs-mathematical-review`, or `no-NL-prose`.
- Notation changes, citations moved/reused with locators, and definition links added.
- Any proposed relocation or duplicate, with the intended target identity.
- Unresolved issues, supporting source locations and proposed next actions.
- Preview/check results, limitations, and proposal/draft ID when submitted.

The coordinator tracks coverage by canonical UUID and distinguishes proposed from
accepted edits. Start with one small representative pilot batch, review the actual
diffs and rendered pages, then expand. Completing an editorial inventory must not
be described as validating the library's mathematics or formalization correspondence.
