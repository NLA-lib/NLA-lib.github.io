---
kind: index
id: arithmetic-models
title: Arithmetic models
summary: Definitions of the arithmetic contracts used by the algorithm pages.
status: ready
---

An algorithm specifies which operations are performed. An arithmetic model specifies
what each operation may return. These choices are separate from the storage format,
matrix-access model, and resource charges.

The library states a model as hypotheses of a theorem or certificate: a property of the
scalar machine, and contracts for the vector and matrix operations that the program
calls. The pages mark a statement with the facts that its Lean signature or the
library's certificate record establishes, and [search](/explore/search/) filters on them.
A statement without a mark has no established fact; it is not thereby exact or
deterministic.

::: definition name="Exact arithmetic" id=exact
Every scalar operation of the machine returns the exact value: literals, addition,
subtraction, multiplication, division by a nonzero number, negation, and the square
root of a nonnegative number (`Ops.ExactModel`). In an exact operation model, dot
products, vector updates, and matrix–vector products are exact as well.

A correspondence theorem on an implementation page then identifies the stored output
with the mathematical method. For CG, the recurrence agrees with mathematical CG, so
classical convergence and finite-termination results apply under their matrix assumptions.
:::

::: definition name="Standard model of rounded arithmetic" id=standard
A scalar machine is in the standard model with unit roundoff $u$ (`Ops.StdModel`) when
each operation returns its exact result with relative error at most $u$:

$$|\widehat{a\circ b}-a\circ b|\le u\,|a\circ b|,\qquad\circ\in\{+,-,\times,/\},$$

with division only by a nonzero number, and likewise for literals and for the square
root of a nonnegative number. Negation is exact. There is no overflow and no underflow.
Exact arithmetic is the case $u=0$.

The model constrains the scalar operations only. A program whose only primitives are
scalar operations and comparisons, such as the stored scalar programs of CG and Lanczos,
needs nothing else. A program that calls vector or matrix operations also needs their
contracts, as in the next three definitions.
:::

::: definition name="Relative-error BLAS + matvec" id=relative
The implementation supplies error coefficients rather than a particular reduction
order. The dot-product contract is

$$|\widehat{\langle\mathbf{x},\mathbf{y}\rangle}-\langle\mathbf{x},\mathbf{y}\rangle|
\le d_n\sum_{i=1}^n |x_i y_i|.$$

This scales with the sum of absolute products, not with the absolute value of the
dot product; the distinction matters when there is cancellation.

A scaled vector addition satisfies

$$|\widehat z_i-(y_i+\alpha x_i)|\le e_a(|y_i|+|\alpha x_i|),$$

and matrix–vector multiplication satisfies

$$\|\widehat{\mathbf{A}\mathbf{v}}-\mathbf{A}\mathbf{v}\|_2
\le e_m\|\mathbf{A}\|_2\|\mathbf{v}\|_2.$$

The library's matrix–vector contract has an absolute allowance $\delta$ in place of
$e_m\|\mathbf{A}\|_2$; the CG theorems take $\delta=e_m\|\mathbf{A}\|_2$.

Scalar arithmetic has unit roundoff $u$. Copies and decoded comparisons are exact.
The solver theorem requires the supplied coefficients to satisfy its accuracy budget.
:::

::: definition name="Standard rounding with sequential BLAS" id=sequential
Scalar operations obey the standard relative-rounding model with unit roundoff $u$
and unbounded exponents. Dot products form rounded products and accumulate them
sequentially, giving

$$d_n=(1+u)^n-1.$$

The BLAS implementation supplies the vector-update bounds. All vector lengths are
admitted. Matvec error is supplied separately; this choice does not assume exact matvecs.
:::

::: definition name="Standard rounding with pairwise BLAS" id=pairwise
Scalar arithmetic has the same relative-rounding contract, while reductions use a
pairwise summation tree:

$$d_n=(1+u)^{\lceil\log_2 n\rceil+1}-1.$$

The implementation requires $\lceil\log_2 n\rceil<\mathrm{depth}$. Pairwise summation
specifies the reduction order; it does not by itself certify parallel execution.
Matvec error is supplied separately.
:::

::: definition name="Accuracy budgets" id=accuracy

For the abstract relative-error CG theorem, choose a nonnegative allowance $E$ with

$$u,d_n,e_a,e_m\le E\le10^{-2}.$$

The named standard profiles use a stricter envelope (`Ops.Standard.Accuracy`), which
the CG and Lanczos operation budgets share:

$$0\le E\le10^{-2},\qquad e_m,e_a\le E,\qquad
u,d_n,e_{\mathrm{scal}}\le E/16.$$

Here $e_{\mathrm{scal}}$ bounds componentwise vector division. Each solver theorem also
has its own assumptions, such as the spectral and iteration-window assumptions of CG,
stated on its implementation page.
:::

Access, randomness and work are not arithmetic. They are marked separately, and a
statement can carry several of these facts.

::: definition name="Uniform model and oracle" id=access
An operation model is uniform (`Ops.AccessModel.Uniform`) when the contracts of its
primitives and queries do not depend on the sizes or on the input. No primitive is then
an oracle for the problem data: the program reaches its input through the stored buffers.
A uniform model can still call kernels, which are primitives with their own contracts and
with work supplied by the caller.

A matrix–vector product that is a primitive with a contract for a given operator is an
oracle: the operator is semantic data of the model, not entries that the program reads.
:::

::: definition name="Random tape" id=randomness
A tape holds, at each position, one entry of each stream of draws. Under a tape law
(`Ops.IsTapeLaw`) all entries are independent, and an entry of a stream has the
distribution of that stream. A statement under a tape law is a statement about a
probability over the tape.
:::

::: definition name="Closed and manifest work" id=work
A certificate bounds the work and the span of its program. The bound is closed when it
does not mention the static count of a program, and manifest when it is stated through
the program's own syntax. A closed bound can still be a parameter that a hypothesis of
the certificate constrains.
:::

[Open ordinary CG](/explore/algorithms/conjugate-gradient/implementations/ordinary/)

[Open ordinary Lanczos](/explore/algorithms/lanczos/implementations/ordinary/)

[Computational-model theory](/explore/theory/computational-models/)
