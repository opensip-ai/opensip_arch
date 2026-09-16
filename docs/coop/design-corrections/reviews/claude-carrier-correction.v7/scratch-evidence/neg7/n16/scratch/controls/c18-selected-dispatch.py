# Control C18 - the SELECTED final open dispatch, executed.
#
# The v6 dispatch evidence came from C2's five cases, which tested an EARLIER table-existence
# predicate. That evidence is historical and does not cover this algorithm. This control implements
# the selected algorithm exactly as carrier-dispatch.v3.json openDispatch.order states it, and
# exercises: the fresh-install path, every lawful durable prefix, a partial object set, and an
# all-names-present-but-invalid-definitions shape.
#
# All SQLite is in-memory. No OS durability is established.
#
# usage: python c18-selected-dispatch.py <source25Root> <v3sqlPath> <dispatchJsonPath> <reportPath>
import json
import os
import re
import sqlite3
import sys

SRC, V3SQL, DISPJSON, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
DDL2 = open(os.path.join(SRC, 'docs/coop/completion/security-schemas.v2/grant-journal.sql'),
            encoding='utf-8').read()
DDL1 = open(os.path.join(SRC, 'docs/coop/completion/security-completion.v1.md'),
            encoding='utf-8').read().split('```sql')[1].split('```')[0]
DDL3 = open(V3SQL, encoding='utf-8').read()
DISP = json.load(open(DISPJSON, encoding='utf-8'))
SEVEN = DISP['openDispatch']['sevenCarrierFormat3Objects']
PKD = 'e' * 64
OPM = 'op-' + 'e' * 32
OPA = 'op-' + 'a' * 32
H = 'b' * 64

checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return ok


ck('the dispatch JSON declares exactly seven carrierFormat 3 objects', len(SEVEN) == 7, SEVEN)


def split_sql(script):
    out, buf, in_trigger, depth = [], [], False, 0
    for raw in script.split('\n'):
        line = raw.split('--')[0] if raw.strip().startswith('--') else raw
        if not line.strip():
            continue
        buf.append(line)
        up = line.upper()
        if not in_trigger and re.search(r'\bCREATE\s+TRIGGER\b', up):
            in_trigger, depth = True, 0
        if in_trigger:
            depth += len(re.findall(r'\bBEGIN\b', up)) + len(re.findall(r'\bCASE\b', up))
            depth -= len(re.findall(r'\bEND\b', up))
            if depth <= 0 and line.rstrip().endswith(';'):
                out.append('\n'.join(buf))
                buf, in_trigger, depth = [], False, 0
        elif line.rstrip().endswith(';'):
            out.append('\n'.join(buf))
            buf = []
    if [b for b in buf if b.strip()]:
        out.append('\n'.join(buf))
    return [s for s in out if s.strip()]


def act_B(c, script=None):
    """One explicit transaction, as the selected law requires."""
    stmts = split_sql(DDL3 if script is None else script)
    prev = c.isolation_level
    c.isolation_level = None
    try:
        c.execute('BEGIN')
        try:
            for s in stmts:
                c.execute(s)
            c.execute('COMMIT')
        except Exception:
            c.execute('ROLLBACK')
            raise
    finally:
        c.isolation_level = prev


# ---------------------------------------------------------------- the algorithm
def reference_definitions():
    """What the selected creation path produces, built through act_B itself."""
    d = sqlite3.connect(':memory:')
    act_B(d)
    out = {r[0]: r[1] for r in d.execute('SELECT name, sql FROM sqlite_master').fetchall()
           if r[0] in SEVEN}
    d.close()
    return out


REF = reference_definitions()
ck('the reference definition set covers all seven objects', set(REF) == set(SEVEN), sorted(REF))


