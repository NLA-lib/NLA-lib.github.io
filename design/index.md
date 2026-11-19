---
title: How NLA-lib defines things
description: A short overview of the key design decisions in NLA-lib.
tab-title: NLA-lib · Design
menu:
  - Home: ../
  - Explorer: ../explore/
  - Design: ./
  - GitHub: https://github.com/NLA-lib/nlalib
---

NLA-lib aims to serve as a foundation for the formalization of new and existing numerical linear algebra results.

Some results in NLA are foundational and straightforward to state formally, but do not appear in existing libraries such as `Mathlib`.
This includes things like the Weyl's inequalities, Cauchy interlacing, the Eckart–Young theorem, the Moore–Penrose pseudoinverse, Jackson's theorem, etc.
For such results, the main benefit of NLA-lib is that it helps people avoid repeatedly proving the same thing for their own work, but it would be appropriate to upstream many of these results to `Mathlib`.

On the other hand, many results in NLA are much blurrier. 
For example, there are many slightly different statements describing how Gaussian matrices give an oblivious subspace embedding.
Moreover, many natural language results in NLA are stated with implicit definitions, quantification, integrability assumptions (e.g. when using Markov’s inequality), orders of limits, etc.
While a standardized library of formalized math can help simplify and clarify the landscape some, the nature of the field means that there are no single "canonical" statements of many results.


## Algorithms

The main benefit of NLA-lib is in facilitate the formal verification of statements about algorithms.
We aim to justify the value of such a library in what follows.

### Mathematical quantities 

Lots of the analyses of algorithms in NLA are essentially proving things about of simple mathematical objects. 
For example, we can define the conjugate gradient method (CG) for solving $\mathbf{A}\mathbf{x} = \mathbf{b}$ with $\mathbf{A}$ positive definite mathematically as a certain minimizer.

::: definition
**Def.**
Let $\mathbf{A}\in\mathbb{R}^{n\times n}$ be positive definite and $\mathbf{b}, \mathbf{x}_0\in\mathbb{R}^n$.
Define $\mathbf{x}_\star = \mathbf{A}^{-1}\mathbf{b}$ and $\mathbf{r}_0 = \mathbf{b} - \mathbf{A}\mathbf{x}_0$.
The $k$-th CG iterate is
$$
\mathbf{x}_k := \argmin_{\mathbf{x} \in \mathbf{x}_0 + \mathcal{K}_k(\mathbf{A}, \mathbf{r}_0)} \|\mathbf{x}_\star - \mathbf{x}\|_{\mathbf{A}},
\qquad
\mathcal{K}_k(\mathbf{A}, \mathbf{r}_0) := \operatorname{span}\{\mathbf{r}_0, \mathbf{A}\mathbf{r}_0, \ldots, \mathbf{A}^{k-1}\mathbf{r}_0\}.
$$

:::

From this definition we can prove theorems such as classical condition number convergence bound for CG:

::: theorem
**Theorem.**
The CG iterates satisfy
$$
\frac{\|\mathbf{x}_\star - \mathbf{x}_k\|_{\mathbf{A}}}{\|\mathbf{x}_\star - \mathbf{x}_0\|_{\mathbf{A}}}
\le 2 \left( \frac{\sqrt{\kappa} - 1}{\sqrt{\kappa} + 1} \right)^k,
$$
where $\kappa = \lambda_{\max}(\mathbf{A}) / \lambda_{\min}(\mathbf{A})$ is the condition number of $\mathbf{A}$.

:::

Many other algorithms in NLA are analyzed in the same way.
For example, the randomized SVD of $\mathbf{A}$ with test matrix $\mathbf{\Omega}$ is the matrix $\mathbf{P}_{\mathbf{A}\mathbf{\Omega}}\mathbf{A}$, where $\mathbf{P}_{\mathbf{A}\mathbf{\Omega}}$ is the orthogonal projector onto the range of $\mathbf{A}\mathbf{\Omega}$.
We can prove bounds about this quantity even without knowing how to compute it.

In these cases, we know that these quantities can be computed efficiently, perhaps in many different ways, and so it is natural to reason about the output itself.


### Specifying an implementation

