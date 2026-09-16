"""Assess the COMPLETE hex-column conjunction and its alternatives on synthetic single-column TEXT tables, under
UTF-8, UTF-16le and UTF-16be, for the four hex shapes (64 hex; op- + 32; run3: + 64; exec1_ + 32).

Candidates: v3/root (typeof + character length + TEXT instr NUL + prefix + hex), v2 (byte length instead of instr),
BLOB instr instead of TEXT instr, TEXT instr with typeof only, and each v3 conjunct removed in turn. Hostile inputs are
the retained v2 hex variants plus the encoding-specific ones of p01. A candidate is exact in an encoding when it has no
hole (admitted value outside the grammar) and no over-refusal (lawful value refused). Reference evidence only.
"""
import hashlib, json, re, sqlite3
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
V2SPEC = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/probes/p01b_storage_matrix.py')
src = (BASE / 'probes/p01_encoding_matrix.py').read_text()
ns = {'re': re}
spec_src = V2SPEC.read_text()
exec(compile(spec_src[spec_src.index('A64, B64, C64, E64'):spec_src.index('def db(table, encoding=None):')], 'v2-p01b-spec', 'exec'), ns)
T, TB, hostile_hex, hexlaw = ns['T'], ns['TB'], ns['hostile_hex'], ns['hexlaw']
exec(compile(src[src.index('ENCODINGS = ('):src.index("spec_src = V2SPEC.read_text()")], 'p01-encodings', 'exec'), ns)
exec(compile(src[src.index('def extra_hex(lawful, enc):'):src.index('def insert(table, base, column, expr, encoding):')], 'p01-extra', 'exec'), ns)
ENCODINGS, CODEC, extra_hex = ns['ENCODINGS'], ns['CODEC'], ns['extra_hex']
SHAPES = [('hex64', '', 64, 'b' * 64), ('op-ref', 'op-', 32, 'op-' + 'a' * 32), ('run3', 'run3:', 64, 'run3:' + 'c' * 64),
          ('exec1', 'exec1_', 32, 'exec1_' + 'a' * 32)]


def terms(prefix, n):
    total, p = len(prefix) + n, len(prefix)
    t = {'typeof': "typeof(x) = 'text'", 'length': 'length(x) = %d' % total, 'instr': 'instr(x, char(0)) = 0',
         'bytelength': 'length(CAST(x AS BLOB)) = %d' % total, 'blobinstr': "instr(CAST(x AS BLOB), x'00') = 0",
         'hex': ("substr(x, %d) NOT GLOB '*[^0-9a-f]*'" % (p + 1)) if prefix else "x NOT GLOB '*[^0-9a-f]*'"}
    if prefix:
        t['prefix'] = "x GLOB '%s*'" % prefix
    return t


CANDIDATES = {
    'v3-root-alternative': ['typeof', 'length', 'instr', 'prefix', 'hex'],
    'v2-byte-length': ['typeof', 'length', 'bytelength', 'prefix', 'hex'],
    'blob-instr-instead-of-text-instr': ['typeof', 'length', 'blobinstr', 'prefix', 'hex'],
    'text-instr-with-typeof-only': ['typeof', 'instr'],
    'v3-minus-typeof': ['length', 'instr', 'prefix', 'hex'],
    'v3-minus-length': ['typeof', 'instr', 'prefix', 'hex'],
    'v3-minus-instr': ['typeof', 'length', 'prefix', 'hex'],
    'v3-minus-hex': ['typeof', 'length', 'instr', 'prefix'],
    'v3-minus-prefix': ['typeof', 'length', 'instr', 'hex'],
}


def attempt(check, expr, value, enc):
    c = sqlite3.connect(':memory:', isolation_level=None)
    try:
        c.execute("PRAGMA encoding = '%s'" % enc)
        c.execute('CREATE TABLE t (x TEXT NOT NULL CHECK (%s))' % check)
        observed = c.execute('PRAGMA encoding').fetchone()[0]
        try:
            c.execute('INSERT INTO t VALUES (%s)' % expr, (value,))
        except sqlite3.DatabaseError:
            return None, observed
        t, b = c.execute('SELECT typeof(x), CAST(x AS BLOB) FROM t').fetchone()
        if t == 'blob':
            u = b
        elif t == 'null':
            u = None
        else:
            try:
                u = b.decode(CODEC[observed]).encode('utf-8')
            except UnicodeDecodeError:
                u = b'\xff<undecodable>'
        return (t, u), observed
    finally:
        c.close()


results = {}
for cand, parts in CANDIDATES.items():
    results[cand] = {}
    for enc in ENCODINGS:
        holes, over = [], []
        for shape, prefix, n, lawful in SHAPES:
            tm = terms(prefix, n)
            check = ' AND '.join(tm[p] for p in parts if p in tm)
            law = hexlaw(prefix, n, False)
            got, observed = attempt(check, '?', lawful, enc)
            if got is None or not law(*got) or observed != enc:
                over.append(shape + ' lawful')
            for label, (expr, value) in hostile_hex(prefix, lawful) + extra_hex(lawful, enc) + [('null', ('?', None))]:
                got, _ = attempt(check, expr, value, enc)
                if got is not None and not law(*got):
                    holes.append('%s %s (%s)' % (shape, label, got[0]))
        results[cand][enc] = {'holes': holes, 'overRefusals': over, 'exact': not holes and not over}
verdict = {cand: all(r['exact'] for r in by.values()) for cand, by in results.items()}
record = {'sqliteVersion': sqlite3.sqlite_version, 'probeInputs': {'v2SpecSha256': hashlib.sha256(V2SPEC.read_bytes()).hexdigest()},
          'exactInAllThreeEncodings': verdict,
          'exactPerEncoding': {cand: {enc: r['exact'] for enc, r in by.items()} for cand, by in results.items()},
          'results': results}
(BASE / 'receipts' / 'p01b-conjunction-ablation.json').write_text(json.dumps(record, indent=1) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'results'}, indent=1))
print(json.dumps({cand: {enc: {'holesFirst6': r['holes'][:6], 'overRefusals': r['overRefusals']} for enc, r in by.items()}
                  for cand, by in results.items()}, indent=1)[-9000:])
expected = {'v3-root-alternative': True}
if not verdict['v3-root-alternative'] or any(verdict[c] for c in CANDIDATES if c.startswith('v3-minus') and c != 'v3-minus-prefix'):
    raise SystemExit(1)
