"""Proposed trusted-host composition; pure reference evidence, no repository execution.

Security still receives explicit synthetic TCB observations (verified signatures,
sealed inventories, consent, OS effects and live boundaries). Callers do not supply
an admission result: this module validates and invokes the actual security model.
These Codex-authored joins require fresh independent Claude review.
"""
import hashlib
import json
import importlib.util
from pathlib import Path
from jsonschema import ValidationError

HERE = Path(__file__).resolve().parent

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, HERE / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

C = load('integration_canonical', 'foundation/canonical.py')
S = load('integration_security', 'security/security_lifecycle_model_v1.py')
N = load('integration_native', 'native/native_evidence_model.v2.py')
W = load('integration_workflow', 'workflows/workflows_model.v1.py')

class Refusal(ValueError):
    pass

class DiscoveryInventoryMismatch(Refusal):
    detail = 'PROJECT.DISCOVERY_INVENTORY_MISMATCH'
    d9 = {'class':'request-rejected','code':'REQUEST.PRECONDITION_FAILED','exit':2}

def security_public_terminations(outcome, refusal_key=None):
    """Project actual security decisions through the one closed host termination boundary."""
    return [public_termination(row['d9'], row['code'],
                row.get('remedy', 'Inspect the named admitted input or current trust state.'), row['subject'])
            for row in S.public_details(outcome, refusal_key)]

def typescript_context_inputs(context, retained_closures, universe, retained_inputs, snapshot_inventory):
    """Reference host join before Plan; retained closures are already admitted TCB inputs."""
    admission = N.admit_native_context('typescript', context, retained_closures)
    binding = N.bind_typescript_universe(universe, admission, context, retained_inputs, snapshot_inventory)
    if binding['result'] != 'ADMIT':
        raise Refusal('native context/universe admission: ' + ','.join(binding['refusals']))
    return {'nativeContextDigests':N.plan_native_context_digests([admission]),
            'sourceUniverse':binding['sourceUniverse'], 'admission':admission}


def public_termination(d9, detail_code, remedy, subject=None):
    """Host projection of an admitted unit outcome; no renderer owns classification."""
    registry = json.loads((HERE / 'public-detail-registry.v1.json').read_text())
    aliases = {r['internalCode']: r['publicCode'] for r in registry['internalAliases']}
    detail_code = aliases.get(detail_code, detail_code)
    if detail_code not in {r['code'] for r in registry['records']}:
        raise Refusal('unregistered public domain detail')
    cls, code = d9['class'], d9.get('code')
    term = {'class': cls, 'domainDetail': {'code': detail_code, 'remedy': remedy}}
    if subject is not None:
        term['domainDetail']['subject'] = subject
    if cls in ('request-rejected', 'operational-failed'):
        term['errorCode'] = code
        if cls == 'operational-failed':
            causes = [cause for cause, error in W.FAULT_TO_ERROR.items() if error == code]
            if len(causes) != 1:
                raise Refusal('unit outcome has no unique host fault cause')
            term['faultCause'] = causes[0]
    elif cls == 'indeterminate':
        term['reasonCodes'] = [code]
    elif cls != 'success':
        raise Refusal('unit outcome requires a different closed termination branch')
    W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', term)
    if d9.get('exit', d9.get('exitCode')) != W.exit_code(term):
        raise Refusal('unit class and exit disagree')
    return term

def owner_rows(owners):
    rows = [{k: o[k] for k in ('ownerKey', 'source', 'ownerFileManifestSha256')} for o in owners]
    rows.sort(key=lambda o: o['ownerKey'].encode('utf-8'))
    if len({o['ownerKey'] for o in rows}) != len(rows):
        raise Refusal('duplicate preparation owner')
    return rows

def owner_digest(owners):
    return hashlib.sha256(C.canonical(owner_rows(owners))).hexdigest()

def grant_ref(grant):
    return 'security.repo-execution-grant.v2:' + C.identity('security.repo-execution-grant.v2', grant)

def grant_set_ref(grants):
    refs = sorted(grant_ref(g) for g in grants)
    if len(refs) != len(set(refs)):
        raise Refusal('duplicate grant reference')
    return 'security.repo-execution-grants.v2:' + C.identity('security.repo-execution-grants.v2', {'schemaVersion': 2, 'grantRefs': refs})

