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

### Algorithms and operation models

An algorithm needs more than a function from inputs to outputs. Two procedures can compute the same mathematical answer while using different operations, having different costs, and behaving differently under rounding. A formal account of an algorithm therefore specifies its steps and the operations those steps use.

There are many combinations to describe. Within conjugate gradient, we can choose different recurrences and orderings. For each variant, we can study exact arithmetic, bounded rounding errors, or a particular floating-point format. We can treat dot products and matrix-vector products as primitive calls, or supply implementations with their own arithmetic assumptions and costs. Even a dot product has sequential and pairwise variants. These choices affect which theorems hold and what their bounds mean.

NLA-lib makes these choices explicit through algorithms, operation models, and certified implementations. Shared contracts let a theorem apply to many compatible combinations, while composition connects a result about abstract operations to the implementations that realize them.

## Algorithms

A mathematical description of an algorithm lets us study its iterates and outputs. For example, conjugate gradient produces approximate solutions to an SPD system, and a dot product computes $x^\mathsf{T}y$. Theorems about these objects establish properties such as convergence and approximation error.

To establish the cost or numerical behavior of a particular procedure, we also specify its steps. A **program** is the formal representation of that procedure. Hestenes–Stiefel CG and another CG recurrence are variants within the CG family. Sequential and pairwise dot products are variants within the dot-product family. An algorithm at one level can implement an operation used by an algorithm at another level.

### Why a counted function is insufficient

Suppose we want to sum $n$ numbers using rounded addition and count the additions. We could wrap each addition in a counter. In Lean, a state monad can carry that counter.

```lean
def addC (fl_add : ℝ → ℝ → ℝ) (a b : ℝ) : StateM ℕ ℝ := do
  modify (· + 1)
  pure (fl_add a b)
```

A summation loop that calls this wrapper has a reasonable count. But a function can also compute the entire sum using Lean's real arithmetic and pass the result through the wrapper once.

```lean
def cheatSum (fl_add : ℝ → ℝ → ℝ) (x : Fin n → ℝ) : StateM ℕ ℝ :=
  addC fl_add 0 (∑ i, x i)
```

The counter reports one addition. If `fl_add` meets the standard relative-error bound with parameter $u$, the result has error at most $u|\sum_i x_i|$. The mathematical statements about this function are valid. However, the exact summation took place outside the counter. The same construction could compute $A^{-1}b$ exactly and round each output entry, charging only for that final rounding.

Making the function generic in its value type is also insufficient. Lean's classical logic can distinguish the real-number case and choose special behavior there. The allowed computation therefore has to be enforced by the representation of a program.

### How the program model enforces the operations

A program is a tree of operation calls and control flow over stored values. Computed values are accessed through those calls. The evaluator executes the tree and records its calls and peak scratch space. The algorithm author expresses the procedure in this language, while the evaluator supplies its accounting.

In a scalar-addition model, summation is a loop that reads an entry and calls addition on the accumulator. The tree has no place to insert an arbitrary Lean function that computes the exact sum. If a higher-level model provides `sum` as a primitive, its theorem counts calls to `sum`. Obtaining a scalar-operation bound then requires a certified implementation of that operation.

The model definition is consequently part of what a reader inspects. It states which computations are primitive and what their calls cost. The program representation enforces use of that model, and the implementation certificates justify moving to a more detailed one.

## Programs and operation models {#programs}

The central idea is **composable operations**. An algorithm is written as pseudocode using operations such as `matvec`, `dot`, and `axpy`. Each operation has an interface specifying its inputs and outputs, and a contract specifying what it guarantees. A theorem analyzes the algorithm under those contracts.

An **operation model** specifies the available operations, their assumptions, and how calls and workspace are counted. For example, a model for conjugate gradient can provide an exact matrix-vector product, exact dot products, and exact vector updates. Another can allow a bounded error in each of those operations. A randomized model also specifies the relevant laws and independence assumptions.

An algorithm together with an operation model gives a precise setting for a theorem. The theorem can establish what the algorithm returns, whether it terminates, its accuracy, how many calls it makes, and its peak scratch space. For example, after initialization, each step of Hestenes–Stiefel CG uses one matrix-vector product and two dot products. The meaning and accuracy of those calls come from the chosen model. Convergence also depends on mathematical assumptions such as positive definiteness of the matrix.

An **implementation** expresses an operation using the operations of another model. A dot product can be implemented using scalar multiplication and sequential addition, or using scalar multiplication and pairwise summation. Its certificate proves that this program meets the dot-product contract, with bounds on its lower-level cost and workspace.

**Composition** substitutes those implementations into the algorithm. The library transfers the theorem through their certificates and computes the resulting cost bounds. A CG theorem stated in terms of vector operations can thus give a theorem about the program built from scalar arithmetic. A matrix-vector product can remain primitive at that level, or be implemented using further operations. The word *primitive* refers to where a particular model ends.

### Standard operation models

The library offers **named, standardized operation models** and certified implementations between them. An author selects a model and its parameters when stating a theorem. Users can also define custom models through the same interfaces.

