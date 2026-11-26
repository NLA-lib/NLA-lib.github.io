---
kind: statement
id: entry-5b7d48c0-fcee-57b8-8b57-f2a9af6012b3
uid: 5b7d48c0-fcee-57b8-8b57-f2a9af6012b3
---
::: theorem result:nystrom-helps name="Nyström helps"
In singular-value form, for positive semidefinite $\mathbf{H}$,
$$\sigma_k(\mathbf{H} - \mathsf{nystrom}(\mathbf{H}, \mathbf{\Omega})) \le
\sigma_k((\mathbf{I} - \mathbf{P}_{\mathbf{\Omega}})\mathbf{H})$$
at every index $k$: the Nyström error is at most the error of projecting $\mathbf{H}$ onto the
orthogonal complement of the test space. At $\mathbf{\Omega} = \mathbf{H}\mathbf{\Omega}_0$ this
compares Nyström from the sample $\mathbf{H}\mathbf{\Omega}_0$ with the randomized SVD of
$\mathbf{H}$ (`NLAlib.sub_rsvd`).
The cited Lemma 5.2 gives the comparison for unitarily invariant norms by a block computation;
here it is expressed basis-free as
$$\mathbf{H}/\mathbf{\Omega} \preceq (\mathbf{I} - \mathbf{P}_{\mathbf{\Omega}})\mathbf{H}
(\mathbf{I} - \mathbf{P}_{\mathbf{\Omega}})\,.$$
:::
