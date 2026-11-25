---
kind: statement
id: nlalib-shiftedqr-shqrsmalleigalgorithm-dfd2780d
uid: dfd2780d-7c4e-51db-aa04-4766a316f48b
---

::: definition decl:NLAlib.ShiftedQR.shqrSmallEigAlgorithm name="Certificate with the BGS III program" id=certificate-small-eig
The fixed program `shqrSmallEigProgram`, over the model of the BGS III program (no oracle) with unit costs, succeeds on every admitted input, every interpretation of the model and every tape, within the static budget, scratch and memory, and writes only the matrix, the accumulator and the failure word. Its accumulator starts from $\mathbf{I}$. At the sizes $(n,k,n_p,F,T)$ its work and span are at most

$$967736\,(n+1)^3(k+1)^4(n_p+1)(F+1)(T+1)^2.$$

The instructions of the BGS III solver are among those counted: the bound covers the whole computation, apart from the parameter words, which are supplied.
:::
