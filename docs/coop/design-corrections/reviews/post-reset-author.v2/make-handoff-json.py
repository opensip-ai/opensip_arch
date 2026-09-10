"""Generates handoff.json (post-reset author v2, Claude) from the corrected working tree: owned deltas, new schema records,
model functions, every new refusal/detail spelling enumerated from the model source, checks run and remaining joins."""
import json, re, importlib.util
from pathlib import Path

R = Path('/Users/sb/code/opensip-ai/opensip_arch'); H = Path('/tmp/opensip-design-corrections/post-reset-author.v2')
SEC = R / 'docs/coop/design-corrections/security'; NAT = R / 'docs/coop/design-corrections/native'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


S = load('sec', SEC / 'security_lifecycle_model_v1.py'); N = load('nat', NAT / 'native_evidence_model.v2.py')
src = (SEC / 'security_lifecycle_model_v1.py').read_text()
frozen_src = Path('/tmp/opensip-design-corrections/candidate-subject.v2/docs/coop/design-corrections/security/security_lifecycle_model_v1.py').read_text()
codes = lambda t: set(re.findall(r"'((?:AUTHZ|TRANSITION|PROJECT|GRANT|PLAN|MIGRATION)\.[A-Z_]+)", t))
new_security = sorted(codes(src) - codes(frozen_src))
frozen_native = Path('/tmp/opensip-design-corrections/candidate-subject.v2/docs/coop/design-corrections/native/native_evidence_model.v2.py').read_text()
new_native = sorted(set(re.findall(r'"(native\.[a-z-]+)"', (NAT / 'native_evidence_model.v2.py').read_text())) - set(re.findall(r'"(native\.[a-z-]+)"', frozen_native)))
sec_schemas = json.load(open(SEC / 'security-lifecycle.schemas.v1.json'))['schemas']
frozen_sec_schemas = json.load(open('/tmp/opensip-design-corrections/candidate-subject.v2/docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'))['schemas']
nat_defs = json.load(open(NAT / 'native-evidence.schemas.v2.json'))['$defs']
frozen_nat_defs = json.load(open('/tmp/opensip-design-corrections/candidate-subject.v2/docs/coop/design-corrections/native/native-evidence.schemas.v2.json'))['$defs']
sec_run = json.load(open(H / 'security-run4.json')); nat_run = json.load(open(H / 'native-run5.json')); probes = json.load(open(H / 'probes-v2.json'))
deltas = json.load(open(H / 'owned-file-deltas.json'))

