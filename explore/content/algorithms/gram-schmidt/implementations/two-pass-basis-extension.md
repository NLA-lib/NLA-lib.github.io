---
kind: implementation
id: two-pass-basis-extension
algorithm: gram-schmidt
title: Two-pass classical Gram–Schmidt basis extension
summary: Extend a stored basis by a block, column by column, with two classical passes and threshold deflation.
status: outline
order: 3
result_ids:
- cgs2-basis-extension
- cgs2-basis-extension-error
- basis-extension-gram-defect
- gram-defect-projector-distance
search_aliases:
- CGS2
- classical Gram–Schmidt with reorthogonalization
- block orthogonalization
- deflation
source_guides:
- docs/algorithms/Block-Golub-Kahan.md
---

This implementation extends a stored basis $\mathbf Q$ ($k$ columns of length $n$) by a block $\mathbf W$ of $\ell$ columns (the Lean statements name the block width `b`). Each column of the block is reduced twice, by classical Gram–Schmidt passes, against the stored basis followed by the new columns already written. A reduced column whose norm falls below a threshold relative to the input column is dropped: a zero column is stored. It is the orthogonalization scheme the library supplies for block Golub–Kahan bidiagonalization.

{{ generated:source-guides }}

## Algorithm

::: definition decl:NLAlib.CGS2.cgs2ExtendImpl name="Column-wise two-pass classical Gram–Schmidt with threshold deflation" id=algorithm
The dimensions are $[n,k,\ell]$; the inputs are the stored basis $\mathbf Q$ and the block $\mathbf W$; the outputs are the new block $\mathbf Q'$, the reduced block (overwriting $\mathbf W$), and the coefficient block $\mathbf C$ with $k+\ell$ rows. The threshold $\tau$ is a rational literal of the implementation. The new block is stored directly after the basis, so the basis and the new columns already written form one contiguous block.

For each column $c=0,\ldots,\ell-1$:

1. Save $\nu=\|\mathbf w_c\|$.
2. Set rows $k,\ldots,k+\ell-1$ of column $c$ of $\mathbf C$ to zero.
3. First pass: compute the coefficients of $\mathbf w_c$ against the $k+c$ stored columns, write them to rows $0,\ldots,k+c-1$ of column $c$ of $\mathbf C$, and reduce $\mathbf w_c$ in place.
4. Second pass: compute coefficients against the same columns into scratch and reduce $\mathbf w_c$ in place again.
5. Add the second coefficients to the first.
6. Compute $\beta=\|\mathbf w_c\|$ for the reduced column.
7. If $\beta\le\tau\nu$, store a zero column $\mathbf q'_c$ and leave the diagonal coefficient zero.
8. Otherwise store $\mathbf q'_c=\mathbf w_c/\beta$ and the diagonal coefficient $C_{k+c,c}=\beta$.

At $\tau=0$ the test is the exact zero guard. A dropped column remains a zero column of the basis. The scratch is $k+\ell$ coefficient cells and three scalar cells.
:::

## Model of arithmetic

The program uses scalar operations, level-one vector operations (dot product, vector update, norm, scaling, copy), and comparisons. The statements below are for two models: exact real arithmetic with exact level-one operations, where the threshold is $0$; and the standard model of rounded arithmetic with level-one error contracts and exact comparisons, where the threshold is positive. Scalars are real.

## Accuracy

The exact contract (an exact extension of a basis by a block) and the rounded contract with parameters $(\eta_0,\mu,\varepsilon)$ are defined on the block Golub–Kahan page. The first statement of each pair below is about decoded matrices; the second is about the program.

::: theorem result:cgs2-basis-extension name="Two exact passes give an exact extension"
Let $\mathbf Q$ be an arbitrary real or complex matrix with $k$ columns, $\mathbf W$ a block of $\ell$ columns, and write $\operatorname{su}(\mathbf M)$ for the strictly upper triangular part of $\mathbf M$. Suppose

