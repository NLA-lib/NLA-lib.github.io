---
kind: statement
id: nlalib-spectralbisection-bisectionprogram-c1b568f6
uid: c1b568f6-4bc5-5e42-91e7-8b77a20c9e57
---

::: definition decl:NLAlib.SpectralBisection.bisectionProgram name="Stored spectral bisection" id=algorithm
Supply a radius bound $R_0$, tolerance $\varepsilon$, precision parameter $\beta$, depth budget $L$, sign-iteration cap $c$, and a random tape. Store complex entries as adjacent real and imaginary words.

1. Store the root matrix and parameters in the root arena.
2. At each downward level, draw $n$ uniform words and $4n^2$ Gaussian words.
3. For each active node, read its matrix $\mathbf{A}$, radius $R$, tolerance, and depth counter $\ell$.
4. For a singleton, store the identity basis and its real diagonal value.
5. For a sufficiently small spectral window, store the identity basis and zero values.
6. Otherwise, choose a sampled shift of scale $R/\ell$.
7. Apply capped [Newton–Schulz sign iteration](/explore/statements/33cd8a3d-4740-5cbd-82aa-7e67e7c152da/) to the shifted matrix, obtaining $\mathbf{B}$.
8. Form $\mathbf{P}_+=(\mathbf{B}+\mathbf{I})/2$ and $\mathbf{P}_-=-(\mathbf{B}-\mathbf{I})/2$.
9. Estimate the positive rank by rounding the computed trace of $\mathbf{P}_+$ and clamping it to the node dimension.
10. If the rank is zero or the full dimension, store the corresponding shifted child.
11. Otherwise, project Gaussian samples and apply [QR](/explore/statements/adb72f11-3503-58f9-89c4-98a60c4f7a40/) to obtain $\mathbf{Q}_+$ and $\mathbf{Q}_-$.
12. Compress the node matrix onto these bases and store the two shifted children.
13. At the depth boundary, store identity bases and zero values.
14. Traverse upward, combining child bases and restoring the eigenvalue shifts.
15. Copy the root basis and values to the output buffers, then release scratch storage.

Each instruction uses the supplied arithmetic. In particular, one-half and the trace are computed with word operations. Reaching an iteration or depth cap produces a defined output; accuracy needs the assumptions below.
:::
