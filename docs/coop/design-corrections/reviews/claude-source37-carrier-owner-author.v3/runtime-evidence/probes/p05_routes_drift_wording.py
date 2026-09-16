"""v3 consistency receipt. Edits nothing.

1. Adoption: v3 DDL statements equal root's alternative applied to v2 final (comment lines excluded); v3 attempt-custody DDL
   equals root's alternative exactly; no byte-length or BLOB predicate remains.
2. Routes unchanged: only dispatch ddlGrammar changed vs v2; S12, read-only, migration and lineage bytes equal v2; every route
   validates under the selected StepTermination and the retained R1/R2 schema and is D9-legal.
3. Wording: no UTF-8-only restriction, fail-closed encoding claim or 'no lawful row is refused' claim in current text; required
   v3 wording present.
4. Drift for root and custody: bindings, generated planning inputs unchanged; frozen37, retained v2 runtime, v2final copy and
   root review files unchanged; only the five expected files differ from v2.
"""
import hashlib, json, re
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
V2RT = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
ROOTREV = Path('/tmp/opensip-design-corrections/root-carrier-encoding-review.v1')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
R1R2 = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/disposable/edited/'
            'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json')
FZ, V2, ED = BASE / 'work/frozen37', BASE / 'work/v2final', BASE / 'work/edited'
p02 = json.loads((BASE / 'receipts/p02-apply-v3.json').read_text())
p00 = json.loads((BASE / 'receipts/p00-setup.json').read_text())
NINE = [f['path'] for f in p02['files']]
DDL = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
AC = 'docs/v2/architecture/attempt-custody.schema.v1.json'
BYTELEN = re.compile(r'length\(CAST\((\w+) AS BLOB\)\) = \d+')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strip_comments(sql):
    return '\n'.join(l for l in sql.splitlines() if not l.lstrip().startswith('--'))


out = {}
v2ddl, v3ddl = (V2 / DDL).read_text(), (ED / DDL).read_text()
v2ac = json.loads((V2 / AC).read_text())['proposedPrivateDDL']
v3ac = json.loads((ED / AC).read_text())['proposedPrivateDDL']
out['ddlStatementsEqualRootAlternative'] = strip_comments(v3ddl) == strip_comments(BYTELEN.subn(r'instr(\1, char(0)) = 0', v2ddl)[0])
out['attemptCustodyDdlEqualsRootAlternative'] = v3ac == BYTELEN.subn(r'instr(\1, char(0)) = 0', v2ac)[0]
out['noByteLengthOrBlobPredicate'] = 'AS BLOB' not in v3ddl and 'AS BLOB' not in v3ac
out['rootCapturedEqualsV2'] = ((ROOTREV / 'captured-carrier.sql').read_bytes() == (V2 / DDL).read_bytes()
                               and (ROOTREV / 'captured-attempt.json').read_bytes() == (V2 / AC).read_bytes())

