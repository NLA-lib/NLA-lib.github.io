# Retiring the old Explorer backend

The Markdown Explorer builds directly from the generic Lean extraction. It no
longer builds an older Explorer first and overwrites its visible navigation.

## Kept

- Exact declaration signatures, source fingerprints and pinned source links.
- Public module/result/declaration records, dependency lists, admission flags,
  snapshot identity, generic keyword search, and safe record paths.
- Editable method/family/implementation/task/theory pages with generated lists.
- Mathematical result titles, aliases, source-backed statements, and rename maps.
- The source-specific Ops CG adapter, which emits fragments and metadata only.
- Independent, optional documentation/lemma-retrieval tools; these do not emit programs.

## Removed

The old program-recognition and target-registry pipeline, registered implementation
inference, Rates/facet tables, resource/status ladder, dependency-graph/catalogue
application, old app/math bundles, and their specialized curation files and tests
are retired. CI no longer extracts or reads the old target-registry file.

Useful algorithm search aliases and result prefixes moved into Markdown headers;
theory source membership is expressed with `module_prefixes`. The builder has no
execution-namespace, specification-catalogue, or NumPy-emitter dependency. Deleting
an old execution declaration does not trigger a stale reviewed-link check.

The generic API has declaration, result, algorithm, task, and module collections.
Discovery associations are labeled as such, without claiming execution correctness
or resource certification. Authored theorem blocks require actual extracted
statements; implementation adapters point to their checked Ops declarations.

Legacy URL redirects and hash-link mappings are retained without the old app.
The retired source graph falls back to the module reference. Declaration renames
preserve statement-change notes; omitted destinations do not invent source records.

## Validation boundary

Migration validation uses temporary outputs and matching source archives. It does
not refresh the pinned 8081 preview or publish a site. Feature-branch commits and pushes
are separate from validation and deployment.
The core repository owns deletion of old execution code and its own checks/tools.
A fresh post-deletion extraction can use the same generic metadata contract.