$$\mathbf H_1=\mathbf Q^{\mathsf{H}}\mathbf W,\quad\mathbf R_1=\operatorname{su}(\mathbf Q'^{\mathsf{H}}\mathbf W),\quad\mathbf W_1=\mathbf W-\mathbf Q\mathbf H_1-\mathbf Q'\mathbf R_1,$$

$$\mathbf H_2=\mathbf Q^{\mathsf{H}}\mathbf W_1,\quad\mathbf R_2=\operatorname{su}(\mathbf Q'^{\mathsf{H}}\mathbf W_1),\quad\mathbf W_2=\mathbf W_1-\mathbf Q\mathbf H_2-\mathbf Q'\mathbf R_2,$$

and that each column of $\mathbf Q'$ is the corresponding column $\mathbf w$ of $\mathbf W_2$ divided by its norm, or the zero column when $\mathbf w=\mathbf 0$. Then $\mathbf Q'$ with coefficients $\mathbf H_1+\mathbf H_2$ and $\mathbf R_1+\mathbf R_2+\mathbf D$, where $\mathbf D$ is the diagonal matrix of the norms of the columns of $\mathbf W_2$, is an exact extension of $\mathbf Q$ by $\mathbf W$.

No hypothesis is made on $\mathbf Q$. Orthonormality of its nonzero columns enters only through the clause of the contract that preserves it.
:::

::: theorem decl:NLAlib.CGS2.cgs2Extend_exact_spec name="The program meets the exact contract at threshold zero" id=exact-execution
Under exact scalar arithmetic, exact level-one operations at every length, and exact comparisons, the implementation with threshold $\tau=0$ runs on all admitted operands of the extension operation, and its decoded basis, block, new block, and coefficients satisfy the exact extension contract. The stored basis is arbitrary: it may contain zero columns and need not be orthonormal on its support.
:::

::: theorem result:cgs2-basis-extension-error name="Column guarantees give the rounded contract"
Let $\mathbf Q$ be a real basis, $\mathbf W$ the block, $\mathbf W'$ the reduced block, $\mathbf Q'$ the new block, and $\mathbf H$, $\mathbf R$ the coefficients, with $\mathbf R$ upper triangular. For every column $c$ assume:

1. the step from $\mathbf w_c$ to $\mathbf w'_c$, with coefficients $(\mathbf H_c,\mathbf R_{<c,c})$, meets the single-vector guarantee on the support with parameters $(\eta_0,\varepsilon_1,\varepsilon_2,\varepsilon_3)$ for the basis $\mathbf V_c=[\mathbf Q,\mathbf Q'_{<c}]$: whenever the Gram defect on the support of $\mathbf V_c$ has spectral norm at most $\eta_0$, $\|\mathbf w_c-\mathbf V_c\mathbf h-\mathbf w'_c\|\le\varepsilon_2\|\mathbf w_c\|$ and $\|\mathbf V_c^{\mathsf{T}}\mathbf w'_c\|\le\varepsilon_1\|\mathbf w'_c\|+\varepsilon_3\|\mathbf w_c\|$;
2. a zero $\mathbf w_c$ gives a zero $\mathbf w'_c$;
3. the computed norms satisfy $|\nu_c-\|\mathbf w_c\||\le E\|\mathbf w_c\|$ and $|\beta_c-\|\mathbf w'_c\||\le E\|\mathbf w'_c\|$;
4. either the column is dropped, with $\beta_c\le\tfrac32\tau\nu_c$, $\mathbf q'_c=\mathbf 0$, and $r_{cc}=0$; or it is kept, with $\tfrac12\tau\nu_c<\beta_c$, $r_{cc}=\beta_c$, and $\|\beta_c\mathbf q'_c-\mathbf w'_c\|\le E\|\mathbf w'_c\|$.

If $\eta_0\le1/100$, $0\le\varepsilon_1,\varepsilon_2,\varepsilon_3\le1/10$, $0\le E\le1/100$, and $\tau>0$, then $(\mathbf Q',\mathbf H,\mathbf R)$ is a rounded extension of $\mathbf Q$ by $\mathbf W$ with window $\eta_0$ and parameters

$$\mu=2\varepsilon_1+\frac{4\varepsilon_3}{\tau}+5E,\qquad\varepsilon=\varepsilon_2+2E+2\tau.$$

The two thresholds in the fourth assumption allow for rounding in the deflation test.
:::

::: theorem decl:NLAlib.CGS2.cgs2Extend_spec name="The program meets the rounded contract" id=rounded-execution
Assume the standard model of rounded arithmetic with unit roundoff $u$, the level-one contracts with dot-product error $e_d(n)$, update error $e_a$, square-root error $e_s$, and scaling error $e_c$, with $e_a,e_s,e_c\ge0$, and exact comparisons. Let $0\le\eta_0\le1/100$, $c\le1/100$, $u\ge0$, $4u\le c$, $0\le E\le1/100$, and let $\tau>0$ be the rational threshold of the implementation. At every admitted dimension $(n,k,\ell)$ assume that the level-one operations admit the length $n$, that $e_d(n)\ge0$, that the pass budget of $k+\ell$ columns holds,

$$(k+\ell+1)\,e_d(n)(1+\eta_0)^2+\bigl((1+e_a)^{k+\ell}-1\bigr)\bigl(1+(k+\ell)(1+e_d(n))(1+\eta_0)^2\bigr)\le c,$$

and that the computed norms are accurate to $E$: $e_d(n)+e_s(1+e_d(n))\le E$. Assume also $e_c\le E$. Then the implementation runs on all admitted operands and its decoded output is a rounded extension with window $\eta_0$ and parameters

$$\mu=4c+\frac{8(\eta_0+c)^2}{\tau}+5E,\qquad\varepsilon=3c+2E+2\tau.$$

Here $c$ is the budget of one classical pass against all stored columns and $E$ the relative accuracy of the computed norms and of the scaling. The bound on a kept column is absolute, so the guarantee covers every returned column.
:::

These statements certify the extension program against its two contracts. The certificate of the block Golub–Kahan driver linked with this program is not stated in the library; see the Scope section of the block Golub–Kahan page.

## Results on the extension contracts

{{ generated:results }}

## Mathematical method

{{ generated:mathematical-method }}
