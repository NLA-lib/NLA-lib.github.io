# Luna research cohort 07 · part 8

Baseline revisions and declaration citation records were checked against `/tmp/nlalib-release-explorer/api/v1`; the assigned Lean sources were inspected. This is an editorial review report, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `a3ae6eab-cfd1-54a1-a5cb-aabb2ed528b6` (`shifted-qr-rounded-small-eig-backward-error`) | `c40e26f12e903225c7b8db767ecbcb0ec1cf7ea91095673e4da771a83820fcd2` | `needs-mathematical-review` |
| `bfa69b03-df3e-57c8-a9a5-dbb0ca6bab06` (`shifted-qr-rounded-small-eig-certificate-accuracy`) | `e1f6be38cff986459b7eb9751079fb6b3b1953e87365abbac079ca52d7e13049` | `needs-mathematical-review` |
| `96f14e8b-ee12-585f-a7a5-5142971ee656` (`small-eig-certificate-accuracy`) | `a007828cf7b37d55473cc086f89028741dd655ac13afdb7217a1e675d2173a0b` | `needs-mathematical-review` |
| `5122ab2d-9ad3-5c4d-a1d7-1ae5aed4b848` (`small-eig-forward-error`) | `c1ac6b120dcf1df555552d527950ca99f7b682dd1639eeccf86140dd5b298af6` | `needs-mathematical-review` |
| `c6b82b37-af7d-54c6-8a6e-3649062c1667` (`spectral-bisection-operation-count-accuracy`) | `c4445d5eb1f90eab73629d35f93772d6acd2f9190a1d078198337abb063cf349` | `needs-mathematical-review` |

## Changes and unresolved context

- Braced `\mathbb{P}` in `shifted-qr-rounded-small-eig-backward-error` and `small-eig-smalleig-measurereal-not-spectrum-le-unconditional`; braced `\mathbb{C}` and `\mathbb{P}` in `spectral-bisection-operation-count-accuracy`. No formulas, parameter ranges, matrix/vector roles, titles, IDs, bindings, or delimiter segmentation changed.
- `shifted-qr-rounded-small-eig-backward-error` depends on “the hypotheses above on $\mathbf{H}$, the machine and the tape.” The shared entry does not contain those hypotheses. The adjacent certificate entry similarly points to “the theorem above.” Both contexts are unresolved in the standalone sources; no machine, sampler, or error conditions were supplied.
- `small-eig-certificate-accuracy` refers to “Theorem 1.1.” Its inherited citation association is BanksGarzaVargasSrivastava2025, Theorem 1.1, but the shared body does not reproduce the assumptions needed for this certificate. The external locator is preserved; no theorem conditions were inferred.
- `small-eig-forward-error` relies on “the machine and the streams as above” and the “forward form” parameter words without identifying those shared hypotheses locally. No direct compatible definition target was established.
- `spectral-bisection-operation-count-accuracy` says the Lean statement gives the unit-roundoff, $β$, absolute-error-floor, and range conditions without stating those conditions in the shared text. This leaves the numerical assumptions needed for the guarantee unstated. They were not reconstructed from Lean.
- These Schur/small-eigenvalue results have distinct solver, tape, and output guarantees; no entries were treated as duplicates. No semantic link was added because the context phrases do not identify a precise compatible definition target.

## Actual inherited citations

The authored `object.references` arrays are empty. These associations were checked in declaration records; no front-matter references were added.

- `NLAlib.ShiftedQR.roundedShQRSmallEig_measureReal_not_spectrum_le_unconditional` — `BanksGarzaVargasSrivastava2022`, Theorem 6.3 (listed twice in `record.references`); `BanksGarzaVargasSrivastava2025`, Theorem 1.1 and Corollary 1.3.
- `NLAlib.ShiftedQR.roundedShQRSmallEig_algorithm_measureReal_not_accepts_le_unconditional` — `BanksGarzaVargasSrivastava2022`, Theorem 6.3 with Theorem 1.4's quantifiers, corrected.
- `NLAlib.SmallEig.smallEig_algorithm_measureReal_not_accepts_le_unconditional` — `BanksGarzaVargasSrivastava2025`, Theorem 1.1.
- `NLAlib.SmallEig.smallEig_measureReal_not_forward_le_unconditional` — `BanksGarzaVargasSrivastava2025`, Corollary 1.3.
- `NLAlib.SpectralBisection.measureReal_not_accepts_countedSpecification_le` — `Shah2024`, Theorem 4.2.

The shifted-QR spectrum statement also has `BanksGarzaVargasSrivastava2022`, Theorem 6.3 twice in its actual inherited record. This repeated pair was not duplicated in authored front matter.

## Registry proposals

No new symbol roles are proposed. The global registry was not changed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. No rendered browser preview was available.
