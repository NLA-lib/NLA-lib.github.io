---
kind: statement
id: filtered-range-finder-approximation-36be1f8d
uid: 36be1f8d-abc5-5dfd-b557-ff75ebe97822
---

::: definition name="Filtered range-finder approximation"
Choose a spectral filter $g$ and a test matrix $\mathbf\Omega$. Form $\mathbf{Y}=\mathbf{A} g(\mathbf{A}^{\mathsf{H}}\mathbf{A})\mathbf\Omega$ and return $\mathbf{P}_{\mathbf{Y}}\mathbf{A}=\mathsf{rsvd}\bigl(\mathbf{A},g(\mathbf{A}^{\mathsf{H}}\mathbf{A})\mathbf\Omega\bigr)$. Polynomial filters can be evaluated through matrix applications; the mathematical analysis also permits more general spectral filters. Power iteration is the special choice $g(\lambda)=\lambda^p$. Final rank truncation is a further choice.
:::
