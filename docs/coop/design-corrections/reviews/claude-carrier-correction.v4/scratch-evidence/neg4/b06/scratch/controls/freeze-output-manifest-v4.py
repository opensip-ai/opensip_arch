# Freeze the v4 output manifest: every deliverable, every patch before/after pair, every control.
# usage: python freeze-output-manifest-v4.py <source25Root> <runtimeRoot>
import hashlib
import json
import os
import sys

SRC, ROOT = sys.argv[1], sys.argv[2]
OUT = os.path.join(ROOT, 'scratch', 'output-manifest.json')
MANIFEST = ('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/'
            'design-corrections/reviews/codex-author-followup.v2/source-manifest.json')


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


man = {
    'artifact': 'opensip.claude-carrier-correction.output-manifest',
    'version': 4,
    'standing': ('Frozen output bytes of a bounded design/reference carrier correction, pass 4. '
                 'No acceptance, readiness, application, implementation authorization or '
                 'self-acceptance. Root assesses, merges with the separately authored PS01 and '
                 'PS04 work, runs the integrated suites, and obtains fresh independent review on '
                 'the merged frozen successor.'),
    'runtimeRoot': ROOT,
    'supersedes': {
        'v3Root': '/tmp/opensip-design-corrections/claude-carrier-correction.v3',
        'retained': 'scratch/v3-evidence/ carries the v3 reports, the v3 recovery draft and the '
                    'pre-renumbering fault-case bytes, all unchanged.',
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
}
for n in ('commit-recovery-plan.v1.json', 'implementation-boundaries-and-build-plan.md'):
    h, nb = sha_path(os.path.join(ROOT, n))
    man['bindings']['planningInputsBoundAtRuntimeRoot'].append(
        {'path': n, 'sha256': h, 'bytes': nb, 'source': 'root latest plan copy supplied in v4'})

man['addedFiles'] = tree('scratch/proposal')

c9 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c9-patches.json'), encoding='utf-8'))
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
     'scratch/out/c4-check.json', 'carrier reference validation including behavioural DDL probes'),
    ('C6', 'scratch/controls/c6-schedules.py', 'scratch/out/c6.json',
     'executable concurrency SCHEDULE controls for both races, with coverage assertions'),
    ('C7', 'scratch/controls/c7-gate-bits.py', 'scratch/out/c7.json',
     'PS05 atomic bit-state gate and the required-delivery phase handoff'),
    ('C8', 'scratch/controls/c8-incompatibility-inventory.py', 'scratch/out/c8.json',
     'exact inventory of which current operational rows the frozen carrier admits'),
    ('C9', 'scratch/controls/apply-owner-patches.py', 'scratch/out/c9-patches.json',
     'minimal owner patches against candidate25 and root latest planning inputs'),
    ('C10', 'scratch/controls/check-correction-v4.py', 'scratch/out/c10.json',
     'reference validation of the v4 additions, owner patches and no-minting claims'),
    ('C11', 'scratch/controls/c11-negative-v4.py', 'scratch/out/c11.json',
     'negative controls: model drifts that reintroduce each caught bug, plus artifact drifts'),
]
for cid, script, rep, what in CONTROLS:
    sh, sb = sha_path(os.path.join(ROOT, script))
    rh, rb = sha_path(os.path.join(ROOT, rep))
    man['executedControls'].append(
        {'id': cid, 'script': script, 'scriptSha256': sh, 'scriptBytes': sb,
         'report': rep, 'reportSha256': rh, 'reportBytes': rb, 'establishes': what})

c6 = json.load(open(os.path.join(ROOT, 'scratch/out/c6.json'), encoding='utf-8'))
c7 = json.load(open(os.path.join(ROOT, 'scratch/out/c7.json'), encoding='utf-8'))
c10 = json.load(open(os.path.join(ROOT, 'scratch/out/c10.json'), encoding='utf-8'))
c11 = json.load(open(os.path.join(ROOT, 'scratch/out/c11.json'), encoding='utf-8'))
c4 = json.load(open(os.path.join(ROOT, 'scratch/out/c4-check.json'), encoding='utf-8'))
man['results'] = {
    'scheduleControlSchedules': c6['totalSchedules'],
    'scheduleControlViolations': c6['violationCount'],
    'scheduleControlCoverageAllHeld': c6['allCoverageAssertionsHeld'],
    'gateModelSchedules': c7['schedules'],
    'gateModelViolations': c7['violationCount'],
    'gateModelAllFourStatesObserved': c7['allFourStatesObserved'],
    'carrierValidationPassed': c4['passed'], 'carrierValidationFailed': c4['failed'],
    'v4ValidationPassed': c10['passed'], 'v4ValidationFailed': c10['failed'],
    'negativeDrifts': c11['total'], 'negativeDetected': c11['detected'],
    'negativeUndetected': c11['undetectedDrifts'],
}
man['notEstablished'] = [
    'OS durability, fsync and F_FULLFSYNC behaviour, and real crash behaviour',
    'real SQLite behaviour under real crashes or real lock contention',
    'real concurrent processes: C6 interleaves a model, not two OS processes',
    'process isolation and real process control; F42 has no feasible model here',
    'Rust compilation, borrow checking or type-level enforcement of any API sketch',
    'any qualification gate; all twelve added fault cases are not-executed',
    'byte compatibility of the pinned prev_sha256 encoding with any real carrierFormat 1 or 2 '
    'instance, because no such instance and no fixture exists in the reviewed corpus',
    'the authorized settle-sweep that would move a crashed attempt out of the admitted phase',
]
man['dependenciesOwnedElsewhere'] = {
    'PS01': 'random store-instance identity and S9 private store-generation lineage; consumed '
            'here as an input only',
    'PS04': 'report release asset anchor; not touched here',
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
