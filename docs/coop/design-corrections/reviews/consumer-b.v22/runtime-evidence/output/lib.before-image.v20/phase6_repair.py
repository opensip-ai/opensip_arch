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
import repair_selection_v19 as RS

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
KIT = S.KIT
REPAIR_DOC = 'workflows/schemas/evaluator3/repair.schema.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'

NATIVE_RELATIONS = None
IMPORTED_RELATIONS = None
# the SELECTED evidence snapshot's own source inventory, path -> row. Set in main() from the
# retained snapshot2 of the evidence Run, never from a local observation of the fixture.
SNAPSHOT_INVENTORY = {}


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


def DD(code, remedy):
    """A DomainDetail: the closed registry code plus its REMEDY. unmetPreconditions members are
    these objects, never bare strings (V19-D4)."""
    return {'code': code, 'remedy': remedy}


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
    # 4. THE SELECTED SNAPSHOT JOIN AND THE PER-EDIT ACTION SHAPE, evaluated BEFORE the
    # closed-world gate. The kit orders the gate only against the PROJECTION ("the prerequisite
    # ... is decided against the evidence Run's own ClosedWorldV2 BEFORE this projection is
    # built"); it publishes no ordering between the gate and the snapshot-condition join, and
    # both are admission obligations. Evaluating the snapshot join first is what makes the
    # intended law REACHABLE: otherwise every replace/delete control on a Run whose closed
    # world is not established is answered by the gate, and the snapshot join would never be
    # exercised -- an invalid prerequisite masking the guard under test.
    inv = SNAPSHOT_INVENTORY
    for e in desc['edits']:
        row = inv.get(e['path'])
        if e['action'] == 'create':
            if row is not None:
                bad('REPAIR.CREATE_PATH_ALREADY_IN_THE_SELECTED_SNAPSHOT',
                    {'path': e['path'], 'snapshotDigest': row['sha256']})
            if e['preimageDigest'] is not None:
                bad('CREATE_HAS_NO_PREIMAGE', e['path'])
            if e['postimageDigest'] is None:
                bad('CREATE_HAS_A_POSTIMAGE', e['path'])
        elif e['action'] == 'delete':
            if row is None:
                bad('REPAIR.SOURCE_MOVED', {'path': e['path'], 'action': 'delete'})
            elif e['preimageDigest'] != row['sha256']:
                bad('REPAIR.TARGET_PREIMAGE_MISMATCH',
                    {'path': e['path'], 'declared': e['preimageDigest'],
                     'snapshotInventory': row['sha256']})
            if e['postimageDigest'] is not None:
                bad('DELETE_HAS_NO_POSTIMAGE', e['path'])
        else:   # replace
            if row is None:
                bad('REPAIR.SOURCE_MOVED',
                    {'path': e['path'], 'action': 'replace',
                     'why': ('a replace names a path the selected evidence snapshot does '
                             'not contain')})
            elif e['preimageDigest'] != row['sha256']:
                bad('REPAIR.TARGET_PREIMAGE_MISMATCH',
                    {'path': e['path'], 'declared': e['preimageDigest'],
                     'snapshotInventory': row['sha256'],
                     'law': 'preimage digest FROM the snapshot inventory'})
            if e['preimageDigest'] is None or e['postimageDigest'] is None:
                bad('REPLACE_HAS_BOTH_IMAGES', e['path'])
    # 5. THE CLOSED-WORLD GATE, under the SELECTION LAW this kit publishes (workflows-and-surfaces
    #    section 6 + repair.schema closedWorld). It reads the SELECTED NATIVE RECORDS, never the
    #    descriptor member, and it is decided BEFORE the descriptor is built. The guard covers
    #    every `delete` and every `replace`, without qualification.
    unsafe = [e for e in desc['edits'] if e['action'] in ('delete', 'replace')]
    sel = RS.select(run_facts['store'], desc['targets'], desc['edits'], label='admission')
    gate = sel['step3_gate']
    if unsafe and not gate['eligible']:
        bad('REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
            {'unsafeEdits': [e['path'] for e in unsafe],
             'relevantUniverses': sel['step1_relevantUniverses']['relevant'],
             'selectedRecordCount': gate['recordCount'],
             'nonVacuous': gate['nonVacuous'],
             # each dissent names ALL SIX ordering members plus that record's own reasons
             'dissents': gate['dissents'], 'notEstablished': gate['notEstablished']})
    if unsafe and desc['evidenceOrigin'] == 'imported-prepared-declared':
        bad('IMPORTED_PREPARED_DECLARED_IS_NEVER_AUTHORITY_FOR_AN_UNSAFE_EDIT',
            desc['evidenceOrigin'])
    # 5b. the descriptor member is the DERIVED five-field display summary of that same selection:
    #     "NOT a copy, NOT a projection of one record, and NOT itself a native producer record".
    #     A create-only plan activates no gate but still READS the selection and BUILDS the member.
    want_cw = sel['step4_displaySummary']
    for f in ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
              'nonliteralLoading', 'externalConsumers'):
        if desc['closedWorld'][f] != want_cw[f]:
            bad('CLOSED_WORLD_SUMMARY_IS_THE_DERIVED_FIVE_FIELD_REDUCTION',
                {'field': f, 'descriptor': desc['closedWorld'][f], 'derived': want_cw[f],
                 'law': ('deadCodeRepairEligible is the conjunction over the selected records '
                         'and false when none were selected; every other member takes the '
                         'LEAST-CLOSED value present; absence is folded in, not hidden'),
                 'selectedRecordCount': gate['recordCount']})
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
        # the per-action image shape is checked in step 4 beside the snapshot join, because
        # the two are one condition: which images an action carries is decided by whether the
        # path is a member of the selected snapshot
    tot = sum(e['postimageBytes'] for e in desc['edits'])
    if desc['totalPostimageBytes'] != tot:
        bad('TOTAL_POSTIMAGE_BYTES_IS_THE_SUM',
            {'declared': desc['totalPostimageBytes'], 'measured': tot})
    if tot > 64 * 1024 * 1024:
        bad('TOTAL_POSTIMAGE_AT_MOST_64_MIB', tot)
    if len(desc['targets']) > 4096 or len(desc['edits']) > 4096:
        bad('AT_MOST_4096_TARGET_FILES', len(desc['edits']))
    # 6b. PER-REQUIREMENT sufficiency: workflows section 6 says preview "ADMITS each evidence
    #     requirement's relation/minResolution against the registered vocabulary and its
    #     relation's own ladder ... and then CONSUMES that requirement's own `satisfied` value;
    #     the semantic sufficiency behind it is owned by native 4.6 sufficiency_v2 and the 4.5
    #     affected-target evidence, PER REQUIREMENT, and is never collapsed into one flag."
    #     So the value is derived per requirement from this Run's own native evidence, and an
    #     unsatisfied requirement must carry its own unmet precondition.
    for r in desc['evidenceRequirements']:
        if r['relation'] not in NATIVE_RELATIONS:
            continue                      # the imported plane has its own producer and law
        der = sufficiency_v2_native(run_facts, r)
        if der['satisfied'] != r['satisfied'] or (
                not r['satisfied'] and r.get('deficiency') != der['deficiency']):
            bad('EVIDENCE_REQUIREMENT_IS_THE_DERIVED_SUFFICIENCY_V2_OUTCOME',
                {'relation': r['relation'], 'minResolution': r['minResolution'],
                 'declared': {'satisfied': r['satisfied'],
                              'deficiency': r.get('deficiency')},
                 'derived': der, 'stepsApplied': der['stepsApplied']})
    for r in desc['evidenceRequirements']:
        if not r['satisfied'] and not desc['unmetPreconditions']:
            bad('UNSATISFIED_REQUIREMENT_EMITS_ITS_OWN_UNMET_PRECONDITION',
                {'relation': r['relation'],
                 'law': ('"An unsatisfied requirement with an empty unmetPreconditions is NOT a '
                         'conforming projection -- the schema alone admits that shape, and the '
                         'emission is decided at admission"')})
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


