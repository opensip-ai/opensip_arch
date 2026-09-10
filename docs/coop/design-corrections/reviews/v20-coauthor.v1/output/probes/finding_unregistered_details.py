"""ROOT-1: two DomainDetail codes emitted by workflows_model.v1.py are not registered.

Found while implementing CB-GAP-1, on the very function it touches. NOT changed here:
altering the code of an existing, reachable refusal changes accepted behaviour outside
the corrected input, and root owns that call. Reported instead, and the CB-GAP-1
ambiguity refusal deliberately does not repeat the pattern.
"""
import importlib.util, json, re
from pathlib import Path

H = Path('/tmp/opensip-design-corrections/v20-coauthor.v1/work/docs/coop/design-corrections')
s = importlib.util.spec_from_file_location('w', H / 'workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(s); s.loader.exec_module(W)

registry = json.loads((H / 'public-detail-registry.v1.json').read_text())
schema_codes = set(json.loads((H / 'workflows/schemas/common.schema.json').read_text())
                   ['$defs']['DomainDetailCode']['enum'])
src = (H / 'workflows/workflows_model.v1.py').read_text()
emitted = sorted(set(re.findall(r"Refusal\([^,]+,\s*'([A-Za-z0-9_.]+)'", src)))
rows = []
for code in emitted:
    if code in schema_codes:
        continue
    term = {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED',
            'domainDetail': {'code': code, 'remedy': 'x'}}
    try:
        W.validate_import_record('workflows/schemas/common.schema.json',
                                 '#/$defs/StepTermination', term)
        carrier = 'ADMITS'
    except W.Refusal:
        carrier = 'REFUSES'
    rows.append({'code': code, 'inClosedSchemaEnum': False,
                 'inPublicDetailRegistry': code in {r['code'] for r in registry['records']},
                 'inInternalAliases': code in {a['internalCode'] for a in registry['internalAliases']},
                 'realPublicCarrier': carrier,
                 'emittedBy': 'workflows_model.verify_scope_parameter_binding'})
print(json.dumps({'standing': 'FINDING for root; source deliberately unchanged',
                  'detailCodesEmitted': len(emitted), 'unregistered': rows}, indent=1))
