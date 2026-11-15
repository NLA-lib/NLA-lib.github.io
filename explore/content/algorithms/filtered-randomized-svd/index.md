---
kind: algorithm
id: filtered-randomized-svd
title: Filtered RSVD
summary: Apply a polynomial filter before constructing a randomized range approximation.
status: outline
order: 13
families:
- subspace-iteration-methods
theory:
- polynomial-approximation
- random-matrices
library_algorithm: filtered-rsvd
uses:
- randomized-svd
library_results: false
result_ids:
- filtered-range-finder-bound
---

Apply a polynomial filter before constructing a randomized range approximation. Subspace iteration is the monomial case. The bound for a general filter is also the comparison through which the gapped block Krylov bounds are proved: singular value by singular value, the error of randomized block Krylov iteration with $q$ blocks is at most that of the range finder at the test matrix $f(\mathbf A^{\mathsf{H}}\mathbf A)\mathbf\Omega$, for every polynomial $f$ of degree less than $q$.

## Implementations

{{ generated:implementations }}

## Definition

::: definition name="Filtered range-finder approximation"
Choose a spectral filter $g$ and a test matrix $\mathbf\Omega$. Form $\mathbf Y=\mathbf A g(\mathbf A^{\mathsf{H}}\mathbf A)\mathbf\Omega$ and return $\mathbf P_{\mathbf Y}\mathbf A=\mathsf{rsvd}\bigl(\mathbf A,g(\mathbf A^{\mathsf{H}}\mathbf A)\mathbf\Omega\bigr)$. Polynomial filters can be evaluated through matrix applications; the mathematical analysis also permits more general spectral filters. Power iteration is the special choice $g(\lambda)=\lambda^p$. Final rank truncation is a further choice.
:::

## Components

{{ generated:components }}

## Mathematical guarantees

::: theorem decl:NLAlib.integral_specNorm_sub_rsvd_aeval_sq_le_of_hasLaw_gaussianMatrix name="Expected spectral error for a polynomial filter" id=expected-spectral
Let $\mathbf A$ be a real matrix with $n$ columns and singular values $\sigma_0\ge\sigma_1\ge\cdots$, let $\mathbf X$ be an $n\times\ell$ matrix with independent standard normal entries, and let $r\le t$ with $t+2\le\ell$. Let $f$ be a real polynomial and $c>0$, $a$ real numbers with

$$|f(\sigma_i^2)|\ge c\quad\text{for } i<r,\qquad|f(\lambda)|\le a\quad\text{for } \lambda\in[0,\sigma_t^2].$$

Then

$$\mathbb E\bigl\|\mathbf A-\mathsf{rsvd}\bigl(\mathbf A,f(\mathbf A^{\mathsf{H}}\mathbf A)\mathbf X\bigr)\bigr\|_2^2\le\sigma_r^2+\Bigl(\frac{a}{c}\Bigr)^2\frac{t}{\ell-t-1}\,\|\mathbf A-[\mathbf A]_t\|_{\mathrm F}^2.$$

The bound is small when the filter is large on the head singular values and small on the tail interval. The deterministic bound for a general spectral filter, the Frobenius form, and the form in every unitarily invariant norm are listed below.
:::

## Further results

{{ generated:results }}

## Mathematical background

{{ generated:theory }}

## Family

{{ generated:families }}

## Appears under these tasks

{{ generated:task-membership }}
