---
kind: statement
id: entry-f718cafe-d505-5dc5-b3cb-153ad204ca6d
uid: f718cafe-d505-5dc5-b3cb-153ad204ca6d
---
::: theorem result:cg-recurrence name="The Hestenes–Stiefel iterates are the CG iterates"
for positive definite $\mathbf{A}$ and
every $k$, with no breakdown hypothesis,
$\mathbf{x}_k = \mathsf{cgIterate}(\mathbf{A}, \mathbf{b}, \mathbf{x}_0, k)$.
Hestenes and Stiefel show
that $\mathbf{x}_k$ minimises the $\mathbf{A}$-norm error on the plane through
$\mathbf{x}_0, \dots, \mathbf{x}_k$, which is $\mathbf{x}_0 + \mathcal{K}_k(\mathbf{A},
\mathbf{r}_0)$ (`Matrix.PosDef.span_cgState_p`), for real symmetric $\mathbf{A}$ and up to
termination; here every $k$.
:::
