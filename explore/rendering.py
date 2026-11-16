"""Safe prose, titles, and path components shared by the Markdown explorer."""
import html
import re
from urllib.parse import quote

def record_component(key):
    """One physical path component; URL quoting adds the HTTP encoding separately."""
    component = str(key).replace('%', '%25').replace('/', '%2F').replace('\\', '%5C')
    return component.replace('.', '%2E') if component in {'.', '..'} else component


NOTES = re.compile(r'(?:\A|\n[ \t]*\n)(?=Note:)')
TAG_LINE = re.compile(r'\s*(?:Result|Algorithm|Asymptotic):')


def split_notes(text):
    """`(statement, notes)` of a docstring. The notes block starts at the first paragraph whose
    first line starts with the literal `Note:` and runs to the end, except for the tag lines
    (`Result:`, `Algorithm:`, `Asymptotic:`), which stay with the statement. The statement is the
    docstring without the notes block; a docstring without one is returned unchanged."""
    text = text or ''
    match = NOTES.search(text)
    if not match:
        return text, ''
    notes, tags = [], []
    for line in text[match.end():].split('\n'):
        (tags if TAG_LINE.match(line) else notes).append(line)
    statement = text[:match.start()].rstrip()
    if tags:
        statement += ('\n\n' if statement else '') + '\n'.join(tags)
    return statement, '\n'.join(notes).strip()


def notes_html(notes, render):
    """The secondary, collapsed block for a docstring's notes; nothing without notes. Its body is
    not an `explorer-disclosure-body`, so statement links stay with the Lean details."""
    if not notes:
        return ''
    return ('<details class="explorer-disclosure explorer-notes"><summary>Notes</summary><div class="explorer-notes-body">' +
            render(re.sub(r'\ANote:\s*', '', notes)) + '</div></details>')


def badge(label, tip='', kind=''):
    return ('<span class="explorer-badge' + (' explorer-badge-' + kind if kind else '') + '"' +
            (' title="' + html.escape(tip, quote=True) + '"' if tip else '') + '>' + html.escape(label) + '</span>')


INDEX_SIZES_LABEL = 'General form: sizes are index types'
INDEX_SIZES_TIP = ('A size is carried by a finite index type: |k| is the number of elements of the index type k, '
                   'and "k nonempty" means k ≥ 1.')


def inline_title(text):
    """Titles share the same safe math/code markup in headings and links."""
    parts = re.split(r'(\$\$.*?\$\$|\$[^$\n]+\$|`[^`]+`)', text)
    return ''.join('<span class="math">' + html.escape(p.strip('$')) + '</span>' if p.startswith('$')
                   else '<code>' + html.escape(p[1:-1]) + '</code>' if p.startswith('`')
                   else html.escape(p) for p in parts)


PROSE_SPAN = re.compile(r'(`+)(.+?)\1|\$\$(.+?)\$\$|\$([^$\n]+?)\$', re.S)
LEAN_NAME = re.compile(r"^[A-Za-z_][\w'.]*$")


def prose_html(text, names=(), missing=None):
    """Render safe prose, code, and TeX; recognized names link to the library."""
    def inline(src):
        slots = []

        def keep(markup):
            slots.append(markup)
            return f'\x00{len(slots) - 1}\x00'

        def lift(m):
            if m[2] is not None:
                code = m[2].strip()
                full = code if code in names else 'NLAlib.' + code if 'NLAlib.' + code in names else None
                if full:
                    return keep(f'<a href="/explore/library/declarations/{quote(record_component(full), safe=".")}/"><code>{html.escape(code)}</code></a>')
                if missing is not None and LEAN_NAME.match(code):
                    missing.append(code)
                return keep(f'<code>{html.escape(code)}</code>')
            if m[3] is not None:
                return keep(f'<span class="math display">{html.escape(m[3].strip(), quote=False)}</span>')
            return keep(f'<span class="math">{html.escape(m[4], quote=False)}</span>')

        s = html.escape(PROSE_SPAN.sub(lift, src), quote=False)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<![*\w])\*([^*\s](?:[^*]*[^*\s])?)\*(?!\*)', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
                   lambda m: f'<a href="{m[2].replace(chr(34), "&quot;")}">{m[1]}</a>', s)
        return re.sub(r'\x00(\d+)\x00', lambda m: slots[int(m[1])], s)

    fences = []

    def fence(m):
        fences.append(m[1])
        return f'\n\n\x01{len(fences) - 1}\x01\n\n'

    text = re.sub(r'^```[^\n]*\n(.*?)\n?^```[ \t]*$', fence, text.replace('\r', ''), flags=re.S | re.M)
    out = []
    for block in re.split(r'\n[ \t]*\n', text.strip()):
        if not block.strip():
            continue
        code = re.fullmatch(r'\s*\x01(\d+)\x01\s*', block)
        if code:
            out.append(f'<pre class="lean">{html.escape(fences[int(code[1])], quote=False)}</pre>')
            continue
        lines = block.split('\n')
        head = re.match(r'(#{1,4})\s+(.*)$', lines[0])
        if head:
            tag = f'h{len(head[1]) + 1}'
            out.append(f'<{tag}>{inline(head[2])}</{tag}>')
            lines = lines[1:]
            if not lines:
                continue
        bullet = r'\s*-\s+' if re.match(r'\s*-\s+', lines[0]) else r'\s*\d+\.\s+'
        if re.match(bullet, lines[0]):
            items = []
            for line in lines:
                if re.match(bullet, line):
                    items.append(re.sub('^' + bullet, '', line))
                else:
                    items[-1] += ' ' + line.strip()
            tag = 'ul' if '-' in bullet else 'ol'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(t)}</li>' for t in items) + f'</{tag}>')
            continue
        para = ' '.join(line.strip() for line in lines)
        display = re.fullmatch(r'\$\$((?:(?!\$\$).)+)\$\$', para, re.S)
        if display:
            out.append(f'<div class="math display">{html.escape(display[1].strip(), quote=False)}</div>')
        else:
            out.append(f'<p>{inline(para)}</p>')
    return '\n'.join(out)
