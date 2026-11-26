# Statements added concurrently on main

PR #25 introduced these six BCW statements at `02a1515`. They are outside the
initial 778-UUID snapshot. The cleanup preserves them byte for byte as merged;
they are not counted as Luna proposals. A presentation inspection found explicit
matrix/vector fonts, standard transpose/adjoint fonts and no inline bibliography
strings to relocate. This is not a mathematical review.

| UUID | Source | Main Git blob |
|---|---|---|
| `a4b8b810-e947-4596-8b7f-424f26b8dfbd` | `explore/content/statements/bcw-asymptotic-depths.md` | `5d3e558703652ac18586b2150bd11d378b46df8b` |
| `39a7e927-15c2-41c3-9d83-4b3358e74d95` | `explore/content/statements/bcw-definition.md` | `325aa2005de4e4cc1ef0a79abf1e7c7b08295ca9` |
| `affc75db-b874-4278-af6e-0e752cd51a1d` | `explore/content/statements/bcw-frobenius-error.md` | `22884748046f734a3b477a4e2fe98f45ac847e58` |
| `2c700dd8-8cdb-4f06-8f14-c38f62c880b0` | `explore/content/statements/bcw-large-p-error.md` | `c72c49ab63a20fff1149a2358aacadf3102df011` |
| `da4acb45-45b9-491c-a313-d000b003ec2b` | `explore/content/statements/bcw-large-p-tail.md` | `9b13bd173a7dc9e3de439c8e1e6faffecb99e1ba` |
| `a72cc0e1-75e8-408a-827b-dc211b166032` | `explore/content/statements/bcw-small-p-error.md` | `f14439dc6442c367be296c7470132ead8a0a41e4` |

Standalone-context follow-up: several bounds use `OPT_p` and shared input
conventions supplied by the algorithm page rather than repeating them in the
statement. Clarify those conventions on independent pages in a separate proposal;
no assumptions, constants, Gaussian-law claims or outputs were rewritten here.
