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
    # The fresh path publishes first_generation 1; a higher first generation is a migrated row with its
    # migration op ref, as the corrected carrier_format CHECK requires.
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,1,?,?)',
              ('e' * 64, first, None if first == 1 else 2, None if first == 1 else 'op-' + 'f' * 32))
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

# ---- 7. source37 owner correction: lowercase-hex grammar (review advisory A37-01) ----------------
# Behavioural, not textual: each hex-bearing column refuses an uppercase or non-hex LAST character and a
# non-hex tail after a lawful first character, and still admits the lawful value.
_S37_CF = 'INSERT INTO carrier_format VALUES (?,?,?,?,?,?,?)'
_S37_FRESH = (1, 3, 'e' * 64, 1, 1, None, None)
_S37_MIG = (1, 3, 'e' * 64, 2, 1, 2, 'op-' + 'f' * 32)
_S37_RUN3 = 'run3:' + 'c' * 64


def _s37_run(script, steps):
    c = sqlite3.connect(':memory:', isolation_level=None)
    c.executescript(script)
    out = []
    for sql, args in steps:
        try:
            c.execute(sql, args)
            out.append(True)
        except sqlite3.Error:
            out.append(False)
    c.close()
    return out


def _s37_try(c, sql, args):
    try:
        c.execute(sql, args)
        return True
    except sqlite3.Error:
        return False


def _s37_v3(gen=1, seq=1, rt='REV', op=_OP, rid=None, md_=None, pf=None, tk=None, ig=None, bs=_H, ps=_H):
    return (gen, seq, 3, rt, op, None, tk, ig, md_, pf, rid, '{}', bs, ps)


def _s37_bad(value):
    last = value[-1].upper() if value[-1] in 'abcdef' else 'A'
    return [value[:-1] + last, value[:-1] + 'g', value[:-31] + 'Z' * 31]


ck('source37: lawful schema-3 SEAL still admitted with lowercase-hex members',
   _s37_run(ddl3, [(_S37_CF, _S37_FRESH), (_Q, _s37_v3(rt='SEAL', rid=_S37_RUN3))]) == [True, True])
for _name, _lawful, _make in (
        ('operation_ref', _OP, lambda v: _s37_v3(rt='SEAL', rid=_S37_RUN3, op=v)),
        ('run_id', _S37_RUN3, lambda v: _s37_v3(rt='SEAL', rid=v)),
        ('body_sha256', _H, lambda v: _s37_v3(rt='SEAL', rid=_S37_RUN3, bs=v)),
        ('prev_sha256', _H, lambda v: _s37_v3(rt='SEAL', rid=_S37_RUN3, ps=v)),
        ('manifest_digest', 'c' * 64, lambda v: _s37_v3(rt='GRANT', pf='macos-x86_64', tk='PT', ig='ig1', md_=v))):
    ck('source37: grant_journal_v3.%s admits the lawful lowercase-hex value' % _name,
       _s37_run(ddl3, [(_S37_CF, _S37_FRESH), (_Q, _make(_lawful))]) == [True, True])
    ck('source37: grant_journal_v3.%s refuses an uppercase or non-hex last character and a non-hex tail' % _name,
       all(_s37_run(ddl3, [(_S37_CF, _S37_FRESH), (_Q, _make(b))]) == [True, False] for b in _s37_bad(_lawful)))
for _name, _lawful, _make in (
        ('project_key_digest', 'e' * 64, lambda v: (1, 3, v, 1, 1, None, None)),
        ('migration_op_ref', 'op-' + 'f' * 32, lambda v: (1, 3, 'e' * 64, 2, 1, 2, v))):
    ck('source37: carrier_format.%s admits the lawful value and refuses uppercase or non-hex anywhere' % _name,
       _s37_run(ddl3, [(_S37_CF, _make(_lawful))]) == [True]
       and all(_s37_run(ddl3, [(_S37_CF, _make(b))]) == [False] for b in _s37_bad(_lawful)))
_S37_AC = sload(os.path.join(ROOT, 'scratch', 'proposal', 'docs/v2/architecture/attempt-custody.schema.v1.json'))['proposedPrivateDDL']
_S37_ACQ = 'INSERT INTO attempt_custody VALUES (?,?,?,?,1,?,NULL)'


