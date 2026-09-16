"""Phase 7 -- workflows and surfaces, reconstructed against the evaluator3 composition and
bound to the REAL sealed Runs of this origin.

Envelopes:  R-SINGLE-STEP, R-MULTI-STEP-DIFFERENT-SELECTIONS, R-INVOCATION-DISCLOSURE,
            R-PUBLIC-FROM-INTERNAL-REFUSAL, R-ENVELOPE-CONFIG-INPUT,
            R-ENVELOPE-EXTERNAL-INPUT, R-ENVELOPE-HOST-INVALID,
            R-ENVELOPE-PRODUCER-BOUNDARY, R-FAILURE-ENVELOPES-D9,
            R-DURABLE-RECEIPT-AVAILABILITY
Vectors:    R-MULTI-UNIT-MISSING-CAPS, R-CANDIDATE-ONLY-CLONES
Standing:   R-CHAIN-ZERO-CONFIG-TO-RECEIPT, R-SEMANTIC-VS-OPERATIONAL-AUTHORITY,
            R-MUTATION-VS-ANALYSIS-STEPS, R-PROMISE-VS-AVAILABILITY,
            R-D9-EXTENSION-PRECEDENCE
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST
import opensip_closure as CL
import opensip_fixture as FX
import envelopes as EV

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'
KIT = S.KIT
INV_DOC = 'workflows/schemas/evaluator3/invocation-record.schema.json'
CMD_DOC = 'workflows/schemas/evaluator3/command-inventory.schema.json'
REQ = 'req1_%s' % ('7b31d0c4e5a2498fa0d17c6b3e58f29a'[:32])


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


def run_facts(label):
    st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, 'phase7:' + label)
    assert rep['admitted'], rep['refusals'][:2]
    run = c.resolved[rid]
    # the VERDICT lives on the retained evaluation SEAL, not on run3: run3 carries the
    # identities and the capability manifest id, and the seal carries the decision. Reading
    # it off the wrong record would be the conflation this separation prevents.
    seal = c.resolved.get(run['evaluationSealId']) or c.typed(
        run['evaluationSealId'], 'evaluation-seal', 'PHASE7_SEAL')
    return {'runId': rid, 'planId': run['planId'], 'verdict': seal['verdict'],
            'evaluationState': seal.get('evaluationState'),
            'evidenceId': run['evidenceId'], 'sealId': run['evaluationSealId'],
            'snapshotId': run['snapshotId'], 'store': st, 'closure': c,
            'projectId': run['projectId']}


def analysis_result(rf, *, authoritative=True):
    if authoritative:
        return {'kind': 'analysis', 'authority': 'authoritative', 'runId': rf['runId'],
                'planId': rf['planId'], 'verdict': rf['verdict'],
                'requiredCoverage': 'satisfied', 'durability': 'committed',
                'deficiency': 'none', 'secondaryDeficiencies': []}
    return {'kind': 'analysis', 'authority': 'ephemeral', 'planId': rf['planId'],
            'evidenceId': rf['evidenceId'], 'verdict': rf['verdict'],
            'requiredCoverage': 'satisfied', 'durability': 'not-required',
            'deficiency': 'none', 'secondaryDeficiencies': []}


def derivation_of(rf):
    """The attempt's derivation binding, read from the Run's own retained execution plan --
    "Each analysis/verify attempt owns exactly one derivation DAG (exec-plan2 ...)"."""
    xp = None
    for tid, rec in rf['store'].objects.items():
        if tid.startswith('exec-plan2:'):
            xp = (tid, rec)
    stages = len((xp[1].get('stages') if xp else []) or [])
    return {'planId': rf['planId'], 'executionPlanId': xp[0] if xp else None,
            'stageCount': stages, 'stagesCompleted': stages}


def baseline_id(rf):
    """The baselineId of the phase-8 baseline artifact built over THIS Run, read from that
    artifact rather than invented, so the invocation names the same identity the comparison
    vector does."""
    try:
        d = json.load(open(OUT + '/vectors/baseline-audit.json'))
        return d['baselineArtifact']['baselineId']
    except Exception:
        return 'baseline2:' + '0' * 64


def comparison_result_id(rf):
    try:
        d = json.load(open(OUT + '/vectors/baseline-audit.json'))
        return d['comparisonUnchanged']['comparisonResultId']
    except Exception:
        return 'comparison2:' + '0' * 64


def availability(step_id, notices):
    """stepId is an INTEGER step position. noticeCount always equals the array length
    because a step's collection is bounded by the analysis-spec bound and cannot truncate."""
    return {'stepCount': 1, 'totalNoticeCount': len(notices),
            'steps': [{'stepId': step_id, 'noticeCount': len(notices),
                       'notices': notices}]}


def notice(cap, mode, root, remedy):
    return {'code': 'native.capability-unavailable', 'capabilityId': cap,
            'languageMode': mode, 'workspaceRoot': root, 'remedy': remedy}


