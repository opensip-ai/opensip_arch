#!/usr/bin/env python3
"""Cross-check: a Python port of C9's `descriptor_admission_cost` (host snapshot_admission.rs at the
pin) reproduces C9's four published vectors (snapshot_admission_tests.rs
`the_admission_price_is_its_formula`); the generic term (admission_model.FROM_JSON) is then
compared with C9 on concrete snapshot descriptors. This is a consistency check of the generic
model, not a soundness proof of either."""
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

ROOT_KEYS, DEFS, QUERY = 7, 54, 20
DOCUMENT, SELECTOR = IDENTITY, '/$defs/snapshot'
ENTRY_LEN = len(DOCUMENT) + 1 + len(SELECTOR)
TOP_KEYS = ['projectId', 'resolvedConfigDigest', 'schemaVersion', 'scopeDigest', 'sourceInventory', 'vcsDigest']
ROW_KEYS = ['bytes', 'path', 'sha256']
LOGICAL_PATH, DOT_SEGMENT, HEX64, PROJECT_ID = (26, 1608, 53), (1, 19, 15), (22, 1431, 23), (50, 2449, 28)
OWNER_LENS = [31, 49, 37, 34]
ROW_COMPARISONS = [(1, 45), (3, 29), (4, 17), (6, 13)]
FIXED_COMPARISONS = [(1, 38), (2, 12), (3, 36), (4, 20), (6, 27)]
IDENT_LEN = len('snapshot2') + 1 + 64
FRAME_FIXED = len('opensip.product.v1\0') + len('snapshot') + 1 + 8


