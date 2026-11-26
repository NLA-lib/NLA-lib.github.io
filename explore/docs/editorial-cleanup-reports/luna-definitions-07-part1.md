# Luna matrix definitions cohort 07, part 1

This report covers the five assigned authored definitions. Baseline revisions and editor metadata were checked in the pinned Explorer objects. All five objects have empty `object.references`, `reference_links: null`, and authored-definition evidence with no linked declaration; consequently none has inherited declaration citations.

| UUID | Source path | Baseline revision | Outcome |
| --- | --- | --- | --- |
| `888a2fcc-0197-5aa6-9225-514a3ae6ef32` | `explore/content/statements/richardson-iteration-888a2fcc.md` | `7a559a7550ec843ff0db9274960c8c07c131e6ba62f8378b1ccc9a8f3fe68bcb` | `already-consistent` |
| `cf917bf1-5d3f-5f8e-8e46-bf4041fd5e43` | `explore/content/statements/shifted-qr-step-cf917bf1.md` | `4e90b64fcc97c9367f5e69216af985d8bc8c51da9ca54fbf38c87a0697cd4e24` | `already-consistent` |
| `b2f1a8ae-a178-59b9-93a3-cb761460b941` | `explore/content/statements/sketch-and-precondition-least-squares-b2f1a8ae.md` | `588be8d66f990b3ad75bf8989206c074b43c1a7bc60878c3c775400c527f7beb` | `proposed` |
| `45ab3f30-a374-55c2-b6f8-93d5c611f4aa` | `explore/content/statements/sketch-and-project-45ab3f30.md` | `7d175d6926af963f9a5cdb079f2e0048d2b2e291cbf7d9959a455da1f140c905` | `already-consistent` |
| `64e42acf-32bf-5004-ae5f-88afdd26ea97` | `explore/content/statements/stochastic-lanczos-quadrature-64e42acf.md` | `5126310937a70b41ce16ebe254b2886cff5ff97fcda308f4804302b1802a9fe8` | `already-consistent` |

## Links and scope findings

- **Sketch-and-precondition least squares**: linked the existing noun phrase “thin QR factorization” to QR factorization, UUID `adb72f11-3503-58f9-89c4-98a60c4f7a40`. The target defines thin QR for complex rectangular matrices with `m\ge n`; the source already names a thin factorization and requires invertible `\mathbf{R}`. The formula and conditions are unchanged.
- **Stochastic Lanczos quadrature**: no definition link was added. The existing Lanczos quadrature definition requires a nonzero starting vector, while this source states only that it uses random probes. The isotropic-probes definition explicitly begins with a square-integrable probe, a condition not stated here. These are potentially relevant targets but do not match the source's stated conditions exactly; no assumptions were added.
- **Richardson iteration, shifted QR step, and sketch-and-project**: already consistent for the requested scope. No direct definition link or inline citation was identified. Existing update formulas and distinctions remain unchanged.

## Citation audit

All five editor objects have empty authored `object.references`, `reference_links: null`, and no declaration evidence, so no inherited declaration citations apply. No inline bibliographic strings occur in these definitions. No citation associations were moved or added.

## Validation and limitations

Verified the QR target's UUID and domain. The stochastic quadrature definition-scope mismatch remains unresolved and is reported rather than strengthened. IDs, titles, formulas, conditions, metadata, and math-environment segmentation are unchanged.

`node explore/tests/check_notation.cjs`: passed, 2,291 authored equations checked with KaTeX and 0 errors. `git diff --check`: passed. No rendered preview was run; these checks do not establish mathematical correctness, link preview behavior, or formalization correspondence.
