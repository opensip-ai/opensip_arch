"""Post-reset author v2 (Claude) scratch probes over the CORRECTED working tree (UNPINNED; pins are Codex's).
Re-runs the reviewer's P3, P9, P10 and P22 observations against the corrected bytes and checks the joins this author
cannot put into the repository (workflow recovery table equality; the reviewer's recovery-dict path). Writes probes-v2.json.
Nothing here is acceptance."""
import copy, json, importlib.util, traceback
from pathlib import Path

ROOT = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections')
OUT = Path(__file__).resolve().parent / 'probes-v2.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


C = load('canonical', ROOT / 'foundation/canonical.py')
S = load('sec', ROOT / 'security/security_lifecycle_model_v1.py')
N = load('nat', ROOT / 'native/native_evidence_model.v2.py')
W = load('wf', ROOT / 'workflows/workflows_model.v1.py')
DD = S.DD
results = []


def probe(pid, title, fn):
    try:
        verdict, ev = fn()
    except Exception as exc:
        verdict, ev = 'PROBE-ERROR', {'exception': repr(exc), 'trace': traceback.format_exc()[-1500:]}
    results.append({'id': pid, 'title': title, 'verdict': verdict, 'evidence': ev}); print(pid, verdict)


def synthetic_fs(root='/home/alice/repo'):
    return {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1},
            '/home/alice': {'kind': 'dir', 'uid': 1000, 'mode': '0700', 'dev': 1}, root: {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1, 'vcs': True},
            root + '/package.json': {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}}


def p3():
    """Reviewer's P3 fixture, now composed through the admitted boundary inventory."""
    fs = synthetic_fs(); R = '/home/alice/repo'
    d = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}; f = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    fs[R + '/vendor'] = dict(d); fs[R + '/vendor/lib'] = dict(d, vcs=True); fs[R + '/vendor/lib/package.json'] = dict(f); fs[R + '/vendor/lib/src'] = dict(d)
    fs[R + '/apps'] = dict(d); fs[R + '/apps/site'] = dict(d); fs[R + '/apps/site/opensip.json'] = dict(f); fs[R + '/apps/site/package.json'] = dict(f)
    fs[R + '/apps/site/sub'] = dict(d); fs[R + '/apps/site/sub/Cargo.toml'] = dict(f)
    sd = S.discovery({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs})
    inv = S.boundary_inventory(sd)
    markers = {p[len(R) + 1:]: {'sha256': '1' * 64} for p, e in fs.items() if p.startswith(R + '/') and e['kind'] == 'file' and p.rpartition('/')[2] in DD.WORKSPACE_MARKERS}
    nd = N.discover_units(markers, None, inv)
    alone = N.discover_units(markers)
    sroots = sorted(DD.relative_locator(R, u['path']) for u in sd['provenance']['units'])
    nroots = sorted({u['rootPath'] for u in nd['units']})
    scope = N.unit_scope_descriptor(nd['units'], [], None, nd['prunedTrees'], inv)
    mem = N.assign_membership(nd['units'], ['index.js', 'vendor/lib/src/x.js', 'apps/site/sub/src/lib.rs'], inv)
    ev = {'inventory': inv, 'securityUnits': sroots, 'nativeUnitsWithInventory': nroots, 'nativeExcludedUnits': nd['boundaries']['excludedUnits'],
          'nativeUnitsStandalone': sorted({u['rootPath'] for u in alone['units']}), 'standaloneSource': alone['boundaries']['source'],
          'scopeExcludedPrefixes': scope['scopeDescriptor']['excludedPathPrefixes'], 'outsideBoundaryFiles': mem['outsideBoundaryFiles'],
          'joinRefusals': {j: (S.discovery({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs, 'explicitJoins': [j]})['detail'],
                               N.discover_units(markers, [j], inv)['refused']['detail']) for j in ('apps/site', 'vendor/lib')}}
    return ('OK' if sroots == nroots == [''] and {'apps/site', 'vendor/lib'} <= set(ev['scopeExcludedPrefixes']) else 'COUNTEREXAMPLE'), ev


