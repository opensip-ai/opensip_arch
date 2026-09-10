"""Workflows-and-surfaces reference model (design evidence, not a host runtime).

Implements the normative semantics of docs/v2/contracts/product-v1/workflows-and-surfaces.md
over synthetic, trusted inputs. Every H-identity uses foundation/canonical.py (exact typed
admission and the joint H(domain, descriptor) recipe); every auxiliary digest is a raw SHA-256
of canonical bytes exactly as identity-and-evidence §2 prescribes. Nothing here executes a
provider, a repository, a renderer or a filesystem; journals, trees and stores are in-memory dicts.

Typed TCB observation boundaries (every one is a trusted model INPUT, never a measurement):
  trust map          {closureId: 'admitted'|'revoked'} - the security unit's current admitted closure set
  grant record       an already-admitted RepoExecutionGrantV2 projection; the security model is not re-run
  truth table        the security owner's per-platform effect table (S10)
  host closures      presence/trust/protocol/platform of pivot closures on the comparing host
  pivot presence     E0..E4 presence per fingerprint, supplied by the case, not computed by detectors
  live tree          an in-memory {LogicalPath: bytes} dict standing in for O_NOFOLLOW custody reads
  native closed-world / evidence origin - the evidence Run's own native ClosedWorldV2 (all seven members),
                        read here and not derived; the repair DESCRIPTOR carries only its five-field projection
SYNTHETIC fixture adapters (never production recipes, never presented as admitted proof):
  synthetic_execution_id      fixture adapter only; production uses the foundation fresh CSPRNG operational-ID recipe
  fixture_tree_snapshot_id    snapshot2 with ZERO config/scope/vcs digests; a fixture adapter only
  SYNTHETIC_VERIFY_*          placeholder plan/evidence/seal ids inside repair_verify results
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'foundation'))
import canonical  # noqa: E402

# ----------------------------------------------------------------------------- identities

def wid(prefix, domain, descriptor):
    return prefix + ':' + canonical.identity(domain, descriptor)

def raw_sha(b):
    return hashlib.sha256(b).hexdigest()

def payload_digest(payload):
    return raw_sha(canonical.canonical(payload))

def doc_digest(doc):
    """Auxiliary raw digest: SHA-256 of the canonical bytes of a closed workflow document
    (PolicyDocumentV1 -> plan.policyDigest; resolved WaiverSetV1 -> plan.waiverDigest; ScopeDocumentV1;
    SourceCorrespondence; BuildIdentityV1; ImportScopeDescriptor; ImportObservationV1; SourceMappingV1).
    The bytes are the retained blob. This is NOT an H(domain) identity."""
    return raw_sha(canonical.canonical(doc))

def rule_program_digest(policy):
    """proof.ruleProgramDigest: raw SHA-256 of canonical RuleProgramV1 = the evaluator's compiled predicate
    program {schemaVersion:1, policyDigest, rules:[{ruleId, ruleProgramRef, emitWhen}]}; retained blob."""
    prog = {'schemaVersion': 1, 'policyDigest': doc_digest(policy), 'rules': [{'ruleId': r['ruleId'], 'ruleProgramRef': r['ruleProgramRef'], 'emitWhen': r['emitWhen']} for r in policy['rules']]}
    return doc_digest(prog)

EXIT = {'success': 0, 'policy-failed': 1, 'request-rejected': 2, 'indeterminate': 3, 'operational-failed': 4, 'interrupted': 130}
AGGREGATE_ORDER = ['operational-failed', 'request-rejected', 'policy-failed', 'indeterminate', 'success']
FAULT_TO_ERROR = {'host-io': 'HOST.IO_FAILURE', 'ledger-busy': 'LEDGER.BUSY_TIMEOUT', 'ledger-corrupt': 'LEDGER.CORRUPT', 'cas-link': 'CAS.LINK_FAILED',
                  'provider-protocol': 'PROVIDER.PROTOCOL_VIOLATION', 'durability-commit': 'DURABILITY.COMMIT_FAILED', 'delivery-required': 'DELIVERY.REQUIRED_FAILED',
                  'output-serialization': 'OUTPUT.SERIALIZATION_FAILED', 'extension-install-io': 'EXTENSION.INSTALL_IO_FAILED', 'serve-protocol': 'SERVE.PROTOCOL_FAULT',
                  # Successor member, narrow. SYSTEM.OUTCOME.ILLEGAL_STATE was already in the closed error
                  # vocabulary with no cause mapping to it, so the host-INVARIANT subtype specifically had no
                  # representable operational-failed termination (that class requires both an errorCode and a
                  # non-none faultCause). Other host-fault causes - host-io, ledger-corrupt, provider-protocol -
                  # already existed and were always representable. No new error code, class or exit code is
                  # added; faultCause does grow by this one member.
                  'host-invariant': 'SYSTEM.OUTCOME.ILLEGAL_STATE'}
RETRYABLE_KINDS = {'analysis', 'verify', 'query', 'render', 'export-delivery', 'doctor'}
NEVER_RETRY_KINDS = {'mutation', 'import', 'repair-apply', 'test-execution', 'repair-preview', 'comparison', 'native-preparation'}
TERMINAL_GATE_KINDS = {'render', 'export-delivery'}
MAX_STEPS = 64
MAX_ATTEMPTS = 3

class Refusal(Exception):
    def __init__(self, error_code, detail=None, remedy='see contract', subject=None):
        super().__init__(error_code)
        self.error_code, self.detail, self.remedy, self.subject = error_code, detail, remedy, subject
    def termination(self):
        t = {'class': 'request-rejected', 'errorCode': self.error_code}
        if self.detail:
            t['domainDetail'] = {'code': self.detail, 'remedy': self.remedy}
            if self.subject:
                t['domainDetail']['subject'] = self.subject
        return t

# ----------------------------------------------------------------------------- generic mutation replay scope

def mutation_replay_scope(request_id, step_id, project_id, operation):
    scope = {'schemaVersion': 1, 'requestId': request_id, 'stepId': step_id,
             'projectId': project_id, 'operation': operation}
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationReplayScopeV1', scope)
    return scope

def mutation_replay_key(scope):
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationReplayScopeV1', scope)
    return canonical.identity('workflow.mutation-intent', scope)

def admit_mutation_replay_key(params, scope):
    """Scope comes from the retained host invocation; never caller-selected receipt lookup input.
    This pure join does not admit the effect, authorize it, or implement a mutation ledger.
    """
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationParams', params)
    key = mutation_replay_key(scope)
    if params['mutationClass'] != scope['operation'] or params['idempotencyKey'] != key:
        raise canonical.AdmissionError('MUTATION_REPLAY_SCOPE_JOIN')
    return key

# ----------------------------------------------------------------------------- evidence retention projection

PINNED_PURGE_CONSEQUENCES = ['named-pins-revoked', 'dependent-evidence-replay-unavailable', 'sealed-history-retained']

def pinned_purge_refusal(request_id, run_id, active_pins):
    """Project an actual pinned store refusal using the complete host-observed pin inventory.

    Pure public projection only: no pin discovery, lease, consent, revocation or GC occurs here.
    The authenticated host supplies all current named pins after the store refuses; neither this
    record nor a caller's --revoke-pins flag establishes destructive lifecycle authorization.
    """
    disclosure = {'runId': run_id, 'activePins': sorted(active_pins, key=lambda p: p['pinId'].encode('utf-8')),
                  'consequences': list(PINNED_PURGE_CONSEQUENCES)}
    validate_import_record('workflows/schemas/common.schema.json', '#/$defs/PinnedPurgeDisclosure', disclosure)
    detail = {'code': 'evidence.pinned', 'subject': run_id,
              'remedy': 'Purge refused. Retain the evidence, release the named pins, or explicitly authorize their revocation after reviewing these consequences.',
              'purgeDisclosure': disclosure}
    term = {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED', 'domainDetail': detail}
    envelope = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 2, 'kind': 'failure',
                'requestId': request_id, 'termination': term, 'exitCode': 2, 'errors': [detail]}
    validate_pinned_purge_refusal(envelope)
    return envelope

def validate_pinned_purge_refusal(envelope):
    """Closed schema plus the cross-field joins a JSON schema cannot express."""
    validate_import_record('workflows/schemas/command-envelope.schema.json', '', envelope)
    term = envelope['termination']
    detail = term.get('domainDetail', {})
    if (envelope['kind'] != 'failure' or envelope['exitCode'] != 2 or
            detail.get('code') != 'evidence.pinned' or
            detail.get('subject') != detail.get('purgeDisclosure', {}).get('runId') or
            not canonical.equal_typed(envelope.get('errors'), [detail])):
        raise canonical.AdmissionError('PINNED_PURGE_PROJECTION_JOIN')
    return envelope

# ----------------------------------------------------------------------------- D9 terminations

def terminate(obs):
    """Observation → StepTermination. obs = {'event': ..., ...}. Only lawful existing D9 codes."""
    e = obs['event']
    detail = obs.get('detail')
    def dd(t, remedy='see contract'):
        if detail:
            t['domainDetail'] = {'code': detail, 'remedy': obs.get('remedy', remedy)}
        return t
    if e == 'completed-analysis':
        v = obs['verdict']
        if v == 'fail':
            return {'class': 'policy-failed', 'runId': obs['runId']} if obs.get('runId') else {'class': 'policy-failed', 'authority': 'ephemeral'}
        if v == 'indeterminate':
            return dd({'class': 'indeterminate', 'reasonCodes': obs.get('reasonCodes', ['VERDICT.INDETERMINATE']), **({'runId': obs['runId']} if obs.get('runId') else {})})
        return {'class': 'success', **({'runId': obs['runId']} if obs.get('runId') else {})}
    if e == 'provider-unavailable':
        return dd({'class': 'indeterminate', 'reasonCodes': ['COVERAGE.PROVIDER_UNAVAILABLE']})
    if e == 'baseline-unsupported':
        return dd({'class': 'indeterminate', 'reasonCodes': ['BASELINE.RECIPE_UNSUPPORTED']})
    if e == 'query-completeness-unmet':
        return dd({'class': 'indeterminate', 'reasonCodes': ['QUERY.COMPLETENESS_UNMET']})
    if e == 'operational-fault':
        cause = obs['faultCause']
        t = {'class': 'operational-failed', 'errorCode': FAULT_TO_ERROR[cause], 'faultCause': cause}
        if obs.get('runId'):
            t['runId'] = obs['runId']
        return dd(t)
    if e == 'rejected':
        return dd({'class': 'request-rejected', 'errorCode': obs['errorCode']})
    if e == 'interrupted':
        t = {'class': 'interrupted', 'signal': obs['signal']}
        if obs.get('runId'):
            t['runId'] = obs['runId']
        return t
    if e == 'doctor-report':
        if not obs['reportProduced']:
            return {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io'}
        t = {'class': 'success'}
        if obs.get('defectsFound', 0) > 0:
            t['domainDetail'] = {'code': 'DOCTOR.DEFECTS_FOUND', 'remedy': 'inspect doctor.defects; exit 0 means the report was produced'}
        return t
    if e == 'query-success':
        return dd({'class': 'success'})
    if e == 'mutation-completed':
        return dd({'class': 'success'})
    if e == 'comparison-result':
        return comparison_termination(obs['result'])
    raise ValueError('unknown observation ' + e)

def comparison_termination(res):
    """ComparisonStepResult -> StepTermination. Derived from the descriptor verdict; never defaults to success."""
    v = res['verdict']
    if v == 'fail':
        return {'class': 'policy-failed', 'runId': res['currentRunId']}
    if v == 'indeterminate':
        code = 'BASELINE.RECIPE_UNSUPPORTED' if res.get('d9Deficiency') == 'baseline-recipe-unsupported' else 'VERDICT.INDETERMINATE'
        t = {'class': 'indeterminate', 'reasonCodes': [code], 'runId': res['currentRunId']}
        if res.get('remedy'):
            t['domainDetail'] = res['remedy']
        return t
    if v == 'pass':
        return {'class': 'success', 'runId': res['currentRunId']}
    raise ValueError('comparison verdict ' + str(v))

def analysis_termination(res, verdict_gate):
    """AnalysisResult -> StepTermination under the step's gate participation.
    self: the Run verdict terminates the step. delegated: only completion/indeterminacy terminate it;
    a failing verdict is success-with-runId because the consuming comparison step owns the gate."""
    if res['verdict'] == 'indeterminate' or res.get('requiredCoverage') != 'satisfied':
        return terminate({'event': 'completed-analysis', 'verdict': 'indeterminate', 'runId': res.get('runId')})
    if verdict_gate == 'delegated':
        return {'class': 'success', **({'runId': res['runId']} if res.get('runId') else {})}
    return terminate({'event': 'completed-analysis', 'verdict': res['verdict'], 'runId': res.get('runId')})

def exit_code(termination):
    return EXIT[termination['class']]

# ----------------------------------------------------------------------------- invocation lifecycle

def validate_dag(steps):
    """Closed admission of the ordered step list. Every refusal is REQUEST.UNSATISFIABLE (2) with a typed detail."""
    if len(steps) == 0 or len(steps) > MAX_STEPS:
        raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.STEP_BOUND_EXCEEDED', 'an invocation has 1..64 steps')
    ids = [s['stepId'] for s in steps]
    if ids != list(range(len(steps))):
        raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_INVALID', 'stepIds must be 0..n-1 in order')
    by = {s['stepId']: s for s in steps}
    consumers = {}
    for s in steps:
        if s['params'].get('kind') != s['kind']:
            raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_INVALID', 'step kind and parameter kind must agree', str(s['stepId']))
        if len(set(s['dependsOn'])) != len(s['dependsOn']):
            raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_INVALID', 'dependsOn entries must be unique', str(s['stepId']))
        for d in s['dependsOn']:
            if not isinstance(d, int) or d < 0 or d >= len(steps):
                raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_INVALID', 'dependsOn names an unknown stepId', str(s['stepId']))
            if d >= s['stepId']:
                raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_CYCLE', 'dependsOn must name lower stepIds', str(s['stepId']))
            if s['requirement'] == 'required' and by[d]['requirement'] == 'optional':
                raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL', 'make the dependency required or the dependent optional', str(s['stepId']))
        if s['dependencyGate'] == 'terminal' and s['kind'] not in TERMINAL_GATE_KINDS:
            raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.GATE_NOT_APPLICABLE', 'dependencyGate=terminal is lawful only for render/export-delivery', str(s['stepId']))
        if s['kind'] in NEVER_RETRY_KINDS and s['retryPolicy'] != 'none':
            raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.RETRY_BUDGET_EXHAUSTED', 'mutating steps are never implicitly retried', str(s['stepId']))
        p = s['params']
        if s['kind'] == 'analysis' and p.get('role') == 'pivot' and p.get('durability') != 'authoritative':
            raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY', 'a pivot analysis is authoritative')
        if s['kind'] == 'comparison':
            for key in ('currentStep', 'pivotStep'):
                if key in p:
                    t = p[key]
                    if t not in s['dependsOn'] or by[t]['kind'] != 'analysis':
                        raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.DEPENDENCY_INVALID', key + ' must name an analysis step in dependsOn', str(s['stepId']))
                    consumers.setdefault(t, []).append(s['stepId'])
            if by[p['currentStep']]['params'].get('verdictGate') != 'delegated' or by[p['currentStep']]['params'].get('durability') != 'authoritative':
                raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.VERDICT_GATE_UNBOUND', 'the comparison currentStep must be an authoritative analysis with verdictGate=delegated', str(s['stepId']))
    for s in steps:
        if s['kind'] == 'analysis' and (s['params'].get('verdictGate') == 'delegated' or s['params'].get('role') == 'pivot'):
            if len(consumers.get(s['stepId'], [])) != 1:
                raise Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.VERDICT_GATE_UNBOUND', 'a delegated/pivot analysis needs exactly one consuming comparison step', str(s['stepId']))

def synthetic_execution_id(request_id, step_id, n):
    """SYNTHETIC fixture label in the EXECUTION-ID-V1 grammar (c2-plan-stage-schema.v4 $.planIntent.wireTypes.executionId).
    That selector declares grammar only and records (RES-C2V4-01) that no producing recipe exists; the host mints
    operational ids. Deriving one from requestId/stepId/attempt here keeps fixtures distinct and reproducible and
    is NOT a recipe any implementation may use."""
    return 'exec1_' + raw_sha((request_id + ':' + str(step_id) + ':' + str(n)).encode())[:32]

_exec_id = synthetic_execution_id

def run_invocation(record, script):
    """record: InvocationRecordV1 without stepResults/termination. script: {stepId: [attempt observations...]},
    optional 'cancelAt': {'stepId': k, 'signal': 'SIGINT'} meaning the signal arrives before step k starts."""
    steps = record['orderedSteps']
    validate_dag(steps)
    mode = record['mode']
    results, outcomes = [], {}
    cancel = script.get('cancelAt')
    cancelled_from = None
    for s in steps:
        sid = s['stepId']
        if cancel and sid >= cancel['stepId'] and cancelled_from is None:
            cancelled_from = sid
        if cancelled_from is not None:
            results.append({'stepId': sid, 'outcome': 'cancelled', 'attempts': [], 'termination': {'class': 'interrupted', 'signal': cancel['signal']}})
            outcomes[sid] = 'cancelled'
            continue
        # dependency gate
        gate_ok, skip = True, None
        for d in s['dependsOn']:
            o = outcomes[d]
            if o == 'cancelled':
                gate_ok, skip = False, 'dependency-cancelled'
            elif s['dependencyGate'] == 'completed' and o != 'completed':
                gate_ok, skip = False, 'dependency-not-completed'
            elif s['dependencyGate'] == 'terminal' and o not in ('completed', 'rejected', 'failed', 'skipped', 'abandoned'):
                gate_ok, skip = False, 'dependency-not-terminal'
        if not gate_ok:
            results.append({'stepId': sid, 'outcome': 'skipped', 'attempts': [], 'skipReason': skip, 'termination': {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED'}})
            outcomes[sid] = 'skipped'
            continue
        # ephemeral authority law
        p = s['params']
        if mode['ephemeral'] and (s['kind'] in ('repair-preview', 'repair-apply', 'verify') or (s['kind'] == 'mutation' and p.get('mutationClass') in ('baseline-adopt', 'baseline-upgrade-apply'))):
            t = Refusal('REQUEST.UNSATISFIABLE', 'WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY', 'drop --ephemeral').termination()
            results.append({'stepId': sid, 'outcome': 'rejected', 'attempts': [], 'termination': t})
            outcomes[sid] = 'rejected'
            continue
        attempts, final = [], None
        obs_list = script.get(str(sid), [{'event': 'completed', 'result': {'kind': 'query', 'items': 0, 'truncated': False, 'completenessMet': True, 'advisory': False}}])
        for n, obs in enumerate(obs_list, 1):
            a = {'executionId': _exec_id(record['requestId'], sid, n), 'outcome': 'completed'}
            if 'installationJournalRefs' in obs:
                if s['kind'] != 'mutation' or p['mutationClass'] not in ('core-update', 'core-repair', 'core-rollback', 'store-migrate', 'store-rollback'):
                    raise ValueError('installation journal belongs only to an installation mutation attempt')
                a['installationJournalRefs'] = obs['installationJournalRefs']
                if 'installationRecoveryStartRef' in obs:
                    a['installationRecoveryStartRef'] = obs['installationRecoveryStartRef']
                    if not a['installationJournalRefs'] or a['installationJournalRefs'][0] != a['installationRecoveryStartRef']:
                        raise ValueError('recovery history must start with its observed durable revision')
                validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/Attempt', a)
            if obs['event'] == 'completed':
                if s['kind'] in ('analysis', 'verify'):
                    a['derivation'] = obs.get('derivation', {'planId': 'plan2:' + '0' * 64, 'executionPlanId': 'exec-plan2:' + '0' * 64, 'stageCount': 1, 'stagesCompleted': 1})
                attempts.append(a)
                res = obs['result']
                if s['kind'] == 'analysis' and p['durability'] == 'ephemeral' and res.get('authority') != 'ephemeral':
                    raise ValueError('script error: ephemeral analysis must yield an ephemeral result')
                if s['kind'] == 'analysis' and res.get('authority') == 'ephemeral' and 'runId' in res:
                    raise ValueError('script error: ephemeral result carries a runId')
                if obs.get('termination'):
                    term = obs['termination']
                elif s['kind'] in ('analysis', 'verify'):
                    term = analysis_termination(res, p.get('verdictGate', 'self') if s['kind'] == 'analysis' else 'self')
                elif s['kind'] == 'comparison':
                    if res.get('kind') != 'comparison':
                        raise ValueError('script error: comparison step must yield a ComparisonStepResult')
                    term = comparison_termination(res)
                else:
                    term = {'class': 'success'}
                final = ('completed', res, term)
                break
            if obs['event'] == 'rejected':
                a['outcome'] = 'rejected'
                attempts.append(a)
                final = ('rejected', None, terminate(obs))
                break
            if obs['event'] == 'operational-fault':
                a['outcome'] = 'failed'
                a['faultCause'] = obs['faultCause']
                attempts.append(a)
                can_retry = s['retryPolicy'] == 'idempotent-retry' and s['kind'] in RETRYABLE_KINDS and obs['faultCause'] == 'ledger-busy' and n < MAX_ATTEMPTS and n < len(obs_list)
                if can_retry:
                    a['retried'] = True
                    continue
                t = terminate(obs)
                if n >= MAX_ATTEMPTS and obs['faultCause'] == 'ledger-busy':
                    t['domainDetail'] = {'code': 'WORKFLOW.RETRY_BUDGET_EXHAUSTED', 'remedy': 'ledger still busy after 3 attempts; retry later'}
                final = ('failed', None, t)
                break
            raise ValueError('unknown script event ' + obs['event'])
        outcome, res, term = final
        r = {'stepId': sid, 'outcome': outcome, 'attempts': attempts, 'termination': term}
        if res is not None:
            r['result'] = res
        results.append(r)
        outcomes[sid] = outcome
    # aggregate
    required = [r for r, s in zip(results, steps) if s['requirement'] == 'required']
    settled = all(r['outcome'] in ('completed', 'rejected', 'failed', 'skipped', 'abandoned') for r in required)
    if cancel and not settled:
        agg = {'class': 'interrupted', 'signal': cancel['signal']}
        committed = [r['result']['runId'] for r in required if r['outcome'] == 'completed' and r.get('result', {}).get('runId')]
        if committed:
            agg['runId'] = committed[-1]
        phase = 'before-settle'
    else:
        classes = [r['termination']['class'] for r in required if r['outcome'] != 'skipped']
        pick = next((c for c in AGGREGATE_ORDER if c in classes), 'success')
        agg = next(r['termination'] for r in required if r['outcome'] != 'skipped' and r['termination']['class'] == pick) if classes else {'class': 'success'}
        matching=[r['termination'] for r in required if r['outcome']!='skipped' and r['termination']['class']==pick]
        agg = dict(next((t for t in matching if t.get('domainDetail')),agg))
        phase = 'after-settle' if cancel else 'none'
    out = dict(record)
    out['stepResults'] = results
    out['termination'] = agg
    out['terminationEmitted'] = True
    if cancel:
        out['cancellation'] = {'requested': True, 'signal': cancel['signal'], 'phase': phase}
    return out, exit_code(agg)

# ----------------------------------------------------------------------------- comparison

AUDIT_PROFILES = {
    'code-regression': {'name': 'code-regression', 'gateCodeNetNew': True, 'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False, 'newWaiverSuppressesCodeNetNew': False, 'gateRuleUnder': 'baseline-or-current'},
    'policy-change': {'name': 'policy-change', 'gateCodeNetNew': True, 'gateNewlyLiveByPolicyAxes': True, 'gateAllCurrentLive': False, 'newWaiverSuppressesCodeNetNew': False, 'gateRuleUnder': 'baseline-or-current'},
    'full-current': {'name': 'full-current', 'gateCodeNetNew': True, 'gateNewlyLiveByPolicyAxes': True, 'gateAllCurrentLive': True, 'newWaiverSuppressesCodeNetNew': True, 'gateRuleUnder': 'current-only'},
    'report-only': {'name': 'report-only', 'gateCodeNetNew': False, 'gateNewlyLiveByPolicyAxes': False, 'gateAllCurrentLive': False, 'newWaiverSuppressesCodeNetNew': True, 'gateRuleUnder': 'current-only'},
}
AXES = ['code', 'detection', 'policy', 'scope', 'waiver']
AXIS_CLASS = {'code': None, 'detection': 'DETECTION-DELTA', 'policy': 'POLICY-DELTA', 'scope': 'SCOPE-DELTA', 'waiver': 'WAIVER-DELTA'}
AXIS_PIVOT = {'policy': 'E1', 'scope': 'E2', 'waiver': 'E3'}
COUNT_KEYS = ['UNCHANGED', 'CODE-NET-NEW', 'CODE-FIXED', 'DETECTION-DELTA', 'POLICY-DELTA', 'SCOPE-DELTA', 'WAIVER-DELTA', 'EVIDENCE-DELTA', 'INDETERMINATE', 'gating']

def resolve_detectors(baseline, current_detectors, host):
    """Detector disposition over the UNION of baseline and current detectors (an added or removed detector never
    raises). host = {'closures': {closureId: {'bytes','trust','protocolMajor','platform'}}, 'protocolMajors': [..],
    'platform': str, 'pivotRunId': run2|absent}. current_detectors = {detectorId: {'closureId','semanticsMajor','compatibleWith': [..]}}."""
    out = {}
    pivot_ids = {p['closureId'] for p in baseline['pivotClosure']}
    def pivot_state():
        for cid in sorted(pivot_ids):
            c = host['closures'].get(cid)
            if c is None or c['bytes'] == 'missing':
                return 'pivot-detector-unavailable'
            if c['trust'] != 'admitted':
                return 'pivot-closure-revoked'
            if c['protocolMajor'] not in host['protocolMajors'] or c['platform'] != host['platform']:
                return 'pivot-closure-incompatible'
        return None if host.get('pivotRunId') else 'pivot-run-not-committed'
    base = {d['detectorId']: d for d in baseline['detectorClosure']}
    for did in sorted(set(base) | set(current_detectors), key=lambda s: s.encode()):
        d, cur = base.get(did), current_detectors.get(did)
        disp = {'detectorId': did, 'baselineClosureId': d['closureId'] if d else None, 'currentClosureId': cur['closureId'] if cur else None,
                'baselineSemanticsMajor': d['semanticsMajor'] if d else None, 'currentSemanticsMajor': cur['semanticsMajor'] if cur else None}
        if d is None:
            disp['method'] = 'detector-added'
        elif cur is None:
            reason = pivot_state()
            if reason is None:
                disp.update(method='detector-removed', pivotRunId=host['pivotRunId'])
            else:
                disp.update(method='indeterminate', indeterminateReason=reason)
        elif cur['closureId'] == d['closureId']:
            disp['method'] = 'identical-closure'
        elif d['closureId'] in cur.get('compatibleWith', []) and cur['semanticsMajor'] == d['semanticsMajor']:
            disp['method'] = 'declared-compatible'
        else:
            reason = pivot_state()
            if reason is None:
                disp['method'] = 'three-way-pivot'
                disp['pivotRunId'] = host['pivotRunId']
            else:
                disp['method'] = 'indeterminate'
                disp['indeterminateReason'] = reason
        out[did] = disp
    return out

def _imports_by_kind(av):
    by = {}
    for i in av.get('imports', []):
        by.setdefault(i['kind'], set()).add(i['importId'])
    return by

def classify(fp, entry_rule, presence, rule_b, rule_c, ev_b, ev_c, detector_disp, profile, unavailable_pivots=()):
    """One entry. presence: {'B','E0','E1','E2','E3','E4','waivedB','waivedC'}; E0 may be None.
    Evidence axis compares exact bound import identities per declared kind, not kind presence."""
    e = {'fingerprint': fp, 'ruleId': entry_rule, 'detectorId': detector_disp['detectorId'], 'presence': presence, 'subsequentDeltas': []}
    gating_b = bool(rule_b and rule_b['enabled'] and rule_b['gating'])
    gating_c = bool(rule_c and rule_c['enabled'] and rule_c['gating'])
    rule_gating = (gating_b or gating_c) if profile['gateRuleUnder'] == 'baseline-or-current' else gating_c
    live = presence['E4'] and not presence['waivedC']
    e['liveInCurrent'] = live
    if unavailable_pivots:
        e.update(classification='INDETERMINATE', indeterminateReason='pivot-reevaluation-unavailable', gates=False)
        return e, ('indeterminate' if rule_gating else None)
    ib, ic = _imports_by_kind(ev_b), _imports_by_kind(ev_c)
    uses = (rule_c or rule_b or {}).get('evidenceUse', [])
    for u in uses:
        sb, sc = ib.get(u['kind'], set()), ic.get(u['kind'], set())
        if u['requirement'] == 'required' and not sc:
            e.update(classification='INDETERMINATE', indeterminateReason='required-evidence-unavailable', gates=False)
            return e, ('indeterminate' if rule_gating else None)
        if sb != sc:
            if rule_gating:
                e.update(classification='INDETERMINATE', indeterminateReason='evidence-availability-changed' if bool(sb) != bool(sc) else 'evidence-content-changed', gates=False)
                return e, 'indeterminate'
            if presence['B'] != presence['E4']:
                e.update(classification='EVIDENCE-DELTA', direction='appeared' if presence['E4'] else 'vanished', gates=False)
                return e, None
    if detector_disp['method'] == 'indeterminate':
        e.update(classification='INDETERMINATE', indeterminateReason=detector_disp['indeterminateReason'], gates=False)
        return e, ('indeterminate' if rule_gating else None)
    chain = [presence['B'], presence['E0'] if presence['E0'] is not None else presence['E1'], presence['E1'], presence['E2'], presence['E3'], presence['E4']]
    changes = [AXES[i] for i in range(5) if chain[i] != chain[i + 1]]
    waiver_changed = presence['waivedB'] != presence['waivedC']
    if not changes:
        if waiver_changed:
            e.update(classification='WAIVER-DELTA', direction='waiver-added' if presence['waivedC'] else 'waiver-removed')
        else:
            e['classification'] = 'UNCHANGED'
    else:
        first = changes[0]
        idx = AXES.index(first)
        appeared = chain[idx + 1]
        if first == 'code':
            e['classification'] = 'CODE-NET-NEW' if appeared else 'CODE-FIXED'
        else:
            e['classification'] = AXIS_CLASS[first]
        e['direction'] = 'appeared' if appeared else 'vanished'
        e['subsequentDeltas'] = changes[1:] + (['waiver'] if waiver_changed and 'waiver' not in changes[1:] else [])
    gates, reason = False, None
    c = e['classification']
    if c == 'CODE-NET-NEW' and profile['gateCodeNetNew'] and rule_gating:
        new_waiver = presence['waivedC'] and not presence['waivedB']
        if live:
            gates, reason = True, 'code-net-new'
        elif not (new_waiver and profile['newWaiverSuppressesCodeNetNew']):
            gates, reason = True, 'code-net-new-policy-hidden'
    if not gates and c in ('POLICY-DELTA', 'SCOPE-DELTA', 'WAIVER-DELTA', 'DETECTION-DELTA') and live and gating_c and profile['gateNewlyLiveByPolicyAxes'] and (e.get('direction') in ('appeared', 'waiver-removed')):
        gates, reason = True, 'newly-live-policy-axis'
    if not gates and live and gating_c and profile['gateAllCurrentLive']:
        gates, reason = True, 'current-live'
    e['gates'] = gates
    if gates:
        e['gateReason'] = reason
    return e, ('fail' if gates else None)

def rule_deficiencies(current_rules):
    """Current-side rules whose required coverage/evidence is unsatisfied, independent of any finding."""
    out = []
    for rid in sorted(current_rules, key=lambda s: s.encode()):
        r = current_rules[rid]
        if not r['enabled']:
            continue
        if r['requiredCoverage'] == 'unsatisfied':
            out.append({'ruleId': rid, 'gating': bool(r['gating']), 'cause': 'required-coverage-unsatisfied'})
        elif r['requiredCoverage'] == 'unknown':
            out.append({'ruleId': rid, 'gating': bool(r['gating']), 'cause': 'required-coverage-unknown'})
    return out

def compare(baseline, current, host, profile_name, current_detectors, accept_origins=()):
    """baseline: BaselineDescriptor (+ entries, _baselineId). current: {'runId','snapshotId','projectId','context',
    'ruleCoverage': {ruleId: RuleCoverage}, 'presence': {fp: PivotPresence}, 'entryRules': {fp: (ruleId, detectorId)},
    'boundPivots': [..names of E1..E3 whose re-evaluation results were actually bound..]}."""
    profile = AUDIT_PROFILES[profile_name]
    desc = {'schemaFamily': 'opensip.product.comparison', 'schemaMajor': 1, 'baselineId': baseline['_baselineId'], 'currentRunId': current['runId'], 'currentSnapshotId': current['snapshotId'],
            'auditProfile': profile, 'baselineContext': baseline['context'], 'currentContext': current['context'], 'detectors': [], 'ruleDeficiencies': [], 'entries': []}
    if baseline['originProjectId'] == current['projectId']:
        desc['projectCorrespondence'] = 'same-project'
    elif baseline['originProjectId'] in accept_origins:
        desc['projectCorrespondence'] = 'declared'
    else:
        desc['projectCorrespondence'] = 'unmapped'
    bc, cc = baseline['context'], current['context']
    desc['contextDelta'] = {'codeChanged': baseline['source']['snapshotId'] != current['snapshotId'], 'detectorChanged': sorted(bc['detectorClosureIds']) != sorted(cc['detectorClosureIds']),
                            'policyChanged': bc['policyDigest'] != cc['policyDigest'], 'scopeChanged': bc['scopeDigest'] != cc['scopeDigest'], 'waiversChanged': bc['waiverSetDigest'] != cc['waiverSetDigest'],
                            'evidenceAvailabilityChanged': sorted(i['importId'] for i in bc['evidenceAvailability'].get('imports', [])) != sorted(i['importId'] for i in cc['evidenceAvailability'].get('imports', []))}
    def whole(reason, code, remedy):
        desc.update(comparisonPerformed=False, wholeIndeterminateReason=reason, remedy={'code': code, 'remedy': remedy}, pivotsAvailable={'E0': 'unavailable', 'E1': 'unavailable', 'E2': 'unavailable', 'E3': 'unavailable'},
                    counts={k: 0 for k in COUNT_KEYS}, verdict='indeterminate', d9Deficiency='baseline-recipe-unsupported')
        return {'comparisonResultId': wid('comparison2', 'workflow.comparison', desc), 'descriptor': desc}
    if desc['projectCorrespondence'] == 'unmapped':
        return whole('baseline-project-unmapped', 'BASELINE.PROJECT_UNMAPPED', 'pass --accept-origin ' + baseline['originProjectId'])
    if baseline['schemaMajor'] != 1:
        return whole('baseline-schema-major-unsupported', 'BASELINE.SCHEMA_MAJOR_UNSUPPORTED', 'upgrade the host or re-adopt the baseline')
    if baseline['fingerprintRecipe']['recipeMajor'] not in host.get('recipeMajors', [2]):
        return whole('baseline-recipe-unsupported', 'BASELINE.SCHEMA_MAJOR_UNSUPPORTED', 'baseline upgrade required')
    for k, key in (('policy', 'policyDigest'), ('scope', 'scopeDigest'), ('waivers', 'waiverSetDigest')):
        if doc_digest(baseline['contextDocuments'][k]) != bc[key]:
            return whole('baseline-context-document-missing', 'BASELINE.CONTEXT_DOCUMENT_MISSING', 'the embedded ' + k + ' document does not match its digest; re-export the baseline')
    dets = resolve_detectors(baseline, current_detectors, host)
    desc['detectors'] = [dets[k] for k in sorted(dets, key=lambda s: s.encode())]
    e0_state = 'not-needed' if not desc['contextDelta']['detectorChanged'] else ('available' if all(d['method'] != 'indeterminate' for d in dets.values()) else 'unavailable')
    bound = set(current.get('boundPivots', []))
    piv = {'E0': e0_state}
    unavailable = []
    for axis, key in (('policy', 'policyChanged'), ('scope', 'scopeChanged'), ('waiver', 'waiversChanged')):
        pv = AXIS_PIVOT[axis]
        if not desc['contextDelta'][key]:
            piv[pv] = 'not-needed'
        elif pv in bound:
            piv[pv] = 'available'
        else:
            piv[pv] = 'unavailable'
            unavailable.append(pv)
    desc['pivotsAvailable'] = piv
    desc['comparisonPerformed'] = True
    b_rules = {r['ruleId']: r for r in baseline['ruleCoverage']}
    c_rules = current['ruleCoverage']
    desc['ruleDeficiencies'] = rule_deficiencies(c_rules)
    b_entries = {x['fingerprint']: x for x in baseline['entries']}
    fps = sorted(set(b_entries) | set(current['presence']), key=lambda s: s.encode())
    counts = {k: 0 for k in COUNT_KEYS}
    verdict_signals = set()
    for fp in fps:
        rule_id, det_id = current['entryRules'].get(fp) or (b_entries[fp]['ruleId'], b_entries[fp]['detectorId'])
        pres = current['presence'].get(fp) or {'B': True, 'E0': False if e0_state == 'available' else None, 'E1': False, 'E2': False, 'E3': False, 'E4': False, 'waivedB': b_entries[fp]['waived'], 'waivedC': False}
        pres = dict(pres)
        pres['B'] = fp in b_entries
        if pres['B']:
            pres['waivedB'] = b_entries[fp]['waived']
        m = dets[det_id]['method']
        if m in ('identical-closure', 'declared-compatible') and e0_state != 'available':
            pres['E0'] = pres['E1']
        elif m == 'detector-added':
            pres['E0'] = False
        elif m == 'detector-removed':
            # E0 is the actually bound old detector on current source. Substituting
            # B would hide new code findings whenever the same PR removed a detector.
            pres['E1'] = pres['E2'] = pres['E3'] = pres['E4'] = False
        elif m == 'indeterminate':
            pres['E0'] = None
        entry, sig = classify(fp, rule_id, pres, b_rules.get(rule_id), c_rules.get(rule_id), bc['evidenceAvailability'], cc['evidenceAvailability'], dets[det_id], profile, unavailable)
        desc['entries'].append(entry)
        counts[entry['classification']] += 1
        if entry['gates']:
            counts['gating'] += 1
        if sig:
            verdict_signals.add(sig)
    for dfc in desc['ruleDeficiencies']:
        if dfc['gating']:
            verdict_signals.add('indeterminate')
    # Missing comparisons can hide findings that never enter either observed set.
    # Their gate effect therefore cannot depend on visiting a finding entry.
    gating_rules = list(c_rules.values())
    if profile['gateRuleUnder'] == 'baseline-or-current':
        gating_rules += list(b_rules.values())
    if (unavailable or e0_state == 'unavailable') and any(r['enabled'] and r['gating'] for r in gating_rules):
        verdict_signals.add('indeterminate')
    desc['counts'] = counts
    desc['verdict'] = 'fail' if 'fail' in verdict_signals else ('indeterminate' if 'indeterminate' in verdict_signals else 'pass')
    if desc['verdict'] == 'indeterminate':
        desc['d9Deficiency'] = 'baseline-recipe-unsupported' if e0_state == 'unavailable' else 'verdict-indeterminate'
        gating_def = [d for d in desc['ruleDeficiencies'] if d['gating']]
        if e0_state == 'unavailable':
            desc['remedy'] = {'code': 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE', 'remedy': 'install or bundle the baseline pivot closure under current trust, or adopt a new baseline explicitly'}
        elif unavailable:
            desc['remedy'] = {'code': 'COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE', 'remedy': 'bind the re-evaluation results for ' + ','.join(unavailable)}
        elif gating_def:
            desc['remedy'] = {'code': 'COMPARISON.REQUIRED_COVERAGE_UNSATISFIED', 'remedy': 'restore required coverage/evidence for ' + ','.join(d['ruleId'] for d in gating_def)}
        else:
            desc['remedy'] = {'code': 'COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE', 'remedy': 're-import the required evidence against the current snapshot'}
    return {'comparisonResultId': wid('comparison2', 'workflow.comparison', desc), 'descriptor': desc}

def comparison_step_result(res):
    """Project a ComparisonResultV1 into the ComparisonStepResult that the invocation lifecycle terminates on."""
    d = res['descriptor']
    out = {'kind': 'comparison', 'comparisonResultId': res['comparisonResultId'], 'currentRunId': d['currentRunId'], 'baselineId': d['baselineId'], 'verdict': d['verdict'], 'comparisonPerformed': d['comparisonPerformed'],
           'counts': {'entries': len(d['entries']), 'gating': d['counts']['gating'], 'indeterminate': d['counts']['INDETERMINATE']}}
    if d.get('d9Deficiency'):
        out['d9Deficiency'] = d['d9Deficiency']
    if d.get('remedy'):
        out['remedy'] = d['remedy']
    return out

# ----------------------------------------------------------------------------- baseline adoption/admission

SCOPE_DOCUMENT_SCHEMA = 'workflows/schemas/policy-document.schema.json'
SCOPE_DOCUMENT_SELECTOR = '#/$defs/ScopeDocumentV1'


def verify_scope_parameter_binding(analysis_spec, scope):
    """Prove that `scope` IS the Run's selected scope-policy analysis-spec parameter.

    This is the join `adopt_baseline` cannot make on its own. `adopt_baseline` receives `plan` as a
    PlanId STRING, so assigning `ctx['scopeDigest'] = doc_digest(scope)` records the digest of
    whatever document the caller passed and proves nothing about selection; the same is true of
    `policyDigest`. Describing that assignment as a binding would be false. The binding is only
    decidable with the retained analysis-spec record in hand, which is what this function takes.

    A parameter row is `{schemaDigest, payloadDigest}`. The row must cite the registered
    ScopeDocumentV1 document AND carry this document's canonical digest as its payload; a document
    that is not a selected parameter, or one cited under a different schema, refuses. Returns the
    verified digest."""
    document = raw_sha((Path(__file__).resolve().parent.parent / SCOPE_DOCUMENT_SCHEMA).read_bytes())
    digest = doc_digest(scope)
    rows = [row for row in analysis_spec.get('parameters', []) if row.get('schemaDigest') == document]
    if not rows:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER',
                      'the analysis spec selects no ScopeDocumentV1 parameter')
    if not any(row.get('payloadDigest') == digest for row in rows):
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH',
                      'the supplied scope document is not the selected scope parameter')
    return digest


def adopt_baseline(run, plan, project_id, policy, scope, waivers, rule_coverage, entries, detector_closure, pivot_closure, context, host_release, analysis_spec=None):
    """Pure projection over documents the caller must ALREADY have admitted.

    PRECONDITION, stated rather than implied: `policy`, `scope` and `waivers` must be exactly the
    documents the Run's Plan selected - `plan.policyDigest`, the ScopeDocumentV1 analysis-spec
    parameter and `plan.waiverDigest`. This function cannot check that from `plan`, which is a
    PlanId string, so with `analysis_spec=None` the scope binding is a CALLER ASSERTION and the
    digest assignment below is a record of what was passed, not evidence of selection. Pass the
    retained analysis-spec record to have the scope binding actually verified here."""
    if run.get('authority') != 'authoritative':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'BASELINE.SOURCE_EPHEMERAL', 'run an authoritative analysis first')
    if run.get('availability', 'retained') != 'retained':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'the Run evidence is ' + run.get('availability'))
    if analysis_spec is not None:
        verify_scope_parameter_binding(analysis_spec, scope)
    ctx = dict(context)
    ctx['policyDigest'] = doc_digest(policy)          # the digest of the PASSED document; equality with plan.policyDigest is the caller's precondition
    ctx['scopeDigest'] = doc_digest(scope)            # verified against the selected parameter above when analysis_spec is supplied
    ctx['waiverSetDigest'] = doc_digest(waivers)      # the digest of the PASSED resolved WaiverSetV1; likewise a precondition
    ents = sorted(entries, key=lambda x: x['fingerprint'].encode())
    if len({x['fingerprint'] for x in ents}) != len(ents):
        raise Refusal('CONFIG.INVALID', None, 'duplicate fingerprint in baseline entries')
    desc = {'schemaFamily': 'opensip.product.baseline', 'schemaMajor': 1, 'originProjectId': project_id, 'source': {'snapshotId': run['snapshotId']}, 'runId': run['runId'], 'planId': plan,
            'fingerprintRecipe': {'domain': 'finding-fingerprint', 'recipeMajor': 2}, 'detectorClosure': detector_closure, 'pivotClosure': sorted(pivot_closure, key=lambda p: p['closureId']),
            'context': ctx, 'contextDocuments': {'policy': policy, 'scope': scope, 'waivers': waivers}, 'ruleCoverage': rule_coverage, 'entries': ents}
    bid = wid('baseline2', 'workflow.baseline', desc)
    pins = sorted({run['runId']} | {p['closureId'] for p in pivot_closure})
    art = {'baselineId': bid, 'descriptor': desc, 'custody': {'exportedByHostRelease': host_release, 'exportedAtUtc': '2026-09-05T00:00:00Z', 'runRetainedAtExport': True, 'retentionPins': pins}}
    return art

def verify_baseline_artifact(art):
    """Fresh-CI admission of a tracked artifact: identity recomputation and internal consistency; no origin store."""
    d = art['descriptor']
    if wid('baseline2', 'workflow.baseline', d) != art['baselineId']:
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'baselineId does not match descriptor')
    if not d['runId'].startswith('run2:'):
        raise Refusal('CONFIG.INVALID', 'BASELINE.SOURCE_EPHEMERAL', 'a baseline names an authoritative run2')
    fps = [x['fingerprint'] for x in d['entries']]
    if fps != sorted(fps, key=lambda s: s.encode()) or len(set(fps)) != len(fps):
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'entries must be sorted and unique')
    for x in d['entries']:
        if 'legacyFingerprint' in x and not x['fingerprint'].startswith('finding-key2:'):
            raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'legacy fingerprints migrate identity only')
    return True

# ----------------------------------------------------------------------------- imports

PAYLOAD_REGISTRY = {
    # ONE closed registry (PayloadRegistryV1). runtime/test/history admit ONLY the workflow payloads; native adapters
    # normalise their runtime-coverage/test-results/history grammars into these BEFORE import. dependency/prepared
    # admit ONLY the native payload domains spelled exactly as native-evidence.md §7.
    ('runtime', 'workflow.import-payload.runtime.v1'): {'owner': 'workflow', 'schemaDocument': 'workflows/schemas/imported-evidence.schema.json', 'selector': '#/$defs/RuntimePayloadV1'},
    ('test', 'workflow.import-payload.test.v1'): {'owner': 'workflow', 'schemaDocument': 'workflows/schemas/test-execution.schema.json', 'selector': '#/$defs/TestPayloadV1'},
    ('history', 'workflow.import-payload.history.v1'): {'owner': 'workflow', 'schemaDocument': 'workflows/schemas/imported-evidence.schema.json', 'selector': '#/$defs/HistoryPayloadV1'},
    ('dependency', 'native.import-payload.dependency-source.v1'): {'owner': 'native', 'schemaDocument': 'native/native-evidence.schemas.v2.json', 'selector': '#/$defs/DependencySourcePayloadV1'},
    ('prepared', 'native.import-payload.prepared-output.v1'): {'owner': 'native', 'schemaDocument': 'native/native-evidence.schemas.v2.json', 'selector': '#/$defs/PreparedOutputPayloadV1'},
}
PAYLOAD_BINDINGS = {k: v['owner'] for k, v in PAYLOAD_REGISTRY.items()}
STALENESS_TABLE = [
    ('exact-snapshot', 'snapshot-equal', 'current', 'consumable'), ('exact-snapshot', 'snapshot-differs', 'stale', 'unmapped-only'),
    ('vcs-revision', 'commit-equal-clean-mapped', 'current', 'consumable'), ('vcs-revision', 'commit-equal-clean-unmapped', 'current', 'unmapped-only'),
    ('vcs-revision', 'commit-equal-dirty', 'unverifiable', 'unmapped-only'),
    ('vcs-revision', 'commit-differs', 'stale', 'unmapped-only'), ('vcs-revision', 'build-identity-differs', 'wrong-build', 'unmapped-only'),
    ('exact-snapshot', 'artifact-corrupt', 'unverifiable', 'refused'), ('vcs-revision', 'artifact-corrupt', 'unverifiable', 'refused'),
]

def registry_row(kind, payload_domain):
    return PAYLOAD_REGISTRY.get((kind, payload_domain))

def validate_import_record(document, selector, value):
    """Only local, pinned schema-closure resources; never resolve an input URL."""
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    from jsonschema import ValidationError
    root = Path(__file__).resolve().parent.parent
    paths = list((root / 'workflows' / 'schemas').glob('*.schema.json'))
    paths += [root / 'native' / 'native-evidence.schemas.v2.json', root / 'foundation' / 'identity-schemas.v2.json']
    docs = {p: canonical.parse(p.read_bytes()) for p in paths}
    registry = Registry().with_resources((d['$id'], Resource(contents=d, specification=DRAFT202012)) for d in docs.values())
    try:
        canonical.typed(value)
        canonical.ExactValidator({'$ref': docs[root / document]['$id'] + selector}, registry=registry).validate(value)
    except (ValidationError, canonical.AdmissionError) as exc:
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'input does not satisfy the pinned ' + selector) from exc

def build_import(kind, payload, payload_domain, registered_schemas, correspondence, producer_closure, adapter_closure, blobs, scope, observation, build=None):
    """registered_schemas: {payloadDomain: exact schema DOCUMENT bytes}. scope: ImportScopeDescriptor (foundation scope-descriptor);
    observation: ImportObservationV1. Every auxiliary digest is raw SHA-256 of canonical bytes; the preimages are returned as blobs."""
    if correspondence is None:
        raise Refusal('CONFIG.INVALID', 'IMPORT.MAPPING_REQUIRED', 'pass --snapshot or --commit')
    if registry_row(kind, payload_domain) is None:
        if not any(pd == payload_domain for _, pd in PAYLOAD_REGISTRY):
            raise Refusal('CONFIG.INVALID', 'IMPORT.PAYLOAD_SCHEMA_UNREGISTERED', 'no registered schema for ' + payload_domain)
        raise Refusal('CONFIG.INVALID', 'IMPORT.KIND_PAYLOAD_MISMATCH', 'payload domain not admitted for kind ' + kind)
    if payload_domain not in registered_schemas:
        raise Refusal('CONFIG.INVALID', 'IMPORT.PAYLOAD_SCHEMA_UNREGISTERED', 'schema document bytes for ' + payload_domain + ' are not in the pinned registry closure')
    row = registry_row(kind, payload_domain)
    if registered_schemas[payload_domain] != (Path(__file__).resolve().parent.parent / row['schemaDocument']).read_bytes():
        raise Refusal('CONFIG.INVALID', 'IMPORT.PAYLOAD_SCHEMA_UNREGISTERED', 'schema bytes differ from the trusted registry closure')
    validate_import_record(row['schemaDocument'], row['selector'], payload)
    validate_import_record('workflows/schemas/common.schema.json', '#/$defs/SourceCorrespondence', correspondence)
    validate_import_record('foundation/identity-schemas.v2.json', '#/$defs/scope-descriptor', scope)
    if payload.get('payloadDomain') != payload_domain:
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'payloadDomain mismatch')
    if scope.get('schemaVersion') != 2 or set(scope) != {'schemaVersion', 'workspaceRoots', 'pathPrefixes', 'excludedPathPrefixes'}:
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'scope must be the foundation scope-descriptor record')
    build_rec = {'schemaVersion': 1, 'buildIdentity': build if build is not None else correspondence.get('buildIdentity')}
    obs = {k:v for k,v in observation.items() if k not in ('completeness','omissions')}
    obs.setdefault('schemaVersion', 1); obs.setdefault('kind', kind)
    for k in ('window', 'population', 'selection', 'revisionRange'):
        obs.setdefault(k, None)
    preimages = {'sourceCorrespondence': correspondence, 'buildIdentity': build_rec, 'scope': scope, 'observation': obs}
    for name, value in [('BuildIdentityV1', build_rec), ('ImportObservationV1', obs)]:
        validate_import_record('workflows/schemas/imported-evidence.schema.json', '#/$defs/' + name, value)
    row = registry_row(kind, payload_domain)
    wrapper = {'schemaVersion': 2, 'kind': kind, 'payloadSchemaDigest': raw_sha(registered_schemas[payload_domain]), 'payloadDigest': payload_digest(payload),
               'sourceCorrespondenceDigest': doc_digest(correspondence), 'buildDigest': doc_digest(build_rec),
               'producerClosure': producer_closure, 'adapterClosure': adapter_closure, 'blobs': sorted(blobs, key=lambda b: b['path'].encode()),
               'scopeDigest': doc_digest(scope), 'observationDigest': doc_digest(obs),
               'completeness': observation.get('completeness', 'complete'), 'omissions': sorted(set(observation.get('omissions', [])))}
    if wrapper['completeness'] != 'complete' and not wrapper['omissions']:
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'completeness != complete requires non-empty omissions')
    validate_import_record('foundation/identity-schemas.v2.json', '#/$defs/import', wrapper)
    return {'importId': wid('import2', 'import', wrapper), 'wrapper': wrapper, 'payloadBinding': {'kind': kind, 'payloadDomain': payload_domain, 'owner': row['owner'], 'schemaDocument': row['schemaDocument'], 'selector': row['selector']},
            'retainedPreimages': {k: canonical.canonical(v) for k, v in preimages.items()}}

def bound_import(record):
    """BoundImport row for EvaluationContext.evidenceAvailability.imports."""
    w = record['wrapper']
    return {'kind': w['kind'], 'importId': record['importId'], 'payloadDigest': w['payloadDigest'], 'sourceCorrespondenceDigest': w['sourceCorrespondenceDigest'], 'scopeDigest': w['scopeDigest'], 'observationDigest': w['observationDigest']}

def admit_source_mapping(mapping, snapshot_inventory, expected_snapshot_id):
    """SourceMappingV1 admission: every sourceSha256 must equal the snapshot2 inventory digest of sourcePath.
    Returns the mapping digest (raw SHA-256 of canonical bytes) or raises IMPORT.SOURCE_MAPPING_REQUIRED."""
    validate_import_record('workflows/schemas/imported-evidence.schema.json', '#/$defs/SourceMappingV1', mapping)
    if mapping['snapshotId'] != expected_snapshot_id:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'IMPORT.SOURCE_MAPPING_REQUIRED', 'mapping snapshot identity differs from the host-admitted target snapshot')
    inv = {b['path']: b['sha256'] for b in snapshot_inventory}
    paths = [e['generatedPath'] for e in mapping['entries']]
    if paths != sorted(paths, key=lambda s: s.encode()) or len(set(paths)) != len(paths):
        raise Refusal('CONFIG.INVALID', 'IMPORT.ARTIFACT_CORRUPT', 'mapping entries must be sorted and unique by generatedPath')
    for e in mapping['entries']:
        if inv.get(e['sourcePath']) != e['sourceSha256']:
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'IMPORT.SOURCE_MAPPING_REQUIRED', 'mapping names a source digest that is not in the snapshot inventory', e['generatedPath'])
    return doc_digest(mapping)

def classify_staleness(correspondence, plan_binding, corrupt=False):
    """plan_binding: {'snapshotId', 'vcsRevision': {...}|None, 'declaredBuildIds': [...], 'admittedSourceMappings': [digest...]}"""
    k = correspondence['kind']
    if corrupt:
        cond = 'artifact-corrupt'
    elif k == 'exact-snapshot':
        cond = 'snapshot-equal' if correspondence['snapshotId'] == plan_binding['snapshotId'] else 'snapshot-differs'
    else:
        pv, cv = plan_binding.get('vcsRevision'), correspondence['vcsRevision']
        if pv is None or pv['commit'] != cv['commit']:
            cond = 'commit-differs'
        elif correspondence.get('buildIdentity') is not None and correspondence['buildIdentity'] not in plan_binding.get('declaredBuildIds', []):
            cond = 'build-identity-differs'
        elif cv['dirty'] or pv['dirty']:
            cond = 'commit-equal-dirty'
        elif correspondence.get('sourceMappingDigest') and correspondence['sourceMappingDigest'] in plan_binding.get('admittedSourceMappings', []):
            cond = 'commit-equal-clean-mapped'
        else:
            cond = 'commit-equal-clean-unmapped'
    for ck, cond_, st, use in STALENESS_TABLE:
        if ck == k and cond_ == cond:
            return {'correspondenceKind': k, 'condition': cond, 'staleness': st, 'usable': use}
    raise ValueError('table gap')

def consumable_runtime_subjects(runtime_payload):
    """Runtime subjects a predicate may consume, by observation polarity. observed-hit is a POSITIVE observation
    ('this subject was executed in the window') and observable-unhit a negative one ('instrumented, never hit');
    both carry the window and population. unobservable/unmapped subjects feed neither polarity, and no window
    establishes universal non-use."""
    hit = [s['path'] for s in runtime_payload['subjects'] if s['observability'] == 'observed-hit']
    unhit = [s['path'] for s in runtime_payload['subjects'] if s['observability'] == 'observable-unhit']
    excluded = [s['path'] for s in runtime_payload['subjects'] if s['observability'] in ('unobservable', 'unmapped')]
    return {'observedHit': hit, 'observableUnhit': unhit, 'neverConsumable': excluded, 'window': runtime_payload['observationWindow'], 'population': runtime_payload['observedPopulation'], 'universalNonUse': False}

def consumable_unhit_subjects(runtime_payload):
    r = consumable_runtime_subjects(runtime_payload)
    return {'subjects': r['observableUnhit'], 'window': r['window'], 'population': r['population'], 'universalNonUse': False}

# ----------------------------------------------------------------------------- policy DSL

# Resolution order is PER-RELATION and never global. The withdrawn RES_ORDER table
# ({'syntax':0,'resolved':1,'type':2,'external':1}) was a single rank shared by every relation over
# an abstract tier vocabulary disjoint from the rung names facts actually carry -- so it could not
# even be indexed by a real fact, and its `external`/`resolved` tie was an arbitrary cross-relation
# rank of exactly the kind the inherited C-1 law forbids. The ladders below are READ from the single
# authority; this module publishes no ladder of its own.
RELATION_LADDERS = {
    name: list(row['ladder'])
    for name, row in canonical.parse(
        (Path(__file__).resolve().parent.parent / 'foundation' / 'relation-payload-schemas.v2.json').read_bytes()
    )['x-opensip-relation-registry']['relations'].items()
}
EVIDENCE_RELATIONS = canonical.parse(
    (Path(__file__).resolve().parent / 'schemas' / 'imported-evidence.schema.json').read_bytes()
)['x-opensip-evidence-relation-registry']['relations']
RELATION_LADDERS.update({name: list(row['ladder']) for name, row in EVIDENCE_RELATIONS.items()})
RUNG_VOCABULARY = {rung for ladder in RELATION_LADDERS.values() for rung in ladder}


def rung_index(relation, rung):
    """Position of `rung` in `relation`'s own ladder, or None if it is not on it.

    None is not 'weakest'. A rung of another relation is not comparable at all, and every caller
    must treat None as a refusal or an indeterminacy, never as a satisfied or failed comparison."""
    ladder = RELATION_LADDERS.get(relation)
    return None if ladder is None or rung not in ladder else ladder.index(rung)


def rung_satisfies(relation, have, need):
    """True when `have` is at least `need` on `relation`'s ladder. Raises when either rung is not a
    member: cross-relation comparison is an admission fault, not a false predicate."""
    have_i, need_i = rung_index(relation, have), rung_index(relation, need)
    if have_i is None or need_i is None:
        raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE',
                      'rung not on the ladder of relation ' + str(relation) + ': ' +
                      str(have if have_i is None else need))
    return have_i >= need_i


SEV_ORDER = {'note': 0, 'warning': 1, 'error': 2}
K_T, K_F, K_U = True, False, None

def glob_match(pattern, path):
    def seg_match(p, s):
        if p == '*':
            return True
        i = j = 0
        star = -1
        while j < len(s):
            if i < len(p) and (p[i] == '?' or p[i] == s[j]):
                i += 1; j += 1
            elif i < len(p) and p[i] == '*':
                star = i; i += 1; mark = j
            elif star >= 0:
                i = star + 1; mark += 1; j = mark
            else:
                return False
        while i < len(p) and p[i] == '*':
            i += 1
        return i == len(p)
    ps, ss = pattern.split('/'), path.split('/')
    def rec(pi, si):
        if pi == len(ps):
            return si == len(ss)
        if ps[pi] == '**':
            return any(rec(pi + 1, k) for k in range(si, len(ss) + 1))
        return si < len(ss) and seg_match(ps[pi], ss[si]) and rec(pi + 1, si + 1)
    return rec(0, 0)

def in_scope(scope, path):
    return any(glob_match(g, path) for g in scope['include']) and not any(glob_match(g, path) for g in scope['exclude'])

def admit_atom(atom, rule_id=None):
    """Close an atom's relation and rung against the two authorities.

    The schema can only say that `relation` is a canonical identifier and that `minResolution` is a
    member of the flat rung vocabulary. Neither is sufficient: the vocabulary is shared across
    relations, so a rung of `calls` reads as a perfectly well-formed value on a `declares` atom.
    Membership of THIS relation's own ladder is the actual law and is decided here."""
    relation = atom['relation']
    ladder = RELATION_LADDERS.get(relation)
    if ladder is None:
        raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE',
                      'atom names relation ' + str(relation) +
                      ', which is neither a registered native fact relation nor a registered '
                      'imported-evidence relation', rule_id)
    if atom['minResolution'] not in ladder:
        raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE',
                      'minResolution ' + str(atom['minResolution']) + ' is not a rung of the ' +
                      str(relation) + ' ladder ' + str(ladder), rule_id)
    # The two planes are separated at admission, not by convention: an evidence relation must
    # declare its kind, and a native fact relation must not claim to be imported evidence.
    evidence_row = EVIDENCE_RELATIONS.get(relation)
    if evidence_row is None:
        if atom.get('evidence') is not None:
            raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE',
                          'native fact relation ' + str(relation) + ' must not carry evidence', rule_id)
    elif atom.get('evidence') != evidence_row['evidenceKind']:
        raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE',
                      'imported-evidence relation ' + str(relation) + ' requires evidence ' +
                      evidence_row['evidenceKind'], rule_id)
    return atom


