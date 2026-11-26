# Luna generated matrix cohort 08, part 2

All five assigned records were checked against authored statements for an existing result/declaration alias before any materialization; no aliases were found. Baseline revision tokens and actual inherited key/locator pairs come from each pinned generated-object record. `object.references` was not used as evidence of citation absence.

| UUID / result | Baseline revision and source path | Outcome | Changes and reference evidence |
|---|---|---|---|
| `a4df81d0-303c-59d7-956e-a8f427da92fc` / `cg-near-optimality-lower-bound` | `99dfb8597fc4db34bd09e7b321366c7397432a6e6d8c268d358e88f236f3a2cc`; `explore/content/statements/entry-a4df81d0-303c-59d7-956e-a8f427da92fc.md` | proposed | Removed inline `[ChenPersson2026, Remark 3]`, reusing inherited `ChenPersson2026` (Remark 3). No notation or links changed. |
| `102b8c07-bd6f-5c32-91af-9497410a350b` / `cg-outlier-bound` | `b687993578b92b07684f4a9d53d268e9810aa8264a8e20657721a7cf9231a139`; `explore/content/statements/entry-102b8c07-bd6f-5c32-91af-9497410a350b.md` | proposed | Removed inline `[Greenbaum1997, §3.1]; locator to verify`, reusing inherited `Greenbaum1997` (§3.1). The exported source's uncertainty note was superseded by the exact locator in this entry's inherited association. No mathematical text changed. |
| `00e83819-1eb1-5eae-84d4-ff117f645f97` / `cg-physical-energy-convergence` | `f7603ae67237284b11894047720e5d302c96d89d2bd40d894ae5525a5ef4f359`; `explore/content/statements/entry-00e83819-1eb1-5eae-84d4-ff117f645f97.md` | proposed | Removed inline `[Saad2003, Theorem 6.29]`, reusing inherited `Saad2003` (Theorem 6.29). Kept “No printed source” as supplied and preserved the exact-model versus computed-decrements attribution sentence. No notation or links changed. |
| `e8e684bb-eddc-50eb-838e-041ca826629e` / `cg-physical-energy-decrements` | `98c7f265d069ffc177986489766f79472090cc04bace2046908b3556cf7ca898`; assigned source path `explore/content/statements/entry-e8e684bb-eddc-50eb-838e-041ca826629e.md` | already-consistent | No inherited references and no inline bibliographic citation or notation issue. Per the no-empty-materialization rule, no source file was created. “No printed source.” is retained in the pinned generated template. |
| `3d90708e-a3e4-54b9-853a-c88e3efbc832` / `cg-physical-energy-quadrature` | `b1bcbbf30bfb089a82b054f58b2578d5ed4490d397e2567a7b54e4c085967d1f`; `explore/content/statements/entry-3d90708e-a3e4-54b9-853a-c88e3efbc832.md` | proposed | Removed inline `[MeurantStrakos2006, (3.17)]`, reusing inherited `MeurantStrakos2006` ((3.17)). Kept the surrounding attribution and limitation prose. No notation or links changed. |

## Review and checks

The other four exported templates were materialized with their original UUIDs, `kind`, ids, result bindings, titles and math unchanged. No new definition links or role-registry proposals were warranted. The decrement entry was audited but left unmaterialized because it had no retained editorial change. No mathematically ambiguous statement was altered.

`git diff --cached --check` passed after staging. `node explore/tests/check_notation.cjs` is run for this group before commit; it checks parseability only, not theorem validity or source correspondence. No rendered-page preview was available in this bounded workspace.
