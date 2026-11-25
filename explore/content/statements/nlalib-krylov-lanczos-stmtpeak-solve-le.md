---
kind: statement
id: nlalib-krylov-lanczos-stmtpeak-solve-le
uid: ca6ffb21-49a0-54fc-81a5-dae0dd103639
---

::: theorem decl:NLAlib.Krylov.Lanczos.stmtPeak_solve_le name="Scratch and output capacity" id=storage
The scoped scratch bound is

$$2n+2+W(n),$$

where $W(n)$ is the maximum declared workspace over the primitive calls used by this program. It does not grow with the cap.

The supplied basis output has $(k+1)n$ cells, the coefficient output has $2k+2$ cells, and the input has $n$ cells. These supplied capacities are additional to scratch. Storage captured by an external operator is accounted for by that operator's model.
:::
