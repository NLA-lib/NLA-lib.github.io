"""Human-facing CG pages: shared cards, mathematical notation, and model descriptions."""
import html
import json
from pathlib import Path
import re

from explore_pages import inline_title, prose_html

BASE = '/explore/algorithms/conjugate-gradient/'
CG = 'NLAlib/Krylov/CG/'
MODELS_URL = '/explore/arithmetic-models/'


def mathematics(text, vectors='AbxvPQHM'):
    """Bold presentation symbols without modifying Lean or existing math fonts."""
    parts = re.split(r'(\$\$[\s\S]*?\$\$|\$[^$\n]+\$)', text)
    token = r'\\(?:mathbf|boldsymbol|mathsf|mathrm|mathbb|mathcal|text|operatorname)\*?\{[^{}]*\}|\\[A-Za-z]+|[A-Za-z]'
    for index in range(1, len(parts), 2):
        parts[index] = re.sub(r'\\mathbf\s+([A-Za-z])', r'\\mathbf{\1}', parts[index])
        parts[index] = re.sub(token, lambda m: r'\mathbf{' + m[0] + '}' if m[0] in vectors else m[0], parts[index])
        parts[index] = re.sub(r'\\(widehat|hat|tilde|widetilde)\s*(\\mathbf\{[A-Za-z]\})', r'\\\1{\2}', parts[index])
    return ''.join(parts)


def prose(text, vectors='AbxvPQHM'):
    return prose_html(mathematics(text, vectors))


def card(title, body, kind='result', identifier=None):
    identity = ' id="' + html.escape(identifier, quote=True) + '"' if identifier else ''
    if kind in {'result', 'cost', 'model', 'algorithm'}:
        label = 'Theorem' if kind in {'result', 'cost'} else 'Definition'
        identity += ' aria-label="' + html.escape(label + ' (' + title + ')', quote=True) + '"'
        prefix = '<span class="explorer-statement-label"><strong>' + label + '</strong> (' + inline_title(mathematics(title)) + ')<strong>.</strong></span> '
        body = '<p>' + prefix + body[3:] if body.startswith('<p>') else '<p>' + prefix + '</p>' + body
        heading = ''
    else:
        heading = '<h3 class="explorer-card-title">' + inline_title(mathematics(title)) + '</h3>'
    return '<article class="explorer-card cg-' + kind + '"' + identity + '>' + heading + body + '</article>'


def disclosure(body, label='Lean statement and details'):
    return '<details class="explorer-disclosure cg-evidence"><summary>' + html.escape(label) + '</summary><div class="explorer-disclosure-body">' + body + '</div></details>'


def result(title, statement, declarations, sources, details=''):
    return card(title, prose(statement) + disclosure(details + ''.join(sources.code(d) for d in declarations)))


def pseudocode_html(phases):
    def steps_html(steps):
        items = []
        for step in steps:
            if isinstance(step, dict):
                items.append('<li>' + prose(step['loop'], 'AbrpqxzPwu') + steps_html(step['steps']) + '</li>')
            else:
                items.append('<li>' + prose(step, 'AbrpqxzPwu') + '</li>')
        return '<ol>' + ''.join(items) + '</ol>'
    return '<div class="cg-pseudocode">' + ''.join(
        '<div class="cg-pseudocode-phase">' + prose(title, 'AbrpqxzPwu') + '</div>' + steps_html(steps)
        for title, steps in phases) + '</div>'


