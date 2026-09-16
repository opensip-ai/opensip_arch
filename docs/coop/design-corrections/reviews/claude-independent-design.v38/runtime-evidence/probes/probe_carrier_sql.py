"""Independent carrierFormat 3 SQL probe over frozen source38 DDL bytes (verified probe copy).

HOSTILE  values outside the author's matrix under UTF-8/UTF-16le/UTF-16be (whitespace/zero-width/NUL enum variants,
         huge and non-finite REALs, leading-space integral text, BLOB record_type).
ORDER    publication, first_generation, contiguity, TERMINAL closure, superseded generation, singleton/immutability.
DISPATCH an independent open-dispatch reading of carrier-format.v3.md sections 8/8.1 on scenarios the author checker does
         not build: carrierFormat-1-like carrier with an inherited row after TERMINAL (F51 second branch), UTF-16 F51,
         read-only recovery of an association against an unmigrated carrierFormat 2 carrier, trailing-space definition.
ROUTES   every publicProjectionByPhase route validates against the frozen evaluator3 StepTermination (R1/R2 bytes).
Reference evidence only; in-memory SQLite; no OS durability.
"""
import json, sqlite3, sys, traceback

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v38'
SRC = RT + '/work/source38-pkg'
SEC = SRC + '/docs/coop/design-corrections/security/'
DDL3 = open(SEC + 'grant-journal.carrier.v3.sql').read()
DDL2 = open(SRC + '/docs/coop/completion/security-schemas.v2/grant-journal.sql').read()
DISP = json.load(open(SEC + 'carrier-dispatch.v3.json'))
OUT = RT + '/receipts/probe-carrier-sql.json'
res = {'sqlite': sqlite3.sqlite_version, 'standing': 'independent reviewer probe; in-memory SQLite; reference evidence only'}
OP, H, RUN = 'op-' + 'a' * 32, 'b' * 64, 'run3:' + 'c' * 64
CF = 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)'
COLS = ['grantGeneration', 'seq', 'record_schema', 'record_type', 'operation_ref', 'request_ref', 'token', 'install_generation_id',
        'manifest_digest', 'platform', 'run_id', 'body', 'body_sha256', 'prev_sha256']
INS = 'INSERT INTO grant_journal_v3 (%s) VALUES (%s)' % (','.join(COLS), ','.join('?' * len(COLS)))


def row(gen=1, seq=1, rs=3, rt='REV', op=OP, rid=None, **kw):
    base = dict(zip(COLS, (gen, seq, rs, rt, op, None, None, None, None, None, rid, '{}', H, H)))
    base.update(kw)
    return [base[c] for c in COLS]


def db(enc='UTF-8', publish=None):
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.execute("PRAGMA encoding = '%s'" % enc)
    c.executescript(DDL3)
    if publish:
        c.execute(CF, publish)
    return c


def attempt(c, sql, args):
    try:
        c.execute(sql, args)
        return 'ADMIT'
    except sqlite3.Error as e:
        return 'REFUSE:' + str(e)[:70]
    except (OverflowError, TypeError, ValueError) as e:
        # attempt1 crashed here: Python sqlite3 cannot bind 2**63; that is a harness limit, not a DDL decision
        return 'HARNESS-UNBINDABLE:' + type(e).__name__


