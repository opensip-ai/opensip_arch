"""Cross-unit reference checks; synthetic TCB inputs, not independent acceptance."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from jsonschema import ValidationError

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('integration_host', HERE / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
checks = []

def check(name, condition):
    checks.append({'id': name, 'passed': bool(condition)})

def refuses(name, fn):
    try:
        fn()
    except (ValueError, ValidationError, M.C.AdmissionError, M.W.Refusal, M.N.C.AdmissionError, M.N.IM.C.AdmissionError):
        check(name, True)
    else:
        check(name, False)

nf = M.C.parse((HERE / 'native/native-cases.v2.json').read_bytes())['fixtures']
sf = M.C.parse((HERE / 'security/execution-principal-cases.v1.json').read_bytes())
wf = M.C.parse((HERE / 'workflows/workflow-cases.v1.json').read_bytes())

def bind(grant, ctx):
    digest = M.owner_digest(grant['owners'])
    grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest
    ctx.pop('semanticGrantPrincipals', None)  # operational admission has no Plan
    ctx.update(projectId=grant['projectId'], snapshotId=grant['snapshotId'], argvDigest=grant['argvDigest'])
    return grant, ctx

for platform in M.S.PLATFORM_TRUTH_TABLE:
    grant, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
    grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId=platform,
                 runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
    argv = ['bin/opensip-test-runner', '--ci']
    grant['argvDigest'] = M.W.payload_digest(argv)
    grant['effects'] = dict(M.S.PLATFORM_TRUTH_TABLE[platform])
    bind(grant, ctx)
    projection = M.test_grant_projection(grant, ctx)
    params = {'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': platform,
              'authorizationRef': projection['securityGrantRef'],
              'argv': argv, 'argv0Source': {'kind': 'toolchain-closure', 'closureId': grant['toolClosureId'], 'member': argv[0]},
              'kind': 'test-execution', 'cwdIsRoot': True, 'consentSource': 'interactive-consent', 'afterStep': 0, 'timeoutMilliseconds': 600000, 'maxOutputBytes': 1048576, 'environmentAllowlist': [], 'effects': grant['effects']}
    wc = {'ci': False, 'projectId': grant['projectId'], 'snapshotId': grant['snapshotId'], 'grant': projection,
          'snapshotMembers': ctx['snapshotMembers'], 'toolchainMembers': {grant['toolClosureId']: ctx['toolClosure']['members']},
          'truthTable': M.S.PLATFORM_TRUTH_TABLE, 'liveEqualsAfterStep': True}
    check('security-to-test.' + platform, M.W.admit_test_execution(params, wc)['admitted'])
    refuses('test-consent-cannot-be-relabeled.' + platform, lambda: M.W.admit_test_execution(dict(params, consentSource='pre-existing-policy'), wc))
    refuses('test-legacy-interactive-spelling-refused.' + platform, lambda: M.W.admit_test_execution(dict(params, consentSource='interactive'), wc))
    ci_interactive=copy.deepcopy(grant);ci_interactive['authorization']['ci']=True
    refuses('security-interactive-test-grant-in-ci-refused.'+platform,lambda:M.test_grant_projection(ci_interactive,dict(ctx,ci=True)))
    for ci in (False, True):
        policy_grant = copy.deepcopy(grant); policy_grant['authorization'] = {'mode':'policy-record','policyRecordId':'a'*64,'ci':ci}
        policy_ctx = dict(ctx,ci=ci); policy_projection = M.test_grant_projection(policy_grant,policy_ctx)
        policy_params = dict(params,consentSource='pre-existing-policy',authorizationRef=policy_projection['securityGrantRef'])
        policy_wc = dict(wc,ci=ci,grant=policy_projection)
        check('security-policy-record-to-test.'+platform+'.ci='+str(ci),M.W.admit_test_execution(policy_params,policy_wc)['admitted'])
        refuses('policy-record-cannot-be-relabeled-interactive.'+platform+'.ci='+str(ci),lambda: M.W.admit_test_execution(dict(policy_params,consentSource='interactive-consent'),policy_wc))
    altered = copy.deepcopy(grant); altered['argvDigest'] = '0' * 64
    refuses('changed-argv-refused.' + platform, lambda: M.test_grant_projection(altered, ctx))

auth = copy.deepcopy(nf['auth']); grants, contexts = [], []
for owner in auth['owners']:
    g, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
    g.update(projectId=auth['projectId'], snapshotId=auth['snapshotId'], owners=M.owner_rows([owner]), executionClass=owner['kind'],
             dependencySourceSetId=auth['dependencySourceSetId'].removeprefix('sha256:'),
             toolClosureId=auth['toolClosure']['closureId'], authorization=auth['authorization'],
             effects={k: v['enforcement'] for k, v in auth['effects'].items()})
    ctx['dependencyClosure'] = {'dependencySourceSetId': g['dependencySourceSetId'], 'owners': {owner['ownerKey']: owner['ownerFileManifestSha256']}}
    ctx['toolClosure']['closureId'] = g['toolClosureId']
    bind(g, ctx); grants.append(g); contexts.append(ctx)
auth['authorizationRef'] = M.grant_set_ref(grants)
prepared = M.admit_preparation(auth, grants, contexts, 'linux-x86_64-gnu', set(), True)
check('preparation-mixed-owner-classes', prepared['admitted'] and len(prepared['securityGrantRefs']) == 2 and not prepared['executed'])
check('native-semantic-owner-preimage', {p['ownerSourceDigest'] for p in prepared['semanticGrantProjection']['principals']} == {g['ownerSourceDigest'] for g in grants})
# Admission occurs before any Plan; consuming analysis joins actual preparation provenance later.
plan_grant = {'schemaVersion': 2, 'projectId': auth['projectId'],
              'principals': prepared['semanticGrantProjection']['principals'],
              'analysisOperations': ['prepare-code', 'read-source'], 'scopeDigest': '0' * 64}
M.N.validate_foundation('semantic-grant', plan_grant)
M.N.IM.ordered(plan_grant)
check('consuming-plan-principals-canonically-ordered', plan_grant['principals'] == sorted(plan_grant['principals'], key=M.C.canonical))
check('consuming-plan-preparation-principal-join', M.S.admit_plan_execution_projection(plan_grant['principals'], grants, 'host-prepared')['result'] == 'ADMIT')
for index, source_grant in enumerate(grants):
    owner_preimage = M.owner_rows(source_grant['owners'])
    M.N.validate_foundation('owner-source-set', owner_preimage)
    owner_hash = hashlib.sha256(M.C.canonical(owner_preimage)).hexdigest()
    check('security-owner-source-record-to-consuming-plan.' + str(index),
          owner_hash == source_grant['ownerSourceDigest'] == M.owner_digest(source_grant['owners'])
          and any(p['closureId'] == source_grant['toolClosureId'] and p['ownerSourceDigest'] == owner_hash
                  for p in plan_grant['principals']))
check('consuming-plan-missing-principal-refused', M.S.admit_plan_execution_projection([], grants, 'host-prepared')['result'] == 'REFUSE')
check('imported-inert-does-not-infer-local-grant', M.S.admit_plan_execution_projection(plan_grant['principals'], [], 'imported-inert')['result'] == 'REFUSE')
check('test-runner-is-operational-not-a-plan-principal', M.S.semantic_projection_for_grants([grant]) == [])
check('test-runner-cannot-be-consumed-as-preparation', M.S.admit_plan_execution_projection([], [grant], 'host-prepared')['result'] == 'REFUSE')
bad_plan_grant = copy.deepcopy(plan_grant); bad_plan_grant['analysisOperations'] = ['test-code']
refuses('analysis-cannot-claim-test-execution-authority', lambda: M.N.validate_foundation('semantic-grant', bad_plan_grant))

refuses('missing-owner-grant-refused', lambda: M.admit_preparation(auth, grants[:1], contexts[:1], 'linux-x86_64-gnu', set(), True))
refuses('wrong-platform-refused', lambda: M.admit_preparation(auth, grants, contexts, 'macos-aarch64', set(), True))
refuses('missing-linker-refused', lambda: M.admit_preparation(auth, grants, contexts, 'linux-x86_64-gnu', set(), False))
bad = copy.deepcopy(grants[0]); bad['ownerSourceDigest'] = '0' * 64
refuses('owner-set-digest-refused', lambda: M.admit_grant(bad, contexts[0]))
bad = copy.deepcopy(grants[0]); bad['owners'] = None
refuses('malformed-owner-list-refused-before-nested-access', lambda: M.admit_grant(bad, contexts[0]))

registry = {domain: (HERE / row['schemaDocument']).read_bytes() for (_, domain), row in M.W.PAYLOAD_REGISTRY.items()}
ds = M.N.dependency_source_set_admit(nf['lock'], [nf['tarballRow']], ['serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index'])
payloads = {
    'prepared': {'schemaVersion': 1, 'payloadDomain': 'native.import-payload.prepared-output.v1', 'set': nf['prepInert']},
    'dependency': {'schemaVersion': 1, 'payloadDomain': 'native.import-payload.dependency-source.v1', 'set': ds['descriptor'],
                   'acquisitionSourcePath': '/synthetic/cache', 'tarballDigests': []},
    'runtime': wf['runtimePayload'],
}
# Replace fixture constants only; no claimed provider observations are generated.
def sub(value):
    if isinstance(value, str) and value.startswith('$'):
        return wf['constants'][value[1:]]
    if isinstance(value, dict):
        return {k: sub(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sub(v) for v in value]
    return value

for kind, payload in payloads.items():
    payload = sub(payload)
    scope = {'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': ['.'], 'excludedPathPrefixes': []}
    kwargs = {'kind': kind, 'payload': payload, 'correspondence': nf['corr'],
              'producer_closure': 'closure2:' + '2' * 64, 'adapter_closure': 'closure2:' + '3' * 64,
              'blobs': [{'path': 'payload.json', 'sha256': M.W.payload_digest(payload), 'bytes': len(M.C.canonical(payload))}], 'scope': scope, 'observation': {}}
    native = M.N.import2_wrap(**kwargs, completeness='complete', omissions=[])
    workflow = M.W.build_import(**kwargs, payload_domain=payload['payloadDomain'], registered_schemas=registry)
    check('native-workflow-wrapper-equality.' + kind, native['wrapper'] == workflow['wrapper'] and native['importId'] == workflow['importId'])
    for name, field in [('sourceCorrespondence', 'sourceCorrespondenceDigest'), ('buildIdentity', 'buildDigest'), ('scope', 'scopeDigest'), ('observation', 'observationDigest')]:
        check('retained-preimage.' + kind + '.' + name, hashlib.sha256(workflow['retainedPreimages'][name]).hexdigest() == workflow['wrapper'][field])

roots = M.C.parse((HERE / 'security/root-schema-cases.v1.json').read_bytes())['roots']
state = {'acceptedVersion': roots['root1']['rootVersion'], 'acceptedRoot': roots['root1']}
chain = [{'root': roots['root2'], 'signers': roots['root1']['rootKeys'] + roots['root2']['rootKeys']}]
clock = roots['root2']['issuedAt']
check('complete-root-chain-admitted', M.S.admit_root_chain(state, chain, clock, clock)['result'] == 'ACCEPT')
bad_chain = copy.deepcopy(chain); bad_chain[0]['root']['indexOrigin'] = False
check('malformed-root-chain-refused-before-chain-primitive', M.S.admit_root_chain(state, bad_chain, clock, clock)['result'] == 'REFUSE')
discovery = M.C.parse((HERE / 'security/discovery-cases.v1.json').read_bytes())['cases'][0]['input']
discovery['explicitJoins'] = ['.']
check('explicit-root-workspace-sentinel', M.S.discovery(discovery)['status'] == 'ACCEPT')

tokens = ['typescript', 'function', 'module.foo', '0', '(', 'x', ':', 'number', ')', ':', 'boolean']
check('native-foundation-subject-discriminator', M.N.subject_discriminator_projection(tokens, [tokens]) == hashlib.sha256(M.C.canonical(tokens)).hexdigest())
refuses('native-ambiguous-subject-refuses', lambda: M.N.subject_discriminator_projection(tokens, [tokens, tokens]))
closures = [{'schemaVersion': 2, 'kind': kind, 'manifestDigest': 'a' * 64, 'tree': [], 'semanticVersion': '2.0.0', 'protocolMajor': 3, 'platform': 'macos-aarch64'} for kind in ('stdlib', 'rust-dev-llvm')]
projection = M.N.native_context_closure_projection(*closures)
check('native-context-closure-suffix-join', projection['typescriptStdlibMerkleRoot'] == M.N.IM.identifier('closure', closures[0])[9:] and projection['rustcDevLlvmDigest'] == M.N.IM.identifier('closure', closures[1])[9:])
scope = {'schemaVersion': 2, 'workspaceRoots': ['unit' + str(i) for i in range(1025)], 'pathPrefixes': ['.'], 'excludedPathPrefixes': []}
refuses('scope-bound-refuses-without-truncation', lambda: M.N.validate_foundation('scope-descriptor', scope))
mapping_case = sub(wf['sourceMappingCases'][0])
refuses('source-mapping-foreign-snapshot-refused', lambda: M.W.admit_source_mapping(mapping_case['mapping'], mapping_case['inventory'], 'snapshot2:' + 'f' * 64))

F = M.load('integration_graph_fixture', 'integration-fixtures.py')
run, objects, blobs = F.build(resolved=True, has_match=True)
def bind_workflow_policy(run, objects, blobs, language):
    """Real workflow fixture compiled and rekeyed into either native language graph."""
    policy = sub(copy.deepcopy(wf['policyDocs']['basePolicy']))
    policy['rules'] = policy['rules'][:1]
    policy['rules'][0]['subjectEnumeration']['universe'] = language
    policy['rules'][0]['emitWhen']['relation'] = 'references'
    policy['rules'][0]['emitWhen']['minResolution'] = 'resolved-binding'
    policy['rules'][0]['subjectEnumeration']['include'] = ['**']
    predicate = policy['rules'][0]['emitWhen']
    predicate_digest = M.W.doc_digest(predicate)
    policy['rules'][0]['ruleProgramRef']['programDigest'] = predicate_digest
    compiled = {'schemaVersion': 1, 'policyDigest': M.W.doc_digest(policy),
                'rules': [{k: r[k] for k in ('ruleId', 'ruleProgramRef', 'emitWhen')} for r in policy['rules']]}
    waivers = wf['policyDocs']['waiversNone']
    for value in (policy, compiled, predicate, waivers):
        blobs[M.W.doc_digest(value)] = M.C.canonical(value)
    plan = copy.deepcopy(objects[run['planId']][1]); plan.update(policyDigest=M.W.doc_digest(policy), waiverDigest=M.W.doc_digest(waivers))
    F.rekey_plan(objects, blobs, run, plan)
    proof_id = objects[run['evaluationSealId']][1]['proofBundleId']
    proof = copy.deepcopy(objects[proof_id][1]); proof['ruleProgramDigest'] = M.W.rule_program_digest(policy)
    pred = proof['predicateProofs'][0]; pred['ruleId'] = policy['rules'][0]['ruleId']; pred['predicateId'] = 'p'
    program_predicate = {'schemaVersion': 2, 'ruleProgramDigest': proof['ruleProgramDigest'], 'ruleId': pred['ruleId'],
                         'predicateId': 'p', 'operation': predicate['op'], 'nodeDigest': predicate_digest}
    program_predicate_digest = M.W.doc_digest(program_predicate); blobs[program_predicate_digest] = M.C.canonical(program_predicate)
    witness = M.C.parse(blobs[pred['witnessDigest']]); witness['programPredicateDigest'] = program_predicate_digest
    pred['witnessDigest'] = M.W.doc_digest(witness); blobs[pred['witnessDigest']] = M.C.canonical(witness)
    F.rekey(objects, proof_id, proof, run)
    seal = copy.deepcopy(objects[run['evaluationSealId']][1]); seal['policyDigest'] = plan['policyDigest']
    F.rekey(objects, run['evaluationSealId'], seal, run)

bind_workflow_policy(run, objects, blobs, 'typescript')

def replay_workflow_fixture(plan, objects, blobs, refs):
    """Finite declared `none references` fixture only, not the full DSL evaluator.
    Recomputes from explicit input views; never reads the claimed proof outcome.
    """
    policy = M.C.parse(blobs[plan['policyDigest']]); rule = policy['rules'][0]
    assert rule['emitWhen'] == {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'filters': []}
    assert len(refs) == 1 and refs[0]['domain'] == 'view'
    view = objects['view2:' + refs[0]['digest']][1]
    matches = sorted(f for f in view['facts'] if objects[f][1]['relation'] == 'references')
    complete = all(M.C.parse(blobs[objects[c][1]['payloadDigest']])['entry']['coverage'] == 'complete' for c in view['coverageIds'])
    value = 'false' if matches else ('true' if complete else 'indeterminate')
    addressed = {'schemaVersion': 2, 'ruleProgramDigest': M.W.rule_program_digest(policy), 'ruleId': rule['ruleId'],
                 'predicateId': 'p', 'operation': 'none', 'nodeDigest': M.W.doc_digest(rule['emitWhen'])}
    witness = {'schemaVersion': 2, 'programPredicateDigest': M.W.doc_digest(addressed), 'matchingFactIds': matches, 'coverageIds': view['coverageIds'], 'countLimit': None, 'childPredicateIds': []}
    pid = M.N.IM.identifier('plan', plan)
    execution = next(k for k, (domain, v) in objects.items() if domain == 'execution-plan' and v['planId'] == pid)
    return {'schemaVersion': 2, 'planId': pid, 'executionPlanId': execution, 'evaluatorClosure': next(k for k in plan['semanticClosures'] if objects[k][1]['kind'] == 'evaluator'),
            'ruleProgramDigest': M.W.rule_program_digest(policy), 'evaluationInputRefs': refs,
            'predicateProofs': [{'ruleId': rule['ruleId'], 'subjectId': 'foo', 'predicateId': 'p', 'operation': 'none', 'inputRefs': refs,
                                 'scopeIds': view['scopeIds'], 'value': value, 'witnessDigest': M.W.doc_digest(witness)}],
            'findingIds': [], 'verdict': {'false': 'pass', 'true': 'fail', 'indeterminate': 'indeterminate'}[value]}

derivation = M.validate_workflow_policy_links(run, objects, blobs)
check('policy-derivation-joins-workflow-plan-and-proof', derivation['descriptor']['planId'] == run['planId'] and derivation['descriptor']['verdict'] == 'pass')
store = M.N.IM.EvidenceStore()
rid = store.prepare(run, objects, blobs, 'exec1_' + 'd' * 32, replay_workflow_fixture)
check('workflow-policy-through-foundation-replay-and-commit', store.commit('exec1_' + 'd' * 32) == 'committed' and rid in store.runs)
bad_objects = copy.deepcopy(objects)
bad_objects[objects[run['evaluationSealId']][1]['proofBundleId']][1]['ruleProgramDigest'] = '0' * 64
refuses('unbound-compiled-policy-program-refused', lambda: M.validate_workflow_policy_links(run, bad_objects, blobs))

bodies = [{'id': name, 'language': 'typescript', 'tokens': [{'kind': 'literal', 'value': str(i)} for i in range(offset, offset + 100)]} for name, offset in [('a', 0), ('b', 1), ('c', 2)]]
groups = M.N.clone_groups('near', bodies, params=dict(M.N.CLONE_PARAMS, nearThresholdMillionths=970000))
check('near-clone-explains-transitive-edges', len(groups) == 1 and [(e['left'], e['right']) for e in groups[0]['matchedEdges']] == [('a', 'b'), ('b', 'c')] and groups[0]['grouping'] == 'connected-component')
refuses('query-cannot-carry-execution-params', lambda: M.W.validate_dag([{'stepId': 0, 'kind': 'query', 'params': {'kind': 'native-preparation'}}]))

# Public details share one closed registry across actual owner outcomes.
registry = M.C.parse((HERE / 'public-detail-registry.v1.json').read_bytes())
details = {r['code'] for r in registry['records']}
common_schema = M.C.parse((HERE / 'workflows/schemas/common.schema.json').read_bytes())
check('public-detail-registry-schema-parity', details == set(common_schema['$defs']['DomainDetailCode']['enum']))

# CB6-MUST-1. The per-requirement sufficiency OUTCOME crosses a unit boundary: native section 4.6
# `sufficiency_v2` produces it and the workflows repair EvidenceRequirement consumes it. The
# workflows bundle resolves only workflows URNs, so the native vocabulary is MIRRORED there; these
# controls hold the mirror to its authority and hold the three vocabularies apart.
native_schemas = M.C.parse((HERE / 'native/native-evidence.schemas.v2.json').read_bytes())
NATIVE_DEFICIENCY_V2 = native_schemas['$defs']['DeficiencyV2']['enum']
repair_schema = M.C.parse((HERE / 'workflows/schemas/repair.schema.json').read_bytes())
check('native-sufficiency-vocabulary-mirror-is-exact',
      common_schema['$defs']['NativeSufficiencyDeficiency']['enum'] == NATIVE_DEFICIENCY_V2)
check('native-sufficiency-mirror-names-its-authority',
      common_schema['$defs']['NativeSufficiencyDeficiency']['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2'
      and repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']
          ['x-opensip-vocabulary']['nativePlaneAuthority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2')
# CX-BV6-03. Repair admits requirements over BOTH evidence planes, and the imported plane is owned
# by the imported-evidence document, not by native section 4.6. These controls hold the two
# vocabularies disjoint, hold each mirror to its own authority, and hold the boundary to deciding
# the plane from REGISTRY MEMBERSHIP rather than from the value.
imported_schema = M.C.parse((HERE / 'workflows/schemas/imported-evidence.schema.json').read_bytes())
IMPORTED_LAW = imported_schema['x-opensip-imported-requirement-law']
check('imported-requirement-mirror-is-exact-and-names-its-own-authority',
      common_schema['$defs']['ImportedRequirementDeficiency']['enum']
      == list(IMPORTED_LAW['precedence'])
      and set(IMPORTED_LAW['precedence']) == set(IMPORTED_LAW['outcomes'])
      and common_schema['$defs']['ImportedRequirementDeficiency']['x-opensip-vocabulary']['authority']
          .endswith('x-opensip-imported-requirement-law/outcomes'))
check('the-two-requirement-planes-are-disjoint-vocabularies',
      not (set(NATIVE_DEFICIENCY_V2) & set(IMPORTED_LAW['precedence'])))
check('the-repair-field-admits-both-plane-vocabularies-and-only-those',
      [b['$ref'].rsplit('/', 1)[1] for b in
       repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']['oneOf']]
      == ['NativeSufficiencyDeficiency', 'ImportedRequirementDeficiency'])
check('the-imported-plane-relations-are-exactly-the-imported-registry',
      set(imported_schema['x-opensip-evidence-relation-registry']['relations'])
      == {'runtime-observation', 'history-change'}
      and all(M.W.requirement_plane(r) == 'imported'
              for r in imported_schema['x-opensip-evidence-relation-registry']['relations'])
      and M.W.requirement_plane('references') == 'native')
# The producers really are different functions over different domains, and neither answers for the
# other. Root's contrast established the domains differ; these controls establish the ROUTING.
_imp_req = {'relation': 'runtime-observation', 'minResolution': 'observed',
            'completeness': 'complete'}
# BV6-V3-IMPORT-BINDING. Targets are FINGERPRINTS and are projected to payload subjects through the
# evidence Run's retained finding-fingerprint subjectKey; they are never read as paths. This is the
# cross-unit half: the foundation descriptor supplies the subject key that the workflows projection
# consumes, so a change to either side is visible here.
_imp_fp = 'finding-key2:' + '1' * 64
_imp_desc = {'schemaVersion': 2, 'ruleStableId': 'r', 'detectorSemanticsMajor': 1,
             'relatedSubjectKeys': [],
             'subjectKey': {'language': 'typescript', 'kind': 'function',
                            'logicalPath': 'src/a.ts', 'qualifiedName': 'foo',
                            'discriminator': 'd'}}
_imp_projection = M.W.project_targets_to_imported_subjects(
    [_imp_fp], 'runtime', {_imp_fp: {'fingerprint': _imp_fp}}, {_imp_fp: _imp_desc},
    [{'path': 'src/a.ts', 'symbol': 'foo', 'observability': 'observed-hit'}])
check('the-target-fingerprint-projects-through-the-retained-finding-subject-key',
      _imp_projection[_imp_fp]['matched'] is True
      and _imp_projection[_imp_fp]['logicalPath'] == _imp_desc['subjectKey']['logicalPath'])
check('the-foundation-fingerprint-descriptor-carries-the-subject-key-the-projection-reads',
      set(M.N.IM.SCHEMA['$defs']['finding-fingerprint']['properties']['subjectKey']['required'])
      == {'language', 'kind', 'logicalPath', 'qualifiedName', 'discriminator'}
      and M.N.IM.SCHEMA['x-opensip-digest-domains']['byDomain']['finding-fingerprint']
          ['representation'] == 'h-identity')
_imp_out = M.W.imported_requirement_outcome(
    _imp_req, _imp_projection,
    {'available': True, 'consumable': False, 'windowSatisfiesRequirement': True}, True)
check('the-imported-producer-emits-an-imported-outcome-for-an-imported-relation',
      _imp_out['satisfied'] is False and _imp_out['deficiency'] == 'import-unmapped-only')
check('the-repair-record-carries-that-exact-imported-value-on-its-own-plane',
      M.W.admit_evidence_requirement(dict(_imp_req, satisfied=False,
                                          deficiency=_imp_out['deficiency']))
      == ('imported', 'import-unmapped-only'))
# BV6-V3-IMPORT-CAUSE: the consumer decides the PER-KIND law, not merely the broad plane.
refuses('a-runtime-relation-cannot-carry-a-history-outcome',
        lambda: M.W.admit_evidence_requirement(
            dict(_imp_req, satisfied=False, deficiency='history-range-insufficient')))
refuses('a-history-relation-cannot-carry-a-runtime-outcome',
        lambda: M.W.admit_evidence_requirement(
            {'relation': 'history-change', 'minResolution': 'observed', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'subject-not-observable'}))
refuses('a-native-relation-cannot-carry-an-imported-outcome',
        lambda: M.W.admit_evidence_requirement(
            {'relation': 'references', 'minResolution': 'resolved-binding',
             'completeness': 'complete', 'satisfied': False, 'deficiency': 'import-unmapped-only'}))
refuses('an-imported-relation-cannot-carry-a-native-outcome',
        lambda: M.W.admit_evidence_requirement(
            dict(_imp_req, satisfied=False, deficiency='resolution-incomplete')))
refuses('the-imported-producer-refuses-a-native-relation',
        lambda: M.W.imported_requirement_outcome(
            {'relation': 'references', 'minResolution': 'resolved-binding',
             'completeness': 'complete'}, _imp_projection, {'available': True}, True))
# The two owning documents must agree that a required receipt carries a bound operation: this is the
# cross-unit half of CX-BV6-04, where the result lives in workflows and the receipt in repair.
_MAP_X = repair_schema['x-opensip-mutation-operation-map']['byStepKindReceiptOperation']
_IR_X = M.C.parse((HERE / 'workflows/schemas/invocation-record.schema.json').read_bytes())['$defs']
check('a-required-receipt-has-a-bound-operation-for-every-mutating-step-kind',
      'receiptId' in _IR_X['ImportResult']['required']
      and 'receiptId' in _IR_X['NativePreparationResult']['required']
      and _MAP_X['import']['operation'] == 'import'
      and _MAP_X['native-preparation']['operation'] == 'native-preparation'
      and 'operation' in repair_schema['$defs']['MutationReceiptV1']['required'])
check('native-sufficiency-outcome-is-not-the-d9-termination-vocabulary',
      set(NATIVE_DEFICIENCY_V2) - set(common_schema['$defs']['D9Deficiency']['enum'])
      == {'derivation-policy-unmet', 'external-consumers-unknown', 'input-closure-incomplete',
          'resolution-incomplete'})
check('the-native-registry-publishes-the-per-requirement-consumer-boundary',
      native_schemas['x-opensip-deficiency-cause-registry']['perRequirementConsumerBoundary']
      ['consumers'][0]['record']
      == 'workflows/schemas/repair.schema.json#/$defs/EvidenceRequirement')
# The producer really emits one of the four, and the consumer record really carries THAT value: a
# real sufficiency_v2 evaluation, not a hand-written string.
_uni_req = {'relation': 'references', 'minResolution': 'resolved-binding', 'completeness': 'complete',
            'quantifier': 'universal-negative', 'unresolvedEdgePolicy': 'forbid'}
_uni_view = {'references': {'resolution': 'resolved-binding', 'coverage': 'complete',
                            'resolutionCompleteness': {'state': 'partial', 'unresolvedEdgeCount': 2,
                                                       'unresolvedEdgeClasses': ['computed-member-access']}}}
_suff = M.N.sufficiency_v2(_uni_req, _uni_view)
check('sufficiency-v2-emits-resolution-incomplete-for-the-destructive-repair-case',
      _suff['satisfied'] is False and _suff['deficiency'] == 'resolution-incomplete')
_carried = {'relation': _uni_req['relation'], 'minResolution': _uni_req['minResolution'],
            'completeness': 'complete', 'satisfied': _suff['satisfied'],
            'deficiency': _suff['deficiency']}
check('the-repair-record-carries-that-exact-producer-value',
      M.W.admit_evidence_requirement(_carried) == ('native', 'resolution-incomplete'))
M.W.validate_import_record('workflows/schemas/repair.schema.json',
                           '#/$defs/EvidenceRequirement', _carried)
check('the-carried-producer-value-is-schema-valid-in-the-consumer-record', True)
refuses('the-d9-mapped-value-is-refused-in-the-consumer-record',
        lambda: M.W.validate_import_record('workflows/schemas/repair.schema.json',
                                           '#/$defs/EvidenceRequirement',
                                           dict(_carried, deficiency='verdict-indeterminate')))

# CB6-ADV-3. The successor D9 artifact is a LIVE, MANDATORY cross-unit obligation, and the correct
# handling of it is to carry the obligation rather than repin the historical evidence. These
# controls hold all three halves at once: the inherited artifact keeps its exact bytes and still
# omits the cause; the selected successor composition DOES carry it and is what the product source
# runs on; and the mismatch is disclosed and attributed rather than silently reconciled.
INHERITED_D9 = M.C.parse((HERE.parent / 'artifacts/d9-exit-contract.v1.14.json').read_bytes())
_inherited_causes = INHERITED_D9['scenarioAxesSchema']['properties']['faultCause']['enum']
check('the-inherited-d9-artifact-still-omits-the-host-invariant-cause',
      'host-invariant' not in _inherited_causes
      and 'host-invariant' not in INHERITED_D9['codeMaps']['faultCauseToErrorCode'])
check('the-inherited-artifact-already-published-the-error-code-with-no-preimage',
      'SYSTEM.OUTCOME.ILLEGAL_STATE' in INHERITED_D9['codeVocabulary']['errorCodes']
      and 'SYSTEM.OUTCOME.ILLEGAL_STATE' not in INHERITED_D9['codeMaps']['faultCauseToErrorCode'].values())
check('the-selected-successor-composition-carries-the-cause-the-inherited-artifact-cannot',
      'host-invariant' in common_schema['$defs']['D9FaultCause']['enum']
      and set(_inherited_causes) | {'host-invariant'}
          == set(common_schema['$defs']['D9FaultCause']['enum']))
check('the-successor-map-stays-injective-and-adds-no-error-code',
      len(set(INHERITED_D9['codeMaps']['faultCauseToErrorCode'].values()))
      == len(INHERITED_D9['codeMaps']['faultCauseToErrorCode'])
      and 'SYSTEM.OUTCOME.ILLEGAL_STATE' in INHERITED_D9['codeVocabulary']['errorCodes'])
check('the-cross-unit-obligation-is-disclosed-and-attributed-not-reconciled-by-repinning',
      native_schemas['x-opensip-public-route-registry']['successorArtifactObligation']['owedBy']
      == 'the D9 exit-contract unit'
      and 'MANDATORY, LIVE and CROSS-UNIT'
      in native_schemas['x-opensip-public-route-registry']['successorArtifactObligation']['standing']
      and 'Publishing the successor D9 artifact belongs to that unit'
      in native_schemas['x-opensip-public-route-registry']['successorArtifactObligation']['neverDischargedByRepinning']
      and 'HISTORICAL and unchanged'
      in common_schema['$defs']['D9FaultCause']['description'])
aliases = {r['internalCode']: r['publicCode'] for r in registry['internalAliases']}
check('security-primary-detail-registry-coverage', {aliases.get(c, c) for c in M.S.D9} <= details)
check('native-detail-registry-coverage', {aliases.get(c, c) for c in M.N.D9_MAP} <= details)
for row in registry['records']:
    example = {'code': row['code'], 'remedy': 'See the owning contract.'}
    if row['code'] == 'evidence.pinned':
        # This detail's owning law needs the complete observed pin inventory, not a bare code.
        example = M.W.pinned_purge_refusal('req1_'+'a'*32, 'run2:'+'a'*64,
                    [{'pinId':'baseline:main','kind':'baseline'}])['termination']['domainDetail']
    M.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail', example)
check('all-registered-owner-details-admitted', len(details) == len(registry['records']))
for code in ('native.execution-not-authorized', 'native.stale-prepared-output', 'native.explicit-root-without-marker'):
    term = M.public_termination(M.N.d9_map(code), code, 'Correct the named admitted input; no repository code was executed.')
    check('native-public-detail.' + code, term['domainDetail']['code'] == code and M.W.exit_code(term) == 2)
for key, detail in [('RECOVERY.REFUSED', 'RECOVERY.REFUSED'), ('MIGRATION.CORRUPT', 'MIGRATION.CORRUPT'), ('GRANT.REFUSED', 'AUTHZ.SOURCE_MOVED')]:
    term = M.public_termination(M.S.d9(key), detail, 'Inspect the current admitted state and repair the named condition.')
    check('security-public-detail.' + detail, term['domainDetail']['code'] == detail)
for code in ('evidence.expired', 'evidence.purged', 'evidence.missing', 'evidence.corrupt'):
    term = M.public_termination({'class': 'indeterminate', 'exit': 3, 'code': 'QUERY.COMPLETENESS_UNMET'}, code, 'Restore the required evidence closure, or report its unavailability.')
    check('identity-public-detail.' + code, term['domainDetail']['code'] == code)
refuses('unregistered-public-detail-refused', lambda: M.public_termination(M.S.d9('GRANT.REFUSED'), 'native.unregistered-future-code', 'unknown'))
refuses('uppercase-storage-alias-refused', lambda: M.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail', {'code': 'STORAGE.BACKUP_CHOICE_REQUIRED', 'remedy': 'alias'}))

# One public spelling for each shared discovery condition, independent of unit owner.
for internal in ('PROJECT.WORKSPACE_UNIT_LIMIT', 'WORKSPACE_UNIT_LIMIT', 'native.too-many-units'):
    term = M.public_termination(M.S.d9('PROJECT.WORKSPACE_UNIT_LIMIT'), internal, 'Narrow the selected workspace.')
    check('shared-unit-cap-canonical-public-code.' + internal, term['domainDetail']['code'] == 'PROJECT.WORKSPACE_UNIT_LIMIT')
for internal in ('PROJECT.EXPLICIT_PATH_INVALID', 'native.explicit-root-grammar'):
    term = M.public_termination(M.S.d9('PROJECT.EXPLICIT_PATH_INVALID'), internal, 'Use a canonical relative workspace root.')
    check('shared-root-grammar-canonical-public-code.' + internal, term['domainDetail']['code'] == 'PROJECT.EXPLICIT_PATH_INVALID')
for internal in (*aliases, 'GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED'):
    refuses('internal-or-dead-detail-not-public.' + internal, lambda c=internal: M.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail', {'code': c, 'remedy': 'internal'}))

# Regression from actual Claude P7: existential presence cannot bypass confidence.
confidence_req = {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'minConfidenceMillionths': 900000,
                  'completeness': 'partial-ok', 'quantifier': 'existential', 'unresolvedEdgePolicy': 'forbid', 'externalConsumerPolicy': 'forbid'}
confidence_view = {'clones': {'relation': 'clones', 'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': 100000,
                             'resolutionCompleteness': {'state': 'not-applicable', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}}}
check('existential-clone-confidence-floor-enforced', M.N.sufficiency_v2(confidence_req, confidence_view).get('deficiency') == 'confidence-floor-unmet')

# Regression from actual Claude P8: a hash-valid import cannot become a hidden finding input.
frun, fobjects, fblobs = F.build(resolved=True, has_match=True)
def fput(value):
    raw = M.C.canonical(value); digest = hashlib.sha256(raw).hexdigest(); fblobs[digest] = raw; return digest
fclosure = next(k for k, (domain, value) in fobjects.items() if domain == 'closure')
control_run, control_objects, control_blobs = F.graph_with_import()
check('finding-import-control-closes-with-selected-import', M.N.IM.close_run(control_run, control_objects, control_blobs).startswith('run2:'))
foreign_id = control_objects[control_run['planId']][1]['importIds'][0]
fobjects[foreign_id] = copy.deepcopy(control_objects[foreign_id]); fblobs.update(control_blobs)
ffingerprint = {'schemaVersion': 2, 'ruleStableId': 'no-consumer', 'detectorSemanticsMajor': 2,
                'subjectKey': {'language': 'typescript', 'kind': 'symbol', 'logicalPath': 'a.ts', 'qualifiedName': 'foo', 'discriminator': 'one'}, 'relatedSubjectKeys': []}
ffk = M.N.IM.identifier('finding-fingerprint', ffingerprint); fobjects[ffk] = ('finding-fingerprint', ffingerprint)
finding = {'schemaVersion': 2, 'fingerprint': ffk, 'ruleClosure': fclosure, 'subjectId': 'foo', 'messageCode': 'unused',
           'parameterDigest': fput({'schemaVersion': 2, 'messageCode': 'unused', 'parameters': {}}), 'severity': 'error', 'evidenceRefs': [{'domain': 'import', 'digest': foreign_id.split(':')[1]}]}
fid = M.N.IM.identifier('finding', finding); fobjects[fid] = ('finding', finding)
pk = fobjects[frun['evaluationSealId']][1]['proofBundleId']; fproof = copy.deepcopy(fobjects[pk][1]); fproof['findingIds'] = [fid]; F.rekey(fobjects, pk, fproof, frun)
ek = frun['evidenceId']; fevidence = copy.deepcopy(fobjects[ek][1]); fevidence['findingIds'] = [fid]; F.rekey(fobjects, ek, fevidence, frun)
try:
    M.N.IM.close_run(frun, fobjects, fblobs)
except M.N.IM.C.AdmissionError as exc:
    check('unselected-finding-import-refused', str(exc) == 'HIDDEN_FINDING_EVIDENCE')
else:
    check('unselected-finding-import-refused', False)
selected_fact = next(k for k, (domain, value) in fobjects.items() if domain == 'fact')
selected_finding = copy.deepcopy(finding); selected_finding['evidenceRefs'] = [{'domain': 'fact', 'digest': selected_fact.split(':')[1]}]
F.rekey(fobjects, fid, selected_finding, frun)
check('finding-cites-selected-view-fact', M.N.IM.close_run(frun, fobjects, fblobs).startswith('run2:'))

# Closed scalar grammars reject final newlines without altering general text encoding.
for definition, value in [('Hash', 'a' * 64), ('ProjectId', 'prj1-' + 'a' * 64)]:
    schema = dict(M.N.IM.SCHEMA, **{'$ref': '#/$defs/' + definition})
    M.C.validate(schema, value)
    check('closed-scalar-valid.' + definition, True)
    for suffix in ('\n', '\r\n', ' '):
        refuses('closed-scalar-suffix-refused.' + definition + '.' + repr(suffix), lambda s=suffix: M.C.validate(schema, value + s))
check('ordinary-newline-text-preserved', M.C.parse(M.C.canonical({'message': 'line one\nline two'}))['message'] == 'line one\nline two')
for definition, value in [('ClosureId2', 'closure2:' + 'a' * 64), ('SnapshotId2', 'snapshot2:' + 'a' * 64)]:
    refuses('native-closed-scalar-newline-refused.' + definition, lambda: M.N.validate_native(definition, value + '\n'))
newline_grant = copy.deepcopy(sf['grantBase']); newline_grant['projectId'] += '\n'
refuses('security-project-id-newline-refused', lambda: M.S.validate_input('RepoExecutionGrantV2', newline_grant))

# Actual security admission -> workflow repair, not a caller-created authorization.
rs = sub(copy.deepcopy(wf['repairScenario']))
repair_tree = {k: v.encode() for k, v in rs['tree'].items()}
repair_run = rs['run']; project_id = wf['constants']['PRJ']
repair_run['snapshotId'] = M.W.fixture_tree_snapshot_id(project_id, repair_tree)
repair_edits = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e) for e in rs['edits']]
repair_trust = {rs['recipe']['closureId']: 'admitted'}
repair_plan = M.W.repair_preview(project_id, repair_tree, repair_run, rs['recipe'], rs['targets'], repair_edits,
                               rs['evidenceRequirements'], rs['permittedScope'], repair_trust)
rf = M.C.parse((HERE / 'security/repair-authorization-cases.v1.json').read_bytes())
repair_auth = copy.deepcopy(rf['authorizationBase'])
repair_auth.update(projectId=project_id, repairPlanId=repair_plan['repairPlanId'],
                   baseSnapshotId=repair_plan['descriptor']['snapshotId'], recipeClosureId=rs['recipe']['closureId'])
repair_ctx = copy.deepcopy(rf['ctxBase']); repair_ctx['admittedClosures'] = list(repair_trust)
def repair_ref(auth):
    return 'security.repair-apply-authorization.v1:' + M.C.identity('security.repair-apply-authorization.v1', auth)
repair_projection = M.repair_authorization_projection(repair_auth, repair_ctx, repair_plan, repair_ref(repair_auth))
postimages = {e['path']: e['postimage'] for e in repair_edits if e.get('postimage') is not None}
journal, receipt, after = M.W.repair_apply(repair_plan, postimages, repair_tree, project_id, wf['constants']['REQ'], 2,
                                         repair_projection, False, 'interactive', {}, repair_trust, {})
check('security-to-repair-complete-authorization-reference', journal['state'] == 'COMMITTED' and journal['authorizationRef'] == repair_ref(repair_auth) and receipt['effectOutcome'] == 'COMPLETED')
wrong_recipe = copy.deepcopy(repair_auth); wrong_recipe['recipeClosureId'] = 'closure2:' + '7' * 64
refuses('security-to-repair-foreign-recipe-refused', lambda: M.repair_authorization_projection(wrong_recipe, repair_ctx, repair_plan, repair_ref(wrong_recipe)))
refuses('security-to-repair-unadmitted-recipe-refused', lambda: M.repair_authorization_projection(repair_auth, dict(repair_ctx, admittedClosures=[]), repair_plan, repair_ref(repair_auth)))
refuses('security-to-repair-foreign-authorization-ref-refused', lambda: M.repair_authorization_projection(repair_auth, repair_ctx, repair_plan, repair_ref(wrong_recipe)))
wrong_plan = copy.deepcopy(repair_plan); wrong_plan['descriptor']['recipe']['closureId'] = 'closure2:' + '7' * 64
refuses('security-to-repair-unhashed-plan-refused', lambda: M.repair_authorization_projection(repair_auth, repair_ctx, wrong_plan, repair_ref(repair_auth)))

# Repair consent is projected from the same admitted security modes as test consent.
for ci in (False, True):
    pa=copy.deepcopy(repair_auth);pa['consent']={'mode':'policy-record','policyRecordId':'a'*64,'ci':ci}
    pc=dict(repair_ctx,ci=ci);pp=M.repair_authorization_projection(pa,pc,repair_plan,repair_ref(pa))
    pj,pr,pt=M.W.repair_apply(repair_plan,postimages,repair_tree,project_id,wf['constants']['REQ'],2,pp,ci,'policy',{},repair_trust,{})
    check('security-policy-record-to-repair.ci='+str(ci),pj['state']=='COMMITTED' and pp['consentSource']=='policy' and pp['ci'] is ci)
    refuses('repair-consent-relabel-refused.ci='+str(ci),lambda:M.W.repair_apply(repair_plan,postimages,repair_tree,project_id,wf['constants']['REQ'],2,pp,ci,'interactive',{},repair_trust,{}))
refuses('repair-ci-context-relabel-refused',lambda:M.W.repair_apply(repair_plan,postimages,repair_tree,project_id,wf['constants']['REQ'],2,repair_projection,True,'interactive',{},repair_trust,{}))

# Core intent -> security namespace scope: caller cannot supply a smaller lease set.
core_intent = {'schemaVersion': 1, 'operation': 'core-update', 'fromCoreClosure': 'closure2:' + '1' * 64,
               'toCoreClosure': 'closure2:' + '2' * 64, 'fromStateSchema': 1, 'toStateSchema': 2,
               'fromStoreGeneration': 3, 'toStoreGeneration': 4,
               'platformProfileSetBodyDigest': 'a' * 64, 'preconditionGeneration': 0, 'rollbackDeadline': None}
check('core-schema-migration-locks-all-namespaces', M.core_transition_scope(core_intent, ['ns-b', 'ns-a'])['namespaces'] == ['ns-a', 'ns-b'])
check('core-same-schema-update-pins-generations-fence-only', M.core_transition_scope(dict(core_intent, fromStateSchema=2, toStoreGeneration=3), ['ns-a'])['namespaces'] == [])
check('core-rollback-locks-all-even-same-schema', M.core_transition_scope(dict(core_intent, fromStateSchema=2, toStoreGeneration=3, operation='core-rollback', rollbackDeadline='2027-01-11T12:00:00Z'), ['ns-a'])['namespaces'] == ['ns-a'])
refuses('core-caller-lease-scope-override-refused', lambda: M.core_transition_scope(dict(core_intent, reselectsStore=False), ['ns-a']))

# Fresh actual security recovery admission joins a real apply journal and exact plan.
rrf = M.C.parse((HERE / 'security/repair-recovery-authorization-cases.v1.json').read_bytes())
rjournal = dict(journal, state='APPLIED'); rjournal.pop('appliedSnapshotId', None)
rctx = copy.deepcopy(rrf['ctxBase']); rctx.update(projectId=project_id, admittedClosures=list(repair_trust), revokedClosures=[])
ra = copy.deepcopy(rrf['authorizationBase']); ra.update(projectId=project_id, repairPlanId=repair_plan['repairPlanId'],
    baseSnapshotId=repair_plan['descriptor']['snapshotId'], recipeClosureId=rs['recipe']['closureId'],
    journalRef=M.S.repair_journal_identity(rjournal), journalState=rjournal['state'],
    observedJournalStateDigest=M.S.repair_journal_state_digest(rjournal), recoveryAction='verify-postimages-and-commit',
    originalRequestId=rjournal['requestId'])
ra['recoveryRequestId'] = 'req1_' + '8' * 32; ra['recoveryExecutionId'] = 'exec1_' + '8' * 32
rctx.update(recoveryRequestId=ra['recoveryRequestId'], recoveryExecutionId=ra['recoveryExecutionId'])
def rrref(a): return M.S.RECOVERY_AUTHZ_DOMAIN + ':' + M.C.identity(M.S.RECOVERY_AUTHZ_DOMAIN, a)
def rrintent(a): return {'schemaVersion': 1, 'kind': 'repair-recover', 'journalRef': a['journalRef'],
    'repairPlanId': a['repairPlanId'], 'recoveryAction': a['recoveryAction'], 'authorizationRef': rrref(a)}
def rrproject(a=ra, c=rctx, j=rjournal): return M.recovery_authorization_projection(a,c,repair_plan,j,rrref(a),rrintent(a))
rprojection = rrproject()
check('security-workflow-journal-preimages-identical', M.W.recovery_journal_bindings(rjournal) == (M.S.repair_journal_identity(rjournal), M.S.repair_journal_state_digest(rjournal)))
check('security-workflow-recovery-action-table-identical', {k:v[0] for k,v in M.W.RECOVERY_TABLE.items() if v[0] in M.W.MUTATING_RECOVERY} == M.S.RECOVERY_ACTION_FOR_STATE)
rout = M.W.repair_recover(rjournal, repair_plan, after, project_id, {}, rprojection)
check('security-to-recovery-full-reference-commits', rout[0]['state'] == 'COMMITTED' and rout[0]['recoveryAuthorizationRef'] == rrref(ra))
refuses('recovery-expired-authority-refused', lambda: rrproject(c=dict(rctx, admittedTime='2028-01-10T12:00:00Z')))
refuses('recovery-moved-journal-refused', lambda: rrproject(j=dict(rjournal, state='INDETERMINATE')))
refuses('recovery-wrong-project-refused', lambda: rrproject(c=dict(rctx, projectId='prj1-'+'9'*64)))
refuses('recovery-revoked-commit-refused', lambda: rrproject(c=dict(rctx, revokedClosures=list(repair_trust))))
refuses('recovery-ci-interactive-refused', lambda: rrproject(c=dict(rctx, ci=True)))
refuses('recovery-original-execution-not-fresh', lambda: rrproject(a=dict(ra,recoveryExecutionId=rjournal['executionId']),c=dict(rctx,recoveryExecutionId=rjournal['executionId'])))
refuses('recovery-fresh-attempt-binding-refused', lambda: rrproject(c=dict(rctx, recoveryExecutionId='exec1_'+'9'*32)))
refuses('recovery-foreign-reference-refused', lambda: M.recovery_authorization_projection(ra,rctx,repair_plan,rjournal,rrref(ra)+'0',rrintent(ra)))
refuses('recovery-caller-projection-refused', lambda: M.W.repair_recover(rjournal,repair_plan,after,project_id,{}, {'repairPlanId':repair_plan['repairPlanId'],'requestId':rjournal['requestId']}))
rbj = dict(rjournal, state='APPLYING'); rba = dict(ra, journalState='APPLYING', observedJournalStateDigest=M.S.repair_journal_state_digest(rbj), recoveryAction='roll-back-renamed')
rbp = rrproject(a=rba,c=dict(rctx,revokedClosures=list(repair_trust),admittedClosures=[]),j=rbj)
preimages = {M.W.raw_sha(v):v for v in repair_tree.values()}
rbo = M.W.repair_recover(rbj,repair_plan,after,project_id,preimages,rbp)
check('recovery-revoked-recipe-still-rolls-back', rbo[0]['state']=='FAILED_ROLLED_BACK' and rbo[0]['_tree']==repair_tree)

# All five installation operations share closed intent/journal semantics and durable recovery.
tf = M.C.parse((HERE / 'security/transition-journal-cases.v1.json').read_bytes())
for key in ('UpdateSchemaChange','UpdateSameSchema','Repair','CoreRollback','StoreMigrate','StoreRollback'):
    ti = tf['records']['intent'+key]; tj = M.S.transition_journal_record(ti,tf['ctxBase']['namespaceRegistry'])
    tc = dict(tf['ctxBase'], currentStateSchema=ti['fromStateSchema'],currentStoreGeneration=ti['fromStoreGeneration'],
              currentCoreGeneration=ti['preconditionGeneration'],leasesHeld=tj['leaseSet'])
    ta = M.admit_installation_transition(ti,tj,tc)
    check('installation-intent-journal-join.'+key, ta['result']=='ADMIT')
    trc = dict(tf['rctx'],leasesReacquired=tj['leaseSet'])
    history = [dict(tj,state=st) for st in ('LEASED','PREPARING','PREPARED','COMMITTED','DONE')]
    hrefs = M.installation_journal_history(ti,history)
    check('installation-attempt-retains-durable-revisions.'+key,len(hrefs)==5 and len(set(hrefs))==5)
    M.W.validate_import_record('workflows/schemas/invocation-record.schema.json','#/$defs/Attempt',{'executionId':'exec1_'+'3'*32,'outcome':'completed','installationJournalRefs':hrefs})
    refuses('installation-history-skipped-state.'+key,lambda:M.installation_journal_history(ti,[history[0],history[-1]]))
    tr = M.recover_installation_transition(tj,ta['journalRef'],trc)
    check('installation-initial-crash-aborts.'+key,tr['action']=='ABORT')
    for state in ('LEASED','PREPARING','PREPARED','COMMITTED','DONE','ABORTED'):
        observed = dict(tj,state=state); observed_ref = M.S.TRANSITION_JOURNAL_DOMAIN+':'+M.C.identity(M.S.TRANSITION_JOURNAL_DOMAIN,observed)
        recovered = M.installation_recovery_attempt(ti,observed,observed_ref,trc,'exec1_'+'7'*32)
        check('installation-fresh-recovery-history.'+key+'.'+state,recovered['attempt']['installationRecoveryStartRef']==observed_ref and recovered['attempt']['installationJournalRefs'][0]==observed_ref and observed['state']==state)
        if recovered['decision']['journalStateAfter'] is not None:
            check('installation-recovery-persists-result-state.'+key+'.'+state,recovered['journals'][-1]['state']==recovered['decision']['journalStateAfter'])
    if ti['operation'] in ('store-migrate','store-rollback'):
        prepared = dict(tj,state='PREPARED'); pref=M.S.TRANSITION_JOURNAL_DOMAIN+':'+M.C.identity(M.S.TRANSITION_JOURNAL_DOMAIN,prepared)
        footprint={'old':{'present':True,'unbootstrappedReason':'RESTORED'},'new':{'dir':'migrating','state':'PREPARED'}}
        recovered=M.installation_recovery_attempt(ti,prepared,pref,dict(trc,storeFootprint=footprint),'exec1_'+'6'*32)
        check('installation-prepared-store-resume-new-attempt.'+key,[j['state'] for j in recovered['journals']]==['PREPARED','COMMITTED','DONE'])
    refuses('installation-recovery-history-wrong-start-ref.'+key,lambda:M.installation_journal_history(ti,[dict(tj,state='COMMITTED')],ta['journalRef']))

    committed = dict(tj,state='COMMITTED'); cref=M.S.TRANSITION_JOURNAL_DOMAIN+':'+M.C.identity(M.S.TRANSITION_JOURNAL_DOMAIN,committed)
    check('installation-committed-crash-finishes.'+key,M.recover_installation_transition(committed,cref,trc)['action']=='RESUME-COMMIT')
    refuses('installation-journal-state-ref-binding.'+key,lambda: M.recover_installation_transition(committed,ta['journalRef'],trc))
    wrong = dict(tj, intentDigest='0'*64); wref=M.S.TRANSITION_JOURNAL_DOMAIN+':'+M.C.identity(M.S.TRANSITION_JOURNAL_DOMAIN,wrong)
    refuses('installation-recovery-rehashes-intent.'+key,lambda:M.recover_installation_transition(wrong,wref,trc))
    if tj['leaseSet']:
        wrong=dict(tj,leaseSet=[]); wref=M.S.TRANSITION_JOURNAL_DOMAIN+':'+M.C.identity(M.S.TRANSITION_JOURNAL_DOMAIN,wrong)
        refuses('installation-recovery-rederives-scope.'+key,lambda:M.recover_installation_transition(wrong,wref,dict(trc,leasesReacquired=[])))
        refuses('installation-initial-incomplete-locks.'+key,lambda:M.admit_installation_transition(ti,tj,dict(tc,leasesHeld=[])))
        check('installation-recovery-busy.'+key,M.recover_installation_transition(tj,ta['journalRef'],dict(trc,leasesReacquired=[]))['action']=='BUSY')
    check('installation-registry-change-quarantines.'+key,M.recover_installation_transition(tj,ta['journalRef'],dict(trc,namespaceRegistry=['foreign']))['action']=='QUARANTINE')

# Shared discovery on one custody inventory (Cargo workspace folding is a later native operation).
disc_case = next(c for c in M.C.parse((HERE / 'security/discovery-cases.v1.json').read_bytes())['cases']
                 if c['id'].startswith('installed-dependencies-and-cargo-build-output'))
di = copy.deepcopy(disc_case['input']); sd = M.S.discovery(di)
root_path = sd['provenance']['selectedRoot']
markers = {p[len(root_path) + 1:]: {'sha256': '1' * 64} for p, info in di['fs'].items()
           if p.startswith(root_path + '/') and info['kind'] == 'file' and p.rpartition('/')[2] in M.S.DD.WORKSPACE_MARKERS}
nd = M.N.discover_units(markers)
security_roots = {u['path'][len(root_path) + 1:] if u['path'] != root_path else '' for u in sd['provenance']['units']}
check('security-native-shared-unit-roots', security_roots == {u['rootPath'] for u in nd['units']})
check('security-native-shared-pruned-trees', [dict(t, path=t['path'][len(root_path) + 1:]) for t in sd['provenance']['prunedTrees']] == nd['prunedTrees'])
check('shared-ignore-does-not-erase-legal-target-directory', M.S.DD.classify_path('packages/target/index.ts', {''}) is None)
check('shared-ignore-prunes-real-cargo-target', M.S.DD.classify_path('target/out.rs', {''}) == ('target', 'cargo-build-output'))

# Operational host composition never drops security's nested project/repository boundary decision.
boundary_input = copy.deepcopy(di)
broot = '/home/alice/repo'; directory = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}
file_row = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
for path in ('apps', 'apps/site', 'apps/site/sub', 'vendor', 'vendor/lib'):
    boundary_input['fs'][broot + '/' + path] = dict(directory)
boundary_input['fs'][broot + '/vendor/lib']['vcs'] = True
for path in ('apps/site/opensip.json', 'apps/site/package.json', 'apps/site/sub/Cargo.toml', 'apps/site/main.ts', 'vendor/lib/package.json', 'vendor/lib/index.ts', 'main.ts'):
    boundary_input['fs'][broot + '/' + path] = dict(file_row)
bfiles = [p[len(broot) + 1:] for p, row in boundary_input['fs'].items() if p.startswith(broot + '/') and row['kind'] == 'file']
bmarkers = {p: {'sha256': '1' * 64} for p in bfiles if p.rpartition('/')[2] in M.S.DD.WORKSPACE_MARKERS}
bjoined = M.admit_repository_discovery(boundary_input, bmarkers, bfiles)
check('host-nested-boundaries-admitted-once', bjoined['boundaries']['nestedProjects'] == ['apps/site'] and bjoined['boundaries']['nestedRepositories'] == ['vendor/lib'])
check('host-nested-boundaries-no-native-units', not any(u['rootPath'].startswith(('apps/site', 'vendor/lib')) for u in bjoined['native']['units']))
check('host-nested-boundaries-no-source-capture', not any(p.startswith(('apps/site/', 'vendor/lib/')) for p in bjoined['sourceCaptureCandidates']))
check('host-nested-boundaries-plan-visible', {'apps/site', 'vendor/lib'} <= set(bjoined['scope']['scopeDescriptor']['excludedPathPrefixes']))
refuses('host-native-inventory-substitution-refused', lambda: M.admit_repository_discovery(boundary_input, dict(bmarkers, **{'foreign/package.json': {'sha256': '2' * 64}}), bfiles))
inside = copy.deepcopy(boundary_input); inside['cwd'] = broot + '/apps/site'
inside_files = ['package.json', 'sub/Cargo.toml', 'main.ts', 'opensip.json']
inside_markers = {p: {'sha256': '1' * 64} for p in inside_files if p.rpartition('/')[2] in M.S.DD.WORKSPACE_MARKERS}
inside_joined = M.admit_repository_discovery(inside, inside_markers, inside_files)
check('host-launch-inside-nested-config-selects-that-project', inside_joined['discovery']['provenance']['selectedRoot'] == broot + '/apps/site' and inside_joined['boundaries']['nestedProjects'] == [])

# Actual typed importer -> retained source correspondence -> identity closure (N-3).
check('run-import-exact-source-closes', M.N.IM.close_run(*F.graph_with_import()).startswith('run2:'))
refuses('run-import-foreign-exact-source-refused', lambda: M.N.IM.close_run(*F.graph_with_import(foreign_snapshot=True)))
check('run-import-current-vcs-mapped-source-closes', M.N.IM.close_run(*F.graph_with_import(correspondence='vcs')).startswith('run2:'))
check('run-import-declared-build-context-closes', M.N.IM.close_run(*F.graph_with_import(correspondence='vcs', build_identity='build-a', declared_builds=['build-a'])).startswith('run2:'))
for kwargs in ({'foreign_snapshot': True}, {'bad_mapping': True}, {'dirty': True}, {'missing_mapping': True}, {'build_identity': 'build-a'}, {'build_identity': 'build-a', 'declared_builds': ['build-b']}):
    refuses('run-import-invalid-vcs-source-refused.' + str(kwargs), lambda kw=kwargs: M.N.IM.close_run(*F.graph_with_import(correspondence='vcs', **kw)))

# Complete native scope admission has its own typed bound below the discovery cap.
large_markers={f'pkg{i:04}/package.json':{'sha256':'1'*64} for i in range(1025)}
large_discovery=M.N.discover_units(large_markers)
try:
    M.N.unit_scope_descriptor(large_discovery['units'],[])
    check('scope-1025-roots-typed-refusal',False)
except M.N.ScopeRefusal as exc:
    term=M.public_termination(exc.d9,exc.detail,'Select at most1024 workspace roots.',f"{exc.subject['field']}:{exc.subject['count']}>{exc.subject['limit']}")
    check('scope-1025-roots-typed-refusal',term['class']=='request-rejected' and term['errorCode']=='REQUEST.UNSATISFIABLE' and M.W.exit_code(term)==2 and exc.subject=={'field':'workspaceRoots','count':1025,'limit':1024})
check('scope-1024-roots-admitted',len(M.N.unit_scope_descriptor(large_discovery['units'][:1024],[])['scopeDescriptor']['workspaceRoots'])==1024)
# Missing promised retained blobs/objects retain the host failure boundary, never a predicate result.
erun,eobjects,eblobs=F.build(resolved=True,has_match=True)
for loss_lane,lost_objects,lost_blobs in (('blobs',eobjects,{}),('objects',{},eblobs)):
    try:
        M.N.IM.close_run(erun,lost_objects,lost_blobs);check('missing-retained-closure-is-typed-operational-loss-' + loss_lane,False)
    except M.N.IM.EvidenceUnavailable as exc:
        M.W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/StepTermination',exc.termination)
        check('missing-retained-closure-is-typed-operational-loss-' + loss_lane,M.W.exit_code(exc.termination)==4 and exc.termination['domainDetail']['code']=='evidence.missing')

try:
    M.admit_repository_discovery(di,{},[]);check('discovery-inventory-mismatch-public-refusal',False)
except M.DiscoveryInventoryMismatch as exc:
    term=M.public_termination(exc.d9,exc.detail,'Re-admit one consistent repository inventory.')
    check('discovery-inventory-mismatch-public-refusal',term['domainDetail']['code']=='PROJECT.DISCOVERY_INVENTORY_MISMATCH' and M.W.exit_code(term)==2)

# Operational 1024/1025-root path: real security discovery and exported boundaries,
# with one coherent synthetic filesystem/marker inventory, not the standalone native instrument.
dir_observation = {'kind':'dir','uid':1000,'mode':'0755','dev':1}
file_observation = {'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':2}
for unit_count in (1024, 1025):
    observed_fs = {'/': dict(dir_observation,uid=0), '/review-home': dict(dir_observation),
                   '/review-home/project': dict(dir_observation,vcs=True)}
    marker_inventory = {}
    for i in range(unit_count):
        rel = 'u' + str(i).zfill(4)
        observed_fs['/review-home/project/' + rel] = dict(dir_observation)
        observed_fs['/review-home/project/' + rel + '/package.json'] = dict(file_observation)
        marker_inventory[rel + '/package.json'] = {'sha256':'a'*64}
    observed_input = {'invokingUid':1000,'accountHome':'/review-home','cwd':'/review-home/project','fs':observed_fs}
    try:
        composed = M.admit_repository_discovery(observed_input, marker_inventory, [])
        check('operational-scope-' + str(unit_count), unit_count == 1024 and len(composed['scope']['scopeDescriptor']['workspaceRoots']) == 1024)
    except M.N.ScopeRefusal as exc:
        term = M.public_termination(exc.d9, exc.detail, 'Select at most1024 workspace roots.',
                                   f"{exc.subject['field']}:{exc.subject['count']}>{exc.subject['limit']}")
        check('operational-scope-' + str(unit_count), unit_count == 1025 and M.W.exit_code(term) == 2
              and term['domainDetail']['subject'] == 'workspaceRoots:1025>1024')
# Host-observation typos are refused at the instrument boundary before a discovery can silently change.
for lane, delta in [('unknown-key', {'config':{}}), ('nonboolean-ci', {'ci':'false'}),
                    ('nonboolean-owner-waiver', {'trustProjectOwner':1}), ('boolean-uid', {'invokingUid':True}),
                    ('invalid-group', {'authorizedGroupIds':[True]})]:
    bad_input = dict(di, **delta)
    try:
        M.S.discovery(bad_input); check('discovery-observation-' + lane, False)
    except M.S.Reject as exc:
        check('discovery-observation-' + lane, str(exc) == 'DISCOVERY_OBSERVATION_SHAPE')
# Blind B M3: two rule orders deliberately differ; hashing never elects an order.
ordered_policy = sub(copy.deepcopy(wf['policyDocs']['basePolicy']))
ra=copy.deepcopy(ordered_policy['rules'][0]);rb=copy.deepcopy(ra)
for rule,rid,op in [(ra,'a.first','exists'),(rb,'b.second','count-at-most')]:
    rule['ruleId']=rid;rule['ruleProgramRef']['ruleStableId']=rid
    rule['emitWhen']={'op':op,'relation':'references','minResolution':'resolved-binding','filters':[]}
    if op=='count-at-most':rule['emitWhen']['n']=3
ordered_policy['rules']=[ra,rb]
M.W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/PolicyDocumentV1',ordered_policy)
M.W.resolve_policy(ordered_policy)
lexical_policy=copy.deepcopy(ordered_policy);lexical_policy['rules'].sort(key=M.C.canonical)
check('blind-policy-object-order-disagrees-with-rule-id-order',lexical_policy['rules']!=ordered_policy['rules'])
check('blind-encoder-preserves-rule-id-order',M.C.parse(M.C.canonical(ordered_policy))['rules']==[ra,rb] and M.W.doc_digest(ordered_policy)!=M.W.doc_digest(lexical_policy))
refuses('blind-policy-canonical-object-order-refused',lambda:M.W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/PolicyDocumentV1',lexical_policy))
refuses('blind-policy-owner-refuses-wrong-order',lambda:M.W.resolve_policy(lexical_policy))
prog={'schemaVersion':1,'policyDigest':M.W.doc_digest(ordered_policy),'rules':[{k:r[k] for k in ('ruleId','ruleProgramRef','emitWhen')} for r in ordered_policy['rules']]}
M.W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/RuleProgramV1',prog)
check('blind-rule-program-same-declared-rule-order',M.W.rule_program_digest(ordered_policy)==hashlib.sha256(M.C.canonical(prog)).hexdigest())
badprog=copy.deepcopy(prog);badprog['rules'].reverse()
refuses('blind-rule-program-wrong-order-refused',lambda:M.W.validate_import_record('workflows/schemas/policy-document.schema.json','#/$defs/RuleProgramV1',badprog))
# Ordered signatures and argv preserve repeated tokens, even though they are unique as calls.
repeated=['(', 'x', ',', 'x', ')']
check('blind-signature-array-preserves-repetitions-and-grammar',M.N.subject_discriminator_projection(repeated,[repeated])==hashlib.sha256(b'["(","x",",","x",")"]').hexdigest())
# Use the directly loaded foundation model; no claimed output golden.
id_spec=importlib.util.spec_from_file_location('blind_regeneration_identity',HERE/'foundation/identity-model.py');id_model=importlib.util.module_from_spec(id_spec);id_spec.loader.exec_module(id_model)
term=id_model.RegenerationMismatch('run2:'+'a'*64).termination
M.W.validate_import_record('workflows/schemas/common.schema.json','#/$defs/StepTermination',term)
check('blind-regeneration-refusal-closed-public-detail',M.W.exit_code(term)==4 and term['domainDetail']['code']=='evidence.regeneration-mismatch')
# Actual Claude's native recipes composed through the host before Plan.
ctx=copy.deepcopy(nf['tsNativeContext']);trees=copy.deepcopy(nf['tsClosureTrees']);u=copy.deepcopy(nf['tsUniverse'])
joined=M.typescript_context_inputs(ctx,trees,u,nf['tsRetainedUniverseInputs'],nf['tsSnapshotInventory'])
check('native-context-host-plan-and-universe-join',joined['nativeContextDigests']==[u['nativeContextId'].removeprefix('sha256:')] and joined['sourceUniverse']==M.N.bind_typescript_universe(u,joined['admission'],ctx,nf['tsRetainedUniverseInputs'],nf['tsSnapshotInventory'])['sourceUniverse'])
for field in ['allowJs','checkJs']:
    bad=copy.deepcopy(u);bad[field]=not bad[field]
    refuses('native-context-host-refuses-overlapping-'+field,lambda bad=bad:M.typescript_context_inputs(ctx,trees,bad,nf['tsRetainedUniverseInputs'],nf['tsSnapshotInventory']))
check('native-context-identical-multiple-unit-use-is-one-plan-member',M.N.plan_native_context_digests([joined['admission'],joined['admission']])==joined['nativeContextDigests'])
check('native-context-omitted-bytes-refuse',M.N.bind_typescript_universe(u,joined['admission'],None)['result']=='REFUSE')
# Additional Codex review: no duplicated option record may contradict another.
for label,mutate in [
    ('module-resolution',lambda c:c.update(moduleResolutionMode=next(x for x in M.N.SCHEMAS['$defs']['TypeScriptModuleResolutionMode']['enum'] if x!=c['moduleResolutionMode']))),
    ('lib-selection',lambda c:c['configProjection']['honoredOptions'].update(lib=['ES2022'])),
    ('lib-order',lambda c:c['toolchain']['libSelection'].reverse()),
    ('component-order',lambda c:c['toolchain']['standardLibraryComponentDigests'].reverse())]:
    bad=copy.deepcopy(ctx);mutate(bad);ad=M.N.admit_native_context('typescript',bad,trees)
    check('native-context-self-agreement-'+label,any(x.startswith('native.native-context-field-mismatch:') for x in ad['refusals']))
    refuses('native-context-refused-options-never-enter-plan-'+label,lambda ad=ad:M.N.plan_native_context_digests([ad]))
# Synthesized options are a second copy of actual effective options, not an unchecked label.
synth={'allowJs':True,'checkJs':False,'module':'node16','moduleResolution':'node16','target':'es2022','strict':False,'skipLibCheck':True,'types':[],'noEmit':True}
sc=copy.deepcopy(ctx);sc['languageMode']='js-synthesized';sc['configProjection']['configGraphPaths']=[];sc['configProjection']['honoredOptions'].update(synth);sc['configProjection']['honoredOptions']['jsx']=None
su=copy.deepcopy(u);su.update(languageMode='js-synthesized',configOrigin='synthesized',synthesizerVersion=1,synthesizedOptions=synth,allowJs=True,jsAdmittedToProgram=True,jsRootFiles=['src/a.js'],programRootFiles=['src/a.js'],tsconfigGraphHash=nf['tsSynthesizedConfigGraphHash'])
sa=M.N.admit_native_context('typescript',sc,trees);su['nativeContextId']=sa['nativeContextId']
check('native-synthesized-options-match-admitted-context',M.typescript_context_inputs(sc,trees,su,nf['tsSynthesizedRetainedUniverseInputs'],nf['tsSnapshotInventory'])['nativeContextDigests']==[sa['planNativeContextDigest']])
badsc=copy.deepcopy(sc);badsc['configProjection']['honoredOptions']['strict']=True;bada=M.N.admit_native_context('typescript',badsc,trees);badsu=copy.deepcopy(su);badsu['nativeContextId']=bada['nativeContextId']
refuses('native-synthesized-option-values-cannot-contradict-context',lambda:M.typescript_context_inputs(badsc,trees,badsu,nf['tsSynthesizedRetainedUniverseInputs'],nf['tsSnapshotInventory']))
# Coverage commitment is the exact scope2 suffix and survives the host/view join.
scope_desc=copy.deepcopy(nf['scopeDescriptor']);payload=copy.deepcopy(nf['coveragePayload'])
coverage=M.N.admit_coverage_result_v3(payload,scope_desc,[])
check('native-coverage-admission-binds-exact-scope-id',coverage['result']=='ADMIT' and coverage['subjectScopeCommitment']=='sha256:'+coverage['scopeId'].removeprefix('scope2:'))
view=copy.deepcopy(nf['coverageView']);view['coverageIds']=[coverage['coverageId']]
check('native-coverage-view-uses-admitted-current-id',M.N.coverage_view_use(view,[coverage])['result']=='ADMIT')
# Actual profile/root refusals flow through registered detail projection and StepTermination validation.
profile_rows=M.C.parse((HERE/'security/public-detail-cases.v1.json').read_bytes())
for name,code in [('standalone-profile','PROFILE_SET.NO_TR_PROFILE_ROLE'),('profile-mismatch','PROFILE_SET.CORE_PIN_MISMATCH'),('envelope','ENVELOPE.SHAPE')]:
    refusal='ROOT.SCHEMA_UNSUPPORTED' if name=='standalone-profile' else 'PAYLOAD-NOT-ADMISSIBLE'
    terms=M.security_public_terminations({'refusal':refusal,'detail':code+':synthetic-reference-observation','d9':M.S.d9(refusal)})
    check('security-new-detail-through-host-'+name,len(terms)==1 and terms[0]['domainDetail']['code']==code and M.W.exit_code(terms[0])==2)
    check('security-registration-is-complete-'+name,not M.S.public_detail(refusal,code)['pendingRegistration'])
check('security-complete-closed-code-set-registered',M.S.SECURITY_PUBLIC_DETAIL_CODES<=details)
# The same common workflow/replay/store path consumes Rust-native evidence too.
rrun, robjects, rblobs = F.build(resolved=True, has_match=True, universe_language='rust')
bind_workflow_policy(rrun, robjects, rblobs, 'rust')
rplan = robjects[rrun['planId']][1]
rspec = F.C.parse(rblobs[rplan['analysisSpecDigest']])
rpolicy = F.C.parse(rblobs[rplan['policyDigest']])
rview = robjects[robjects[rrun['evidenceId']][1]['viewIds'][0]][1]
rfact = robjects[rview['facts'][0]][1]
runiverse = F.M.parse_h_frame(rblobs[rfact['sourceUniverse']], 'native-semantic-universe')
check('rust-workflow-input-request-policy-universe-agree',
      rspec['requestedCapabilities'][0]['languageMode'] == 'rust-cargo' and
      rpolicy['rules'][0]['subjectEnumeration']['universe'] == 'rust' and
      runiverse[0] == 'native.semantic-universe.rust.v2')
ranchor = rfact['anchors'][0]
check('rust-workflow-fact-anchors-real-rust-fixture-source',
      ranchor['path'] == 'src/lib.rs' and rblobs[ranchor['blobDigest']] == b'pub fn root() {}\n')
rderivation = M.validate_workflow_policy_links(rrun, robjects, rblobs)
check('rust-workflow-policy-joins-common-plan-and-proof',
      rderivation['descriptor']['planId'] == rrun['planId'] and rderivation['descriptor']['verdict'] == 'pass')
rstore = M.N.IM.EvidenceStore(); reid = 'exec1_' + 'c' * 32
rrid = rstore.prepare(rrun, robjects, rblobs, reid, replay_workflow_fixture)
check('rust-workflow-policy-through-replay-and-commit',
      rstore.commit(reid) == 'committed' and rrid in rstore.runs)
# Exact Rust source retention loss reaches the closed shared public termination branch.
missing_rust_blobs = dict(rblobs); missing_rust_blobs.pop(ranchor['blobDigest'])
try:
    F.M.close_run(rrun, robjects, missing_rust_blobs)
except F.M.EvidenceUnavailable as exc:
    M.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', exc.termination)
    check('rust-source-loss-is-operational-shared-termination',
          M.W.exit_code(exc.termination) == 4 and exc.termination['domainDetail']['code'] == 'evidence.missing')
else:
    check('rust-source-loss-is-operational-shared-termination', False)
# Actual reference-store refusal -> complete current public projection. Ledger names/lease
# remain explicit trusted observations; this does not simulate destructive authorization.
rstore.pins.add(rrid)
retained_run_before = F.C.canonical(rstore.query(rrid))
refusal_result = rstore.purge(rrid)
named_pin_observation = [{'pinId':'baseline:main','kind':'baseline'}, {'pinId':'repair:42','kind':'repair-prerequisite'}]
check('pinned-store-refusal-preserves-run-and-pins', refusal_result == 'pinned' and rrid in rstore.pins and
      F.C.canonical(rstore.query(rrid)) == retained_run_before and rstore.availability[rrid]['state'] == 'retained')
purge_public = M.W.pinned_purge_refusal('req1_'+'d'*32, rrid, named_pin_observation)
check('pinned-store-to-closed-public-envelope', M.W.validate_pinned_purge_refusal(purge_public) == purge_public and
      purge_public['termination']['domainDetail']['code'] == 'evidence.pinned' and purge_public['exitCode'] == 2)
check('pinned-store-public-output-names-all-observed-pins',
      purge_public['errors'][0]['purgeDisclosure']['activePins'] == named_pin_observation)
check('integration-check-identifiers-unique', len({c['id'] for c in checks}) == len(checks))

# Preserve the bounded subject when projecting native refusals through workflows.
def scope_limit_observation(field, count, prefix):
    """Invoke the real native bounded-selection boundary and project its real typed refusal."""
    try:
        M.N.admit_plan_selection_cardinality({field: [prefix + ('%064x' % i) for i in range(count)]})
    except M.N.ScopeRefusal as exc:
        termination = M.N.scope_refusal_termination(exc)
        detail = termination['domainDetail']
        return detail, {'event': 'rejected', 'errorCode': termination['errorCode'],
                        'detail': detail['code'], 'subject': detail['subject'],
                        'remedy': detail['remedy']}
    raise AssertionError('expected an actual ScopeRefusal for ' + field)

for _field, _count, _prefix in (('semanticClosures', 129, 'closure2:'),
                                ('nativeContextDigests', 129, ''),
                                ('importIds', 257, 'import2:')):
    _detail, _obs = scope_limit_observation(_field, _count, _prefix)
    _term = M.W.terminate(dict(_obs))
    check('native-scope-limit-subject-survives-the-workflow-envelope.' + _field,
          _term['domainDetail'].get('subject') == _detail['subject']
          == _field + ':' + str(_count) + '>' + str(M.N.plan_selection_bound(_field)))
    check('native-scope-limit-public-route-is-unchanged-across-the-seam.' + _field,
          _term['class'] == 'request-rejected'
          and _term['errorCode'] == 'REQUEST.UNSATISFIABLE'
          and _term['domainDetail']['code'] == 'PROJECT.SCOPE_LIMIT'
          and _term['domainDetail']['remedy'] == M.N.SCOPE_LIMIT_REMEDY[_field]
          and M.W.exit_code(_term) == 2)
# The two bounded fields that predate the Plan arrays cross the same seam, so the join is a
# property of the shared law rather than of the three new fields.
for _field, _refuse in (('requestedCapabilities',
                         lambda: M.N.admit_requested_capability_cardinality(
                             [{'capabilityId': 'references', 'languageMode': 'ts-tsconfig',
                               'workspaceRoot': 'r%05d' % i, 'required': True}
                              for i in range(M.N.requested_capability_bound() + 1)])),
                        ('workspaceRoots',
                         lambda: M.N.unit_scope_descriptor(
                             [{'rootPath': 'r%05d' % i, 'languageMode': 'ts-tsconfig',
                               'languageFamily': 'tsjs'} for i in range(1025)], []))):
    try:
        _refuse()
        _observed = None
    except M.N.ScopeRefusal as _exc:
        _d = M.N.scope_refusal_termination(_exc)['domainDetail']
        _observed = M.W.terminate({'event': 'rejected', 'errorCode': 'REQUEST.UNSATISFIABLE',
                                   'detail': _d['code'], 'subject': _d['subject'],
                                   'remedy': _d['remedy']})['domainDetail'].get('subject')
    check('inherited-scope-limit-subject-survives-the-workflow-envelope.' + _field,
          _observed == _field + ':1025>1024')

# Synthetic trusted invocation and earlier result from the existing fixture, not an admitted Run.
def _scope_expand(value):
    if isinstance(value, str) and value.startswith('$'):
        return wf['constants'][value[1:]]
    if isinstance(value, list):
        return [_scope_expand(x) for x in value]
    if isinstance(value, dict):
        return {k: _scope_expand(v) for k, v in value.items()}
    return value
_scope_case = _scope_expand(copy.deepcopy(wf['invocationCases'][0]))
_scope_step = _scope_case['steps'][0]
_scope_record = {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 1,
    'requestId': wf['constants']['REQ'], 'projectId': wf['constants']['PRJ'],
    'workflow': {'kind': 'builtin', 'name': 'analyze'}, 'mode': _scope_case['mode'],
    'orderedSteps': [{'stepId': i, 'kind': _scope_step['kind'],
        'requirement': _scope_step['requirement'], 'dependsOn': [] if i == 0 else [0],
        'dependencyGate': 'completed', 'retryPolicy': _scope_step['retry'],
        'params': _scope_step['params']} for i in range(2)]}
for _field, _count, _prefix in (('semanticClosures', 129, 'closure2:'),
                               ('nativeContextDigests', 129, ''), ('importIds', 257, 'import2:')):
    _detail, _obs = scope_limit_observation(_field, _count, _prefix)
    _inv, _exit = M.W.run_invocation(copy.deepcopy(_scope_record),
        {'0': copy.deepcopy(_scope_case['script']['0']), '1': [_obs]})
    _first, _refused = _inv['stepResults']
    check('scope-refusal-invocation-keeps-exact-step-and-aggregate-subject.' + _field,
          _refused['termination']['domainDetail'] == _detail
          and _inv['termination']['domainDetail'] == _detail and _exit == 2)
    check('scope-refusal-invocation-preserves-earlier-result.' + _field,
          _first['result'] == _scope_case['script']['0'][0]['result'])
    check('scope-refusal-invocation-mints-no-refused-result-or-derivation.' + _field,
          _refused['outcome'] == 'rejected' and 'result' not in _refused
          and all('derivation' not in a for a in _refused['attempts']))
    M.W.validate_import_record('workflows/schemas/invocation-record.schema.json', '', _inv)
    check('scope-refusal-invocation-record-is-schema-admitted.' + _field, True)

parser = argparse.ArgumentParser(); parser.add_argument('--report', required=True); args = parser.parse_args()
report = {'standing': 'PROPOSED, Codex-authored, independent Claude review pending', 'productQualification': False,
          'syntheticTcbInputs': True, 'checks': checks, 'passed': sum(c['passed'] for c in checks),
          'failed': [c['id'] for c in checks if not c['passed']]}
Path(args.report).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'checks'}))
raise SystemExit(bool(report['failed']))
