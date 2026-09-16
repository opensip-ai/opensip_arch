# Freeze the v7 output manifest: every deliverable, every patch before/after pair, every control.
#
# The manifest records what THIS pass executed over THESE bytes. It does not carry forward v5 or
# v6 result counts, because the v7 bytes differ from both and the v6 checks did not cover them.
#
# usage: python freeze-output-manifest-v7.py <source25Root> <runtimeRoot>
import hashlib
import json
import os
import sys

SRC, ROOT = sys.argv[1], sys.argv[2]
OUT = os.path.join(ROOT, 'scratch', 'output-manifest.json')
MANIFEST = ('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/'
            'design-corrections/reviews/codex-author-followup.v2/source-manifest.json')
V6 = '/tmp/opensip-design-corrections/claude-carrier-correction.v6'
PLANROOT = '/tmp/opensip-design-corrections/claude-carrier-correction.v4'


def sha_path(p):
    b = open(p, 'rb').read()
    return hashlib.sha256(b).hexdigest(), len(b)


def tree(rel):
    root = os.path.join(ROOT, rel)
    rows = []
    for dp, dn, fn in os.walk(root):
        for n in sorted(fn):
            p = os.path.join(dp, n)
            h, nb = sha_path(p)
            rows.append({'path': os.path.relpath(p, ROOT), 'sha256': h, 'bytes': nb})
    return sorted(rows, key=lambda r: r['path'])


def rep(name):
    return json.load(open(os.path.join(ROOT, 'scratch/out', name), encoding='utf-8'))


man = {
    'artifact': 'opensip.claude-carrier-correction.output-manifest',
    'version': 7,
    'standing': ('Frozen output bytes of a bounded design/reference carrier correction, pass 7. '
                 'No acceptance, readiness, application, implementation authorization or '
                 'self-acceptance. Root assesses, merges with the separately authored PS01 and '
                 'PS04 work, owns F00-F37, the final sourcepins, the final normativekit and the '
                 'final integrated checks, and obtains fresh independent review on the merged '
                 'frozen successor.'),
    'runtimeRoot': ROOT,
    'supersedes': {
        'v6Root': V6,
        'citedNotCopied': ('The v6 selected inputs are cited by digest below. Nested historical '
                           'evidence was NOT copied into this runtime again.'),
        'resultsDoNotCarryForward': (
            'The v6 control results do NOT cover these bytes. Concretely: the v6 attempt-custody '
            'schema carried a DUPLICATE `admitted` key and every v6 check over it passed, because '
            'json.load is last-wins. Every JSON check in this pass admits through '
            'object_pairs_hook duplicate-key rejection, and C17 asserts that the v6 bytes ARE '
            'rejected by it, so the check is demonstrated able to fail.'),
    },
    'bindings': {},
    'addedFiles': [],
    'patchedOwnerFiles': [],
    'patchedPlanningInputs': [],
    'executedControls': [],
}

fh, fb = sha_path(MANIFEST)
sm = json.load(open(MANIFEST, encoding='utf-8'))
byPath = {f['path']: f for f in sm['files']}
man['bindings'] = {
    'candidateManifestSha256': fh,
    'candidateManifestMatchesExpected':
        fh == 'fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d',
    'candidateRoot': sm['snapshotRoot'],
    'candidateMemberCount': sm['fileCount'],
    'planningInputsBoundAtRuntimeRoot': [],
    'v6SelectedInputsCitedByDigest': [],
}
for n in ('commit-recovery-plan.v1.json', 'implementation-boundaries-and-build-plan.md'):
    h, nb = sha_path(os.path.join(PLANROOT, n))
    man['bindings']['planningInputsBoundAtRuntimeRoot'].append(
        {'path': n, 'sha256': h, 'bytes': nb,
         'source': 'root latest plan copy, read read-only from the immutable v4 runtime because '
                   'this runtime did not re-supply it'})

# v6 selected inputs: cited by digest, at the path they occupied in v6.
V6_SELECTED = [
    'scratch/proposal/attempt-custody.schema.v1.json',
    'scratch/proposal/carrier-fault-cases.v1.json',
    'scratch/proposal/docs/v2/architecture/commit-recovery-readonly.v3.md',
    'scratch/proposal/docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'scratch/proposal/docs/coop/design-corrections/security/carrier-format.v3.md',
    'scratch/proposal/docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
    'scratch/proposal/docs/coop/design-corrections/security/carrier-migration.v1.md',
    'scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py',
    'scratch/proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
]
for rel in V6_SELECTED:
    p = os.path.join(V6, rel)
    if os.path.exists(p):
        h, nb = sha_path(p)
        man['bindings']['v6SelectedInputsCitedByDigest'].append(
            {'v6Path': rel, 'sha256': h, 'bytes': nb, 'copiedIntoThisRuntime': False})

