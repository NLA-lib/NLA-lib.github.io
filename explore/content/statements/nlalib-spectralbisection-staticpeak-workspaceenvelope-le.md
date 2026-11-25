---
kind: statement
id: nlalib-spectralbisection-staticpeak-workspaceenvelope-le
uid: cf88b5ab-1c6e-5e1b-a9b7-3af59a9bf94b
---

::: theorem decl:NLAlib.SpectralBisection.staticPeak_workspaceEnvelope_le name="Scratch storage" id=scratch
For $n\ge2$, peak scratch capacity is at most

$$6n^2L+32n^2+4nL+7n+2L+24+E(n).$$

The bound includes the arenas and nested scratch allocations. It is independent of the sign-iteration cap $c$.
:::
