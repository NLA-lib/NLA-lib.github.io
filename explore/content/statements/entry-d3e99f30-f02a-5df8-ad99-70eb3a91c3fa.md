---
kind: statement
id: entry-d3e99f30-f02a-5df8-ad99-70eb3a91c3fa
uid: d3e99f30-f02a-5df8-ad99-70eb3a91c3fa
---
::: theorem result:basis-extension-gram-defect name="One block step of the loss of orthogonality"
let $\mathbf{D}(\cdot)$ be the Gram defect
on the support, $\mathbf{D}(\mathbf{Q}) = \mathbf{Q}^{\mathsf{T}}\mathbf{Q} -
\operatorname{diag}(\mathbf{s})$ with $s_j = 0$ at a zero column of $\mathbf{Q}$ and $s_j = 1$
otherwise. If $(\mathbf{Q}', \mathbf{H}, \mathbf{R})$ is a [rounded extension](/explore/statements/fb78aa8d-2d5c-5c09-8bde-5ce9dd46a393/)
(`NLAlib.IsBasisExtensionErr`) of the real basis $\mathbf{Q}$ with parameters
$(\eta_0, \mu, \varepsilon)$, $\mathbf{Q}'$ has $b$ columns and $\mathbf{Q}$ is in the window,
$\sqrt{\|\mathbf{D}(\mathbf{Q})\|_{\mathsf{F}}^2 + 3b\mu^2} \le \eta_0$, then
$$\|\mathbf{D}([\mathbf{Q}, \mathbf{Q}'])\|_{\mathsf{F}}^2 \le
\|\mathbf{D}(\mathbf{Q})\|_{\mathsf{F}}^2 + 3b\mu^2\,.$$
No printed source.
:::
