#!/usr/bin/env python3
"""Independent verification of the frozen v10 candidate subject.

Checks, for the manifest at MANIFEST:
  1. manifest self-digest
  2. every declared file exists, with exact byte length and sha256
  3. no undeclared regular files anywhere under snapshotRoot
  4. no symlinks / non-regular files (which would defeat digesting)
"""
import hashlib
import json
import os
import sys

MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v10.json'
EXPECT_MANIFEST_SHA = '82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    raw = open(MANIFEST, 'rb').read()
    man_sha = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    root = man['snapshotRoot']

    out = {
        'manifestPath': MANIFEST,
        'manifestSha256': man_sha,
        'manifestSha256Matches': man_sha == EXPECT_MANIFEST_SHA,
        'snapshotRoot': root,
        'declaredFileCount': man['fileCount'],
        'declaredTotalBytes': man['totalBytes'],
        'predecessorManifestSha256': man.get('predecessorManifestSha256'),
    }

    declared = {}
    dup = []
    for rec in man['files']:
        if rec['path'] in declared:
            dup.append(rec['path'])
        declared[rec['path']] = rec
    out['duplicateDeclaredPaths'] = dup
    out['declaredListLength'] = len(man['files'])
    out['declaredUniquePaths'] = len(declared)
    out['fileCountConsistent'] = len(man['files']) == man['fileCount']

    missing, badsha, badlen = [], [], []
    total = 0
    for path, rec in declared.items():
        full = os.path.join(root, path)
        if not os.path.isfile(full) or os.path.islink(full):
            missing.append(path)
            continue
        size = os.path.getsize(full)
        total += size
        if size != rec['bytes']:
            badlen.append({'path': path, 'declared': rec['bytes'], 'actual': size})
        got = sha256_file(full)
        if got != rec['sha256']:
            badsha.append({'path': path, 'declared': rec['sha256'], 'actual': got})

    out['missing'] = missing
    out['lengthMismatches'] = badlen
    out['digestMismatches'] = badsha
    out['sumOfActualBytes'] = total
    out['totalBytesMatches'] = total == man['totalBytes']

    # undeclared inventory
    undeclared = []
    nonregular = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full) or not os.path.isfile(full):
                nonregular.append(rel)
                continue
            if rel not in declared:
                undeclared.append(rel)
        for name in dirnames:
            full = os.path.join(dirpath, name)
            if os.path.islink(full):
                nonregular.append(os.path.relpath(full, root) + '/ (symlink dir)')
    out['undeclaredFiles'] = sorted(undeclared)
    out['undeclaredCount'] = len(undeclared)
    out['nonRegularEntries'] = sorted(nonregular)

    out['VERDICT_CLEAN'] = bool(
        out['manifestSha256Matches'] and not missing and not badlen and not badsha
        and not undeclared and not nonregular and not dup
        and out['totalBytesMatches'] and out['fileCountConsistent']
    )
    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    print()


if __name__ == '__main__':
    main()
