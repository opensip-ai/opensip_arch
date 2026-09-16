"""Verify the author source workspace is an exact frozen31 subset before authoring."""
import hashlib, json, os

AUTHOR = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'author-source-baseline.json')


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


rows, missing, differ = [], [], []
for dirpath, dirnames, filenames in os.walk(AUTHOR):
    for name in sorted(filenames):
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, AUTHOR)
        frozen = os.path.join(FROZEN, rel)
        h = sha(full)
        if not os.path.exists(frozen):
            missing.append(rel)
            rows.append({'path': rel, 'sha256': h, 'bytes': os.path.getsize(full),
                         'frozenMatch': None})
            continue
        fh = sha(frozen)
        ok = (fh == h)
        if not ok:
            differ.append(rel)
        rows.append({'path': rel, 'sha256': h, 'bytes': os.path.getsize(full),
                     'frozenMatch': ok})

rows.sort(key=lambda r: r['path'])
print('authorFiles', len(rows))
print('custodyClaim', json.load(open(
    '/tmp/opensip-design-corrections/repair-selection-successor.v1/input-custody.json'))['copiedFiles'])
print('notInFrozen31', len(missing), missing[:10])
print('differFromFrozen31', len(differ), differ[:10])
print('exactMatches', sum(1 for r in rows if r['frozenMatch'] is True))

json.dump({'authorRoot': AUTHOR, 'frozenRoot': FROZEN, 'fileCount': len(rows),
           'exactMatches': sum(1 for r in rows if r['frozenMatch'] is True),
           'notInFrozen31': missing, 'differFromFrozen31': differ,
           'files': rows}, open(OUT, 'w'), indent=2)
print('WROTE', OUT)
