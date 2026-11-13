'use strict';
(async function () {
  const root = document.body.dataset.root || './';
  const api = root + 'api/v1/';
  const read = async name => {
    const version = name === 'search-index.json' ? document.body.dataset.searchVersion : document.body.dataset.snapshot;
    const response = await fetch(api + name + '?v=' + version);
    if (!response.ok) throw new Error('Could not load ' + name);
    const data = await response.json();
    if (data.snapshot && data.snapshot.extraction_sha256 !== document.body.dataset.snapshot)
      throw new Error('Search snapshot differs from this page. Reload to use one release.');
    return data;
  };
  const params = new URLSearchParams(location.search);
  if (location.hash.startsWith('#open/')) {
    try {
      const links = await read('legacy-links.json');
      const key = decodeURIComponent(location.hash.slice(6));
      location.replace(links.modules[key] || root + 'library/modules/');
    } catch (_) { location.replace(root + 'library/modules/'); }
    return;
  }
  const old = /^#([rdma])\/([^?]+)(?:\?(.*))?$/.exec(location.hash);
  if (old) {
    try {
      const links = await read('legacy-links.json');
      const kinds = {r: 'results', d: 'declarations', m: 'modules', a: 'algorithms'};
      const picked = new URLSearchParams(old[3] || '').get('s');
      const key = decodeURIComponent(old[2]);
      const target = (picked && links.declarations[picked]) ||
        (old[1] === 'r' && links.result_focus[key]) || links[kinds[old[1]]][key];
      if (target) { location.replace(target); return; }
    } catch (_) { /* The static page remains readable when metadata is unavailable. */ }
  }
  function renderMath(math) {
    if (window.katex) window.katex.render(math.textContent, math, {
      displayMode: math.classList.contains('display'), throwOnError: false, trust: false
    });
  }
  for (const math of document.querySelectorAll('.math')) renderMath(math);
  function revealSection() {
    let target;
    try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (_) { return; }
    if (!target) return;
    for (let node = target; node; node = node.parentElement) if (node.tagName === 'DETAILS') node.open = true;
    target.scrollIntoView();
  }
  revealSection();
  window.addEventListener('hashchange', revealSection);
  function titleLink(item) {
    const link = document.createElement('a'); link.href = item.url;
    for (const part of item.title.split(/(\$\$.*?\$\$|\$[^$\n]+\$|`[^`]+`)/)) {
      if (part.startsWith('$')) {
        const math = document.createElement('span'); math.className = 'math';
        math.textContent = part.replace(/^\$+|\$+$/g, ''); renderMath(math); link.append(math);
      } else if (part.startsWith('`')) {
        const code = document.createElement('code'); code.textContent = part.slice(1, -1); link.append(code);
      } else link.append(document.createTextNode(part));
    }
    return link;
  }
  let searchPromise;
  function getSearch() {
    if (!searchPromise) searchPromise = read('search-index.json').then(data => window.NlaSearch.create(data.entries, data.synonyms)).catch(error => { searchPromise = null; throw error; });
    return searchPromise;
  }
  const headerInput = document.getElementById('site-query');
  const quick = document.getElementById('quick-search');
  if (headerInput && quick) {
    headerInput.addEventListener('focus', () => { getSearch().catch(() => {}); }, {once: true});
    // Warm the cache after the page paints, so typing does not start a large download.
    if ('requestIdleCallback' in window) requestIdleCallback(() => { getSearch().catch(() => {}); }, {timeout: 1500});
    let timer, revision = 0;
    headerInput.addEventListener('input', () => {
      clearTimeout(timer);
      const current = ++revision;
      if (!headerInput.value.trim()) { quick.hidden = true; return; }
      timer = setTimeout(async () => {
        const query = headerInput.value.trim();
        quick.textContent = 'Searching…'; quick.hidden = false;
        try {
          const searchIndex = await getSearch();
          if (current !== revision) return;
          const results = searchIndex(query);
          const list = document.createElement('ul');
          for (const item of results.entries.slice(0, 6)) {
            const li = document.createElement('li');
            const link = titleLink(item);
            li.append(link); list.append(li);
          }
          const note = document.createElement('p');
          const all = document.createElement('a'); all.href = root + 'search/?q=' + encodeURIComponent(query);
          all.textContent = results.entries.length ? `See all ${results.entries.length} ${results.related ? 'related ' : ''}results` : 'No results. Try a shorter term.';
          note.append(all); quick.replaceChildren(list, note); quick.hidden = false;
        } catch (_) { quick.textContent = 'Search could not load. Submit to retry.'; quick.hidden = false; }
      }, 180);
    });
    headerInput.addEventListener('keydown', event => { if (event.key === 'Escape') { clearTimeout(timer); revision++; quick.hidden = true; } });
  }
  const form = document.getElementById('library-search');
  if (!form) return;
  const status = document.getElementById('search-status');
  const output = document.getElementById('search-results');
  const more = document.getElementById('more-results');
  form.elements.q.value = params.get('q') || '';
  form.elements.kind.value = params.get('kind') || '';
  let index;
  try { index = await getSearch(); }
  catch (_) { status.textContent = 'Search data could not be loaded. Reload to retry.'; return; }
  let matched = [], shown = 0, related = false;
  function append() {
    for (const item of matched.slice(shown, shown + 40)) {
      const li = document.createElement('li');
      const link = titleLink(item);
      const summary = document.createElement('p'); summary.textContent = item.summary || item.kind;
      li.append(link, summary); output.append(li);
    }
    shown = Math.min(shown + 40, matched.length); more.hidden = shown >= matched.length;
    status.textContent = !form.elements.q.value.trim() ? 'Enter a mathematical term or Lean name.' : `${matched.length} ${related ? 'related ' : ''}results; showing ${shown}.`;
  }
  function search() {
    const q = form.elements.q.value.trim();
    const kind = form.elements.kind.value;
    const result = index(q, kind); matched = result.entries; related = result.related;
    output.replaceChildren(); shown = 0; append();
    const query = new URLSearchParams(); if (q) query.set('q', q); if (kind) query.set('kind', kind);
    history.replaceState(null, '', location.pathname + (query.size ? '?' + query : ''));
  }
  let timer;
  form.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 180); });
  form.addEventListener('submit', e => { e.preventDefault(); clearTimeout(timer); search(); });
  more.addEventListener('click', append);
  search();
})();
