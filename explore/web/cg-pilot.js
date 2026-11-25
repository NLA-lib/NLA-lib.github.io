'use strict';
(() => {
  const picker = document.getElementById('computation-model');
  const models = picker ? Array.from(picker.options, option => option.value) : [];
  // A retired model id selects the model that replaced it; an unknown one selects the first.
  const retired = new Map(picker ? Array.from(picker.options).flatMap(option =>
    (option.dataset.aliases || '').split(' ').filter(Boolean).map(alias => [alias, option.value])) : []);
  document.addEventListener('click', async (event) => {
    const link = event.target.closest('[data-copy-link]');
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    try {
      await navigator.clipboard.writeText(new URL(link.getAttribute('href'), location.href).href);
      const status = link.parentElement.querySelector('.copy-link-status');
      status.textContent = 'Link copied';
      setTimeout(() => { status.textContent = ''; }, 2000);
    } catch {
      location.assign(link.href);
    }
  });
  for (const card of document.querySelectorAll('.statement-overview')) {
    const details = card.querySelector('.explorer-result-details');
    const summary = details.querySelector('summary');
    const toggle = summary.querySelector('.statement-expand');
    const link = summary.querySelector('a');
    toggle.addEventListener('click', event => {
      event.preventDefault(); event.stopPropagation(); details.open = !details.open;
    });
    details.addEventListener('toggle', () => {
      toggle.setAttribute('aria-expanded', String(details.open));
      toggle.setAttribute('aria-label', details.open ? 'Collapse statement' : 'Expand statement');
      toggle.querySelector('span').textContent = details.open ? '↑' : '↓';
    });
    card.addEventListener('click', event => {
      if (event.defaultPrevented || event.target.closest('button,a,input,select,textarea') || window.getSelection()?.toString()) return;
      if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      location.assign(link.href);
    });
    // Keep native links (including modified clicks) and buttons independent.
    summary.addEventListener('click', event => {
      if (event.target.closest('a,button,input,select,textarea')) return;
      event.preventDefault();
      if (!event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) location.assign(link.href);
    });
  }
  function fragmentTarget() {
    try { return document.getElementById(decodeURIComponent(location.hash.slice(1))); }
    catch { return null; }
  }
  function revealFragment() {
    const target = fragmentTarget();
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === 'DETAILS') node.open = true;
    }
    return target;
  }
  function applyModel() {
    const url = new URL(location.href);
    const targetModel = fragmentTarget()?.closest('[data-cg-model]')?.dataset.cgModel;
    const asked = retired.get(url.searchParams.get('model')) || url.searchParams.get('model');
    const value = models.includes(asked) ? asked : (targetModel || models[0]);
    if (picker) {
      picker.value = value;
      for (const section of document.querySelectorAll('[data-cg-model]')) section.hidden = section.dataset.cgModel !== value;
      document.getElementById('model-status').textContent = 'Showing ' + picker.selectedOptions[0].textContent;
    }
    if (value) for (const link of document.querySelectorAll('[data-model-link]')) {
      const target = new URL(link.href);
      target.searchParams.set('model', value);
      link.href = target.pathname + target.search + target.hash;
    }
    revealFragment();
  }
  if (picker) picker.addEventListener('change', () => {
    const url = new URL(location.href);
    url.searchParams.set('model', picker.value);
    history.pushState(null, '', url);
    applyModel();
  });
  // Browsers restore saved form values after popstate; let the URL win afterward.
  window.addEventListener('popstate', () => setTimeout(applyModel, 0));
  window.addEventListener('pageshow', applyModel);
  window.addEventListener('hashchange', () => {
    applyModel();
    revealFragment()?.scrollIntoView({ block: 'start' });
  });
  applyModel();
})();