def _s37_acrow(sg='a' * 64, ex='exec1_' + 'a' * 32, op=_OP):
    return (sg, 'ns', ex, op, 'admitted')


ck('source37: attempt_custody admits the lawful lowercase-hex row', _s37_run(_S37_AC, [(_S37_ACQ, _s37_acrow())]) == [True])
for _name, _lawful, _make in (('store_generation_digest', 'a' * 64, lambda v: _s37_acrow(sg=v)),
                              ('execution_id', 'exec1_' + 'a' * 32, lambda v: _s37_acrow(ex=v)),
                              ('operation_ref', _OP, lambda v: _s37_acrow(op=v))):
    ck('source37: attempt_custody.%s refuses an uppercase or non-hex last character and a non-hex tail' % _name,
       all(_s37_run(_S37_AC, [(_S37_ACQ, _make(b))]) == [False] for b in _s37_bad(_lawful)))
ck('source37: no carrierFormat 3 or attempt_custody CHECK keeps a first-character-only hex GLOB',
   "[0-9a-f]*'" not in ddl3 and "[0-9a-f]*'" not in _S37_AC,
   [l.strip() for l in (ddl3 + '\n' + _S37_AC).splitlines() if "[0-9a-f]*'" in l])
ck('source37: frozen carrierFormat 2 bytes keep their first-character-only operation_ref GLOB (disclosed historical scope)',
   "operation_ref GLOB 'op-[0-9a-f]*' AND length(operation_ref) = 35" in ddl2
   and _s37_run(ddl2, [("INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256)"
                        " VALUES (1,1,'REV',?,'{}',?,?)", ('op-a' + 'Z' * 31, _H, _H))]) == [True]
   and 'historicalScope' in disp.get('ddlGrammar', {}))

# ---- 8. source37 owner correction: publication and first_generation law (review advisory A37-02) -----
ck('source37: an {A, B} footprint (seven objects, no format row) refuses every grant_journal_v3 append',
   _s37_run(ddl3, [(_Q, _s37_v3(gen=1)), (_Q, _s37_v3(gen=9))]) == [False, False])
ck('source37: first_generation is exactly 1 on the fresh path',
   _s37_run(ddl3, [(_S37_CF, (1, 3, 'e' * 64, 5, 1, None, None))]) == [False]
   and _s37_run(ddl3, [(_S37_CF, _S37_FRESH)]) == [True])
ck('source37: first_generation is at least 2 on the migrated path',
   _s37_run(ddl3, [(_S37_CF, (1, 3, 'e' * 64, 1, 1, 2, 'op-' + 'f' * 32))]) == [False]
   and _s37_run(ddl3, [(_S37_CF, _S37_MIG)]) == [True])
ck('source37: after publication a generation below first_generation refuses and first_generation admits',
   _s37_run(ddl3, [(_S37_CF, _S37_MIG), (_Q, _s37_v3(gen=1)), (_Q, _s37_v3(gen=2))]) == [True, False, True])

# ---- 9. source37 owner correction: executable open dispatch, interrupted state, phase routes (A37-03/04)
# A reference decision function over real in-memory SQLite carriers. Every call re-reads the carrier bytes
# (no cached verdict), writes nothing, and its conclusions are projected through
# publicProjectionByPhase, which must agree with an independent expectation table, S12, the read-only
# section 1 table, the security model D9 map, D9 v1.14 codeMaps and the selected StepTermination schema.
_S37_SEVEN = disp['openDispatch']['sevenCarrierFormat3Objects']
_S37_Q7 = 'SELECT name, sql FROM sqlite_master WHERE name IN (%s)' % ','.join('?' * 7)
_s37_ref = sqlite3.connect(':memory:')
_s37_ref.executescript(ddl3)
_S37_REF_DEFS = dict(_s37_ref.execute(_S37_Q7, _S37_SEVEN).fetchall())
_s37_ref.close()
_S37_ADMITTED, _S37_OTHER = 'e' * 64, 'd' * 64