def walk_atoms(predicate, visit):
    """Apply `visit` to every atom of a predicate tree."""
    if predicate['op'] in ('and', 'or'):
        for operand in predicate['operands']:
            walk_atoms(operand, visit)
    elif predicate['op'] == 'not':
        walk_atoms(predicate['operand'], visit)
    else:
        visit(predicate)


def admit_policy_rule(rule):
    """The COMPLETE per-rule policy admission: every atom's relation and rung, AND the rule-level
    obligation that an atom consuming imported evidence is covered by an `evidenceUse` declaration.

    Factored out so the Run closure can reuse exactly this, rather than a subset. An earlier
    revision had the closure call `admit_atom` alone, so a policy whose evidence atom carried NO
    matching `evidenceUse` was refused by `resolve_policy` and yet admitted by `close_run` - the
    same document accepted at one boundary and rejected at the other. Whether an atom may consume
    imported evidence is part of whether the atom is admissible, so both boundaries must ask it."""
    declared = {u['kind'] for u in rule['evidenceUse']}
    def visit(p):
        admit_atom(p, rule['ruleId'])
        if p.get('evidence') and p['evidence'] not in declared:
            raise Refusal('CONFIG.INVALID', 'IMPORT.ABSENT_FOR_PREDICATE', 'atom uses evidence ' + p['evidence'] + ' without an evidenceUse declaration', rule['ruleId'])
    walk_atoms(rule['emitWhen'], visit)
    return rule


