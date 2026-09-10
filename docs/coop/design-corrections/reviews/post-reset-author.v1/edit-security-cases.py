"""Post-reset author (Claude) case-file edits for the security unit. All five files round-trip through
json.dumps(indent=2, ensure_ascii=False) + newline. Expected values are hand-authored from the contract text
(same author, not an independent oracle); digests recomputed with the model's own metadata canonicalizer."""
import copy, hashlib, importlib.util, json
from pathlib import Path
SEC = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security')
spec = importlib.util.spec_from_file_location('m', SEC / 'security_lifecycle_model_v1.py'); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
cs = importlib.util.spec_from_file_location('c', SEC.parent / 'foundation' / 'canonical.py'); C = importlib.util.module_from_spec(cs); cs.loader.exec_module(C)


def load(name):
    raw = (SEC / name).read_bytes(); doc = json.loads(raw)
    assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw, name
    return doc


def save(name, doc):
    (SEC / name).write_bytes((json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode())


RENAME = {'macos-arm64': 'macos-aarch64', 'linux-x86_64': 'linux-x86_64-gnu', 'linux-arm64': 'linux-aarch64-gnu'}


def rename_platform_keys(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            nk = RENAME.get(k, k) if k in RENAME else k
            out[nk] = rename_platform_keys(v)
        if 'platform' in out and out['platform'] in RENAME:
            out['platform'] = RENAME[out['platform']]
        return out
    if isinstance(node, list):
        return [rename_platform_keys(v) for v in node]
    return node


# ------------------------------------------------------------------ platform-admission-cases.v1.json (MUST-2)
pa = load('platform-admission-cases.v1.json')
pa = rename_platform_keys(pa)
pa['standing'] = pa['standing'].replace(
    'The four lanes named in the population',
    'The population is keyed by the ONE machine platform vocabulary (linux-aarch64-gnu, linux-x86_64-gnu, macos-aarch64, macos-x86_64; the same ids as RepoExecutionGrantV2.platformId, the native capability matrix and the workflow test-execution schema); the historical spellings macos-arm64 / linux-x86_64 / linux-arm64 are display aliases only and refuse when presented as a platform or used as a profile-set key. The four lanes named in the population')
for c in pa['cases']:
    if c['id'].startswith('linux-arm64-'):
        c['id'] = 'linux-aarch64-gnu-' + c['id'][len('linux-arm64-'):]
pa['cases'].extend([
    {'id': 'machine-id-admits-and-carries-its-display-alias-as-output-only',
     'input': {'profileSet': '$profileSet', 'observed': '$macos'},
     'expect': {'result': 'ADMIT', 'platform': 'macos-aarch64', 'displayAlias': 'macos-arm64', 'tier': 'EXACT-MEASURED'},
     'inputSchemas': {'profileSet': 'PlatformProfileSetV1'}, 'inputValid': True},
    {'id': 'display-alias-presented-as-the-platform-refuses-typed',
     'input': {'profileSet': '$profileSet', 'observed': {'$from': 'macos', 'platform': 'macos-arm64'}},
     'expect': {'result': 'REFUSE', 'platform': 'macos-arm64', 'displayAlias': None,
                'refusals': ['NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:macos-aarch64'],
                'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'EXTENSION.ADMISSION_REJECTED'}}},
    {'id': 'linux-display-alias-presented-as-the-platform-refuses-typed',
     'input': {'profileSet': '$profileSet', 'observed': {'$from': 'linux', 'platform': 'linux-x86_64'}},
     'expect': {'result': 'REFUSE', 'refusals': ['NT-TCB-PROFILE-UNQUALIFIED:platform-display-alias-not-machine-id:linux-x86_64-gnu']}},
    {'id': 'profile-set-keyed-by-a-display-alias-is-schema-invalid-and-refuses-before-any-predicate',
     'input': {'profileSet': '$profileSetAliasKeyed', 'observed': '$macos'},
     'expect': {'result': 'REFUSE', 'refusals': ['NT-TCB-PROFILE-UNQUALIFIED:PROFILE_SET_KEY_NOT_MACHINE_ID:macos-arm64']},
     'inputSchemas': {'profileSet': 'PlatformProfileSetV1'}, 'inputValid': False},
    {'id': 'every-machine-id-admits-under-the-same-profile-set-macos-x86_64',
     'input': {'profileSet': '$profileSet', 'observed': '$macosIntel'},
     'expect': {'result': 'ADMIT', 'platform': 'macos-x86_64', 'displayAlias': 'macos-x86_64', 'lane': 'macos-15-intel'}},
    {'id': 'every-machine-id-admits-under-the-same-profile-set-linux-x86_64-gnu',
     'input': {'profileSet': '$profileSet', 'observed': '$linux'},
     'expect': {'result': 'ADMIT', 'platform': 'linux-x86_64-gnu', 'displayAlias': 'linux-x86_64', 'lane': 'ubuntu-24.04'}},
])
alias_keyed = copy.deepcopy(pa['profileSet']['platforms']['macos-aarch64'])
pa['profileSetAliasKeyed'] = {'$from': 'profileSet', 'platforms': {'macos-arm64': alias_keyed}}
save('platform-admission-cases.v1.json', pa)

# ------------------------------------------------------------------ root-schema-cases.v1.json (MUST-2 profile-set bodies)
rs = load('root-schema-cases.v1.json')
old_digest = rs['envelope']['bodyDigest']
rs = rename_platform_keys(rs)
new_digest = M.metadata_sha('opensip.metadata.platform-profile-set.1', rs['envelope']['body'])
assert new_digest != old_digest
text = json.dumps(rs, indent=2, ensure_ascii=False).replace(old_digest, new_digest)
rs = json.loads(text)
assert rs['envelope']['bodyDigest'] == new_digest
save('root-schema-cases.v1.json', rs)
print('profile-set body digest', old_digest, '->', new_digest)

# ------------------------------------------------------------------ execution-principal-cases.v1.json (SHOULD-2, MUST-2)
ep = load('execution-principal-cases.v1.json')
ep['standing'] = ep['standing'].replace(
    'Every effect value must equal the security owner\'s platform truth table.',
    'Every effect value must equal the security owner\'s platform truth table. Admission is OPERATIONAL and precedes any Plan (post-reset review SHOULD-2): no Plan semantic-grant projection is an admission input; the Plan-time join is the separate `execution-projection` model (admit_plan_execution_projection) over the consumed preparation grants, and a test-runner grant (workflow test-execution step, no Plan) is projected by nothing. platformId uses the ONE machine vocabulary shared with S8; display aliases refuse.')
del ep['ctxBase']['semanticGrantPrincipals']
EMPTY_OWNERS_DIGEST = hashlib.sha256(C.canonical([])).hexdigest()
for c in ep['cases']:
    if 'refusals' in c.get('expect', {}):
        c['expect']['refusals'] = [r for r in c['expect']['refusals'] if r != 'GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED']
    if c['id'] == 'semantic-grant-projection-missing-the-principal-refuses':
        c['id'] = 'operational-grant-admits-without-any-plan-projection-preparation-precedes-analysis'
        c['input'] = {'grant': '$grant', 'ctx': '$ctx'}
        c['expect'] = {'result': 'ADMIT', 'semanticGrantIdentity': 'foundation semantic-grant (identity-and-evidence section 3), projected into plan2; distinct from securityGrantRef'}
        c['note'] = 'The ctx carries no semanticGrantPrincipals: preparation runs before the analysis Plan exists, so the projection cannot be an admission input. The Plan-time join is admit_plan_execution_projection (cases below).'
    if c['id'] == 'test-runner-with-snapshot-member-argv0-admits-for-workflow-owner':
        c['expect']['ownerBinding.snapshotOwners'] = []
        c['expect']['ownerBinding.dependencyClosureOwners'] = []
TEST_RUNNER = {'$from': 'grant', 'executionClass': 'test-runner', 'owners': [], 'dependencySourceSetId': None,
               'ownerSourceDigest': EMPTY_OWNERS_DIGEST, 'runner': {'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'}}
ep['cases'].extend([
    {'id': 'test-runner-grant-admits-with-no-plan-empty-owner-digest-is-bookkeeping-not-the-runner-binding',
     'input': {'grant': TEST_RUNNER, 'ctx': {'$from': 'ctx', 'ownerSourceDigest': EMPTY_OWNERS_DIGEST}},
     'expect': {'result': 'ADMIT', 'ownerBinding.runner': {'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'},
                'ownerBinding.snapshotOwners': [], 'ownerBinding.dependencyClosureOwners': [],
                'ownerBinding.toolClosureId': 'closure2:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'},
     'inputSchemas': {'grant': 'RepoExecutionGrantV2'}, 'inputValid': True,
     'note': 'ownerSourceDigest = raw SHA-256 of the canonical empty owner array (' + EMPTY_OWNERS_DIGEST + '): canonical empty-set bookkeeping keeping the record shape uniform. It binds no program; the runner is bound by runner + toolClosureId/snapshot membership + argvDigest (next case).'},
    {'id': 'test-runner-runner-outside-both-sealed-sets-refuses-although-the-empty-owner-digest-matches',
     'input': {'grant': dict(TEST_RUNNER, runner={'kind': 'toolchain-closure', 'member': 'bin/sh'}), 'ctx': {'$from': 'ctx', 'ownerSourceDigest': EMPTY_OWNERS_DIGEST}},
     'expect': {'result': 'REFUSE', 'refusals': ['GRANT.RUNNER_NOT_IN_TOOL_CLOSURE'],
                'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.PRECONDITION_FAILED'}}},
    {'id': 'a-ctx-projection-is-never-consulted-not-an-authority-condition',
     'input': {'grant': '$grant', 'ctx': {'$from': 'ctx', 'semanticGrantPrincipals': [{'kind': 'trusted-repository-code', 'closureId': 'closure2:0000000000000000000000000000000000000000000000000000000000000000', 'ownerSourceDigest': '0000000000000000000000000000000000000000000000000000000000000000'}]}},
     'expect': {'result': 'ADMIT'},
     'note': 'A projection supplied beside the grant (whether matching or, as here, foreign) changes nothing: it is not read. The integration host must not fabricate ctx.semanticGrantPrincipals from the grant; it derives the Plan requirement with semantic_projection_for_grants and checks it at Plan admission.'},
    {'id': 'platform-display-alias-in-grant-refuses-typed-and-is-schema-invalid',
     'input': {'grant': {'$from': 'grant', 'platformId': 'macos-arm64'}, 'ctx': '$ctx'},
     'expect': {'result': 'REFUSE', 'refusals': ['GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID:macos-aarch64'],
                'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.PRECONDITION_FAILED'}},
     'inputSchemas': {'grant': 'RepoExecutionGrantV2'}, 'inputValid': False},
    {'id': 'macos-x86_64-machine-id-admits-completing-the-four-platform-join',
     'input': {'grant': {'$from': 'grant', 'platformId': 'macos-x86_64'}, 'ctx': '$ctx'},
     'expect': {'result': 'ADMIT', 'effects.environment': 'ENFORCED-BY-CONSTRUCTION'},
     'inputSchemas': {'grant': 'RepoExecutionGrantV2'}, 'inputValid': True},
    # ---- Plan-time projection join (separate model)
    {'id': 'semantic-projection-for-grants-projects-preparation-grants-only-never-the-test-runner',
     'model': 'semantic-projection', 'outputSchema': 'SemanticProjectionV1',
     'input': {'grants': ['$grant', TEST_RUNNER]},
     'expect': {'principals': [{'kind': 'trusted-repository-code', 'closureId': 'closure2:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                'ownerSourceDigest': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'}]}},
    {'id': 'plan-projection-equal-to-the-consumed-preparation-grants-admits',
     'model': 'execution-projection', 'outputSchema': 'ExecutionProjectionAdmissionV1',
     'input': {'planPrincipals': [{'kind': 'first-party', 'closureId': 'closure2:0000000000000000000000000000000000000000000000000000000000000000', 'ownerSourceDigest': None},
                                  {'kind': 'trusted-repository-code', 'closureId': 'closure2:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 'ownerSourceDigest': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'}],
               'consumedGrants': ['$grant'], 'preparedResolution': 'host-prepared'},
     'expect': {'result': 'ADMIT', 'refusals': [], 'd9': None, 'requiredPrincipals.length': 1, 'testRunnerProjected': False}},
    {'id': 'plan-missing-a-consumed-preparation-grant-principal-refuses-at-plan-time',
     'model': 'execution-projection', 'outputSchema': 'ExecutionProjectionAdmissionV1',
     'input': {'planPrincipals': [{'kind': 'first-party', 'closureId': 'closure2:0000000000000000000000000000000000000000000000000000000000000000', 'ownerSourceDigest': None}],
               'consumedGrants': ['$grant'], 'preparedResolution': 'host-prepared'},
     'expect': {'result': 'REFUSE', 'refusals': ['PLAN.EXECUTION_PRINCIPAL_NOT_PROJECTED:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'],
                'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.PRECONDITION_FAILED'}}},
    {'id': 'plan-projecting-a-repository-code-principal-no-grant-backs-refuses-prepared-availability-implies-no-grant',
     'model': 'execution-projection', 'outputSchema': 'ExecutionProjectionAdmissionV1',
     'input': {'planPrincipals': [{'kind': 'trusted-repository-code', 'closureId': 'closure2:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 'ownerSourceDigest': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'}],
               'consumedGrants': [], 'preparedResolution': 'imported-inert'},
     'expect': {'result': 'REFUSE', 'refusals': ['PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff']}},
    {'id': 'test-runner-grant-is-never-a-consumed-plan-grant',
     'model': 'execution-projection', 'outputSchema': 'ExecutionProjectionAdmissionV1',
     'input': {'planPrincipals': [], 'consumedGrants': [TEST_RUNNER], 'preparedResolution': 'host-prepared'},
     'expect': {'result': 'REFUSE', 'refusals': ['PLAN.TEST_RUNNER_HAS_NO_PLAN', 'PLAN.HOST_PREPARED_WITHOUT_GRANT']}},
])
save('execution-principal-cases.v1.json', ep)

# ------------------------------------------------------------------ lease-cases.v1.json (SHOULD-6)
lc = load('lease-cases.v1.json')
lc['standing'] += (' Post-reset review SHOULD-6: every lease names a REGISTERED project namespace (`namespaceRegistry`; default ns-default); a core transition '
                   '(core update|repair|rollback, store migrate|rollback) holds the install-wide fence throughout and takes EXCLUSIVE on every AFFECTED registered '
                   'namespace in locator byte order, all-or-nothing and non-blocking (core-transition-acquire/release); the affected set is decided by '
                   'core_transition_affected_namespaces from the intent and the registry, never from user input or a directory listing.')
A = lambda actor, op, **kw: dict({'actor': actor, 'op': op}, **kw)
lc['cases'].extend([
    {'id': 'core-transition-holds-the-fence-throughout-and-takes-exclusive-on-every-registered-namespace-in-locator-order',
     'input': {'namespaceRegistry': ['ns-b', 'ns-a', 'ns-c'],
               'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=['ns-a', 'ns-b', 'ns-c']),
                           A('R', 'fence-acquire'), A('T', 'trust-write'), A('T', 'core-transition-release'), A('T', 'fence-release'),
                           A('R', 'fence-acquire'), A('R', 'lease', mode='SHARED-READ', namespace='ns-b'), A('R', 'fence-release')]},
     'expect': {'deadlockFree': True, 'trace.1.result': 'ACQUIRED-ALL:ns-a,ns-b,ns-c', 'trace.2.result': 'BLOCKED-BY:T',
                'trace.3.result': 'COMMITTED (readers see it via WAL snapshot; no reader is blocked)', 'trace.4.result': 'RELEASED-ALL:ns-c,ns-b,ns-a',
                'trace.7.result': 'ACQUIRED', 'final.fence': None, 'final.coreTransitions': {}, 'final.namespaces.ns-b.readers': ['R']}},
    {'id': 'core-transition-with-a-busy-namespace-is-all-or-nothing-releases-acquired-leases-and-reports-busy',
     'input': {'namespaceRegistry': ['ns-a', 'ns-b', 'ns-c'],
               'actions': [A('R', 'fence-acquire'), A('R', 'lease', mode='SHARED-READ', namespace='ns-b'), A('R', 'fence-release'),
                           A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=['ns-a', 'ns-b', 'ns-c']), A('T', 'fence-release')]},
     'expect': {'deadlockFree': True, 'trace.4.result': 'BUSY:ns-b:R (non-blocking; released ns-a; report PROJECT.BUSY, release the fence, retry outside the fence)',
                'trace.5.result': 'RELEASED', 'final.namespaces.ns-a.exclusive': None, 'final.namespaces.ns-c.exclusive': None, 'final.coreTransitions': {}}},
    {'id': 'core-transition-affecting-no-namespace-holds-the-fence-only-and-a-live-append-writer-continues',
     'input': {'namespaceRegistry': ['ns-a'],
               'actions': [A('W', 'fence-acquire'), A('W', 'lease', mode='APPEND-WRITE', namespace='ns-a'), A('W', 'fence-release'),
                           A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=[]), A('T', 'core-transition-release'), A('T', 'fence-release')]},
     'expect': {'deadlockFree': True, 'trace.4.result': 'ACQUIRED-ALL:no-namespace-affected', 'final.namespaces.ns-a.writer': 'W', 'final.fence': None}},
    {'id': 'core-transition-naming-an-unregistered-namespace-is-a-violation-negative',
     'input': {'namespaceRegistry': ['ns-a'],
               'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=['ns-a', 'ns-zzz'])]},
     'expect': {'deadlockFree': False, 'trace.1.result': 'REFUSED-UNREGISTERED-NAMESPACE:ns-zzz', 'violations': ['T names unregistered namespace(s) ns-zzz in a core transition']}},
    {'id': 'core-transition-lease-set-out-of-locator-order-is-refused-negative',
     'input': {'namespaceRegistry': ['ns-a', 'ns-b'],
               'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=['ns-b', 'ns-a'])]},
     'expect': {'deadlockFree': False, 'trace.1.result': 'REFUSED-LOCK-ORDER'}},
    {'id': 'releasing-the-fence-while-a-core-transition-holds-leases-is-a-violation-negative',
     'input': {'namespaceRegistry': ['ns-a'],
               'actions': [A('T', 'fence-acquire'), A('T', 'core-transition-acquire', namespaces=['ns-a']), A('T', 'fence-release')]},
     'expect': {'deadlockFree': False, 'trace.2.result': 'REFUSED-TRANSITION-HOLDS-LEASES', 'final.fence': 'T'}},
    {'id': 'lease-on-an-unregistered-namespace-is-refused-negative',
     'input': {'namespaceRegistry': ['ns-a'],
               'actions': [A('A', 'fence-acquire'), A('A', 'lease', mode='SHARED-READ', namespace='ns-arbitrary')]},
     'expect': {'deadlockFree': False, 'trace.1.result': 'REFUSED-UNREGISTERED-NAMESPACE'}},
    {'id': 'two-namespaces-are-independent-a-writer-in-one-never-blocks-a-writer-in-the-other',
     'input': {'namespaceRegistry': ['ns-a', 'ns-b'],
               'actions': [A('W1', 'fence-acquire'), A('W1', 'lease', mode='APPEND-WRITE', namespace='ns-a'), A('W1', 'fence-release'),
                           A('W2', 'fence-acquire'), A('W2', 'lease', mode='APPEND-WRITE', namespace='ns-b'), A('W2', 'fence-release')]},
     'expect': {'deadlockFree': True, 'trace.4.result': 'ACQUIRED', 'final.namespaces.ns-a.writer': 'W1', 'final.namespaces.ns-b.writer': 'W2'}},
    {'id': 'core-transition-scope-state-schema-change-affects-every-registered-namespace',
     'model': 'core-transition-scope', 'outputSchema': 'CoreTransitionScopeV1',
     'input': {'intent': {'operation': 'core-update', 'fromStateSchema': 1, 'toStateSchema': 2, 'reselectsStore': False}, 'namespaceRegistry': ['ns-b', 'ns-a']},
     'expect': {'affects': 'all-registered', 'namespaces': ['ns-a', 'ns-b']}},
    {'id': 'core-transition-scope-same-schema-core-update-affects-no-namespace-generations-stay-pinned',
     'model': 'core-transition-scope', 'outputSchema': 'CoreTransitionScopeV1',
     'input': {'intent': {'operation': 'core-update', 'fromStateSchema': 2, 'toStateSchema': 2, 'reselectsStore': False}, 'namespaceRegistry': ['ns-b', 'ns-a']},
     'expect': {'affects': 'none', 'namespaces': []}},
    {'id': 'core-transition-scope-core-repair-same-schema-affects-no-namespace',
     'model': 'core-transition-scope', 'outputSchema': 'CoreTransitionScopeV1',
     'input': {'intent': {'operation': 'core-repair', 'fromStateSchema': 2, 'toStateSchema': 2, 'reselectsStore': False}, 'namespaceRegistry': ['ns-a']},
     'expect': {'affects': 'none', 'namespaces': []}},
    {'id': 'core-transition-scope-rollback-always-affects-every-registered-namespace',
     'model': 'core-transition-scope', 'outputSchema': 'CoreTransitionScopeV1',
     'input': {'intent': {'operation': 'core-rollback', 'fromStateSchema': 2, 'toStateSchema': 2, 'reselectsStore': False}, 'namespaceRegistry': ['ns-a']},
     'expect': {'affects': 'all-registered', 'namespaces': ['ns-a']}},
    {'id': 'core-transition-scope-store-migrate-affects-every-registered-namespace',
     'model': 'core-transition-scope', 'outputSchema': 'CoreTransitionScopeV1',
     'input': {'intent': {'operation': 'store-migrate', 'fromStateSchema': 1, 'toStateSchema': 2, 'reselectsStore': True}, 'namespaceRegistry': []},
     'expect': {'affects': 'all-registered', 'namespaces': []}},
    {'id': 'core-transition-scope-unknown-operation-is-a-model-rejection',
     'model': 'core-transition-scope',
     'input': {'intent': {'operation': 'install', 'fromStateSchema': 1, 'toStateSchema': 1}, 'namespaceRegistry': ['ns-a']},
     'expectReject': 'CORE_TRANSITION_OPERATION:install'},
])
save('lease-cases.v1.json', lc)

