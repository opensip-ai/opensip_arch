"""Phase 6 repair / mutation reconstruction, built on the REAL admitted TypeScript Run.

  R-REPAIR-DESCRIPTOR               RepairPlanDescriptor reconstructed from that Run's native
                                    evidence, with repairPlanId = H('workflow.repair-plan', d).
  R-REPAIR-AUTHORITY-PER-TARGET     the authority boundary and the per-target requirements,
                                    with independently chosen discriminating controls.
  R-MIN-RESOLUTION-REPAIR-EVIDENCE  evidenceRequirements rows produced by the SAME
                                    sufficiency_v2 results as the min-resolution cases, over
                                    BOTH evidence planes.
  R-MUTATION-REPLAY-SCOPE           MutationReplayScopeV1 and its H('workflow.mutation-intent')
                                    key.
  R-REPAIR-APPLY-KEY                the repair-apply key, measured to be a DIFFERENT recipe
                                    over DIFFERENT inputs -- not the same value under a new
                                    name.
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
import opensip_eval as E

OUT = '/tmp/opensip-design-corrections/consumer-b.v16/output'
KIT = S.KIT
REPAIR_DOC = 'workflows/schemas/evaluator3/repair.schema.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'

NATIVE_RELATIONS = None
IMPORTED_RELATIONS = None


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


def load_ts():
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    c = CL.Closure(st)
    rid = [t for t in st.objects if t.startswith('run3:')][0]
    rep = c.close_run(rid, 'phase6-repair')
    assert rep['admitted'], rep['refusals'][:2]
    return st, c, rid, doc


# --------------------------------------------------------------------- admission laws
def admit_descriptor(desc, plan_id, run_facts):
    """The laws the repair schema DELEGATES to admission, implemented here because stock
    JSON Schema cannot express them. Returns the ordered refusals."""
    ref = []

    def bad(code, detail):
        ref.append({'code': code, 'detail': detail})

    # 1. identity
    want = K.ID('workflow.repair-plan', desc)
    if plan_id != want:
        bad('REPAIR_PLAN_ID_IS_H_OF_THE_DESCRIPTOR',
            {'declared': plan_id, 'recomputed': want})
    # 2. evidence-requirement PLANE, decided from the relation's registry membership
    for i, r in enumerate(desc['evidenceRequirements']):
        rel = r['relation']
        native = rel in NATIVE_RELATIONS
        imported = rel in IMPORTED_RELATIONS
        if native == imported:
            bad('EVIDENCE_REQUIREMENT_RELATION_REGISTERED_IN_EXACTLY_ONE_PLANE', rel)
            continue
        if native and r['minResolution'] not in NATIVE_RELATIONS[rel]['ladder']:
            bad('REQUIREMENT_RUNG_ON_THIS_RELATIONS_LADDER',
                {'relation': rel, 'rung': r['minResolution'],
                 'ladder': NATIVE_RELATIONS[rel]['ladder']})
        dv = r.get('deficiency')
        if dv is None:
            if not r['satisfied']:
                bad('UNSATISFIED_REQUIREMENT_STATES_ITS_DEFICIENCY', rel)
            continue
        if native and dv not in NATIVE_DEF:
            bad('CROSS_PLANE_DEFICIENCY_VALUE:NATIVE_RELATION_CARRIES_AN_IMPORTED_VALUE',
                {'relation': rel, 'value': dv})
        if imported and dv not in IMPORTED_DEF:
            bad('CROSS_PLANE_DEFICIENCY_VALUE:IMPORTED_RELATION_CARRIES_A_NATIVE_VALUE',
                {'relation': rel, 'value': dv})
    # 3. every target is a fingerprint of the evidence Run, and a matched one
    for t in desc['targets']:
        if t not in run_facts['fingerprints']:
            bad('REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE', t)
    # 4. unsafe edits need the evidence Run's OWN ClosedWorldV2, read before the projection
    unsafe = [e for e in desc['edits'] if e['action'] in ('delete', 'replace')]
    if unsafe and not run_facts['closedWorld']['deadCodeRepairEligible']:
        bad('REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
            {'unsafeEdits': [e['path'] for e in unsafe],
             'evidenceRunDeadCodeRepairEligible': False,
             'reasonsFromThatRecord': run_facts['closedWorld'].get('reasons')})
    if unsafe and desc['evidenceOrigin'] == 'imported-prepared-declared':
        bad('IMPORTED_PREPARED_DECLARED_IS_NEVER_AUTHORITY_FOR_AN_UNSAFE_EDIT',
            desc['evidenceOrigin'])
    # 5. the projection is the five fields of that same record, unchanged
    for f in ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
              'nonliteralLoading', 'externalConsumers'):
        if desc['closedWorld'][f] != run_facts['closedWorld'][f]:
            bad('CLOSED_WORLD_PROJECTION_TAKEN_UNCHANGED_FROM_THE_EVIDENCE_RUN',
                {'field': f, 'descriptor': desc['closedWorld'][f],
                 'evidenceRun': run_facts['closedWorld'][f]})
    # 6. edits: ordering, uniqueness, scope, byte accounting, bounds
    paths = [e['path'] for e in desc['edits']]
    if paths != sorted(paths, key=lambda p: p.encode()):
        bad('EDITS_SORTED_ASCENDING_BY_PATH_UTF8_BYTES', paths)
    if len(set(paths)) != len(paths):
        bad('EDIT_PATH_UNIQUE', paths)
    for e in desc['edits']:
        if not any(E.glob_match(g, e['path']) for g in desc['permittedEditScope']):
            bad('EDIT_WITHIN_PERMITTED_EDIT_SCOPE',
                {'path': e['path'], 'scope': desc['permittedEditScope']})
        if e['postimageBytes'] > 16 * 1024 * 1024:
            bad('PER_POSTIMAGE_AT_MOST_16_MIB', e['path'])
        if e['action'] == 'create' and e['preimageDigest'] is not None:
            bad('CREATE_HAS_NO_PREIMAGE', e['path'])
        if e['action'] == 'delete' and e['postimageDigest'] is not None:
            bad('DELETE_HAS_NO_POSTIMAGE', e['path'])
        if e['action'] == 'replace' and (e['preimageDigest'] is None
                                         or e['postimageDigest'] is None):
            bad('REPLACE_HAS_BOTH_IMAGES', e['path'])
    tot = sum(e['postimageBytes'] for e in desc['edits'])
    if desc['totalPostimageBytes'] != tot:
        bad('TOTAL_POSTIMAGE_BYTES_IS_THE_SUM',
            {'declared': desc['totalPostimageBytes'], 'measured': tot})
    if tot > 64 * 1024 * 1024:
        bad('TOTAL_POSTIMAGE_AT_MOST_64_MIB', tot)
    if len(desc['targets']) > 4096 or len(desc['edits']) > 4096:
        bad('AT_MOST_4096_TARGET_FILES', len(desc['edits']))
    # 7. applicability
    all_sat = all(r['satisfied'] for r in desc['evidenceRequirements'])
    want_app = all_sat and not desc['unmetPreconditions']
    if desc['applicable'] != want_app:
        bad('APPLICABLE_IFF_EVERY_REQUIREMENT_SATISFIED_AND_NO_UNMET_PRECONDITION',
            {'declared': desc['applicable'], 'derived': want_app})
    if desc['applicable'] and desc['recipeTrust'] != 'admitted':
        bad({'not-admitted': 'REPAIR.RECIPE_TRUST_NOT_ADMITTED',
             'revoked': 'REPAIR.RECIPE_TRUST_REVOKED'}[desc['recipeTrust']],
            desc['recipeTrust'])
    return ref


def schema_admit(plan):
    try:
        S.admit(REPAIR_DOC, '#/$defs/RepairPlanV1', plan, 'repair-plan')
        return True, None
    except Exception as e:
        return False, str(e)[:600]


# --------------------------------------------------------------------- the reconstruction
def evidence_from_run():
    st, c, rid, doc = load_ts()
    fps, findings = [], []
    for tid, rec in sorted(st.objects.items()):
        if tid.startswith('finding-key2:'):
            fps.append(tid)
        if tid.startswith('finding3:'):
            findings.append((tid, rec))
    # the evidence Run's own ClosedWorldV2: every Coverage entry carries one; the repair law
    # says "that same Run's ClosedWorldV2", and this Run's entries agree, which is recorded
    cws = []
    for cid, cv in sorted(c.coverages_seen.items()):
        pay = c.canonical_record(cv['payloadDigest'], B.NATIVE_DOC,
                                 '#/$defs/CoverageResultV3', 'P6R')
        cws.append(pay['entry']['closedWorld'])
    distinct = {K.C(x) for x in cws}
    run = c.resolved.get(rid) or c.typed(rid, 'run', 'RUN')
    plan_rec = None
    for tid, rec in st.objects.items():
        if tid.startswith('plan2:'):
            plan_rec = rec
    return {'store': st, 'closure': c, 'runId': rid, 'fingerprints': fps,
            'findings': findings, 'closedWorld': cws[0],
            'closedWorldDistinctRecordsInThisRun': len(distinct),
            'closedWorldAgreementNote': (
                'this Run carries %d Coverage entries whose ClosedWorldV2 records reduce to '
                '%d distinct canonical value(s); the repair law names "that same Run\'s '
                'ClosedWorldV2" without saying which Coverage entry owns it when a Run has '
                'several, which is recorded as an observation, not worked around.'
                % (len(cws), len(distinct))),
            'snapshotId': plan_rec['snapshotId'], 'planId': run['planId'],
            'projectId': (plan_rec.get('projectId')
                          or c.snap.get('projectId') if hasattr(c, 'snap') else None)}


def descriptor(ev, *, unsafe=False, origin='native-analysis', trust='admitted',
               reqs=None, targets=None, edits=None, scope=None, unmet=None,
               closed_world=None, applicable=None, limitations=None):
    cw = closed_world or {f: ev['closedWorld'][f] for f in
                          ('deadCodeRepairEligible', 'exportsClosed',
                           'entryPointsRecognized', 'nonliteralLoading',
                           'externalConsumers')}
    POST = b'export function pad2(s) { return s.padStart(2, "0"); }\n// repaired\n'
    if edits is None:
        edits = [{'path': 'src/legacy.js', 'action': 'replace' if unsafe else 'create',
                  'preimageDigest': (K.raw_sha256(
                      b'export function pad2(s) { return s.padStart(2, "0"); }\n')
                      if unsafe else None),
                  'postimageDigest': K.raw_sha256(POST),
                  'postimageBytes': len(POST)}]
    if reqs is None:
        reqs = [{'relation': 'clones', 'minResolution': 'normalized-body-hash',
                 'completeness': 'complete', 'satisfied': True},
                {'relation': 'imports', 'minResolution': 'resolved-target',
                 'completeness': 'complete', 'satisfied': True}]
    desc = {
        'schemaFamily': 'opensip.product.repair-plan', 'schemaMajor': 2,
        'projectId': ev['projectId'], 'snapshotId': ev['snapshotId'],
        'evidenceRunId': ev['runId'], 'planId': ev['planId'],
        'recipe': {'contributionId': 'contrib.clone-hygiene',
                   'recipeId': 'clone-hygiene.extract-shared-body',
                   'recipeVersion': '1.2.0',
                   'closureId': ev['findings'][0][1].get('detectorClosureId')
                   or [t for t in ev['store'].objects if t.startswith('closure2:')][0]},
        'recipeTrust': trust, 'evidenceOrigin': origin, 'closedWorld': cw,
        'targets': targets if targets is not None else [ev['fingerprints'][0]],
        'edits': sorted(edits, key=lambda e: e['path'].encode()),
        'totalPostimageBytes': sum(e['postimageBytes'] for e in edits),
        'evidenceRequirements': reqs,
        # `**` is a WHOLE-SEGMENT wildcard matching zero or more segments, and the only
        # published semantics (`**/*.ts` matches root `a.ts`) is the one the evaluator
        # implements. A TRAILING `**` is therefore written as `**/*` so the final segment is
        # matched explicitly rather than relying on an unstated convention.
        'permittedEditScope': scope if scope is not None else ['src/**/*'],
        'applicable': applicable,
        'unmetPreconditions': unmet or [],
        'limitations': limitations or [],
    }
    if desc['applicable'] is None:
        desc['applicable'] = (all(r['satisfied'] for r in desc['evidenceRequirements'])
                              and not desc['unmetPreconditions'])
    return desc


def case(ev, label, classification, expect, **kw):
    desc = descriptor(ev, **kw)
    plan_id = K.ID('workflow.repair-plan', desc)
    if kw.get('_break_identity'):
        plan_id = 'repairplan2:' + '0' * 64
    plan = {'repairPlanId': plan_id, 'descriptor': desc}
    ok, err = schema_admit(plan)
    refs = admit_descriptor(desc, plan_id, ev) if ok else []
    row = {'case': label, 'classification': classification,
           'repairPlanId': plan_id,
           'owningSchemaAdmitted': ok, 'owningSchemaError': err,
           'delegatedAdmissionRefusals': refs,
           'firstRefusal': (refs[0] if refs else
                            ({'code': 'OWNING_SCHEMA', 'detail': err} if not ok else None)),
           'admitted': ok and not refs,
           'expectedOwnerJoin': expect,
           'descriptor': desc}
    if expect:
        got = json.dumps(row['firstRefusal'] or {})
        row['firstRefusalIsTheIntendedJoin'] = expect in got
    return row


def main():
    global NATIVE_RELATIONS, IMPORTED_RELATIONS, NATIVE_DEF, IMPORTED_DEF
    NATIVE_RELATIONS = kitdoc(B.RELATION_DOC)['x-opensip-relation-registry']['relations']
    imp = kitdoc(IMPORTED_DOC)
    IMPORTED_RELATIONS = imp['x-opensip-evidence-relation-registry']['relations']
    common = kitdoc('workflows/schemas/evaluator3/common.schema.json')
    NATIVE_DEF = set(common['$defs']['NativeSufficiencyDeficiency']['enum'])
    IMPORTED_DEF = set(common['$defs']['ImportedRequirementDeficiency']['enum'])

    ev = evidence_from_run()
    pos = case(ev, 'repair-descriptor-positive-safe-create', 'valid', None)
    rows = [pos]
    # ---- per-target / authority controls
    rows.append(case(ev, 'unsafe-replace-without-deadCodeRepairEligible', 'invalid',
                     'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED', unsafe=True))
    cw_true = {'deadCodeRepairEligible': True, 'exportsClosed': 'closed',
               'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
               'externalConsumers': 'none-declared'}
    # THE DISTINGUISHING PAIR. Editing the descriptor's five-field projection to say the
    # closed world is established does NOT move the gate: the gate reads the evidence Run's
    # own ClosedWorldV2, so the unsafe case still refuses AT THE GATE...
    r = case(ev, 'unsafe-replace-with-a-forged-projection-still-refuses-at-the-gate',
             'invalid', 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
             unsafe=True, closed_world=cw_true)
    r['whyThisIsTheDistinguishingControl'] = (
        'the projection was edited to the permissive value and the refusal did not move: '
        'authority is read from the evidence Run, and the projection is carried for display '
        'and for the repairplan2 identity only.')
    rows.append(r)
    # ...and the projection check itself is isolated by a SAFE edit, where no gate applies
    rows.append(case(ev, 'safe-create-with-a-projection-that-contradicts-the-run',
                     'invalid',
                     'CLOSED_WORLD_PROJECTION_TAKEN_UNCHANGED_FROM_THE_EVIDENCE_RUN',
                     unsafe=False, closed_world=cw_true))
    rows.append(case(ev, 'target-is-not-a-fingerprint-of-the-evidence-run', 'invalid',
                     'REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE',
                     targets=['finding-key2:' + 'a' * 64]))
    rows.append(case(ev, 'edit-outside-the-permitted-edit-scope', 'invalid',
                     'EDIT_WITHIN_PERMITTED_EDIT_SCOPE', scope=['docs/**/*']))
    rows.append(case(ev, 'applicable-true-with-an-unmet-precondition', 'invalid',
                     'APPLICABLE_IFF_EVERY_REQUIREMENT_SATISFIED',
                     unmet=['REPAIR.CLOSED_WORLD_NOT_ESTABLISHED'], applicable=True))
    rows.append(case(ev, 'applicable-true-while-the-recipe-trust-is-revoked', 'invalid',
                     'REPAIR.RECIPE_TRUST_REVOKED', trust='revoked'))
    # ---- R-MIN-RESOLUTION-REPAIR-EVIDENCE: both planes, cross-plane refused
    both = [{'relation': 'types', 'minResolution': 'checked', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'required-relation-missing'},
            {'relation': 'runtime-observation', 'minResolution': 'observed',
             'completeness': 'partial-acceptable', 'satisfied': False,
             'deficiency': 'import-unmapped-only'}]
    rows.append(case(ev, 'evidence-requirements-over-both-planes', 'valid', None,
                     reqs=both, unmet=['REPAIR.EVIDENCE_INSUFFICIENT'],
                     applicable=False))
    cross = [{'relation': 'types', 'minResolution': 'checked', 'completeness': 'complete',
              'satisfied': False, 'deficiency': 'import-unmapped-only'}]
    rows.append(case(ev, 'native-requirement-carrying-an-imported-deficiency-value',
                     'invalid', 'CROSS_PLANE_DEFICIENCY_VALUE', reqs=cross,
                     unmet=['x'], applicable=False))
    cross2 = [{'relation': 'runtime-observation', 'minResolution': 'observed',
               'completeness': 'complete', 'satisfied': False,
               'deficiency': 'resolution-incomplete'}]
    rows.append(case(ev, 'imported-requirement-carrying-a-native-deficiency-value',
                     'invalid', 'CROSS_PLANE_DEFICIENCY_VALUE', reqs=cross2,
                     unmet=['x'], applicable=False))
    rows.append(case(ev, 'requirement-rung-not-on-that-relations-ladder', 'invalid',
                     'REQUIREMENT_RUNG_ON_THIS_RELATIONS_LADDER',
                     reqs=[{'relation': 'clones', 'minResolution': 'resolved-target',
                            'completeness': 'complete', 'satisfied': True}]))

    # ---- R-MUTATION-REPLAY-SCOPE and R-REPAIR-APPLY-KEY
    scope_rec = {'schemaVersion': 1, 'requestId': 'req-7f3a1c', 'stepId': 'step-2',
                 'projectId': ev['projectId'], 'operation': 'purge'}
    mutation_key = K.H('workflow.mutation-intent', scope_rec)
    apply_pre = {'operation': 'repair-apply', 'projectId': ev['projectId'],
                 'repairPlanId': pos['repairPlanId'],
                 'baseSnapshotId': ev['snapshotId']}
    apply_key = K.raw_sha256(K.C(apply_pre))
    import_scope = dict(scope_rec, operation='import')
    prep_scope = dict(scope_rec, operation='native-preparation')
    keys = {
        'requirement': ['R-MUTATION-REPLAY-SCOPE', 'R-REPAIR-APPLY-KEY'],
        'law': (REPAIR_DOC + '#/x-opensip-mutation-operation-map/'
                'receiptIdempotencyKeyByStepKind/recipes'),
        'genericMutation': {
            'recipe': 'H("workflow.mutation-intent", MutationReplayScopeV1)',
            'preimage': scope_rec, 'key': mutation_key,
            'isBare64Hex': True,
            'whyBare': ('workflows section 10: workflow.mutation-intent returns its BARE '
                        '64-hex H value, so it takes no typed prefix'),
            'lookupMeaning': ('an equal COMPLETED receipt permits delivery replay with no '
                              'second effect; different fresh requests never deduplicate')},
        'repairApply': {
            'recipe': 'raw SHA-256 of C({operation, projectId, repairPlanId, '
                      'baseSnapshotId})',
            'preimage': apply_pre, 'key': apply_key,
            'isAnHIdentity': False,
            'whyDifferent': ('content-derived, NOT request-scoped: no requestId and no '
                             'stepId appear, so the same plan over the same base snapshot '
                             'has ONE key across separate requests -- the opposite property '
                             'from the generic recipe'),
            'excludedFromTheGenericFields': True},
        'importStep': {'preimage': import_scope,
                       'key': K.H('workflow.mutation-intent', import_scope)},
        'nativePreparationStep': {'preimage': prep_scope,
                                  'key': K.H('workflow.mutation-intent', prep_scope)},
        'measuredInequalities': {
            'genericMutationVsRepairApply': mutation_key != apply_key,
            'repairApplyIsNotHOverTheSamePreimage':
                apply_key != K.H('workflow.mutation-intent', apply_pre),
            'importVsNativePreparation':
                K.H('workflow.mutation-intent', import_scope)
                != K.H('workflow.mutation-intent', prep_scope),
            'importVsGeneric': K.H('workflow.mutation-intent', import_scope)
                               != mutation_key,
            'note': ('the three H-based keys differ ONLY in the operation token, which is '
                     'what the law says; the repair-apply key differs in RECIPE, not just '
                     'in a field value, and is not an H identity at all')},
        'repairApplyIsRefusedByTheGenericOperationEnum': 'repair-apply' not in set(
            kitdoc(REPAIR_DOC)['x-opensip-mutation-operation-map'][
                'admissibleGenericFieldDomain']['operations']),
    }

    doc = {'consumerId': 'consumer-b.v16',
           'standing': ('reconstructed from the admitted TypeScript Run. No repair was '
                        'previewed, applied or authorized against any product: these are '
                        'record reconstructions and admission controls only.'),
           'evidenceRun': {'runId': ev['runId'], 'snapshotId': ev['snapshotId'],
                           'planId': ev['planId'],
                           'fingerprintCount': len(ev['fingerprints']),
                           'closedWorldV2FromTheRun': ev['closedWorld'],
                           'closedWorldNote': ev['closedWorldAgreementNote']},
           'controls': rows, 'idempotencyKeys': keys}
    with open(OUT + '/vectors/repair-descriptor.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    with open(OUT + '/vectors/mutation-keys.json', 'w') as f:
        json.dump(keys, f, indent=1, default=str)

    bad = []
    for r in rows:
        want_admit = r['classification'] == 'valid'
        okk = (r['admitted'] == want_admit
               and (want_admit or r.get('firstRefusalIsTheIntendedJoin', True)))
        print('%-58s %-8s admitted=%-5s first=%s'
              % (r['case'][:58], r['classification'], r['admitted'],
                 json.dumps(r['firstRefusal'] or {}, default=str)[:90]))
        if not okk:
            bad.append((r['case'], r['expectedOwnerJoin'], r['firstRefusal'],
                        r['owningSchemaError']))
    print()
    for k, v in keys['measuredInequalities'].items():
        if k != 'note':
            print('  inequality %-34s %s' % (k, v))
    print('  repair-apply excluded from the generic operation enum:',
          keys['repairApplyIsRefusedByTheGenericOperationEnum'])
    if bad:
        print('\nFAILURES:', json.dumps(bad, indent=1, default=str)[:2500])
    assert not bad, [b[0] for b in bad]
    assert all(v for k, v in keys['measuredInequalities'].items() if k != 'note')


main()
