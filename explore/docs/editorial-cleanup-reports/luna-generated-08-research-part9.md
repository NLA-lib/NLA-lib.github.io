# Luna generated research cohort 08, part 9

Scope: exactly `research[8]` from `/tmp/nla-luna-cohort-08.json`. Each baseline revision, generated source and inherited reference pair was checked in its pinned object.

| UUID | Result | Source path | Baseline revision | Outcome | Edit | Actual inherited references |
| --- | --- | --- | --- | --- | --- | --- |
| `deb9cd0c-d96b-5430-81a8-91998791c218` | `spectral-bisection-diagonalization` | `explore/content/statements/entry-deb9cd0c-d96b-5430-81a8-91998791c218.md` | `5bbf6bc7d4c830d9b7268267a1af76e0bd6953eeed625e652710c252107c5bba` | `proposed` | Removed inline citation; retained comparison details about $R_0$, node-dependent accuracy, constants, and nonformalized operation count. | `Shah2024`, Theorem 4.2 |
| `f4d4d0ae-90be-549e-ada9-fcf1cc63b4af` | `spectral-bisection-diagonalization-bits` | `explore/content/statements/entry-f4d4d0ae-90be-549e-ada9-fcf1cc63b4af.md` | `a25db597eaa7395598989155b98f6f58cccd1bb7f6a76de34a653e838949f020` | `proposed` | Removed inline citation; retained the source bit-count formula, sample point comparisons, and shift-avoidance qualification. | `Shah2024`, Theorem 4.2 |
| `c4d23d43-3249-5842-987f-06fe5083e715` | `spectral-density-kolmogorov-tail` | `explore/content/statements/entry-c4d23d43-3249-5842-987f-06fe5083e715.md` | `66e86948e2cc7e95069081c59669d02ea7008b81055ae4eb8a995ad0584ffa90` | `proposed` | Removed inline citation and preserved the unresolved locator-check note and uniform-sphere model qualification. | `ChenTrogdonUbaru2021`, §3 |
| `2e76e626-f2d5-5e11-a53c-60fcca367d9c` | `spectral-density-lipschitz-tail` | `explore/content/statements/entry-2e76e626-f2d5-5e11-a53c-60fcca367d9c.md` | `0d0cb11a1bf9acc1c20cf25130cff65e8804e5f7db1e329ddabd46843fb55d23` | `proposed` | Removed inline citation and retained the explicit theorem-number-check note and uniform-sphere qualification. | `ChenTrogdonUbaru2021`, the Wasserstein bound for SLQ |
| `d6adf613-2ea6-5904-90f3-53743b8f6ec2` | `spectral-measure` | `explore/content/statements/entry-d6adf613-2ea6-5904-90f3-53743b8f6ec2.md` | `a23caa1e99a5c28195e0b758ab1b9e22bbc38992f2d00308feda9969726ad61e` | `proposed` | Removed inline citation and retained the real-symmetric/Riemann–Stieltjes versus `RCLike` scope comparison. | `GolubMeurant2010`, Ch. 7 |

The listed associations are the exact `reference_links.inherited` pairs; no authored duplicates were added. Existing vector/matrix fonts and transpose conventions are consistent. No definition link was added; no precise scope-compatible concept target was verified. IDs, titles, result bindings, formulas, hypotheses and front matter were preserved.

## Unresolved issues

- Both spectral-density entries explicitly warn that their citation locators need checking; those warnings remain. No replacement locator was inferred.
- The long finite-precision diagonalization statements contain many parameter constraints and source comparisons. Those were retained, not mathematically audited.
- The spectral-measure entry's real-symmetric source scope versus its broader `RCLike` result is preserved as a scope comparison, not treated as proof that the source establishes the broader result.
- No preview/rendering was run.

## Validation

- `node explore/tests/check_notation.cjs`: passed; 2,702 authored equations checked with KaTeX, 0 errors.
- `git diff --check`: passed.
- Required staged content audit and manifest UUID/staged-path checks: passed.
