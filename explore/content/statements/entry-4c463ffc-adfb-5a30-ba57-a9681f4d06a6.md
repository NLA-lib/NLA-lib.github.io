---
kind: statement
id: entry-4c463ffc-adfb-5a30-ba57-a9681f4d06a6
uid: 4c463ffc-adfb-5a30-ba57-a9681f4d06a6
---
::: theorem result:gaussian-ose name="Gaussian subspace embedding"
For $\mathbf{U}$ with orthonormal columns,
$\mathbf{S} = \lvert k \rvert^{-1/2} \, \mathbf{G}$ is a subspace embedding for
$\operatorname{range} \mathbf{U}$ with constants
$$\Bigl(1 \mp \frac{\sqrt{\lvert p \rvert} + t}{\sqrt{\lvert k \rvert}}\Bigr)^2$$
outside probability $2 e^{-t^2/2}$, for
$0 \le t \le \sqrt{\lvert k \rvert} - \sqrt{\lvert p \rvert}$; Gordon's Gram
sandwich for the $k \times p$ Gaussian $\mathbf{G}\mathbf{U}$.
Woodruff’s Theorem 6 gives $\lvert k \rvert = \Theta((\lvert p \rvert + \log(1/\delta))/\varepsilon^2)$ without a constant; Martinsson and Tropp state
$1 \mp (1 + \sqrt{\lvert p \rvert})/\sqrt{\lvert k \rvert} \mp t/\sqrt{\lvert k \rvert}$ for our $t$.
:::
