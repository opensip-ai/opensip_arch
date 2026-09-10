#!/usr/bin/env python3
"""Probe 01 (pre-review custody): verify every declared file hash/length in the
frozen v16 manifest against the frozen snapshot, and enumerate undeclared
inventory (files present on disk but absent from the manifest).

Writes ONLY under /tmp/opensip-design-corrections/post-reset-review.v16.
Reads the frozen snapshot and the in-repo manifest read-only.
"""
import hashlib, json, os, sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v16.json'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

man_sha = sha256(MANIFEST)
m = json.load(open(MANIFEST))
root = m['snapshotRoot']

sample = m['files'][0]
print('manifestSha256', man_sha)
print('file record keys:', sorted(sample.keys()))

declared = {}
for rec in m['files']:
    declared[rec['path']] = rec

missing, hash_mismatch, len_mismatch = [], [], []
total_declared_bytes = 0
for path, rec in declared.items():
    full = os.path.join(root, path)
    if not os.path.isfile(full):
        missing.append(path)
        continue
    st = os.stat(full)
    exp_len = rec.get('bytes', rec.get('length', rec.get('size')))
    if exp_len is not None and st.st_size != exp_len:
        len_mismatch.append((path, exp_len, st.st_size))
    exp_hash = rec.get('sha256')
    got = sha256(full)
    if exp_hash and got != exp_hash:
        hash_mismatch.append((path, exp_hash, got))
    total_declared_bytes += st.st_size

# undeclared inventory
on_disk = []
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, root)
        on_disk.append(rel)
undeclared = sorted(set(on_disk) - set(declared))
symlinks = []
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames + dirnames:
        full = os.path.join(dirpath, fn)
        if os.path.islink(full):
            symlinks.append(os.path.relpath(full, root))

result = {
    'probe': 'probe-01-verify-subject',
    'phase': 'pre-review',
    'manifestPath': MANIFEST,
    'manifestSha256': man_sha,
    'manifestSha256Matches': man_sha == 'ca5f36d421fb38d264f49fc6b2e1eeffee5bbe8182a7fe25bd50787244042ee9',
    'snapshotRoot': root,
    'declaredFileCount': m['fileCount'],
    'declaredFileRecords': len(m['files']),
    'declaredPathsUnique': len(declared),
    'declaredTotalBytes': m['totalBytes'],
    'observedTotalBytesOfDeclared': total_declared_bytes,
    'observedFilesOnDisk': len(on_disk),
    'missingCount': len(missing),
    'missing': missing[:50],
    'hashMismatchCount': len(hash_mismatch),
    'hashMismatch': hash_mismatch[:50],
    'lengthMismatchCount': len(len_mismatch),
    'lengthMismatch': len_mismatch[:50],
    'undeclaredCount': len(undeclared),
    'undeclared': undeclared[:200],
    'symlinkCount': len(symlinks),
    'symlinks': symlinks[:50],
    'predecessorManifestSha256': m['predecessorManifestSha256'],
    'standing': m['standing'],
    'authors': m['authors'],
    'reviewPending': m['reviewPending'],
    'applicationPending': m['applicationPending'],
}
phase = sys.argv[1] if len(sys.argv) > 1 else 'pre'
result['phase'] = phase
with open(os.path.join(OUT, f'probe-01-verify-subject.{phase}.json'), 'w') as f:
    json.dump(result, f, indent=2, sort_keys=True)
print(json.dumps({k: v for k, v in result.items()
                  if k not in ('undeclared', 'missing', 'hashMismatch', 'lengthMismatch', 'symlinks')},
                 indent=2, sort_keys=True))
