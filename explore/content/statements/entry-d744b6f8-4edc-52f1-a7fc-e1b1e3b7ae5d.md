---
kind: statement
id: entry-d744b6f8-4edc-52f1-a7fc-e1b1e3b7ae5d
uid: d744b6f8-4edc-52f1-a7fc-e1b1e3b7ae5d
---
::: theorem result:rank-one-eigenvalue-update name="Brauer's theorem"
A rank-one update along an eigenvector $\mathbf{x}$ of $\mathbf{A}$ with
eigenvalue $\mu$ moves $\mu$ to $\mu + \mathbf{y}^{\mathsf{T}}\mathbf{x}$ and leaves the other
eigenvalues in place, as an identity of characteristic polynomials over any commutative ring:
$$(X - \mu) \, p_{\mathbf{A} + \mathbf{x}\mathbf{y}^{\mathsf{T}}}(X)
  = (X - \mu - \mathbf{y}^{\mathsf{T}}\mathbf{x}) \, p_{\mathbf{A}}(X),$$
with $p_{\mathbf{M}}(X) = \det(X\mathbf{I} - \mathbf{M})$.
Over a field, a nonzero $\mathbf{x}$ implies that $X-\mu$ divides $p_{\mathbf{A}}$.
Cancelling this factor exhibits the common polynomial for the unchanged eigenvalues, including
their multiplicities. To write the update as $\mathbf{x}\mathbf{v}^{\mathsf{H}}$ over $\mathbb{C}$,
take `y = star v`.

Note: The cited theorem gives the complex case.
:::
