# Control C13 - the private carrier-format migration protocol, by execution.
#
# Two parts:
#   1. Reproduce root's frozen-owner counterexample, so the reason the logical store-migrate intent
#      cannot be reused is established from the owner rather than asserted.
#   2. Fault-prefix controls over the three durable acts with realistic ONE-SIDED footprints,
#      including the failure-after-TERMINAL-before-final-metadata case. For every prefix: build
#      exactly that durable state, run the open dispatch and the recovery decision, assert the
#      standing and resume action, then finish the migration and assert the end state.
#
# All SQLite is in-memory. No frozen file, no on-disk carrier.
#
# usage: python c13-migration-prefixes.py <source25Root> <v3sqlPath> <reportPath>
import copy
import importlib.util
import json
import os
import sqlite3
import sys

SRC, V3SQL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SEC = os.path.join(SRC, 'docs/coop/design-corrections/security')
DDL2 = open(os.path.join(SRC, 'docs/coop/completion/security-schemas.v2/grant-journal.sql'),
            encoding='utf-8').read()
DDL3 = open(V3SQL, encoding='utf-8').read()
PKD = 'e' * 64
OPM = 'op-' + 'e' * 32          # the store-gc migration operation's own token
OPA = 'op-' + 'a' * 32          # an ordinary analysis operation
H = 'b' * 64
CAP = 9007199254740991

checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return ok


# ======================================================= 1. root's counterexample, reproduced
spec = importlib.util.spec_from_file_location(
    'rootsec', os.path.join(SEC, 'security_lifecycle_model_v1.py'))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
fx = json.loads(open(os.path.join(SEC, 'transition-journal-cases.v1.json'),
                     encoding='utf-8').read())['records']

good = copy.deepcopy(fx['intentStoreMigrate'])
ck('the lawful logical store-migrate intent is admitted', M.admit_transition_intent(good) == [])

same = copy.deepcopy(good)
same['toStateSchema'] = same['fromStateSchema']
same['toStoreGeneration'] = same['fromStoreGeneration']
carrier_only = M.admit_transition_intent(same)
ck('a carrier-only transition reusing store-migrate is refused MIGRATE_REQUIRES_SCHEMA_ADVANCE',
   'TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE' in carrier_only, carrier_only)
ck('a carrier-only transition reusing store-migrate is refused SCHEMA_CHANGE_SELECTS_NEW_STORE',
   'TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE' in carrier_only, carrier_only)

newop = copy.deepcopy(same)
newop['operation'] = 'carrier-migrate'
invented = M.admit_transition_intent(newop)
ck('an invented carrier-migrate operation is refused by the closed operation enum',
   any(r.startswith('TRANSITION.OPERATION') for r in invented), invented)

sl = json.load(open(os.path.join(SEC, 'security-lifecycle.schemas.v1.json'), encoding='utf-8'))
intent_req = sl['schemas']['InstallationTransitionIntentV1']['required']
journal_req = sl['schemas']['InstallationTransitionJournalV1']['required']
ck('the transition intent is a closed 11-member record', len(intent_req) == 11, len(intent_req))
ck('the transition journal is a closed 20-member record', len(journal_req) == 20, len(journal_req))
ck('neither transition record has any carrier field',
   not any('arrier' in f for f in intent_req + journal_req))

# ======================================================= 2. the existing authorization owner
inv = json.load(open(os.path.join(
    SRC, 'docs/coop/design-corrections/workflows/command-inventory.v3.json'), encoding='utf-8'))
gc = [c for c in inv['commands'] if c['name'] == 'store-gc'][0]
status = [c for c in inv['commands'] if c['name'] == 'store-status'][0]
ck('store-gc is security-owned', gc['owner'] == 'security', gc['owner'])
ck('store-gc carries the exclusive-lease authorization class',
   gc['authorizationClass'] == 'exclusive-lease', gc['authorizationClass'])
ck('store-gc writes NO tracked intent, so it does not drag in the S9.2 transition protocol',
   gc['writesTrackedIntent'] is False)
ck('store-gc already has a mutation step', 'mutation' in gc['steps'], gc['steps'])
ck('store-status already reports migration-state, so no new surface is needed',
   'migration-state' in status['parityFields'], status['parityFields'])

# ======================================================= 3. the three durable acts
C2COLS = ('grantGeneration', 'seq', 'record_type', 'operation_ref', 'request_ref', 'token',
          'install_generation_id', 'manifest_digest', 'platform', 'body', 'body_sha256',
          'prev_sha256')
Q2 = ('INSERT INTO grant_journal (' + ','.join(C2COLS) + ') VALUES ('
      + ','.join(['?'] * len(C2COLS)) + ')')
C3COLS = ('grantGeneration', 'seq', 'record_schema', 'record_type', 'operation_ref', 'request_ref',
          'token', 'install_generation_id', 'manifest_digest', 'platform', 'run_id', 'body',
          'body_sha256', 'prev_sha256')
Q3 = ('INSERT INTO grant_journal_v3 (' + ','.join(C3COLS) + ') VALUES ('
      + ','.join(['?'] * len(C3COLS)) + ')')