If we want to understand stuff about a specific algorithm, i.e. a sequence of steps that computes the quantity, then we need to know what these steps are.
For CG the usual choice is the recurrence of Hestenes and Stiefel:[@HestenesStiefel1952].

```
CG(A,b,x,k):
    r = b - A x
    p = r
    for j = 1, 2, ..., k:
        α = (r, r) / (p, A p)
        x = x + α p
        r' = r - α A p
        β = (r', r') / (r, r)
        p = r' + β p
        r = r'
    return x
```

In exact arithmetic, one can prove that `CG(A,b,x_0,k)` returns the CG iterate $\mathbf{x}_k$, and hence enjoys any of the properties we have proved about this mathematical quantity.

Of course, the above implementation is not the only way to compute $\mathbf{x}_k$; other implementations, for instance those based on the Lanczos recurrence, can also be used to compute the same mathematical quantity.
Moreover, the recurrence above is not even fully specified; it uses inner products, sums of vectors, and products with $\mathbf{A}$, but each of these can be computed in several ways.
While these implementations all produce $\mathbf{x}_k$ in exact arithmetic, their costs, and their behavior in inexact arithmetic, may differ.

In NLA, we are used to implicitly choosing the level of granularity that is ~relevant~ based on informal knowledge and vibes.
For example, in the implementation of CG we may not specify how inner products are performed, because we have some kind of understanding that any reasonable implementation will produce similar results.
Yet, we specify the order of vector operations because these do have a large qualitative impact on the quantity computed.

NLA-lib allows the base-operations, and promises about their accuracy, to be specified. 
For example, CG can be written at the level of vector operations, with promises about how accurately these operations are computed. 
Alternately, specific arithmetic routines can be used in place of generic vector operations, with promises about how accurately arithmetic is performed.
In general, these choices are modular, which allows various computational kernels to be combined easily.


### Measuring costs

Once an implementation is specified down to individual base operations, we can count costs.
A typical result gives the cost and the accuracy together.
Consider for example the following stylized example.

::: definition
**Def.**
Let $a \oplus b$ denote floating point addition: the floating point number nearest to $a + b$.
If no overflow or underflow occurs, then $a \oplus b = (a + b)(1 + \delta)$ for some $\lvert\delta\rvert \le u$, where $u$ is the unit roundoff.
:::

::: definition
**Def.**
`SUM` is the program

```
SUM(x_1, ..., x_n):
    s = x_1
    for i = 2, ..., n
        s = s ⊕ x_i
    return s
```

:::

::: theorem
**Theorem.**
For any floating point numbers $x_1, \ldots, x_n$, if no overflow or underflow occurs, `SUM` uses $n-1$ floating point additions and returns a value $s$ satisfying
$$
\Bigl\lvert s - \sum_{i=1}^n x_i \Bigr\rvert \le \bigl((1+u)^{n-1} - 1\bigr) \sum_{i=1}^n \lvert x_i \rvert.
$$

:::

