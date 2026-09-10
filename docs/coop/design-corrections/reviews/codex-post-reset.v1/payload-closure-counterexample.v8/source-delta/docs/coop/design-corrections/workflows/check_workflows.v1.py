"""Workflows-and-surfaces reference checker: schema closure, hand-authored cases, model execution, report.
Run: python -I -B check_workflows.v1.py --report workflows-report.v1.json  (Python 3.12, jsonschema 4.25.1)
Design evidence only; not product qualification.
"""
import argparse
import copy
import glob
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'foundation'))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator, ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

spec = importlib.util.spec_from_file_location('workflows_model', HERE / 'workflows_model.v1.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

CHECKS = []

def check(cid, ok, detail=''):
    CHECKS.append({'id': cid, 'ok': bool(ok), 'detail': detail if not ok else ''})
    return ok

# ----------------------------------------------------------------------------- schema registry
SCHEMAS = {}
for p in sorted(glob.glob(str(HERE / 'schemas' / '*.schema.json'))):
    s = canonical.parse(Path(p).read_bytes())
    Draft202012Validator.check_schema(s)
    SCHEMAS[s['$id']] = s
FOUNDATION = canonical.parse((HERE.parent / 'foundation' / 'identity-schemas.v2.json').read_bytes())
REG = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()] + [(FOUNDATION['$id'], Resource(contents=FOUNDATION, specification=DRAFT202012))])
U = 'urn:opensip:product-v1:workflows:'

def validator(ref):
    sid, _, frag = ref.partition('#')
    return canonical.ExactValidator({'$ref': sid + '#' + frag} if frag else {'$ref': sid}, registry=REG)

def valid(ref, value):
    try:
        canonical.typed(value)
        validator(ref).validate(value)
        return True, ''
    except (ValidationError, canonical.AdmissionError) as e:
        return False, str(e).splitlines()[0][:200]

def must_valid(cid, ref, value):
    ok, why = valid(ref, value)
    return check(cid, ok, why)

def must_invalid(cid, ref, value):
    ok, _ = valid(ref, value)
    return check(cid, not ok, 'unexpectedly valid')

# Numeric confidence uses only the declared numeric operators; string coercion is not policy semantics.
for cmp in ('eq', 'neq', 'in', 'prefix', 'glob'):
    must_invalid('policy.numeric-field-string-operator.' + cmp, U + 'policy-document#/$defs/FieldFilter',
                 {'field': 'confidenceMillionths', 'cmp': cmp, 'value': ['900000'] if cmp == 'in' else '900000'})
for cmp in ('gte', 'lte'):
    must_valid('policy.numeric-field-number-operator.' + cmp, U + 'policy-document#/$defs/FieldFilter',
               {'field': 'confidenceMillionths', 'cmp': cmp, 'value': 900000})

def synthetic_recovery_projection(journal, plan):
    # Unit-only trusted projection; actual security admission is exercised by check-integration.py.
    journal_ref, state_digest = M.recovery_journal_bindings(journal)
    return {'result': 'ADMIT', 'repairPlanId': plan['repairPlanId'], 'originalRequestId': journal['requestId'],
            'projectId': plan['descriptor']['projectId'], 'baseSnapshotId': journal['baseSnapshotId'],
            'journalRef': journal_ref, 'journalStateDigest': state_digest,
            'recoveryAction': M.RECOVERY_TABLE[journal['state']][0],
            'securityRecoveryAuthorizationRef': 'security.repair-recovery-authorization.v1:' + 'c' * 64}

# ----------------------------------------------------------------------------- cases
RAW = canonical.parse((HERE / 'workflow-cases.v1.json').read_bytes())
C = dict(RAW['constants'])
C['ARGV'] = M.raw_sha(canonical.canonical(['scripts/test.sh', '--ci']))
C['ARGV2'] = M.raw_sha(canonical.canonical(['/usr/bin/bash', '-c', 'rm -rf .']))
C['TOOL0#bin/node']=C['TOOL0']+'#bin/node'
C['ARGV4']=M.raw_sha(canonical.canonical(['node','test.js']))
C['ARGV3'] = M.raw_sha(canonical.canonical(['bin/node', 'test.js']))