FRESH = (1, 3, 'e' * 64, 1, 1, None, None)
# ---------------------------------------------------------------- HOSTILE
hostile = {}
for enc in ('UTF-8', 'UTF-16le', 'UTF-16be'):
    cases = {
        'record_type trailing space': row(rt='REV '), 'record_type NUL': row(rt='REV\x00'), 'record_type BLOB': row(rt=b'REV'),
        'record_type zero-width': row(rt='RE​V'), 'platform NUL on GRANT': row(rt='GRANT', token='t', install_generation_id='i', manifest_digest=H, platform='macos-x86_64\x00'),
        'operation_ref zero-width tail': row(op='op-' + 'a' * 31 + '​'), 'operation_ref fullwidth hyphen': row(op='op－' + 'a' * 32),
        'body_sha256 leading space': row(body_sha256=' ' + H[1:]), 'run_id on SEAL uppercase prefix': row(rt='SEAL', rid='RUN3:' + 'c' * 64),
        'seq 2^63 as REAL': row(seq=float(2 ** 63)), 'seq 2^63 as text (affinity overflow)': row(seq='9223372036854775808'),'seq NaN': row(seq=float('nan')), 'seq +inf': row(seq=float('inf')),
        'seq leading-space integral text': row(seq=' 1'), 'seq integral text': row(seq='1'), 'grantGeneration boolean True': row(gen=True),
        'record_schema text 3': row(rs='3'), 'body BLOB': row(body=b'{}'), 'body NUL-suffixed text': row(body='{}\x00'),
        'lawful REV': row(), 'lawful SEAL': row(rt='SEAL', rid=RUN),
    }
    out = {}
    for label, args in cases.items():
        c = db(enc, FRESH)
        r = attempt(c, INS, args)
        if r == 'ADMIT':
            t = c.execute('SELECT typeof(seq), typeof(grantGeneration), typeof(record_schema), typeof(body), length(body) FROM grant_journal_v3').fetchone()
            r = 'ADMIT ' + repr(t)
        out[label] = r
        c.close()
    fcases = {'first_generation 1.0 REAL': (1, 3, 'e' * 64, 1.0, 1, None, None), 'first_generation text 1': (1, 3, 'e' * 64, '1', 1, None, None),
              'project_key_digest zero-width': (1, 3, 'e' * 63 + '​', 1, 1, None, None),
              'migrated_from 2 op-ref NUL tail': (1, 3, 'e' * 64, 2, 1, 2, 'op-' + 'f' * 31 + '\x00'),
              'chain_law 1.0 REAL': (1, 3, 'e' * 64, 1, 1.0, None, None)}
    for label, args in fcases.items():
        c = db(enc)
        out[label] = attempt(c, CF, args)
        c.close()
    hostile[enc] = out
res['HOSTILE'] = hostile

# ---------------------------------------------------------------- ORDER
c = db()
order = {'append before publication': attempt(c, INS, row())}
order['fresh first_generation 2 refused'] = attempt(c, CF, (1, 3, 'e' * 64, 2, 1, None, None))
order['migrated first_generation 1 refused'] = attempt(c, CF, (1, 3, 'e' * 64, 1, 1, 2, 'op-' + 'f' * 32))
order['migrated without op ref refused'] = attempt(c, CF, (1, 3, 'e' * 64, 5, 1, 2, None))
order['publish migrated first_generation 5'] = attempt(c, CF, (1, 3, 'e' * 64, 5, 1, 2, 'op-' + 'f' * 32))
order['second format row refused'] = attempt(c, CF, (1, 3, 'e' * 64, 6, 1, 2, 'op-' + 'f' * 32))
order['update format row refused'] = attempt(c, 'UPDATE carrier_format SET first_generation = 6', ())
order['delete format row refused'] = attempt(c, 'DELETE FROM carrier_format', ())
order['append gen 4 below first refused'] = attempt(c, INS, row(gen=4))
order['append gen 5 seq 2 non-contiguous refused'] = attempt(c, INS, row(gen=5, seq=2))
order['append gen 5 seq 1'] = attempt(c, INS, row(gen=5, seq=1))
order['TERMINAL as recordSchema 3 refused'] = attempt(c, INS, row(gen=5, seq=2, rs=3, rt='TERMINAL'))
order['TERMINAL recordSchema 1'] = attempt(c, INS, row(gen=5, seq=2, rs=1, rt='TERMINAL'))
order['append after TERMINAL refused'] = attempt(c, INS, row(gen=5, seq=3))
order['REV as recordSchema 1 refused'] = attempt(c, INS, row(gen=6, seq=1, rs=1))
order['append gen 6'] = attempt(c, INS, row(gen=6, seq=1))
order['append superseded gen 5 (seq 4, contiguity fires first)'] = attempt(c, INS, row(gen=5, seq=4))
c2 = db(publish=(1, 3, 'e' * 64, 5, 1, 2, 'op-' + 'f' * 32))
order['isolated: gen 5 seq 1'] = attempt(c2, INS, row(gen=5, seq=1))
order['isolated: gen 6 seq 1'] = attempt(c2, INS, row(gen=6, seq=1))
order['isolated: contiguous gen 5 seq 2 after gen 6 (superseded law)'] = attempt(c2, INS, row(gen=5, seq=2))
order['update journal refused'] = attempt(c, 'UPDATE grant_journal_v3 SET body = ?', ('{"x":1}',))
order['SEAL without run_id refused'] = attempt(c, INS, row(gen=6, seq=2, rt='SEAL'))
order['TERMINAL with platform refused'] = attempt(c, INS, row(gen=6, seq=2, rs=1, rt='TERMINAL', platform='macos-x86_64'))
res['ORDER'] = order

