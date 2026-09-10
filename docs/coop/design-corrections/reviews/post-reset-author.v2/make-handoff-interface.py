"""Generates handoff-interface.json for Codex from the corrected security/native bytes (exact record examples and the
references the model computes). UNPINNED scratch; not acceptance."""
import json, importlib.util
from pathlib import Path

ROOT = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections')
OUT = Path(__file__).resolve().parent / 'handoff-interface.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


C = load('canonical', ROOT / 'foundation/canonical.py')
S = load('sec', ROOT / 'security/security_lifecycle_model_v1.py')
N = load('nat', ROOT / 'native/native_evidence_model.v2.py')
chk = load('chk', ROOT / 'security/check-security-lifecycle.v1.py')

rdoc = C.parse((ROOT / 'security/repair-recovery-authorization-cases.v1.json').read_bytes()); rsubs = chk.build_subs(rdoc)
authz, rctx = rsubs['authorization'], rsubs['ctx']
adm = S.admit_recovery_authorization(authz, rctx)
recovery_ref = 'security.repair-recovery-authorization.v1:' + C.identity('security.repair-recovery-authorization.v1', authz)

tdoc = C.parse((ROOT / 'security/transition-journal-cases.v1.json').read_bytes()); tsubs = chk.build_subs(tdoc)
intent = tsubs['intentStoreMigrate']; reg = ['ns-b', 'ns-a', 'ns-c']
journal = S.transition_journal_record(intent, reg)
tadm = S.admit_transition_journal(journal, {'intent': intent, 'intentDigest': S.transition_intent_digest(intent), 'namespaceRegistry': reg, 'fenceHeld': True,
                                            'leasesHeld': journal['leaseSet'], 'currentStateSchema': 1, 'currentStoreGeneration': 3, 'currentCoreGeneration': 8, 'admittedTime': '2027-01-10T12:00:00Z'})

R, fs = chk._p3_repo()
sd = S.discovery({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs})
inv = S.boundary_inventory(sd)
markers = {p[len(R) + 1:]: {'sha256': '1' * 64} for p, e in fs.items() if p.startswith(R + '/') and e['kind'] == 'file' and p.rpartition('/')[2] in S.WORKSPACE_MARKERS}
nd = N.discover_units(markers, None, inv)

