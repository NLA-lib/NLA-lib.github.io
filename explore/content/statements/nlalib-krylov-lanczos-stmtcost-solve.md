---
kind: statement
id: nlalib-krylov-lanczos-stmtcost-solve
uid: 3318f77c-2fb6-5ae5-a52e-c7239d83ab69
---

::: theorem decl:NLAlib.Krylov.Lanczos.stmtCost_solve name="Operation budget" id=operations
For dimension $n$ and cap $k$, the static budget permits at most $k$ matvecs, $1+2k$ length-$n$ dot products, $2k$ vector updates, $1+2k$ vector copies, and $1+k$ vector normalizations.

It also permits $1+k$ square roots, $2k$ scalar negations, $(k+2)n+2k+2$ zero literals, and $1+2k$ positivity queries. Initialization is included; early stopping can reduce the actual calls. Work is obtained by charging these calls according to the chosen primitive costs. The displayed Lean statement identifies the complete primitive-call budget.
:::
