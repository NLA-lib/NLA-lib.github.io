---
kind: statement
id: spectral-bisection-operation-count-accuracy
uid: c6b82b37-af7d-54c6-8a6e-3649062c1667
---

::: theorem result:spectral-bisection-operation-count-accuracy name="Operation count and accuracy on one event" id=operation-count-accuracy
Let $\mathbf{A}\in\mathbb{C}^{n\times n}$, $n\ge2$, be Hermitian with $\|\mathbf{A}\|_2\le R$, stored as $n^2$ pairs of words, with a tolerance $0<\varepsilon\le2^{-15}$, a parameter $\beta>0$, a depth $L\ge\lceil\log_2\varepsilon^{-1}\rceil+5$ and a sign-iteration cap $c$ of at least `newtonSchulzSteps`. Matrix multiplication and QR are primitives whose declared cost at order $j$ is at most $T(j)$, with $T$ monotone and superadditive. Arithmetic is a floating-point machine accurate with unit roundoff $u$ (`FloatMachine.IsAccurate`), natural literals up to $\max(n,4)$ are exact, and the tape holds independent uniform and standard Gaussian draws, rounded to machine words. Let $0<\theta\le1$. The Lean statement gives the conditions that make $u$ small relative to $\theta\beta$ and $\beta$, and those on $\beta$, the absolute-error floor and the range.

Then, for every interpretation of the primitives that meets the model, with probability at least $1-\theta$ over the tape the run succeeds, its work and its span are at most

$$(L+1)\,c\,(362n^3+146n^2+222n)+L\,(1587n^3+760n^2+2429n+305)+1599n^3+818n^2+2509n+680+(L+1)(2c+11)\,T(n),$$

its scratch and memory are within the bounds of its specification, and it stores $\mathbf{U}$ and a real vector $\mathbf{d}$ with

$$\|\mathbf{A}-\mathbf{U}\operatorname{diag}(\mathbf{d})\mathbf{U}^{\mathsf{H}}\|_2\le2\varepsilon R,\qquad(1-\varepsilon/3)^2\mathbf{I}\preceq\mathbf{U}^{\mathsf{H}}\mathbf{U}\preceq(1+\varepsilon/3)^2\mathbf{I}.$$

The last term of the work is the matrix work; the others count the instructions that are not matrix operations. The success of the run and its resource bounds hold on every tape; only the accuracy of the output is probabilistic.
:::