def base_carrier(gen=7, rows=3):
    """A lawful carrierFormat 2 carrier with an open generation."""
    c = sqlite3.connect(':memory:')
    c.executescript(DDL2)
    for s in range(1, rows + 1):
        c.execute(Q2, (gen, s, 'RCO', OPA, None, None, None, None, None, '{}', H, H))
    c.commit()
    return c


def act_A(c, gen, op=OPM):
    """Append the TERMINAL that closes the inherited generation. Atomic single INSERT."""
    tail = c.execute('SELECT COALESCE(MAX(seq),0) FROM grant_journal WHERE grantGeneration=?',
                     (gen,)).fetchone()[0]
    c.execute(Q2, (gen, tail + 1, 'TERMINAL', op, None, None, None, None, None, '{}', H, H))
    c.commit()


def act_B(c):
    """Create the new objects. One DDL transaction, all-or-nothing."""
    c.executescript(DDL3)
    c.commit()


def act_C(c, gen):
    """Publish the format row. first_generation is RECOMPUTED here, never fixed earlier."""
    mx = c.execute('SELECT COALESCE(MAX(grantGeneration),0) FROM grant_journal').fetchone()[0]
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,2,?)', (PKD, mx + 1, OPM))
    c.commit()


# ---- the open dispatch, keyed on the ROW and not the tables -------------------
def objects(c):
    return {r[0] for r in c.execute('SELECT name FROM sqlite_master').fetchall()}


def format_row(c):
    if 'carrier_format' not in objects(c):
        return None
    r = c.execute('SELECT carrier_format, project_key_digest, first_generation, chain_law '
                  'FROM carrier_format WHERE singleton=1').fetchone()
    return r


def detect(c):
    n = objects(c)
    if 'grant_journal_v3' in n:
        return 3
    if 'grant_journal' in n and 'gj_seq_contiguous' in n:
        return 2
    if 'grant_journal' in n:
        return 1
    return 0


def tail_record(c, gen):
    return c.execute('SELECT seq, record_type, operation_ref FROM grant_journal '
                     'WHERE grantGeneration=? ORDER BY seq DESC LIMIT 1', (gen,)).fetchone()


def recover(c, gen, myOp=OPM):
    """Total recovery decision over the durable prefix. Returns (prefix, standing, resume)."""
    n = objects(c)
    row = format_row(c)
    t = tail_record(c, gen)
    terminal = bool(t and t[1] == 'TERMINAL')
    objects_created = 'grant_journal_v3' in n and 'carrier_format' in n
    if row is not None:
        return 'ABC', 'carrierFormat-3-complete', 'none'
    if objects_created:
        # verify the existing object definitions byte-equal the selected DDL before resuming
        fresh = sqlite3.connect(':memory:')
        fresh.executescript(DDL2)
        fresh.executescript(DDL3)
        want = {r[0]: r[1] for r in fresh.execute(
            'SELECT name, sql FROM sqlite_master').fetchall()}
        have = {r[0]: r[1] for r in c.execute(
            'SELECT name, sql FROM sqlite_master').fetchall()}
        fresh.close()
        if any(have.get(k) != v for k, v in want.items()):
            return 'AB', 'MIGRATION.CORRUPT', 'refuse'
        return 'AB', 'inherited-format-generation-closed', 'resume-at-C'
    if terminal:
        own = (t[2] == myOp)
        return 'A', 'inherited-format-generation-closed', (
            'resume-at-B (our own TERMINAL)' if own else 'resume-at-B (closed by another op)')
    return '', 'inherited-format-open', 'start-at-A'


# ---- prefix table ------------------------------------------------------------
GEN = 7
PREFIX_CASES = [
    ('prefix empty', []),
    ('prefix A - failure after TERMINAL, before any new object', ['A']),
    ('prefix AB - failure after objects, before the format row', ['A', 'B']),
    ('prefix ABC - complete', ['A', 'B', 'C']),
]
EXPECT = {
    '': ('inherited-format-open', 'start-at-A', 2),
    'A': ('inherited-format-generation-closed', 'resume-at-B (our own TERMINAL)', 2),
    'AB': ('inherited-format-generation-closed', 'resume-at-C', 2),
    'ABC': ('carrierFormat-3-complete', 'none', 3),
}
prefix_rows = []
for label, acts in PREFIX_CASES:
    c = base_carrier(GEN)
    for a in acts:
        {'A': lambda: act_A(c, GEN), 'B': lambda: act_B(c), 'C': lambda: act_C(c, GEN)}[a]()
    pfx, standing, resume = recover(c, GEN)
    fmt = detect(c)
    want = EXPECT[''.join(acts)]
    row = {'case': label, 'acts': acts, 'observedPrefix': pfx, 'standing': standing,
           'resume': resume, 'detectedFormat': fmt,
           'expected': {'standing': want[0], 'resume': want[1], 'format': want[2]}}
    ok = (standing == want[0] and resume == want[1] and fmt == want[2]
          and pfx == ''.join(acts))
    ck('prefix recovery is exact: ' + label, ok, row)

    # finish the migration from wherever we are, then assert the end state
    if standing != 'carrierFormat-3-complete':
        if 'A' not in acts:
            act_A(c, GEN)
        if 'B' not in acts:
            act_B(c)
        act_C(c, GEN)
    row['finalFormat'] = detect(c)
    row['finalFirstGeneration'] = format_row(c)[2]
    ck('migration completes from ' + label, row['finalFormat'] == 3, row['finalFormat'])
    # a schema-3 SEAL is writable in the new generation, and nowhere below it
    fg = row['finalFirstGeneration']
    try:
        c.execute(Q3, (fg, 1, 3, 'SEAL', OPA, None, None, None, None, None,
                       'run3:' + '0' * 64, '{}', H, H))
        c.commit()
        sealed = True
    except sqlite3.Error:
        sealed = False
    ck('a schema-3 SEAL is admitted in the new generation after ' + label, sealed)
    # recovery is idempotent: running it again changes nothing
    p2, s2, r2 = recover(c, GEN)
    ck('recovery is idempotent after ' + label, (p2, s2, r2) == ('ABC', 'carrierFormat-3-complete',
                                                                'none'))
    prefix_rows.append(row)
    c.close()

