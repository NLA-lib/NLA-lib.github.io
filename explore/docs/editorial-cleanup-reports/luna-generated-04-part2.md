# Luna generated results 04 — part 2

This report covers the second five named results in `/tmp/nla-luna-cohort-04.json`.
The alias check found no existing authored statement with any assigned
`result:` binding. Exact exported templates were materialized at the assigned
paths with IDs, titles, kinds and theorem bindings intact. Original mathematical
expressions and math-delimiter segmentation are preserved.

The snapshots have empty authored `object.references` arrays. The inherited
citation associations listed below were read from `reference_links.inherited`.
No citations were borrowed from related declarations.

## Per-UUID results

### `1626e38d-7b50-553b-8634-1b9cda95b03d` — `amm-srht-spectral`

- Baseline revision: `40df1d50b2ca41c1ee664e75f73faf51da1adeaed71645a240ce892abf14879a`.
- Source: `explore/content/statements/entry-1626e38d-7b50-553b-8634-1b9cda95b03d.md`; declaration `NLAlib.measureReal_specNorm_conjTranspose_mul_sub_ge_le_of_hasLaw_srht` in `NLAlib/Sketching/Structured/SRHTMultiplication.lean`.
- Outcome: `proposed`.
- Removed `[Tropp2011a, Lemma 3.3]` from the body while retaining the source qualifier that the reference supports flattening and that the bound is this proof’s, with no printed source in hand. The inherited `Tropp2011a`, Lemma 3.3 association remains attached. Added an ordinary link on “SRHT” to [Subsampled randomized Hadamard transform](/explore/statements/604d3a67-5a4c-5dc9-9933-06e04ea9ac41/). The target defines the same transform from a supplied bounded orthonormal matrix, signs and without-replacement row selection. No math font or formula changes.
- Needs mathematical review: the prose ends “Any field,” but the formal signature is over `RCLike 𝕜`. The displayed bound also depends on helper bounds whose source names remain in HTML comments; preserved without altering them. The Tropp citation supports only flattening; the source states that the bound itself has no printed source.

### `d8971d3c-b85b-54eb-8089-7148a3b15095` — `arnoldi-basis`

- Baseline revision: `f2340ca248c9873a34b10c9088daec27a830db57d38d23f968c47c016ac86409`.
- Source: `explore/content/statements/entry-d8971d3c-b85b-54eb-8089-7148a3b15095.md`; declaration `NLAlib.IsGradedKrylovBasis.eq_arnoldiMatrix` in `NLAlib/Krylov/Processes/Lanczos.lean`.
- Outcome: `already-consistent`.
- No citation or notation edits. No definition link added: the available authored Krylov-space definition is real-only, while this declaration is generic over `RCLike`. The Arnoldi-process definition does not state the graded-basis characterization used here, so it was not treated as an exact substitute target.
- Needs mathematical review: the body calls the diagonal positive “in the order of `\Bbbk`,” although the theorem signature permits complex `\Bbbk`; it does not spell out how positivity is interpreted for the complex field. The prose also relies on the undefined-in-body phrase “graded basis.” The declaration signature gives `IsGradedKrylovBasis` and the positive-diagonal condition; no interpretation was added.

### `32569e9a-bd08-5fe4-a6d4-4e985e217334` — `arnoldi-breakdown`

- Baseline revision: `a6cd032e095e0e82420af71ce27d647f1d850d441ccd65d7ac92d3a9fb698f1d`.
- Source: `explore/content/statements/entry-32569e9a-bd08-5fe4-a6d4-4e985e217334.md`; declaration `NLAlib.mgsArnoldiHessenberg_apply_succ_eq_zero_iff` in `NLAlib/Krylov/Processes/ArnoldiRecurrence.lean`.
- Outcome: `proposed`.
- Removed `[Saad2003, Proposition 6.6]`; inherited `Saad2003`, Proposition 6.6, remains attached. Removed the duplicate sentence-final period produced when the citation was removed. No math or definition link changes.
- Needs mathematical review: `h_{j+1,j}` and `\nu` are not defined in the body; the declaration identifies them as a subdiagonal entry of the Arnoldi Hessenberg matrix and the Krylov grade. The authored grade definition is real-only, while this theorem permits `RCLike`, so no link was added.

### `ca12c08e-6518-5efb-b1d7-78063a6b6cce` — `arnoldi-hessenberg`

- Baseline revision: `cc6ce215420121959c00ada5d9e1f9493eb033bbdd3d33cf313bb03ce5267779`.
- Source: `explore/content/statements/entry-ca12c08e-6518-5efb-b1d7-78063a6b6cce.md`; declaration `NLAlib.IsGradedKrylovBasis.isUpperHessenberg` in `NLAlib/Krylov/Processes/Lanczos.lean`.
- Outcome: `no-NL-prose`.
- The exported body contained only `[Saad2003, §6.3]`. Removed this citation string because the inherited `Saad2003`, §6.3 association is retained below the statement. The body is now empty; no theorem summary was invented. The formal title and result binding remain intact.
- Unresolved: the citation-only body supplied no independently readable natural-language statement. Any summary requires a separate editorial decision based on the theorem signature.

### `484e0bc1-28b6-53c1-be7b-2d3fd0a1d244` — `arnoldi-recurrence`

- Baseline revision: `eeed4e201e9ac411b23c45fbc973ad789c2e73416d64632d1ee6e69a975afcf2`.
- Source: `explore/content/statements/entry-484e0bc1-28b6-53c1-be7b-2d3fd0a1d244.md`; declaration `NLAlib.mgsArnoldiHessenberg_eq` in `NLAlib/Krylov/Processes/ArnoldiRecurrence.lean`.
- Outcome: `proposed`.
- Removed `[Saad2003, §6.3]`; the exact inherited association `Saad2003`, §6.3, remains attached. Removed the duplicate sentence-final period from the citation boundary. Matrices and indices were already object-aware. No link added: the only natural target mention is inside math, and linking it would require changing the preserved delimiter segmentation; the field-generic Arnoldi definition is not a direct definition of this recurrence.
- Unresolved: the body refers to “canonical bases” without stating their defining property. The result is an exact formula for the named Arnoldi matrices; no extra explanation was added.

## References and checks

No global notation additions are proposed. `Tropp2011a`, `Saad2003` Proposition 6.6, and `Saad2003` §6.3 are inherited associations from the linked declarations. No inline citation strings remain in this group. The only definition link is the verified SRHT definition above. `node explore/tests/check_notation.cjs` passed: 2,385 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 255 sources; all five UUIDs, generated IDs and result bindings matched, and a source-to-output comparison confirmed original math expressions and delimiter segmentation are unchanged. The inherited `Tropp2011a` and `Saad2003` keys have frontend `.bib` entries. `git diff --check` passed. No rendered preview or full build was run.
