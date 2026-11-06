# How NLAlib defines things

This page provides an overview of several choices NLA-lib makes in formalizing numerical linear algebra. More precise rules are in the repository.

## Why formalizing NLA is hard

The challenges of formalizing NLA are in many ways different from those in certain parts of theoretical math. For instance, the Lean statement of Fermat's last theorem is extremely simple and easy for a human to check, even though the formal proof itself is incredibly long. In contrast, natural language results in NLA are often stated with implicit definitions, quantification (e.g. when using big-$O$), integrability assumptions (e.g. when using Markov's inequality), and models of computation. Moreover, there are many formal statements that are all slight variants of one another (for example, with slightly different bounds on parameters). This adds a number of subtleties to formalizing NLA not encountered in certain areas of pure math.

### Quantification and constants

Results in NLA are often stated asymptotically: with $s = O(k/\varepsilon)$ columns, the error is at most $(1+\varepsilon)$ times optimal with high probability. Such a statement leaves implicit what the hidden constant may depend on, and in what order the quantifiers come. One advantage of formalization is making this kind of thing precise. The cost is that such statements are more verbose. For reference, we have also included "simpler" versions of many statements of the form "there exists $C > 0$ such that $for all $k>0$, blah". In such statements, the hidden constant may trade off very poorly with the range of validity in parameters, so the constants used may be extremely large, even when the more precise bound is better.

### Algorithms

Much of NLA is concerned with algorithms. In NLA-lib, algorithms (and theorems about algorithms) can roughly be broken into two categories:

- **Mathematical quantities.** First, are theorems about algorithms as mathematical objects. For instance, the mathematical object: `rsvd A Ω` is the projection $\mathbf{P}_{\mathbf{A}\mathbf{\Omega}}\mathbf{A}$, and a theorem bounds its error. Such theorems are typically simpler to state and read, and typically reflect literature results well.
- **Programs.** The second kind is about particular implementation of a mathematical algorithm; i.e. a sequence of operations that, in principle, outputs the mathematical object. The rounding model is not part of the program: the same program can run with exact arithmetic, or with any arithmetic that meets an error contract such as the standard model. A theorem about rounding holds for every arithmetic that meets its contract, and specific formats, such as IEEE double, are proved to meet it. We [expand on the implementation of programs below](#programs).

## Programs

A program is a particular sequence of operations that computes a mathematical object. This lets us keep track of things like how many operations or matrix-vector products the program uses, how much memory it needs, and how accurate it is in finite precision. These are properties of a particular way of computing the object, not of the object, so the program itself must be something a theorem can talk about.

### Example: summing numbers

Suppose we want to sum $n$ real numbers in floating point, and count the additions. To reason about rounding, make the rounded addition a parameter `fl_add` that satisfies the standard model: $\mathrm{fl}(a+b) = (a+b)(1+\delta)$ with $\lvert\delta\rvert \le u$. To count, use a counter that every addition increments, as one would in Python with a class that holds a count. Lean has no hidden mutable state, but the state monad passes a counter along:

```lean
def addC (fl_add : ℝ → ℝ → ℝ) (a b : ℝ) : StateM ℕ ℝ := do
  modify (· + 1)          -- counter += 1
  pure (fl_add a b)

def recSum (fl_add : ℝ → ℝ → ℝ) (x : Fin n → ℝ) : StateM ℕ ℝ :=
  Fin.foldlM n (fun s i => addC fl_add s (x i)) 0
```

The increment lives inside the counted addition, so whoever writes `recSum` places no ticks. Two theorems follow by induction on the loop: the counter ends at $n$, and the computed sum is within $\gamma_{n-1}\sum_i \lvert x_i \rvert$ of the true one, where $\gamma_k = (1-u)^{-k} - 1$ (Higham, §4.2). For an algorithm designer who only adds through `addC`, this is the right cost and the right error.

The trouble is that nothing makes a designer do so. The counter counts only the additions that go through it:

```lean
def cheatSum (fl_add : ℝ → ℝ → ℝ) (x : Fin n → ℝ) : StateM ℕ ℝ :=
  addC fl_add 0 (∑ i, x i)       -- count: 1
```

The counter ends at $1$, and the standard model gives, in one line, an error of at most $u \lvert \sum_i x_i \rvert$. Both the accuracy and cost claims beat every real summation algorithm. The theorems are correct; what is wrong is that `∑ i, x i` did $n-1$ additions exactly, in an arithmetic no computer has, without passing the counter. The same is true of the Python class: `self.add(0, sum(x))` reports one addition. And the trick works anywhere: to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$, compute $\mathbf{A}^{-1}\mathbf{b}$ exactly and round each entry, for $n$ counted operations and componentwise relative error $u$.

Attempts to forbid the bypass fail too. For example, making the code generic in the number type, so that it has no `∑` to call, does not work: Lean's logic is classical, so generic code can ask which type it was given and cheat only on `ℝ`.

A trustworthy designer never bypasses the counter. A library that accepts proofs from anyone, including automated provers, cannot rely on that: "uses only the allowed operations" has to be guaranteed by the statement itself.

### How NLAlib rules it out

NLAlib keeps the counter, and moves it into the interpreter. A program is a tree built from a fixed set of instructions, with no Lean function inside it, so the allowed operations are a definition: there is no `∑` to call and no way to ask which type a value has. The library defines how a tree runs: the state of a run has a count, and the run adds to it for every instruction it executes, however the result is used. The only way a program can add is an addition instruction, and the only thing that executes instructions is the run. So `cheatSum` cannot be written, and the count is a property of the run, not of how the author wrote the code.

Recursive summation as a program is a loop of additions into one cell:

```lean
def sum (p : P) (dst : Cell VB VI) (x : VB) (n : IExp VI) : Builder P ι VB VI Unit := do
  ins (.lit p dst 0)                                           -- dst ← 0
  forRange n fun i => ins (.bin p .add dst dst ⟨x, .var i⟩)   -- dst ← dst + x[i]
```

It has two theorems, each proved by induction on the loop.

1. **Exact arithmetic.** If the cells of `x` hold $x_0, \ldots, x_{n-1}$, the run succeeds, writes $\sum_i x_i$ into `dst`, and counts $n$ additions and one literal. The invariant: after $i$ iterations, `dst` holds $\sum_{j<i} x_j$, and the counts are $i$ additions and one literal.
2. **Rounded arithmetic.** Under the contract `IsRelErrSem` with unit roundoff $u$, every addition stays in range and returns $(a+b)(1+\delta)$ with $\lvert\delta\rvert \le u$. The invariant: `dst` holds $\sum_{j<i} x_j(1+\eta_j)$ with $\lvert\eta_j\rvert \le \gamma_{i-1}$, using that adding to zero is exact. At the end, the computed $w$ satisfies $\lvert \sum_i x_i - w \rvert \le \gamma_{n-1} \sum_i \lvert x_i \rvert$.

The cost in the first theorem and the error in the second are about the same tree, so together they say what `cheatSum` could not: this accuracy, at this cost. IEEE double is proved to meet the contract, so the bound holds for it too. The library's `dot` kernel is this program with a multiplication in the loop; its theorems are `exec_dot` and `IsRelErrSem.exec_dot_abs_sum_mul_sub_le`.

Every kind of operation is counted separately: arithmetic, comparisons, literals and copies, reads of stored entries, matrix-vector products, random draws, and memory. Index arithmetic and loop control are not counted; they depend only on the sizes.

A published cost result is a proof of a target: a statement written and registered by the library, about a registered program, that fixes the program before the sizes, the matrix and the random draws. The prover supplies only the proof, and a hash of everything the statement reaches stops it from being weakened.

### Arithmetic models

A program does not fix its arithmetic. A run is given a value semantics, which says what each operation returns or that it fails, and each theorem names the one it assumes.

- **Exact arithmetic.** Operations on real or complex numbers, with no rounding. This is where counts are proved, and where a program is shown to compute its mathematical object.
- **Error contracts.** A contract is a condition on the semantics. For example, the standard model of floating point arithmetic, `IsRelErrSem`, requires every operation to return its exact result times $(1+\delta)$ with $\lvert\delta\rvert \le u$. Variants of this model that have a bounded exponent range (so that numbers might overflow or underflow) require, in addition, that the exact result of every operation lies in the representable range, so a program must prove that it never overflows; with gradual underflow, the error gains an absolute term, $\lvert a - z \rvert \le u\lvert a \rvert + \eta$.

To apply a result to a particular arithmetic, such as IEEE 754 double precision, one proves that the arithmetic meets the contract.

### Matrix-vector products

Many NLA algorithms, such as Krylov methods and sketching, touch the matrix only through products $\mathbf{x} \mapsto \mathbf{A}\mathbf{x}$, and their cost is counted in products. The counter problem appears again. Give a Lean function a product `mv` and count the calls through a wrapper, and it can still recover $\mathbf{A}$ without a single counted call:

```lean
noncomputable def recover (mv : (Fin n → ℝ) → (Fin n → ℝ)) : Matrix (Fin n) (Fin n) ℝ :=
  if h : ∃ A : Matrix (Fin n) (Fin n) ℝ, ∀ x, mv x = A *ᵥ x then h.choose else 0
```

In NLAlib the product is an instruction, `apply`, counted like arithmetic, and a program fixed before the matrix sees it only through these counted calls.

A program can instead read stored entries of the matrix, each read counted, and a matrix-free result gives the dense and sparse results by substitution.

As for arithmetic, the product has error contracts of its own (`IsMatvecErr`), and a result under rounding holds for every oracle that meets its contract.

## Some design decisions we made

- **Definitions are total**, as in Mathlib ([why this is fine](https://xenaproject.wordpress.com/2020/07/05/division-by-zero-in-type-theory-a-faq/)): the inverse of a singular matrix is defined to be $0$, and each such value is documented. So we can prove "the inverse of a non-invertible matrix is zero", but this is a fact about the convention, not about inverses. Anything that actually uses invertibility, such as $\mathbf{A}^{-1}\mathbf{A} = \mathbf{I}$, fails for singular $\mathbf{A}$ (it gives $\mathbf{0} = \mathbf{I}$), so it can only be proved with the hypothesis that $\mathbf{A}$ is invertible. A theorem that needs nondegeneracy states it as a hypothesis.
- **Randomness is explicit.** A test matrix is a random variable $\mathbf{\Omega}$ on an arbitrary probability space, with a hypothesis on its law (Gaussian, Haar, a sparse sign sketch). Statements do not build the matrix from random entries on a space of its own.
- **Expectations come with integrability.** An expectation is an integral, and totality applies here too: the integral of a non-integrable function is defined to be $0$. So a bound like $\mathbb{E}\|\mathbf{A} - \mathsf{rsvd}(\mathbf{A},\mathbf{\Omega})\|_{\mathsf{F}} \le B$ would hold trivially if the error were not integrable, and every such bound comes with a separate theorem that it is.

## Where to read more

- [CONTRIBUTING.md](https://github.com/NLA-lib/nlalib/blob/main/CONTRIBUTING.md) is the library's contract: representation, total definitions, statement shapes, randomness, constants and asymptotic forms (§5), and the checks that enforce them.
- [docs/design/Computation.md](https://github.com/NLA-lib/nlalib/blob/main/docs/design/Computation.md) is the design of the program layer: the syntax, the run, the access models, the error contracts, and what is proved and what is trusted.
- The explorer has the definitions and theorems named on this page, with their statements and sources.