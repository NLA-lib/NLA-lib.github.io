---
kind: statement
id: nlalib-schur-verifiedschurwith-measurereal-not-flag-le
uid: d695353d-56d2-5d1a-8f96-0d7943757d1e
---

::: theorem decl:NLAlib.Schur.verifiedSchurWith_measureReal_not_flag_le name="An accurate solver passes the check" id=verified-passes
On that machine, with a measurable interpretation that reads the tape only in its windows, let $64(n+2)^3u\le1$, $0\le\kappa\le64(n+2)^2u$, $4096(n+2)^3u\le\theta\le1$, $e_U\le1/2$ and $\sqrt{n+1}\,\delta'\le\theta/8$. Let `Solve` end, from every input memory and except with probability at most $\varphi$, in a measurable postcondition that implies a Schur output of $\mathbf{A}$ with errors $\delta',e_U$, survives rewriting the flag to $0$ and survives the release of scratch. Then the probability is at most $\varphi$ that `verifiedSchurWith Solve` fails, writes outside $\mathbf{A}$, $\widehat{\mathbf{U}}$ and the flag, or does not store the flag $0$ with that postcondition.
:::
