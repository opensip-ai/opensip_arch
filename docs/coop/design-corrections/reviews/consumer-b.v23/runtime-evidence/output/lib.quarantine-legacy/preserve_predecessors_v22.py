"""Preserve generation 20's exact final claimed-positive artifacts BEFORE generation 22 corrects them.

Run ONCE, before any stage of the generation-22 command regenerates an artifact. The copy is the
failing predecessor the instruction requires to be kept: several of these artifacts are shown by
generation 22 to be wrong under current law (atom completeness/causes, imported-observation
polarity) or never admitted against their owning schema. They are retained byte-for-byte with a
sha256 manifest, and are NEVER read back as truth, executed, or re-labelled as generation 22.
"""
import hashlib
import json
import os
import shutil

OUT = '/tmp/opensip-design-corrections/consumer-b.' + 'v22' + '/output'
DEST = OUT + '/predecessors.v20'
DIRS = ('runs', 'query', 'vectors', 'envelopes', 'traces', 'checkpoints')
FILES = ('blind-review.md', 'blind-review.json', 'helper-corrections.json',
         'requirement-status.json', 'verify-all.json', 'progress.v20.json')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if os.path.exists(DEST):
        raise SystemExit('predecessor copy already exists; runs once only: ' + DEST)
    os.makedirs(DEST)
    for d in DIRS:
        shutil.copytree(os.path.join(OUT, d), os.path.join(DEST, d))
    for f in FILES:
        shutil.copy2(os.path.join(OUT, f), os.path.join(DEST, f))
    manifest = {}
    for base, _dirs, names in os.walk(DEST):
        for n in sorted(names):
            p = os.path.join(base, n)
            rel = os.path.relpath(p, DEST)
            if rel == 'PREDECESSOR-MANIFEST.json':
                continue
            manifest[rel] = {'sha256': sha(p), 'bytes': os.path.getsize(p)}
    # the copy must equal the source byte for byte at the moment it was taken
    mismatched = [rel for rel, row in manifest.items()
                  if sha(os.path.join(OUT, rel)) != row['sha256']]
    doc = {'standing': __doc__, 'generationOfTheBytes': 'consumer-b.' + 'v20',
           'preservedBy': 'consumer-b.' + 'v22',
           'fileCount': len(manifest), 'mismatchedAgainstSourceAtCopyTime': mismatched,
           'files': manifest}
    with open(os.path.join(DEST, 'PREDECESSOR-MANIFEST.json'), 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print('preserved %d files under %s, mismatched at copy time: %d'
          % (len(manifest), DEST, len(mismatched)))
    print('blind-review.json sha256 %s' % manifest['blind-review.json']['sha256'])
    assert not mismatched, mismatched[:5]


main()