# ---------------------------------------------------------------- DISPATCH (independent reading of section 8 / 8.1)
SEVEN = DISP['openDispatch']['sevenCarrierFormat3Objects']
REF = sqlite3.connect(':memory:')
REF.executescript(DDL3)
REFDEFS = dict(REF.execute('SELECT name, sql FROM sqlite_master WHERE name IN (%s)' % ','.join('?' * 7), SEVEN).fetchall())


def open_dispatch(c, phase, admitted, assoc=None):
    """Independent transcription: binding first on read-only; names; partial; definitions; row read last; post checks."""
    if phase == 'readOnlyRecovery' and assoc is not None and assoc['journalCarrierDigest'] != admitted:
        return 'binding-unusable'
    names = {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
    present = [n for n in SEVEN if n in names]
    if not present:
        if 'grant_journal' in names:
            fmt = 'carrierFormat2' if 'gj_seq_contiguous' in names else 'carrierFormat1'
            return fmt
        return 'fresh-install'
    if len(present) != 7:
        return 'migration-footprint-corrupt'
    defs = dict(c.execute('SELECT name, sql FROM sqlite_master WHERE name IN (%s)' % ','.join('?' * 7), SEVEN).fetchall())
    if defs != REFDEFS:
        return 'migration-footprint-corrupt'
    rowv = c.execute('SELECT project_key_digest, first_generation FROM carrier_format WHERE singleton = 1').fetchone()
    if rowv is None:
        if c.execute('SELECT 1 FROM grant_journal_v3 LIMIT 1').fetchone():
            return 'migration-footprint-corrupt'
        return 'incomplete-footprint'
    if rowv[0] != admitted:
        return 'carrier-project-binding-mismatch'
    if 'grant_journal' in names:
        top = c.execute('SELECT MAX(grantGeneration) FROM grant_journal').fetchone()[0]
        after = c.execute("SELECT 1 FROM grant_journal g WHERE EXISTS (SELECT 1 FROM grant_journal t WHERE t.grantGeneration = g.grantGeneration "
                          "AND t.record_type = 'TERMINAL' AND t.seq < g.seq) LIMIT 1").fetchone()
        if (top is not None and top >= rowv[1]) or after:
            return 'split-brain-custody-condition'
    low = c.execute('SELECT MIN(grantGeneration) FROM grant_journal_v3').fetchone()[0]
    if low is not None and low < rowv[1]:
        return 'migration-footprint-corrupt'
    if phase == 'readOnlyRecovery' and assoc is not None and assoc['grantGeneration'] < rowv[1]:
        return 'unknown-carrier-incompatible'
    return 'carrierFormat3'


def public(phase, standing):
    proj = DISP['publicProjectionByPhase']
    if phase == 'readOnlyRecovery':
        key = proj['readOnlyStandingOfDispatchResult'].get(standing)
        return None if key is None else proj['readOnlyRecovery'][key]
    return proj.get(phase, {}).get(standing)


GJ2 = 'INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256) VALUES (?,?,?,?,\'{}\',?,?)'
ADM = 'e' * 64
disp = {}
# carrierFormat-1-like: inherited DDL with its triggers removed, TERMINAL-closed, migrated, then a row after TERMINAL
try:
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.executescript(DDL2)
    for (tname,) in c.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'").fetchall():
        c.execute('DROP TRIGGER "%s"' % tname)
    c.execute(GJ2, (1, 1, 'REV', OP, H, H))
    c.execute(GJ2, (1, 2, 'TERMINAL', 'op-' + '9' * 32, H, H))
    fmt_before = open_dispatch(c, 'writerOrMaintenanceOpen', ADM)
    c.executescript(DDL3)
    c.execute(CF, (1, 3, ADM, 2, 1, 1, 'op-' + '9' * 32))
    clean = open_dispatch(c, 'writerOrMaintenanceOpen', ADM)
    c.execute(GJ2, (1, 3, 'REV', OP, H, H))  # format-1 has no TERMINAL trigger: a row after TERMINAL
    st = open_dispatch(c, 'writerOrMaintenanceOpen', ADM)
    ro = open_dispatch(c, 'readOnlyRecovery', ADM, {'journalCarrierDigest': ADM, 'grantGeneration': 2})
    disp['format1-row-after-terminal'] = {'beforeMigration': fmt_before, 'cleanAfterPublication': clean, 'writer': st, 'writerRoute': public('writerOrMaintenanceOpen', st),
                                          'readOnly': ro, 'readOnlyRoute': public('readOnlyRecovery', ro)}
except Exception as exc:
    disp['format1-row-after-terminal'] = {'error': repr(exc), 'tb': traceback.format_exc()[-800:]}
# UTF-16 F51
try:
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.execute("PRAGMA encoding = 'UTF-16le'")
    c.executescript(DDL2)
    c.execute(GJ2, (1, 1, 'REV', OP, H, H))
    c.execute(GJ2, (1, 2, 'TERMINAL', 'op-' + '9' * 32, H, H))
    c.executescript(DDL3)
    c.execute(CF, (1, 3, ADM, 2, 1, 2, 'op-' + '9' * 32))
    seal = attempt(c, INS, row(gen=2, rt='SEAL', rid=RUN))
    c.execute(GJ2, (2, 1, 'REV', OP, H, H))
    st = open_dispatch(c, 'writerOrMaintenanceOpen', ADM)
    disp['utf16-f51'] = {'encoding': c.execute('PRAGMA encoding').fetchone()[0], 'sealAdmitted': seal, 'writer': st,
                         'writerRoute': public('writerOrMaintenanceOpen', st),
                         'defsEqualReference': dict(c.execute('SELECT name, sql FROM sqlite_master WHERE name IN (%s)' % ','.join('?' * 7), SEVEN).fetchall()) == REFDEFS}
except Exception as exc:
    disp['utf16-f51'] = {'error': repr(exc), 'tb': traceback.format_exc()[-800:]}
# unmigrated carrierFormat 2 with an association (association implies a committed v3 SEAL)
try:
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.executescript(DDL2)
    c.execute(GJ2, (1, 1, 'REV', OP, H, H))
    st = open_dispatch(c, 'readOnlyRecovery', ADM, {'journalCarrierDigest': ADM, 'grantGeneration': 2})
    disp['format2-with-association'] = {'readOnly': st, 'routeInReadOnlyStandingMap': public('readOnlyRecovery', st),
                                        'mapKeys': sorted(DISP['publicProjectionByPhase']['readOnlyStandingOfDispatchResult'])}
except Exception as exc:
    disp['format2-with-association'] = {'error': repr(exc)}
# definition differing only by trailing whitespace in a trigger body
try:
    mutated = DDL3.replace("RAISE(ABORT, 'grant journal is append-only'); END;", "RAISE(ABORT, 'grant journal is append-only');  END;", 1)
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.executescript(mutated)
    st = open_dispatch(c, 'writerOrMaintenanceOpen', ADM)
    disp['whitespace-only-definition-change'] = {'mutationApplied': mutated != DDL3, 'writer': st, 'writerRoute': public('writerOrMaintenanceOpen', st)}
except Exception as exc:
    disp['whitespace-only-definition-change'] = {'error': repr(exc)}
res['DISPATCH'] = disp

# ---------------------------------------------------------------- ROUTES vs frozen StepTermination
try:
    sys.path.insert(0, SRC + '/docs/coop/design-corrections/foundation')
    import canonical
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    common = json.load(open(SRC + '/docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'))
    reg = Registry().with_resource(common['$id'], Resource(contents=common, specification=DRAFT202012))
    routes = {}
    for phase, body in DISP['publicProjectionByPhase'].items():
        if phase in ('standing', 'phaseLaws', 'readOnlyStandingOfDispatchResult'):
            continue
        for st, p in body.items():
            t = {'class': p['class']}
            for k in ('errorCode', 'faultCause'):
                if p[k] is not None:
                    t[k] = p[k]
            if p['domainDetail']:
                t['domainDetail'] = {'code': p['domainDetail'], 'remedy': 'probe'}
            try:
                canonical.ExactValidator({'$ref': common['$id'] + '#/$defs/StepTermination'}, registry=reg).validate(t)
                routes[phase + '/' + st] = 'VALID'
            except Exception as e:
                routes[phase + '/' + st] = 'INVALID:' + str(e).split('\n')[0][:120]
    res['ROUTES'] = routes
except Exception as exc:
    res['ROUTES'] = {'error': repr(exc), 'tb': traceback.format_exc()[-800:]}

json.dump(res, open(OUT, 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str)[:12000])
