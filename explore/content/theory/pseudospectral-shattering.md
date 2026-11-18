---
kind: theory
id: pseudospectral-shattering
title: Pseudospectral shattering and Gaussian regularization
summary: A small complex Gaussian perturbation makes a matrix diagonalizable with a bounded eigenvector condition number and separated eigenvalues, with polynomial tails.
status: outline
order: 16
parents:
- random-matrices
- perturbation-theory
prerequisites:
- singular-values
- spectral-theory
module_prefixes:
- NLAlib.RandomMatrix.Shattering
search_aliases:
- Pseudospectral shattering
- Ginibre perturbation
- Gaussian regularization
- Eigenvector condition number tail
- Eigenvalue gap tail
---

A matrix can have eigenvalues that are arbitrarily ill conditioned, or no basis of eigenvectors at all. A small random perturbation removes both problems with high probability. For a deterministic $\mathbf M$ of order $n$, a scale $\gamma>0$ and a standard complex Gaussian matrix $\mathbf G$ (independent entries of mean square modulus one), the perturbation

$$\mathbf M+\gamma n^{-1/2}\mathbf G$$

has, outside an event of small probability, simple eigenvalues with all gaps above $t$ and an eigenvector matrix $\mathbf V$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le1/t$. This is *pseudospectral shattering* (Banks, Garza-Vargas, Kulkarni and Srivastava): the $\varepsilon$-pseudospectrum splits into small components, one around each eigenvalue. Randomized eigensolvers such as the [randomized shifted inverse iteration of BGS III](/explore/algorithms/inverse-iteration/implementations/small-eig/) perturb their input in this way, so that every later step can assume a diagonalizable matrix with a known condition number and eigenvalue separation.

The library proves the two tails in an elementary polynomial form. Its exponents are weaker than the printed ones, and the tails are stated so that sharper ones can replace them. This page collects the tails and the deterministic and probabilistic facts they are built from. It is meant to grow as further results are added.

## The two tails

::: theorem decl:NLAlib.measureReal_not_exists_isEigenvalueListing_le_le_log_sq_of_hasLaw_complexGaussianMatrix name="Eigenvalue gap of a Ginibre perturbation" id=gap-tail
Let $\mathbf G$ be a standard complex Gaussian matrix of order $n$, $\mathbf M$ deterministic, $0<2\gamma\le\|\mathbf M\|_2$ and $0<t\le\gamma$. Then

$$\mathbb P\bigl[\text{no eigenvalue listing of }\mathbf M+\gamma n^{-1/2}\mathbf G\text{ has }|\lambda_i-\lambda_j|>t\text{ for all }i\ne j\bigr]\le10000e\,n^5\sqrt{t/\gamma}\Bigl(\frac{\|\mathbf M\|_2}{\gamma}+\log\frac{\gamma}{t}\Bigr)^2.$$
:::

