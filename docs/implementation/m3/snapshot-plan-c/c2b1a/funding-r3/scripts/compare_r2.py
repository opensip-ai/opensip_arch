#!/usr/bin/env python3
"""Regression: the r3 census (explicit measured boundary) against the preserved r2 census
(scripts/r2/) on every well-formed scenario record. r3 changes no term's price: it changes where
the census charges and counts (RF-1), the depth gate (NBO-1) and adds the retained-length lookup
to the census. So every term's allocation side, pass side and total must be EQUAL to r2's."""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = sys.argv[:2]
import vectors as V3
spec = importlib.util.spec_from_file_location('m2', os.path.join(HERE, 'r2', 'admission_model.py'))
M2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(M2)
M3 = V3


def terms_with(M, r, is_r3):
    R = M.Record
    tool = R(r['tool'], M.IDENTITY, '/$defs/closure', identity=True)
    std = R(r['stdlib'], M.IDENTITY, '/$defs/closure', identity=True)
    out = {
        'T-CLOSURE tool': M.T_CLOSURE('closure2:' + 'c' * 64, tool, 3),
        'T-CLOSURE stdlib': M.T_CLOSURE('closure2:' + 'b' * 64, std, 3),
        'T-FRAME-CTX': M.T_FRAME('native.context.typescript.v2', 'native-context', R(r['context'], M.NATIVE, V3.CTX), 400),
        'T-FRAME-UNI': M.T_FRAME('native.semantic-universe.typescript.v2', 'native-semantic-universe', R(r['universe'], M.NATIVE, V3.UNI), 400),
        'T-REC-GRAPH': M.T_RECORD('#' + V3.GRAPH, R(r['graph'], M.NATIVE, V3.GRAPH), 400),
    }
    if r['layout']:
        out['T-REC-LAYOUT'] = M.T_RECORD('#' + V3.LAYOUT, R(r['layout'], M.NATIVE, V3.LAYOUT), 400)
    return {k: (tuple(v.alloc), tuple(v.passes), tuple(v.total())) for k, v in out.items()}


ok, n = True, 0
for name, r, _ in V3.SCENARIOS:
    a, b = terms_with(M2, r, False), terms_with(M3, r, True)
    for k in a:
        eq = a[k] == b[k]
        ok &= eq; n += 1
        print(f'{name:22} {k:17} r2 total {a[k][2]}  r3 total {b[k][2]}  alloc/pass/total equal {eq}')
print(f'ALL {n} terms r3 == r2 (allocation side, pass side, total):', ok)
assert ok
