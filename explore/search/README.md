# Matrix lemma search prototype

For LLM-assisted browsing and context recovery, use the
[documentation MCP server](DOCUMENTATION_MCP.md). It exposes the original mathematical API
without loading proof bodies and does not require the embedding dependencies below.

An isolated local prototype alongside the explorer. It searches proved Matrix declarations and
matrix-related ForMathlib helpers; it does not alter the deployed explorer, library, or proofs.

The pipeline combines BM25 over names/docstrings/signatures with local 384-dimensional
`BAAI/bge-small-en-v1.5` embeddings using reciprocal-rank fusion. The model runs through
FastEmbed/ONNX on CPU. Queries and declarations are not sent to a hosted embedding service.
Initial setup downloads Python packages and public model files. Model downloads require
`--download-model`; omit that flag on subsequent runs to use only the local cache.

## Run

From the explorer repository root:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r search/requirements.txt
# Supply an existing schema-1 extraction from the NLAlib explorer workflow.
.venv/bin/python -m search.matrix --data data/explore-data.json --download-model --serve 8765
```

Open <http://127.0.0.1:8765>. The server binds only to loopback. It offers retrieval, not Lean
execution. Source links point to the extraction's exact commit. The prototype is not deployed.

CLI examples:

```sh
.venv/bin/python -m search.matrix --data data/explore-data.json \
  --query 'Taking the generalized inverse twice recovers the matrix'
.venv/bin/python -m search.matrix --data data/explore-data.json \
  --query 'specNorm (X * Y) ≤ specNorm X * specNorm Y'
.venv/bin/python -m search.matrix --data data/explore-data.json \
  --evaluate search/matrix_queries.json
```

`--mode lexical`, `semantic`, and `hybrid` permit direct comparison. For a dependency-free lexical
baseline, use `python3` with both `--lexical-only --mode lexical`. That baseline is BM25, not an
exact reproduction of the deployed explorer's ranking. Missing embeddings never silently fall
back to keywords. The `.search-cache/` directory contains downloaded models and embedding arrays;
arrays are keyed by extraction SHA-256, model name, document text and index format version.

## Variable names and Lean checking

A text-shape heuristic ignores short variable spellings while preserving repeated occurrences.
It helps retrieve `specNorm_mul_le` using `X, Y` instead of `A, B`. This heuristic is **not** an
elaborated-expression comparison or a mathematical equivalence checker.

The optional local CLI can test a candidate against a goal with arbitrary variable names and
reordered local hypotheses:

```sh
.venv/bin/python -m search.matrix --data data/explore-data.json \
  --query NLAlib.specNorm_mul_le --limit 1 \
  --lean-repo /path/to/nlalib \
  --context '(leftMatrix rightMatrix : Matrix (Fin 2) (Fin 2) ℝ)' \
  --goal 'NLAlib.specNorm (leftMatrix * rightMatrix) ≤ NLAlib.specNorm leftMatrix * NLAlib.specNorm rightMatrix'
```

The checker imports the candidate's already-built module, applies that candidate at the root,
then uses bounded `solve_by_elim` over local assumptions to close remaining goals. It checks
diagnostics and printed axioms, permitting only `propext`, `Classical.choice`, and `Quot.sound`.
Lean runs in a separate process group with heartbeat, memory, thread and wall-time limits.
It does not rebuild imports. Failure means **not established within these bounds**, not that
the lemma cannot apply. Definitions are searchable, but the checker is intended for theorems.

Context and goal are trusted local Lean input, not a security sandbox. Do not expose this checker
as a public endpoint. Its result explicitly says **checked against local build**: search snapshot
and local compiled-module freshness are not yet verified to match. No automatic rewrite search,
unfolding search, or dependency-aware hypothesis permutation engine is implemented. Lean itself
handles instantiation and local assumption order during the bounded check.

## Evaluation and scope

`matrix_queries.json` contains 22 questions independently prepared before evaluating retrieval.
Expected names were checked in extraction commit `79f8cc2f74523a30d1d53316542b826018e245a4`.
It includes natural-language paraphrases, definite versus semidefinite matrices, norms, spectral
perturbation, projectors, pseudoinverses, truncation and subspace angles. Metrics are hit@5,
hit@10 and reciprocal rank of the first listed relevant theorem. Other relevant answers may
exist; this is a small development benchmark, not a held-out estimate of general performance.

The [saved first evaluation](evaluation.json), over 2,394 declarations, gives:

| Method | Relevant theorem in top 5 | In top 10 | Mean reciprocal rank, top 100 |
|---|---:|---:|---:|
| BM25 keywords | 12/22 | 15/22 | 0.491 |
| Local embeddings | 14/22 | 14/22 | 0.492 |
| Hybrid | 13/22 | 15/22 | 0.502 |

The semantic improvement is modest; fusion does not outperform both components on every metric.
The generic English model still misses queries such as pseudoinverse involution and can confuse
nearby formulations. These measurements do not justify replacing production search or enforcing
reuse automatically. `statement_queries.json` separately checks the same spectral product bound
with original, renamed and subscripted variables; all three retrieve it first in the keyword mode.
Real Lean integration tests check arbitrary multiword variable names and reordered hypotheses,
and reject both a false goal and an unrelated candidate when a local assumption proves the goal.

```sh
python3 -m unittest discover -s tests -p 'test_matrix_search.py'
MATRIX_SEARCH_LEAN_REPO=/path/to/nlalib python3 -m unittest discover -s tests -p 'test_matrix_search.py'
```

Next steps: extract canonical Lean expression trees for reliable structural candidate matching;
include the pinned Mathlib corpus; validate local build/index freshness; collect independent user
queries and relevance judgments; integrate the best-performing retrieval into the explorer and
proof-worker tooling. Semantic retrieval and proof dependencies remain advisory evidence, not a
guarantee that the best possible lemma has been found.