doc = {
    'standing': 'Author handoff interface (Claude post-reset author v2) for Codex joins. Owned bytes: security/, native/, discovery-defaults.py, the two contracts. Nothing here is accepted; pins/reports/registry/workflow schemas are Codex\'s.',
    'runWith': '/tmp/opensip-architecture-review-env/bin/python -I -B; load modules by path as integration-host-model.py does',
    '1_repairRecoveryAuthorization': {
        'issue': 'P9 / CX-01 / SHOULD-5: recovery mutation authority was a caller dict bound to plan+requestId and retained as auth:<16hex>',
        'securityRecord': 'security-lifecycle.schemas.v1.json#/schemas/RepairRecoveryAuthorizationV1 (product data, closed)',
        'admission': 'S.admit_recovery_authorization(authz, ctx) -> RecoveryAuthorizationAdmissionV1; ADMIT iff every binding holds; refusals AUTHZ.*; D9 REQUEST.PRECONDITION_FAILED except AUTHZ.RECIPE_CLOSURE_REVOKED -> EXTENSION.ADMISSION_REJECTED',
        'fullReference': {'grammar': '^security\\.repair-recovery-authorization\\.v1:[0-9a-f]{64}(?![\\s\\S])',
                          'recipe': "'security.repair-recovery-authorization.v1:' + C.identity('security.repair-recovery-authorization.v1', authz)  (foundation product H)",
                          'example': recovery_ref},
        'journalIdentity': {'function': 'S.repair_journal_identity(journal)', 'domain': S.JOURNAL_IDENTITY_DOMAIN, 'preimageKeys': list(S.JOURNAL_IDENTITY_KEYS),
                            'noncircular': 'excludes state, stagedPaths, appliedPaths, preimageBlobs, blockedPaths, restoreIntent, appliedSnapshotId, faultCause and recoveryAuthorizationRef; the same journal has one identity in every state',
                            'example': adm['journalRef']},
        'observedJournalState': {'function': 'S.repair_journal_state_digest(journal)', 'preimage': 'raw SHA-256 of canonical {state, stagedPaths, appliedPaths, preimageBlobs} as read under the EXCLUSIVE lease before any recovery write',
                                 'replay': 'single use: any successful recovery mutation changes state -> AUTHZ.JOURNAL_STATE_MOVED on replay; a crash/requires-broker before the first write leaves it unchanged -> the same authorization resumes inside its lifetime with a fresh recoveryExecutionId',
                                 'example': adm['journalStateDigest']},
        'trustedContextInputs': adm['trustedContextInputs'],
        'ctxExample': rctx,
        'authorizationExample': authz,
        'admissionExample': adm,
        'actionTable': {'securityRECOVERY_ACTION_FOR_STATE': S.RECOVERY_ACTION_FOR_STATE, 'terminalStatesAdmitNoMutation': ['COMMITTED', 'FAILED_CLEAN', 'FAILED_ROLLED_BACK', 'RECOVERY_BLOCKED'],
                        'integrationCheckToRetain': 'assert {st: row[0] for st,row in W.RECOVERY_TABLE.items() if row[0] in W.MUTATING_RECOVERY} == S.RECOVERY_ACTION_FOR_STATE'},
        'trustLaw': 'discard-temps / roll-back-renamed never consult recipe trust (a revoked recipe MUST still roll back); verify-postimages-and-commit re-consults it (revoked refuses first, not-admitted refuses)',
        'codexJoins': [
            'workflows/schemas/repair.schema.json RepairApplyJournalV1.recoveryAuthorizationRef: replace the free string with common#/$defs/RecoveryAuthorizationRef using the grammar above (full reference, never auth:<16hex>)',
            'workflows_model.v1.py repair_recover: take the admitted RecoveryAuthorizationAdmissionV1 projection (host-created after S.admit_recovery_authorization over the journal AS READ) instead of a caller dict; write the full reference into the journal; keep the closed recovery table and its preimage/postimage law unchanged',
            'integration-host-model.py: recovery_authorization_projection(authz, ctx, plan, journal, ref) mirroring repair_authorization_projection: validate_input RepairRecoveryAuthorizationV1, check ref == computed, bind ctx from the rehashed plan and the journal read under the lease, call S.admit_recovery_authorization',
            'public-detail-registry.v1.json: register the new AUTHZ.* details listed in handoff.json (owner security)',
            'command-inventory: repair-recover --apply-recovery takes the authorization PATH (or interactive consent) under authorizationClass exclusive-lease; inspection needs none'],
    },
    '2_installationTransition': {
        'issue': 'P10 / SHOULD-6: CoreTransitionIntentV1 admits only core-update|repair|rollback and no record names the journaled lease set',
        'intentContract': {'record': 'security-lifecycle.schemas.v1.json#/schemas/InstallationTransitionIntentV1',
                           'requiredFields': sorted(S.TRANSITION_INTENT_KEYS), 'operations': list(S.TRANSITION_OPERATIONS),
                           'semantics': 'S.admit_transition_intent(intent) -> [] or TRANSITION.* refusals: repair keeps closure/schema/store; update changes closure, never lowers schema, schema change selects a new store generation, same schema keeps it; rollback changes closure, never raises schema, needs the host-observed rollbackDeadline; store-migrate keeps the core closure, advances schema, new store generation; store-rollback keeps the core closure, retreats schema, re-selects the retained generation, needs the deadline',
                           'intentDigest': 'S.transition_intent_digest(intent) = raw SHA-256 of canonical intent = mutation step inputDescriptorDigest (S15)',
                           'workflowSchemaDelta': 'CoreTransitionIntentV1: operation enum += store-migrate, store-rollback; required += fromStoreGeneration, toStoreGeneration (uint64); keep the other nine fields; command inventory store-migrate/store-rollback carry this intent'},
        'journal': {'record': 'security-lifecycle.schemas.v1.json#/schemas/InstallationTransitionJournalV1', 'constructor': 'S.transition_journal_record(intent, registry) (state LEASED; written only after every lease is held)',
                    'admission': 'S.admit_transition_journal(journal, ctx) -> TransitionJournalAdmissionV1; journalRef = security.installation-transition-journal.v1:<H>',
                    'ctxKeys': tadm['trustedContextInputs'], 'scopeLaw': 'affects/leaseSet == S.core_transition_affected_namespaces(intent, frozen registry); a caller-chosen smaller set is TRANSITION.SCOPE_MISMATCH and TRANSITION.LEASE_SET_NOT_HELD',
                    'example': journal, 'admissionExample': tadm},
        'recovery': {'function': 'S.recover_transition_journal(journal, ctx) -> TransitionRecoveryV1', 'ctxKeys': ['namespaceRegistry', 'fenceHeld', 'leasesReacquired', 'storeFootprint'],
                     'table': {k: {'action': v[0], 'journalStateAfter': v[1], 'rationale': v[2]} for k, v in S.TRANSITION_RECOVERY_TABLE.items()},
                     'failClosed': 'registry differs -> QUARANTINE MIGRATION.CORRUPT; lease set not exactly re-acquired -> PROJECT.BUSY; no fence -> TRANSITION.FENCE_NOT_HELD; PREPARED store op without footprint -> QUARANTINE'},
        'leaseSchedule': 'lease_schedule op transition-journal {actor, namespaces}: JOURNALED only under the fence after core-transition-acquire of exactly that set',
        'codexJoins': ['integration-host-model.core_transition_scope: validate the successor intent, call S.admit_transition_intent, S.core_transition_affected_namespaces, then S.transition_journal_record/admit_transition_journal with the registry read under the fence',
                       'workflows: store-migrate/store-rollback commands bind the same intent; the invocation retains journalRef',
                       'public-detail-registry: TRANSITION.* details (owner security); D9 REQUEST.PRECONDITION_FAILED'],
    },
    '3_admittedBoundaryInventory': {
        'issue': 'P3: native discovery ignored security nestedRepositories/nestedProjects; Plan scope did not name them',
        'securityExport': 'S.boundary_inventory(discovery_result) -> AdmittedBoundaryInventoryV1 (relative scope paths; Reject unless status ACCEPT); shared implementation DD.boundary_inventory_from_provenance(provenance)',
        'nativeConsumption': 'N.discover_units(markers, explicit_roots, boundaries) / N.assign_membership(units, files, boundaries) / N.unit_scope_descriptor(units, ignore_paths, prefixes, pruned_trees, boundaries)',
        'inventoryExample': inv,
        'nativeOutputExample': {'units': [u['rootPath'] for u in nd['units']], 'boundaries': nd['boundaries'], 'prunedTrees': nd['prunedTrees']},
        'laws': ['boundaries.prunedTrees must equal the native-derived prunedTrees over the same marker inventory (native.boundary-inventory-mismatch otherwise): caller ignores are never proof of completeness',
                 'explicit root at/below a boundary: native.explicit-root-crosses-boundary (CONFIG.INVALID); security refuses the same join as JOIN_CROSSES_NESTED_*',
                 'boundaries=None is the standalone pure instrument only (boundaries.source = none with disclosure); an operational host composition must pass the security export'],
        'codexJoins': ['check-integration.py security-native-shared-unit-roots: feed S.boundary_inventory(sd) to N.discover_units and assert unit roots AND excludedUnits agree (the security sweep admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery does this over the P3 fixture)',
                       'integration-host-model: compose discovery -> boundary_inventory -> native discovery; convert absolute locators only through DD.relative_locator',
                       'public-detail-registry: native.explicit-root-crosses-boundary (CONFIG.INVALID), native.boundary-inventory-mismatch (REQUEST.PRECONDITION_FAILED)'],
    },
}
OUT.write_text(json.dumps(doc, indent=1) + '\n')
print('wrote', OUT)