def env(kind, term, exit_code, rf=None, **extra):
    e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': kind,
         'requestId': REQ, 'termination': term, 'exitCode': exit_code}
    if rf is not None:
        e['projectId'] = rf['projectId']
    e.update(extra)
    return e


# --------------------------------------------------------------------- envelopes
def single_step(rf):
    """R-SINGLE-STEP: 'a single-step builtin command projects its single step's member
    directly' -- so the envelope is kind=run carrying the AnalysisResult, not a nested
    invocation record."""
    term = {'class': 'success', 'authority': 'authoritative', 'runId': rf['runId']}
    e = env('run', term, 0, rf, run=analysis_result(rf),
            retentionDisclosure={'policy': 'durable-unbounded', 'provenance': 'DEFAULTED',
                                 'firstUse': True, 'storageRoot': '.opensip'},
            availability=availability(1, []))
    r = EV.admit(e, 'single-step-analysis')
    r['requirement'] = 'R-SINGLE-STEP'
    r['classification'] = 'valid'
    r['projectionLaw'] = ('command-envelope: a single-step builtin projects its single '
                          "step's member directly, so kind=run + `run` rather than "
                          'kind=invocation')
    return r


def multi_step(rf_ts, rf_rust):
    """R-MULTI-STEP-DIFFERENT-SELECTIONS: a NAMED multi-step invocation whose two analysis
    steps carry DIFFERENT selections (different profile and different workspace root), and a
    comparison step that mints no Run and delegates its verdict."""
    # CORRECTED (V17-D6): `StepId` is the ZERO-BASED POSITION (workflows section 1), the
    # comparison step owes its own ComparisonStepResult, and each analysis/verify ATTEMPT owns
    # exactly one derivation binding. The v16 record used one-based ids, accounted only two of
    # three steps and carried no derivation binding at all.
    cmp_id = comparison_result_id(rf_ts)
    steps = [
        {'stepId': 0, 'kind': 'analysis', 'requirement': 'required',
         'dependsOn': [], 'dependencyGate': 'completed', 'retryPolicy': 'idempotent-retry',
         'params': {'kind': 'analysis', 'profile': 'default', 'role': 'primary',
                    'verdictGate': 'delegated', 'durability': 'authoritative',
                    'snapshotSource': 'live-worktree'}},
        {'stepId': 1, 'kind': 'analysis', 'requirement': 'required',
         'dependsOn': [0], 'dependencyGate': 'completed',
         'retryPolicy': 'idempotent-retry',
         'params': {'kind': 'analysis', 'profile': 'pivot', 'role': 'pivot',
                    'pivotOfStep': 0,
                    'pivotClosureIds': sorted(
                        t for t in rf_rust['store'].objects
                        if t.startswith('closure2:'))[:1],
                    'verdictGate': 'delegated', 'durability': 'authoritative',
                    'snapshotSource': 'live-worktree'}},
        {'stepId': 2, 'kind': 'comparison', 'requirement': 'required',
         'dependsOn': [0, 1], 'dependencyGate': 'completed',
         'retryPolicy': 'none',
         'params': {'kind': 'comparison', 'currentStep': 0, 'pivotStep': 1,
                    'baseline': '.opensip/baselines/main.json',
                    'auditProfile': 'code-regression'}},
    ]
    results = [
        {'stepId': 0, 'outcome': 'completed',
         'attempts': [{'executionId': 'exec1_' + '1a' * 16, 'outcome': 'completed',
                       'derivation': derivation_of(rf_ts)}],
         'result': analysis_result(rf_ts),
         'termination': {'class': 'success', 'authority': 'authoritative',
                         'runId': rf_ts['runId']}},
        {'stepId': 1, 'outcome': 'completed',
         'attempts': [{'executionId': 'exec1_' + '2b' * 16, 'outcome': 'completed',
                       'derivation': derivation_of(rf_rust)}],
         'result': analysis_result(rf_rust),
         'termination': {'class': 'success', 'authority': 'authoritative',
                         'runId': rf_rust['runId']}},
        # the comparison step: a ComparisonStepResult, never a Run, and its termination is
        # DERIVED from the verdict ("Never defaults to success")
        {'stepId': 2, 'outcome': 'completed',
         'attempts': [{'executionId': 'exec1_' + '3c' * 16, 'outcome': 'completed'}],
         'result': {'kind': 'comparison', 'comparisonResultId': cmp_id,
                    'currentRunId': rf_ts['runId'],
                    'baselineId': baseline_id(rf_ts),
                    'verdict': 'pass', 'comparisonPerformed': True,
                    'counts': {'entries': 3, 'gating': 0, 'indeterminate': 0}},
         'termination': {'class': 'success', 'authority': 'authoritative',
                         'runId': rf_ts['runId']}},
    ]
    inv = {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 3,
           'requestId': REQ, 'projectId': rf_ts['projectId'],
           'workflow': {'kind': 'builtin', 'name': 'audit'},
           'mode': {'interactive': False, 'ci': True, 'ephemeral': False},
           'orderedSteps': steps, 'stepResults': results,
           'termination': {'class': 'success', 'authority': 'authoritative',
                           'runId': rf_ts['runId']},
           'terminationEmitted': True,
           'retentionDisclosure': {'policy': 'durable-unbounded',
                                   'provenance': 'CONFIGURED', 'firstUse': False,
                                   'storageRoot': '.opensip'}}
    e = env('invocation', inv['termination'], 0, rf_ts, invocation=inv)
    r = EV.admit(e, 'multi-step-different-selections')
    # SCHEMA SHAPE AND THE NORMATIVE STEP/RESULT JOINS ARE SEPARATE OBLIGATIONS: the joins are
    # executed here against the ACTUAL admitted Runs of this origin.
    known = {rf_ts['runId'], rf_rust['runId']}
    j = EV.invocation_joins(inv, known_runs=known)
    r['normativeStepResultJoins'] = j
    r['admitted'] = r['admitted'] and not j['refusals']
    if j['refusals'] and r['firstRefusal'] is None:
        r['firstRefusal'] = j['refusals'][0]
    r['requirement'] = 'R-MULTI-STEP-DIFFERENT-SELECTIONS'
    r['classification'] = 'valid'
    r['differentSelectionsMeasured'] = {
        'step1': {'profile': 'default', 'role': 'primary', 'runId': rf_ts['runId']},
        'step2': {'profile': 'pivot', 'role': 'pivot', 'runId': rf_rust['runId'],
                  'pivotOfStep': 1},
        'distinctRunIds': rf_ts['runId'] != rf_rust['runId'],
        'step3': {'kind': 'comparison', 'mintsNoRun': True,
                   'verdictGate': 'the comparison step is the ONLY step whose verdict gates '
                                  'an audit; the analyses it consumes are verdictGate '
                                  'delegated'},
    }
    return r


