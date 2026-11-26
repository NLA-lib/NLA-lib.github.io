---
kind: statement
id: block-golub-kahan-band-structure
uid: 30ae638f-d7d8-5b6c-91f0-65d57ae2c0de
---

::: theorem result:block-golub-kahan-band-structure name="Band structure of the coefficients" id=band-structure
For an [exact run](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/) with block width $\ell$:

1. $\mathbf{R}$ is upper triangular and vanishes above its $\ell$-th superdiagonal: $\mathbf{R}_{ic}=0$ for $i>c$ and for $c>i+\ell$.
2. $\mathbf{S}$ vanishes above its diagonal and below its $\ell$-th subdiagonal: $\mathbf{S}_{ic}=0$ for $i<c$ and for $i>c+\ell$.

Thus $\mathbf{R}$ and $\mathbf{S}^{\mathsf{H}}$ are zero outside the band $0\le\text{column}-\text{row}\le \ell$. For $\ell=1$, $\mathbf{S}^{\mathsf{H}}$ is upper bidiagonal.
:::
