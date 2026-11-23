"""Arithmetic and execution-model facts of a declaration, one detector per fact.

A fact is reported only when its detector establishes it from one of three sources: a named
hypothesis of the declaration's own Lean signature, the library's certificate record
(`scripts/ops_certificates.txt`, written and compared by `scripts/OpsPrograms.lean`), or an
`ops` field of the extraction. No detector reads names, docstrings or tags, and none infers a
fact from a definition it would have to unfold. A declaration without a fact carries no badge:
absence says nothing about its model.
"""
import hashlib
from pathlib import Path
import re
import sys

CERTIFICATES = 'scripts/ops_certificates.txt'
ALGORITHM = 'NLAlib.Ops.Algorithm'
FLAGS = ('uniform', 'confined', 'charged')
BOUNDS = ('budget', 'work', 'scratch')
PROBLEM_FIELDS = ('problem', 'derived', 'unstored', 'oracles', 'claim')
OPENERS, CLOSERS = '([{⦃', ')]}⦄'

# facet -> value -> (badge label, explanation). The explanation says what was detected.
FACTS = {
    'arithmetic': {
        'exact': ('Exact arithmetic',
                  'The statement assumes exact arithmetic: a scalar machine whose operations return the '
                  'exact values (Ops.ExactModel), or the exact scheme of a standard operation model.'),
        'standard': ('Standard rounding',
                     'The statement assumes the standard model of rounded arithmetic with unit roundoff u '
                     '(Ops.StdModel): every scalar operation has relative error at most u, with no overflow '
                     'or underflow. A standard operation model (Ops.Standard.Model) fixes such a machine.'),
        'relative-error': ('Relative-error BLAS',
                           'The statement assumes level-1 vector operations that meet relative error '
                           'coefficients supplied by the caller (Ops.IsBlas1), not a reduction order.'),
    },
    'access': {
        'uniform': ('Uniform model',
                    'The operation model is uniform (Ops.AccessModel.Uniform): no primitive contract '
                    'depends on the sizes or on the input, so no primitive is an oracle for the problem '
                    'data. A uniform model can still call kernels with their own contracts and weights.'),
        'oracle': ('Oracle: matrix–vector product',
                   'A matrix–vector product is a primitive with a contract for a given operator '
                   '(Ops.IsMatvec, Ops.IsExactMatvec, the operator of an Ops.Standard.Model, or an operator '
                   'group reported by the extraction): the operator is semantic data of the model, not '
                   'entries that the program reads.'),
        'kernel': ('Kernel primitives',
                   'The extraction reports primitives of the operation model that are kernels: '
                   'operations specified by a contract, with work supplied by the caller.'),
    },
    'randomness': {
        'tape-law': ('Random tape',
                     'The statement assumes a law of the tape of draws (Ops.IsTapeLaw): independent '
                     'entries, each stream with a given distribution.'),
        'sampling': ('Sampling primitive',
                     'The extraction reports that the certified program calls a sampling operation '
                     '(Ops.SampleOp), which reads the tape of draws.'),
    },
    'work': {
        'closed': ('Work: closed',
                   'The work and span bounds of this certificate do not mention the static count of a '
                   'program (the check scripts/OpsPrograms.lean of the library). A closed bound can '
                   'still be a parameter that a hypothesis of the certificate constrains.'),
        'manifest': ('Work: program manifest',
                     'The library records the work or span bound of this certificate as stated through '
                     'the static count of its own program. Its check keeps the record from overstating '
                     'a certificate, so a bound closed since then can still be recorded as manifest.'),
    },
}
FACETS = {'arithmetic': 'Arithmetic', 'access': 'Access', 'randomness': 'Randomness', 'work': 'Work'}

# What the program of a model is built from. Together with the arithmetic labels above this is
# the whole vocabulary of model names: implementation pages, badges and search filters share it.
PROGRAMS = {
    'blas-matvec': 'BLAS + matvec',
    'relative-blas-matvec': 'relative-error BLAS + matvec',
    'relative-blas': 'relative-error BLAS',
    'stored-scalar': 'stored scalar',
}


def model_title(arithmetic, program=None):
    """The name of a model of an implementation page: the arithmetic label and, where the page
    needs it to tell its models apart, what the program is built from, after a middle dot."""
    return FACTS['arithmetic'][arithmetic][0] + (' · ' + PROGRAMS[program] if program else '')


