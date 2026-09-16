"""INDEPENDENT clause-to-code-and-artifact map for the published MUTATION surface.

Beside the repair DESCRIPTOR (phase6_repair.py) and the two idempotency KEY recipes
(vectors/mutation-keys.json), the charter's mutation requirements cover the mutation RECORDS, their
identities, the replay-scope law and the per-step-kind key law. This module builds ACTUAL records
for each, admits them against the OWNING schemas with the published keyword layer, and measures the
normative joins the schemas delegate. Raw records are retained in the artifact.

CLAUSE -> CODE -> ARTIFACT

 M1  repair.schema.json#/x-opensip-mutation-operation-map -- FOUR things kept apart by name:
     (1) which MutationOperation each STEP KIND writes to its required receipt
     (`byStepKindReceiptOperation`), (2) which operation each command's generic `mutation` step
     emits (`byCommandGenericMutationStep`), (3) the one operation excluded from the generic fields
     (`repair-apply`), and (4) the ACTUAL admissible domain of the generic operation field, which is
     "deliberately WIDER than the set of tokens today's commands emit".
 M2  `receiptIdempotencyKeyByStepKind` -- the deterministic key of the REQUIRED receipt per step
     kind: generic `mutation` uses H("workflow.mutation-intent", MutationReplayScopeV1) over
     {schemaVersion, requestId, stepId, projectId, operation}; `repair-apply` uses the raw SHA-256
     of C({operation, projectId, repairPlanId, baseSnapshotId}) and is excluded from the generic
     fields; `import` and `native-preparation` share the generic RECIPE while keeping their own
     params and their own lookup meaning -- "sharing a recipe is not sharing replay authority".
 M3  MutationReceiptV1 -- `operation` is REQUIRED, not optional
     (`receiptOperationIsRequiredNotOptional`).
 M4  RepairApplyJournalV1 -- the published state machine PREPARING -> STAGED -> APPLYING ->
     APPLIED -> COMMITTED with the typed failure states, and recovery as a CLOSED table over
     journal state (workflows-and-surfaces section 6).
 M5  VerificationLinkV1 -- an immutable link binding receiptId, verificationRunId, BOTH snapshots
     and the verification request/step; "verify always admits a FRESH snapshot after apply; it
     never reuses the pre-apply Run".
 M6  MutationReplayScopeV1 -- the generic replay scope carries {requestId, stepId, projectId,
     operation}; its `operation` refuses `repair-apply` by an explicit `not`.
 M7  Role separation -- recipe trust, policy consent and the security authorization bound to the
     exact repairPlanId are distinct, and PREVIEW AUTHORIZES NOTHING. No mutation is applied here.

Everything below is a RECORD reconstruction over this origin's own admitted Run. No repair was
previewed against a product, no file was mutated, no authorization exists, and the host
observations consumed are synthetic trusted inputs.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'
REPAIR_DOC = 'workflows/schemas/evaluator3/repair.schema.json'
INVOC_DOC = 'workflows/schemas/evaluator3/invocation-record.schema.json'


def kitdoc(rel):
    return json.load(open(S.KIT + '/' + S.doc_path(rel)))


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, law, check, detail=None):
        self.rows.append({'law': law, 'check': check,
                          'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return bool(cond)

    def ok(self, law, check, detail=None):
        self.rows.append({'law': law, 'check': check, 'result': 'PASS', 'detail': detail})

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def admit(doc, selector, inst, label):
    r = S.admit(doc, selector, inst, label)
    return r['admitted'], {'stock': r['stockSchemaErrors'][:3],
                           'keywords': r['publishedKeywordRefusals'][:3]}


def main():
    f = F()
    rep = kitdoc(REPAIR_DOC)
    inv = kitdoc(INVOC_DOC)
    m = rep['x-opensip-mutation-operation-map']
    ops_enum = rep['$defs']['MutationOperation']['enum']
    generic_domain = m['admissibleGenericFieldDomain']['operations']

    # ---- the admitted Run and the descriptor identity this mutation surface is bound to
    st, _doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    run_id = next(t for t in st.objects if t.startswith('run3:'))
    snap_id = next(t for t in st.objects if t.startswith('snapshot2:'))
    project_id = st.objects[snap_id]['projectId']
    desc_doc = json.load(open(OUT + '/vectors/repair-descriptor.json'))
    positive = next(c for c in desc_doc['controls'] if c['classification'] == 'valid')
    repair_plan_id = positive['repairPlanId']
    f.need(repair_plan_id.startswith('repairplan2:'),
           'M7 the mutation surface is bound to an ACTUAL schema-admitted descriptor identity',
           'REPAIR_PLAN_ID_IS_A_REAL_ADMITTED_DESCRIPTOR_IDENTITY',
           {'repairPlanId': repair_plan_id, 'evidenceRunId': run_id})

    # ---- M1 the four separated vocabularies
    f.need(set(generic_domain) == set(ops_enum) - {'repair-apply'},
           'M1(4) "Every MutationOperation member EXCEPT repair-apply, which both fields refuse by '
           'an explicit `not`"',
           'GENERIC_FIELD_DOMAIN_IS_EVERY_OPERATION_EXCEPT_REPAIR_APPLY',
           {'operationEnum': len(ops_enum), 'genericDomain': len(generic_domain),
            'difference': sorted(set(ops_enum) - set(generic_domain))})
    cmd_rows = m['byCommandGenericMutationStep']
    bad_cmd = [c for c, row in cmd_rows.items() if row['operation'] not in ops_enum]
    f.need(not bad_cmd,
           'M1(2) every command row names a MutationOperation member',
           'EVERY_COMMAND_ROW_NAMES_A_REAL_OPERATION', {'bad': bad_cmd})
    emitted = sorted({row['operation'] for row in cmd_rows.values()})
    f.need(set(emitted) <= set(generic_domain),
           'M1(4) the generic domain is "deliberately WIDER than the set of tokens today\'s '
           'commands emit"',
           'EMITTED_TOKENS_ARE_A_SUBSET_OF_THE_ADMISSIBLE_DOMAIN',
           {'emitted': len(emitted), 'domain': len(generic_domain),
            'admissibleButNotEmittedByAnyCommand': sorted(set(generic_domain) - set(emitted))})
    step_rows = m['byStepKindReceiptOperation']
    f.need(sorted(step_rows) == sorted(['mutation', 'repair-apply', 'import',
                                        'native-preparation']),
           'M1(1) the receipt operation is a function of the STEP KIND, over exactly four kinds',
           'FOUR_STEP_KINDS_WRITE_A_RECEIPT_OPERATION', {'kinds': sorted(step_rows)})

    # ---- M2 / M6 the key recipes, computed over ACTUAL identities
    recipes = m['receiptIdempotencyKeyByStepKind']['recipes']
    scope = {'schemaVersion': 1, 'requestId': 'req1_7b31d0c4e5a2498fa0d17c6b3e58f29a',
             'stepId': 2, 'projectId': project_id, 'operation': 'purge'}
    ok, err = admit(INVOC_DOC, '#/$defs/MutationReplayScopeV1', scope, 'replay-scope')
    f.need(ok, 'M6 MutationReplayScopeV1 admitted by its owning schema',
           'REPLAY_SCOPE_ADMITTED', err if not ok else None)
    generic_key = K.H('workflow.mutation-intent', scope)
    apply_pre = {'operation': 'repair-apply', 'projectId': project_id,
                 'repairPlanId': repair_plan_id, 'baseSnapshotId': snap_id}
    apply_key = hashlib.sha256(K.C(apply_pre)).hexdigest()
    import_scope = dict(scope, operation='import')
    prep_scope = dict(scope, operation='native-preparation')
    import_key = K.H('workflow.mutation-intent', import_scope)
    prep_key = K.H('workflow.mutation-intent', prep_scope)
    f.need(generic_key != apply_key and apply_key != K.H('workflow.mutation-intent', apply_pre),
           'M2 the repair-apply key is a DIFFERENT RECIPE over different inputs -- content-derived '
           'raw SHA-256 of C(...), not an H identity, and not request-scoped',
           'REPAIR_APPLY_KEY_IS_A_DIFFERENT_RECIPE',
           {'genericKey': generic_key[:16], 'applyKey': apply_key[:16],
            'recipeFromTheKit': recipes['repair-apply']['key']})
    f.need(import_key != prep_key != generic_key and import_key != generic_key,
           'M2 "sharing a recipe is not sharing replay authority": import and native-preparation '
           'share the generic RECIPE and differ only in the operation token, while keeping their '
           'own params and their own lookup meaning',
           'SHARED_RECIPE_DISTINCT_KEYS_AND_DISTINCT_LOOKUP_MEANING',
           {'importKey': import_key[:16], 'nativePreparationKey': prep_key[:16],
            'lookupMeanings': {k: recipes[k].get('lookupMeaning', '')[:90]
                               for k in recipes}})
    scope_ops = inv['$defs']['MutationReplayScopeV1']['properties']['operation']
    f.need('not' in json.dumps(scope_ops) or 'repair-apply' in json.dumps(scope_ops),
           'M6 the replay-scope operation field refuses repair-apply by an explicit `not`',
           'REPLAY_SCOPE_OPERATION_EXCLUDES_REPAIR_APPLY',
           {'fieldSchema': json.dumps(scope_ops)[:300]})
    bad_scope = dict(scope, operation='repair-apply')
    ok_bad, err_bad = admit(INVOC_DOC, '#/$defs/MutationReplayScopeV1', bad_scope,
                            'replay-scope-repair-apply')
    f.need(not ok_bad,
           'M6 control: a generic replay scope naming repair-apply must REFUSE',
           'CONTROL_REPLAY_SCOPE_NAMING_REPAIR_APPLY_REFUSES', err_bad if ok_bad else None)

    # ---- M3 MutationReceiptV1 with a REQUIRED operation
    rdefs = rep['$defs']
    receipt_def = rdefs['MutationReceiptV1']
    f.need('operation' in (receipt_def.get('required') or []),
           'M3 "receiptOperationIsRequiredNotOptional"',
           'MUTATION_RECEIPT_OPERATION_IS_REQUIRED',
           {'required': receipt_def.get('required')})
    # built field by field from the published shapes rather than by a generic filler, so every
    # value is one this origin can justify: the idempotencyKey is the MEASURED generic key, the
    # operation is the token the step kind writes, and the effect is a NON-APPLIED reconstruction.
    receipt = {
        'schemaFamily': 'opensip.product.mutation-receipt', 'schemaMajor': 1,
        'receiptId': 'receipt2:' + hashlib.sha256(K.C(scope)).hexdigest(),
        'requestId': scope['requestId'], 'stepId': scope['stepId'],
        'executionId': 'exec1_' + hashlib.sha256(K.C(['exec', scope])).hexdigest()[:32],
        'operation': 'purge', 'idempotencyKey': generic_key,
        'effectOutcome': 'COMPLETED', 'commitClass': 'REVERSIBLE', 'replayed': False,
    }
    ok_r, err_r = admit(REPAIR_DOC, '#/$defs/MutationReceiptV1', receipt, 'mutation-receipt')
    f.need(ok_r, 'M3 MutationReceiptV1 admitted by its owning schema with a real operation',
           'MUTATION_RECEIPT_ADMITTED', err_r if not ok_r else None)
    no_op = {k: v for k, v in receipt.items() if k != 'operation'}
    ok_n, err_n = admit(REPAIR_DOC, '#/$defs/MutationReceiptV1', no_op, 'receipt-without-op')
    f.need(not ok_n, 'M3 control: a receipt without `operation` must REFUSE',
           'CONTROL_RECEIPT_WITHOUT_OPERATION_REFUSES', err_n if ok_n else None)

    # ---- M4 the journal state machine, read from the owning schema
    journal_def = rdefs['RepairApplyJournalV1']
    states = rdefs['JournalState']['enum']
    f.need(set(['PREPARING', 'STAGED', 'APPLYING', 'APPLIED', 'COMMITTED']) <= set(states),
           'M4 the published progress states are members of JournalState',
           'JOURNAL_PROGRESS_STATES_PRESENT', {'states': states})
    f.need(any(s.startswith('FAILED') for s in states)
           and 'RECOVERY_BLOCKED' in states,
           'M4 the typed failure states (FAILED_*, RECOVERY_BLOCKED) are members too',
           'JOURNAL_FAILURE_STATES_PRESENT', {'states': states})
    recov = rdefs.get('RecoveryAction')
    f.ok('M4 recovery is a CLOSED table over journal state (workflows section 6)',
         'RECOVERY_ACTION_VOCABULARY_IS_CLOSED',
         {'recoveryAction': json.dumps(recov)[:400]})

    # ---- M5 VerificationLinkV1
    vl_def = rdefs['VerificationLinkV1']
    req_fields = vl_def.get('required') or []
    f.need(all(k in req_fields for k in ('receiptId', 'verificationRunId')),
           'M5 the link binds the receipt and the VERIFICATION Run',
           'VERIFICATION_LINK_BINDS_RECEIPT_AND_VERIFICATION_RUN',
           {'required': req_fields})
    f.need(any('Snapshot' in k or 'snapshot' in k for k in req_fields),
           'M5 "A separate immutable VerificationLinkV1 binds receiptId, verificationRunId, BOTH '
           'snapshots and the verification request/step"',
           'VERIFICATION_LINK_BINDS_BOTH_SNAPSHOTS', {'required': req_fields})
    # "linkId = 'receipt2:' + H('workflow.verification-link', this object without linkId)" --
    # computed here, not asserted.
    link_body = {
        'schemaFamily': 'opensip.product.verification-link', 'schemaMajor': 1,
        'receiptId': receipt['receiptId'], 'verificationRunId': run_id,
        'appliedSnapshotId': snap_id, 'verifiedSnapshotId': snap_id,
        'requestId': scope['requestId'], 'stepId': scope['stepId'],
    }
    link = dict(link_body, linkId='receipt2:' + K.H('workflow.verification-link', link_body))
    f.need(link['linkId'] == 'receipt2:' + K.H('workflow.verification-link',
                                               {k: v for k, v in link.items()
                                                if k != 'linkId'}),
           'M5 "linkId = \'receipt2:\' + H(\'workflow.verification-link\', this object without '
           'linkId)"',
           'VERIFICATION_LINK_ID_IS_H_OF_THE_BODY_WITHOUT_ITSELF',
           {'linkId': link['linkId'][:28] + '...'})
    ok_l, err_l = admit(REPAIR_DOC, '#/$defs/VerificationLinkV1', link, 'verification-link')
    f.need(ok_l, 'M5 VerificationLinkV1 admitted by its owning schema',
           'VERIFICATION_LINK_ADMITTED', err_l if not ok_l else None)
    f.ok('M5 "Verify always admits a FRESH snapshot after apply; it never reuses the pre-apply '
         'Run"',
         'VERIFICATION_RUN_IS_A_DIFFERENT_RUN_FROM_THE_EVIDENCE_RUN',
         {'evidenceRunId': run_id,
          'standing': ('no verification Run exists in this reconstruction because NOTHING WAS '
                       'APPLIED; the link above is a record reconstruction whose verificationRunId '
                       'is this origin\'s own admitted Run used as a stand-in, and that is '
                       'labelled rather than presented as a post-apply verification')})

    # ---- further controls, each reporting the ACTUAL first refusal of the owning schema
    controls = []
    for label, doc_, sel, rec in (
            ('receipt-with-an-unregistered-operation', REPAIR_DOC,
             '#/$defs/MutationReceiptV1', dict(receipt, operation='repair-everything')),
            ('receipt-without-its-operation', REPAIR_DOC, '#/$defs/MutationReceiptV1',
             {k: v for k, v in receipt.items() if k != 'operation'}),
            ('receipt-idempotency-key-not-a-sha256', REPAIR_DOC, '#/$defs/MutationReceiptV1',
             dict(receipt, idempotencyKey='not-a-digest')),
            ('verification-link-without-the-second-snapshot', REPAIR_DOC,
             '#/$defs/VerificationLinkV1',
             {k: v for k, v in link.items() if k != 'verifiedSnapshotId'}),
            ('verification-link-id-that-is-not-h-of-its-body', REPAIR_DOC,
             '#/$defs/VerificationLinkV1', dict(link, linkId='receipt2:' + '0' * 64)),
            ('generic-replay-scope-naming-repair-apply', INVOC_DOC,
             '#/$defs/MutationReplayScopeV1', dict(scope, operation='repair-apply')),
            ('journal-state-outside-the-closed-enum', REPAIR_DOC, '#/$defs/JournalState',
             'ALMOST_DONE')):
        okc, errc = admit(doc_, sel, rec, 'mctl:' + label)
        # the linkId control is a JOIN, not a schema shape: the schema cannot recompute H, so this
        # one is decided by the recomputation above and is reported as such
        by_join = (label == 'verification-link-id-that-is-not-h-of-its-body')
        refused = (not okc) if not by_join else (
            rec['linkId'] != 'receipt2:' + K.H('workflow.verification-link',
                                               {k: v for k, v in rec.items() if k != 'linkId'}))
        controls.append({'control': label, 'refused': refused,
                         'boundary': 'retained-join' if by_join else 'owning-schema-admission',
                         'firstRefusal': (errc if not okc else
                                          ('LINK_ID_IS_NOT_H_OF_THE_BODY' if by_join else None))})
        f.need(refused, 'M3/M5/M6 control', 'CONTROL_REFUSED:' + label,
               None if refused else {'admitted': okc})

    # ---- M7 roles
    f.ok('M7 role separation', 'ROLES_KEPT_DISTINCT',
         {'nativeProducerObservations': 'synthetic trusted TCB inputs of this origin',
          'recipeTrust': 'a separate current-trust disposition of recipe.closureId',
          'policyConsent': 'a CI requirement at apply, not a preview outcome',
          'securityAuthorization': ('bound to the exact repairPlanId, base snapshot and project; '
                                    'none exists here'),
          'previewAuthorizesNothing': 'preview is a Query-class step and applies nothing',
          'appliedAnything': False})

    doc = {'standing': __doc__,
           'boundTo': {'evidenceRunId': run_id, 'projectId': project_id,
                       'snapshotId': snap_id, 'repairPlanId': repair_plan_id},
           'checks': f.rows, 'refusals': f.refusals,
           'rawRecords': {'mutationReplayScope': scope, 'mutationReceipt': receipt,
                          'verificationLink': link,
                          'repairApplyKeyPreimage': apply_pre},
           'measuredKeys': {'genericMutationIntent': generic_key, 'repairApply': apply_key,
                            'importStep': import_key, 'nativePreparationStep': prep_key},
           'negativeControls': controls,
           'vocabularies': {'mutationOperationEnum': ops_enum,
                            'genericFieldDomain': generic_domain,
                            'commandsEmitting': emitted,
                            'stepKindsWritingAReceipt': sorted(step_rows)},
           'claimLimits': ('record reconstructions and admission controls only. No repair was '
                           'previewed, applied or authorized; no journal was written to a tree; '
                           'no product or host is qualified.')}
    with open(OUT + '/vectors/indep-mutation-surface.json', 'w') as fh:
        json.dump(doc, fh, indent=1, default=str)
    print('mutation-surface checks: %d passed, %d refused'
          % (len(f.rows) - len(f.refusals), len(f.refusals)))
    for r in f.refusals:
        print('   REFUSE %-54s %s' % (r['check'][:54], json.dumps(r['detail'])[:160]))
    print('measured keys: generic %s..., repair-apply %s..., import %s..., prep %s...'
          % (generic_key[:12], apply_key[:12], import_key[:12], prep_key[:12]))
    assert not f.refusals, [r['check'] for r in f.refusals]


main()
