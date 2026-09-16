"""Save exact before-images of every file this author session will edit."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEFORE = os.path.join(RT, 'before-images')

EDITED = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
]
NEW = [
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
]

rows = []
for rel in EDITED:
    src = os.path.join(SRC, rel)
    dst = os.path.join(BEFORE, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        print('before-image already saved, not overwriting:', rel)
    else:
        shutil.copy2(src, dst)
    raw = open(src, 'rb').read()
    rows.append({'path': rel, 'status': 'to-be-edited',
                 'beforeSha256': hashlib.sha256(raw).hexdigest(),
                 'beforeBytes': len(raw),
                 'beforeImage': os.path.relpath(dst, RT)})
for rel in NEW:
    exists = os.path.exists(os.path.join(SRC, rel))
    rows.append({'path': rel, 'status': 'to-be-created',
                 'beforeSha256': None, 'beforeBytes': None,
                 'existedBefore': exists, 'beforeImage': None})

out = os.path.join(RT, 'probes', 'before-images.json')
json.dump(rows, open(out, 'w'), indent=2)
for r in rows:
    print(r['status'], r['beforeBytes'], (r['beforeSha256'] or '-')[:16], r['path'])
print('WROTE', out)