A lot of formalization of numerical algorithms has this shape.
Libraries such as [Flean](https://github.com/minusgix/flean), [FloatSpec](https://reservoir.lean-lang.org/@Beneficial-AI-Foundation/FloatSpec) and [FloatLib](https://arxiv.org/abs/2609.19352) formalize floating point formats and rounding in Lean, and [SciLean](https://reservoir.lean-lang.org/@lecopivo/scilean) is a library for writing numerical programs in Lean.
With these, an algorithm is an ordinary Lean function, and a theorem is a statement about the value it returns.


#### Not so fast!!

The astute reader will recognize that the theorem above is *meaningless* without the definition of `SUM`; when an algorithm is an ordinary function, Lean checks the bound on the value it returns, but the count "$n-1$ additions" is only as good as the reader's inspection of the definition.
In other words, the user needs to check what the algorithm is, and that the operations being counted are the only work it does.

Consider for example the following example.

::: definition
**Def.**
`EXACT_SUM` is the program

```
EXACT_SUM(x_1, ..., x_n):
    s = x_1
    for i = 2, ..., n
        s = s + x_i
    return fl(s) ⊕ 0
```

:::

::: theorem
**Theorem.**
For any floating point numbers $x_1, \ldots, x_n$, if no overflow or underflow occurs, `EXACT_SUM` uses one floating point addition and returns a value $s$ satisfying
$$
\Bigl\lvert s - \sum_{i=1}^n x_i \Bigr\rvert \le u \sum_{i=1}^n  x_i .
$$

:::

This theorem is true, and it claims an error and cost that are each seemingly impossible.
The issue is that `EXACT_SUM` is not something a computer can run with one floating point addition: it adds real numbers exactly and rounds once at the end.
However, nothing in Lean prevents this, since the real numbers and their exact arithmetic are available to every definition.
In particular, statements about cost must also discuss what an algorithm is not allowed to do.
Yet, this is only stated implicitly in essentially all numerical analysis results. 

#### Even more!!

This is not the only way we can produce statements that are seemingly too good to be true.
For example:

::: definition
**Def.**
`OVERFLOW_SUM` is the program

```
OVERFLOW_SUM(x_1, ..., x_n):
    a = largest floating point number
    s = a ⊕ a         // always overflows
    return 0
```

:::

::: theorem
**Theorem.**
For any floating point numbers $x_1, \ldots, x_n$, if no overflow or underflow occurs, `OVERFLOW_SUM` uses one floating point addition and returns a value $s$ satisfying
$$
\Bigl\lvert s - \sum_{i=1}^n x_i \Bigr\rvert \le u \sum_{i=1}^n  x_i .
$$

:::

Here, the addition in `OVERFLOW_SUM` overflows on every input, so the hypothesis "no overflow or underflow occurs" is never satisfied and the theorem is vacuous.


## How NLA-lib handles things

Both of the examples above are easy to observe because the programs are simple and can be inspected directly.
However, for more complicated algorithms, having to check that the implementation of an algorithm is correct by hand undermines much of the value of formal verification.

In NLA-lib, we define *programs* as a fixed tree of operation calls and control flow.
An *operation model* dictates which operations a program may call (e.g. scalar `+`, `dot`, a product with $\mathbf{A}$, etc.), what each operation guarantees, and how much each call costs.
The operations, guarantees, and costs are flexible so that users can prove results using subroutine that have not been anticipated.
At the same time, we provide several ``standard'' collections of base operations (e.g. BLAS1 operations to relative accuracy, the standard model of floating point arithmetic, etc.) which specify base operations, their guarantees, and their costs.


### Trust

The value of our approach is that users are able to outsource trust of many things to the library. 
In particular, a user who trusts that NLA-lib's definition programs and standard collections of base operations are sound can have faith that some algorithm satisfies the specified accuracy and runtime guarantees. 
We hope that as more users adopt NLA-lib for their own work, that this will help identify any bugs in our implementations, and increase the overall trust in the library.

## Formalizing software

Our approach for formalization differs from other related formalization projects in aim. 
In particular, we aim to be able to reason about the theoretical analysis of algorithms, including in models of inexact arithmetic.

One might argue that what we should care about is whether the "real-world" implementations work.
For example, it would be wonderful if when you called an eigensolver in LAPACK, it would be guaranteed to succeed and produce an accurate output. 
However, doing so would require reasoning about FORTRAN, the compiler, whatever implementation of BLAS is being used, and the system the code is being run on.

An intermediate approach is to write the software in Lean itself.
Lean is a programming language as well as a proof assistant, and projects such as [SciLean](https://github.com/lecopivo/SciLean) (scientific computing in Lean) and [FloatLib](https://arxiv.org/abs/2609.19352) (verified floating point arithmetic in Lean) make it possible to write numerical code that runs reasonably fast.
One can then use Lean to reason about the outputs of these codes.

Such algorithms can inherent much of the error bounds from NLA-lib.
In particular, the way we define error bounds typically involve showing that our programs satisfy certain mathematical conditions, which then imply error bounds.
A bridge showing that other software satisfies the relevant mathematical conditions allows the error bounds to be applied.



## Where to read more

- [CONTRIBUTING.md](https://github.com/NLA-lib/nlalib/blob/main/CONTRIBUTING.md): the library's full rules and the checks that enforce them.
- The [Explorer](../explore/): theorem statements and source links.

