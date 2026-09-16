"""Preserve generation 22's exact final artifacts BEFORE generation 23 corrects or regenerates them.

Written fresh for generation 23 and run ONCE, before any stage of the generation-23 command runs.
The generation-23 kit changes the atom contract, the projection registry and the incoming-search
schema, so some generation-22 claimed positives may be wrong under current law (the runtime
polarity reading of V22-D3 is the first candidate). The failing predecessor must be kept: every
generation-22 artifact is copied byte-for-byte with a sha256 manifest, and is NEVER read back as
truth, executed, or re-labelled as generation 23. The generation-20 predecessors that generation 22
preserved stay where they are (predecessors.v20) and are not copied again.
"""
import hashlib
import json
import os
import shutil

OUT = '/tmp/opensip-design-corrections/consumer-b.' + 'v23' + '/output'
DEST = OUT + '/predecessors.v22'
DIRS = ('runs', 'query', 'vectors', 'envelopes', 'traces', 'checkpoints')
NOTES_EXCLUDED = ('v22-stage-io',)
FILES = ('blind-review.md', 'blind-review.json', 'helper-corrections.json',
         'requirement-status.json', 'verify-all.json', 'progress.v22.json')


def sha(p):
    with open(p, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    if os.path.exists(DEST):
        raise SystemExit('predecessor copy already exists; runs once only: ' + DEST)
    os.makedirs(DEST)
    for d in DIRS:
        shutil.copytree(os.path.join(OUT, d), os.path.join(DEST, d))
    # generation-23 notes already written (the path census, the pre-rebind label audit) are not
    # generation-22 bytes and are not part of the predecessor copy
    shutil.copytree(os.path.join(OUT, 'notes'), os.path.join(DEST, 'notes'),
                    ignore=lambda _d, names: [n for n in names
                                              if n in NOTES_EXCLUDED or n.startswith('v23-')])
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
    mismatched = [rel for rel, row in manifest.items()
                  if sha(os.path.join(OUT, rel)) != row['sha256']]
    doc = {'standing': __doc__, 'generationOfTheBytes': 'consumer-b.' + 'v22',
           'preservedBy': 'consumer-b.' + 'v23',
           'notesExcluded': ('notes/v22-stage-io/ is not copied: those per-stage logs are already '
                             'per-command receipts that no generation-23 stage writes'),
           'fileCount': len(manifest), 'mismatchedAgainstSourceAtCopyTime': mismatched,
           'files': manifest}
    with open(os.path.join(DEST, 'PREDECESSOR-MANIFEST.json'), 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print('preserved %d files under %s, mismatched at copy time: %d'
          % (len(manifest), DEST, len(mismatched)))
    print('blind-review.json sha256 %s' % manifest['blind-review.json']['sha256'])
    assert not mismatched, mismatched[:5]


main()
