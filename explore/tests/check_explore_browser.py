"""Optional browser QA for a built release; requires Playwright and a Chromium executable.

Run: python tests/check_explore_browser.py --site site --chromium /path/to/chrome-headless-shell
"""
import argparse
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import threading
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from preview import ExploreHandler


class Handler(ExploreHandler):
    def log_message(self, *args):
        pass


def check(site, chromium, screenshots):
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(site.parent)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}/explore/'
    errors = []
    checks = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chromium, args=['--no-sandbox'])
            context = browser.new_context()
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: errors.append(f'HTTP {response.status}: {response.url}')
                    if response.status >= 400 else None)
            examples = ['', 'algorithms/conjugate-gradient/', 'algorithms/randomized-svd/',
                        'low-rank-approximation/?algorithm=RSVD', 'theory/matrix-perturbation/',
                        'results/greenbaum-backward-model/', 'results/cg-galerkin-formula/',
                        'declarations/NLAlib.CGImplementation.exec_rounded_compiled/']
            for width in [1280, 390]:
                page.set_viewport_size({'width': width, 'height': 900})
                for path in examples:
                    response = page.goto(base + path, wait_until='networkidle')
                    assert response.status == 200, path
                    assert page.locator('h1').count() == 1, path
                    assert page.locator('header > h1').count() == 1, path
                    assert page.locator('header nav a').all_text_contents() == ['Home', 'Explorer', 'Design', 'GitHub'], path
                    assert page.locator('h1').bounding_box()['y'] < page.locator('header nav').bounding_box()['y'], path
                    overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                    if overflow:
                        print(page.evaluate('''JSON.stringify([...document.querySelectorAll('body *')]
                          .filter(e => e.getBoundingClientRect().right > innerWidth + 1)
                          .slice(0, 12).map(e => ({tag:e.tagName, cls:String(e.className),
                            right:e.getBoundingClientRect().right,
                            parents:[e.parentElement,e.parentElement?.parentElement,e.parentElement?.parentElement?.parentElement]
                              .filter(Boolean).map(p=>({tag:p.tagName,cls:String(p.className),
                                width:p.getBoundingClientRect().width,overflow:getComputedStyle(p).overflow,
                                display:getComputedStyle(p).display,position:getComputedStyle(p).position}))})))'''))
                    assert not overflow, path
                    assert page.locator('.katex-error').count() == 0, path
                    if path.startswith('results/'):
                        assert page.locator('.page-title .katex').count() > 0, path
                    if path.startswith('low-rank-approximation/'):
                        assert page.locator('details[open]').count() == 0
                        page.locator('#bounds').locator('xpath=ancestor::details[1]').locator(':scope > summary').click()
                        page.locator('[data-bound-group]').first.locator(':scope > summary').click()
                        heading = page.locator('.bound-title').first
                        assert heading.evaluate("e => getComputedStyle(e).display") == 'block'
                        assert heading.evaluate("e => getComputedStyle(e, '::before').content") == 'none'
                        # Compare the actual typographic baselines, not the outer box tops.
                        # An inline-block with overflow:auto used to lift equations in prose.
                        shift = page.locator('.bound-guarantee .math').first.evaluate('''math => {
                          const marker = () => {
                            const span = document.createElement('span');
                            span.style.cssText = 'display:inline-block;width:0;height:0;padding:0;margin:0';
                            return span;
                          };
                          const inside = marker(), outside = marker();
                          math.append(inside); math.after(outside);
                          const delta = inside.getBoundingClientRect().y - outside.getBoundingClientRect().y;
                          inside.remove(); outside.remove();
                          return delta;
                        }''')
                        assert abs(shift) < 1, f'Inline equation shifted by {shift}px at {width}px'
                    if screenshots and path in ['', 'algorithms/conjugate-gradient/', 'low-rank-approximation/?algorithm=RSVD']:
                        screenshots.mkdir(parents=True, exist_ok=True)
                        file = ('home' if not path else path.split('/')[0]) + f'-{width}.png'
                        page.screenshot(path=str(screenshots / file), full_page=True)
                    checks.append(f'{width}px {path or "home"}')
                page.goto(base.removesuffix('explore/') + 'design/', wait_until='networkidle')
                assert page.locator('.math .katex').count() > 0
                assert page.locator('.katex-error').count() == 0
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                checks.append(f'{width}px Design mathematics')
            page.goto(base + 'low-rank-approximation/?algorithm=RSVD', wait_until='networkidle')
            assert page.locator('.bound-filters').count() == 0
            assert page.locator('details[open]').count() == 0
            page.locator('#bounds').locator('xpath=ancestor::details[1]').locator(':scope > summary').click()
            group = page.locator('[data-bound-group]').first
            assert group.locator('[data-bound]:visible').count() == 0
            group.locator(':scope > summary').click()
            assert group.locator('[data-bound]:visible').count() > 0
            group.locator(':scope > summary').click()
            assert page.locator('[data-bound]:visible').count() == 0
            checks.append('sections start collapsed and bounds have no filter controls')
            page.goto(base + 'search/?q=pinv_pinv&kind=theorem', wait_until='networkidle')
            assert page.locator('#search-results a').count() > 0
            page.locator('#search-results a').first.click()
            assert '/declarations/' in page.url
            assert 'pinv_pinv' in page.locator('#signature').text_content()
            checks.append('proof building block search and exact signature')
            page.goto(base + 'search/?q=CG+lower+bounds', wait_until='networkidle')
            assert page.locator('#search-results a[href="/explore/results/cg-near-optimality-lower-bound/"]').count() == 1
            page.goto(base, wait_until='networkidle')
            page.locator('#site-query').fill('beta-subgaussian')
            page.locator('#quick-search li a').first.wait_for()
            assert page.locator('#quick-search li a .katex').count() > 0
            page.goto(base + 'search/?q=beta-subgaussian', wait_until='networkidle')
            assert page.locator('#search-results a .katex').count() > 0
            checks.append('mathematical term search and typeset search-result titles')
            index = json.loads((site / 'api/v1/search-index.json').read_text())
            special = next(x for x in index['entries'] if '?' in x['id'] and x['kind'] == 'def')
            page.goto(base.removesuffix('/explore/') + special['url'], wait_until='networkidle')
            assert special['id'] in page.locator('.page-title').text_content()
            checks.append('encoded question mark in a Lean declaration URL')
            page.goto(base + '#a/cg', wait_until='networkidle')
            page.wait_for_url('**/algorithms/conjugate-gradient/')
            checks.append('legacy algorithm link')
            page.goto(base + '#r/cg-program?s=NLAlib.storedEntriesConjugateGradient', wait_until='networkidle')
            page.wait_for_url('**/declarations/NLAlib.storedEntriesConjugateGradient/')
            checks.append('legacy selected statement link')
            data = json.loads((site / 'data.json').read_text())
            old, selected = next(iter(data['aliasFocus'].items()))
            page.goto(base + '#r/' + old, wait_until='networkidle')
            page.wait_for_url('**/declarations/**')
            assert data['decls'][selected]['n'] in page.locator('.page-title').text_content()
            checks.append('merged result alias retains its selected statement')
            page.goto(base + 'catalog/', wait_until='networkidle')
            assert page.locator('#q').is_visible()
            checks.append('catalogue retained')
            no_js = browser.new_context(java_script_enabled=False)
            static = no_js.new_page()
            static.goto(base + 'algorithms/conjugate-gradient/')
            assert static.locator('a[href*="/declarations/NLAlib.CGImplementation.exec_rounded_compiled/"]').count() > 0
            assert static.locator('.implementation-details[open]').count() == 0
            details = static.locator('.implementation-details').filter(has_text='Unbounded relative-error scalar contract')
            assert not details.locator('dl').is_visible()
            details.locator('summary').click()
            assert details.locator('dl').is_visible()
            assert details.locator('a[href="/explore/declarations/NLAlib.Computation.IsRelErrSem/"]').is_visible()
            assert details.locator('a[href="/explore/declarations/NLAlib.Computation.AddsZeroExactly/"]').is_visible()
            static.goto(base + 'declarations/NLAlib.CGImplementation.exec_rounded_compiled/')
            assert 'horizon' in static.locator('#signature').text_content()
            checks.append('implementation evidence and complete API without JavaScript')
            page.goto(base, wait_until='networkidle')
            categories = page.locator('.category-list > li > a')
            assert categories.count() > 0
            assert page.locator('.category-card').count() == 0
            page.locator('.category-list a[href="/explore/linear-systems/"]').click()
            assert page.locator('#algorithms').text_content() == 'Algorithms'
            page.locator('#algorithms').locator('xpath=ancestor::details[1]').locator(':scope > summary').click()
            assert page.locator('#algorithms').locator('xpath=ancestor::details[1]').locator('ul a').count() > 0
            assert not (site / 'reports').exists()
            assert not (site / 'agents').exists()
            checks.append('regular category list leads to algorithms within each category')
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    assert not errors, errors
    print(json.dumps({'checks': checks, 'browser_errors': errors}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('site'))
    parser.add_argument('--chromium', required=True)
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    check(args.site.resolve(), args.chromium, args.screenshots)
