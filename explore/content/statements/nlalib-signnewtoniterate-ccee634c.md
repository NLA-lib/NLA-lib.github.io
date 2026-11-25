---
kind: statement
id: nlalib-signnewtoniterate-ccee634c
uid: ccee634c-02eb-5769-8d49-3bf04e99f8af
---

::: definition decl:NLAlib.signNewtonIterate name="Newton matrix-sign iteration"
Start from $\mathbf{X}_0=\mathbf{A}$ and set $\mathbf{X}_{j+1}=\tfrac12(\mathbf{X}_j+\mathbf{X}_j^{-1})$. The convergence theorem requires spectral separation from the imaginary axis and establishes invertibility of the relevant iterates. This inverse-averaging method differs from the inverse-free Newton–Schulz sign update.
:::