for n in ('ddl-atomicity.py', 'ddl-atomicity.json', 'root-F00-F37-proposed.json'):
    p_ = os.path.join(V6, n)
    if os.path.exists(p_):
        h, nb = sha_path(p_)
        man['bindings'].setdefault('rootSuppliedEarlierUnmodified', []).append(
            {'path': n, 'sha256': h, 'bytes': nb, 'runtime': 'v6', 'modified': False})

man['addedFiles'] = tree('scratch/proposal')

# the two records that moved to a stable normative path in this pass
man['stableNormativePathMoves'] = [
    {'from': 'scratch/proposal/attempt-custody.schema.v1.json (v6, runtime-relative)',
     'to': 'docs/v2/architecture/attempt-custody.schema.v1.json',
     'reason': 'a stable normative record must not be addressed through a correction run'},
    {'from': 'scratch/proposal/carrier-fault-cases.v1.json (v6, runtime-relative)',
     'to': 'docs/v2/architecture/carrier-fault-cases.v1.json',
     'reason': 'same; the F38-F53 cases are consumed by the recovery plan'},
]

c9 = rep('c9-patches.json')
for bucket, key in (('ownerFiles', 'patchedOwnerFiles'),
                    ('planningFiles', 'patchedPlanningInputs')):
    for f in c9[bucket]:
        ph, pb = sha_path(os.path.join(ROOT, 'scratch', 'patched', f['path']))
        dh, db = sha_path(os.path.join(ROOT, f['patch']))
        row = {'path': f['path'], 'source': f['source'],
               'beforeSha256': f['beforeSha256'], 'beforeBytes': f['beforeBytes'],
               'afterSha256': ph, 'afterBytes': pb,
               'afterMatchesApplyRun': ph == f['afterSha256'],
               'patchPath': f['patch'], 'patchSha256': dh, 'patchBytes': db,
               'addedLines': f['addedLines'], 'removedLines': f['removedLines']}
        if bucket == 'ownerFiles':
            m = byPath.get(f['path'])
            row['beforeMatchesFrozenManifest'] = bool(
                m and m['sha256'] == f['beforeSha256'] and m['bytes'] == f['beforeBytes'])
        man[key].append(row)

CONTROLS = [
    ('C1', 'scratch/controls/c1.py', 'scratch/out/c1.json',
     'inherited carrier laws, set algebra, digest semantics, 14-row reconcile_witness table'),
    ('C2', 'scratch/controls/c2.py', 'scratch/out/c2.json',
     'carrierFormat 3 DDL probes, migration, open dispatch, anchor-field discrimination'),
    ('C4b', 'scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py',
     'scratch/out/c4-check.json',
     'selected carrier validator: behavioural DDL probes, and new in v7, strict duplicate-key '
     'admission of every selected JSON file, the stable normative paths, the row-last dispatch '
     'order and the no-run-directory-for-LAW scan'),
    ('C6', 'scratch/controls/c6-schedules.py', 'scratch/out/c6.json',
     'executable concurrency SCHEDULE controls for both races, with coverage assertions'),
    ('C7', 'scratch/controls/c7-gate-bits.py', 'scratch/out/c7.json',
     'PS05 atomic bit-state gate and the required-delivery phase handoff'),
    ('C8', 'scratch/controls/c8-incompatibility-inventory.py', 'scratch/out/c8.json',
     'exact inventory of which current operational rows the frozen carrier admits'),
    ('C9', 'scratch/controls/apply-owner-patches.py', 'scratch/out/c9-patches.json',
     'minimal owner patches against candidate25 and root latest planning inputs'),
    ('C10', 'scratch/controls/check-correction-v7.py', 'scratch/out/c10.json',
     'bounded reference validation of the additions, owner patches and no-minting claims, '
     'repointed to the stable normative paths and to the corrected tracedExistingOwners shape'),
    ('C12', 'scratch/controls/c12-d9-projection.py', 'scratch/out/c12.json',
     'every recovery projection and post-publication outcome validated against the actual frozen '
     'StepTermination schema, using only existing vocabulary members'),
    ('C13', 'scratch/controls/c13-migration-prefixes.py', 'scratch/out/c13.json',
     'root counterexample reproduced, the store-gc authorization traced, and fault-prefix '
     'recovery over every durable prefix of the three migration acts'),
    ('C14', 'scratch/controls/c14-settlement.py', 'scratch/out/c14.json',
     'the settlement matrix, the purged-receipt law, the proposed private DDL and the sweep '
     'decision matrix, reading the schema at its stable path under strict admission'),
    ('C15', 'scratch/controls/c15-root-atomicity-replay.py', 'scratch/out/c15.json',
     "root's own AST extraction and injected SQL failure replayed against the corrected act B"),
    ('C16', 'scratch/controls/c16-receipt-join.py', 'scratch/out/c16.json',
     'the receipt join against the actual closed eight-member commit-receipt and the actual '
     'thirteen-field association, with store-binding mismatch caught at the owning join'),
    ('C17', 'scratch/controls/c17-strict-json-propagation.py', 'scratch/out/c17.json',
     'NEW in v7: strict duplicate-key admission over the selected JSON set, with the v6 '
     'attempt-custody bytes asserted to be REJECTED, plus the six propagation corrections'),
    ('C18', 'scratch/controls/c18-selected-dispatch.py', 'scratch/out/c18.json',
     'NEW in v7: the SELECTED dispatch algorithm executed on lawful prefixes, partial shapes, '
     'all-names-but-malformed shapes, inherited carriers and the fresh empty install, asserting '
     'that no format row is read before the object set is validated'),
    ('C19', 'scratch/controls/c19-negative-v7.py', 'scratch/out/c19.json',
     'NEW in v7: negative controls that reintroduce each v7 defect, including the duplicate key '
     'and the law-deferral to a correction-run directory'),
]
for cid, script, r, what in CONTROLS:
    sh, sb = sha_path(os.path.join(ROOT, script))
    rh, rb = sha_path(os.path.join(ROOT, r))
    man['executedControls'].append(
        {'id': cid, 'script': script, 'scriptSha256': sh, 'scriptBytes': sb,
         'report': r, 'reportSha256': rh, 'reportBytes': rb, 'establishes': what})

