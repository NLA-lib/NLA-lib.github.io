---
kind: statement
id: nlalib-mgs-factor-peak-le
uid: 75eae202-4e88-5a08-b9ed-7af0208f76ae
---

::: theorem decl:NLAlib.MGS.factor_peak_le name="In-place scratch bound" id=storage
If every primitive workspace is at most $w$ cells, the complete matrix program uses at most $2+w$ scratch cells above the supplied $nm$-cell matrix. Thus resident capacity is at most

$$nm+2+w.$$

With zero primitive workspace, the scoped scratch allocation is exactly two cells. This bound requires no full-rank assumption and includes the zero-residual branch.
:::
