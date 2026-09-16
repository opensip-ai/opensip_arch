# Control C17 - strict JSON admission and cross-file propagation for every SELECTED file.
#
# Two jobs root required:
#   1. STRICT duplicate-key rejection on ALL selected JSON files. The v6 checks used json.load,
#      which is last-wins, so a duplicate "admitted" key in attempt-custody survived undetected.
#   2. Propagation checks ACROSS files, so a law corrected in one document cannot be left
#      contradicted in another.
#
# usage: python c17-strict-json-propagation.py <runtimeRoot> <v6Root> <reportPath>
import hashlib
import json
import os
import re
import sys

ROOT, V6, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PROP = os.path.join(ROOT, 'scratch', 'proposal')
checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:400]})
    return ok


def strict_pairs(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError('DUPLICATE KEY: %s' % k)
        seen[k] = v
    return seen


def strict_load(path):
    return json.load(open(path, encoding='utf-8'), object_pairs_hook=strict_pairs)


# ---- 1. strict duplicate-key admission over every selected JSON -------------
selected_json, selected_all = [], []
for dp, dn, fn in os.walk(PROP):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        selected_all.append(p)
        if n.endswith('.json'):
            selected_json.append(p)

ck('selected JSON files were found', len(selected_json) >= 4, len(selected_json))
strict_results = {}
for p in selected_json:
    rel = os.path.relpath(p, PROP)
    try:
        strict_load(p)
        strict_results[rel] = 'admitted'
    except ValueError as e:
        strict_results[rel] = 'REJECTED: %s' % e
    ck('strict duplicate-key admission: ' + rel, strict_results[rel] == 'admitted',
       strict_results[rel])

# the v6 bytes must still fail, so the check is proven able to fail
v6ac = os.path.join(V6, 'scratch', 'proposal', 'attempt-custody.schema.v1.json')
v6_rejected = None
if os.path.exists(v6ac):
    try:
        strict_load(v6ac)
        v6_rejected = False
    except ValueError:
        v6_rejected = True
ck('the strict check rejects the v6 attempt-custody bytes, proving it can fail',
   v6_rejected is True, v6_rejected)

# embedded JSON-ish text in the SQL and markdown is not parsed; only real JSON is
ck('every selected JSON parses under the ordinary parser too',
   all(not v.startswith('REJECTED') for v in strict_results.values()))

# ---- 2. the selected file set and its stable normative paths ----------------
EXPECTED = {
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/commit-recovery-readonly.v3.md',
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'docs/coop/design-corrections/security/carrier-format.v3.md',
    'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
    'docs/coop/design-corrections/security/carrier-migration.v1.md',
    'docs/coop/design-corrections/security/check-carrier-v3.py',
    'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
}
actual = {os.path.relpath(p, PROP) for p in selected_all}
ck('the selected set is exactly the nine stable normative paths', actual == EXPECTED,
   sorted(actual ^ EXPECTED))
ck('no selected file sits outside docs/', all(a.startswith('docs/') for a in actual),
   sorted(a for a in actual if not a.startswith('docs/')))

# ---- 3. no normative file may require scratch/ or a superseded draft for LAW -
LAWWORDS = re.compile(r'\b(must|shall|requires?|is required|refuses?)\b', re.I)
bad_law = []
for p in selected_all:
    rel = os.path.relpath(p, PROP)
    for i, line in enumerate(open(p, encoding='utf-8', errors='replace')):
        if 'scratch/' not in line and 'owner-correction.v3' not in line:
            continue
        histmark = any(w in line.lower() for w in (
            'evidence', 'historical', 'executed', 'exercis', 'retained', 'carries no law',
            'reproduc', 'probe', 'control'))
        if LAWWORDS.search(line) and not histmark:
            bad_law.append('%s:%d %s' % (rel, i + 1, line.strip()[:90]))
ck('no selected file makes a scratch/ or owner-correction.v3 citation carry law', not bad_law,
   bad_law)

ac = strict_load(os.path.join(PROP, 'docs/v2/architecture/attempt-custody.schema.v1.json'))
disp = strict_load(os.path.join(
    PROP, 'docs/coop/design-corrections/security/carrier-dispatch.v3.json'))
rec = open(os.path.join(PROP, 'docs/v2/architecture/commit-recovery-readonly.v3.md'),
           encoding='utf-8').read()
fmt = open(os.path.join(PROP, 'docs/coop/design-corrections/security/carrier-format.v3.md'),
           encoding='utf-8').read()
mig = open(os.path.join(PROP, 'docs/coop/design-corrections/security/carrier-migration.v1.md'),
           encoding='utf-8').read()
cases = strict_load(os.path.join(PROP, 'docs/v2/architecture/carrier-fault-cases.v1.json'))
flat = {'rec': re.sub(r'\s+', ' ', rec), 'fmt': re.sub(r'\s+', ' ', fmt),
        'mig': re.sub(r'\s+', ' ', mig)}
casetext = json.dumps(cases)

# ---- 4. PS owners named at their integrated paths, consumed unchanged -------
ck('PS-01 is named at its integrated owner path',
   'docs/v2/architecture/store-instance-lineage.v1.json' in json.dumps(disp)
   and 'store-instance-lineage.v1.json' in json.dumps(ac)
   and 'store-instance-lineage.v1.json' in flat['rec'])
ck('PS-04 is named at its integrated owner path',
   'docs/v2/architecture/report-asset-binding.v1.json' in json.dumps(disp)
   and 'report-asset-binding.v1.json' in flat['rec'])
ck('no selected file redefines the PS-01 binding tuple',
   'storeInstanceId' not in json.dumps(ac) and 'storeInstanceId' not in flat['rec'])

# ---- 5. attempt-custody scoping propagation --------------------------------
acj = json.dumps(ac)
ck('attempt custody no longer claims the reservation makes the admitted phase existing law',
   'therefore the admitted phase, is existing law' not in acj)
ck('attempt custody states what existing law does NOT give',
   'whatExistingLawDoesNotGive' in ac['tracedExistingOwners'])
ck('attempt custody no longer claims no second record',
   'No second record' not in acj)
ck('attempt custody is scoped to durable-authoritative commit-capable attempts',
   'durable-authoritative commit-capable attempts' in acj)
ck('attempt custody excludes read-only and ephemeral modes',
   'excludedModes' in ac['tracedExistingOwners']
   and '--ephemeral' in ac['tracedExistingOwners']['excludedModes'])
ck('the phase description does not license a cleanup-path write',
   'guarded cleanup path' not in ac['properties']['phase']['description']
   and 'may NOT write' in ac['properties']['phase']['description'])
ck('the writer law does not name the cleanup path as a writer',
   not any('its cleanup path' in l for l in ac['laws']))
ck('the writer law explicitly forbids a stopped cleanup-only session write',
   any('stopped cleanup-only session may NOT write' in l for l in ac['laws']))
ck('the recovery document repeats the same scoping',
   'pre-use uniqueness rule' in flat['rec']
   and 'Read-only requests and `--ephemeral` acquire no row' in flat['rec'])
ck('the recovery document forbids the stopped session write',
   'stopped cleanup-only session may not write' in flat['rec'].lower())

# ---- 6. mandatory receipt joins --------------------------------------------
ck('the receipt join is mandatory on all five members, not caller-conditional',
   'where the caller supplies them' not in acj
   and 'MANDATORY on all five' in ac['joins']['toReceipt'])
ck('the receipt join says the values come from admission, never from caller fields',
   'never from caller-supplied request fields' in ac['joins']['toReceipt'])
ck('the receipt is still described as closed with no store binding',
   'NO storeGenerationDigest on the receipt' in ac['joins']['correctionNote'])

# ---- 7. dispatch algorithm propagation -------------------------------------
order = disp['openDispatch']['order']
ck('the dispatch order is the row-last algorithm, not table existence',
   isinstance(order, list) and all('step' in o for o in order), order)
firstconds = ' '.join(str(o.get('if', '')) for o in order[:4])
ck('no dispatch branch selects format 3 from table existence alone',
   'table grant_journal_v3 exists AND table carrier_format exists' not in json.dumps(order))
ck('the dispatch reads object names before any table content',
   'names only' in json.dumps(order[0]))
_o = json.dumps(order)


def before(a, b, text):
    """a must appear, b must appear, and a must precede b. Absence fails cleanly."""
    ia, ib = text.find(a), text.find(b)
    return ia != -1 and ib != -1 and ia < ib


ck('the partial-object refusal precedes the row read',
   before('some but not all', 'carrier_format row', _o))
ck('definition validation precedes the row read',
   before('any stored definition differs', 'carrier_format row', _o))
ck('the dispatch declares the row is read last', disp['openDispatch']
   .get('rowIsReadLastAndOnlyAfterValidation') is True)
ck('the dispatch names all seven carrierFormat 3 objects',
   len(disp['openDispatch']['sevenCarrierFormat3Objects']) == 7)
ck('the fresh-install path is stated and reads no absent table',
   disp['openDispatch']['freshInstallPath']['readsAbsentTables'] is False)
ck('the dispatch and the migration agree that detection is row-keyed',
   disp['migration']['detectionIsKeyedOnTheFormatRow'] is True
   and 'row' in disp['migration']['detectionOrder'])
ck('the prose pseudocode also reads the row last',
   before('some but not all seven names', 'read the carrier_format row', flat['fmt']))
ck('the prose states the malformed all-names case',
   'all seven names' in flat['fmt'] and 'wrong definitions' in flat['fmt'])
ck('the prose states the fresh-install path', 'FRESH INSTALL' in flat['fmt'])
ck('the stale five-case dispatch evidence is labelled historical',
   'historical evidence' in flat['fmt'].lower()
   and 'retained only as historical evidence' in json.dumps(disp['openDispatch']))

# ---- 8. second-migration and usability scoping ------------------------------
ck('the second-migration-aborts phrasing is scoped to historical evidence',
   'belongs to the historical C2 evidence' in flat['fmt']
   and 'not** the current recovery law' in flat['fmt'])
ck('the migration no longer claims an unmigrated carrier is fully usable',
   'fully usable by a format-aware core' not in flat['mig'])
ck('the migration scopes usability to historical reading versus current writes',
   'Historical reading is unaffected' in flat['mig']
   and 'Current authoritative writes are not possible' in flat['mig'])

# ---- 9. fault case propagation ---------------------------------------------
ids = [c['id'] for c in cases['cases']]
ck('the sixteen case ids are unchanged, F38 through F53',
   ids == ['F%d' % n for n in range(38, 54)], ids)
ck('every case is still not-executed',
   all(c['executionStanding'] == 'not-executed' for c in cases['cases']))
ck('F47 no longer requires a transition intent',
   'intent written only after every lease is held' not in casetext
   and 'NO installation transition intent or journal is written' in casetext)
ck('F48 scopes the typed refusal to a carrierFormat-AWARE core',
   'carrierFormat-AWARE core' in casetext and 'FORMAT-UNAWARE core cannot be made to refuse'
   in casetext)
ck('F50 replaces the retry narrative with stop-and-fresh-attempt',
   'COMMIT OR BARRIER UNCERTAINTY STOPS THE ATTEMPT' in casetext
   and 'never retries an act or proceeds' in casetext)
ck('F50 states act B is one explicit transaction and rejects bulk script',
   'ONE explicit transaction' in casetext and 'bulk-script execution is NOT an acceptable' in casetext)
ck('F52 no longer calls receipt-plus-admitted a contradiction',
   'A receipt present with the attempt still admitted is also a contradiction' not in casetext
   and 'LAWFUL pre-settle interval' in casetext)
ck('F52 covers the missing-custody-row case without a negative',
   'custody-unknown-legacy' in casetext)
ck('F52 distinguishes a logical tombstone from missing bytes and forbids forgery',
   'logical retained tombstone' in casetext and 'no receipt is ever forged' in casetext)
ck('F38 distinguishes the aborted action from the pre-sweep observer standing',
   'ACTUAL ABORTED ACTION' in casetext and 'OBSERVER standing before any sweep' in casetext)
ck('F38 is consistent with F36 on the sweep outcome',
   'settles refused' in casetext and 'terminal-not-committed' in casetext)
ck('F40 separates D9 terminality from durable settled custody',
   'TWO SENSES OF TERMINAL' in casetext
   and 'does NOT mean the private attempt-custody phase is settled' in casetext)
ck('F32 is not among the cases this correction edits',
   'F32' not in ids)

# ---- 10. recovery completeness: no operative rule deferred to v2 ------------
ck('no section defers an operative rule to the superseded v2 draft',
   'Unchanged from v2' not in rec and 'Unchanged in mechanism from v2' not in rec)
for frag in ('witnessSchema', 'bodySha256', 'PENDING` requiring', 'contiguity',
             'floorOk', 'domain-framed', 'run3', 'witness-committed-tail',
             'witness-pending-at-tail', 'sc-trust-floor', 'at most two', 'Determinism'):
    ck('recovery states the operative detail inline: ' + frag, frag in rec)
ck('recovery states the uncovered missing-custody-row case',
   'custody-unknown-legacy' in rec and 'never a negative' in flat['rec'].lower())
ck('recovery distinguishes logical retention from missing bytes',
   'logical retained record' in flat['rec'].lower()
   and 'raw both-absent observation' in flat['rec'].lower())
ck('recovery forbids forging a receipt from a tombstone',
   'never presented as a\nreceipt' in rec or 'never presented as a receipt' in flat['rec'])
ck('the two-tail clause is selected, with the may-drop wording gone',
   'SELECTED conservative diagnostic policy' in rec and 'Root may drop it' not in rec)

# ---- 11. v6 input provenance, cited not copied ------------------------------
v6files = {}
v6prop = os.path.join(V6, 'scratch', 'proposal')
for dp, dn, fn in os.walk(v6prop):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        v6files[os.path.relpath(p, v6prop)] = {
            'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest(),
            'bytes': os.path.getsize(p)}
ck('the v6 selected inputs are readable for citation', len(v6files) == 9, sorted(v6files))

rep = {'control': 'c17-strict-json-propagation',
       'strictJsonAdmission': strict_results,
       'v6AttemptCustodyRejectedByStrictCheck': v6_rejected,
       'selectedFiles': sorted(actual),
       'v6InputProvenance': v6files,
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
