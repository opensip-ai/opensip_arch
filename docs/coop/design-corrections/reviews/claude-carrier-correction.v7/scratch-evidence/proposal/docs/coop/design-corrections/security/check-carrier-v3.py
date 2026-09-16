# Reference validation for the carrierFormat 3 correction.
#
# Validates the proposed artifacts against the FROZEN Source25 members they claim to join, so a
# drifted assertion fails here rather than being believed. Read-only except for its report.
#
# usage: python check-carrier-v3.py <source25Root> <runtimeRoot> <reportPath>
import hashlib
import json
import os
import re
import sqlite3
import sys

SRC, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SEC = os.path.join(ROOT, 'scratch', 'proposal', 'docs', 'coop',
                   'design-corrections', 'security')
CAP = 9007199254740991

checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:400]})
    return ok


def load(rel):
    return open(os.path.join(SRC, rel), encoding='utf-8').read()


def _no_dup(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise ValueError('DUPLICATE KEY: ' + k)
        seen.add(k)
    return dict(pairs)


def sload(path):
    """Strict JSON admission: reject duplicate object keys instead of taking the last value.

    json.load is last-wins, so a file carrying two `admitted` keys parses cleanly and every
    assertion about the surviving value is silently about only one of them. Every selected JSON
    file in this correction is admitted through here.
    """
    with open(path, encoding='utf-8') as fh:
        return json.load(fh, object_pairs_hook=_no_dup)


disp = sload(os.path.join(SEC, 'carrier-dispatch.v3.json'))
ddl3 = open(os.path.join(SEC, 'grant-journal.carrier.v3.sql'), encoding='utf-8').read()
hw = sload(os.path.join(SEC, 'carrier-highwater.schema.v1.json'))

# ---- 1. every asserted frozen fact re-derived from the frozen bytes -----------
ddl2 = load('docs/coop/completion/security-schemas.v2/grant-journal.sql')
md1 = load('docs/coop/completion/security-completion.v1.md')
ddl1 = md1.split('```sql')[1].split('```')[0]


def rt_set(text):
    m = re.search(r'record_type\s+TEXT\s+NOT NULL CHECK \(record_type IN\s*\(([^)]*)\)', text)
    return set(re.findall(r"'([A-Z]+)'", m.group(1)))


def pf_set(text):
    m = re.search(r'platform\s+TEXT\s*CHECK \(platform I[SN][^(]*\(([^)]*)\)', text)
    return set(re.findall(r"'([a-z0-9x_-]+)'", m.group(1)))


for fmt, text in (('1', ddl1), ('2', ddl2)):
    ck('dispatch carrierFormat %s recordTypeSet equals frozen DDL' % fmt,
       set(disp['carrierFormats'][fmt]['recordTypeSet']) == rt_set(text),
       sorted(rt_set(text)))
    ck('dispatch carrierFormat %s platformSet equals frozen DDL' % fmt,
       set(disp['carrierFormats'][fmt]['platformSet']) == pf_set(text),
       sorted(pf_set(text)))
    ck('dispatch carrierFormat %s admitsSeal false matches frozen DDL' % fmt,
       disp['carrierFormats'][fmt]['admitsSeal'] is False and 'SEAL' not in rt_set(text))

ck('frozen carrierFormat 2 has the three append triggers',
   all(t in ddl2 for t in ('gj_seq_contiguous', 'gj_no_update', 'gj_no_delete')))
ck('frozen carrierFormat 1 has no contiguity trigger',
   'gj_seq_contiguous' not in ddl1)

# Every asserted trigger/check flag is re-derived from the frozen DDL text, for BOTH inherited
# formats. A misstated flag for either must fail here.
for fmt, text in (('1', ddl1), ('2', ddl2)):
    derived = {
        'hasSeqRangeCheck': 'seq <= 9007199254740991' in text,
        'hasContiguityTrigger': 'grant journal sequence must be tail+1' in text,
        'hasTerminalClosureTrigger': 'grant journal carrier is TERMINAL' in text,
        'hasReservedSlotTrigger': 'is the reserved terminal slot' in text,
    }
    for flag, val in derived.items():
        ck('dispatch carrierFormat %s %s matches frozen DDL' % (fmt, flag),
           disp['carrierFormats'][fmt][flag] is val, 'derived=%s' % val)

sl = json.loads(load('docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'))
jr = sl['$defs']['JournalRecord']
t3 = set(jr['properties']['recordType']['enum'])
ck('dispatch carrierFormat 3 operational types equal frozen schema 3',
   set(disp['carrierFormats']['3']['operationalRecordTypes']) == t3, sorted(t3))
ck('frozen schema 3 excludes TERMINAL', 'TERMINAL' not in t3)
ck('frozen schema 3 bodies are closed', jr.get('additionalProperties') is False)
ck('frozen schema 3 recordSchema const is 3', jr['properties']['recordSchema']['const'] == 3)
ck('dispatch does not claim TERMINAL is a public JournalRecord',
   disp['carrierFormats']['3']['terminalIsPublicJournalRecord'] is False)
lin = set(sl['schemas']['LinearizationV1']['properties']['journalTypes']['items']['enum'])
ck('LinearizationV1 journalTypes still exclude TERMINAL', 'TERMINAL' not in lin and lin == t3)
ck('frozen schema 3 seq is the broad i64 shape, so the carrier narrowing must be stated',
   jr['properties']['seq'] == {'$ref': '#/$defs/I64Positive'})

b1 = json.loads(load('docs/coop/completion/security-schemas.v2/journal-record.schema.json'))
term = [v for v in b1['oneOf'] if v['properties']['recordType']['const'] == 'TERMINAL']
ck('the frozen recordSchema-1 TERMINAL body exists and is reused verbatim', len(term) == 1)
ck('frozen TERMINAL body recordSchema const is 1',
   term and term[0]['properties']['recordSchema']['const'] == 1)
ck('frozen TERMINAL cause enum unchanged by this correction',
   term and term[0]['properties']['cause']['enum'] == ['projectPurge', 'grantGenerationClosure'])

sec = load('docs/v2/contracts/product-v1/security-and-lifecycle.md')
tbl = re.findall(r'^\| `([a-z0-9x_-]+)` \| ([a-z0-9x_-]+) \| ', sec, re.M)
mids = set(x[0] for x in tbl)
ck('S8 machine id table found with four rows', len(tbl) == 4, tbl)
ck('dispatch carrierFormat 3 platformSet equals the S8 machine ids',
   set(disp['carrierFormats']['3']['platformSet']) == mids, sorted(mids))
alias_only = set(x[1] for x in tbl) - mids
ck('carrierFormat 3 DDL refuses every alias-only spelling',
   all(("'" + a + "'") not in ddl3 for a in alias_only), sorted(alias_only))

# ---- 2. the proposed DDL agrees with what the dispatch says about it ----------
ck('carrierFormat 3 DDL record_type set equals the dispatch union',
   rt_set(ddl3) == t3 | {'TERMINAL'}, sorted(rt_set(ddl3)))
ck('carrierFormat 3 DDL platform set equals the dispatch set',
   pf_set(ddl3) == set(disp['carrierFormats']['3']['platformSet']))
for frag in ('record_schema IN (1, 3)', "record_type <> 'TERMINAL'",
             'seq >= 1 AND seq <= 9007199254740991', '9007199254740991 is the reserved terminal slot',
             'grant journal is append-only', 'grant journal sequence must be tail+1',
             'grant journal carrier is TERMINAL', 'chain_law = 1',
             'precedes the carrierFormat 3 first generation',
             'cannot append to a superseded grant generation'):
    ck('carrierFormat 3 DDL states: ' + frag, frag in ddl3)
ck('carrierFormat 3 DDL creates the new table, not the inherited one',
   'CREATE TABLE grant_journal_v3' in ddl3 and 'CREATE TABLE grant_journal ' not in ddl3)
ck('carrierFormat 3 DDL uses CREATE TABLE IF NOT EXISTS only for the two inherited side tables',
   ddl3.count('CREATE TABLE IF NOT EXISTS') == 2
   and 'CREATE TABLE IF NOT EXISTS carrier_quarantine' in ddl3
   and 'CREATE TABLE IF NOT EXISTS carrier_capacity_pause' in ddl3)
ck('carrierFormat 3 DDL contains no ALTER, DROP, UPDATE or DELETE of inherited objects',
   not re.search(r'\b(ALTER|DROP)\b', ddl3))
ck('carrierFormat 3 DDL is valid SQLite and applies cleanly',
   (lambda c: (c.executescript(ddl3), True)[1])(sqlite3.connect(':memory:')))

# Behavioural probes, not text matching: a removed or weakened constraint must fail here even if
# the surrounding prose still mentions it.
C3COLS = ('grantGeneration', 'seq', 'record_schema', 'record_type', 'operation_ref',
          'request_ref', 'token', 'install_generation_id', 'manifest_digest', 'platform',
          'run_id', 'body', 'body_sha256', 'prev_sha256')
_Q = ('INSERT INTO grant_journal_v3 (' + ','.join(C3COLS) + ') VALUES ('
      + ','.join(['?'] * len(C3COLS)) + ')')


def probe(rows, first=1):
    """Apply the DDL to a fresh in-memory carrier and return admit/refuse per row."""
    c = sqlite3.connect(':memory:')
    c.executescript(ddl3)
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,NULL,NULL)', ('e' * 64, first))
    c.commit()
    out = []
    for r in rows:
        try:
            c.execute(_Q, r)
            c.commit()
            out.append(True)
        except sqlite3.Error:
            out.append(False)
    c.close()
    return out


