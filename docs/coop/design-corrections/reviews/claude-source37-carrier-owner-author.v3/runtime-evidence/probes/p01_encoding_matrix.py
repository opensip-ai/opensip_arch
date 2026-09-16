"""Byte-safe, setup-safe storage-class / whole-value grammar matrix under THREE database text encodings.

argv[1] = frozen37 | v2final | rootalt | edited; argv[2] == 'strict' exits 1 on any hole, over-refusal or admitted root
counterexample in any encoding. 'rootalt' is root's alternative derived mechanically from the v2 final bytes: every
length(CAST(column AS BLOB)) = N becomes instr(column, char(0)) = 0 (typeof, character length, prefix and hex guards kept).

Per encoding (UTF-8, UTF-16le, UTF-16be) the column matrix is the retained v2 28-column / 341-variant spec (exec'd from
the v2 runtime, digest recorded) plus encoding-specific hostile TEXT for the 10 hex columns (overlong NUL, overlong hex
digit, CESU surrogate, lone continuation byte; lone UTF-16 surrogate, NUL code unit, odd trailing byte; fullwidth and
Arabic-Indic digits). Read-back is typeof() and CAST(column AS BLOB) decoded in the observed database encoding; a TEXT
value that does not decode is unlawful for every grammar-bearing column.
Oracle: an ADMITTED row must store the lawful storage class and whole-value grammar; every canonical lawful value must
be ADMITTED. Reference evidence only.
"""
import hashlib, json, re, sqlite3, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
V2SPEC = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/probes/p01b_storage_matrix.py')
TREE = sys.argv[1]
STRICT = len(sys.argv) > 2 and sys.argv[2] == 'strict'
DDL_REL = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
AC_REL = 'docs/v2/architecture/attempt-custody.schema.v1.json'
BYTELEN = re.compile(r'length\(CAST\((\w+) AS BLOB\)\) = \d+')
if TREE == 'rootalt':
    src = BASE / 'work/v2final'
    DDL, n_ddl = BYTELEN.subn(r'instr(\1, char(0)) = 0', (src / DDL_REL).read_text())
    AC, n_ac = BYTELEN.subn(r'instr(\1, char(0)) = 0', json.loads((src / AC_REL).read_text())['proposedPrivateDDL'])
    derivation = {'ddlReplacements': n_ddl, 'attemptCustodyReplacements': n_ac}
else:
    src = BASE / 'work' / TREE
    DDL = (src / DDL_REL).read_text()
    AC = json.loads((src / AC_REL).read_text())['proposedPrivateDDL']
    derivation = None
V2DDL = (BASE / 'work/frozen37/docs/coop/completion/security-schemas.v2/grant-journal.sql').read_text()
ENCODINGS = ('UTF-8', 'UTF-16le', 'UTF-16be')
CODEC = {'UTF-8': 'utf-8', 'UTF-16le': 'utf-16-le', 'UTF-16be': 'utf-16-be'}

spec_src = V2SPEC.read_text()
ns = {'re': re}
exec(compile(spec_src[spec_src.index('A64, B64, C64, E64'):spec_src.index('def db(table, encoding=None):')], 'v2-p01b-spec', 'exec'), ns)
SPEC, T, TB, SEAL, FRESH, ADMITTED = ns['SPEC'], ns['T'], ns['TB'], ns['SEAL'], ns['FRESH'], ns['ADMITTED']
B64, E64, OP, RUN, EXEC = ns['B64'], ns['E64'], ns['OP'], ns['RUN'], ns['EXEC']
HEX_COLUMNS = {('carrier_format', 'project_key_digest'): '', ('carrier_format', 'migration_op_ref'): 'op-',
               ('grant_journal_v3', 'operation_ref'): 'op-', ('grant_journal_v3', 'run_id'): 'run3:',
               ('grant_journal_v3', 'manifest_digest'): '', ('grant_journal_v3', 'body_sha256'): '',
               ('grant_journal_v3', 'prev_sha256'): '', ('attempt_custody', 'store_generation_digest'): '',
               ('attempt_custody', 'execution_id'): 'exec1_', ('attempt_custody', 'operation_ref'): 'op-'}


