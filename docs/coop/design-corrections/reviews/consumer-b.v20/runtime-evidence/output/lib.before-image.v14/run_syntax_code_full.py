"""Completes the pilot syntax-only CODE Run: policy, Plan, inventories, view, execution
plan, ExecutionInputsV1, then composes the evaluator3 outputs and exports the store."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import run_syntax_code as RSC

OUT = '/tmp/opensip-design-corrections/consumer-b.v14/output'


def policy_document(detector_tid):
    rules = [
        {'ruleId': 'rule.declares-advisory',
         'ruleProgramRef': {'contributionId': 'contrib.clone-hygiene',
                            'ruleStableId': 'clone-hygiene.declares-present',
                            'semanticsMajor': 1, 'programDigest': K.raw_sha256(
                                b'clone-hygiene.declares-present.v1')},
         'enabled': True, 'severity': 'warning', 'gate': False,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'symbol'},
         'emitWhen': {'op': 'exists', 'relation': 'declares',
                      'minResolution': 'syntactic', 'filters': []},
         'evidenceUse': [], 'messageCode': 'declares.present'},
        {'ruleId': 'rule.no-duplicate-body',
         'ruleProgramRef': {'contributionId': 'contrib.clone-hygiene',
                            'ruleStableId': 'clone-hygiene.no-duplicate-body',
                            'semanticsMajor': 2, 'programDigest': K.raw_sha256(
                                b'clone-hygiene.no-duplicate-body.v2')},
         'enabled': True, 'severity': 'error', 'gate': True,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file',
                                'include': ['src/**/*.js']},
         'emitWhen': {'op': 'none', 'relation': 'clones',
                      'minResolution': 'normalized-body-hash', 'filters': []},
         'evidenceUse': [], 'messageCode': 'clones.duplicate-body'},
        {'ruleId': 'rule.unresolved-edge-advisory',
         'ruleProgramRef': {'contributionId': 'contrib.clone-hygiene',
                            'ruleStableId': 'clone-hygiene.no-unresolved-edge',
                            'semanticsMajor': 1, 'programDigest': K.raw_sha256(
                                b'clone-hygiene.no-unresolved-edge.v1')},
         'enabled': True, 'severity': 'note', 'gate': False,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'symbol'},
         'emitWhen': {'op': 'none', 'relation': 'unresolved-edge',
                      'minResolution': 'observed', 'filters': []},
         'evidenceUse': [], 'messageCode': 'unresolved-edge.absent'},
        {'ruleId': 'rule.zz-disabled',
         'ruleProgramRef': {'contributionId': 'contrib.clone-hygiene',
                            'ruleStableId': 'clone-hygiene.disabled-probe',
                            'semanticsMajor': 1, 'programDigest': K.raw_sha256(
                                b'clone-hygiene.disabled-probe.v1')},
         'enabled': False, 'severity': 'note', 'gate': True,
         'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
         'emitWhen': {'op': 'exists', 'relation': 'literal',
                      'minResolution': 'syntactic', 'filters': []},
         'evidenceUse': [], 'messageCode': 'literal.present'},
    ]
    rules.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2,
            'gateSeverityAtLeast': 'warning', 'rules': rules}


def emission_plan(policy, detector_tid):
    rows = [{'ruleId': r['ruleId'],
             'contributionId': r['ruleProgramRef']['contributionId'],
             'ruleStableId': r['ruleProgramRef']['ruleStableId'],
             'semanticsMajor': r['ruleProgramRef']['semanticsMajor'],
             'detectorClosure': detector_tid, 'stabilityClass': 'path-stable',
             'emissionProfile': 'declarative-subject-v1'} for r in policy['rules']]
    rows.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaVersion': 1, 'policyDigest': K.rec_digest(policy), 'rules': rows}


def complete(g):
    b, st, sh = g['b'], g['st'], g['sh']
    cl = g['closures']
    snapshot_id, uni_hex, ctx_hex = g['snapshot_id'], g['uni_hex'], g['ctx_hex']

    # ---------------------------------------------------------------- policy / waivers
    policy = policy_document(cl['detector'])
    policy_dig = b.record(B.POLICY_V2_DOC, '#/$defs/PolicyDocumentV2', policy, 'policy')
    waivers = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}
    waiver_dig = b.record(B.POLICY_V1_DOC, '#/$defs/WaiverSetV1', waivers, 'waivers')
    rule_program = CO.build_rule_program(policy)
    rp_dig = b.record(B.POLICY_V2_DOC, '#/$defs/RuleProgramV2', rule_program, 'rule-program')
    emit = emission_plan(policy, cl['detector'])
    emit_dig = b.record(B.EMIT_PLAN_DOC, '#', emit, 'emission-plan')

    # ---------------------------------------------------------------- analysis spec / grant
    reqcaps = sorted([
        {'capabilityId': 'inventory', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': True},
        {'capabilityId': 'syntax', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': True},
        {'capabilityId': 'clones-fact', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': True},
        {'capabilityId': 'unresolved-edge', 'languageMode': 'syntax-only',
         'workspaceRoot': '.', 'required': False},
    ], key=lambda r: K.C(r))
    params = sorted([
        {'schemaDigest': B.doc_sha(B.ENUM_PLAN_DOC), 'payloadDigest': g['enum_plan_dig']},
        {'schemaDigest': B.doc_sha(B.EMIT_PLAN_DOC), 'payloadDigest': emit_dig},
    ], key=lambda r: K.C(r))
    spec = {'schemaVersion': 2, 'requestedCapabilities': reqcaps,
            'policyPackIds': ['pack.clone-hygiene'], 'parameters': params}
    spec_dig = b.record(B.IDENTITY_DOC, '#/$defs/analysis-spec', spec, 'analysis-spec')

    grant = {'schemaVersion': 2, 'projectId': g['snapshot']['projectId'],
             'principals': K.cset([{'kind': 'first-party', 'closureId': cl['provider'],
                                    'ownerSourceDigest': None},
                                   {'kind': 'first-party', 'closureId': cl['evaluator'],
                                    'ownerSourceDigest': None}]),
             'analysisOperations': sorted(['read-source', 'native-analysis'],
                                          key=lambda s: K.C(s)),
             'scopeDigest': sh['scopeDigest']}
    grant_dig = b.record(B.IDENTITY_DOC, '#/$defs/semantic-grant', grant, 'semantic-grant')

    # ---------------------------------------------------------------- plan
    plan = {'schemaVersion': 2, 'snapshotId': snapshot_id,
            'capabilityManifestId': g['capres']['capabilityManifestId'],
            'semanticClosures': K.cset_strings([cl['provider'], cl['evaluator'],
                                                cl['detector']]),
            'analysisSpecDigest': spec_dig, 'resolvedConfigDigest': sh['configDigest'],
            'nativeContextDigests': [ctx_hex], 'importIds': [],
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDigest': sh['scopeDigest'],
            'budget': dict(g['config']['analysis']['budget']),
            'semanticGrantDigest': grant_dig,
            'capabilityManifestBytesDigest': g['capres']['committedBytesSha256']}
    plan_id = b.framed('plan', B.IDENTITY_DOC, '#/$defs/plan', plan, 'plan')

    # ---------------------------------------------------------------- inventories
    inventories = []
    for cap_id, kind, rows, examined in g['inv_specs']:
        inv = g['mk_inv'](cap_id, kind, rows, examined)
        inv['planId'] = plan_id
        b.admit(B.SUBJ_INV_DOC, '#', inv, 'subject-inventory:%s:%s' % (cap_id, kind))
        d = st.put_record(inv, label='subject-inventory:%s:%s' % (cap_id, kind))
        inventories.append((d, inv))

    # ---------------------------------------------------------------- view
    view_id = b.view(plan_id, g['view_parts']['scopes'], list(g['facts']),
                     g['view_parts']['coverages'], cl['provider'],
                     [B.doc_sha(B.RELATION_DOC), B.doc_sha(B.NATIVE_DOC)], 'syntax')

    # ---------------------------------------------------------------- execution plan
    stage_spec = {'schemaVersion': 2, 'planId': plan_id, 'producerClosure': cl['provider'],
                  'operation': 'syntax.analyze.v1',
                  'parameters': [params[0]],
                  'outputDomains': sorted(['coverage', 'view'], key=lambda s: K.C(s)),
                  'outputSchemaDigest': B.doc_sha(B.NATIVE_DOC)}
    stage_dig = b.record(B.IDENTITY_DOC, '#/$defs/stage-spec', stage_spec, 'stage-spec')
    exec_plan = {'schemaVersion': 2, 'planId': plan_id,
                 'stages': [{'ordinal': 0, 'stageSpecDigest': stage_dig, 'requires': [],
                             'outputDomains': stage_spec['outputDomains']}]}
    exec_plan_id = b.framed('execution-plan', B.IDENTITY_DOC, '#/$defs/execution-plan',
                            exec_plan, 'execution-plan')

    # ---------------------------------------------------------------- ExecutionInputsV1
    host_derived = K.cset([{'domain': 'subject-inventory', 'digest': d}
                           for d, _ in inventories])
    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(view_id)}]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])
    selected = K.cset(stage_out + host_derived)
    cell_outcomes = []
    cells = g['enum_plan']['cells']
    accounts = []
    rel_for_cap = {'inventory': [('file', 'enumerated'), ('package', 'manifest-declared'),
                                 ('vcs-change', 'vcs-reported')],
                   'syntax': [('declares', 'syntactic'), ('literal', 'syntactic'),
                              ('control-flow', 'syntactic')],
                   'clones-fact': [('clones', 'normalized-body-hash')],
                   'unresolved-edge': [('unresolved-edge', 'observed')]}
    cov_by_rel = {}
    for cid in g['view_parts']['coverages']:
        pay = g['coverage_payloads'][cid]
        cov_by_rel[(pay['key']['relation'], pay['key']['resolution'])] = st.suffix(cid)
    for i, c in enumerate(cells):
        bind = c['programBindings'][0]
        avail = bind.get('universe') is not None
        invs = sorted([d for d, inv in inventories if inv['cellOrdinal'] == i],
                      key=lambda s: K.C(s))
        cell_outcomes.append({
            'ordinal': i, 'cellOrdinal': i, 'programOrdinal': 0,
            'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
            'workspaceRoot': c['workspaceRoot'], 'required': c['required'],
            'kinds': c['kinds'], 'universe': bind.get('universe'),
            'enumeratorStatus': 'selected' if avail else 'unselected',
            'enumeratorClosure': cl['provider'] if avail else None,
            'state': 'complete' if avail else 'unavailable',
            'deficiency': None if avail else bind['deficiency'],
            'nativeCause': None if avail else bind['nativeCause'],
            'stageOrdinal': 0 if avail else None,
            'stageOrdinalNullReason': None if avail else 'optional-unselected',
            'inventoryDigests': invs,
            'viewDigests': [st.suffix(view_id)] if avail else [],
            'candidateResultDigest': None})
        for rel, rung in rel_for_cap[c['capabilityId']]:
            if not avail:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unavailable-null-universe',
                                 'coverageIds': []})
            elif (rel, rung) in cov_by_rel:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': uni_hex,
                                 'targetUniverse': uni_hex,
                                 'applicability': 'supported-available',
                                 'coverageIds': [cov_by_rel[(rel, rung)]]})
            elif rel == 'vcs-change':
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'inapplicable-vcs', 'coverageIds': []})
            else:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unsupported-typed', 'coverageIds': []})
    exec_inputs = {
        'schemaVersion': 1, 'planId': plan_id, 'executionPlanId': exec_plan_id,
        'evaluatorClosure': cl['evaluator'],
        'enumerationPlanDigest': g['enum_plan_dig'], 'analysisSpecDigest': spec_dig,
        'hostCapture': {'custody': 'host-tcb-evidence-store', 'observation': 'stage-return',
                        'stageReceipts': [{'ordinal': 0, 'stageSpecDigest': stage_dig,
                                           'producerClosure': cl['provider'],
                                           'outputDomains': stage_spec['outputDomains'],
                                           'outputRefs': stage_out, 'state': 'complete',
                                           'unavailableReason': None}],
                        'hostDerivedRefs': host_derived},
        'selectedRefs': selected, 'cellOutcomes': cell_outcomes,
        'nativeCoverageAccounts': accounts, 'candidateResultRefs': [],
    }
    b.admit(B.EXEC_IN_DOC, '#', exec_inputs, 'execution-inputs')
    exec_in_dig = st.put_record(exec_inputs, label='execution-inputs')

    # ---------------------------------------------------------------- compose outputs
    inp = E.Inputs(st, plan_id, plan, exec_plan_id, cl['evaluator'], policy, rule_program,
                   waivers, emit, g['enum_plan'], inventories,
                   {view_id: st.objects[view_id]}, g['facts'], g['scopes'], g['coverages'],
                   g['coverage_payloads'], g['fact_payloads'],
                   {uni_hex: ('native.semantic-universe.syntax.v2',
                              st.objects['native.semantic-universe.syntax.v2#' + uni_hex])},
                   {ctx_hex: ('native.context.syntax.v2',
                              st.objects['native.context.syntax.v2#' + ctx_hex])},
                   exec_inputs, snapshot=g['snapshot'])
    inp.analysis_spec = spec
    out = CO.compose(inp, st, emit, exec_in_dig, snapshot_id)

    # retain every composed output as its own canonical record / frame
    for wd, w in out['witnesses'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/predicate-witness', w, 'witness:' + wd[:8])
        st.put_record(w, label='witness:' + wd[:8])
        pp = {'schemaVersion': 2, 'ruleProgramDigest': out['ruleProgramDigest']}
    # program-predicate records (preimages of programPredicateDigest)
    for pp in out['proof']['predicateProofs']:
        w = out['witnesses'][pp['witnessDigest']]
        node = node_at(out['ruleProgram'], pp['ruleId'], pp['predicateId'])
        rec = {'schemaVersion': 2, 'ruleProgramDigest': out['ruleProgramDigest'],
               'ruleId': pp['ruleId'], 'predicateId': pp['predicateId'],
               'operation': pp['operation'], 'nodeDigest': K.rec_digest(node)}
        assert K.rec_digest(rec) == w['programPredicateDigest']
        b.admit(B.IDENTITY_DOC, '#/$defs/program-predicate', rec,
                'program-predicate:%s:%s' % (pp['ruleId'], pp['predicateId']))
        st.put_record(rec, label='program-predicate:%s:%s' % (pp['ruleId'], pp['predicateId']))
    for fid, frec in out['findings'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/finding', frec, 'finding:' + fid[:18])
        st.put_framed('finding', frec, label='finding:' + fid[:18])
        aux = out['findingAux'][fid]
        b.admit(B.IDENTITY_DOC, '#/$defs/finding-parameters', aux['parameters'],
                'finding-parameters:' + fid[:18])
        st.put_record(aux['parameters'], label='finding-parameters:' + fid[:18])
        if aux['fingerprint']:
            b.admit(B.IDENTITY_DOC, '#/$defs/finding-fingerprint', aux['fingerprint'],
                    'finding-fingerprint:' + fid[:18])
            st.put_framed('finding-fingerprint', aux['fingerprint'],
                          label='finding-fingerprint:' + fid[:18])
    # evaluation-subject frames: typed roots reached from findings and predicate proofs.
    # They are retained so retained-closure resolution and independent root admission can
    # fetch and re-hash them rather than trusting a typed string.
    for sid, srec in out['subjects'].items():
        b.admit(B.IDENTITY_DOC, '#/$defs/evaluation-subject', srec,
                'evaluation-subject:' + sid[:18])
        st.put_framed('evaluation-subject', srec, label='evaluation-subject:' + sid[:18])
    b.admit(B.IDENTITY_DOC, '#/$defs/proof-bundle', out['proof'], 'proof-bundle')
    st.put_framed('proof-bundle', out['proof'], label='proof-bundle')
    b.admit(B.IDENTITY_DOC, '#/$defs/semantic-evidence', out['evidence'], 'semantic-evidence')
    st.put_framed('semantic-evidence', out['evidence'], label='semantic-evidence')
    b.admit(B.IDENTITY_DOC, '#/$defs/evaluation-seal', out['seal'], 'evaluation-seal')
    st.put_framed('evaluation-seal', out['seal'], label='evaluation-seal')
    b.admit(B.IDENTITY_DOC, '#/$defs/run', out['run'], 'run')
    st.put_framed('run', out['run'], label='run')
    b.admit(B.IDENTITY_DOC, '#/$defs/policy-derivation', out['policyDerivation'],
            'policy-derivation')
    st.put_framed('policy-derivation', out['policyDerivation'], label='policy-derivation')

    g.update(dict(policy=policy, policy_dig=policy_dig, waivers=waivers,
                  waiver_dig=waiver_dig, rule_program=rule_program, rp_dig=rp_dig,
                  emit=emit, emit_dig=emit_dig, spec=spec, spec_dig=spec_dig,
                  grant=grant, grant_dig=grant_dig, plan=plan, plan_id=plan_id,
                  inventories=inventories, view_id=view_id, stage_spec=stage_spec,
                  stage_dig=stage_dig, exec_plan=exec_plan, exec_plan_id=exec_plan_id,
                  exec_inputs=exec_inputs, exec_in_dig=exec_in_dig, out=out, inp=inp))
    return g


def node_at(rule_program, rule_id, addr):
    root = [r for r in rule_program['rules'] if r['ruleId'] == rule_id][0]['emitWhen']
    for a, n in E.address_nodes(root):
        if a == addr:
            return n
    raise KeyError(addr)


def main():
    g = RSC.build()
    g = complete(g)
    out = g['out']
    print('planId    ', g['plan_id'])
    print('runId     ', out['runId'])
    print('sealId    ', out['sealId'])
    print('evidenceId', out['evidenceId'])
    print('proofId   ', out['proofId'])
    print('verdict   ', out['proof']['verdict'], 'state', out['proof']['evaluationState'])
    print('findings  ', len(out['findings']), 'waived', len(out['proof']['waivedFindingIds']))
    print('predicateProofs', len(out['proof']['predicateProofs']))
    print('execDeficiencies', len(out['proof']['executionDeficiencies']))
    print('budget', out['budget'])
    for rr in out['proof']['ruleResults']:
        print('  rule %-34s outcome=%-13s findings=%d defs=%d enum=%s'
              % (rr['ruleId'], rr['outcome'], len(rr['findingIds']),
                 len(rr['deficiencies']), rr['enumeration']['state']))
    print('admissions', len(g['b'].admissions),
          'all admitted', all(a['admitted'] for a in g['b'].admissions))
    print('store blobs', len(g['st'].blobs), 'objects', len(g['st'].objects))


if __name__ == '__main__':
    main()
