"""Shared reviewer harness: load the frozen fixture builders WITHOUT running the authored suite.

Loads check-identity.py source only up to the end of graph_with_import (the last builder
definition), so none of the authored check() assertions execute. Passing authored tests is
not acceptance; this harness exists so the reviewer can drive the builders directly.

Loaded from the reviewer's own verified disposable copy, never the frozen subject in place,
so no shipped report can be overwritten (the v4 in-tree overwrite incident).
"""
import ast, hashlib, json
from pathlib import Path

COPY = Path('/tmp/opensip-design-corrections/post-reset-review.v9/work/copy')
SUBJECT = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
FOUND = COPY / 'docs/coop/design-corrections/foundation'


def load(verify=True):
    fixture = FOUND / 'check-identity.py'
    src = fixture.read_text()
    if verify:
        # the copy must be byte-identical to the frozen subject
        a = hashlib.sha256(fixture.read_bytes()).hexdigest()
        b = hashlib.sha256((SUBJECT / 'docs/coop/design-corrections/foundation/check-identity.py').read_bytes()).hexdigest()
        assert a == b, ('copy drifted from frozen subject', a, b)
    tree = ast.parse(src)
    last = next(n for n in tree.body
                if isinstance(n, ast.FunctionDef) and n.name == 'graph_with_import').end_lineno
    ns = {'__file__': str(fixture), '__name__': 'reviewer_v9_fixture'}
    exec(compile('\n'.join(src.split('\n')[:last]), str(fixture), 'exec'), ns)
    ns['_fixtureSha256'] = hashlib.sha256(fixture.read_bytes()).hexdigest()
    ns['_truncatedAtLine'] = last
    return ns


def custody(paths):
    out = {}
    for p in paths:
        f = SUBJECT / p
        b = f.read_bytes()
        out[p] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    return out
