# CG Explorer pilot

The Markdown explorer at `/explore/` has Algorithms, Theory, and Library entry points.
The full generated reference lives at `/explore/library/`. The algorithms path adds a hierarchy:
family → mathematical method → implementation → arithmetic selection.
CG and PCG have separate mathematical pages in the Galerkin family. Three implementation pages show natural-language
pseudocode and theorem statements. Native disclosures hold Lean code and details.
The shared algorithm and vector-level operation/storage estimates precede the model
selector. Arithmetic assumptions, successful-execution statements and convergence
results appear under the selected model. Implementation proof infrastructure stays
in disclosures. Properties are titled result cards, with no comparison table.

Each mathematical method page stacks implementation cards with descriptions below each link, without bullets.
Implementation pages omit sibling navigation and the state metadata strip. Algorithms and
results use grey boxes with a 4px black left border only, square corners and KaTeX formulas.
Lean lives in disclosures.
Operations show concrete vector-operation counts and work estimates; memory shows
buffer counts and an explicit payload-cell bound including operation workspace.
The selected model name is not repeated below the selector. All card types share
`.explorer-card` and `.explorer-disclosure` in `web/cg-pilot.css`, with common spacing,
typography and a monochrome palette. Statement labels run inline with the first
paragraph: bold Theorem or Definition, an optional parenthesized name, and a bold period.
Statement bodies use upright Source Sans 3 with line height 1.5. Both Theorem and
Definition labels, including the parenthesized name and closing period, are italic;
the keyword and period are bold. Lean disclosures remain upright. Mathematics uses
standard KaTeX HTML rendering and its bundled fonts. Pseudocode has one operation
per numbered line, in Lean execution order, with separate initialization and loop
phases; the full-reorthogonalization sweep is a nested loop. The ordinary CG display
shows the zero-start initializer; the exact general-start initializer is in Lean details.
Implementation sections are Operations and Storage, then Accuracy.
The arithmetic selector is unboxed. Presentation math uses
`\mathbf` for vectors and matrices; original Lean statements are preserved exactly.
The concept page introduces four core mathematical results in plain language;
additional extracted results remain in a closed disclosure.

Ordinary CG uses the carried-residual implementation; the separate recomputed-residual
implementation is removed. Old variant URLs redirect to the corresponding implementation,
preserving the selected model. The exact-arithmetic Accuracy section has one theorem:
`Solve.runs_solve` identifies the actual stored output with the mathematical CG or PCG
iterate. CG and reorthogonalized CG admit any cap and stop at the earlier of the cap
and Krylov grade. The current PCG theorem requires the iteration count to be at most
its preconditioned Krylov grade. Convergence and finite-termination statements remain
on mathematical method pages. Operations and storage retain their own resource results.
Rounded sections retain execution and convergence-with-rounding results.

Ordinary CG supports exact arithmetic, abstract relative-error BLAS
and matvec, standard sequential and standard pairwise views. The abstract model uses
`Rounded.runs_solve` composed with `Output.stable`. Sequential and pairwise views use
`Standard.runs_solve_of_model`; their assumptions and reduction bounds differ.
`/explore/arithmetic-models/` explains all four models, cancellation-aware dot error,
componentwise axpy error, normwise matvec error and the accuracy envelope. It is
linked directly below every model selector. Other implementations show a missing-evidence state
for rounded models. The model is stored in `?model=...`, survives family and method navigation,
and supports reload and browser Back. Without JavaScript all model sections remain
readable. The selector controls arithmetic/reduction choices, rather than promising
arbitrary combinations of storage, cost and backend models.

This pilot reads new working-tree sources separately from the published library
extraction. Every preview file has a SHA-256 fingerprint and an entry in
`api/v1/cg-pilot.json`. Source links go to GitHub. Published source records use their
pinned file-and-line URLs; unpublished preview declarations link to the repository
and explicitly state that those changes are not yet published. It does not fabricate public commit links or
claim a full `Ops.Algorithm` resource certificate. Source inspection is a presentation
and drift check; the library's Lean checks establish formal correctness.

Build using matching published data and sources, with the optional current core:

```sh
python3 explore/build.py --data /path/to/explore-data.json --src /path/to/published/NLAlib --out _site/explore --core-src /path/to/current/NLAlib
python3 preview.py --directory _site --port 8081
```

Open `http://127.0.0.1:8081/explore/algorithms/conjugate-gradient/`.
The carried-residual model demo is at
`/explore/algorithms/conjugate-gradient/implementations/ordinary/?model=pairwise`.

Checks:

```sh
cd explore
python3 -m unittest discover -s tests
python3 tests/check_cg_pilot_browser.py --chromium /path/to/chrome-headless-shell
```

The adapter does not edit the library or its extraction. The regular build renders
Markdown pages after filling the optional CG fragments. A build without current
core sources shows implementation outlines. See [the architecture](explorer-architecture.md)
and [authoring guide](../../content/README.md) for editable pages and generated metadata.
