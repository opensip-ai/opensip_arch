"""v2 consistency receipt. Edits nothing.

1. Routes unchanged: publicProjectionByPhase, S12, read-only, migration and lineage bytes equal v1; every route still
   validates under the selected StepTermination and the retained R1/R2 schema, and is D9-legal.
2. Wording: no v2 nine-file text still claims earlier carrierFormat 3 / attempt_custody bytes were never instantiated
   or that the grammar was exact before this revision; the corrected product-scoped wording is present.
3. Binding drift for root: frozen37 manifest pins, normative-inputs v5, coverage sources, pin ledgers, planning
   contractSections; generated planning inputs unchanged; frozen37, retained v1 runtime and v1final copy unchanged.
"""
import hashlib, json, re
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
V1RT = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
R1R2 = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/disposable/edited/'
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json')
FZ, V1, ED = BASE / 'work/frozen37', BASE / 'work/v1final', BASE / 'work/edited'
p02 = json.loads((BASE / 'receipts/p02-apply-v2.json').read_text())
p00 = json.loads((BASE / 'receipts/p00-setup.json').read_text())
NINE = [f['path'] for f in p02['files']]


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = {}
# 1. routes
d1 = json.loads((V1 / 'docs/coop/design-corrections/security/carrier-dispatch.v3.json').read_text())
d2 = json.loads((ED / 'docs/coop/design-corrections/security/carrier-dispatch.v3.json').read_text())
unchanged_keys = {k: d1[k] == d2[k] for k in d1 if k != 'ddlGrammar'}
out['dispatchOnlyDdlGrammarChanged'] = all(unchanged_keys.values()) and set(d1) == set(d2)
out['routeOwnersByteEqualV1'] = {rel: (ED / rel).read_bytes() == (V1 / rel).read_bytes() for rel in (
    'docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/architecture/commit-recovery-readonly.v3.md',
    'docs/coop/design-corrections/security/carrier-migration.v1.md', 'docs/v2/architecture/store-instance-lineage.v1.json')}