def variant_page(v, sources, models, pseudocode, operations, memory):
    folder = CG + v['folder'] + '/'
    get = lambda file, name, kind='theorem': sources.declaration(folder + file, name, kind)
    rounded_folder = CG + 'HSCG/Carried/FinitePrecision/'
    rounded_get = lambda file, name, kind='theorem': sources.declaration(rounded_folder + file, name, kind)
    carried = v['id'] == 'carried'
    body = '<p class="eyebrow"><a href="/explore/">Explorer</a> / <a data-model-link href="' + BASE + '">Conjugate gradient</a></p>'
    body += prose(v['description'])

    instructions = prose(r'Given a real matrix $A$ and a right-hand side $b$. ' + (
        r'The zero-start form below assumes the iterate buffer already contains $x=0$. The exact solver also has an initializer for a general starting guess.' if carried else
        r'The iterate buffer initially contains the starting guess $x_0$.'))
    instructions += pseudocode_html(pseudocode)
    code = '<h4>Round</h4>' + sources.code(get(v['code'], v['step'], 'def'))
    code += '<h4>Solver initialized from an initial guess</h4>' + sources.code(get(v['solver'], 'solve', 'def'))
    code += '<h4>Exact recurrence connection</h4>' + sources.code(get('Solve.lean', 'runs_solve'))
    if carried:
        code += '<h4>Solver initialized at zero</h4>' + sources.code(rounded_get('Alg.lean', 'solve', 'def'))
    body += '<section id="shared-algorithm">' + card(v['short'], instructions + disclosure(code, 'Lean implementation'), 'algorithm') + '</section>'

    budget = get(v['solver'], 'staticCost_solve')
    peak = get(v['solver'], 'staticPeak_solve_le')
    cost_details = '<p>Counts are at the vector-operation level. Scalar literals, copies, stopping queries and their precise accounting are retained below.</p>'
    cost_details += sources.code(get(v['solver'], 'solveCount', 'def')) + sources.code(budget)
    memory_details = '<p>The readable total uses compact buffers and includes the right-hand side and caller-owned working vectors. The Lean statement bounds additional scratch. The supplied function W accounts for each operation’s workspace.</p>'
    memory_details += sources.code(get(v['solver'], 'solvePeak', 'def')) + sources.code(peak)
    if carried:
        cost_details += '<h4>Zero-start solver</h4>' + sources.code(rounded_get('Alg.lean', 'staticCost_solve'))
        memory_details += '<h4>Zero-start solver</h4>' + sources.code(rounded_get('Alg.lean', 'staticPeak_solve_le'))
    body += '<section id="shared-theorems"><h2>Operations and Storage</h2>'
    body += card('Operation count', prose(r'Let $n$ be the dimension and $k$ the number of iterations, or the cap for a solver that stops early. ' + operations) + disclosure(cost_details), 'cost')
    body += card('Storage bound', prose(memory + r' Here $W_{\max}$ is the largest temporary workspace of a called operation. Matrix and preconditioner storage are additional. These are scalar payload cells, not bytes.') + disclosure(memory_details), 'cost') + '</section>'

    body += '<h2>Accuracy</h2><section class="cg-model-picker"><label for="computation-model">Model of arithmetic</label><select id="computation-model">' + ''.join('<option value="' + key + '">' + html.escape(label) + '</option>' for key, label in models) + '</select><p class="explorer-card-note"><a href="' + MODELS_URL + '">Definitions and assumptions of the arithmetic models</a></p><p id="model-status" class="visually-hidden" role="status"></p></section>'
    body += '<noscript><p>All model sections are displayed below without JavaScript.</p></noscript>'

    for key, label in models:
        body += '<section data-cg-model="' + key + '" aria-label="' + html.escape(label, quote=True) + '">'
        if key != 'exact' and not carried:
            body += card('Implementation coverage', '<p>This pilot has no rounded execution theorem for this variant. Ordinary CG has one for this model.</p><p><a data-model-link href="' + BASE + 'variants/carried/">Open ordinary CG</a></p>', 'note') + '</section>'
            continue
        if key == 'exact':
            assumptions = r'Assume exact scalar operations, dot products, vector updates, and matrix–vector products, correct comparisons, admissible distinct buffers, and enough working memory. '
            if v['id'] == 'pcg':
                statement = r'Let $\mathbf A$ and the applied inverse preconditioner $\mathbf P$ be symmetric positive definite, and let $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$. ' + assumptions
                statement += r'If $k\le g$, where $g=\dim\mathcal K(\mathbf P\mathbf A,\mathbf P\mathbf r_0)$, and the preconditioner is applied exactly, the program executes successfully and its decoded stored output is the mathematical PCG iterate: $$\widehat{\mathbf x}=\operatorname{PCG}(\mathbf A,\mathbf P,\mathbf b,\mathbf x_0,k).$$'
            else:
                statement = r'Let $\mathbf A$ be symmetric positive definite, let $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$, and choose any iteration cap $k$. ' + assumptions
                statement += r'The program executes successfully and its decoded stored output is the mathematical CG iterate: $$\widehat{\mathbf x}=\operatorname{CG}(\mathbf A,\mathbf b,\mathbf x_0,q),\qquad q=\min\{k,g\},\qquad g=\dim\mathcal K(\mathbf A,\mathbf r_0).$$ The program stops at the cap or earlier when the residual becomes zero.'
            body += result('Exact output', statement, [get('Solve.lean', 'runs_solve')], sources)
        else:
            body += rounded_results(key, sources, rounded_get)
        body += '</section>'
    body += '<p class="record-link"><a data-model-link href="' + BASE + '">CG overview and mathematical results</a> · <a href="/explore/api/v1/cg-pilot.json">Source snapshot</a></p>'
    return body


