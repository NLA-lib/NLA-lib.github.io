# Luna randomized cleanup 03 — part 2

Scope is the second five assigned authored definitions in `/tmp/nla-luna-cohort-03.json`.
Baseline revisions below come from the pinned editor-object snapshots and linked
`declarations/*.json` records. The declaration-backed entries have empty authored
`object.references` but nonempty inherited declaration citations; those associations
are preserved. Their bodies contain no inline bibliographic strings to relocate. No
citation was borrowed from a related entry.

## Per-UUID results

### `dd0c654f-b783-516b-b7c3-04b96f1a90f3` — Subspace embedding

- Baseline revision: `a40c4d5ac5acce6ce6ea348bf5c8ed36c108d4a9ac42170d691095e11b1a88e7`.
- Source: `explore/content/statements/subspace-embedding-dd0c654f.md`.
- Outcome: `already-consistent`.
- Matrix/vector symbols, scalar distortion `\varepsilon`, and norm subscripts are already object-aware. No citations or definition links added. This is an authored definition with no linked declaration; no inherited declaration references apply.
- Unresolved: the ambient dimensions for `S` and `V` are implicit in the map and are not specified. Preserved as written.

### `161d8fd6-2f0a-5e7e-8b4c-e7e67c1e6289` — CountSketch

- Baseline revision: `102a6ef5ba67bd1c6b34b8d142e3faece061c0a1e75c219741f014d0fb33c56c`.
- Source: `explore/content/statements/nlalib-countsketchmatrix-161d8fd6.md`.
- Outcome: `proposed`.
- Added a link on “embedding guarantees” to [Subspace embedding](/explore/statements/dd0c654f-b783-516b-b7c3-04b96f1a90f3/), which defines the norm-distortion condition. The target and this statement are compatible with the real/complex sketch setting. The matrix-entry notation `\mathbf{S}_{a,i}` correctly bolds only the matrix symbol; `a,i,n,s,h,\sigma_i` remain scalar/index/function roles.
- Inherited citation associations preserved from `NLAlib.countSketchMatrix`: `Woodruff2014` (§2.1, before Theorem 8), `CamanoEpperlyMeyerTropp2025` ((B.1)), and `MartinssonTropp2020` (Remark 9.1). No citation string was in this statement body; no additional reference was added.
- Unresolved: none identified for this editorial pass.

### `604d3a67-5a4c-5dc9-9933-06e04ea9ac41` — Subsampled randomized Hadamard transform

- Baseline revision: `357993c58e092d02ae1f36198faacdeddb11987562b304bc50a6717e0daad4e9`.
- Source: `explore/content/statements/nlalib-srhtmatrix-604d3a67.md`.
- Outcome: `already-consistent`.
- Matrix symbols `S,R,H,D` are bold; scalar dimensions and scaling parameters remain unbolded. No inline citations or links added.
- Inherited citations preserved from `NLAlib.srhtMatrix`: `MartinssonTropp2020` (§9.3), `HalkoMartinssonTropp2011` (§4.6), and `Woodruff2014` (Theorem 7). `object.references` was empty, but the linked declaration record supplies these inherited associations.
- Unresolved: “the library’s more general structured-transform definition” has no distinct matching authored definition target verified in the shared statements. No link added.

### `15e6c9dc-370c-5cb2-b684-46e5f33e39f2` — Range-finder approximation

- Baseline revision: `e468237fd597168509fa2416e297a93fb703c5489aa86f40fa0357566187d2ca`.
- Source: `explore/content/statements/nlalib-rsvd-15e6c9dc.md`.
- Outcome: `already-consistent`.
- Matrix symbols and the scalar rank parameter are correctly styled. No inline citations or links added.
- Inherited citations preserved from `NLAlib.rsvd`: `HalkoMartinssonTropp2011` (Algorithm 4.1) and `MartinssonTropp2020` (Algorithm 8). The authored references list is empty; these were checked in the linked declaration record.
- Unresolved: none identified for this editorial pass.

### `22476dc5-4a8c-59f3-95a5-929740cd4e5b` — Truncated SVD

- Baseline revision: `48aecdba1438c70d12f7944ab09de080f67def2e2caa027e33ed8de047290dff`.
- Source: `explore/content/statements/nlalib-truncatedsvd-22476dc5.md`.
- Outcome: `proposed`.
- Added a link on the first useful occurrence of “singular values” to [Singular values](/explore/statements/581c9098-24f3-55b6-bd36-a47af48b21ff/). The target defines the decreasing, zero-padded singular values of real or complex matrices, matching this entry’s `RCLike` declaration. No mathematical text or delimiters were changed.
- Inherited citation preserved from `NLAlib.truncatedSVD`: `GolubVanLoan2013`, fourth edition, Theorem 2.4.8. No inline citation string was present; no additional reference was added.
- Unresolved: the exact tie-breaking rule is described only as “the library fixes a choice”; its rule is not supplied here. Retained as written without guessing the choice.

## Checks and references

All citation keys above exist in the frontend bibliography. No new citation associations were added. The only links added target the exact subspace-embedding and singular-value definitions; no other link target was verified as necessary and scope-matched. No global symbol-role additions are proposed. `node explore/tests/check_notation.cjs` passed: 2,303 authored equations checked with KaTeX, 0 errors. `statement_sources.load_statements` parsed all 245 sources; all five batch IDs and both linked target UUIDs were present. All inherited citation keys have frontend `.bib` files. `git diff --check` passed. No rendered preview or full content build was run; these checks do not establish mathematical correctness.
