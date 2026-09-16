"""Exact SHA-256 of every owner selector file read, in source37, source38 and the consumer24 kit, plus consumer files read."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1'
S37 = '/tmp/opensip-design-corrections/candidate-subject.v37'
S38 = '/tmp/opensip-design-corrections/candidate-subject.v38'
KIT = '/tmp/opensip-design-corrections/consumer-b.v24/subject'
CON = '/tmp/opensip-design-corrections/consumer-b.v24'
SELECTORS = [
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/security-and-lifecycle.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
    'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/query-projection-contract.v3.md',
    'docs/coop/design-corrections/workflows/command-inventory.v3.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/command-inventory.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/detector-manifest.schema.json',
    'docs/coop/design-corrections/workflows/schemas/test-execution.schema.json',
    'docs/coop/design-corrections/workflows/schemas/common.schema.json',
    'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
    'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md',
    'docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json',
    'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
    'docs/coop/design-corrections/public-detail-registry.v1.json',
    'docs/coop/artifacts/permission-truth-tables.v9.json',
]
REFERENCE_CODE_READ = [
    'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/query_surface_projection.v3.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
    'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
    'docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py',
    'docs/coop/design-corrections/foundation/canonical.py',
    'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py',
    'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
]
CONSUMER_READ = [
    'output/blind-review.md', 'output/blind-review.json', 'output/notes/10-gaps.md', 'output/notes/02-decisions-and-gap-candidates.md',
    'output/vectors/baseline-audit.json', 'output/vectors/graph-query.json', 'output/envelopes/public-termination.json',
    'output/tools/phase8_compare.py', 'subject/consumer-input-manifest.json',
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.isfile(p) else None


rows = []
for rel in SELECTORS + REFERENCE_CODE_READ:
    a, b, k = sha(os.path.join(S37, rel)), sha(os.path.join(S38, rel)), sha(os.path.join(KIT, rel))
    rows.append({'path': rel, 'normative': rel in SELECTORS, 'source37': a, 'source38': b, 'kit37': k,
                 'changed37to38': a != b, 'inKit': k is not None, 'kitEqualsSource37': k == a if k else None})
res = {'selectors': rows, 'consumerFiles': {rel: sha(os.path.join(CON, rel)) for rel in CONSUMER_READ},
       'probeScripts': {f: sha(os.path.join(RT, 'probes', f)) for f in sorted(os.listdir(RT + '/probes'))},
       'receipts': {f: sha(os.path.join(RT, 'receipts', f)) for f in sorted(os.listdir(RT + '/receipts'))}}
json.dump(res, open(RT + '/receipts/read-hashes.json', 'w'), indent=1)
for r in rows:
    print(('N ' if r['normative'] else 'R ') + ('CHANGED ' if r['changed37to38'] else '        ') + ('kit ' if r['inKit'] else '    ') + r['path'] + ' ' + str(r['source38'])[:16])
print(json.dumps(res['consumerFiles'], indent=1))