This is a weaker polynomial form of Lemma B.1 of BGS III. The exponent of $t/\gamma$ is $1/2$ here and $2$ in the source. The proof covers a disk containing the spectrum by a net of $36(R/t)^2$ points. Two eigenvalues close to a net point force a small second-smallest singular value (see [eigenvalue clustering](#clustering) below), whose tail is of fourth order. The proof then combines the condition tail below at the cutoff $(\gamma/t)^{1/4}$ with a norm cutoff.

::: theorem decl:NLAlib.measureReal_not_exists_pseudoConditionNumber_le_le_log_sq_of_hasLaw_complexGaussianMatrix name="Eigenvector condition number of a Ginibre perturbation" id=condition-tail
Let $\mathbf G$ be a standard complex Gaussian matrix of order $n$, $\mathbf M$ deterministic, $0<2\gamma\le\|\mathbf M\|_2$ and $0<t\le1$. Then

$$\mathbb P\bigl[\mathbf M+\gamma n^{-1/2}\mathbf G\text{ has no diagonalization }\mathbf V\operatorname{diag}(\mathbf d)\mathbf V^{-1}\text{ with }\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le1/t\bigr]\le128e\,n^3t^2\Bigl(\frac{\|\mathbf M\|_2}{\gamma}+\log\frac1t\Bigr)^2.$$
:::

This is Theorem 1.5 of Banks, Kulkarni, Mukherjee and Srivastava in a polynomial-tail form. The proof integrates the area of the $\varepsilon$-pseudospectrum inside a disk over the Gaussian law, using Fubini and the shifted smallest-singular-value tail. Fatou's lemma bounds the expected lower limit of the normalized areas. A matrix without a good diagonalizer has a large lower limit, by the [pseudospectral area inequality](#area-inequality), so Markov's inequality applies without choosing eigenvectors measurably.

::: theorem decl:NLAlib.measureReal_not_exists_class_le_of_hasLaw_complexGaussianMatrix name="The diagonalization class, from the two tails" id=class
Let records $c_1$ and $c_2$ bound the gap tail and the condition tail. Let $\gamma>0$, $0<t_1\le\gamma$ and $0<t_2\le1$, and put $K=(\|\mathbf M\|_2+4\gamma)/\gamma$. Then $\mathbf M+\gamma n^{-1/2}\mathbf G$ has no diagonalization $\mathbf V\operatorname{diag}(\mathbf d)\mathbf V^{-1}$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le1/t_2$ and $|d_i-d_j|\ge t_1$ for $i\ne j$ with probability at most

$$\bar C_1n^{\bar a_1}(t_1/\gamma)^{\bar b_1}\bigl(K+\log(\gamma/t_1)\bigr)^{\bar c_1}+\bar C_2n^{\bar a_2}t_2^{\bar b_2}\bigl(K+\log(1/t_2)\bigr)^{\bar c_2},$$

where $(\bar C_i,\bar a_i,\bar b_i,\bar c_i)$ is the record $c_i$ normalized. No norm condition is needed: when $\|\mathbf M\|_2<2\gamma$ the tails are applied to $\mathbf M+4\gamma\mathbf I$.
:::

The tails are recorded as four numbers $(C,a,b,c)$, the bound $C\,n^a\,s^b\,(K+\log(1/s))^c$ (`PolyLogTail`). The predicates `BoundsGinibreGap` and `BoundsGinibreCondition` say that a record bounds the gap or the condition tail. The library proves them for the records `ginibreGapTail` $=(10000e,5,1/2,2)$ and `ginibreConditionTail` $=(128e,3,2,2)$ (`boundsGinibreGap_ginibreGapTail`, `boundsGinibreCondition_ginibreConditionTail`). The theorems that use the tails take a record as a hypothesis, and each has an unconditional corollary at the proved records. So a sharper tail, such as the printed gap exponent $2$, plugs in without changing them.

## Ingredients

### Small balls and singular values

::: theorem decl:NLAlib.measureReal_norm_mulVec_add_le_le_of_hasLaw_complexGaussianVector name="Shifted small ball" id=small-ball
Let $\mathbf g$ be a standard complex Gaussian vector, $\mathbf P$ a nonzero orthogonal projector and $\mathbf c$ a deterministic vector. Then $\mathbb P\bigl[\|\mathbf P(\mathbf g+\mathbf c)\|\le s\bigr]\le s^2$ for every $s\ge0$.
:::

::: theorem decl:NLAlib.measureReal_singularValues_add_smul_le_le_exp_one_mul_of_hasLaw_complexGaussianMatrix name="Smallest singular value of a shifted Ginibre matrix" id=least-singular-value
For any deterministic $\mathbf M$ of order $n$ and $\gamma>0$, $x\ge0$,

$$\mathbb P\bigl[\sigma_{\min}(\mathbf M+\gamma n^{-1/2}\mathbf G)\le x\bigr]\le e\,n^2x^2/\gamma^2.$$
:::

The source of this bound is Lemma 3.3 of Banks, Kulkarni, Mukherjee and Srivastava, which has constant $1$ in place of $e$. The proof here is the probe argument of Sankar, Spielman and Teng, in its complex version.

::: theorem decl:NLAlib.measureReal_singularValues_add_smul_le_le_pow_four_of_hasLaw_complexGaussianMatrix name="Second-smallest singular value" id=second-singular-value
For any deterministic $\mathbf M$ of order $n\ge2$ and $\gamma>0$, $x\ge0$, the second-smallest singular value satisfies

$$\mathbb P\bigl[\sigma_{n-2}(\mathbf M+\gamma n^{-1/2}\mathbf G)\le x\bigr]\le n^5(x/\gamma)^4.$$

The singular values are indexed from $0$ in non-increasing order.
:::

### Pseudospectral area

::: theorem decl:NLAlib.ofReal_sum_sq_le_liminf_measure_inter_ball_of_mul_eq_mul_diagonal name="Area of the pseudospectrum and eigenvalue condition numbers" id=area-condition
For a diagonalizable matrix with distinct eigenvalues strictly inside a disk of radius $R$, the sum of the squared condition numbers of its eigenvalues is at most the lower limit, as $\varepsilon\to0$, of $4/(\pi\varepsilon^2)$ times the area of $\{z:\sigma_{\min}(z\mathbf I-\mathbf A)\le\varepsilon\}$ inside the disk.
:::

::: theorem decl:NLAlib.ofReal_sq_div_card_le_liminf_measure_inter_ball_of_not_exists name="Pseudospectral area inequality" id=area-inequality
Let $\mathbf A$ of order $n$ have simple spectrum, $\|\mathbf A\|_2<R$ and $B>0$. If $\mathbf A$ has no diagonalization $\mathbf V\operatorname{diag}(\mathbf d)\mathbf V^{-1}$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le B$, then for every positive sequence $\varepsilon_j\to0$,

$$\frac{B^2}n\le\liminf_{j\to\infty}\frac4{\pi\varepsilon_j^2}\operatorname{area}\bigl(\{z:\sigma_{\min}(z\mathbf I-\mathbf A)\le\varepsilon_j\}\cap\{|z|<R\}\bigr).$$
:::

Both are Lemmas 3.1 and 3.2 of Banks, Kulkarni, Mukherjee and Srivastava, with the sufficient factor $4$ of the local area estimate.

### Eigenvalue clustering

::: theorem decl:NLAlib.singularValues_le_mul_pseudoConditionNumber_of_mul_eq_mul_diagonal name="Two close eigenvalues force a small second singular value" id=clustering
If a diagonalizer $\mathbf V$ of $\mathbf A$ has two distinct columns whose eigenvalues are within $r\ge0$ of $z$, then the second-smallest singular value of $z\mathbf I-\mathbf A$ is at most $r\,\|\mathbf V\|_2\|\mathbf V^{-1}\|_2$.
:::

::: theorem decl:NLAlib.exists_mem_singularValues_le_of_not_exists_isEigenvalueListing name="A net detects close eigenvalue pairs" id=clustering-net
Let $\mathbf A$ of order $n\ge2$ have a diagonalizer $\mathbf V$ with $\|\mathbf V\|_2\|\mathbf V^{-1}\|_2\le B$, let $\|\mathbf A\|_2<R$ and $r>0$, and let $Z$ be a finite set such that every point of the disk of radius $R$ is within $r/2$ of $Z$. If no eigenvalue listing of $\mathbf A$ has all gaps above $r$, then some $z\in Z$ has second-smallest singular value of $z\mathbf I-\mathbf A$ at most $2rB$.
:::

### Simple spectrum

::: theorem decl:NLAlib.ae_charpoly_separable_of_hasLaw_complexGaussianMatrix name="Almost surely simple spectrum" id=simple-spectrum
For any deterministic $\mathbf M$ and any complex $c\ne0$, the matrix $\mathbf M+c\,\mathbf G$ has simple spectrum almost surely: its characteristic polynomial is separable.
:::

## Formal definitions

{{ generated:definitions }}

## Background

{{ generated:prerequisites }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
