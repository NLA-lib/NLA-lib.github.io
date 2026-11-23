---
title: Routines, models and certificates
description: How NLA-lib states what an algorithm costs and how accurate it is, built up for one small example.
tab-title: NLA-lib · Routines
menu:
  - Home: ../
  - Explorer: ../explore/
  - Design: ./
  - GitHub: https://github.com/NLA-lib/nlalib
---

As we observed, a cost or accuracy theorem about an algorithm is only meaningful if it is clear what the algorithm is allowed to do and what each of its steps costs.
NLA-lib makes this explicit with three pieces:

- a **routine**: a fixed tree of calls and control flow, which can call only operations from a closed list, together with its interface: its dimensions and how it uses each operand;
- an **operation model**: for each operation, a *contract* saying what a call guarantees, and an associated *cost*;
- a **certificate**: a theorem that for every implementation of the operations that satisfies the contracts, the routine, run on the buffers of a problem, runs to completion, within its cost budget, and its output satisfies its specification.

A fourth piece, **linking**, replaces an operation by a routine written in smaller operations and carries the certificate down with it.

This page provides an introduction to these concepts the explicit integrator
$$
\mathbf{x}_{t+1} = \mathbf{x}_t + h\mathbf{A}\mathbf{x}_t, \qquad t = 0, 1, \ldots, N-1,
$$
as an example.
**This page is an explanation of how NLA-lib works, not an example of how to use NLA-lib!!**