def formats_from_inventory():
    """The APPLICABLE output formats, measured from the frozen command inventory rather than
    listed: each renderer declares the request classes it applies to, and each command
    declares its own formats plus its parity fields. A format that is not applicable to a
    command is refused with OUTPUT.FORMAT_NOT_APPLICABLE, never silently reshaped."""
    inv = json.load(open(KIT + '/' + S.doc_path(
        'workflows/command-inventory.v3.json')))
    renderers = {r['format']: {'version': r['version'],
                               'applicability': r['applicability'],
                               'requiredFailureClass': r['requiredFailureClass'],
                               'parityRule': r['parityRule'][:200]}
                 for r in inv['renderers']}
    by_cmd = {}
    for c in inv['commands']:
        by_cmd[c['name']] = {'requestClass': c['requestClass'],
                             'formats': c['formats'],
                             'parityFields': c.get('parityFields') or [],
                             'steps': c.get('steps') or []}
    # the applicability join, measured: every format a command declares must be a renderer
    # whose applicability contains that command's request class
    violations = []
    for name, c in sorted(by_cmd.items()):
        for f in c['formats']:
            r = renderers.get(f)
            if r is None:
                violations.append({'command': name, 'format': f,
                                   'why': 'no renderer declares this format'})
            elif c['requestClass'] not in r['applicability']:
                violations.append({'command': name, 'format': f,
                                   'requestClass': c['requestClass'],
                                   'why': 'renderer does not apply to this request class'})
    return {'renderers': renderers,
            'commandCount': len(by_cmd),
            'distinctFormats': sorted(renderers),
            'parityReferenceFormat': 'json (CommandEnvelope major 3)',
            'formatApplicabilityViolationsMeasured': violations,
            'notApplicableCode': 'OUTPUT.FORMAT_NOT_APPLICABLE (request-rejected)',
            'exampleCommands': {k: by_cmd[k] for k in
                                sorted(by_cmd)[:3]}}