def admit_grant(grant, context):
    # Complete shape admission precedes any nested access in the decision model.
    try:
        S.validate_input('RepoExecutionGrantV2', grant)
    except (ValidationError, S._C.AdmissionError) as exc:
        raise Refusal('GRANT.SHAPE') from exc
    digest = owner_digest(grant['owners'])
    if grant['owners'] != owner_rows(grant['owners']) or digest != grant['ownerSourceDigest'] or digest != context.get('ownerSourceDigest'):
        raise Refusal('owner-set preimage does not join the grant and host context')
    admitted = S.admit_repo_execution_grant(grant, context)
    if admitted['result'] != 'ADMIT':
        raise Refusal('; '.join(admitted['refusals']))
    return admitted

def test_grant_projection(grant, context):
    admitted = admit_grant(grant, context)
    if grant['executionClass'] != 'test-runner':
        raise Refusal('test-runner grant required')
    runner = grant['runner']
    program = runner['member'] if runner['kind'] == 'snapshot-member' else grant['toolClosureId'] + '#' + runner['member']
    return {
        'result': admitted['result'], 'principalClass': admitted['principalClass'],
        'executionClass': grant['executionClass'], 'projectId': grant['projectId'],
        'snapshotId': grant['snapshotId'], 'argvDigest': grant['argvDigest'],
        'programs': [program], 'expiry': grant['expiry'], 'inherited': grant['inherited'],
        'platformId': grant['platformId'], 'toolchainClosureId': grant['toolClosureId'],
        'effects': admitted['effects'], 'securityGrantRef': grant_ref(grant),
        'consentSource': 'pre-existing-policy' if grant['authorization']['mode'] == 'policy-record' else 'interactive-consent',
    }

def repair_authorization_projection(authorization, context, plan, authorization_ref):
    """Admit actual security bytes before supplying the workflow's trusted projection."""
    S.validate_input('RepairApplyAuthorizationV1', authorization)
    W.validate_import_record('workflows/schemas/repair.schema.json', '#/$defs/RepairPlanV1', plan)
    descriptor = plan['descriptor']
    if plan['repairPlanId'] != W.wid('repairplan2', 'workflow.repair-plan', descriptor):
        raise Refusal('repair plan content identity mismatch')
    expected_ref = 'security.repair-apply-authorization.v1:' + C.identity('security.repair-apply-authorization.v1', authorization)
    if authorization_ref != expected_ref:
        raise Refusal('repair authorization reference mismatch')
    bound = dict(context, projectId=descriptor['projectId'], repairPlanId=plan['repairPlanId'],
                 baseSnapshotId=descriptor['snapshotId'], recipeClosureId=descriptor['recipe']['closureId'])
    admitted = S.admit_repair_authorization(authorization, bound)
    if admitted['result'] != 'ADMIT':
        raise Refusal('; '.join(admitted['refusals']))
    return {'projectId': descriptor['projectId'], 'repairPlanId': plan['repairPlanId'],
            'snapshotId': descriptor['snapshotId'], 'live': True,
            'securityAuthorizationRef': expected_ref, 'ci': bound['ci'],
            'consentSource': 'policy' if authorization['consent']['mode'] == 'policy-record' else 'interactive'}

