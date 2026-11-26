---
kind: statement
id: entry-3026fd08-ad2d-54e5-bac4-aebadaf30019
uid: 3026fd08-ad2d-54e5-bac4-aebadaf30019
---
::: theorem result:hutchpp-variance name="The variance of Gaussian Hutch++ for a positive semidefinite matrix"
If the
$n \times \lvert s \rvert$ sketch test matrix $\mathbf{S}$ and the $n \times \ell$ residual test
matrix $\mathbf{G}$, $\ell \ge 1$, are independent and standard Gaussian, then for every real
positive semidefinite $\mathbf{A}$ and every $r \ge 1$ with $2r + 1 \le \lvert s \rvert$,
$$\operatorname{Var}[\mathsf{hutchpp}(\mathbf{A}, \mathbf{S}, \mathbf{G})] \le
\frac{(\operatorname{tr}\mathbf{A})^2}{\ell\, r}\,,$$
`NLAlib.variance_hutchpp_le_nuclearNorm_of_hasLaw_gaussianMatrix` with
$\|\mathbf{A}\|_* = \operatorname{tr}\mathbf{A}$. With $r = (m - 2)/8$,
$\lvert s \rvert = (m + 2)/4$ and $\ell = (m - 2)/2$ it is
$16(\operatorname{tr}\mathbf{A})^2/(m - 2)^2$ for $m = 2\lvert s \rvert + \ell$ products.

Note: The cited comparison uses sign residual probes (see
`NLAlib.variance_hutchpp_of_hasLaw_rademacherMatrix`).
:::