# ------------------------------------------------------------------ discovery-cases.v1.json (MUST-3, ADV-3)
dc = load('discovery-cases.v1.json')
dc['standing'] += (' v3 (post-reset review MUST-3/ADV-3): ONE shared discovery rule (../discovery-defaults.py) prunes dependency trees (node_modules), VCS trees and Cargo build output '
                   '(`target` directly under a Cargo.toml directory) by exact path segment before any custody walk; installed package manifests are never units and never count toward '
                   'the 4096 first-party cap, which refuses typed (PROJECT.WORKSPACE_UNIT_LIMIT -> REQUEST.UNSATISFIABLE); explicit roots use the identity sentinel `.` with the same '
                   'normalization as the native unit instrument; a nested opensip.json is a deliberate project boundary in both directions.')


def D(path, uid=1000, mode='0755', vcs=None, gid=None):
    e = {'kind': 'dir', 'uid': uid, 'mode': mode, 'dev': 1}
    if vcs: e['vcs'] = True
    if gid is not None: e['gid'] = gid
    return path, e


def F(path, uid=1000, mode='0644'):
    return path, {'kind': 'file', 'uid': uid, 'mode': mode, 'nlink': 1, 'size': 100}


BASE = [D('/', uid=0), D('/home', uid=0), D('/home/alice', mode='0700')]


