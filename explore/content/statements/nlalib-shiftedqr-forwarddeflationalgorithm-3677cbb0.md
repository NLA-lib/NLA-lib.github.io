---
kind: statement
id: nlalib-shiftedqr-forwarddeflationalgorithm-3677cbb0
uid: 3677cbb0-38a4-5a27-bfbb-f16fd4935300
---

::: definition decl:NLAlib.ShiftedQR.forwardDeflationAlgorithm name="Backward and forward error certificate"
Under the stated input assumptions, execution terminates and initializes all $N$ stored complex outputs. Their multiset is exactly the characteristic-polynomial roots of $\mathbf{H}+\mathbf{E}$, including algebraic multiplicities, for a perturbation satisfying
$$\|\mathbf{E}\|_2\le (N-1)\delta\|\mathbf{H}\|_{\mathrm F}.$$
Every stored output is also within
$$\frac B2(N-1)\delta\|\mathbf{H}\|_{\mathrm F}$$
of some eigenvalue of $\mathbf{H}$. This forward bound is directed from outputs to the input spectrum; it does not assert a bijective matching or reverse coverage. The certificate retains the original resource guarantees.
:::
