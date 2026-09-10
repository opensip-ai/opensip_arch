import hashlib, json, os

OUT = '/tmp/opensip-design-corrections/post-reset-review.v18'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


files = []
for dp, dn, fn in os.walk(OUT):
    if '/disposable-copy' in dp:
        continue
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, OUT)
        if rel == 'custody.json':
            continue
        files.append({'path': rel, 'bytes': os.path.getsize(p), 'sha256': sha(p)})
files.sort(key=lambda x: x['path'])

custody = {
    'review': 'post-reset-review.v18',
    'subjectManifestSha256': 'cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44',
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B (3.12.13)',
    'writeScope': OUT,
    'liveRepositoryBytesWritten': 0,
    'frozenSnapshotBytesWritten': 0,
    'subjectVerification': {
        'before': 'logs/... p01 run: 7864/7864 verified, 0 mismatch, 0 extra, bytes 544831302',
        'after': 'logs/subject-verify-final.txt: identical result, manifest re-hash unchanged'},
    'disposableCopy': {
        'root': OUT + '/disposable-copy',
        'basis': 'FULL exact copy of all 7864 declared files',
        'deltaVersusFrozenAfterAllSixCanonicalRuns': {'added': 0, 'removed': 0, 'changed': 0},
        'retained': True},
    'controlTrees': {
        'count': 14, 'totalFilesAcrossTrees': 110124,
        'inventoryBeforePrune': 'logs/control-tree-inventory-before-prune.json',
        'pruned': True,
        'whyPruned': '14 full snapshot copies totalling ~7.4 GB. Each was a throwaway injection tree, not '
                     'candidate source. All 42 generated reports from those trees are retained under '
                     'evidence/control-reports/, and every probe source that builds them is retained, so '
                     'each tree is reconstructible from the frozen snapshot plus the probe.'},
    'failedAttemptsPreserved': [
        'probes/failed-attempt-01-p11-unconditional-injection.py + logs/p11-ten-context-controls.json',
        'probes/failed-attempt-02-p22-regex-monotonicity.py + probes/p22.out',
        'probes/p04_exact_ast_proof.py (guarded_by predicate) + probes/p04.out',
        'logs/p13-render-control.json (3 escaped-uncaught render injections)',
        'probes/p08.out (raise-site miscount, corrected in probes/p10.out)'],
    'files': files,
    'fileCount': len(files),
    'totalBytes': sum(f['bytes'] for f in files),
    'implementationAuthorized': False, 'readinessChanged': False, 'productQualification': False,
}
json.dump(custody, open(OUT + '/custody.json', 'w'), indent=1)
print('custody files=%d bytes=%d' % (custody['fileCount'], custody['totalBytes']))
for f in files:
    if f['path'] in ('review.json', 'review.md'):
        print(' ', f['path'], f['bytes'], f['sha256'])
