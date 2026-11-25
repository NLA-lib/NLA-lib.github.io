---
uid: 043355f4-9949-5f19-87f1-1f96a7841153
kind: index
id: arithmetic-models
title: Arithmetic models
summary: Definitions of the arithmetic contracts used by the algorithm pages.
status: ready
---

An algorithm specifies which operations are performed. An arithmetic model specifies
what each operation may return. These choices are separate from the storage format,
matrix-access model, and resource charges.

The library states a model as hypotheses of a theorem or certificate: a property of the
scalar machine, and contracts for the vector and matrix operations that the program
calls. The pages mark a statement with the facts that its Lean signature or the
library's certificate record establishes, and [search](/explore/search/) filters on them.
A statement without a mark has no established fact; it is not thereby exact or
deterministic.

{{ statement:exact-arithmetic-3bd3e996 }}

{{ statement:standard-rounding-65719e4e }}

{{ statement:relative-error-blas-matvec-5bd8642a }}

{{ statement:sequential-summation-in-standard-rounding-01b91c62 }}

{{ statement:accuracy-budgets-e4a4357b }}

Access, randomness and work are not arithmetic. They are marked separately, and a
statement can carry several of these facts.

{{ statement:uniform-model-and-oracle-e571c120 }}

{{ statement:random-tape-6de47ac7 }}

{{ statement:closed-and-manifest-work-b7eb3355 }}

[Open ordinary CG](/explore/algorithms/conjugate-gradient/implementations/ordinary/)

[Open ordinary Lanczos](/explore/algorithms/lanczos/implementations/ordinary/)

[Computational-model theory](/explore/theory/computational-models/)
