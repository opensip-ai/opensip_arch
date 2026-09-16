"""Validate every carrier public route against the selected StepTermination schema of the edited copy AND against the
R1/R2-tightened StepTermination from the retained termination assessment (read only), plus D9 v1.14 legality.

Shows the carrier routes stay lawful whether or not root integrates the accepted R1/R2 minimal patch.
"""
import hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
ED = BASE / 'work/edited'
R1R2 = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/disposable/edited/'
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json')
disp = json.loads((ED / 'docs/coop/design-corrections/security/carrier-dispatch.v3.json').read_text())
d9 = json.loads((ED / 'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_text())
fault = dict(d9['codeMaps']['faultCauseToErrorCode'], **{'host-invariant': 'SYSTEM.OUTCOME.ILLEGAL_STATE'})
reject = set(d9['codeMaps']['rejectionCauseToErrorCode'].values())
schemas = {}
for label, path in (('selectedCurrent', ED / 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'),
                    ('r1r2Assessment', R1R2)):
    raw = path.read_bytes()
    doc = json.loads(raw)
    schemas[label] = {'sha256': hashlib.sha256(raw).hexdigest(), 'validator': Draft202012Validator(
        {'$ref': doc['$id'] + '#/$defs/StepTermination'},
        registry=Registry().with_resource(doc['$id'], Resource(contents=doc, specification=DRAFT202012)))}
rows, ok = [], True
for phase in ('writerOrMaintenanceOpen', 'maintenanceActCPublication', 'readOnlyRecovery'):
    for standing, p in disp['publicProjectionByPhase'][phase].items():
        t = {'class': p['class']}
        for k in ('errorCode', 'faultCause'):
            if p[k] is not None:
                t[k] = p[k]
        if p['domainDetail'] is not None:
            t['domainDetail'] = {'code': p['domainDetail'], 'remedy': 'reference projection'}
        legal = (fault.get(p['faultCause']) == p['errorCode']) if p['class'] == 'operational-failed' else (
            p['class'] == 'request-rejected' and p['faultCause'] is None and p['errorCode'] in reject)
        row = {'phase': phase, 'standing': standing, 'termination': t, 'exit': p['exit'], 'd9Legal': legal}
        for label, s in schemas.items():
            errs = sorted(e.message for e in s['validator'].iter_errors(t))
            row[label] = errs or 'ADMIT'
            ok = ok and not errs
        ok = ok and legal
        rows.append(row)
record = {'schemas': {k: v['sha256'] for k, v in schemas.items()}, 'rows': rows, 'allAdmittedAndLegal': ok}
(BASE / 'receipts' / 'p05-route-schema-compat.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if not ok:
    raise SystemExit(1)