def dispatch(c):
    """The SELECTED algorithm, step for step. Returns (result, readsOfV3Content)."""
    reads = 0
    names = {r[0] for r in c.execute('SELECT name FROM sqlite_master').fetchall()}
    present = [o for o in SEVEN if o in names]

    # step 2: none present -> fall through without reading any v3 table
    if not present:
        if 'grant_journal' in names and 'gj_seq_contiguous' in names:
            return 2, reads
        if 'grant_journal' in names:
            return 1, reads
        return 'fresh-install-create-3', reads

    # step 3: partial name set
    if len(present) != len(SEVEN):
        return 'MIGRATION.CORRUPT:partial-objects', reads

    # step 4: all names, definitions must be valid
    have = {r[0]: r[1] for r in c.execute('SELECT name, sql FROM sqlite_master').fetchall()
            if r[0] in SEVEN}
    if have != REF:
        return 'MIGRATION.CORRUPT:invalid-definitions', reads

    # step 5: only now read the row
    reads += 1
    row = c.execute('SELECT carrier_format, project_key_digest, first_generation, chain_law '
                    'FROM carrier_format WHERE singleton=1').fetchone()
    if row is not None:
        return 3, reads
    return 'incomplete-footprint-resume-at-C', reads


C2COLS = ('grantGeneration', 'seq', 'record_type', 'operation_ref', 'request_ref', 'token',
          'install_generation_id', 'manifest_digest', 'platform', 'body', 'body_sha256',
          'prev_sha256')
Q2 = ('INSERT INTO grant_journal (' + ','.join(C2COLS) + ') VALUES ('
      + ','.join(['?'] * len(C2COLS)) + ')')
GEN = 7


def inherited(fmt=2, rows=3):
    c = sqlite3.connect(':memory:')
    c.executescript(DDL2 if fmt == 2 else DDL1)
    for s in range(1, rows + 1):
        c.execute(Q2, (GEN, s, 'RCO', OPA, None, None, None, None, None, '{}', H, H))
    c.commit()
    return c


def act_A(c, gen=GEN, op=OPM):
    tail = c.execute('SELECT COALESCE(MAX(seq),0) FROM grant_journal WHERE grantGeneration=?',
                     (gen,)).fetchone()[0]
    c.execute(Q2, (gen, tail + 1, 'TERMINAL', op, None, None, None, None, None, '{}', H, H))
    c.commit()


def act_C(c, migrated_from=2, op=OPM, first=None):
    if first is None:
        first = c.execute(
            'SELECT COALESCE(MAX(grantGeneration),0) FROM grant_journal').fetchone()[0] + 1
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,?,?)',
              (PKD, first, migrated_from, op))
    c.commit()


cases = []


def case(label, build, want, wantReads=None):
    c = build()
    got, reads = dispatch(c)
    ok = got == want and (wantReads is None or reads == wantReads)
    cases.append({'case': label, 'expected': want, 'got': got, 'contentReads': reads,
                  'pass': ok})
    ck('dispatch: ' + label, ok, [got, reads])
    c.close()


# ---- the fresh-install path, with NO inherited table -------------------------
case('fresh install, empty database', lambda: sqlite3.connect(':memory:'),
     'fresh-install-create-3', 0)


def fresh_created():
    c = sqlite3.connect(':memory:')
    act_B(c)
    act_C(c, migrated_from=None, op=None, first=1)
    return c


case('fresh install after acts B and C, no inherited table', fresh_created, 3, 1)
c = fresh_created()
row = c.execute('SELECT first_generation, migrated_from, migration_op_ref, chain_law '
                'FROM carrier_format WHERE singleton=1').fetchone()
ck('the fresh-install row is first_generation 1, migrated_from null, chain_law 1',
   row == (1, None, None, 1), row)
ck('the fresh-install path created no inherited table',
   'grant_journal' not in {r[0] for r in c.execute('SELECT name FROM sqlite_master')})
c.close()

# ---- inherited formats, no v3 object at all ---------------------------------
case('inherited carrierFormat 2, unmigrated', lambda: inherited(2), 2, 0)
case('inherited carrierFormat 1, unmigrated', lambda: inherited(1), 1, 0)

# ---- lawful durable prefixes ------------------------------------------------
case('prefix A: TERMINAL only', lambda: (lambda c: (act_A(c), c)[1])(inherited(2)), 2, 0)


def prefix_AB():
    c = inherited(2)
    act_A(c)
    act_B(c)
    return c


