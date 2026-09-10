"""Independent reviewer probes over a scratch COPY of candidate-subject.v1.
Run with /tmp/opensip-architecture-review-env/bin/python -I -B.
Every probe records what the frozen reference bytes actually do; expectations are
the reviewer's reading of the five product contracts. Nothing here edits the subject.
"""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
SCRATCH = OUT.parent / 'scratch' / 'docs' / 'coop' / 'design-corrections'
ARTIFACTS = OUT.parent / 'scratch' / 'docs' / 'coop' / 'artifacts'
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v1.json')

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, SCRATCH / rel)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

C = load('p_canonical', 'foundation/canonical.py')
IM = load('p_identity', 'foundation/identity-model.py')
S = load('p_security', 'security/security_lifecycle_model_v1.py')
N = load('p_native', 'native/native_evidence_model.v2.py')
W = load('p_workflows', 'workflows/workflows_model.v1.py')
F = load('p_fixture', 'integration-fixtures.py')
HM = load('p_hostmodel', 'integration-host-model.py')
SC = load('p_seccheck', 'security/check-security-lifecycle.v1.py')

from jsonschema import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

RESULTS = []
def record(pid, title, observed, expected_by_contract, verdict):
    RESULTS.append({'id': pid, 'title': title, 'observed': observed, 'expectedByContract': expected_by_contract, 'verdict': verdict})

SCHEMAS = {}
for p in sorted((SCRATCH / 'workflows' / 'schemas').glob('*.schema.json')):
    s = C.parse(p.read_bytes()); SCHEMAS[s['$id']] = s
