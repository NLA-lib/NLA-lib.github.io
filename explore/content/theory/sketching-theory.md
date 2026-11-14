---
kind: theory
id: sketching-theory
title: Embeddings and sketch guarantees
summary: Johnson–Lindenstrauss, subspace embeddings, approximate matrix multiplication, and projection-cost
  preservation.
status: outline
parents:
- probability
- matrix-analysis
prerequisites:
- subspaces
- concentration
module_prefixes:
- NLAlib.Sketching.Gaussian
- NLAlib.Sketching.Sparse
- NLAlib.Sketching.Structured
- NLAlib.Sketching.Properties
- NLAlib.Sketching.Sampling
---

The right sketch property depends on what the algorithm must preserve. A subspace embedding preserves all vector norms in one subspace. Approximate matrix multiplication controls a product, while projection-cost preservation supports comparisons between low-rank subspaces.

::: definition name="Subspace embedding"
A matrix $\mathbf S$ is an embedding of a subspace $V$ with squared-norm distortion $\varepsilon$ if

$$(1-\varepsilon)\|\mathbf x\|_2^2\le\|\mathbf S\mathbf x\|_2^2\le(1+\varepsilon)\|\mathbf x\|_2^2\qquad\text{for every }\mathbf x\in V.$$

An oblivious distribution chooses $\mathbf S$ independently of the fixed target subspace, with a stated success probability. The dimension and probability requirements differ among sketch laws.
:::

## Background

{{ generated:prerequisites }}

## Results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
