"""Small shared BibTeX reader; preserve complete source entries for editing/export."""
import html
import re
from urllib.parse import urlsplit

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327", "v": "\u030c"}

def tex_accents(s):
    """`in{\\'e}galit{\\'e}`, `\\"o`, `\\c{c}` -> the accented letters."""
    import unicodedata
    s = re.sub(r'\\([\'`^"~]|[cv](?=[{ ]))\s*\{?(\w)\}?', lambda m: unicodedata.normalize(
        'NFC', m.group(2) + ACCENTS[m.group(1)]), s)
    for cmd, ch in (('AA', 'Å'), ('aa', 'å'), ('ss', 'ß'), ('o', 'ø'), ('O', 'Ø'), ('l', 'ł')):
        s = re.sub(r'\\' + cmd + r'(?![a-zA-Z])\s?', ch, s)
    return s.replace('--', '–')


def _braced(text, start):
    depth=0
    for i in range(start,len(text)):
        if text[i]=='{' and (i==0 or text[i-1]!='\\'):depth+=1
        elif text[i]=='}' and (i==0 or text[i-1]!='\\'):
            depth-=1
            if depth==0:return text[start+1:i],i+1
    raise ValueError('Unclosed braces in BibTeX')


def parse_bib_text(source):
    records={};position=0
    pattern=re.compile(r'(?m)^[ \t]*@(\w+)\s*\{\s*([A-Za-z][A-Za-z0-9_-]*)\s*,')
    while True:
        match=pattern.search(source,position)
        if not match:break
        kind,key=match.groups();start=source.index('{',match.start())
        body,end=_braced(source,start);position=end
        if key in records:raise ValueError('Duplicate citation key: '+key)
        body=body[body.index(',')+1:];fields={};i=0
        while i<len(body):
            while i<len(body) and (body[i].isspace() or body[i]==','):i+=1
            if i==len(body):break
            if body[i]=='%':
                newline=body.find('\n',i);i=len(body) if newline<0 else newline+1;continue
            field=re.match(r'([A-Za-z][A-Za-z0-9_-]*)\s*=\s*',body[i:])
            if not field:raise ValueError('Expected a BibTeX field such as title = {Title}')
            name=field[1].lower();i+=field.end()
            if i>=len(body):raise ValueError('Missing BibTeX field value')
            if body[i]=='{':value,i=_braced(body,i)
            elif body[i]=='"':
                begin=i+1;i=begin
                while i<len(body) and (body[i]!='"' or body[i-1]=='\\'):i+=1
                if i==len(body):raise ValueError('Unclosed quoted BibTeX field')
                value=body[begin:i];i+=1
            else:
                begin=i
                while i<len(body) and body[i]!=',':i+=1
                value=body[begin:i].strip()
                if not re.fullmatch(r'[A-Za-z0-9_-]+',value):raise ValueError('Use braced or quoted BibTeX field values')
            if name in fields:raise ValueError('Duplicate BibTeX field: '+name)
            normalized=tex_accents(' '.join(value.split()))
            fields[name]=''.join(part if part.startswith('$') else re.sub(r'[{}]','',part) for part in re.split(r'(\$[^$]*\$)',normalized))
        authors=[a.strip() for a in fields.get('author','').split(' and ') if a.strip()]
        names=[]
        for author in authors:
            if ',' in author:
                last,first=[x.strip() for x in author.split(',',1)];names.append(first+' '+last)
            else:names.append(author)
        who=', '.join(names[:-1])+(' and ' if len(names)>1 else '')+(names[-1] if names else '')
        venue=fields.get('journal') or fields.get('booktitle') or fields.get('publisher') or ''
        if fields.get('series') and kind.lower()=='book':venue=(fields['series']+' '+fields.get('volume','')).strip()+(', '+fields['publisher'] if fields.get('publisher') else '')
        year=fields.get('year','');display_year='' if year and venue.endswith(year) else year
        text=f"{who}. {fields.get('title','')}. {venue}{', ' if venue and display_year else ''}{display_year}."
        url=fields.get('url') or ('https://doi.org/'+fields['doi'] if fields.get('doi') else 'https://arxiv.org/abs/'+fields['eprint'] if fields.get('eprint') else None)
        publication={name:fields.get(name,'') for name in ('publisher','journal','booktitle','volume','number','pages','edition','institution','school')}
        records[key]={'text':' '.join(text.split()).replace(' .','.'),'url':url,'title':fields.get('title',''),'authors':names,
            'year':year,'doi':fields.get('doi'),'arxiv':fields.get('eprint'),**publication,'entry_type':kind.lower(),'bibtex':source[match.start():end].strip()+'\n'}
    return records


