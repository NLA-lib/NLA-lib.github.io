---
kind: statement
id: arnoldi-relation
uid: dfe0f5c1-7607-5831-98c2-83dedb7248da
---

::: theorem result:arnoldi-relation name="Arnoldi relation"
For the library's [canonical Krylov bases](/explore/statements/1ebd9712-579d-596a-966f-9119a353806b/) $\mathbf{Q}_j$, including their zero-column convention after breakdown,

$$\mathbf{A}\mathbf{Q}_k=\mathbf{Q}_{k+1}(\mathbf{Q}_{k+1}^{\mathsf{H}}\mathbf{A}\mathbf{Q}_k).$$

Note: Applying the full operator to the current basis is represented in the next Krylov space by a small coefficient matrix.
:::
