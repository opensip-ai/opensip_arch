"""Exact storage-class and whole-string grammar matrix for every column of the carrierFormat 3 DDL and the private
attempt_custody DDL of one tree (argv[1] = frozen37 | v1final | edited); argv[2] == 'strict' exits 1 on any hole.

Oracle, per column: an ADMITTED row must STORE a value of the lawful storage class that satisfies the column law
exactly (whole string, no NUL, no BLOB, integer not REAL); every canonical lawful value must be ADMITTED.
A hole is an admitted row whose stored value violates the law; an over-refusal is a refused canonical lawful value.
Hostile inputs include root's NUL-suffix and ASCII-hex BLOB counterexamples. Reference evidence only.
"""
import json, re, sqlite3, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
COPY = sys.argv[1]
STRICT = len(sys.argv) > 2 and sys.argv[2] == 'strict'
SRC = BASE / 'work' / COPY
DDL = (SRC / 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql').read_text()
AC = json.loads((SRC / 'docs/v2/architecture/attempt-custody.schema.v1.json').read_text())['proposedPrivateDDL']

A64, B64, C64, E64 = 'a' * 64, 'b' * 64, 'c' * 64, 'e' * 64
OP, RUN, EXEC = 'op-' + 'a' * 32, 'run3:' + 'c' * 64, 'exec1_' + 'a' * 32


def hexlaw(prefix, n, nullable):
    pat = re.compile(re.escape(prefix) + '[0-9a-f]{%d}' % n)
    return lambda v: (v is None and nullable) or (type(v) is str and pat.fullmatch(v) is not None)


def intlaw(pred, nullable=False):
    return lambda v: (v is None and nullable) or (type(v) is int and pred(v))


def enumlaw(values, nullable=False):
    return lambda v: (v is None and nullable) or (type(v) is str and v in values)


def textlaw(nullable):
    return lambda v: (v is None and nullable) or type(v) is str


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


def TB(b):  # TEXT carrying arbitrary raw bytes (for invalid UTF-8)
    return ('CAST(? AS TEXT)', b)


def hostile_hex(prefix, lawful):
    n = len(lawful)
    mid = n // 2
    rows = [('uppercase-last', T(lawful[:-1] + 'A')), ('nonhex-last', T(lawful[:-1] + 'g')),
            ('nul-suffix-Z', T(lawful + '\x00Z')), ('nul-suffix', T(lawful + '\x00')),
            ('nul-middle-same-chars', T(lawful[:mid] + '\x00' + lawful[mid + 1:])),
            ('nul-after-prefix', T(prefix + '\x00' + lawful[len(prefix) + 1:])),
            ('ascii-hex-blob', T(lawful.encode())), ('ascii-hex-blob-nul-suffix', T(lawful.encode() + b'\x00Z')),
            ('nonhex-blob', T(b'Z' * n)), ('invalid-utf8-text-same-bytes', TB(lawful[:-1].encode() + b'\xc0')),
            ('trailing-newline', T(lawful + '\n')), ('leading-space', T(' ' + lawful[1:])),
            ('short', T(lawful[:-1])), ('long', T(lawful + 'a')), ('integer', T(12345)), ('real', T(1.5)),
            ('multibyte-same-chars', T(lawful[:-1] + 'é'))]
    if prefix:
        rows += [('uppercase-prefix', T(prefix.upper() + lawful[len(prefix):])),
                 ('wrong-prefix', T('x' * len(prefix) + lawful[len(prefix):])),
                 ('prefix-blob', T(lawful.encode()))]
    return rows


def hostile_int(lawful):
    return [('text-integral', T(str(lawful))), ('real-integral', T(float(lawful))), ('real-fraction', T(lawful + 0.5)),
            ('blob', T(bytes([lawful]))), ('text-nul', T(str(lawful) + '\x00')), ('text-fraction', T(str(lawful) + '.5'))]


def hostile_enum(lawful):
    return [('blob', T(lawful.encode())), ('nul-suffix', T(lawful + '\x00')), ('nul-suffix-Z', T(lawful + '\x00Z')),
            ('uppercase', T(lawful.upper())), ('integer', T(7))]


def hostile_text(lawful):
    return [('blob', T(lawful.encode())), ('integer', T(7)), ('real', T(2.5)), ('with-nul', T(lawful + '\x00x'))]


# table, column, law, [(canonical base, value)], hostile base, hostile variants
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
    stored, st = c.execute('SELECT %s, typeof(%s) FROM %s' % (column, column, table)).fetchone()
    return {'result': 'ADMIT', 'storedType': st, 'stored': repr(stored)[:90], '_value': stored}


rows, holes, over = [], [], []
for table, column, law, canon, hbase, hostile in SPEC:
    for i, (base, value) in enumerate(canon):
        r = insert(table, base, column, T(value))
        ok = r['result'] == 'ADMIT' and law(r['_value'])
        if not ok:
            over.append('%s.%s canonical[%d]' % (table, column, i))
        rows.append({'table': table, 'column': column, 'variant': 'canonical-%d' % i, 'result': r['result'],
                     'storedType': r.get('storedType'), 'lawful': ok, 'reason': r.get('reason')})
    for label, expr in hostile:
        r = insert(table, hbase, column, expr)
        hole = r['result'] == 'ADMIT' and not law(r['_value'])
        if hole:
            holes.append('%s.%s %s (stored %s %s)' % (table, column, label, r['storedType'], r['stored']))
        rows.append({'table': table, 'column': column, 'variant': label, 'result': r['result'], 'storedType': r.get('storedType'),
                     'stored': r.get('stored'), 'hole': hole, 'reason': r.get('reason')})

# UTF-16 database text encoding: lawful and hostile hex values (observation of the byte-length assumption)
utf16 = {}
for label, expr in [('lawful', T(B64)), ('nul-suffix-Z', T(B64 + '\x00Z')), ('ascii-hex-blob', T(B64.encode()))]:
    r = insert('grant_journal_v3', SEAL, 'body_sha256', expr, encoding='UTF-16le')
    utf16[label] = {k: v for k, v in r.items() if k != '_value'}

# raw SQLite semantics behind the counterexamples
s = sqlite3.connect(':memory:')
sem = {
    'sqliteVersion': sqlite3.sqlite_version,
    'lengthStopsAtNul': s.execute('SELECT length(?)', (B64 + '\x00Z',)).fetchone()[0],
    'byteLengthOfNulSuffix': s.execute('SELECT length(CAST(? AS BLOB))', (B64 + '\x00Z',)).fetchone()[0],
    'globSeesOnlyBeforeNul': s.execute("SELECT ? NOT GLOB '*[^0-9a-f]*'", (B64 + '\x00Z',)).fetchone()[0],
    'asciiHexBlobLengthAndGlob': s.execute("SELECT typeof(?), length(?), ? NOT GLOB '*[^0-9a-f]*'", (B64.encode(),) * 3).fetchone(),
    'blobEqualsTextNever': s.execute("SELECT CAST(? AS BLOB) = 'SEAL'", ('SEAL',)).fetchone()[0],
    'textNulSuffixEqualsText': s.execute("SELECT ? = 'SEAL'", ('SEAL\x00',)).fetchone()[0],
}
s.execute("CREATE TABLE t_text (x TEXT CHECK (typeof(x) = 'text'))")
s.execute("CREATE TABLE t_int (x INTEGER CHECK (typeof(x) = 'integer'))")
for name, sql, arg in (('textColumnIntegerInputUnderTypeofText', 'INSERT INTO t_text VALUES (?)', 5),
                       ('integerColumnTextInputUnderTypeofInteger', 'INSERT INTO t_int VALUES (?)', '5'),
                       ('integerColumnRealIntegralUnderTypeofInteger', 'INSERT INTO t_int VALUES (?)', 5.0)):
    try:
        s.execute(sql, (arg,))
        sem[name] = 'ADMIT'
    except sqlite3.DatabaseError as e:
        sem[name] = 'REFUSE:' + str(e)
sem['storedAfterAffinity'] = [s.execute('SELECT typeof(x), x FROM t_text').fetchall(), s.execute('SELECT typeof(x), x FROM t_int').fetchall()]

record = {'copy': COPY, 'semantics': sem, 'holes': holes, 'overRefusals': over, 'holeCount': len(holes),
          'variantCount': len(rows), 'utf16Observation': utf16, 'rows': rows}
out = BASE / 'receipts' / ('p01-storage-matrix.%s.json' % COPY)
if out.exists():
    raise SystemExit('preserve earlier receipt: ' + str(out))
out.write_text(json.dumps(record, indent=1, default=str) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'rows'}, indent=1, default=str))
if STRICT and (holes or over):
    raise SystemExit(1)
