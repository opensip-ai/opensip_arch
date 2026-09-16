"""Read exact final consumer envelopes; owner schema checks only, no Run acceptance."""
from pathlib import Path
import collections
import hashlib
import importlib.util
import json

ROOT = Path('/tmp/opensip-design-corrections')
SOURCE = ROOT / 'candidate-subject.v37'
CONSUMER = ROOT / 'consumer-b.v24/output/envelopes'
OUT = Path(__file__).parent
owner = SOURCE / 'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py'
spec = importlib.util.spec_from_file_location('root_envelope_owner37', owner)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
rows = []
inputs = []

def visit(value, path, filename, classification=None):
    if isinstance(value, dict):
        classification = value.get('classification', classification)
        if value.get('schemaFamily') == 'opensip.product.envelope':
            row = dict(file=filename, pointer=path, consumerClassification=classification)
            try:
                model.validate_profile('urn:opensip:product-v1:workflows:evaluator3:command-envelope:3', value)
                row.update(schema='ADMIT')
            except Exception as exc:
                row.update(schema='REFUSE', exceptionType=type(exc).__name__, reason=str(exc))
            rows.append(row)
        for key, child in value.items():
            visit(child, path + '/' + key.replace('~', '~0').replace('/', '~1'), filename, classification)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            visit(child, path + '/' + str(index), filename, classification)

for path in sorted(CONSUMER.glob('*.json')):
    if '.attempt' in path.name:
        continue
    raw = path.read_bytes()
    inputs.append(dict(file=path.name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    visit(json.loads(raw), '', path.name)

result = dict(
    standing='Exact final exported envelope schema admission only. No reconstruction helper imported; no envelope repaired. This does not verify Run closure, public-route semantics or whole charter conformance. Attempt files preserved and excluded from final census. Nested negative exhibits are recorded without interpreting refusal as an unexpected failure.',
    sourceManifestSha256='245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680',
    ownerSha256=hashlib.sha256(owner.read_bytes()).hexdigest(),
    inputs=inputs, rows=rows,
    counts=dict(collections.Counter(row['schema'] for row in rows)),
)
(OUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(dict(files=len(inputs), envelopes=len(rows), counts=result['counts'], refusals=[{k:v for k,v in r.items() if k != 'reason'} | {'reason':r.get('reason','')[:250]} for r in rows if r['schema']=='REFUSE']), indent=2))
