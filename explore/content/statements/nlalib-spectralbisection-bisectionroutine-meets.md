---
kind: statement
id: nlalib-spectralbisection-bisectionroutine-meets
uid: 0cd1700e-4394-558a-9ae2-d85e718cf79c
---

::: theorem decl:NLAlib.SpectralBisection.bisectionRoutine_meets name="Execution agrees with the word algorithm" id=execution
Under the primitive contracts, readable inputs, sufficient separated output capacity, and exact bounded dimension literals, the solver terminates and stores exactly the basis and values returned by the mathematical word algorithm with the same arithmetic and random tape. It consumes exactly

$$(L+1)(n+4n^2)$$

random words and releases its scoped scratch storage. This correspondence does not require a numerical-success assumption.
:::
