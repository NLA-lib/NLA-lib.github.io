---
title: How NLA-lib defines things
description: How NLA-lib specifies mathematical problems, programs, operation contracts, and verified implementations.
tab-title: NLA-lib · Design
menu:
  - Home: ../
  - Explorer: ../explore/
  - Design: ./
  - GitHub: https://github.com/NLA-lib/nlalib
---

This page provides an overview of several choices NLA-lib makes in formalizing numerical linear algebra.
More precise rules are in the repository.

## Why formalizing NLA is hard

The challenges of formalizing NLA are in many ways different from those in certain parts of theoretical math.
For instance, the Lean statement of Fermat's last theorem is extremely simple and easy for a human to check, even though the formal proof itself is incredibly long.
In contrast, natural language results in NLA are often stated with implicit definitions, quantification (e.g. when using big-$O$), integrability assumptions (e.g. when using Markov's inequality), and models of computation.
Moreover, there are many formal statements that are all slight variants of one another (for example, with slightly different bounds on parameters).
This creates a number of subtleties to formalizing NLA.

### Quantification and constants

A bound of the form $O(k/\varepsilon)$ can leave implicit what the constant depends on and how small $\varepsilon$ must be. The formal statement fixes the order of those quantifiers. When the library also gives a bound with explicit constants, readers can use it to see what the theorem guarantees for their parameters.

## Programs

A mathematical specification describes what an algorithm should compute. For conjugate gradient, it starts with a symmetric positive definite (SPD) system $Ax=b$ and describes the iterates and their error. A **program** gives the steps that compute those iterates, including the stopping rule. This gives us a way to state which operations a run uses, how much scratch space it needs, and how accurate its output is.

NLA-lib's new program model, `Ops`, gives scalar arithmetic, matrix-vector products, BLAS kernels, and random draws a common interface. An **operation** names a call and specifies the shape of its inputs and outputs. Its **contract** says what the call guarantees. An exact `matvec` contract gives $Ax$. A rounded contract can give an error bound for the returned vector. A draw contract can specify which entries of a random tape the call returns, and the theorem states the law of that tape.

An **implementation** supplies a program for an operation using lower-level calls, with a proof that it meets the contract. A **profile** collects implementations and their certificates. For example, a sequential BLAS profile implements a dot product using scalar multiplication and sequential addition. A **stack** combines profiles down to the chosen primitives. A matrix-free stack can keep `matvec` as a primitive and count one call each time the program uses it.

**Linking** substitutes implementations into the program. The library transfers the guarantee through their certificates and computes the resulting cost bounds. The same CG program can therefore have a bound in matrix-vector products and vector operations, and a linked bound that also counts the scalar operations used to implement the vector kernels. The evaluator follows the program's tree of calls and control flow, counting the calls it executes and tracking peak scratch space.

### Arithmetic models

An exact-arithmetic theorem is a result in its own right. It can establish that the program returns the mathematical iterate and prove identities or termination properties specific to exact arithmetic. A rounded theorem gives a guarantee under stated error contracts. In the standard model, for instance, a scalar result has the form $\mathrm{fl}(z)=z(1+\delta)$ with $|\delta|\le u$ on the operation's domain. A profile that meets those contracts gives a linked guarantee with its particular error constants. For bounded formats, the guarantee states any conditions needed to stay in range.

## Reading an algorithm page

The redesigned Explorer will have curated pages organized by mathematical problem and algorithm family. The conjugate gradient family page will introduce the SPD solve, explain the role of the residual, and link to variants such as Hestenes–Stiefel CG (HSCG) and preconditioned CG. A variant page will put readable pseudocode near the top, then show the available implementations, what they assume, and the guarantees proved for them.

### A conjugate gradient example

Here is the mathematical pseudocode for HSCG with an initial guess $x$ and an iteration cap $k$. In exact arithmetic, the residual test stops the iteration when the system is solved. The CG port will supply the checked program and its particular stopping rule.

```text
r ← b − A x
p ← r
ρ ← dot(r, r)
repeat at most k times:
    if ρ = 0: return x
    q ← A p
    α ← ρ / dot(p, q)
    x ← x + α p
    r ← r − α q
    ρ_new ← dot(r, r)
    p ← r + (ρ_new / ρ) p
    ρ ← ρ_new
return x
```

After initialization, each update shown here uses one matrix-vector product and two dot products. An HSCG page can explain which calls a stack keeps and which it implements. For instance, sequential and pairwise dot products use different summation orders and give different rounding bounds. Each guarantee should name its assumptions, the accuracy or mathematical property it establishes, and the level at which operations and workspace are counted. Preconditioned CG gets its own pseudocode and guarantees because it adds a preconditioner call and changes the recurrence.

The curated explanation links to the relevant formal statements and sources. The generated reference is a separate view for complete theorem signatures, extracted declarations, and machine-readable records.

## Some design decisions we made

- **Definitions are total**, as in Mathlib ([why this is fine](https://xenaproject.wordpress.com/2020/07/05/division-by-zero-in-type-theory-a-faq/)): the inverse of a singular matrix is defined to be $0$, and each such value is documented.
So we can prove "the inverse of a non-invertible matrix is zero", but this is a fact about the convention, not about inverses.
Anything that actually uses invertibility, such as $\mathbf{A}^{-1}\mathbf{A} = \mathbf{I}$, fails for singular $\mathbf{A}$ (it gives $\mathbf{0} = \mathbf{I}$), so it can only be proved with the hypothesis that $\mathbf{A}$ is invertible.
A theorem that needs nondegeneracy states it as a hypothesis.
- **Randomness is explicit.** A test matrix is a random variable $\mathbf{\Omega}$ on an arbitrary probability space, with a hypothesis on its law (Gaussian, Haar, a sparse sign sketch).
Statements do not build the matrix from random entries on a space of its own.
- **Expectations come with integrability.** An expectation is an integral, and totality applies here too: the integral of a non-integrable function is defined to be $0$.
So a bound like $\mathbb{E}\|\mathbf{A} - \mathsf{rsvd}(\mathbf{A},\mathbf{\Omega})\|_{\mathsf{F}} \le B$ would hold trivially if the error were not integrable, and every such bound comes with a separate theorem that it is.
- **Scope of software verification.** The library proves properties of mathematical algorithms and the programs it defines.
Proving stuff about particular software, such as LAPACK, would introduce many new challenges and is currently out of scope.

## Where to read more

- [CONTRIBUTING.md](https://github.com/NLA-lib/nlalib/blob/main/CONTRIBUTING.md) is the library's contract: representation, total definitions, statement shapes, randomness, constants and asymptotic forms (§5), and the checks that enforce them.
- The [Explorer](../explore/) provides theorem statements and source links for the library.