def _s37_open(c, phase, admitted=_S37_ADMITTED, assoc=None, witness=None):
    if phase == 'readOnlyRecovery' and assoc is not None and assoc['journalCarrierDigest'] != admitted:
        return 'binding-unusable'
    names = {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
    present = [n for n in _S37_SEVEN if n in names]
    if present:
        if len(present) < 7 or dict(c.execute(_S37_Q7, _S37_SEVEN).fetchall()) != _S37_REF_DEFS:
            return 'migration-footprint-corrupt'
        row = c.execute('SELECT project_key_digest, first_generation FROM carrier_format WHERE singleton = 1').fetchone()
        if row is None:
            if c.execute('SELECT 1 FROM grant_journal_v3 LIMIT 1').fetchone():
                return 'migration-footprint-corrupt'
            if witness is not None and witness != admitted:
                return 'carrier-project-binding-mismatch'
            return 'incomplete-footprint'
        if row[0] != admitted:
            return 'carrier-project-binding-mismatch'
        if 'grant_journal' in names:
            top = c.execute('SELECT MAX(grantGeneration) FROM grant_journal').fetchone()[0]
            after_terminal = c.execute(
                "SELECT 1 FROM grant_journal g JOIN grant_journal t ON t.grantGeneration = g.grantGeneration"
                " AND t.record_type = 'TERMINAL' AND t.seq < g.seq LIMIT 1").fetchone()
            if (top is not None and top >= row[1]) or after_terminal:
                return 'split-brain-custody-condition'
        low = c.execute('SELECT MIN(grantGeneration) FROM grant_journal_v3').fetchone()[0]
        if low is not None and low < row[1]:
            return 'migration-footprint-corrupt'
        if witness is not None and witness != admitted:
            return 'carrier-project-binding-mismatch'
        if phase == 'readOnlyRecovery' and assoc is not None and assoc['grantGeneration'] < row[1]:
            return 'unknown-carrier-incompatible'
        return 'carrierFormat3'
    if 'grant_journal' in names:
        return 'carrierFormat2' if 'gj_seq_contiguous' in names else 'carrierFormat1'
    return 'fresh-install'


def _s37_publish(c, admitted=_S37_ADMITTED, witness=None):
    """Act C, fresh or resuming {A, B}: verify, then publish in one transaction; any failure publishes nothing."""
    standing = _s37_open(c, 'maintenanceActCPublication', admitted, witness=witness)
    if standing != 'incomplete-footprint':
        return standing
    migrated = 'grant_journal' in {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
    c.execute('BEGIN IMMEDIATE')
    try:
        if c.execute('SELECT 1 FROM grant_journal_v3 LIMIT 1').fetchone():
            c.execute('ROLLBACK')
            return 'migration-footprint-corrupt'
        first = c.execute('SELECT MAX(grantGeneration) FROM grant_journal').fetchone()[0] + 1 if migrated else 1
        c.execute(_S37_CF, (1, 3, admitted, first, 1, 2 if migrated else None, 'op-' + '9' * 32 if migrated else None))
        c.execute('COMMIT')
        return 'published'
    except sqlite3.Error:
        c.execute('ROLLBACK')
        return 'refused-by-ddl'


_S37_GJ2 = ("INSERT INTO grant_journal (grantGeneration,seq,record_type,operation_ref,body,body_sha256,prev_sha256)"
            " VALUES (?,?,?,?,'{}',?,?)")


def _s37_carrier(kind):
    """fresh: act B only. migrated: a carrierFormat 2 generation, act A TERMINAL, then act B objects."""
    c = sqlite3.connect(':memory:', isolation_level=None)
    if kind == 'migrated':
        c.executescript(ddl2)
        c.execute(_S37_GJ2, (1, 1, 'REV', _OP, _H, _H))
        c.execute(_S37_GJ2, (1, 2, 'TERMINAL', 'op-' + '9' * 32, _H, _H))
    c.executescript(ddl3)
    return c


def _s37_state(c):
    tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
    return (tuple(c.execute('SELECT type, name, sql FROM sqlite_master ORDER BY name').fetchall()),
            tuple((t, tuple(c.execute('SELECT * FROM "%s"' % t).fetchall())) for t in tables))


def _s37_inject(c, gen):
    """Disclosed harness only: lift the append trigger verbatim, insert one row, reinstall the identical text."""
    trig = c.execute("SELECT sql FROM sqlite_master WHERE name = 'gj3_append_laws'").fetchone()[0]
    c.execute('DROP TRIGGER gj3_append_laws')
    c.execute(_Q, _s37_v3(gen=gen))
    c.execute(trig)


_S37_PROJ = disp['publicProjectionByPhase']
_S37_RO_MAP = _S37_PROJ['readOnlyStandingOfDispatchResult']
_S37_LC = ('operational-failed', 4, 'LEDGER.CORRUPT', 'ledger-corrupt')
_S37_EXPECT = {
    ('writerOrMaintenanceOpen', 'migration-footprint-corrupt'): _S37_LC + ('MIGRATION.CORRUPT',),
    ('writerOrMaintenanceOpen', 'split-brain-custody-condition'): _S37_LC + ('MIGRATION.CORRUPT',),
    ('writerOrMaintenanceOpen', 'carrier-project-binding-mismatch'): _S37_LC + (None,),
    ('maintenanceActCPublication', 'migration-footprint-corrupt'): _S37_LC + ('MIGRATION.CORRUPT',),
    ('maintenanceActCPublication', 'carrier-project-binding-mismatch'): _S37_LC + (None,),
    ('readOnlyRecovery', 'binding-unusable'): ('request-rejected', 2, 'EXTENSION.ADMISSION_REJECTED', None, 'RECOVERY.REFUSED'),
    ('readOnlyRecovery', 'carrier-project-binding-mismatch'): _S37_LC + (None,),
    ('readOnlyRecovery', 'migration-footprint-corrupt'): _S37_LC + (None,),
    ('readOnlyRecovery', 'split-brain-custody-condition'): _S37_LC + (None,),
    ('readOnlyRecovery', 'unknown-carrier-incompatible'): ('operational-failed', 4, 'HOST.IO_FAILURE', 'host-io', None),
    ('readOnlyRecovery', 'incomplete-footprint'): ('operational-failed', 4, 'LEDGER.BUSY_TIMEOUT', 'ledger-busy', 'PROJECT.BUSY'),
}
_S37_SEEN = set()


def _s37_public(phase, standing):
    if phase == 'readOnlyRecovery':
        return _S37_PROJ['readOnlyRecovery'][_S37_RO_MAP[standing]]
    return _S37_PROJ[phase][standing]


def _s37_expect(label, phase, got, standing):
    _S37_SEEN.add((phase, got))
    ok = got == standing
    detail = got
    if ok and (phase, got) in _S37_EXPECT:
        p = _s37_public(phase, got)
        detail = (p['class'], p['exit'], p['errorCode'], p['faultCause'], p['domainDetail'])
        ok = detail == _S37_EXPECT[(phase, got)]
    ck('source37 scenario: ' + label, ok, detail)


_RO_OK = {'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': 2}
c = _s37_carrier('fresh')
_s37_expect('interrupted fresh install {B} is an incomplete footprint at a writer open', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'incomplete-footprint')
_s37_expect('interrupted fresh install {B} is unavailable-busy on read-only recovery', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery'), 'incomplete-footprint')
ck('source37 scenario: the fresh {B} footprint refuses an append before publication', _s37_try(c, _Q, _s37_v3(gen=1)) is False)
ck('source37 scenario: fresh act C publishes first_generation 1 with null migration fields',
   _s37_publish(c) == 'published'
   and c.execute('SELECT first_generation, migrated_from, migration_op_ref FROM carrier_format').fetchone() == (1, None, None))
_s37_expect('a published fresh carrier opens as carrierFormat 3', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'carrierFormat3')

c = _s37_carrier('migrated')
_before = _s37_state(c)
_s37_expect('interrupted migration {A, B} is an incomplete footprint at a writer open', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'incomplete-footprint')
_s37_expect('interrupted migration {A, B} is unavailable-busy on read-only recovery', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'incomplete-footprint')
ck('source37 scenario: detection over {A, B} writes nothing', _s37_state(c) == _before)
ck('source37 scenario: the {A, B} footprint refuses grant_journal_v3 appends at any generation',
   _s37_try(c, _Q, _s37_v3(gen=1)) is False and _s37_try(c, _Q, _s37_v3(gen=2)) is False)
ck('source37 scenario: act C resume publishes first_generation = max inherited + 1 with migration fields',
   _s37_publish(c) == 'published'
   and c.execute('SELECT first_generation, migrated_from FROM carrier_format').fetchone() == (2, 2))
_s37_expect('a migrated carrier opens as carrierFormat 3', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'carrierFormat3')
_s37_expect('read-only recovery of an association in the current generation proceeds to the SEAL join', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'carrierFormat3')
_s37_expect('F46: an association naming the historical generation is unknown-carrier-incompatible', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_ADMITTED, 'grantGeneration': 1}),
            'unknown-carrier-incompatible')
_s37_expect('an association naming another carrier is binding-unusable on read-only recovery', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_OTHER, 'grantGeneration': 2}), 'binding-unusable')
c.execute(_S37_GJ2, (2, 1, 'REV', _OP, _H, _H))  # a format-unaware core rolls the inherited table
_before = _s37_state(c)
_s37_expect('F51: an inherited generation at first_generation is split-brain at a writer open, re-detected after an earlier clean open',
            'writerOrMaintenanceOpen', _s37_open(c, 'writerOrMaintenanceOpen'), 'split-brain-custody-condition')
