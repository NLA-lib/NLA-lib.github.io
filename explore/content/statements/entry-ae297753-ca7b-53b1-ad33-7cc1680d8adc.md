---
kind: statement
id: entry-ae297753-ca7b-53b1-ad33-7cc1680d8adc
uid: ae297753-ca7b-53b1-ad33-7cc1680d8adc
---
::: theorem result:gram-correspondence name="The Gram correspondence for block Krylov Nyström of a positive semidefinite matrix"
the
error of NysBKI is the Gram matrix of the error of RBKI of the square root,
$$\mathbf{H} - \mathsf{nystromBKI}(\mathbf{H}, \mathbf{\Omega}, q) =
\mathbf{E}^{\mathsf{H}}\mathbf{E}, \qquad
\mathbf{E} = \mathbf{H}^{1/2} - \mathsf{rbki}(\mathbf{H}^{1/2}, \mathbf{\Omega}, q)\,;$$
NysBKI with $q$ products with $\mathbf{H}$ is RBKI with $2q$ products with $\mathbf{H}^{1/2}$.
NysSI needs no twin: `Matrix.PosSemidef.sub_nystrom_eq` at the test matrix
$\mathbf{H}^p\mathbf{\Omega}$ is RSI of $\mathbf{H}^{1/2}$ with $p$ power steps.

:::