_OP = 'op-' + 'a' * 32
_H = 'b' * 64
_RUN = 'run3:' + '0' * 64


def _row(seq, rs, rt, pf=None, tk=None, ig=None, md=None, rid=None):
    return (1, seq, rs, rt, _OP, None, tk, ig, md, pf, rid, '{}', _H, _H)


ck('DDL behaviourally refuses TERMINAL offered as record_schema 3',
   probe([_row(1, 3, 'TERMINAL')]) == [False])
ck('DDL behaviourally admits TERMINAL as the frozen record_schema 1 body',
   probe([_row(1, 1, 'TERMINAL')]) == [True])
ck('DDL behaviourally refuses an operational type offered as record_schema 1',
   probe([_row(1, 1, 'SEAL', rid=_RUN)]) == [False])
ck('DDL behaviourally admits a schema-3 SEAL carrying run3',
   probe([_row(1, 3, 'SEAL', rid=_RUN)]) == [True])
ck('DDL behaviourally refuses a SEAL with no run_id',
   probe([_row(1, 3, 'SEAL')]) == [False])
def _grant(pf):
    return _row(1, 3, 'GRANT', pf=pf, tk='PT-FS-READ-PROJECT', ig='ig1', md='c' * 64)


ck('DDL behaviourally refuses every alias-only platform on a GRANT',
   all(probe([_grant(a)]) == [False] for a in sorted(alias_only)), sorted(alias_only))
