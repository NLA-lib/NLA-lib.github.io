---
kind: statement
id: nlalib-mgs-factorroutine-meets
uid: 60522b5b-99ce-5e10-9702-ddaea0dbe79a
---

::: theorem decl:NLAlib.MGS.factorRoutine_meets name="Exact execution correspondence" id=execution
Under the exact primitive contracts and the theorem's live, readable, writable matrix-buffer conditions, the program terminates and overwrites the matrix with exactly the mathematical `gramSchmidtQ` of the input. No full-rank or successful-execution premise is assumed. Rectangular matrices, dependent columns, and zero dimensions are admitted.

The shared mathematical method describes how the nonzero columns span the original range. Rounded orthogonality bounds for two classical passes concern a different implementation and are not substituted for this exact MGS statement.
:::
