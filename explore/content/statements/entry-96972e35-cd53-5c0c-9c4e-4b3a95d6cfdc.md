---
kind: statement
id: entry-96972e35-cd53-5c0c-9c4e-4b3a95d6cfdc
uid: 96972e35-cd53-5c0c-9c4e-4b3a95d6cfdc
---
::: theorem result:range-finder-structural-bound name="The structural bound of the range finder, Frobenius form"
For $\mathbf{A} \in \Bbbk^{m \times n}$, $\mathbf{\Omega} \in \Bbbk^{n \times l}$ and
$\mathbf{Z} \in \Bbbk^{n \times r}$ with orthonormal columns and
$\mathbf{Z}^{\mathsf{H}}\mathbf{\Omega}$ of full row rank (`(Ωᴴ * Z).rank = Z.rank`), with
$\mathbf{E} = \mathbf{A} - \mathbf{A}\mathbf{Z}\mathbf{Z}^{\mathsf{H}}$ and
$\mathbf{M} = \mathbf{E}\mathbf{\Omega}(\mathbf{Z}^{\mathsf{H}}\mathbf{\Omega})^{+}$,
$$\|\mathbf{A} - \mathsf{rsvd}(\mathbf{A}, \mathbf{\Omega})\|_{\mathsf{F}}^2 \le
\|\mathbf{E}\|_{\mathsf{F}}^2 + \|\mathbf{M}\|_{\mathsf{F}}^2\,.$$
The cited HMT and CEMT results use a top-$k$ frame; Woodruff treats any frame over $\mathbb{R}$.
This statement uses the displayed full-row-rank condition.
:::
