"""Byte-safe exact storage-class and whole-value grammar matrix (argv[1] = frozen37 | v1final | edited; argv[2] == 'strict'
exits 1 on any hole or over-refusal).

p01 crashed on frozen37: its first-character GLOB admitted an invalid-UTF-8 TEXT value that Python could not decode
on read-back. That receipt is retained. This probe reads back typeof(column) and CAST(column AS BLOB) and applies
the oracle to raw bytes, so no admitted value can crash the observation.

Oracle, per column: an ADMITTED row must STORE the lawful storage class with a value satisfying the column law over
its whole byte string; every canonical lawful value must be ADMITTED.
"""
import json, re, sqlite3, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
COPY = sys.argv[1]
STRICT = len(sys.argv) > 2 and sys.argv[2] == 'strict'
SRC = BASE / 'work' / COPY
DDL = (SRC / 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql').read_text()
AC = json.loads((SRC / 'docs/v2/architecture/attempt-custody.schema.v1.json').read_text())['proposedPrivateDDL']
V2 = (BASE / 'work/frozen37/docs/coop/completion/security-schemas.v2/grant-journal.sql').read_text()

A64, B64, C64, E64 = 'a' * 64, 'b' * 64, 'c' * 64, 'e' * 64
OP, RUN, EXEC = 'op-' + 'a' * 32, 'run3:' + 'c' * 64, 'exec1_' + 'a' * 32


def hexlaw(prefix, n, nullable):
    pat = re.compile(re.escape(prefix).encode() + b'[0-9a-f]{%d}' % n)
    return lambda t, b: (t == 'null' and nullable) or (t == 'text' and pat.fullmatch(b) is not None)


def intlaw(pred, nullable=False):
    return lambda t, b: (t == 'null' and nullable) or (t == 'integer' and pred(int(b)))


def enumlaw(values, nullable=False):
    enc = {v.encode() for v in values}
    return lambda t, b: (t == 'null' and nullable) or (t == 'text' and b in enc)


def textlaw(nullable):
    return lambda t, b: (t == 'null' and nullable) or t == 'text'


FRESH = {'singleton': 1, 'carrier_format': 3, 'project_key_digest': E64, 'first_generation': 1, 'chain_law': 1,
         'migrated_from': None, 'migration_op_ref': None}
MIGRATED = dict(FRESH, first_generation=2, migrated_from=2, migration_op_ref='op-' + 'f' * 32)
SEAL = {'grantGeneration': 1, 'seq': 1, 'record_schema': 3, 'record_type': 'SEAL', 'operation_ref': OP, 'request_ref': None,
        'token': None, 'install_generation_id': None, 'manifest_digest': None, 'platform': None, 'run_id': RUN,
        'body': '{}', 'body_sha256': B64, 'prev_sha256': B64}
REV = dict(SEAL, record_type='REV', run_id=None)
GRANT = dict(SEAL, record_type='GRANT', run_id=None, token='PT', install_generation_id='ig1', manifest_digest=C64,
             platform='macos-x86_64')
ADMITTED = {'store_generation_digest': A64, 'namespace_id': 'ns', 'execution_id': EXEC, 'operation_ref': OP,
            'record_schema': 1, 'phase': 'admitted', 'settled_outcome': None}
SETTLED = dict(ADMITTED, phase='settled', settled_outcome='refused')


def T(v):
    return ('?', v)


def TB(b):
    return ('CAST(? AS TEXT)', b)


def hostile_hex(prefix, lawful):
    n, mid, p = len(lawful), len(lawful) // 2, len(prefix)
    rows = [('uppercase-last', T(lawful[:-1] + 'A')), ('nonhex-last', T(lawful[:-1] + 'g')),
            ('nonhex-tail', T(lawful[:p + 1] + 'Z' * (n - p - 1))),
            ('nul-suffix-Z', T(lawful + '\x00Z')), ('nul-suffix', T(lawful + '\x00')),
            ('nul-middle-same-chars', T(lawful[:mid] + '\x00' + lawful[mid + 1:])),
            ('ascii-hex-blob', T(lawful.encode())), ('ascii-hex-blob-nul-suffix', T(lawful.encode() + b'\x00Z')),
            ('nonhex-blob', T(b'Z' * n)), ('invalid-utf8-text-same-bytes', TB(lawful[:-1].encode() + b'\xc0')),
            ('invalid-utf8-text-nul', TB(lawful.encode() + b'\x00\xff')),
            ('trailing-newline', T(lawful + '\n')), ('leading-space', T(' ' + lawful[1:])),
            ('short', T(lawful[:-1])), ('long', T(lawful + 'a')), ('integer', T(12345)), ('real', T(1.5)),
            ('multibyte-same-chars', T(lawful[:-1] + 'é'))]
    if prefix:
        rows += [('uppercase-prefix', T(prefix.upper() + lawful[p:])), ('wrong-prefix', T('x' * p + lawful[p:])),
                 ('nul-after-prefix', T(prefix + '\x00' + lawful[p + 1:]))]
    return rows


def hostile_int(lawful):
    return [('text-integral', T(str(lawful))), ('real-integral', T(float(lawful))), ('real-fraction', T(lawful + 0.5)),
            ('blob', T(bytes([lawful]))), ('text-nul', T(str(lawful) + '\x00')), ('text-fraction', T(str(lawful) + '.5'))]


def hostile_enum(lawful):
    return [('blob', T(lawful.encode())), ('nul-suffix', T(lawful + '\x00')), ('nul-suffix-Z', T(lawful + '\x00Z')),
            ('uppercase', T(lawful.upper())), ('integer', T(7))]


def hostile_text(lawful):
    return [('blob', T(lawful.encode())), ('integer', T(7)), ('real', T(2.5)), ('with-nul', T(lawful + '\x00x'))]


SPEC = [
    ('carrier_format', 'singleton', intlaw(lambda v: v == 1), [(FRESH, 1)], FRESH, hostile_int(1)),
    ('carrier_format', 'carrier_format', intlaw(lambda v: v == 3), [(FRESH, 3)], FRESH, hostile_int(3)),
    ('carrier_format', 'project_key_digest', hexlaw('', 64, False), [(FRESH, E64)], FRESH, hostile_hex('', E64) + [('null', T(None))]),
    ('carrier_format', 'first_generation', intlaw(lambda v: 1 <= v <= 9223372036854775807), [(FRESH, 1), (MIGRATED, 2), (MIGRATED, 9)], MIGRATED, hostile_int(2)),
    ('carrier_format', 'chain_law', intlaw(lambda v: v == 1), [(FRESH, 1)], FRESH, hostile_int(1)),
    ('carrier_format', 'migrated_from', intlaw(lambda v: v in (1, 2), True), [(FRESH, None), (MIGRATED, 2), (MIGRATED, 1)], MIGRATED, hostile_int(2)),
    ('carrier_format', 'migration_op_ref', hexlaw('op-', 32, True), [(FRESH, None), (MIGRATED, 'op-' + 'f' * 32)], MIGRATED, hostile_hex('op-', 'op-' + 'f' * 32)),
    ('grant_journal_v3', 'grantGeneration', intlaw(lambda v: v >= 1), [(SEAL, 1)], SEAL, hostile_int(1)),
    ('grant_journal_v3', 'seq', intlaw(lambda v: v >= 1), [(SEAL, 1)], SEAL, hostile_int(1)),
    ('grant_journal_v3', 'record_schema', intlaw(lambda v: v in (1, 3)), [(SEAL, 3)], SEAL, hostile_int(3)),
    ('grant_journal_v3', 'record_type', enumlaw({'GRANT', 'RA', 'ICI', 'RCI', 'ICO', 'RCO', 'REV', 'CLN', 'SEAL', 'TERMINAL'}), [(SEAL, 'SEAL'), (REV, 'REV')], SEAL, hostile_enum('SEAL')),
    ('grant_journal_v3', 'operation_ref', hexlaw('op-', 32, False), [(SEAL, OP)], SEAL, hostile_hex('op-', OP) + [('null', T(None))]),
    ('grant_journal_v3', 'request_ref', textlaw(True), [(SEAL, None), (SEAL, 'req')], SEAL, hostile_text('req')),
    ('grant_journal_v3', 'token', textlaw(True), [(SEAL, None), (GRANT, 'PT')], GRANT, hostile_text('PT')),
    ('grant_journal_v3', 'install_generation_id', textlaw(True), [(SEAL, None), (GRANT, 'ig1')], GRANT, hostile_text('ig1')),
    ('grant_journal_v3', 'manifest_digest', hexlaw('', 64, True), [(SEAL, None), (GRANT, C64)], GRANT, hostile_hex('', C64)),
    ('grant_journal_v3', 'platform', enumlaw({'macos-aarch64', 'macos-x86_64', 'linux-x86_64-gnu', 'linux-aarch64-gnu'}, True), [(SEAL, None), (GRANT, 'macos-x86_64')], GRANT, hostile_enum('macos-x86_64') + [('alias', T('macos-arm64'))]),
    ('grant_journal_v3', 'run_id', hexlaw('run3:', 64, True), [(SEAL, RUN), (REV, None)], SEAL, hostile_hex('run3:', RUN)),
    ('grant_journal_v3', 'body', textlaw(False), [(SEAL, '{}')], SEAL, hostile_text('{}') + [('null', T(None))]),
    ('grant_journal_v3', 'body_sha256', hexlaw('', 64, False), [(SEAL, B64)], SEAL, hostile_hex('', B64) + [('null', T(None))]),
    ('grant_journal_v3', 'prev_sha256', hexlaw('', 64, False), [(SEAL, B64)], SEAL, hostile_hex('', B64) + [('null', T(None))]),
    ('attempt_custody', 'store_generation_digest', hexlaw('', 64, False), [(ADMITTED, A64)], ADMITTED, hostile_hex('', A64) + [('null', T(None))]),
    ('attempt_custody', 'namespace_id', textlaw(False), [(ADMITTED, 'ns')], ADMITTED, hostile_text('ns') + [('null', T(None))]),
    ('attempt_custody', 'execution_id', hexlaw('exec1_', 32, False), [(ADMITTED, EXEC)], ADMITTED, hostile_hex('exec1_', EXEC) + [('null', T(None))]),
    ('attempt_custody', 'operation_ref', hexlaw('op-', 32, False), [(ADMITTED, OP)], ADMITTED, hostile_hex('op-', OP) + [('null', T(None))]),
    ('attempt_custody', 'record_schema', intlaw(lambda v: v == 1), [(ADMITTED, 1)], ADMITTED, hostile_int(1)),
    ('attempt_custody', 'phase', enumlaw({'admitted', 'settled'}), [(ADMITTED, 'admitted'), (SETTLED, 'settled')], ADMITTED, hostile_enum('admitted')),
    ('attempt_custody', 'settled_outcome', enumlaw({'committed', 'refused'}, True), [(ADMITTED, None), (SETTLED, 'refused')], SETTLED, hostile_enum('refused')),
]


def db(table, encoding=None):
    c = sqlite3.connect(':memory:', isolation_level=None)
    if encoding:
        c.execute("PRAGMA encoding = '%s'" % encoding)
    if table == 'attempt_custody':
        c.executescript(AC)
    else:
        c.executescript(DDL)
        if table == 'grant_journal_v3':
            c.execute('INSERT INTO carrier_format VALUES (1,3,?,1,1,NULL,NULL)', (E64,))
    return c


def insert(table, base, column, expr, encoding=None):
    c = db(table, encoding)
    cols = list(base)
    exprs, params = [], []
    for k in cols:
        e, p = expr if k == column else ('?', base[k])
        exprs.append(e)
        params.append(p)
    try:
        c.execute('INSERT INTO %s (%s) VALUES (%s)' % (table, ','.join(cols), ','.join(exprs)), params)
    except sqlite3.DatabaseError as e:
        return {'result': 'REFUSE', 'reason': str(e).split('\n')[0][:120]}
    t, b = c.execute('SELECT typeof(%s), CAST(%s AS BLOB) FROM %s' % (column, column, table)).fetchone()
    return {'result': 'ADMIT', 'storedType': t, 'storedBytesHex': (b.hex() if b is not None else None), '_t': t, '_b': b}


rows, holes, over = [], [], []
for table, column, law, canon, hbase, hostile in SPEC:
    for i, (base, value) in enumerate(canon):
        r = insert(table, base, column, T(value))
        ok = r['result'] == 'ADMIT' and law(r['_t'], r['_b'])
        if not ok:
            over.append('%s.%s canonical[%d] %s' % (table, column, i, r.get('reason')))
        rows.append({'table': table, 'column': column, 'variant': 'canonical-%d' % i, 'result': r['result'],
                     'storedType': r.get('storedType'), 'lawful': ok, 'reason': r.get('reason')})
    for label, expr in hostile:
        r = insert(table, hbase, column, expr)
        hole = r['result'] == 'ADMIT' and not law(r['_t'], r['_b'])
        if hole:
            holes.append('%s.%s %s (stored %s %s)' % (table, column, label, r['storedType'], (r['storedBytesHex'] or '')[:80]))
        rows.append({'table': table, 'column': column, 'variant': label, 'result': r['result'], 'storedType': r.get('storedType'),
                     'storedBytesHex': (r.get('storedBytesHex') or None) and r['storedBytesHex'][:160], 'hole': hole,
                     'reason': r.get('reason')})

utf16 = {}
for label, expr in [('lawful', T(B64)), ('nul-suffix-Z', T(B64 + '\x00Z')), ('ascii-hex-blob', T(B64.encode()))]:
    r = insert('grant_journal_v3', SEAL, 'body_sha256', expr, encoding='UTF-16le')
    utf16[label] = {k: v for k, v in r.items() if not k.startswith('_')}

root = {}
for label, table, base, column, expr in [
        ('body_sha256 hex+NUL+Z', 'grant_journal_v3', SEAL, 'body_sha256', T(B64 + '\x00Z')),
        ('operation_ref op-hex+NUL+Z', 'grant_journal_v3', SEAL, 'operation_ref', T(OP + '\x00Z')),
        ('run_id run3:hex+NUL+Z', 'grant_journal_v3', SEAL, 'run_id', T(RUN + '\x00Z')),
        ('body_sha256 ASCII-hex BLOB64', 'grant_journal_v3', SEAL, 'body_sha256', T(B64.encode())),
        ('project_key_digest ASCII-hex BLOB64', 'carrier_format', FRESH, 'project_key_digest', T(E64.encode()))]:
    r = insert(table, base, column, expr)
    root[label] = {k: v for k, v in r.items() if not k.startswith('_')}

hist = {}
c2 = sqlite3.connect(':memory:', isolation_level=None)
c2.executescript(V2)
for label, op in (('first-character-only', 'op-a' + 'Z' * 31), ('nul-suffix', OP + '\x00Z'), ('ascii-hex-blob', OP.encode())):
    try:
        c2.execute('INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256) VALUES (?,?,?,?,?,?,?)',
                   (len(hist) + 1, 1, 'REV', op, '{}', B64, B64))
        hist[label] = 'ADMIT'
    except sqlite3.DatabaseError as e:
        hist[label] = 'REFUSE:' + str(e).split('\n')[0]

record = {'copy': COPY, 'holes': holes, 'overRefusals': over, 'holeCount': len(holes), 'variantCount': len(rows),
          'rootCounterexamples': root, 'utf16Observation': utf16, 'frozenCarrierFormat2HistoricalOperationRef': hist,
          'rows': rows}
out = BASE / 'receipts' / ('p01b-storage-matrix.%s.json' % COPY)
if out.exists():
    raise SystemExit('preserve earlier receipt: ' + str(out))
out.write_text(json.dumps(record, indent=1) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'rows'}, indent=1))
if STRICT and (holes or over):
    raise SystemExit(1)
