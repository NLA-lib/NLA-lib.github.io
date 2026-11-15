---
kind: algorithm
id: hutchpp
title: Hutch++
summary: Combine a low-rank approximation with residual trace estimation.
status: outline
order: 19
theory:
- random-matrices
- concentration
library_algorithm: hutchpp
uses:
- girard-hutchinson
- qr
search_aliases:
- Hutch plus plus
- trace estimation
source_guides:
- docs/algorithms/HutchPlusPlus.md
result_ids:
- hutchpp-unbiased
---

Combine a low-rank approximation with residual trace estimation.

{{ generated:source-guides }}

## Implementations

{{ generated:implementations }}

## Definition

::: definition decl:NLAlib.hutchpp name="Hutch++"
Choose a range sketch $\mathbf S$ and let $\mathbf P$ be the orthogonal projector onto $\operatorname{range}(\mathbf A\mathbf S)$. Compute the captured trace $\operatorname{tr}(\mathbf P\mathbf A)$ and add a Girard–Hutchinson estimate, with fresh probes, of $\operatorname{tr}((\mathbf I-\mathbf P)\mathbf A(\mathbf I-\mathbf P))$. The low-rank part and residual estimator have separate roles; the probability results specify the required independence and distribution.
:::



## Components

{{ generated:components }}

## Mathematical guarantees

::: theorem result:hutchpp-unbiased name="Unbiasedness with independent residual probes"
Suppose the range sketch is almost everywhere measurable, the residual probe matrix is independent of it and has at least one column, and each residual probe is square integrable and isotropic. For every square $\mathbf A$,

$$\mathbb E[\mathsf{hutch++}(\mathbf A)]=\operatorname{tr}(\mathbf A).$$

The range sketch can have any distribution. Residual probes need not be independent of one another for this expectation identity.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Appears under these tasks

{{ generated:task-membership }}