case('prefix AB: objects created, no row', prefix_AB, 'incomplete-footprint-resume-at-C', 1)


def prefix_ABC():
    c = prefix_AB()
    act_C(c)
    return c


case('prefix ABC: complete', prefix_ABC, 3, 1)

# ---- partial object set ----------------------------------------------------
def partial_one():
    c = inherited(2)
    act_A(c)
    c.execute('CREATE TABLE carrier_format (singleton INTEGER PRIMARY KEY)')
    c.commit()
    return c


case('partial: a lone malformed carrier_format stub', partial_one,
     'MIGRATION.CORRUPT:partial-objects', 0)


def partial_six():
    c = prefix_ABC()
    c.execute('DROP TRIGGER gj3_no_delete')
    c.commit()
    return c


case('partial: six of seven objects present', partial_six,
     'MIGRATION.CORRUPT:partial-objects', 0)

# ---- ALL SEVEN NAMES, invalid definitions ----------------------------------
def all_names_wrong():
    """Every one of the seven names exists, but the definitions are stubs. Name presence alone
    must never be sufficient, which is why step 4 exists."""
    c = inherited(2)
    act_A(c)
    c.execute('CREATE TABLE carrier_format (singleton INTEGER PRIMARY KEY, carrier_format INTEGER,'
              ' project_key_digest TEXT, first_generation INTEGER, chain_law INTEGER)')
    c.execute('CREATE TABLE grant_journal_v3 (x INTEGER)')
    for t in ('cf_no_update', 'cf_no_delete'):
        c.execute("CREATE TRIGGER %s BEFORE UPDATE ON carrier_format BEGIN SELECT 1; END" % t)
    for t in ('gj3_no_update', 'gj3_no_delete', 'gj3_append_laws'):
        c.execute("CREATE TRIGGER %s BEFORE UPDATE ON grant_journal_v3 BEGIN SELECT 1; END" % t)
    c.commit()
    return c


c = all_names_wrong()
names = {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
ck('the malformed shape really does carry all seven names',
   all(o in names for o in SEVEN), sorted(SEVEN - names if isinstance(SEVEN, set) else
                                          [o for o in SEVEN if o not in names]))
c.close()
case('all seven names present, every definition invalid', all_names_wrong,
     'MIGRATION.CORRUPT:invalid-definitions', 0)


def all_names_one_wrong():
    c = prefix_ABC()
    c.execute('DROP TRIGGER gj3_no_delete')
    c.execute('CREATE TRIGGER gj3_no_delete BEFORE DELETE ON grant_journal_v3 '
              'BEGIN SELECT 1; END')
    c.commit()
    return c


case('all seven names present, ONE definition altered', all_names_one_wrong,
     'MIGRATION.CORRUPT:invalid-definitions', 0)

# ---- the row is never read before validation -------------------------------
ck('no MIGRATION.CORRUPT case ever read table content',
   all(x['contentReads'] == 0 for x in cases
       if isinstance(x['got'], str) and x['got'].startswith('MIGRATION.CORRUPT')))
ck('no inherited-format or fresh-install case ever read a carrierFormat 3 table',
   all(x['contentReads'] == 0 for x in cases
       if x['got'] in (1, 2, 'fresh-install-create-3')))
ck('only a complete valid object set leads to a row read',
   all(x['contentReads'] == 1 for x in cases
       if x['got'] == 3 or x['got'] == 'incomplete-footprint-resume-at-C'))
ck('every dispatch case matched its expected outcome', all(x['pass'] for x in cases))

rep = {'control': 'c18-selected-dispatch',
       'algorithmSource': 'carrier-dispatch.v3.json openDispatch.order (selected)',
       'supersededEvidence': ("C2's five cases tested the earlier table-existence predicate and "
                              'are historical evidence only'),
       'standing': 'in-memory only; no OS durability, fsync or real crash behaviour',
       'cases': cases,
       'passed': sum(1 for c_ in checks if c_['pass']),
       'failed': sum(1 for c_ in checks if not c_['pass']),
       'checks': checks}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
for c_ in checks:
    if not c_['pass']:
        print('  FAIL', c_['check'], '::', c_['detail'])