def resolve_policy(doc):
    ids = [r['ruleId'] for r in doc['rules']]
    if len(set(ids)) != len(ids) or ids != sorted(ids, key=lambda s: s.encode()):
        raise Refusal('CONFIG.INVALID', 'POLICY.UNKNOWN_RULE', 'ruleIds must be unique and sorted')
    for r in doc['rules']:
        admit_policy_rule(r)
    return doc

def resolve_waivers(wset, as_of):
    seen, eff, expired, dups = {}, [], [], []
    for w in wset['waivers']:
        key = canonical.canonical(w['target'])
        if key in seen:
            dups.append(w['waiverId'])
            continue
        seen[key] = w['waiverId']
        if as_of and w['expires'] is not None and w['expires'] < as_of:
            expired.append(w['waiverId'])
            continue
        eff.append(w)
    if dups:
        raise Refusal('CONFIG.INVALID', 'POLICY.DUPLICATE_WAIVER', 'remove one waiver', ','.join(dups))
    effective = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': eff}
    return effective, {'asOfDate': as_of or '0000-00-00', 'effectiveCount': len(eff), 'expired': expired, 'duplicatesRejected': dups}

def _field(fact, name):
    return fact.get(name)

def _filter_ok(fact, f):
    v = _field(fact, f['field'])
    if v is None:
        return False
    c, x = f['cmp'], f['value']
    return {'eq': lambda: v == x, 'neq': lambda: v != x, 'in': lambda: v in x, 'prefix': lambda: str(v).startswith(x), 'glob': lambda: glob_match(x, str(v)), 'gte': lambda: v >= x, 'lte': lambda: v <= x}[c]()