def growths(count, total, size):
    if count == 0:
        return Z
    minimum = 8 if size == 1 else 4
    mean = max(-(-total // count), 1)
    ev = count * (3 + log2(mean))
    return C(ev, ev, (total * 6 + count * 3 * minimum) * size + ev * RECORD)


def parsed_strings(count, total):
    if count == 0:
        return Z
    mean = max(-(-total // count), 1)
    ev = count * (3 + log2(mean))
    return C(ev, ev, total * 8 + count * 32)


def affine(f, count, keys):
    zero, one = f(0), f(1)
    return zero * count + C(*(max(b - a, 0) * keys for a, b in zip(zero, one)))


def dispatch9(row):
    index, through, pattern = row
    owners = sum(len(DOCUMENT) + o for o in OWNER_LENS)
    return pss(len(OWNER_LENS) + index + 1, owners + through + (index + 1) * pattern)


def resolve9(length, name):
    a = Z
    p = pss(1, length) + search(D, len(DOCUMENT)) + pss(2, 2 * length)
    for part, members in [(len('$defs'), ROOT_KEYS), (name, DEFS)]:
        a = a + p_string(part)
        p = p + pss(1, part) + search(members, part)
    return a, p


def lookup9():
    entries = tree_search(POPULATION)
    mem = pss(entries, entries * 2 * (ENTRY_LEN + 1))
    a = formatted(len(SELECTOR)) + formatted(ENTRY_LEN) + owned(len(SELECTOR))
    p = (pss(1, len(SELECTOR)) + pss(1, 2 * (len(DOCUMENT) + 1)) + pss(D, D * 2 * (len(DOCUMENT) + 1))
         + pss(1, ENTRY_LEN) + mem + pss(1, len(SELECTOR)) + mem)
    return a, p


def parse9(s):
    n = s['rows']
    total = p_entry(s['length']) + p_value() * (7 + 4 * n)
    for members, key in enumerate(TOP_KEYS):
        total = total + p_string(len(key)) + p_search(members, len(key)) + p_insert(members, len(key))
    for value in s['top']:
        total = total + p_string(value)
    total = total + p_array(n)
    for members, key in enumerate(ROW_KEYS):
        total = total + (p_string(len(key)) + p_search(members, len(key)) + p_insert(members, len(key))) * n
    return total + p_string(64) * n + parsed_strings(n, s['paths'])


def row_walks(s):
    keys = sum(map(len, ROW_KEYS))
    return pss(4 * s['rows'], s['rows'] * (keys + 64) + s['paths'])


def walk9(s):
    return pss(3, sum(map(len, TOP_KEYS)) + sum(s['top'])) + pss(4, 0) + row_walks(s)


def lookups(table):
    return sum((search(m, QUERY) * c for m, c in table), Z)


def order_check(s):
    n = s['rows']
    a = owned(4) + owned(STRING) + owned(4 * STR_SLOT) * n
    p = pss(ORDER_ARMS, ORDER_ARMS * 2 * (ORDER_ARM + 1)) + search(3, 4) * n + pss(n, 2 * (s['paths'] + n))
    return a, p


def evaluation9(s):
    n, P, S = s['rows'], s['paths'], s['segments']
    project, config, scope, vcs = s['top']
    a = Z
    p = pss(9, 0) + pss(7, 0) * n + lookups(FIXED_COMPARISONS) + lookups(ROW_COMPARISONS) * n
    for length, name in [(ENTRY_LEN, len('snapshot')), (17, 9), (24, 16)]:
        ra, rp = resolve9(length, name)
        a, p = a + ra, p + rp
    for length, name in [(12, 4), (19, 11)]:
        ra, rp = resolve9(length, name)
        a, p = a + ra * n, p + rp * n
    p = p + pss(5, 2 * project + config + scope + vcs) + pss(4 * n, 3 * P) + pss(0, 64 * n)
    p = p + pss(1, 16) * (6 + 4 * n) + pss(12 + 11 * n, 0)
    p = (p + dispatch9(PROJECT_ID) + pss(1, project + 5) + dispatch9(HEX64) + pss(1, config)
         + dispatch9(HEX64) + pss(1, scope) + dispatch9(HEX64) + pss(1, vcs)
         + (dispatch9(LOGICAL_PATH) + dispatch9(DOT_SEGMENT) + dispatch9(HEX64)) * n
         + pss(n + 2 * S, 3 * P) + pss(S, P + 6 * S + 2 * n) + pss(n, 64 * n) + pss(3, 2))
    rows = s['encoded_rows']
    a = a + growths(n, rows, 1) + growth(20, 1) * n
    ins = affine(lambda key: btree_insert(n, key, VEC_SLOT), n, rows)
    a = a + C(ins[0], 0, ins[2])
    p = p + row_walks(s) + pss(4 * n, 2 * rows) + pss(ins[1], 0)
    p = p + row_walks(s) + pss(2, 4)
    oa, op = order_check(s)
    return a + oa, p + op


def ordered9(s):
    n, P, S = s['rows'], s['paths'], s['segments']
    paths = pss(n + S, 2 * P + 12 * S)
    oa, op = order_check(s)
    a = owned(4) + oa
    p = (pss(6 + 12, 24 * (QUERY + 1)) + pss(ORDER_ARMS, ORDER_ARMS * 2 * (ORDER_ARM + 1))
         + search(3, 4) * n + paths + op + pss(n + 9 * n, n * 6 * 2 * 7) + paths)
    return a, p


def hash9(s):
    n, L = s['rows'], s['length']
    F = FRAME_FIXED + L
    a = growth(L, 1) + growth(20, 1) * (n + 1) + growth(F, 1)
    p = pss(1, len('snapshot')) + pss(7 + 4 * n, 2 * L) + pss(1, F + L) + digest_cost(F)
    return a, p


def identifier9():
    return owned(64) + formatted(IDENT_LEN), pss(32, 96) + pss(1, 2 * IDENT_LEN)


def c9(s):
    a, p = parse9(s), walk9(s)
    for pa, pp in [lookup9(), evaluation9(s), ordered9(s), hash9(s), identifier9()]:
        a, p = a + pa, p + pp
    return a + p


PUBLISHED = [((0, 0, 0, 0, 404), (171, 2104, 169857)), ((1, 1, 1, 98, 502), (248, 2991, 228095)),
             ((3, 27, 4, 312, 718), (411, 4812, 356391)),
             ((100_000, 3_000_000, 400_000, 4_000_000, 4_000_000), (9400213, 109502146, 8445542509))]


def shape(rows, paths, segs, enc, length):
    return dict(top=[69, 64, 64, 64], rows=rows, paths=paths, segments=segs, encoded_rows=enc, length=length)


def snapshot(rows):
    return {'projectId': 'prj1-' + 'a' * 64, 'resolvedConfigDigest': 'b' * 64, 'schemaVersion': 1,
            'scopeDigest': 'c' * 64, 'vcsDigest': 'd' * 64,
            'sourceInventory': [{'bytes': b, 'path': p, 'sha256': 'e' * 64} for p, b in rows]}


if __name__ == '__main__':
    for args, expect in PUBLISHED:
        got = tuple(c9(shape(*args)))
        print('C9 port', args, got, 'published', expect, 'OK' if got == expect else 'MISMATCH')
        assert got == expect
    cases = {
        'empty': [],
        'one-row': [('a', 0)],
        'three-rows': [('a/b', 7), ('c/d/e/f', 18446744073709551615), ('g', 2)],
        '200 longest paths': [('/'.join([f'{i:03d}' + 'x' * 252] + ['x' * 255] * 14 + ['y' * 254, 'z']), 1) for i in range(200)],
        '300 escaped': [(f'd\u0001\"q{i:04d}/é中\U0001F600\t', i) for i in range(300)],
        '2000 short': [(f'f{i:05d}', i) for i in range(2000)],
    }
    for name, rows in cases.items():
        rows = sorted(rows, key=lambda r: r[0].encode())
        snap = snapshot(rows)
        s = c9_shape(snap); s['length'] = _M.Record(snap, IDENTITY, '/$defs/snapshot').st.L
        ours = _M.FROM_JSON('snapshot', _M.Record(snap, IDENTITY, '/$defs/snapshot', identity=True)).total()
        theirs = c9(s)
        ratio = tuple(round(a / b, 3) if b else None for a, b in zip(ours, theirs))
        print(f'{name:18} generic {tuple(ours)}  C9 {tuple(theirs)}  generic/C9 {ratio}')
