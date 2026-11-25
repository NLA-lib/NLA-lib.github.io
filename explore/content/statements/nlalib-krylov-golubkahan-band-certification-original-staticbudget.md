---
kind: statement
id: nlalib-krylov-golubkahan-band-certification-original-staticbudget
uid: 34337bed-f4b8-5514-b1d8-717d0f0e391b
---

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.original_staticBudget name="Primitive operation counts" id=counts
At the sizes $(m,n,\ell,q)$, the primitive part of the static budget of the fixed program is

- $n\ell$ scalar draws from the tape stream;
- $q\ell$ products with $\mathbf{A}$;
- $q\ell$ products with its adjoint;
- $2q+1$ basis extensions: one of the start block against the empty basis and, for each $j<q$, one of $\ell$ columns of length $m$ against $j\ell$ stored columns and one of $\ell$ columns of length $n$ against $(j+1)\ell$ stored columns.

The full budget also counts the structural instructions (index arithmetic, addressing, allocation, and control); the library records it as the instruction count of the program, not as a closed formula.
:::
