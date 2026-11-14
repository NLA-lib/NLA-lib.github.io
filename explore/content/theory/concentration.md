---
kind: theory
id: concentration
title: Concentration inequalities
summary: Markov, Chebyshev, Bernstein, Hanson–Wright, and matrix Chernoff inequalities.
status: outline
order: 14
parents:
- probability
module_prefixes:
- NLAlib.Probability.Tail
- NLAlib.Probability.BoundedDifferences
- NLAlib.Probability.MatrixConcentration
- NLAlib.Probability.QuadraticForm.HansonWright
- NLAlib.Probability.Distributions.GaussianConcentration
- NLAlib.Probability.SubGaussian
- NLAlib.Probability.SubExponential
- NLAlib.ForMathlib.Probability.Moments.PaleyZygmund
- NLAlib.ForMathlib.Probability.Martingale.OptionalStopping
- NLAlib.Probability.ConvexOrder
- NLAlib.Probability.SubGaussianVector
result_ids:
- markov-inequality
---

Markov, Chebyshev, Bernstein, Hanson–Wright, and matrix Chernoff inequalities. The introductory exposition is incomplete; available library statements are listed below.

## Mathematical guarantees

::: theorem result:markov-inequality name="Markov bound"
For an integrable random variable $X$ that is nonnegative almost surely, and $t>0$,

$$\Pr\{X\ge t\}\le\frac{\mathbb E X}{t}.$$

The checked result holds more generally for a measure and its integral. Integrability is an explicit hypothesis.
:::

## Further results

{{ generated:results }}

## Formal definitions

{{ generated:definitions }}

## Used by algorithms

{{ generated:used-by }}

## Broader topics

{{ generated:parent-topics }}