ck('DDL behaviourally admits every S8 machine id on a GRANT',
   all(probe([_grant(m)]) == [True] for m in sorted(mids)), sorted(mids))
ck('DDL behaviourally refuses an append after TERMINAL',
   probe([_row(1, 1, 'TERMINAL'), _row(2, 3, 'REV')]) == [True, False])
ck('DDL behaviourally refuses a non-contiguous sequence',
   probe([_row(2, 3, 'REV')]) == [False])
ck('DDL behaviourally refuses the five historical-only record types',
   all(probe([_row(1, 3, t)]) == [False]
       for t in ('NARROW', 'EXPIRY', 'AUD', 'CHECKPOINT', 'MIGRATION')))
ck('DDL behaviourally refuses a generation below first_generation',
   probe([_row(1, 3, 'REV')], first=5) == [False]
   and probe([(5, 1, 3, 'REV', _OP, None, None, None, None, None, None, '{}', _H, _H)],
             first=5) == [True])
ck('DDL behaviourally refuses an append to a superseded generation',
   probe([(1, 1, 3, 'REV', _OP, None, None, None, None, None, None, '{}', _H, _H),
          (2, 1, 3, 'REV', _OP, None, None, None, None, None, None, '{}', _H, _H),
          (1, 2, 3, 'REV', _OP, None, None, None, None, None, None, '{}', _H, _H)])
   == [True, True, False])
