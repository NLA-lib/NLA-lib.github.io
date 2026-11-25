---
kind: statement
id: nlalib-schur-verifiedschuralgorithm-cbea4e58
uid: cbea4e58-b0f0-50f9-8290-46f3da3fd35f
---

::: definition decl:NLAlib.Schur.verifiedSchurAlgorithm name="Certificate of the verified solver" id=verified-certificate
The fixed program `verifiedSchurProgram`, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the accumulator and the flag. Its every-tape claim is the flag-conditional Schur form. At the sizes $(n,n_r,n_q,k,F,T)$ its work and span are at most `verifiedSchurWork`,

$$384547(n+1)^3(k+1)^4(n_r+n_q+1)(F+1)(T+1)^2+1619(n+1)^3+32(n+1)^2+128.$$
:::