def admit_preparation(auth, grants, contexts, platform_id, policy_records, linker_in_closure):
    N.validate_native('AuthorizedExecutionV2', auth)
    if len(grants) != len(contexts) or len(grants) != len(auth['owners']):
        raise Refusal('one class-specific grant per preparation owner is required')
    if grant_set_ref(grants) != auth['authorizationRef']:
        raise Refusal('preparation authorization reference does not bind the grant set')
    expected = {o['ownerKey']: o for o in auth['owners']}
    if len(expected) != len(auth['owners']):
        raise Refusal('duplicate preparation owner')
    seen = set()
    for grant, ctx in zip(grants, contexts):
        admit_grant(grant, ctx)
        if len(grant['owners']) != 1:
            raise Refusal('preparation grants are scoped to one owner')
        row = grant['owners'][0]
        owner = expected.get(row['ownerKey'])
        if owner is None or row != owner_rows([owner])[0] or row['ownerKey'] in seen:
            raise Refusal('foreign, changed or repeated preparation owner')
        seen.add(row['ownerKey'])
        if grant['executionClass'] != owner['kind']:
            raise Refusal('preparation owner execution class mismatch')
        for key in ('projectId', 'snapshotId'):
            if grant[key] != auth[key]:
                raise Refusal('preparation ' + key + ' mismatch')
        if grant['toolClosureId'] != auth['toolClosure']['closureId'] or grant['platformId'] != platform_id:
            raise Refusal('preparation tool closure or platform mismatch')
        if grant['dependencySourceSetId'] != auth['dependencySourceSetId'].removeprefix('sha256:'):
            raise Refusal('preparation dependency closure mismatch')
        if grant['authorization'] != auth['authorization'] or grant['effects'] != {k: v['enforcement'] for k, v in auth['effects'].items()}:
            raise Refusal('preparation consent or effect disclosure mismatch')
    preflight = N.authorized_execution_admit(auth, policy_records, linker_in_closure)
    if not preflight['admitted']:
        raise Refusal('; '.join(preflight['refusals']))
    # Native preflight enumerates owners in owner-key order; Plan principals are
    # a semantic set ordered by canonical bytes, as the foundation requires.
    semantic_projection = dict(preflight['semanticGrantProjection'])
    semantic_projection['principals'] = S.semantic_projection_for_grants(grants)
    if {C.canonical(p) for p in semantic_projection['principals']} != {C.canonical(p) for p in preflight['semanticGrantProjection']['principals']}:
        raise Refusal('native and admitted security principal projections disagree')
    return {'admitted': True, 'securityGrantRefs': sorted(grant_ref(g) for g in grants),
            'semanticGrantProjection': semantic_projection,
            'disclosure': preflight['disclosure'], 'executed': False}

def validate_workflow_policy_links(run, objects, blobs):
    """Extra workflow compiler/retained-policy joins before foundation replay/seal.
    Native payload admission and the actual evaluator remain separate trusted code.
    """
    plan = objects[run['planId']][1]
    seal = objects[run['evaluationSealId']][1]
    proof = objects[seal['proofBundleId']][1]
    policy_bytes = blobs[plan['policyDigest']]
    policy = C.parse(policy_bytes)
    W.validate_import_record('workflows/schemas/policy-document.schema.json', '#/$defs/PolicyDocumentV1', policy)
    if W.doc_digest(policy) != plan['policyDigest'] or C.canonical(policy) != policy_bytes:
        raise Refusal('retained policy bytes do not join the Plan')
    expected = {'schemaVersion': 1, 'policyDigest': plan['policyDigest'],
                'rules': [{k: r[k] for k in ('ruleId', 'ruleProgramRef', 'emitWhen')} for r in policy['rules']]}
    W.validate_import_record('workflows/schemas/policy-document.schema.json', '#/$defs/RuleProgramV1', expected)
    if proof['ruleProgramDigest'] != W.rule_program_digest(policy) or blobs[proof['ruleProgramDigest']] != C.canonical(expected):
        raise Refusal('compiled rule program does not join the admitted policy')
    waiver = C.parse(blobs[plan['waiverDigest']])
    W.validate_import_record('workflows/schemas/policy-document.schema.json', '#/$defs/WaiverSetV1', waiver)
    if W.doc_digest(waiver) != plan['waiverDigest']:
        raise Refusal('resolved waiver preimage mismatch')
    derivation = {'schemaVersion': 2, 'planId': run['planId'], 'proofBundleId': seal['proofBundleId'],
                  'policyDigest': plan['policyDigest'], 'waiverDigest': plan['waiverDigest'], 'verdict': proof['verdict']}
    return {'policyDerivationId': N.IM.identifier('policy-derivation', derivation), 'descriptor': derivation}


def core_transition_scope(intent, namespace_registry):
    """Trusted host projection after exact intent admission; namespace registry is observed under the fence.
    Same-schema update/repair retain the selected store; rollback selects the rollback store.
    Closure/profile/generation admission is still required by the lifecycle before mutation.
    """
    W.validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/CoreTransitionIntentV1', intent)
    S.validate_input('InstallationTransitionIntentV1', intent)
    reasons = S.admit_transition_intent(intent)
    if reasons:
        raise Refusal('; '.join(reasons))
    return S.core_transition_affected_namespaces(intent, namespace_registry)


