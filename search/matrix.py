"""Matrix declaration search: BM25, local embeddings, and optional Lean checking.

Run with python -m search.matrix --help. Retrieval scores are never proof certificates.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import threading
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
MODEL = 'BAAI/bge-small-en-v1.5'
INDEX_FORMAT = 'matrix-search-v1'
STOP = set('a an and are as at be by for from if in is it of on or that the this to with '
           'any every all each where which when its their than theorem lemma show prove'.split())
IDENT = re.compile(r'[\w\u2080-\u209f]+(?:\.[\w\u2080-\u209f]+)*', re.UNICODE)


def tokens(text):
    text = re.sub(r'<!--.*?-->', ' ', text or '', flags=re.S)
    text = re.sub(r'\\(?:mathbf|mathsf|mathbb|mathrm|operatorname|left|right)\b', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text).lower()
    return [w for w in re.findall(r'[^\W_]+', text) if len(w) > 1 and w not in STOP]


def conclusion(signature):
    """Find the outer type separator, not colons inside parameter binders."""
    depth = 0
    for i, c in enumerate(signature):
        if c in '([{⦃':
            depth += 1
        elif c in ')]}⦄':
            depth -= 1
        elif c == ':' and depth == 0:
            return signature[i + 1:].strip()
    return signature.strip()


def shape(text):
    """A retrieval heuristic only: ignore short variable spellings, retain repetition.

    This is deliberately NOT a Lean parser or an alpha-equivalence certificate.
    """
    names = {}
    def replace(m):
        word = m.group()
        if word.isdecimal() or word in {'ℝ', 'ℂ', 'ℕ', 'ℤ', 'ℚ', '𝕜'}:
            return word
        if len(word) == 1 or re.fullmatch(r'[A-Za-zα-ωΑ-Ω][₀-₉0-9′\']*', word):
            return names.setdefault(word, f'var{len(names)}')
        return word
    return re.sub(r'\s+', '', IDENT.sub(replace, text))


class Index:
    def __init__(self, data, cache=ROOT / '.search-cache', semantic=True, download_model=False):
        self.path = Path(data)
        raw = self.path.read_bytes()
        self.fingerprint = hashlib.sha256(raw).hexdigest()
        source = json.loads(raw)
        if source.get('schema') != 1 or not re.fullmatch(r'[a-f0-9]{40}', source.get('commit', '')):
            raise ValueError('Expected schema 1 explorer data with a full commit hash')
        self.commit = source['commit']
        # Include matrix-related upstream helpers; exclude scaffolds and admitted declarations.
        self.decls = [d for d in source['decls'] if not d.get('sorry') and (
            d['module'].startswith('NLAlib.Matrix.') or
            d['module'].startswith('NLAlib.ForMathlib.') and 'Matrix' in d['module'].split('.'))
            and not d['name'].endswith(('_def', '_eq_1'))]
        self.docs = [self.document(d) for d in self.decls]
        self.counts = [Counter(tokens(x)) for x in self.docs]
        self.lengths = [sum(x.values()) for x in self.counts]
        self.avg_length = sum(self.lengths) / max(len(self.lengths), 1)
        self.df = Counter(t for c in self.counts for t in c)
        self.shapes = [shape(conclusion(d.get('signature', ''))) for d in self.decls]
        self.cache = Path(cache)
        self.download_model = download_model
        self.model = None
        self.vectors = None
        self.lock = threading.Lock()
        if semantic:
            self.load_embeddings()

    @staticmethod
    def document(d):
        # Put the informative natural-language text first: the model truncates at 512 tokens.
        return f"{d['name']}\n{d.get('doc') or ''}\n{d.get('signature') or d.get('statement', '')}"

    def load_embeddings(self):
        import numpy as np
        from fastembed import TextEmbedding
        self.cache.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha256((self.fingerprint + MODEL + INDEX_FORMAT + '\n'.join(self.docs))
                             .encode()).hexdigest()
        self.model = TextEmbedding(model_name=MODEL, cache_dir=str(self.cache / 'models'), threads=2,
                                   local_files_only=not self.download_model)
        path = self.cache / f'{key}.npz'
        if path.exists():
            with np.load(path, allow_pickle=False) as a:
                self.vectors = a['vectors']
            if self.vectors.shape != (len(self.decls), 384) or not np.isfinite(self.vectors).all():
                raise ValueError('Invalid embedding-cache dimensions')
        else:
            self.vectors = np.asarray(list(self.model.embed(self.docs, batch_size=32)), dtype=np.float32)
            np.savez_compressed(path, vectors=self.vectors)
        self.vectors /= np.maximum(np.linalg.norm(self.vectors, axis=1, keepdims=True), 1e-12)

    def lexical(self, query):
        scores = [0.] * len(self.decls)
        for t in set(tokens(query)):
            df = self.df[t]
            if not df:
                continue
            idf = math.log(1 + (len(self.decls) - df + .5) / (df + .5))
            for i, c in enumerate(self.counts):
                tf = c[t]
                if tf:
                    scores[i] += idf * tf * 2.2 / (tf + 1.2 * (.25 + .75 * self.lengths[i] / self.avg_length))
        return scores

    def search(self, query, limit=10, mode='hybrid'):
        if not query.strip() or limit < 1:
            return []
        if mode not in ('hybrid', 'lexical', 'semantic'):
            raise ValueError('Unknown retrieval mode')
        if mode != 'lexical' and self.model is None:
            raise ValueError('Semantic/hybrid search requires embeddings; use --lexical-only with --mode lexical')
        lex = self.lexical(query)
        sem = None
        if mode != 'lexical':
            import numpy as np
            with self.lock:
                v = np.asarray(list(self.model.query_embed(query))[0], dtype=np.float32)
            sem = self.vectors @ (v / max(np.linalg.norm(v), 1e-12))
        score = [0.] * len(lex)
        channels = []
        if mode != 'semantic':
            channels.append(('lexical', lex))
        if sem is not None:
            channels.append(('semantic', sem))
        reasons = [[] for _ in lex]
        for label, values in channels:
            order = sorted(range(len(values)), key=lambda i: (-float(values[i]), self.decls[i]['name']))
            for rank, i in enumerate(order[:100], 1):
                if label == 'lexical' and values[i] <= 0:
                    continue
                score[i] += 1 / (20 + rank)
                if rank <= 20:
                    reasons[i].append(f'{label} rank {rank}')
        qshape = shape(query)
        for i, d in enumerate(self.decls):
            if query.strip() == d['name']:
                score[i] += 1
                reasons[i].append('exact declaration name')
            if qshape and qshape == self.shapes[i]:
                score[i] += .15
                reasons[i].append('variable-insensitive text shape (unverified)')
        out = []
        for i in sorted(range(len(score)), key=lambda i: (-score[i], self.decls[i]['name'])):
            if score[i] <= 0:
                continue
            d = self.decls[i]
            out.append({**d, 'score': score[i], 'reasons': reasons[i], 'verification': 'not checked',
                        'commit': self.commit,
                        'source': f"https://github.com/NLA-lib/NLAlib/blob/{self.commit}/"
                                  f"{d['module'].replace('.', '/')}.lean#L{d['line']}"})
            if len(out) >= limit:
                break
        return out


def check_candidate(repo, candidate, goal, context='', timeout=45):
    """Check trusted user-supplied Lean code; never run from the HTTP endpoint.

    A successful result proves the goal with the restricted candidate/local assumptions.
    It does not establish source freshness; this is reported explicitly.
    """
    name, module = candidate['name'], candidate['module']
    if not re.fullmatch(r"[\w.\u2080-\u209f']+", name) or not re.fullmatch(r'[\w.]+', module):
        raise ValueError('Invalid declaration or module name')
    forbidden = r'\b(sorry|admit|axiom|unsafe|partial|native_decide|set_option|import|example|theorem|def|run_cmd|elab)\b'
    if re.search(forbidden, context + '\n' + goal):
        return {'status': 'invalid input', 'detail': 'Use theorem parameter binders and a goal expression only'}
    src = f'''import {module}
set_option autoImplicit false
set_option maxHeartbeats 200000
-- Generated checking code: applying a candidate can close all goals immediately.
set_option linter.unreachableTactic false
set_option linter.unusedTactic false
theorem matrixSearchVerified {context} : {goal} := by
  apply {name}
  all_goals solve_by_elim (maxDepth := 3) (symm := false) (exfalso := false) only [*]
#print axioms matrixSearchVerified
'''
    p = subprocess.Popen(['lake', 'env', 'lean', '--stdin', '--json', '-M', '8000', '-j', '1'],
                         cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True, env={**os.environ, 'LEAN_NUM_THREADS': '1'})
    try:
        stdout, stderr = p.communicate(src, timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        p.communicate()
        return {'status': 'timeout', 'seconds': timeout}
    diagnostics = []
    for line in stdout.splitlines():
        try:
            diagnostics.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    messages = '\n'.join(str(d.get('data', '')) for d in diagnostics)
    axiom_match = re.search(r"'matrixSearchVerified' depends on axioms: \[([^\]]*)\]", messages)
    no_axioms = "'matrixSearchVerified' does not depend on any axioms" in messages
    axioms = set(x.strip() for x in axiom_match[1].split(',') if x.strip()) if axiom_match else set()
    clean = not any(d.get('severity') in ('error', 'warning') for d in diagnostics)
    checked = p.returncode == 0 and clean and (axiom_match or no_axioms) and axioms <= {
        'propext', 'Classical.choice', 'Quot.sound'}
    return {'status': 'checked against local build' if checked else 'not established',
            'freshness': 'not verified; local compiled modules may differ from the search snapshot',
            'axioms': sorted(axioms),
            'detail': (stdout + stderr)[-6000:], 'proof': src if checked else None}


def evaluate(index, cases):
    if not cases:
        raise ValueError('The benchmark must contain at least one query')
    names = {d['name'] for d in index.decls}
    for case in cases:
        if not case['expected'] or not set(case['expected']) <= names:
            raise ValueError(f"Unknown expected declaration in {case['id']}")
    report = {'commit': index.commit, 'source_sha256': index.fingerprint,
              'index_format': INDEX_FORMAT, 'model': MODEL if index.model else None,
              'declarations': len(index.decls), 'queries': len(cases), 'modes': {}}
    for mode in (('lexical',) if index.model is None else ('lexical', 'semantic', 'hybrid')):
        rows = []
        for c in cases:
            hits = index.search(c['query'], 100, mode)
            rank = next((i for i, h in enumerate(hits, 1) if h['name'] in c['expected']), None)
            rows.append({'id': c['id'], 'rank': rank, 'query': c['query'],
                         'top': [h['name'] for h in hits[:5]]})
        report['modes'][mode] = {'hit_at_5': sum(r['rank'] is not None and r['rank'] <= 5 for r in rows) / len(rows),
                                 'hit_at_10': sum(r['rank'] is not None and r['rank'] <= 10 for r in rows) / len(rows),
                                 'mrr_at_100': sum(1 / r['rank'] for r in rows if r['rank']) / len(rows),
                                 'results': rows}
    return report


def serve(index, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == '/':
                body = (ROOT / 'search' / 'index.html').read_bytes()
                mime = 'text/html; charset=utf-8'
            elif parsed.path == '/api/search':
                args = parse_qs(parsed.query)
                q = args.get('q', [''])[0][:2000]
                try:
                    hits = index.search(q, mode=args.get('mode', ['hybrid'])[0])
                    body = json.dumps({'commit': index.commit, 'hits': hits}).encode()
                except ValueError as e:
                    self.send_error(400, str(e))
                    return
                mime = 'application/json; charset=utf-8'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
    server = HTTPServer(('127.0.0.1', port), Handler)
    print(f'Matrix search: http://127.0.0.1:{port} ({len(index.decls)} declarations, {index.commit[:8]})', flush=True)
    server.serve_forever()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--cache', type=Path, default=ROOT / '.search-cache')
    p.add_argument('--lexical-only', action='store_true')
    p.add_argument('--download-model', action='store_true', help='Allow initial public model download')
    p.add_argument('--mode', choices=['lexical', 'semantic', 'hybrid'], default='hybrid')
    p.add_argument('--query')
    p.add_argument('--limit', type=int, default=10)
    p.add_argument('--evaluate', type=Path)
    p.add_argument('--serve', type=int, metavar='PORT')
    p.add_argument('--lean-repo', type=Path)
    p.add_argument('--goal', help='Trusted Lean goal expression, checked against each retrieved candidate')
    p.add_argument('--context', default='', help='Trusted Lean theorem parameter binders, including hypotheses')
    a = p.parse_args()
    index = Index(a.data, a.cache, not a.lexical_only, a.download_model)
    if a.evaluate:
        print(json.dumps(evaluate(index, json.loads(a.evaluate.read_text())), indent=2))
    elif a.serve:
        serve(index, a.serve)
    else:
        if not a.query:
            p.error('Provide --query, --evaluate or --serve')
        hits = index.search(a.query, a.limit, a.mode)
        if a.goal:
            if not a.lean_repo:
                p.error('--goal requires --lean-repo')
            for h in hits:
                h['verification'] = check_candidate(a.lean_repo, h, a.goal, a.context)
        print(json.dumps({'commit': index.commit, 'hits': hits}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
