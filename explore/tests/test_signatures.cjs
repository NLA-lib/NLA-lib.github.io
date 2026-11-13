const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'web/app.js'), 'utf8');
// Evaluate the actual renderer in isolation, with only its DOM/highlighter boundary stubbed.
const renderer = source.slice(source.indexOf('  function leanBlock(i) {'),
                              source.indexOf('  // One formal statement', source.indexOf('  function leanBlock(i) {')));
const fixtures = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/scoped-statements.json'), 'utf8'));
function render(d) {
  const context = { decls: [d], h: () => ({ innerHTML: '' }), leanHtml: text => text };
  vm.createContext(context);
  return vm.runInContext(renderer + '\nleanBlock(0)', context);
}
for (const d of fixtures) {
  test(`source context survives elaborated toggle: ${d.name}`, () => {
    const box = render({ st: d.statement, sig: d.signature });
    assert.ok(box.innerHTML.includes(d.statement));
    box.toggle();
    assert.ok(box.innerHTML.includes(d.signature));
    assert.ok(box.innerHTML.includes(d.statement));
    assert.ok(box.innerHTML.includes('implicit arguments may be omitted'));
    box.toggle();
    assert.ok(box.innerHTML.includes(d.statement));
  });
}
test('signature-only fallback warns on both views', () => {
  for (const st of [undefined, null, '']) {
    const box = render({ st, sig: 'predicate : StronglyMeasurable X' });
    for (let view = 0; view < 2; view++) {
      assert.ok(box.innerHTML.includes('Source statement unavailable'));
      assert.ok(box.innerHTML.includes('implicit arguments may be omitted'));
      assert.ok(box.innerHTML.includes('predicate : StronglyMeasurable X'));
      box.toggle();
    }
  }
});

const prototype = fs.readFileSync(path.join(root, 'search/index.html'), 'utf8');
const prototypeRenderer = prototype.slice(prototype.indexOf('function appendFormalStatement('),
                                           prototype.indexOf('async function search()'));
function renderPrototype(hit) {
  const parts = [];
  const context = { node: (tag, text) => ({ tag, text }), hit,
                    article: { append: (...nodes) => parts.push(...nodes) } };
  vm.createContext(context);
  vm.runInContext(prototypeRenderer + '\nappendFormalStatement(article, hit)', context);
  return parts.map(n => n.text).join('\n');
}
test('prototype search retains all seven source statements and labels signature fallback', () => {
  for (const d of fixtures) {
    const text = renderPrototype(d);
    assert.ok(text.includes(d.statement));
    assert.ok(text.includes(d.signature));
    assert.ok(text.includes('implicit arguments may be omitted'));
  }
  const fallback = renderPrototype({ signature: 'StronglyMeasurable X' });
  assert.ok(fallback.includes('Source statement unavailable'));
  assert.ok(fallback.includes('may omit implicit arguments'));
});
