# How NLAlib defines things

A theorem checked by a computer leaves nothing to the reader. Before a bound on the randomized SVD can be stated, the library has to fix what a matrix is, what the algorithm returns, what a random test matrix is and what "$O(k/\varepsilon)$ samples suffice" quantifies over. Statements about cost need a model of computation as well, and that is where most of the subtleties are. This page explains the choices NLAlib makes and why; the rules themselves are in the repository.

## How a result is stated

**Matrices.** A matrix is Mathlib's `Matrix m n 𝕜`: rows and columns indexed by arbitrary finite types, entries in $\mathbb{R}$ or $\mathbb{C}$. Results are stated once for both fields wherever the proof allows.

**Total definitions.** Every definition has a value at every input, and the value in degenerate cases is documented: the pseudoinverse of the zero matrix is zero, the inverse of a singular matrix is zero, `eigenvalue A k` is $0$ for $k$ beyond the dimension. A theorem that needs nondegeneracy states it as a hypothesis, and one whose proof does not need it is stated without it, instead of every statement and every use carrying side conditions. The price is that a statement can be true only because of the padding ("some eigenvalue of $\mathbf{A}$ exceeds $-3$" holds for every matrix), so quantified indices carry their range.

**Algorithms are the object they compute.** An algorithm is defined by its output as a mathematical object, not by pseudocode. The randomized SVD with test matrix $\mathbf{\Omega}$ is the projection of $\mathbf{A}$ onto the range of the sketch, with no choice of orthonormal basis (`rsvd`):

$$\mathsf{rsvd}(\mathbf{A},\mathbf{\Omega}) := \mathbf{P}_{\mathbf{A}\mathbf{\Omega}}\mathbf{A}.$$

The conjugate gradient iterate after $q$ steps is the Galerkin solution on the Krylov space $\mathcal{K}_q(\mathbf{A}, \mathbf{r}_0)$ (`cgIterate`); that the Hestenes–Stiefel recurrence produces it for positive definite $\mathbf{A}$ is a theorem (`Matrix.PosDef.cgState_x_eq`). Hutch++ is the trace of a randomized SVD plus a Girard–Hutchinson estimate on the complement (`hutchpp`). A theorem saying that a procedure computes the object is a realisation theorem. Error bounds are proved about the object, so they hold for every implementation a realisation theorem covers, whichever orthonormalisation it uses.

**Randomness.** A random test matrix is a measurable map from a probability space to matrices, with a hypothesis on its law: Gaussian, Haar, a sparse sign sketch. An expected error is an integral and a tail bound is the probability of an event. A theorem that needs only a property of the sketch, such as being a subspace embedding, takes that property as its hypothesis, so it applies to every sketch that has it.

**Constants.** Bounds carry explicit constants. When the literature says that $O(k/\varepsilon)$ samples suffice, the library proves the explicit bound and derives a corollary of the form

$$\exists\, C, \varepsilon_0 > 0 \;\; \forall\, m, n, \mathbf{A}, \mathbf{\Omega}, \varepsilon \in (0, \varepsilon_0] : \quad \ell \ge C k/\varepsilon \implies \text{bound}.$$

The constant comes before every dimension ($m$ and $n$ here), so it is genuinely absolute; a factor such as $\log n$ appears in the threshold, never inside $C$. These corollaries are the rows of the [Rates page](../rates/).

## Why a model of computation is subtle

Statements about cost, such as "the randomized SVD needs two passes over $\mathbf{A}$" or "CG terminates in at most $n$ steps", need a model of computation, and informal arguments are often loose here.