def extra_hex(lawful, enc):
    head = lawful[:-1]
    if enc == 'UTF-8':
        raw = [('overlong-nul-c080', head.encode() + b'\xc0\x80'), ('overlong-hex-digit-c0b0', head.encode() + b'\xc0\xb0'),
               ('cesu-surrogate', head.encode() + b'\xed\xa0\x80'), ('lone-continuation-byte', head.encode() + b'\x80')]
    else:
        codec = CODEC[enc]
        raw = [('lone-surrogate-unit', head.encode(codec) + (b'\x00\xd8' if enc == 'UTF-16le' else b'\xd8\x00')),
               ('nul-code-unit-suffix', lawful.encode(codec) + '\x00'.encode(codec)),
               ('odd-trailing-byte', lawful.encode(codec) + b'\x41')]
    return [(label, TB(b)) for label, b in raw] + [('fullwidth-digit', T(head + '０')), ('arabic-indic-digit', T(head + '٠'))]


def insert(table, base, column, expr, encoding):
    c = sqlite3.connect(':memory:', isolation_level=None)
    try:
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
        observed = c.execute('PRAGMA encoding').fetchone()[0]
        cols = list(base)
        exprs, params = [], []
        for k in cols:
            e_, p_ = expr if k == column else ('?', base[k])
            exprs.append(e_)
            params.append(p_)
        try:
            c.execute('INSERT INTO %s (%s) VALUES (%s)' % (table, ','.join(cols), ','.join(exprs)), params)
        except sqlite3.DatabaseError as e:
            return {'result': 'REFUSE', 'reason': str(e).split('\n')[0][:120], 'encoding': observed}
        t, b = c.execute('SELECT typeof(%s), CAST(%s AS BLOB) FROM %s' % (column, column, table)).fetchone()
        if t == 'null':
            u = None
        elif t == 'blob':
            u = b
        else:
            try:
                u = b.decode(CODEC[observed]).encode('utf-8')
            except UnicodeDecodeError:
                u = b'\xff<undecodable>'
        return {'result': 'ADMIT', 'storedType': t, 'storedBytesHex': (b.hex() if b is not None else None), 'encoding': observed,
                '_t': t, '_u': u}
    finally:
        c.close()


per_encoding = {}
for enc in ENCODINGS:
    rows, holes, over, affinity, base_holes, base_rows = [], [], [], [], 0, 0
    for table, column, law, canon, hbase, hostile in SPEC:
        variants = list(hostile)
        extras = extra_hex(dict(hbase)[column] if dict(hbase)[column] is not None else canon[-1][1], enc) if (table, column) in HEX_COLUMNS else []
        for i, (base, value) in enumerate(canon):
            r = insert(table, base, column, T(value), enc)
            ok = r['result'] == 'ADMIT' and r['encoding'] == enc and law(r['_t'], r['_u'])
            if not ok:
                over.append('%s.%s canonical[%d] %s' % (table, column, i, r.get('reason')))
            rows.append({'table': table, 'column': column, 'variant': 'canonical-%d' % i, 'set': 'v2-341', 'result': r['result'],
                         'storedType': r.get('storedType'), 'lawful': ok, 'reason': r.get('reason')})
            base_rows += 1
        for set_name, group in (('v2-341', variants), ('encoding-extra', extras)):
            for label, expr in group:
                r = insert(table, hbase, column, expr, enc)
                hole = r['result'] == 'ADMIT' and not law(r['_t'], r['_u'])
                if hole:
                    holes.append('%s.%s %s [%s] (stored %s %s)' % (table, column, label, set_name, r['storedType'], (r['storedBytesHex'] or '')[:64]))
                    if set_name == 'v2-341':
                        base_holes += 1
                elif r['result'] == 'ADMIT':
                    affinity.append('%s.%s %s -> %s' % (table, column, label, r['storedType']))
                rows.append({'table': table, 'column': column, 'variant': label, 'set': set_name, 'result': r['result'],
                             'storedType': r.get('storedType'), 'storedBytesHex': (r.get('storedBytesHex') or None) and r['storedBytesHex'][:160],
                             'hole': hole, 'reason': r.get('reason')})
                if set_name == 'v2-341':
                    base_rows += 1
    root = {}
    for label, table, base, column, expr in [
            ('body_sha256 hex+NUL+Z', 'grant_journal_v3', SEAL, 'body_sha256', T(B64 + '\x00Z')),
            ('operation_ref op-hex+NUL+Z', 'grant_journal_v3', SEAL, 'operation_ref', T(OP + '\x00Z')),
            ('run_id run3:hex+NUL+Z', 'grant_journal_v3', SEAL, 'run_id', T(RUN + '\x00Z')),
            ('body_sha256 ASCII-hex BLOB64', 'grant_journal_v3', SEAL, 'body_sha256', T(B64.encode())),
            ('project_key_digest ASCII-hex BLOB64', 'carrier_format', FRESH, 'project_key_digest', T(E64.encode())),
            ('project_key_digest uppercase', 'carrier_format', FRESH, 'project_key_digest', T(E64[:-1] + 'A')),
            ('store_generation_digest NUL-suffix', 'attempt_custody', ADMITTED, 'store_generation_digest', T('a' * 64 + '\x00Z'))]:
        r = insert(table, base, column, expr, enc)
        root[label] = {k: v for k, v in r.items() if not k.startswith('_')}
    per_encoding[enc] = {'v2SetRows': base_rows, 'totalRows': len(rows), 'holes': holes, 'holeCount': len(holes), 'v2SetHoleCount': base_holes,
                         'overRefusals': over, 'lawfulAffinityOrRefusalFreeAdmissions': affinity,
                         'rootCounterexamples': root, 'rootCounterexamplesAllRefused': all(v['result'] == 'REFUSE' for v in root.values()),
                         'rows': rows}
