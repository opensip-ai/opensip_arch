"""Independent semantic proof replay.

Runs AFTER identity/schema/closure admission, in a FRESH process, over the EXPORTED bytes
only. It reconstructs the evaluator inputs from the retained store, recomputes the complete
proof bundle and every downstream output identity, and compares the recomputed bundle to
the retained claim byte for byte. A mismatch is a refusal of that positive.

It never reads a claimed finding, witness value, verdict, count or parameter as an input.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import opensip_closure as CL
import opensip_store as ST


def reconstruct_inputs(st, cl, run):
    """Rebuild the evaluator input closure from the RETAINED STORE, using only records the
    closure walk admitted. Output records (proof/finding/witness/evidence/seal) are NOT
    read as inputs."""
    plan = cl.resolved[run['planId']]
    snap = cl.resolved[run['snapshotId']]
    seal = cl.resolved[run['evaluationSealId']]
    ev = cl.resolved[run['evidenceId']]
    proof_claim = cl.resolved[seal['proofBundleId']]

    policy = json.loads(st.get_blob(plan['policyDigest']).decode())
    waivers = json.loads(st.get_blob(plan['waiverDigest']).decode())
    spec = json.loads(st.get_blob(plan['analysisSpecDigest']).decode())

    enum_plan = emit_plan = None
    for p in spec['parameters']:
        if p['schemaDigest'] == B.doc_sha(B.ENUM_PLAN_DOC):
            enum_plan = json.loads(st.get_blob(p['payloadDigest']).decode())
        elif p['schemaDigest'] == B.doc_sha(B.EMIT_PLAN_DOC):
            emit_plan = json.loads(st.get_blob(p['payloadDigest']).decode())
    if enum_plan is None or emit_plan is None:
        raise E.EvalError('REQUIRED_EVALUATOR3_PARAMETER_NOT_RETAINED')

    exec_in_dig = proof_claim['executionInputsDigest']
    exec_inputs = json.loads(st.get_blob(exec_in_dig).decode())

    inventories = []
    for r in exec_inputs['selectedRefs']:
        if r['domain'] == 'subject-inventory':
            inventories.append((r['digest'],
                                json.loads(st.get_blob(r['digest']).decode())))
    inventories.sort(key=lambda t: t[0])

    views, facts, scopes, coverages, cov_pay, fact_pay = {}, {}, {}, {}, {}, {}
    for vid in ev['viewIds']:
        v = cl.resolved[vid]
        views[vid] = v
        for fid in v['facts']:
            f = cl.resolved[fid]
            facts[fid] = f
            fact_pay[fid] = json.loads(st.get_blob(f['payloadDigest']).decode())
        for sid in v['scopeIds']:
            scopes[sid] = cl.resolved[sid]
        for cid in v['coverageIds']:
            c = cl.resolved[cid]
            coverages[cid] = c
            cov_pay[cid] = json.loads(st.get_blob(c['payloadDigest']).decode())
    for r in proof_claim['evaluationInputRefs']:
        if r['domain'] == 'coverage':
            cid = 'coverage2:' + r['digest']
            if cid not in coverages and cid in cl.resolved:
                coverages[cid] = cl.resolved[cid]
                cov_pay[cid] = json.loads(
                    st.get_blob(coverages[cid]['payloadDigest']).decode())

    universes, contexts = {}, {}
    for hx, (dom, rec) in cl.universe_cache.items():
        if rec is not None:
            universes[hx] = (dom, rec)
    for hx, (dom, rec) in cl.context_cache.items():
        contexts[hx] = (dom, rec)

    imports, import_payloads = {}, {}
    for iid in plan['importIds']:
        imports[iid] = cl.resolved.get(iid) or cl.typed(iid, 'import', 'REPLAY_IMPORT')
        if imports[iid]:
            import_payloads[iid] = json.loads(
                st.get_blob(imports[iid]['payloadDigest']).decode())

    rule_program = json.loads(st.get_blob(proof_claim['ruleProgramDigest']).decode())

    inp = E.Inputs(st, run['planId'], plan, proof_claim['executionPlanId'],
                   proof_claim['evaluatorClosure'], policy, rule_program, waivers,
                   emit_plan, enum_plan, inventories, views, facts, scopes, coverages,
                   cov_pay, fact_pay, universes, contexts, exec_inputs,
                   imports=imports, import_payloads=import_payloads, snapshot=snap)
    inp.analysis_spec = spec
    return inp, emit_plan, exec_in_dig, proof_claim, seal, ev, run


def compare(recomputed, claimed, label):
    """Compare C of the COMPLETE recomputed object to the retained claim."""
    a, b = K.C(recomputed), K.C(claimed)
    out = {'object': label, 'equal': a == b,
           'recomputedSha256': K.raw_sha256(a), 'retainedSha256': K.raw_sha256(b)}
    if a != b:
        diffs = []
        if isinstance(recomputed, dict) and isinstance(claimed, dict):
            for k in sorted(set(recomputed) | set(claimed)):
                ra, rb = recomputed.get(k, '<<absent>>'), claimed.get(k, '<<absent>>')
                if K.C(ra) != K.C(rb):
                    diffs.append({'field': k,
                                  'recomputed': json.loads(K.C(ra).decode())
                                  if ra != '<<absent>>' else None,
                                  'retained': json.loads(K.C(rb).decode())
                                  if rb != '<<absent>>' else None})
        out['fieldDifferences'] = diffs
    return out


def replay(export_path, label=''):
    st, doc = ST.Store.load(export_path)
    run_id = doc['claim']['runId']
    cl = CL.Closure(st)
    closure_report = cl.close_run(run_id, label)
    result = {'label': label, 'exportPath': export_path, 'runId': run_id,
              'closure': {'admitted': closure_report['admitted'],
                          'checksPassed': closure_report['checksPassed'],
                          'checksNotApplicable': closure_report['checksNotApplicable'],
                          'checksRefused': closure_report['checksRefused'],
                          'refusals': closure_report['refusals']},
              'closureFullReport': closure_report}
    if not closure_report['admitted']:
        result['replayAttempted'] = False
        result['verdict'] = 'CLOSURE_REFUSED_BEFORE_REPLAY'
        return result
    run = cl.resolved[run_id]
    inp, emit_plan, exec_in_dig, proof_claim, seal_claim, ev_claim, _ = \
        reconstruct_inputs(st, cl, run)
    out = CO.compose(inp, st, emit_plan, exec_in_dig, run['snapshotId'])

    comparisons = [
        compare(out['proof'], proof_claim, 'proof-bundle'),
        compare(out['evidence'], ev_claim, 'semantic-evidence'),
        compare(out['seal'], seal_claim, 'evaluation-seal'),
        compare(out['run'], run, 'run'),
    ]
    # every referenced output preimage and identity
    id_cmp = [
        {'identity': 'proof3', 'recomputed': out['proofId'],
         'retained': seal_claim['proofBundleId'],
         'equal': out['proofId'] == seal_claim['proofBundleId']},
        {'identity': 'evidence3', 'recomputed': out['evidenceId'],
         'retained': run['evidenceId'], 'equal': out['evidenceId'] == run['evidenceId']},
        {'identity': 'seal3', 'recomputed': out['sealId'],
         'retained': run['evaluationSealId'],
         'equal': out['sealId'] == run['evaluationSealId']},
        {'identity': 'run3', 'recomputed': out['runId'], 'retained': run_id,
         'equal': out['runId'] == run_id},
    ]
    # findings: full records, parameter bytes, fingerprints, citations
    finding_cmp = []
    claimed_findings = {}
    for fid in proof_claim['findingIds']:
        claimed_findings[fid] = cl.resolved[fid]
    for fid, frec in sorted(out['findings'].items()):
        cl_rec = claimed_findings.get(fid)
        row = {'findingId': fid, 'presentInClaim': cl_rec is not None}
        if cl_rec is not None:
            row.update(compare(frec, cl_rec, 'finding:' + fid[:18]))
            aux = out['findingAux'][fid]
            pb = st.get_blob(frec['parameterDigest'])
            row['parameterBytesRetainedAndEqual'] = (pb == K.C(aux['parameters']))
            if aux['fingerprint']:
                row['fingerprintRecomputed'] = K.ID('finding-fingerprint', aux['fingerprint'])
                row['fingerprintEqualsClaim'] = (
                    row['fingerprintRecomputed'] == cl_rec['fingerprint'])
        finding_cmp.append(row)
    extra = sorted(set(claimed_findings) - set(out['findings']))
    # witnesses: every retained witness must be the recomputed one
    wit_cmp = []
    for pp in out['proof']['predicateProofs']:
        w = out['witnesses'][pp['witnessDigest']]
        retained = st.get_blob(pp['witnessDigest'])
        wit_cmp.append({'ruleId': pp['ruleId'], 'predicateId': pp['predicateId'],
                        'subjectId': pp['subjectId'],
                        'witnessRetained': retained is not None,
                        'witnessBytesEqual': retained == K.C(w),
                        'value': pp['value']})
    result.update({
        'replayAttempted': True,
        'recomputedFrom': ('retained Plan, policy, rule program, waivers, enumeration and '
                           'emission parameters, subject inventories, views, facts, scopes, '
                           'Coverage payloads, native contexts/universes and '
                           'ExecutionInputsV1 -- no claimed output was read as an input'),
        'bundleComparisons': comparisons,
        'identityComparisons': id_cmp,
        'findingComparisons': finding_cmp,
        'claimedFindingsNotRecomputed': extra,
        'witnessComparisons': wit_cmp,
        'budget': out['budget'],
        'recomputedVerdict': out['proof']['verdict'],
        'retainedVerdict': proof_claim['verdict'],
        'subjectEnumeration': {rr['ruleId']: {
            'state': rr['enumeration']['state'],
            'selectedSubjectIds': rr['enumeration']['selectedSubjectIds'],
            'unresolvedSubjectIds': rr['enumeration']['unresolvedSubjectIds'],
            'inventoryRefs': rr['enumeration']['inventoryRefs'],
            'incompleteInventoryRefs': rr['enumeration']['incompleteInventoryRefs'],
            'outcome': rr['outcome'],
            'deficiencies': rr['deficiencies']} for rr in out['proof']['ruleResults']},
        'matchingFactIdsAndCoverageIds': [
            {'ruleId': pp['ruleId'], 'predicateId': pp['predicateId'],
             'subjectId': pp['subjectId'], 'operation': pp['operation'],
             'value': pp['value'],
             'matchingFactIds': out['witnesses'][pp['witnessDigest']]['matchingFactIds'],
             'uncertainFactIds': out['witnesses'][pp['witnessDigest']]['uncertainFactIds'],
             'coverageIds': out['witnesses'][pp['witnessDigest']]['coverageIds'],
             'scopeIds': pp['scopeIds'],
             'childPredicateIds': out['witnesses'][pp['witnessDigest']]['childPredicateIds'],
             'deficiencies': out['witnesses'][pp['witnessDigest']]['deficiencies']}
            for pp in out['proof']['predicateProofs']],
    })
    allok = (all(c['equal'] for c in comparisons) and all(c['equal'] for c in id_cmp)
             and not extra and all(r.get('equal', False) for r in finding_cmp)
             and all(r['witnessBytesEqual'] and r['witnessRetained'] for r in wit_cmp)
             and all(r.get('parameterBytesRetainedAndEqual', True) for r in finding_cmp)
             and all(r.get('fingerprintEqualsClaim', True) for r in finding_cmp))
    result['verdict'] = 'REPLAY_MATCH' if allok else 'REPLAY_MISMATCH_REFUSED'
    result['replayAdmitted'] = allok
    return result
