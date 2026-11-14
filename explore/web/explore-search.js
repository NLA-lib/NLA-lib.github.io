/* Keyword retrieval shared by the header and full search page. No proof applicability claim. */
(function (root) {
  'use strict';
  const stop = new Set('a an the of for to in on and is are with does do how can i we that this about what which'.split(' '));
  const lower = value => String(value || '').toLowerCase();
  const words = value => lower(value).match(/[\p{L}\p{N}_]+/gu) || [];
  const stem = word => word === 'matrices' ? 'matrix' : word.endsWith('ies') ? word.slice(0, -3) + 'y' : word.length > 4 && word.endsWith('s') ? word.slice(0, -1) : word;
  const contains = (text, term) => text.includes(term) || (term.includes(' ') && words(term).every(word => text.includes(word)));
  function create(entries, synonyms = {}) {
    const aliases = {...synonyms, cg: ['conjugate gradient', 'cg'],
      'conjugate gradient': ['cg', 'conjugate gradient'],
      'generalized inverse': ['pinv', 'pseudoinverse'], product: ['mul', 'multiplication', 'product']};
    const documents = entries.filter(e => !e.admission_reported).map(e => ({e,
      name: lower(e.id), title: lower(e.title),
      aliases: (e.aliases || []).map(lower),
      text: lower([e.id, e.title, e.summary, e.signature, e.module, e.search_text].join(' '))}));
    return function search(query, kind = '') {
      const q = lower(query).trim();
      if (!q) return {entries: [], related: false};
      let remaining = q;
      const groups = [];
      for (const phrase of Object.keys(aliases).sort((a, b) => b.length - a.length)) {
        const escaped = phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const re = new RegExp('(^|[^\\p{L}\\p{N}_])' + escaped + '(?=$|[^\\p{L}\\p{N}_])', 'gu');
        if (re.test(remaining)) {
          groups.push([phrase, ...aliases[phrase].map(lower)]);
          remaining = remaining.replace(re, ' ');
        }
      }
      for (const word of words(remaining)) if (!stop.has(word)) groups.push([...new Set([word, stem(word)])]);
      if (!groups.length) return {entries: [], related: false};
      let ranked = documents.filter(d => !kind || d.e.kind === kind).map(d => {
        let hits = 0, score = ['result', 'algorithm'].includes(d.e.kind) ? 2 : 0;
        for (const group of groups) {
          const weight = Math.max(0, ...group.map(term => d.aliases.includes(term) ? 8 : contains(d.name, term) ? 6 : contains(d.title, term) ? 5 : contains(d.text, term) ? 1 : 0));
          if (weight) hits++;
          score += weight;
        }
        if (d.name === q || d.name.endsWith('.' + q) || d.aliases.includes(q)) score += 1000;
        return {entry: d.e, hits, score};
      });
      const complete = ranked.filter(r => r.hits === groups.length);
      const related = !complete.length;
      ranked = complete.length ? complete : ranked.filter(r => r.hits >= Math.max(1, Math.ceil(groups.length * .6)));
      ranked.sort((a, b) => b.hits - a.hits || b.score - a.score || a.entry.id.localeCompare(b.entry.id));
      return {entries: ranked.map(r => r.entry), related};
    };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {create};
  else root.NlaSearch = {create};
})(globalThis);
