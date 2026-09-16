"""Save exact before-images of every file this v2 author session will edit."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v2/source'
RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEFORE = os.path.join(RT, 'before-images')

OWNED = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
]

rows = []
for rel in OWNED:
    src = os.path.join(SRC, rel)
    dst = os.path.join(BEFORE, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        print('already saved, not overwriting:', rel)
    else:
        shutil.copy2(src, dst)
    raw = open(src, 'rb').read()
    rows.append({'path': rel, 'beforeSha256': hashlib.sha256(raw).hexdigest(),
                 'beforeBytes': len(raw), 'beforeImage': 'before-images/' + rel})
    print('%8d %s %s' % (len(raw), rows[-1]['beforeSha256'][:16], rel))

json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'before-images.json'), 'w'), indent=2)
print('saved', len(rows))