def rounded_results(key, sources, get):
    if key == 'relative':
        description = r'Assume scalar operations have relative error at most $u$. Supply bounds $d_n$ for dot products, $e_a$ for scaled vector additions, and $e_m$ for matrix–vector products. These bounds describe the operations directly; they do not prescribe a reduction order.'
        bounds = r'Choose a nonnegative common allowance $E$ with $$\max\{u,d_n,e_a,e_m\}\le E\le 10^{-2}.$$'
        evidence = [get('Solve.lean', 'runs_solve'), get('Stability.lean', 'Output.stable')]
    else:
        description = (r'Scalar operations have unit roundoff $u$, and dot products accumulate sequentially. Their error coefficient is $$d_n=(1+u)^n-1.$$' if key == 'sequential' else r'Scalar operations have unit roundoff $u$, and dot products use pairwise reductions. Their error coefficient is $$d_n=(1+u)^{\lceil\log_2n\rceil+1}-1.$$ The reduction depth must satisfy $\lceil\log_2n\rceil<\mathrm{depth}$.')
        bounds = r'Choose $0\le E\le10^{-2}$ large enough for the scalar, dot-product, vector-update and matvec error budgets. The named standard profile uses the common accuracy conditions documented on the arithmetic-models page.'
        evidence = [get('Standard.lean', 'runs_solve_of_model')]
    model = prose(description + ' ' + bounds)
    model += '<p><a href="' + MODELS_URL + '#relative">What these error bounds mean</a></p>'
    body = card('Arithmetic assumptions', model, 'model')
    conditions = r'Let $A$ be symmetric positive definite, with eigenvalues in $[a,a^{\prime}]$, $a>0$, and put $\kappa=a^{\prime}/a$. Start at $x_0=0$ and use cap $k$. If the operations satisfy the selected error budgets and $$3Ea^{\prime}\le a,\qquad k^2\sqrt k\,E\kappa^2\le10^{-5},$$ the solver executes successfully. It performs at most $k$ rounds, stopping early if the computed residual becomes zero.'
    body += result('Successful execution', conditions, evidence, sources,
        '<p>The exact contracts, admissible lengths, scalar sign tests, distinct live buffers and memory requirements are stated below. In the abstract relative model, the two displayed statements compose execution with stability of its actual output.</p>')
    convergence = r'Under these assumptions, let $Ax_\star=b$. At every completed step $j\le m$, the computed iterates satisfy $$\|x_\star-x_j\|_A^2\le4\theta^{2j}\|x_\star\|_A^2+\frac{2\|b\|_2^2\delta}{a^2}+135j^2E\kappa\frac{\|b\|_2^2}{a},$$ where $$\theta=\frac{\sqrt{2\kappa+1}-1}{\sqrt{2\kappa+1}+1},\qquad\delta=6000m^2\sqrt m\,E\kappa a^{\prime}.$$ The first term decreases geometrically; the other terms quantify the effect of rounding. Here $\|v\|_A^2=v^{\mathsf T}Av$.'
    body += result('Convergence with rounding', convergence, [sources.declaration('NLAlib/Krylov/FinitePrecision/CGEnergy.lean', 'quadForm_sub_x_le_four_mul_pow_add')], sources,
        '<p>The execution theorem identifies the solver’s stored output with the run in this bound.</p>' + sources.code(get('Stability.lean', 'StableOutput', 'def')))
    return body


