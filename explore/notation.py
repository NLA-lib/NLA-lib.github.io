"""Source-level math diagnostics. Never infer symbol roles from letter case."""
import json
import re
from pathlib import Path
from markdown_it import MarkdownIt

CONFIG = Path(__file__).with_name('notation.json')

def policy():
    return json.loads(CONFIG.read_text())['documents']

def math_spans(text):
    """Math islands and delimiter errors, excluding Markdown code and escaped dollars."""
    offsets=[0]
    for line in text.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
    excluded=[]
    for token in MarkdownIt('commonmark').parse(text):
        if token.type in {'fence','code_block'}:excluded.append((offsets[token.map[0]],offsets[token.map[1]]))
    for match in re.finditer(r'(`+)([\s\S]*?)\1',text):
        if not any(a<=match.start()<b for a,b in excluded):excluded.append(match.span())
    def escaped(index):
        count=0
        while index>0 and text[index-1]=='\\':count+=1;index-=1
        return count%2==1
    spans,issues=[],[];index=0
    while index<len(text):
        blocked=next((b for a,b in excluded if a<=index<b),None)
        if blocked is not None:index=blocked;continue
        opener=next((value for value in ['$$',r'\[',r'\(', '$'] if text.startswith(value,index) and not escaped(index)),None)
        if not opener:index+=1;continue
        closer={r'\[':r'\]',r'\(':r'\)'}.get(opener,opener)
        end=index+len(opener)
        while True:
            end=text.find(closer,end)
            if end<0:break
            if escaped(end) or any(a<=end<b for a,b in excluded):end+=len(closer);continue
            if opener=='$' and '\n' in text[index:end]:end=-1
            break
        if end<0:
            issues.append({'severity':'error','code':'math-delimiter','line':text.count('\n',0,index)+1,'message':'Unclosed '+opener+' math delimiter.'});index+=len(opener);continue
        finish=end+len(closer)
        spans.append((index,finish,text[index+len(opener):end],opener in {'$$',r'\['}))
        index=finish
    return spans,issues

TOKEN = re.compile(r'\\[a-zA-Z]+|[a-zA-Z]|[{}]')

def diagnostics(text, roles=None):
    spans,issues=math_spans(text);roles=roles or {}
    symbols=set(roles.get('vectors',[])+roles.get('matrices',[]))
    for start,end,tex,display in spans:
        line=text.count('\n',0,start)+1
        def issue(code,message,severity='error',position=0):
            issues.append({'severity':severity,'code':code,'line':line+tex.count('\n',0,position),'message':message})
        balance=0
        for match in re.finditer(r'(?<!\\)[{}]',tex):
            balance+=1 if match[0]=='{' else -1
            if balance<0:break
        if balance:issue('math-braces','Unbalanced braces in LaTeX.')
        # These are style suggestions because T or H can also be scalar exponents.
        for match in re.finditer(r'\^\s*(?:\{\s*[TH]\s*\}|[TH]|\\top|\{\\top\}|\{\\mathrm\{[TH]\}\})',tex):
            letter='H' if 'H' in match[0] else 'T'
            issue('transpose-style','Use ^{\\mathsf{'+letter+'}} for '+('Hermitian transpose.' if letter=='H' else 'transpose.'),'warning',match.start())
        # A declared vector/matrix is required to be explicitly bold. Commands,
        # text/operator names, and subscripts such as x in A_x stay untouched.
        tokens=list(TOKEN.finditer(tex));stack=[];pending=None
        for token in tokens:
            value=token[0]
            if value.startswith('\\'):
                pending=value if value in {r'\mathbf',r'\boldsymbol',r'\text',r'\operatorname',r'\mathrm',r'\mathsf',r'\mathbb',r'\mathcal'} else None
                continue
            if value=='{':stack.append(pending or (stack[-1] if stack else None));pending=None;continue
            if value=='}':
                if stack:stack.pop()
                pending=None;continue
            font=pending or (stack[-1] if stack else None);pending=None
            if value in symbols and font not in {r'\mathbf',r'\boldsymbol',r'\text',r'\operatorname',r'\mathrm',r'\mathsf',r'\mathbb',r'\mathcal'}:
                issue('symbol-weight',value+' is declared as a vector/matrix; write \\mathbf{'+value+'}.',position=token.start())
    return issues

def normalize(text,roles=None):
    """Explicit migration helper for reviewed documents; never used while rendering."""
    spans,_=math_spans(text);symbols=set((roles or {}).get('vectors',[])+(roles or {}).get('matrices',[]))
    for start,end,tex,display in reversed(spans):
        tex=re.sub(r'\\(mathbf|mathsf|boldsymbol)\s+([A-Za-z])',lambda m:'\\'+m[1]+'{'+m[2]+'}',tex)
        # Preserve explicit fonts and whole command names while bolding declared symbols.
        parts=[];cursor=0;tokens=list(TOKEN.finditer(tex));stack=[];pending=None
        for token in tokens:
            parts.append(tex[cursor:token.start()]);value=token[0]
            if value.startswith('\\'):pending=value if value in {r'\mathbf',r'\boldsymbol',r'\text',r'\operatorname',r'\mathrm',r'\mathsf',r'\mathbb',r'\mathcal'} else None
            elif value=='{':stack.append(pending or (stack[-1] if stack else None));pending=None
            elif value=='}':
                if stack:stack.pop()
                pending=None
            else:
                font=pending or (stack[-1] if stack else None);pending=None
                if value in symbols and font is None:value=r'\mathbf{'+value+'}'
            parts.append(value);cursor=token.end()
        parts.append(tex[cursor:]);tex=''.join(parts)
        opener=text[start:start+2] if text.startswith(('$$',r'\[',r'\('),start) else '$'
        closer={r'\[':r'\]',r'\(':r'\)'}.get(opener,opener)
        text=text[:start]+opener+tex+closer+text[end:]
    return text
