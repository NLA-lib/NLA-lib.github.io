---
kind: theory
id: random-sampling-models
title: Sampling maps and ideal-tape couplings
summary: Relate ideal samples, rounded stored tapes, and the same mathematical word algorithm.
status: ready
parents:
- finite-precision
- probability-distributions
search_aliases:
- NLAlib.eigh_toFloatMachine_map_samples
- NLAlib.eigh_eighTapeMachine_eq_eigh_eighIdealTree
---

A probability analysis may start with ideal real samples while a program consumes stored words. A coupling connects these descriptions without changing the arithmetic or the matrix routines used by the algorithm. It is distinct from proving a numerical accuracy bound.

::: theorem decl:NLAlib.Ops.Machine.eigh_toFloatMachine_map_samples name="Changing the sample representation"
Fix the word machine, decoding, matrix multiplication, and QR functions. Suppose two uniform samplers and two Gaussian samplers agree after maps $f$ and $g$ of their sample inputs. Then the complete mathematical spectral-bisection solver returns identical words after applying those maps to its sample tree.

The agreement is an explicit hypothesis for every uniform scale and sample, and for every Gaussian input. This is an equality of word computations, not a claim that rounded arithmetic is exact real arithmetic.
:::

::: theorem decl:NLAlib.SpectralBisection.eigh_tapeMachine_roundTape name="Rounded tape and ideal sample tree"
Fix a word machine, its matrix routines, an ideal real tape, and rounding functions for uniform and Gaussian words. The spectral-bisection reference on the rounded tape returns exactly the ideal-sample recursion using those same word functions and routines. The equality holds at any fixed starting tape position.

This supplies the functional bridge needed to transfer a probability analysis. A separate theorem establishes the numerical good event and its probability.
:::

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