FOUND = C.parse((SCRATCH / 'foundation' / 'identity-schemas.v2.json').read_bytes())
REG = Registry().with_resources([(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()] + [(FOUND['$id'], Resource(contents=FOUND, specification=DRAFT202012))])
U = 'urn:opensip:product-v1:workflows:'
def wf_valid(ref, value):
    try:
        C.typed(value); C.ExactValidator({'$ref': ref}, registry=REG).validate(value); return True
    except (ValidationError, C.AdmissionError):
        return False

# P1: closed DomainDetailCode enum cannot carry details defined by the other units
foreign = ['native.execution-not-authorized', 'native.stale-prepared-output', 'native.explicit-root-without-marker',
           'storage.backup-choice-required', 'GRANT.REFUSED', 'AUTHZ.SOURCE_MOVED', 'RECOVERY.REFUSED',
           'CLOCK-EXCURSION-FORWARD', 'ROOT.SCHEMA_UNSUPPORTED', 'evidence.purged', 'evidence.expired', 'MIGRATION.CORRUPT',
           'STORAGE.BACKUP_CHOICE_REQUIRED']
obs = {code: wf_valid(U + 'common#/$defs/StepTermination', {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED', 'domainDetail': {'code': code, 'remedy': 'x'}}) for code in foreign}
record('P1', 'CommandEnvelope/StepTermination closed DomainDetailCode enum vs details minted by the identity/security/native contracts', obs,
       'workflows §9: typed detail travels beside an existing code; native §10 and security S12 say their details are request-rejection detail; identity §5 names evidence.{expired,purged,missing,corrupt}',
       'COUNTEREXAMPLE: no other unit\'s detail is admissible in the public envelope; the storage detail is spelled two ways (security/identity lowercase vs workflows uppercase)')

# P2: platform identifier vocabulary split inside the security unit
sec_schema = C.parse((SCRATCH / 'security' / 'security-lifecycle.schemas.v1.json').read_bytes())
pps_keys = sorted(sec_schema['schemas']['PlatformProfileSetV1']['properties']['platforms']['properties'].keys())
grant_plat = sorted(sec_schema['schemas']['RepoExecutionGrantV2']['properties']['platformId']['enum'])
def resolve_case(doc, idx):
    subs = SC.build_subs(doc); case = list(SC.iter_cases(doc))[idx]
    return SC.resolve_input(case['input'], subs), case
pcases = C.parse((SCRATCH / 'security' / 'platform-admission-cases.v1.json').read_bytes())
inp, case0 = resolve_case(pcases, 0)
adm_native = S.platform_admit(inp['profileSet'], dict(inp['observed'], platform='macos-aarch64'))
adm_sec = S.platform_admit(inp['profileSet'], inp['observed'])
record('P2', 'Platform vocabulary: PlatformProfileSetV1/platform_admit vs RepoExecutionGrantV2.platformId, native matrix and qualification gates',
       {'profileSetPlatformKeys': pps_keys, 'grantPlatformIdEnum': grant_plat, 'SUPPORTED_POPULATION': sorted(S.SUPPORTED_POPULATION), 'PLATFORM_TRUTH_TABLE': sorted(S.PLATFORM_TRUTH_TABLE),
        'platform_admit(macos-aarch64)': adm_native['result'] + ':' + (adm_native['refusals'] or ['-'])[0], 'platform_admit(' + inp['observed']['platform'] + ')': adm_sec['result'], 'case': case0['id']},
       'security S8/S10, native §1.1 and qualification-gates name one four-platform family set; integration-issues item 3 claims the four machine IDs are shared',
       'COUNTEREXAMPLE: admitted platform identities (macos-arm64/linux-arm64/linux-x86_64) and grant/native/matrix identities (macos-aarch64/linux-aarch64-gnu/linux-x86_64-gnu) coincide only for macos-x86_64; no mapping is specified')

# P3: zero-config automatic unit discovery over an installed node_modules tree
disc_doc = C.parse((SCRATCH / 'security' / 'discovery-cases.v1.json').read_bytes())
dinp, dcase = resolve_case(disc_doc, 0)
base_run = S.discovery(copy.deepcopy(dinp))
root = base_run['provenance']['selectedRoot']
base_dir = copy.deepcopy(dinp['fs'][root]); base_dir.pop('vcs', None)
base_file = next((e for e in dinp['fs'].values() if e.get('kind') == 'file'), None) or {'kind': 'file', 'uid': dinp['invokingUid'], 'gid': 0, 'mode': '0644', 'nlink': 1, 'size': 10}
small = copy.deepcopy(dinp); small.pop('explicitJoins', None); small.pop('configWorkspaceRoots', None)
small['fs'][root + '/package.json'] = copy.deepcopy(base_file)
small['fs'][root + '/node_modules'] = copy.deepcopy(base_dir)
for name in ('left-pad', 'lodash'):
    small['fs'][root + '/node_modules/' + name] = copy.deepcopy(base_dir)
    small['fs'][root + '/node_modules/' + name + '/package.json'] = copy.deepcopy(base_file)
out_small = S.discovery(small)
big = copy.deepcopy(small)
for i in range(4200):
    big['fs'][root + '/node_modules/pkg%04d' % i] = copy.deepcopy(base_dir)
    big['fs'][root + '/node_modules/pkg%04d/package.json' % i] = copy.deepcopy(base_file)
try:
    out_big = S.discovery(big)
except Exception as e:
    out_big = {'status': 'MODEL-EXCEPTION', 'refusal': repr(e), 'detail': 'the WORKSPACE_UNIT_LIMIT refusal path itself fails: REQUEST.UNSATISFIABLE is not in the security D9 table; no fixture exercises the cap'}
record('P3', 'Security S3 automatic marker scan treats every node_modules/*/package.json as a workspace unit; the 4096 cap refuses an ordinary installed JS repository',
       {'baseCase': dcase['id'], 'selectedRoot': root, 'baseStatus': base_run['status'], 'smallStatus': out_small['status'], 'smallUnits': [u['path'] for u in out_small.get('provenance', {}).get('units', [])],
        'bigStatus': out_big['status'], 'bigRefusal': out_big.get('refusal'), 'bigDetail': out_big.get('detail')},
       'security S3: automatic units are any marker-bearing directory under the admitted root, capped at 4096 (REQUEST.UNSATISFIABLE); native U-4 treats node_modules as a host-ignore convention for file membership only; no contract says unit discovery skips node_modules/target/.git',
       'COUNTEREXAMPLE: the zero-config default on a repository with installed dependencies enumerates dependency packages as units and refuses above 4096')

# P4: native host-ignore substring match; node_modules markers become units
units = N.discover_units({'package.json': {'sha256': 'a' * 64}})['units']
rows = N.assign_membership(units, ['packages/target/index.ts', 'src/target/x.ts', 'index.ts'])['rows']
nm_units = N.discover_units({'package.json': {'sha256': 'a' * 64}, 'node_modules/left-pad/package.json': {'sha256': 'b' * 64}})['units']
record('P4', 'Native U-4 host-ignore convention is matched as a path substring; native discover_units creates units for node_modules markers',
       {'membership': {r['path']: [r['membership'], r['reason']] for r in rows}, 'unitsFromNodeModulesMarkers': [u['rootPath'] for u in nm_units]},
       'native §1.4 U-4: host-ignore-convention (node_modules/, .git/, target/); U-1: a directory holding package.json yields a tsjs unit',
       'COUNTEREXAMPLE: packages/target/index.ts (not a Cargo target dir) is erased from the program as host-ignore; a node_modules package.json becomes a program unit')

# P5: native discover_units refuses the foundation/security root sentinel "."
r = N.discover_units({'package.json': {'sha256': 'a' * 64}, 'web/tsconfig.json': {'sha256': 'b' * 64}}, explicit_workspace_roots=['.'])
dot_result = r['refused'] if r['refused'] else {'units': [u['rootPath'] for u in r['units']]}
r2 = N.discover_units({'package.json': {'sha256': 'a' * 64}, 'web/tsconfig.json': {'sha256': 'b' * 64}}, explicit_workspace_roots=['web'])
sec_dot = S.discovery(dict(copy.deepcopy(dinp), explicitJoins=['.']))['status']
record('P5', 'Config2 discovery.workspaceRoots ["."]: security accepts "." as the admitted root; native refuses it as a root without a marker',
       {'nativeExplicitDot': dot_result, 'nativeExplicitWeb': [u['rootPath'] for u in r2['units']], 'securityExplicitJoinDot': sec_dot},
       'identity §3: "." alone denotes the admitted project root; security S12: a workspace root "." names the already admitted project root; native §1.4 consumes Config2 workspaceRoots as exact roots',
       'COUNTEREXAMPLE: the same Config2 value is CONFIG.INVALID (native.explicit-root-without-marker) in the native reference and ACCEPT in the security reference')

# P6: UNKNOWN backup status
sec_unknown = S.storage_write_admission('UNKNOWN', False, None, True, False)
id_unknown = IM.storage_admission('unknown')
record('P6', 'UNKNOWN backup-managed storage: S3.1 prose vs both reference models',
       {'security_storage_write_admission(UNKNOWN,ci)': sec_unknown['result'] + ':' + str(sec_unknown['choice']), 'identity_storage_admission(unknown)': id_unknown},
       'security S3.1 prose: "backup-managed or UNKNOWN ... needs an explicit choice"; identity §5, the security S13 addendum, both models and the inventory flag join: UNKNOWN admits with disclosure',
       'PROSE DEFECT: S3.1 contradicts its own model, its fixture (unknown-backup-status-is-not-not-backed-up) and the identity contract')

# P7: native sufficiency_v2 step-9 shortcut bypasses the confidence floor that v1 enforced
req = {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'minConfidenceMillionths': 900000, 'completeness': 'partial-ok', 'quantifier': 'existential', 'unresolvedEdgePolicy': 'forbid', 'externalConsumerPolicy': 'forbid'}
view = {'clones': {'relation': 'clones', 'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': 100000, 'resolutionCompleteness': {'state': 'not-applicable', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}}}
record('P7', 'Native sufficiency v2 evaluates the one-rung/existential/partial-ok shortcut (step 9) before the confidence-floor check (step 3)',
       {'v2': N.sufficiency_v2(req, view), 'v1': N.sufficiency_v1({'relation': 'clones', 'minResolution': 'normalized-body-hash', 'minConfidenceMillionths': 900000, 'completeness': 'partial-ok'}, view)},
       'native §4.6: nine steps "evaluated in this order"; step 3 (confidence-floor-unmet) precedes step 9',
       'COUNTEREXAMPLE: v2 returns satisfied with confidence 100000 below floor 900000 where the retained v1 oracle refuses; prose order and model order disagree')

# P8: identity close_run admits a finding whose evidence names an import outside the Plan
run, objects, blobs = F.build(resolved=True, has_match=True)
def put(value):
    raw = value if type(value) is bytes else C.canonical(value); d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d
empty = put({})
closure = next(k for k, (d, v) in objects.items() if d == 'closure')
imp = {'schemaVersion': 2, 'kind': 'runtime', 'payloadSchemaDigest': empty, 'payloadDigest': empty, 'sourceCorrespondenceDigest': empty, 'buildDigest': empty,
       'producerClosure': closure, 'adapterClosure': closure, 'blobs': [], 'scopeDigest': empty, 'observationDigest': empty, 'completeness': 'complete', 'omissions': []}
imp_id = IM.identifier('import', imp); objects[imp_id] = ('import', imp)
fp = {'schemaVersion': 2, 'ruleStableId': 'no-consumer', 'detectorSemanticsMajor': 2, 'subjectKey': {'language': 'typescript', 'kind': 'symbol', 'logicalPath': 'a.ts', 'qualifiedName': 'foo', 'discriminator': 'one'}, 'relatedSubjectKeys': []}
fk = IM.identifier('finding-fingerprint', fp); objects[fk] = ('finding-fingerprint', fp)
finding = {'schemaVersion': 2, 'fingerprint': fk, 'ruleClosure': closure, 'subjectId': 'foo', 'messageCode': 'unused', 'parameterDigest': put({}), 'severity': 'error',
           'evidenceRefs': [{'domain': 'import', 'digest': imp_id.split(':')[1]}]}
fid = IM.identifier('finding', finding); objects[fid] = ('finding', finding)
pk = objects[run['evaluationSealId']][1]['proofBundleId']; proof = copy.deepcopy(objects[pk][1]); proof['findingIds'] = [fid]; F.rekey(objects, pk, proof, run)
ek = run['evidenceId']; ev = copy.deepcopy(objects[ek][1]); ev['findingIds'] = [fid]; F.rekey(objects, ek, ev, run)
plan_imports = objects[run['planId']][1]['importIds']
try:
    closed = IM.close_run(run, objects, blobs); p8 = 'ACCEPTED ' + closed[:24]
except Exception as e:
    p8 = 'REFUSED ' + repr(e)
record('P8', 'Identity closure: finding.evidenceRefs may name an import2 that is neither in plan.importIds nor in proof.evaluationInputRefs',
       {'planImportIds': plan_imports, 'evidenceImportIds': objects[run['evidenceId']][1]['importIds'], 'close_run': p8},
       'identity §4: all consumed data are listed in evaluationInputRefs, no hidden lookup; §3: rejects extra authoritative roots and unresolved references',
       'COUNTEREXAMPLE: an import outside the Plan is accepted as finding evidence by close_run (only predicate inputRefs are constrained)')

# P9: workflows evaluate(): non-gating rule with absent required evidence vs incomplete coverage
policy = {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 1, 'gateSeverityAtLeast': 'error', 'rules': [
    {'ruleId': 'advisory-runtime', 'ruleProgramRef': {'contributionId': 'x', 'ruleStableId': 'advisory-runtime', 'semanticsMajor': 1, 'programDigest': 'a' * 64}, 'enabled': True, 'severity': 'note', 'gate': False,
     'subjectEnumeration': {'universe': 'ts', 'subjectKind': 'file', 'include': ['**']}, 'emitWhen': {'op': 'exists', 'relation': 'runtime-observation', 'minResolution': 'syntax', 'filters': [], 'evidence': 'runtime'},
     'evidenceUse': [{'kind': 'runtime', 'requirement': 'required'}]}]}
scope = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['**'], 'exclude': []}
waivers = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}
res_abs = W.evaluate(policy, scope, waivers, {'subjects': ['src/a.ts'], 'facts': [], 'coverage': 'complete', 'evidenceAvailable': []})
res_cov = W.evaluate(policy, scope, waivers, {'subjects': ['src/a.ts'], 'facts': [], 'coverage': 'unknown', 'evidenceAvailable': ['runtime']})
record('P9', 'Workflow evaluate(): a NON-gating rule whose required evidence is absent flips the verdict to indeterminate, while the same non-gating rule under incomplete coverage does not',
       {'requiredEvidenceAbsent': res_abs['verdict'], 'coverageUnknownWithEvidence': res_cov['verdict']},
       'workflows §5: "an indeterminate gating rule is a typed deficiency"; identity §4: fail dominates indeterminate dominates pass',
       'INCONSISTENCY: two indeterminacy sources are treated differently for non-gating rules; the contract does not say which is intended')

# P10: comparison evidence axis with a re-collected runtime import on a gating rule
rule = {'ruleId': 'r', 'enabled': True, 'gating': True, 'requiredCoverage': 'satisfied', 'evidenceUse': [{'kind': 'runtime', 'requirement': 'required'}]}
pres = {'B': True, 'E0': True, 'E1': True, 'E2': True, 'E3': True, 'E4': True, 'waivedB': False, 'waivedC': False}
ev_b = {'importKinds': ['runtime'], 'relations': [], 'imports': [{'kind': 'runtime', 'importId': 'import2:' + 'a' * 64}]}
ev_c = {'importKinds': ['runtime'], 'relations': [], 'imports': [{'kind': 'runtime', 'importId': 'import2:' + 'b' * 64}]}
entry, sig = W.classify('finding-key2:' + '1' * 64, 'r', pres, rule, rule, ev_b, ev_c, {'detectorId': 'd', 'method': 'identical-closure'}, W.AUDIT_PROFILES['code-regression'])
record('P10', 'Comparison: any change of a gating rule\'s bound import identity (a freshly collected runtime artifact) makes every entry of that rule INDETERMINATE',
       {'classification': entry['classification'], 'reason': entry.get('indeterminateReason'), 'verdictSignal': sig},
       'workflows §3 evidence axis as written: evidence-content-changed on a gating rule is INDETERMINATE',
       'DESIGN CONSEQUENCE (contract-consistent): a gating rule with declared runtime/test evidence never yields a determinate changed-code verdict unless the identical import2 is bound on both sides')

# P11: test-runner grant requires a Plan semantic-grant projection; the workflow test step has no Plan
sf = C.parse((SCRATCH / 'security' / 'execution-principal-cases.v1.json').read_bytes())
grant, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId='macos-aarch64', runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
argv = ['bin/opensip-test-runner', '--ci']; grant['argvDigest'] = W.payload_digest(argv); grant['effects'] = dict(S.PLATFORM_TRUTH_TABLE['macos-aarch64'])
digest = HM.owner_digest(grant['owners']); grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest
ctx.update(projectId=grant['projectId'], snapshotId=grant['snapshotId'], argvDigest=grant['argvDigest'])
ctx_no_plan = copy.deepcopy(ctx); ctx_no_plan['semanticGrantPrincipals'] = []
without = S.admit_repo_execution_grant(grant, ctx_no_plan)
ctx['semanticGrantPrincipals'] = [{'kind': 'trusted-repository-code', 'closureId': grant['toolClosureId'], 'ownerSourceDigest': digest}]
with_ = S.admit_repo_execution_grant(grant, ctx)
record('P11', 'Test-runner grant admission requires a Plan semantic-grant projection; a test-execution step is an operational step with no Plan',
       {'withoutProjection': without['result'] + ':' + ','.join(without['refusals']), 'withProjection': with_['result'], 'ownerSourceDigestOfEmptyOwnerSet': digest,
        'integrationChecker': 'check-integration.py bind() derives ctx.semanticGrantPrincipals from the grant itself'},
       'security S10: GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED otherwise; workflows §1/§7: test-execution mints no Run and has no Plan; identity §3: projection lists operations needed by the analysis',
       'GAP: no contract states which Plan projects the test-code principal for a test-runner grant; the integration evidence fabricates the projection from the grant')

# P12: every D9 code used by the workflow enum exists in d9-exit-contract.v1.14
d9raw = (ARTIFACTS / 'd9-exit-contract.v1.14.json').read_bytes().decode()
codes = SCHEMAS[U + 'common']['$defs']['D9ErrorCode']['enum'] + SCHEMAS[U + 'common']['$defs']['D9ReasonCode']['enum']
missing = [c for c in codes if ('"' + c + '"') not in d9raw]
record('P12', 'Workflow D9ErrorCode/D9ReasonCode enum members present in the pinned d9-exit-contract.v1.14', {'missingFromD9': missing, 'checked': len(codes)},
       'workflows §0/§9: class/code/exit table retained; no new D9 family', 'OK' if not missing else 'COUNTEREXAMPLE')

# P13: product quality report schema: exactly 7 measured runs?
pq = C.parse((SCRATCH / 'foundation' / 'product-quality-report.schema.v3.json').read_bytes())
def find_key(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r_ = find_key(v, key)
            if r_ is not None: return r_
    if isinstance(o, list):
        for v in o:
            r_ = find_key(v, key)
            if r_ is not None: return r_
    return None
el = find_key(pq, 'elapsedNanos'); wr = find_key(pq, 'warmupRuns')
record('P13', 'Product quality report: elapsedNanos cardinality vs validator median index sorted()[3]', {'elapsedNanos': {k: el.get(k) for k in ('minItems', 'maxItems')} if isinstance(el, dict) else el, 'warmupRuns': wr},
       'admission §3: 3 warmups then 7 measured runs', 'OK' if isinstance(el, dict) and el.get('minItems') == 7 and el.get('maxItems') == 7 else 'CHECK')

# P14: lease scope of core lifecycle commands
inv = C.parse((SCRATCH / 'workflows' / 'command-inventory.v1.json').read_bytes())
core = {c['name']: c['authorizationClass'] for c in inv['commands'] if c['name'].startswith(('core-', 'update', 'install', 'store-', 'trust-'))}
record('P14', 'Lease scope of core update/repair/rollback: S7 lists update as fence-only, S13 says the three core operations use EXCLUSIVE (a per-namespace project lease)', core,
       'security S7: EXCLUSIVE is a per-namespace project lease; trust/core state is written under the install fence', 'GAP: which namespace(s) must be EXCLUSIVE for an install-level core transition is unspecified')

# P15: frozen subject unchanged after all probes
manifest = json.load(open(MANIFEST))
bad = [f['path'] for f in manifest['files'] if hashlib.sha256((Path(manifest['snapshotRoot']) / f['path']).read_bytes()).hexdigest() != f['sha256']]
record('P15', 'Frozen subject unchanged after probes', {'changed': bad, 'verified': len(manifest['files']) - len(bad)}, 'read-only subject', 'OK' if not bad else 'SUBJECT MUTATED')

out = {'standing': 'independent reviewer probes over a scratch copy; not part of the subject', 'manifestSha256': hashlib.sha256(MANIFEST.read_bytes()).hexdigest(), 'python': sys.version.split()[0], 'results': RESULTS}
(OUT / 'independent-probes.json').write_text(json.dumps(out, indent=2, default=str) + '\n')
for r_ in RESULTS:
    print(r_['id'], r_['verdict'][:100]); print('   ', json.dumps(r_['observed'], default=str)[:420])