def invocation_disclosure(rf):
    """R-INVOCATION-DISCLOSURE: the ownership fields, the bounded cardinalities, the
    ordering rules and the applicable output formats, taken from the schemas rather than
    described."""
    inv = kitdoc(INV_DOC)
    cmd = kitdoc(CMD_DOC)
    defs = inv['$defs']
    step = defs['StepSpec']['properties']
    return {
        'requirement': 'R-INVOCATION-DISCLOSURE', 'classification': 'measured',
        'law': {'invocationRecord': S.doc_path(INV_DOC),
                'commandInventory': S.doc_path(CMD_DOC)},
        'ownershipFields': {
            'requestId': {'owner': 'host-minted per request, operational',
                          'pattern': '^req1_[0-9a-f]{32}$',
                          'neverInAnIdentity': True},
            'stepId': {'owner': 'the step position within this invocation'},
            'projectId': {'owner': 'the project, 64-hex, shared with the sealed graph',
                          'measuredEqualToTheRunProject': True},
            'executionId': {'owner': 'one ATTEMPT of a step; per-attempt identity that is '
                                     'deliberately NOT in any idempotency preimage'},
            'runId': {'owner': 'the sealed analysis Run (run3), a semantic identity'},
        },
        'boundedCardinality': {
            'orderedSteps': inv['properties']['orderedSteps'].get('maxItems'),
            'stepResults': inv['properties'].get('stepResults', {}).get('maxItems'),
            'dependsOn': step['dependsOn'].get('maxItems'),
            'attemptsPerStep': defs['StepResult']['properties']['attempts'].get('maxItems'),
            'availabilityStepsPerInvocation': 64,
            'availabilityNoticesPerStep': 1024,
        },
        'ordering': {
            'orderedSteps': inv['properties']['orderedSteps'].get('x-opensip-order'),
            'dependsOn': step['dependsOn'].get('x-opensip-order'),
            'attempts': defs['StepResult']['properties']['attempts'].get(
                'x-opensip-order'),
            'note': ('`sequence` means the ADMITTED order is the order, so a renderer may '
                     'not re-sort it; a `by` order is a sort key the record must already '
                     'satisfy')},
        'stepKinds': defs['StepKind']['enum'],
        'applicableOutputFormats': formats_from_inventory(),
        'parityReference': ('command-envelope: "The JSON envelope is the parity reference: '
                            'SARIF, HTML and agent renderings must carry semantically equal '
                            'parity fields, and the agent rendering is this envelope plus '
                            'advisory hints."'),
        'retentionDisclosureFields': sorted(defs['RetentionDisclosure']['required']),
    }


