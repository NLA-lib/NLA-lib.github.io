---
kind: statement
id: uniform-model-and-oracle-e571c120
uid: e571c120-4ca1-5f41-ab7a-d718b5a59289
---

::: definition name="Uniform model and oracle" id=access
An operation model is uniform (`Ops.AccessModel.Uniform`) when the contracts of its
primitives and queries do not depend on the sizes or on the input. No primitive is then
an oracle for the problem data: the program reaches its input through the stored buffers.
A uniform model can still call kernels, which are primitives with their own contracts and
with work supplied by the caller.

A matrix–vector product that is a primitive with a contract for a given operator is an
oracle: the operator is semantic data of the model, not entries that the program reads.
:::