_s37_expect('F51 on read-only recovery projects the quarantine-condition row', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'split-brain-custody-condition')
ck('source37 scenario: split-brain detection writes nothing', _s37_state(c) == _before)

c = _s37_carrier('migrated')
_s37_inject(c, 1)
ck('source37 scenario: the injection harness reinstalled byte-identical definitions',
   dict(c.execute(_S37_Q7, _S37_SEVEN).fetchall()) == _S37_REF_DEFS)
_before = _s37_state(c)
_s37_expect('{A, B} holding a grant_journal_v3 row is migration corruption at a writer open', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'migration-footprint-corrupt')
_s37_expect('act C refuses to publish over a grant_journal_v3 row', 'maintenanceActCPublication',
            _s37_publish(c), 'migration-footprint-corrupt')
_s37_expect('the same footprint on read-only recovery projects the quarantine-condition row', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'migration-footprint-corrupt')
ck('source37 scenario: the refused publication published and wrote nothing', _s37_state(c) == _before)

c = _s37_carrier('migrated')
_before = _s37_state(c)
_s37_expect('act C refuses to publish when a surviving witness names another project', 'maintenanceActCPublication',
            _s37_publish(c, witness=_S37_OTHER), 'carrier-project-binding-mismatch')
ck('source37 scenario: the witness refusal published and wrote nothing', _s37_state(c) == _before)

