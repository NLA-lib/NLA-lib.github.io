---
kind: statement
id: nlalib-cgs2-cgs2extendroutine-meets-exact
uid: 8c857b38-dcb9-5698-b8b0-0f647fe28c56
---

::: theorem decl:NLAlib.CGS2.cgs2ExtendRoutine_meets_exact name="The program meets the exact contract at threshold zero" id=exact-execution
Under exact scalar arithmetic, exact level-one operations at every length, and exact comparisons, the implementation with threshold $\tau=0$ runs on all admitted operands of the extension operation, and its decoded basis, block, new block, and coefficients satisfy the [exact extension contract](/explore/statements/12a7ec72-6c64-59e6-b7de-7aff8d055ba2/). The stored basis is arbitrary: it may contain zero columns and need not be orthonormal on its support.
:::
