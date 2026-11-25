"""Shared reference identities for mathematical statements and their proof locators."""
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from rendering import safe_link


def editorial_references(content):
    path = Path(content) / 'references.json'
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get('schema_version') != 1 or set(data) != {'schema_version', 'references'} or not isinstance(data['references'], dict):
        raise ValueError('references.json requires schema_version: 1 and a references object')
    for key, record in data['references'].items():
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', key) or not isinstance(record, dict):
            raise ValueError('Invalid reference identity')
        if not isinstance(record.get('text'), str) or not record['text'].strip():
            raise ValueError('Each reference requires a citation text')
        if record.get('url') and (not isinstance(record['url'], str) or urlsplit(record['url']).scheme != 'https' or not safe_link(record['url'])):
            raise ValueError('Reference links must be safe HTTPS URLs')
    return data['references']


def references_panel(citations, registry, *, disclosure=True):
    seen, rows = set(), []
    for citation in citations:
        key, locator = citation['key'], citation.get('locator', '')
        if (key, locator) in seen:
            continue
        seen.add((key, locator))
        record = registry.get(key) or citation
        text = record.get('text') or key
        url = record.get('url')
        label = html.escape(text)
        if url and safe_link(url):
            label = '<a href="' + html.escape(url, quote=True) + '" rel="noopener noreferrer">' + label + '</a>'
        rows.append('<li id="reference-' + html.escape(key, quote=True) + '" data-reference-id="' + html.escape(key, quote=True) + '">' + label +
                    (' <span class="reference-locator">' + html.escape(locator) + '</span>' if locator else '') + '</li>')
    body = '<ol>' + ''.join(rows) + '</ol>' if rows else '<p>No references have been attached to this statement yet.</p>'
    if not disclosure:
        return '<section class="statement-references" id="references"><h2>References</h2>' + body + '<p class="reference-directory"><a href="/explore/references/">Shared bibliography</a></p></section>'
    return '<details class="explorer-disclosure statement-references"><summary>References' + (' (' + str(len(rows)) + ')' if rows else '') + '</summary><div class="explorer-disclosure-body">' + body + '<p><a href="/explore/references/">Shared bibliography</a></p></div></details>'
