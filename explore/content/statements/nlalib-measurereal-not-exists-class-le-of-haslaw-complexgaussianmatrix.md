---
kind: statement
id: nlalib-measurereal-not-exists-class-le-of-haslaw-complexgaussianmatrix
uid: d12d207c-4b10-5d38-b3af-794f3ecfb298
---

::: theorem decl:NLAlib.measureReal_not_exists_class_le_of_hasLaw_complexGaussianMatrix name="The diagonalization class, from the two tails" id=class
Let records $c_1$ and $c_2$ bound the [gap tail](/explore/statements/d8fd5d15-a8e2-53c0-aaf5-f021e9b3cb9b/) and the [condition tail](/explore/statements/33c3f20b-3401-544f-aaa4-a0644553f22e/). Let $\gamma>0$, $0<t_1\le\gamma$ and $0<t_2\le1$, and put $K=(\|\mathbf{M}\|_2+4\gamma)/\gamma$. Then $\mathbf{M}+\gamma n^{-1/2}\mathbf{G}$ has no diagonalization $\mathbf{V}\operatorname{diag}(\mathbf{d})\mathbf{V}^{-1}$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le1/t_2$ and $|d_i-d_j|\ge t_1$ for $i\ne j$ with probability at most

$$\bar C_1n^{\bar a_1}(t_1/\gamma)^{\bar b_1}\bigl(K+\log(\gamma/t_1)\bigr)^{\bar c_1}+\bar C_2n^{\bar a_2}t_2^{\bar b_2}\bigl(K+\log(1/t_2)\bigr)^{\bar c_2},$$

where $(\bar C_i,\bar a_i,\bar b_i,\bar c_i)$ is the record $c_i$ normalized. No norm condition is needed: when $\|\mathbf{M}\|_2<2\gamma$ the tails are applied to $\mathbf{M}+4\gamma\mathbf{I}$.
:::
