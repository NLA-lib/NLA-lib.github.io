---
kind: statement
id: entry-819cba98-32b4-5c5b-923a-ad88bfe9e2cd
uid: 819cba98-32b4-5c5b-923a-ad88bfe9e2cd
---
::: theorem result:sketch-and-solve-lower-bound name="No random sketch beats a random orthonormal one"
(Epperly and Webber's minimax lower bound
for sketch-and-solve): for a random sketch $\mathbf{\Omega} \in \mathbb{R}^{m \times \ell}$ of any
law with full column rank almost surely, $\mathbf{A} \in \mathbb{R}^{m \times n}$ with
$r = \operatorname{rank}\mathbf{A}$, $r + 2 \le \ell$ and any $\mathbf{B}$, there is an orthogonal
$\mathbf{U}$ with <!-- value haarProjectionFactor m \ell r -->
$$\Bigl(1 + \frac{m - \ell}{m - r}\cdot\frac{r}{\ell - r - 1}\Bigr)
\|(\mathbf{I} - \mathbf{P}_{\mathbf{A}})\mathbf{B}\|_{\mathsf{F}}^2 \le
\mathbb{E}\|\mathbf{U}\mathbf{B} -
\mathbf{U}\mathbf{A}\,\mathsf{sketchAndSolve}(\mathbf{U}\mathbf{A},
\mathbf{\Omega}^{\mathsf{H}}, \mathbf{U}\mathbf{B})\|_{\mathsf{F}}^2\,,$$
in extended reals (the expectation may be infinite). With
`NLAlib.integral_frobNorm_sub_mul_sketchAndSolve_sq_of_hasLaw_haarFrame` (equality for a Haar
sketch): the random orthonormal sketch is minimax optimal.


Note: The cited result takes a supremum over problems of rank $r$.
:::
