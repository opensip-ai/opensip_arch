"""Post-reset author v2 (Claude): security case additions.
  * NEW repair-recovery-authorization-cases.v1.json (S10.2, P9)
  * NEW transition-journal-cases.v1.json (S9.2, P10)
  * lease-cases.v1.json: transition-journal op cases (S7)
  * discovery-cases.v1.json: boundary-inventory export cases (S3, P3)
Case files round-trip with json.dumps(indent=2, ensure_ascii=False) + newline. Journal identities / state digests and
intent / registry digests are computed with the model's own functions and recorded under `computed` with the recipe
named; expectations are hand-authored from the contract text (same author, not an independent oracle). Idempotent."""
import copy, importlib.util, json
from pathlib import Path

SEC = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security')
spec = importlib.util.spec_from_file_location('m', SEC / 'security_lifecycle_model_v1.py'); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)


def dump(path, doc):
    path.write_bytes((json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode())


def load_roundtrip(name):
    raw = (SEC / name).read_bytes(); doc = json.loads(raw)
    assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw, name
    return doc


H = lambda c: c * 64
PRJ = 'prj1-' + H('a'); PLAN = 'repairplan2:' + H('b'); SNAP = 'snapshot2:' + H('c'); RECIPE = 'closure2:' + H('e'); REVOKED = 'closure2:' + H('9')
REQ_APPLY = 'req1_' + '1' * 32; EXEC_APPLY = 'exec1_' + '1' * 32; REQ_REC = 'req1_' + '2' * 32; EXEC_REC = 'exec1_' + '2' * 32
D9_PRE = {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.PRECONDITION_FAILED'}
D9_EXT = {'class': 'request-rejected', 'exit': 2, 'code': 'EXTENSION.ADMISSION_REJECTED'}

# ------------------------------------------------------------------ repair recovery authorization (S10.2)
journal_base = {'schemaFamily': 'opensip.product.repair-apply-journal', 'schemaMajor': 1, 'requestId': REQ_APPLY, 'stepId': 2, 'executionId': EXEC_APPLY,
                'repairPlanId': PLAN, 'baseSnapshotId': SNAP, 'authorizationRef': 'security.repair-apply-authorization.v1:' + H('a'),
                'state': 'APPLYING', 'stagedPaths': ['src/a.ts', 'src/b.ts'], 'appliedPaths': ['src/a.ts'],
                'preimageBlobs': [{'path': 'src/a.ts', 'sha256': H('5'), 'bytes': 10}, {'path': 'src/b.ts', 'sha256': H('6'), 'bytes': 12}]}
records = {
    'journalApplying': journal_base,
    'journalApplied': dict(journal_base, state='APPLIED', appliedPaths=['src/a.ts', 'src/b.ts']),
    'journalCommitted': dict(journal_base, state='COMMITTED', appliedPaths=['src/a.ts', 'src/b.ts'], appliedSnapshotId='snapshot2:' + H('d')),
    'journalRolledBack': dict(journal_base, state='FAILED_ROLLED_BACK'),
    'journalBlocked': dict(journal_base, state='RECOVERY_BLOCKED', blockedPaths=['src/a.ts']),
    'journalApplyingAfterRequiresBroker': dict(journal_base, restoreIntent=[{'path': 'src/a.ts', 'restoreDigest': H('5')}]),
    'journalOfOtherPlan': dict(journal_base, repairPlanId='repairplan2:' + H('0')),
}
computed = {}
for name, j in records.items():
    computed['ref_' + name] = M.repair_journal_identity(j)
    computed['digest_' + name] = M.repair_journal_state_digest(j)
assert computed['ref_journalApplying'] == computed['ref_journalApplied'] == computed['ref_journalCommitted'] == computed['ref_journalRolledBack'] == computed['ref_journalBlocked'] == computed['ref_journalApplyingAfterRequiresBroker']
assert computed['digest_journalApplying'] == computed['digest_journalApplyingAfterRequiresBroker'] != computed['digest_journalRolledBack']
assert computed['ref_journalOfOtherPlan'] != computed['ref_journalApplying']

ctx_base = {'projectId': PRJ, 'repairPlanId': PLAN, 'baseSnapshotId': SNAP, 'journal': '$journalApplying', 'recoveryRequestId': REQ_REC,
            'recoveryExecutionId': EXEC_REC, 'ci': False, 'admittedTime': '2027-01-10T12:00:00Z', 'custodyAdmitted': True, 'policyAdmitsRepair': True,
            'recipeClosureId': RECIPE, 'revokedClosures': [REVOKED], 'admittedClosures': [RECIPE]}
authz_base = {'authorizationSchema': 1, 'kind': 'repair-recover', 'projectId': PRJ, 'repairPlanId': PLAN, 'baseSnapshotId': SNAP, 'recipeClosureId': RECIPE,
              'journalRef': '$ref_journalApplying', 'journalState': 'APPLYING', 'observedJournalStateDigest': '$digest_journalApplying',
              'recoveryAction': 'roll-back-renamed', 'originalRequestId': REQ_APPLY, 'recoveryRequestId': REQ_REC, 'recoveryExecutionId': EXEC_REC,
              'consent': {'mode': 'interactive-explicit', 'policyRecordId': None, 'ci': False}, 'issuedAt': '2027-01-10T11:30:00Z',
              'expiresAt': '2027-01-11T11:30:00Z', 'leaseMode': 'EXCLUSIVE', 'mutationBoundary': 'host-broker', 'repositoryExecution': False, 'newEdits': False}
COMMIT_AUTHZ = {'$from': 'authorization', 'journalRef': '$ref_journalApplied', 'journalState': 'APPLIED', 'observedJournalStateDigest': '$digest_journalApplied',
                'recoveryAction': 'verify-postimages-and-commit'}
COMMIT_CTX = {'$from': 'ctx', 'journal': '$journalApplied'}


def rc(cid, authz=None, ctx=None, expect=None, valid=None, note=None):
    c = {'id': cid, 'input': {'authorization': authz if authz is not None else '$authorization', 'ctx': ctx if ctx is not None else '$ctx'}, 'expect': expect}
    if valid is not None:
        c['inputSchemas'] = {'authorization': 'RepairRecoveryAuthorizationV1'}; c['inputValid'] = valid
    if note:
        c['note'] = note
    return c


def refuse(refusals, d9=D9_PRE, **more):
    e = {'result': 'REFUSE', 'refusals': refusals, 'd9': d9, 'grantsRepositoryExecution': False, 'grantsNewEdits': False, 'action': None}
    e.update(more); return e


recovery_cases = [
    rc('valid-rollback-recovery-authorization-admits-under-exclusive-broker-boundary-without-consulting-recipe-trust',
       expect={'result': 'ADMIT', 'action': 'roll-back-renamed', 'leaseMode': 'EXCLUSIVE', 'mutationBoundary': 'host-broker', 'grantsRepositoryExecution': False,
               'grantsNewEdits': False, 'planScope': 'original-plan-only', 'recipeTrustConsulted': False, 'journalRef': '$ref_journalApplying',
               'journalStateDigest': '$digest_journalApplying', 'identityDomain': 'security.repair-recovery-authorization.v1', 'd9': None,
               'trustedContextInputs.length': 13}, valid=True),
    rc('rollback-recovery-admits-although-the-recipe-closure-is-revoked-safe-rollback-is-not-re-execution',
       authz={'$from': 'authorization', 'recipeClosureId': REVOKED}, ctx={'$from': 'ctx', 'recipeClosureId': REVOKED, 'admittedClosures': []},
       expect={'result': 'ADMIT', 'action': 'roll-back-renamed', 'recipeTrustConsulted': False},
       note='Restoring retained preimages after the recipe was revoked is exactly what revocation rollback is; recipe trust is not an input to rollback/cleanup.'),
    rc('discard-temps-recovery-for-a-staged-journal-admits-without-recipe-trust',
       authz={'$from': 'authorization', 'recipeClosureId': REVOKED, 'journalState': 'STAGED', 'observedJournalStateDigest': '$digest_journalStaged', 'recoveryAction': 'discard-temps'},
       ctx={'$from': 'ctx', 'journal': '$journalStaged', 'recipeClosureId': REVOKED, 'admittedClosures': []},
       expect={'result': 'ADMIT', 'action': 'discard-temps', 'recipeTrustConsulted': False}),
    rc('commit-recovery-with-a-revoked-recipe-refuses-first-under-current-trust',
       authz=dict(COMMIT_AUTHZ, recipeClosureId=REVOKED), ctx=dict(COMMIT_CTX, recipeClosureId=REVOKED),
       expect=refuse(['AUTHZ.RECIPE_CLOSURE_REVOKED'], D9_EXT, recipeTrustConsulted=True),
       note='verify-postimages-and-commit would commit the recipe\'s postimages: that is re-executing the recipe\'s effect and needs the recipe admitted under CURRENT trust.'),
    rc('commit-recovery-with-an-admitted-recipe-admits-and-consults-trust',
       authz=COMMIT_AUTHZ, ctx=COMMIT_CTX,
       expect={'result': 'ADMIT', 'action': 'verify-postimages-and-commit', 'recipeTrustConsulted': True, 'journalRef': '$ref_journalApplied', 'journalStateDigest': '$digest_journalApplied'}),
    rc('commit-recovery-with-a-recipe-not-positively-admitted-refuses',
       authz=COMMIT_AUTHZ, ctx=dict(COMMIT_CTX, admittedClosures=[]),
       expect=refuse(['AUTHZ.RECIPE_CLOSURE_NOT_ADMITTED'], recipeTrustConsulted=True)),
    rc('requested-action-other-than-the-one-the-journal-state-admits-refuses',
       authz={'$from': 'authorization', 'recoveryAction': 'verify-postimages-and-commit'},
       expect=refuse(['AUTHZ.RECOVERY_ACTION_MISMATCH'], recipeTrustConsulted=True),
       note='An APPLYING journal admits only roll-back-renamed; the caller cannot pick commit. The finite action is bound in the record, not chosen at recovery time.'),
    rc('terminal-journal-state-admits-no-recovery-mutation-inspection-is-read-only',
       authz={'$from': 'authorization', 'journalState': 'COMMITTED', 'observedJournalStateDigest': '$digest_journalCommitted', 'recoveryAction': 'discard-temps'},
       ctx={'$from': 'ctx', 'journal': '$journalCommitted'},
       expect=refuse(['AUTHZ.RECOVERY_NOT_MUTATING:COMMITTED'], journalRef='$ref_journalCommitted'),
       note='The journal identity is the same for every state of one journal (noncircular preimage); a committed journal has nothing to authorize and repair_inspect needs no record.'),
    rc('recovery-blocked-journal-is-never-authorizable',
       authz={'$from': 'authorization', 'journalState': 'RECOVERY_BLOCKED', 'observedJournalStateDigest': '$digest_journalBlocked'},
       ctx={'$from': 'ctx', 'journal': '$journalBlocked'},
       expect=refuse(['AUTHZ.RECOVERY_NOT_MUTATING:RECOVERY_BLOCKED'])),
    rc('journal-identity-mismatch-refuses-bound-to-the-exact-original-journal',
       authz={'$from': 'authorization', 'journalRef': 'security.repair-apply-journal-identity.v1:' + H('0')},
       expect=refuse(['AUTHZ.JOURNAL_MISMATCH'], journalRef='$ref_journalApplying')),
    rc('replay-after-a-successful-rollback-refuses-observed-journal-state-moved',
       ctx={'$from': 'ctx', 'journal': '$journalRolledBack'},
       expect=refuse(['AUTHZ.JOURNAL_STATE_MISMATCH', 'AUTHZ.JOURNAL_STATE_MOVED', 'AUTHZ.RECOVERY_NOT_MUTATING:FAILED_ROLLED_BACK'],
                     journalRef='$ref_journalApplying', journalStateDigest='$digest_journalRolledBack'),
       note='Single use: the rollback changed the journal state, so the retained authorization no longer matches the observed state digest (and the journal is terminal).'),
    rc('crash-before-the-first-recovery-write-leaves-the-state-digest-unchanged-and-the-same-authorization-resumes',
       ctx={'$from': 'ctx', 'journal': '$journalApplyingAfterRequiresBroker', 'admittedTime': '2027-01-11T09:00:00Z', 'recoveryExecutionId': 'exec1_' + '3' * 32},
       authz={'$from': 'authorization', 'recoveryExecutionId': 'exec1_' + '3' * 32},
       expect={'result': 'ADMIT', 'action': 'roll-back-renamed', 'journalStateDigest': '$digest_journalApplying'},
       note='A requires-broker return (restore intent recorded, no target written) or a crash before the first restore leaves {state, stagedPaths, appliedPaths, preimageBlobs} unchanged; the same recovery request may resume with a fresh attempt inside the lifetime.'),
    rc('expired-authorization-refuses', ctx={'$from': 'ctx', 'admittedTime': '2027-01-11T11:30:01Z'}, expect=refuse(['AUTHZ.EXPIRED'])),
    rc('not-yet-valid-authorization-refuses', ctx={'$from': 'ctx', 'admittedTime': '2027-01-10T11:29:59Z'}, expect=refuse(['AUTHZ.NOT_YET_VALID'])),
    rc('lifetime-beyond-the-24h-bound-refuses', authz={'$from': 'authorization', 'expiresAt': '2027-01-11T11:30:01Z'}, expect=refuse(['AUTHZ.LIFETIME_BOUND'])),
    rc('expiry-not-after-issue-refuses', authz={'$from': 'authorization', 'expiresAt': '2027-01-10T11:30:00Z'}, expect=refuse(['AUTHZ.LIFETIME_BOUND', 'AUTHZ.EXPIRED'])),
    rc('no-admitted-time-context-refuses', ctx={'$from': 'ctx', 'admittedTime': None}, expect=refuse(['AUTHZ.NO_ADMITTED_TIME_CONTEXT']),
       note='The current time is the S4 admitted evaluation time, never the raw wall clock.'),
    rc('recovery-request-equal-to-the-original-apply-request-refuses-not-fresh',
       authz={'$from': 'authorization', 'recoveryRequestId': REQ_APPLY}, ctx={'$from': 'ctx', 'recoveryRequestId': REQ_APPLY},
       expect=refuse(['AUTHZ.RECOVERY_REQUEST_NOT_FRESH'])),
    rc('recovery-request-mismatch-with-the-invocation-refuses', ctx={'$from': 'ctx', 'recoveryRequestId': 'req1_' + '3' * 32},
       expect=refuse(['AUTHZ.RECOVERY_REQUEST_MISMATCH'])),
    rc('original-request-differing-from-the-journal-refuses', authz={'$from': 'authorization', 'originalRequestId': 'req1_' + '4' * 32},
       expect=refuse(['AUTHZ.ORIGINAL_REQUEST_MISMATCH'])),
    rc('repository-execution-true-is-not-grantable-through-recovery-authorization', authz={'$from': 'authorization', 'repositoryExecution': True},
       expect=refuse(['AUTHZ.REPOSITORY_EXECUTION_NOT_GRANTABLE_HERE']), valid=False),
    rc('new-edits-true-is-not-grantable-through-recovery-authorization', authz={'$from': 'authorization', 'newEdits': True},
       expect=refuse(['AUTHZ.NEW_EDITS_NOT_GRANTABLE_HERE']), valid=False,
       note='Recovery never writes a byte the original plan did not name; broadening the plan needs a new preview/apply.'),
    rc('ci-interactive-consent-refuses', authz={'$from': 'authorization', 'consent': {'mode': 'interactive-explicit', 'policyRecordId': None, 'ci': True}},
       ctx={'$from': 'ctx', 'ci': True}, expect=refuse(['AUTHZ.CI_REQUIRES_POLICY_RECORD'])),
    rc('ci-with-policy-record-admits', authz={'$from': 'authorization', 'consent': {'mode': 'policy-record', 'policyRecordId': H('d'), 'ci': True}},
       ctx={'$from': 'ctx', 'ci': True}, expect={'result': 'ADMIT'}),
    rc('custody-not-re-admitted-on-the-recovery-invocation-refuses', ctx={'$from': 'ctx', 'custodyAdmitted': False}, expect=refuse(['AUTHZ.CUSTODY_NOT_ADMITTED']),
       note='The S3 custody rule of the current host applies to the recovery invocation itself; an old admission does not carry over.'),
    rc('repair-plan-mismatch-refuses-bound-to-exact-plan-identity', authz={'$from': 'authorization', 'repairPlanId': 'repairplan2:' + H('0')},
       expect=refuse(['AUTHZ.REPAIR_PLAN_MISMATCH'])),
    rc('journal-of-a-different-plan-in-context-refuses', ctx={'$from': 'ctx', 'journal': '$journalOfOtherPlan'},
       expect=refuse(['AUTHZ.JOURNAL_NOT_OF_THIS_PLAN', 'AUTHZ.JOURNAL_MISMATCH'], journalRef='$ref_journalOfOtherPlan')),
    rc('append-write-lease-mode-refuses-recovery-needs-exclusive', authz={'$from': 'authorization', 'leaseMode': 'APPEND-WRITE'}, expect=refuse(['AUTHZ.LEASE_MODE']), valid=False),
    rc('mutation-boundary-other-than-the-host-broker-refuses', authz={'$from': 'authorization', 'mutationBoundary': 'in-process'}, expect=refuse(['AUTHZ.MUTATION_BOUNDARY']), valid=False),
    rc('project-policy-not-admitting-repair-refuses', ctx={'$from': 'ctx', 'policyAdmitsRepair': False}, expect=refuse(['AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR'])),
    rc('unknown-member-refuses-shape', authz={'$from': 'authorization', 'extra': True}, expect=refuse(['AUTHZ.SHAPE']), valid=False),
    rc('consent-ci-integer-zero-is-not-false-shape', authz={'$from': 'authorization', 'consent': {'mode': 'interactive-explicit', 'policyRecordId': None, 'ci': 0}},
       expect=refuse(['AUTHZ.CONSENT_SHAPE']), valid=False),
]
records['journalStaged'] = dict(journal_base, state='STAGED', appliedPaths=[])
computed['ref_journalStaged'] = M.repair_journal_identity(records['journalStaged']); computed['digest_journalStaged'] = M.repair_journal_state_digest(records['journalStaged'])
recovery_doc = {
    'standing': "SYNTHETIC RepairRecoveryAuthorizationV1 records evaluated by security_lifecycle_model_v1.admit_recovery_authorization (S10.2, post-reset review v2 P9). Repair recovery is a separately authorized host-brokered mutation within the ORIGINAL plan's authority under the EXCLUSIVE lease: it restores retained preimages or verifies-and-commits exact postimages, never runs repository code, never writes a byte the plan did not name and never broadens the plan. Identity H('security.repair-recovery-authorization.v1', record) is the workflow RepairApplyJournalV1.recoveryAuthorizationRef. `computed` values are produced by the model's repair_journal_identity (H over the closed noncircular identity preimage) and repair_journal_state_digest (raw SHA-256 of canonical {state, stagedPaths, appliedPaths, preimageBlobs}); expectations are same-author, not an independent oracle.",
    'model': 'recovery-authorization',
    'computed': computed,
    'records': records,
    'ctxBase': ctx_base,
    'authorizationBase': authz_base,
    'cases': recovery_cases,
}
dump(SEC / 'repair-recovery-authorization-cases.v1.json', recovery_doc)

# ------------------------------------------------------------------ installation transition intent / journal / recovery (S9.2)
CA, CB = 'closure2:' + H('1'), 'closure2:' + H('2')
PROFILE = H('d')
intents = {
    'intentUpdateSchemaChange': {'schemaVersion': 1, 'operation': 'core-update', 'fromCoreClosure': CA, 'toCoreClosure': CB, 'fromStateSchema': 1, 'toStateSchema': 2,
                                 'fromStoreGeneration': 3, 'toStoreGeneration': 4, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 7, 'rollbackDeadline': None},
    'intentUpdateSameSchema': {'schemaVersion': 1, 'operation': 'core-update', 'fromCoreClosure': CA, 'toCoreClosure': CB, 'fromStateSchema': 2, 'toStateSchema': 2,
                               'fromStoreGeneration': 4, 'toStoreGeneration': 4, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 7, 'rollbackDeadline': None},
    'intentRepair': {'schemaVersion': 1, 'operation': 'core-repair', 'fromCoreClosure': CA, 'toCoreClosure': CA, 'fromStateSchema': 2, 'toStateSchema': 2,
                     'fromStoreGeneration': 4, 'toStoreGeneration': 4, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 7, 'rollbackDeadline': None},
    'intentCoreRollback': {'schemaVersion': 1, 'operation': 'core-rollback', 'fromCoreClosure': CB, 'toCoreClosure': CA, 'fromStateSchema': 2, 'toStateSchema': 2,
                           'fromStoreGeneration': 4, 'toStoreGeneration': 4, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 8, 'rollbackDeadline': '2027-02-01T00:00:00Z'},
    'intentStoreMigrate': {'schemaVersion': 1, 'operation': 'store-migrate', 'fromCoreClosure': CB, 'toCoreClosure': CB, 'fromStateSchema': 1, 'toStateSchema': 2,
                           'fromStoreGeneration': 3, 'toStoreGeneration': 4, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 8, 'rollbackDeadline': None},
    'intentStoreRollback': {'schemaVersion': 1, 'operation': 'store-rollback', 'fromCoreClosure': CB, 'toCoreClosure': CB, 'fromStateSchema': 2, 'toStateSchema': 1,
                            'fromStoreGeneration': 4, 'toStoreGeneration': 3, 'platformProfileSetBodyDigest': PROFILE, 'preconditionGeneration': 8, 'rollbackDeadline': '2027-02-01T00:00:00Z'},
}
REG = ['ns-b', 'ns-a', 'ns-c']; REG_SORTED = ['ns-a', 'ns-b', 'ns-c']
tcomputed = {'registryDigest3': M.registry_digest(REG), 'registryDigestEmpty': M.registry_digest([]), 'registryDigest4': M.registry_digest(REG + ['ns-d'])}
trecords = {}
for name, it in intents.items():
    tcomputed['digest_' + name] = M.transition_intent_digest(it)
    trecords['journal_' + name[len('intent'):]] = M.transition_journal_record(it, REG)
trecords['journal_UpdateSchemaChange_emptyRegistry'] = M.transition_journal_record(intents['intentUpdateSchemaChange'], [])
trecords['journal_UpdateSchemaChange_smallerLeaseSet'] = dict(trecords['journal_UpdateSchemaChange'], leaseSet=['ns-a'])
trecords['journal_UpdateSchemaChange_preparing'] = dict(trecords['journal_UpdateSchemaChange'], state='PREPARING')
trecords['journal_UpdateSchemaChange_prepared'] = dict(trecords['journal_UpdateSchemaChange'], state='PREPARED')
trecords['journal_UpdateSchemaChange_committed'] = dict(trecords['journal_UpdateSchemaChange'], state='COMMITTED')
trecords['journal_UpdateSchemaChange_done'] = dict(trecords['journal_UpdateSchemaChange'], state='DONE')
trecords['journal_UpdateSchemaChange_wrongField'] = dict(trecords['journal_UpdateSchemaChange'], toCoreClosure=CA)
trecords['journal_StoreMigrate_prepared'] = dict(trecords['journal_StoreMigrate'], state='PREPARED')
trecords['journal_CoreRollback_committed'] = dict(trecords['journal_CoreRollback'], state='COMMITTED')
assert trecords['journal_UpdateSchemaChange']['leaseSet'] == REG_SORTED and trecords['journal_UpdateSameSchema']['leaseSet'] == [] and trecords['journal_UpdateSchemaChange_emptyRegistry']['leaseSet'] == []
tctx = {'intent': '$intentUpdateSchemaChange', 'intentDigest': '$digest_intentUpdateSchemaChange', 'namespaceRegistry': REG, 'fenceHeld': True, 'leasesHeld': REG_SORTED,
        'currentStateSchema': 1, 'currentStoreGeneration': 3, 'currentCoreGeneration': 7, 'admittedTime': '2027-01-10T12:00:00Z'}
rctx = {'namespaceRegistry': REG, 'fenceHeld': True, 'leasesReacquired': REG_SORTED, 'storeFootprint': None}


def tj(cid, journal, ctx, expect, note=None):
    c = {'id': cid, 'model': 'transition-journal', 'outputSchema': 'TransitionJournalAdmissionV1', 'input': {'journal': journal, 'ctx': ctx}, 'expect': expect}
    if note: c['note'] = note
    return c


def ti(cid, intent, expect, note=None):
    c = {'id': cid, 'model': 'transition-intent', 'outputSchema': 'TransitionIntentAdmissionV1', 'input': {'intent': intent}, 'expect': expect}
    if note: c['note'] = note
    return c


def tr(cid, journal, ctx, expect, note=None):
    c = {'id': cid, 'model': 'transition-recovery', 'outputSchema': 'TransitionRecoveryV1', 'input': {'journal': journal, 'ctx': ctx}, 'expect': expect}
    if note: c['note'] = note
    return c


def trefuse(refusals):
    return {'result': 'REFUSE', 'refusals': refusals, 'd9': D9_PRE, 'journalRef': None}


def ctx_for(name, held, schema, store, gen=None, **more):
    c = {'$from': 'ctx', 'intent': '$' + name, 'intentDigest': '$digest_' + name, 'leasesHeld': held, 'currentStateSchema': schema, 'currentStoreGeneration': store}
    if gen is not None: c['currentCoreGeneration'] = gen
    c.update(more); return c


journal_cases = [
    dict(tj('schema-change-core-update-journals-every-registered-namespace-as-its-exact-lease-set', '$journal_UpdateSchemaChange', '$ctx',
       {'result': 'ADMIT', 'affects': 'all-registered', 'leaseSet': REG_SORTED, 'd9': None, 'trustedContextInputs.length': 9},
       'The journal names the exact lease set the composition held (locator order), the frozen registry, the admitted-intent digest and the from-bindings observed under the fence.'),
         inputSchemas={'journal': 'InstallationTransitionJournalV1', 'ctx.intent': 'InstallationTransitionIntentV1'}, inputValid=True),
    tj('same-schema-core-update-journals-the-empty-lease-set-generations-stay-pinned', '$journal_UpdateSameSchema', ctx_for('intentUpdateSameSchema', [], 2, 4),
       {'result': 'ADMIT', 'affects': 'none', 'leaseSet': []}),
    tj('core-repair-journals-the-empty-lease-set', '$journal_Repair', ctx_for('intentRepair', [], 2, 4), {'result': 'ADMIT', 'affects': 'none', 'leaseSet': []}),
    tj('core-rollback-inside-the-window-journals-every-registered-namespace', '$journal_CoreRollback', ctx_for('intentCoreRollback', REG_SORTED, 2, 4, 8),
       {'result': 'ADMIT', 'affects': 'all-registered', 'leaseSet': REG_SORTED}),
    tj('core-rollback-after-the-host-observed-deadline-refuses', '$journal_CoreRollback', ctx_for('intentCoreRollback', REG_SORTED, 2, 4, 8, admittedTime='2027-02-01T00:00:01Z'),
       trefuse(['TRANSITION.ROLLBACK_WINDOW_EXPIRED']), 'The deadline is the host-observed rollback window in the admitted intent; user arguments cannot extend it.'),
    tj('core-rollback-without-an-admitted-time-context-refuses', '$journal_CoreRollback', ctx_for('intentCoreRollback', REG_SORTED, 2, 4, 8, admittedTime=None),
       trefuse(['TRANSITION.NO_ADMITTED_TIME_CONTEXT'])),
    dict(tj('store-migrate-journals-every-registered-namespace-and-the-new-store-generation', '$journal_StoreMigrate', ctx_for('intentStoreMigrate', REG_SORTED, 1, 3, 8),
       {'result': 'ADMIT', 'affects': 'all-registered', 'leaseSet': REG_SORTED}), inputSchemas={'journal': 'InstallationTransitionJournalV1', 'ctx.intent': 'InstallationTransitionIntentV1'}, inputValid=True),
    tj('store-rollback-inside-the-window-journals-every-registered-namespace', '$journal_StoreRollback', ctx_for('intentStoreRollback', REG_SORTED, 2, 4, 8),
       {'result': 'ADMIT', 'affects': 'all-registered', 'leaseSet': REG_SORTED}),
    tj('caller-chosen-smaller-lease-set-refuses-scope-mismatch', '$journal_UpdateSchemaChange_smallerLeaseSet', {'$from': 'ctx', 'leasesHeld': ['ns-a']},
       trefuse(['TRANSITION.SCOPE_MISMATCH', 'TRANSITION.LEASE_SET_NOT_HELD']),
       'The affected set is decided by core_transition_affected_namespaces over the frozen registry, never by the caller; a smaller set fails both the scope and the held-set law.'),
    tj('busy-namespace-means-the-lease-set-is-not-held-and-no-journal-may-be-written', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'leasesHeld': ['ns-a']},
       trefuse(['TRANSITION.LEASE_SET_NOT_HELD']), 'All-or-nothing: with ns-b busy the composition released ns-a, reported PROJECT.BUSY and never reached the journal write.'),
    tj('fence-not-held-refuses', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'fenceHeld': False}, trefuse(['TRANSITION.FENCE_NOT_HELD'])),
    tj('intent-digest-mismatch-refuses', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'intentDigest': H('0')}, trefuse(['TRANSITION.INTENT_DIGEST_MISMATCH'])),
    tj('journal-field-differing-from-the-admitted-intent-refuses', '$journal_UpdateSchemaChange_wrongField', '$ctx', trefuse(['TRANSITION.INTENT_FIELD_MISMATCH:toCoreClosure'])),
    tj('registry-differing-from-the-frozen-registry-refuses-fail-closed', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'namespaceRegistry': REG + ['ns-d'], 'leasesHeld': REG_SORTED + ['ns-d']},
       trefuse(['TRANSITION.REGISTRY_MISMATCH', 'TRANSITION.REGISTRY_DIGEST_MISMATCH', 'TRANSITION.SCOPE_MISMATCH'])),
    tj('current-state-schema-differing-from-the-intent-refuses', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'currentStateSchema': 2}, trefuse(['TRANSITION.CURRENT_SCHEMA_MISMATCH'])),
    tj('current-store-generation-differing-from-the-intent-refuses', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'currentStoreGeneration': 4}, trefuse(['TRANSITION.CURRENT_STORE_MISMATCH'])),
    tj('precondition-core-generation-differing-refuses', '$journal_UpdateSchemaChange', {'$from': 'ctx', 'currentCoreGeneration': 8}, trefuse(['TRANSITION.PRECONDITION_GENERATION_MISMATCH'])),
    tj('journal-not-in-the-initial-leased-state-refuses', '$journal_UpdateSchemaChange_preparing', '$ctx', trefuse(['TRANSITION.INITIAL_STATE:PREPARING'])),
    tj('empty-registry-schema-change-journals-all-registered-with-an-empty-lease-set', '$journal_UpdateSchemaChange_emptyRegistry', {'$from': 'ctx', 'namespaceRegistry': [], 'leasesHeld': []},
       {'result': 'ADMIT', 'affects': 'all-registered', 'leaseSet': []}),
    {'id': 'journal-shape-with-an-unknown-member-refuses', 'model': 'transition-journal', 'outputSchema': 'TransitionJournalAdmissionV1',
     'input': {'journal': {'$from': 'journal_UpdateSchemaChange', 'extra': True}, 'ctx': '$ctx'}, 'expect': trefuse(['TRANSITION.JOURNAL_SHAPE']),
     'inputSchemas': {'journal': 'InstallationTransitionJournalV1'}, 'inputValid': False},
    ti('core-repair-changing-the-closure-refuses', {'$from': 'intentRepair', 'toCoreClosure': CB}, {'result': 'REFUSE', 'refusals': ['TRANSITION.REPAIR_MUST_KEEP_CLOSURE']}),
    ti('store-migrate-without-a-schema-advance-refuses', {'$from': 'intentStoreMigrate', 'fromStateSchema': 2}, {'result': 'REFUSE', 'refusals': ['TRANSITION.MIGRATE_REQUIRES_SCHEMA_ADVANCE']}),
    ti('store-operation-changing-the-core-closure-refuses', {'$from': 'intentStoreMigrate', 'toCoreClosure': CA}, {'result': 'REFUSE', 'refusals': ['TRANSITION.STORE_OPERATION_KEEPS_CORE']}),
    ti('same-schema-core-update-re-selecting-the-store-refuses', {'$from': 'intentUpdateSameSchema', 'toStoreGeneration': 5}, {'result': 'REFUSE', 'refusals': ['TRANSITION.SAME_SCHEMA_KEEPS_STORE']}),
    ti('schema-change-without-a-new-store-refuses', {'$from': 'intentUpdateSchemaChange', 'toStoreGeneration': 3}, {'result': 'REFUSE', 'refusals': ['TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE']}),
    ti('core-rollback-without-a-deadline-refuses', {'$from': 'intentCoreRollback', 'rollbackDeadline': None}, {'result': 'REFUSE', 'refusals': ['TRANSITION.ROLLBACK_REQUIRES_DEADLINE']}),
    ti('core-update-carrying-a-deadline-refuses', {'$from': 'intentUpdateSchemaChange', 'rollbackDeadline': '2027-02-01T00:00:00Z'}, {'result': 'REFUSE', 'refusals': ['TRANSITION.DEADLINE_ONLY_FOR_ROLLBACK']}),
    ti('unknown-operation-refuses', {'$from': 'intentRepair', 'operation': 'install'}, {'result': 'REFUSE', 'refusals': ['TRANSITION.OPERATION:install']}),
    {'id': 'nine-field-legacy-intent-without-store-generations-refuses-shape', 'model': 'transition-intent', 'outputSchema': 'TransitionIntentAdmissionV1',
     'input': {'intent': {k: v for k, v in intents['intentUpdateSchemaChange'].items() if k not in ('fromStoreGeneration', 'toStoreGeneration')}},
     'expect': {'result': 'REFUSE', 'refusals': ['TRANSITION.INTENT_SHAPE'], 'requiredFields': sorted(M.TRANSITION_INTENT_KEYS), 'operations': list(M.TRANSITION_OPERATIONS)},
     'inputSchemas': {'intent': 'InstallationTransitionIntentV1'}, 'inputValid': False,
     'note': 'The current workflow CoreTransitionIntentV1 (nine fields, three operations) cannot express a store operation or the store binding; the required successor contract is the requiredFields/operations output.'},
    ti('schema-version-true-is-not-one-exact-typed', {'$from': 'intentRepair', 'schemaVersion': True}, {'result': 'REFUSE', 'refusals': ['TRANSITION.INTENT_SCHEMA']}),
    ti('every-well-formed-operation-admits', '$intentStoreRollback', {'result': 'ADMIT', 'refusals': [], 'd9': None}),
    tr('crash-at-leased-aborts-and-releases-the-journaled-set', '$journal_UpdateSchemaChange', '$rctx',
       {'action': 'ABORT', 'journalStateAfter': 'ABORTED', 'reacquire': REG_SORTED, 'refusal': None, 'd9': None, 'trustedContextInputs.length': 4}),
    tr('crash-at-prepared-store-migrate-with-the-old-store-fenced-resumes-commit-from-step-3', '$journal_StoreMigrate_prepared',
       {'$from': 'rctx', 'storeFootprint': {'old': {'present': True, 'unbootstrappedReason': 'RESTORED'}, 'new': {'dir': 'migrating', 'state': 'PREPARED'}}},
       {'action': 'RESUME-COMMIT', 'fromStep': 3, 'journalStateAfter': 'DONE', 'reacquire': REG_SORTED}),
    tr('crash-at-prepared-store-migrate-with-the-old-store-unfenced-aborts', '$journal_StoreMigrate_prepared',
       {'$from': 'rctx', 'storeFootprint': {'old': {'present': True, 'unbootstrappedReason': None}, 'new': {'dir': 'migrating', 'state': 'PREPARED'}}},
       {'action': 'ABORT', 'journalStateAfter': 'ABORTED'}),
    tr('crash-at-prepared-store-operation-without-a-footprint-quarantines', '$journal_StoreMigrate_prepared', '$rctx',
       {'action': 'QUARANTINE', 'refusal': 'MIGRATION.CORRUPT', 'd9': {'class': 'operational-failed', 'exit': 4, 'code': 'LEDGER.CORRUPT'}}),
    tr('crash-at-prepared-core-update-aborts-the-unselected-generation', '$journal_UpdateSchemaChange_prepared', '$rctx', {'action': 'ABORT', 'journalStateAfter': 'ABORTED'}),
    tr('crash-at-committed-core-rollback-resumes-and-is-never-reversed', '$journal_CoreRollback_committed', '$rctx',
       {'action': 'RESUME-COMMIT', 'journalStateAfter': 'DONE', 'reacquire': REG_SORTED}, 'An expired rollback window after commit does not undo a committed rollback (S15).'),
    tr('registry-changed-since-the-journal-quarantines-migration-corrupt', '$journal_UpdateSchemaChange', {'$from': 'rctx', 'namespaceRegistry': REG + ['ns-d'], 'leasesReacquired': REG_SORTED + ['ns-d']},
       {'action': 'QUARANTINE', 'refusal': 'MIGRATION.CORRUPT', 'd9': {'class': 'operational-failed', 'exit': 4, 'code': 'LEDGER.CORRUPT'}, 'reacquire': REG_SORTED},
       'Registration needs the fence, so a namespace registered after the intent cannot exist; finding one makes the footprint ambiguous and nothing is chosen.'),
    tr('journaled-lease-set-not-exactly-reacquired-is-busy', '$journal_UpdateSchemaChange', {'$from': 'rctx', 'leasesReacquired': ['ns-a', 'ns-c']},
       {'action': 'BUSY', 'refusal': 'PROJECT.BUSY', 'd9': {'class': 'operational-failed', 'exit': 4, 'code': 'LEDGER.BUSY_TIMEOUT'}, 'reacquire': REG_SORTED}),
    tr('recovery-without-the-fence-refuses', '$journal_UpdateSchemaChange', {'$from': 'rctx', 'fenceHeld': False},
       {'action': 'REFUSE', 'refusal': 'TRANSITION.FENCE_NOT_HELD', 'd9': D9_PRE}),
    tr('done-journal-only-releases', '$journal_UpdateSchemaChange_done', '$rctx', {'action': 'RELEASE-ONLY', 'journalStateAfter': 'DONE'}),
    tr('same-schema-journal-recovers-with-the-empty-lease-set', '$journal_UpdateSameSchema', {'$from': 'rctx', 'leasesReacquired': []}, {'action': 'ABORT', 'reacquire': []}),
]
transition_doc = {
    'standing': "SYNTHETIC installation transition intents, InstallationTransitionJournalV1 records and crash-recovery contexts evaluated by security_lifecycle_model_v1.admit_transition_intent / admit_transition_journal / recover_transition_journal (S9.2, post-reset review v2 P10). One closed journal serves core update|repair|rollback and store migrate|rollback under the S7 core-transition lock set: it binds the admitted-intent digest, from/to closure, schema, store generation and core generation, the registry frozen under the fence, the affected set and the EXACT lease set held (never caller-chosen), and is written only after every lease is held. `computed` values come from the model's transition_intent_digest and registry_digest; `records` journals are built by transition_journal_record over the fixture registry ['ns-b','ns-a','ns-c']. Expectations are same-author, not an independent oracle; the host observations in every ctx are asserted TCB inputs.",
    'computed': tcomputed,
    'records': dict(intents, **trecords),
    'ctxBase': tctx,
    'rctx': rctx,
    'cases': journal_cases,
}
dump(SEC / 'transition-journal-cases.v1.json', transition_doc)