- **What is an operation?** Is a square root one operation? A comparison? An orthonormal basis? If "compute an SVD" were a single step, every low-rank approximation problem would cost one operation. A model must fix a small set of primitive operations and build the rest from them.
- **Exact real arithmetic is an idealisation.** It is the usual setting for flop counts and for CG's finite termination. But one real number can hold unbounded information: its digits could store a whole matrix, or a table of answers. A model allowing arbitrary operations on reals, such as extracting a digit, could hide all the work inside one number, so exact models must restrict the operations.
- **Finite precision is not exact arithmetic with a small error.** The model $\mathrm{fl}(a \circ b) = (a \circ b)(1+\delta)$ with $|\delta| \le u$ is a proof tool, and exact arithmetic satisfies it for every $u$, so "$u > 0$" does not define floating point. Nor is exact arithmetic a format with unlimited parameters: unbounded binary significands give the dyadic rationals, which miss $1/3$ and $\sqrt{2}$. Exact and rounded arithmetic are separate interpretations of the same program.
- **Exact and rounded runs can take different paths.** Started at $x = 2$, the loop "replace $x$ by $(1+x)/2$ until $x = 1$" never stops in exact arithmetic, since $x - 1$ only halves; in double precision it stops after 53 steps. CG terminates in at most $n$ steps in exact arithmetic and in general not in floating point. A theorem about one kind of run says nothing about the other.
- **Uncounted work.** A count of matrix-vector products means something only if the algorithm cannot do other work for free. In a proof assistant this is a real risk: a Lean function can compute anything, including the answer, and a wrapper that counts operations charges only what it is told to. Memory, random number generation and reading the matrix are also easy to leave out.
- **Breakdown.** Lanczos divides by $\beta_j$, Gram–Schmidt by a norm, Cholesky by its pivots. Breakdown has to be ruled out under the stated hypotheses: "if it succeeds, the output is accurate" is weaker than "it succeeds, and the output is accurate".
- **Access to the matrix.** Krylov and randomized methods often see $\mathbf{A}$ only through products $\mathbf{x} \mapsto \mathbf{A}\mathbf{x}$. The natural costs are the number of products and of passes over the matrix: a block product $\mathbf{A}\mathbf{X}$ with $\ell$ columns is $\ell$ matvecs but one pass, or load. The price of a product depends on how $\mathbf{A}$ is stored (about $n^2$ dense, $\mathrm{nnz}(\mathbf{A})$ sparse, less for fast transforms), so a reusable theorem counts products and leaves their price to the representation.

## How NLAlib handles it

The results in the library today are about the mathematical objects that algorithms compute, not the cost of computing them; the resources on the Rates page (sketch size, block size, depth) are parameters of these objects. A program layer for cost statements was designed and approved by the maintainer on 2026-10-23. Its implementation is starting and is not yet in the library. The plan:

- **The mathematical definitions stay the specifications.** Nothing that exists changes; a program is connected to its definition by a realisation theorem.
- **Algorithms become programs in a small language over allocated memory**, written as BLAS code is: they allocate buffers, overwrite them in place, call kernels such as dot products and axpy, and draw random numbers. A program holds no number outside its counted memory and cannot call arbitrary Lean functions, so there is nowhere to do uncounted work.
- **An exact interpretation comes first.** Running a program gives its output and a separate count for each kind of operation: additions, multiplications, divisions and square roots each on their own, comparisons (the only way to branch on a value), loads and matvecs, random draws, and current and peak memory. Flops and weighted costs are computed from these counts. Division by zero makes the run fail in exact arithmetic too, so theorems must rule out breakdown.
- **The program sees the matrix only through products.** One composition theorem, proved once, says that replacing the product by an implementation (dense, or sparse in coordinate form) gives the same output, with each matvec charged at that implementation's cost. Dense and sparse costs are then corollaries of the matvec count.
- **Later stages** add floating-point formats through error contracts, such as a relative error per operation, stated separately from the formats, and reduce costs to bit-level operations by the same kind of substitution.
- **Programs print as NumPy** for testing against standard implementations. This translation is not verified.

The first targets are Hutch++ and Lanczos. For Hutch++ the statement is to read: the exact run of the program returns `hutchpp` of the test matrices it drew, with two loads and stated numbers of matvecs, draws, other operations and memory cells. The existing error bounds for `hutchpp` then carry over to the program with no new probability.

## Where to read more

- [CONTRIBUTING.md](https://github.com/NLA-lib/nlalib/blob/main/CONTRIBUTING.md) is the library's contract: representation, total definitions, statement shapes, randomness, constants and asymptotic forms (§5), and the checks that enforce them.
- [docs/design/Computation.md](https://github.com/NLA-lib/nlalib/blob/main/docs/design/Computation.md) will hold the design of the program layer; it is added to the repository with the implementation.
- The [explorer](../) has the definitions and theorems named on this page, with their statements and sources.
