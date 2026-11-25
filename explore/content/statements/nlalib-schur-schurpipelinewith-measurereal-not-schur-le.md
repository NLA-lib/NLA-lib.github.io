---
kind: statement
id: nlalib-schur-schurpipelinewith-measurereal-not-schur-le
uid: 92fb9508-4283-5233-8460-928bf7187ea8
---

::: theorem decl:NLAlib.Schur.schurPipelineWith_measureReal_not_schur_le name="Any stages that meet their contracts compose" id=swappable-stages
Let a norm estimate with constants $c_1,c_2$, a regularizer with error $\delta_R$ and failure $\varphi_R$ into a class $C$, a reducer with errors $(\varepsilon_{H,U},\varepsilon_{H,T})$, and a Schur core from a class $C'$ with errors $(\varepsilon_{C,U},\varepsilon_{C,T})$ and failure $\varphi_C$ meet their contracts, the regularizer on norms at most $2/c_1$ and the core on norms at most $4/c_1$. Let the reducer's similarity carry $C$ into $C'$. Put $\varepsilon=(1+\varepsilon_{H,U})(1+\varepsilon_{C,U})-1$, and assume $c_1>0$, $8(n+1)u\le1/4$, $\delta_R\le1/c_1$, $0\le\varepsilon_{H,T}\le1/8$, $\varepsilon_{H,U},\varepsilon_{C,U}\ge0$, $\varepsilon\le1/16$ and $\varphi_R,\varphi_C\ge0$. Then, except with probability $\varphi_R+\varphi_C$, the pipeline stores the flag $0$ and a Schur output of $\mathbf{A}$ with

$$\|\mathbf{A}-\widehat{\mathbf{U}}\widehat{\mathbf{T}}\widehat{\mathbf{U}}^{\mathsf{H}}\|_2\le\Bigl(2c_2\sqrt{n+1}\bigl(\delta_R+3\varepsilon_{H,T}/c_1+\varepsilon_{C,T}+8\varepsilon/c_1\bigr)+8(n+1)u\Bigr)\|\mathbf{A}\|_2,$$

$$\|\widehat{\mathbf{U}}^{\mathsf{H}}\widehat{\mathbf{U}}-\mathbf{I}\|_2\le2\varepsilon+\varepsilon^2.$$
:::
