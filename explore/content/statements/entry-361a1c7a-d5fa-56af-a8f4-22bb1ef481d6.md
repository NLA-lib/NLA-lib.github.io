---
kind: statement
id: entry-361a1c7a-d5fa-56af-a8f4-22bb1ef481d6
uid: 361a1c7a-d5fa-56af-a8f4-22bb1ef481d6
---
::: theorem result:preconditioned-lanczos-recurrence name="The preconditioned recurrence is the split recurrence"
For Hermitian $\mathbf{A}$ and any
$\mathbf{C}$ with $\mathbf{M} = \mathbf{C}\mathbf{C}^{\mathsf{H}}$, the computed
$\mathbf{z}_j$ are $\mathbf{C}\mathbf{q}_j$ for the canonical Lanczos basis of
$\mathbf{C}^{\mathsf{H}}\mathbf{A}\mathbf{C}$ from $\mathbf{C}^{\mathsf{H}}\mathbf{b}$, every $q$,
with no breakdown hypothesis and no invertibility of $\mathbf{C}$: the matrix of the
$\mathbf{z}_j$ computed by $q$ steps from $\mathbf{b}$ is
$\mathbf{C}\,\mathsf{arnoldiMatrix}(\mathbf{C}^{\mathsf{H}}\mathbf{A}\mathbf{C},
\mathbf{C}^{\mathsf{H}}\mathbf{b}, q)$.
The inherited locator requires verification.
:::