def admit_repository_discovery(discovery_input, markers, files, ignore_paths=()):
    """Actual security discovery -> admitted boundary inventory -> native units/membership/scope.
    fs/marker metadata/file names are synthetic trusted observations of one inventory.
    Returned sourceCaptureCandidates still require per-file custody/handle/hash admission.
    No caller-authored boundary list or alternate explicit roots enter this join.
    """
    discovery = S.discovery(discovery_input)
    if discovery['status'] != 'ACCEPT':
        raise Refusal('security discovery refused')
    provenance = discovery['provenance']; S.validate_input('DiscoveryProvenanceV1', provenance)
    root = provenance['selectedRoot']
    observed = {p[len(root) + 1:] for p, row in discovery_input['fs'].items()
                if p.startswith(root + '/') and row['kind'] == 'file'}
    expected_markers = {p for p in observed if p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}
    if set(markers) != expected_markers or not set(files) <= observed:
        raise DiscoveryInventoryMismatch('native inventory differs from security discovery observations')
    boundaries = S.DD.boundary_inventory_from_provenance(provenance)
    explicit = None if provenance['unitSource'] == 'automatic' else [S.DD.spell_root(S.DD.relative_locator(root, u['path'])) for u in provenance['units']]
    native = N.discover_units(markers, explicit, boundaries)
    if native['refused'] is not None:
        if native['refused']['detail'] == 'native.boundary-inventory-mismatch':
            raise DiscoveryInventoryMismatch('admitted boundary inventory differs from native discovery')
        raise Refusal(native['refused']['detail'])
    membership = N.assign_membership(native['units'], files, boundaries)
    scope = N.unit_scope_descriptor(native['units'], list(ignore_paths), None, native['prunedTrees'], boundaries)
    outside = set(membership['outsideBoundaryFiles'])
    return {'discovery': discovery, 'boundaries': boundaries, 'native': native,
            'membership': membership, 'scope': scope,
            'sourceCaptureCandidates': sorted(set(files) - outside, key=lambda p: p.encode())}


def recovery_authorization_projection(authorization, context, plan, journal, authorization_ref, intent):
    """Host binds retained bytes read under the lease to the fresh recovery invocation.
    context is a trusted observation as documented by S10.2, never request parameters.
    """
    S.validate_input('RepairRecoveryAuthorizationV1', authorization)
    W.validate_import_record('workflows/schemas/repair.schema.json', '#/$defs/RepairPlanV1', plan)
    W.validate_import_record('workflows/schemas/repair.schema.json', '#/$defs/RepairApplyJournalV1', journal)
    W.validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/RepairRecoveryIntentV1', intent)
    descriptor = plan['descriptor']
    if descriptor['projectId'] != context['projectId'] or plan['repairPlanId'] != W.wid('repairplan2', 'workflow.repair-plan', descriptor):
        raise Refusal('recovery project or plan identity mismatch')
    expected_ref = S.RECOVERY_AUTHZ_DOMAIN + ':' + C.identity(S.RECOVERY_AUTHZ_DOMAIN, authorization)
    journal_ref = S.repair_journal_identity(journal)
    if authorization_ref != expected_ref or intent != {
        'schemaVersion': 1, 'kind': 'repair-recover', 'journalRef': journal_ref,
        'repairPlanId': plan['repairPlanId'], 'recoveryAction': authorization['recoveryAction'],
        'authorizationRef': expected_ref}:
        raise Refusal('recovery intent or authorization reference mismatch')
    bound = dict(context, repairPlanId=plan['repairPlanId'], baseSnapshotId=descriptor['snapshotId'],
                 recipeClosureId=descriptor['recipe']['closureId'], journal=journal)
    admitted = S.admit_recovery_authorization(authorization, bound)
    if admitted['result'] != 'ADMIT':
        raise Refusal('; '.join(admitted['refusals']))
    return {'result': 'ADMIT', 'projectId': descriptor['projectId'], 'repairPlanId': plan['repairPlanId'],
            'baseSnapshotId': descriptor['snapshotId'], 'originalRequestId': journal['requestId'],
            'journalRef': admitted['journalRef'], 'journalStateDigest': admitted['journalStateDigest'],
            'recoveryAction': admitted['action'], 'securityRecoveryAuthorizationRef': expected_ref}


