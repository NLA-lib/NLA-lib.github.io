---
kind: statement
id: nlalib-spectralbisection-certifies-work
uid: f7cd488d-0af0-5fd3-8467-b88519a1ea9d
---

::: theorem decl:NLAlib.SpectralBisection.certifies_work name="Work and sequential span" id=work
For $n\ge2$, with exact decoding of natural literals through $\max(n,4)$ and the stated primitive cost contracts, both total work and sequential span are at most

$$\mathcal{H}(n,L,c)+(L+1)(2c+11)T(n).$$

At a node of dimension $k$, splitting costs at most $(2c+9)T(k)$ in matrix work and reconstruction at most $2T(k)$. Disjoint node slots and superadditivity bound their sum at each level by the root-size term. The scalar budget $\mathcal{H}$ remains conservative.
:::