def binders(signature):
    """The types of the named explicit binders `(names : type)` of a pretty-printed signature, in
    order, each on one line. Binders in other brackets, anonymous binders and the conclusion
    after the top-level colon are left out."""
    text = signature or ''
    found, depth, start = [], 0, None
    for index, char in enumerate(text):
        if char in OPENERS:
            if depth == 0:
                start = index
            depth += 1
        elif char in CLOSERS and depth:
            depth -= 1
            if depth == 0 and text[start] == '(':
                names, colon, kind = ' '.join(text[start + 1:index].split()).partition(' : ')
                if colon and re.fullmatch(r"[\w'✝ ]+", names):
                    found.append(kind)
        elif char == ':' and depth == 0:
            break
    return found


def assumes(signature, dependencies, name):
    """Whether the signature has a hypothesis `(h : name …)`. The printed head may omit leading
    namespaces, so `name` must also be a statement dependency and the only one with that ending."""
    if name not in dependencies:
        return False
    for kind in binders(signature):
        head = kind.split(' ', 1)[0]
        if (name == head or name.endswith('.' + head)) and not any(
                other != name and (other == head or other.endswith('.' + head)) for other in dependencies):
            return True
    return False


def exact_scheme(signature, dependencies):
    """Whether a hypothesis fixes the scheme of a standard operation model to the exact one:
    `(h : model.scheme = Ops.Standard.Scheme.exact)`."""
    return 'NLAlib.Ops.Standard.Scheme' in dependencies and any(
        re.fullmatch(r"[\w'.]+\.scheme = (?:NLAlib\.)?Ops\.Standard\.Scheme\.exact", kind) for kind in binders(signature))


def exact_arithmetic(signature, dependencies):
    """A hypothesis `Ops.ExactModel dec M`, or the exact scheme of a standard operation model."""
    return assumes(signature, dependencies, 'NLAlib.Ops.ExactModel') or exact_scheme(signature, dependencies)


def standard_model(signature, dependencies):
    """A hypothesis `Ops.StdModel u dec M`, or a standard operation model `Ops.Standard.Model`,
    whose machine satisfies `StdModel` at the roundoff of its scheme. The exact scheme is reported
    by `exact_arithmetic` instead."""
    return (assumes(signature, dependencies, 'NLAlib.Ops.StdModel') or
            assumes(signature, dependencies, 'NLAlib.Ops.Standard.Model') and not exact_scheme(signature, dependencies))


def relative_error_blas(signature, dependencies):
    """A hypothesis `Ops.IsBlas1 dec ε ok J`: level-1 operations at supplied error coefficients."""
    return assumes(signature, dependencies, 'NLAlib.Ops.IsBlas1')


def matvec_primitive(signature, dependencies):
    """A hypothesis `Ops.IsMatvec dec A δ I` or `Ops.IsExactMatvec dec A I`, the contract of a
    matrix–vector primitive for the operator `A`, or a standard operation model, whose signature
    has that primitive for the operator supplied with the input."""
    return any(assumes(signature, dependencies, name) for name in
               ['NLAlib.Ops.IsMatvec', 'NLAlib.Ops.IsExactMatvec', 'NLAlib.Ops.Standard.Model'])


def tape_law(signature, dependencies):
    """A hypothesis `Ops.IsTapeLaw law P ξ`: the statement is about a random tape."""
    return assumes(signature, dependencies, 'NLAlib.Ops.IsTapeLaw')


def parse_certificates(text):
    """`{name: line}` of `scripts/ops_certificates.txt`. A line is `name hyps=N uniform=yes|no
    confined=yes|no charged=yes|no budget=closed|manifest work=… scratch=…`, optionally followed
    by all of `problem=derived|handwritten derived=N|?|- unstored=yes|no|- oracles=… claim=…`,
    which are validated and not used; anything else is an error, so a record in another format
    is not read as this one."""
    lines = {}
    for raw in text.splitlines():
        if not raw.strip():
            continue
        name, *fields = raw.split()
        values = dict(field.split('=', 1) for field in fields if '=' in field)
        base = {'hyps', *FLAGS, *BOUNDS}
        if (len(values) != len(fields) or set(values) not in (base, base | set(PROBLEM_FIELDS)) or name in lines
                or not values['hyps'].isdigit() or any(values[key] not in {'yes', 'no'} for key in FLAGS)
                or any(values[key] not in {'closed', 'manifest'} for key in BOUNDS)
                or ('problem' in values and (values['problem'] not in {'derived', 'handwritten'}
                                             or not re.fullmatch(r'\d+|\?|-', values['derived'])
                                             or values['unstored'] not in {'yes', 'no', '-'}
                                             or not values['oracles'] or not values['claim']))):
            raise ValueError('unrecognized certificate line: ' + raw)
        lines[name] = {'hyps': int(values['hyps']), **{key: values[key] == 'yes' for key in FLAGS},
                       **{key: values[key] for key in BOUNDS}}
    return lines


