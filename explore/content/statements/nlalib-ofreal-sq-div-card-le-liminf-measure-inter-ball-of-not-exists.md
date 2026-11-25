---
kind: statement
id: nlalib-ofreal-sq-div-card-le-liminf-measure-inter-ball-of-not-exists
uid: 81417ef6-1efe-5265-9d7a-7b1abb433e5b
---

::: theorem decl:NLAlib.ofReal_sq_div_card_le_liminf_measure_inter_ball_of_not_exists name="Pseudospectral area inequality" id=area-inequality
Let $\mathbf{A}$ of order $n$ have simple spectrum, $\|\mathbf{A}\|_2<R$ and $B>0$. If $\mathbf{A}$ has no diagonalization $\mathbf{V}\operatorname{diag}(\mathbf{d})\mathbf{V}^{-1}$ with $\|\mathbf{V}\|_2\|\mathbf{V}^{-1}\|_2\le B$, then for every positive sequence $\varepsilon_j\to0$,

$$\frac{B^2}n\le\liminf_{j\to\infty}\frac4{\pi\varepsilon_j^2}\operatorname{area}\bigl(\{z:\sigma_{\min}(z\mathbf{I}-\mathbf{A})\le\varepsilon_j\}\cap\{|z|<R\}\bigr).$$
:::
