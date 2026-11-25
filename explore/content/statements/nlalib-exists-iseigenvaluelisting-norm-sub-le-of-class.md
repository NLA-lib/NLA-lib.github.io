---
kind: statement
id: nlalib-exists-iseigenvaluelisting-norm-sub-le-of-class
uid: 57ec5e8f-9d28-5793-b43a-fa7abfa993c3
---

::: theorem decl:NLAlib.exists_isEigenvalueListing_norm_sub_le_of_class name="Forward error through a diagonalizable matrix"
Let $\mathbf{A}+\mathbf{E}_1=\mathbf{V}\operatorname{diag}(\mathbf{d})\mathbf{V}^{-1}$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le B$ and eigenvalues separated by $g>0$, and let $\|\mathbf{E}_2\|_2\le g/(16(n+1)B)$. Then every listing $\mathbf{r}$ of the eigenvalues of $\mathbf{A}+\mathbf{E}_1+\mathbf{E}_2$ is matched to a listing $\boldsymbol\lambda$ of those of $\mathbf{A}$ with

$$|r_i-\lambda_i|\le B\|\mathbf{E}_2\|_2+(2n+1)\bigl(2\|\mathbf{A}\|_2+\|\mathbf{E}_1\|_2\bigr)^{1-1/(n+1)}\|\mathbf{E}_1\|_2^{1/(n+1)}$$

for every $i$. The first term is the Bauer–Fike perturbation of the diagonalizable matrix; the second is the Ostrowski–Elsner matching for the rest.
:::
