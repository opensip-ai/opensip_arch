import json, hashlib, os

MP = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
d = json.load(open(MP))
root = d['snapshotRoot']
idx = {f['path']: f for f in d['files']}

TARGETS = [
    'docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py',
    'docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py',
    'docs/coop/design-corrections/foundation/check-replay.v3.py',
    'docs/coop/design-corrections/foundation/check-identity.py',
    'docs/coop/design-corrections/foundation/identity-model.v3.py',
    'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
    'docs/coop/design-corrections/foundation/atom_model.v1.py',
    'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
    'docs/coop/design-corrections/foundation/incoming-search.schema.v1.json',
    'docs/coop/design-corrections/integration-fixtures.py',
    'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
    'docs/coop/design-corrections/workflows/schemas/common.schema.json',
    'docs/coop/design-corrections/public-detail-registry.v1.json',
]

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

prev = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified-subject-files.json')))
seen = {r['path'] for r in prev}
prev.extend(r for r in out if r['path'] not in seen)
json.dump(sorted(prev, key=lambda r: r['path']),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verified-subject-files.json'), 'w'), indent=2)
print('total verified', len(prev))
