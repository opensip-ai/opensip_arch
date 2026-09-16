"""Composition of evaluator3 outputs from admitted retained inputs.

Implements evaluator-composition-contract.v3 sections 3, 4, 5, 9.1-9.7 exactly as written.
Reads no claimed output. Every field is derived.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_eval as E

TRUE, FALSE, UNK = E.TRUE, E.FALSE, E.UNK
SEVERITY_ORDER = {'note': 0, 'warning': 1, 'error': 2}


def kleene_and(vals):
    if FALSE in vals:
        return FALSE
    if all(v == TRUE for v in vals):
        return TRUE
    return UNK


def kleene_or(vals):
    if TRUE in vals:
        return TRUE
    if all(v == FALSE for v in vals):
        return FALSE
    return UNK


def kleene_not(v):
    return {TRUE: FALSE, FALSE: TRUE, UNK: UNK}[v]


def build_rule_program(policy):
    """composition 9.1: RuleProgramV2 is `{schemaVersion:2, policyDigest, rules:[{ruleId,
    ruleProgramRef, emitWhen} for each policy.rules member in policy order]}`."""
    return {'schemaVersion': 2, 'policyDigest': K.rec_digest(policy),
            'rules': [{'ruleId': r['ruleId'], 'ruleProgramRef': r['ruleProgramRef'],
                       'emitWhen': r['emitWhen']} for r in policy['rules']]}


def scope_document_parameter(inp, analysis_spec, store):
    """Recover the optional selected ScopeDocumentV1 analysis-spec parameter.
    The `parameter` payload class is keyed by the cited schemaDigest; ONE Plan selects at
    most one parameter per registered row (payload registry selectionCardinality)."""
    reg = E._reg(B.IDENTITY_DOC, 'x-opensip-payload-registry')['classes']['parameter']['rows']
    rows = {}
    for key, row in reg.items():
        rows[S.load_doc(row['document'])['sha256']] = (row['document'], row['selector'])
    picked = {}
    for p in analysis_spec['parameters']:
        if p['schemaDigest'] not in rows:
            raise E.EvalError('PAYLOAD_PARAMETER_SCHEMA_UNREGISTERED:%s' % p['schemaDigest'])
        doc, sel = rows[p['schemaDigest']]
        picked.setdefault((doc, sel), []).append(p)
    for k, v in picked.items():
        if len(v) > 1:
            raise E.EvalError('ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:%s' % (k,))
    for (doc, sel), v in picked.items():
        if sel == '#/$defs/ScopeDocumentV1':
            b = store.get_blob(v[0]['payloadDigest'])
            if b is None:
                raise E.EvalError('PARAMETER_PAYLOAD_NOT_RETAINED')
            return json.loads(b.decode())
    return None


def compose(inp, store, emit_plan, exec_inputs_digest, snapshot_id):
    """Returns the complete composed output bundle, all derived."""
    policy = inp.policy
    rule_program = build_rule_program(policy)
    if K.rec_digest(rule_program) != K.rec_digest(inp.rule_program):
        raise E.EvalError('RULE_PROGRAM_NOT_THE_POLICY_PROJECTION')
    rule_program_digest = K.rec_digest(rule_program)
    if rule_program['policyDigest'] != K.rec_digest(policy):
        raise E.EvalError('RULE_PROGRAM_POLICY_DIGEST_MISMATCH')
    if inp.plan['policyDigest'] != rule_program['policyDigest']:
        raise E.EvalError('PLAN_POLICY_DIGEST_MISMATCH')

    # ---- EI = Cset(ExecutionInputsV1.selectedRefs U {XI})
    XI = {'domain': 'execution-inputs', 'digest': exec_inputs_digest}
    EI = K.cset(list(inp.execution_inputs['selectedRefs']) + [XI])
    forbidden = {'proof-bundle', 'finding', 'evaluation-seal', 'run', 'semantic-evidence'}
    for r in EI:
        if r['domain'] in forbidden:
            raise E.EvalError('PROOF_INPUT_REF_FORBIDDEN_DOMAIN:%s' % r['domain'])
    for iid in inp.plan['importIds']:
        if {'domain': 'import', 'digest': iid.split(':', 1)[1]} not in EI:
            raise E.EvalError('PLAN_IMPORT_NOT_IN_EVALUATION_INPUT_REFS:%s' % iid)

    scope_doc = scope_document_parameter(inp, inp.analysis_spec, store)

    emit_by_rule = {r['ruleId']: r for r in emit_plan['rules']}
    if sorted(emit_by_rule) != sorted(r['ruleId'] for r in policy['rules']):
        raise E.EvalError('EMISSION_PLAN_DOES_NOT_BIND_EVERY_POLICY_RULE')
    ns = {}
    for r in emit_plan['rules']:
        key = (r['ruleStableId'], r['semanticsMajor'])
        if key in ns:
            raise E.EvalError('FINGERPRINT_NAMESPACE_NOT_UNIQUE:%s' % (key,))
        ns[key] = r['ruleId']

    # ---- enumeration per rule
    enum_by_rule, enum_defs = {}, {}
    for r in policy['rules']:
        if not r['enabled']:
            enum_by_rule[r['ruleId']] = ([], [], [], [], 'disabled')
            enum_defs[r['ruleId']] = []
            continue
        sel, unres, inv_refs, inc_refs, defs_, state = E.enumerate_subjects(inp, r, scope_doc)
        enum_by_rule[r['ruleId']] = (sel, unres, inv_refs, inc_refs, state)
        enum_defs[r['ruleId']] = defs_

    # ---- budget preflight (composition section 3), checked unsigned 64-bit
    Sset = sum(len(enum_by_rule[r['ruleId']][0]) for r in policy['rules'] if r['enabled'])
    Fcnt = len(inp.facts)
    Icnt = sum(len(p.get('subjects', [])) if isinstance(p, dict) else 0
               for p in inp.import_payloads.values())
    Kcnt = len(inp.coverages)
    Ecnt = sum(len(i['rows']) for _, i in inp.inventories) + \
        sum(len(c['programBindings']) for c in inp.enumeration_plan['cells'])
    work = Ecnt
    for r in policy['rules']:
        if not r['enabled']:
            continue
        N = E.count_nodes(r['emitWhen'])
        A = E.count_atoms(r['emitWhen'])
        per = N + A * (Fcnt + Icnt + Kcnt)
        work += per * len(enum_by_rule[r['ruleId']][0])
        if work > 2 ** 64 - 1:
            raise E.EvalError('BUDGET_ARITHMETIC_OVERFLOW')
    budget = inp.plan['budget']['limit']
    budget_exhausted = work > budget

    witnesses, predicate_proofs, findings, finding_records = {}, [], {}, {}
    rule_results, waived, subjects = [], [], {}
    for r in policy['rules']:
        for t in enum_by_rule[r['ruleId']][0]:
            subjects[t[0]] = t[1]
    rule_defs = {r['ruleId']: list(enum_defs[r['ruleId']]) for r in policy['rules']}

    if not budget_exhausted:
        for r in policy['rules']:
            if not r['enabled']:
                continue
            sel, unres, inv_refs, inc_refs, state = enum_by_rule[r['ruleId']]
            # required-import deficiencies (composition 9.5)
            plan_kinds = {inp.imports[i]['kind'] for i in inp.plan['importIds']} \
                if inp.plan['importIds'] else set()
            for eu in r.get('evidenceUse') or []:
                if eu['requirement'] == 'required' and eu['kind'] not in plan_kinds:
                    rule_defs[r['ruleId']].append(
                        {'source': 'import', 'cause': 'evidence-kind-unavailable',
                         'subjectId': None, 'predicateId': None, 'inputRefs': [],
                         'evidenceKind': eu['kind'], 'nativeCause': None, 'universe': None})
            for sid, srec, row, uni, inv_ref in sel:
                addressed = E.address_nodes(r['emitWhen'])
                values = {}
                # postorder: deepest addresses first
                for addr, node in sorted(addressed, key=lambda t: -len(t[0])):
                    pp, wit, defs_ = eval_node(inp, r, node, addr, sid, srec, values,
                                               EI, rule_program_digest, inv_refs)
                    values[addr] = pp['value']
                    witnesses[pp['witnessDigest']] = wit
                    predicate_proofs.append(pp)
                    rule_defs[r['ruleId']] += defs_
                root_val = values['p']
                if root_val == TRUE:
                    fid, frec, fparams, fkey = mint_finding(
                        inp, r, emit_by_rule[r['ruleId']], sid, srec, row, uni,
                        predicate_proofs, witnesses, EI)
                    findings[fid] = frec
                    finding_records[fid] = {'parameters': fparams, 'fingerprint': fkey}
                    if frec['correspondence']['state'] == 'unmatched':
                        rule_defs[r['ruleId']].append(
                            {'source': 'correspondence',
                             'cause': frec['correspondence']['reason'],
                             'subjectId': sid, 'predicateId': 'p',
                             'inputRefs': inv_refs, 'evidenceKind': None,
                             'nativeCause': None, 'universe': None})

    # ---- waiver membership (composition section 5)
    for fid, frec in findings.items():
        for w in inp.waivers['waivers']:
            t = w['target']
            if 'fingerprint' in t and frec['fingerprint'] == t['fingerprint']:
                waived.append(fid)
            elif ('ruleId' in t and t['ruleId'] == frec['ruleId']
                  and t['subjectPath'] == frec['subject']['logicalPath']):
                waived.append(fid)

    # ---- rule results
    for r in policy['rules']:
        rid = r['ruleId']
        sel, unres, inv_refs, inc_refs, state = enum_by_rule[rid]
        my_findings = K.cset_strings([f for f, v in findings.items() if v['ruleId'] == rid])
        if budget_exhausted and r['enabled']:
            rule_defs[rid].append({'source': 'execution', 'cause': 'work-budget-exhausted',
                                   'subjectId': None, 'predicateId': None, 'inputRefs': [],
                                   'evidenceKind': None, 'nativeCause': None,
                                   'universe': None})
        defs_ = K.cset(rule_defs[rid])
        if not r['enabled']:
            outcome, enum_rec = 'disabled', {'state': 'disabled', 'inventoryRefs': [],
                                             'selectedSubjectIds': [],
                                             'unresolvedSubjectIds': [],
                                             'incompleteInventoryRefs': []}
        else:
            enum_rec = {'state': state, 'inventoryRefs': inv_refs,
                        'selectedSubjectIds': K.cset_strings([s[0] for s in sel]),
                        'unresolvedSubjectIds': K.cset_strings(unres),
                        'incompleteInventoryRefs': inc_refs}
            gates = (r['gate'] and SEVERITY_ORDER[r['severity']]
                     >= SEVERITY_ORDER[policy['gateSeverityAtLeast']])
            live_unwaived = [f for f in my_findings if f not in waived]
            if not gates:
                outcome = 'pass'
            elif live_unwaived:
                outcome = 'fail'
            else:
                blocking = blocking_causes(r, predicate_proofs, witnesses, sel)
                if state != 'complete' or unres or blocking:
                    outcome = 'indeterminate'
                else:
                    outcome = 'pass'
        rule_results.append({'ruleId': rid, 'enumeration': enum_rec, 'outcome': outcome,
                             'findingIds': my_findings, 'deficiencies': defs_})
    rule_results.sort(key=lambda x: x['ruleId'].encode())

    # ---- executionDeficiencies bridge (composition 9.6)
    exec_defs = execution_deficiencies(inp, XI, EI, budget_exhausted)

    # ---- verdict (composition section 5 + 9.7)
    if any(rr['outcome'] == 'fail' for rr in rule_results):
        verdict = 'fail'
    elif any(rr['outcome'] == 'indeterminate' for rr in rule_results) or exec_defs:
        verdict = 'indeterminate'
    else:
        verdict = 'pass'

    proof = {
        'schemaVersion': 3, 'planId': inp.plan_id, 'executionPlanId': inp.exec_plan_id,
        'evaluatorClosure': inp.evaluator_closure,
        'ruleProgramDigest': rule_program_digest,
        'evaluationInputRefs': EI,
        'predicateProofs': sorted(
            predicate_proofs,
            key=lambda p: (p['ruleId'] + ',' + p['subjectId'] + ',' + p['predicateId']).encode()),
        'findingIds': K.cset_strings(list(findings)),
        'verdict': verdict,
        'evaluationState': 'budget-exhausted' if budget_exhausted else 'evaluated',
        'ruleResults': rule_results,
        'waivedFindingIds': K.cset_strings(waived),
        'executionDeficiencies': exec_defs,
        'executionInputsDigest': exec_inputs_digest,
    }
    if budget_exhausted:
        proof['predicateProofs'] = []
        proof['findingIds'] = []

    view_ids = K.cset_strings(['view2:' + r['digest'] for r in EI if r['domain'] == 'view'])
    cov = set()
    for v in view_ids:
        cov |= set(inp.views[v]['coverageIds'])
    cov |= {'coverage2:' + r['digest'] for r in EI if r['domain'] == 'coverage'}
    evidence = {'schemaVersion': 3, 'planId': inp.plan_id, 'viewIds': view_ids,
                'coverageIds': K.cset_strings(sorted(cov)),
                'importIds': K.cset_strings(inp.plan['importIds']),
                'findingIds': proof['findingIds'],
                'proofBundleId': K.ID('proof-bundle', proof)}
    seal = {'schemaVersion': 3, 'planId': proof['planId'],
            'executionPlanId': proof['executionPlanId'],
            'evidenceId': K.ID('semantic-evidence', evidence),
            'evaluatorClosure': proof['evaluatorClosure'],
            'policyDigest': inp.plan['policyDigest'],
            'proofBundleId': K.ID('proof-bundle', proof), 'verdict': proof['verdict']}
    run = {'schemaVersion': 3, 'projectId': inp.snapshot['projectId'],
           'snapshotId': inp.plan['snapshotId'], 'planId': proof['planId'],
           'evidenceId': seal['evidenceId'],
           'evaluationSealId': K.ID('evaluation-seal', seal),
           'capabilityManifestId': inp.plan['capabilityManifestId']}
    pol_deriv = {'schemaVersion': 3, 'planId': run['planId'],
                 'proofBundleId': seal['proofBundleId'],
                 'policyDigest': inp.plan['policyDigest'],
                 'waiverDigest': inp.plan['waiverDigest'], 'verdict': proof['verdict']}
    return {
        'ruleProgram': rule_program, 'ruleProgramDigest': rule_program_digest,
        'evaluationInputRefs': EI, 'proof': proof, 'proofId': K.ID('proof-bundle', proof),
        'witnesses': witnesses, 'findings': findings, 'findingAux': finding_records,
        'evidence': evidence, 'evidenceId': seal['evidenceId'],
        'seal': seal, 'sealId': run['evaluationSealId'],
        'run': run, 'runId': K.ID('run', run),
        'policyDerivation': pol_deriv,
        'policyDerivationId': K.ID('policy-derivation', pol_deriv),
        'subjects': subjects,
        'budget': {'workUnits': work, 'planLimit': budget, 'exhausted': budget_exhausted,
                   'terms': {'E': Ecnt, 'F': Fcnt, 'I': Icnt, 'K': Kcnt,
                             'selectedSubjectsOverEnabledRules': Sset}},
        'scopeDocumentParameter': scope_doc,
    }


def row_for(inp, srec):
    """The inventory row of this subject, needed by the import subject-scalar law."""
    for _, inv in inp.inventories:
        for r in inv['rows']:
            if (r['kind'] == srec['kind']
                    and r['nativeSubjectId'] == srec['nativeSubjectId']):
                return r
    raise E.EvalError('SUBJECT_ROW_NOT_IN_ANY_RETAINED_INVENTORY')


def eval_node(inp, rule, node, addr, sid, srec, values, EI, rule_program_digest, inv_refs):
    op = node['op']
    prog_pred = {'schemaVersion': 2, 'ruleProgramDigest': rule_program_digest,
                 'ruleId': rule['ruleId'], 'predicateId': addr, 'operation': op,
                 'nodeDigest': K.rec_digest(node)}
    ppd = K.rec_digest(prog_pred)
    defs_ = []
    if op in ('and', 'or', 'not'):
        kids = E.child_addresses(node, addr)
        vals = [values[k] for k in kids]
        value = (kleene_and(vals) if op == 'and'
                 else kleene_or(vals) if op == 'or' else kleene_not(vals[0]))
        child_defs = []
        wit = {'schemaVersion': 3, 'programPredicateDigest': ppd, 'matchingFactIds': [],
               'coverageIds': [], 'countLimit': None,
               'childPredicateIds': K.cset_strings(kids), 'matchingImportRows': [],
               'uncertainFactIds': [], 'uncertainImportRows': [],
               'deficiencies': K.cset(child_defs), 'kind': 'boolean'}
        scope_ids = []
        pp = {'ruleId': rule['ruleId'], 'subjectId': sid, 'predicateId': addr,
              'operation': op, 'inputRefs': EI, 'scopeIds': K.cset_strings(scope_ids),
              'value': value, 'witnessDigest': K.rec_digest(wit)}
        return pp, wit, defs_
    if node['relation'] in E.evidence_registry()['relations']:
        res = E.evaluate_imported_atom(inp, node, srec, sid, row_for(inp, srec))
        for c in res['causes']:
            defs_.append({'source': 'import', 'cause': c['code'], 'subjectId': sid,
                          'predicateId': addr, 'inputRefs': EI,
                          'evidenceKind': c['evidenceKind'], 'nativeCause': None,
                          'universe': None})
        wit = {'schemaVersion': 3, 'programPredicateDigest': ppd, 'matchingFactIds': [],
               'coverageIds': [], 'countLimit': None, 'childPredicateIds': [],
               'matchingImportRows': res['knownRows'], 'uncertainFactIds': [],
               'uncertainImportRows': res['uncertainRows'],
               'deficiencies': K.cset(defs_), 'kind': 'imported-atom'}
        pp = {'ruleId': rule['ruleId'], 'subjectId': sid, 'predicateId': addr,
              'operation': op, 'inputRefs': EI, 'scopeIds': [], 'value': res['value'],
              'witnessDigest': K.rec_digest(wit)}
        return pp, wit, defs_
    res = E.evaluate_native_atom(inp, node, srec, sid, None, inv_refs)
    for c in res['causes']:
        defs_.append({'source': 'native', 'cause': c['code'], 'subjectId': sid,
                      'predicateId': addr, 'inputRefs': EI, 'evidenceKind': None,
                      'nativeCause': c.get('nativeCause'), 'universe': c.get('universe')})
    for d in res['nativeDeficiencies']:
        defs_.append({'source': 'native', 'cause': d, 'subjectId': sid,
                      'predicateId': addr, 'inputRefs': EI, 'evidenceKind': None,
                      'nativeCause': None, 'universe': None})
    for cid, dfc, ncause, uni in res['coverageEntryDeficiencies']:
        defs_.append({'source': 'native', 'cause': dfc, 'subjectId': sid,
                      'predicateId': addr,
                      'inputRefs': [{'domain': 'coverage', 'digest': cid.split(':', 1)[1]}],
                      'evidenceKind': None, 'nativeCause': ncause, 'universe': uni})
    wit = {'schemaVersion': 3, 'programPredicateDigest': ppd,
           'matchingFactIds': res['knownFactIds'], 'coverageIds': res['coverageIds'],
           'countLimit': res['countLimit'], 'childPredicateIds': [],
           'matchingImportRows': [], 'uncertainFactIds': res['uncertainFactIds'],
           'uncertainImportRows': [], 'deficiencies': K.cset(defs_), 'kind': 'native-atom'}
    pp = {'ruleId': rule['ruleId'], 'subjectId': sid, 'predicateId': addr, 'operation': op,
          'inputRefs': EI, 'scopeIds': res['scopeIds'], 'value': res['value'],
          'witnessDigest': K.rec_digest(wit)}
    return pp, wit, defs_


def blocking_causes(rule, predicate_proofs, witnesses, sel):
    """Root-indeterminate gating relevance: for an indeterminate and/or node only its
    indeterminate children contribute blocking causes; a determinate root has no
    truth-blocking cause (composition section 3)."""
    out = []
    by = {}
    for pp in predicate_proofs:
        if pp['ruleId'] != rule['ruleId']:
            continue
        by.setdefault(pp['subjectId'], {})[pp['predicateId']] = pp
    for sid, nodes in by.items():
        root = nodes.get('p')
        if root is None or root['value'] != UNK:
            continue
        stack = ['p']
        while stack:
            a = stack.pop()
            pp = nodes[a]
            if pp['value'] != UNK:
                continue
            w = witnesses[pp['witnessDigest']]
            if w['kind'] == 'boolean':
                stack += list(w['childPredicateIds'])
            else:
                for d in w['deficiencies']:
                    if d['source'] in ('native', 'import'):
                        out.append(d['cause'])
    return out


def mint_finding(inp, rule, emit_row, sid, srec, row, uni, predicate_proofs, witnesses, EI):
    """composition 9.7 + section 4 declarative-subject-v1 emission profile."""
    mine = [pp for pp in predicate_proofs
            if pp['ruleId'] == rule['ruleId'] and pp['subjectId'] == sid]
    root = [pp for pp in mine if pp['predicateId'] == 'p'][0]
    known_facts, uncertain_facts, cov, imports_seen = set(), set(), set(), set()
    for pp in mine:
        w = witnesses[pp['witnessDigest']]
        known_facts |= set(w['matchingFactIds'])
        uncertain_facts |= set(w['uncertainFactIds'])
        cov |= set(w['coverageIds'])
    matching_fact_count = len(known_facts)
    matching_import_count = 0

    # discriminator: file/package use SHA256(C([])); symbol uses the detector's ordered
    # nonempty signatureTokens from the projection whose closureId equals ruleClosure
    if srec['kind'] in ('file', 'package'):
        disc = K.raw_sha256(K.C([]))
        reason = None
    else:
        proj = [p for p in row.get('projections', [])
                if p['closureId'] == emit_row['detectorClosure']]
        toks = proj[0]['signatureTokens'] if proj else []
        if not toks:
            disc, reason = None, 'projection-unavailable'
        else:
            disc, reason = K.raw_sha256(K.C(toks)), None
    fingerprint = None
    if reason is None:
        fp = {'schemaVersion': 2, 'ruleStableId': emit_row['ruleStableId'],
              'detectorSemanticsMajor': emit_row['semanticsMajor'],
              'subjectKey': {'language': row['subjectLanguage'], 'kind': srec['kind'],
                             'logicalPath': row['path'],
                             'qualifiedName': row['qualifiedName'],
                             'discriminator': disc},
              'relatedSubjectKeys': []}
        fingerprint = K.ID('finding-fingerprint', fp)
        fpkey = fp
    else:
        fpkey = None
    message_code = rule.get('messageCode') or rule['ruleId']
    params = {'schemaVersion': 2, 'messageCode': message_code,
              'parameters': {'ruleId': rule['ruleId'], 'subjectPath': row['path'],
                             'qualifiedName': row['qualifiedName'],
                             'subjectKind': srec['kind'],
                             'subjectLanguage': row['subjectLanguage'],
                             'matchingFactCount': matching_fact_count,
                             'matchingImportCount': matching_import_count}}
    ev = [{'domain': 'predicate-witness', 'digest': root['witnessDigest']}]
    for f in sorted(known_facts | uncertain_facts):
        ev.append({'domain': 'fact', 'digest': f.split(':', 1)[1]})
    for c in sorted(cov):
        ev.append({'domain': 'coverage', 'digest': c.split(':', 1)[1]})
    for r in EI:
        if r['domain'] == 'import':
            ev.append({'domain': 'import', 'digest': r['digest']})
    finding = {'schemaVersion': 3, 'fingerprint': fingerprint,
               'ruleClosure': emit_row['detectorClosure'], 'subjectId': sid,
               'messageCode': message_code, 'parameterDigest': K.rec_digest(params),
               'severity': rule['severity'], 'evidenceRefs': K.cset(ev),
               'ruleId': rule['ruleId'],
               'subject': {'language': row['subjectLanguage'], 'kind': srec['kind'],
                           'logicalPath': row['path'],
                           'qualifiedName': row['qualifiedName']},
               'correspondence': {'state': 'matched' if fingerprint else 'unmatched',
                                  'reason': reason}}
    return K.ID('finding', finding), finding, params, fpkey


def execution_deficiencies(inp, XI, EI, budget_exhausted):
    """composition 9.6. Internal requiredCellDeficiencies rows are derived here from the
    retained ExecutionInputsV1 cellOutcomes / nativeCoverageAccounts, NOT asserted."""
    reg = E._reg(B.IDENTITY_DOC, 'x-opensip-evaluator-deficiency-registry')
    exec_members = set(reg['sources']['execution'])
    rows = []
    ei = inp.execution_inputs
    cells = inp.enumeration_plan['cells']
    for co in ei['cellOutcomes']:
        if not co['required']:
            continue
        if co['state'] == 'complete':
            continue
        originating = []
        for d in co['inventoryDigests']:
            originating.append({'domain': 'subject-inventory', 'digest': d})
        for acc in ei['nativeCoverageAccounts']:
            if acc['cellOrdinal'] != co['cellOrdinal'] or acc['programOrdinal'] != co['programOrdinal']:
                continue
            for cid in acc['coverageIds']:
                originating.append({'domain': 'coverage', 'digest': cid})
        if co['candidateResultDigest']:
            originating.append({'domain': 'candidate-producer-result',
                                'digest': co['candidateResultDigest']})
        d = co['deficiency']
        if d in exec_members:
            cause = d
        elif d is None or d == 'source-syntax-invalid':
            cause = 'required-cell-unsatisfied'
        else:
            raise E.EvalError('EVALUATOR_EXECUTION_CAUSE_UNREGISTERED:%s' % d)
        rows.append({'source': 'execution', 'cause': cause, 'subjectId': None,
                     'predicateId': None,
                     'inputRefs': K.cset([XI] + originating),
                     'evidenceKind': None, 'nativeCause': co['nativeCause'],
                     'universe': co['universe']})
    if budget_exhausted:
        rows.append({'source': 'execution', 'cause': 'work-budget-exhausted',
                     'subjectId': None, 'predicateId': None, 'inputRefs': EI,
                     'evidenceKind': None, 'nativeCause': None, 'universe': None})
    return K.cset(rows)
