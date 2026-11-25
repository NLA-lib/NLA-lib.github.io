---
uid: de2c07b8-baa8-51a2-9367-3e18260f4814
kind: implementation
id: two-pass-basis-extension
algorithm: gram-schmidt
title: Two-pass classical Gram–Schmidt basis extension
summary: Extend a stored basis by a block, column by column, with two classical passes and threshold deflation.
status: outline
order: 3
arithmetic_models:
- id: exact
  arithmetic: exact
- id: standard
  arithmetic: standard
  program: relative-blas
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

This implementation extends a stored basis $\mathbf{Q}$ ($k$ columns of length $n$) by a block $\mathbf{W}$ of $\ell$ columns (the Lean statements name the block width `b`). Each column of the block is reduced twice, by classical Gram–Schmidt passes, against the stored basis followed by the new columns already written. A reduced column whose norm falls below a threshold relative to the input column is dropped: a zero column is stored. It is the orthogonalization scheme the library supplies for block Golub–Kahan bidiagonalization.

{{ generated:source-guides }}

## Algorithm

{{ statement:nlalib-cgs2-cgs2extendroutine-af080b3b }}

## Model of arithmetic

{{ generated:arithmetic-model-selector }}

The program uses scalar operations, level-one vector operations (dot product, vector update, norm, scaling, copy), and comparisons. The statements below are for two models: exact real arithmetic with exact level-one operations, where the threshold is $0$; and the standard model of rounded arithmetic with level-one error contracts and exact comparisons, where the threshold is positive. Scalars are real.

## Accuracy

The exact contract (an exact extension of a basis by a block) is defined on the [Golub–Kahan process](/explore/algorithms/golub-kahan/) page, and the rounded contract with parameters $(\eta_0,\mu,\varepsilon)$ on its [implementation](/explore/algorithms/golub-kahan/implementations/full-reorthogonalization/) page. The first statement of each pair below is about decoded matrices; the second is about the program.

::: model exact
{{ statement:cgs2-basis-extension }}

{{ statement:nlalib-cgs2-cgs2extendroutine-meets-exact }}

::: end-model

::: model standard
{{ statement:cgs2-basis-extension-error }}

{{ statement:nlalib-cgs2-cgs2extendroutine-meets }}
::: end-model

These statements certify the extension program against its two contracts. The certificate of the block Golub–Kahan driver linked with this program is not stated in the library; see the Scope section of the [block Golub–Kahan implementation](/explore/algorithms/golub-kahan/implementations/full-reorthogonalization/#section-scope) page.

## Results on the extension contracts

{{ generated:results }}

## Mathematical method

{{ generated:mathematical-method }}