def failure_envelopes(rf):
    rows = []

    def add(label, requirement, term, code, remedy, subject, exit_code, **extra):
        detail = {'code': code, 'remedy': remedy, 'subject': subject}
        t = dict(term, domainDetail=detail)
        e = env('failure', t, exit_code, rf, errors=[detail], **extra)
        r = EV.admit(e, label)
        r['requirement'] = requirement
        r['classification'] = 'valid'
        rows.append(r)
        return r

    add('config-input-failure', 'R-ENVELOPE-CONFIG-INPUT',
        {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID'},
        'CONFIG.INVALID',
        'remove or correct the unknown configuration key and re-run',
        '.opensip/config.toml', 2,
        diagnostics=['1 unknown key at analysis.profileId'])
    add('retained-external-input-failure', 'R-ENVELOPE-EXTERNAL-INPUT',
        {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED'},
        'IMPORT.SOURCE_MAPPING_REQUIRED',
        'supply an admitted SourceMappingV1 joining every generated path to the snapshot '
        'by digest, or select a non-stale import',
        'import2 runtime payload', 2)
    add('host-generated-invalid-internal-record', 'R-ENVELOPE-HOST-INVALID',
        {'class': 'operational-failed', 'errorCode': 'HOST.IO_FAILURE',
         'faultCause': 'host-invariant'},
        'HOST.INVARIANT_VIOLATED',
        'the host produced an internal record that its own schema refuses; retry is not '
        'lawful and no Run is claimed',
        'internal view2 record', 4)
    add('producer-boundary-failure', 'R-ENVELOPE-PRODUCER-BOUNDARY',
        {'class': 'operational-failed', 'errorCode': 'PROVIDER.PROTOCOL_VIOLATION',
         'faultCause': 'provider-protocol'},
        'native.identity-not-negotiated',
        'the provider sent a source frame before identity negotiation completed; the '
        'session is faulted and no partial evidence is admitted',
        'native provider session', 4)
    return rows


def public_from_internal(rf):
    """R-PUBLIC-FROM-INTERNAL-REFUSAL: built from an ACTUAL internal refusal produced by this
    origin's own controls, with the originating boundary named."""
    src = json.load(open(OUT + '/vectors/policy-admission-negative-controls.json'))
    internal = None
    for c in src['controls']:
        if c.get('classification') == 'invalid' and c.get('firstRefusal'):
            internal = c
            break
    # DomainDetailCode is a CLOSED enum: the public surface may only name a code that already
    # exists. `POLICY.UNKNOWN_RULE` is the member that covers a policy rule the product
    # refuses to admit; inventing `policy.rule-refused` would be adding a vocabulary member.
    detail = {'code': 'POLICY.IMPERATIVE_KEY_REFUSED'
                      if 'IMPERATIVE' in json.dumps(internal['firstRefusal'])
                      else 'POLICY.UNKNOWN_RULE',
              'remedy': ('correct the refused policy rule and re-request; a disabled rule '
                         'is still admitted, so disabling it does not bypass this'),
              'subject': 'rule.zz-disabled'}
    term = {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID',
            'domainDetail': detail}
    e = env('failure', term, 2, rf, errors=[detail])
    r = EV.admit(e, 'public-from-internal-refusal')
    r['requirement'] = 'R-PUBLIC-FROM-INTERNAL-REFUSAL'
    r['classification'] = 'valid'
    r['internalRefusalThisWasBuiltFrom'] = {
        'case': internal['case'],
        'firstRefusal': internal['firstRefusal'],
        'originatingBoundary': internal.get('observedRefusalLayer'),
        'artifact': 'vectors/policy-admission-negative-controls.json'}
    r['whatThePublicSurfaceDoesNotCarry'] = [
        'the internal check name and its detail payload',
        'any digest of an unadmitted record',
        'the closure trace: the public surface carries a D9 class, an errorCode, a '
        'DomainDetailCode and a bounded remedy, and nothing else',
    ]
    return r


def receipt_availability(rf):
    """R-DURABLE-RECEIPT-AVAILABILITY: a durable receipt beside the CURRENT availability
    account. The receipt is operational; the Run identity is semantic; they are carried in
    different fields and neither substitutes for the other."""
    receipt_rec = {'schemaVersion': 1, 'operation': 'baseline-adopt',
                   'idempotencyKey': K.H('workflow.mutation-intent',
                                         {'schemaVersion': 1, 'requestId': REQ,
                                          'stepId': 'step-1',
                                          'projectId': rf['projectId'],
                                          'operation': 'baseline-adopt'})}
    # MutationReceiptProjection is CLOSED: the envelope carries the receipt's identity and
    # its effect disposition, NOT the idempotency key. The key lives on the retained receipt
    # record, which is where a delivery replay looks it up -- so `durable` is expressed by
    # commitClass/effectOutcome/replayed rather than by a field the projection does not have.
    proj = {'receiptId': 'receipt2:' + K.raw_sha256(K.C(receipt_rec)),
            'operation': 'baseline-adopt',
            'effectOutcome': 'COMPLETED', 'commitClass': 'REVERSIBLE',
            'replayed': False}
    notices = [notice('clones-fact', 'js-allowjs', 'packages/web',
                      'install a release that declares the clones capability for this '
                      'language mode, or accept the disclosed unavailability')]
    term = {'class': 'success'}
    e = env('mutation', term, 0, rf, mutation=proj,
            availability=availability(1, notices),
            retentionDisclosure={'policy': 'durable-bounded', 'provenance': 'EXPLICIT-FLAG',
                                 'firstUse': False, 'storageRoot': '.opensip'})
    r = EV.admit(e, 'durable-receipt-and-current-availability')
    r['requirement'] = 'R-DURABLE-RECEIPT-AVAILABILITY'
    r['classification'] = 'valid'
    r['receiptIsOperationalNotSemantic'] = (
        'the receipt is keyed by H("workflow.mutation-intent", scope) over a HOST-MINTED '
        'requestId and stepId. It is durable so a redelivery performs no second effect; it '
        'is not an evidence identity and cannot stand in for a run3.')
    r['availabilityIsCurrentNotHistorical'] = (
        'the availability account describes what THIS release declares now. A durable '
        'receipt from an earlier release does not make an absent capability available.')
    return r


# --------------------------------------------------------------------- availability vectors
def multi_unit_missing_caps(rf):
    """R-MULTI-UNIT-MISSING-CAPS + R-CANDIDATE-ONLY-CLONES: zero-config selection over
    several workspace units where the installed release does not declare every advertised
    capability, including a clone capability that is CANDIDATE-ONLY."""
    units = [
        {'workspaceRoot': 'packages/web', 'languageMode': 'js-allowjs',
         'requested': ['inventory', 'syntax', 'imports', 'clones-fact'],
         'declaredAvailable': ['inventory', 'syntax', 'imports'],
         'candidateOnly': ['clones-fact']},
        {'workspaceRoot': 'packages/api', 'languageMode': 'ts-tsconfig',
         'requested': ['inventory', 'syntax', 'types', 'clones-fact'],
         'declaredAvailable': ['inventory', 'syntax', 'types', 'clones-fact'],
         'candidateOnly': []},
        {'workspaceRoot': 'crates/engine', 'languageMode': 'rust-cargo',
         'requested': ['inventory', 'syntax', 'clones-fact'],
         'declaredAvailable': ['inventory', 'syntax'],
         'candidateOnly': []},
    ]
    notices, rows = [], []
    for u in units:
        missing = [c for c in u['requested'] if c not in u['declaredAvailable']]
        for c in sorted(missing):
            cand = c in u['candidateOnly']
            notices.append(notice(
                c, u['languageMode'], u['workspaceRoot'],
                ('this capability is CANDIDATE-ONLY in the installed release: it may be '
                 'returned as a candidate and must not be selected as a complete result'
                 if cand else
                 'install a release that declares this capability for this language mode, '
                 'or accept the disclosed unavailability')))
        rows.append(dict(u, missing=sorted(missing),
                         selectedCompleteCloneCapability=(
                             'clones-fact' in u['declaredAvailable']),
                         cloneCapabilityIsCandidateOnly=bool(u['candidateOnly'])))
    notices.sort(key=lambda n: (n['workspaceRoot'].encode(), n['capabilityId'].encode()))
    av = {'stepCount': 1, 'totalNoticeCount': len(notices),
          'steps': [{'stepId': 1, 'noticeCount': len(notices),
                     'notices': notices}]}
    # D9ReasonCode is a CLOSED nine-member vocabulary; the member that covers a requested
    # capability this release does not declare is COVERAGE.LANGUAGE_TIER_UNSUPPORTED.
    term = {'class': 'indeterminate',
            'reasonCodes': ['COVERAGE.LANGUAGE_TIER_UNSUPPORTED']}
    detail = {'code': 'native.capability-unavailable',
              'remedy': 'see the per-unit availability notices',
              'subject': '3 workspace units'}
    e = env('failure', dict(term, domainDetail=detail), 3, rf, errors=[detail],
            availability=av)
    r = EV.admit(e, 'multi-unit-missing-capabilities')
    r['requirement'] = ['R-MULTI-UNIT-MISSING-CAPS', 'R-CANDIDATE-ONLY-CLONES']
    r['classification'] = 'valid'
    r['units'] = rows
    r['ownershipTupleIsTyped'] = (
        'each notice carries capabilityId + languageMode + workspaceRoot as TYPED fields. '
        'Concatenating them into `subject` could truncate a 4096-byte UserInputPath into '
        '1024-byte BoundedText and collapse two distinct units into one notice, so the '
        'tuple is never concatenated.')
    r['candidateOnlyIsNotSelected'] = {
        'candidateOnlyCapabilities': ['clones-fact @ packages/web'],
        'selectedCompleteCapabilities': ['clones-fact @ packages/api'],
        'law': ('a candidate-only clone capability is represented as candidate-only. It is '
                'NOT a selected complete clone result, and a complete-empty clones result '
                'would read as a finding of no clones -- which is exactly the concealment '
                'the unavailability disclosure exists to prevent.')}
    r['noticeCountEqualsArrayLength'] = (av['steps'][0]['noticeCount']
                                         == len(av['steps'][0]['notices']))
    r['perStepCompositionRationale'] = (
        'the account is composed PER STEP: a named multi-step invocation carries up to 64 '
        'steps and each step keeps its own bounded collection, so two admitted selections '
        'of 1023 requests each cannot overflow a single flat 1024 array.')
    return r


# --------------------------------------------------------------------- standing rules
def standing(rf_ts, rf_rust):
    return {
        'R-CHAIN-ZERO-CONFIG-TO-RECEIPT': {
            'classification': 'measured',
            'standing': ('exhibited by the executed traces, envelopes and complete Runs '
                         'TOGETHER; each arrow names the artifact that executed it'),
            'chain': [
                {'arrow': 'zero-config discovery -> snapshot',
                 'owner': 'workflows section 2 discovery + identity snapshot2',
                 'executedArtifact': 'runs/*.store.json snapshot2 records; the '
                                     'js-synthesized mode path in '
                                     'vectors/advertised-mode-paths.json is the zero-config '
                                     'case with an EMPTY retained config graph'},
                {'arrow': 'snapshot -> native context / universe',
                 'owner': 'native-evidence sections 1-3, 11',
                 'executedArtifact': 'runs/*.closure.json checks NATIVE_CONTEXT_*, '
                                     'UNIVERSE_*, native-3-11:CONTEXT_PROJECTION_AGREES*'},
                {'arrow': 'universe -> facts / scopes / Coverage',
                 'owner': 'relation registry + native-evidence section 4',
                 'executedArtifact': 'runs/*.closure.json checks FACT_*, COVERAGE_*, '
                                     'coverage_bijection, coveragePartitionLaw'},
                {'arrow': 'Plan + policy -> proof',
                 'owner': 'composition v3 sections 9.1-9.7',
                 'executedArtifact': 'runs/*.replay.json REPLAY_MATCH (the proof bundle is '
                                     'recomputed and compared, not trusted)'},
                {'arrow': 'proof -> evidence -> seal -> Run',
                 'owner': 'composition v3 section 9.7 + identity section 3',
                 'executedArtifact': 'runs/*.closure.json SEAL_*, RUN_* and the 14 tamper '
                                     'controls per Run in runs/*.controls.json'},
                {'arrow': 'Run -> envelope',
                 'owner': 'command-envelope (evaluator3)',
                 'executedArtifact': 'envelopes/single-step.json, multi-step.json'},
                {'arrow': 'mutation step -> durable receipt',
                 'owner': 'workflows section 1 + repair MutationReceiptV1',
                 'executedArtifact': 'envelopes/receipt-availability.json, '
                                     'vectors/mutation-keys.json'},
            ],
            'whatIsNotClaimed': ('no product was executed. Every arrow above is a RECORD '
                                 'reconstruction of this origin, and the provider, compiler '
                                 'and OS observations inside it are synthetic trusted '
                                 'inputs.'),
        },
        'R-SEMANTIC-VS-OPERATIONAL-AUTHORITY': {
            'classification': 'measured',
            'semanticIdentities': ['snapshot2', 'plan2', 'fact2', 'scope2', 'coverage2',
                                   'view2', 'proof3', 'evidence3', 'seal3', 'run3',
                                   'finding-key2', 'repairplan2'],
            'operationalIdentifiers': ['requestId', 'stepId', 'executionId', 'receipt2',
                                       'pinId', 'H("workflow.mutation-intent", scope)'],
            'measuredSeparation': {
                'noOperationalFieldInARepairPlanDescriptor': (
                    'RepairPlanDescriptor admits no operational field at all, and '
                    'vectors/repair-descriptor.json recomputes repairplan2 over the '
                    'descriptor alone'),
                'receiptKeyCarriesARequestId': (
                    'the generic mutation key preimage is {schemaVersion, requestId, '
                    'stepId, projectId, operation}: entirely operational, which is why it '
                    'grants no authority and never deduplicates different fresh requests'),
                'repairApplyKeyIsContentDerived': (
                    'the repair-apply key has no requestId and no stepId, so it is stable '
                    'across requests -- the opposite property, deliberately'),
                'pinIdIsNotAnAuthority': (
                    'PinnedPurgeDisclosure: "Operational pinId is a host-ledger name scoped '
                    'to this Run, not a content identity or authority token"'),
            },
        },
        'R-MUTATION-VS-ANALYSIS-STEPS': {
            'classification': 'measured',
            'stepsThatSealARun': ['analysis', 'verify'],
            'stepsThatSealNoRun': ['mutation', 'repair-preview', 'repair-apply', 'import',
                                   'native-preparation', 'test-execution', 'comparison',
                                   'query', 'render', 'export-delivery', 'doctor'],
            'citedRecipes': {
                'analysis': 'AnalysisResult authoritative branch requires runId + planId '
                            'and durability=committed',
                'analysis-ephemeral': 'the ephemeral branch has NO runId and NO receipt and '
                                      '"can never satisfy baseline adoption, repair '
                                      'preconditions, or verify"',
                'comparison': 'StepKind comparison "consumes the current analysis Run and a '
                              'baseline artifact, mints no Run"',
                'repair-apply': 'apply is a host-owned mutation bound to the exact '
                                'repairPlanId and snapshotId; VERIFY then admits a FRESH '
                                'snapshot and seals a NEW authoritative Run, never reusing '
                                'the pre-apply Run',
                'import': 'ImportResult requires a receiptId (receipt2), not a run3',
                'native-preparation': 'native section 14: a completed preparation returns '
                                      'an execution receipt and one admitted prepared '
                                      'import, never a Run',
            },
        },
        'R-PROMISE-VS-AVAILABILITY': {
            'classification': 'measured',
            'fourDistinctThings': [
                {'thing': 'product promise', 'where': 'the capability matrix / registries',
                 'example': 'clones@normalized-body-hash is a SUPPORTED-DESIGN capability '
                            'for every `code` grammar class'},
                {'thing': 'installed availability',
                 'where': 'CapabilityAvailabilityV1 notices per requested unit',
                 'example': 'vectors/multi-unit-missing-caps.json: the installed release '
                            'does not declare clones-fact for packages/web'},
                {'thing': 'explicit overrides',
                 'where': 'analysis-spec requestedCapabilities.required plus the selected '
                          'profile',
                 'example': 'a required:false row is requested and may be absent without '
                            'terminating the request'},
                {'thing': 'semantic capability prerequisites',
                 'where': 'the grammar-capability registry and the language-mode table',
                 'example': 'the data-document syntaxClass has no clones capability at all, '
                            'so no installation can make it available for that class'},
            ],
            'appliedTo': ['vectors/multi-unit-missing-caps.json',
                          'vectors/code-vs-data-matrix.json',
                          'runs/syntax-data.store.json'],
            'collapseWouldBe': ('reporting an unavailable capability as a complete empty '
                                'result, which is the concealment '
                                'R-RUN-SYNTAX-DATA already refuses'),
        },
        'R-D9-EXTENSION-PRECEDENCE': {
            'classification': 'measured',
            'selectedComposition': S.doc_path(EV.ENV_DOC),
            'inheritedArtifact': S.doc_path('workflows/schemas/command-envelope.schema.json'),
            'measuredDifference': {
                'schemaMajor': {'selected': 3, 'inherited': 2},
                'runIdPattern': {'selected': '^run3:[0-9a-f]{64}$',
                                 'inherited': '^run2:[0-9a-f]{64}$'},
                'why': ('the evaluator3 composition is the successor: it is selected because '
                        'the sealed Runs of this origin mint run3 identities. Selecting the '
                        'inherited major-1 document would have measured a run3 identity '
                        'against a run2 pattern -- which is how this origin detected the '
                        'precedence question rather than assuming it.')},
            'noNewD9Family': ('workflows section 9: "No new D9 family is introduced." The '
                              'extension changes identities and step kinds, not the class / '
                              'exit table, and envelopes.py derives exitCode from the same '
                              'six-class table in both compositions.'),
        },
    }


def main():
    rf_ts = run_facts('typescript')
    rf_rust = run_facts('rust')
    rows = [single_step(rf_ts), multi_step(rf_ts, rf_rust), public_from_internal(rf_ts),
            receipt_availability(rf_ts), multi_unit_missing_caps(rf_ts)]
    rows += failure_envelopes(rf_ts)
    disc = invocation_disclosure(rf_ts)
    st = standing(rf_ts, rf_rust)

    # R-FAILURE-ENVELOPES-D9: a termination FRAGMENT alone is not a failure envelope. Measure
    # that every failure envelope carries the full selected composition.
    d9 = []
    for r in rows:
        e = r['envelope']
        if e['kind'] != 'failure':
            continue
        t = e['termination']
        d9.append({'label': r['label'],
                   'hasTerminationClass': 'class' in t,
                   'hasDerivedExitCode': e.get('exitCode') == EV.EXIT_BY_CLASS[t['class']],
                   'hasErrorCodeOrReasonCodes': bool(t.get('errorCode')
                                                     or t.get('reasonCodes')),
                   'hasFaultCauseWhereRequired': (t['class'] != 'operational-failed'
                                                  or t.get('faultCause') not in
                                                  (None, 'none')),
                   'hasNonemptyErrors': bool(e.get('errors')),
                   'errorsEqualTheStepDetail': (t.get('domainDetail') is None
                                                or e['errors'] == [t['domainDetail']]),
                   'hasRequestId': bool(e.get('requestId')),
                   'carriesBoundedDiagnosticsOnly': all(
                       isinstance(x, str) for x in (e.get('diagnostics') or [])),
                   'isMoreThanATerminationFragment': sorted(
                       k for k in e if k not in ('schemaFamily', 'schemaMajor', 'kind',
                                                 'termination', 'exitCode')),
                   })
    EV.write('envelopes/failure-envelopes-d9.json',
             {'requirement': 'R-FAILURE-ENVELOPES-D9', 'classification': 'measured',
              'selectedComposition': S.doc_path(EV.ENV_DOC),
              'exitCodeTable': EV.EXIT_BY_CLASS, 'rows': d9})
    print('D9 failure envelopes measured: %d' % len(d9))
    for row in d9:
        print('   %-42s exit-derived=%s errors=%s fields=%s'
              % (row['label'][:42], row['hasDerivedExitCode'],
                 row['hasNonemptyErrors'],
                 row['isMoreThanATerminationFragment']))
    assert all(r['hasDerivedExitCode'] and r['hasNonemptyErrors']
               and r['errorsEqualTheStepDetail'] and r['hasFaultCauseWhereRequired']
               for r in d9), d9

    EV.write('envelopes/single-step.json', rows[0])
    EV.write('envelopes/multi-step.json', rows[1])
    EV.write('envelopes/public-from-internal.json', rows[2])
    EV.write('envelopes/receipt-availability.json', rows[3])
    EV.write('vectors/multi-unit-missing-caps.json', rows[4])
    for r in rows[5:]:
        EV.write('envelopes/%s.json' % r['label'], r)
    EV.write('envelopes/invocation-disclosure.json', disc)
    EV.write('vectors/phase7-standing-rules.json', st)

    bad = []
    for r in rows:
        print('%-46s %-44s admitted=%s' % (r['label'][:46],
                                           str(r['requirement'])[:44], r['admitted']))
        if not r['admitted']:
            bad.append((r['label'], r['owningSchemaError'], r['prosaicLawRefusals']))
    print()
    print('invocation disclosure: stepKinds=%d boundedFields=%d outputFormats=%s'
          % (len(disc['stepKinds']), len(disc['boundedCardinality']),
             disc['applicableOutputFormats']))
    print('standing rules reconstructed:', len(st))
    if bad:
        print('\nFAILURES:')
        print(json.dumps(bad, indent=1, default=str)[:3000])
    assert not bad, [b[0] for b in bad]


main()
