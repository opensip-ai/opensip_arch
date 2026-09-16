"""Storage-class / whole-value grammar matrix, setup-safe (argv[1] = frozen37 | v1final | edited; argv[2] == 'strict').

p01c failed on every tree before any insert: it reused p01b's column spec through exec() in a namespace that lacked
the `re` module. Those receipts are retained. This probe is p01c with that namespace supplying `re`; the column
matrix, oracle, setup-refusal handling, UTF-16 observation and root counterexamples are otherwise identical.
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
spec_src = (BASE / 'probes/p01b_storage_matrix.py').read_text()
ns = {'re': re}
exec(compile(spec_src[spec_src.index('A64, B64, C64, E64'):spec_src.index('def db(table, encoding=None):')], 'p01b-spec', 'exec'), ns)
SPEC, T, SEAL, FRESH, ADMITTED = ns['SPEC'], ns['T'], ns['SEAL'], ns['FRESH'], ns['ADMITTED']
B64, E64, OP, RUN, EXEC = ns['B64'], ns['E64'], ns['OP'], ns['RUN'], ns['EXEC']


def insert(table, base, column, expr, encoding=None):
    c = sqlite3.connect(':memory:', isolation_level=None)
    try:
        if encoding:
            c.execute("PRAGMA encoding = '%s'" % encoding)
        if table == 'attempt_custody':
            c.executescript(AC)
        else:
            c.executescript(DDL)
            if table == 'grant_journal_v3':
                try:
                    c.execute('INSERT INTO carrier_format VALUES (1,3,?,1,1,NULL,NULL)', (E64,))
                except sqlite3.DatabaseError as e:
                    return {'result': 'SETUP-REFUSE', 'reason': str(e).split('\n')[0][:120]}
        cols = list(base)
        exprs, params = [], []
        for k in cols:
            e_, p_ = expr if k == column else ('?', base[k])
            exprs.append(e_)
            params.append(p_)
        try:
            c.execute('INSERT INTO %s (%s) VALUES (%s)' % (table, ','.join(cols), ','.join(exprs)), params)
        except sqlite3.DatabaseError as e:
            return {'result': 'REFUSE', 'reason': str(e).split('\n')[0][:120]}
        t, b = c.execute('SELECT typeof(%s), CAST(%s AS BLOB) FROM %s' % (column, column, table)).fetchone()
        return {'result': 'ADMIT', 'storedType': t, 'storedBytesHex': (b.hex() if b is not None else None), '_t': t, '_b': b}
    finally:
        c.close()


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
for label, table, base, column, expr in [
        ('grant_journal_v3.body_sha256 lawful', 'grant_journal_v3', SEAL, 'body_sha256', T(B64)),
        ('grant_journal_v3.body_sha256 nul-suffix-Z', 'grant_journal_v3', SEAL, 'body_sha256', T(B64 + '\x00Z')),
        ('carrier_format.project_key_digest lawful', 'carrier_format', FRESH, 'project_key_digest', T(E64)),
        ('carrier_format.project_key_digest nul-suffix-Z', 'carrier_format', FRESH, 'project_key_digest', T(E64 + '\x00Z')),
        ('carrier_format.project_key_digest ascii-hex-blob', 'carrier_format', FRESH, 'project_key_digest', T(E64.encode())),
        ('attempt_custody.execution_id lawful', 'attempt_custody', ADMITTED, 'execution_id', T(EXEC)),
        ('attempt_custody.execution_id nul-suffix-Z', 'attempt_custody', ADMITTED, 'execution_id', T(EXEC + '\x00Z')),
        ('attempt_custody.execution_id ascii-hex-blob', 'attempt_custody', ADMITTED, 'execution_id', T(EXEC.encode()))]:
    r = insert(table, base, column, expr, encoding='UTF-16le')
    utf16[label] = {k: v for k, v in r.items() if not k.startswith('_')}
utf16_fail_closed = all(v['result'] in ('REFUSE', 'SETUP-REFUSE') for v in utf16.values())

root = {}
for label, table, base, column, expr in [
        ('body_sha256 hex+NUL+Z', 'grant_journal_v3', SEAL, 'body_sha256', T(B64 + '\x00Z')),
        ('operation_ref op-hex+NUL+Z', 'grant_journal_v3', SEAL, 'operation_ref', T(OP + '\x00Z')),
        ('run_id run3:hex+NUL+Z', 'grant_journal_v3', SEAL, 'run_id', T(RUN + '\x00Z')),
        ('body_sha256 ASCII-hex BLOB64', 'grant_journal_v3', SEAL, 'body_sha256', T(B64.encode())),
        ('project_key_digest ASCII-hex BLOB64', 'carrier_format', FRESH, 'project_key_digest', T(E64.encode()))]:
    r = insert(table, base, column, expr)
    root[label] = {k: v for k, v in r.items() if not k.startswith('_')}
root_refused = all(v['result'] == 'REFUSE' for v in root.values())

hist = {}
for label, op in (('first-character-only', 'op-a' + 'Z' * 31), ('nul-suffix', OP + '\x00Z'), ('ascii-hex-blob', OP.encode())):
    c2 = sqlite3.connect(':memory:', isolation_level=None)
    c2.executescript(V2)
    try:
        c2.execute('INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256) VALUES (1,1,?,?,?,?,?)',
                   ('REV', op, '{}', B64, B64))
        hist[label] = 'ADMIT'
    except sqlite3.DatabaseError as e:
        hist[label] = 'REFUSE:' + str(e).split('\n')[0]
    c2.close()

record = {'copy': COPY, 'sqliteVersion': sqlite3.sqlite_version, 'holes': holes, 'overRefusals': over, 'holeCount': len(holes),
          'variantCount': len(rows), 'rootCounterexamples': root, 'rootCounterexamplesAllRefused': root_refused,
          'utf16Observation': utf16, 'utf16FailsClosed': utf16_fail_closed,
          'frozenCarrierFormat2HistoricalOperationRef': hist, 'rows': rows}
out = BASE / 'receipts' / ('p01d-storage-matrix.%s.json' % COPY)
if out.exists():
    raise SystemExit('preserve earlier receipt: ' + str(out))
out.write_text(json.dumps(record, indent=1) + '\n')
summary = {k: v for k, v in record.items() if k not in ('rows', 'holes')}
summary['holesFirst5'] = holes[:5]
print(json.dumps(summary, indent=1)[-7000:])
if STRICT and (holes or over or not root_refused or not utf16_fail_closed):
    raise SystemExit(1)
