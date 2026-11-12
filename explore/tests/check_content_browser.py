"""Browser QA for the Markdown explorer. Requires a running preview and Playwright."""
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8081')
parser.add_argument('--chromium', required=True)
parser.add_argument('--screenshots', type=Path, default=Path('/tmp/explorer-content-screenshots'))
args = parser.parse_args()
base = args.url.rstrip('/') + '/explore/'
args.screenshots.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chromium, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    assert page.goto(base).status == 200
    assert page.get_by_role('navigation', name='Explorer').get_by_role('link').count() == 3
    assert page.locator('main > .explorer-card').count() == 3
    page.screenshot(path=str(args.screenshots / 'home.png'), full_page=True)
    # The padding at the far edge of a navigation card follows its title link.
    card = page.locator('main .explorer-link-card').first
    bounds = card.bounding_box()
    page.mouse.click(bounds['x'] + bounds['width'] - 10, bounds['y'] + bounds['height'] - 10)
    expect(page).to_have_url(base + 'algorithms/')
    page.goto(base + 'tasks/linear-systems/')
    page.get_by_role('link', name='Galerkin methods', exact=True).click()
    assert page.locator('main .explorer-link-card').count() == 4
    assert page.get_by_role('link', name='Preconditioned CG (PCG)', exact=True).is_visible()
    assert page.get_by_role('link', name='Block CG', exact=True).is_visible()
    assert page.get_by_role('link', name='Full orthogonalization method (FOM)', exact=True).is_visible()
    page.get_by_role('link', name='Conjugate gradient (CG)', exact=True).click()
    assert page.locator('main .explorer-link-card[href*="/implementations/"]').count() == 2
    assert page.get_by_role('link', name='Standard PCG recurrence', exact=True).count() == 0
    ordinary = page.get_by_role('link', name='Ordinary CG', exact=True)
    bounds = ordinary.bounding_box()
    page.mouse.click(bounds['x'] + bounds['width'] - 10, bounds['y'] + bounds['height'] - 10)
    expect(page).to_have_url(base + 'algorithms/conjugate-gradient/implementations/ordinary/?model=exact')
    page.goto(base + 'families/residual-minimization-methods/')
    assert page.get_by_role('link', name='GMRES', exact=True).is_visible()
    assert page.get_by_role('link', name='MINRES', exact=True).is_visible()
    page.goto(base + 'tasks/matrix-factorizations/')
    page.get_by_role('link', name='Matrix factorizations', exact=True).click()
    assert page.get_by_role('link', name='LU factorization', exact=True).is_visible()
    assert page.get_by_role('link', name='PLU factorization', exact=True).is_visible()
    page.goto(base + 'tasks/low-rank-approximation/')
    page.get_by_role('link', name='RSVD-type methods', exact=True).click()
    assert page.locator('main .explorer-link-card').count() == 4
    page.get_by_role('link', name='Late-truncated RSVD', exact=True).click()
    assert page.get_by_role('article', name='Theorem (Orthogonal error decomposition)', exact=True).is_visible()
    assert page.locator('.katex-error').count() == 0
    for task in ['eigenvalues', 'matrix-functions', 'quadrature', 'trace-estimation']:
        page.goto(base + 'tasks/' + task + '/')
        links = page.get_by_role('link', name='Lanczos process', exact=True)
        assert links.count() == 1
        assert '/algorithms/lanczos/' in links.get_attribute('href')
    page.get_by_role('link', name='Lanczos process', exact=True).click()
    assert page.url.split('?')[0] == base + 'algorithms/lanczos/'
    assert page.get_by_role('heading', name='Lanczos process', exact=True).is_visible()
    assert page.get_by_role('link', name='Lanczos matrix-function approximation', exact=True).count() == 1
    assert page.get_by_role('link', name='Stochastic Lanczos quadrature', exact=True).count() == 1
    page.get_by_role('link', name='Ordinary Lanczos', exact=True).click()
    assert page.url.split('?')[0].endswith('/algorithms/lanczos/implementations/ordinary/')
    assert page.get_by_role('heading', name='Operations and Storage').is_visible()
    assert page.get_by_role('heading', name='Accuracy', exact=True).is_visible()
    assert page.locator('#computation-model').count() == 0
    page.goto(base + 'algorithms/lsqr/')
    assert 'Placeholder' in page.locator('.content-status').inner_text()
    assert page.locator('.cg-result').count() == 0
    for topic in ['matrix-analysis', 'polynomial-approximation']:
        page.goto(base + 'theory/' + topic + '/')
        link = page.get_by_role('link', name='Matrix polynomials and functional calculus', exact=True)
        assert link.count() == 1
        assert link.get_attribute('href') == '/explore/theory/matrix-polynomials/'
        assert page.locator('#computation-model').count() == 0
    page.screenshot(path=str(args.screenshots / 'theory.png'), full_page=True)
    page.goto(base + 'theory/chebyshev-polynomials/')
    assert page.get_by_role('link', name='Conjugate gradient (CG)', exact=True).count() <= 1
    page.goto(base + 'library/')
    assert '7,722 declarations' in page.locator('main').inner_text()
    page.get_by_role('link', name='Named results', exact=True).click()
    page.locator('main .entry-list a').first.click()
    assert '/library/results/' in page.url
    assert page.locator('a[href^="https://github.com/"]').count() > 0
    page.goto(base + 'algorithms/conjugate-gradient/')
    assert page.locator('.cg-result').count() == 4
    assert page.locator('.katex-error').count() == 0
    for section in ['mathematical-background', 'appears-under-these-tasks', 'family']:
        assert page.locator('#section-' + section).get_attribute('open') is None
    sections = page.locator('main > details.explorer-section')
    assert 'Implementations' in sections.first.locator('summary').first.inner_text()
    theorem = page.locator('.cg-result').first
    permalink = theorem.locator('.statement-permalink').get_attribute('href')
    assert permalink.startswith('#theorem-')
    page.context.grant_permissions(['clipboard-read', 'clipboard-write'], origin=args.url)
    theorem.locator('.cg-evidence > summary').click()
    theorem.locator('[data-copy-link]').click()
    expect(theorem.locator('.copy-link-status')).to_have_text('Link copied')
    assert page.evaluate('navigator.clipboard.readText()').endswith(permalink)
    guarantees = page.locator('#section-mathematical-cg-in-exact-arithmetic')
    guarantees.locator('summary').first.click()
    assert not theorem.is_visible()
    page.evaluate('(hash) => location.hash = hash', permalink)
    expect(theorem).to_be_visible()
    page.get_by_role('link', name='Ordinary CG', exact=True).click()
    assert page.url.split('?')[0].endswith('/implementations/ordinary/')
    assert page.locator('.cg-pseudocode').is_visible()
    page.select_option('#computation-model', 'relative')
    assert page.locator('[data-cg-model="relative"]').is_visible()
    assert page.locator('.katex-error').count() == 0
    model_link = page.locator('[data-cg-model="relative"] .cg-result .statement-permalink').first.get_attribute('href')
    assert model_link.startswith('?model=relative#relative-')
    page.goto(base + 'algorithms/conjugate-gradient/implementations/ordinary/' + model_link)
    assert page.locator('#computation-model').input_value() == 'relative'
    expect(page.locator(model_link[model_link.index('#'):])).to_be_visible()
    page.screenshot(path=str(args.screenshots / 'cg.png'), full_page=True)
    page.goto(base + 'search/?q=Lanczos&kind=algorithm')
    expect(page.locator('#search-results li').first).to_be_visible(timeout=20000)
    assert '/algorithms/lanczos/' in page.locator('#search-results').inner_html()
    page.goto(base)
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.goto(base + 'algorithms/conjugate-gradient/implementations/ordinary/?model=pairwise')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.locator('.katex-error').count() == 0
    page.screenshot(path=str(args.screenshots / 'mobile.png'), full_page=True)
    static = browser.new_context(java_script_enabled=False).new_page()
    static.goto(base + 'tasks/eigenvalues/')
    assert static.get_by_role('link', name='Lanczos process', exact=True).is_visible()
    assert not errors, errors
    browser.close()
print('PASS: Markdown navigation, canonical multi-task Lanczos, theory cross-listing, placeholders, Library, CG models, search, mobile, no-JS')
