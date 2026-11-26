# Luna generated results 04 — part 1

This report covers the first five named results assigned in `/tmp/nla-luna-cohort-04.json`.
Each exact exported `source_markdown` template was materialized at its assigned
`source_path`. The pre-materialization alias check found no authored statement with
any of these `result:` bindings. UUIDs, generated IDs, kinds, titles, result bindings,
mathematical expressions, and delimiter segmentation are retained.

The editor snapshots have empty authored `object.references` arrays. Inherited
references below were read from each snapshot's `reference_links.inherited`, not
inferred from those empty arrays. No references were borrowed from related results.

## Per-UUID results

### `329be497-eaac-5ded-8e53-229f108a0f5b` — `albert-theorem`

- Baseline revision: `6072f5600ef627ab60b995065b7eafd34c37874ea57e7d459fed19d7342e2e95`.
- Source: `explore/content/statements/entry-329be497-eaac-5ded-8e53-229f108a0f5b.md`; declaration `NLAlib.posSemidef_fromBlocks_iff_exists` in `NLAlib/Matrix/Basic/SchurComplement.lean`.
- Outcome: `proposed`.
- Removed `[HornJohnson2013, Theorem 7.7.9]` from the box while retaining the explanation that the cited formulation uses the pseudoinverse solution and range condition, whereas this result permits any solution. The inherited reference association is exact: `HornJohnson2013`, Theorem 7.7.9 (second edition). No notation change or definition link.
- Unresolved: none identified for this editorial pass.

### `09c415ab-71d6-54a8-9368-71c4bb24bcb1` — `amm-countsketch`

- Baseline revision: `e1f4b822dce21f369791d47bc725d3e4aaf8b81165a22b32524077986ef3243d`.
- Source: `explore/content/statements/entry-09c415ab-71d6-54a8-9368-71c4bb24bcb1.md`; declaration `NLAlib.integral_frobNorm_conjTranspose_mul_sub_sq_le_of_hasLaw_countSketch` in `NLAlib/Sketching/Sparse/CountSketch.lean`.
- Outcome: `proposed`.
- Removed the inline Woodruff citation and replaced the dangling “there” with “Woodruff’s bound,” retaining the comparison that Woodruff’s real-field JL-moment bound uses `3\varepsilon`. The inherited reference `Woodruff2014`, Theorems 13 and 14, remains attached. Matrices/norms are already object-aware; no link added.
- Needs mathematical review: the body says “over any field,” while the linked formal signature is for `[RCLike 𝕜]`; its prose fragment also does not state the `CountSketch` law for `S` that appears in the formal signature. These conditions were not changed under this editorial-only pass.

### `75d825fd-d8f5-514f-a172-b055c892f8e6` — `amm-ose`

- Baseline revision: `1949e343154b0030318b707cfd955e0a5a2eb554e90840b5972c430e7c719c8a`.
- Source: `explore/content/statements/entry-75d825fd-d8f5-514f-a172-b055c892f8e6.md`; declaration `NLAlib.HasJLMoment.integral_frobNorm_conjTranspose_mul_sub_rpow_le` in `NLAlib/Sketching/Properties/MatrixMultiplication.lean`.
- Outcome: `proposed`.
- Removed `[Woodruff2014, Theorem 13]`, retaining the comparison that Woodruff’s bound uses `3\varepsilon`; the inherited `Woodruff2014`, Theorem 13 association is exact. Kept the stated real-only theorem and the separate complex sharpness example, with Pauli matrices bold and scalar random variables unbold. No definition link added.
- Unresolved: no additional issue beyond the distinction already stated in the body between the real theorem and the complex example.

### `b6186659-9ac3-5ed4-8d2b-a4809261a416` — `amm-sampling`

- Baseline revision: `1cb03e02298ea7ccdb1e25b9a2cb36847ff04c5de3120e6d46d25ed4b3b1fb1c`.
- Source: `explore/content/statements/entry-b6186659-9ac3-5ed4-8d2b-a4809261a416.md`; declaration `NLAlib.integral_frobNorm_conjTranspose_mul_sub_sq_le_of_hasLaw_samplingSketch` in `NLAlib/Sketching/Sampling/MatrixMultiplication.lean`.
- Outcome: `proposed`.
- Removed the inline `[MartinssonTropp2020, §7.1]`; the inherited association `MartinssonTropp2020`, §7.1, preserves that locator. No notation changes or definition links.
- Unresolved citation: the body also says “Drineas, Kannan and Mahoney 2006, Lemma 4 (citation to confirm).” No matching frontend bibliography entry was found, and no inherited association carries it. This string remains in the statement rather than being dropped or converted into invented metadata. Propose a separate bibliography/reference review to confirm the source and locator before structuring it.
- Needs mathematical review: the body starts with a conditional fragment (“if”), and the row norms are unsubscripted although the declaration signature uses Euclidean row norms (`WithLp.toLp 2`). No claim or norm subscript was changed.

### `00a27249-178a-5ab2-874f-d1911f8ddac4` — `amm-sampling-spectral`

- Baseline revision: `669109af3ab7d264c161e256506286852946cb786b69d2e68e7b757642a5fa36`.
- Source: `explore/content/statements/entry-00a27249-178a-5ab2-874f-d1911f8ddac4.md`; declaration `NLAlib.measureReal_specNorm_conjTranspose_mul_sub_ge_le_of_hasLaw_samplingSketch` in `NLAlib/Sketching/Sampling/MatrixMultiplication.lean`.
- Outcome: `proposed`.
- Removed inline citations to `MartinssonTropp2020` and `Tropp2015`; the inherited references preserve §7.3, Theorem 7.2, and §6.4 respectively. Kept the original qualifier that the Tropp corollary locator needs checking. No notation changes or definition links.
- Needs mathematical review: the readable body is a conditional fragment, and its source note marks the corollary locator for `Tropp2015` as uncertain even though the linked declaration record carries §6.4. That uncertainty is retained explicitly; the locator was not independently corrected.

## References and checks

The only citation that remains as an unstructured string is the unverified Drineas–Kannan–Mahoney candidate above; its exact source key/locator is not in the frontend bibliography or inherited associations. All other cited keys exist in the frontend bibliography and the inherited associations listed above were preserved. No definition links were added because no exact in-scope definition target was verified as useful to the first occurrence in these statements. No registry changes proposed. `node explore/tests/check_notation.cjs` passed: 2,353 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 250 sources; all five assigned UUIDs, generated IDs and result bindings matched, and a source-to-output comparison confirmed every original math segment is byte-for-byte unchanged. The four inherited citation keys have frontend `.bib` entries. `git diff --check` passed. No preview or full content build was run.