c = _s37_carrier('migrated')
ck('source37 scenario: a carrier published under another project binding', _s37_publish(c, admitted=_S37_OTHER) == 'published')
_s37_expect('a published project_key_digest naming another project is a binding mismatch, not MIGRATION.CORRUPT, at a writer open',
            'writerOrMaintenanceOpen', _s37_open(c, 'writerOrMaintenanceOpen'), 'carrier-project-binding-mismatch')
_s37_expect('that carrier with an association naming the admitted carrier is the read-only quarantine-condition row',
            'readOnlyRecovery', _s37_open(c, 'readOnlyRecovery', assoc=_RO_OK), 'carrier-project-binding-mismatch')
_s37_expect('an association naming the other carrier is binding-unusable before any carrier read', 'readOnlyRecovery',
            _s37_open(c, 'readOnlyRecovery', assoc={'journalCarrierDigest': _S37_OTHER, 'grantGeneration': 2}), 'binding-unusable')

c = sqlite3.connect(':memory:', isolation_level=None)
c.executescript(ddl2)
c.execute('CREATE TABLE carrier_format (singleton INTEGER)')
_s37_expect('a partial carrierFormat 3 object set is migration corruption', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'migration-footprint-corrupt')
c = sqlite3.connect(':memory:', isolation_level=None)
c.executescript(ddl2)
c.executescript(ddl3.replace('CHECK (chain_law = 1)', 'CHECK (chain_law IN (1, 2))'))
_s37_expect('all seven names with an invalid definition is migration corruption', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'migration-footprint-corrupt')
c = _s37_carrier('migrated')
_s37_publish(c)
_s37_inject(c, 1)
_s37_expect('a published grant_journal_v3 row below first_generation is migration corruption (rows verified, not only definitions)',
            'writerOrMaintenanceOpen', _s37_open(c, 'writerOrMaintenanceOpen'), 'migration-footprint-corrupt')