def eval_pred(p, subject, facts, coverage_complete, evidence_available, evidence_req):
    """Strong Kleene over the finite view. Returns True/False/None."""
    op = p['op']
    if op == 'and':
        vals = [eval_pred(o, subject, facts, coverage_complete, evidence_available, evidence_req) for o in p['operands']]
        return False if any(v is False for v in vals) else (True if all(v is True for v in vals) else None)
    if op == 'or':
        vals = [eval_pred(o, subject, facts, coverage_complete, evidence_available, evidence_req) for o in p['operands']]
        return True if any(v is True for v in vals) else (False if all(v is False for v in vals) else None)
    if op == 'not':
        v = eval_pred(p['operand'], subject, facts, coverage_complete, evidence_available, evidence_req)
        return None if v is None else (not v)
    ev = p.get('evidence')
    if ev and ev not in evidence_available:
        return None
    complete = coverage_complete
    # Ladder comparison inside ONE relation. A fact of another relation is filtered out before the
    # comparison, so no cross-relation rung is ever compared; a fact of THIS relation carrying a
    # rung that is not on this relation's ladder is an admission fault and raises.
    matches = [f for f in facts
               if f['relation'] == p['relation'] and f['subject'] == subject
               and rung_satisfies(p['relation'], f['resolution'], p['minResolution'])
               and all(_filter_ok(f, fl) for fl in p['filters'])]
    if op == 'exists':
        return True if matches else (False if complete else None)
    if op == 'none':
        return False if matches else (True if complete else None)
    if op == 'count-at-most':
        n = len({canonical.canonical(m) for m in matches})
        return False if n > p['n'] else (True if complete else None)
    if op == 'all-covered':
        return True if complete else None
    raise ValueError(op)

