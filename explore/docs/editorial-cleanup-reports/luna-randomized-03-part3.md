# Luna randomized cleanup 03 — part 3

Scope is the final five assigned authored definitions in `/tmp/nla-luna-cohort-03.json`.
Baseline revisions are from pinned editor-object snapshots. For linked declarations,
I checked their `declarations/*.json` records for inherited citations; the entries do
not contain inline citation strings, so those inherited associations are retained
without adding duplicate references. No related-source citations were borrowed.

## Per-UUID results

### `254f7f6f-1199-596d-9347-4d32f1eab873` — Nyström approximation

- Baseline revision: `d9673926f7e275f980bac010d8c3c36c0a0944fa6513de0a066eebfa94e12c3c`.
- Source: `explore/content/statements/nlalib-nystrom-254f7f6f.md`.
- Outcome: `proposed`.
- Changed the Greek test matrix from `\mathbf\Omega` to `\boldsymbol{\Omega}` throughout, preserving formula layout. The Hermitian transpose and matrix/vector roles remain as supplied; dimensions are not bolded.
- Inherited references preserved from `NLAlib.nystrom`: `MartinssonTropp2020` ((2.3), (14.1)); `EpperlyWebber2026` (Definition 3.4; arXiv:2605.19096v2, 31 July 2026); `HalkoMartinssonTropp2011` (Algorithm 5.5). The body has no citation string.
- No definition link added. The statement locally identifies `\dagger` as the Moore–Penrose pseudoinverse; no separate statement-level definition target was verified. The existing pseudoinverse theory page is not a standalone definition target.
- Unresolved: the Lean function is defined for any square `RCLike` matrix, while this explanatory definition scopes the formula to Hermitian positive-semidefinite `A`. This scope is preserved; it should not be interpreted as a formal restriction on the function’s domain. Dimensions of the test matrix are implicit in the product.

### `a93c5a2a-f071-5e53-ad6e-926ccafcbdad` — Generalized Nyström approximation

- Baseline revision: `406fada175afc374b7f33c24fa7fc298142b2a9654c39c7ab2c7cbb58549e63b`.
- Source: `explore/content/statements/nlalib-generalizednystrom-a93c5a2a.md`.
- Outcome: `proposed`.
- Changed Greek sketch matrices from `\mathbf\Omega,\mathbf\Psi` to `\boldsymbol{\Omega},\boldsymbol{\Psi}`. Added a link to [Orthogonal projection](/explore/statements/2fa76a05-ce3c-5a1c-9aee-625c01bfd829/) on the existing phrase “orthogonally projecting”; the target defines the complex-compatible projector concept used in the comparison. No formula, condition, or delimiter was changed.
- Inherited references preserved from `NLAlib.generalizedNystrom`: `EpperlyWebber2026` (Definition 4.1; arXiv:2605.19096v2, 31 July 2026) and `TroppYurtseverUdellCevher2017` ((4.1)–(4.3)). The body has no citation string.
- Unresolved: none identified for this editorial pass.

### `200f4a3a-dbac-5835-8b48-0b498cf09ba3` — Early and late truncation

- Baseline revision: `77dd1516952e67139d0f9112edef407d543d67bf869c03095f61b553d24fb79e`.
- Source: `explore/content/statements/early-and-late-truncation-200f4a3a.md`.
- Outcome: `proposed`.
- Changed `\mathbf\Omega` to `\boldsymbol{\Omega}` in the first sketch expression. The original formula uses the bracket notation `[\mathbf{A}\boldsymbol{\Omega}]_s`; no layout or delimiter changes were made. No link was added because the only occurrence of the truncation concept is the bracketed formula, and a link label would require changing or escaping the expression. No bibliographic references are associated with this authored definition.
- Unresolved: the source does not define the bracket truncation notation locally. The assigned set includes a truncated-SVD definition, but the expression is retained without a link to avoid changing the formula label.

### `e8701eac-1468-573d-bb7a-8a6e8f3bb811` — Late-truncated RSVD

- Baseline revision: `744ee3f5743a166c45da4ec9f4c0cfea6ea8c115ffeff927562fb4133bb0a822`.
- Source: `explore/content/statements/late-truncated-rsvd-e8701eac.md`.
- Outcome: `proposed`.
- Changed `\mathbf\Omega` to `\boldsymbol{\Omega}` and linked the existing phrase “truncated SVD” to [Truncated SVD](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/), which defines the rank-at-most-`k` operation and its choice among ties. No formula or delimiter changes. No citation strings or references.
- Unresolved: the exact projection and test-matrix dimensions remain implicit in the supplied formula; none were inferred.

### `a10be3ad-32a7-5746-ab21-26a6bf70c410` — Early-truncated RSVD

- Baseline revision: `ee378241b0e419dc30bdc6da54ed21e35990f9cbccf74c004e39e7e596c95734`.
- Source: `explore/content/statements/nlalib-earlytruncatedrsvd-a10be3ad.md`.
- Outcome: `proposed`.
- Changed `\mathbf\Omega` to `\boldsymbol{\Omega}`. Linked the existing phrase “rank-at-most-`k` approximation” to [Truncated SVD](/explore/statements/22476dc5-4a8c-59f3-95a5-929740cd4e5b/), whose definition supplies the matching truncation operation. No formula or delimiter changes.
- Inherited references preserved from `NLAlib.earlyTruncatedRSVD`: `Woodruff2014` (Theorem 61), and `CohenElderMuscoMuscoPersu2015` (§10.1 and §7.2; bibliography note specifies arXiv:1410.6801v3, 3 April 2015, with locators following that version). No inline citation string was present.
- Unresolved: none identified for this editorial pass.

## Checks and references

No global symbol-role additions are proposed. Greek sketch matrices `\boldsymbol{\Omega}` and `\boldsymbol{\Psi}` are bolded locally. The references section below each declaration-backed statement continues to use the inherited locator associations listed above; no new citations were added. `node explore/tests/check_notation.cjs` passed: 2,303 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 245 sources; all five batch IDs and both linked target UUIDs were present. All inherited citation keys have frontend `.bib` files. `git diff --check` passed. No rendered preview or full content build was run; these checks do not establish mathematical correctness.
