---
kind: statement
id: nlalib-nystrombki-8647f4e3
uid: 8647f4e3-cefb-5ae0-9fac-51da15589631
---

::: definition decl:NLAlib.nystromBKI name="Nyström block Krylov iteration"
For Hermitian positive-semidefinite $\mathbf{A}$, a start block $\mathbf\Omega$ with $\ell$ columns, and $q$ blocks, build the test matrix $[\mathbf\Omega,\mathbf{A}\mathbf\Omega,\ldots,\mathbf{A}^{q-1}\mathbf\Omega]$ and apply the Nyström construction to it:

$$\mathsf{nysbki}(\mathbf{A},\mathbf\Omega,q)=\mathsf{nystrom}\bigl(\mathbf{A},[\mathbf\Omega,\mathbf{A}\mathbf\Omega,\ldots,\mathbf{A}^{q-1}\mathbf\Omega]\bigr).$$

The powers are retained together rather than keeping only the last one.
:::
