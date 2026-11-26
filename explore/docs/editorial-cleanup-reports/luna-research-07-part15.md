# Luna research cohort 07, part 15

Scope: manifest `research[14]` in `/tmp/nla-luna-cohort-07.json`; exactly five assigned statements reviewed. This editorial review does not certify the mathematical claims or formal correspondence.

| UUID | Source path | Baseline revision | Outcome | Editorial changes | Inherited key/locator pairs |
| --- | --- | --- | --- | --- | --- |
| `30e238be-e5c3-513a-93a0-69c47b1b537c` | `explore/content/statements/srht-flattening.md` | `052956f77674db5c923be30495a68a1dc293ad5c434759fe2d1b5161a2a1d998` | `already-consistent` | No source edits; existing matrix fonts are clear. | `CamanoEpperlyMeyerTropp2025`, Imported Theorem 4.3; `Tropp2011a`, Lemma 3.3 |
| `d5c04cd3-1440-51a5-afad-18cf3acb4fa8` | `explore/content/statements/three-precision-iterative-refinement.md` | `0089270a99553a79f19242be3956ea94bcc7946cbccb6fde8dca88c8b6625ec3` | `needs-mathematical-review` | No source edits. | `CarsonHigham2018`, Corollary 3.3 |
| `fddf9c5b-4258-5153-a554-e27c7168cb23` | `explore/content/statements/truncated-gn-lower-bound.md` | `27c4ecdbd912a65b8e6c645d63c5a1e943f4542629e06120cbfb1ce09d4afd9d` | `proposed` | Replaced unbraced `\\mathbf\\Omega` and `\\mathbf\\Psi` with explicit `\\boldsymbol{\\Omega}` and `\\boldsymbol{\\Psi}` notation. | None in linked declaration record |
| `c1ff4d2f-9c6b-5435-9fac-c5ae60632af3` | `explore/content/statements/verified-schur-certificate.md` | `fc4e72a22ba4234b8eeedbd42be50f7eb99e58f747eb1e27e8624901e1dcac7e` | `needs-mathematical-review` | No source edits. | `BanksGarzaVargasSrivastava2022`, Theorem 1.4; `BanksGarzaVargasSrivastava2025`, Theorem 1.1 |
| `ba50b7b7-4199-5605-8b73-6702f764b5c4` | `explore/content/statements/verified-schur-every-tape.md` | `ede962252c317eec0e1f8f2c59f5df07204927277224f6b32ebe3b8f4b702b87` | `needs-mathematical-review` | No source edits. | None in linked declaration record |

## Evidence and unresolved issues

- Inherited citations were read by following each editor object's `evidence.declaration` to the declaration record's `references`. The exact pairs are listed above; no reference front matter was added.
- `three-precision-iterative-refinement` says the run meets an “instruction bound above,” but that bound is absent from the statement itself. The linked declaration is `NLAlib.LinearSystems.Refinement.Rounded.Certification.algorithm_checked`; clarify the intended bound and context before editing. The formula and assumptions were left intact.
- `truncated-gn-lower-bound` describes independent standard Gaussian sketches but does not specify their dimensions or fields in the readable statement. The pinned source is `NLAlib/LowerBounds/LowRank/TruncatedGeneralizedNystrom.lean`, declaration `eventually_le_integral_frobNorm_sub_truncatedSVD_generalizedNystrom_fromBlocks_sq`. Verify the exact sketch domains before adding them. The lower bound is for a specific input family, as the statement says.
- `verified-schur-certificate` refers to “the hypotheses of the failure bound” without identifying that theorem or restating its hypotheses. It also refers to a Schur output without giving a formal definition link. Verify the failure-bound target before changing the prose.
- `verified-schur-every-tape` depends on “the machine as above,” leaves `\\varphi` unconstrained, and uses `\\delta_{\\mathrm{int}}` without defining it in the statement. Review these context dependencies; no conditions or interpretations were invented.
- No direct, scope-compatible definition links were verified for the named algorithms or their certificates. No links or symbol-role registry additions were proposed.
- No formulas, assumptions, delimiter segmentation, titles, bindings, IDs or metadata changed. Only the two Greek matrix symbols in `truncated-gn-lower-bound.md` changed font.

## Validation

- `node explore/tests/check_notation.cjs`: passed (2,290 equations; 0 errors).
- `git diff --check`: passed.
- Required staged content audit: passed ID, front-matter, kind, binding, title and target-ID checks. It reports 82 statement files changed in branch history; the only mathematical-fragment discrepancy needing explicit review is the pre-existing `markov-inequality.md` change, and the only added reference metadata is the earlier `cg-chebyshev-bound.md` association. Neither is part of this batch. The edited lower-bound statement is not flagged.
- Preview/rendering was not run in this local source-only review.