def evaluate(policy, scope, effective_waivers, fixture, overrides=()):
    """fixture: {'subjects': [...], 'facts': [...], 'coverage': 'complete'|'partial'|'unknown', 'evidenceAvailable': [...]} → verdict, findings, indeterminate rules, disclosures."""
    rules = {r['ruleId']: dict(r) for r in policy['rules']}
    for o in overrides:
        if o['ruleId'] in rules:
            rules[o['ruleId']][o['field']] = o['value']
    waived_keys = set()
    for w in effective_waivers['waivers']:
        t = w['target']
        waived_keys.add(('fp', t['fingerprint']) if 'fingerprint' in t else ('rs', t['ruleId'], t['subjectPath']))
    complete = fixture['coverage'] == 'complete'
    findings, indeterminate, optional_absent, advisory_only = [], [], [], True
    verdict_fail = False
    gating_indeterminate = False
    for rid in sorted(rules, key=lambda s: s.encode()):
        r = rules[rid]
        if not r['enabled']:
            continue
        req_kinds = {u['kind'] for u in r['evidenceUse'] if u['requirement'] == 'required'}
        opt_kinds = {u['kind'] for u in r['evidenceUse'] if u['requirement'] == 'optional'}
        gating = r['gate'] and SEV_ORDER[r['severity']] >= SEV_ORDER[policy['gateSeverityAtLeast']]
        if req_kinds - set(fixture['evidenceAvailable']):
            indeterminate.append(rid)
            gating_indeterminate = gating_indeterminate or gating
            continue
        rule_indet = False
        enum = r['subjectEnumeration']
        for s in fixture['subjects']:
            if not in_scope(scope, s):
                continue
            if enum.get('include') and not any(glob_match(g, s) for g in enum['include']):
                continue
            if any(glob_match(g, s) for g in enum.get('exclude', [])):
                continue
            v = eval_pred(r['emitWhen'], s, fixture['facts'], complete, set(fixture['evidenceAvailable']), req_kinds)
            if v is True:
                waived = ('rs', rid, s) in waived_keys
                findings.append({'ruleId': rid, 'subject': s, 'waived': waived})
                if gating and not waived:
                    verdict_fail = True
            elif v is None:
                rule_indet = True
        if rule_indet:
            if complete and (opt_kinds - set(fixture['evidenceAvailable'])):
                optional_absent.append(rid)  # disclosed IMPORT.ABSENT_FOR_PREDICATE; not a gating deficiency
            else:
                indeterminate.append(rid)
                gating_indeterminate = gating_indeterminate or gating
    if verdict_fail:
        verdict = 'fail'
    elif gating_indeterminate:
        verdict = 'indeterminate'
    elif any(not f['waived'] for f in findings):
        verdict = 'advisory'
    else:
        verdict = 'pass'
    return {'verdict': verdict, 'findings': findings, 'indeterminateRules': sorted(set(indeterminate)), 'optionalEvidenceAbsent': sorted(set(optional_absent))}

