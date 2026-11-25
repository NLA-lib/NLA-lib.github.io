---
kind: statement
id: nlalib-krylov-golubkahan-band-isexactstoredrun-mul-conjtranspose-mul-conjtranspose-eq-rbki
uid: 22bf30ab-6185-5d8f-8b97-3a1ef452ff55
---

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.IsExactStoredRun.mul_conjTranspose_mul_conjTranspose_eq_rbki name="Stored factors of an exact run" id=stored-factors
Let $\mathbf{U}$, $\mathbf{V}$, and the packed coefficient block columns $\mathbf{S}_j$ be the stored blocks of an exact run for a real matrix $\mathbf{A}$ from the start block $\mathbf\Omega$, and let $\mathbf{S}$ be the assembled $(q+1)\ell\times q\ell$ matrix. Then

$$\mathbf{U}\mathbf{S}^{\mathsf{H}}\mathbf{V}^{\mathsf{H}}=\mathsf{rbki}(\mathbf{A},\mathbf\Omega,q).$$

This is an exact-arithmetic identity for the decoded output.
:::