def admit_installation_transition(intent, journal, context):
    """Complete intent -> journal admission; real fence/lease/trust observations remain host TCB.
    The namespace registry and current generations are read under the installation fence.
    """
    core_transition_scope(intent, context['namespaceRegistry'])
    S.validate_input('InstallationTransitionJournalV1', journal)
    bound = dict(context, intent=intent, intentDigest=S.transition_intent_digest(intent))
    admitted = S.admit_transition_journal(journal, bound)
    if admitted['result'] != 'ADMIT':
        raise Refusal('; '.join(admitted['refusals']))
    return admitted


def recover_installation_transition(journal, journal_ref, context):
    """The retained state bytes must match their durable full reference before recovery.
    Each durable state revision has its own reference; no caller nominates accepted bytes.
    """
    S.validate_input('InstallationTransitionJournalV1', journal)
    expected = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, journal)
    if expected != journal_ref:
        raise Refusal('installation journal content identity mismatch')
    intent = {'schemaVersion': 1, **{k: journal[k] for k in S.INTENT_BOUND_FIELDS}}
    scope = core_transition_scope(intent, journal['registry'])
    if journal['intentDigest'] != S.transition_intent_digest(intent) or journal['affects'] != scope['affects'] or journal['leaseSet'] != scope['namespaces']:
        raise Refusal('installation journal intent or scope mismatch')
    return S.recover_transition_journal(journal, context)


def installation_journal_history(intent, journals, recovery_start_ref=None):
    """Validate durable revisions before attaching operational references to an Attempt.
    Journals are host-read records from the fenced installation location, not request input.
    The initial admission (including actual locks) has already succeeded.
    """
    if not journals or len(journals) > 64:
        raise Refusal('installation journal history bound')
    references = []
    allowed = {'LEASED': {'PREPARING', 'ABORTED'}, 'PREPARING': {'PREPARED', 'ABORTED'},
               'PREPARED': {'COMMITTED', 'ABORTED'}, 'COMMITTED': {'DONE'}, 'DONE': set(), 'ABORTED': set()}
    first = None; previous = None
    for journal in journals:
        S.validate_input('InstallationTransitionJournalV1', journal)
        current = {k:v for k,v in journal.items() if k != 'state'}
        if first is None:
            first = current
            if recovery_start_ref is None:
                if journal['state'] != 'LEASED':
                    raise Refusal('installation journal history must start LEASED')
            else:
                observed_ref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN,journal)
                if recovery_start_ref != observed_ref:
                    raise Refusal('recovery history does not begin with the observed durable revision')
        elif current != first or journal['state'] not in allowed[previous]:
            raise Refusal('installation journal immutable fields or transition mismatch')
        if journal['intentDigest'] != S.transition_intent_digest(intent) or any(journal[k] != intent[k] for k in S.INTENT_BOUND_FIELDS):
            raise Refusal('installation journal differs from mutation intent')
        scope = core_transition_scope(intent, journal['registry'])
        if journal['leaseSet'] != scope['namespaces'] or journal['affects'] != scope['affects'] or journal['registryDigest'] != S.registry_digest(journal['registry']):
            raise Refusal('installation journal scope or registry mismatch')
        references.append(S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN,journal))
        previous = journal['state']
    return references


def installation_recovery_attempt(intent, journal, journal_ref, context, execution_id):
    """Trusted host recovery step before ordinary project admission, not a request endpoint.
    The journal/ref/context are observed under the installation fence. Recovery never
    re-executes the original update recipe or rewrites the earlier abandoned Attempt.
    """
    decision = recover_installation_transition(journal,journal_ref,context)
    journals = [journal]
    if decision['journalStateAfter'] == 'DONE' and journal['state'] != 'DONE':
        if journal['state'] != 'COMMITTED':
            journals.append(dict(journal,state='COMMITTED'))
        journals.append(dict(journal,state='DONE'))
    elif decision['action'] == 'ABORT':
        journals.append(dict(journal,state='ABORTED'))
    references = installation_journal_history(intent,journals,journal_ref)
    attempt = {'executionId':execution_id,'outcome':'completed' if decision['action'] in ('RESUME-COMMIT','ABORT','RELEASE-ONLY') else 'failed',
               'installationRecoveryStartRef':journal_ref,'installationJournalRefs':references}
    W.validate_import_record('workflows/schemas/invocation-record.schema.json','#/$defs/Attempt',attempt)
    return {'decision':decision,'attempt':attempt,'journals':journals}
