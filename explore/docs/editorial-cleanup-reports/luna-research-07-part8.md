# Luna research cohort 07 · part 8 (corrected manifest coverage)

This report covers exactly the five UUIDs in `/tmp/nla-luna-cohort-07.json` `research[7]`. Baseline revisions and inherited declaration citations were checked against `/tmp/nlalib-release-explorer/api/v1`; relevant Lean source declarations were inspected. This is an editorial review report, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `eacde6b9-1053-568f-8c81-625ce5f50695` (`nlalib-schur-verifiedschurwith-writes`) | `593a535b3f340c3e6455b977432a6406eff8e664507b6b305a52f79804c49343` | `already-consistent` |
| `7455a12b-551e-5cab-81d5-9a9386edaa48` (`nlalib-shiftedqr-roundedshqrschur-measurereal-not-schur-le`) | `8d90be9cc15de4de0f3d68f35133732228e13124218596befdc6a1c73927c778` | `needs-mathematical-review` |
| `f0edd998-f0db-5d93-a1ae-725a1c29ace9` (`nlalib-shiftedqr-roundedshqrwith-measurereal-not-spectrum-le`) | `a555dec3c4e3830544e3f0a3d10fedbba7f9687bbeae9c663e74dd5c3a48a535` | `needs-mathematical-review` |
| `ed822a80-d2e0-5322-b99b-49d2e08073ac` (`nlalib-singularvalues-le-mul-pseudoconditionnumber-of-mul-eq-mul-diagonal`) | `d1535e2e57bd9260723f8e6103c81b1d3cf5040605dd4ed75bdf9000ba45282a` | `already-consistent` |
| `4db025d7-bfbb-5ade-a7bc-94a4f0d7e94f` (`nlalib-smalleig-smalleig-measurereal-not-spectrum-le-unconditional`) | `d34ba2ddd88f4c772578d06c30689e78f7d40632ddddf3e26d558e54cb2e6fc5` | `proposed` |

## Notation and review findings

- Braced `\mathbb{P}` in the SmallEig unconditional spectrum bound. No formula, matrix/vector role, condition, title, UUID, binding, or display segmentation changed.
- `nlalib-schur-verifiedschurwith-writes` and `nlalib-singularvalues-le-mul-pseudoconditionnumber-of-mul-eq-mul-diagonal` already use appropriate matrix/vector fonts and transpose notation; no direct existing definition link was needed.
- The shifted-QR Schur result refers to “the machine and the sampler as above” and the Schur pair in “Shape of the guarantee” above; these are not specified locally in its shared body. Its companion solver theorem similarly says “under the same hypotheses on the machine, the solver and the input.” No assumptions or links were inferred; both entries need review for the intended context.
- The SmallEig statement refers to the machine and streams “as above” and to proved tail records without identifying them in this body. The font fix does not address that context dependency.
- The three Schur/small-eigenvalue guarantees have distinct solver, input, and output conditions. No entries were merged.

## Actual inherited citations

The authored `object.references` arrays are empty. Citations below come from each linked declaration record's `record.references`; no front-matter references were added.

- `NLAlib.Schur.verifiedSchurWith_writes` — none.
- `NLAlib.ShiftedQR.roundedShQRSchur_measureReal_not_schur_le` — `BanksGarzaVargasSrivastava2022`, Theorem 6.3 (listed twice in `record.references`); `BanksGarzaVargasSrivastava2025`, Theorem 1.1 and Corollary 1.3.
- `NLAlib.ShiftedQR.roundedShQRWith_measureReal_not_spectrum_le` — `BanksGarzaVargasSrivastava2022`, Theorem 6.3 (listed twice in `record.references`).
- `NLAlib.singularValues_le_mul_pseudoConditionNumber_of_mul_eq_mul_diagonal` — none.
- `NLAlib.SmallEig.smallEig_measureReal_not_spectrum_le_unconditional` — `BanksGarzaVargasSrivastava2025`, Theorem 1.1.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. No rendered browser preview was available.
