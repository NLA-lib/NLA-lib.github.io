"""Markdown-authored explorer navigation over the extracted library records.

YAML front matter owns editorial identity and relationships. Generated sections
own lists and formal metadata; authored theorem prose never replaces Lean evidence.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shlex
import shutil
from urllib.parse import quote, urljoin

from markdown_it import MarkdownIt
import yaml

from cg_presentation import card, disclosure, mathematics, prose
from rendering import inline_title, record_component, prose_html

BASE = '/explore/'
KINDS = {'home', 'index', 'task', 'family', 'algorithm', 'implementation', 'theory'}
RELATIONS = {'tasks': 'task', 'theory': 'theory', 'prerequisites': 'theory',
             'parents': 'theory', 'uses': 'algorithm', 'families': 'family'}
MARKER = re.compile(r'^\{\{\s*generated:([a-z-]+)\s*\}\}\s*$', re.M)
STATEMENT = re.compile(r'^::: (theorem|definition)(?: (result|decl):([^\s]+))?([^\n]*)\n(.*?)\n:::\s*$', re.M | re.S)
MD = MarkdownIt('commonmark', {'html': False}).enable('table')


def slug(text):
    return '-'.join(re.findall(r'[a-z0-9]+', text.lower())) or 'statement'


class StatementLinks(HTMLParser):
    """Give every statement a stable fragment and retain its arithmetic context."""
    def __init__(self, body):
        super().__init__(convert_charrefs=False)
        self.output, self.stack = [], []
        self.used = set(re.findall(r'\bid="([^"]+)"', body))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        model = attrs.get('data-cg-model') or (self.stack[-1][1] if self.stack else None)
        context = self.stack[-1][2] if self.stack else None
        raw = self.get_starttag_text()
        statement = tag == 'article' and any('cg-' + kind in attrs.get('class', '').split()
                                            for kind in ['result', 'cost', 'model', 'algorithm'])
        if statement:
            identifier = attrs.get('id')
            if not identifier:
                base = (model + '-' if model else '') + slug(attrs.get('aria-label', 'statement'))
                identifier, suffix = base, 2
                while identifier in self.used:
                    identifier, suffix = base + '-' + str(suffix), suffix + 1
                self.used.add(identifier)
                raw = raw[:-1] + ' id="' + identifier + '">'
            href = ('?model=' + model if model else '') + '#' + identifier
            context = {'href': href, 'label': attrs.get('aria-label', 'statement'), 'inserted': False}
        self.output.append(raw)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, model, context, 'explorer-disclosure-body' in attrs.get('class', '').split()))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                _, _, context, disclosure_body = self.stack[index]
                if context and not context['inserted'] and (disclosure_body or tag == 'article'):
                    self.output.append('<p class="source-label statement-actions"><a class="statement-permalink" data-copy-link '
                        'href="' + context['href'] + '" aria-label="' + html.escape('Copy link to ' + context['label'], quote=True) +
                        '">Copy link</a><span class="copy-link-status" role="status"></span></p>')
                    context['inserted'] = True
                del self.stack[index:]
                break
        self.output.append('</' + tag + '>')

    def handle_startendtag(self, tag, attributes): self.output.append(self.get_starttag_text())

    def handle_data(self, data): self.output.append(data)
    def handle_entityref(self, name): self.output.append('&' + name + ';')
    def handle_charref(self, name): self.output.append('&#' + name + ';')
    def handle_comment(self, data): self.output.append('<!--' + data + '-->')


def statement_links(body):
    if '<article' not in body:
        return body
    parser = StatementLinks(body)
    parser.feed(body)
    return ''.join(parser.output)


@dataclass
class Page:
    source: Path
    meta: dict
    body: str

    @property
    def kind(self):
        return self.meta['kind']

    @property
    def key(self):
        return self.kind + ':' + (self.meta['algorithm'] + '/' if self.kind == 'implementation' else '') + self.meta['id']

    @property
    def path(self):
        if self.kind == 'home':
            return ''
        if self.kind == 'index':
            return self.meta['id']
        if self.kind == 'implementation':
            return 'algorithms/' + self.meta['algorithm'] + '/implementations/' + self.meta['id']
        return {'family': 'families', 'algorithm': 'algorithms', 'task': 'tasks', 'theory': 'theory'}[self.kind] + '/' + self.meta['id']

    @property
    def url(self):
        return BASE + (self.path + '/' if self.path else '')


def load_pages(directory):
    pages = {}
    routes = set()
    for file in sorted(Path(directory).rglob('*.md')):
        if file.name == 'README.md':
            continue
        match = re.fullmatch(r'---\n(.*?)\n---\n(.*)', file.read_text(), re.S)
        if not match:
            raise ValueError(f'{file}: expected YAML front matter')
        meta = yaml.safe_load(match[1])
        if not isinstance(meta, dict) or not all(meta.get(k) for k in ['kind', 'id', 'title']):
            raise ValueError(f'{file}: kind, id and title are required')
        if 'library_topics' in meta:
            raise ValueError(f'{file}: use module_prefixes instead of retired library_topics')
        if meta['kind'] not in KINDS or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(meta['id'])):
            raise ValueError(f'{file}: invalid kind or id')
        if meta['kind'] == 'implementation' and not meta.get('algorithm'):
            raise ValueError(f'{file}: implementation requires algorithm')
        if meta.get('status', 'outline') not in {'ready', 'outline', 'placeholder'}:
            raise ValueError(f'{file}: invalid status')
        if not isinstance(meta.get('sections_collapsed', False), bool):
            raise ValueError(f'{file}: sections_collapsed must be a boolean')
        page = Page(file, meta, match[2])
        if page.key in pages or page.path in routes:
            raise ValueError(f'{file}: duplicate identity or route')
        pages[page.key] = page
        routes.add(page.path)
    # Task-local groups own discovery placement. An algorithm's URL and global
    # conceptual families remain independent of the task's editorial taxonomy.
    grouped_tasks = {p.meta['id'] for p in pages.values() if p.kind == 'task' and 'groups' in p.meta}
    for page in pages.values():
        if 'groups' in page.meta and page.kind != 'task':
            raise ValueError(f'{page.source}: groups belong to task pages')
        if page.kind == 'algorithm':
            if not isinstance(page.meta.get('tasks', []), list):
                raise ValueError(f'{page.source}: tasks must be a list')
            page.meta['tasks'] = [t for t in page.meta.get('tasks', []) if t not in grouped_tasks]
    for task in [p for p in pages.values() if p.kind == 'task' and 'groups' in p.meta]:
        groups = task.meta['groups']
        if not isinstance(groups, list) or not groups:
            raise ValueError(f'{task.source}: groups must be a nonempty list')
        ids = set()
        for group in groups:
            if not isinstance(group, dict) or not all(group.get(k) for k in ['id', 'title', 'algorithms']):
                raise ValueError(f'{task.source}: each group requires id, title and algorithms')
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(group['id'])) or group['id'] in ids:
                raise ValueError(f'{task.source}: invalid or duplicate group id')
            ids.add(group['id'])
            members = group['algorithms']
            if not isinstance(members, list) or any(not isinstance(m, str) for m in members) or len(set(members)) != len(members):
                raise ValueError(f'{task.source}: group algorithms must be a list of distinct algorithm IDs')
            if group.get('family') and 'family:' + group['family'] not in pages:
                raise ValueError(f'{task.source}: unknown group family {group["family"]}')
            if group.get('family'):
                family = pages['family:' + group['family']]
                if task.meta['id'] not in family.meta.setdefault('tasks', []):
                    family.meta['tasks'].append(task.meta['id'])
            summaries = group.get('summaries', {})
            if not isinstance(summaries, dict) or set(summaries) - set(members) or any(not isinstance(v, str) for v in summaries.values()):
                raise ValueError(f'{task.source}: group summaries must describe its algorithm IDs')
            for member in members:
                if 'algorithm:' + member not in pages:
                    raise ValueError(f'{task.source}: unknown group algorithm {member}')
                algorithm = pages['algorithm:' + member]
                if task.meta['id'] not in algorithm.meta['tasks']:
                    algorithm.meta['tasks'].append(task.meta['id'])
    for page in pages.values():
        for relation, kind in RELATIONS.items():
            values = page.meta.get(relation, [])
            if not isinstance(values, list):
                raise ValueError(f'{page.source}: {relation} must be a list')
            for value in values:
                if kind + ':' + value not in pages:
                    raise ValueError(f'{page.source}: unknown {relation} reference {value}')
        if page.kind == 'implementation' and 'algorithm:' + page.meta['algorithm'] not in pages:
            raise ValueError(f'{page.source}: unknown parent algorithm')
    for kind, relation in [('theory', 'parents'), ('theory', 'prerequisites'), ('algorithm', 'uses')]:
        visited, active = set(), set()
        def visit(key):
            if key in active:
                raise ValueError(f'Cycle in {relation}: {key}')
            if key in visited:
                return
            active.add(key)
            for target in pages[key].meta.get(relation, []):
                visit(kind + ':' + target)
            active.remove(key)
            visited.add(key)
        for page in pages.values():
            if page.kind == kind:
                visit(page.key)
    return pages


def markdown(text):
    """CommonMark with escaped TeX islands, typeset client-side by KaTeX."""
    islands = []
    def keep(match):
        raw = match[0]
        display = raw.startswith('$$')
        tex = raw[2:-2] if display else raw[1:-1]
        islands.append('<span class="math' + (' display' if display else '') + '">' + html.escape(tex.strip()) + '</span>')
        return 'EXPLORERMATHISLAND' + str(len(islands) - 1) + 'END'
    # Protect code fences and inline code from math replacement.
    chunks = re.split(r'(```[\s\S]*?```|`[^`\n]+`)', text)
    for i in range(0, len(chunks), 2):
        chunks[i] = re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$', keep, mathematics(chunks[i]))
    rendered = MD.render(''.join(chunks))
    return re.sub(r'EXPLORERMATHISLAND(\d+)END', lambda m: islands[int(m[1])], rendered)


class Explorer:
    def __init__(self, site, content):
        self.site = Path(site)
        self.api = self.site / 'api/v1'
        self.content = Path(content)
        self.pages = load_pages(content)
        self.records = {}
        for kind in ['algorithms', 'tasks', 'results', 'declarations', 'modules', 'guides']:
            records = [json.loads(p.read_text())['record'] for p in (self.api / kind).glob('*.json')]
            self.records[kind] = {record['id']: record for record in records}
        self.template = (self.site / 'index.html').read_text()
        self.search_version = ''
        self.search_form = ('<form id="library-search" role="search"><label>Query <input id="library-query" name="q" type="search"></label>'
            '<label>Kind <select id="kind" name="kind"><option value="">All</option><option>theorem</option><option>def</option>'
            '<option>structure</option><option>result</option><option>algorithm</option></select></label><button>Search</button></form>'
            '<p id="search-status" role="status"></p><ol id="search-results"></ol><button type="button" id="more-results" hidden>More results</button>'
            '<noscript><p>Use the <a href="/explore/library/modules/">module index</a> to browse without JavaScript.</p></noscript>')
        self.cg = json.loads((self.api / 'cg-pilot-fragments.json').read_text()) if (self.api / 'cg-pilot-fragments.json').exists() else {}
        moves = self.api / 'module-moves.json'
        self.module_moves = json.loads(moves.read_text())['moves'] if moves.exists() else {}

    def link(self, page):
        return '<a href="' + page.url + '"' + (' data-model-link' if page.kind in {'family', 'algorithm', 'implementation'} else '') + '>' + inline_title(mathematics(page.meta['title'])) + '</a>'

    def cards(self, pages, summaries=None, preserve_order=False):
        items = []
        pages = list(pages)
        for page in pages if preserve_order else sorted(pages, key=lambda p: (p.meta.get('order', 100), p.meta['title'])):
            summary = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', markdown((summaries or {}).get(page.meta['id'], page.meta.get('summary', ''))), flags=re.S)
            items.append('<a class="explorer-card explorer-link-card" href="' + page.url + '" aria-label="' +
                html.escape(page.meta['title'], quote=True) + '"' +
                (' data-model-link' if page.kind in {'family', 'algorithm', 'implementation'} else '') +
                '><h3 class="explorer-card-title">' + inline_title(mathematics(page.meta['title'])) + '</h3>' +
                summary + '</a>')
        return ''.join(items) or '<p>No entries have been added yet.</p>'

    def status(self, page):
        if page.meta.get('renderer') == 'cg' and page.meta.get('source_variant') not in self.cg:
            return 'outline'
        return page.meta.get('status', 'outline')

    def associated(self, page, relation, reverse=False):
        target_kind = RELATIONS[relation]
        if reverse:
            return [p for p in self.pages.values() if page.meta['id'] in p.meta.get(relation, [])]
        return [self.pages[target_kind + ':' + key] for key in page.meta.get(relation, [])]

    def selection(self, page):
        results, definitions = set(page.meta.get('result_ids', [])), set()
        aid = page.meta.get('library_algorithm')
        if aid:
            if aid not in self.records['algorithms']:
                raise ValueError(f'{page.source}: unknown library_algorithm {aid}')
            if page.meta.get('library_results', True):
                results.update(self.records['algorithms'][aid]['results'])
        prefixes = page.meta.get('module_prefixes', [])
        for name, d in self.records['declarations'].items():
            if any(d['module'] == prefix or d['module'].startswith(prefix + '.') for prefix in prefixes):
                results.update(d['results'])
                if d['kind'] != 'theorem':
                    definitions.add(name)
        for prefix in page.meta.get('result_prefixes', []):
            results.update(rid for rid in self.records['results'] if rid == prefix or rid.startswith(prefix + '-'))
        missing = results - self.records['results'].keys()
        if missing:
            raise ValueError(f'{page.source}: unknown result IDs {sorted(missing)}')
        return sorted(results), sorted(definitions)

    def evidence(self, declaration):
        link = declaration['source']['url']
        return '<pre><code>' + html.escape(declaration['signature']) + '</code></pre>' + (
            '<p><a href="' + html.escape(link, quote=True) + '">Full source on GitHub</a></p>' if link else '<p><a href="https://github.com/NLA-lib/NLAlib">Source repository on GitHub</a> · <code>' + html.escape(declaration['source'].get('path', declaration['module'])) + '</code></p><p>This statement comes from an unpublished working-tree snapshot; a revision-specific source link is unavailable.</p>')

    def result_reference(self, key):
        """Browse documented results in place; keep the exact Lean evidence separate."""
        record = self.records['results'][key]
        declaration = self.records['declarations'][record['primary']]
        label = ('Statement' if declaration.get('admission_reported') else
                 'Theorem' if declaration['kind'] == 'theorem' else 'Definition')
        text = declaration.get('docstring') or declaration.get('summary', '')
        text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
        text = re.sub(r'^(?:Result|Algorithm):[^\n]*$', '', text, flags=re.M).strip()
        # The title is already in the disclosure header. Retain all hypotheses,
        # formulas, qualifications and references in the documented statement.
        text = re.sub(r'^\*\*[^*]+\*\*\s*[:.]?\s*', '', text).strip() or text
        body = prose_html(text) if text else '<p>The exact statement is available in the Lean details below.</p>'
        if declaration.get('admission_reported'):
            body = '<p>This library statement reports an admission.</p>' + body
        body += disclosure(self.evidence(declaration))
        title = inline_title(mathematics(record['title']))
        return '<article class="explorer-card cg-result explorer-result-reference" id="' + label.lower() + '-' + slug(key) + \
            '" aria-label="' + html.escape(label + ' (' + record['title'] + ')', quote=True) + \
            '"><details class="explorer-disclosure explorer-result-details"><summary><span class="explorer-statement-label"><strong>' + \
            label + '</strong> (' + title + ')<strong>.</strong></span></summary><div class="explorer-disclosure-body">' + body + '</div></details></article>'

    def statement(self, match):
        kind, source_kind, key, options, body = match.groups()
        title = ''
        declaration = None
        if source_kind == 'result':
            if key not in self.records['results']:
                raise ValueError('Unknown result in Markdown statement: ' + key)
            record = self.records['results'][key]
            declaration = self.records['declarations'][record['primary']]
            title = record['title']
        elif source_kind == 'decl':
            if key not in self.records['declarations']:
                raise ValueError('Unknown declaration in Markdown statement: ' + key)
            declaration = self.records['declarations'][key]
            title = key.removeprefix('NLAlib.')
        elif kind == 'theorem':
            raise ValueError('A theorem block must name a library result or declaration')
        if declaration and (kind == 'theorem') != (declaration['kind'] == 'theorem'):
            raise ValueError('Statement kind disagrees with library declaration: ' + key)
        if declaration and kind == 'theorem' and declaration.get('admission_reported'):
            raise ValueError('Cannot present an admitted declaration as a checked theorem: ' + key)
        identifier = kind + '-' + slug(key) if key else None
        for option in shlex.split(options):
            if option.startswith('id='):
                identifier = option.split('=', 1)[1]
                if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', identifier):
                    raise ValueError('Invalid statement anchor: ' + identifier)
                continue
            if not option.startswith('name='):
                raise ValueError('Unknown statement option: ' + option)
            title = option.split('=', 1)[1]
        if not title:
            raise ValueError('An authored definition requires a name')
        return card(title, markdown(body) + (disclosure(self.evidence(declaration)) if declaration else ''),
                    'result' if kind == 'theorem' else 'model', identifier)

    def generated(self, slot, page):
        if slot == 'task-groups':
            if page.kind != 'task':
                raise ValueError(f'{page.source}: task-groups requires a task page')
            sections = []
            for group in page.meta.get('groups', []):
                body = markdown(group.get('summary', ''))
                body += self.cards([self.pages['algorithm:' + key] for key in group['algorithms']],
                                   group.get('summaries'), preserve_order=True)
                if group.get('family'):
                    family = self.pages['family:' + group['family']]
                    body += '<p class="record-link">' + self.link(family) + '</p>'
                opened = '' if page.meta.get('sections_collapsed') else ' open'
                sections.append('<details class="explorer-section task-group"' + opened + ' id="group-' + group['id'] +
                    '"><summary><h2>' + inline_title(group['title']) + '</h2></summary><div class="explorer-section-body">' + body + '</div></details>')
            return ''.join(sections)
        if slot == 'source-guides':
            guides = [g for g in self.records['guides'].values() if g['source']['path'] in page.meta.get('source_guides', [])]
            links = ''.join('<p><a href="' + g['url'] + '">' + inline_title(g['title']) + '</a></p>' for g in guides)
            return disclosure(links, 'Implementation guides') if links else ''
        if slot == 'entry-points':
            return self.cards(self.pages['index:' + key] for key in ['algorithms', 'theory', 'library'])
        if slot == 'tasks':
            return self.cards(p for p in self.pages.values() if p.kind == 'task')
        if slot == 'algorithms':
            if page.kind == 'family':
                return self.cards(self.associated(page, 'families', reverse=True))
            return self.cards(p for p in self.pages.values() if p.kind == 'algorithm' and
                              (page.kind != 'task' or page.meta['id'] in p.meta.get('tasks', [])) and
                              not any(page.kind != 'task' or page.meta['id'] in self.pages['family:' + family].meta.get('tasks', [])
                                      for family in p.meta.get('families', [])))
        if slot == 'families':
            return self.cards(self.associated(page, 'families') if page.kind == 'algorithm' else
                              [p for p in self.pages.values() if p.kind == 'family' and
                               (page.kind != 'task' or page.meta['id'] in p.meta.get('tasks', []))])
        if slot == 'implementations':
            matches = [p for p in self.pages.values() if p.kind == 'implementation' and p.meta['algorithm'] == page.meta['id']]
            return self.cards(matches) if matches else ''
        if slot == 'mathematical-method':
            return self.cards([self.pages['algorithm:' + page.meta['algorithm']]])
        if slot == 'theory':
            return self.cards(self.associated(page, 'theory'))
        if slot == 'theory-topics':
            return self.cards(p for p in self.pages.values() if p.kind == 'theory' and not p.meta.get('parents'))
        if slot == 'subtopics':
            return self.cards(self.associated(page, 'parents', reverse=True))
        if slot == 'parent-topics':
            matches = self.associated(page, 'parents')
            return self.cards(matches) if matches else ''
        if slot == 'prerequisites':
            matches = self.associated(page, 'prerequisites')
            return self.cards(matches) if matches else ''
        if slot == 'used-by':
            topics = {page.meta['id']}
            while True:
                expanded = topics | {p.meta['id'] for p in self.pages.values() if p.kind == 'theory' and topics.intersection(p.meta.get('parents', []))}
                if expanded == topics:
                    break
                topics = expanded
            matches = [p for p in self.pages.values() if p.kind == 'algorithm' and topics.intersection(p.meta.get('theory', []))]
            if not matches:
                return ''
            rendered = self.cards(matches)
            return disclosure(rendered, f'{len(matches)} algorithms using this topic or its subtopics') if len(matches) > 6 else rendered
        if slot == 'applications':
            components = {page.meta['id']}
            while True:
                expanded = components | {p.meta['id'] for p in self.pages.values() if p.kind == 'algorithm'
                                         and components.intersection(p.meta.get('uses', []))}
                if expanded == components:
                    break
                components = expanded
            matches = [p for p in self.pages.values() if p.kind == 'algorithm'
                       and p.meta['id'] in components - {page.meta['id']}]
            return self.cards(matches) if matches else ''
        if slot == 'components':
            matches = self.associated(page, 'uses')
            return self.cards(matches) if matches else ''
        if slot == 'task-membership':
            parent = self.pages['algorithm:' + page.meta['algorithm']] if page.kind == 'implementation' else page
            return self.cards(self.associated(parent, 'tasks'))
        if slot == 'results':
            result_ids, _ = self.selection(page)
            authored = set()
            for statement in STATEMENT.finditer(page.body):
                if statement[2] == 'result':
                    authored.add(self.records['results'][statement[3]]['primary'])
                elif statement[2] == 'decl':
                    authored.add(statement[3])
            items = []
            for key in result_ids:
                primary = self.records['results'][key]['primary']
                if primary not in authored:
                    items.append(self.result_reference(key))
                    authored.add(primary)
            return ''.join(items)
        if slot == 'definitions':
            _, names = self.selection(page)
            if not names:
                return ''
            rendered = self.reference_list('declarations', names)
            return rendered
        if slot == 'library-counts':
            return '<p>' + ' · '.join(f'{len(rs):,} {kind}' for kind, rs in self.records.items()
                                      if kind in {'results', 'declarations', 'modules'}) + '</p>'
        if slot == 'library-index':
            return ''.join('<p><a href="' + BASE + 'library/' + kind + '/">' + label + '</a></p>'
                           for kind, label in [('results', 'Named results'), ('definitions', 'Definitions and interfaces'),
                                               ('modules', 'Source modules'), ('guides', 'Implementation guides')]
                           if kind != 'guides' or self.records['guides'])
        if slot == 'search':
            form = self.search_form.replace('<option>variant</option>', '<option>implementation</option>')
            for kind in ['family', 'implementation', 'task', 'theory', 'guide']:
                if '<option>' + kind + '</option>' not in form:
                    form = form.replace('<option>algorithm</option>', '<option>algorithm</option><option>' + kind + '</option>')
            return form
        if slot.startswith('cg-'):
            source = page.meta.get('source_variant', 'concept')
            fragment = self.cg.get(source, {}).get(slot)
            if fragment:
                return fragment.replace('/conjugate-gradient/variants/carried/', '/conjugate-gradient/implementations/ordinary/').replace('/conjugate-gradient/variants/pcg/', '/preconditioned-conjugate-gradient/implementations/standard/').replace('/conjugate-gradient/variants/reorth/', '/conjugate-gradient/implementations/full-reorthogonalization/')
            return '<p class="content-placeholder">The detailed CG preview requires matching core-source metadata. This section will be filled by the source adapter.</p>'
        raise ValueError(f'{page.source}: unknown generated section {slot}')

    def reference_list(self, kind, keys):
        if not keys:
            return '<p>No library records are selected for this section yet.</p>'
        return '<ul class="entry-list">' + ''.join('<li><a href="' + self.reference_url(kind, key) + '">' +
            inline_title(mathematics(self.records[kind][key].get('title', key))) + '</a></li>' for key in keys) + '</ul>'

    @staticmethod
    def reference_url(kind, key):
        return BASE + 'library/' + kind + '/' + quote(record_component(key), safe='.') + '/'

    def render_body(self, page):
        slots = []
        def keep(value):
            if not value:
                return ''
            slots.append(value)
            return '\n\nEXPLORERGENERATEDBLOCK' + str(len(slots) - 1) + 'END\n\n'
        text = STATEMENT.sub(lambda m: keep(self.statement(m)), page.body)
        text = MARKER.sub(lambda m: keep(self.generated(m[1], page)), text)
        if re.search(r'\{\{\s*generated:|^::: (theorem|definition)', text, re.M):
            raise ValueError(f'{page.source}: malformed generated marker or statement block')
        lines = text.splitlines(keepends=True)
        headings = [t for t in MD.parse(text) if t.type == 'heading_open' and t.tag == 'h2' and t.level == 0]
        if headings:
            rendered = markdown(''.join(lines[:headings[0].map[0]]))
            for index, heading in enumerate(headings):
                start, end = heading.map
                stop = headings[index + 1].map[0] if index + 1 < len(headings) else len(lines)
                title = ''.join(lines[start:end])
                section_body = markdown(''.join(lines[end:stop]))
                if not section_body.strip():
                    continue
                opened = '' if page.meta.get('sections_collapsed') or slug(title) in {'mathematical-background', 'appears-under-these-tasks', 'family', 'broader-topics', 'formal-definitions'} else ' open'
                rendered += '<details class="explorer-section"' + opened + ' id="section-' + slug(title) + '"><summary>' + markdown(title) + \
                    '</summary><div class="explorer-section-body">' + section_body + '</div></details>'
        else:
            rendered = markdown(text)
        return re.sub(r'<p>EXPLORERGENERATEDBLOCK(\d+)END</p>', lambda m: slots[int(m[1])], rendered)

    def write(self, path, title, body, active=''):
        body = statement_links(body)
        links = [('algorithms', 'Algorithms'), ('theory', 'Theory'), ('library', 'Library')]
        nav = '<nav class="explorer-navigation" aria-label="Explorer">' + ''.join(
            '<a href="' + BASE + key + '/"' + (' aria-current="page"' if key == active else '') + '>' + label + '</a>' for key, label in links) + '</nav>'
        page = re.sub(r'<main id="content">.*?</main>', lambda _: '<main id="content">' + nav +
            ('<h2 class="page-title">' + inline_title(mathematics(title)) + '</h2>' if path else '') + body + '</main>', self.template, flags=re.S)
        page = re.sub(r'<title>.*?</title>', lambda _: '<title>NLA-lib · Explorer' + (' · ' + html.escape(title) if path else '') + '</title>', page)
        page = re.sub(r'<meta name="description"[^>]*>', '', page)
        page = re.sub(r'<link rel="canonical"[^>]*>', '', page)
        page = re.sub(r'(href|src)="(?:\.\./|\./)*(?=(?:css/|style\.|explore[.-]|vendor/|cg-pilot\.))', r'\1="/explore/', page)
        page = re.sub(r'data-root="[^"]*"', 'data-root="/explore/"', page)
        page = re.sub(r'class="explore-pages(?: cg-pilot)?"', 'class="explore-pages cg-pilot"', page)
        if '/explore/cg-pilot.css' not in page:
            page = page.replace('</head>', '<link rel="stylesheet" href="/explore/cg-pilot.css"><script defer src="/explore/cg-pilot.js"></script></head>')
        version = self.search_version
        page = re.sub(r'data-search-version="[^"]*"', 'data-search-version="' + version + '"', page)
        page = page.replace('/explore/catalog/', '/explore/library/modules/')
        page = page.replace('Source catalogue and dependency graphs', 'Library reference')
        if path == 'search':
            page = page.replace('<form id="site-search"', '<form hidden id="site-search"')
        target = self.site / path / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)

    def render_library(self):
        from source_documents import rewrite_links
        for kind in ['results', 'declarations', 'modules']:
            for key, record in self.records[kind].items():
                if kind == 'results':
                    declarations = [self.records['declarations'][name] for name in record['declarations']]
                    body = '<p class="eyebrow">Library · Result group</p>' + ''.join(
                        card(d['id'].removeprefix('NLAlib.'), prose(d.get('summary', '') or d['kind']) + disclosure(self.evidence(d)),
                             'result' if d['kind'] == 'theorem' else 'model') for d in declarations)
                elif kind == 'declarations':
                    body = '<p class="eyebrow">Library · ' + html.escape(record['kind']) + '</p>'
                    if record.get('admission_reported'):
                        body += '<p class="content-status">The extraction reports an admitted dependency for this declaration.</p>'
                    if record.get('statement_changed'):
                        body += '<p class="source-label">This statement changed in the recorded rename: ' + ', '.join(
                            '<code>' + html.escape(name) + '</code>' for name in record['statement_changed']) + '.</p>'
                    docs = prose(record['docstring'])
                    if record['source']['url']:
                        docs = re.sub(r'href="([^\"]+\.(?:lean|md)(?:#[^\"]*)?)"', lambda m:
                            'href="' + html.escape(urljoin(record['source']['url'], html.unescape(m[1])), quote=True) + '"', docs)
                    body += docs + self.evidence(record)
                    body += '<p>Import <code>' + html.escape(record['module']) + '</code>.</p>'
                else:
                    docs = prose(record.get('summary', ''))
                    origin = next((self.records['declarations'][name]['source']['url']
                                   for name in record['declarations'] if self.records['declarations'][name]['source']['url']), None)
                    if origin:
                        docs = re.sub(r'href="([^\"]+\.(?:lean|md)(?:#[^\"]*)?)"', lambda m:
                            'href="' + html.escape(urljoin(origin, html.unescape(m[1])), quote=True) + '"', docs)
                    body = '<p class="eyebrow">Library · Source module</p>' + docs
                    body += '<h2>Declarations</h2>' + self.reference_list('declarations', record['declarations'])
                self.write('library/' + kind + '/' + record_component(key), record.get('title', key), body, 'library')
        # Rewritten computation interfaces need explanatory landings, not aliases
        # pretending that the old and new Lean statements are interchangeable.
        reconciliation = json.loads(Path(__file__).with_name('legacy_math_reconciliation.json').read_text())
        legacy_path = self.api / 'legacy-links.json'
        legacy = json.loads(legacy_path.read_text()) if legacy_path.is_file() else None
        for old, entry in reconciliation['declarations'].items():
            targets = entry.get('current', [])
            if entry['status'] != 'rewritten-interface' or old in self.records['declarations'] or not targets or not all(n in self.records['declarations'] for n in targets):
                continue
            landing = 'library/declarations/' + record_component(old)
            body = '<p>The sampling interface was rewritten during the Ops migration. The current statements use the Ops machine and tape interfaces, with their own explicit hypotheses.</p>'
            related = [p for p in self.pages.values() if p.url == entry['page']]
            if related:
                body += self.cards(related)
            body += '<h2>Current statements</h2>' + self.reference_list('declarations', targets)
            self.write(landing, old, body, 'library')
            from library import write_redirect
            write_redirect(self.site / 'declarations' / record_component(old) / 'index.html', BASE + landing + '/')
            if legacy is not None:
                legacy['declarations'][old] = BASE + landing + '/'
        if legacy is not None:
            legacy_path.write_text(json.dumps(legacy, ensure_ascii=False, separators=(',', ':')) + '\n')
        for key, guide in self.records['guides'].items():
            body = '<p class="source-label">' + html.escape(guide['source']['kind']) + ' · <code>' + html.escape(guide['source']['path']) + '</code></p>'
            guide_body = re.sub(r'^# [^\n]*\n', '', guide['markdown'], count=1)
            body += '<div class="guide-content">' + rewrite_links(markdown(guide_body), guide['source']['path'],
                self.records['modules'], self.records['guides'], guide['source']['url']) + '</div>'
            body += '<p class="source-label"><a href="source.md">Source Markdown</a> · SHA-256 <code>' + guide['source']['sha256'] + '</code></p>'
            if guide['source']['url']:
                body += '<p><a href="' + guide['source']['url'] + '">Full source on GitHub</a></p>'
            self.write('library/guides/' + key, guide['title'], body, 'library')
            (self.site / 'library/guides' / key / 'source.md').write_text(guide['markdown'])
        if self.records['guides']:
            self.write('library/guides', 'Implementation guides', self.reference_list('guides', sorted(self.records['guides'])), 'library')
        for old, move in self.module_moves.items():
            body = '<p>Mathematical declarations moved to the references below. Retired execution APIs are not restored by this module mapping.</p>'
            body += '<p>' + html.escape(move['note']) + '</p>' + self.reference_list('modules', move['modules'])
            self.write('library/module-moves/' + record_component(old), old, body, 'library')
        for key, record in self.records['algorithms'].items():
            if record.get('url', '').startswith(BASE + 'library/algorithms/'):
                body = '<p>Source-tagged discovery group. This association does not certify an implementation.</p>'
                body += '<h2>Declarations</h2>' + self.reference_list('declarations', [m['declaration'] for m in record.get('members', [])])
                body += '<h2>Results</h2>' + self.reference_list('results', record['results'])
                self.write('library/algorithms/' + record_component(key), record['title'], body, 'library')
        for kind, title in [('results', 'Named results'), ('modules', 'Source modules')]:
            self.write('library/' + kind, title, self.reference_list(kind, sorted(self.records[kind])), 'library')
        definitions = sorted(key for key, d in self.records['declarations'].items() if d['kind'] != 'theorem')
        self.write('library/definitions', 'Definitions and interfaces', self.reference_list('declarations', definitions), 'library')

    def search_and_registry(self):
        path = self.api / 'search-index.json'
        data = json.loads(path.read_text())
        inherited_search = {e['library_algorithm']: e.get('library_search_text', '')
                            for e in data['entries'] if e.get('library_algorithm')}
        data['entries'] = [entry for entry in data['entries'] if not entry.get('editorial_page')]
        alg_routes = {p.meta['library_algorithm']: p.url for p in self.pages.values()
                      if p.kind == 'algorithm' and p.meta.get('library_algorithm')}
        for p in self.pages.values():
            if p.meta.get('library_algorithm'):
                alg_routes.setdefault(p.meta['library_algorithm'], p.url)
        # Human URLs belong to the new explorer; formal identities and signatures stay unchanged.
        for kind in ['declarations', 'results', 'modules', 'algorithms']:
            for key, record in self.records[kind].items():
                url = alg_routes.get(key) if kind == 'algorithms' else self.reference_url(kind, key)
                if url:
                    record['url'] = url
                    record_file = self.api / kind / (record_component(key) + '.json')
                    envelope = json.loads(record_file.read_text())
                    envelope['record']['url'] = url
                    record_file.write_text(json.dumps(envelope, ensure_ascii=False, separators=(',', ':')) + '\n')
        retained = []
        for entry in data['entries']:
            kind = 'guides' if entry['kind'] == 'guide' else 'declarations' if entry['kind'] not in {'result', 'algorithm'} else entry['kind'] + 's'
            if kind == 'algorithms' and entry['id'] in alg_routes:
                inherited_search[entry['id']] = entry['search_text']
                continue
            entry['url'] = alg_routes.get(entry['id'], entry['url']) if kind == 'algorithms' else self.reference_url(kind, entry['id'])
            retained.append(entry)
        data['entries'] = retained
        for page in self.pages.values():
            data['entries'].append({'id': page.key, 'kind': page.kind, 'title': page.meta['title'], 'url': page.url,
                'summary': page.meta.get('summary', ''), 'module': '', 'record': BASE + 'api/v1/editorial-pages.json',
                'aliases': page.meta.get('search_aliases', []),
                'search_text': ' '.join(re.findall(r'\w+', page.body.lower() + ' ' + page.meta['title'].lower() + ' ' + ' '.join(page.meta.get('search_aliases', [])))) + ' ' + inherited_search.get(page.meta.get('library_algorithm'), ''),
                'library_algorithm': page.meta.get('library_algorithm'),
                'library_search_text': inherited_search.get(page.meta.get('library_algorithm'), ''),
                'admission_reported': False, 'editorial_page': True})
        path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
        self.search_version = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        path.with_suffix('.json.gz').write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        registry = {'schema_version': 1, 'pages': [{**p.meta, 'status': self.status(p), 'url': p.url,
            'source': str(p.source.relative_to(self.content)), 'source_sha256': hashlib.sha256(p.source.read_bytes()).hexdigest()}
            for p in self.pages.values()]}
        (self.api / 'editorial-pages.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')

    def build(self):
        # Resolve every marker before replacing any rendered page.
        rendered = {p.key: self.render_body(p) for p in self.pages.values()}
        for asset in ['cg-pilot.css', 'cg-pilot.js', 'explore.css', 'explore.js', 'explore-search.js']:
            shutil.copyfile(Path(__file__).parent / 'web' / asset, self.site / asset)
            digest = hashlib.sha256((self.site / asset).read_bytes()).hexdigest()[:12]
            self.template = re.sub(r'((?:href|src)="(?:/explore/)?' + re.escape(asset) + r')(?:\?[^\"]*)?"',
                                   lambda m: m[1] + '?v=' + digest + '"', self.template)
        self.search_and_registry()
        self.render_library()
        for page in self.pages.values():
            active = ('theory' if page.kind == 'theory' or page.key in {'index:theory', 'index:arithmetic-models'} else
                      'library' if page.key == 'index:library' else '' if page.kind == 'home' or page.key == 'index:search' else 'algorithms')
            body = rendered[page.key]
            if page.kind == 'implementation':
                body = '<p class="eyebrow">Implementation</p>' + body
            if page.meta.get('renderer') == 'cg' and page.meta.get('source_variant') in self.cg:
                body += '<p class="record-link">Implementation preview from the current computational core · <a href="/explore/api/v1/cg-pilot.json">Source metadata</a></p>'
            if self.status(page) == 'placeholder':
                body = '<p class="content-status">Placeholder · page structure only</p>' + body
            self.write(page.path, page.meta['title'], body, active)
        # Keep existing bookmarks, including their arithmetic-model query strings.
        redirects = {'families/cg-type-methods': BASE + 'families/galerkin-methods/'}
        for page in self.pages.values():
            if page.kind == 'implementation':
                redirects['algorithms/' + page.meta['algorithm'] + '/variants/' + page.meta['id']] = page.url
        for old, new in {'carried': 'conjugate-gradient/implementations/ordinary',
                         'ordinary': 'conjugate-gradient/implementations/ordinary',
                         'hscg': 'conjugate-gradient/implementations/ordinary',
                         'pcg': 'preconditioned-conjugate-gradient/implementations/standard',
                         'preconditioned': 'preconditioned-conjugate-gradient/implementations/standard',
                         'reorth': 'conjugate-gradient/implementations/full-reorthogonalization'}.items():
            redirects['algorithms/conjugate-gradient/variants/' + old] = BASE + 'algorithms/' + new + '/'
        for old, new in redirects.items():
            if new not in {page.url for page in self.pages.values()}:
                continue
            self.write(old, 'Page moved', '<p><a href="' + new + '">Continue to the implementation</a>.</p>' +
                       '<script>location.replace(' + json.dumps(new) + '+location.search+location.hash)</script>' +
                       '<noscript><meta http-equiv="refresh" content="0;url=' + new + '"></noscript>')
        print(f'Markdown explorer: {len(self.pages)} authored pages; {sum(len(self.records[k]) for k in ["declarations", "results", "modules"]):,} library records')


def build(site, content=None):
    explorer = Explorer(site, content or Path(__file__).parent / 'content')
    explorer.build()
    return explorer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True, type=Path)
    parser.add_argument('--content', type=Path, default=Path(__file__).parent / 'content')
    args = parser.parse_args()
    build(args.site, args.content)
