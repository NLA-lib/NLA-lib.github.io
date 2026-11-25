---
kind: statement
id: nlalib-nystrom-254f7f6f
uid: 254f7f6f-1199-596d-9347-4d32f1eab873
---

::: definition decl:NLAlib.nystrom name="Nyström approximation"
For a Hermitian positive-semidefinite matrix $\mathbf{A}$ and test matrix $\mathbf\Omega$, form

$$\widehat{\mathbf{A}}=\mathbf{A}\mathbf\Omega(\mathbf\Omega^{\mathsf{H}}\mathbf{A}\mathbf\Omega)^{\dagger}\mathbf\Omega^{\mathsf{H}}\mathbf{A}.$$

The symbol $\dagger$ denotes the Moore–Penrose pseudoinverse, allowing a rank-deficient middle matrix. Sampling columns is a special choice of the test matrix.
:::
