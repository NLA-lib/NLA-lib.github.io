---
kind: statement
id: nlalib-shiftedqr-counteddeflationalgorithm-aaf66e60
uid: aaf66e60-a561-5e3e-abff-5cc278379268
---

::: definition decl:NLAlib.ShiftedQR.countedDeflationAlgorithm name="Full program work and span certificate"
The same program has both numerical guarantees above. Write $W$ for work and $S$ for sequential span. Their conservative bound is
$$W,\ S\le17109\,b^{14}\bigl(1+K(b^5)\bigr),$$
where $b=N+m+k+F+M+1$.
Here $K(L)$ is the finite maximum of the supplied costs of both spectral primitives over dimension lists of length at most two and entries at most $L$. The bound includes scalar, index, comparison, address, control, and allocation charges. It makes no polynomial-growth assumption about the primitive costs. This is a full-program upper bound, rather than the paper's tight complexity estimate or a bit-complexity bound.
:::