d2 = json.loads((V2 / 'docs/coop/design-corrections/security/carrier-dispatch.v3.json').read_text())
d3 = json.loads((ED / 'docs/coop/design-corrections/security/carrier-dispatch.v3.json').read_text())
out['dispatchOnlyDdlGrammarChanged'] = set(d2) == set(d3) and all(d2[k] == d3[k] for k in d2 if k != 'ddlGrammar')
out['routeOwnersByteEqualV2'] = {rel: (ED / rel).read_bytes() == (V2 / rel).read_bytes() for rel in (
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
routes_ok, routes = True, []
for phase in ('writerOrMaintenanceOpen', 'maintenanceActCPublication', 'readOnlyRecovery'):
    for standing, p in d3['publicProjectionByPhase'][phase].items():
        t = {'class': p['class']}
        for k in ('errorCode', 'faultCause'):
            if p[k] is not None:
                t[k] = p[k]
        if p['domainDetail'] is not None:
            t['domainDetail'] = {'code': p['domainDetail'], 'remedy': 'reference projection'}
        legal = (fault.get(p['faultCause']) == p['errorCode']) if p['class'] == 'operational-failed' else (
            p['class'] == 'request-rejected' and p['faultCause'] is None and p['errorCode'] in reject)
        row = {'phase': phase, 'standing': standing, 'class': p['class'], 'exit': p['exit'], 'errorCode': p['errorCode'],
               'faultCause': p['faultCause'], 'domainDetail': p['domainDetail'], 'd9Legal': legal}
        for label, (_, v) in validators.items():
            errs = sorted(e.message for e in v.iter_errors(t))
            row[label] = errs or 'ADMIT'
            routes_ok = routes_ok and not errs
        routes_ok = routes_ok and legal
        routes.append(row)
out['routes'] = routes
out['routesAdmittedAndLegal'] = routes_ok
out['schemaSha256'] = {k: v[0] for k, v in validators.items()}

stale = re.compile(r'Byte lengths assume|assume the SQLite database text encoding UTF-8|under another encoding every hex-bearing row is refused|'
                   r'which fails closed|no lawful row is refused|encodingAssumption|Every column\s*(?:--\s*)?therefore states its storage class with typeof', re.I)
hits = []
for rel in NINE:
    text = (ED / rel).read_text(encoding='utf-8')
    for m in stale.finditer(text):
        line = text.count('\n', 0, m.start()) + 1
        hits.append('%s:%d %s' % (rel, line, m.group(0)))
required = {
    DDL: ['instr(column, char(0)) = 0', 'no encoding is required of a carrier', 'either by an explicit typeof() guard'],
    'docs/coop/design-corrections/security/carrier-format.v3.md': ['no encoding is required of a carrier', 'by one of two mechanisms',
                                                                  'the v2 encoding restriction is withdrawn', 'including the source37 v1 and v2 revisions'],
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json': ['encodingIndependence', 'instr(column, char(0)) = 0', 'by one of two mechanisms'],
    AC: ['exact enumeration on phase and settled_outcome', 'no encoding is required'],
}
missing = [rel + ': ' + s for rel, ss in required.items() for s in ss if s not in (ED / rel).read_text(encoding='utf-8')]
out['staleWordingHits'] = hits
out['requiredWordingMissing'] = missing

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
out['bindingDrift'] = [{'path': f['path'], 'frozen37': f['frozen37Sha256'], 'v2': f['v2Sha256'], 'v3': f['v3Sha256'], 'changedInV3': f['changedInV3'],
                        'manifestPinIsFrozen': sorted(pins.get(f['path'], set())) == [f['frozen37Sha256']],
                        'normativeInputsV5': f['path'] in v5,
                        'coverageSources': len([k for k, r in coverage['sources'].items() if r['path'] == f['path']]),
                        'pinLedgers': len([l for l, lp in ledgers.items() if f['path'] in lp])} for f in p02['files']]
out['generatedPlanningInputsUnchanged'] = {rel: (ED / rel).read_bytes() == (FZ / rel).read_bytes() for rel in (
    'docs/v2/architecture/commit-recovery-plan.v1.json', 'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/architecture/implementation-normative-inputs.v5.json', 'docs/coop/completion/security-schemas.v2/grant-journal.sql',
    'docs/coop/design-corrections/security/source-pins.v1.json', 'docs/coop/design-corrections/current-source-map.proposed.md')}
out['frozen37Unchanged'] = all(sha((FROZEN / r['path']).read_bytes()) == r['frozen37'] for r in p00['rows'])
out['v2RuntimeUnchanged'] = (all(sha((V2RT / n).read_bytes()) == h for n, h in p00['v2Review'].items())
                             and all(sha((V2RT / 'work/edited' / r['path']).read_bytes()) == r['v2'] for r in p00['rows']))
out['rootReviewUnchanged'] = all(sha((ROOTREV / n).read_bytes()) == h for n, h in p00['rootCaptured'].items())
tree = json.loads((BASE / 'receipts/p00-v2-edited-tree-manifest.json').read_text())
out['v2finalCopyUnchanged'] = all(sha((V2 / k).read_bytes()) == v for k, v in tree.items())
out['editedDiffersFromV2In'] = sorted(k for k, v in tree.items() if sha((ED / k).read_bytes()) != v)
out['editedExtraFiles'] = sorted(str(p.relative_to(ED)) for p in ED.rglob('*') if p.is_file() and str(p.relative_to(ED)) not in tree)
ok = (out['ddlStatementsEqualRootAlternative'] and out['attemptCustodyDdlEqualsRootAlternative'] and out['noByteLengthOrBlobPredicate']
      and out['rootCapturedEqualsV2'] and out['dispatchOnlyDdlGrammarChanged'] and all(out['routeOwnersByteEqualV2'].values())
      and routes_ok and not hits and not missing and all(out['generatedPlanningInputsUnchanged'].values())
      and out['frozen37Unchanged'] and out['v2RuntimeUnchanged'] and out['rootReviewUnchanged'] and out['v2finalCopyUnchanged']
      and not out['editedExtraFiles'] and out['editedDiffersFromV2In'] == sorted(f['path'] for f in p02['files'] if f['changedInV3']))
out['allOk'] = ok
(BASE / 'receipts' / 'p05-routes-drift-wording.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('routes', 'bindingDrift')}, indent=2))
if not ok:
    raise SystemExit(1)
