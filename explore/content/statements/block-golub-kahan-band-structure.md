---
kind: statement
id: block-golub-kahan-band-structure
uid: 30ae638f-d7d8-5b6c-91f0-65d57ae2c0de
---

::: theorem result:block-golub-kahan-band-structure name="Band structure of the coefficients" id=band-structure
Over $\mathbb{K}=\mathbb{R}$ or $\mathbb{C}$, let $\mathbf{A}\in\mathbb{K}^{m\times n}$ and an initial block
$\boldsymbol{\Omega}\in\mathbb{K}^{n\times\ell}$ define an exact run of
[block Golub–Kahan bidiagonalization](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/)
for $q$ steps. Let $\mathbf{R}\in\mathbb{K}^{q\ell\times q\ell}$ and
$\mathbf{S}\in\mathbb{K}^{(q+1)\ell\times q\ell}$ be its left and right
coefficient matrices. Then:

1. $\mathbf{R}$ is upper triangular and vanishes above its $\ell$-th superdiagonal: $\mathbf{R}_{ic}=0$ for $i>c$ and for $c>i+\ell$.
2. $\mathbf{S}$ vanishes above its diagonal and below its $\ell$-th subdiagonal: $\mathbf{S}_{ic}=0$ for $i<c$ and for $i>c+\ell$.

Thus $\mathbf{R}$ and $\mathbf{S}^{\mathsf{H}}$ are zero outside the band $0\le\text{column}-\text{row}\le \ell$. For $\ell=1$, $\mathbf{S}^{\mathsf{H}}$ is upper bidiagonal.
:::