def run_policy_test(suite, scope=None):
    scope = scope or {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['**'], 'exclude': []}
    res = {'schemaFamily': 'opensip.product.policy-test-result', 'schemaMajor': 1, 'suiteDigest': canonical.identity('workflow.policy-test-suite', suite),
           'candidatePolicyDigest': doc_digest(suite['candidatePolicy']), 'overridesApplied': list(suite.get('overrides', [])), 'enforcementUnchanged': True, 'resolverRefusals': []}
    try:
        policy = resolve_policy(suite['candidatePolicy'])
        eff, wres = resolve_waivers(suite['waivers'], suite.get('asOfDate'))
        res['resolverAccepted'] = True
    except Refusal as r:
        res.update(resolverAccepted=False, resolverRefusals=[r.termination()['domainDetail']], effectivePolicyDigest=res['candidatePolicyDigest'],
                   waiverResolution={'asOfDate': suite.get('asOfDate', '0000-00-00'), 'effectiveCount': 0, 'expired': [], 'duplicatesRejected': [r.subject] if r.detail == 'POLICY.DUPLICATE_WAIVER' else []},
                   results=[], summary={'passed': 0, 'failed': 0, 'indeterminate': 0, 'notExecutable': 0})
        res['policyTestResultId'] = wid('policytest2', 'workflow.policy-test-result', res)
        return res, r
    eff_policy = dict(policy)
    if suite.get('overrides'):
        rules = {r['ruleId']: dict(r) for r in policy['rules']}
        for o in suite['overrides']:
            rules[o['ruleId']][o['field']] = o['value']
        eff_policy['rules'] = [rules[k] for k in sorted(rules, key=lambda s: s.encode())]
    res['effectivePolicyDigest'] = doc_digest(eff_policy)
    res['waiverResolution'] = wres
    out, summary = [], {'passed': 0, 'failed': 0, 'indeterminate': 0, 'notExecutable': 0}
    for case in suite['cases']:
        subj = case['subject']
        if subj['kind'] == 'sources':
            cr = {'id': case['id'], 'outcome': 'not-executable', 'observedVerdict': 'indeterminate', 'findings': [], 'indeterminateRules': [], 'expectationOutcomes': ['indeterminate'] * len(case['expectations'])}
            summary['notExecutable'] += 1
            out.append(cr)
            continue
        ev = evaluate(eff_policy, scope, eff, subj)
        eo = []
        for x in case['expectations']:
            if x['kind'] == 'finding':
                n = [f for f in ev['findings'] if f['ruleId'] == x['ruleId'] and (not x.get('subjects') or f['subject'] in x['subjects'])]
                ok = len(n) >= x['minCount'] and ('maxCount' not in x or len(n) <= x['maxCount'])
                eo.append('met' if ok else ('indeterminate' if x['ruleId'] in ev['indeterminateRules'] else 'unmet'))
            elif x['kind'] == 'no-finding':
                if x['ruleId'] in ev['indeterminateRules']:
                    eo.append('indeterminate')
                else:
                    eo.append('met' if not any(f['ruleId'] == x['ruleId'] for f in ev['findings']) else 'unmet')
            elif x['kind'] == 'verdict':
                eo.append('met' if ev['verdict'] == x['verdict'] else 'unmet')
            else:
                eo.append('met' if x['ruleId'] in ev['indeterminateRules'] else 'unmet')
        outcome = 'failed' if 'unmet' in eo else ('indeterminate' if 'indeterminate' in eo else 'passed')
        summary[outcome] += 1
        out.append({'id': case['id'], 'outcome': outcome, 'observedVerdict': ev['verdict'], 'findings': ev['findings'], 'indeterminateRules': ev['indeterminateRules'], 'expectationOutcomes': eo})
    res['results'], res['summary'] = out, summary
    res['policyTestResultId'] = wid('policytest2', 'workflow.policy-test-result', res)
    return res, None

# ----------------------------------------------------------------------------- repair

def fixture_tree_snapshot_id(project_id, tree):
    """SYNTHETIC fixture adapter. Produces a snapshot2 over an in-memory tree with ZERO resolvedConfig/scope/vcs digests.
    It is used only so that the repair fixtures can compare 'tree equals the evidence snapshot' by identity; it is not the
    production snapshot recipe (identity-and-evidence §2) and its ids are never presented as admitted proof."""
    inv = [{'path': p, 'sha256': raw_sha(b), 'bytes': len(b)} for p, b in sorted(tree.items(), key=lambda kv: kv[0].encode())]
    return wid('snapshot2', 'snapshot', {'schemaVersion': 2, 'projectId': project_id, 'sourceInventory': inv, 'resolvedConfigDigest': '0' * 64, 'scopeDigest': '0' * 64, 'vcsDigest': '0' * 64})

tree_snapshot_id = fixture_tree_snapshot_id
SYNTHETIC_VERIFY_PLAN = 'plan2:' + '1' * 64
SYNTHETIC_VERIFY_EVIDENCE = 'evidence2:' + '1' * 64
SYNTHETIC_VERIFY_SEAL = 'seal2:' + '1' * 64
UNSAFE_ACTIONS = {'delete', 'replace'}