d9 = json.loads((ED / 'docs/coop/artifacts/d9-exit-contract.v1.14.json').read_text())
fault = dict(d9['codeMaps']['faultCauseToErrorCode'], **{'host-invariant': 'SYSTEM.OUTCOME.ILLEGAL_STATE'})
reject = set(d9['codeMaps']['rejectionCauseToErrorCode'].values())
validators = {}
for label, path in (('selectedCurrent', ED / 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'), ('r1r2Assessment', R1R2)):
    doc = json.loads(path.read_bytes())
    validators[label] = (sha(path.read_bytes()), Draft202012Validator({'$ref': doc['$id'] + '#/$defs/StepTermination'},
                         registry=Registry().with_resource(doc['$id'], Resource(contents=doc, specification=DRAFT202012))))
routes_ok = True
routes = []
for phase in ('writerOrMaintenanceOpen', 'maintenanceActCPublication', 'readOnlyRecovery'):
    for standing, p in d2['publicProjectionByPhase'][phase].items():
        t = {'class': p['class']}
        for k in ('errorCode', 'faultCause'):
            if p[k] is not None:
                t[k] = p[k]
        if p['domainDetail'] is not None:
            t['domainDetail'] = {'code': p['domainDetail'], 'remedy': 'reference projection'}
        legal = (fault.get(p['faultCause']) == p['errorCode']) if p['class'] == 'operational-failed' else (
            p['class'] == 'request-rejected' and p['faultCause'] is None and p['errorCode'] in reject)
        row = {'phase': phase, 'standing': standing, 'd9Legal': legal}
        for label, (_, v) in validators.items():
            errs = sorted(e.message for e in v.iter_errors(t))
            row[label] = errs or 'ADMIT'
            routes_ok = routes_ok and not errs
        routes_ok = routes_ok and legal
        routes.append(row)
out['routes'] = routes
out['routesAdmittedAndLegal'] = routes_ok
out['schemaSha256'] = {k: v[0] for k, v in validators.items()}

# 2. wording
stale = re.compile(r'never instantiated|instance was ever created|table was ever created|never created from|'
                   r'matches? the stated grammar exactly|enforces the stated grammar exactly|stated grammar is enforced', re.I)
hits = []
for rel in NINE:
    for i, line in enumerate((ED / rel).read_text(encoding='utf-8').splitlines()):
        if stale.search(line):
            hits.append('%s:%d %s' % (rel, i + 1, line.strip()[:120]))
required = {
    'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql': ['No product implementation or deployed carrier', 'Reference in-memory SQLite instances'],
    'docs/coop/design-corrections/security/carrier-format.v3.md': ['No product implementation or deployed carrier', 'Reference in-memory SQLite instances', '**Revision history of this law.**'],
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json': ['No product implementation or deployed carrier', 'Reference in-memory SQLite instances'],
    'docs/v2/architecture/attempt-custody.schema.v1.json': ['No product implementation or deployed ledger table', 'reference in-memory SQLite instances'],
}
missing = [rel + ': ' + s for rel, ss in required.items() for s in ss if s not in (ED / rel).read_text(encoding='utf-8')]
out['staleWordingHits'] = hits
out['requiredWordingMissing'] = missing

# 3. drift and custody
pins = {}


def walk(o, into):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            into.setdefault(o['path'], set()).add(o['sha256'])
        for v in o.values():
            walk(v, into)
    elif isinstance(o, list):
        for v in o:
            walk(v, into)


walk(json.loads(MANIFEST.read_bytes()), pins)
v5 = {r['path']: r['sha256'] for r in json.loads((FZ / 'docs/v2/architecture/implementation-normative-inputs.v5.json').read_text())['files']}
coverage = json.loads((FZ / 'docs/v2/architecture/implementation-coverage.v1.json').read_text())
ledgers = {}
for p in sorted((FZ / 'docs/coop/design-corrections').rglob('*source-pins*.json')):
    lp = {}
    walk(json.loads(p.read_text()), lp)
    ledgers[str(p.relative_to(FZ))] = lp
drift = []
for f in p02['files']:
    rel = f['path']
    drift.append({'path': rel, 'frozen37': f['frozen37Sha256'], 'v1': f['v1Sha256'], 'v2': f['v2Sha256'], 'changedInV2': f['changedInV2'],
                  'manifestPinIsFrozen': sorted(pins.get(rel, set())) == [f['frozen37Sha256']],
                  'normativeInputsV5': rel in v5, 'coverageSources': [k for k, r in coverage['sources'].items() if r['path'] == rel],
                  'pinLedgers': sorted(l for l, lp in ledgers.items() if rel in lp)})
out['bindingDrift'] = drift
out['generatedPlanningInputsUnchanged'] = {rel: (ED / rel).read_bytes() == (FZ / rel).read_bytes() for rel in (
    'docs/v2/architecture/commit-recovery-plan.v1.json', 'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/architecture/implementation-normative-inputs.v5.json', 'docs/coop/completion/security-schemas.v2/grant-journal.sql',
    'docs/coop/design-corrections/security/source-pins.v1.json', 'docs/coop/design-corrections/current-source-map.proposed.md')}
out['frozen37Unchanged'] = all(sha((FROZEN / r['path']).read_bytes()) == r['frozenSha256'] for r in p00['rows'])
out['v1RuntimeUnchanged'] = (sha((V1RT / 'review.json').read_bytes()) == p00['v1ReviewJsonSha256']
                             and sha((V1RT / 'review.md').read_bytes()) == p00['v1ReviewMdSha256']
                             and sha((V1RT / 'proposed-edits.diff').read_bytes()) == p00['v1ProposedEditsDiffSha256']
                             and all(sha((V1RT / 'work/edited' / f['path']).read_bytes()) == f['v1Sha256'] for f in p02['files']))
tree = json.loads((BASE / 'receipts/p00-v1-edited-tree-manifest.json').read_text())
out['v1finalCopyUnchanged'] = all(sha((V1 / k).read_bytes()) == v for k, v in tree.items())
out['editedDiffersFromV1OnlyInFiveFiles'] = sorted(k for k, v in tree.items() if sha((ED / k).read_bytes()) != v)
extra = sorted(str(p.relative_to(ED)) for p in ED.rglob('*') if p.is_file() and str(p.relative_to(ED)) not in tree)
out['editedExtraFiles'] = extra
ok = (out['dispatchOnlyDdlGrammarChanged'] and all(out['routeOwnersByteEqualV1'].values()) and routes_ok and not hits and not missing
      and all(out['generatedPlanningInputsUnchanged'].values()) and out['frozen37Unchanged'] and out['v1RuntimeUnchanged']
      and out['v1finalCopyUnchanged'] and not extra
      and out['editedDiffersFromV1OnlyInFiveFiles'] == sorted(f['path'] for f in p02['files'] if f['changedInV2']))
out['allOk'] = ok
(BASE / 'receipts' / 'p05-routes-drift-wording.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('routes', 'bindingDrift')}, indent=2))
if not ok:
    raise SystemExit(1)
