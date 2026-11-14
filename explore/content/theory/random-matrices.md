---
kind: theory
id: random-matrices
title: Random matrices and sketch laws
summary: Gaussian matrices, Haar frames, CountSketch, and subsampled randomized Hadamard transforms.
status: outline
order: 15
parents:
- probability
module_prefixes:
- NLAlib.RandomMatrix
---

A sketch guarantee depends on the law of the random matrix, including its scaling. Gaussian entries, orthonormal random frames, random signs, and sparse hashes preserve geometry in different ways.

::: definition name="Gaussian sketches and Haar frames"
A standard real Gaussian matrix has independent $N(0,1)$ entries. A Haar frame is a random orthonormal frame whose distribution is invariant under orthogonal or unitary changes of coordinates. These are different laws: orthonormalizing a Gaussian matrix changes the representation and requires the corresponding distributional result. Complex Gaussian scaling is specified separately in the relevant law.
:::

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