def sufficiency_v2_native(run_facts, req):
    """native-evidence.md section 4.6 `sufficiency_v2`, per requirement, over THIS Run's retained
    native view. Implemented for the steps a repair EvidenceRequirement can decide:

      1. "Relation absent from the view -> required-relation-missing."
      2. "Rung below minResolution -> the rung-unavailable cause ... else
         required-relation-missing."
      3. "confidenceMillionths < minConfidenceMillionths -> confidence-floor-unmet."
      5. "completeness=complete and coverage!=complete -> THE ENTRY'S OWN DEFICIENCY."

    Steps 4, 6, 7 and 8 are recorded NOT-APPLICABLE with the reason: they read
    `derivationPolicy`, the `quantifier`, `externalConsumerPolicy` and `dependsOn`, which live on
    the native RequirementV2 of the recipe and are not members of the repair EvidenceRequirement
    record -- the repair record carries the OUTCOME, not the producer's inputs. "There is no early
    exit": the steps below all run, and the most specific cause by section 10 precedence is the
    one reported.
    """
    rel, rung = req['relation'], req['minResolution']
    ladder = (NATIVE_RELATIONS.get(rel) or {}).get('ladder') or []
    steps, entries = [], []
    for cid, cv in sorted(run_facts['closure'].coverages_seen.items()):
        pay = run_facts['closure'].canonical_record(
            cv['payloadDigest'], B.NATIVE_DOC, '#/$defs/CoverageResultV3', 'SUFF')
        if pay and pay['key']['relation'] == rel:
            entries.append((cid, pay))
    if not entries:
        steps.append('1: relation absent from the view')
        return {'satisfied': False, 'deficiency': 'required-relation-missing',
                'stepsApplied': steps,
                'notApplicable': ['4 derivationPolicy', '6 quantifier', '7 externalConsumers',
                                  '8 dependsOn']}
    best = None
    for cid, pay in entries:
        r_ix = ladder.index(pay['key']['resolution']) if pay['key']['resolution'] in ladder else -1
        want_ix = ladder.index(rung) if rung in ladder else -1
        if r_ix >= want_ix >= 0:
            best = (cid, pay)
            break
    if best is None:
        steps.append('2: every retained rung is below minResolution')
        return {'satisfied': False, 'deficiency': 'required-relation-missing',
                'stepsApplied': steps,
                'notApplicable': ['4', '6', '7', '8']}
    cid, pay = best
    ent = pay['entry']
    steps.append('2: a retained partition reaches the requested rung (%s)'
                 % pay['key']['resolution'])
    floor = req.get('minConfidenceMillionths')
    if floor is not None and ent['confidenceMillionths'] < floor:
        steps.append('3: confidence below the floor')
        return {'satisfied': False, 'deficiency': 'confidence-floor-unmet',
                'stepsApplied': steps, 'notApplicable': ['4', '6', '7', '8']}
    if req['completeness'] == 'complete' and ent['coverage'] != 'complete':
        steps.append("5: completeness=complete and coverage!=complete -> the entry's own "
                     'deficiency')
        return {'satisfied': False, 'deficiency': ent['deficiency'],
                'coverageId': cid, 'stepsApplied': steps,
                'notApplicable': ['4', '6', '7', '8']}
    steps.append('5: satisfied over the retained partition')
    return {'satisfied': True, 'deficiency': None, 'coverageId': cid, 'stepsApplied': steps,
            'notApplicable': ['4', '6', '7', '8'],
            'note': 'satisfied=true may still carry section 4.6 disclosures, which this '
                    'consumer record does not carry'}


