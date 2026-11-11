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

## Programs and operation models {#programs}

The central idea is **composable operations**. An algorithm is written as pseudocode using operations such as `matvec`, `dot`, and `axpy`. Each operation has an interface specifying its inputs and outputs, and a contract specifying what it guarantees. A theorem analyzes the algorithm under those contracts.

An **operation model** specifies the available operations, their assumptions, and how calls and workspace are counted. For example, a model for conjugate gradient can provide an exact matrix-vector product, exact dot products, and exact vector updates. Another can allow a bounded error in each of those operations. A randomized model also specifies the relevant laws and independence assumptions.

An algorithm together with an operation model gives a precise setting for a theorem. The theorem can establish what the algorithm returns, whether it terminates, its accuracy, how many calls it makes, and its peak scratch space. For example, after initialization, each step of Hestenes–Stiefel CG uses one matrix-vector product and two dot products. The meaning and accuracy of those calls come from the chosen model. Convergence also depends on mathematical assumptions such as positive definiteness of the matrix.

An **implementation** expresses an operation using the operations of another model. A dot product can be implemented using scalar multiplication and sequential addition, or using scalar multiplication and pairwise summation. Its certificate proves that this program meets the dot-product contract, with bounds on its lower-level cost and workspace.

**Composition** substitutes those implementations into the algorithm. The library transfers the theorem through their certificates and computes the resulting cost bounds. A CG theorem stated in terms of vector operations can thus give a theorem about the program built from scalar arithmetic. A matrix-vector product can remain primitive at that level, or be implemented using further operations. The word *primitive* refers to where a particular model ends.

NLA-lib provides standard operation models and standard collections of implementations, and users can define their own. These answer two useful questions when reading a result.

| Choice | What it specifies | CG example |
|---|---|---|
| Operation model | Available calls, assumptions, and cost conventions | Exact or error-bounded `matvec`, `dot`, and vector updates |
| Implementations | How calls are realized using another model | Sequential or pairwise dot products using scalar arithmetic |

The library's new program model, `Ops`, supplies the language of calls and control flow, the evaluator that counts a run, and the composition theorems. Its current implementation collections are called *profiles*, and their compositions are called *stacks*.

### Arithmetic models

An exact-arithmetic theorem is a result in its own right. It can establish that a program returns the mathematical iterate and prove identities or termination properties specific to exact arithmetic. A rounded theorem gives a guarantee under stated error contracts. In the standard model, for instance, a scalar result has the form $\mathrm{fl}(z)=z(1+\delta)$ with $|\delta|\le u$ on the operation's domain. A certified implementation supplies particular error constants to the algorithm's theorem. For bounded formats, the guarantee states any conditions needed to stay in range.

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

An HSCG page will explain the operation models under which the recurrence has been analyzed and the implementations available for its calls. It can then show how choosing sequential or pairwise dot products affects a composed implementation. Each guarantee should name its assumptions, the accuracy or mathematical property it establishes, and the level at which operations and workspace are counted. Preconditioned CG gets its own pseudocode and guarantees because it adds a preconditioner call and changes the recurrence.

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
