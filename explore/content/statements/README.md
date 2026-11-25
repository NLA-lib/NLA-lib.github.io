# Shared statement sources

Each file here owns one authored theorem (or definition). A page imports it using
its stable `id`, not a filesystem path:

```markdown
{{ statement:cg-chebyshev-bound }}
```

For example, `cg-chebyshev-bound.md` has the following structure:

```markdown
---
kind: statement
id: cg-chebyshev-bound
uid: a-permanent-uuid
---

::: theorem result:cg-chebyshev-bound name="Chebyshev convergence"
The mathematical statement, including hypotheses and LaTeX.
:::
```

Use an actual canonical UUID for `uid` when adding a new file. Keep both identifiers
when renaming or moving the file. The UUID owns editor revisions, discussion, and
reactions; the readable ID is the import key. Multiple pages can import the same
file and share its text and identity. Each page keeps its own connecting exposition.
Remove an import to remove a placement; do not delete a shared file still in use.

The block's `result:` or `decl:` reference supplies exact Lean evidence. Existing
checks still reject unknown evidence, mismatched declaration kinds, unsourced
checked-theorem blocks, and reported admissions presented as checked theorems.
An optional `id=` on the block preserves a particular statement fragment link.
Do not nest statement imports or generated sections inside a statement file.

The 137 authored theorem blocks were extracted into these files without changing
their expanded page content. The 105 authored definitions also have individual sources so page Markdown consists
of exposition and imports. Legacy inline blocks remain supported by the renderer. Results
which only have generated Lean documentation still use that fallback until given
a curated statement source; the local editor supports editing their readable text.

Imports must occupy their own line. Code-fence examples remain literal. Unknown
imports, duplicate IDs/UUIDs, duplicate imports on the same page, and malformed
source blocks reject the build. The static `api/v1/editorial-statements.json`
registry records file hashes and every importing page. Page metadata also records
the resolved-body hash, so a shared-statement edit invalidates dependent content
fingerprints even when a page's own Markdown file did not change.

Publishing remains separate from the local editor. Local draft/revision saves do
not write these files; future accepted proposals will update these fixed source
files through the protected GitHub workflow.
