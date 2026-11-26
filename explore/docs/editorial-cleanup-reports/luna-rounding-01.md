# Luna rounding statements batch 01

Source snapshot: `83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`.
Baseline revisions, evidence, and reference associations were checked against
`/tmp/nlalib-release-explorer/api/v1/editor/objects/` and, for the theorem, its
linked declaration record. No proposal was submitted; this is a local review batch.

| UUID / entry | Baseline revision | Source | Outcome |
| --- | --- | --- | --- |
| `ea514d30-5b7f-5590-a122-8ec993658af3` (`cg-scalar-rounded-operation-count-energy-error`) | `b81d87a1d518141d683d140179dffbaf878e96bc4279695ad6fc9073e01f5fae` | `explore/content/statements/cg-scalar-rounded-operation-count-energy-error.md` | `proposed`; mathematical review needed for source/body correspondence |
| `65719e4e-6ea0-536c-91c1-7624e92b30d1` (`standard-rounding-65719e4e`) | `8aacce247805ed383c865e5b8dea6e298f5ed1335a009596f9ee172b64c769e7` | `explore/content/statements/standard-rounding-65719e4e.md` | `proposed` |
| `01b91c62-c0a4-5fb4-b5a3-c4049d568957` (`sequential-summation-in-standard-rounding-01b91c62`) | `f0a6b14fb0a487505843534b77bbb106dc971969308595e031c2ca875b24a971` | `explore/content/statements/sequential-summation-in-standard-rounding-01b91c62.md` | `proposed` |

## Edits and references

- `cg-scalar-rounded-operation-count-energy-error`: retained existing bold matrix/vector notation; braced `\mathbb{R}` and `\mathbf{0}` consistently. Linked the existing phrase “standard model” to the standard-rounding definition at `/explore/statements/65719e4e-6ea0-536c-91c1-7624e92b30d1/`.
- `standard-rounding-65719e4e`: no notation changes were needed. Unit roundoff `u` and the other arithmetic symbols are scalars. The entry is itself the relevant definition, so no self-link was added.
- `sequential-summation-in-standard-rounding-01b91c62`: no vector or matrix symbols occur; `u`, `d_n`, and `n` remain scalar/coefficient/dimension notation. Linked the existing phrase “standard-rounding model” to the definition at `/explore/statements/65719e4e-6ea0-536c-91c1-7624e92b30d1/`. No link was added for pairwise summation because the nearby library definitions concern its error coefficient/profile, not the summation concept itself.
- No citation strings were changed or duplicated. For the theorem UUID, `reference_links.inherited` is absent in this snapshot, so the linked declaration `NLAlib.Krylov.CG.HSCG.Carried.Rounded.Stored.Certification.exec_scalarProgram_work_le_and_quadForm_le` was checked; its `record.references` contains `StrakosTichy2002`, §10. That is the actual inherited pair. The two authored definitions have no formal declaration and no inherited references (`object.references` is empty for authored references).
- The Lean docstring for the theorem also contains `[Greenbaum1997SIMAX]` in the sentence attributing the energy bound to `NLAlib.CGRun.quadForm_sub_x_le_four_mul_pow_add` (`ScalarTheorem.lean:81–83`), but this key is not in the linked declaration's `record.references`. It was not added to this statement: its relation is to the cited component theorem, and the assigned statement's reference support needs curator review if that association should be retained separately.
- All UUIDs, IDs, theorem/definition kinds, result binding, formulas, hypotheses, and existing metadata were preserved. No global symbol registry changes were made.

## Symbol-role registry proposal

If the registry is expanded, propose for `statements/cg-scalar-rounded-operation-count-energy-error.md`:

```json
{"matrices": ["A"], "vectors": ["b", "r", "x"]}
```

The other two assigned entries contain no Latin vector or matrix symbols. `u` is a scalar unit roundoff in every occurrence and should not be bolded.

## Unresolved issues

- `cg-scalar-rounded-operation-count-energy-error.md:8–22` does not identify the specific Hestenes–Stiefel scalar program or its zero initial iterate, although the formal docstring at `NLAlib/Krylov/CG/HSCG/Carried/Rounded/ScalarTheorem.lean:47–84` states both. The text describes the fixed program only as “the run” and “the fixed program.” Confirm whether shared surrounding context is intended to supply the algorithm and initialization; do not add those claims without review.
- The same Lean docstring attributes the exact-CG component bound to `Greenbaum1997SIMAX`, but this is not represented in inherited `record.references` (which contains only `StrakosTichy2002`, §10). Keep the source attribution distinction under review; no related theorem citation was transferred or added.
- `standard-rounding-65719e4e.md` and `sequential-summation-in-standard-rounding-01b91c62.md` are authored definitions with no formal Lean declaration. No missing hypotheses or conflicting definitions were identified in their supplied content.

## Validation and limits

`node explore/tests/check_notation.cjs` and `git diff --check` were run after editing. The notation check validates math parsing and declared notation rules; it does not verify the mathematical claims. The exact definition target was read in `standard-rounding-65719e4e.md` and its UUID matches the link. No rendered browser preview or repeated-placement preview was available in this source-only batch.