def mutation_refused():
    """Both a row mutation and a row removal must abort on the new table."""
    c = sqlite3.connect(':memory:')
    c.executescript(ddl3)
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,1,1,NULL,NULL)', ('e' * 64,))
    c.execute(_Q, _row(1, 3, 'REV'))
    c.commit()
    refused = []
    for st in ('UPDATE grant_journal_v3 SET request_ref=NULL',
               'DELETE FROM grant_journal_v3'):
        try:
            c.execute(st)
            c.commit()
            refused.append(False)
        except sqlite3.Error:
            refused.append(True)
    c.close()
    return refused


ck('DDL behaviourally refuses UPDATE and DELETE on the new table',
   mutation_refused() == [True, True])
def cf_mutation_refused(stmt):
    c = sqlite3.connect(':memory:')
    c.executescript(ddl3)
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,1,1,NULL,NULL)', ('e' * 64,))
    c.commit()
    try:
        c.execute(stmt)
        c.commit()
        return False
    except sqlite3.Error:
        return True
    finally:
        c.close()


ck('DDL behaviourally refuses mutation of the carrier_format binding',
   [cf_mutation_refused(s) for s in ('UPDATE carrier_format SET first_generation=9',
                                     'DELETE FROM carrier_format')] == [True, True])

# ---- 3. high-water schema is a usable closed shape ---------------------------
try:
    import jsonschema
    V = jsonschema.Draft202012Validator
    V.check_schema({k: v for k, v in hw.items() if not k[0].isupper()
                    and k not in ('extraAdmissionRules', 'notAClaim')})
    sch = {k: v for k, v in hw.items() if k in ('type', 'additionalProperties', 'required', 'properties')}
    good = {'highWaterSchema': 1, 'projectKeyDigest': 'a' * 64, 'grantGeneration': 1,
            'lastSeq': 5, 'tailSha256': 'b' * 64}
    zero = dict(good, lastSeq=0, tailSha256=None)
    ck('high-water accepts a well-formed record', V(sch).is_valid(good))
    ck('high-water accepts lastSeq 0 with null tailSha256', V(sch).is_valid(zero))
    ck('high-water refuses an unknown member', not V(sch).is_valid(dict(good, extra=1)))
    ck('high-water refuses a missing tailSha256 member',
       not V(sch).is_valid({k: v for k, v in good.items() if k != 'tailSha256'}))
    ck('high-water refuses lastSeq above the uint53 cap', not V(sch).is_valid(dict(good, lastSeq=CAP + 1)))
    ck('high-water refuses a boolean highWaterSchema', not V(sch).is_valid(dict(good, highWaterSchema=True)))
    ck('high-water lastSeq cap equals the physical carrier cap',
       hw['properties']['lastSeq']['maximum'] == CAP)
except ImportError as e:
    ck('jsonschema available', False, e)

# ---- 4. the patched planning inputs -----------------------------------------
# The patched-plan and patched-prose checks moved to scratch/controls/check-correction-v4.py,
# which owns the F38-F49 renumbering, the F32 preservation check and the D9 namespace checks.
# This validator keeps only the association joins it needs for the carrier.
P = os.path.join(ROOT, 'scratch', 'patched')
plan = json.load(open(os.path.join(P, 'commit-recovery-plan.v1.json'), encoding='utf-8'))
md = open(os.path.join(P, 'implementation-boundaries-and-build-plan.md'), encoding='utf-8').read()
ck('patched prose names the COV-03 resolution', 'COV-03 resolved (proposed, not accepted)' in md)
ck('patched prose names the recovery algorithm document',
   'commit-recovery-readonly.v3.md' in md)

assoc = plan['recordSchema']['properties']
ck('association journalSeq still excludes the reserved terminal slot',
   assoc['journalSeq']['maximum'] == CAP - 1)
