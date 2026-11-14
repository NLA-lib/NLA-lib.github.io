# Markdown explorer architecture

The primary explorer has Algorithms, Theory, and Library entry points. Algorithms
can be discovered through overlapping tasks. Theory has its own canonical topics;
the Library is the generated full reference, not a competing editorial taxonomy.

## Canonical identities

| Object | Route below `/explore/` | Editable source |
| --- | --- | --- |
| Family | `families/galerkin-methods/` | `content/families/galerkin-methods.md` |
| Task | `tasks/eigenvalues/` | `content/tasks/eigenvalues.md` |
| Algorithm | `algorithms/lanczos/` | `content/algorithms/lanczos/index.md` |
| Implementation | `algorithms/lanczos/implementations/ordinary/` | `content/algorithms/lanczos/implementations/ordinary.md` |
| Theory topic | `theory/matrix-polynomials/` | `content/theory/matrix-polynomials.md` |
| Library record | `library/declarations/<name>/` | extracted library metadata |

Task membership does not determine an algorithm's URL. Lanczos appears under
eigenvalues, matrix functions, quadrature, and trace estimation, with one identity.
Lanczos matrix-function approximation and stochastic Lanczos quadrature are separate
compositions, linked to the common process through `uses`.

## Families, mathematical methods, and implementations

The Algorithms entry point lists tasks. Each task owns a custom organization of
methods, using ordered `groups` in its Markdown front matter. A task can group by
algorithmic family, problem structure, output, or the role of a shared component.
Those groups need not be uniform across tasks. Lanczos can appear under Krylov
eigenvalue methods in one task and shared quadrature recurrences in another.

Every group links to the same canonical mathematical algorithm pages. Those pages
own their implementations, with arithmetic choices inside an implementation.
Task membership is derived from the task groups, so editing placement also updates
the method's backlinks. Task-specific card descriptions do not change the method's
identity or definition. Group membership is discovery metadata, not a proof claim.

Global family pages remain shared conceptual references. A task group can link a
family while selecting only the members relevant to that task. The Algorithms
entry point does not also show a parallel global family or method list.

Galerkin methods contains CG, PCG, Block CG, and FOM. The CG page owns the mathematical
iterate and its exact guarantees; carried-residual and fully reorthogonalized
recurrences link back to that one analysis. PCG has a separate mathematical page:
its preconditioned search spaces and spectral hypotheses must not be mixed with
unpreconditioned CG statements.

RSVD-type methods contains the untruncated range-finder approximation, late-truncated
RSVD, early-truncated RSVD, and early-and-late-truncated RSVD. Their mathematical
outputs differ. The combined method has an intermediate sketch rank and a final
output rank; setting them equal makes the final truncation redundant. Each method
owns its analysis and lists concrete implementations separately. The combined and
block methods are explicitly marked as outlines/placeholders until reviewed.

A canonical URL is a navigation identity, not a claim that the algorithm has canonical
exact-arithmetic theory. Only genuinely canonical mathematical methods own that theory.
Specific numerical algorithms, including Shah spectral bisection, keep their numerical
analysis with the implementation; a strategy overview supplies navigation.

Mathematical method pages present definitions and method-specific guarantees.
Implementation pages present recurrences, resources, and connection theorems to the
mathematical output, followed by arithmetic-dependent accuracy. A shared theorem is
stored once in the extracted library and can be referenced from several pages.

## Organizing mathematical theory

Theory is organized around mathematical objects and reusable questions, rather than
algorithm execution steps or source folders. Each topic has an introduction,
definitions, hypotheses, results, prerequisites, and algorithm connections.

Matrix analysis groups norms, spectra, singular values, subspaces, pseudoinverses,
and perturbation theory. Polynomial approximation groups Chebyshev polynomials,
minimax approximation, orthogonal polynomials, and quadrature. Probability groups
concentration and random matrices. Computational models explain operation access,
arithmetic contracts, representation, and resources.

Parents are many-to-many. Matrix polynomials and Krylov spaces belong to both matrix
analysis and polynomial approximation, with one canonical page each. A theorem can
be listed in multiple topics but has one extracted statement record. "Used by"
links are editorial discovery relationships, not proof dependencies; the Library
retains the actual declaration dependencies.

Theory pages do not inherit the Operations and Storage / Accuracy template. Those
sections describe an algorithm implementation. Arithmetic selection appears only
where a checked program/model connection is available.

## Authored prose and generated evidence

`content_pages.py` reads YAML headers and ordinary Markdown. Generated markers
insert relationship lists and snapshot-backed library records. Statement blocks
combine editable prose with an exact Lean signature and source link. The
CG adapter fills its Ops-specific fragments; the Markdown controls the page
around them. A matching current core is optional and never inferred from an old
published extraction.

Placeholders reserve navigation identities and explain the intended scope. They do
not manufacture code, operation counts, arithmetic choices, or theorems. Existing
library statements can still be listed on an outline page, with that distinction
visible. Missing metadata and broken typed references reject the build.

Empty generated sections are omitted. Unknown task-group members, duplicate group
IDs, and cycles in component, theory-parent, or prerequisite graphs reject the
build. The [organization audit](organization-audit.md) records a review of every
authored page and remaining exposition gaps. `audit_organization.py` checks task
reachability and source-selector coverage against a selected snapshot.

The source and authoring guide is [content/README.md](../../content/README.md).

The build reads the generic extraction directly. It has no old program/target
registry or code-emitter dependency. See [legacy retirement](legacy-retirement.md).
