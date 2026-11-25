---
kind: statement
id: nlalib-krylov-golubkahan-band-certification-staticpeak-solveprogram-le-solvepeak
uid: 5c5ad6bf-3fdc-55bd-a427-6489b7c4a18d
---

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.staticPeak_solveProgram_le_solvePeak name="Scratch storage" id=scratch
For every resource model, the scratch of the fixed program at the sizes $(m,n,\ell,q)$ is at most

$$\max(m,n)\,\ell+w+w_{\mathrm q},$$

where $w$ is the largest declared workspace among the primitive calls of the run: a draw, a product with $\mathbf{A}$, a product with its adjoint, and the $2q+1$ basis extensions at their dimensions. No common bound on the workspaces of the primitives is assumed. The block of $\max(m,n)\,\ell$ words holds the drawn block and then the products.

Here $w_{\mathrm q}$ is the maximum declared workspace of any query included in the program's instruction budget, with maximum zero when there are no queries. It is also zero when all admitted queries have zero workspace. Adding this reservation allows query scratch to overlap the largest live allocation, giving a conservative total in abstract word cells.
:::