def concept_page(records, api):
    body = prose(r'CG solves a symmetric positive-definite system $Ax=b$ by choosing successive iterates from a Krylov space. The variants below change the recurrence or how its state is retained; an arithmetic model then specifies how its operations are computed.')
    body += '<h2>Variants</h2><div class="cg-variant-list">'
    for v in records:
        title = '<a data-model-link href="' + BASE + 'variants/' + v['id'] + '/">' + html.escape(v['short']) + '</a>'
        coverage = 'Exact, relative-error BLAS + matvec, standard sequential, and standard pairwise arithmetic.' if len(v['models']) > 1 else 'Exact-arithmetic implementation results.'
        body += '<article class="explorer-card cg-variant"><h3 class="explorer-card-title">' + title + '</h3>' + prose(v['description']) + '<p class="explorer-card-note">' + coverage + '</p></article>'
    body += '</div><h2>Related methods</h2><p><a href="/explore/algorithms/lanczos/">Lanczos</a> · <a href="/explore/search/?q=MINRES">MINRES</a> · <a href="/explore/search/?q=conjugate%20gradient%20least%20squares">CGLS</a></p><h2 id="analysis">Mathematical CG in exact arithmetic</h2>'
    body += prose(r'Let $A$ be symmetric positive definite, let $Ax_\star=b$, and let $x_k$ denote the mathematical CG iterate from $x_0$. Write $r_0=b-Ax_0$ and $\|v\|_A^2=v^{\mathsf T}Av$. The variant pages connect these mathematical facts to actual solver outputs.', 'Abrxv')
    core = {
        'cg-optimality': ('Energy optimality', r'The CG iterate minimizes the energy error over the initial guess plus the available Krylov space: $$x_k\in\operatorname*{arg\,min}_{y\in x_0+\mathcal K_k(A,r_0)}\|x_\star-y\|_A^2,$$ where $\mathcal K_k(A,r_0)=\operatorname{span}\{r_0,Ar_0,\ldots,A^{k-1}r_0\}$. The iterates therefore improve as the search space grows.'),
        'cg-chebyshev-bound': ('Chebyshev convergence', r'If the eigenvalues of $A$ lie in $[a,a^{\prime}]$ with $a>0$, then $$\|x_\star-x_k\|_A^2\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2k}\|x_\star-x_0\|_A^2,\qquad\kappa=\frac{a^{\prime}}{a}.$$ The interval ratio controls the rate of convergence.'),
        'cg-polynomial-bound': ('Polynomial error bound', r'For every polynomial $p$ of degree at most $k$ with $p(0)=1$, $$\|x_\star-x_k\|_A^2\le\|p(A)(x_\star-x_0)\|_A^2.$$ A polynomial that is small on the spectrum gives a small CG error.'),
        'cg-finite-termination': ('Finite termination', r'Let $g=\dim\operatorname{span}\{r_0,Ar_0,A^2r_0,\ldots\}$. Once $k\ge g$, $$x_k=x_\star.$$ Since $g\le n$ for an $n$-dimensional system, at most $n$ exact-arithmetic steps suffice.'),
    }
    algorithm = json.loads((api / 'algorithms/cg.json').read_text())['record']
    further = ''
    for rid in list(core) + [rid for rid in algorithm['results'] if rid not in core]:
        r = json.loads((api / 'results' / (rid + '.json')).read_text())['record']
        d = json.loads((api / 'declarations' / (r['primary'] + '.json')).read_text())['record']
        summary = d['summary'] or d['docstring'].split('\n\n')[0]
        source = d['source']['url'] or 'https://github.com/NLA-lib/nlalib'
        details = '<pre><code>' + html.escape(d['signature']) + '</code></pre><p><a href="' + html.escape(source, quote=True) + '">Full source on GitHub</a></p>'
        if rid in core:
            title, summary = core[rid]
            body += card(title, prose(summary, 'Abrxvy') + disclosure(details))
        else:
            further += card(r['title'], prose(summary) + disclosure(details))
    return body + disclosure(further, 'Further analysis and implementation results')


