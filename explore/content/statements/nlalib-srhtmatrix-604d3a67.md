---
kind: statement
id: nlalib-srhtmatrix-604d3a67
uid: 604d3a67-5a4c-5dc9-9933-06e04ea9ac41
---

::: definition decl:NLAlib.srhtMatrix name="Subsampled randomized Hadamard transform"
For a dimension admitting a normalized Hadamard matrix $\mathbf{H}$, form $\mathbf{S}=\sqrt{n/s}\,\mathbf{R}\mathbf{H}\mathbf{D}$, where $\mathbf{D}$ contains independent random signs and $\mathbf{R}$ selects $s$ rows. Sampling without replacement requires $1\le s\le n$. The library's more general structured-transform definition also accepts a supplied orthogonal transform; sampling with replacement is a separate law.
:::
