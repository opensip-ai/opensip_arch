"""Phase 8 -- baseline audit and comparison, reconstructed from the REAL sealed TypeScript Run
as the current side and an independently constructed baseline of the same project.

  R-BASELINE-AUDIT        a BaselineArtifact + ComparisonResult pair, both schema-admitted,
                          with baselineId = H('workflow.baseline', descriptor) and
                          comparisonResultId = H('workflow.comparison', descriptor).
  R-CMP-MISSING           missing-evidence comparison case.
  R-CMP-EVIDENCE-CHANGED  evidence-changed comparison case (the evidence axis compares import
                          IDENTITIES, not kind presence).
  R-CMP-EMPTY-RESULT      empty-result comparison case: zero entries is NOT the same as a
                          comparison that was not performed.
  R-SCOPE-POLICY-ONLY-COMPARISON  only the bound ScopeDocumentV1 changes.
  R-E0-VS-E1-E3           E0 (a prior detector EXECUTION) versus E1..E3 (re-evaluation of
                          current retained evidence).
  R-PIVOT-ONLY-FINGERPRINTS  fingerprints present only at a pivot are retained as such.
  R-HOST-CAPTURED-VS-CANDIDATE  host-captured required work versus candidate-only returns.
  R-EMPTY-PARTIAL-UNAVAILABLE-MISSING  the four states measured side by side.
  R-DETECTOR-COMPAT-FILE  the reserved authenticated listing file versus the component
                          manifest body.
  R-TEST-PREP-REPAIR-AUTH authorization records for test, preparation and repair.
  R-PURGE-REPLAY-OUTPUT-FAILURE  purge/replay and required-output failure envelopes.
  R-SUBSYSTEM-OWNERS      which subsystem owns every decision above.
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
import envelopes as EV
import comparison_law as CMPL
import opensip_eval as E

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
KIT = S.KIT
BASE_DOC = 'workflows/schemas/evaluator3/baseline-artifact.schema.json'
CMP_DOC = 'workflows/schemas/evaluator3/comparison-result.schema.json'
REQ = 'req1_9c4f70ab23d8416eb5207fd1ac36e8b9'

# V23-D6: the generation-22 hand-written comparison helpers (AUDIT_PROFILES with report-only
# suppressing nothing, ZERO_COUNTS, evidence_availability, context, baseline, baseline_entries,
# comparison) are removed; their bytes are kept in lib.before-image.v22/phase8.py. The profile
# table and every derivation now live in comparison_law.py.


def current_side():
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, 'phase8')
    assert rep['admitted'], rep['refusals'][:2]
    run = c.resolved[rid]
    plan = c.plan
    proof = None
    for t, r in st.objects.items():
        if t.startswith('proof3:'):
            proof = r
    # the policy, waiver and scope DOCUMENTS are retained as labelled BLOBS under their raw
    # SHA-256 (that is their published identity recipe), not as typed graph objects
    def blob_rec(label):
        d = st.labels.get(label)
        if d is None:
            return None, None
        by = st.get_blob(d)
        return json.loads(by.decode()), d

    policy, policy_dig = blob_rec('policy')
    waivers, waiver_dig = blob_rec('waivers')
    scope, scope_dig = blob_rec('scope-document')
    fps, findings = [], []
    for t, r in sorted(st.objects.items()):
        if t.startswith('finding-key2:'):
            fps.append(t)
        if t.startswith('finding3:'):
            findings.append((t, r))
    imports = [(t, r) for t, r in sorted(st.objects.items()) if t.startswith('import2:')]
    detector = None
    for t, r in st.objects.items():
        if isinstance(r, dict) and r.get('kind') == 'detector':
            detector = (t, r)
    return {'store': st, 'closure': c, 'runId': rid, 'run': run, 'plan': plan,
            'proof': proof, 'policy': policy, 'scope': scope, 'waivers': waivers,
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDocumentDigest': scope_dig,
            'fingerprints': fps, 'findings': findings, 'imports': imports,
            'detector': detector, 'projectId': run['projectId'],
            'snapshotId': run['snapshotId'], 'planId': run['planId']}


def admit(doc, selector, inst, label, *, identity_field=None, identity_domain=None):
    ok, err = True, None
    try:
        res = S.admit(doc, selector, inst, label)
        if not res['admitted']:
            ok, err = False, {'stock': res['stockSchemaErrors'][:4],
                              'keywords': res['publishedKeywordRefusals'][:4]}
    except Exception as e:
        ok, err = False, '%s: %s' % (type(e).__name__, str(e)[:400])
    idok = None
    if identity_field:
        idok = inst[identity_field] == K.ID(identity_domain, inst['descriptor'])
    return {'label': label, 'owningSchemaAdmitted': ok, 'owningSchemaError': err,
            'identityRecomputed': idok,
            'admitted': ok and (idok is not False)}


def main():
    cur = current_side()
    rows = []
    out = {'consumerId': 'consumer-b.v23',
           'standing': ('the CURRENT side is the real sealed TypeScript Run of this origin; '
                        'the baseline is an independently constructed artifact over the same '
                        'Run. No product executed any comparison: these are record '
                        'reconstructions plus the identity and admission laws.')}

    # ---------- R-BASELINE-AUDIT, R-CMP-*, R-SCOPE-POLICY-ONLY, R-PIVOT-ONLY, R-E0-VS-E1-E3
    # V23-D6: every comparison and baseline record is DERIVED from explicit premises by
    # comparison_law.py. The premises are retained in vectors/comparison-premises.json and are
    # re-derived by indep_comparison_law.py, which does not import comparison_law.
    cs = comparison_scenarios(cur)
    bl = cs['baseline-audit-unchanged']['baseline']
    cmp_ok = cs['baseline-audit-unchanged']['record']
    miss = cs['missing-context-document']['record']
    ev = cs['evidence-changed']['record']
    emp = cs['empty-result']['record']
    sc = cs['scope-policy-only']['record']
    po = cs['pivot-only-fingerprint']['record']
    rows += cs['admissionRows']
    e0e3 = cs['e0VsE1E3']

    # ------------------------------------------------- R-HOST-CAPTURED-VS-CANDIDATE
    hc = {
        'requirement': 'R-HOST-CAPTURED-VS-CANDIDATE', 'classification': 'measured',
        'hostCapturedRequiredWork': {
            'meaning': ('work the HOST performed and captured itself, so the retained bytes '
                        'are its own observation and the result is required evidence'),
            'examplesInThisReconstruction': [
                {'what': 'the snapshot inventory and every file fact',
                 'artifact': 'runs/*.store.json snapshot2 + fact2 file@enumerated',
                 'required': True},
                {'what': 'the native context / universe of each language Run',
                 'artifact': 'runs/*.closure.json NATIVE_CONTEXT_* and UNIVERSE_* checks',
                 'required': True}],
        },
        'candidateOnlyReturns': {
            'meaning': ('a result the product may RETURN AS A CANDIDATE but must not select '
                        'as a complete result; it carries no required-evidence authority'),
            'examplesInThisReconstruction': [
                {'what': 'the clones capability on a release that declares it candidate-only',
                 'artifact': 'vectors/multi-unit-missing-caps.json '
                             'candidateOnlyIsNotSelected',
                 'required': False},
                {'what': 'an unmapped-only import',
                 'artifact': 'vectors/imported-observation-boundary.json -- unmapped-only '
                             'evidence "may be listed and queried but never feeds a '
                             'predicate"',
                 'required': False}],
        },
        'theErrorThisPrevents': (
            'reporting a candidate-only return as host-captured required work would let an '
            'unselected or unmapped result satisfy a required-coverage obligation.'),
        'measuredJoin': {
            'importsConsumableForAPredicate': [
                i['importId'] for i in
                bl['descriptor']['context']['evidenceAvailability']['imports']],
            'note': ('the one import of the TypeScript Run is snapshot-equal and therefore '
                     'consumable; a candidate-only or unmapped-only import would appear in '
                     'the same array but could not be a predicate input')},
    }

    # ------------------------------------- R-EMPTY-PARTIAL-UNAVAILABLE-MISSING
    four = four_states()

    # ------------------------------------------------- R-DETECTOR-COMPAT-FILE
    compat = detector_compat(cur)

    # ------------------------------------------------- R-TEST-PREP-REPAIR-AUTH
    auth = test_prep_repair_auth(cur)

    # ------------------------------------------------- R-PURGE-REPLAY-OUTPUT-FAILURE
    prf = purge_replay_output(cur)
    rows += prf['envelopes']

    # ------------------------------------------------- R-PUBLIC-TERMINATION-EXAMPLES
    pte = public_termination(cur)
    rows += pte['envelopes']

    # ------------------------------------------------- R-SUBSYSTEM-OWNERS
    owners = subsystem_owners()

    out.update({'controls': rows, 'e0VsE1E3': e0e3, 'hostCapturedVsCandidate': hc,
                'fourStates': four, 'detectorCompatibility': compat,
                'authorizations': auth, 'purgeReplayOutput': prf['summary'],
                'publicTermination': pte['summary'], 'subsystemOwners': owners})
    EV.write('envelopes/purge-replay-output-failure.json',
             {'requirement': 'R-PURGE-REPLAY-OUTPUT-FAILURE', 'summary': prf['summary'],
              'envelopes': prf['envelopes']})
    EV.write('envelopes/public-termination.json',
             {'requirement': 'R-PUBLIC-TERMINATION-EXAMPLES',
              'summary': pte['summary'], 'envelopes': pte['envelopes']})
    EV.write('vectors/baseline-audit.json',
             {'baselineArtifact': bl, 'comparisonUnchanged': cmp_ok,
              'admission': [r for r in rows if r['requirement'] == 'R-BASELINE-AUDIT']})
    EV.write('vectors/comparison-missing.json', miss)
    EV.write('vectors/comparison-evidence-changed.json', ev)
    EV.write('vectors/comparison-empty-result.json', emp)
    EV.write('vectors/comparison-scope-policy-only.json', sc)
    EV.write('vectors/baseline-e0-e3.json', e0e3)
    EV.write('vectors/comparison-premises.json', cs['premisesDoc'])
    EV.write('vectors/comparison-baselines.json', cs['baselinesDoc'])
    EV.write('vectors/comparison-pivot-only-fingerprints.json', po)
    EV.write('vectors/host-captured-vs-candidate.json', hc)
    EV.write('vectors/empty-partial-unavailable-missing.json', four)
    EV.write('vectors/detector-compatibility-file.json', compat)
    EV.write('vectors/test-prep-repair-authorization.json', auth)
    EV.write('vectors/phase8-subsystem-owners.json', owners)
    EV.write('vectors/phase8-all.json', out)

    bad = []
    for r in rows:
        print('%-44s %-34s admitted=%-5s identity=%s'
              % (r['label'][:44], str(r['requirement'])[:34], r['admitted'],
                 r.get('identityRecomputed')))
        if not r['admitted']:
            bad.append((r['label'], r['owningSchemaError']))
    print()
    print('four-state rows: %d | detector-compat checks: %d | authorizations: %d'
          % (len(four['states']), len(compat['measured']), len(auth['records'])))
    missing_ex = [s['state'] for s in four['states'] if not s['measuredExample']]
    print('four states with a measured example: %d/%d %s'
          % (len(four['states']) - len(missing_ex), len(four['states']),
             'missing=' + str(missing_ex) if missing_ex else ''))
    assert not missing_ex, missing_ex
    if bad:
        print(json.dumps(bad, indent=1, default=str)[:3000])
    assert not bad, [b[0] for b in bad]


PIVOT_CLOSURE_KINDS = ('detector', 'evaluator', 'provider', 'toolchain', 'stdlib', 'schema-set')


def synthetic_id(domain, what):
    """a schema-valid identity for a record this reconstruction does NOT hold; always labelled
    syntheticHelperOnly in the premises that use it"""
    return K.ID(domain, {'syntheticHelperOnly': what})


def ts_side(cur):
    """The REAL TypeScript side of a comparison, read from the retained Run: its documents, the
    detector and pivot closures, the bound import, matched findings with the fingerprint subject
    path, the waived set, rule results and execution deficiencies."""
    st, proof, policy = cur['store'], cur['proof'], cur['policy']
    emit = json.loads(st.get_blob(st.labels['emission-plan']).decode())
    det_tid, det = cur['detector']
    manifest = json.loads(st.get_blob(det['manifestDigest']).decode())
    sev = {r['ruleId']: r['severity'] for r in policy['rules']}
    det_name = {}
    for t, r in st.objects.items():
        if t.startswith('closure2:') and r.get('kind') == 'detector':
            det_name[t] = json.loads(st.get_blob(r['manifestDigest']).decode())['name']
    findings = []
    for fid in proof['findingIds']:
        f = st.objects[fid]
        key = st.objects[f['fingerprint']]
        findings.append({'findingId': fid, 'fingerprint': f['fingerprint'], 'ruleId': f['ruleId'],
                         'detectorId': det_name[f['ruleClosure']], 'subjectId': f['subjectId'],
                         'subjectPath': key['subjectKey']['logicalPath'],
                         'severity': sev[f['ruleId']], 'waived': fid in proof['waivedFindingIds'],
                         'matched': f['correspondence']['state'] == 'matched'})
    imports = []
    for t, w in sorted(st.objects.items()):
        if t.startswith('import2:'):
            assert K.ID('import', w) == t, t
            imports.append({'kind': w['kind'], 'importId': t, 'payloadDigest': w['payloadDigest'],
                            'sourceCorrespondenceDigest': w['sourceCorrespondenceDigest'],
                            'scopeDigest': w['scopeDigest'],
                            'observationDigest': w['observationDigest']})
    side = {
        'projectId': cur['projectId'], 'snapshotId': cur['snapshotId'], 'runId': cur['runId'],
        'planId': cur['planId'],
        'documents': {'policy': policy, 'scope': cur['scope'], 'waivers': cur['waivers']},
        'detectors': [{'detectorId': manifest['name'], 'closureId': det_tid,
                       'semanticsMajor': int(det['semanticVersion'].split('.')[0]),
                       'semanticVersion': det['semanticVersion'],
                       'contributionId': sorted({r['contributionId'] for r in emit['rules']
                                                 if r['detectorClosure'] == det_tid})[0],
                       'manifestDigest': det['manifestDigest']}],
        'pivotClosure': [{'closureId': t, 'kind': r['kind'], 'manifestDigest': r['manifestDigest'],
                          'protocolMajor': r['protocolMajor'], 'platform': r['platform']}
                         for t, r in sorted(st.objects.items())
                         if t.startswith('closure2:') and r.get('kind') in PIVOT_CLOSURE_KINDS],
        'boundImports': imports, 'findings': findings,
        'ruleResults': {rr['ruleId']: {'outcome': rr['outcome'],
                                       'enumerationState': rr['enumeration']['state'],
                                       'unresolvedSubjects':
                                           len(rr['enumeration']['unresolvedSubjectIds'])}
                        for rr in proof['ruleResults']},
        'stabilityClassByRule': {r['ruleId']: r['stabilityClass'] for r in emit['rules']},
        'evaluationState': proof['evaluationState'],
        'executionDeficiencies': proof['executionDeficiencies']}
    for label, doc in (('policy', policy), ('scope-document', cur['scope']),
                       ('waivers', cur['waivers'])):
        assert CMPL.doc_digest(doc) == st.labels[label], label
    return side


def scope_selects(scope_doc, path):
    return (any(E.glob_match(g, path) for g in scope_doc['include'])
            and not any(E.glob_match(g, path) for g in scope_doc['exclude']))


def comparison_scenarios(cur):
    """The six comparison/baseline scenarios, each derived from explicit premises."""
    import copy
    ev_rel = json.load(open(KIT + '/' + S.doc_path(B.IMPORTED_DOC)))[
        'x-opensip-evidence-relation-registry']['relations']
    st = cur['store']
    real = ts_side(cur)
    out, prem_rows, baselines, adm = {}, [], {}, []

    def build(name, reqs, record_file, base_side, cur_side, profile, real_sides, synthetic=(),
              pivots=None, override=None, notes=None, remedy=None, extra=None):
        bl_ = CMPL.baseline_artifact(base_side, ev_rel, override)
        prem = {'scenario': name, 'requirements': reqs, 'profile': profile,
                'auditProfileRecord': CMPL.AUDIT_PROFILES[profile],
                'baselineSide': base_side, 'currentSide': cur_side, 'pivots': pivots or {},
                'overrideDocuments': override, 'declaredCompatible': [],
                'realSides': real_sides, 'syntheticHelperOnly': list(synthetic),
                'derivationNotes': notes or {}, 'remedyText': remedy}
        prem.update(extra or {})
        rec = CMPL.derive(prem, bl_, ev_rel)
        if record_file == 'vectors/baseline-audit.json':
            prem['recordRef'] = {'file': record_file, 'pointer': '/comparisonUnchanged'}
            prem['baselineRef'] = {'file': record_file, 'pointer': '/baselineArtifact'}
        else:
            prem['recordRef'] = {'file': record_file, 'pointer': ''}
            prem['baselineRef'] = {'file': 'vectors/comparison-baselines.json',
                                   'pointer': '/' + name}
            baselines[name] = bl_
        for label, doc_, inst, idf, dom in (
                ('baseline:' + name, BASE_DOC, bl_, 'baselineId', 'workflow.baseline'),
                ('comparison:' + name, CMP_DOC, rec, 'comparisonResultId',
                 'workflow.comparison')):
            r_ = admit(doc_, '#', inst, label, identity_field=idf, identity_domain=dom)
            r_['requirement'] = reqs[0]
            r_['classification'] = 'valid'
            adm.append(r_)
        prem_rows.append(prem)
        out[name] = {'baseline': bl_, 'record': rec, 'premises': prem}
        return bl_, rec

    # S0: the TypeScript Run adopted as its own baseline and compared with itself
    build('baseline-audit-unchanged', ['R-BASELINE-AUDIT'], 'vectors/baseline-audit.json',
          real, real, 'code-regression', {'baselineSide': True, 'currentSide': True},
          notes={'baselineSide': 'the real TypeScript Run adopted as the baseline',
                 'verdict': ('the current Run carries a required execution deficiency, which '
                             'section 3 says still affects the comparison verdict')})
    # S1: the baseline's embedded scope document is NOT the document its context digest names
    wrong_scope = copy.deepcopy(real['documents']['scope'])
    wrong_scope['exclude'] = sorted(set(wrong_scope['exclude']) | {'src/util.ts'})
    build('missing-context-document', ['R-CMP-MISSING'], 'vectors/comparison-missing.json',
          real, real, 'code-regression', {'baselineSide': True, 'currentSide': True},
          override={'scope': wrong_scope},
          notes={'baselineSide': ('the real TypeScript Run adopted as the baseline, exported with '
                                  'an embedded scope document that is not the one '
                                  'context.scopeDigest names: the named context document is '
                                  'missing from the artifact')},
          remedy=('re-export the baseline with the exact scope document its context digest names; '
                  'no comparison is performed against a baseline whose context cannot be read'))
    # S2: the baseline was adopted from a Run bound to a DIFFERENT runtime import of the same kind
    wrapper = next(w for t, w in st.objects.items() if t.startswith('import2:'))
    payload = json.loads(st.get_blob(wrapper['payloadDigest']).decode())
    alt_payload = copy.deepcopy(payload)
    for row in alt_payload['subjects']:
        if row['path'] == 'src/util.ts':
            row.clear()
            row.update({'path': 'src/util.ts', 'observability': 'unobservable',
                        'mappingGap': 'helper-only: the prior capture emitted no source map for it'})
    alt_payload['mappingGaps'] = sorted(set(alt_payload['mappingGaps']) | {'src/util.ts'})
    alt_adm = S.admit(B.IMPORTED_DOC, '#/$defs/RuntimePayloadV1', alt_payload, 'alt-runtime-payload')
    alt_wrapper = dict(wrapper, payloadDigest=K.raw_sha256(K.C(alt_payload)))
    alt_wrapper_adm = S.admit(B.IDENTITY_DOC, '#/$defs/import', alt_wrapper, 'alt-import-wrapper')
    alt_id = K.ID('import', alt_wrapper)
    ev_base = copy.deepcopy(real)
    ev_base.update(runId=synthetic_id('run', 'the prior TypeScript Run bound to the alternative '
                                              'runtime import'),
                   planId=synthetic_id('plan', 'the Plan of that prior Run'),
                   boundImports=[{'kind': alt_wrapper['kind'], 'importId': alt_id,
                                  'payloadDigest': alt_wrapper['payloadDigest'],
                                  'sourceCorrespondenceDigest':
                                      alt_wrapper['sourceCorrespondenceDigest'],
                                  'scopeDigest': alt_wrapper['scopeDigest'],
                                  'observationDigest': alt_wrapper['observationDigest']}],
                   findings=[f for f in real['findings']
                             if not (f['ruleId'] == 'rule.e-runtime-mapped-observation'
                                     and f['subjectPath'] == 'src/util.ts')])
    build('evidence-changed', ['R-CMP-EVIDENCE-CHANGED'], 'vectors/comparison-evidence-changed.json',
          ev_base, real, 'code-regression', {'baselineSide': False, 'currentSide': True},
          synthetic=['baselineSide', 'baselineSide.runId', 'baselineSide.planId',
                     'baselineSide.boundImports (alternative payload constructed and '
                     'schema-admitted, never captured)',
                     'baselineSide.findings (derived by the atom law from that payload, not '
                     'evaluated by a product)'],
          notes={'baselineSide.findings': (
              'under the alternative payload src/util.ts is `unobservable`, which never enters '
              'the polarity set, so rule.e (unfiltered exists) is indeterminate there and emits '
              'no finding; rule.c (observability=observed-hit) is false for src/util.ts under '
              'either payload; every other finding is unchanged')},
          extra={'alternativeImport': {'payload': alt_payload, 'payloadAdmitted': alt_adm['admitted'],
                                       'wrapper': alt_wrapper,
                                       'wrapperAdmitted': alt_wrapper_adm['admitted'],
                                       'importId': alt_id}})
    # S3: an empty fingerprint population -- both sides synthetic, because every retained Run of
    # this origin emits at least one fingerprinted finding
    empty = copy.deepcopy(real)
    empty.update(runId=synthetic_id('run', 'a TypeScript Run whose rules emit no finding'),
                 planId=synthetic_id('plan', 'its Plan'),
                 snapshotId=synthetic_id('snapshot', 'its snapshot'), findings=[],
                 ruleResults={r['ruleId']: {'outcome': 'pass' if r['enabled'] else 'disabled',
                                            'enumerationState': ('complete' if r['enabled']
                                                                 else 'disabled'),
                                            'unresolvedSubjects': 0}
                              for r in real['documents']['policy']['rules']},
                 executionDeficiencies=[])
    empty_base = copy.deepcopy(empty)
    empty_base.update(runId=synthetic_id('run', 'the baseline Run of the same empty snapshot'),
                      planId=synthetic_id('plan', 'the baseline Plan of the same empty snapshot'))
    build('empty-result', ['R-CMP-EMPTY-RESULT'], 'vectors/comparison-empty-result.json',
          empty_base, empty, 'code-regression', {'baselineSide': False, 'currentSide': False},
          synthetic=['baselineSide', 'currentSide',
                     'why: every retained Run of this origin emits at least one fingerprinted '
                     'finding, so no retained current side has an empty population'])
    # S4: only the bound ScopeDocumentV1 changed
    base_scope = copy.deepcopy(real['documents']['scope'])
    base_scope['exclude'] = sorted(set(base_scope['exclude']) | {'src/util.ts'})
    sc_base = copy.deepcopy(real)
    sc_base['documents']['scope'] = base_scope
    sc_base.update(runId=synthetic_id('run', 'the prior TypeScript Run under the narrower scope '
                                              'document'),
                   planId=synthetic_id('plan', 'its Plan (the scope document is an analysis-spec '
                                               'parameter)'),
                   findings=[f for f in real['findings'] if scope_selects(base_scope,
                                                                          f['subjectPath'])])
    e2 = [{k: f[k] for k in ('fingerprint', 'ruleId', 'detectorId', 'subjectPath')}
          for f in real['findings'] if f['matched'] and scope_selects(base_scope, f['subjectPath'])]
    build('scope-policy-only', ['R-SCOPE-POLICY-ONLY-COMPARISON'],
          'vectors/comparison-scope-policy-only.json', sc_base, real, 'policy-change',
          {'baselineSide': False, 'currentSide': True},
          synthetic=['baselineSide', 'baselineSide.runId', 'baselineSide.planId',
                     'baselineSide.findings (the current findings the baseline scope selects)'],
          pivots={'E2': {'fingerprints': e2, 'reconstructedReEvaluation': True,
                         'derivation': ('E2 = current detector, current policy, BASELINE scope: the '
                                        'retained current findings whose subject the embedded '
                                        'baseline ScopeDocumentV1 selects; the scope document '
                                        'selects subjects, it changes no fact or Coverage')}},
          notes={'discoveryScope': ('plan.scopeDigest (the foundation scope-descriptor that decided '
                                    'which SOURCE was discovered) is the same on both sides: %s'
                                    % cur['plan'].get('scopeDigest'))})
    # S5: a fingerprint present ONLY at a pivot
    prior_closure = synthetic_id('closure', 'the prior ts-hygiene detector closure, semantics '
                                            'major 1')
    pv_base = copy.deepcopy(real)
    pv_base['detectors'] = [dict(real['detectors'][0], closureId=prior_closure,
                                 semanticsMajor=1, semanticVersion='1.0.0',
                                 manifestDigest=K.raw_sha256(b'helper-only prior detector manifest'))]
    pv_base['pivotClosure'] = [dict(c, closureId=prior_closure,
                                    manifestDigest=pv_base['detectors'][0]['manifestDigest'])
                               if c['kind'] == 'detector' else c for c in real['pivotClosure']]
    for r in pv_base['documents']['policy']['rules']:
        if r['ruleId'] == 'rule.d-disabled-probe':
            r['enabled'] = True
    pv_base['ruleResults']['rule.d-disabled-probe'] = {'outcome': 'pass',
                                                      'enumerationState': 'complete',
                                                      'unresolvedSubjects': 0}
    pv_base.update(runId=synthetic_id('run', 'the baseline Run of the prior detector'),
                   planId=synthetic_id('plan', 'its Plan'))
    x_row = {'fingerprint': 'finding-key2:' + K.raw_sha256(
        b'helper-only: the rule.d finding the current detector emits under the baseline policy'),
        'ruleId': 'rule.d-disabled-probe', 'detectorId': real['detectors'][0]['detectorId'],
        'subjectPath': 'package.json'}
    matched = [{k: f[k] for k in ('fingerprint', 'ruleId', 'detectorId', 'subjectPath')}
               for f in real['findings'] if f['matched']]
    build('pivot-only-fingerprint', ['R-PIVOT-ONLY-FINGERPRINTS', 'R-E0-VS-E1-E3'],
          'vectors/comparison-pivot-only-fingerprints.json', pv_base, real, 'code-regression',
          {'baselineSide': False, 'currentSide': True},
          synthetic=['baselineSide', 'baselineSide.detectors (prior closure)', 'pivots.E0',
                     'pivots.E1'],
          pivots={'E0': {'pivotRunId': synthetic_id('run', 'the committed three-way pivot Run of '
                                                           'the prior detector over the current '
                                                           'snapshot'),
                         'fingerprints': matched, 'syntheticHelperOnly': True,
                         'derivation': ('the prior detector over the same snapshot reproduces the '
                                        'baseline set; it does not implement rule.d')},
                  'E1': {'fingerprints': sorted(matched + [x_row],
                                                key=lambda r: r['fingerprint'].encode()),
                         'syntheticHelperOnly': True,
                         'derivation': ('the current detector re-evaluated under the BASELINE '
                                        'policy, where rule.d is enabled, emits one more '
                                        'fingerprint on package.json')}},
          notes={'currentPolicy': 'rule.d is disabled in the current policy, so E2..E4 lack it'})
    by = {k: v['record']['descriptor'] for k, v in out.items()}
    pv = by['pivot-only-fingerprint']
    e0e3 = {
        'requirement': 'R-E0-VS-E1-E3', 'classification': 'measured',
        'law': ('workflows-and-surfaces section 3 pivot table + comparison-result '
                '#/$defs/PivotPresence, pivotsAvailable and DetectorDisposition.method'),
        'pivots': {
            'B': 'the baseline artifact entries (a retained artifact, not an execution)',
            'E0': 'the PRIOR detector closure executed over current source (an execution that '
                  'needs the closure retained, trusted and runnable; a committed pivot Run)',
            'E1': 'the current detector re-evaluated under the baseline POLICY (no execution)',
            'E2': 'the current detector and policy re-evaluated under the baseline SCOPE',
            'E3': 'the current detector, policy and scope re-evaluated under the baseline WAIVERS',
            'E4': 'the current Run'},
        'measuredFromTheDerivedRecords': {
            'pivotOnlyScenario': {
                'detectors': pv['detectors'], 'pivotsAvailable': pv['pivotsAvailable'],
                'e0IsAPriorDetectorExecution': any(d['method'] == 'three-way-pivot'
                                                   and 'pivotRunId' in d for d in pv['detectors']),
                'e1IsAReEvaluationWithNoRun': (pv['pivotsAvailable']['E1'] == 'available'),
                'standing': 'the E0 pivot Run and the prior closure are synthetic helper-only'},
            'scopeOnlyScenario': {'pivotsAvailable': by['scope-policy-only']['pivotsAvailable'],
                                  'e2Derivation': out['scope-policy-only']['premises']['pivots'][
                                      'E2']['derivation']},
            'unchangedScenario': {'pivotsAvailable': by['baseline-audit-unchanged'][
                'pivotsAvailable']}},
        'presenceNullMeans': ('null means the pivot was not bound (not-needed or unavailable); '
                              'false means it was bound and the fingerprint was absent'),
    }
    out.update(admissionRows=adm, e0VsE1E3=e0e3,
               premisesDoc={'standing': CMPL.__doc__, 'scenarios': prem_rows},
               baselinesDoc=baselines)
    return out


def four_states():
    """R-EMPTY-PARTIAL-UNAVAILABLE-MISSING -- four DISTINCT states, each measured on a real
    retained artifact of this origin. One label for all four is failure."""
    rows = []
    for label in ('syntax-code', 'syntax-data', 'rust-partial'):
        st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        c = CL.Closure(st)
        rid = [t for t in st.objects if t.startswith('run3:')][0]
        c.close_run(rid, 'phase8-four:' + label)
        for cid, cv in sorted(c.coverages_seen.items()):
            sc = c.scopes_seen[cv['scopeId']]
            pay = c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                     '#/$defs/CoverageResultV3', 'P8')
            e = pay['entry']
            facts = [f for f in c.facts_seen.values()
                     if f['relation'] == sc['relation']
                     and f['resolution'] == sc['resolution']]
            rows.append({'run': label, 'pair': '%s@%s' % (sc['relation'],
                                                          sc['resolution']),
                         'coverage': e['coverage'], 'deficiency': e.get('deficiency'),
                         'nativeCause': e.get('nativeCause'),
                         'factCount': len(facts),
                         'state': ('complete-empty' if e['coverage'] == 'complete'
                                   and not facts else
                                   'complete-nonempty' if e['coverage'] == 'complete'
                                   else 'partial/unknown-with-a-published-cause')})
    return {
        'requirement': 'R-EMPTY-PARTIAL-UNAVAILABLE-MISSING',
        'classification': 'measured',
        'states': [
            {'state': 'complete-empty',
             'means': 'the question was examined exhaustively and the answer is zero',
             'carriedBy': 'CoverageResultV3 coverage=complete with no matching fact and '
                          'deficiency=null',
             'measuredExample': next((r for r in rows
                                      if r['state'] == 'complete-empty'), None)},
            {'state': 'partial',
             'means': ('the question was examined over an incomplete input: the examined '
                       'part is answered and the unexamined part is disclosed with its own '
                       'cause. The defining feature is that the cause is about the INPUT, '
                       'not about the capability'),
             'carriedBy': 'coverage=unknown WITH a published (deficiency, nativeCause) pair '
                          'whose deficiency is an input deficiency',
             'measuredExample': next(
                 (r for r in rows if r['coverage'] != 'complete'
                  and r['deficiency'] != 'language-tier-unsupported'), None),
             'whyItIsNotTheUnavailableRow': (
                 'input-closure-incomplete / body-language-owner-unenumerated says the '
                 'CAPABILITY EXISTS and the input did not support a complete answer. '
                 'language-tier-unsupported / capability-missing says the capability cannot '
                 'be served at all. The two carry different causes on purpose, and '
                 'R-CLONE-DEFICIENCY-PAIRING is the Run that exhibits the first.')},
            {'state': 'unavailable',
             'means': 'the capability cannot be served for this subject at all',
             'carriedBy': 'coverage=unknown with deficiency=language-tier-unsupported and '
                          'nativeCause=capability-missing',
             'measuredExample': next((r for r in rows
                                      if r.get('deficiency') ==
                                      'language-tier-unsupported'), None)},
            {'state': 'missing committed bytes',
             'means': 'a digest is named but its preimage is not retained',
             'carriedBy': 'NOT a Coverage state at all: it is a CUSTODY refusal at closure',
             'measuredExample': {
                 'artifact': 'vectors/native-join-negative-controls.json',
                 'control': 'grammar-bundle-manifest-bytes-dropped-but-still-a-tree-member',
                 'firstRefusal': '*:PREIMAGE_NOT_RETAINED',
                 'why': ('this is why the four must stay distinct: a missing byte is a '
                         'custody failure of the graph, not an analysis outcome, and it '
                         'cannot be reported as an empty or unavailable result')}},
        ],
        'allMeasuredRows': rows,
        'oneLabelForAllFourWouldBe': (
            'reporting unavailable or partial as complete-empty, which would read as a '
            'finding of zero -- the exact concealment the syntax-data Run refuses'),
    }


def detector_compat(cur):
    """R-DETECTOR-COMPAT-FILE: a detector compatibility LISTING is the reserved authenticated
    FILE, not the component manifest BODY."""
    nat = json.load(open(KIT + '/' + S.doc_path(
        'workflows/schemas/evaluator3/detector-manifest.schema.json')))
    det_tid, det = cur['detector']
    tree = det.get('tree') or []
    reserved = [r for r in tree if 'compat' in r.get('path', '').lower()]
    # V22-D10: generation 20 reported the CLOSURE DESCRIPTOR's keys under the name
    # componentManifestBodyKeys. The component manifest body is the retained blob the descriptor's
    # manifestDigest names; both are reported now, under their own names.
    manifest_keys = []
    mb = cur['store'].get_blob((det.get('manifestDigest') or '').split(':')[-1])
    if mb is not None:
        try:
            def keys_of(n):
                if isinstance(n, dict):
                    for k, v in n.items():
                        manifest_keys.append(k)
                        keys_of(v)
                elif isinstance(n, list):
                    for v in n:
                        keys_of(v)
            keys_of(json.loads(mb.decode()))
            manifest_keys = sorted(set(manifest_keys))
        except (ValueError, UnicodeDecodeError):
            manifest_keys = ['<the retained manifest bytes are not JSON>']
    return {
        'requirement': 'R-DETECTOR-COMPAT-FILE', 'classification': 'measured',
        'law': {'detectorManifest': S.doc_path(
            'workflows/schemas/evaluator3/detector-manifest.schema.json'),
            'title': nat.get('title'),
            'reservedFileKeys': [k for k in json.dumps(nat).split('"')
                                 if 'compat' in k.lower()][:6]},
        'measured': [
            {'check': 'THE_LISTING_IS_A_FILE_IN_THE_SIGNED_TREE_NOT_A_MANIFEST_FIELD',
             'detectorClosureId': det_tid,
             'closureDescriptorKeys': sorted(det),
             'componentManifestDigest': det.get('manifestDigest'),
             'componentManifestBodyKeys': manifest_keys,
             'listingAmongThoseKeys': any('compat' in k.lower()
                                          for k in list(det) + manifest_keys),
             'reservedTreeRows': reserved,
             'result': ('the component manifest body of this origin\'s detector closure '
                        'carries NO compatibility listing field, which is the shape the law '
                        'requires: the listing is a separate authenticated file whose digest '
                        'is a row of the signed tree, so it is covered by the same '
                        'closure identity without becoming part of the manifest body')},
            {'check': 'CANONICAL_METADATA_AND_SIGNED_TREE_OWNERS_APPLY',
             'owners': ['identity-and-evidence section 3 component-manifest-id over C of the '
                        'manifest record', 'the signed closure tree rows (path, sha256)'],
             'result': ('a listing file therefore has exactly the custody of any other tree '
                        'member: its bytes must be retained and re-hash, and changing it '
                        'mints a different closure2 identity')},
            {'check': 'WHY_NOT_THE_MANIFEST_BODY',
             'result': ('putting the listing in the manifest body would make every '
                        'compatibility edit a new component-manifest-id and therefore a new '
                        'closure identity for an unchanged executable, and it would make the '
                        'listing unavailable to a consumer who holds the file set but not '
                        'the manifest record')},
        ],
        'notReconstructedBeyondThis': (
            'this origin did not author a compatibility listing: the requirement is '
            'conditional ("if reconstructed") and what it demands is the DISTINCTION, which '
            'is measured above against the real retained detector closure.'),
    }


SECURITY_DOC = 'security/security-lifecycle.schemas.v1.json'
INVOC_DOC = 'workflows/schemas/evaluator3/invocation-record.schema.json'


def security_admit(selector, inst):
    """security-lifecycle.schemas.v1.json carries no $id, so it is not a member of the pinned
    registry. Its records live under the document's `schemas` member and reference its `$defs`
    by local pointer, so the SAME reference Draft 2020-12 validator is applied to a root holding
    exactly those two members plus a root $ref to the selector; nothing is reimplemented."""
    import jsonschema
    doc = json.load(open(KIT + '/' + S.doc_path(SECURITY_DOC)))
    root = {'$defs': doc['$defs'], 'schemas': doc['schemas'], '$ref': selector}
    errs = sorted(jsonschema.Draft202012Validator(root).iter_errors(inst),
                  key=lambda e: list(e.absolute_path))
    return not errs, [{'path': '/'.join(str(p) for p in e.absolute_path),
                       'message': e.message[:240]} for e in errs[:3]]


def test_prep_repair_auth(cur):
    """R-TEST-PREP-REPAIR-AUTH: authorization RECORDS, not host execution.

    V22-D10: generation 20 published this requirement as an explanatory table (the params
    definition NAMES and refusal code strings), which no process could re-check. The records
    below are CONSTRUCTED and ADMITTED against their owning schemas, bound to this origin's
    admitted repair descriptor and TypeScript Run where the kit gives a join, and each field that
    names a record this reconstruction does not construct is labelled helper-only.
    """
    rep = json.load(open(OUT + '/vectors/repair-descriptor.json'))
    pos = [c for c in rep['controls'] if c['classification'] == 'valid'][0]
    desc = pos['descriptor']
    auth = {'authorizationSchema': 1, 'kind': 'repair-apply', 'projectId': cur['projectId'],
            'repairPlanId': pos['repairPlanId'], 'baseSnapshotId': desc['snapshotId'],
            'recipeClosureId': desc['recipe']['closureId'],
            'consent': {'mode': 'policy-record',
                        'policyRecordId': K.raw_sha256(b'helper-only CI repair policy record'),
                        'ci': True},
            'expiry': 'operation-end', 'leaseMode': 'EXCLUSIVE', 'repositoryExecution': False}
    auth_ref = ('security.repair-apply-authorization.v1:'
                + K.H('security.repair-apply-authorization.v1', auth))
    repair_params = {'kind': 'repair-apply', 'planStep': 1, 'repairPlanId': pos['repairPlanId'],
                     'consentSource': 'policy', 'authorizationRef': auth_ref}
    test_params = {
        'kind': 'test-execution', 'argv': ['node_modules/.bin/vitest', 'run'],
        'argv0Source': {'kind': 'snapshot-member', 'path': 'node_modules/.bin/vitest'},
        'cwdIsRoot': True, 'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner',
        'platformId': 'linux-x86_64-gnu',
        'authorizationRef': ('security.repo-execution-grant.v2:'
                             + K.raw_sha256(b'helper-only repo execution grant')),
        'consentSource': 'pre-existing-policy', 'afterStep': 1, 'timeoutMilliseconds': 600000,
        'maxOutputBytes': 1048576, 'environmentAllowlist': ['CI', 'HOME'],
        'effects': {'network': 'DISCLOSURE-ONLY', 'subprocess': 'DISCLOSURE-ONLY',
                    'filesystemWrite': 'ENFORCED-AT-HOST-BROKER',
                    'environment': 'ENFORCED-BY-CONSTRUCTION'}}
    prep_params = {'kind': 'native-preparation',
                   'authorizationDescriptorDigest': K.raw_sha256(b'helper-only AuthorizedExecutionV2'),
                   'securityGrantSetRef': ('security.repo-execution-grants.v2:'
                                           + K.raw_sha256(b'helper-only grant set'))}

    def inv(selector, inst):
        r = S.admit(INVOC_DOC, selector, inst, 'auth:' + selector)
        return r['admitted'], (r['stockSchemaErrors'][:2] + r['publishedKeywordRefusals'][:2])

    def submitted(role, doc, selector, inst):
        ok, err = (security_admit(selector, inst) if doc == SECURITY_DOC else inv(selector, inst))
        return {'role': role, 'document': doc, 'selector': selector, 'instance': inst,
                'admitted': ok, 'errors': err}

    records = [
        {'step': 'repair-apply', 'paramsDef': 'invocation-record #/$defs/RepairApplyParams',
         'submitted': [submitted('params', INVOC_DOC, '#/$defs/RepairApplyParams', repair_params),
                       submitted('authorization', SECURITY_DOC,
                                 '#/schemas/RepairApplyAuthorizationV1', auth)],
         'identityJoins': {
             'authorizationRefIsProductHOfTheAdmittedAuthorization': repair_params['authorizationRef'] == auth_ref,
             'repairPlanIdIsTheAdmittedPositiveDescriptor': repair_params['repairPlanId'] == pos['repairPlanId'] == auth['repairPlanId'],
             'baseSnapshotIsTheEvidenceRunSnapshot': auth['baseSnapshotId'] == cur['snapshotId']},
         'syntheticHelperOnly': ['authorization.consent.policyRecordId (the policy record is not '
                                 'constructed)'],
         'authorizationClass': 'a security authorization bound to the EXACT repairPlanId and baseSnapshotId',
         'refusals': ['AUTHZ.BASE_SNAPSHOT_MISMATCH', 'AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR',
                      'REPAIR.TARGET_PREIMAGE_MISMATCH', 'REPAIR.SOURCE_MOVED'],
         'd9': 'request-rejected 2 / REQUEST.PRECONDITION_FAILED', 'sealsARun': False,
         'receipt': ('a MutationReceiptV1 keyed by the content-derived repair-apply key; VERIFY '
                     'afterwards admits a FRESH snapshot and seals a NEW Run'),
         'measuredKey': 'vectors/mutation-keys.json repairApply.key'},
        {'step': 'test-execution', 'paramsDef': 'invocation-record #/$defs/TestExecutionParams',
         'submitted': [submitted('params', INVOC_DOC, '#/$defs/TestExecutionParams', test_params)],
         'syntheticHelperOnly': ['authorizationRef (the RepoExecutionGrantV2 grant is not '
                                 'constructed)', 'argv0Source.path (no test runner is inventoried '
                                 'by this origin\'s Runs)'],
         'authorizationClass': 'explicit consent, and in CI a policy record',
         'refusals': ['TEST.INTERACTIVE_CONSENT_IN_CI', 'TEST.CONFINEMENT_CLAIM_REFUSED'],
         'd9': 'request-rejected 2 / REQUEST.PRECONDITION_FAILED', 'sealsARun': False,
         'receipt': 'a test import is admitted; the step mints no run3'},
        {'step': 'native-preparation',
         'paramsDef': 'invocation-record #/$defs/NativePreparationParams',
         'submitted': [submitted('params', INVOC_DOC, '#/$defs/NativePreparationParams', prep_params)],
         'syntheticHelperOnly': ['authorizationDescriptorDigest (AuthorizedExecutionV2 is not '
                                 'constructed)', 'securityGrantSetRef'],
         'authorizationClass': ('per-owner native preparation authorization (workflows section 12 '
                                'delegating to native section 14 and security S15)'),
         'refusals': ['native.execution-not-authorized', 'native.prepare-bound-exceeded',
                      'native.prepared-output-not-inert'],
         'd9': 'request-rejected 2 for authorization, operational-failed 4 for a fault',
         'sealsARun': False,
         'receipt': 'an execution receipt plus ONE admitted prepared import, never a Run',
         'retryPolicy': 'none by schema -- there is no automatic retry'},
    ]
    for r in records:
        assert all(s['admitted'] for s in r['submitted']), (r['step'], r['submitted'])

    hexx = K.raw_sha256(b'another')
    controls = []

    def control(case, step, doc, selector, inst, law_refusal=None, masks=None):
        ok, err = (security_admit(selector, inst) if doc == SECURITY_DOC else inv(selector, inst))
        refused = (not ok) or bool(law_refusal)
        first = ({'boundary': 'owning-schema', 'errors': err} if not ok
                 else ({'boundary': 'prose-law', 'code': law_refusal} if law_refusal else None))
        controls.append({'case': case, 'step': step, 'classification': 'invalid',
                         'document': doc, 'selector': selector, 'instance': inst,
                         'schemaAdmitted': ok, 'lawRefusal': law_refusal, 'refused': refused,
                         'firstRefusal': first,
                         'masksLater': masks or ('the owning schema refuses first, so no prose law '
                                                 'is reached' if not ok else
                                                 'schema admits; the prose law is the first refusal')})
    control('repair-apply-authorization-ref-names-another-domain', 'repair-apply', INVOC_DOC,
            '#/$defs/RepairApplyParams',
            dict(repair_params, authorizationRef='security.repo-execution-grant.v2:' + hexx))
    control('repair-apply-authorization-grants-repository-execution', 'repair-apply',
            SECURITY_DOC, '#/schemas/RepairApplyAuthorizationV1', dict(auth, repositoryExecution=True))
    other_base = dict(auth, baseSnapshotId='snapshot2:' + '0' * 64)
    control('repair-apply-authorization-bound-to-another-base-snapshot', 'repair-apply',
            SECURITY_DOC, '#/schemas/RepairApplyAuthorizationV1', other_base,
            law_refusal=('AUTHZ.BASE_SNAPSHOT_MISMATCH'
                         if other_base['baseSnapshotId'] != cur['snapshotId'] else None))
    control('test-execution-cwd-not-root-without-cwd', 'test-execution', INVOC_DOC,
            '#/$defs/TestExecutionParams', dict(test_params, cwdIsRoot=False))
    control('test-execution-platform-enforcement-claim', 'test-execution', INVOC_DOC,
            '#/$defs/TestExecutionParams',
            dict(test_params, effects=dict(test_params['effects'], network='ENFORCED-PLATFORM:seatbelt')))
    ci = dict(test_params, consentSource='interactive-consent')
    control('test-execution-interactive-consent-in-ci', 'test-execution', INVOC_DOC,
            '#/$defs/TestExecutionParams', ci,
            law_refusal='TEST.INTERACTIVE_CONSENT_IN_CI' if ci['consentSource'] == 'interactive-consent' else None)
    control('native-preparation-grant-set-ref-wrong-prefix', 'native-preparation', INVOC_DOC,
            '#/$defs/NativePreparationParams',
            dict(prep_params, securityGrantSetRef='security.repo-execution-grant.v2:' + hexx))
    assert all(c['refused'] for c in controls), [c['case'] for c in controls if not c['refused']]
    return {
        'requirement': 'R-TEST-PREP-REPAIR-AUTH', 'classification': 'valid + invalid controls',
        'standing': ('authorization RECORDS constructed and admitted against their owning schemas. '
                     'NOTHING was executed: no test ran, no preparation ran, no repair was applied. '
                     'Every field listed under syntheticHelperOnly names a record this '
                     'reconstruction does not construct and is not evidence-bound.'),
        'records': records, 'controls': controls,
        'threeSeparatelyAuthorizedSteps': (
            'preview, apply and verify are three separately authorized steps: a preview '
            'authorization is not an apply authorization, and an apply authorization does '
            'not authorize the verify analysis that follows it.'),
        'whatThisOriginDidNotDo': ['run a test', 'prepare native inputs',
                                   'apply a repair', 'write any product file'],
    }


def purge_replay_output(cur):
    """R-PURGE-REPLAY-OUTPUT-FAILURE: purge, replay and required-output failures."""
    rows = []

    def mk(label, cls, code, detail_code, remedy, subject, exit_code, **extra):
        detail = {'code': detail_code, 'remedy': remedy, 'subject': subject}
        term = dict(cls, domainDetail=detail)
        e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3,
             'kind': 'failure', 'requestId': REQ, 'projectId': cur['projectId'],
             'termination': term, 'exitCode': exit_code, 'errors': [detail]}
        e.update(extra)
        r = EV.admit(e, label)
        r['requirement'] = 'R-PURGE-REPLAY-OUTPUT-FAILURE'
        r['classification'] = 'valid'
        rows.append(r)
        return r

    # V23-D9: each case now names the premise (event position) and the owner text that selects its
    # route. Generation 22 (predecessors.v22/vectors/phase8-all.json) routed a missing retained
    # replay input as indeterminate exit 3 and paired OUTPUT.FORMAT_NOT_APPLICABLE with
    # REQUEST.PRECONDITION_FAILED; both contradicted the owners cited below.
    premises = {
        'purge-after-replay-dependency': {
            'eventPosition': 'a command prerequisite (the retained baseline/replay input the '
                             'command names) is known purged BEFORE evaluation starts',
            'owner': 'docs/v2/contracts/product-v1/identity-and-evidence.md section 5',
            'quote': 'Command-specific comparison-baseline or repair-input prerequisites likewise '
                     'keep request rejection before evaluation (exit 2)'},
        'replay-required-evidence-missing': {
            'eventPosition': 'retained bytes a SELECTED replay needs are found missing while that '
                             'operation runs',
            'owner': 'docs/v2/contracts/product-v1/identity-and-evidence.md section 5; '
                     'workflows/workflow-projection-contract.v3.md section 0 (lost retained bytes '
                     'are a custody route, not correspondence-incomplete)',
            'quote': 'Inability encountered during a selected operation remains HOST.IO_FAILURE '
                     'with evidence detail (exit 4).'},
        'required-output-delivery-failed': {
            'eventPosition': 'the Run committed; the selected required renderer then fails',
            'owner': 'workflows/command-inventory.v3.json goldens analyze-renderer-failed-after-commit '
                     'and audit-renderer-failed-after-comparison',
            'quote': 'DELIVERY.REQUIRED_FAILED / DELIVERY.RENDERER_FAILED_AFTER_COMMIT, '
                     'operational-failed, exit 4'},
        'output-format-not-applicable': {
            'eventPosition': 'a renderer that is not applicable to the command is requested',
            'owner': 'workflows/command-inventory.v3.json golden sarif-not-applicable and the sarif '
                     'renderer parityRule',
            'quote': 'REQUEST.UNKNOWN_OPTION with domainDetail OUTPUT.FORMAT_NOT_APPLICABLE, '
                     'request-rejected, exit 2'},
    }
    mk('purge-after-replay-dependency', {'class': 'request-rejected',
                                         'errorCode': 'REQUEST.PRECONDITION_FAILED'},
       None, 'evidence.purged',
       'the evidence this replay depends on was purged; adopt a new baseline or re-analyse. '
       'Sealed history is retained, so the Run identity still resolves even though its '
       'replay inputs do not',
       cur['runId'], 2)
    mk('replay-required-evidence-missing', {'class': 'operational-failed',
                                            'errorCode': 'HOST.IO_FAILURE',
                                            'faultCause': 'host-io'},
       None, 'evidence.missing',
       'retained bytes the replay needs are missing from the store; restore them from a verified '
       'backup or re-analyse. A lost input is neither a negative finding nor an indeterminate '
       'verdict',
       cur['runId'], 4)
    mk('required-output-delivery-failed', {'class': 'operational-failed',
                                           'errorCode': 'DELIVERY.REQUIRED_FAILED',
                                           'faultCause': 'delivery-required',
                                           'runId': cur['runId']},
       None, 'DELIVERY.RENDERER_FAILED_AFTER_COMMIT',
       'the Run was committed and the REQUIRED output could not be delivered; the commit is '
       'not rolled back and the failure is operational, not a policy verdict',
       'json renderer', 4)
    mk('output-format-not-applicable', {'class': 'request-rejected',
                                        'errorCode': 'REQUEST.UNKNOWN_OPTION'},
       None, 'OUTPUT.FORMAT_NOT_APPLICABLE',
       'the requested format is not applicable to this command; use json or agent',
       'sarif for a mutation command', 2)
    for r in rows:
        r['premise'] = premises[r['label']]
    return {'envelopes': rows,
            'summary': {
                'requirement': 'R-PURGE-REPLAY-OUTPUT-FAILURE',
                'cases': [r['label'] for r in rows],
                'predecessor': 'predecessors.v22/vectors/phase8-all.json (V23-D9)',
                'distinctions': {
                    'purgedVsMissing': ('evidence.purged is a DELIBERATE removal under an '
                                        'authorized purge; evidence.missing is an absence '
                                        'the host did not authorize. Both refuse, with '
                                        'different codes and different remedies.'),
                    'requiredOutputAfterCommit': ('a delivery failure AFTER the commit is '
                                                  'operational-failed with '
                                                  'faultCause=delivery-required and keeps '
                                                  'the runId: the Run exists and the '
                                                  'verdict is not reclassified'),
                    'eventPositionDecidesTheRoute': (
                        'a purged prerequisite known before evaluation is request-rejected exit 2; '
                        'missing bytes met during the selected operation are HOST.IO_FAILURE exit '
                        '4; only successfully admitted PARTIAL native inputs give an indeterminate '
                        'Run (exit 3), which is not this case'),
                }}}


def public_termination(cur):
    """R-PUBLIC-TERMINATION-EXAMPLES -- one PUBLIC example per D9 termination class.

    V23-D11: generation 22 (predecessors.v22/envelopes/public-termination.json) bound a `pass` and a
    `fail` AnalysisResult to the REAL TypeScript Run, whose sealed verdict is indeterminate, and
    paired codes no owner pairs (REQUEST.UNKNOWN_OPTION with CONFIG.INVALID, a coverage reason with
    evidence.missing, LEDGER.BUSY_TIMEOUT with storage.backup-choice-required, an interrupt carrying
    an evidence.missing error). Each example now reproduces the command-inventory.v3 golden it
    cites; a Run identity no retained Run can supply (every retained Run is sealed indeterminate)
    is a labelled synthetic helper-only value."""
    rows = []
    gold = {g['id']: g for g in json.load(open(KIT + '/' + S.doc_path(
        'workflows/command-inventory.v3.json')))['goldens']}

    def synthetic(domain, what):
        return domain + ':' + K.raw_sha256(('synthetic-helper-only:public-termination:' + what).encode())

    def mk(label, golden, term, kind, synthetic_fields=(), note=None, **extra):
        g = gold[golden]
        e = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 3, 'kind': kind,
             'requestId': REQ, 'projectId': cur['projectId'],
             'termination': term, 'exitCode': EV.EXIT_BY_CLASS[term['class']]}
        e.update(extra)
        r = EV.admit(e, label)
        r['requirement'] = 'R-PUBLIC-TERMINATION-EXAMPLES'
        r['classification'] = 'valid'
        r['d9Class'] = term['class']
        r['golden'] = {k: g.get(k) for k in ('id', 'command', 'situation', 'class', 'exitCode',
                                             'errorCode', 'reasonCode', 'domainDetail')}
        r['syntheticHelperOnly'] = list(synthetic_fields)
        if note:
            r['standing'] = note
        rows.append(r)
        return r

    def detail(g, subject):
        return {'code': g['domainDetail'], 'remedy': g['remedy'], 'subject': subject}

    def run_block(run_id, plan_id, verdict):
        return {'kind': 'analysis', 'authority': 'authoritative', 'runId': run_id, 'planId': plan_id,
                'verdict': verdict, 'requiredCoverage': 'satisfied', 'durability': 'committed',
                'deficiency': 'none', 'secondaryDeficiencies': []}

    r1, p1 = synthetic('run3', 'pass-run'), synthetic('plan2', 'pass-plan')
    mk('termination-success', 'default-first-use-durable', {'class': 'success'}, 'run',
       ['run.runId', 'run.planId'], run=run_block(r1, p1, 'pass'))
    r2, p2 = synthetic('run3', 'fail-run'), synthetic('plan2', 'fail-plan')
    mk('termination-policy-failed', 'analyze-policy-failed', {'class': 'policy-failed', 'runId': r2},
       'run', ['run.runId', 'run.planId', 'termination.runId'], run=run_block(r2, p2, 'fail'))
    g = gold['import-unmapped-artifact']
    d = detail(g, 'import artifact')
    mk('termination-request-rejected', g['id'],
       {'class': 'request-rejected', 'errorCode': g['errorCode'], 'domainDetail': d},
       'failure', errors=[d])
    g = gold['audit-required-coverage-unknown-zero-findings']
    d = detail(g, 'audit comparison')
    mk('termination-indeterminate', g['id'],
       {'class': 'indeterminate', 'reasonCodes': [g['reasonCode']], 'domainDetail': d},
       'failure', errors=[d])
    g = gold['default-closure-bytes-corrupt']
    d = detail(g, 'selected closure')
    mk('termination-operational-failed', g['id'],
       {'class': 'operational-failed', 'errorCode': g['errorCode'], 'faultCause': 'host-io',
        'domainDetail': d}, 'failure', errors=[d])
    inv = {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 3, 'requestId': REQ,
           'projectId': cur['projectId'], 'workflow': {'kind': 'builtin', 'name': 'analyze'},
           'mode': {'interactive': False, 'ci': True, 'ephemeral': False},
           'orderedSteps': [{'stepId': 0, 'kind': 'analysis', 'requirement': 'required',
                             'dependsOn': [], 'dependencyGate': 'completed',
                             'retryPolicy': 'idempotent-retry',
                             'params': {'kind': 'analysis', 'profile': 'default', 'role': 'primary',
                                        'verdictGate': 'self', 'durability': 'authoritative',
                                        'snapshotSource': 'live-worktree'}}],
           'stepResults': [{'stepId': 0, 'outcome': 'cancelled', 'attempts': [],
                            'termination': {'class': 'interrupted', 'signal': 'SIGINT'}}],
           'termination': {'class': 'interrupted', 'signal': 'SIGINT'},
           'terminationEmitted': True,
           'retentionDisclosure': {'policy': 'durable-unbounded', 'provenance': 'DEFAULTED',
                                   'firstUse': False, 'storageRoot': '.opensip'}}
    mk('termination-interrupted-before-settle', 'interrupted-before-settle', inv['termination'],
       'invocation', note=(
           'workflows-and-surfaces section 1 Cancellation: before settle the remaining steps are '
           '`cancelled`, the aggregate is `interrupted` (130) and an aborted analysis attempt leaves '
           'no Run, so no runId. Carried as kind=invocation because kind=failure requires a '
           'DomainDetail and no registered code names an interruption (advisory V23-A1). Only the '
           'analysis step is modelled; the import and render steps the inventory lists for analyze '
           'are not.'), invocation=inv)
    return {'envelopes': rows,
            'summary': {'requirement': 'R-PUBLIC-TERMINATION-EXAMPLES',
                        'classesCovered': sorted({r['d9Class'] for r in rows}),
                        'exitTable': EV.EXIT_BY_CLASS,
                        'goldensCited': [r['golden']['id'] for r in rows],
                        'predecessor': 'predecessors.v22/envelopes/public-termination.json (V23-D11)',
                        'afterSettleIsNeverReclassified': (
                            'the interrupted example carries NO runId, because a runId is '
                            'lawful there only when a Run was committed before the '
                            'interrupt; an interrupt after settle keeps the settled class '
                            'instead of becoming interrupted')}}


def subsystem_owners():
    return {
        'requirement': 'R-SUBSYSTEM-OWNERS', 'classification': 'explanatory',
        'owners': [
            {'decision': 'what bytes are in the snapshot and what their digests are',
             'subsystem': 'identity (foundation)',
             'selector': 'identity-and-evidence section 3 + identity-schemas.v3 snapshot2'},
            {'decision': 'which relation@rung a fact may carry and what its payload is',
             'subsystem': 'relation registry (foundation)',
             'selector': 'relation-payload-schemas.v2 x-opensip-relation-registry'},
            {'decision': 'what a native context/universe must agree with',
             'subsystem': 'native evidence',
             'selector': 'native-evidence sections 1-3, 11 + '
                         'x-opensip-digest-domains domainSets'},
            {'decision': 'whether a capability can be served at all for a language',
             'subsystem': 'native evidence (grammar capability registry)',
             'selector': 'native-evidence x-opensip-grammar-capability-registry'},
            {'decision': 'which rules are admitted and which predicates they evaluate',
             'subsystem': 'evaluator (composition v3)',
             'selector': 'workflows-and-surfaces section 5 + composition sections 1/2/9'},
            {'decision': 'the verdict of a Run',
             'subsystem': 'evaluator seal',
             'selector': 'composition v3 section 9.7 seal3'},
            {'decision': 'the verdict of an AUDIT',
             'subsystem': 'comparison',
             'selector': 'comparison-result AuditProfile + the comparison STEP, which is '
                         'the only step whose verdict gates an audit'},
            {'decision': 'whether a pivot may be executed and whether it is deterministic',
             'subsystem': 'comparison + closure custody',
             'selector': 'comparison-result IndeterminateReason pivot-* members'},
            {'decision': 'the D9 class, exit code and error code of a request',
             'subsystem': 'workflow host',
             'selector': 'workflows section 9 + common StepTermination'},
            {'decision': 'whether a mutation may happen at all',
             'subsystem': 'security authorization',
             'selector': 'AUTHZ.* detail codes + security unit; workflows explicitly does '
                         'NOT decide authorization'},
            {'decision': 'whether an output format is applicable',
             'subsystem': 'renderer inventory',
             'selector': 'command-inventory renderers[].applicability + '
                         'OUTPUT.FORMAT_NOT_APPLICABLE'},
            {'decision': 'what a retained import may prove',
             'subsystem': 'imported evidence',
             'selector': 'imported-evidence StalenessRule + '
                         'x-opensip-imported-requirement-law'},
        ],
        'whatIsNotOwnedHere': (
            'no subsystem in this kit authorizes a product implementation, and this origin '
            'claims none.'),
    }


main()
