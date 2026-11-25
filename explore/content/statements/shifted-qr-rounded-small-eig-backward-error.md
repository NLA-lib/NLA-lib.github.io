---
kind: statement
id: shifted-qr-rounded-small-eig-backward-error
uid: a3ae6eab-cfd1-54a1-a5cb-aabb2ed528b6
---

::: theorem result:shifted-qr-rounded-small-eig-backward-error name="Eigenvalues with the BGS III program, unconditional" id=accuracy-small-eig
Under the hypotheses above on $\mathbf{H}$, the machine and the tape, with $u\le u_0$ at the proved tail records, start the program `roundedShQRSmallEig` from a memory holding $\mathbf{H}$, a stored accumulator, the threshold word and the parameter words. Then

$$\mathbb P\bigl[\text{the run fails, writes outside the matrix, the accumulator and the failure word, or does not set the failure word to }0\text{ and store an upper triangular }\widehat{\mathbf{T}}\text{ whose diagonal lists }\operatorname{spec}(\mathbf{H}+\mathbf{E})\text{ with }\|\mathbf{E}\|_2\le\delta\bigr]\le\varphi.$$

The theorem has no hypothesis on a small-block solver and none on random matrices.
:::