c6, c7, c10, c4 = rep('c6.json'), rep('c7.json'), rep('c10.json'), rep('c4-check.json')
c12, c13, c14 = rep('c12.json'), rep('c13.json'), rep('c14.json')
c15, c16, c17 = rep('c15.json'), rep('c16.json'), rep('c17.json')
c18, c19 = rep('c18.json'), rep('c19.json')
cases = json.load(open(os.path.join(ROOT, 'scratch/proposal/docs/v2/architecture/'
                                    'carrier-fault-cases.v1.json'), encoding='utf-8'))
man['results'] = {
    'scheduleControlSchedules': c6['totalSchedules'],
    'scheduleControlViolations': c6['violationCount'],
    'scheduleControlCoverageAllHeld': c6['allCoverageAssertionsHeld'],
    'gateModelSchedules': c7['schedules'],
    'gateModelViolations': c7['violationCount'],
    'gateModelAllFourStatesObserved': c7['allFourStatesObserved'],
    'carrierValidationPassed': c4['passed'], 'carrierValidationFailed': c4['failed'],
    'boundedValidatorPassed': c10['passed'], 'boundedValidatorFailed': c10['failed'],
    'd9ProjectionPassed': c12['passed'], 'd9ProjectionFailed': c12['failed'],
    'migrationPrefixPassed': c13['passed'], 'migrationPrefixFailed': c13['failed'],
    'settlementPassed': c14['passed'], 'settlementFailed': c14['failed'],
    'actBAtomicityReplayPassed': c15['passed'], 'actBAtomicityReplayFailed': c15['failed'],
    'v5ActBSurvivingObjects': c15['rootPriorFinding']['tablesSurvivingFailure'],
    'correctedActBSurvivingObjects': c15['v6FaultedRun']['tablesSurvivingFailure'],
    'receiptJoinPassed': c16['passed'], 'receiptJoinFailed': c16['failed'],
    'strictJsonPropagationPassed': c17['passed'], 'strictJsonPropagationFailed': c17['failed'],
    'v6AttemptCustodyRejectedByStrictAdmission': c17.get('v6AttemptCustodyRejectedByStrictCheck'),
    'selectedDispatchPassed': c18['passed'], 'selectedDispatchFailed': c18['failed'],
    'negativeDrifts': c19['drifts'], 'negativeDetected': c19['detected'],
    'negativeUndetected': c19['undetected'], 'negativeCleanFailures': c19['cleanFailures'],
    'addedFaultCases': len(cases['cases']),
    'addedFaultCaseIds': [c['id'] for c in cases['cases']],
    'addedFaultCasesAllNotExecuted': all(c['executionStanding'] == 'not-executed'
                                         for c in cases['cases']),
}
man['notEstablished'] = [
    'OS durability, fsync and F_FULLFSYNC behaviour, and real crash behaviour',
    'real SQLite behaviour under real crashes or real lock contention',
    'real concurrent processes: C6 interleaves a model, not two OS processes',
    'process isolation and real process control; F42 has no feasible model here',
    'Rust compilation, borrow checking or type-level enforcement of any API sketch',
    'any qualification gate; all SIXTEEN added fault cases F38-F53 are not-executed',
    'byte compatibility of the pinned prev_sha256 encoding with any real carrierFormat 1 or 2 '
    'instance, because no such instance and no fixture exists in the reviewed corpus',
    'act B atomicity beyond in-memory transaction behaviour: C13 and C15 establish that the '
    'corrected helper rolls back as one transaction, and nothing about fsync or real crashes',
    'the authorized settlement sweep as an executed behaviour: it is specified and its decision '
    'matrix is reference-executed in C14, which is NOT a qualification of the sweep',
    'that the v6 control results cover these bytes; they do not, and are not reused here',
    'that the no-run-directory-for-LAW scan is exhaustive: its evidence-versus-law classifier is '
    'LEXICAL, so a law deferral phrased as an ordinary evidence citation would pass it',
    'that the selected dispatch is correct on a real SQLite file that a foreign writer is '
    'concurrently mutating: C18 drives in-memory databases through the same helper',
    'the F00-F37 dispositions, the final sourcepins, the final normativekit and the final '
    'integrated checks, which are root-owned and untouched here',
]
man['standingCorrections'] = {
    'correctedInThisPass': [
        'the selected attempt-custody schema carried a DUPLICATE `admitted` key; the key is now '
        'single and merged, and every selected JSON file is admitted under strict duplicate-key '
        'rejection in C4b, C9, C10, C14 and C17',
        'the v6 claim that identity section 2 already made every attempt reservation DURABLE is '
        'WITHDRAWN: the reservation is a pre-use uniqueness rule, and the durable scoped record '
        'is an addition, not a restatement',
        'openDispatch.order detected carrierFormat 3 by table existence while the migration '
        'section said detection is keyed on the format row; the order is now row-last, refuses '
        'a partial object set and validates all seven definitions before any row read',
        'carrier-migration section 6 deferred the PS-01 lineage allocation LAW to '
        '`owner-correction.v3`; it now cites the stable owner path and restates nothing',
    ],
    'previouslyStaleMetadata': [
        'the v5 manifest said twelve additions; the correct count is sixteen, F38 through F53',
        'the v5 manifest listed the settlement sweep as an unspecified remaining obligation; it '
        'is specified in commit-recovery-readonly.v3.md section 4 and its DDL placement is the '
        'selected storage-owned evidence ledger, so only its EXECUTION remains, as qualification',
        'the v6 manifest carried v6 control results as though they covered the selected bytes; '
        'this manifest carries only results executed over the bytes frozen here',
    ],
    'notArchitecturalGaps': [
        'unexecuted real SQLite crashes, processes and OS gates are product qualification',
        'the format-unaware old-core detection limitation is a selected disclosed limitation, '
        'with release ordering as an implementation and release obligation',
        'retained-custody-only confirmation and chain_law 1 are selected limits',
        'the two-agreeing-tails clause is a selected conservative diagnostic policy',
    ],
}
man['dependenciesOwnedElsewhere'] = {
    'PS01': 'docs/v2/architecture/store-instance-lineage.v1.json owns the random store-instance '
            'identity and the S9 private store-generation lineage; consumed here as an unchanged '
            'input only, with no binding tuple or digest shape redefined',
    'PS04': 'docs/v2/architecture/report-asset-binding.v1.json owns the report release asset '
            'anchor; not touched here',
    'rootOwned': 'F00-F37, the final sourcepins, the final normativekit and the final integrated '
                 'checks are root-owned and are not edited in this runtime',
}

with open(OUT, 'w', encoding='utf-8') as fh2:
    fh2.write(json.dumps(man, indent=1) + '\n')
print('WROTE', OUT)
print('added %d, owner patches %d, planning patches %d, controls %d'
      % (len(man['addedFiles']), len(man['patchedOwnerFiles']),
         len(man['patchedPlanningInputs']), len(man['executedControls'])))
print('owner before-bytes match frozen manifest:',
      [f['beforeMatchesFrozenManifest'] for f in man['patchedOwnerFiles']])
print(json.dumps(man['results'], indent=1))
