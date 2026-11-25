---
kind: statement
id: nlalib-krylov-lanczos-certification-algorithm-bdfac892
uid: bdfac892-aa5e-5014-991c-ef2499ca3d72
---

::: definition decl:NLAlib.Krylov.Lanczos.Certification.algorithm name="Rounded certificate of the same program" id=rounded-certificate
Let $\mathbf{A}$ be the symmetric matrix of the operator. Assume that the scheme admits vectors of length $n$, that the matrix–vector allowance is at most $e_m\|\mathbf{A}\|_2$, and that an allowance $E$ satisfies the [accuracy envelope](/explore/arithmetic-models/#accuracy) of the standard profiles for $e_m$, the unit roundoff and the level-one error coefficients at length $n$. No assumption is made on the spectrum.

Then, for every admitted size and every input, the program of the listing runs successfully within its static instruction budget, with the work and span that the weights of the model give to that budget. It stores vectors and coefficients that are either the initialized output of zero steps or the values of a rounded Lanczos run of some length at most the cap $k$, with local error allowance $E$ (`Lanczos.Rounded.Output`). It stops before the cap only at a zero computed norm or coupling coefficient, and it leaves the tape position unchanged.
:::