def sub(o):
    if isinstance(o, str) and o.startswith('$'):
        key = o[1:]
        if key in C:
            return C[key]
        if key in RAW['policyDocs']:
            return sub(RAW['policyDocs'][key])
        raise KeyError(o)
    if isinstance(o, dict):
        return {sub(k) if isinstance(k, str) and k.startswith('$') else k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    return o

CASES = sub(RAW)
POL = CASES['policyDocs']
ROOT_SCHEMA_CHECKS = 0
for sid in SCHEMAS:
    ROOT_SCHEMA_CHECKS += 1
check('schemas.compiled', len(SCHEMAS) == 13, str(len(SCHEMAS)))
check('foundation.import-def-present', 'import' in FOUNDATION['$defs'])

# ----------------------------------------------------------------------------- schema vectors
for defn, vec in CASES['schemaVectors'].items():
    for i, v in enumerate(vec['accept']):
        must_valid(f'vector.{defn}.accept.{i}', U + 'common#/$defs/' + defn, v)
    for i, v in enumerate(vec['reject']):
        must_invalid(f'vector.{defn}.reject.{i}', U + 'common#/$defs/' + defn, v)
for i, t in enumerate(CASES['terminationVectors']['accept']):
    must_valid(f'termination.accept.{i}', U + 'common#/$defs/StepTermination', t)
for i, t in enumerate(CASES['terminationVectors']['reject']):
    must_invalid(f'termination.reject.{i}', U + 'common#/$defs/StepTermination', t)
for i, e in enumerate(CASES['envelopeVectors']['accept']):
    must_valid(f'envelope.accept.{i}', U + 'command-envelope', e)
    check(f'envelope.accept.{i}.exit-matches-class', M.EXIT[e['termination']['class']] == e['exitCode'])
for i, e in enumerate(CASES['envelopeVectors']['reject']):
    must_invalid(f'envelope.reject.{i}', U + 'command-envelope', e)

# ----------------------------------------------------------------------------- inventory
INV = canonical.parse((HERE / 'command-inventory.v1.json').read_bytes())
must_valid('inventory.schema', U + 'command-inventory', INV)
names = [c['name'] for c in INV['commands']]
enum = SCHEMAS[U + 'command-inventory']['$defs']['CommandName']['enum']
check('inventory.every-command-once', sorted(names) == sorted(enum) and len(set(names)) == len(names))
rend = {r['format']: r for r in INV['renderers']}
for c in INV['commands']:
    check('inventory.formats-applicable.' + c['name'], all(c['requestClass'] in rend[f]['applicability'] for f in c['formats']))
    check('inventory.tracked-intent-explicit.' + c['name'], (not c['writesTrackedIntent']) or c['name'] in ('policy-init', 'waive', 'baseline-adopt', 'baseline-export', 'baseline-upgrade'))
    check('inventory.repo-exec-only-explicit-commands.' + c['name'], (c['repositoryExecution'] == 'never') == (c['name'] not in ('test-run', 'native-prepare')))
    check('inventory.advisory-never-sarif.' + c['name'], (not c['advisory']) or 'sarif' not in c['formats'])
check('inventory.default-is-durable-authoritative', next(c for c in INV['commands'] if c['name'] == 'default')['authority'] == 'authoritative-default')
check('inventory.has-lifecycle-and-doctor', {'install', 'update', 'doctor', 'purge'} <= set(names))
gold_ids = [g['id'] for g in INV['goldens']]
check('inventory.golden-ids-unique', len(set(gold_ids)) == len(gold_ids))
for g in INV['goldens']:
    obs = CASES['goldenObservations'].get(g['id'])
    if not check('golden.observation-present.' + g['id'], obs is not None):
        continue
    t = M.terminate(obs)
    ok = t['class'] == g['class'] and M.exit_code(t) == g['exitCode'] and t.get('errorCode') == g.get('errorCode') and (t.get('reasonCodes') or [None])[0] == g.get('reasonCode') and t.get('domainDetail', {}).get('code') == g.get('domainDetail')
    check('golden.model-reaches.' + g['id'], ok, json.dumps(t))
    must_valid('golden.termination-schema.' + g['id'], U + 'common#/$defs/StepTermination', t)
check('golden.doctor-defects-exit-zero', M.exit_code(M.terminate(CASES['goldenObservations']['doctor-defects-found'])) == 0)
check('golden.unavailable-3-vs-delivery-4', M.exit_code(M.terminate(CASES['goldenObservations']['default-missing-required-closure'])) == 3 and M.exit_code(M.terminate(CASES['goldenObservations']['default-closure-bytes-corrupt'])) == 4)

# ----------------------------------------------------------------------------- invocation lifecycle
def build_record(case, rid):
    steps = []
    for i, s in enumerate(case['steps']):
        steps.append({'stepId': i, 'kind': s['kind'], 'requirement': s['requirement'], 'dependsOn': s['dependsOn'], 'dependencyGate': s['gate'], 'retryPolicy': s['retry'], 'params': s['params']})
    return {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 1, 'requestId': rid, 'projectId': C['PRJ'], 'workflow': {'kind': 'builtin', 'name': 'analyze'}, 'mode': case['mode'], 'orderedSteps': steps}

for case in CASES['invocationCases']:
    cid = 'invocation.' + case['id']
    rec = build_record(case, C['REQ'])
    exp = case['expect']
    if exp.get('schemaInvalid'):
        must_invalid(cid + '.schema-invalid', U + 'invocation-record', rec)
        continue
    if not must_valid(cid + '.spec-schema', U + 'invocation-record', rec):
        continue
    try:
        out, code = M.run_invocation(rec, case['script'])
    except M.Refusal as r:
        check(cid + '.refusal', exp.get('refusal') == r.detail, r.detail)
        continue
    if 'refusal' in exp:
        check(cid + '.refusal', False, 'no refusal')
        continue
    must_valid(cid + '.record-schema', U + 'invocation-record', out)
    check(cid + '.exit', code == exp['exit'] and out['termination']['class'] == exp['class'], json.dumps(out['termination']))
    if 'outcomes' in exp:
        check(cid + '.outcomes', [r['outcome'] for r in out['stepResults']] == exp['outcomes'], json.dumps([r['outcome'] for r in out['stepResults']]))
    if 'runIdInTermination' in exp:
        check(cid + '.run-in-termination', out['termination'].get('runId') == exp['runIdInTermination'])
    if exp.get('noRunId'):
        check(cid + '.no-run-id', 'runId' not in out['termination'] and not any('runId' in (r.get('result') or {}) for r in out['stepResults']))
    if 'detail' in exp:
        check(cid + '.detail', out['termination'].get('domainDetail', {}).get('code') == exp['detail'], json.dumps(out['termination']))
    if 'errorCode' in exp:
        check(cid + '.error-code', out['termination'].get('errorCode') == exp['errorCode'])
    if 'faultCause' in exp:
        check(cid + '.fault-cause', out['termination'].get('faultCause') == exp['faultCause'])
    if 'reasonCode' in exp:
        check(cid + '.reason-code', exp['reasonCode'] in out['termination'].get('reasonCodes', []))
    if 'phase' in exp:
        check(cid + '.cancel-phase', out['cancellation']['phase'] == exp['phase'])
    if 'skipReason' in exp:
        check(cid + '.skip-reason', all(out['stepResults'][int(k)].get('skipReason') == v for k, v in exp['skipReason'].items()))
    if 'attempts' in exp:
        check(cid + '.attempts', all(len(out['stepResults'][int(k)]['attempts']) == v for k, v in exp['attempts'].items()))
    if exp.get('distinctExecutionIds'):
        ids = [a['executionId'] for r in out['stepResults'] for a in r['attempts']]
        check(cid + '.distinct-execution-ids', len(set(ids)) == len(ids) and all(valid(U + 'common#/$defs/ExecutionId', i)[0] for i in ids))
    if exp.get('verifyRunDiffers'):
        check(cid + '.verify-run-differs', out['stepResults'][0]['result']['runId'] != out['stepResults'][3]['result']['runId'])
        check(cid + '.verify-resnapshot', out['stepResults'][3]['result']['verification']['verifiedSnapshotId'] == out['stepResults'][2]['result']['appliedSnapshotId'])
    if exp.get('derivationDistinct'):
        d0, d3 = out['stepResults'][0]['attempts'][0]['derivation'], out['stepResults'][3]['attempts'][0]['derivation']
        check(cid + '.derivation-binding-distinct', d0['executionPlanId'] != d3['executionPlanId'] and d0['stageCount'] <= 1024)
check('invocation.step-bound-64', SCHEMAS[U + 'invocation-record']['properties']['orderedSteps']['maxItems'] == 64 and SCHEMAS[U + 'common']['$defs']['StepId']['maximum'] == 63)
check('invocation.derivation-bound-1024', SCHEMAS[U + 'invocation-record']['$defs']['DerivationBinding']['properties']['stageCount']['maximum'] == 1024 and FOUNDATION['$defs']['execution-plan']['properties']['stages']['maxItems'] == 1024)
check('invocation.ephemeral-union-closed', all('runId' not in b['properties'] for b in SCHEMAS[U + 'invocation-record']['$defs']['AnalysisResult']['oneOf'] if b['properties']['authority']['const'] == 'ephemeral'))

# ----------------------------------------------------------------------------- baseline + comparison
def fixture_evidence(value,overrides=None):
    v=copy.deepcopy(value)
    v['imports']=[{'kind':kind,'importId':(overrides or {}).get(kind,C['IMP_RT'] if kind=='runtime' else C['IMP_HIST']), 'payloadDigest':C['H0'],'sourceCorrespondenceDigest':C['H0'],'scopeDigest':C['H0'],'observationDigest':C['H0']} for kind in v['importKinds']]
    return v
BS = CASES['baselineSpec']

def make_baseline(policy, scope, waivers, rule_cov, project=C['PRJ'], evidence=None):
    run = {'authority': 'authoritative', 'availability': 'retained', 'snapshotId': C['SNAP0'], 'runId': C['RUN0']}
    ctx = {'detectorClosureIds': [d['closureId'] for d in BS['detectorClosure']], 'evidenceAvailability': fixture_evidence(evidence or BS['evidenceAvailability'])}
    return M.adopt_baseline(run, C['PLAN0'], project, policy, scope, waivers, rule_cov, BS['entries'], BS['detectorClosure'], BS['pivotClosure'], ctx, '1.0.0')

BASE = make_baseline(POL['basePolicy'], POL['scopeAll'], POL['waiversFp2'], CASES['ruleCoverage']['full'])
must_valid('baseline.artifact-schema', U + 'baseline-artifact', BASE)
check('baseline.fresh-ci-verify', M.verify_baseline_artifact(BASE))
check('baseline.pins-run-and-pivot-closures', set(BASE['custody']['retentionPins']) == {C['RUN0'], C['DET_A0'], C['EVAL0'], C['TOOL0']})
check('baseline.identity-excludes-custody', M.wid('baseline2', 'workflow.baseline', BASE['descriptor']) == BASE['baselineId'])
tampered = copy.deepcopy(BASE)
tampered['descriptor']['entries'][0]['waived'] = True
try:
    M.verify_baseline_artifact(tampered); check('baseline.tamper-detected', False)
except M.Refusal as r:
    check('baseline.tamper-detected', r.detail == 'IMPORT.ARTIFACT_CORRUPT')
try:
    M.adopt_baseline({'authority': 'ephemeral', 'snapshotId': C['SNAP0'], 'runId': C['RUN0']}, C['PLAN0'], C['PRJ'], POL['basePolicy'], POL['scopeAll'], POL['waiversNone'], CASES['ruleCoverage']['full'], BS['entries'], BS['detectorClosure'], BS['pivotClosure'], {'detectorClosureIds': [C['DET_A0']], 'evidenceAvailability': BS['evidenceAvailability']}, '1.0.0')
    check('baseline.ephemeral-cannot-adopt', False)
except M.Refusal as r:
    check('baseline.ephemeral-cannot-adopt', r.detail == 'BASELINE.SOURCE_EPHEMERAL')
legacy = copy.deepcopy(BASE['descriptor']['entries'][0]); legacy['legacyFingerprint'] = 'fp1:' + 'e' * 64
must_valid('baseline.legacy-fingerprint-is-migration-field-only', U + 'baseline-artifact#/$defs/BaselineEntry', legacy)
check('baseline.pivot-closure-never-legacy', all(p['kind'] in ('detector', 'evaluator', 'toolchain', 'stdlib', 'schema-set') for p in BASE['descriptor']['pivotClosure']))

for case in CASES['comparisonCases']:
    cid = 'comparison.' + case['id']
    base = copy.deepcopy(BASE)
    if 'baselineEntries' in case:
        base['descriptor']['entries'] = copy.deepcopy(case['baselineEntries'])
        base['baselineId'] = M.wid('baseline2', 'workflow.baseline', base['descriptor'])
    if case.get('tamperContext'):
        base['descriptor']['contextDocuments']['policy'] = POL['policyDisabledUnused']
    bd = dict(base['descriptor']); bd['_baselineId'] = base['baselineId']
    cur_ctx = {'policyDigest': M.doc_digest(POL[case['currentPolicy']]), 'scopeDigest': M.doc_digest(POL[case['currentScope']]),
               'waiverSetDigest': M.doc_digest(POL[case['currentWaivers']]), 'detectorClosureIds': [case['currentDetector']['closureId']], 'evidenceAvailability': fixture_evidence(case['currentEvidence'],case.get('importOverrides'))}
    presence, entry_rules = {}, {}
    bmap = {e['fingerprint']: e for e in BS['entries']}
    rule_of = {C['FP1']: ('no-unused-export', 'ts-detector'), C['FP2']: ('no-unused-export', 'ts-detector'), C['FP3']: ('no-unused-export', 'ts-detector'), C['FP4']: ('no-unused-export', 'ts-detector'), C['FP5']: ('runtime-unhit-export', 'ts-detector'), C['FP6']: ('stale-file-advisory', 'ts-detector')}
    for fp, p in case['presence'].items():
        presence[fp] = {'B': fp in bmap, 'E0': p['E0'], 'E1': p['E1'], 'E2': p['E2'], 'E3': p['E3'], 'E4': p['E4'], 'waivedB': bmap[fp]['waived'] if fp in bmap else False, 'waivedC': p['waivedC']}
        entry_rules[fp] = case.get('entryRules',{}).get(fp) or rule_of[fp]
    current = {'runId': C['RUN1'], 'snapshotId': C['SNAP1'], 'projectId': case.get('currentProject', C['PRJ']), 'context': cur_ctx, 'ruleCoverage': {r['ruleId']: r for r in CASES['ruleCoverage'][case['currentRuleCoverage']]}, 'presence': presence, 'entryRules': entry_rules}
    cd = case.get('currentDetectors',{'ts-detector': dict(case['currentDetector'])})
    current['context']['detectorClosureIds']=sorted(d['closureId'] for d in cd.values())
    current['boundPivots']=case.get('boundPivots',['E1','E2','E3'])
    for over in case.get('ruleCoverageOverride',[]):current['ruleCoverage'][over['ruleId']].update(over)
    res = M.compare(bd, current, CASES['hosts'][case['host']], case['profile'], cd, tuple(case.get('acceptOrigins', [])))
    must_valid(cid + '.schema', U + 'comparison-result', res)
    d, exp = res['descriptor'], case['expect']
    check(cid + '.performed', d['comparisonPerformed'] == exp['performed'])
    check(cid + '.verdict', d['verdict'] == exp['verdict'], d['verdict'])
    if 'E0' in exp:
        check(cid + '.pivot-E0', d['pivotsAvailable']['E0'] == exp['E0'], d['pivotsAvailable']['E0'])
    for pv in ('E1', 'E2', 'E3'):
        if pv in exp:
            check(cid + '.pivot-' + pv, d['pivotsAvailable'][pv] == exp[pv])
    if 'detectorMethods' in exp:
        check(cid + '.detector-methods', {x['detectorId']: x['method'] for x in d['detectors']} == exp['detectorMethods'])
    if 'ruleDeficiencies' in exp:
        check(cid + '.rule-deficiencies', [[x['ruleId'], x['gating'], x['cause']] for x in d['ruleDeficiencies']] == exp['ruleDeficiencies'])
    if 'detectorMethod' in exp:
        check(cid + '.detector-method', d['detectors'][0]['method'] == exp['detectorMethod'], d['detectors'][0]['method'])
    if 'detectorReason' in exp:
        check(cid + '.detector-reason', d['detectors'][0].get('indeterminateReason') == exp['detectorReason'])
    if 'wholeReason' in exp:
        check(cid + '.whole-reason', d.get('wholeIndeterminateReason') == exp['wholeReason'] and d['entries'] == [])
    if 'remedyCode' in exp:
        check(cid + '.remedy-code', d['remedy']['code'] == exp['remedyCode'])
    if 'correspondence' in exp:
        check(cid + '.correspondence', d['projectCorrespondence'] == exp['correspondence'])
    if 'd9Deficiency' in exp:
        check(cid + '.d9-deficiency', d.get('d9Deficiency') == exp['d9Deficiency'], d.get('d9Deficiency'))
    ents = {e['fingerprint']: e for e in d['entries']}
    for fp, ex in exp.get('entries', {}).items():
        e = ents.get(fp)
        ok = e is not None and e['classification'] == ex[0] and e['gates'] == ex[1] and (len(ex) < 3 or e.get('gateReason') == ex[2])
        check(cid + '.entry.' + fp[-4:], ok, json.dumps(e))
    for fp, axes in exp.get('subsequent', {}).items():
        check(cid + '.subsequent.' + fp[-4:], ents[fp]['subsequentDeltas'] == axes, json.dumps(ents[fp]['subsequentDeltas']))
    for fp, reason in exp.get('entryReason', {}).items():
        check(cid + '.entry-reason.' + fp[-4:], ents[fp].get('indeterminateReason') == reason)
    for k, v in exp.get('counts', {}).items():
        check(cid + '.count.' + k, d['counts'][k] == v, str(d['counts'][k]))
    check(cid + '.entries-sorted', [e['fingerprint'] for e in d['entries']] == sorted(e['fingerprint'] for e in d['entries']))
    check(cid + '.gating-count-consistent', d['counts']['gating'] == sum(1 for e in d['entries'] if e['gates']))
    check(cid + '.identity-recomputes', M.wid('comparison2', 'workflow.comparison', d) == res['comparisonResultId'])
check('comparison.profiles-schema', all(valid(U + 'comparison-result#/$defs/AuditProfile', p)[0] for p in M.AUDIT_PROFILES.values()))
check('comparison.enum-precedence-not-gate', all(SCHEMAS[U + 'comparison-result']['$defs']['Entry']['properties']['gates']['type'] == 'boolean' for _ in [0]))

# ----------------------------------------------------------------------------- imports
REGISTERED={domain:(HERE.parent/row['schemaDocument']).read_bytes() for (kind,domain),row in M.PAYLOAD_REGISTRY.items()}
native_spec = importlib.util.spec_from_file_location('native_import_fixture_adapter', HERE.parent / 'native' / 'native_evidence_model.v2.py')
N = importlib.util.module_from_spec(native_spec); native_spec.loader.exec_module(N)
NF = canonical.parse((HERE.parent / 'native' / 'native-cases.v2.json').read_bytes())['fixtures']
DS = N.dependency_source_set_admit(NF['lock'], [NF['tarballRow']], ['serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index'])
NATIVE_PAYLOADS = {
    'native.import-payload.dependency-source.v1': {'schemaVersion': 1, 'payloadDomain': 'native.import-payload.dependency-source.v1', 'set': DS['descriptor'], 'acquisitionSourcePath': '/synthetic/cache', 'tarballDigests': [{'packageKey': 'serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index', 'crateTarballSha256': 'a' * 64}]},
    'native.import-payload.prepared-output.v1': {'schemaVersion': 1, 'payloadDomain': 'native.import-payload.prepared-output.v1', 'set': NF['prepInert']},
}
RT = CASES['runtimePayload']
must_valid('import.runtime-payload-schema', U + 'imported-evidence#/$defs/RuntimePayloadV1', RT)
built = {}
for case in CASES['importCases']:
    cid = 'import.' + case['id']
    regs = dict(REGISTERED)
    if case.get('unregister'):
        regs.pop(case['payloadDomain'])
    payload = dict(RT) if case['payloadDomain'].startswith('workflow') else copy.deepcopy(NATIVE_PAYLOADS.get(case['payloadDomain'], {'payloadDomain': case['payloadDomain']}))
    payload.update(case.get('payloadOverride', {}))
    if case.get('replaceSchemaBytes'):
        regs[case['payloadDomain']] = b'{"type":"object"}'
    payload['payloadDomain'] = case['payloadDomain'] if case['payloadDomain'] != 'workflow.import-payload.runtime.v1' else RT['payloadDomain']
    try:
        r = M.build_import(case['kind'], payload, case['payloadDomain'], regs, case['correspondence'], C['PROD'], C['ADAPT'], [{'path': 'coverage/v8.json', 'sha256': C['H0'], 'bytes': 10}], {'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['src'],'excludedPathPrefixes':[]}, {'window':case.get('window'), 'population':'test-suite', 'completeness':case.get('completeness','partial'),'omissions':case.get('omissions',['dist not instrumented'])})
    except M.Refusal as x:
        check(cid + '.refusal', case['expect'].get('refusal') == x.detail and (case['expect'].get('errorCode') is None or case['expect']['errorCode'] == x.error_code), x.detail)
        continue
    if 'refusal' in case['expect']:
        check(cid + '.refusal', False, 'no refusal'); continue
    built[case['id']] = r
    must_valid(cid + '.wrapper-foundation-import-schema', FOUNDATION['$id'] + '#/$defs/import', r['wrapper'])
    must_valid(cid + '.wrapper-workflow-mirror-schema', U + 'imported-evidence#/$defs/ImportWrapperV2', r['wrapper'])
    check(cid + '.import-id-prefix', r['importId'].startswith('import2:'))
    check(cid + '.wrapper-id-not-payload-digest', r['importId'][8:] != r['wrapper']['payloadDigest'])
    check(cid + '.identity-is-foundation-domain', r['importId'] == 'import2:' + canonical.identity('import', r['wrapper']))
    if 'owner' in case['expect']:
        check(cid + '.owner', r['payloadBinding']['owner'] == case['expect']['owner'])
    if case.get('compareTo'):
        o = built[case['compareTo']]
        check(cid + '.same-payload-digest', o['wrapper']['payloadDigest'] == r['wrapper']['payloadDigest'])
        check(cid + '.different-import-id', o['importId'] != r['importId'])
    rec = {'schemaFamily': 'opensip.product.imported-evidence', 'schemaMajor': 1, 'importId': r['importId'], 'wrapper': r['wrapper'], 'payloadBinding': r['payloadBinding'], 'correspondence': case['correspondence'], 'projectId': C['PRJ'], 'sourcePath': './coverage/v8.json', 'receiptId': 'receipt2:' + '1' * 64}
    must_valid(cid + '.record-schema', U + 'imported-evidence#/$defs/ImportedEvidenceRecordV1', rec)
for case in CASES['sourceMappingCases']:
    try:
        digest = M.admit_source_mapping(case['mapping'], case['inventory'], C['SNAP1'])
        check('source-mapping.' + case['id'], case['expect'].get('ok') is True and digest == M.doc_digest(case['mapping']))
    except M.Refusal as exc:
        check('source-mapping.' + case['id'], exc.detail == case['expect'].get('refusal'), exc.detail)
for case in CASES['stalenessCases']:
    r = M.classify_staleness(case['correspondence'], case['plan'], corrupt=case.get('corrupt', False))
    must_valid('staleness.row-schema.' + case['id'], U + 'imported-evidence#/$defs/StalenessRule', r)
    check('staleness.' + case['id'], [r['staleness'], r['usable']] == case['expect'], json.dumps(r))
cu = M.consumable_unhit_subjects(RT)
check('import.only-observable-unhit-consumable', cu['subjects'] == CASES['runtimePayloadExpect']['consumableUnhit'] and cu['universalNonUse'] is False)
check('import.window-disclosed-with-unhit', cu['window'] == RT['observationWindow'] and cu['population'] == RT['observedPopulation'])
must_invalid('import.unobservable-with-hits-rejected', U + 'imported-evidence#/$defs/RuntimeSubject', {'path': 'src/c.ts', 'observability': 'unobservable', 'hits': 0})
must_invalid('import.wrapper-kind-outside-enum', U + 'imported-evidence#/$defs/ImportWrapperV2', dict(built['runtime-wrapper-joins-foundation-import']['wrapper'], kind='coverage'))
plan_import_schema = FOUNDATION['$defs']['plan']['properties']['importIds']['items']
check('import.plan-import-ids-are-wrappers', canonical.ExactValidator(plan_import_schema).is_valid('import2:' + 'a' * 64)
      and not canonical.ExactValidator(plan_import_schema).is_valid('fact2:' + 'a' * 64)
      and not canonical.ExactValidator(plan_import_schema).is_valid('import2:' + 'a' * 64 + '\n'))

# ----------------------------------------------------------------------------- policy DSL
SUITE = CASES['policySuite']
must_valid('policy.suite-schema', U + 'policy-test#/$defs/PolicyTestSuiteV1', SUITE)
must_valid('policy.document-schema', U + 'policy-document#/$defs/PolicyDocumentV1', POL['basePolicy'])
res1, _ = M.run_policy_test(SUITE)
res2, _ = M.run_policy_test(copy.deepcopy(SUITE))
must_valid('policy.result-schema', U + 'policy-test#/$defs/PolicyTestResultV1', res1)
PE = CASES['policySuiteExpect']
check('policy.resolver-accepted', res1['resolverAccepted'] == PE['resolverAccepted'])
check('policy.expired-waiver-disclosed', res1['waiverResolution']['expired'] == PE['expired'])
for r in res1['results']:
    check('policy.case.' + r['id'], r['outcome'] == PE['outcomes'][r['id']], json.dumps(r))
check('policy.deterministic', res1['policyTestResultId'] == res2['policyTestResultId'])
check('policy.enforcement-unchanged', res1['enforcementUnchanged'] is True and res1['effectivePolicyDigest'] == res1['candidatePolicyDigest'])
for case in CASES['policyRefusals']:
    cid = 'policy.refusal.' + case['id']
    suite = copy.deepcopy(SUITE)
    if 'waivers' in case:
        suite['waivers']['waivers'] = case['waivers']
    if 'policyExtra' in case:
        suite['candidatePolicy'].update(case['policyExtra'])
    if 'policyEmitWhen' in case:
        suite['candidatePolicy']['rules'][0]['emitWhen'] = case['policyEmitWhen']
    if 'policyEvidenceUse' in case:
        suite['candidatePolicy']['rules'][1]['evidenceUse'] = case['policyEvidenceUse']
    if 'overrides' in case:
        suite['overrides'] = case['overrides']
    if case['expect'].get('schemaInvalid'):
        must_invalid(cid + '.schema-invalid', U + 'policy-test#/$defs/PolicyTestSuiteV1', suite)
        continue
    r, refusal = M.run_policy_test(suite)
    if 'refusal' in case['expect']:
        check(cid, refusal is not None and refusal.detail == case['expect']['refusal'] and r['resolverAccepted'] is False, getattr(refusal, 'detail', None))
        must_valid(cid + '.result-schema', U + 'policy-test#/$defs/PolicyTestResultV1', r)
    else:
        check(cid + '.effective-differs', r['effectivePolicyDigest'] != r['candidatePolicyDigest'])
        check(cid + '.candidate-unchanged', r['candidatePolicyDigest'] == res1['candidatePolicyDigest'] and r['overridesApplied'] == case['overrides'])
check('policy.glob-closed', M.glob_match('src/**/*.ts', 'src/a/b.ts') and not M.glob_match('src/*.ts', 'src/a/b.ts') and not M.glob_match('{a,b}', 'a'))
check('policy.kleene-and-false-dominates', M.eval_pred({'op': 'and', 'operands': [{'op': 'none', 'relation': 'imports', 'minResolution': 'resolved', 'filters': []}, {'op': 'exists', 'relation': 'imports', 'minResolution': 'resolved', 'filters': []}]}, 's', [{'relation': 'imports', 'subject': 's', 'target': 't', 'resolution': 'resolved'}], False, set(), set()) is False)
check('policy.kleene-or-unknown-propagates', M.eval_pred({'op': 'or', 'operands': [{'op': 'none', 'relation': 'imports', 'minResolution': 'resolved', 'filters': []}, {'op': 'exists', 'relation': 'x', 'minResolution': 'syntax', 'filters': []}]}, 's', [], False, set(), set()) is None)

# ----------------------------------------------------------------------------- repair
RS = CASES['repairScenario']
def tree_bytes(t):
    return {k: v.encode() for k, v in t.items()}
for case in RS['cases']:
    cid = 'repair.' + case['id']
    tree = tree_bytes(RS['tree'])
    run = dict(RS['run'])
    if case.get('runAvailability'):
        run['availability'] = case['runAvailability']
    trust = {C['PROD']: 'revoked' if case.get('revokeRecipe') else 'admitted'}
    if case.get('trustAbsent'):trust={}
    if case.get('runOverride'):run.update(case['runOverride'])
    for field in ['closedWorld','evidenceOrigin']:
        if field in case:run[field]=case[field]
    edits = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e) for e in RS['edits']] + ([case['extraEdit']] if case.get('extraEdit') else [])
    scope = list(RS['permittedScope'])
    if case.get('mutateTreeBeforePreview'):
        tree.update(tree_bytes(case['mutateTreeBeforePreview']))
    run['snapshotId'] = M.tree_snapshot_id(C['PRJ'], tree_bytes(RS['tree']))
    try:
        plan = M.repair_preview(C['PRJ'], tree, run, RS['recipe'], RS['targets'], edits, RS['evidenceRequirements'], scope, trust, ephemeral=case.get('ephemeral', False))
    except M.Refusal as r:
        check(cid, case['expect'].get('refusal') == r.detail, r.detail); continue
    exp = case['expect']
    if 'refusal' in exp and 'journal' not in exp and 'recoverAction' not in exp and not case.get('mutateTreeAfterApply') and not case.get('mutateTreeBeforeApply') and not case.get('authorization') and not case.get('ci') and not case.get('applyTrust') and 'authorizationLive' not in case:
        check(cid, False, 'no refusal at preview'); continue
    must_valid(cid + '.plan-schema', U + 'repair#/$defs/RepairPlanV1', plan)
    if 'applicable' in exp:
        check(cid + '.applicable', plan['descriptor']['applicable'] == exp['applicable'] and (exp['applicable'] or plan['descriptor']['unmetPreconditions'][0]['code'] == exp['unmet']))
        if 'editCount' in exp:
            check(cid + '.edits', len(plan['descriptor']['edits']) == exp['editCount'] and plan['descriptor']['edits'][0]['action'] == 'delete' and plan['descriptor']['edits'][0]['postimageDigest'] is None)
        if not exp['applicable'] or 'journal' not in exp:
            continue
    postimages = {e['path']: e['postimage'].encode() for e in RS['edits'] if e.get('postimage') is not None}
    auth = case.get('authorization') or {'repairPlanId': plan['repairPlanId'], 'snapshotId': plan['descriptor']['snapshotId'], 'projectId': C['PRJ']}
    if case.get('authorization'):
        auth = {'repairPlanId': case['authorization']['repairPlanId'], 'snapshotId': plan['descriptor']['snapshotId'], 'projectId': C['PRJ']}
    auth['live']=case.get('authorizationLive',True)
    auth['consentSource']=case.get('consent','policy'); auth['ci']=case.get('ci',False)
    # Synthetic admitted security projection; actual admission is exercised by integration.
    auth['securityAuthorizationRef'] = 'security.repair-apply-authorization.v1:' + 'a' * 64
    receipts = {};preimages={M.raw_sha(b):b for b in tree.values()}
    if case.get('corruptRetainedPreimage'):
        preimages[M.raw_sha(tree[case['corruptRetainedPreimage']])] = b'corrupted retained bytes'
    if case.get('journalState'):
        j0 = {'schemaFamily': 'opensip.product.repair-apply-journal', 'schemaMajor': 1, 'requestId': C['REQ'], 'stepId': 2, 'executionId': 'exec1_' + '0' * 32, 'repairPlanId': plan['repairPlanId'], 'baseSnapshotId': plan['descriptor']['snapshotId'], 'authorizationRef': auth['securityAuthorizationRef'], 'state': case['journalState'], 'stagedPaths': ['src/a.ts', 'src/b.ts'], 'appliedPaths': ['src/a.ts']}
        live = dict(tree); live.pop('src/a.ts')
        if case['journalState'] == 'APPLIED':
            live['src/b.ts'] = postimages['src/b.ts']; j0['appliedPaths'] = ['src/a.ts', 'src/b.ts']
        must_valid(cid + '.journal-schema', U + 'repair#/$defs/RepairApplyJournalV1', j0)
        if case.get('appliedIncludesB'):j0['appliedPaths']=['src/a.ts','src/b.ts'];live['src/b.ts']=postimages['src/b.ts']
        live.update(tree_bytes(case.get('userEditAfterApply',{})))
        if case.get('inspectOnly'):
            observed=M.repair_inspect(j0,plan,live);check(cid,observed['state']==exp['inspectState'] and observed['journalIntegrity']==exp['inspectIntegrity']);continue
        try:
            j1, action, outcome, term = M.repair_recover(j0, plan, live, C['PRJ'],None if case.get('noPreimageStore') else preimages,None if case.get('noRecoveryAuth') else synthetic_recovery_projection(j0, plan))
        except M.Refusal as r:
            check(cid,exp.get('recoverRefusal')==r.detail,r.detail);continue
        check(cid, action == exp['recoverAction'] and j1['state'] == exp['recoverState'], action + '/' + j1['state'])
        if 'recoverDetail' in exp: check(cid + '.recovery-detail', term.get('domainDetail',{}).get('code') == exp['recoverDetail'])
        if exp.get('recoveryTreeUnchanged'): check(cid + '.recovery-no-write', j1.get('_tree',live) == live)
        must_valid(cid + '.recovery-termination-schema', U + 'common#/$defs/StepTermination', term)
        must_valid(cid + '.journal-after-schema', U + 'repair#/$defs/RepairApplyJournalV1', {k:v for k,v in j1.items() if k!='_tree'})
        continue
    live = dict(tree)
    if case.get('mutateTreeBeforeApply'):
        live.update(tree_bytes(case.get('mutateTreeBeforeApply',{})))
    try:
        journal, receipt, after = M.repair_apply(plan, postimages, live, C['PRJ'], C['REQ'], 2, auth, case.get('ci', False), case.get('consent', 'policy'), receipts,case.get('applyTrust',trust),preimages, fault_after_renames=case.get('faultAfterRenames'), corrupt_path=case.get('corruptPath'))
    except M.Refusal as r:
        check(cid, exp.get('refusal') == r.detail, r.detail)
        if exp.get('treeUnchanged'):
            check(cid + '.tree-unchanged', live == dict(tree, **tree_bytes(case.get('mutateTreeBeforeApply',{}))))
        continue
    must_valid(cid + '.journal-schema', U + 'repair#/$defs/RepairApplyJournalV1', journal)
    must_valid(cid + '.receipt-schema', U + 'repair#/$defs/MutationReceiptV1', receipt)
    check(cid + '.receipt-identity', M.wid('receipt2', 'workflow.mutation-receipt', {k: v for k, v in receipt.items() if k != 'receiptId'}) == receipt['receiptId'])
    if case.get('replay'):
        j2, r2, after2 = M.repair_apply(plan, postimages, after, C['PRJ'], C['REQ2'], 2, auth, False, 'policy', receipts,trust,preimages)
        check(cid, j2['state'] == exp['journal'] and r2['effectOutcome'] == exp['effect'] and r2['replayed'] is True and r2['idempotencyKey'] == receipt['idempotencyKey'] and after2 == after)
        must_valid(cid + '.replay-receipt-schema', U + 'repair#/$defs/MutationReceiptV1', r2)
        continue
    if 'journal' in exp:
        check(cid + '.state', journal['state'] == exp['journal'] and receipt['effectOutcome'] == exp['effect'], journal['state'] + '/' + receipt['effectOutcome'])
    if 'rollback' in exp:
        check(cid + '.rollback', receipt['rollback'] == exp['rollback'])
    if exp.get('treeEqualsOriginal'):
        check(cid + '.tree-restored', after == tree)
    if exp.get('recoverRefuses'):
        j1, action, outcome, term = M.repair_recover(journal, plan, after, C['PRJ'],preimages,synthetic_recovery_projection(journal, plan))
        check(cid + '.recover', action == 'refuse' and term['class'] == exp['recoverClass'] and term['domainDetail']['code'] == exp['recoverDetail'])
        must_valid(cid + '.recover-termination-schema', U + 'common#/$defs/StepTermination', term)
    if 'treeHasA' in exp:
        check(cid + '.tree-postimages', ('src/a.ts' in after) == exp['treeHasA'] and after['src/b.ts'] == exp['bContent'].encode())
    if exp.get('verifyOk') or exp.get('verifyRunDiffersFromEvidenceRun') or case.get('mutateTreeAfterApply'):
        live2 = dict(after)
        if case.get('mutateTreeAfterApply'):
            live2.update(tree_bytes(case['mutateTreeAfterApply']))
        try:
            v,link = M.repair_verify(receipt, live2, C['PRJ'], 0, 0)
            must_valid(cid+'.verification-link',U+'repair#/$defs/VerificationLinkV1',link)
        except M.Refusal as r:
            check(cid + '.verify', exp.get('refusal') == r.detail, r.detail); continue
        must_valid(cid + '.verify-result-schema', U + 'invocation-record#/$defs/AnalysisResult', v)
        check(cid + '.verify', v['verification']['snapshotMatched'] and v['runId'] != RS['run']['runId'] and v['verification']['verifiedSnapshotId'] == receipt['appliedSnapshotId'])
check('repair.recovery-table-closed', set(M.RECOVERY_TABLE) == set(SCHEMAS[U + 'repair']['$defs']['JournalState']['enum']))
for st, (a, rs_, oc) in M.RECOVERY_TABLE.items():
    must_valid('repair.recovery-row-schema.' + st, U + 'repair#/$defs/RecoveryAction', {'state': st, 'action': a, 'resultState': rs_, 'receiptOutcome': oc})

# ----------------------------------------------------------------------------- test execution
TE = CASES['testExecution']
for case in TE['cases']:
    cid = 'test.' + case['id']
    params = dict(TE['params']); params.update(case.get('params', {}))
    ctx = copy.deepcopy(TE['ctx']); ctx.update(case.get('ctx', {}))
    exp = case['expect']
    if exp.get('schemaInvalid'):
        must_invalid(cid + '.schema-invalid', U + 'test-execution#/$defs/TestExecutionStepParams', params)
        if 'refusal' not in exp and 'admitted' not in exp:
            continue
    else:
        must_valid(cid + '.params-schema', U + 'test-execution#/$defs/TestExecutionStepParams', params)
    try:
        a = M.admit_test_execution(params, ctx)
    except M.Refusal as r:
        check(cid, exp.get('refusal') == r.detail, r.detail); continue
    if 'refusal' in exp:
        check(cid, False, 'no refusal'); continue
    check(cid, a['admitted'] and a['confinementClaimed'] is False and 'does not prevent network access' in a['disclosure'])
    if exp.get('importKind'):
        payload = M.test_payload(params, 1, b'ok\n', b'', tool_closure=None)
        must_valid(cid + '.payload-schema', U + 'test-execution#/$defs/TestPayloadV1', payload)
        w = M.build_import('test', payload, 'workflow.import-payload.test.v1', REGISTERED, {'kind': 'exact-snapshot', 'snapshotId': C['SNAP1']}, C['PROD'], C['ADAPT'], [{'path': 'stdout.txt', 'sha256': payload['stdoutDigest'], 'bytes': 3}], {'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]}, {'selection':{'mode':'full','completenessEstablished':True},'completeness':'complete','omissions':[]})
        must_valid(cid + '.wrapper-foundation', FOUNDATION['$id'] + '#/$defs/import', w['wrapper'])
        check(cid + '.wrapper-kind-test', w['wrapper']['kind'] == exp['importKind'] and w['payloadBinding']['payloadDomain'] == exp['payloadDomain'])
        result = {'kind': 'test-execution', 'importId': w['importId'], 'payloadDigest': w['wrapper']['payloadDigest'], 'testResult': 'failed', 'exitStatus': 1, 'timedOut': False, 'outputTruncated': False, 'disclosureEmitted': True}
        must_valid(cid + '.step-result-schema', U + 'test-execution#/$defs/TestExecutionStepResult', result)
check('test.result-is-never-coverage-or-verdict', not ({'coverageId', 'verdict'} & set(SCHEMAS[U + 'test-execution']['$defs']['TestExecutionStepResult']['properties'])))
check('test.no-shell-string-field', 'command' not in SCHEMAS[U + 'test-execution']['$defs']['TestExecutionStepParams']['properties'] and SCHEMAS[U + 'test-execution']['$defs']['TestExecutionStepParams']['properties']['argv']['type'] == 'array')

# ----------------------------------------------------------------------------- exact generic replay keys
mutation_scope = M.mutation_replay_scope(C['REQ'], 0, C['PRJ'], 'baseline-adopt')
mutation_key = M.mutation_replay_key(mutation_scope)
check('mutation-key.exact-H-preimage-distinguished-from-raw-C',
      mutation_key == canonical.identity('workflow.mutation-intent', mutation_scope) and
      mutation_key != M.raw_sha(canonical.canonical(mutation_scope)))
mutation_params = {'kind':'mutation','mutationClass':'baseline-adopt','idempotencyKey':mutation_key}
check('mutation-key.host-scope-admits-bound-params', M.admit_mutation_replay_key(mutation_params, mutation_scope) == mutation_key)
for field, value in [('requestId','req1_'+'f'*32),('stepId',1),('projectId','prj1-'+'f'*64),('operation','purge')]:
    altered = dict(mutation_scope, **{field:value})
    check('mutation-key.'+field+'-changes-key', M.mutation_replay_key(altered) != mutation_key)
    try:M.admit_mutation_replay_key(mutation_params, altered)
    except canonical.AdmissionError:check('mutation-key.'+field+'-cannot-reuse-key',True)
    else:check('mutation-key.'+field+'-cannot-reuse-key',False)
for name, altered in [('undefined-effect',dict(mutation_scope,effect={})),('repair-apply',dict(mutation_scope,operation='repair-apply')),
                      ('caller-extra-nonce',dict(mutation_scope,nonce=1)),('newline-request',dict(mutation_scope,requestId=C['REQ']+'\n'))]:
    must_invalid('mutation-key.closed-scope-refuses-'+name, U+'invocation-record#/$defs/MutationReplayScopeV1',altered)
must_invalid('mutation-key.repair-apply-not-generic-mutation', U+'invocation-record#/$defs/MutationParams', dict(mutation_params,mutationClass='repair-apply'))
# Repair apply's existing suite below/above retains its cross-request content-derived replay checks.

# ----------------------------------------------------------------------------- complete pinned-purge refusal
PURGE_PINS = [{'pinId':'repair:fix-42','kind':'repair-prerequisite'}, {'pinId':'baseline:main','kind':'baseline'}]
purge_envelope = M.pinned_purge_refusal(C['REQ'], C['RUN1'], PURGE_PINS)
check('purge.failure-is-closed-precondition-2', purge_envelope['kind'] == 'failure' and
      purge_envelope['termination']['errorCode'] == 'REQUEST.PRECONDITION_FAILED' and M.exit_code(purge_envelope['termination']) == 2)
must_valid('purge.complete-envelope-schema', U + 'command-envelope', purge_envelope)
purge_detail = purge_envelope['termination']['domainDetail']
check('purge.names-complete-pins-deterministically', purge_detail['purgeDisclosure']['activePins'] == list(reversed(PURGE_PINS)))
check('purge.disclosure-has-exact-consequences', purge_detail['purgeDisclosure']['consequences'] ==
      ['named-pins-revoked','dependent-evidence-replay-unavailable','sealed-history-retained'])
check('purge.projection-does-not-mutate-ledger-observation', PURGE_PINS[0]['pinId'] == 'repair:fix-42')
for name, change in [
    ('missing-disclosure', lambda d: d.pop('purgeDisclosure')),
    ('empty-pins', lambda d: d['purgeDisclosure'].update(activePins=[])),
    ('duplicate-pin', lambda d: d['purgeDisclosure']['activePins'].append(d['purgeDisclosure']['activePins'][0])),
    ('wrong-pin-order', lambda d: d['purgeDisclosure']['activePins'].reverse()),
    ('unknown-pin-kind', lambda d: d['purgeDisclosure']['activePins'][0].update(kind='guessed')),
    ('unknown-pin-field', lambda d: d['purgeDisclosure']['activePins'][0].update(authorized=True)),
    ('missing-consequence', lambda d: d['purgeDisclosure']['consequences'].pop()),
    ('misordered-consequences', lambda d: d['purgeDisclosure']['consequences'].reverse()),
    ('newline-run-id', lambda d: d['purgeDisclosure'].update(runId=C['RUN1']+'\n')),
    ('disclosure-on-other-code', lambda d: d.update(code='evidence.purged')),
]:
    bad = copy.deepcopy(purge_detail); change(bad)
    must_invalid('purge.detail-refuses-'+name, U + 'common#/$defs/DomainDetail', bad)
for name, change in [
    ('wrong-subject', lambda e: e['termination']['domainDetail'].update(subject='run2:'+'f'*64)),
    ('hidden-error-disclosure', lambda e: e['errors'][0]['purgeDisclosure']['activePins'].pop()),
    ('wrong-exit', lambda e: e.update(exitCode=0)),
    ('wrong-class', lambda e: e['termination'].update({'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io'})),
]:
    bad = copy.deepcopy(purge_envelope)
    # Break aliasing of the producer's repeated detail for an actual cross-field disagreement.
    bad['errors'] = copy.deepcopy(bad['errors']); change(bad)
    try: M.validate_pinned_purge_refusal(bad)
    except (M.Refusal, canonical.AdmissionError): check('purge.envelope-refuses-'+name, True)
    else: check('purge.envelope-refuses-'+name, False)
many_pins = [{'pinId':f'baseline:{i:04}', 'kind':'baseline'} for i in range(65)]
check('purge.more-than-64-pins-not-truncated', len(M.pinned_purge_refusal(C['REQ'], C['RUN1'], many_pins)['errors'][0]['purgeDisclosure']['activePins']) == 65)
purge_cmd = next(c for c in INV['commands'] if c['name']=='purge')
purge_parity = {'run-id':C['RUN1'], 'receipt-id':None, 'availability':'retained', 'termination-class':'request-rejected',
                'purge-disclosure':purge_detail['purgeDisclosure']}
purge_renderings = [M.render({'envelope':purge_envelope,'parity':purge_parity}, fmt, purge_cmd) for fmt in purge_cmd['formats']]
check('purge.complete-disclosure-all-advertised-renderers', M.parity_holds(purge_renderings) and
      all(r['parity']['purge-disclosure'] == purge_detail['purgeDisclosure'] for r in purge_renderings))
reduced = copy.deepcopy(purge_cmd); reduced['parityFields'].remove('purge-disclosure')
must_invalid('purge.inventory-cannot-drop-disclosure', U + 'command-inventory#/$defs/Command', reduced)

# ----------------------------------------------------------------------------- render parity
CMD = {c['name']: c for c in INV['commands']}
for case in CASES['renderCases']:
    cid = 'render.' + case['id']
    cmd = CMD[case['command']]
    parity = {k: ('x-' + k) for k in cmd['parityFields']}
    parity['findings'] = [{'fingerprint': C['FP1']}]
    env = {'parity': parity, 'envelope': {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 2}, 'hints': ['consider opensip inspect']}
    try:
        rs = [M.render(env, f, cmd) for f in case['formats']]
    except M.Refusal as r:
        check(cid, case['expect'].get('refusal') == r.detail, r.detail); continue
    check(cid + '.parity', M.parity_holds(rs) == case['expect']['parity'])
    for rendering in rs:
        if rendering['format'] == 'sarif':
            check(cid + '.sarif-results-equal-declared-findings', rendering['results'] == parity['findings'] and 'findings' in cmd['parityFields'])
            check(cid + '.sarif-verdict-and-deficiency-preserved', rendering['runProperties'] == {'verdict': parity['verdict'], 'deficiency': parity['deficiency']})
            check(cid + '.sarif-no-content-outside-common-projection', rendering['results'] == rendering['parity']['findings'] and all(rendering['runProperties'][k] == rendering['parity'][k] for k in ('verdict','deficiency')))
    if case['expect'].get('agentHasHints'):
        ag = next(r for r in rs if r['format'] == 'agent'); js = next(r for r in rs if r['format'] == 'json')
        check(cid + '.agent-is-json-plus-hints', ag['agentHints'] and ag['parity'] == js['parity'] and ag['envelope'] == js['envelope'])
# Removing a required analysis field must fail inventory admission even if every renderer
# would otherwise agree on the same incomplete field set.
for command in INV['commands']:
    if 'sarif' not in command['formats']:
        continue
    for field in ('run-id','verdict','required-coverage','deficiency','findings','termination-class','retention-disclosure'):
        reduced = copy.deepcopy(command); reduced['parityFields'].remove(field)
        must_invalid('render.' + command['name'] + '.missing-required-' + field, U + 'command-inventory#/$defs/Command', reduced)
check('render.every-advertised-sarif-command-exercised',
      {c['name'] for c in INV['commands'] if 'sarif' in c['formats']} ==
      {c['command'] for c in CASES['renderCases'] if 'sarif' in c['formats'] and 'refusal' not in c['expect']})
check('render.required-failure-after-commit-keeps-run', M.terminate({'event': 'operational-fault', 'faultCause': 'delivery-required', 'runId': C['RUN1']}).get('runId') == C['RUN1'])
check('render.every-renderer-required-failure-is-4', all(r['requiredFailureClass'] == 'operational-failed' for r in INV['renderers']))

# ----------------------------------------------------------------------------- review
FINDINGS = [{'fingerprint': C['FP1'], 'ruleId': 'no-unused-export', 'gating': True, 'subjectPath': 'src/a.ts'}]
ADVISORY = [{'kind': 'clone-candidate', 'subjectPath': 'src/dup.ts', 'evidenceLevel': 'advisory-only', 'sourceFingerprint': C['H0']}, {'kind': 'runtime-unhit', 'subjectPath': 'src/b.ts', 'evidenceLevel': 'partial-coverage', 'sourceFingerprint': C['H0']}]
for case in CASES['reviewCases']:
    cid = 'review.' + case['id']
    exp = case['expect']
    base_cands = M.candidates_from_run(C['RUN1'], FINDINGS, ADVISORY, {}, case['today'], C['PRJ'])
    for c in base_cands:
        must_valid(cid + '.candidate-schema.' + c['kind'], U + 'review#/$defs/Candidate', c)
    if 'advisoryControlBearing' in exp:
        check(cid, all(c['controlBearing'] == (c['kind'] == 'finding') for c in base_cands))
    if case.get('disposition'):
        target = next(c for c in base_cands if c['kind'] == 'clone-candidate')
        try:
            disp = M.review_join(target['candidateId'], case['disposition']['disposition'], {'kind': 'human', 'id': 'reviewer-1'}, 'dup of src/a.ts', case.get('reviewDate','2026-09-05'), case['disposition']['until'])
        except M.Refusal as r:
            check(cid, exp.get('refusal') == r.detail, r.detail); continue
        must_valid(cid + '.disposition-schema', U + 'review#/$defs/ReviewDisposition', disp)
        disp['receiptId'] = 'receipt2:' + '2' * 64
        cands = M.candidates_from_run(C['RUN1'], FINDINGS, ADVISORY, {target['candidateId']: disp}, case['today'], C['PRJ'])
        t2 = next(c for c in cands if c['candidateId'] == target['candidateId'])
        check(cid, t2['suppressed'] == exp['suppressed'] and t2.get('previouslyReviewed', False) == exp.get('previouslyReviewed', False))
        if case.get('newRun'):
            other=M.candidates_from_run(C['RUN0'],FINDINGS,ADVISORY,{target['candidateId']:disp},case['today'],C['PRJ'])
            check(cid+'.persists-across-run',next(c for c in other if c['kind']=='clone-candidate')['suppressed'] is True)
            changed=copy.deepcopy(ADVISORY);changed[0]['sourceFingerprint']='d'*64
            after=M.candidates_from_run(C['RUN0'],FINDINGS,changed,{target['candidateId']:disp},case['today'],C['PRJ'])
            check(cid+'.changed-evidence-resurfaces',next(c for c in after if c['kind']=='clone-candidate')['suppressed'] is False)
        must_valid(cid + '.candidate-after-schema', U + 'review#/$defs/Candidate', t2)
    if case.get('extraField'):
        d = {'candidateId': base_cands[0]['candidateId'], 'disposition': 'accept', 'reviewer': {'kind': 'model', 'id': 'llm', 'modelClosureId': C['PROD']}, 'note': '', 'suppressUntil': None, 'advisory': True}
        d.update(case['extraField'])
        must_invalid(cid, U + 'review#/$defs/ReviewDisposition', d)
    if case.get('briefCount'):
        ids = ['candidate2:' + format(i, '064x') for i in range(case['briefCount'])]
        b = M.review_brief(C['RUN1'], ids, {'kind': 'model', 'id': 'llm', 'modelClosureId': C['PROD']})
        must_valid(cid + '.brief-schema', U + 'review#/$defs/ReviewBrief', b)
        check(cid, b['truncated'] == exp['truncated'] and len(b['candidates']) == exp['briefSize'] and b['advisory'] is True)
check('review.schemas-have-no-control-fields', all(k not in SCHEMAS[U + 'review']['$defs']['ReviewDisposition']['properties'] for k in ('verdict', 'runId', 'baselineId', 'authorizationRef', 'repairPlanId')))
check('query.advisory-ops-subset', set(SCHEMAS[U + 'graph-query']['$defs']['AdvisoryOperation']['enum']) <= set(SCHEMAS[U + 'graph-query']['$defs']['Operation']['enum']))

# ----------------------------------------------------------------------------- doctor
rep, term = M.doctor(True, [{'code': 'DELIVERY.CLOSURE_BYTES_CORRUPT', 'remedy': 'reinstall'}, {'code': 'COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED', 'remedy': 'install'}])
must_valid('doctor.result-schema', U + 'invocation-record#/$defs/DoctorResult', rep)
check('doctor.defects-report-exit-0', M.exit_code(term) == 0 and rep['defectsFound'] == 2 and term['domainDetail']['code'] == 'DOCTOR.DEFECTS_FOUND')
rep2, term2 = M.doctor(False, [])
check('doctor.unproducible-exit-4', M.exit_code(term2) == 4 and rep2['reportProduced'] is False)

# ----------------------------------------------------------------------------- obligation map integrity
import fnmatch  # noqa: E402
OMAP = canonical.parse((HERE / 'obligation-map.v1.json').read_bytes())
ids = [c['id'] for c in CHECKS]
for fb in OMAP['feedback']:
    for pat in fb['cases']:
        check(f'obligation-map.point-{fb["point"]}.cases-exist.{pat}', any(fnmatch.fnmatchcase(i, pat) or i == pat for i in ids), 'no check matches')
    for s in fb['schemas']:
        check(f'obligation-map.point-{fb["point"]}.schema-exists.{s}', (HERE / 'schemas' / s).is_file())
check('obligation-map.all-nine-feedback-points', sorted(fb['point'] for fb in OMAP['feedback']) == list(range(1, 10)))
check('obligation-map.ar-obligations', sorted(o['id'] for o in OMAP['obligations']) == ['AR-08', 'AR-10', 'AR-11', 'AR-13', 'AR-16'])

# ----------------------------------------------------------------------------- report
a = argparse.ArgumentParser(); a.add_argument('--report', required=True); args = a.parse_args()
failed = [c for c in CHECKS if not c['ok']]
report = {
    'unit': 'workflows-and-surfaces', 'standing': 'PROPOSED reference evidence; NOT SELF-ACCEPTED; not product qualification',
    'python': sys.version.split()[0], 'schemaCount': len(SCHEMAS), 'checkCount': len(CHECKS), 'passed': len(CHECKS) - len(failed), 'failed': failed,
    'boundaries': [
        'All inputs are synthetic trusted model inputs; presence sets for pivots E0..E4 are supplied by the case, not computed by running detectors.',
        'No provider, repository code, renderer, ledger or filesystem is executed; journals and trees are in-memory.',
        'Expected values and mixed-author corrections require fresh independent Claude review; passing this checker is not acceptance.',
        'Security-unit grant admission is stubbed by an already-admitted grant record; the security model is not re-executed here.'
    ],
    'productQualification': False,
    'sourceSha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py')) + sorted(HERE.glob('*.json')) + sorted((HERE / 'schemas').glob('*.json')) if 'report' not in p.name and p.name != 'initial-author-response.json'}
}
Path(args.report).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'checks': len(CHECKS), 'passed': report['passed'], 'failed': len(failed)}))
for f in failed[:40]:
    print('FAIL', f['id'], f['detail'])
sys.exit(1 if failed else 0)
