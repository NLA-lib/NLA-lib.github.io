---
kind: statement
id: entry-d5aa8c62-cf4f-52b4-a631-4303da76fdc7
uid: d5aa8c62-cf4f-52b4-a631-4303da76fdc7
---
::: theorem result:measurable-selection name="Measurable selection from a closed set with compact sections"
Let $X$ be a topological
space whose open sets are measurable, $Y$ a finite-dimensional Hausdorff real topological vector
space with its Borel $\sigma$-algebra, and $S \subseteq X \times Y$ closed with every section
$S_x = \{y \mid (x, y) \in S\}$ nonempty and the sections lying locally uniformly inside compact
sets (each $x$ has a neighbourhood $U$ and a compact $K$ with $S_{x'} \subseteq K$ for
$x' \in U$). Then there is a Borel measurable $f : X \to Y$ with $(x, f(x)) \in S$ for every $x$
(the lexicographically least point of each section, in the coordinates of a basis, measurable
by `IsClosed.measurable_of_forall_toLex_equivFun_le`). Upstream candidate.
The cited comparison is for weakly measurable closed-valued correspondences into a Polish space;
here the condition is a closed set with locally compact sections in a finite-dimensional space.
:::
