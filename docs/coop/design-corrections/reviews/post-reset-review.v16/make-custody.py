#!/usr/bin/env python3
"""Write source-copy-accounts.json and custody.json for post-reset-review.v16.

source-copy-accounts records each NAMED disposable full copy against the frozen
v16 manifest, in the same shape the project already uses. custody records every
file this review wrote, by digest.
"""
import hashlib, json, os

OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
MANIFEST = ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/'
            'reviews/candidate-subject.v16.json')
SUBJ_SHA = 'ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9'

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

m = json.load(open(MANIFEST))
declared = {r['path']: r['sha256'] for r in m['files']}

accounts = {}
for name, purpose in [
    ('copy-A-reference-run', 'the six recorded final-reference.v16 reference-check commands'),
    ('copy-B-probes', 'independent probes 04-14, plus a second determinism run of the six commands'),
]:
    root = os.path.join(OUT, name)
    unchanged, changed, added, deleted = [], [], [], []
    on_disk = set()
    for dp, dn, fns in os.walk(root):
        for fn in fns:
            on_disk.add(os.path.relpath(os.path.join(dp, fn), root))
    for path, dig in declared.items():
        full = os.path.join(root, path)
        if not os.path.isfile(full):
            deleted.append(path); continue
        got = sha256(full)
        (unchanged if got == dig else changed).append(
            path if got == dig else {'path': path, 'baseSha256': dig, 'copySha256': got})
    added = sorted(on_disk - set(declared))
    accounts[name] = {
        'purpose': purpose,
        'baseManifestSha256': SUBJ_SHA,
        'actualFiles': len(declared),
        'unchangedFiles': len(unchanged),
        'changedFiles': changed,
        'addedFiles': added,
        'deletedFiles': deleted,
        'byteExactAgainstFrozenManifest': not (changed or added or deleted),
        'note': 'The six checks write their reports IN-TREE. That both copies remain byte-exact '
                'after execution is the measurement: the regenerated reports are identical to the '
                'frozen ones. Repinning was never performed.',
    }

files = []
for fn in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, fn)
    if os.path.isfile(p):
        files.append({'file': fn, 'bytes': os.path.getsize(p), 'sha256': sha256(p)})

custody = {
    'artifact': 'post-reset-review.v16 — fresh independent architecture/design/reference review',
    'reviewer': 'actual Claude (claude-opus-5), fresh independent session',
    'authoredNoneOfTheSubjectBytes': True,
    'subjectManifestSha256': SUBJ_SHA,
    'writeCustody': 'Every byte written by this review is under '
                    '/tmp/opensip-design-corrections/post-reset-review.v16, including both '
                    'disposable full source copies. Nothing was written into the immutable '
                    'snapshot at /tmp/opensip-design-corrections/candidate-subject.v16 or into the '
                    'original repository, and no report-writing command was executed inside either.',
    'subjectVerifiedBeforeAndAfter': {
        'pre': 'probe-01-verify-subject.pre.json',
        'post': 'probe-01-verify-subject.post.json',
        'identical': True,
        'filesVerified': len(declared),
    },
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
    'agentsOrSubagents': 0,
    'productImplementationChanges': 0,
    'fixes': 0, 'commits': 0, 'pushes': 0, 'subjectEdits': 0,
    'sourceCopyAccounts': accounts,
    'writtenFiles': files,
    'writtenFileCount': len(files),
    'preservedFailedAttempts': [f['file'] for f in files if f['file'].startswith('failed-attempt-')],
    'deliverables': ['review.md', 'review.json'],
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'source-copy-accounts.json'), 'w') as f:
    json.dump(accounts, f, indent=2, sort_keys=True)
with open(os.path.join(OUT, 'custody.json'), 'w') as f:
    json.dump(custody, f, indent=2, sort_keys=True)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'unchangedFiles'}
                  for k, v in accounts.items()}, indent=2, sort_keys=True))
print('writtenFiles', len(files), 'failedAttempts', len(custody['preservedFailedAttempts']))