def repair_preview(project_id, snapshot_tree, run, recipe, targets, edits, evidence_requirements, permitted_scope, trust, ephemeral=False):
    """trust: the security unit's current admitted closure set {closureId: 'admitted'|'revoked'}; ABSENCE is not admission.
    run carries the evidence Run's own native ClosedWorldV2 (native-evidence section 4.5, SEVEN members) and
    evidenceOrigin. The unsafe-repair gate below reads that FULL record - deadCodeRepairEligible and reasons -
    BEFORE any descriptor exists; RepairPlanDescriptor.closedWorld is the five-field PROJECTION of it, closed by
    repair.schema.json, so a literal seven-member copy is refused there and no descriptor field is the gate."""
    unmet = []
    if ephemeral or run.get('authority') != 'authoritative':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE', 'run an authoritative analysis first')
    if run.get('availability', 'retained') != 'retained' or run.get('sealedAssurance') != 'replayable':
        unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'remedy': 'restore or regenerate the Run evidence; assurance must be replayable'})
    disp = trust.get(recipe['closureId'])
    recipe_trust = 'admitted' if disp == 'admitted' else ('revoked' if disp == 'revoked' else 'not-admitted')
    if recipe_trust == 'revoked':
        unmet.append({'code': 'REPAIR.RECIPE_TRUST_REVOKED', 'remedy': 'update the recipe contribution'})
    elif recipe_trust == 'not-admitted':
        unmet.append({'code': 'REPAIR.RECIPE_TRUST_NOT_ADMITTED', 'remedy': 'install the recipe contribution under current trust; absence of a revocation is not admission'})
    for t in targets:
        if t not in run['findings']:
            raise Refusal('REQUEST.PRECONDITION_FAILED', None, 'target fingerprint not in the evidence Run', t)
    snap = fixture_tree_snapshot_id(project_id, snapshot_tree)
    if run['snapshotId'] != snap:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.SOURCE_MOVED', 'the live tree no longer equals the evidence Run snapshot')
    cw = run['closedWorld']
    origin = run.get('evidenceOrigin', 'native-analysis')
    norm = []
    for e in sorted(edits, key=lambda x: x['path'].encode()):
        if not any(glob_match(g, e['path']) for g in permitted_scope):
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.EDIT_OUTSIDE_PERMITTED_SCOPE', 'recipe emitted an edit outside its permitted scope', e['path'])
        pre = raw_sha(snapshot_tree[e['path']]) if e['path'] in snapshot_tree else None
        if e['action'] == 'create' and pre is not None or e['action'] != 'create' and pre is None:
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.TARGET_PREIMAGE_MISMATCH', 'edit action disagrees with the snapshot', e['path'])
        post = e.get('postimage')
        norm.append({'path': e['path'], 'action': e['action'], 'preimageDigest': pre, 'postimageDigest': raw_sha(post) if post is not None else None, 'postimageBytes': len(post) if post is not None else 0})
    unsafe = any(x['action'] in UNSAFE_ACTIONS for x in norm)
    if unsafe:
        if not cw['deadCodeRepairEligible']:
            unmet.append({'code': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED', 'remedy': 'native deadCodeRepairEligible is false (' + ','.join(cw.get('reasons', [])) + '); declare entry points/consumers explicitly and re-run analysis'})
        if origin == 'imported-prepared-declared':
            unmet.append({'code': 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED', 'remedy': 'an imported DECLARED prepared expansion is not authority for an unsafe repair; run native analysis or import a verified prepared set'})
    for req in evidence_requirements:
        # Repair reuses the policy rung type, so it must reuse the policy rung LAW too: sharing a
        # schema definition is not sharing an admission. An unsatisfied requirement is a reported
        # unmet precondition; a requirement whose relation or rung is not registered is a malformed
        # request and refuses, because `satisfied: false` would otherwise let an unregistered
        # relation pass as an ordinary evidence gap.
        admit_atom({'relation': req['relation'], 'minResolution': req['minResolution'],
                    'evidence': EVIDENCE_RELATIONS.get(req['relation'], {}).get('evidenceKind')})
        if not req['satisfied']:
            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'remedy': 'evidence requirement unsatisfied: ' + req['relation']})
    desc = {'schemaFamily': 'opensip.product.repair-plan', 'schemaMajor': 1, 'projectId': project_id, 'snapshotId': snap, 'evidenceRunId': run['runId'], 'planId': run['planId'], 'recipe': recipe,
            'recipeTrust': recipe_trust, 'evidenceOrigin': origin,
            # the published 7 -> 5 projection: dynamicDispatch and reasons are dropped, and the gate above
            # already consumed them, so deleting a field here can never reach an unmade decision
            'closedWorld': {k: cw[k] for k in ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized', 'nonliteralLoading', 'externalConsumers')},
            'targets': sorted(targets), 'edits': norm, 'totalPostimageBytes': sum(x['postimageBytes'] for x in norm), 'evidenceRequirements': evidence_requirements, 'permittedEditScope': sorted(permitted_scope),
            'applicable': not unmet, 'unmetPreconditions': unmet, 'limitations': ['external consumers outside the sealed snapshot are not observed']}
    return {'repairPlanId': wid('repairplan2', 'workflow.repair-plan', desc), 'descriptor': desc}

def _receipt(request_id, step_id, execution_id, idem, plan, d, outcome, file_outcomes, rollback, detail=None, applied=None):
    r = {'schemaFamily': 'opensip.product.mutation-receipt', 'schemaMajor': 1, 'requestId': request_id, 'stepId': step_id, 'executionId': execution_id, 'operation': 'repair-apply', 'idempotencyKey': idem,
         'effectOutcome': outcome, 'commitClass': 'REVERSIBLE', 'replayed': False, 'repairPlanId': plan['repairPlanId'], 'baseSnapshotId': d['snapshotId'], 'fileOutcomes': file_outcomes, 'rollback': rollback}
    if applied:
        r['appliedSnapshotId'] = applied
    if detail:
        r['domainDetail'] = detail
    r['receiptId'] = wid('receipt2', 'workflow.mutation-receipt', r)
    return r

def repair_apply(plan, postimages, live_tree, project_id, request_id, step_id, authorization, ci, consent, receipts, trust, preimage_store, fault_after_renames=None, corrupt_path=None):
    """Journaled apply over an in-memory tree. authorization: {'repairPlanId','snapshotId','projectId','live': bool} or None
    (live=False models a revocation observed at the broker checkpoint). trust: current admitted closure set re-read at the
    broker linearization point. preimage_store: digest -> bytes, the retained preimage blobs written before STAGED.
    Returns (journal, receipt, tree)."""
    d = plan['descriptor']
    execution_id = synthetic_execution_id(request_id, step_id, 1)
    journal = {'schemaFamily': 'opensip.product.repair-apply-journal', 'schemaMajor': 1, 'requestId': request_id, 'stepId': step_id, 'executionId': execution_id, 'repairPlanId': plan['repairPlanId'],
               'baseSnapshotId': d['snapshotId'], 'authorizationRef': authorization['securityAuthorizationRef'] if authorization else 'security.repair-apply-authorization.v1:' + '0' * 64, 'state': 'PREPARING', 'stagedPaths': [], 'appliedPaths': [], 'preimageBlobs': []}
    idem = raw_sha(canonical.canonical({'operation': 'repair-apply', 'projectId': project_id, 'repairPlanId': plan['repairPlanId'], 'baseSnapshotId': d['snapshotId']}))
    prior = receipts.get(idem)
    if prior and prior['effectOutcome'] == 'COMPLETED':
        rc = dict(prior); rc['replayed'] = True; rc['requestId'] = request_id; rc['stepId'] = step_id; rc['executionId'] = execution_id
        rc.pop('receiptId'); rc['receiptId'] = wid('receipt2', 'workflow.mutation-receipt', rc)
        journal['state'] = 'COMMITTED'; journal['appliedSnapshotId'] = prior['appliedSnapshotId']
        return journal, rc, live_tree
    if not d['applicable']:
        raise Refusal('REQUEST.PRECONDITION_FAILED', d['unmetPreconditions'][0]['code'], d['unmetPreconditions'][0]['remedy'])
    if authorization is None or authorization.get('repairPlanId') != plan['repairPlanId'] or authorization.get('snapshotId') != d['snapshotId'] or authorization.get('projectId') != project_id:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.CONSENT_NOT_BOUND', 'authorization must bind this exact repairPlanId, snapshotId and projectId')
    if authorization.get('consentSource') != consent or authorization.get('ci') is not ci:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.CONSENT_NOT_BOUND', 'repair consent source and CI must equal the admitted security projection')
    if ci and consent != 'policy':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.CONSENT_NOT_BOUND', 'CI requires policy consent')
    if fixture_tree_snapshot_id(project_id, live_tree) != d['snapshotId']:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.TARGET_PREIMAGE_MISMATCH', 're-run repair preview on the current snapshot')
    # STAGED: retained preimage blobs, temp writes + preimage re-verification
    for e in d['edits']:
        pre = raw_sha(live_tree[e['path']]) if e['path'] in live_tree else None
        if pre != e['preimageDigest']:
            journal['state'] = 'FAILED_CLEAN'
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.TARGET_PREIMAGE_MISMATCH', 're-run repair preview on the current snapshot', e['path'])
        if e['action'] != 'delete' and raw_sha(postimages[e['path']]) != e['postimageDigest']:
            journal['state'] = 'FAILED_CLEAN'
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'IMPORT.ARTIFACT_CORRUPT', 'postimage bytes do not match the plan', e['path'])
        if pre is not None:
            preimage_store[pre] = live_tree[e['path']]
            journal['preimageBlobs'].append({'path': e['path'], 'sha256': pre, 'bytes': len(live_tree[e['path']])})
        journal['stagedPaths'].append(e['path'])
    journal['state'] = 'STAGED'
    # broker linearization checkpoint: current trust and live authorization re-read before the first rename
    if trust.get(d['recipe']['closureId']) != 'admitted':
        journal['state'] = 'FAILED_CLEAN'
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.RECIPE_TRUST_REVOKED' if trust.get(d['recipe']['closureId']) == 'revoked' else 'REPAIR.RECIPE_TRUST_NOT_ADMITTED', 'recipe closure is not admitted under current trust at apply time')
    if not authorization.get('live', True):
        journal['state'] = 'FAILED_CLEAN'
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.CONSENT_NOT_BOUND', 'authorization was revoked before the first rename')
    tree = dict(live_tree)
    journal['state'] = 'APPLYING'
    file_outcomes = []
    for i, e in enumerate(d['edits']):
        if fault_after_renames is not None and i >= fault_after_renames:
            j2, action, outcome, term = _repair_recover_action(journal, plan, tree if corrupt_path is None else dict(tree, **{corrupt_path: b'\x00corrupt'}), project_id, preimage_store)
            tree = j2.pop('_tree', tree)
            journal.update({k: v for k, v in j2.items() if not k.startswith('_')})
            journal['faultCause'] = 'host-io'
            blocked = journal.get('blockedPaths', [])
            for e2 in d['edits']:
                st = 'blocked' if e2['path'] in blocked else ('restored' if e2['path'] in journal['appliedPaths'] else 'untouched')
                file_outcomes.append({'path': e2['path'], 'before': e2['preimageDigest'], 'after': raw_sha(tree[e2['path']]) if e2['path'] in tree else None, 'state': st})
            detail = {'code': 'REPAIR.RECOVERY_BLOCKED', 'remedy': 'inspect the listed paths; the journal is retained'} if blocked else {'code': 'REPAIR.SOURCE_MOVED', 'remedy': 'no target byte remains changed'}
            receipt = _receipt(request_id, step_id, execution_id, idem, plan, d, outcome, file_outcomes, 'blocked' if blocked else 'completed', detail)
            receipts[idem] = receipt
            return journal, receipt, tree
        if e['action'] == 'delete':
            tree.pop(e['path'])
        else:
            tree[e['path']] = postimages[e['path']]
        journal['appliedPaths'].append(e['path'])
    journal['state'] = 'APPLIED'
    applied = fixture_tree_snapshot_id(project_id, tree)
    journal.update(state='COMMITTED', appliedSnapshotId=applied)
    for e in d['edits']:
        file_outcomes.append({'path': e['path'], 'before': e['preimageDigest'], 'after': e['postimageDigest'], 'state': 'applied'})
    receipt = _receipt(request_id, step_id, execution_id, idem, plan, d, 'COMPLETED', file_outcomes, 'not-needed', applied=applied)
    receipts[idem] = receipt
    return journal, receipt, tree

RECOVERY_TABLE = {
    'PREPARING': ('discard-temps', 'FAILED_CLEAN', 'FAILED'), 'STAGED': ('discard-temps', 'FAILED_CLEAN', 'FAILED'), 'APPLYING': ('roll-back-renamed', 'FAILED_ROLLED_BACK', 'FAILED'),
    'APPLIED': ('verify-postimages-and-commit', 'COMMITTED', 'COMPLETED'), 'COMMITTED': ('none', 'COMMITTED', 'COMPLETED'), 'FAILED_CLEAN': ('none', 'FAILED_CLEAN', 'FAILED'),
    'FAILED_ROLLED_BACK': ('none', 'FAILED_ROLLED_BACK', 'FAILED'), 'RECOVERY_BLOCKED': ('refuse', 'RECOVERY_BLOCKED', 'INDETERMINATE'), 'INDETERMINATE': ('verify-postimages-and-commit', 'COMMITTED', 'COMPLETED'),
}
MUTATING_RECOVERY = {'discard-temps', 'roll-back-renamed', 'verify-postimages-and-commit'}
_BLOCKED_TERM = {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'domainDetail': {'code': 'REPAIR.RECOVERY_BLOCKED', 'remedy': 'inspect the listed paths manually; the journal is retained'}}

def repair_inspect(journal, plan, live_tree):
    """Read-only recovery inspection: journal integrity and per-path digest comparison. Needs no authorization; mutates nothing."""
    d = plan['descriptor']
    edits = {x['path']: x for x in d['edits']}
    integrity = journal['repairPlanId'] == plan['repairPlanId'] and set(journal['appliedPaths']) <= set(journal['stagedPaths']) <= set(edits) and all(p in edits for p in journal['appliedPaths'])
    rows = []
    for p, e in edits.items():
        cur = raw_sha(live_tree[p]) if p in live_tree else None
        rows.append({'path': p, 'current': cur, 'preimage': e['preimageDigest'], 'postimage': e['postimageDigest'], 'atPreimage': cur == e['preimageDigest'], 'atPostimage': cur == e['postimageDigest'], 'applied': p in journal['appliedPaths']})
    return {'state': journal['state'], 'journalIntegrity': integrity, 'plannedAction': RECOVERY_TABLE[journal['state']][0], 'paths': sorted(rows, key=lambda r: r['path'].encode())}

def recovery_journal_bindings(journal):
    """Exact shared security S10.2 preimages; no authority is minted by these identities."""
    keys = ('schemaFamily', 'schemaMajor', 'requestId', 'stepId', 'executionId', 'repairPlanId', 'baseSnapshotId', 'authorizationRef')
    identity = 'security.repair-apply-journal-identity.v1:' + canonical.identity('security.repair-apply-journal-identity.v1', {k: journal[k] for k in keys})
    state = {'state': journal['state'], 'stagedPaths': journal.get('stagedPaths', []), 'appliedPaths': journal.get('appliedPaths', []), 'preimageBlobs': journal.get('preimageBlobs', [])}
    return identity, raw_sha(canonical.canonical(state))


def repair_recover(journal, plan, live_tree, project_id, preimage_store=None, recovery_authorization=None):
    """Closed recovery table. Inspection is read-only; any mutating action needs recovery_authorization bound to this journal's
    exact plan, journal identity/state, project, action and full security authorization reference (REPAIR.RECOVERY_NOT_AUTHORIZED otherwise). Returns (journal', action, receiptOutcome, termination);
    journal'['_tree'] carries the restored tree when bytes were actually restored."""
    validate_import_record('workflows/schemas/repair.schema.json', '#/$defs/RepairApplyJournalV1', journal)
    validate_import_record('workflows/schemas/repair.schema.json', '#/$defs/RepairPlanV1', plan)
    action, result_state, outcome = RECOVERY_TABLE[journal['state']]
    d = plan['descriptor']
    j = dict(journal)
    insp = repair_inspect(journal, plan, live_tree)
    if plan['repairPlanId'] != wid('repairplan2', 'workflow.repair-plan', d):
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.RECOVERY_NOT_AUTHORIZED', 'repair plan identity mismatch')
    if action in MUTATING_RECOVERY:
        journal_ref, state_digest = recovery_journal_bindings(journal)
        g = recovery_authorization
        bound = g is not None and g.get('result') == 'ADMIT' and g.get('repairPlanId') == plan['repairPlanId'] \
            and g.get('originalRequestId') == journal['requestId'] and g.get('projectId') == project_id \
            and g.get('baseSnapshotId') == journal['baseSnapshotId'] == d['snapshotId'] \
            and g.get('journalRef') == journal_ref and g.get('journalStateDigest') == state_digest and g.get('recoveryAction') == action
        if not bound:
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.RECOVERY_NOT_AUTHORIZED', 'recovery mutation needs fresh security admission bound to this exact journal, observed state, action and project; inspection is read-only')
        validate_import_record('workflows/schemas/common.schema.json', '#/$defs/RepairRecoveryAuthorizationRef', g.get('securityRecoveryAuthorizationRef'))
        j['recoveryAuthorizationRef'] = g['securityRecoveryAuthorizationRef']
    return _repair_recover_action(j, plan, live_tree, project_id, preimage_store)


def _repair_recover_action(journal, plan, live_tree, project_id, preimage_store):
    """Internal broker mechanics, entered only from an admitted recovery or compensation
    within the still-running apply attempt. The latter retains its original apply authority
    and does not manufacture a fresh recovery grant. Never a public request entry point.
    """
    action, result_state, outcome = RECOVERY_TABLE[journal['state']]
    d = plan['descriptor']; j = dict(journal)
    insp = repair_inspect(journal, plan, live_tree)
    if d['projectId'] != project_id:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.RECOVERY_NOT_AUTHORIZED', 'repair belongs to another project')
    if not insp['journalIntegrity']:
        j.update(state='RECOVERY_BLOCKED', blockedPaths=sorted(set(journal['appliedPaths']) - {x['path'] for x in d['edits']}, key=lambda s: s.encode()) or [x['path'] for x in d['edits']][:1])
        return j, 'refuse', 'INDETERMINATE', _BLOCKED_TERM
    edits = {x['path']: x for x in d['edits']}
    if action == 'roll-back-renamed':
        tree = dict(live_tree)
        # Check every retained byte before the first restore, including paths later
        # in the sequence. A digest-key lookup alone does not establish integrity.
        for p in j['appliedPaths']:
            e = edits[p]
            digest = e['preimageDigest']
            if digest is not None and preimage_store is not None and digest in preimage_store and raw_sha(preimage_store[digest]) != digest:
                j.update(state='RECOVERY_BLOCKED', blockedPaths=[p], _tree=dict(live_tree))
                return j, 'refuse', 'INDETERMINATE', {'class': 'operational-failed', 'errorCode': 'LEDGER.CORRUPT', 'faultCause': 'ledger-corrupt', 'domainDetail': {'code': 'REPAIR.PREIMAGE_CORRUPT', 'remedy': 'restore the exact retained preimage blob before recovery; no target was changed'}}
        blocked, restored = [], []
        for p in j['appliedPaths']:
            e = edits[p]
            cur = raw_sha(tree[p]) if p in tree else None
            if cur == e['preimageDigest']:
                continue  # already at preimage (crash after restore); nothing to do
            if cur != e['postimageDigest']:
                blocked.append(p)
                continue
            if e['preimageDigest'] is None:
                tree.pop(p, None); restored.append(p)
            elif preimage_store is not None and e['preimageDigest'] in preimage_store:
                tree[p] = preimage_store[e['preimageDigest']]; restored.append(p)
            else:
                j.update(state='APPLYING', restoreIntent=[{'path': q, 'restoreDigest': edits[q]['preimageDigest']} for q in j['appliedPaths']])
                return j, 'requires-broker', 'INDETERMINATE', {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE', 'faultCause': 'host-io', 'domainDetail': {'code': 'REPAIR.RECOVERY_REQUIRES_BROKER', 'remedy': 'the retained preimage blob is not readable here; the exact restore intent is returned and nothing was changed'}}
        if blocked:
            j.update(state='RECOVERY_BLOCKED', blockedPaths=sorted(blocked, key=lambda s: s.encode()))
            j['_tree'] = tree
            return j, 'refuse', 'INDETERMINATE', _BLOCKED_TERM
        j['state'] = result_state
        j['_tree'] = tree
        return j, action, outcome, {'class': 'success'}
    if action == 'refuse':
        return j, action, outcome, _BLOCKED_TERM
    if action == 'verify-postimages-and-commit':
        unexpected = []
        for p, e in edits.items():
            cur = raw_sha(live_tree[p]) if p in live_tree else None
            if cur != e['postimageDigest']:
                unexpected.append(p)
        if unexpected or set(j['appliedPaths']) != set(edits):
            j.update(state='RECOVERY_BLOCKED', blockedPaths=sorted(unexpected or list(set(edits) - set(j['appliedPaths'])), key=lambda s: s.encode()))
            return j, 'refuse', 'INDETERMINATE', _BLOCKED_TERM
        j.update(state='COMMITTED', appliedSnapshotId=fixture_tree_snapshot_id(project_id, live_tree))
        return j, action, outcome, {'class': 'success'}
    j['state'] = result_state
    return j, action, outcome, {'class': 'success'}

def repair_verify(receipt, live_tree, project_id, verify_findings_remaining, net_new, request_id='req1_' + '0' * 32, step_id=3):
    """Fresh snapshot after apply; seals a new authoritative Run (SYNTHETIC placeholder plan/evidence/seal ids) and returns
    (AnalysisResult, VerificationLinkV1). The apply receipt is never modified."""
    fresh = fixture_tree_snapshot_id(project_id, live_tree)
    if receipt['effectOutcome'] != 'COMPLETED':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'apply did not complete')
    if fresh != receipt['appliedSnapshotId']:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'REPAIR.SOURCE_MOVED', 'the tree changed after apply; re-run analysis instead of verify')
    run_id = wid('run2', 'run', {'schemaVersion': 2, 'projectId': project_id, 'snapshotId': fresh, 'planId': SYNTHETIC_VERIFY_PLAN, 'evidenceId': SYNTHETIC_VERIFY_EVIDENCE, 'evaluationSealId': SYNTHETIC_VERIFY_SEAL, 'capabilityManifestId': '1' * 64})
    verdict = 'fail' if net_new else ('advisory' if verify_findings_remaining else 'pass')
    result = {'kind': 'verify', 'authority': 'authoritative', 'runId': run_id, 'planId': SYNTHETIC_VERIFY_PLAN, 'verdict': verdict, 'requiredCoverage': 'satisfied', 'durability': 'committed', 'deficiency': 'none', 'secondaryDeficiencies': [],
              'verification': {'appliedSnapshotId': receipt['appliedSnapshotId'], 'verifiedSnapshotId': fresh, 'snapshotMatched': True, 'targetsRemaining': verify_findings_remaining, 'netNewFindings': net_new}}
    link = {'schemaFamily': 'opensip.product.verification-link', 'schemaMajor': 1, 'receiptId': receipt['receiptId'], 'verificationRunId': run_id, 'appliedSnapshotId': receipt['appliedSnapshotId'], 'verifiedSnapshotId': fresh, 'requestId': request_id, 'stepId': step_id}
    link['linkId'] = wid('receipt2', 'workflow.verification-link', link)
    return result, link

# ----------------------------------------------------------------------------- test execution

import re as _re
ENV_RE = _re.compile(r'^[A-Z_][A-Z0-9_]*$')
PLATFORMS = ('macos-aarch64', 'macos-x86_64', 'linux-x86_64-gnu', 'linux-aarch64-gnu')

def admit_test_execution(params, ctx):
    """ctx: {'ci', 'projectId', 'snapshotId', 'grant': security RepoExecutionGrantV2 admission projection or None,
    'snapshotMembers': [...], 'toolchainMembers': {closureId: [tree paths]}, 'truthTable': {platformId: {effect: value}}, 'liveEqualsAfterStep': bool}.
    The grant is a trusted model input (the security model is not re-run). It must bind project, snapshot, argv digest, execution class
    and the exact program (snapshot member, or toolchain closure + member); every effect value must EQUAL the truth-table row."""
    validate_import_record('workflows/schemas/test-execution.schema.json', '#/$defs/TestExecutionStepParams', params)
    if params['principal'] != 'P-TRUSTED-REPO' or params['executionClass'] != 'test-runner':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.PRINCIPAL_NOT_ADMITTED', 'test execution requires the trusted-repository-code principal, class test-runner')
    if ctx['ci'] and params['consentSource'] != 'pre-existing-policy':
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.INTERACTIVE_CONSENT_IN_CI', 'record a policy authorization bound to the argv digest before CI')
    src = params['argv0Source']
    program = src['path'] if src['kind'] == 'snapshot-member' else src['closureId'] + '#' + src['member']
    g = ctx.get('grant')
    argv_digest = raw_sha(canonical.canonical(params['argv']))
    bound = g is not None and g.get('result') == 'ADMIT' and g.get('principalClass') == 'repository-code' and g.get('executionClass') == 'test-runner' \
        and g.get('projectId') == ctx.get('projectId') and g.get('snapshotId') == ctx.get('snapshotId') and g.get('argvDigest') == argv_digest \
        and program in g.get('programs', []) and g.get('expiry') == 'operation-end' and not g.get('inherited') and g.get('platformId') == params['platformId'] \
        and g.get('securityGrantRef') == params.get('authorizationRef') and g.get('consentSource') == params['consentSource']
    if not bound:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.PRINCIPAL_NOT_ADMITTED', 'no admitted grant bound to this project, snapshot, argv digest, execution class, program and platform')
    if src['kind'] == 'snapshot-member':
        if src['path'] not in ctx['snapshotMembers'] or params['argv'][0] != src['path']:
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.ARGV_NOT_IN_CLOSURE', 'argv[0] must be a sealed snapshot member or a toolchain closure member')
    else:
        members = ctx['toolchainMembers'].get(src['closureId'], [])
        if src['member'] not in members or params['argv'][0] != src['member'] or src['closureId'] != g.get('toolchainClosureId'):
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.ARGV_NOT_IN_CLOSURE', 'argv[0] must be byte-equal to an inventoried member of the grant-declared toolchain closure; aliases and PATH lookups are refused')
    for v in params['environmentAllowlist']:
        if not ENV_RE.match(v) or v == 'PATH':
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.ENV_NOT_ALLOWLISTED', 'PATH is never copied; names must match the allowlist grammar', v)
    row = ctx['truthTable'].get(params['platformId'])
    if row is None:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.CONFINEMENT_CLAIM_REFUSED', 'no truth-table row for platform ' + params['platformId'])
    for effect, val in params['effects'].items():
        if val != row.get(effect):
            raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.CONFINEMENT_CLAIM_REFUSED', 'effect value must equal the security truth table exactly (' + str(row.get(effect)) + ')', effect)
    if g.get('effects') != params['effects']:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.CONFINEMENT_CLAIM_REFUSED', 'grant effects differ from the step effects')
    if not ctx['liveEqualsAfterStep']:
        raise Refusal('REQUEST.PRECONDITION_FAILED', 'TEST.SOURCE_MOVED', 'the live tree no longer equals the afterStep snapshot')
    return {'admitted': True, 'disclosure': 'Repository test command will run with your user authority. OpenSIP does not prevent network access or other effects on this platform.', 'confinementClaimed': False, 'securityGrantRef': g.get('securityGrantRef')}

def test_payload(params, exit_status, stdout, stderr, timed_out=False, signal=None, max_out=None, tool_closure=None):
    trunc = max_out is not None and (len(stdout) > max_out or len(stderr) > max_out)
    return {'payloadDomain': 'workflow.import-payload.test.v1', 'producer': 'host-test-execution', 'argvDigest': raw_sha(canonical.canonical(params['argv'])), 'toolClosureId': tool_closure,
            'exitStatus': exit_status, 'signal': signal, 'timedOut': timed_out, 'stdoutDigest': raw_sha(stdout), 'stderrDigest': raw_sha(stderr), 'stdoutBytes': len(stdout), 'stderrBytes': len(stderr),
            'outputTruncated': trunc, 'tests': [], 'selection': {'mode': 'full', 'completenessEstablished': False}}

# ----------------------------------------------------------------------------- rendering / parity

def render(envelope, fmt, command):
    formats = command['formats']
    if fmt not in formats:
        raise Refusal('REQUEST.UNKNOWN_OPTION', 'OUTPUT.FORMAT_NOT_APPLICABLE', 'use one of ' + ','.join(formats))
    # Presence in the envelope does NOT make a field part of declared parity: render selects only the
    # command's declared parityFields. `capability-availability` is declared for the analysis commands so the
    # release-availability account reaches human, SARIF and HTML too, not only the JSON/agent envelope.
    #
    # Access is STRICT and deliberately so. An earlier revision guarded this with `if k in envelope['parity']`
    # so an old fixture would keep passing, and that silently weakened the inherited required-field behavior for
    # EVERY declared parity field: a missing required-coverage simply vanished from all five formats instead of
    # failing. Section 8 is explicit - a missing field or projection exception is a required-delivery operational
    # fault, never a successful partial rendering - and it also says this KeyError alone is not a public
    # termination: the host converts it to operational-failed / DELIVERY.REQUIRED_FAILED with
    # faultCause=delivery-required, retaining a committed RunId. A caller with no selection supplies the explicit
    # empty availability value rather than omitting the field.
    parity = {k: envelope['parity'][k] for k in command['parityFields']}
    if fmt == 'json':
        return {'format': 'json', 'parity': parity, 'envelope': envelope['envelope']}
    if fmt == 'agent':
        return {'format': 'agent', 'parity': parity, 'envelope': envelope['envelope'], 'agentHints': envelope.get('hints', [])}
    if fmt == 'sarif':
        return {'format': 'sarif', 'parity': parity, 'results': parity['findings'], 'runProperties': {'verdict': parity['verdict'], 'deficiency': parity['deficiency']}}
    if fmt == 'html':
        return {'format': 'html', 'parity': parity, 'static': True, 'scriptFetched': False}
    return {'format': 'human', 'parity': parity, 'lines': [k + ': ' + canonical.canonical(v).decode() for k, v in sorted(parity.items())]}

def parity_holds(renderings):
    ps = [canonical.canonical(r['parity']) for r in renderings]
    return all(p == ps[0] for p in ps)

# ----------------------------------------------------------------------------- review

def candidates_from_run(run_id, findings, advisory, dispositions, today, project_id):
    """findings: [{fingerprint, ruleId, gating, subjectPath}]; advisory: [{kind, subjectPath, evidenceLevel}]; dispositions: {candidateId: ReviewDisposition+receiptId}."""
    out = []
    for f in findings:
        cid = wid('candidate2', 'workflow.candidate', {'projectId': project_id, 'kind': 'finding', 'key': f['fingerprint']})
        c = {'candidateId': cid, 'runId': run_id, 'kind': 'finding', 'fingerprint': f['fingerprint'], 'ruleId': f['ruleId'], 'evidenceLevel': 'proof-backed', 'subjectPath': f['subjectPath'], 'controlBearing': bool(f['gating']), 'suppressed': False}
        out.append(c)
    for a in advisory:
        cid = wid('candidate2', 'workflow.candidate', {'projectId': project_id, 'kind': a['kind'], 'key': a['sourceFingerprint']})
        out.append({'candidateId': cid, 'runId': run_id, 'kind': a['kind'], 'evidenceLevel': a['evidenceLevel'], 'subjectPath': a['subjectPath'], 'controlBearing': False, 'suppressed': False})
    for c in out:
        d = dispositions.get(c['candidateId'])
        if d and d['disposition'] in ('reject', 'defer'):
            if d['suppressUntil'] is None or d['suppressUntil'] >= today:
                c['suppressed'] = True
                c['suppressedBy'] = d['receiptId']
            else:
                c['previouslyReviewed'] = True
    return sorted(out, key=lambda c: c['candidateId'])

def review_join(candidate_id, disposition, reviewer, note, today, until):
    try:
        _days(today)
        if until is not None: _days(until)
    except ValueError as exc:
        raise Refusal('CONFIG.INVALID', 'REVIEW.ADVISORY_ONLY', 'review dates must be valid calendar dates') from exc
    if disposition == 'accept':
        until = None
    elif until is None:
        raise Refusal('CONFIG.INVALID', 'REVIEW.ADVISORY_ONLY', 'reject/defer suppression requires an expiry within 365 days')
    if until is not None and (until < today or _days(until) - _days(today) > 365):
        raise Refusal('CONFIG.INVALID', 'REVIEW.ADVISORY_ONLY', 'suppressUntil must be within 365 days')
    return {'candidateId': candidate_id, 'disposition': disposition, 'reviewer': reviewer, 'note': note, 'suppressUntil': until, 'advisory': True}

def _days(d):
    from datetime import date
    return date.fromisoformat(d).toordinal()

def review_brief(run_id, candidate_ids, producer, limit=1000):
    ids = [c for c in candidate_ids]
    return {'runId': run_id, 'candidates': ids[:limit], 'producer': producer, 'advisory': True, 'truncated': len(ids) > limit}

# ----------------------------------------------------------------------------- doctor

def doctor(store_openable, defects):
    if not store_openable:
        return {'kind': 'doctor', 'reportProduced': False, 'defectsFound': 0, 'defects': []}, terminate({'event': 'doctor-report', 'reportProduced': False})
    return {'kind': 'doctor', 'reportProduced': True, 'defectsFound': len(defects), 'defects': defects}, terminate({'event': 'doctor-report', 'reportProduced': True, 'defectsFound': len(defects)})