def load_certificates(source, declarations):
    """The certificate record of a verified source snapshot, as `(lines, provenance)`. The record
    is used only when it parses and every listed name is a definition of the extraction whose type
    mentions `Ops.Algorithm`; otherwise it has another format or describes another snapshot, and
    no line is used."""
    path = Path(source) / CERTIFICATES if source else None
    if not path or not path.is_file():
        return {}, None
    raw = path.read_bytes()
    provenance = {'path': CERTIFICATES, 'sha256': hashlib.sha256(raw).hexdigest(), 'used': False, 'certificates': 0}
    try:
        lines = parse_certificates(raw.decode())
    except ValueError as error:
        print(f'warning: {CERTIFICATES}: {error}; its flags are not used', file=sys.stderr)
        return {}, provenance
    foreign = sorted(name for name in lines if name not in declarations or declarations[name]['kind'] == 'theorem'
                     or ALGORITHM not in declarations[name].get('typeDeps', []))
    if foreign:
        print(f'warning: {CERTIFICATES} lists {len(foreign)} names that are not certificates of this extraction '
              f'({foreign[0]}, …); its flags are not used', file=sys.stderr)
        return {}, provenance
    provenance.update(used=True, certificates=len(lines))
    return lines, provenance


def certificate(original, recorded=None):
    """The certificate line of a declaration: the `ops` field of the extraction when it has one
    (computed with the declaration), else the line of the certificate record. `None` for a
    declaration that is not a certificate."""
    ops = original.get('ops')
    if isinstance(ops, dict) and all(isinstance(ops.get(key), bool) for key in FLAGS) and all(
            ops.get(key) in {'closed', 'manifest'} for key in BOUNDS):
        return {'hyps': ops.get('hyps'), **{key: ops[key] for key in FLAGS + BOUNDS}, 'source': 'extraction'}
    if recorded:
        return {**recorded, 'source': CERTIFICATES}
    return None


def work_bound(line):
    """`closed` or `manifest` for a certificate; nothing for any other declaration."""
    return line['work'] if line else None


def uniform_model(line):
    """Whether an `Ops.AccessModel.Uniform` instance is recorded for the certificate's model. A
    missing instance is not reported: it does not establish an oracle."""
    return bool(line and line['uniform'])


def reported_arithmetic(ops):
    """`ops.arithmetic` of the extraction: `exact` or `standard` for the certificate's model."""
    return ops.get('arithmetic') if ops.get('arithmetic') in {'exact', 'standard'} else None


def reported_oracle(ops):
    """`ops.oracle` of the extraction: the model has an operator applied as a primitive."""
    return ops.get('oracle') is True


def reported_kernels(ops):
    """`ops.kernels` of the extraction: the names of the kernel operation types of the model."""
    kernels = ops.get('kernels')
    return kernels if isinstance(kernels, list) and kernels and all(isinstance(k, str) for k in kernels) else []


def reported_sampling(ops):
    """`ops.sampling` of the extraction: the certified program calls a sampling operation."""
    return ops.get('sampling') is True


def facts(original, recorded=None):
    """`(facts, certificate line)` of an extracted declaration. A fact is `{facet, value,
    evidence}`; `evidence` names what established it."""
    signature, dependencies = original.get('signature') or '', original.get('typeDeps', [])
    ops = original.get('ops') if isinstance(original.get('ops'), dict) else {}
    line = certificate(original, recorded)
    found = []

    def add(facet, value, evidence):
        if not any(f['facet'] == facet and f['value'] == value for f in found):
            found.append({'facet': facet, 'value': value, 'evidence': evidence})

    if exact_arithmetic(signature, dependencies):
        add('arithmetic', 'exact', 'signature hypothesis')
    if standard_model(signature, dependencies):
        add('arithmetic', 'standard', 'signature hypothesis')
    if relative_error_blas(signature, dependencies):
        add('arithmetic', 'relative-error', 'signature hypothesis')
    if reported_arithmetic(ops) and not any(f['facet'] == 'arithmetic' for f in found):
        add('arithmetic', reported_arithmetic(ops), 'extraction')
    if uniform_model(line):
        add('access', 'uniform', line['source'])
    if matvec_primitive(signature, dependencies):
        add('access', 'oracle', 'signature hypothesis')
    if reported_oracle(ops):
        add('access', 'oracle', 'extraction')
    if reported_kernels(ops):
        add('access', 'kernel', 'extraction')
    if tape_law(signature, dependencies):
        add('randomness', 'tape-law', 'signature hypothesis')
    if reported_sampling(ops):
        add('randomness', 'sampling', 'extraction')
    if work_bound(line):
        add('work', work_bound(line), line['source'])
    return found, line


def tags(model_facts):
    """Search tags `facet:value` of a list of facts."""
    return [fact['facet'] + ':' + fact['value'] for fact in model_facts or []]