def models_page(sources):
    get = lambda file, name, kind='def': sources.declaration('NLAlib/Ops/' + file, name, kind)
    body = '<p class="eyebrow"><a href="/explore/">Explorer</a> / Arithmetic models</p>'
    body += prose(r'The algorithm specifies the sequence of operations. An arithmetic model states what each computed operation may return. A convergence theorem combines those local error bounds with assumptions on $A$, the iteration cap and available memory. The following models are currently used by ordinary CG in this pilot.')
    body += card('Exact arithmetic', prose(r'Scalar arithmetic, dot products, vector updates and matrix–vector products are exact. The CG iterate therefore agrees with its mathematical recurrence, and finite-termination and classical Chebyshev bounds apply.') + disclosure(sources.code(get('Profiles/Standard.lean', 'Scheme.roundoff'))), 'model', 'exact')
    relative = r'BLAS operations and matvecs are abstract operations with supplied error coefficients. For dot products, $$|\widehat{\langle\mathbf{x},\mathbf{y}\rangle}-\langle\mathbf{x},\mathbf{y}\rangle|\le d_n\sum_{i=1}^n|x_i y_i|.$$ The bound scales with the sum of absolute products; cancellation can make it much larger than a relative error in the dot-product value itself. A scaled vector addition obeys $$|\widehat z_i-(y_i+\alpha x_i)|\le e_a(|y_i|+|\alpha x_i|).$$ Matrix–vector multiplication has the normwise bound $$\|\widehat{A v}-A v\|_2\le e_m\|A\|_2\|v\|_2.$$ Scalar arithmetic has unit roundoff $u$; copies and decoded comparisons are exact. This model supplies $d_n,e_a,e_m$ without choosing sequential or pairwise implementations.'
    body += card('Relative-error BLAS + matvec', prose(relative, 'Abv') + disclosure(sources.code(get('Catalog/Blas1.lean', 'IsDotErr')) + sources.code(get('Catalog/Blas1.lean', 'IsAxpyErr'))), 'model', 'relative')
    body += card('Standard rounding with sequential BLAS', prose(r'Scalar operations use the standard relative-rounding model with unit roundoff $u$ and unbounded exponents. Dot products form rounded products and accumulate them sequentially, giving $$d_n=(1+u)^n-1.$$ The BLAS implementation supplies the vector-update bounds. All vector lengths are admitted. Matvec error is supplied separately; choosing this model does not assume exact matvecs.') + disclosure(sources.code(get('Profiles/Standard.lean', 'Scheme.errors'))), 'model', 'sequential')
    body += card('Standard rounding with pairwise BLAS', prose(r'Scalar arithmetic is the same, but reductions use a pairwise summation tree: $$d_n=(1+u)^{\lceil\log_2n\rceil+1}-1.$$ The implementation requires $\lceil\log_2n\rceil<\mathrm{depth}$. This improves the error coefficient’s dependence on vector length. Pairwise summation describes the reduction order; it does not by itself certify parallel runtime. Matvec error is supplied separately.') + disclosure(sources.code(get('Profiles/Standard.lean', 'Scheme.admits'))), 'model', 'pairwise')
    envelope = r'The named standard profiles use a common allowance $E$ satisfying $$0\le E\le10^{-2},\quad e_m,e_a\le E,\quad u,d_n,e_{\mathrm{scal}}\le E/16.$$ Here $e_{\mathrm{scal}}$ bounds componentwise vector division. The abstract relative-error CG theorem needs only $u,d_n,e_a,e_m\le E$; the stricter standard envelope is shared with other solvers. CG additionally requires the spectral and iteration-window conditions shown with its convergence theorem.'
    body += card('How operation errors enter the CG theorem', prose(envelope) + disclosure(sources.code(get('Profiles/Standard.lean', 'Accuracy', 'structure'))), 'model', 'accuracy')
    body += '<p><a href="' + BASE + 'variants/carried/">Return to ordinary CG</a></p>'
    return body
