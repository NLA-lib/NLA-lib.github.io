---
kind: statement
id: entry-dc8e0c8e-14ca-54b7-bf8d-4bea26c61c35
uid: dc8e0c8e-14ca-54b7-bf8d-4bea26c61c35
---
::: theorem result:left-right-eigenvectors name="Left-right eigenvector deflation"
If $\mathbf{A}\mathbf{x}=\mu\mathbf{x}$ and
$\mathbf{y}^{\mathsf{T}}\mathbf{A}=\mu\mathbf{y}^{\mathsf{T}}$ with
$\mathbf{y}^{\mathsf{T}}\mathbf{x}\ne0$, an invertible $\mathbf{S}$ has a column $\mathbf{x}$
and the corresponding inverse row
$$\frac{\mathbf{y}^{\mathsf{T}}}{\mathbf{y}^{\mathsf{T}}\mathbf{x}}.$$
That coordinate of
$\mathbf{S}^{-1}\mathbf{A}\mathbf{S}$ has diagonal entry $\mu$ and all other row and column
entries zero. The normalized outer product is the conjugate of that coordinate projector.
This generalizes the cited theorem to arbitrary fields and finite index types, with bilinear left
rows in place of conjugated columns.
Adapted from `NLAlib.exists_isolated_eigenvector_similarity` in `tchen-research/NLAlib` at
`77514ce42a0e437d837797a063ac161f41022730`.
:::
