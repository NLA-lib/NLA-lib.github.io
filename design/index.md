---
title: How NLA-lib defines things
description: Brief overview of some of the key design decisions in NLA-lib.
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

Results in NLA are often stated using notation like big-O that is typically not defined precisely.
As such, statements often leave implicit in what order the quantifiers come.
One advantage of formalization is making this kind of thing precise.
The cost is that the precise statements are more verbose.
For reference, we have also included "simpler" versions of many statements of the form "there exist $C, \varepsilon_0 > 0$ such that for all $k$ and all $\varepsilon \in (0, \varepsilon_0]$, BLAH".
In such statements, the hidden constant may trade off very poorly with the range of validity in parameters, so the constants used may be extremely large, even when the more precise bound is better.

### Algorithms

Much of NLA is concerned with algorithms.
In NLA-lib, algorithms (and theorems about algorithms) can roughly be broken into two categories:

- **Mathematical quantities.** The first kind are theorems about algorithms as mathematical objects.
For instance, the mathematical object: `rsvd A Ω` is the projection $\mathbf{P}_{\mathbf{A}\mathbf{\Omega}}\mathbf{A}$, and corresponding theorems bound its error.
Such theorems are typically relatively simple to state and read, and typically reflect literature results well.
- **Programs.** The second kind is about a particular implementation of a mathematical algorithm: a sequence of operations that, in principle, outputs the mathematical object.
We describe such algorithms using Programs, which are written in a small language that NLA-lib defines in Lean.
A Program is built from a fixed set of instructions, and the library defines how it runs, so theorems can say what it computes, what it costs, and how accurate it is in finite precision.
We [expand on the implementation of programs below](#programs).

## Programs

A program is a particular sequence of operations that computes a mathematical object.
This lets us keep track of things like how many operations or matrix-vector products the program uses, how much memory it needs, and how accurate it is in finite precision.
These are properties of a particular way of computing the object, not of the object, so the program itself must be something a theorem can talk about.

### Example: summing numbers

Suppose we want to sum $n$ real numbers in floating point, and count the additions.
To reason about rounding, make the rounded addition a parameter `fl_add` that satisfies the standard model: $\mathrm{fl}(a+b) = (a+b)(1+\delta)$ with $\lvert\delta\rvert \le u$.
To count, use a counter that every addition increments, as one would in Python with a class that holds a count.
Lean has no hidden mutable state, but the state monad passes a counter along:

```lean
def addC (fl_add : ℝ → ℝ → ℝ) (a b : ℝ) : StateM ℕ ℝ := do
  modify (· + 1)          -- counter += 1
  pure (fl_add a b)

def recSum (fl_add : ℝ → ℝ → ℝ) (x : Fin n → ℝ) : StateM ℕ ℝ :=
  Fin.foldlM n (fun s i => addC fl_add s (x i)) 0
```

The increment lives inside the counted addition, so whoever writes `recSum` places no ticks.
Two theorems follow by induction on the loop: the counter ends at $n$, and the computed sum is within $\gamma_{n-1}\sum_i \lvert x_i \rvert$ of the true one, where $\gamma_k = (1-u)^{-k} - 1$ (Higham, §4.2).
For an algorithm designer who only adds through `addC`, this is the right cost and the right error.

The trouble is that nothing makes a designer do so.
The counter counts only the additions that go through it:

```lean
def cheatSum (fl_add : ℝ → ℝ → ℝ) (x : Fin n → ℝ) : StateM ℕ ℝ :=
  addC fl_add 0 (∑ i, x i)       -- count: 1
```

The counter ends at $1$, and the standard model gives, in one line, an error of at most $u \lvert \sum_i x_i \rvert$.
Both the accuracy and cost claims beat every real summation algorithm.
The theorems are correct; what is wrong is that `∑ i, x i` did $n-1$ additions exactly, in an arithmetic no computer has, without passing the counter.
And the trick works anywhere: to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$, compute $\mathbf{A}^{-1}\mathbf{b}$ exactly and round each entry, for $n$ counted operations and componentwise relative error $u$.

Basic attempts to forbid the bypass fail too.
For example, making the code generic in the number type, so that it has no `∑` to call, does not work: Lean's logic is classical, so generic code can ask which type it was given and cheat only on `ℝ`.

### How NLA-lib rules it out

NLA-lib keeps the counter, and moves it into the interpreter.
A program is a tree built from a fixed set of instructions, with no Lean function inside it, so the allowed operations are a definition: there is no `∑` to call and no way to ask which type a value has.
The library defines how a tree runs: the state of a run has a count, and the run adds to it for every instruction it executes, however the result is used.
The only way a program can add is an addition instruction, and the only thing that executes instructions is the run.
So `cheatSum` cannot be written, and the count is a property of the run, not of how the author wrote the code.

Recursive summation as a program is a loop of additions into one cell:

```lean
def sum (p : P) (dst : Cell VB VI) (x : VB) (n : IExp VI) : Builder P ι VB VI Unit := do
  ins (.lit p dst 0)                                           -- dst ← 0
  forRange n fun i => ins (.bin p .add dst dst ⟨x, .var i⟩)   -- dst ← dst + x[i]
```

It has two theorems, each proved by induction on the loop.

1. **Exact arithmetic.** If the cells of `x` hold $x_0, \ldots, x_{n-1}$, the run succeeds, writes $\sum_i x_i$ into `dst`, and counts $n$ additions and one literal.
The invariant: after $i$ iterations, `dst` holds $\sum_{j<i} x_j$, and the counts are $i$ additions and one literal.
2. **Rounded arithmetic.** Under the contract `IsRelErrSem` with unit roundoff $u$, every addition stays in range and returns $(a+b)(1+\delta)$ with $\lvert\delta\rvert \le u$.
The invariant: `dst` holds $\sum_{j<i} x_j(1+\eta_j)$ with $\lvert\eta_j\rvert \le \gamma_{i-1}$, using that adding to zero is exact.
At the end, the computed $w$ satisfies $\lvert \sum_i x_i - w \rvert \le \gamma_{n-1} \sum_i \lvert x_i \rvert$.

The cost in the first theorem and the error in the second are about the same tree, so together they say what `cheatSum` could not: this accuracy, at this cost.
IEEE double is proved to meet the contract, so the bound holds for it too.
The library's `dot` kernel is this program with a multiplication in the loop; its theorems are `exec_dot` and `IsRelErrSem.exec_dot_abs_sum_mul_sub_le`.

Every kind of operation is counted separately: arithmetic, comparisons, literals and copies, reads of stored entries, matrix-vector products, random draws, and memory.
Index arithmetic and loop control are not counted; they depend only on the sizes.

A published cost result is a proof of a target: a statement written and registered by the library, about a registered program, that fixes the program before the sizes, the matrix and the random draws.
The prover supplies only the proof, and a hash of everything the statement reaches stops it from being weakened.

### Arithmetic models

A program does not fix its arithmetic.
A run is given a value semantics, which says what each operation returns or that it fails, and each theorem names the one it assumes.

- **Exact arithmetic.** Operations on real or complex numbers, with no rounding.
This is where counts are proved, and where a program is shown to compute its mathematical object.
- **Error contracts.** A contract is a condition on the semantics.
For example, the standard model of floating point arithmetic, `IsRelErrSem`, requires every operation to return its exact result times $(1+\delta)$ with $\lvert\delta\rvert \le u$.
Variants of this model that have a bounded exponent range (so that numbers might overflow or underflow) require, in addition, that the exact result of every operation lies in the representable range, so a program must prove that it never overflows; with gradual underflow, the error gains an absolute term, $\lvert a - z \rvert \le u\lvert a \rvert + \eta$.

To apply a result to a particular arithmetic, such as IEEE 754 double precision, one proves that the arithmetic meets the contract.

### Oracles and certified routines

Algorithms in NLA are often described and analyzed in terms of abstracted subroutines (e.g. matrix-vector products, orthogonalization, and least squares solves).
NLA-lib supports this in two ways: oracles, whose guarantees are assumed, and certified routines, whose guarantees are proved.

- **Oracles.** An oracle is a primitive, like an arithmetic operation: a program can call it but cannot see how it is computed.
What an oracle returns is assumed through a contract, just as `IsRelErrSem` is the contract for arithmetic.
The main example of an oracle in NLA-lib is matrix-vector products.
- **Certified routines.** A routine is ordinary code.
Its certificate is a theorem that it succeeds, changes only its outputs, and meets an error bound.
A program that takes a routine as a parameter is proved for every routine with that certificate; for instance, Lanczos with full reorthogonalization is proved for any orthogonalization routine certified by `IsOrthRoutine`.

## Some design decisions we made

- **Definitions are total**, as in Mathlib ([why this is fine](https://xenaproject.wordpress.com/2020/07/05/division-by-zero-in-type-theory-a-faq/)): the inverse of a singular matrix is defined to be $0$, and each such value is documented.
So we can prove "the inverse of a non-invertible matrix is zero", but this is a fact about the convention, not about inverses.
Anything that actually uses invertibility, such as $\mathbf{A}^{-1}\mathbf{A} = \mathbf{I}$, fails for singular $\mathbf{A}$ (it gives $\mathbf{0} = \mathbf{I}$), so it can only be proved with the hypothesis that $\mathbf{A}$ is invertible.
A theorem that needs nondegeneracy states it as a hypothesis.
- **Randomness is explicit.** A test matrix is a random variable $\mathbf{\Omega}$ on an arbitrary probability space, with a hypothesis on its law (Gaussian, Haar, a sparse sign sketch).
Statements do not build the matrix from random entries on a space of its own.
- **Expectations come with integrability.** An expectation is an integral, and totality applies here too: the integral of a non-integrable function is defined to be $0$.
So a bound like $\mathbb{E}\|\mathbf{A} - \mathsf{rsvd}(\mathbf{A},\mathbf{\Omega})\|_{\mathsf{F}} \le B$ would hold trivially if the error were not integrable, and every such bound comes with a separate theorem that it is.
- **No focus on software implementation.** Our algorithms are defined mathematically or as Programs as described above.
Proving stuff about particular software, such as LAPACK, would introduce many new challenges and is currently out of scope.

## Where to read more

- [CONTRIBUTING.md](https://github.com/NLA-lib/nlalib/blob/main/CONTRIBUTING.md) is the library's contract: representation, total definitions, statement shapes, randomness, constants and asymptotic forms (§5), and the checks that enforce them.
- [docs/design/Computation.md](https://github.com/NLA-lib/nlalib/blob/main/docs/design/Computation.md) is the design of the program layer: the syntax, the run, the access models, the error contracts, and what is proved and what is trusted.
- The [explorer](../explore/) has the definitions and theorems named on this page, with their statements and sources.