# ------------------------------------------------------------------ lease-cases: transition-journal op
lease = load_roundtrip('lease-cases.v1.json')
A = lambda actor, op, **kw: dict({'actor': actor, 'op': op}, **kw)
lease_new = [
    {'id': 'transition-journal-names-the-exact-held-lease-set-after-all-or-nothing-acquisition',
     'input': {'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=REG_SORTED), A('T', 'transition-journal', namespaces=REG_SORTED),
                           A('T', 'core-transition-release'), A('T', 'fence-release')], 'namespaceRegistry': REG},
     'expect': {'deadlockFree': True, 'trace.1.result': 'ACQUIRED-ALL:ns-a,ns-b,ns-c', 'trace.2.result': 'JOURNALED:ns-a,ns-b,ns-c', 'trace.3.result': 'RELEASED-ALL:ns-c,ns-b,ns-a', 'final.fence': None}},
    {'id': 'transition-journal-before-the-lease-set-is-held-is-a-violation-negative',
     'input': {'actions': [A('T', 'fence-acquire'), A('T', 'transition-journal', namespaces=REG_SORTED), A('T', 'fence-release')], 'namespaceRegistry': REG},
     'expect': {'deadlockFree': False, 'trace.1.result': 'REFUSED-LEASE-SET-NOT-HELD', 'violations': ['T journals a transition before its lease set is held']}},
    {'id': 'transition-journal-naming-a-set-other-than-the-held-set-is-a-violation-negative',
     'input': {'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=REG_SORTED), A('T', 'transition-journal', namespaces=['ns-a']),
                           A('T', 'core-transition-release'), A('T', 'fence-release')], 'namespaceRegistry': REG},
     'expect': {'deadlockFree': False, 'trace.2.result': 'REFUSED-LEASE-SET-MISMATCH', 'violations': ['T journals a lease set (ns-a) that differs from the held set (ns-a,ns-b,ns-c)']}},
    {'id': 'same-schema-transition-journals-the-empty-lease-set-under-the-fence-alone',
     'input': {'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=[]), A('T', 'transition-journal', namespaces=[]),
                           A('T', 'core-transition-release'), A('T', 'fence-release')], 'namespaceRegistry': REG},
     'expect': {'deadlockFree': True, 'trace.1.result': 'ACQUIRED-ALL:no-namespace-affected', 'trace.2.result': 'JOURNALED:no-namespace-affected'}},
    {'id': 'transition-journal-without-the-fence-is-a-violation-negative',
     'input': {'actions': [A('T', 'transition-journal', namespaces=[])], 'namespaceRegistry': REG},
     'expect': {'deadlockFree': False, 'trace.0.result': 'REFUSED-NO-FENCE'}},
]
new_ids = {c['id'] for c in lease_new}
lease['cases'] = [c for c in lease['cases'] if c['id'] not in new_ids] + lease_new
dump(SEC / 'lease-cases.v1.json', lease)

