'use strict';
(() => {
  const picker = document.getElementById('computation-model');
  const models = ['exact', 'relative', 'sequential', 'pairwise'];
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
    const value = models.includes(url.searchParams.get('model')) ? url.searchParams.get('model') : (targetModel || 'exact');
    if (picker) {
      picker.value = value;
      for (const section of document.querySelectorAll('[data-cg-model]')) section.hidden = section.dataset.cgModel !== value;
      document.getElementById('model-status').textContent = 'Showing ' + picker.selectedOptions[0].textContent;
    }
    for (const link of document.querySelectorAll('[data-model-link]')) {
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