def one_reference(source, expected_key=None):
    if not isinstance(source,str) or len(source.encode())>120000 or '\x00' in source:raise ValueError('BibTeX must be at most 120 KB')
    records=parse_bib_text(source)
    if len(records)!=1:raise ValueError('Provide exactly one BibTeX entry')
    key,record=next(iter(records.items()))
    if len(key)>120:raise ValueError('Citation keys must be at most 120 characters')
    if expected_key is not None and key!=expected_key:raise ValueError('Keep the citation key '+expected_key+' unchanged so existing citations keep working')
    # Reject trailing or leading content except comments/whitespace.
    residual=source.replace(record['bibtex'].strip(),'',1)
    if re.sub(r'(?m)%[^\n]*','',residual).strip():raise ValueError('Only one BibTeX entry and comments are allowed')
    if not record['title'].strip():raise ValueError('A BibTeX title field is required')
    if record.get('url'):
        url=urlsplit(record['url'])
        if url.scheme!='https' or not url.hostname or url.username or url.password or any(c.isspace() for c in record['url']):raise ValueError('Reference URLs must be HTTPS without credentials')
    return key,record


def citation_parts(record):
    def escape(value):return html.escape(str(value or ''))
    def safe_url(value):
        try:parsed=urlsplit(value or '')
        except ValueError:return False
        return parsed.scheme=='https' and bool(parsed.hostname) and not parsed.username and not parsed.password and not any(c.isspace() for c in value)
    def link(label,url):
        return '<a href="'+html.escape(url,quote=True)+'" rel="noopener noreferrer">'+label+'</a>' if safe_url(url) else label
    if not record.get('title'):
        return '<span class="reference-text">'+escape(record.get('text',''))+'</span>'
    authors=record.get('authors',[])
    who=', '.join(authors[:-1])+(' and ' if len(authors)>1 else '')+(authors[-1] if authors else '')
    output=('<span class="reference-authors">'+escape(who)+'.</span> ') if who else ''
    def title_markup(value):
        return ''.join('<span class="math">'+escape(part[1:-1])+'</span>' if part.startswith('$') and part.endswith('$') else escape(part) for part in re.split(r'(\$[^$]+\$)',value))
    title=link(title_markup(record['title'].rstrip('.')),record.get('url'))
    tag='cite' if record.get('entry_type') in {'book','proceedings','manual','phdthesis','mastersthesis','techreport'} else 'span'
    output+='<'+tag+' class="reference-title">'+title+'.</'+tag+'> '
    venue=[]
    if record.get('journal'):venue.append('<cite class="reference-journal">'+escape(record['journal'])+'</cite>')
    elif record.get('booktitle'):venue.append('In <cite>'+escape(record['booktitle'])+'</cite>')
    if record.get('volume'):venue.append('<strong class="reference-volume">'+escape(record['volume'])+'</strong>'+(' ('+escape(record['number'])+')' if record.get('number') else ''))
    if record.get('pages'):venue.append('pp. '+escape(record['pages']))
    if record.get('edition'):
        edition=str(record['edition'])
        if edition.isdigit():
            n=int(edition);edition+=('th' if n%100 in {11,12,13} else {1:'st',2:'nd',3:'rd'}.get(n%10,'th'))
        venue.append(escape(edition)+' ed.')
    publisher=record.get('publisher') or record.get('institution') or record.get('school')
    if publisher:venue.append('<span class="reference-publisher">'+escape(publisher)+'</span>')
    if record.get('year'):venue.append('<span class="reference-year">'+escape(record['year'])+'</span>')
    if venue:output+='<span class="reference-publication">'+', '.join(venue)+'.</span>'
    identifiers=[]
    if record.get('doi'):identifiers.append(link('DOI: '+escape(record['doi']),'https://doi.org/'+record['doi']))
    if record.get('arxiv'):identifiers.append(link('arXiv:'+escape(record['arxiv']),'https://arxiv.org/abs/'+record['arxiv']))
    if identifiers:output+=' <span class="reference-identifiers">'+' · '.join(identifiers)+'</span>'
    return output


def citation_html(record):
    return '<p class="reference-preview">'+citation_parts(record)+'</p>'