def p9():
    """Reviewer's P9: a caller dict is no longer the design; the security record is closed and admitted."""
    doc = C.parse((ROOT / 'security/repair-recovery-authorization-cases.v1.json').read_bytes())
    chk = load('chk', ROOT / 'security/check-security-lifecycle.v1.py')
    subs = chk.build_subs(doc)
    authz, ctx = subs['authorization'], subs['ctx']
    adm = S.admit_recovery_authorization(authz, ctx)
    S.validate_input('RepairRecoveryAuthorizationV1', authz)
    ref = 'security.repair-recovery-authorization.v1:' + C.identity('security.repair-recovery-authorization.v1', authz)
    # the workflow model's MUTATING rows must equal the security action table (Codex integration check to retain)
    wf_mutating = {st: row[0] for st, row in W.RECOVERY_TABLE.items() if row[0] in W.MUTATING_RECOVERY}
    # replay after rollback: state moved
    j2 = dict(ctx['journal'], state='FAILED_ROLLED_BACK')
    replay = S.admit_recovery_authorization(authz, dict(ctx, journal=j2))
    # commit under a revoked recipe refuses; rollback under a revoked recipe admits
    revoked = dict(ctx, recipeClosureId=ctx['revokedClosures'][0], admittedClosures=[])
    rb = S.admit_recovery_authorization(dict(authz, recipeClosureId=ctx['revokedClosures'][0]), revoked)
    ja = dict(ctx['journal'], state='APPLIED', appliedPaths=['src/a.ts', 'src/b.ts'])
    commit_authz = dict(authz, recipeClosureId=ctx['revokedClosures'][0], journalState='APPLIED', observedJournalStateDigest=S.repair_journal_state_digest(ja), recoveryAction='verify-postimages-and-commit')
    cm = S.admit_recovery_authorization(commit_authz, dict(revoked, journal=ja))
    # the current workflow bytes still accept the caller dict (Codex join pending): reproduce the reviewer's observation
    caller_dict_path = 'auth:' in (ROOT / 'workflows/workflows_model.v1.py').read_text()
    ev = {'admit': adm['result'], 'action': adm['action'], 'recipeTrustConsulted': adm['recipeTrustConsulted'], 'fullReference': ref, 'journalRef': adm['journalRef'],
          'identityNoncircular': S.repair_journal_identity(ctx['journal']) == S.repair_journal_identity(dict(ctx['journal'], state='COMMITTED', recoveryAuthorizationRef=ref)),
          'replayAfterRollback': replay['refusals'], 'rollbackUnderRevokedRecipe': rb['result'], 'commitUnderRevokedRecipe': (cm['result'], cm['refusals'], cm['d9']['code']),
          'workflowMutatingRows': wf_mutating, 'securityActionTable': S.RECOVERY_ACTION_FOR_STATE, 'tablesAgree': wf_mutating == S.RECOVERY_ACTION_FOR_STATE,
          'workflowStillMintsAuthPrefix(CodexJoinPending)': caller_dict_path}
    ok = adm['result'] == 'ADMIT' and ev['identityNoncircular'] and rb['result'] == 'ADMIT' and cm['result'] == 'REFUSE' and ev['tablesAgree']
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev


