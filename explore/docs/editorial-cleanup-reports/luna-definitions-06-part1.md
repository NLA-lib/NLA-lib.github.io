# Luna matrix definitions cohort 06, part 1

This report covers only the first five assigned definitions. Baseline revisions and editor metadata were checked in the pinned Explorer editor objects. Each object's authored `object.references` is empty and `reference_links` is null; declaration-level references were checked in the pinned declaration records.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `aaf66e60-a561-5e3e-abff-5cc278379268` | `explore/content/statements/nlalib-shiftedqr-counteddeflationalgorithm-aaf66e60.md` | `1eaebe2c3c80849e1431cebf0bb06ec09d0dda4d34948abf1afa4ecb6da1e7f1` | `already-consistent` |
| `80c3e8b3-6580-5d88-b3ef-e58fffc65691` | `explore/content/statements/nlalib-shiftedqr-exactdeflationalgorithm-80c3e8b3.md` | `4b6ef8699b627e629617f31e375c73a07748ddd6770c051669916fc0e1167ba4` | `already-consistent` |
| `3677cbb0-38a4-5a27-bfbb-f16fd4935300` | `explore/content/statements/nlalib-shiftedqr-forwarddeflationalgorithm-3677cbb0.md` | `9ff634aed12e99eda6faa31a752b754a4d6e01a15d932f4e5d149f77a1231913` | `already-consistent` |
| `a68765a4-81c5-5022-8248-82be1f44fc19` | `explore/content/statements/nlalib-shiftedqr-kernelroutines-a68765a4.md` | `430a041a6ec0e05f91abc637d3e15761a2dae1604566c35417056b5cfd38e1fa` | `already-consistent` |
| `dfd2780d-7c4e-51db-aa04-4766a316f48b` | `explore/content/statements/nlalib-shiftedqr-shqrsmalleigalgorithm-dfd2780d.md` | `3f0d0019fcd6f99a27a785d511d7884b2bb98ac176df46175c0758a8805345e2` | `already-consistent` |

## Findings and source associations

All five assigned definitions already use explicit matrix bolding and appropriately typed scalar/dimension symbols. Their formulas, work/span expressions, input/output conditions, and titles were left unchanged. No direct definition target was identified for the program-specific phrases in these entries; no related concepts were substituted as link targets. The exact solver interface's wording about the stronger interfaces and its Lean details was left intact.

Actual inherited declaration citations:

- `NLAlib.ShiftedQR.countedDeflationAlgorithm`: none.
- `NLAlib.ShiftedQR.exactDeflationAlgorithm`: none.
- `NLAlib.ShiftedQR.forwardDeflationAlgorithm`: `GolubVanLoan2013`, edition 4, Theorem 7.2.2.
- `NLAlib.ShiftedQR.KernelRoutines`: none.
- `NLAlib.ShiftedQR.shqrSmallEigAlgorithm`: none.

No body contains an inline bibliographic string. The inherited citation remains associated with its declaration; no citation was copied to another statement. IDs, UUIDs, formal bindings, formulas, metadata and math-environment segmentation are unchanged.

## Validation and limitations

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run. These checks do not establish mathematical correctness or formalization correspondence.