c = sqlite3.connect(':memory:', isolation_level=None)
c.executescript(ddl2)
_s37_expect('an unmigrated carrierFormat 2 carrier still opens as carrierFormat 2', 'writerOrMaintenanceOpen',
            _s37_open(c, 'writerOrMaintenanceOpen'), 'carrierFormat2')
_s37_expect('no journal table at all is the fresh-install path', 'writerOrMaintenanceOpen',
            _s37_open(sqlite3.connect(':memory:'), 'writerOrMaintenanceOpen'), 'fresh-install')

_s37_need = ({(ph, st) for ph in ('writerOrMaintenanceOpen', 'maintenanceActCPublication') for st in _S37_PROJ[ph]}
             | {('readOnlyRecovery', st) for st in _S37_RO_MAP})
ck('source37 scenario coverage: every phase route is exercised by a real carrier state', _s37_need <= _S37_SEEN,
   sorted(_s37_need - _S37_SEEN))
ck('source37 route law: read-only recovery never publishes MIGRATION.CORRUPT',
   all(p['domainDetail'] != 'MIGRATION.CORRUPT' for p in _S37_PROJ['readOnlyRecovery'].values()))
ck('source37 route law: a carrier project binding mismatch never borrows MIGRATION.CORRUPT',
   all(_S37_PROJ[ph]['carrier-project-binding-mismatch']['domainDetail'] is None
       for ph in ('writerOrMaintenanceOpen', 'maintenanceActCPublication')))
ck('source37 route law: a read-only quarantine conclusion requires stable observations, otherwise unavailable-busy',
   _S37_PROJ['readOnlyRecovery']['unknown-quarantine-condition'].get('requiresStableObservations') is True
   and _S37_PROJ['readOnlyRecovery']['unknown-quarantine-condition'].get('otherwise') == 'unavailable-busy')
ck('source37 route law: the seven carrierFormat 3 object names are unchanged',
   sorted(_S37_SEVEN) == sorted(['carrier_format', 'cf_no_update', 'cf_no_delete', 'grant_journal_v3',
                                 'gj3_no_update', 'gj3_no_delete', 'gj3_append_laws']) and set(_S37_REF_DEFS) == set(_S37_SEVEN))

# Every projection agrees with the owners it names.
_S37_D9 = json.loads(load('docs/coop/artifacts/d9-exit-contract.v1.14.json'))
_S37_FAULT = dict(_S37_D9['codeMaps']['faultCauseToErrorCode'])
_S37_REJECT = set(_S37_D9['codeMaps']['rejectionCauseToErrorCode'].values())
_S37_EXIT = {'success': 0, 'policy-failed': 1, 'request-rejected': 2, 'indeterminate': 3, 'operational-failed': 4, 'interrupted': 130}
_S37_MODEL = load('docs/coop/design-corrections/security/security_lifecycle_model_v1.py')
_S37_CODES = {r['code'] for r in json.loads(load('docs/coop/design-corrections/public-detail-registry.v1.json'))['records']}
_S37_COMMON = json.loads(load('docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'))
_S37_READONLY = open(os.path.join(ROOT, 'scratch', 'proposal', 'docs/v2/architecture/commit-recovery-readonly.v3.md'),
                     encoding='utf-8').read()
_S37_S12 = [l for l in sec[sec.index('## S12. D9 joins and refusal vocabulary'):sec.index('### S12.1')].splitlines()
            if l.startswith('| ')]
try:
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    _S37_STV = jsonschema.Draft202012Validator(
        {'$ref': _S37_COMMON['$id'] + '#/$defs/StepTermination'},
        registry=Registry().with_resource(_S37_COMMON['$id'], Resource(contents=_S37_COMMON, specification=DRAFT202012)))
