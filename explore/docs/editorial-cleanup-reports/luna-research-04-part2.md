# Luna research cohort 04 · part 2

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. Baseline revisions and
formal evidence were checked against `/tmp/nlalib-release-explorer/api/v1/editor/objects/`;
inherited references were checked through the linked declaration records. No proposal
was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `9fd58d97-e831-5cb7-9bf8-24b035ded4c6` (`dense-schur-backward-error`) | `72367420e9112d455a75b6c47206083300a258b869bf5b507b506b432dabd19b` | `explore/content/statements/dense-schur-backward-error.md` | `already-consistent`; unresolved “as above” context |
| `db934d13-3642-524f-9980-66c833e0f17a` (`dense-schur-certificate-accuracy`) | `892995e3a848d7dd8c62a409e2c59f6b1a166a02be9bf3d7bad0246b5685e05e` | `explore/content/statements/dense-schur-certificate-accuracy.md` | `proposed`; unresolved inherited hypotheses |
| `76f46a7e-26fd-5477-b3af-e95d89422696` (`dense-schur-exact-unitary`) | `da501bcf9b933eafd2b293a6ba2b02674c91ccf4e94fa825aeff9dd16a23fa0c` | `explore/content/statements/dense-schur-exact-unitary.md` | `proposed`; unresolved inherited hypotheses |
| `0fd77512-96c3-582c-b497-d366e5477268` (`dense-schur-small-block-oracle`) | `dc5536502edb5b6ba88602f068d90713c4327def1aef25d358896a89512775c0` | `explore/content/statements/dense-schur-small-block-oracle.md` | `already-consistent`; unresolved “as above” and “ranges above” context |
| `6b9702ff-31b4-53a0-a649-f5445c79ee30` (`eckart-young-frobenius-044d6c37`) | `aa2f4bb96983dd8a92d2ee8ca1b5ee6cf888b06d6ef9ab1051b6e3dbf67b9262` | `explore/content/statements/eckart-young-frobenius-044d6c37.md` | `already-consistent`; duplicate relationship reported |

## Changes and inherited references

- The dense Schur statements already use role-aware matrix/vector notation and braced
  font commands; no math formatting was changed.
- `dense-schur-certificate-accuracy` links the existing phrase “dense Schur theorem”
  to the primary statement at `/explore/statements/9fd58d97-e831-5cb7-9bf8-24b035ded4c6/`.
- `dense-schur-exact-unitary` links the existing phrase “same hypotheses” to that
  same primary statement. This is a direct source-scope cross-reference, not a new
  theorem claim.
- No safe definition link was added to the small-block-oracle statement: the
  existing small-block leaf entry describes a particular solver meeting the
  contract, not the generic contract `L` must satisfy. No link was added to the
  primary dense Schur theorem itself.
- The Eckart–Young formula uses matrix notation consistently. Its peer entry
  `eckart-young-frobenius.md` (UUID `35e54249-105c-5da3-980b-30e3d93943b4`, in
  batch 3) has the same `result:eckart-young-frobenius` binding and exactly the same
  inequality with the same rank condition, but has a distinct UUID, ID, title and
  prose. The two entries are likely duplicate authored statements; both identities
  are retained for curator review.
- Actual inherited citation pairs from linked declaration records:
  `dense-schur-backward-error` — `BanksGarzaVargasSrivastava2022`, Theorem 1.4;
  `BanksGarzaVargasSrivastava2025`, Theorem 1.1.
  `dense-schur-certificate-accuracy` — the same two pairs.
  `dense-schur-exact-unitary` — none.
  `dense-schur-small-block-oracle` — `BanksGarzaVargasSrivastava2022`, Theorem 6.3.
  `eckart-young-frobenius-044d6c37` — `HornJohnson2013`, §7.4.9.
  `reference_links.inherited` is absent in this snapshot, so each declaration's
  `record.references` was inspected. No citation was duplicated or moved inline.
- All UUIDs, IDs, theorem kinds, result bindings, formulas, assumptions, titles and
  metadata were retained.

## Symbol-role registry proposal

No global registry changes are proposed. All five statements already identify
their matrices and scalars with the appropriate roles.

## Unresolved issues

- `dense-schur-backward-error.md:8` and `dense-schur-small-block-oracle.md:8` refer
  to “the machine and the streams as above”; the statement files do not contain
  those antecedents. The small-block statement also refers to parameter ranges
  “above.” Do not fill these in without identifying the intended surrounding source.
- `dense-schur-certificate-accuracy.md:8` and `dense-schur-exact-unitary.md:8`
  inherit assumptions through a direct link to the primary theorem. Confirm that
  this is sufficient for standalone reading; no assumptions were copied or inferred.
- The two Eckart–Young Frobenius entries retain separate IDs and UUIDs despite
  sharing a result binding and inequality; review for duplication without merging
  or deleting either identity in this pass.
- No citation mismatch or missing proof URL was found. All five linked declarations
  have `admission_reported: false`.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after
editing. The notation check validates math parsing and registered notation roles,
not theorem correctness. The two direct dense-Schur links were checked against
the target statement's scope. No rendered browser or repeated-placement preview
was available.
