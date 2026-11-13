"""Safe prose, titles, and path components shared by the Markdown explorer."""
import html
import re
from urllib.parse import quote

def record_component(key):
    """One physical path component; URL quoting adds the HTTP encoding separately."""
    component = str(key).replace('%', '%25').replace('/', '%2F').replace('\\', '%5C')
    return component.replace('.', '%2E') if component in {'.', '..'} else component


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
