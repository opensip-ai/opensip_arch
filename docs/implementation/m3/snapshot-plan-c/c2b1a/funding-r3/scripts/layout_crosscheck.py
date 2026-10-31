#!/usr/bin/env python3
"""Cross-check on the native owner: a Python port of C2b-0's layout record admission price
(host node_modules_layout.rs `admission_cost`, :292-520 at the pin, which prices
`SchemaHandle::admit_json` of ResolvedNodeModulesLayoutV1 over `push_record`'s bytes) compared
with the generic ADMIT term on the same records. Consistency only, not a soundness proof."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:2]
from admission_model import *  # noqa: F401,F403

# r2: the model's primitives return split prices; the ports below use their totals.
import admission_model as _M
def _t(f): return lambda *a: f(*a).total()
for _n in ('search', 'pss', 'owned', 'growth', 'formatted', 'p_string', 'p_entry', 'p_value', 'p_search',
           'p_insert', 'p_array', 'btree_insert', 'digest_cost'):
    globals()[_n] = _t(getattr(_M, _n))
import json as _json
nbytes = lambda s: len(s.encode('utf-8'))
canon = lambda x: _json.dumps(x, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode('utf-8')

SEL = '/$defs/ResolvedNodeModulesLayoutV1'


def payload_len(t):
    return sum(2 if c in '"\\\b\f\n\r\t' else 6 if ord(c) < 0x20 else len(c.encode()) for c in t)


def row_length(r):
    return 152 + sum(payload_len(r[k]) for k in ('installPath', 'packageName', 'packageVersion', 'realPath'))


def record_parse_cost(length, rows):
    total = p_entry(length) + p_value() * (3 + 6 * len(rows))
    for members, key in enumerate(['entries', 'schemaVersion']):
        total = total + p_string(len(key)) + p_search(members, len(key)) + p_insert(members, len(key))
    total = total + p_array(len(rows))
    for r in rows:
        fields = [('contentSha256', 64), ('installPath', nbytes(r['installPath'])), ('packageName', nbytes(r['packageName'])),
                  ('packageVersion', nbytes(r['packageVersion'])), ('realPath', nbytes(r['realPath']))]
        for members, (key, value) in enumerate(fields):
            total = total + p_string(len(key)) + p_string(value) + p_search(members, len(key)) + p_insert(members, len(key))
    return total


def admission_search_cost(rows):
    entry = len(NATIVE) + 1 + len(SEL)
    ec = tree_search(POPULATION)
    total = C(0, ec, ec * entry * 2)
    rc = tree_search(len(rows))
    for i, r in enumerate(rows):
        total = total + C(0, rc, rc * row_length(r) * 2)
        if i:
            total = total + C(0, 4, 2 * nbytes(r['installPath']))
    return total


def pattern_dispatch():
    owner_bytes = 3 * len(NATIVE) + 31
    path_bytes = (3 * 54 + 123) + (2 * 54 + 108)
    digest_bytes = (12 * 23 + 733) + (2 * 23 + 108) + (23 + 15) + (23 + 57) + (23 * 23 + 1431)
    edges = 3 * 2 + 2 * ((3 + 2) + (32 + 6)) + (12 + 2 + 2 + 23) + (32 + 2 * (12 + 23))
    return C(0, edges, 3 * owner_bytes + 2 * path_bytes + digest_bytes)


def evaluation_cost(length, rows):
    c = map_search
    fixed_maps = 18 * c(5) + 15 * c(6) + 11 * c(1) + c(1) + 4 * c(2) + 2
    row_maps = 24 * c(4) + 12 * (c(3) + c(3) + c(1) + c(4) + c(1) + c(4) + c(2) + c(2)) + c(6) + 10 * c(5) + c(5) + 20
    rcmp = c(D) + c(10) + c(115)
    doc_bytes = 2 * c(D) * len(NATIVE)
    root_bytes = 2 * c(10) * len('$defs')
    initial = doc_bytes + root_bytes + 2 * c(115) * len('ResolvedNodeModulesLayoutV1') + 84 + 4 * len(SEL)
    path_r = doc_bytes + root_bytes + 2 * c(115) * len('CanonicalPath') + 21 + 4 * 20
    digest_r = doc_bytes + root_bytes + 2 * c(115) * len('DigestHex') + 17 + 4 * 16
    total = C(0, fixed_maps + rcmp + 5, 40 * fixed_maps + initial + 2 * (49 + 34 + 32) + 24 + length * 32)
    for r in rows:
        pat = pattern_dispatch()
        scans = (nbytes(r['installPath']) + nbytes(r['realPath']) + nbytes(r['packageName']) + nbytes(r['packageVersion']) + 64) * 2
        preds = (nbytes(r['installPath']) + nbytes(r['realPath'])) * 16
        total = total + C(0, row_maps + 3 * rcmp + pat[1] + 6,
                          40 * row_maps + 2 * path_r + digest_r + pat[2] + 72 + 256 + scans + preds)
    return total


def admission_cost(length, rows):
    total = record_parse_cost(length, rows) + C(0, 64 + 128 * len(rows), 0)
    for b in [5, 27, STRING, 8, 11]:
        o = owned(b)
        total = total + C(o[0], 0, o[2])
    for r in rows:
        for b in [5, 13, 5, 13, 5, 9, VEC_SLOT + row_length(r), STR_SLOT]:
            o = owned(b)
            total = total + C(o[0], 0, o[2])
    return total + admission_search_cost(rows) + evaluation_cost(length, rows)


def layout(n, install=lambda i: f'node_modules/p{i:05d}', real=None):
    rows = [{'contentSha256': 'f' * 64, 'installPath': install(i), 'packageName': f'p{i:05d}',
             'packageVersion': '1.0.0', 'realPath': (real or install)(i)} for i in range(n)]
    rows.sort(key=lambda r: r['installPath'].encode())
    return {'entries': rows, 'schemaVersion': 1}


if __name__ == '__main__':
    cases = {'empty': layout(0), 'one': layout(1), '100': layout(100),
             '1000 long': layout(1000, lambda i: 'node_modules/' + f'{i:05d}' + 'x' * 4000),
             '300 escaped': layout(300, lambda i: f'node_modules/q{i:04d}\u0001\t\"é')}
    for name, rec in cases.items():
        raw = canon(rec)
        assert len(raw) == 32 + max(len(rec['entries']) - 1, 0) + sum(row_length(r) for r in rec['entries'])
        ours = _M.ADMIT(_M.Record(rec, NATIVE, SEL)).total()
        theirs = admission_cost(len(raw), rec['entries'])
        print(f'{name:12} generic {tuple(ours)}  C2b-0 {tuple(theirs)}  generic/C2b-0',
              tuple(round(a / b, 3) if b else None for a, b in zip(ours, theirs)))
