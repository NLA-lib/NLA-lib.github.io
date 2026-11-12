from pathlib import Path
import argparse
from playwright.sync_api import sync_playwright, expect

parser = argparse.ArgumentParser(description='Browser QA for a running CG pilot preview.')
parser.add_argument('--url', default='http://127.0.0.1:8081')
parser.add_argument('--chromium', required=True)
parser.add_argument('--screenshots', type=Path, default=Path('/tmp/cg-pilot-screenshots'))
args = parser.parse_args()
root = args.url.rstrip('/')
base = root + '/explore/algorithms/conjugate-gradient/'
shots = args.screenshots
shots.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1300, 'height': 1000})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    assert page.goto(base).status == 200
    variants = page.locator('main .explorer-link-card[href*="/implementations/"]')
    assert variants.count() == 2
    assert variants.locator('ul, li').count() == 0
    assert page.locator('.katex-error').count() == 0
    page.screenshot(path=str(shots / 'overview.png'), full_page=True)
    page.get_by_role('link', name='Ordinary CG', exact=True).click()
    page.evaluate('document.fonts.ready')
    assert page.locator('.katex-html').count() > 0
    paragraph = page.locator('.cg-cost > p').first
    assert 'Source Sans 3' in paragraph.evaluate('(node) => getComputedStyle(node).fontFamily')
    assert paragraph.evaluate('(node) => getComputedStyle(node).fontStyle') == 'normal'
    assert paragraph.locator('.explorer-statement-label').evaluate('(node) => getComputedStyle(node).fontStyle') == 'italic'
    assert paragraph.evaluate('(node) => parseFloat(getComputedStyle(node).lineHeight) / parseFloat(getComputedStyle(node).fontSize)') == 1.5
    assert page.locator('[data-cg-model]:visible').count() == 1
    assert page.locator('[data-cg-model="exact"]').is_visible()
    assert page.get_by_role('article', name='Theorem (Exact output)', exact=True).is_visible()
    assert page.locator('[data-cg-model="exact"] .cg-result').count() == 1
    assert page.get_by_role('heading', name='Operations and Storage', exact=True).is_visible()
    assert page.get_by_role('heading', name='Accuracy', exact=True).is_visible()
    assert page.locator('.cg-model-picker.explorer-card').count() == 0
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderRadius') == '0px'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderLeftColor') == 'rgb(17, 17, 17)'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderLeftWidth') == '4px'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderTopWidth') == '0px'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderRightWidth') == '0px'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).borderBottomWidth') == '0px'
    assert page.locator('.explorer-statement-label').first.locator('strong').all_text_contents() == ['Definition', '.']
    assert page.locator('.explorer-statement-label').first.evaluate('(node) => node.parentElement.tagName') == 'P'
    assert page.locator('.explorer-card').first.evaluate('(node) => getComputedStyle(node).backgroundColor') == 'rgb(244, 244, 244)'
    assert page.locator('main table').count() == 0
    assert page.locator('.cg-variants, .cg-facts').count() == 0
    assert page.locator('[data-cg-model] > h2').count() == 0
    assert page.locator('.cg-pseudocode').is_visible()
    assert page.locator('.cg-pseudocode .katex').count() > 0
    assert page.locator('#shared-theorems .katex-display').count() > 0
    assert page.locator('.katex-error').count() == 0
    assert page.locator('.cg-evidence[open]').count() == 0
    assert page.evaluate('document.querySelector("#shared-theorems").compareDocumentPosition(document.querySelector(".cg-model-picker")) & Node.DOCUMENT_POSITION_FOLLOWING')
    shared = page.locator('#shared-algorithm, #shared-theorems').all_inner_texts()
    assert page.locator('.cg-evidence a[href^="/explore/"]').count() == 0
    assert page.locator('.cg-evidence a[href^="https://github.com/"]').count() > 0
    page.locator('#shared-theorems .cg-evidence summary').first.click()
    assert page.locator('#shared-theorems .cg-evidence pre').first.is_visible()
    page.locator('#shared-theorems .cg-evidence summary').first.click()
    page.select_option('#computation-model', 'sequential')
    assert '?model=sequential' in page.url
    assert page.locator('[data-cg-model="sequential"]').is_visible()
    assert page.locator('[data-cg-model="sequential"] .cg-result').count() == 2
    assert page.locator('#shared-algorithm, #shared-theorems').all_inner_texts() == shared
    page.select_option('#computation-model', 'pairwise')
    assert page.locator('[data-cg-model="pairwise"]').is_visible()
    assert 'depth' in page.locator('[data-cg-model="pairwise"] .cg-model').inner_text()
    page.reload()
    assert page.locator('#computation-model').input_value() == 'pairwise'
    page.go_back()
    expect(page.locator('#computation-model')).to_have_value('sequential')
    page.select_option('#computation-model', 'relative')
    assert page.locator('[data-cg-model="relative"]').is_visible()
    assert 'IsBlas1' in page.locator('[data-cg-model="relative"]').text_content()
    assert 'IsMatvec' in page.locator('[data-cg-model="relative"]').text_content()
    assert page.locator('.katex-error').count() == 0
    page.select_option('#computation-model', 'pairwise')
    page.screenshot(path=str(shots / 'carried-pairwise.png'), full_page=True)
    # The concept page retains the model choice for the next variant.
    page.get_by_role('link', name='Conjugate gradient (CG)', exact=True).click()
    page.locator('#section-family > summary').click()
    page.get_by_role('link', name='Galerkin methods', exact=True).click()
    page.get_by_role('link', name='Preconditioned CG (PCG)', exact=True).click()
    page.get_by_role('link', name='Standard PCG recurrence', exact=True).click()
    assert page.locator('#computation-model').input_value() == 'pairwise'
    assert 'no rounded execution theorem' in page.locator('[data-cg-model="pairwise"]').inner_text()
    page.select_option('#computation-model', 'exact')
    assert 'preconditioner' in page.locator('[data-cg-model="exact"]').inner_text()
    # Every local link in pilot pages resolves, including line-linked source viewers.
    for variant, url in [('ordinary', base + 'implementations/ordinary/'),
                         ('preconditioned', root + '/explore/algorithms/preconditioned-conjugate-gradient/implementations/standard/'),
                         ('full-reorthogonalization', base + 'implementations/full-reorthogonalization/')]:
        page.goto(url)
        assert page.locator('.cg-variants, .cg-facts').count() == 0
        assert page.locator('.katex-error').count() == 0
        exact = page.locator('[data-cg-model="exact"]')
        assert exact.locator('.cg-result').count() == 1
        assert exact.get_by_role('article', name='Theorem (Exact output)', exact=True).is_visible()
        assert 'theorem runs_solve' in exact.locator('pre').text_content()
        assert 'Chebyshev convergence' not in exact.inner_text()
        links = page.locator('main a[href^="/explore/"]').evaluate_all('(links) => [...new Set(links.map(a => a.getAttribute("href")))]')
        for link in links:
            response = page.request.get(root + link.split('#')[0])
            assert response.status == 200, (link, response.status)
    page.goto(base + 'implementations/ordinary/?model=pairwise')
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'mobile overflow'
    page.screenshot(path=str(shots / 'mobile.png'), full_page=True)
    page.goto(root + '/explore/arithmetic-models/')
    assert page.locator('#relative, #exact, #sequential, #pairwise, #accuracy').count() == 5
    assert page.locator('.katex-error').count() == 0
    assert page.locator('main .katex').count() > 10
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors, errors
    # Static content remains readable without JavaScript.
    static = browser.new_context(java_script_enabled=False).new_page()
    static.goto(base + 'implementations/ordinary/')
    assert static.locator('[data-cg-model]:visible').count() == 4
    assert static.locator('.cg-pseudocode').is_visible()
    browser.close()
print('PASS: CG family, separate CG/PCG methods, three implementations, square monochrome cards, model switching, history/reload, source links, mobile, no-JS; no page errors')