# ------------------------------------------------------------------ discovery-cases: boundary inventory export
disc = load_roundtrip('discovery-cases.v1.json')
R = '/home/alice/repo'
d = lambda **kw: dict({'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}, **kw)
f = lambda: {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
p3_fs = {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home/alice': d(mode='0700'),
         R: d(vcs=True), R + '/package.json': f(), R + '/vendor': d(), R + '/vendor/lib': d(vcs=True), R + '/vendor/lib/package.json': f(), R + '/vendor/lib/src': d(),
         R + '/vendor/lib/node_modules': d(), R + '/vendor/lib/node_modules/x': d(), R + '/vendor/lib/node_modules/x/package.json': f(),
         R + '/apps': d(), R + '/apps/site': d(), R + '/apps/site/opensip.json': f(), R + '/apps/site/package.json': f(), R + '/apps/site/sub': d(), R + '/apps/site/sub/Cargo.toml': f()}
custody_fs = {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home/alice': d(mode='0700'),
              R: d(vcs=True), R + '/package.json': f(), R + '/Cargo.toml': dict(f(), mode='0666'), R + '/tools': d(uid=1001), R + '/tools/package.json': f()}
nested_case = next(c for c in disc['cases'] if c['id'] == 'nested-config-inside-a-vcs-root-is-a-deliberate-project-boundary-launch-inside-selects-it')
disc_new = [
    {'id': 'boundary-inventory-exports-nested-repository-and-nested-project-as-relative-scope-paths', 'model': 'boundary-inventory', 'outputSchema': 'AdmittedBoundaryInventoryV1',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': p3_fs},
     'expect': {'schemaVersion': 1, 'source': 'security.discovery', 'selectedRoot': R, 'nestedRepositories': ['vendor/lib'], 'nestedProjects': ['apps/site'], 'custodyExcludedUnits': [],
                'prunedTrees': [{'path': 'vendor/lib/node_modules', 'reason': 'dependency-tree', 'markerCount': 1}]},
     'note': 'The post-reset v2 P3 fixture. The inventory is the trusted output an operational host passes unchanged to the native discover_units; absolute custody locators become relative scope paths under the selected root.'},
    {'id': 'boundary-inventory-from-a-launch-inside-the-nested-config-names-no-boundary', 'model': 'boundary-inventory', 'outputSchema': 'AdmittedBoundaryInventoryV1',
     'input': copy.deepcopy(nested_case['input']),
     'expect': {'selectedRoot': '/home/alice/mono/site', 'nestedRepositories': [], 'nestedProjects': [], 'custodyExcludedUnits': [], 'prunedTrees': []}},
    {'id': 'boundary-inventory-carries-custody-excluded-units-verbatim', 'model': 'boundary-inventory', 'outputSchema': 'AdmittedBoundaryInventoryV1',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': custody_fs},
     'expect': {'selectedRoot': R, 'nestedRepositories': [], 'nestedProjects': [],
                'custodyExcludedUnits': [{'path': '', 'reason': 'MARKER_CUSTODY:Cargo.toml:WRITABLE_BY_OTHERS'}, {'path': 'tools', 'reason': 'DIRECTORY_CUSTODY:FOREIGN_OWNER'}]},
     'note': 'Custody-excluded units are explicit unknown required scope (S3); the native layer marks their files outside-project-boundary rather than scanning uncustodied source.'},
    {'id': 'boundary-inventory-of-a-refused-discovery-exports-nothing', 'model': 'boundary-inventory',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': p3_fs, 'trustProjectOwner': True},
     'expectReject': 'BOUNDARY_INVENTORY_REQUIRES_ACCEPT'},
]
new_ids = {c['id'] for c in disc_new}
disc['cases'] = [c for c in disc['cases'] if c['id'] not in new_ids] + disc_new
dump(SEC / 'discovery-cases.v1.json', disc)
print('recovery cases', len(recovery_cases), 'transition cases', len(journal_cases), 'lease +', len(lease_new), 'discovery +', len(disc_new))
