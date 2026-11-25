---
kind: statement
id: nlalib-schur-denseschuralgorithm-90192996
uid: 90192996-6dc6-5054-aca9-ae0e5756c82c
---

::: definition decl:NLAlib.Schur.denseSchurAlgorithm name="Certificate of the dense Schur solver" id=certificate
The fixed program, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the accumulator and the flag. At the sizes $(n,n_r,n_q,k,F,T)$ its work and span are at most `denseSchurWork`,

$$120(n+1)^2+201(n+1)^2+2998(n+1)^3+380748(n+1)^3(k+1)^4(n_r+n_q+1)(F+1)(T+1)^2+128(n+2)^2.$$

The terms are the norm estimate, the regularizer, the reduction, the core with its small-block solver, and the glue. The parameter words are supplied and their computation is not charged.
:::
