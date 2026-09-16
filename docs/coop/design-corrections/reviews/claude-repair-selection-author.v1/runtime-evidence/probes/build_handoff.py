"""Build the exact changed-file handoff: path, before/after SHA256 and bytes, plus a
verification that NOTHING outside the declared set changed in the author source."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v31'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(RT, 'probes')

DECLARED = {
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md': 'edited',
    'docs/v2/contracts/product-v1/native-evidence.md': 'edited',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json': 'edited',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json': 'edited',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py': 'edited',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py': 'edited',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py': 'edited',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py': 'created',
}


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


baseline = {r['path']: r for r in json.load(open(os.path.join(HERE, 'author-source-baseline.json')))['files']}

rows, undeclared, unchanged_declared = [], [], []
present = set()
for dirpath, _dirs, files in os.walk(SRC):
    for name in sorted(files):
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, SRC)
        present.add(rel)
        now = sha(full)
        base = baseline.get(rel)
        if base is None:
            if DECLARED.get(rel) != 'created':
                undeclared.append({'path': rel, 'kind': 'new-file-not-declared'})
            continue
        if now != base['sha256'] and rel not in DECLARED:
            undeclared.append({'path': rel, 'kind': 'changed-but-not-declared'})

missing = [p for p in baseline if p not in present]

for rel, kind in sorted(DECLARED.items()):
    full = os.path.join(SRC, rel)
    after = sha(full)
    after_bytes = os.path.getsize(full)
    if kind == 'edited':
        before = baseline[rel]
        frozen = os.path.join(FROZEN, rel)
        rows.append({
            'path': rel, 'change': 'edited',
            'beforeSha256': before['sha256'], 'beforeBytes': before['bytes'],
            'afterSha256': after, 'afterBytes': after_bytes,
            'beforeImage': 'before-images/' + rel,
            'beforeMatchedFrozen31': before['sha256'] == sha(frozen),
            'actuallyChanged': after != before['sha256'],
        })
    else:
        rows.append({
            'path': rel, 'change': 'created',
            'beforeSha256': None, 'beforeBytes': None,
            'afterSha256': after, 'afterBytes': after_bytes,
            'beforeImage': None, 'existedInFrozen31': os.path.exists(os.path.join(FROZEN, rel)),
        })

# every before-image on disk must still equal the frozen31 byte-image
image_ok = []
for rel, kind in sorted(DECLARED.items()):
    if kind != 'edited':
        continue
    img = os.path.join(RT, 'before-images', rel)
    image_ok.append({'path': rel, 'beforeImagePresent': os.path.exists(img),
                     'beforeImageEqualsFrozen31': os.path.exists(img) and sha(img) == sha(os.path.join(FROZEN, rel))})

out = {
    'standing': 'AUTHOR_PENDING_REVIEW. No author acceptance, no root agreement, no application.',
    'authorSourceRoot': SRC,
    'baselineFileCount': len(baseline),
    'currentFileCount': len(present),
    'changedFiles': rows,
    'undeclaredChanges': undeclared,
    'missingFiles': missing,
    'beforeImageVerification': image_ok,
}
json.dump(out, open(os.path.join(RT, 'changed-file-handoff.json'), 'w'), indent=2)

print('baseline files', len(baseline), '-> current', len(present))
print('undeclared changes', len(undeclared), undeclared[:5])
print('missing files', len(missing), missing[:5])
for r in rows:
    print(' ', r['change'], r['path'])
    print('     before', r['beforeBytes'], (r['beforeSha256'] or '-')[:16],
          '-> after', r['afterBytes'], r['afterSha256'][:16])
print('before-image checks:', all(i['beforeImagePresent'] and i['beforeImageEqualsFrozen31'] for i in image_ok))
