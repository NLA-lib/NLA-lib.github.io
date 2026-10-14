---
title: NLA-lib
description: NLA-lib: a lean 4 library for numerical linear algebra
keywords: NLA-lib,  lean, lean4, formal verification
---

We are building NLA-lib, a Lean 4 library covering core results from numerical linear algebra.
The aim of this library is to serve as a bridge between mathlib and the higher-level numerical linear algebra theorems that are often imported in written proofs.

The project is hosted on [Github](https://github.com/NLA-lib/nlalib) and you can view the results through our [online explorer](./explore).
This is a work in progress.

## Contributing

We eventually hope that this will become a community project and we will provide more details on contributing soon.
In the meantime, if you are interested in getting involved, please send an email to: [tyler.chen@nyu.edu](mailto:tyler.chen@nyu.edu) or open an issue on Github.

## Scope

The current scope includes topics such as:

- **Matrix Analysis:** SVD, pseudoinverses, spectral theory, perturbation bounds, and conditioning.
- **Probability & Concentration:** Gaussian and sub-Gaussian distributions, scalar and matrix concentration inequalities.
- **Random Matrix Theory:** Spectral bounds, singular values, and random matrix embeddings.
- **Randomized Sketching:** Johnson–Lindenstrauss, Gaussian sketches, SRHT, CountSketch, sparse embeddings, and leverage-score sampling.
- **Low-Rank Approximation:** Randomized SVD, Nyström methods, and randomized Cholesky.
- **Spectral Estimation:** Hutchinson, Hutch++, stochastic Lanczos quadrature, and trace estimation.
- **Iterative Solvers:** Krylov methods, conjugate gradients, GMRES, randomized Kaczmarz, and sketch-and-project.
- **Matrix Functions:** Polynomial approximation, matrix exponentials, and spectral function approximation.

We eventually will plan to expand to more topics, including finite precision analysis.


