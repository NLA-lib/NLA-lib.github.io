# Luna research cohort 07 · part 7

Baseline revisions and declaration references were checked against `/tmp/nlalib-release-explorer/api/v1`; the linked Lean sources were inspected. This is an editorial review report, not a theorem or proof audit.

| UUID / entry | Baseline revision | Outcome |
| --- | --- | --- |
| `d800ebd7-32d8-5630-95fe-390e2cf2603b` (`nlalib-ops-machine-eigh-tofloatmachine-map-samples`) | `494fd593cd7a42bce2ddcf4fbe7f0418b9120238b7f318fd4d0313816819a3c2` | `already-consistent` |
| `be09b239-c7ce-55b7-b6cf-fefa3c51abe2` (`nlalib-refinementrun-norm-sub-x-succ-le`) | `dd4f0cfb868228e7bfb1d1129e5628321ec61023710abfdfceb0718627aa395f` | `needs-mathematical-review` |
| `35b1d0b4-eb55-5a94-a77d-b2ae5486ab56` (`nlalib-schur-denseschur-terminates`) | `f55a79290defdecb7d9bf974ce78377cae72697943bfcf34e1ea944db51992b6` | `needs-mathematical-review` |
| `92fb9508-4283-5233-8460-928bf7187ea8` (`nlalib-schur-schurpipelinewith-measurereal-not-schur-le`) | `cdb4d076b734e678ccd37163faeb52fe5bee3b241067aa2376c13e7998de9a0b` | `needs-mathematical-review` |
| `d695353d-56d2-5d1a-8f96-0d7943757d1e` (`nlalib-schur-verifiedschurwith-measurereal-not-flag-le`) | `fdea5a91d9fa2fa4697140ba34378f0a7796710148be3d8850ae7cd805fc8636` | `needs-mathematical-review` |

## Review findings

All five entries already use consistent role-aware fonts and transpose notation. No formula, hypothesis, title, UUID, binding, or delimiter segmentation was changed. No definition target was verified that would clarify the context without implying unstated assumptions.

- `nlalib-ops-machine-eigh-tofloatmachine-map-samples`: notation and wording are self-contained enough for this result; no edit needed.
- `nlalib-refinementrun-norm-sub-x-succ-le`: “with $\varphi$ and $\xi$ as above” leaves both quantities undefined in this shared body. The nearby definition of `RefinementRun` gives iteration contracts but not these two parameters. A different iterative-refinement theorem defines similar quantities under different assumptions, so it is not a safe substitute. Please define the intended parameters or identify the exact context before revising.
- `nlalib-schur-denseschur-terminates`: “On the same machine” points outside the shared body. The entry does not identify the machine setup to which it refers. Do not infer it from a nearby dense-Schur theorem without confirming that identity.
- `nlalib-schur-schurpipelinewith-measurereal-not-schur-le`: the theorem is explicitly a composition under stage contracts, but the shared body does not state the contents of the norm-estimate, regularizer, reducer, or Schur-core contracts. Those are formal inputs to the theorem; no conditions were invented or expanded.
- `nlalib-schur-verifiedschurwith-measurereal-not-flag-le`: “On that machine” likewise depends on external context. The solver contract is described abstractly, and no exact machine definition is named here. A reviewer should identify the intended machine and contract entry before proposing links or prose changes.

## Actual inherited citations

The authored `object.references` arrays and linked declaration `record.references` are empty for all five entries. No citations were added or moved.

- `NLAlib.Ops.Machine.eigh_toFloatMachine_map_samples` — none.
- `NLAlib.RefinementRun.norm_sub_x_succ_le` — none.
- `NLAlib.Schur.denseSchur_terminates` — none.
- `NLAlib.Schur.schurPipelineWith_measureReal_not_schur_le` — none.
- `NLAlib.Schur.verifiedSchurWith_measureReal_not_flag_le` — none.

## Registry proposals

No notation registry changes are proposed.

## Validation and limitations

`node explore/tests/check_notation.cjs` passed: 2,290 authored equations checked with KaTeX, 0 errors. `git diff --check` passed. These checks do not establish theorem correctness or formal/readable equivalence. No rendered browser preview was available.