def fs_of(entries):
    return dict(BASE + entries)


R = '/home/alice/repo'
installed = fs_of([
    D(R, vcs=True), F(R + '/Cargo.toml'), F(R + '/package.json'),
    D(R + '/node_modules'), D(R + '/node_modules/left-pad'), F(R + '/node_modules/left-pad/package.json'),
    D(R + '/node_modules/lodash'), F(R + '/node_modules/lodash/package.json'),
    D(R + '/node_modules/rusty'), F(R + '/node_modules/rusty/Cargo.toml'),
    D(R + '/target'), D(R + '/target/debug'), D(R + '/target/debug/build'), F(R + '/target/debug/build/package.json'),
    D(R + '/packages'), D(R + '/packages/target'), F(R + '/packages/target/package.json'),
    D(R + '/packages/web'), F(R + '/packages/web/package.json'), D(R + '/packages/web/node_modules'), D(R + '/packages/web/node_modules/x'), F(R + '/packages/web/node_modules/x/package.json'),
    D(R + '/src'), D(R + '/src/target'), F(R + '/src/target/tsconfig.json'),
    D(R + '/docs'),
])
dc['cases'].extend([
    {'id': 'installed-dependencies-and-cargo-build-output-are-pruned-by-segment-legal-target-directories-stay-units',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R + '/src', 'fs': installed},
     'expect': {'status': 'ACCEPT', 'provenance.mode': 'vcs-default', 'provenance.unitSource': 'automatic',
                'provenance.units': [{'path': R, 'kind': 'workspace-auto', 'markers': ['Cargo.toml', 'package.json']},
                                     {'path': R + '/packages/target', 'kind': 'workspace-auto', 'markers': ['package.json']},
                                     {'path': R + '/packages/web', 'kind': 'workspace-auto', 'markers': ['package.json']},
                                     {'path': R + '/src/target', 'kind': 'workspace-auto', 'markers': ['tsconfig.json']}],
                'provenance.prunedTrees': [{'path': R + '/node_modules', 'reason': 'dependency-tree', 'markerCount': 3},
                                           {'path': R + '/packages/web/node_modules', 'reason': 'dependency-tree', 'markerCount': 1},
                                           {'path': R + '/target', 'reason': 'cargo-build-output', 'markerCount': 1}],
                'provenance.excludedUnits': [], 'provenance.nestedProjects': []},
     'note': 'packages/target and src/target are ordinary source directories: their parents hold no Cargo.toml. node_modules/rusty/Cargo.toml does not make a Cargo root. Four first-party units, three pruned trees, no cap pressure.'},
    {'id': 'config2-workspace-root-dot-names-the-admitted-root-under-the-shared-sentinel-normalization',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R + '/src', 'fs': installed, 'configWorkspaceRoots': ['.']},
     'expect': {'status': 'ACCEPT', 'provenance.unitSource': 'config-workspace-roots',
                'provenance.units': [{'path': R, 'kind': 'config-workspace-root', 'markers': ['Cargo.toml', 'package.json']}], 'provenance.warnings': []}},
    {'id': 'config2-workspace-root-with-trailing-slash-normalizes-like-the-native-instrument',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['packages/web/']},
     'expect': {'status': 'ACCEPT', 'provenance.units': [{'path': R + '/packages/web', 'kind': 'config-workspace-root', 'markers': ['package.json']}]}},
    {'id': 'explicit-root-without-a-language-marker-admits-custody-and-warns-the-language-layer-refuses-config-invalid',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['docs']},
     'expect': {'status': 'ACCEPT', 'provenance.units': [{'path': R + '/docs', 'kind': 'config-workspace-root', 'markers': []}],
                'provenance.warnings': ['EXPLICIT_ROOT_WITHOUT_LANGUAGE_MARKER:' + R + '/docs']},
     'note': 'Explicit roots are exact roots, never scan roots. Custody is admitted here; native discover_units refuses the same root as CONFIG.INVALID native.explicit-root-without-marker, so the invocation terminates typed with this provenance retained.'},
    {'id': 'explicit-root-inside-an-installed-dependency-tree-refuses',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['node_modules/left-pad']},
     'expect': {'status': 'REFUSE', 'refusal': 'PROJECT.EXPLICIT_PATH_INVALID', 'path': R + '/node_modules/left-pad',
                'detail': 'JOIN_INSIDE_PRUNED_TREE:dependency-tree:node_modules', 'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'CONFIG.INVALID'}}},
    {'id': 'explicit-root-inside-cargo-build-output-refuses-but-a-source-directory-called-target-is-admitted',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['target/debug']},
     'expect': {'status': 'REFUSE', 'refusal': 'PROJECT.EXPLICIT_PATH_INVALID', 'detail': 'JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target'}},
    {'id': 'explicit-root-source-directory-called-target-is-admitted',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['packages/target']},
     'expect': {'status': 'ACCEPT', 'provenance.units': [{'path': R + '/packages/target', 'kind': 'config-workspace-root', 'markers': ['package.json']}]}},
    {'id': 'explicit-root-empty-string-and-dot-segments-are-grammar-refusals',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': installed, 'configWorkspaceRoots': ['packages/./web']},
     'expect': {'status': 'REFUSE', 'refusal': 'PROJECT.EXPLICIT_PATH_INVALID', 'detail': 'JOIN_PATH_GRAMMAR'}},
])
# ADV-3: nested opensip.json as a deliberate project boundary, both directions
N = '/home/alice/mono'
nested = fs_of([
    D(N, vcs=True), F(N + '/Cargo.toml'), D(N + '/crates'), D(N + '/crates/core'), F(N + '/crates/core/Cargo.toml'),
    D(N + '/site'), F(N + '/site/opensip.json'), F(N + '/site/package.json'), D(N + '/site/src'),
    D(N + '/other'), D(N + '/other/deep'),
])
dc['cases'].extend([
    {'id': 'nested-config-inside-a-vcs-root-is-a-deliberate-project-boundary-launch-inside-selects-it',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': N + '/site/src', 'fs': nested},
     'expect': {'status': 'ACCEPT', 'provenance.mode': 'config', 'provenance.selectedRoot': N + '/site', 'provenance.configPath': N + '/site/opensip.json',
                'provenance.stopReason': 'CANDIDATE', 'provenance.units': [{'path': N + '/site', 'kind': 'workspace-auto', 'markers': ['package.json']}],
                'provenance.nestedProjects': []}},
    {'id': 'nested-config-inside-a-vcs-root-launch-elsewhere-selects-the-vcs-root-and-never-enters-the-nested-project',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': N + '/other/deep', 'fs': nested},
     'expect': {'status': 'ACCEPT', 'provenance.mode': 'vcs-default', 'provenance.selectedRoot': N, 'provenance.nestedProjects': [N + '/site'],
                'provenance.units': [{'path': N, 'kind': 'workspace-auto', 'markers': ['Cargo.toml']}, {'path': N + '/crates/core', 'kind': 'workspace-auto', 'markers': ['Cargo.toml']}],
                'provenance.excludedUnits': [{'path': N + '/site', 'reason': 'INSIDE_NESTED_PROJECT'}]},
     'note': 'The decision (ADV-3): a config file is an author-declared project boundary. It wins over the VCS root for launches inside it, and the enclosing VCS-root project treats it like a nested repository: recorded, never entered. Scope therefore depends on which project you launched in, never on which directory of one project.'},
    {'id': 'explicit-join-crossing-into-a-nested-project-refuses',
     'input': {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': N + '/other', 'fs': nested, 'explicitJoins': ['site/src']},
     'expect': {'status': 'REFUSE', 'refusal': 'PROJECT.EXPLICIT_PATH_INVALID', 'detail': 'JOIN_CROSSES_NESTED_PROJECT', 'path': N + '/site/src'}},
])
save('discovery-cases.v1.json', dc)
print('ok; empty owners digest', EMPTY_OWNERS_DIGEST)
