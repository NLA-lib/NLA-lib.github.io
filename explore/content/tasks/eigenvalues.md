---
kind: task
id: eigenvalues
title: Eigenvalues
summary: Approximate extremal or interior eigenvalues and their invariant subspaces.
status: ready
order: 1
theory:
- spectral-theory
- krylov-spaces
- perturbation-theory
groups:
- id: spectral-splitting
  title: Spectral divide-and-conquer
  summary: Split the spectrum, solve smaller invariant-subspace problems, and assemble a diagonalization.
  algorithms:
  - spectral-bisection
- id: krylov
  title: Krylov factorizations
  summary: Shared basis constructions used to extract Ritz eigenvalues and vectors; the factorizations also serve linear solves, matrix functions, and quadrature.
  algorithms:
  - lanczos
  - arnoldi
  summaries:
    lanczos: Build an orthonormal Krylov basis and a tridiagonal factorization for a Hermitian operator.
    arnoldi: Build an orthonormal Krylov basis and an upper-Hessenberg factorization for a general operator.
- id: subspace-iteration
  title: Power and subspace iteration
  summary: Improve one vector or a block of vectors by repeatedly applying an operator or a shifted inverse.
  algorithms:
  - power-iteration
  - inverse-iteration
  - rsi
  summaries:
    rsi: For a Hermitian positive-semidefinite matrix, improve a randomized starting block to approximate
      a dominant invariant subspace.
- id: qr-iteration
  title: QR eigenvalue methods
  summary: Apply orthogonal similarities to a square matrix. QR iteration is distinct from computing a
    QR factorization.
  algorithms:
  - qr-iteration
- id: jacobi
  title: Jacobi methods
  summary: Diagonalize a Hermitian matrix using successive plane rotations.
  algorithms:
  - jacobi-eigenvalue
- id: components
  title: Eigensolver building blocks
  summary: Reduce the matrix representation or extract subspace bases before the main eigensolver steps.
  algorithms:
  - deflation
  - hessenberg-reduction
---

Approximate extremal or interior eigenvalues and their invariant subspaces.

{{ generated:task-groups }}

## Mathematical background

{{ generated:theory }}