# ---- commit uncertainty on A -------------------------------------------------
c = base_carrier(GEN)
act_A(c, GEN)
pfx, standing, resume = recover(c, GEN, myOp=OPM)
ck('commit uncertainty on A resolves to our own TERMINAL by its operationRef',
   resume == 'resume-at-B (our own TERMINAL)', resume)
pfx2, st2, res2 = recover(c, GEN, myOp='op-' + 'b' * 32)
ck('a TERMINAL closed by another operation is still a lawful resume, not a repair',
   res2 == 'resume-at-B (closed by another op)', res2)
# a retry of A can never double-apply
try:
    act_A(c, GEN)
    doubled = True
    err = ''
except sqlite3.Error as e:
    doubled = False
    err = str(e)
ck('retrying A cannot double-apply: the frozen TERMINAL trigger refuses it', not doubled, err)
c.close()

# ---- act B is atomic, and the row-keyed detection is what makes AB recoverable
c = base_carrier(GEN)
act_A(c, GEN)
act_B(c)
ck('after B the new tables exist but detection still reports the inherited format',
   'grant_journal_v3' in objects(c) and detect(c) == 2, detect(c))
ck('after B there is no format row', format_row(c) is None)
act_C(c, GEN)
ck('after C detection reports carrierFormat 3', detect(c) == 3)
fg = format_row(c)[2]
ck('first_generation is recomputed as max inherited generation plus one',
   fg == GEN + 1, fg)
ck('chain_law is exactly 1', format_row(c)[3] == 1)
try:
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,9,2,2,?)', (PKD, OPM))
    c.commit()
    second = True
except sqlite3.Error:
    second = False
ck('a second format row is refused', not second)
c.close()

# ---- the benign interleaving: an old core rolls to a new generation in the old table
c = base_carrier(GEN)
act_A(c, GEN)
for s in range(1, 3):                           # a format-unaware core rolls to GEN+1 in place
    c.execute(Q2, (GEN + 1, s, 'RCO', OPA, None, None, None, None, None, '{}', H, H))
c.commit()
act_B(c)
act_C(c, GEN)
fg = format_row(c)[2]
ck('first_generation recomputed after a benign old-core roll skips the occupied generation',
   fg == GEN + 2, fg)
ck('the old-core generation stays in the inherited table and is not migrated',
   c.execute('SELECT COUNT(*) FROM grant_journal WHERE grantGeneration=?',
             (GEN + 1,)).fetchone()[0] == 2)
# split-brain detection: a generation at or above first_generation in the INHERITED table
c.execute(Q2, (fg, 1, 'RCO', OPA, None, None, None, None, None, '{}', H, H))
c.commit()
splits = c.execute('SELECT COUNT(*) FROM grant_journal WHERE grantGeneration >= ?',
                   (fg,)).fetchone()[0]
ck('a generation at or above first_generation in the inherited table is detectable split-brain',
   splits == 1, splits)
c.close()

# ---- chain_law 2 is refused by the DDL --------------------------------------
c = sqlite3.connect(':memory:')
c.executescript(DDL3)
try:
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,2,2,NULL,NULL)', (PKD,))
    c.commit()
    cl2 = True
except sqlite3.Error:
    cl2 = False
ck('the DDL refuses the unselected chain_law 2', not cl2)
c.close()

rep = {'control': 'c13-migration-prefixes',
       'rootCounterexample': {'carrierOnlyRefusals': carrier_only, 'inventedOperation': invented},
       'authorizationOwner': {'command': 'store-gc', 'owner': gc['owner'],
                              'authorizationClass': gc['authorizationClass'],
                              'writesTrackedIntent': gc['writesTrackedIntent'],
                              'reportedBy': 'store-status.parityFields.migration-state'},
       'prefixCases': prefix_rows,
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
