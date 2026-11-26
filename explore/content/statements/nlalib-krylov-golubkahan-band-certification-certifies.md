---
kind: statement
id: nlalib-krylov-golubkahan-band-certification-certifies
uid: d8206024-5e81-58e5-ae97-3f5e3e459750
---

::: theorem decl:NLAlib.Krylov.GolubKahan.Band.Certification.certifies name="Total exact certificate over an abstract extension" id=execution
For all sizes $(m,n,\ell,q)$, every real $m\times n$ matrix $\mathbf{A}$, every interpretation whose products are the exact products with $\mathbf{A}$ and its adjoint and whose basis extension meets the [exact contract](/explore/statements/12a7ec72-6c64-59e6-b7de-7aff8d055ba2/), and every tape, the counted run of the fixed program succeeds within its static budget and resource bounds. It consumes $n\ell$ words of the tape, releases its scratch, and leaves five output blocks that decode to an [exact run](/explore/statements/4dfc5d02-1a58-53ba-8b1b-f151f3a1fa58/) for $\mathbf{A}$ from the start block decoded from the tape.

There is no rank, nonbreakdown, or successful-run hypothesis. The extension operation is abstract in this statement: it certifies the driver for any interpretation meeting the exact contract and does not name a concrete orthogonalization program.
:::
