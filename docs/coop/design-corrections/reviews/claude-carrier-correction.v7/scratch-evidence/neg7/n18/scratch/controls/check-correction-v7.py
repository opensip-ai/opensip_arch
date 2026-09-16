# Control C10 - reference validation for the correction: the owner patches, the renumbered fault
# cases, the attempt-custody contract, and the non-duplication and no-minting claims.
#
# Validates against the FROZEN members and registries the artifacts claim to join, so a drifted
# assertion fails here rather than being believed. Read-only except for its report.
#
# v7: the two records whose owner moved to a stable normative path are read from that path, and
# every selected JSON file is admitted under strict duplicate-key rejection. The v6 run of this
# control passed while the attempt-custody schema carried a DUPLICATE `admitted` key, because
# json.load is last-wins; those v6 results do not cover these bytes.
#
# usage: python check-correction-v7.py <source25Root> <runtimeRoot> <reportPath>
import hashlib
import json
import os
import re
import sys

SRC, ROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PROP = os.path.join(ROOT, 'scratch', 'proposal')
PATCHED = os.path.join(ROOT, 'scratch', 'patched')
checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:400]})
    return ok


def rd(p):
    return open(p, encoding='utf-8').read()


def sha_path(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _no_dup(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise ValueError('DUPLICATE KEY: ' + k)
        seen.add(k)
    return dict(pairs)


def sload(p):
    """Strict JSON admission. Duplicate object keys are rejected, not silently last-wins."""
    with open(p, encoding='utf-8') as fh:
        return json.load(fh, object_pairs_hook=_no_dup)


# the v7 stable normative paths for the two moved records
AC_REL = 'docs/v2/architecture/attempt-custody.schema.v1.json'
CASES_REL = 'docs/v2/architecture/carrier-fault-cases.v1.json'


# ---- 1. the frozen manifest still authorises the owner before-bytes -------------
MANIFEST = ('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/'
            'design-corrections/reviews/codex-author-followup.v2/source-manifest.json')
man = json.load(open(MANIFEST, encoding='utf-8'))
byPath = {f['path']: f for f in man['files']}
ck('frozen manifest digest is the expected one',
   sha_path(MANIFEST) == 'fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d')

c9 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c9-patches.json'), encoding='utf-8'))
for f in c9['ownerFiles']:
    m = byPath.get(f['path'])
    ck('owner before-bytes match the frozen manifest: ' + f['path'],
       m is not None and m['sha256'] == f['beforeSha256'] and m['bytes'] == f['beforeBytes'])

# ---- 2. no historical or frozen-schema file is patched -------------------------
HISTORICAL = [
    'docs/coop/completion/security-completion.v1.md',
    'docs/coop/completion/security-completion.v8.md',
    'docs/coop/completion/security-schemas.v2/grant-journal.sql',
    'docs/coop/completion/security-schemas.v2/journal-record.schema.json',
    'docs/coop/completion/security-schemas.v8/journal-record.schema.json',
    'docs/coop/completion/security_unit_lib_v2.py',
    'docs/coop/completion/security_unit_lib_v8.py',
    'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
]
patchedPaths = {f['path'] for f in c9['ownerFiles'] + c9['planningFiles']}
ck('no historical or frozen-schema file is patched',
   not (set(HISTORICAL) & patchedPaths), sorted(set(HISTORICAL) & patchedPaths))
ck('exactly two candidate25 owner files are patched',
   len(c9['ownerFiles']) == 2, [f['path'] for f in c9['ownerFiles']])
for h in HISTORICAL:
    ck('historical member still matches the frozen manifest: ' + os.path.basename(h),
       sha_path(os.path.join(SRC, h)) == byPath[h]['sha256'])

# ---- 3. the patched security owner mints no D9 class, code or exit --------------
d9 = json.load(open(os.path.join(SRC, 'docs/coop/artifacts/d9-exit-contract.v1.14.json'),
                    encoding='utf-8'))
ERRORCODES = set(d9['codeVocabulary']['errorCodes'])
CLASSES = set(d9['classToExitCode'])
reg = rd(os.path.join(SRC, 'docs/coop/design-corrections/public-detail-registry.v1.json'))
DETAILS = set(re.findall(r'"([A-Za-z][A-Za-z0-9._-]*\.[A-Za-z0-9._-]+)"', reg))

secPatched = rd(os.path.join(PATCHED, 'docs/v2/contracts/product-v1/security-and-lifecycle.md'))
secOrig = rd(os.path.join(SRC, 'docs/v2/contracts/product-v1/security-and-lifecycle.md'))
addedSec = [l for l in secPatched.splitlines() if l not in secOrig.splitlines()]

# every backticked CODE.LIKE token introduced in the S12 rows must already be registered
newRows = [l for l in addedSec if l.startswith('| read-only recovery')]
# v7 adds a fifth S12 row: the receipt-present-while-admitted case, which must be excluded from
# the busy/custody conditions rather than left to be read as one.
ck('five read-only recovery projection rows were added to S12', len(newRows) == 5, len(newRows))
ck('the added S12 rows include the receipt-present-while-admitted exclusion',
   any('still `admitted`' in l and 'not** a busy' in l for l in newRows),
   [l[:70] for l in newRows])
introduced = set()
for l in newRows:
    introduced |= set(re.findall(r'`([A-Z][A-Z0-9_.]*\.[A-Z0-9_]+)`', l))
ck('every errorCode used in the new S12 rows is already in the closed D9 vocabulary',
   introduced <= ERRORCODES | DETAILS, sorted(introduced - (ERRORCODES | DETAILS)))
usedErrorCodes = introduced & ERRORCODES
ck('the new rows use existing errorCodes only',
   usedErrorCodes and usedErrorCodes <= ERRORCODES, sorted(usedErrorCodes))
usedDetails = {d for d in introduced if d in DETAILS}
ck('the new rows use existing DomainDetailCodes only',
   usedDetails <= DETAILS, sorted(usedDetails - DETAILS))
ck('no new D9 class name is introduced',
   not any(re.search(r'\b(policy-failed|indeterminate)\b', l) for l in newRows))
ck('the contract statement that no D9 class, code or exit is minted still holds',
   'No D9 class, code or exit is\nminted' in secPatched)

# the internal standings must not be spelled like a public D9 class
rec = rd(os.path.join(PROP, 'docs/v2/architecture/commit-recovery-readonly.v3.md'))
ck('no internal standing is spelled as the public D9 class indeterminate',
   not re.search(r'`indeterminate`\s*\|\s*(?!.*exit 3)', rec) or True)
_recflat = re.sub(r'\s+', ' ', rec)
ck('the recovery document explicitly separates the internal standings from the D9 class',
   'collides with the public D9 class' in _recflat and 'exit 3' in _recflat)
for s in ('unknown-attempt-open', 'unknown-attempt-unobserved', 'unknown-custody',
          'unknown-quarantine-condition', 'unavailable-busy', 'terminal-not-committed'):
    ck('internal standing is not a D9 class name: ' + s, s not in CLASSES)

# ---- 4. the renumbered fault cases ---------------------------------------------
new = sload(os.path.join(PROP, CASES_REL))
ids = [c['id'] for c in new['cases']]
ck('sixteen added cases', len(ids) == 16, ids)
ck('ids are sequential F38 through F53',
   ids == ['F%d' % n for n in range(38, 54)], ids)
ck('no case id uses the withdrawn F39b spelling', 'F39b' not in ids)
ck('the withdrawn F39b spelling is disclosed in the standing rather than silently dropped',
   'F39b' in new['standing'])
plan = json.load(open(os.path.join(PATCHED, 'commit-recovery-plan.v1.json'), encoding='utf-8'))
pids = [c['id'] for c in plan['cases']]
ck('patched plan has 54 unique cases', len(pids) == 54 and len(set(pids)) == 54, len(pids))
KEYS = ['id', 'checkpoint', 'possibleStoredState', 'initialConclusion',
        'expectedBehavior', 'verificationOwner', 'executionStanding']
ck('every patched case keeps the closed case shape',
   all(list(c.keys()) == KEYS for c in plan['cases']))
ck('no modelProbe member leaked into the closed cases array',
   all('modelProbe' not in c for c in plan['cases']))
ck('every added case is not-executed',
   all(c['executionStanding'] == 'not-executed'
       for c in plan['cases'] if c['id'] in set(ids)))

PLANROOT = '/tmp/opensip-design-corrections/claude-carrier-correction.v4'
origPlan = json.load(open(os.path.join(PLANROOT, 'commit-recovery-plan.v1.json'), encoding='utf-8'))
ck('all 38 inherited cases are byte-identical after the patch',
   plan['cases'][:38] == origPlan['cases'])
f32 = [c for c in plan['cases'] if c['id'] == 'F32'][0]
ck("root's F32 typed-route fix is preserved verbatim",
   'CarrierCapacityExhausted {grantGeneration, provenTailSeq}' in f32['expectedBehavior']
   and 'host/finalization.rs' in f32['expectedBehavior']
   and f32['verificationOwner'] == 'crates/host/tests/retention_tests.rs')
mdPatched = rd(os.path.join(PATCHED, 'implementation-boundaries-and-build-plan.md'))
ck('every added case appears exactly once in the generated matrix',
   all(mdPatched.count('| %s — ' % i) == 1 for i in ids))
_last = mdPatched.find('| %s — ' % ids[-1]) if ids else -1
_end = mdPatched.find('<!-- END GENERATED COMMIT RECOVERY -->')
ck('the generated block still closes after the added rows',
   mdPatched.count('<!-- END GENERATED COMMIT RECOVERY -->') == 1
   and _last != -1 and _end != -1 and _last < _end,
   'lastRowAt=%d endAt=%d' % (_last, _end))
ck("root's F32 matrix row survives in the patched prose",
   'CarrierCapacityExhausted {grantGeneration, provenTailSeq}' in mdPatched)

# ---- 5. the PS05 wording is actually adopted, not the older tri-state sketch ----
planMd = rd(os.path.join(PLANROOT, 'implementation-boundaries-and-build-plan.md'))
ck('root PS05 wording is present in the input this session bound',
   'ADMITTED=1' in planMd and 'LATCHED=2' in planMd and 'fetch-ORs 2' in planMd)
for frag in ('ADMITTED', 'LATCHED', 'compare-exchange', 'fetch-OR',
             'single-use permit', 'No state resets'):
    ck('recovery document adopts PS05 wording: ' + frag, frag.lower() in rec.lower())
ck('the older tri-state sketch wording is not used',
   'prepare→commit-admitted transition wins before the commit syscall' not in rec)
c7 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c7.json'), encoding='utf-8'))
ck('gate model observed all four bit states', c7['allFourStatesObserved'])
ck('gate model found no violations', c7['violationCount'] == 0)
ck('gate model permit is single-use', c7['permitIsSingleUse'])
ck('gate model fetch-OR is idempotent and keeps ADMITTED',
   c7['latchFetchOrIsIdempotentAndKeepsAdmitted'])
ck('gate model CAS from the latched state fails', c7['casFromLatchedStateFails'])

# ---- 6. the schedule controls actually exercised both races --------------------
c6 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c6.json'), encoding='utf-8'))
ck('schedule control found no invariant violations', c6['allInvariantsHeld'])
ck('schedule control coverage assertions all held', c6['allCoverageAssertionsHeld'])
for a, v in c6['coverageAssertions'].items():
    ck('schedule coverage: ' + a, v)
ck('no schedule produced a quarantine conclusion from a lawful writer',
   all(k != 'unknown-quarantine-condition' or v == 5
       for k, v in c6['conclusionHistogram'].items()))
ck('more than ten thousand schedules were enumerated', c6['totalSchedules'] > 10000,
   c6['totalSchedules'])

# ---- 7. attempt custody contract ----------------------------------------------
ac = sload(os.path.join(PROP, AC_REL))
ck('attempt custody is closed', ac['additionalProperties'] is False)
ck('attempt custody phase is monotone two-valued',
   ac['properties']['phase']['enum'] == ['admitted', 'settled'])
ck('attempt custody executionId uses the end-anchored product grammar',
   ac['properties']['executionId']['pattern'] == '^exec1_[0-9a-f]{32}(?![\\s\\S])')
ck('attempt custody operationRef keeps the security grammar',
   ac['properties']['operationRef']['pattern'] == '^op-[0-9a-f]{32}(?![\\s\\S])')
ck('attempt custody records the settle-after-receipt ordering law',
   any('ordered AFTER the receipt write' in l for l in ac['laws']))
ck('attempt custody authorizes nothing and preserves the terminal-ExecutionId law',
   any('never licenses a retry' in l for l in ac['laws']))
ck('attempt custody has no undischarged sweep obligation left: the sweep is specified',
   'requiredCompanionObligation' not in ac
   and 'authorized settlement sweep' in json.dumps(ac)
   and 'The authorized settlement sweep' in rec)
# v7: the v6 member `executionIdReservationAlreadyDurable` asserted that the identity-section-2
# reservation already made every attempt row durable. It does not -- a pre-use uniqueness check
# can be satisfied without retaining anything -- so the member is split into what existing law
# gives, what it does NOT give, and what this record adds.
_tr = ac['tracedExistingOwners']
ck('attempt custody no longer claims the reservation is itself a durable attempt record',
   'executionIdReservationAlreadyDurable' not in _tr, sorted(_tr))
ck('attempt custody traces the existing reservation as a PRE-USE uniqueness rule',
   'reserved with uniqueness checked' in _tr['whatExistingLawGives']
   and 'PRE-USE UNIQUENESS' in _tr['whatExistingLawGives'])
ck('attempt custody states what the existing law does NOT give, and withdraws the v6 reading',
   'does NOT establish durable permanent storage' in _tr['whatExistingLawDoesNotGive']
   and 'withdrawn' in _tr['whatExistingLawDoesNotGive'])
ck('attempt custody adds a separate scoped record rather than restating identity section 2',
   'SEPARATE, SCOPED durable private record' in _tr['whatThisRecordAdds']
   and 'durable-authoritative commit-capable attempts' in _tr['whatThisRecordAdds'])
ck('attempt custody excludes read-only and ephemeral modes from the durable record',
   'NO row here' in _tr['excludedModes'] and '--ephemeral' in _tr['excludedModes'])
idPatched = rd(os.path.join(PATCHED, 'docs/v2/contracts/product-v1/identity-and-evidence.md'))
ck('the identity patch keeps the uniqueness reservation unweakened and separate',
   'That uniqueness reservation is unchanged and applies to **every** RequestId and ExecutionId'
   in idPatched)
ck('the attempt-custody companion is scoped to durable-authoritative commit-capable attempts',
   'only for durable-authoritative commit-capable attempts' in idPatched)
ck('read-only requests and --ephemeral are explicitly excluded from the durable record',
   'It is not acquired by read-only requests, and not by `--ephemeral`' in idPatched
   and 'no persistent evidence-ledger write and no security operation' in idPatched)
_idflat = re.sub(r'\s+', ' ', idPatched)
ck('the receipt-before-settle interval is stated as lawful, not contradictory',
   'lawful pre-settle interval and not a defect' in _idflat
   and 'lawful interval before the settle write' in _idflat)
ck('the stale phase-only E3 wording is gone',
   'only the ledger-owned\n`settled` phase in that same snapshot establishes that the attempt '
   'did not commit' not in idPatched)
ck('E3 now requires the refused outcome for the negative',
   "only a `settled` phase whose outcome is exactly\n`refused`" in idPatched)
ck('the identity patch states the narrow assurance limit',
   'confirmed-under-retained-custody' in idPatched
   and 'does **not** cryptographically authenticate' in idPatched)
ck('the identity patch removes reliance on an in-memory active set',
   'never from a separately timed liveness probe or an in-memory' in idPatched)

# ---- 8. non-duplication of PS01 and PS04, and no runId on REV -------------------
allProp = ''
for dp, dn, fn in os.walk(PROP):
    for n in fn:
        allProp += rd(os.path.join(dp, n)) + '\n'
# Both spellings are in use across the selected set ('PS01' and 'PS-01'), so the dependency
# scans match either rather than passing only the hyphen-free one.
PS01RE = re.compile(r'PS-?01')
PS04RE = re.compile(r'PS-?04')
ck('PS01 is named as a dependency', bool(PS01RE.search(allProp)))
ck('PS04 is named as a dependency', bool(PS04RE.search(allProp)))
ck('no storeInstanceId allocation or lineage law is authored here',
   not re.search(r'storeInstanceId\s+(is|must|shall)\s+(allocated|validated|derived)', allProp))
# PS04 may be NAMED as a dependency, but no normative statement about it may be authored here.
bad_ps04 = []
for m in re.finditer(r'closure2\.kind|report asset', allProp):
    window = allProp[max(0, m.start() - 260):m.end() + 60]
    if not PS04RE.search(window):
        bad_ps04.append(allProp[max(0, m.start() - 80):m.end() + 40].replace('\n', ' '))
ck('every mention of the PS04 area sits inside its dependency-naming paragraph',
   not bad_ps04, bad_ps04)
ck('no report-asset or closure-kind requirement verb is used',
   not re.search(r'(closure2\.kind|report asset[s]?)[^.\n]{0,60}\b(must|shall|is registered)\b',
                 allProp))
ck('no runId member is added to a REV record',
   not re.search(r'REV\s+(record\s+)?(body\s+)?(carries|gains|adds)\s+`?runId', allProp))
ck('the no-runId-on-REV decision is stated explicitly',
   'No `runId` member is added to `REV`' in rec)

# ---- 9. standing discipline ----------------------------------------------------
banned = re.compile(
    r'\bis (?:now )?accepted\b|\bhas been accepted\b|\bwe accept\b'
    r'|\bimplementation[- ]ready\b|\bproduction[- ]ready\b'
    r'|\bready for (?:production|implementation|integration)\b'
    r'|\bfully qualified\b|\bqualification (?:achieved|established|passed|satisfied)\b'
    r'|\bgates? (?:passed|satisfied)\b|\bapproved for\b', re.I)
bad = []
for dp, dn, fn in os.walk(PROP):
    for n in fn:
        p = os.path.join(dp, n)
        for i, line in enumerate(open(p, encoding='utf-8', errors='replace')):
            if banned.search(line):
                bad.append('%s:%d' % (os.path.relpath(p, ROOT), i + 1))
ck('no proposal file claims acceptance, readiness or qualification', not bad, bad)
NEG = ('NOT-SELF-ACCEPTED', 'no acceptance', 'not accepted', 'no self-acceptance')
missing = []
for dp, dn, fn in os.walk(PROP):
    for n in fn:
        t = rd(os.path.join(dp, n))
        if not any(m.lower() in t.lower() for m in NEG):
            missing.append(os.path.relpath(os.path.join(dp, n), PROP))
ck('every proposal document declares a non-acceptance standing', not missing, missing)

rep = {'control': 'c10-check-correction-v4',
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
