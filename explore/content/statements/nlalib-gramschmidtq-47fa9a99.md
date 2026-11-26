---
kind: statement
id: nlalib-gramschmidtq-47fa9a99
uid: 47fa9a99-bf7f-54d6-ad4e-a307c2efa85a
---

::: definition decl:NLAlib.gramSchmidtQ name="Gram–Schmidt orthogonalization"
Process the input columns in order. Remove from each column its components along the earlier nonzero orthonormal columns, then normalize a nonzero residual. A zero residual represents a dependent column and remains zero in the library's rank-revealing convention. Classical Gram–Schmidt forms projection coefficients from a common input residual; modified Gram–Schmidt updates that residual after each projection.

Note: Repeated passes are separate implementation choices.
:::
