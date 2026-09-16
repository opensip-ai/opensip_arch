# Freeze the output manifest: hashes every deliverable plus the bindings it was authored against.
# usage: python freeze-output-manifest.py <source25Root> <runtimeRoot>
import hashlib
import json
import os
import sys

SRC, ROOT = sys.argv[1], sys.argv[2]
OUT = os.path.join(ROOT, 'scratch', 'output-manifest.json')

FROZEN_MANIFEST = ('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/'
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
    'version': 3,
    'standing': ('Frozen output bytes of a bounded design/reference carrier correction. '
                 'No acceptance, readiness, application, implementation authorization or '
                 'self-acceptance. Root assesses and integrates; a fresh substantive review '
                 'on these frozen successor bytes remains pending.'),
    'runtimeRoot': ROOT,
    'bindings': {},
    'addedFiles': [],
    'patchedPlanningInputs': [],
    'executedControls': [],
}

# bindings: the four bound inputs and the frozen Source25 manifest
im = json.load(open(os.path.join(ROOT, 'input-manifest.json'), encoding='utf-8'))
bound = []
for f in im['files']:
    h, nb = sha_path(os.path.join(ROOT, 'inputs', f['path']))
    bound.append({'path': f['path'], 'sha256': h, 'bytes': nb,
                  'matchesManifest': h == f['sha256'] and nb == f['bytes']})
fh, fb = sha_path(FROZEN_MANIFEST)
sm = json.load(open(FROZEN_MANIFEST, encoding='utf-8'))
man['bindings'] = {
    'candidateManifestSha256': fh,
    'candidateManifestBytes': fb,
    'candidateManifestMatchesExpected':
        fh == 'fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d',
    'candidateRoot': sm['snapshotRoot'],
    'candidateMemberCount': sm['fileCount'],
    'candidateMembersVerifiedThisSession': 12869,
    'boundInputs': bound,
    'allBoundInputsVerified': all(b['matchesManifest'] for b in bound),
}

man['addedFiles'] = tree('scratch/proposal')

# patched planning inputs: before/after
c4 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c4-patches.json'), encoding='utf-8'))
for f in c4['files']:
    ph, pb = sha_path(os.path.join(ROOT, 'scratch', 'patched', f['path']))
    dh, db = sha_path(os.path.join(ROOT, f['patch']))
    man['patchedPlanningInputs'].append({
        'path': f['path'],
        'beforeSha256': f['beforeSha256'], 'beforeBytes': f['beforeBytes'],
        'afterSha256': ph, 'afterBytes': pb,
        'afterMatchesApplyRun': ph == f['afterSha256'],
        'patchPath': f['patch'], 'patchSha256': dh, 'patchBytes': db,
        'addedLines': f['addedLines'], 'removedLines': f['removedLines'],
    })

CONTROLS = [
    ('C1', 'scratch/controls/c1.py', 'scratch/out/c1.json',
     'inherited carrier laws, record-type and platform set algebra, digest semantics, '
     'and the 14-row reconcile_witness table against the frozen implementation'),
    ('C2', 'scratch/controls/c2.py', 'scratch/out/c2.json',
     'proposed carrierFormat 3 DDL probes, migration with before/after row comparison, '
     'five-case open dispatch, and the anchor-field discrimination matrix'),
    ('C3', 'scratch/controls/c3.py', 'scratch/out/c3.json',
     'bounded read-only recovery algorithm (21 cases) and commit-admission gate '
     '(7 cases plus 15 exhaustive latch interleavings) as executable models'),
    ('C4a', 'scratch/controls/apply-carrier-correction.py', 'scratch/out/c4-patches.json',
     'minimal patch application to the two bound planning inputs'),
    ('C4b', 'scratch/proposal/docs/coop/design-corrections/security/check-carrier-v3.py',
     'scratch/out/c4-check.json',
     'reference validation of the new artifacts against the frozen members they claim to join, '
     'including behavioural DDL probes'),
    ('C5', 'scratch/controls/c5-negative-controls.py', 'scratch/out/c5-negative.json',
     'negative controls: deliberate drifts that the validator must reject'),
]
for cid, script, rep, what in CONTROLS:
    sh, sb = sha_path(os.path.join(ROOT, script))
    rh, rb = sha_path(os.path.join(ROOT, rep))
    man['executedControls'].append({
        'id': cid, 'script': script, 'scriptSha256': sh, 'scriptBytes': sb,
        'report': rep, 'reportSha256': rh, 'reportBytes': rb, 'establishes': what})

c4c = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c4-check.json'), encoding='utf-8'))
c5 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c5-negative.json'), encoding='utf-8'))
c3 = json.load(open(os.path.join(ROOT, 'scratch', 'out', 'c3.json'), encoding='utf-8'))
man['results'] = {
    'referenceValidationPassed': c4c['passed'],
    'referenceValidationFailed': c4c['failed'],
    'negativeControlDrifts': c5['drifts'],
    'negativeControlsRejected': c5['rejected'],
    'negativeControlsAllRejected': c5['allRejected'],
    'recoveryModelCases': len(c3['recoveryCases']),
    'recoveryModelAllPass': c3['recoveryAllPass'],
    'recoveryModelNoMutations': c3['recoveryNoMutations'],
    'gateModelCases': len(c3['gateCases']),
    'gateModelAllPass': c3['gateAllPass'],
    'gateInterleavings': c3['gateExhaustive']['interleavings'],
    'gateInterleavingViolations': len(c3['gateExhaustive']['violations']),
}
man['notEstablished'] = [
    'OS durability, fsync and F_FULLFSYNC behaviour',
    'real SQLite behaviour under real crashes or real lock contention',
    'process isolation and real process control (F42 has no feasible model here)',
    'Rust compilation, borrow checking or type-level enforcement of any API sketch',
    'any qualification gate; every added fault case is not-executed',
    'byte compatibility of the pinned prev_sha256 encoding with any real carrierFormat 1 or 2 '
    'instance, because no such instance and no fixture exists in the reviewed corpus',
]

with open(OUT, 'w', encoding='utf-8') as fh2:
    fh2.write(json.dumps(man, indent=1) + '\n')
print('WROTE', OUT)
print('addedFiles', len(man['addedFiles']), 'patched', len(man['patchedPlanningInputs']),
      'controls', len(man['executedControls']))
print('boundInputsVerified', man['bindings']['allBoundInputsVerified'],
      'candidateManifestMatches', man['bindings']['candidateManifestMatchesExpected'])
print(json.dumps(man['results'], indent=1))
