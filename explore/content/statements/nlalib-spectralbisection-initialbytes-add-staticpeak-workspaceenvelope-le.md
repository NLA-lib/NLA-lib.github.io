---
kind: statement
id: nlalib-spectralbisection-initialbytes-add-staticpeak-workspaceenvelope-le
uid: 60207554-de12-55e9-aa40-b0c5c81d3f44
---

::: theorem decl:NLAlib.SpectralBisection.initialBytes_add_staticPeak_workspaceEnvelope_le name="Resident storage" id=resident
For $n\ge2$, including the supplied input, parameter, and output buffers, total resident capacity is at most

$$6n^2L+36n^2+4nL+8n+2L+27+E(n).$$

The supplied buffers contribute $4n^2+n+3$ cells.
:::