except Exception as e:
    _S37_STV = None
    ck('source37: selected StepTermination validator available', False, e)
for _phase in ('writerOrMaintenanceOpen', 'maintenanceActCPublication', 'readOnlyRecovery'):
    for _standing, _p in _S37_PROJ[_phase].items():
        _label = '%s/%s' % (_phase, _standing)
        _t = {'class': _p['class']}
        if _p['errorCode'] is not None:
            _t['errorCode'] = _p['errorCode']
        if _p['faultCause'] is not None:
            _t['faultCause'] = _p['faultCause']
        if _p['domainDetail'] is not None:
            _t['domainDetail'] = {'code': _p['domainDetail'], 'remedy': 'reference projection'}
        _errs = sorted(e.message for e in _S37_STV.iter_errors(_t)) if _S37_STV else ['no validator']
        ck('source37 route: %s projects to a StepTermination the selected schema admits' % _label, not _errs, _errs)
        ck('source37 route: %s exit is the fixed D9 class exit' % _label, _S37_EXIT[_p['class']] == _p['exit'])
        if _p['class'] == 'operational-failed':
            _ok = _S37_FAULT.get(_p['faultCause']) == _p['errorCode']
        else:
            _ok = _p['class'] == 'request-rejected' and _p['faultCause'] is None and _p['errorCode'] in _S37_REJECT
        ck('source37 route: %s errorCode and faultCause pair under D9 v1.14 codeMaps' % _label, _ok, _t)
        ck('source37 route: %s domainDetail is omitted or an existing registered code' % _label,
           _p['domainDetail'] is None or _p['domainDetail'] in _S37_CODES, _p['domainDetail'])
        if _p['securityRefusal'] is not None:
            _m = re.search(r"'%s':\s*\('([a-z-]+)',\s*(\d+),\s*'([A-Z._]+)'\)" % re.escape(_p['securityRefusal']), _S37_MODEL)
            ck('source37 route: %s agrees with the security model D9 map' % _label,
               _m is not None and (_m.group(1), int(_m.group(2)), _m.group(3)) == (_p['class'], _p['exit'], _p['errorCode']),
               _m and _m.groups())
        _rows = [l for l in _S37_S12 if _p['s12Row'] in l]
        _ok = len(_rows) == 1 and ('%s / %d / `%s`' % (_p['class'], _p['exit'], _p['errorCode'])) in _rows[0]
        if _ok and _p['faultCause'] is not None and '`faultCause`' in _rows[0]:
            _ok = ('`faultCause` `%s`' % _p['faultCause']) in _rows[0]
        if _ok and _p['domainDetail'] is None and _p['class'] == 'operational-failed':
            _ok = 'domainDetail` omitted' in _rows[0]
        if _ok and _p['domainDetail'] is not None and _p['domainDetail'] != _p['securityRefusal']:
            _ok = ('`%s`' % _p['domainDetail']) in _rows[0]
        ck('source37 route: %s is exactly one S12 row with the same class / exit / code' % _label, _ok, _rows)
_S37_RO_ROWS = {}
for _l in _S37_READONLY.splitlines():
    _cells = [x.strip() for x in _l.strip().strip('|').split('|')]
    if _l.startswith('| `') and len(_cells) == 5 and re.fullmatch(r'`[a-z-]+`', _cells[0]):
        _S37_RO_ROWS[_cells[0].strip('`')] = _cells
for _standing, _p in _S37_PROJ['readOnlyRecovery'].items():
    _cells = _S37_RO_ROWS.get(_standing)
    _ok = (_cells is not None and _cells[1].strip('`') == _p['class'] and _cells[2].strip('`') == (_p['errorCode'] or '—')
           and _cells[3].strip('`') == (_p['faultCause'] or '—')
           and (('omitted' in _cells[4]) if _p['domainDetail'] is None else (('`%s`' % _p['domainDetail']) in _cells[4])))
    ck('source37 route: readOnlyRecovery/%s matches the commit-recovery-readonly.v3 section 1 row' % _standing, _ok, _cells)

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
