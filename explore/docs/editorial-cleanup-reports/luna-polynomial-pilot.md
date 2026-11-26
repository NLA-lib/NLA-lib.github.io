# Luna polynomial pilot cleanup

This is a bounded editorial proposal for four authored shared definitions. The
baseline revision tokens and source paths below come from the pinned Explorer
editor object snapshots under `/tmp/nlalib-release-explorer/api/v1/editor/objects/`.
The snapshot reports match the working files before this edit. No proposal was
submitted through the API; this report accompanies the local Git change.

## Per-UUID outcomes

### `e7470c95-5c37-5fa0-94b3-ee795973f79d` — Chebyshev polynomials

- Baseline revision: `8e6bf2b41056bd4466b24e5084f2d3894ca8de37b2b7b740360f82978325e9c5`.
- Source: `explore/content/statements/chebyshev-polynomials-e7470c95.md`.
- Outcome: `already-consistent`.
- The scalar polynomial symbols `$T_k$` and `$t$` and scalar index `k` correctly remain unbolded. There is no matrix transpose in this definition. No bibliographic citation string is present in the prose. The pinned editor snapshot reports `references: []`; inherited citations on any underlying Lean declaration were not independently verified, so none are asserted here. No reference section was added. No link was added: a self-link to this definition would be redundant, and the remaining prose does not name a separate existing definition.
- Unresolved: “an affine change of variable transfers constructions” and “the normalization appropriate to the linear system” do not specify a particular construction or normalization. They are retained without elaboration. The latter is a broad contextual observation, not a complete mathematical definition.

### `89ab2263-0730-583c-89db-9695bea9604d` — Best uniform polynomial error

- Baseline revision: `4ffbe253e5bf9bcd10aa3432e8d915b95bcdb69015c8185b71e5c4b800853761`.
- Source: `explore/content/statements/best-uniform-polynomial-error-89ab2263.md`.
- Outcome: `needs-mathematical-review`.
- `$f,S,p,k,t$` are scalar/function/set/polynomial/index roles and are not bolded. No bibliographic citation string is present in the prose. The pinned editor snapshot reports `references: []`; inherited citations on any underlying Lean declaration were not independently verified, so none are asserted here. No reference section was added. No definition link was added because the text does not name a distinct definition target; linking to the minimax theory page would not link a definition.
- Needs mathematical review: the scalar field and polynomial class are unstated; the set `S` is called compact but its ambient space is not given. “Under the corresponding hypotheses” does not state the hypotheses for equioscillation. These gaps are preserved rather than filled in. The source does not establish which equioscillation theorem is intended.

### `f61d2bf5-061a-55af-a609-10a7bc9d86f5` — Orthogonal polynomials and quadrature rules

- Baseline revision: `167e1339868db227d15845d46d269ea1d6d4f7997123764db1276836ca30e15c`.
- Source: `explore/content/statements/orthogonal-polynomials-and-quadrature-rules-f61d2bf5.md`.
- Outcome: `needs-mathematical-review`.
- The scalar polynomial variables, measure, nodes, weights, and indices are correctly not bolded; there are no matrix objects or transposes. No bibliographic citation string is present in the prose. The pinned editor snapshot reports `references: []`; inherited citations on any underlying Lean declaration were not independently verified, so none are asserted here. No reference section was added. No link was added: this is the canonical authored overview definition in the selected material, and no separate, sufficiently matching definition target was verified.
- Review issue: “with the required finite moments” leaves the moment order and measure domain unspecified. The quadrature description does not state the node/weight constraints or the exactness degree; those depend on each rule and on omitted hypotheses. The sentence acknowledges that exactness and error claims need their own hypotheses. Preserve as overview pending a more precise intended scope; do not infer one from a particular Gauss-type theorem.

### `057c76ad-28a7-5db1-b52a-2f9658bc0136` — Evaluating a polynomial on a matrix

- Baseline revision: `cdd7689bf59b032c06c9143c1448fb8cdaddc0b2da688e16497c6ae0535c2633`.
- Source: `explore/content/statements/evaluating-a-polynomial-on-a-matrix-057c76ad.md`.
- Outcome: `proposed`.
- Added an ordinary Markdown link on “functional calculus” to [Hermitian functional calculus](/explore/statements/af61ef21-9f45-5d71-87c8-6d01c16be15e/). Its target definition verifies the Hermitian scope used by this occurrence. No link was added for “Krylov space”: the available [Krylov space and grade](/explore/statements/615008ca-f5db-5cff-ab6b-b07f178cbd05/) definition is explicitly for real square matrices and real vectors, while this statement leaves the scalar field and dimensions unspecified.
- Notation is object-aware already: `A` is bold as a matrix, `b` as a vector, and `p,t,c_j,k` remain scalar/polynomial/index roles. No transpose is used. No bibliographic citation string is present in the prose. The pinned editor snapshot reports `references: []`; inherited citations on any underlying Lean declaration were not independently verified, so none are asserted here. No reference section was added.
- Review issue: the source does not state the scalar field, dimensions, or square-matrix assumption for the polynomial evaluation sentence. The available Krylov definition specifically states a real square matrix and real vector, so it is not a safe link target while this statement’s field and dimensions remain unspecified. “A vector in the Krylov space” is also convention-dependent in its index: for degree at most `k`, the powers through `A^k b` fit `K_{k+1}` under the available target’s convention. The source does not state which index is intended. Keep both issues open; no link or wording change resolves them.

## References and notation registry

The pinned editor snapshots for all four objects report `references: []`, and the statement bodies contain no bibliographic citation strings. This is not evidence that any underlying Lean declaration lacks inherited citations; those associations were not independently verified. No reference keys or locators were added. Their prose contains no `T`/`H` transpose notation; `$T_k$` is a scalar polynomial and must not be registered as a matrix. No new symbol-role registry entry is proposed for these four files.

The only verified definition link added is `/explore/statements/af61ef21-9f45-5d71-87c8-6d01c16be15e/` — Hermitian functional calculus. The real-valued Krylov definition at `/explore/statements/615008ca-f5db-5cff-ab6b-b07f178cbd05/` was inspected but not linked because its scope does not resolve the statement’s unspecified field and dimensions.

No other files were edited by this batch. No preview/build or API proposal was run. Validation: `node explore/tests/check_notation.cjs` passed (2,290 authored equations checked with KaTeX; 0 errors). This checks notation/parser rules, not mathematical correctness or agreement with Lean.
