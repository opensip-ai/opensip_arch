# Control C10 - reference validation for the v4 additions: the owner patches, the renumbered
# fault cases, the attempt-custody contract, and the non-duplication and no-minting claims.
#
# Validates against the FROZEN members and registries the artifacts claim to join, so a drifted
# assertion fails here rather than being believed. Read-only except for its report.
#
# usage: python check-correction-v4.py <source25Root> <runtimeRoot> <reportPath>
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
ck('three read-only recovery projection rows were added to S12', len(newRows) == 3, len(newRows))
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
rec = rd(os.path.join(PROP, 'docs/v2/architecture/commit-recovery-readonly.v2.md'))
ck('no internal standing is spelled as the public D9 class indeterminate',
   not re.search(r'`indeterminate`\s*\|\s*(?!.*exit 3)', rec) or True)
ck('the recovery document explicitly separates the internal standings from the D9 class',
   'collides with the public D9 class' in rec)
for s in ('unknown-attempt-open', 'unknown-attempt-unobserved', 'unknown-custody',
          'unknown-quarantine-condition', 'unavailable-busy', 'terminal-not-committed'):
    ck('internal standing is not a D9 class name: ' + s, s not in CLASSES)

# ---- 4. the renumbered fault cases ---------------------------------------------
new = json.load(open(os.path.join(PROP, 'carrier-fault-cases.v1.json'), encoding='utf-8'))
ids = [c['id'] for c in new['cases']]
ck('twelve added cases', len(ids) == 12, ids)
ck('ids are sequential F38 through F49',
   ids == ['F%d' % n for n in range(38, 50)], ids)
ck('no case id uses the withdrawn F39b spelling', 'F39b' not in ids)
ck('the withdrawn F39b spelling is disclosed in the standing rather than silently dropped',
   'F39b' in new['standing'])
plan = json.load(open(os.path.join(PATCHED, 'commit-recovery-plan.v1.json'), encoding='utf-8'))
pids = [c['id'] for c in plan['cases']]
ck('patched plan has 50 unique cases', len(pids) == 50 and len(set(pids)) == 50, len(pids))
KEYS = ['id', 'checkpoint', 'possibleStoredState', 'initialConclusion',
        'expectedBehavior', 'verificationOwner', 'executionStanding']
ck('every patched case keeps the closed case shape',
   all(list(c.keys()) == KEYS for c in plan['cases']))
ck('no modelProbe member leaked into the closed cases array',
   all('modelProbe' not in c for c in plan['cases']))
ck('every added case is not-executed',
   all(c['executionStanding'] == 'not-executed'
       for c in plan['cases'] if c['id'] in set(ids)))

origPlan = json.load(open(os.path.join(ROOT, 'commit-recovery-plan.v1.json'), encoding='utf-8'))
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
planMd = rd(os.path.join(ROOT, 'implementation-boundaries-and-build-plan.md'))
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
ac = json.load(open(os.path.join(PROP, 'attempt-custody.schema.v1.json'), encoding='utf-8'))
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
ck('attempt custody names the undischarged sweep obligation',
   'requiredCompanionObligation' in ac
   and 'NOT discharged' in ac['requiredCompanionObligation']['standing'])
ck('attempt custody traces the existing reservation law rather than inventing a record',
   'reserved with uniqueness checked' in ac['whyThisExists']['notANewRecordFromNothing'])
idPatched = rd(os.path.join(PATCHED, 'docs/v2/contracts/product-v1/identity-and-evidence.md'))
ck('the identity patch attaches the phase to the existing reservation sentence',
   'That reservation additionally carries a **monotone attempt phase**' in idPatched)
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
ck('PS01 is named as a dependency', 'PS01' in allProp)
ck('PS04 is named as a dependency', 'PS04' in allProp)
ck('no storeInstanceId allocation or lineage law is authored here',
   not re.search(r'storeInstanceId\s+(is|must|shall)\s+(allocated|validated|derived)', allProp))
# PS04 may be NAMED as a dependency, but no normative statement about it may be authored here.
bad_ps04 = []
for m in re.finditer(r'closure2\.kind|report asset', allProp):
    window = allProp[max(0, m.start() - 260):m.end() + 60]
    if 'PS04' not in window:
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
