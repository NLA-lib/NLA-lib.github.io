# Research-facing editorial cleanup

The Luna pass inspected all **778 entries** in the agreed snapshot: 242 authored
statements and 536 additional named-result candidates. Raw Lean helper descriptions
are deferred. This is an editorial pass, not an academic peer-review attestation.

| Outcome | Entries |
|---|---:|
| Proposed editorial changes | 606 |
| Inspected, unchanged | 129 |
| Held for mathematical/formulation review | 38 |
| No complete NL prose | 3 |
| Possible named-result alias | 2 |

Changes standardize vector/matrix fonts, move bibliographic strings to existing
structured references, add scope-compatible definition links and clean sentence
transitions. UUIDs, source kinds, formal bindings and relationships are preserved.
Original hypotheses and expressions are retained; the small reviewed pilot
layout/notation exceptions are explained in `root-pilot-review.md`.

- [Instructions for Luna agents](../luna-editorial-cleanup.md)
- [Per-UUID outcomes](reviewed-inventory.csv) and [complete scope](research-scope-inventory.csv)
- [Follow-up issues](follow-up-issues.md), including missing assumptions and uncertain locators
- [68 possible authored/generated aliases](possible-authored-aliases.csv), left unmerged
- [Concurrent BCW additions](concurrent-main-additions.md), preserved byte for byte
- [Coordinator review and corrections](root-pilot-review.md)

Validation: the existing Explorer test suite passed (139 tests, 8 optional skips); all 6,311
authored equations passed KaTeX checks. The source audit validates identities,
parsed titles, kinds, bindings, math fragments and link targets. All 605 relocated
key/locator associations remain present in both the pinned source records and the
current library build. The complete build succeeds with 152 authored pages, 19,711
library records and 17,854 collaboration objects. These checks do not certify
theorem truth or source adequacy.

The comparison baseline is site commit `a1d2898` with library revision
`83c32ccbc1cadb2fd73c94081f5f9f6fe052a817`. The current build uses library revision
`e207eefa3d0c91354b42affc0bfcd982a3b05807` to support concurrently merged BCW pages.
An earlier checkpoint was merged through PR #24; newer proposals remain on the
cleanup review branch. The inventory marks current source versions observed on main.

## Standalone statements follow-up

The subsequent [context and commentary pass](standalone-context-review.md) responds
to gaps found on the live CG page. It screens the same 778 UUIDs, edits 204 source
entries and separates commentary from mathematical boxes. Its
[final inventory](standalone-inventory.csv) records current proposal hashes and
remaining context issues separately from this earlier pass.
