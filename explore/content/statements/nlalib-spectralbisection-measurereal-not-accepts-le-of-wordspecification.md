---
kind: statement
id: nlalib-spectralbisection-measurereal-not-accepts-le-of-wordspecification
uid: 67eaecd1-e828-5359-a866-13159be34f30
---

::: theorem decl:NLAlib.SpectralBisection.measureReal_not_accepts_le_of_wordSpecification name="Accuracy transfers to the stored output" id=accuracy
Suppose the numerical reference returns an approximate diagonalization with error parameters $\eta=2\varepsilon R_0$ and $\kappa=\varepsilon/3$, except on a tape event of probability at most $\theta$. For a probability tape law, the certified execution satisfies its functional and resource specification and stores $\mathbf{U},\mathbf{d}$ with

$$\|\mathbf{A}-\mathbf{U}\operatorname{diag}(\mathbf{d})\mathbf{U}^{\mathsf{H}}\|_2\le 2\varepsilon R_0,$$

$$(1-\varepsilon/3)^2\mathbf{I}\preceq\mathbf{U}^{\mathsf{H}}\mathbf{U}\preceq(1+\varepsilon/3)^2\mathbf{I},$$

with probability at least $1-\theta$. Here the matrices and parameters denote decoded stored words.

The failure event includes execution failure, any resource-bound violation, and incorrect numerical output. Establishing the reference premise separately requires Hermitian input, a valid radius bound, sufficient precision, depth and sign-iteration cap, and the stated sampler and tape-law assumptions. This transfer theorem does not by itself establish those numerical hypotheses.
:::
