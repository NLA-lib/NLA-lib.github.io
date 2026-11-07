---
title: NLA-lib
description: NLA-lib: a lean 4 library for numerical linear algebra
keywords: NLA-lib,  lean, lean4, formal verification
menu:
  - Home: ./
  - Explorer: ./explore/
  - Rates: ./explore/rates/
  - Algorithms: ./explore/algorithms/
  - Design: ./design/
  - GitHub: https://github.com/NLA-lib/nlalib
---

We are building NLA-lib, an open source Lean 4 library covering numerical linear algebra.
The aim of this library is to serve as a foundation for the formalization of new and existing numerical linear algebra results, including research performed autonomously by agents.

The project is hosted on [Github](https://github.com/NLA-lib/nlalib).
You can view the results through our [online explorer](./explore).
This is a work in progress.

## Highlights

Here are some highlights of the project so far:

- **Coverage.** We have formalized a lot of theorems in matrix analysis, polynomial approximation, random matrices and concentration, Krylov methods, sketching, least squares, low-rank approximation, trace estimation, and lower bounds.
- **Low-rank approximation.** We proved that truncated generalized Nyström is an optimal method for Frobenius low-rank approximation.
- **Finite-precision Krylov methods.** We proved several new results about the standard implementation of conjugate gradient in finite precision (most past results were about Lanczos).
- **Eigensolvers.** We formalized bounds for Shah's randomized [spectral bisection algorithm](https://arxiv.org/abs/2408.09880) for Hermitian diagonalization.


## Contributing

If you are interested in getting involved, please send an email to: [tyler.chen@nyu.edu](mailto:tyler.chen@nyu.edu) or open an issue or pull request on Github.


