---
kind: statement
id: entry-9fed7e3a-b9a3-5d3f-882f-0ab58167f30f
uid: 9fed7e3a-b9a3-5d3f-882f-0ab58167f30f
---
::: theorem result:pminres-split-system name="Preconditioned MINRES is MINRES on the split system"
For invertible $\mathbf{A}$ and
$\mathbf{C}$ with $\mathbf{M} = \mathbf{C}\mathbf{C}^{\mathsf{H}}$ and
$\mathbf{C}\mathbf{y}_0 = \mathbf{x}_0$,
$\mathsf{pminresIterate}(\mathbf{A}, \mathbf{M}, \mathbf{b}, \mathbf{x}_0, q) =
\mathbf{C}\,\mathsf{gmresIterate}(\mathbf{C}^{\mathsf{H}}\mathbf{A}\mathbf{C},
\mathbf{C}^{\mathsf{H}}\mathbf{b}, \mathbf{y}_0, q)$. Invertibility of $\mathbf{A}$ makes both
minimisers unique; for singular $\mathbf{A}$ the two least-norm choices differ.
:::
