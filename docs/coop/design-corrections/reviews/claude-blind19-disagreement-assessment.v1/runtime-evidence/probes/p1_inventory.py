"""P1: verify manifest + the five exact exports, and locate the artifacts I will read."""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
RB = '/tmp/opensip-design-corrections/root-blind19-final-source32.v1'
CB = '/tmp/opensip-design-corrections/consumer-b.v19'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


out = {}
out['manifestSha256'] = sha(MANIFEST)
out['manifestMatches'] = out['manifestSha256'] == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'
man = json.load(open(MANIFEST))
out['manifestFileCount'] = len(man['files'])
out['snapshotRoot'] = man.get('snapshotRoot')

summary = json.load(open(os.path.join(RB, 'summary.json')))
rows = []
for r in summary['results']:
    exp = os.path.join(RB, r['name'], 'exact-export.json')
    got = sha(exp) if os.path.exists(exp) else None
    rows.append({'name': r['name'], 'runId': r['runId'],
                 'declaredExportSha256': r['exportSha256'], 'recomputed': got,
                 'match': got == r['exportSha256'],
                 'transport': r['transportAdmission'], 'structural': r['structuralAdmission'],
                 'semantic': r['semanticAdmission'], 'reason': r['reason']})
out['exports'] = rows
out['allExportsMatch'] = all(r['match'] for r in rows)

# owner files I will read, hashed against the manifest
idx = {f['path']: f['sha256'] for f in man['files']}
owners = [
    'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py',
    'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
    'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json',
    'docs/coop/design-corrections/native/native-capability-matrix.v2.json',
    'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
    'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json',
]
ow = []
for rel in owners:
    p = os.path.join(ROOT32, rel)
    if not os.path.exists(p):
        ow.append({'path': rel, 'present': False})
        continue
    h = sha(p)
    ow.append({'path': rel, 'present': True, 'sha256': h,
               'inManifest': rel in idx, 'manifestMatch': idx.get(rel) == h,
               'bytes': os.path.getsize(p)})
out['ownersRead'] = ow

# consumer output tree
cons = []
for dp, _d, fs in os.walk(CB):
    for n in sorted(fs):
        full = os.path.join(dp, n)
        cons.append({'path': os.path.relpath(full, CB), 'bytes': os.path.getsize(full),
                     'sha256': sha(full)})
out['consumerFiles'] = cons
out['consumerFileCount'] = len(cons)

json.dump(out, open(os.path.join(HERE, 'p1-inventory.json'), 'w'), indent=2)
print('manifest match     :', out['manifestMatches'], '| files', out['manifestFileCount'])
print('all exports match  :', out['allExportsMatch'])
for r in rows:
    print('  ', 'OK ' if r['match'] else 'BAD', r['name'], r['semantic'], r['reason'][:80])
print('owners read:')
for o in ow:
    print('  ', 'OK ' if o.get('manifestMatch') else ('MISS' if not o['present'] else 'DIFF'),
          o.get('bytes'), o['path'])
print('consumer files     :', out['consumerFileCount'])
for c in cons[:40]:
    print('   ', c['bytes'], c['path'])