ck('association runId is still run3 only', 'run3:' in assoc['runId']['pattern'])
ck('association operationRef grammar unchanged', assoc['operationRef']['pattern'].startswith('^op-'))
ck('dispatch carrier-side owner split matches the association fields',
   set(disp['associationJoins']['carrierSideValuesOwnedBySecurity'])
   | set(disp['associationJoins']['storageSideValuesOwnedByStorage'])
   | {'runId'} == set(plan['recordSchema']['required']))

# ---- 5. no self-acceptance anywhere in the proposal --------------------------
# Phrase-level, so ordinary words like "custody-qualified" or "silently accepted" do not
# false-positive. The checker file itself is excluded because it carries these phrases as data.
banned = re.compile(
    r'\bis (?:now )?accepted\b|\bhas been accepted\b|\bwe accept\b'
    r'|\bimplementation[- ]ready\b|\bproduction[- ]ready\b'
    r'|\bready for (?:production|implementation|integration)\b'
    r'|\bfully qualified\b|\bqualification (?:achieved|established|passed|satisfied)\b'
    r'|\bgates? (?:passed|satisfied)\b|\bapproved for\b', re.I)
bad = []
SELF = os.path.abspath(__file__)
for dp, dn, fn in os.walk(os.path.join(ROOT, 'scratch', 'proposal')):
    for n in fn:
        p = os.path.join(dp, n)
        if os.path.abspath(p) == SELF:
            continue
        for i, line in enumerate(open(p, encoding='utf-8', errors='replace')):
            if banned.search(line):
                bad.append('%s:%d %s' % (os.path.relpath(p, ROOT), i + 1, line.strip()[:80]))
ck('no proposal file claims acceptance, readiness or qualification', not bad, bad)

# and the converse: every proposal document must positively declare a non-acceptance standing
NEG = ('NOT-SELF-ACCEPTED', 'no acceptance', 'not accepted', 'no self-acceptance')
missing = []
for rel in ('docs/v2/architecture/carrier-fault-cases.v1.json',
            'docs/coop/design-corrections/security/carrier-format.v3.md',
            'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
            'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
            'docs/v2/architecture/commit-recovery-readonly.v3.md',
            'docs/coop/design-corrections/security/carrier-migration.v1.md',
            'docs/v2/architecture/attempt-custody.schema.v1.json'):
    txt = open(os.path.join(ROOT, 'scratch', 'proposal', rel), encoding='utf-8').read()
    if not any(m.lower() in txt.lower() for m in NEG):
        missing.append(rel)
ck('every proposal document declares a non-acceptance standing', not missing, missing)

# ---- 6. strict JSON admission and stable normative paths ---------------------
# The v6 attempt-custody schema shipped with a DUPLICATE `admitted` key. Every check over it
# passed because json.load is last-wins: the collision was invisible to the parser and therefore
# to the validator. These checks admit each selected JSON file strictly, so the same class of
# defect fails here.
SELECTED_JSON = (
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
)
dupes = []
for rel in SELECTED_JSON:
    try:
        sload(os.path.join(ROOT, 'scratch', 'proposal', rel))
    except ValueError as e:
        dupes.append('%s: %s' % (rel, e))
ck('every selected JSON file is admitted under strict duplicate-key rejection', not dupes, dupes)

# The two records whose owner moved to a stable normative path must actually be there, and must
# say so, so a consumer is not left resolving a correction-run directory.
for rel in ('docs/v2/architecture/attempt-custody.schema.v1.json',
            'docs/v2/architecture/carrier-fault-cases.v1.json'):
    ck('selected record is present at its stable normative path: ' + rel,
       os.path.exists(os.path.join(ROOT, 'scratch', 'proposal', rel)))
ac = sload(os.path.join(ROOT, 'scratch', 'proposal',
                        'docs/v2/architecture/attempt-custody.schema.v1.json'))
ck('attempt custody declares its own stable normative path',
   ac.get('stableNormativePath') == 'docs/v2/architecture/attempt-custody.schema.v1.json',
   ac.get('stableNormativePath'))
ck('the dispatch declares its own stable normative path',
   disp.get('stableNormativePath')
   == 'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
   disp.get('stableNormativePath'))

