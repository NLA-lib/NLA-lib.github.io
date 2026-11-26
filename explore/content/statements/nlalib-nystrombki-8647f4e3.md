---
kind: statement
id: nlalib-nystrombki-8647f4e3
uid: 8647f4e3-cefb-5ae0-9fac-51da15589631
---

::: definition decl:NLAlib.nystromBKI name="Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf{A}$, a start block $\boldsymbol{\Omega}$ with $\ell$ columns, and $q$ blocks, build the test matrix $[\boldsymbol{\Omega},\mathbf{A}\boldsymbol{\Omega},\ldots,\mathbf{A}^{q-1}\boldsymbol{\Omega}]$ and apply the [Nyström construction](/explore/statements/254f7f6f-1199-596d-9347-4d32f1eab873/) to it:

$$\mathsf{nysbki}(\mathbf{A},\boldsymbol{\Omega},q)=\mathsf{nystrom}\bigl(\mathbf{A},[\boldsymbol{\Omega},\mathbf{A}\boldsymbol{\Omega},\ldots,\mathbf{A}^{q-1}\boldsymbol{\Omega}]\bigr).$$

The powers are retained together rather than keeping only the last one.
:::
