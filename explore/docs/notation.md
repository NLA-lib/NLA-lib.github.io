# Mathematical notation

Write the notation explicitly in Markdown. The renderer preserves the source:
capitalization does not imply a matrix, and lowercase letters do not imply vectors.

| Meaning | Source |
| --- | --- |
| Latin vector or matrix | `\mathbf{x}`, `\mathbf{A}` |
| Greek vector or matrix | `\boldsymbol{\omega}`, `\boldsymbol{\Omega}` |
| Transpose | `\mathbf{A}^{\mathsf{T}}` |
| Hermitian transpose | `\mathbf{A}^{\mathsf{H}}` |
| Scalar, dimension or index | `\alpha`, `n`, `k` |
| Scalar conjugation | `\overline{z}` or the convention explicitly stated by the author |

Use braces around font arguments. Keep subscripts and superscripts outside the bold
symbol, for example `\mathbf{x}_k`, rather than making the index bold. Do not
mechanically change every `*` into Hermitian transpose: scalar conjugation and
adjoints require mathematical context. Probability and expectation retain their
own fonts, such as `\mathbb{P}` and `\mathbb{E}`.

Supported math delimiters are `$…$`, `$$…$$`, `\(…\)` and `\[…\]`. Escape a literal
dollar as `\$`. Inline/fenced/indented code is kept literal. The same parser serves
rendering and the notation checker.

Run `node explore/tests/check_notation.cjs` from the repository root. It compiles
all authored math with the vendored browser KaTeX and checks source-level notation.
Both the test and deployment workflows run this check. It does not modify Lean
statements, validate the truth of a result, or infer variable types.

`explore/notation.json` declares reviewed vector and matrix symbols by source file.
These declarations make a bare declared symbol a blocking error. Initial scopes
cover the CG overview, its optimality statement, and quadrature overview; expand
this registry during content review. Unregistered documents still get delimiter,
brace and KaTeX syntax validation. Transpose style checks are suggestions because
`T` and `H` can also be scalar exponents. A reviewer resolves those cases.

The browser editor reports line-specific diagnostics and KaTeX errors, and checks
math again before saving a revision. The structured API rejects unclosed math,
unbalanced braces and violations of declared symbol roles. Drafts can remain
unfinished. Full KaTeX validation is a publication CI gate, including for agent
contributions; the Python API's structural check is not a complete TeX compiler.
Formal Lean statements remain upstream content. Readable prose initially generated
from Lean docstrings can acquire a shared frontend Markdown file through the editor,
keeping its UUID and Lean binding; this does not modify the Lean source.