Everything named `My…` or `my…` below is ours, written for this example; everything else is NLA-lib's.
The example is in the library and checked by Lean, with every proof complete: [`NLAlib/Ops/Examples/Integrator.lean`](https://github.com/NLA-lib/nlalib/blob/main/NLAlib/Ops/Examples/Integrator.lean) for steps 1–4 and [`IntegratorLink.lean`](https://github.com/NLA-lib/nlalib/blob/main/NLAlib/Ops/Examples/IntegratorLink.lean) for step 5.
The code below is quoted from those files; `…` marks a proof or a field left out of this page.


## 1. Name the operations

The integrator needs a product with $\mathbf{A}$ and a vector update.
We list them, and nothing else, as a closed type:

```
inductive MyOperation where
  | matvec   -- matvec [n, n] (x) → (y)
  | axpy     -- axpy [n] (α, x, y) → (y)
```

These are names only: `MyOperation.matvec` has no fields, so it carries no matrix, no error bound and no cost.
Its meaning is attached in step 3.


## 2. Write the routines

A routine is written with NLA-lib's `routine%` notation.
Its header is its interface: the dimensions in brackets, then each operand with its length.
An operand named only on the left of `→` is *read*; one named only on the right is *written*; one named on both sides is *updated in place*.

A step is a call of each operation; the integrator is $N$ steps.

```
/-- One step: X ← X + h · (A X). -/
def myStep : Routine MyOperation Empty := noted% routine% [n] (h : 1, X : n) → (X) {
  let Y ← alloc n;
  call MyOperation.matvec [n, n] (X) → (Y);
  call MyOperation.axpy [n] (h, Y, X) → (X)
}

/-- N steps. -/
def myIntegrate : Routine MyOperation Empty := noted% routine% [n, N] (h : 1, X : n) → (X) {
  for t < N { run myStep [n] (h, X) }
}
```

`Empty` is the type of tests: these routines never branch on data.
`run myStep [n] (h, X)` runs the tree of `myStep` on those operands, and `noted%` keeps the names in the tree for printing, with no effect on a run.
The tree is the same for every $n$ and $N$, and apart from control flow and the scratch vector `Y`, everything it does is a call of an operation: it never sees a number except through what those calls write.

The interface is not a comment: it fixes what a caller must supply and what the routine may touch.
`myIntegrate` reads one cell `h`, reads and writes $n$ cells `X`, writes nothing else and draws no random numbers; an operand that is written is in a different buffer from every other operand.

**The program.** A *program* is a routine run on the buffers of a problem: the sizes are its dimensions and the supplied buffers, in order, are its operands.

```
/-- The program: sizes n and N, buffers h and X. -/
def myProgram : Program MyOperation Empty 2 2 := myIntegrate.close 2 2
```

**The problem** is derived from the routine: we state the mathematical inputs, which of them are accepted, and what each buffer holds.

```
def myDomain : myIntegrate.Domain ℝ 2 2 where
  valid _ := True                              -- every n and N
  In d := ℝ × (Fin (d 0) → ℝ)                  -- the inputs: a step h and a vector x₀
  accepts _ _ := True                          -- all of them
  slot d := ![.stored Codec.scalar Prod.fst,   -- the buffer h holds the step
              .stored (Codec.vector (d 0)) Prod.snd]   -- the buffer X holds the vector
  …  -- each slot fits its operand; the inputs are determined by the buffers

def myProblem : Problem ℝ 2 2 := myDomain.problem
```

A slot is `stored` (an encoded input), `derived` (words computed from the inputs by a stated formula) or `blank` (uninitialised cells, for an operand that is only written).
There is no other way to fill a buffer, so a problem cannot quietly supply part of the answer.


## 3. Define the model

**Contracts.** A contract of an operation has two parts: a relation between the blocks a call reads and the blocks it writes, a `BlockRel`, and an *admission* saying which operands a call may be given.
For matvec we promise a product with $\mathbf{A}$ accurate to $\delta$ in norm; for axpy, an update accurate to $e$ in each entry.

```
/-- matvec [n, n] (x) → (y):  ‖A x − y‖ ≤ δ ‖x‖. -/
def myMatvecRel (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ : ℝ) : BlockRel ℝ where
  nd := 2
  inLens d := [d.headD 0]
  outLens d := [d.headD 0]
  rel d X _ Y := match X, Y with
    | [x], [y] => let n := d.headD 0
        ‖WithLp.toLp 2 (A n *ᵥ decv id n x - decv id n y)‖ ≤
          δ * ‖WithLp.toLp 2 (decv id n x)‖
    | _, _ => False

/-- axpy [n] (α, x, y) → (y):  |zᵢ − (yᵢ + α xᵢ)| ≤ e (|yᵢ| + |α xᵢ|). -/
def myAxpyRel (e : ℝ) : BlockRel ℝ where
  nd := 1
  inLens d := [1, d.headD 0, d.headD 0]
  outLens d := [d.headD 0]
  rel d X _ Y := match X, Y with
    | [[a], x, y], [z] => ∀ i < d.headD 0,
        |vec z i - (vec y i + a * vec x i)| ≤ e * (|vec y i| + |a * vec x i|)
    | _, _ => False
```

The matrix $\mathbf{A}$ and the allowances $\delta$ and $e$ are parameters of the contracts, not of the routines: the tree never reads the entries of $\mathbf{A}$.
Norms of vectors are Euclidean, and $\|\mathbf{A}\|$ is the operator norm they induce.

The admissions are NLA-lib's (`NLAlib/Ops/Catalog/Blas1.lean`): matvec writes its result apart from its input (`OutApart`), and axpy updates its last input in place, with the other two in other buffers (`InPlace`).
An admission is the operation-side form of a routine's interface, and step 5 uses it that way.

**Costs.** NLA-lib *counts* every call of each operation at its dimensions and every structural instruction (loop round, frame, allocation, index evaluation); the count comes from the tree alone.
The model then *weighs* the count with a `ResourceModel`, and the *work* is the weighted sum.
We weigh a matvec at $[n, n]$ as $2n^2$, an axpy at $[n]$ as $2n$, and each structural instruction as $1$.

```
def myWork : MyOperation → List ℕ → ℕ
  | .matvec, d => 2 * d.headD 0 ^ 2
  | .axpy, d => 2 * d.headD 0

def myResources : ResourceModel MyOperation Empty where
  formats := [.cell]
  operation
    | .matvec => ⟨[.cell], [.cell]⟩
    | .axpy => ⟨[.cell, .cell, .cell], [.cell]⟩
  -- neither operation needs scratch space of its own
  workspace _ _ := 0
  operationWork := myWork
  operationSpan := myWork
  coreWork _ _ := 1
  coreSpan _ _ := 1
  …  -- the (empty) tests, and three proofs that a span is at most the work
```

**Memory** is tracked separately, as the *peak* scratch space in use above the input buffers.
It comes from allocations in the tree (`let Y ← alloc n` holds its cells while its body runs) and from each call's `workspace`, which the model declares; here it is $0$.
Each buffer has a *format* giving the bytes a cell is charged; here every buffer is the one-byte `.cell`, so bytes and cells coincide.
Space used one statement after another, including every round of a loop, is reused, so `Y` costs $n$ cells, not $Nn$; only nesting adds.
NLA-lib computes this bound from the tree as `staticPeak`, as it computes the count as `staticCost`.

**The model.** An `AccessModel` attaches a contract to every name, fixes the costs, and carries a *witness*: a proof that at every input some implementation satisfies all the contracts at once.

```
noncomputable def myModel (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ)
    (hδ : 0 ≤ δ) (he : 0 ≤ e) : AccessModel MyOperation Empty myProblem where
  word := 0
  operation _ _
    | .matvec => (myMatvecRel A δ).spec (OutApart fun _ => True)
    | .axpy => (myAxpyRel e).spec (InPlace fun _ => True)
  query _ _ q := nomatch q
  resources := myResources
  -- the witness: the exact product and the exact update
  realize _ _ _ := ⟨Interp.ofFns (myExact A), fun o => by
    cases o
    · exact myExact_matvec A hδ
    · exact myExact_axpy A he, fun q => nomatch q⟩
```

An implementation of the operations is an *interpretation*, `Interp`; `I.Satisfies … o C` says that `I`'s version of the operation `o` satisfies the contract `C`.

**The witness.** `realize` is a proof obligation: here, the exact product and update (`myExact A`) satisfy both contracts, since their errors are $0$ and $\delta, e \ge 0$; that is why `myModel` takes `hδ` and `he`.
It matters because a certificate says "for every implementation satisfying the contracts": with $\delta = -1$ no implementation would, and every bound would be provable.


## 4. State what the routine does, and certify it

There are two statements: a judgment about the routine wherever it is called, and a certificate about one run from the problem's initial memory, with its cost.
The second follows from the first.

### The routine meets its specification

A routine's *specification* is a precondition and a postcondition on the contents of its operands.
It mentions no memory, no addresses and no tree.
The error of one step, relative to the norm of the vector, is
$$
\eta = |h|\delta + e\bigl(1 + |h|(\|\mathbf{A}\| + \delta)\bigr),
$$
`myEta A δ e h` in the code, and the specification of the integrator is

```
noncomputable def myIntegrateSpec (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ) :
    Routine.Spec ℝ :=
  spec% [n, N] ([h], x₀) → (xT) ensures
    ‖WithLp.toLp 2 (decv id n xT - ((1 + h • A n) ^ N) *ᵥ decv id n x₀)‖ ≤
      ((‖1 + h • A n‖ + myEta (A n) δ e h) ^ N - ‖1 + h • A n‖ ^ N) *
        ‖WithLp.toLp 2 (decv id n x₀)‖
```

`R.Meets I S` is NLA-lib's one judgment about a routine: under the interpretation `I`, on any memory and any operands that fit the interface, the tree of `R` runs to completion, changes nothing outside the operands it writes, draws exactly the random numbers it declares, and leaves contents that satisfy the postcondition of `S`.

::: theorem
**Theorem (`myIntegrate_meets`).**
Let $\mathbf{G} = \mathbf{I} + h\mathbf{A}$ and $g = \|\mathbf{G}\|$.
For every implementation of matvec and axpy that satisfies the contracts, the integrator, called at any $n$, $N$ and operands $h$, $\mathbf{x}_0$, runs to completion, writes only $\mathbf{x}$, and leaves there $\mathbf{x}_N$ with
$$
\|\mathbf{x}_N - \mathbf{G}^N\mathbf{x}_0\| \le \bigl((g + \eta)^N - g^N\bigr)\|\mathbf{x}_0\|.
$$

```
theorem myIntegrate_meets (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ) (hδ : 0 ≤ δ)
    (he : 0 ≤ e) {I : Interp MyOperation Empty ℝ}
    (hmatvec : I.Satisfies .total .matvec ((myMatvecRel A δ).spec (OutApart fun _ => True)))
    (haxpy : I.Satisfies .total .axpy ((myAxpyRel e).spec (InPlace fun _ => True))) :
    myIntegrate.Meets I (myIntegrateSpec A δ e) := by
  routine_intro [n, N] (h, X) reads (hs, xs)
  …  -- the loop, with one `call` of the step's judgment in each round
```
:::

*Proof sketch.*
The bound uses the two contracts and nothing else.
`myStep` has its own judgment, `myStep_meets`: one step computes $\mathbf{G}\mathbf{x}_t$ plus an error of norm at most $\eta\|\mathbf{x}_t\|$.
That error is $h$ times the matvec error, at most $|h|\delta\|\mathbf{x}_t\|$, plus the axpy error, whose entries are at most $e(|x_i| + |h||(\mathbf{A}\mathbf{x}_t)_i + \text{matvec error}_i|)$ and whose norm is therefore at most $e\bigl(1 + |h|(\|\mathbf{A}\| + \delta)\bigr)\|\mathbf{x}_t\|$.
The integrator's proof never looks inside `myStep`: each round *calls* `myStep_meets` and receives the block it wrote with its postcondition; the errors then propagate through $\mathbf{G}$.

This is what makes routines plug together: the judgment holds on any memory and operands, and says what the routine does *not* touch, so the same theorem serves a caller and the certificate below.

### The certificate

A `Specification` lists the claims about one run: a bound for each resource, and a condition on the final memory.
Here `d` holds the sizes ($n$ is `d 0`, $N$ is `d 1`), `x` the input ($h$ is `x.val.1.1`, $\mathbf{x}_0$ is `x.val.1.2`), and `μ` the final memory:

```
-- accuracy: the buffer X holds a vector x_N within the bound of myIntegrateSpec
def myGood (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ) (d : Fin 2 → ℕ)
    (x : myProblem.Input d) (μ : Mem ℝ) : Prop :=
  ∃ xT, μ.store.readBlock 1 0 (d 0) = some xT ∧
    let G := 1 + x.val.1.1 • A (d 0)
    ‖WithLp.toLp 2 (decv id (d 0) xT - (G ^ d 1) *ᵥ x.val.1.2)‖ ≤
      ((‖G‖ + myEta (A (d 0)) δ e x.val.1.1) ^ d 1 - ‖G‖ ^ d 1) * ‖WithLp.toLp 2 x.val.1.2‖

-- work: N products weighing 2n², N updates weighing 2n, 28 structural instructions in
-- each round and 11 outside the loop
def myProgramWork (d : Fin 2 → ℕ) : ℕ := 2 * d 1 * d 0 ^ 2 + 2 * d 1 * d 0 + 28 * d 1 + 11

noncomputable def mySpec (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ) :
    Specification MyOperation Empty myProblem where
  good d x _ _ μ := myGood A δ e d x μ
  -- the count of calls and structural instructions, entry by entry
  budget := staticCost myProgram
  -- its weight, and the critical path: calls run one after another, so span = work
  work := myProgramWork
  span := myProgramWork
  -- scratch: the n cells of Y; memory: the scratch, h (1 cell) and X (n cells)
  scratch d := d 0
  memory d := 1 + 2 * d 0
```

`mySpec` proves nothing; it only states the claims.
The budget is the tree's own count; the other bounds are explicit polynomials in $n$ and $N$.

NLA-lib packages a program with a proof of its specification as an `Algorithm`, and builds one from a routine's judgment on its derived problem with `Routine.Domain.algorithm`:

```
noncomputable def myAlgorithm (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ) (δ e : ℝ)
    (hδ : 0 ≤ δ) (he : 0 ≤ e) :
    Algorithm (myModel A δ e hδ he) (mySpec A δ e) :=
  myDomain.algorithm (fun _ _ => myIntegrateSpec A δ e)
    (fun _ _ _ _ hI => myIntegrate_meets A δ e hδ he (hI.1 .matvec) (hI.1 .axpy))
    (fun _ _ _ _ _ => trivial)   -- the precondition holds at every accepted input
    …  -- the output condition follows from the postcondition
    (fun _ _ => le_rfl) (fun d _ => myProgram_peak d) (fun d _ => (work_myProgram d).le)
    (fun d _ => (span_myProgram d).le) …
```

That the buffers hold $h$ and $\mathbf{x}_0$ holds by construction of the problem, so what remains is that the postcondition, read on them, is `myGood`.
For the cost, NLA-lib proves once that no run exceeds `staticCost` and `staticPeak` of its tree; we prove that those are the polynomials of `mySpec` (next section).

::: theorem
**Theorem (what `myAlgorithm` states).**
For every $n$, $N$, input $(h, \mathbf{x}_0)$ and implementation of matvec and axpy that satisfies the contracts, `myProgram` runs to completion, and that one run satisfies:

1. *Accuracy.* The bound of `myIntegrate_meets`, on the buffer $\mathbf{x}$.
2. *Cost.* It makes no more calls and structural instructions than the tree contains, `staticCost myProgram`; its work and its span are at most $2Nn^2 + 2Nn + 28N + 11$.
3. *Memory.* Its scratch is at most $n$ cells, and its memory, with the $1 + n$ cells of input, at most $2n + 1$.

```
theorem myProgram_certifies
    (A : (n : ℕ) → Matrix (Fin n) (Fin n) ℝ)
    (δ e : ℝ) (hδ : 0 ≤ δ) (he : 0 ≤ e) :
    myProgram.Certifies (myModel A δ e hδ he) (mySpec A δ e) :=
  (myAlgorithm A δ e hδ he).correct
```
:::

`Certifies` is NLA-lib's (`NLAlib/Ops/Static.lean`); what "runs" means in it is spelled out [below](#what-the-definitions-rest-on).
The same claim stated on the mathematical inputs, `Inputs.Checked`, follows for every certificate on a derived problem (`myDomain.checked_all`).

The `Algorithm` *contains* `myProgram`: its type says "there is a program that meets `mySpec` in `myModel`", and proving it means handing over a program with its certificate.
That is how the library states its results, and what `Algorithm.link` in step 5 takes and returns.
It is a `def`, not a `theorem`, because a program is data.

### Explicitly bounding costs

The polynomials of items 2 and 3 come from theorems about the tree alone, which work out `staticCost` and `staticPeak`:

::: theorem
**Theorem (`myProgram_calls`).**
For every $n$ and $N$, the tree of `myProgram` contains $N$ matvec calls at $[n, n]$, $N$ axpy calls at $[n]$, and no other operation.

```
theorem myProgram_calls (d : Fin 2 → ℕ) :
    Count.original (staticCost myProgram d) =
      d 1 • (Count.one MyOperation.matvec [d 0, d 0] + Count.one MyOperation.axpy [d 0]) := by
  …  -- the proof
```
:::

`Count.original` sets the structural instructions aside and keeps the calls.

::: theorem
**Theorem (`myProgram_peak`).**
For every $n$ and $N$, the scratch of the tree of `myProgram` is at most $n$ cells.

```
theorem myProgram_peak (d : Fin 2 → ℕ) : staticPeak myResources myProgram d ≤ d 0 := by
  …  -- the proof
```
:::

The $n$ cells are `Y`, reused by every round; it is not an equality because when $N = 0$ nothing is allocated.

::: theorem
**Theorem (`work_myProgram`, `span_myProgram`).**
Weighted by `myResources`, the count of the tree is exactly $2Nn^2 + 2Nn + 28N + 11$: the $N$ products and $N$ updates, $28$ structural instructions in each round (the round itself, the frame of the step, the allocation of `Y`, and the index and operand evaluations of the two calls) and $11$ outside the loop.
Calls run one after another, so the span is the same.

```
theorem work_myProgram (d : Fin 2 → ℕ) :
    myResources.work (staticCost myProgram d) = myProgramWork d := by
  …  -- the proof
```
:::

Together with the certificate: every run makes at most $N$ matvec calls and $N$ axpy calls, with work at most $2Nn^2 + 2Nn + 28N + 11$, and uses at most $n$ cells of scratch and $2n + 1$ in all.

When every operation and structural instruction weighs at most one, `Routine.certify` goes further: it takes the same judgment and returns a certificate whose work polynomial the Lean kernel computes from the tree, with no cost statement from the author.

## 5. Go down a level

The certificate holds for any implementation of matvec and axpy that satisfies the contracts.
To say what happens in floating point arithmetic, we implement axpy with rounded scalar operations and link; matvec stays an operation, as for a matrix-free $\mathbf{A}$.

Implementing axpy is steps 1–4 again, one level down: new operations (scalar arithmetic, and matvec), a routine (a loop over the entries, already in the library), a model (the standard model of floating point arithmetic with unit roundoff $u$), and a judgment:

```
inductive MyLowOperation where
  | scalar (o : ScalarOp)
  | matvec

/-- y ← y + α x, one rounded multiplication and one rounded addition per entry. -/
def myAxpy : Routine MyLowOperation Empty := axpyLoopRoutine

theorem myAxpy_meets {M : Machine ℝ} {I : Interp MyLowOperation Empty ℝ} (hI : IsScalar M I)
    {u : ℝ} (hM : StdModel u id M) (hu : 0 ≤ u) :
    myAxpy.Meets I (.ofRel (myAxpyRel ((1 + u) ^ 2 - 1)) fun _ => True) := by
  …  -- the library's judgment of the loop
```

The specification is the axpy contract itself, `myAxpyRel e` with $e = (1+u)^2 - 1$: each entry is rounded twice, $\bigl(y_i + \alpha x_i(1+\delta_1)\bigr)(1+\delta_2)$ with $|\delta_1|, |\delta_2| \le u$.
The interface of `myAxpy` also matches the contract's (three blocks read, the last updated in place), which NLA-lib checks (`myAxpy_implements`), so the routine's judgment *is* the operation's contract.

**Linking.** A table says what replaces each operation:

```
def myTable : Table MyOperation MyLowOperation Empty
  | .axpy => .inl myAxpy.impl
  | .matvec => .inr .matvec
```

`Algorithm.link` takes `myAlgorithm` and `myTable` and returns a certificate for `myProgram.link myTable` in the lower model.
Its one real obligation is `myAxpy_meets` with `myAxpy_implements`; the analysis of the iteration is not repeated.
Only the cost and memory are bounded again, since the linked program is a different tree.

::: theorem
**Theorem (after linking: `myLinkedAlgorithm`, `myLinkedProgram_calls`, `myLinkedProgram_peak`).**
`myProgram.link myTable` makes at most $N$ matvec calls, $Nn$ multiplications and $Nn$ additions, and no other operation; its work is at most $2Nn^2 + 22Nn + 34N + 11$; it uses at most $n + 1$ cells of scratch; and its output satisfies the accuracy bound of step 4 with $e = (1+u)^2 - 1$.

```
theorem myLinkedProgram_calls (d : Fin 2 → ℕ) :
    Count.original (staticCost myLinkedProgram d) =
      d 1 • (Count.one MyLowOperation.matvec [d 0, d 0] +
        d 0 • (Count.one (MyLowOperation.scalar .mul) [] +
          Count.one (MyLowOperation.scalar .add) [])) := by
  …  -- the proof
```
:::

If $\mathbf{A}$ were stored as data, matvec could be implemented and linked the same way.

## Why it is set up this way

**A routine can only call operations.**
A tree cannot hold a Lean function or a real number, and index expressions never read the data, so every effect on the data is a `call`.
The `EXACT_SUM` trick on the [design page](./), adding exactly and rounding once, cannot be written as a routine.

**A routine cannot choose its own cost or conditions.**
Its count comes from the tree, including the trees it calls, and the conditions for calling it come from its interface.
Its only free statement is its specification, which a reader can check against the mathematics.

**A model can still promise too much.**
A contract "write $\mathbf{G}\mathbf{x}$ exactly" would make the integrator exact, and a contract that depends on the input could write the answer in one call.
So NLA-lib names what to check: a model is *confined* if its contracts touch only their operands, *uniform* if they do not depend on the input, and *charged* if every call costs something (`NLAlib/Ops/Examples/Oracles.lean` shows what goes wrong without each).
Ours is confined and uniform; it is not charged, since an axpy of length $0$ weighs nothing, which is harmless because the work is bounded explicitly.

**A model cannot promise the impossible.**
That is what the witness of step 3 is for.

**What a reader checks.**
To trust a certificate, read the problem, the model and the specification; Lean checks the routine, its proof and the count.
`scripts/OpsPrograms.lean` prints all three for any certificate, with a summary of its properties (here `uniform=yes confined=yes charged=no`, `work=closed`), and the library does not let that summary get weaker.


## What the definitions rest on

Lean checks that a certificate follows from the definitions, not that the definitions mean what a reader thinks, so NLA-lib keeps that part small:

- **Execution is a set of rules**, one per construct with its charge (`NLAlib/Ops/Reference/Semantics.lean`, about two hundred lines); the evaluator the proofs use is proved to agree with them (`Program.certifies_iff_reference`).
- **The conventions are listed**, such as one word per cell and one unit per index operation, in [`docs/design/Ops-ReferenceReview.md`](https://github.com/NLA-lib/nlalib/blob/main/docs/design/Ops-ReferenceReview.md).
- **The trusted base is computed**: the declarations a certificate's statement depends on are recorded in `scripts/ops_trusted_base.txt`, and changing them needs sign-off.

No theorem says a model's costs are right: whether a matvec should weigh $2n^2$ is a modelling choice, made where the reader can see it.


## What NLA-lib provides

We wrote each piece ourselves to show how they fit.
In practice you rarely need to: NLA-lib has standard operations (scalar arithmetic, level-one BLAS, matrix–vector and matrix products, QR) with their contracts, standard implementations of them as routines, such as the axpy loop we used, and standard operation models, both exact and in floating point arithmetic.
Using them also means less to trust: the standard models are shared by every certificate in the library, and are proved confined, uniform (or name their oracle) and charged (`NLAlib/Ops/Profiles/Confined.lean`), so a reader who has checked them once only has to read your problem and specification.

To write a routine of your own, start with [`docs/contributing/routines.md`](https://github.com/NLA-lib/nlalib/blob/main/docs/contributing/routines.md); the library's conjugate gradient certificate, `NLAlib/Krylov/CG/HSCG/Carried/Certification.lean`, has the same shape as the integrator's.