hist = {}
for enc in ENCODINGS:
    for label, op in (('first-character-only', 'op-a' + 'Z' * 31), ('nul-suffix', OP + '\x00Z'), ('ascii-hex-blob', OP.encode())):
        c2 = sqlite3.connect(':memory:', isolation_level=None)
        c2.execute("PRAGMA encoding = '%s'" % enc)
        c2.executescript(V2DDL)
        try:
            c2.execute('INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256) VALUES (1,1,?,?,?,?,?)',
                       ('REV', op, '{}', B64, B64))
            hist['%s %s' % (enc, label)] = 'ADMIT'
        except sqlite3.DatabaseError as e:
            hist['%s %s' % (enc, label)] = 'REFUSE:' + str(e).split('\n')[0]
        c2.close()
record = {'tree': TREE, 'sqliteVersion': sqlite3.sqlite_version, 'v2SpecSha256': hashlib.sha256(V2SPEC.read_bytes()).hexdigest(),
          'ddlSha256': hashlib.sha256(DDL.encode()).hexdigest(), 'attemptCustodyDdlSha256': hashlib.sha256(AC.encode()).hexdigest(),
          'rootAltDerivation': derivation, 'frozenCarrierFormat2HistoricalOperationRef': hist,
          'summary': {enc: {k: v for k, v in d.items() if k in ('v2SetRows', 'totalRows', 'holeCount', 'v2SetHoleCount', 'rootCounterexamplesAllRefused')}
                      | {'overRefusalCount': len(d['overRefusals'])} for enc, d in per_encoding.items()},
          'perEncoding': per_encoding}
out = BASE / 'receipts' / ('p01-encoding-matrix.%s.json' % TREE)
if out.exists():
    raise SystemExit('preserve earlier receipt: ' + str(out))
out.write_text(json.dumps(record, indent=1) + '\n')
printable = {k: v for k, v in record.items() if k != 'perEncoding'}
printable['holesFirst8'] = {enc: d['holes'][:8] for enc, d in per_encoding.items()}
printable['overRefusalsFirst8'] = {enc: d['overRefusals'][:8] for enc, d in per_encoding.items()}
printable['lawfulAffinityOrRefusalFreeAdmissions'] = {enc: d['lawfulAffinityOrRefusalFreeAdmissions'] for enc, d in per_encoding.items()}
print(json.dumps(printable, indent=1)[-12000:])
bad = any(d['holeCount'] or d['overRefusals'] or not d['rootCounterexamplesAllRefused'] for d in per_encoding.values())
if STRICT and bad:
    raise SystemExit(1)
