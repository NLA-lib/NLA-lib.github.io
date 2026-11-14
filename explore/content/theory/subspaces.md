---
kind: theory
id: subspaces
title: Subspaces and projectors
summary: Orthonormal bases, projectors, angles, and approximation by subspaces.
status: outline
order: 4
parents:
- matrix-analysis
module_prefixes:
- NLAlib.Matrix.Subspaces
---

Many numerical methods first select a subspace and then solve or approximate within it. The projector describes that choice independently of the basis used to represent it.

::: definition name="Orthogonal projection"
If $\mathbf Q$ has orthonormal columns, then $\mathbf P=\mathbf Q\mathbf Q^{\mathsf{H}}$ is the orthogonal projector onto their range: $\mathbf P^{\mathsf{H}}=\mathbf P$ and $\mathbf P^2=\mathbf P$. For any vector $\mathbf x$, the projected vector lies in the subspace and the residual $\mathbf x-\mathbf P\mathbf x$ is orthogonal to it. Principal angles compare two subspaces rather than particular choices of basis.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