def schema_admit(plan):
    """HELPER CORRECTION V19-D4: this function used to call S.admit inside a try/except and
    return True whenever no EXCEPTION was raised. S.admit does not raise -- it RETURNS a result
    whose `admitted` flag carries the verdict -- so every owning-schema refusal was silently read
    as a pass, and the owning-schema boundary of this phase's controls measured nothing. The
    result is now read."""
    try:
        r = S.admit(REPAIR_DOC, '#/$defs/RepairPlanV1', plan, 'repair-plan')
    except Exception as e:                       # a genuine resolution/IO failure
        return False, '%s: %s' % (type(e).__name__, str(e)[:400])
    if r['admitted']:
        return True, None
    return False, json.dumps({'stockSchemaErrors': r['stockSchemaErrors'][:4],
                              'publishedKeywordRefusals':
                                  r['publishedKeywordRefusals'][:4]})[:900]


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
    POST = b'export function pad2(s) { return s.padStart(2, "0"); }\n// repaired\n'
    if edits is None:
        if unsafe:
            # a REPLACE names an EXISTING snapshot member and its preimage digest comes FROM
            # the snapshot inventory -- not from a locally recomputed guess about the bytes
            row = SNAPSHOT_INVENTORY['src/legacy.js']
            edits = [{'path': 'src/legacy.js', 'action': 'replace',
                      'preimageDigest': row['sha256'],
                      'postimageDigest': K.raw_sha256(POST),
                      'postimageBytes': len(POST)}]
        else:
            # a CREATE names a path the selected snapshot does NOT contain (V17-D7): the two
            # actions are different snapshot conditions
            new_path = 'src/shared-pad.js'
            assert new_path not in SNAPSHOT_INVENTORY, new_path
            edits = [{'path': new_path, 'action': 'create', 'preimageDigest': None,
                      'postimageDigest': K.raw_sha256(POST),
                      'postimageBytes': len(POST)}]
    if reqs is None:
        # DERIVED per requirement by section 4.6 over this Run's own evidence, not asserted
        reqs = []
        for rel, rung in (('clones', 'normalized-body-hash'),
                          ('imports', 'resolved-target')):
            row = {'relation': rel, 'minResolution': rung, 'completeness': 'complete'}
            der = sufficiency_v2_native(ev, row)
            row['satisfied'] = der['satisfied']
            if not der['satisfied']:
                row['deficiency'] = der['deficiency']
            reqs.append(row)
    targets_eff = targets if targets is not None else [ev['fingerprints'][0]]
    edits_eff = sorted(edits, key=lambda e: e['path'].encode())
    # the descriptor member is the DERIVED five-field display summary of the selection over THIS
    # descriptor's own targets and edits (repair.schema closedWorld + workflows section 6)
    cw = closed_world or RS.select(ev['store'], targets_eff, edits_eff,
                                   label='descriptor')['step4_displaySummary']
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
        'targets': targets_eff,
        'edits': edits_eff,
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

    global SNAPSHOT_INVENTORY
    ev = evidence_from_run()
    # the SELECTED evidence snapshot's own inventory, taken from the retained snapshot2 of the
    # Run the descriptor names -- this is the record the preimage law points at
    SNAPSHOT_INVENTORY = {r['path']: r
                          for r in ev['closure'].snap['sourceInventory']}
    pos = case(ev, 'repair-descriptor-positive-safe-create', 'valid', None)
    rows = [pos]
    # ---- per-target / authority controls
    rows.append(case(ev, 'unsafe-replace-without-deadCodeRepairEligible', 'invalid',
                     'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED', unsafe=True))
    cw_true = {'deadCodeRepairEligible': True, 'exportsClosed': 'closed',
               'entryPointsRecognized': 'all', 'nonliteralLoading': 'none',
               'externalConsumers': 'none-declared'}
    # THE DISTINGUISHING PAIR. Editing the descriptor's five-field SUMMARY to say the closed
    # world is established does NOT move the gate: the gate reads the SELECTED NATIVE RECORDS, so
    # the unsafe case still refuses AT THE GATE...
    r = case(ev, 'unsafe-replace-with-a-forged-summary-still-refuses-at-the-gate',
             'invalid', 'REPAIR.CLOSED_WORLD_NOT_ESTABLISHED',
             unsafe=True, closed_world=cw_true)
    r['whyThisIsTheDistinguishingControl'] = (
        'the summary was edited to the permissive value and the refusal did not move: '
        '"NO MEMBER OF IT IS AUTHORITATIVE, the boolean included", and the gate reads the full '
        'selected records including the two members the summary does not carry.')
    rows.append(r)
    # ...and the SUMMARY law itself is isolated by a SAFE edit, where no gate applies. This is
    # where a recipe-selected favourable record would otherwise have survived.
    rows.append(case(ev, 'safe-create-with-a-summary-that-is-not-the-derived-reduction',
                     'invalid',
                     'CLOSED_WORLD_SUMMARY_IS_THE_DERIVED_FIVE_FIELD_REDUCTION',
                     unsafe=False, closed_world=cw_true))
    # the recipe-selected-record control the new law exists to refuse: copy the FIVE fields of ONE
    # favourable retained Coverage entry instead of reducing over every selected record
    sel_pos = RS.select(ev['store'], [ev['fingerprints'][0]],
                        [{'path': 'src/shared-pad.js', 'action': 'create',
                          'preimageDigest': None,
                          'postimageDigest': K.raw_sha256(b'x'), 'postimageBytes': 1}],
                        label='control')
    favourable = None
    for rec in sel_pos['step2_selectedRecords']:
        cwr = rec['closedWorld']
        if favourable is None or (cwr.get('nonliteralLoading') == 'none'
                                  and cwr.get('exportsClosed') != 'unknown'):
            favourable = dict(rec)
    if favourable is not None:
        one = {f: favourable['closedWorld'][f] for f in
               ('deadCodeRepairEligible', 'exportsClosed', 'entryPointsRecognized',
                'nonliteralLoading', 'externalConsumers')}
        one['deadCodeRepairEligible'] = True        # the favourable reading a recipe would pick
        rr = case(ev, 'summary-copied-from-one-recipe-selected-coverage-entry', 'invalid',
                  'CLOSED_WORLD_SUMMARY_IS_THE_DERIVED_FIVE_FIELD_REDUCTION',
                  unsafe=False, closed_world=one)
        rr['recipeSelectedRecord'] = {'coverageId': favourable['coverageId'],
                                      'relation': favourable['relation'],
                                      'resolution': favourable['resolution']}
        rr['whyThisIsRefused'] = (
            'selection is "independent of the plan\'s evidenceRequirements: a recipe can neither '
            'narrow it to a favourable relation or rung nor remove a conflicting record from it"')
        rows.append(rr)
    # a LITERAL seven-field ClosedWorldV2 copy: refused by the OWNING SCHEMA, which closes the
    # member at exactly five fields
    seven = dict(cw_true, dynamicDispatch='not-applicable', reasons=[])
    rows.append(case(ev, 'summary-as-a-literal-seven-field-ClosedWorldV2-copy', 'invalid',
                     'OWNING_SCHEMA', unsafe=False, closed_world=seven))
    rows.append(case(ev, 'target-is-not-a-fingerprint-of-the-evidence-run', 'invalid',
                     'REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE',
                     targets=['finding-key2:' + 'a' * 64]))
    rows.append(case(ev, 'edit-outside-the-permitted-edit-scope', 'invalid',
                     'EDIT_WITHIN_PERMITTED_EDIT_SCOPE', scope=['docs/**/*']))
    rows.append(case(ev, 'applicable-true-with-an-unmet-precondition', 'invalid',
                     'APPLICABLE_IFF_EVERY_REQUIREMENT_SATISFIED',
                     unmet=[DD('REPAIR.CLOSED_WORLD_NOT_ESTABLISHED', 'establish the native closed world for every relevant universe before an unsafe edit')], applicable=True))
    rows.append(case(ev, 'applicable-true-while-the-recipe-trust-is-revoked', 'invalid',
                     'REPAIR.RECIPE_TRUST_REVOKED', trust='revoked'))
    # ---- R-MIN-RESOLUTION-REPAIR-EVIDENCE: both planes, cross-plane refused
    both = [{'relation': 'types', 'minResolution': 'checked', 'completeness': 'complete',
             'satisfied': False, 'deficiency': 'required-relation-missing'},
            {'relation': 'runtime-observation', 'minResolution': 'observed',
             'completeness': 'partial-acceptable', 'satisfied': False,
             'deficiency': 'import-unmapped-only'}]
    rows.append(case(ev, 'evidence-requirements-over-both-planes', 'valid', None,
                     reqs=both, unmet=[DD('REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'the evidence Run cannot supply what this requirement needs: types@checked (native plane, required-relation-missing) and runtime-observation@observed (imported plane, import-unmapped-only)')],
                     applicable=False))
    cross = [{'relation': 'types', 'minResolution': 'checked', 'completeness': 'complete',
              'satisfied': False, 'deficiency': 'import-unmapped-only'}]
    rows.append(case(ev, 'native-requirement-carrying-an-imported-deficiency-value',
                     'invalid', 'CROSS_PLANE_DEFICIENCY_VALUE', reqs=cross,
                     unmet=[DD('REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'per-requirement insufficiency')],
                     applicable=False))
    cross2 = [{'relation': 'runtime-observation', 'minResolution': 'observed',
               'completeness': 'complete', 'satisfied': False,
               'deficiency': 'resolution-incomplete'}]
    rows.append(case(ev, 'imported-requirement-carrying-a-native-deficiency-value',
                     'invalid', 'CROSS_PLANE_DEFICIENCY_VALUE', reqs=cross2,
                     unmet=[DD('REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'per-requirement insufficiency')],
                     applicable=False))
    rows.append(case(ev, 'requirement-rung-not-on-that-relations-ladder', 'invalid',
                     'REQUIREMENT_RUNG_ON_THIS_RELATIONS_LADDER',
                     reqs=[{'relation': 'clones', 'minResolution': 'resolved-target',
                            'completeness': 'complete', 'satisfied': True}]))
    # ---- v17: THE SELECTED SNAPSHOT JOIN. All three are shape-valid FileEdits.
    POST = b'// repaired\n'
    rows.append(case(
        ev, 'create-names-a-path-the-selected-snapshot-already-contains', 'invalid',
        'REPAIR.CREATE_PATH_ALREADY_IN_THE_SELECTED_SNAPSHOT',
        edits=[{'path': 'src/legacy.js', 'action': 'create', 'preimageDigest': None,
                'postimageDigest': K.raw_sha256(POST),
                'postimageBytes': len(POST)}]))
    rows.append(case(
        ev, 'replace-names-a-path-the-selected-snapshot-does-not-contain', 'invalid',
        'REPAIR.SOURCE_MOVED',
        edits=[{'path': 'src/moved-away.js', 'action': 'replace',
                'preimageDigest': K.raw_sha256(b'whatever'),
                'postimageDigest': K.raw_sha256(POST),
                'postimageBytes': len(POST)}],
        scope=['src/**/*']))
    rows.append(case(
        ev, 'replace-preimage-digest-is-not-the-snapshot-inventory-digest', 'invalid',
        'REPAIR.TARGET_PREIMAGE_MISMATCH',
        edits=[{'path': 'src/legacy.js', 'action': 'replace',
                'preimageDigest': K.raw_sha256(b'a plausible but wrong preimage'),
                'postimageDigest': K.raw_sha256(POST),
                'postimageBytes': len(POST)}]))
    # MEASURED BOUNDARY (V19-D4): with the owning-schema result actually read, this one refuses at
    # the SCHEMA -- FileEdit.allOf[action=delete] pins postimageDigest to null and postimageBytes
    # to the const 0. Reported where it actually refuses rather than relabelled to the delegated
    # check that would also have caught it.
    rows.append(case(
        ev, 'delete-carries-a-postimage', 'invalid', 'OWNING_SCHEMA',
        edits=[{'path': 'src/legacy.js', 'action': 'delete',
                'preimageDigest': SNAPSHOT_INVENTORY['src/legacy.js']['sha256'],
                'postimageDigest': K.raw_sha256(POST), 'postimageBytes': len(POST)}]))

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

    # V20-D6: CURRENT origin id, re-stated each generation; the records below are this
    # generation's own reconstructions over this generation's admitted Run.
    doc = {'consumerId': 'consumer-b.' + 'v20',
           'standing': ('reconstructed from the admitted TypeScript Run. No repair was '
                        'previewed, applied or authorized against any product: these are '
                        'record reconstructions and admission controls only.'),
           'rolesKeptDistinct': {
               'nativeProducerObservations': (
                   'every Coverage entry, ClosedWorldV2 and provider return this descriptor reads '
                   'is a SYNTHETIC TRUSTED TCB INPUT authored by this origin. The selection law '
                   'decides which of them the gate reads; it does not make any of them true, and '
                   'no compiler, provider or host is qualified by them.'),
               'recipeTrust': (
                   'a separate positive disposition of recipe.closureId under CURRENT trust: only '
                   '`admitted` is applicable, `not-admitted` is REPAIR.RECIPE_TRUST_NOT_ADMITTED '
                   'and `revoked` is REPAIR.RECIPE_TRUST_REVOKED. "Absence of a revocation is '
                   'never admission."'),
               'policyConsent': 'a CI-side requirement at apply, not a preview outcome',
               'securityAuthorization': (
                   'apply is bound to the exact repairPlanId, base snapshot and project by a '
                   'security-unit authorization (REPAIR.CONSENT_NOT_BOUND). Nothing in this '
                   'phase creates, holds or implies one.'),
               'previewAuthorizesNothing': (
                   'preview is a Query-class step: `applicable=true` is a disclosure that the '
                   'preconditions held, and trust, consent, current-snapshot equality and that '
                   'bound authorization are all still required at apply. No automatic source '
                   'edit, and verify always seals a NEW Run over a fresh snapshot rather than '
                   'reusing this evidence Run.'),
               'closedWorldSummaryAuthority': (
                   'NONE. No member of the descriptor summary is authoritative, the boolean '
                   'included; the gate reads the full selected records.')},
           'closedWorldSelection': RS.select(
               ev['store'], [ev['fingerprints'][0]],
               [{'path': 'src/shared-pad.js', 'action': 'create', 'preimageDigest': None,
                 'postimageDigest': K.raw_sha256(b'x'), 'postimageBytes': 1}],
               label='positive-descriptor'),
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
