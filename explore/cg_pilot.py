"""Overlay a source-backed CG pilot on a built Explorer.

This is an explicit local preview of the new Ops API, alongside the published
library snapshot. It never upgrades source inspection into a formal certificate.
Run after build.py: python3 cg_pilot.py --site ../_site/explore --src <NLAlib>
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
from cg_presentation import concept_page, models_page, variant_page

BASE = '/explore/algorithms/conjugate-gradient/'
CG = 'NLAlib/Krylov/CG/'
MODELS = [('exact', 'Exact arithmetic'), ('relative', 'Relative-error BLAS + matvec'),
          ('sequential', 'Standard rounding · sequential'),
          ('pairwise', 'Standard rounding · pairwise')]
PSEUDOCODE = {
    'carried': [
        ('Initialize:', [
            r'Copy $b$ into $r$.',
            r'Copy $b$ into $p$.',
            r'Compute $\rho\leftarrow\langle r,r\rangle$.',
        ]),
        (r'Repeat while $\rho>0$, up to the iteration cap:', [
            r'Compute $q\leftarrow Ap$.',
            r'Compute $\sigma\leftarrow\langle p,q\rangle$.',
            r'Compute $\alpha\leftarrow\rho/\sigma$.',
            r'Update $x\leftarrow x+\alpha p$.',
            r'Negate $\alpha\leftarrow-\alpha$.',
            r'Update $r\leftarrow r+\alpha q$.',
            r'Compute $\rho_{\mathrm{new}}\leftarrow\langle r,r\rangle$.',
            r'Compute $\beta\leftarrow\rho_{\mathrm{new}}/\rho$.',
            r'Copy $r$ into $q$.',
            r'Update $q\leftarrow q+\beta p$.',
            r'Copy $q$ into $p$.',
            r'Copy $\rho_{\mathrm{new}}$ into $\rho$.',
        ]),
    ],
    'pcg': [
        ('Initialize from the starting iterate:', [
            r'Copy $b$ into $r$.',
            r'Compute $q\leftarrow Ax$.',
            r'Set $\alpha\leftarrow-1$.',
            r'Update $r\leftarrow r+\alpha q$.',
            r'Apply the inverse preconditioner $z\leftarrow Pr$.',
            r'Copy $z$ into $p$.',
        ]),
        ('Repeat for the prescribed horizon:', [
            r'Compute $\rho\leftarrow\langle r,z\rangle$.',
            r'Compute $q\leftarrow Ap$.',
            r'Compute $\sigma\leftarrow\langle p,q\rangle$.',
            r'Compute $\alpha\leftarrow\rho/\sigma$.',
            r'Update $x\leftarrow x+\alpha p$.',
            r'Negate $\alpha\leftarrow-\alpha$.',
            r'Update $r\leftarrow r+\alpha q$.',
            r'Apply the inverse preconditioner $z\leftarrow Pr$.',
            r'Compute $\rho_{\mathrm{new}}\leftarrow\langle r,z\rangle$.',
            r'Compute $\beta\leftarrow\rho_{\mathrm{new}}/\rho$.',
            r'Copy $z$ into $u$.',
            r'Update $u\leftarrow u+\beta p$.',
            r'Copy $u$ into $p$.',
        ]),
    ],
    'reorth': [
        ('Initialize from the starting iterate:', [
            r'Copy $b$ into $r$.',
            r'Compute $q\leftarrow Ax$.',
            r'Set $\alpha\leftarrow-1$.',
            r'Update $r\leftarrow r+\alpha q$.',
            r'Copy $r$ into $p$.',
            r'Compute the stopping value $\nu\leftarrow\langle r,r\rangle$.',
        ]),
        (r'Repeat while $\nu>0$, up to the iteration cap:', [
            'Save a copy of the current residual in the history.',
            r'Compute $\rho\leftarrow\langle r,r\rangle$.',
            r'Compute $w\leftarrow Ap$.',
            r'Compute $\sigma\leftarrow\langle p,w\rangle$.',
            r'Compute $\alpha\leftarrow\rho/\sigma$.',
            r'Update $x\leftarrow x+\alpha p$.',
            r'Negate $\alpha\leftarrow-\alpha$.',
            r'Update $r\leftarrow r+\alpha w$.',
            {'loop': r'For each saved residual $q$, in order:', 'steps': [
                r'Compute $\tau\leftarrow\langle q,r\rangle$.',
                r'Compute $\sigma\leftarrow\langle q,q\rangle$.',
                r'Compute $\tau\leftarrow\tau/\sigma$.',
                r'Negate $\tau\leftarrow-\tau$.',
                r'Update $r\leftarrow r+\tau q$.',
            ]},
            r'Compute $\rho_{\mathrm{new}}\leftarrow\langle r,r\rangle$.',
            r'Compute $\beta\leftarrow\rho_{\mathrm{new}}/\rho$.',
            r'Copy $r$ into $z$.',
            r'Update $z\leftarrow z+\beta p$.',
            r'Copy $z$ into $p$.',
            r'Refresh $\nu\leftarrow\langle r,r\rangle$.',
        ]),
    ],
}
OPERATIONS = {
    'carried': r'Each iteration uses one matrix–vector product, two dot products, three scaled vector additions and two vector copies, plus a constant number of scalar operations. If a matrix–vector product costs $T(n)$, then for $k\ge1$ the total work, including initialization, is $$O\bigl(k(n+T(n))\bigr).$$ A zero start initializes with two vector copies and one dot product. An arbitrary initial guess additionally needs one matrix–vector product and one scaled vector addition.',
    'pcg': r'Each iteration uses one matrix–vector product and one application of the inverse preconditioner, three dot products, three scaled vector additions, two vector copies, two divisions and one sign change. Initialization adds one application of each operator, one scaled vector addition and two copies. For $k\ge1$ iterations and operator costs $T_A(n)$ and $T_P(n)$, total work is $$O\bigl(k(n+T_A(n)+T_P(n))\bigr).$$',
    'reorth': r'With cap $k$, there are at most $k+1$ matrix–vector products. Each active round performs the ordinary CG updates, saves a residual and refreshes the stopping test. Round $i$ additionally projects against $i$ stored residuals, each projection using two dot products, one division and one scaled vector addition. The full run makes at most $k(k+1)/2$ such projections. For $k\ge1$ and matvec cost $T(n)$, total work is $$O\bigl(kT(n)+k^2n\bigr).$$',
}
MEMORY = {
    'carried': r'The solver keeps the right-hand side, three $n$-vectors and the cached scalar $\rho$. A round reuses one scratch $n$-vector and three scalar cells. Including the largest temporary workspace of a called operation, $$\text{memory}\le 5n+4+W_{\max}.$$ Storage does not grow with the cap.',
    'pcg': r'The right-hand side and four working $n$-vectors occupy $5n$ cells. Add two scratch $n$-vectors, four scalar cells and the largest workspace needed by any scalar, BLAS, matrix or preconditioner call: $$\text{memory}\le 7n+4+W_{\max}.$$ Storage does not grow with the iteration count.',
    'reorth': r'With cap $k$, the solver reserves $kn$ cells for the residual history. Including the right-hand side, three working vectors, two scratch vectors, scalar scratch and the largest temporary operation workspace, a convenient bound is $$\text{memory}\le (k+6)n+7+W_{\max}.$$ Unlike short-recurrence CG, storage grows linearly with the cap.',
}
VARIANTS = [
    dict(id='carried', title='Ordinary conjugate gradient (CG)', short='Ordinary CG', folder='HSCG/Carried',
         description='Cache the residual’s computed squared length and reuse it in the next round. This saves one dot product per iteration and fixes which computed value is used under rounding.',
         state='x, r, p, ρ', dots='2', scratch='n + 3', code='Alg.lean', step='step', solver='Alg.lean',
         result='The stored iterate is cgIterate at the smaller of the cap and the initial residual’s Krylov grade.'),
    dict(id='pcg', title='Preconditioned CG', short='Preconditioned CG', folder='HSPCG',
         description='Apply a supplied preconditioner and carry the preconditioned residual. The preconditioner is part of the operation contract.',
         state='x, r, z, p', dots='—', scratch='See source budget', code='Alg.lean', step='step', solver='Alg.lean',
         result='The stored output agrees with the preconditioned CG recurrence under the theorem’s exact preconditioner and nonbreakdown assumptions.'),
    dict(id='reorth', title='CG with full reorthogonalization', short='Reorthogonalized CG', folder='Reorth',
         description='Keep the residual history and project the new residual against it. The solver stops at zero residual or the iteration cap.',
         state='x, r, p + history', dots='History-dependent', scratch='See source budget', code='Alg.lean', step='sweep', solver='Solver.lean',
         result='The stored iterate is the exact CG iterate at the cap or its earlier grade; a sufficiently large cap returns a solution.'),
]


def esc(value):
    return html.escape(str(value), quote=True)


class Sources:
    def __init__(self, root, out, published_revision=None, source_hashes=None):
        self.root, self.out = Path(root), Path(out)
        self.files = {}
        self.source_hashes = source_hashes or {}
        self.archive_revision = published_revision if re.fullmatch(r'[0-9a-f]{40}', published_revision or '') else None
        checkout = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
        self.is_checkout = checkout.returncode == 0 and Path(checkout.stdout.strip()).resolve() == self.root.resolve()
        # Link only to a published revision containing identical file bytes.
        refs = subprocess.run(['git', '-C', str(root), 'for-each-ref', '--sort=-committerdate',
                               '--format=%(objectname)', 'refs/remotes/origin/'], capture_output=True, text=True)
        self.revisions = list(dict.fromkeys(refs.stdout.splitlines())) if refs.returncode == 0 else []
        self.source_revisions = {}

    def read(self, path):
        if path not in self.files:
            content = (self.root / path).read_text()
            self.files[path] = dict(text=content, sha256=hashlib.sha256(content.encode()).hexdigest())
        return self.files[path]['text']

    def declaration(self, path, name, kind='theorem'):
        text = self.read(path)
        match = re.search(r'^' + (r'(?:noncomputable )?' if kind == 'def' else '') + kind + r' ' + re.escape(name) + r'(?=\s|:)', text, re.M)
        if not match:
            raise ValueError(f'Missing {kind} {name} in {path}')
        end = re.search(r'\n(?:/--|end |(?:noncomputable )?def |theorem )', text[match.end():])
        block = text[match.start():match.end() + end.start() if end else len(text)].rstrip()
        if kind == 'theorem':
            block = re.split(r'\s*:=\s*by\b', block, maxsplit=1)[0]
        line = text[:match.start()].count('\n') + 1
        if path not in self.source_revisions:
            revision = None
            if not self.is_checkout and self.archive_revision and self.source_hashes.get(path) == self.files[path]['sha256']:
                revision = self.archive_revision
            else:
                for candidate in self.revisions:
                    published = subprocess.run(['git', '-C', str(self.root), 'show', candidate + ':' + path],
                                               capture_output=True, text=True)
                    if published.returncode == 0 and published.stdout == text:
                        revision = candidate
                        break
            self.source_revisions[path] = revision
        revision = self.source_revisions[path]
        github = ('https://github.com/NLA-lib/nlalib/blob/' + revision + '/' + path + '#L' + str(line)
                  if revision else None)
        return dict(path=path, name=name, kind=kind, line=line, text=block,
                    github_url=github,
                    url=github or 'https://github.com/NLA-lib/nlalib')

    def link(self, declaration, label=None):
        url = declaration.get('github_url') or 'https://github.com/NLA-lib/nlalib'
        title = label or ('Full source on GitHub' if declaration.get('github_url') else 'GitHub repository')
        return f'<a href="{esc(url)}">{esc(title)}</a>'

    def code(self, declaration):
        note = '' if declaration.get('github_url') else ' · This core preview is not yet published on GitHub.'
        return '<pre class="definition"><code>' + esc(declaration['text']) + '</code></pre><p class="source-label">' + self.link(declaration) + esc(note) + '</p>'


def build(site, source, published_revision=None, source_hashes=None):
    site = Path(site)
    template = (site / 'algorithms/conjugate-gradient/index.html').read_text()
    # Reapplying the overlay must not register the model controller twice.
    template = re.sub(r'<link rel="stylesheet" href="/explore/cg-pilot.css">|<script defer src="/explore/cg-pilot.js"></script>', '', template)
    sources = Sources(source, site, published_revision, source_hashes)
    records = []
    fragments = {}

    def write(path, title, body):
        page = re.sub(r'<main id="content">.*?</main>', lambda _: '<main id="content"><h2 class="page-title">' + esc(title) + '</h2>' + body + '</main>', template, flags=re.S)
        page = re.sub(r'<title>.*?</title>', lambda _: '<title>NLA-lib · Explorer · ' + esc(title) + '</title>', page)
        page = re.sub(r'<link rel="canonical"[^>]+>', '', page)
        # Absolute asset paths also work on nested variant and source pages.
        page = re.sub(r'(href|src)="(?:\.\./)+(?=(?:css/|style\.|explore[.-]|vendor/))', r'\1="/explore/', page)
        page = re.sub(r'data-root="[^"]*"', 'data-root="/explore/"', page)
        page = re.sub(r'class="explore-pages(?: cg-pilot)?"', 'class="explore-pages cg-pilot"', page)
        page = re.sub(r' data-math-font="[^"]*"', '', page)
        script_hash = hashlib.sha256((Path(__file__).parent / 'web/explore.js').read_bytes()).hexdigest()[:12]
        page = re.sub(r'explore\.js\?v=[^"\s]+', 'explore.js?v=' + script_hash, page)
        page = page.replace('</head>', '<link rel="stylesheet" href="/explore/cg-pilot.css"><script defer src="/explore/cg-pilot.js"></script></head>')
        target = site / path if path.endswith('.html') else site / path / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)

    for variant in VARIANTS:
        folder = CG + variant['folder'] + '/'
        carried = variant['id'] == 'carried'
        record = dict(**variant,
            step_source=sources.declaration(folder + variant['code'], variant['step'], 'def'),
            solver_source=sources.declaration(folder + variant['solver'], 'solve', 'def'),
            exact_theorem=sources.declaration(folder + 'Solve.lean', 'runs_solve'),
            models=[key for key, _ in MODELS] if carried else ['exact'])
        if carried:
            record['convergence_theorem'] = sources.declaration(folder + 'Bounds.lean', 'runs_solve_chebyshev')
        if carried:
            record['rounded_theorem'] = sources.declaration(CG + 'HSCG/Carried/FinitePrecision/Standard.lean', 'runs_solve_of_model')
            record['relative_theorems'] = [sources.declaration(CG + 'HSCG/Carried/FinitePrecision/' + file, name)
                for file, name in [('Solve.lean', 'runs_solve'), ('Stability.lean', 'Output.stable')]]
        records.append(record)
        body = variant_page(variant, sources, MODELS, PSEUDOCODE[variant['id']],
                            OPERATIONS[variant['id']], MEMORY[variant['id']])
        definition = re.search(r'(<section id="shared-algorithm">.*?</section>)', body, re.S)[1]
        resources = re.search(r'(<section id="shared-theorems">.*?</section>)', body, re.S)[1]
        resources = resources.replace('<h2>Operations and Storage</h2>', '')
        accuracy = body.split('<h2>Accuracy</h2>', 1)[1].split('<p class="record-link">', 1)[0]
        fragments[variant['id']] = {'cg-definition': definition, 'cg-resources': resources, 'cg-accuracy': accuracy}
        write('algorithms/conjugate-gradient/variants/' + variant['id'], variant['title'], body)
    write('algorithms/conjugate-gradient/variants/hscg', 'Ordinary conjugate gradient (CG)',
          '<script>location.replace("../carried/" + location.search + location.hash)</script>'
          '<p><a href="../carried/">Open ordinary CG</a></p>')
    write('arithmetic-models', 'Arithmetic models', models_page(sources))
    write('algorithms/conjugate-gradient', 'Conjugate gradient (CG)',
          concept_page(records, site / 'api/v1'))

    # Add a direct algorithms path while keeping the complete existing topic browser.
    homepage = site / 'index.html'
    page = homepage.read_text()
    entry = '<div class="cg-entry"><p><a href="/explore/algorithms/">Browse algorithms →</a> <span class="muted">Concepts, variants and implementations</span></p><p><a href="' + BASE + '">Try the CG pilot →</a> <span class="muted">Switch computation models on a variant page</span></p></div><h2>Browse the whole library</h2>'
    if 'class="cg-entry"' not in page:
        page = page.replace('<ul class="entry-list category-list">', entry + '<ul class="entry-list category-list">', 1)
    homepage.write_text(page)
    commit = published_revision or subprocess.run(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                                                 capture_output=True, text=True).stdout.strip() or None
    snapshot = published_revision and all(sources.source_revisions[p] == published_revision
                                         for p in sources.files)
    payload = dict(schema_version=1, source=dict(commit=commit, kind='published-snapshot' if snapshot else 'working-tree-preview',
                   files={p: {'sha256': r['sha256']} for p, r in sources.files.items()}),
                   models=[dict(id=k, title=v) for k, v in MODELS], variants=records)
    (site / 'api/v1/cg-pilot.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    (site / 'api/v1/cg-pilot-fragments.json').write_text(json.dumps(fragments, ensure_ascii=False) + '\n')
    for asset in ['cg-pilot.js', 'cg-pilot.css', 'explore.js']:
        (site / asset).write_text((Path(__file__).parent / 'web' / asset).read_text())
    print(f'CG pilot: {len(records)} variants, {len(sources.files)} fingerprinted source files → {site}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True, type=Path)
    parser.add_argument('--src', required=True, type=Path)
    args = parser.parse_args()
    build(args.site, args.src)
