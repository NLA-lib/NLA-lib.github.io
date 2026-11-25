---
kind: statement
id: accuracy-budgets-e4a4357b
uid: e4a4357b-8f1b-5f40-b418-ed1b6bbfa79a
---

::: definition name="Accuracy budgets" id=accuracy

For the abstract relative-error CG theorem, choose a nonnegative allowance $E$ with

$$u,d_n,e_a,e_m\le E\le10^{-2}.$$

The named standard profiles use a stricter envelope (`Ops.Standard.Accuracy`), which
the CG and Lanczos operation budgets share:

$$\begin{gathered}0\le E\le10^{-2},\qquad e_m,e_a\le E,\\
u,d_n,e_{\mathrm{scal}}\le E/16.\end{gathered}$$

Here $e_{\mathrm{scal}}$ bounds componentwise vector division. Each solver theorem also
has its own assumptions, such as the spectral and iteration-window assumptions of CG,
stated on its implementation page.
:::
