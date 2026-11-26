# Follow-up issues from the editorial pass

This pass preserves mathematical claims and records uncertainties. It does not
supply peer-review attestations. The detailed per-UUID reports and
`reviewed-inventory.csv` retain the baseline revisions and editorial outcomes.

## Complete standalone formulations

- Givens QR has only the fragment “of a tall upper Hessenberg matrix.” Its proposed
  citation-only cleanup was held without materializing a new file.
- The Arnoldi-Hessenberg, LU and Fréchet entries include citation-only formulations.
  No theorem summary was invented for them.
- Several CG/Lanczos, Schur, small-eigenvalue, RBKI and Nyström bounds refer to
  “the same hypotheses,” “as above,” undefined parameters or unnamed machine
  contracts. Recovering those assumptions needs a separate mathematical proposal.
- Some named result groups contain several distinct claims. Their identities were
  not merged, and ambiguous materializations were held for review.

## Check sources without upgrading their status

- Verify the flagged Greenbaum, Saad, Gautschi, Szegő, Davis, Trefethen,
  Paley–Zygmund and Achlioptas locators. The reports distinguish a retained locator
  from a checked source claim.
- The Dasgupta–Gupta and other mentioned secondary works need confirmed bibliography
  associations before their attribution can be relocated safely.
- Keep comparisons between printed results and the local formulation explicit:
  real versus complex fields, exact versus rounded arithmetic, different constants,
  boundary/support cases, and draft-only provenance matter.
- Existing references to maintainer drafts remain references to drafts. They were
  not converted into published proof claims or independent review badges.

## Review identities and definition targets separately

- `possible-authored-aliases.csv` records 68 possible generated/authored aliases.
  `root-generated-aliases.md` records two additional named-result pairs. Distinct
  UUIDs, discussion threads and histories were preserved.
- Resolve real-only Krylov definitions before linking them from general RCLike
  statements. Check normalized embedding definitions against general two-constant
  conditions; a similar name is insufficient.
- Check the eigenvalue-ordering and majorization conventions flagged in the
  Schur–Horn reports before changing their mathematical prose.
- The six concurrently merged BCW statements are preserved separately. Their
  common input conventions and `OPT_p` notation are supplied by the algorithm page;
  independently readable statement pages may need explicit context in a later edit.