A model is assembled from **operation groups**. For example, a CG model can select a scalar-arithmetic group, a BLAS1 group, and a matrix-vector-product group. Each group defines its operation names, input and output shapes, and a bundled contract. The theorem can assume that bundle as a single hypothesis. The individual primitive declarations live in the shared catalog, where their definitions can be reviewed once and reused across algorithms.

The standard choices cover several independent questions.

| Choice | Examples | What it determines |
|---|---|---|
| Operation level | Scalar arithmetic or BLAS operations | Which calls the algorithm uses and counts |
| Arithmetic assumptions | Exact results or standard rounding-error bounds | The guarantees available for those calls |
| Matrix access | A matvec oracle or stored matrix entries | How the program accesses the matrix |
| Implementation | Sequential or pairwise dot products | How higher-level calls are realized |

These choices combine. A theorem can analyze HSCG using error-bounded BLAS operations and an exact matvec oracle. A certified sequential BLAS implementation then supplies particular error constants and scalar-operation costs. Implementing the matvec gives a further composition step.

Standard models collect scalar and BLAS1 operation groups, exact or standard-model arithmetic contracts, and matrix-access contracts into named combinations. Certified implementations include sequential and pairwise BLAS algorithms. A format-specific model such as IEEE64 specifies its arithmetic behavior and any range conditions needed by its guarantees. Dot-product summation order is a separate implementation choice.

### Defining and checking a model

The model interface collects the operation groups and their parameters, their contracts, and the conventions for costs, workspace, tests, index conversions, and randomness. Its definition determines the complete set of permitted calls. An algorithm declaration names the groups it uses, so its interface records which operations it requires.

A standard model definition also has a **joint witness** showing that its assumptions can be met together for the stated parameter range. An implementation collection supplies a certificate for each operation it implements, and the generic composition theorems transfer correctness and resource bounds. Shared definitions perform this work at the group and model level, so an algorithm author can reuse the named model and certificate bundles.

This gives authors a short model declaration and gives reviewers a precise definition to expand. The human page explains the chosen groups and assumptions. The generated reference displays the full primitive list, contracts, and certificates for inspection.

The `Ops` evaluator, contracts, and composition theorems provide the foundations for this interface. Implementation collections are called *profiles*, and their compositions are called *stacks*.

### Arithmetic models

An exact-arithmetic theorem is a result in its own right. It can establish that a program returns the mathematical iterate and prove identities or termination properties specific to exact arithmetic. A rounded theorem gives a guarantee under stated error contracts. In the standard model, for instance, a scalar result has the form $\mathrm{fl}(z)=z(1+\delta)$ with $|\delta|\le u$ on the operation's domain. A certified implementation supplies particular error constants to the algorithm's theorem. For bounded formats, the guarantee states any conditions needed to stay in range.

### What the definition enforces, and what contributors choose

For claims about computation, our formal definition of an **algorithm** is a program over a declared operation interface. Mathematical recurrences and readable pseudocode explain that program. The definition fixes how the procedure can compute; the contributor chooses the procedure and the interface it uses.

| Aspect | Enforced by the formal representation | Chosen by the contributor |
|---|---|---|
| Computation | The program uses the calls and control flow admitted by its interface. | The recurrence, ordering, stopping rule, and operation groups. |
| Primitive operations | Calls have the input and output shapes declared by the model. | Where the model stops: scalar arithmetic, BLAS, a matvec oracle, or another interface. |
| Accounting | The evaluator derives calls and workspace from execution under the declared conventions. | The cost assigned to each primitive and the resource bound to prove. |
| Guarantees | Lean checks a proof against its stated contracts and hypotheses. | The contracts, input conditions, and theorem being proved. |
| Composition | A certified implementation must meet the contract required at the substitution boundary. | Which implementation supplies each operation, and how far to lower the program. |

Thus, using the algorithm definition prevents hidden arithmetic outside the declared interface. It does not by itself make a chosen interface a useful model of computation. A contributor can declare an exact linear solve as one primitive; a theorem counting one such call then means exactly that. Claiming a scalar-operation cost requires implementing that primitive and proving the corresponding bound.

Likewise, the definition does not automatically establish convergence, numerical stability, or termination. These are proved properties of a particular program under particular assumptions. Selecting a standard model reuses a reviewed set of operations, contracts, and accounting conventions. A custom model makes those same choices explicit for review.

## Reading an algorithm page

The Explorer has curated pages organized by mathematical problem and algorithm family. The conjugate gradient family page introduces the SPD solve, explains the role of the residual, and links to variants such as Hestenes–Stiefel CG (HSCG) and preconditioned CG. A variant page puts readable pseudocode near the top, then shows the available implementations, what they assume, and the guarantees proved for them.

### A conjugate gradient example

Here is the mathematical pseudocode for HSCG with an initial guess $x$ and an iteration cap $k$. In exact arithmetic, the residual test stops the iteration when the system is solved. The formal program specifies the stopping rule used by its guarantees.

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

The HSCG page explains the operation models under which the recurrence is analyzed and the implementations available for its calls. It shows how choosing sequential or pairwise dot products affects a composed implementation. Each guarantee names its assumptions, the accuracy or mathematical property it establishes, and the level at which operations and workspace are counted. Preconditioned CG gets its own pseudocode and guarantees because it adds a preconditioner call and changes the recurrence.

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
