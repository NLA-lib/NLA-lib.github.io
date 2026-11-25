---
kind: statement
id: nlalib-ops-machine-eigh-tofloatmachine-map-samples
uid: d800ebd7-32d8-5630-95fe-390e2cf2603b
---

::: theorem decl:NLAlib.Ops.Machine.eigh_toFloatMachine_map_samples name="Changing the sample representation"
Fix the word machine, decoding, matrix multiplication, and QR functions. Suppose two uniform samplers and two Gaussian samplers agree after maps $f$ and $g$ of their sample inputs. Then the complete mathematical spectral-bisection solver returns identical words after applying those maps to its sample tree.

The agreement is an explicit hypothesis for every uniform scale and sample, and for every Gaussian input. This is an equality of word computations, not a claim that rounded arithmetic is exact real arithmetic.
:::
