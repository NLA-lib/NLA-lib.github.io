---
kind: statement
id: hutchpp-unbiased
uid: e14bcce7-62ce-54e6-998e-40ef966c42bb
---

::: theorem result:hutchpp-unbiased name="Unbiasedness with independent residual probes"
Suppose the range sketch is almost everywhere measurable, the residual probe matrix is independent of it and has at least one column, and each residual probe is square integrable and isotropic. For every square $\mathbf{A}$,

$$\mathbb E[\mathsf{hutch++}(\mathbf{A})]=\operatorname{tr}(\mathbf{A}).$$

The range sketch can have any distribution. Residual probes need not be independent of one another for this expectation identity.
:::
