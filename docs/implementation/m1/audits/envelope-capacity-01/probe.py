"""Compare the owned required availability shape with the envelope codec cap."""
import ast
import hashlib
import json
from pathlib import Path
import types

ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
ROOT = Path(__file__).resolve().parent
sources = {
    'canonical': ARCH/'docs/coop/design-corrections/foundation/canonical.py',
    'identity': ARCH/'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
    'matrix': ARCH/'docs/coop/design-corrections/native/native-capability-matrix.v2.json',
    'common': ARCH/'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
    'native': ARCH/'docs/coop/design-corrections/native/native_evidence_model.v2.py',
    'report-budget': Path('/tmp/opensip-implementation/m1-report-projection-subject-07/owner/budget-derivations.v1.json'),
}
pins = []
raws = {}
for name, path in sources.items():
    raw = path.read_bytes()
    raws[name] = raw
    pins.append({'role': name, 'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
ref = types.ModuleType('canonical_reference')
exec(compile(raws['canonical'], str(sources['canonical']), 'exec'), ref.__dict__)
nodes = []
for n in ast.parse(raws['native']).body:
    if isinstance(n, ast.FunctionDef) and n.name in ('release_absence_notices', 'invocation_availability', 'admit_requested_capabilities'):
        nodes.append(n)
    elif isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PUBLIC_ROUTE_REMEDIES' for t in n.targets):
        nodes.append(n)
assert len(nodes) == 4
native = {'CAPABILITY_MATRIX': json.loads(raws['matrix']), 'AdmissionError': ref.AdmissionError}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(sources['native']), 'exec'), native)
schema = json.loads(raws['common'])
schema['$ref'] = '#/$defs/CapabilityAvailabilityV1'
rows = []
for count in (1, 2):
    per_step = []
    for step in range(count):
        undeclared = [{'capabilityId': 'calls', 'languageMode': 'js-synthesized',
                       'workspaceRoot': ('unit-'+format(i, '04d')+'/').ljust(4096, 'x')}
                      for i in range(995)]
        per_step.append((step, undeclared))
    requested = [dict(row, required=True) for row in per_step[0][1]]
    requested.sort(key=ref.canonical)
    native['admit_requested_capabilities'](requested)
    spec = {'schemaVersion': 2, 'requestedCapabilities': requested, 'parameters': [], 'policyPackIds': []}
    spec_schema = json.loads(raws['identity']); spec_schema['$ref'] = '#/$defs/analysis-spec'
    ref.validate(spec_schema, spec)
    spec_bytes = len(ref.canonical(spec))
    account = native['invocation_availability'](per_step)
    ref.validate(schema, account)
    # Every value has been admitted as exact JSON; this measures the same
    # canonical spelling without invoking the profile's size refusal first.
    raw = json.dumps(account, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    error = None
    try:
        ref.canonical(account)
    except ref.AdmissionError as exc:
        error = str(exc)
    rows.append({'stepCount': count, 'noticesPerStep': 995, 'workspaceRootChars': 4096,
                 'schemaAdmitted': True, 'requestVocabularyAdmitted': True, 'analysisSpecShapeAndCodecAdmittedBytes': spec_bytes, 'canonicalBytes': len(raw), 'canonicalSha256': hashlib.sha256(raw).hexdigest(),
                 'codecRefusal': error})
result = {'standing': 'Root capacity audit, not an end-to-end invocation or native-selection reproduction',
          'pins': pins, 'codecMaxBytes': ref.MAX_BYTES,
          'reportEnvelopeCodecMaxBytes': json.loads(raws['report-budget'])['envelopeCodecMaxBytes'],
          'cases': rows,
          'finding': 'A schema-admitted required availability account alone can exceed the selected envelope codec limit. Appending it to any envelope cannot fit. Need an explicit capacity/admission or delivery owner decision; no loss of required notices or implicit truncation.',
          'limits': 'Actual requested-capability vocabulary function and analysis-spec shape/codec exercised; parameters are empty so full parameter-selection admission is not claimed. Synthetic unit rows; not proof that every constructed path/unit set passes filesystem or native selection admission. Actual host closure, request preflight, error dispatch and final serializers are unimplemented.'}
(ROOT/'result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ('codecMaxBytes', 'reportEnvelopeCodecMaxBytes', 'cases')}, indent=2))