doc = {
    'author': 'actual Claude, post-reset author session v2 (separate from the independent reviewer session 7d1caf68-2161-4824-979a-99da60d6f5be)',
    'standing': 'proposed design/reference corrections in the working tree; NOT committed, NOT pushed, NOT self-accepted; no product implementation; frozen candidate-subject.v2 untouched (manifest re-verified); pins, retained reports, registry, foundation/, workflows/, integration files, crosswalks, D-372 and readiness untouched',
    'inputs': ['/tmp/opensip-design-corrections/post-reset-review.v2/review.md + review.json (final; arrived during this session)', 'probes/independent-probes.{json,py} P3, P9, P10, P22', 'reviews/post-reset-author.v1/handoff.md', 'docs/coop/design-corrections/README.md'],
    'reviewerIssuesAddressed': {
        'N-1 / P3': 'admitted boundary inventory: security exports nested repositories/projects and custody exclusions; native consumes them; Plan scope names them; explicit root crossing refuses; standalone instrument discloses source=none',
        'N-4 / P9 / CX-01 / SHOULD-5': 'closed RepairRecoveryAuthorizationV1 + admit_recovery_authorization; noncircular journal identity; observed-state single use / crash resume; rollback never consults recipe trust, commit does',
        'N-5 / P10 / SHOULD-6': 'InstallationTransitionIntentV1 field/operation contract (5 operations incl. store migrate/rollback) + InstallationTransitionJournalV1 with exact lease set + admission + crash recovery; lease-schedule transition-journal op',
        'A-3 / P22': 'explicit Cargo workspace root keeps member folding and member target pruning; member selected alone is its own package unit',
        'A-4 (owned parts)': 'Config2 trailing-slash claim corrected in S3/native §1.4 and the fixture re-labelled as the CLI path; S14 singular EXCLUSIVE lease wording replaced by the lock set; /tmp citations in both contracts and READMEs replaced by repository paths; empty native-fix-handoff.v3.md removed from the native consumed-source list',
        'A-5': 'S3 and native §1.4 U-4a state that pruned trees receive no discovery/custody walk while read-set bytes from them are custody-checked by the snapshot reader and Plan-bound',
        'notAddressedNotMine': ['N-2 registry spellings (Codex; the new spellings below are listed for registration)', 'N-3 identity closure import correspondence (Codex/foundation)', 'A-1 analysisOperations vs preparedResolution (touches foundation semantic-grant schema; left for the next round, security admit_plan_execution_projection could take an operations argument)', 'A-2 integration consentSource (Codex)'],
    },
    'ownedFileDeltas': deltas,
    'newSecuritySchemaRecords': sorted(set(sec_schemas) - set(frozen_sec_schemas)),
    'newNativeSchemaDefs': sorted(set(nat_defs) - set(frozen_nat_defs)),
    'changedNativeSchemaDefs': ['UnitDiscoveryV1 (+boundaries)', 'FileMembershipRowV1 (membership +outside-project-boundary; reason +nested-repository, nested-project, custody-excluded)', 'UnitMembershipV1 (+outsideBoundaryFiles)'],
    'changedSecuritySchemaRecords': ['LeaseTraceV1 (trace op +transition-journal)', '$defs +RequestId, ExecutionId, JournalState, RecoveryAction, NamespaceList, StateSchema, TransitionOperation, TransitionRefusal, LogicalPath'],
    'newModelFunctions': {
        'security': ['boundary_inventory(result)', 'admit_recovery_authorization(authz, ctx)', 'repair_journal_identity(journal)', 'repair_journal_state_digest(journal)', 'admit_transition_intent(intent)', 'transition_intent_digest(intent)', 'registry_digest(registry)', 'transition_journal_record(intent, registry)', 'admit_transition_journal(journal, ctx)', 'recover_transition_journal(journal, ctx)', 'lease_schedule op transition-journal', 'core_transition_affected_namespaces: reselect also when fromStoreGeneration != toStoreGeneration', 'run_case models recovery-authorization | boundary-inventory | transition-intent | transition-journal | transition-recovery'],
        'discovery-defaults': ['relative_locator(root, absolute)', 'boundary_inventory_from_provenance(provenance)', 'classify_boundary(path, nestedRepositories, nestedProjects)', 'classify_custody_exclusion(dir, marker, custodyExcluded)', 'boundary_excluded_prefixes(inventory)', 'DISCOVERY_DEFAULTS_VERSION = 2'],
        'native': ['discover_units(markers, explicit_workspace_roots=None, boundaries=None)', 'assign_membership(units, files, boundaries=None)', 'unit_scope_descriptor(units, ignore_paths, explicit_path_prefixes=None, pruned_trees=None, boundaries=None)', 'D9_MAP +native.explicit-root-crosses-boundary (CONFIG.INVALID), +native.boundary-inventory-mismatch (REQUEST.PRECONDITION_FAILED)'],
    },
    'newRefusalSpellingsForRegistry': {'security (D9 per S12; TRANSITION.* -> REQUEST.PRECONDITION_FAILED via TRANSITION.REFUSED; AUTHZ.* as S10.1 except AUTHZ.RECIPE_CLOSURE_REVOKED)': new_security,
                                       'native': new_native,
                                       'parameterisedSuffixes': ['AUTHZ.RECOVERY_NOT_MUTATING:<state>', 'AUTHZ.JOURNAL_CONTEXT:<detail>', 'AUTHZ.REQUEST_ID_SHAPE:<field>', 'TRANSITION.OPERATION:<op>', 'TRANSITION.INTENT_FIELD_MISMATCH:<field>', 'TRANSITION.CLOSURE_SHAPE:<field>', 'TRANSITION.STATE_SCHEMA:<field>', 'TRANSITION.GENERATION_SHAPE:<field>', 'TRANSITION.INITIAL_STATE:<state>', 'TRANSITION.CONTEXT_INTENT:<intent refusal>']},
    'identityDomains': ['security.repair-recovery-authorization.v1 (RepairRecoveryAuthorizationV1; full reference = domain + ":" + H)', 'security.repair-apply-journal-identity.v1 (noncircular journal identity over JOURNAL_IDENTITY_KEYS)', 'security.installation-transition-journal.v1 (InstallationTransitionJournalV1)'],
    'checks': {
        'security (UNPINNED, pin gate bypassed)': {'report': str(H / 'security-run4.json'), 'passed': sec_run['passed'], 'counts': sec_run['counts'], 'sweeps': [(s['name'], s['holds']) for s in sec_run['sweeps']], 'schemasValidated': len(sec_run['schemasValidated']), 'baseline': '361/361, 8 sweeps (security-baseline.json)'},
        'native (UNPINNED)': {'report': str(H / 'native-run5.json'), 'result': nat_run['result'], 'cases': {k: nat_run['cases'][k] for k in ('total', 'passed', 'positive', 'negative')}, 'defs': nat_run['schemas']['defs'], 'openObjects': nat_run['schemas']['openObjects'], 'baseline': '93/93 (native-baseline.json)'},
        'author probes (UNPINNED)': {'report': str(H / 'probes-v2.json'), 'verdicts': {r['id']: r['verdict'] for r in probes['results']}},
        'pinnedRunsExpectedToFailAtPinGate': 'pins name Codex-owned files that changed earlier and now also the changed owned files; retained reports in the repo are the frozen bytes (unchanged)',
        'frozenCandidateV2': 'all manifest files re-verified byte-identical after this session',
    },
    'limitations': ['expectations are same-author, not an independent oracle', 'RECOVERY_ACTION_FOR_STATE mirrors the workflow RECOVERY_TABLE mutating rows (equality verified only in probes-v2.py; the integration checker must retain it)', 'the security checker now loads native_evidence_model.v2.py for the boundary sweep (cross-unit coupling; Codex to pin it)', 'no OS, lock, clock or crypto measurement; every ctx value is an asserted host observation'],
    'remainingJoins': [
        'workflows repair.schema.json: RepairApplyJournalV1.recoveryAuthorizationRef -> closed RecoveryAuthorizationRef grammar ^security\\.repair-recovery-authorization\\.v1:[0-9a-f]{64}(?![\\s\\S]); repair_recover consumes the host projection of admit_recovery_authorization (drop the auth:<16hex> mint); integration-host-model recovery projection; retain the action-table equality check',
        'workflows invocation-record.schema.json CoreTransitionIntentV1: operation enum += store-migrate, store-rollback; required += fromStoreGeneration, toStoreGeneration; integration-host-model.core_transition_scope -> admit_transition_intent + transition_journal_record/admit_transition_journal with the registry read under the fence; store-migrate/store-rollback commands bind the intent',
        'check-integration.py: compose S.boundary_inventory(sd) into N.discover_units on a nested-repository/nested-project fixture (security sweep already does); stop treating the marker inventory alone as the join',
        'public-detail-registry.v1.json: register the spellings in newRefusalSpellingsForRegistry (N-2 consolidation is Codex\'s call)',
        're-pin security/source-pins.v1.json (+ native_evidence_model.v2.py, discovery-defaults.py) and native/source-pins.v2.json (drop native-fix-handoff.v3.md); regenerate both retained reports; freeze a new subject; fresh independent review',
        'top-level README / crosswalk / post-reset dispositions: record N-1/N-4/N-5/A-3/A-4/A-5 dispositions and this handoff directory',
    ],
    'notClaimed': 'no acceptance, no product qualification, no OS/crypto measurement',
}
(H / 'handoff.json').write_text(json.dumps(doc, indent=1) + '\n')
print('new security spellings', len(new_security), new_security)
print('new native spellings', new_native)
print('new security records', doc['newSecuritySchemaRecords']); print('new native defs', doc['newNativeSchemaDefs'])
