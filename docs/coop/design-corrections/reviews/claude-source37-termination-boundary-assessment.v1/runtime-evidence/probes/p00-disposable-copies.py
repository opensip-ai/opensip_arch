"""Create disposable baseline and edited copies of frozen candidate37 docs; verify exact key bytes.

reviews/ and __pycache__ are excluded (no other origin's artifacts are copied). Frozen bytes are only read.
An existing copy is never overwritten.
"""
import hashlib, json, shutil
from pathlib import Path

FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
EXPECT_MANIFEST = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
BASE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1')
KEY = [
    'docs/coop/design-corrections/workflows/schemas/common.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
    'docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json',
    'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
    'docs/coop/design-corrections/workflows/check_workflows.v1.py',
    'docs/coop/design-corrections/foundation/evaluator_fault_model.v3.py',
    'docs/coop/design-corrections/foundation/evaluator-fault-observation.schema.v3.json',
    'docs/coop/design-corrections/integration-host-model.py',
    'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'docs/coop/artifacts/d9-exit-contract.v1.14.json',
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


manifest_bytes = MANIFEST.read_bytes()
manifest = json.loads(manifest_bytes)
pins = {}


def walk(o):
    if isinstance(o, dict):
        path, digest = o.get('path'), o.get('sha256')
        if isinstance(path, str) and isinstance(digest, str):
            pins[path] = digest
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(manifest)
record = {'manifestSha256': hashlib.sha256(manifest_bytes).hexdigest()}
record['manifestMatches'] = record['manifestSha256'] == EXPECT_MANIFEST
record['manifestPinnedPathCount'] = len(pins)
ignore = shutil.ignore_patterns('reviews', '__pycache__')
for name in ('baseline', 'edited'):
    dest = BASE / 'disposable' / name / 'docs'
    shutil.copytree(FROZEN / 'docs', dest, ignore=ignore, symlinks=True, dirs_exist_ok=False)
rows = []
for rel in KEY:
    frozen = sha(FROZEN / rel)
    manifest_pin = next((d for p, d in pins.items() if p == rel or p.endswith('/' + rel) or rel.endswith('/' + p)), None)
    rows.append({'path': rel, 'frozenSha256': frozen, 'manifestPin': manifest_pin,
                 'manifestAgrees': None if manifest_pin is None else manifest_pin == frozen,
                 'baselineEqual': sha(BASE / 'disposable/baseline' / rel) == frozen,
                 'editedEqual': sha(BASE / 'disposable/edited' / rel) == frozen})
record['keyFiles'] = rows
record['allCopiesEqual'] = all(r['baselineEqual'] and r['editedEqual'] for r in rows)
record['noManifestDisagreement'] = all(r['manifestAgrees'] is not False for r in rows)
(BASE / 'probes' / 'p00-disposable-copies.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if not (record['manifestMatches'] and record['allCopiesEqual'] and record['noManifestDisagreement']):
    raise SystemExit(1)
