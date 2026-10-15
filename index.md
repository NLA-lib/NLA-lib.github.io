---
title: NLA-lib
description: NLA-lib: a lean 4 library for numerical linear algebra
keywords: NLA-lib,  lean, lean4, formal verification
menu:
  - Home: ./
  - Explorer: ./explore/
  - Books: ./explore/books/
  - GitHub: https://github.com/NLA-lib/nlalib
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

We also cover results from a number of key books such as:

- Roger A. Horn and Charles R. Johnson, [*Matrix Analysis*](./explore/books/#b-HornJohnson2013), second edition, 2013.
- Joel A. Tropp, [*An Introduction to Matrix Concentration Inequalities*](./explore/books/#b-Tropp2015), 2015.
- Roman Vershynin, [*High-Dimensional Probability*](./explore/books/#b-Vershynin2018), 2018.

The [book explorer](./explore/books/) goes through each of these chapter by chapter and shows which of its numbered results the library has, with links to them.

