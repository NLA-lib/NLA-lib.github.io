---
kind: statement
id: entry-8ede3e75-01f1-52ee-ac5e-09bd60a613a0
uid: 8ede3e75-01f1-52ee-ac5e-09bd60a613a0
---
::: theorem result:lanczos-fa-cg name="CG is Lanczos-FA for the inverse"
For every Hermitian $\mathbf{A}$:
$\mathsf{lanczosFA}(\mathbf{A}, x \mapsto x^{-1}, \mathbf{b}, q) =
\mathsf{cgIterate}(\mathbf{A}, \mathbf{b}, \mathbf{0}, q)$ (CG from the zero start), with
Lean's $0^{-1} = 0$ matching the
pseudoinverse junk value of `galerkinInverse`.
:::