# No stable normative file may resolve its LAW through a correction-run directory.
#
# A run path is admissible in exactly two roles: as a citation of executed evidence, and in the
# sentence that denies any such dependency. Anywhere else -- an operative rule that defers its
# content to `owner-correction.v3` or to a scratch draft -- is a leak, because a consumer reading
# the repo cannot resolve it. This scan found exactly that in carrier-migration §6 (PS-01 lineage
# allocation "is in owner-correction.v3"), which is why the distinction is drawn by role and not
# by simply exempting the files.
RUNREF = re.compile(r'scratch/|owner-correction\.v3|claude-carrier-correction\.v\d')
#
# The classifier is lexical and therefore approximate: it recognises the evidence-citation and
# self-containment roles by wording. It is not a proof that no leak exists, only that none of the
# recognised leak shapes does. A leak phrased as an ordinary evidence citation would pass.
PROVENANCE = re.compile(
    r'"(?:modelProbe|executedEvidence|evidence|report|executedMatrix|'
    r'bodySha256ExecutedEvidence|executedProbe)"\s*:'          # JSON evidence fields
    r'|Evidence:|by execution|executed evidence|retained in'    # prose evidence citations
    r'|marks executed evidence|Control C\d'
    r'|requires no scratch|No operative rule requires'          # the self-containment denials
    r'|recovered from a superseded draft', re.I)
leaks = []
for rel in SELECTED_JSON + (
        'docs/v2/architecture/commit-recovery-readonly.v3.md',
        'docs/coop/design-corrections/security/carrier-format.v3.md',
        'docs/coop/design-corrections/security/carrier-migration.v1.md'):
    p = os.path.join(ROOT, 'scratch', 'proposal', rel)
    lines = open(p, encoding='utf-8').read().splitlines()
    for i, line in enumerate(lines):
        if not RUNREF.search(line):
            continue
        # Markdown prose is hard-wrapped, so the citation verb can sit on the previous line
        # ("Root's result is retained in\n`scratch/v5-evidence`"). Classify over the sentence
        # window, not the physical line.
        window = ' '.join(lines[max(0, i - 1):i + 2])
        if not PROVENANCE.search(window):
            leaks.append('%s:%d %s' % (rel, i + 1, line.strip()[:70]))
ck('no stable normative file resolves its law through a correction-run directory',
   not leaks, leaks or 'lexical classifier; recognised leak shapes only')

# The open dispatch must read the format row LAST: after names and definitions are validated.
order = json.dumps(disp['openDispatch']['order'])
ck('the dispatch declares the row is read last and only after validation',
   disp['openDispatch'].get('rowIsReadLastAndOnlyAfterValidation') is True)
ck('the dispatch declares exactly seven carrierFormat 3 objects',
   len(set(disp['openDispatch']['sevenCarrierFormat3Objects'])) == 7,
   disp['openDispatch']['sevenCarrierFormat3Objects'])
for a, b, label in (('some but not all', 'carrier_format row', 'partial-object refusal'),
                    ('any stored definition differs', 'carrier_format row',
                     'definition validation')):
    ia, ib = order.find(a), order.find(b)
    ck('%s precedes the format-row read' % label, ia != -1 and ib != -1 and ia < ib,
       'positions %d,%d' % (ia, ib))
ck('detection is keyed on the format row, not on table existence',
   disp['migration'].get('detectionIsKeyedOnTheFormatRow') is True)
ck('the migration detection order agrees with the dispatch order',
   'row is read LAST' in disp['migration'].get('detectionOrder', ''),
   disp['migration'].get('detectionOrder', '')[:80])
ck('the fresh-install path does not read absent tables',
   disp['openDispatch']['freshInstallPath'].get('readsAbsentTables') is False)

rep = {'control': 'c4-check-carrier-v3',
       'passed': sum(1 for c in checks if c['pass']),
       'failed': sum(1 for c in checks if not c['pass']),
       'checks': checks}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
for c in checks:
    if not c['pass']:
        print('  FAIL', c['check'], '::', c['detail'])