def p10():
    """Reviewer's P10: store migrate/rollback and the journaled lease set are now representable."""
    doc = C.parse((ROOT / 'security/transition-journal-cases.v1.json').read_bytes())
    chk = load('chk2', ROOT / 'security/check-security-lifecycle.v1.py')
    subs = chk.build_subs(doc)
    reg = ['ns-b', 'ns-a', 'ns-c']
    out = {}
    for name in ('intentUpdateSchemaChange', 'intentUpdateSameSchema', 'intentRepair', 'intentCoreRollback', 'intentStoreMigrate', 'intentStoreRollback'):
        it = subs[name]
        j = S.transition_journal_record(it, reg)
        S.validate_input('InstallationTransitionIntentV1', it); S.validate_input('InstallationTransitionJournalV1', j)
        ctx = {'intent': it, 'intentDigest': S.transition_intent_digest(it), 'namespaceRegistry': reg, 'fenceHeld': True, 'leasesHeld': j['leaseSet'],
               'currentStateSchema': it['fromStateSchema'], 'currentStoreGeneration': it['fromStoreGeneration'], 'currentCoreGeneration': it['preconditionGeneration'],
               'admittedTime': '2027-01-10T12:00:00Z'}
        adm = S.admit_transition_journal(j, ctx)
        out[name] = {'affects': j['affects'], 'leaseSet': j['leaseSet'], 'admit': adm['result'], 'refusals': adm['refusals']}
    smaller = S.admit_transition_journal(dict(S.transition_journal_record(subs['intentUpdateSchemaChange'], reg), leaseSet=['ns-a']),
                                         {'intent': subs['intentUpdateSchemaChange'], 'intentDigest': S.transition_intent_digest(subs['intentUpdateSchemaChange']), 'namespaceRegistry': reg,
                                          'fenceHeld': True, 'leasesHeld': ['ns-a'], 'currentStateSchema': 1, 'currentStoreGeneration': 3, 'currentCoreGeneration': 7, 'admittedTime': '2027-01-10T12:00:00Z'})
    tr = S.lease_schedule([{'actor': 't', 'op': 'fence-acquire'}, {'actor': 't', 'op': 'transition-journal', 'namespaces': ['ns-a', 'ns-b', 'ns-c']},
                           {'actor': 't', 'op': 'core-transition-acquire', 'namespaces': ['ns-a', 'ns-b', 'ns-c']}, {'actor': 't', 'op': 'transition-journal', 'namespaces': ['ns-a', 'ns-b', 'ns-c']}], reg)
    rec = S.recover_transition_journal(dict(S.transition_journal_record(subs['intentStoreMigrate'], reg), state='PREPARED'),
                                       {'namespaceRegistry': reg, 'fenceHeld': True, 'leasesReacquired': ['ns-a', 'ns-b', 'ns-c'],
                                        'storeFootprint': {'old': {'present': True, 'unbootstrappedReason': 'RESTORED'}, 'new': {'dir': 'migrating', 'state': 'PREPARED'}}})
    ev = {'perOperation': out, 'callerSmallerSet': smaller['refusals'], 'journalOpTrace': [(t['op'], t['result']) for t in tr['trace']],
          'crashPreparedStoreMigrate': (rec['action'], rec['fromStep'], rec['reacquire']),
          'workflowIntentEnumStill3(CodexJoinPending)': C.parse((ROOT / 'workflows/schemas/invocation-record.schema.json').read_bytes())['$defs']['CoreTransitionIntentV1']['properties']['operation']['enum']}
    ok = all(v['admit'] == 'ADMIT' for v in out.values()) and out['intentStoreMigrate']['affects'] == 'all-registered' and out['intentUpdateSameSchema']['leaseSet'] == [] \
        and 'TRANSITION.SCOPE_MISMATCH' in smaller['refusals'] and tr['trace'][1]['result'] == 'REFUSED-LEASE-SET-NOT-HELD' and tr['trace'][3]['result'].startswith('JOURNALED:')
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev


def p22():
    markers = {'Cargo.toml': {'sha256': '1' * 64, 'isCargoWorkspace': True}, 'crates/a/Cargo.toml': {'sha256': '1' * 64}, 'crates/b/Cargo.toml': {'sha256': '1' * 64}}
    auto = N.discover_units(markers); expl = N.discover_units(markers, ['.'])
    files = ['crates/a/src/lib.rs', 'crates/a/target/debug/x.rs', 'target/debug/y.rs']
    ma = N.assign_membership(auto['units'], files); me = N.assign_membership(expl['units'], files)
    ev = {'automaticMembers': [u['memberPackageRoots'] for u in auto['units']], 'explicitRootMembers': [u['memberPackageRoots'] for u in expl['units']],
          'automaticRows': {r['path']: r['reason'] for r in ma['rows']}, 'explicitRows': {r['path']: r['reason'] for r in me['rows']}}
    return ('OK' if ev['automaticRows'] == ev['explicitRows'] and ev['explicitRootMembers'] == [['crates/a', 'crates/b']] else 'COUNTEREXAMPLE'), ev


probe('P3', 'nested repository/project exclusion joins native unit discovery through the admitted boundary inventory', p3)
probe('P9', 'closed RepairRecoveryAuthorizationV1 with security admission; noncircular journal identity; safe rollback vs commit', p9)
probe('P10', 'InstallationTransitionJournalV1 represents store migrate/rollback and the exact lease set; caller cannot narrow; lease-schedule journal op', p10)
probe('P22', 'explicit Cargo workspace root keeps member folding and member target pruning', p22)
OUT.write_text(json.dumps({'standing': 'author scratch probes over the corrected working tree, UNPINNED; not acceptance', 'results': results}, indent=1, default=str) + '\n')
print('wrote', OUT)
