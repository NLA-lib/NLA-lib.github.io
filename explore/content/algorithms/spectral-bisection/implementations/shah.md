---
kind: implementation
id: shah
algorithm: spectral-bisection
title: Randomized spectral bisection
summary: Shah's Hermitian eigensolver with stored-word arithmetic, explicit random draws, and certified resources.
status: ready
order: 0
source_guides:
- docs/algorithms/Spectral-Bisection.md
---

Diagonalize a stored Hermitian matrix $\mathbf A\in\mathbb C^{n\times n}$ by splitting its spectrum, solving the smaller problems, and assembling a basis $\mathbf U$ and real values $\mathbf d$. This implementation follows Shah's randomized spectral-bisection method.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.SpectralBisection.program name="Stored spectral bisection" id=algorithm
Supply a radius bound $R_0$, tolerance $\varepsilon$, precision parameter $\beta$, depth budget $L$, sign-iteration cap $c$, and a random tape. Store complex entries as adjacent real and imaginary words.

1. Store the root matrix and parameters in the root arena.
2. At each downward level, draw $n$ uniform words and $4n^2$ Gaussian words.
3. For each active node, read its matrix $\mathbf A$, radius $R$, tolerance, and depth counter $\ell$.
4. For a singleton, store the identity basis and its real diagonal value.
5. For a sufficiently small spectral window, store the identity basis and zero values.
6. Otherwise, choose a sampled shift of scale $R/\ell$.
7. Apply capped Newton–Schulz sign iteration to the shifted matrix, obtaining $\mathbf B$.
8. Form $\mathbf P_+=(\mathbf B+\mathbf I)/2$ and $\mathbf P_-=-(\mathbf B-\mathbf I)/2$.
9. Estimate the positive rank by rounding the computed trace of $\mathbf P_+$ and clamping it to the node dimension.
10. If the rank is zero or the full dimension, store the corresponding shifted child.
11. Otherwise, project Gaussian samples and apply QR to obtain $\mathbf Q_+$ and $\mathbf Q_-$.
12. Compress the node matrix onto these bases and store the two shifted children.
13. At the depth boundary, store identity bases and zero values.
14. Traverse upward, combining child bases and restoring the eigenvalue shifts.
15. Copy the root basis and values to the output buffers, then release scratch storage.

Each instruction uses the supplied arithmetic. In particular, one-half and the trace are computed with word operations. Reaching an iteration or depth cap produces a defined output; accuracy needs the assumptions below.
:::

## Model of arithmetic

The dense word model supplies scalar arithmetic and decoding, matrix multiplication, full QR, comparisons, bounded integer conversions, and explicit random draws. Scalar transformations, copies, control flow, and allocation are counted separately. This is a parameterized arithmetic model; a concrete floating-point format must establish the primitive accuracy and range assumptions.

Matrix multiplication and QR have supplied work and workspace costs. The bounds below count abstract scalar cells, rather than bytes. Complex matrix entries occupy two cells.

## Operations and Storage

Write $T(k)$ for a monotone, superadditive bound on a matrix primitive whose largest dimension is $k$. Require this bound for every primitive shape, including zero dimensions. Let $\mathcal{H}(n,L,c)$ denote the static program budget with matrix-kernel work set to zero: it includes scalar arithmetic, sampling, literals, queries, addressing, control flow, frames, and allocation.

::: theorem decl:NLAlib.SpectralBisection.certifies_work name="Work and sequential span" id=work
For $n\ge2$, with exact decoding of natural literals through $\max(n,4)$ and the stated primitive cost contracts, both total work and sequential span are at most

$$\mathcal{H}(n,L,c)+(L+1)(2c+11)T(n).$$

At a node of dimension $k$, splitting costs at most $(2c+9)T(k)$ in matrix work and reconstruction at most $2T(k)$. Disjoint node slots and superadditivity bound their sum at each level by the root-size term. The scalar budget $\mathcal{H}$ remains conservative.
:::

Let $E(n)$ be the maximum workspace cost of multiplication and QR over all call dimensions at most $n$; no monotonicity of workspace is required.

::: theorem decl:NLAlib.SpectralBisection.staticPeak_workspaceEnvelope_le name="Scratch storage" id=scratch
For $n\ge2$, peak scratch capacity is at most

$$6n^2L+32n^2+4nL+7n+2L+24+E(n).$$

The bound includes the arenas and nested scratch allocations. It is independent of the sign-iteration cap $c$.
:::

::: theorem decl:NLAlib.SpectralBisection.initialBytes_add_staticPeak_workspaceEnvelope_le name="Resident storage" id=resident
For $n\ge2$, including the supplied input, parameter, and output buffers, total resident capacity is at most

$$6n^2L+36n^2+4nL+8n+2L+27+E(n).$$

The supplied buffers contribute $4n^2+n+3$ cells.
:::

## Accuracy

::: theorem decl:NLAlib.SpectralBisection.writes_solve name="Execution agrees with the word algorithm" id=execution
Under the primitive contracts, readable inputs, sufficient separated output capacity, and exact bounded dimension literals, the solver terminates and stores exactly the basis and values returned by the mathematical word algorithm with the same arithmetic and random tape. It consumes exactly

$$(L+1)(n+4n^2)$$

random words and releases its scoped scratch storage. This correspondence does not require a numerical-success assumption.
:::

::: theorem decl:NLAlib.SpectralBisection.measureReal_not_accepts_le_of_wordSpecification name="Accuracy transfers to the stored output" id=accuracy
Suppose the numerical reference returns an approximate diagonalization with error parameters $\eta=2\varepsilon R_0$ and $\kappa=\varepsilon/3$, except on a tape event of probability at most $\theta$. For a probability tape law, the certified execution satisfies its functional and resource specification and stores $\mathbf U,\mathbf d$ with

$$\|\mathbf A-\mathbf U\operatorname{diag}(\mathbf d)\mathbf U^{\mathsf{H}}\|_2\le 2\varepsilon R_0,$$

$$(1-\varepsilon/3)^2\mathbf I\preceq\mathbf U^{\mathsf{H}}\mathbf U\preceq(1+\varepsilon/3)^2\mathbf I,$$

with probability at least $1-\theta$. Here the matrices and parameters denote decoded stored words.

The failure event includes execution failure, any resource-bound violation, and incorrect numerical output. Establishing the reference premise separately requires Hermitian input, a valid radius bound, sufficient precision, depth and sign-iteration cap, and the stated sampler and tape-law assumptions. This transfer theorem does not by itself establish those numerical hypotheses.
:::

## Mathematical method

{{ generated:mathematical-method }}
