import json, hashlib, os

MP = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
d = json.load(open(MP))
root = d['snapshotRoot']
idx = {f['path']: f for f in d['files']}

TARGETS = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
    'docs/v2/contracts/product-v1/admission-and-qualification.md',
    'docs/v2/contracts/product-v1/security-and-lifecycle.md',
    'docs/v2/contracts/product-v1/README.md',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
]

print('snapshotRoot', root, 'exists=', os.path.isdir(root))
out = []
for t in TARGETS:
    e = idx.get(t)
    fp = os.path.join(root, t)
    if e is None:
        print('NOT-IN-MANIFEST', t)
        continue
    if not os.path.exists(fp):
        print('MISSING-ON-DISK', t)
        continue
    h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
    ok = (h == e['sha256'])
    out.append({'path': t, 'bytes': e['bytes'], 'sha256': h, 'match': ok})
    print('OK  ' if ok else 'FAIL', e['bytes'], t, h)

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified-subject-files.json'), 'w'), indent=2)
