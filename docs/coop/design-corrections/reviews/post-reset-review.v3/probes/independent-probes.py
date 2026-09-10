"""Independent reviewer probes for frozen candidate-subject.v3.

Reviewer: fresh actual Claude session (started on claude-fable-5-1, interrupted by an
API 429 quota error with no verdict; resumed and completed on claude-opus-5).
Authored none of the subject bytes. Every probe is executable and reports OK / GAP /
COUNTEREXAMPLE with the exact observed values. Reference code runs over synthetic
fixtures only; signatures, OS observations, evaluator callbacks and pivot presences are
declared synthetic TCB inputs and are treated as such. Nothing here is product
qualification.

Run: /tmp/opensip-architecture-review-env/bin/python -I -B independent-probes.py
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
import traceback
from pathlib import Path

SCRATCH = Path('/tmp/opensip-design-corrections/post-reset-review.v3/scratch/docs/coop/design-corrections')
SNAP = Path('/tmp/opensip-design-corrections/candidate-subject.v3')
OUT = Path('/tmp/opensip-design-corrections/post-reset-review.v3/probes/independent-probes.json')

spec = importlib.util.spec_from_file_location('probe_host', SCRATCH / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
C, S, N, W = M.C, M.S, M.N, M.W
F = M.load('probe_fixtures', 'integration-fixtures.py')

results = []


def record(pid, title, status, detail):
    results.append({'id': pid, 'title': title, 'status': status, 'detail': detail})
    print('%-5s %-11s %s' % (pid, status, title))


def probe(pid, title):
    def deco(fn):
        try:
            status, detail = fn()
        except Exception as exc:  # a probe that dies is itself a finding
            status, detail = 'ERROR', {'exception': repr(exc), 'traceback': traceback.format_exc()[-2000:]}
        record(pid, title, status, detail)
        return fn
    return deco


def refuses(fn):
    """Return (True, reason) when fn() refuses, else (False, value)."""
    try:
        v = fn()
    except Exception as exc:
        return True, type(exc).__name__ + ': ' + str(exc)[:300]
    return False, repr(v)[:300]


CASES = C.parse((SCRATCH / 'workflows' / 'workflow-cases.v1.json').read_bytes())
SF = C.parse((SCRATCH / 'security' / 'execution-principal-cases.v1.json').read_bytes())
NF = C.parse((SCRATCH / 'native' / 'native-cases.v2.json').read_bytes())['fixtures']
RRF = C.parse((SCRATCH / 'security' / 'repair-recovery-authorization-cases.v1.json').read_bytes())
RAF = C.parse((SCRATCH / 'security' / 'repair-authorization-cases.v1.json').read_bytes())
TJF = C.parse((SCRATCH / 'security' / 'transition-journal-cases.v1.json').read_bytes())
REGISTRY = C.parse((SCRATCH / 'public-detail-registry.v1.json').read_bytes())
INVENTORY = C.parse((SCRATCH / 'workflows' / 'command-inventory.v1.json').read_bytes())


CONST = dict(CASES['constants'])
CONST['ARGV'] = W.raw_sha(C.canonical(['scripts/test.sh', '--ci']))
CONST['ARGV2'] = W.raw_sha(C.canonical(['/usr/bin/bash', '-c', 'rm -rf .']))
CONST['TOOL0#bin/node'] = CONST['TOOL0'] + '#bin/node'
CONST['ARGV4'] = W.raw_sha(C.canonical(['node', 'test.js']))
CONST['ARGV3'] = W.raw_sha(C.canonical(['bin/node', 'test.js']))


def sub(value):
    """Constant substitution equivalent to the unit checker's: keys, values and policyDoc references."""
    if isinstance(value, str) and value.startswith('$'):
        key = value[1:]
        if key in CONST:
            return CONST[key]
        if key in CASES['policyDocs']:
            return sub(CASES['policyDocs'][key])
        raise KeyError(value)
    if isinstance(value, dict):
        return {sub(k) if isinstance(k, str) and k.startswith('$') else k: sub(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sub(v) for v in value]
    return value


SUBBED = sub(CASES)
POL = SUBBED['policyDocs']
BS = SUBBED['baselineSpec']


def fixture_evidence(value, overrides=None):
    v = copy.deepcopy(value)
    v['imports'] = [{'kind': k, 'importId': (overrides or {}).get(k, CONST['IMP_RT'] if k == 'runtime' else CONST['IMP_HIST']),
                     'payloadDigest': CONST['H0'], 'sourceCorrespondenceDigest': CONST['H0'],
                     'scopeDigest': CONST['H0'], 'observationDigest': CONST['H0']} for k in v['importKinds']]
    return v


def make_baseline(policy, scope, waivers, rule_cov, project=None, evidence=None):
    run = {'authority': 'authoritative', 'availability': 'retained', 'snapshotId': CONST['SNAP0'], 'runId': CONST['RUN0']}
    ctx = {'detectorClosureIds': [d['closureId'] for d in BS['detectorClosure']],
           'evidenceAvailability': fixture_evidence(evidence or BS['evidenceAvailability'])}
    return W.adopt_baseline(run, CONST['PLAN0'], project or CONST['PRJ'], policy, scope, waivers, rule_cov,
                            BS['entries'], BS['detectorClosure'], BS['pivotClosure'], ctx, '1.0.0')


# ===================================================================== MUST/prior findings

@probe('P1', 'MUST-2 one machine platform vocabulary across every consumer')
def p1():
    gates = C.parse((SCRATCH / 'qualification-gates.proposed.json').read_bytes())
    matrix = C.parse((SCRATCH / 'native' / 'native-capability-matrix.v2.json').read_bytes())
    sets = {
        'security.PLATFORM_IDS': sorted(S.PLATFORM_IDS),
        'security.SUPPORTED_POPULATION': sorted(S.SUPPORTED_POPULATION),
        'security.PLATFORM_TRUTH_TABLE': sorted(S.PLATFORM_TRUTH_TABLE),
        'native.matrix.platformFamilies': sorted(matrix['platformFamilies']),
        'workflow.PLATFORMS': sorted(W.PLATFORMS),
        'gates.platformFamilies': sorted(gates['platformFamilies']),
    }
    one = len({tuple(v) for v in sets.values()}) == 1
    grant, ctx = copy.deepcopy(SF['grantBase']), copy.deepcopy(SF['ctxBase'])
    grant['platformId'] = S.PLATFORM_DISPLAY_ALIASES['macos-aarch64']
    alias = S.admit_repo_execution_grant(grant, ctx)
    alias_refused = any(x.startswith('GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID') for x in alias['refusals'])
    g13 = C.parse((SCRATCH / 'foundation' / 'g13-result-schema.v5.json').read_bytes())
    g13_scoped = 'harness.DR-G13' in json.dumps(g13)
    ok = one and alias_refused and g13_scoped
    return ('OK' if ok else 'GAP'), {'sets': sets, 'oneVocabulary': one,
                                     'displayAliasRefused': alias_refused, 'aliasRefusals': alias['refusals'],
                                     'g13SchemaScopedHistorical': g13_scoped}


@probe('P2', 'MUST-3 zero-config discovery: dependency pruning, typed cap, exact 4096')
def p2():
    installed = N.synthetic_marker_set(0, 4200)
    firstparty = N.synthetic_marker_set(4200, 0, root_marker=False)
    exact = N.synthetic_marker_set(4096, 0, root_marker=False)
    a = N.discover_units(installed)
    b = N.discover_units(firstparty)
    c = N.discover_units(exact)
    e_installed = S.DD.enumerate_units(installed)
    e_first = S.DD.enumerate_units(firstparty)
    keeps_target = S.DD.classify_path('packages/target/index.ts', {''}) is None
    prunes_target = S.DD.classify_path('target/debug/x.rs', {''}) == ('target', 'cargo-build-output')
    ok = (len(a['units']) == 1 and a['prunedTrees'] == [{'path': 'node_modules', 'reason': 'dependency-tree', 'markerCount': 4200}]
          and b['refused'] is not None and b['refused']['detail'] == 'native.too-many-units'
          and b['refused']['d9']['exitCode'] == 2 and len(c['units']) == 4096
          and e_installed['refusal'] is None and e_first['refusal']['detail'] == 'WORKSPACE_UNIT_LIMIT'
          and keeps_target and prunes_target)
    return ('OK' if ok else 'GAP'), {'installedUnits': len(a['units']), 'prunedTrees': a['prunedTrees'],
                                     'firstPartyRefusal': b['refused'] and {k: v for k, v in b['refused'].items() if k != 'd9'},
                                     'firstPartyD9': b['refused'] and b['refused']['d9'],
                                     'exactCapUnits': len(c['units']),
                                     'sharedRuleKeepsPackagesTarget': keeps_target, 'sharedRulePrunesCargoTarget': prunes_target}


def boundary_fixture():
    """The v2 P3 shape: one nested repository (vendor/lib) and one nested project (apps/site)."""
    disc_case = next(c for c in C.parse((SCRATCH / 'security' / 'discovery-cases.v1.json').read_bytes())['cases']
                     if c['id'].startswith('installed-dependencies-and-cargo-build-output'))
    inp = copy.deepcopy(disc_case['input'])
    root = '/home/alice/repo'
    d = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}
    f = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    for p in ('apps', 'apps/site', 'apps/site/sub', 'vendor', 'vendor/lib'):
        inp['fs'][root + '/' + p] = dict(d)
    inp['fs'][root + '/vendor/lib']['vcs'] = True
    for p in ('apps/site/opensip.json', 'apps/site/package.json', 'apps/site/sub/Cargo.toml',
              'apps/site/main.ts', 'vendor/lib/package.json', 'vendor/lib/index.ts', 'main.ts'):
        inp['fs'][root + '/' + p] = dict(f)
    files = [p[len(root) + 1:] for p, row in inp['fs'].items() if p.startswith(root + '/') and row['kind'] == 'file']
    markers = {p: {'sha256': '1' * 64} for p in files if p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}
    return inp, markers, files, root


@probe('P3', 'N-1 nested repository/project boundary reaches native units, membership, scope and capture')
def p3():
    inp, markers, files, root = boundary_fixture()
    joined = M.admit_repository_discovery(inp, markers, files)
    sec = joined['discovery']['provenance']
    sec_roots = {u['path'][len(root) + 1:] if u['path'] != root else '' for u in sec['units']}
    nat_roots = {u['rootPath'] for u in joined['native']['units']}
    excluded = {r['path']: r['reason'] for r in joined['native']['boundaries']['excludedUnits']}
    outside = joined['membership']['outsideBoundaryFiles']
    # a standalone native instrument over the same markers still sees the nested trees
    standalone = {u['rootPath'] for u in N.discover_units(markers)['units']}
    ok = (sec_roots == nat_roots
          and joined['boundaries']['nestedProjects'] == ['apps/site']
          and joined['boundaries']['nestedRepositories'] == ['vendor/lib']
          and excluded == {'apps/site': 'nested-project', 'apps/site/sub': 'nested-project', 'vendor/lib': 'nested-repository'}
          and sorted(outside) == sorted(p for p in files if p.startswith(('apps/site/', 'vendor/lib/')))
          and {'apps/site', 'vendor/lib'} <= set(joined['scope']['scopeDescriptor']['excludedPathPrefixes'])
          and not any(p.startswith(('apps/site/', 'vendor/lib/')) for p in joined['sourceCaptureCandidates'])
          and standalone > nat_roots)
    subst = refuses(lambda: M.admit_repository_discovery(inp, dict(markers, **{'foreign/package.json': {'sha256': '2' * 64}}), files))
    inside = copy.deepcopy(inp)
    inside['cwd'] = root + '/apps/site'
    ifiles = ['package.json', 'sub/Cargo.toml', 'main.ts', 'opensip.json']
    ij = M.admit_repository_discovery(inside, {p: {'sha256': '1' * 64} for p in ifiles if p.rpartition('/')[2] in S.DD.WORKSPACE_MARKERS}, ifiles)
    inside_ok = ij['discovery']['provenance']['selectedRoot'] == root + '/apps/site' and ij['boundaries']['nestedProjects'] == []
    return ('OK' if ok and subst[0] and inside_ok else 'GAP'), {
        'securityUnitRoots': sorted(sec_roots), 'nativeUnitRoots': sorted(nat_roots),
        'standaloneNativeRootsWithoutInventory': sorted(standalone),
        'excludedUnits': excluded, 'outsideBoundaryFiles': sorted(outside),
        'scopeExcludedPathPrefixes': joined['scope']['scopeDescriptor']['excludedPathPrefixes'],
        'sourceCaptureCandidates': joined['sourceCaptureCandidates'],
        'substitutedInventoryRefused': subst, 'launchInsideNestedConfigSelectsIt': inside_ok}


@probe('P4', 'N-2/MUST-1 one public detail code per shared condition; registry/schema parity')
def p4():
    common = C.parse((SCRATCH / 'workflows' / 'schemas' / 'common.schema.json').read_bytes())
    enum = set(common['$defs']['DomainDetailCode']['enum'])
    codes = {r['code'] for r in REGISTRY['records']}
    aliases = {r['internalCode']: r['publicCode'] for r in REGISTRY['internalAliases']}
    cap = {M.public_termination(S.d9('PROJECT.WORKSPACE_UNIT_LIMIT'), i, 'narrow the workspace')['domainDetail']['code']
           for i in ('PROJECT.WORKSPACE_UNIT_LIMIT', 'WORKSPACE_UNIT_LIMIT', 'native.too-many-units')}
    root = {M.public_termination(S.d9('PROJECT.EXPLICIT_PATH_INVALID'), i, 'use a canonical relative root')['domainDetail']['code']
            for i in ('PROJECT.EXPLICIT_PATH_INVALID', 'native.explicit-root-grammar')}
    unreg = refuses(lambda: M.public_termination(S.d9('GRANT.REFUSED'), 'native.invented-code', 'x'))
    alias_public = [a for a in aliases if a in enum]
    dead = [c for c in ('GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED', 'STORAGE.BACKUP_CHOICE_REQUIRED',
                        'provider-unavailable/capability-missing') if c in enum]
    sec_covered = {aliases.get(c, c) for c in S.D9} <= codes
    nat_covered = {aliases.get(c, c) for c in N.D9_MAP} <= codes
    ok = (enum == codes and cap == {'PROJECT.WORKSPACE_UNIT_LIMIT'} and root == {'PROJECT.EXPLICIT_PATH_INVALID'}
          and unreg[0] and not alias_public and not dead and sec_covered and nat_covered)
    return ('OK' if ok else 'GAP'), {'registryRecords': len(codes), 'schemaEnum': len(enum), 'parity': enum == codes,
                                     'capProjections': sorted(cap), 'rootGrammarProjections': sorted(root),
                                     'internalAliases': aliases, 'aliasesAdmittedPublicly': alias_public,
                                     'deadCodesStillPublic': dead, 'unregisteredRefused': unreg,
                                     'securityDetailsCovered': sec_covered, 'nativeDetailsCovered': nat_covered}


@probe('P5', 'N-3/CX-07 Run closure parses retained import source correspondence and declared build context')
def p5():
    ok_exact = M.N.IM.close_run(*F.graph_with_import()).startswith('run2:')
    ok_vcs = M.N.IM.close_run(*F.graph_with_import(correspondence='vcs')).startswith('run2:')
    ok_build = M.N.IM.close_run(*F.graph_with_import(correspondence='vcs', build_identity='build-a',
                                                     declared_builds=['build-a'])).startswith('run2:')
    negatives = {}
    for label, kw in [('foreignExactSnapshot', {}),
                      ('foreignVcsSnapshot', {'correspondence': 'vcs', 'foreign_snapshot': True}),
                      ('mappingDigestMismatch', {'correspondence': 'vcs', 'bad_mapping': True}),
                      ('dirtyWorktree', {'correspondence': 'vcs', 'dirty': True}),
                      ('mappingAbsent', {'correspondence': 'vcs', 'missing_mapping': True}),
                      ('declaredBuildWithNoExpectedContext', {'correspondence': 'vcs', 'build_identity': 'build-a'}),
                      ('declaredBuildOutsideExpectedSet', {'correspondence': 'vcs', 'build_identity': 'build-a',
                                                           'declared_builds': ['build-b']})]:
        if label == 'foreignExactSnapshot':
            negatives[label] = refuses(lambda: M.N.IM.close_run(*F.graph_with_import(foreign_snapshot=True)))
        else:
            negatives[label] = refuses(lambda k=kw: M.N.IM.close_run(*F.graph_with_import(**k)))
    # the importer cannot nominate its own expected build labels: the parameter is an analysis-spec row
    schema = C.parse((SCRATCH / 'foundation' / 'import-source-context.schema.json').read_bytes())
    declared_only = set(schema['properties']) == {'schemaVersion', 'declaredBuildIds'} and schema['additionalProperties'] is False
    ok = ok_exact and ok_vcs and ok_build and all(v[0] for v in negatives.values()) and declared_only
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'exactSnapshotCloses': ok_exact, 'mappedVcsCloses': ok_vcs,
                                                'declaredBuildInExpectedSetCloses': ok_build,
                                                'negatives': negatives, 'contextSchemaClosed': declared_only}


@probe('P6', 'N-4 repair recovery authorization -> workflow mutation join')
def p6():
    rs = sub(copy.deepcopy(CASES['repairScenario']))
    tree = {k: v.encode() for k, v in rs['tree'].items()}
    project = CASES['constants']['PRJ']
    run = rs['run']
    run['snapshotId'] = W.fixture_tree_snapshot_id(project, tree)
    edits = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e) for e in rs['edits']]
    trust = {rs['recipe']['closureId']: 'admitted'}
    plan = W.repair_preview(project, tree, run, rs['recipe'], rs['targets'], edits,
                            rs['evidenceRequirements'], rs['permittedScope'], trust)
    auth = copy.deepcopy(RAF['authorizationBase'])
    auth.update(projectId=project, repairPlanId=plan['repairPlanId'],
                baseSnapshotId=plan['descriptor']['snapshotId'], recipeClosureId=rs['recipe']['closureId'])
    actx = copy.deepcopy(RAF['ctxBase'])
    actx['admittedClosures'] = list(trust)
    aref = 'security.repair-apply-authorization.v1:' + C.identity('security.repair-apply-authorization.v1', auth)
    proj = M.repair_authorization_projection(auth, actx, plan, aref)
    postimages = {e['path']: e['postimage'] for e in edits if e.get('postimage') is not None}
    journal, receipt, after = W.repair_apply(plan, postimages, tree, project, CASES['constants']['REQ'], 2,
                                             proj, False, 'interactive', {}, trust, {})
    applied = dict(journal, state='APPLIED')
    applied.pop('appliedSnapshotId', None)
    ctx = copy.deepcopy(RRF['ctxBase'])
    ctx.update(projectId=project, admittedClosures=list(trust), revokedClosures=[])
    ra = copy.deepcopy(RRF['authorizationBase'])
    ra.update(projectId=project, repairPlanId=plan['repairPlanId'], baseSnapshotId=plan['descriptor']['snapshotId'],
              recipeClosureId=rs['recipe']['closureId'], journalRef=S.repair_journal_identity(applied),
              journalState='APPLIED', observedJournalStateDigest=S.repair_journal_state_digest(applied),
              recoveryAction='verify-postimages-and-commit', originalRequestId=applied['requestId'],
              recoveryRequestId='req1_' + '8' * 32, recoveryExecutionId='exec1_' + '8' * 32)
    ctx.update(recoveryRequestId=ra['recoveryRequestId'], recoveryExecutionId=ra['recoveryExecutionId'], journal=applied)

    def ref(a):
        return S.RECOVERY_AUTHZ_DOMAIN + ':' + C.identity(S.RECOVERY_AUTHZ_DOMAIN, a)

    def intent(a):
        return {'schemaVersion': 1, 'kind': 'repair-recover', 'journalRef': a['journalRef'],
                'repairPlanId': a['repairPlanId'], 'recoveryAction': a['recoveryAction'], 'authorizationRef': ref(a)}

    def project_authz(a=None, c=None, j=None):
        a = a or ra
        c = dict(ctx, **(c or {}))
        j = j or applied
        return M.recovery_authorization_projection(a, c, plan, j, ref(a), intent(a))

    good = project_authz()
    out = W.repair_recover(applied, plan, after, project, {}, good)
    committed = out[0]['state'] == 'COMMITTED' and out[0]['recoveryAuthorizationRef'] == ref(ra)
    # negatives
    neg = {}
    neg['expiredAuthority'] = refuses(lambda: project_authz(c={'admittedTime': '2028-01-10T12:00:00Z'}))
    neg['journalStateMoved'] = refuses(lambda: project_authz(j=dict(applied, state='INDETERMINATE')))
    neg['foreignProject'] = refuses(lambda: project_authz(c={'projectId': 'prj1-' + '9' * 64}))
    neg['revokedRecipeOnCommit'] = refuses(lambda: project_authz(c={'revokedClosures': list(trust)}))
    neg['ciWithInteractiveConsent'] = refuses(lambda: project_authz(c={'ci': True}))
    neg['reusedOriginalExecution'] = refuses(lambda: project_authz(
        a=dict(ra, recoveryExecutionId=applied['executionId']), c={'recoveryExecutionId': applied['executionId']}))
    neg['freshExecutionAfterCrashNeedsFreshGrant'] = refuses(lambda: project_authz(c={'recoveryExecutionId': 'exec1_' + '9' * 32}))
    neg['custodyNotReAdmitted'] = refuses(lambda: project_authz(c={'custodyAdmitted': False}))
    neg['policyDoesNotAdmitRepair'] = refuses(lambda: project_authz(c={'policyAdmitsRepair': False}))
    neg['forgedReference'] = refuses(lambda: M.recovery_authorization_projection(ra, ctx, plan, applied, ref(ra) + '0', intent(ra)))
    neg['callerDictProjection'] = refuses(lambda: W.repair_recover(
        applied, plan, after, project, {}, {'repairPlanId': plan['repairPlanId'], 'requestId': applied['requestId']}))
    neg['terminalStateNotMutating'] = S.admit_recovery_authorization(
        dict(ra, journalState='COMMITTED'), dict(ctx, journal=dict(applied, state='COMMITTED')))['refusals']
    # safe rollback proceeds under a revoked recipe; commit does not
    rb_journal = dict(applied, state='APPLYING')
    rb = dict(ra, journalState='APPLYING', observedJournalStateDigest=S.repair_journal_state_digest(rb_journal),
              recoveryAction='roll-back-renamed')
    rb_proj = project_authz(a=rb, c={'revokedClosures': list(trust), 'admittedClosures': []}, j=rb_journal)
    preimages = {W.raw_sha(v): v for v in tree.values()}
    rb_out = W.repair_recover(rb_journal, plan, after, project, preimages, rb_proj)
    rolled_back = rb_out[0]['state'] == 'FAILED_ROLLED_BACK' and rb_out[0]['_tree'] == tree
    tables_equal = ({k: v[0] for k, v in W.RECOVERY_TABLE.items() if v[0] in W.MUTATING_RECOVERY}
                    == S.RECOVERY_ACTION_FOR_STATE)
    bindings_equal = W.recovery_journal_bindings(applied) == (S.repair_journal_identity(applied),
                                                              S.repair_journal_state_digest(applied))
    # journal identity is noncircular: it must not move when recovery writes its own reference
    with_ref = dict(applied, recoveryAuthorizationRef=ref(ra))
    noncircular = S.repair_journal_identity(with_ref) == S.repair_journal_identity(applied)
    ok = (committed and rolled_back and tables_equal and bindings_equal and noncircular
          and all(v[0] for k, v in neg.items() if k != 'terminalStateNotMutating')
          and any(x.startswith('AUTHZ.RECOVERY_NOT_MUTATING') for x in neg['terminalStateNotMutating']))
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'commitRecoveryAdmitted': committed,
                                                'rollbackUnderRevokedRecipe': rolled_back,
                                                'actionTablesIdentical': tables_equal,
                                                'journalPreimagesIdentical': bindings_equal,
                                                'journalIdentityNoncircular': noncircular, 'negatives': neg}


@probe('P7', 'N-5/CX-06 five installation operations: intent, journal, scope, durable revisions, recovery')
def p7():
    per_op, neg = {}, {}
    for key in ('UpdateSchemaChange', 'UpdateSameSchema', 'Repair', 'CoreRollback', 'StoreMigrate', 'StoreRollback'):
        intent = TJF['records']['intent' + key]
        journal = S.transition_journal_record(intent, TJF['ctxBase']['namespaceRegistry'])
        ctx = dict(TJF['ctxBase'], currentStateSchema=intent['fromStateSchema'],
                   currentStoreGeneration=intent['fromStoreGeneration'],
                   currentCoreGeneration=intent['preconditionGeneration'], leasesHeld=journal['leaseSet'])
        adm = M.admit_installation_transition(intent, journal, ctx)
        rctx = dict(TJF['rctx'], leasesReacquired=journal['leaseSet'])
        history = [dict(journal, state=st) for st in ('LEASED', 'PREPARING', 'PREPARED', 'COMMITTED', 'DONE')]
        refs = M.installation_journal_history(intent, history)
        crash = M.recover_installation_transition(journal, adm['journalRef'], rctx)
        committed = dict(journal, state='COMMITTED')
        cref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, committed)
        finish = M.recover_installation_transition(committed, cref, rctx)
        # the workflow intent schema must admit the same closed record
        wf_admits = refuses(lambda i=intent: W.validate_import_record(
            'workflows/schemas/invocation-record.schema.json', '#/$defs/CoreTransitionIntentV1', i))[0] is False
        per_op[key] = {'operation': intent['operation'], 'affects': journal['affects'], 'leaseSet': journal['leaseSet'],
                       'admitted': adm['result'], 'durableRevisions': len(set(refs)),
                       'crashAtLeased': crash['action'], 'crashAtCommitted': finish['action'],
                       'workflowSchemaAdmitsIntent': wf_admits,
                       'intentDigestIsMutationInputDescriptor': journal['intentDigest'] == S.transition_intent_digest(intent)}
        if journal['leaseSet']:
            neg['scopeNarrowedByCaller.' + key] = refuses(
                lambda i=intent, j=journal, c=ctx: M.admit_installation_transition(i, dict(j, leaseSet=[], affects='none'), c))
        else:
            neg['scopeWidenedByCaller.' + key] = refuses(
                lambda i=intent, j=journal, c=ctx: M.admit_installation_transition(
                    i, dict(j, leaseSet=list(TJF['ctxBase']['namespaceRegistry']), affects='all-registered'), c))
        wrong = dict(journal, intentDigest='0' * 64)
        wref = S.TRANSITION_JOURNAL_DOMAIN + ':' + C.identity(S.TRANSITION_JOURNAL_DOMAIN, wrong)
        neg['recoveryRehashesIntent.' + key] = refuses(lambda w=wrong, r=wref, c=rctx: M.recover_installation_transition(w, r, c))
        neg['journalRefBoundToState.' + key] = refuses(
            lambda j=committed, r=adm['journalRef'], c=rctx: M.recover_installation_transition(j, r, c))
        neg['historySkipsState.' + key] = refuses(lambda i=intent, h=history: M.installation_journal_history(i, [h[0], h[-1]]))
        if journal['leaseSet']:
            neg['incompleteLocks.' + key] = refuses(
                lambda i=intent, j=journal, c=ctx: M.admit_installation_transition(i, j, dict(c, leasesHeld=[])))
            per_op[key]['busyOnPartialReacquire'] = M.recover_installation_transition(
                journal, adm['journalRef'], dict(rctx, leasesReacquired=[]))['action']
        per_op[key]['registryChangeQuarantines'] = M.recover_installation_transition(
            journal, adm['journalRef'], dict(rctx, namespaceRegistry=['foreign']))['action']
    ops = {v['operation'] for v in per_op.values()}
    total = set(S.TRANSITION_OPERATIONS) == ops
    admitted = all(v['admitted'] == 'ADMIT' and v['workflowSchemaAdmitsIntent'] and v['durableRevisions'] == 5
                   and v['crashAtLeased'] == 'ABORT' and v['crashAtCommitted'] == 'RESUME-COMMIT'
                   and v['registryChangeQuarantines'] == 'QUARANTINE'
                   and v['intentDigestIsMutationInputDescriptor'] for v in per_op.values())
    # totality of the intent admission over every operation x schema x store combination
    base = TJF['records']['intentUpdateSchemaChange']
    combos, unclassified = 0, []
    for op in S.TRANSITION_OPERATIONS:
        for fs_, ts_ in ((1, 1), (1, 2), (2, 1), (2, 2)):
            for fg, tg in ((3, 3), (3, 4)):
                for dl in (None, '2027-01-11T12:00:00Z'):
                    combos += 1
                    i = dict(base, operation=op, fromStateSchema=fs_, toStateSchema=ts_,
                             fromStoreGeneration=fg, toStoreGeneration=tg, rollbackDeadline=dl)
                    if op == 'core-repair':
                        i['toCoreClosure'] = i['fromCoreClosure']
                    r = S.admit_transition_intent(i)
                    if not isinstance(r, list):
                        unclassified.append(i)
    ok = total and admitted and all(v[0] for v in neg.values()) and not unclassified
    return ('OK' if ok else 'GAP'), {'operationsCovered': sorted(ops), 'totalOperationSet': total,
                                     'perOperation': per_op, 'negatives': neg,
                                     'intentAdmissionCombinationsTotal': combos, 'unclassifiedCombinations': len(unclassified)}


# ===================================================================== new probes

@probe('P8', 'test-execution consent: the host projection can never emit pre-existing-policy (CI lane)')
def p8():
    """A-2 claims the step's consentSource is projected from the actual admitted security consent.
    Security Consent.mode is the closed enum {interactive-explicit, policy-record}; the host projection
    compares it against the string 'pre-existing-policy', which no security record can carry."""
    platform = 'linux-x86_64-gnu'
    grant, ctx = copy.deepcopy(SF['grantBase']), copy.deepcopy(SF['ctxBase'])
    argv = ['bin/opensip-test-runner', '--ci']
    grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId=platform,
                 runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'},
                 argvDigest=W.payload_digest(argv), effects=dict(S.PLATFORM_TRUTH_TABLE[platform]),
                 authorization={'mode': 'policy-record', 'policyRecordId': 'c' * 64, 'ci': True})
    digest = M.owner_digest(grant['owners'])
    grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest
    ctx.pop('semanticGrantPrincipals', None)
    ctx.update(projectId=grant['projectId'], snapshotId=grant['snapshotId'], argvDigest=grant['argvDigest'], ci=True)
    admitted = S.admit_repo_execution_grant(grant, ctx)
    projection = M.test_grant_projection(grant, ctx)
    params = {'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': platform,
              'authorizationRef': projection['securityGrantRef'], 'argv': argv,
              'argv0Source': {'kind': 'toolchain-closure', 'closureId': grant['toolClosureId'], 'member': argv[0]},
              'kind': 'test-execution', 'cwdIsRoot': True, 'consentSource': 'pre-existing-policy', 'afterStep': 0,
              'timeoutMilliseconds': 600000, 'maxOutputBytes': 1048576, 'environmentAllowlist': [],
              'effects': grant['effects']}
    wctx = {'ci': True, 'projectId': grant['projectId'], 'snapshotId': grant['snapshotId'], 'grant': projection,
            'snapshotMembers': ctx['snapshotMembers'],
            'toolchainMembers': {grant['toolClosureId']: ctx['toolClosure']['members']},
            'truthTable': S.PLATFORM_TRUTH_TABLE, 'liveEqualsAfterStep': True}
    policy_lane = refuses(lambda: W.admit_test_execution(params, wctx))
    interactive_lane = refuses(lambda: W.admit_test_execution(dict(params, consentSource='interactive-consent'), wctx))
    # the correct mapping (security policy-record -> workflow pre-existing-policy) admits
    corrected = dict(projection, consentSource='pre-existing-policy')
    fixed = refuses(lambda: W.admit_test_execution(params, dict(wctx, grant=corrected)))
    consent_enum = C.parse((SCRATCH / 'security' / 'security-lifecycle.schemas.v1.json').read_bytes())['$defs']['Consent']['properties']['mode']['enum']
    source = (SCRATCH / 'integration-host-model.py').read_text().splitlines()
    line = next((i + 1, l.strip()) for i, l in enumerate(source) if 'consentSource' in l and 'pre-existing-policy' in l)
    broken = (admitted['result'] == 'ADMIT' and projection['consentSource'] == 'interactive-consent'
              and policy_lane[0] and interactive_lane[0] and not fixed[0])
    return ('COUNTEREXAMPLE' if broken else 'OK'), {
        'securityGrantAdmitted': admitted['result'], 'securityConsentModeEnum': consent_enum,
        'grantAuthorizationMode': grant['authorization']['mode'],
        'projectedConsentSource': projection['consentSource'],
        'ciPolicyLaneRefused': policy_lane, 'ciInteractiveLaneRefused': interactive_lane,
        'admitsOnlyUnderCorrectedMapping': not fixed[0],
        'offendingProjection': {'file': 'integration-host-model.py', 'line': line[0], 'text': line[1]},
        'consequence': 'no `opensip test run` invocation can be admitted in CI through the host composition'}


@probe('P9', 'first-party units between 1025 and 4096 admit discovery but have no typed scope refusal')
def p9():
    """Native section 1.4/14: discovery admits 4096 first-party unit directories while the foundation
    scope descriptor admits at most 1024 workspace roots. The 1025..4096 band has no D9 code or
    registered public detail anywhere."""
    markers = N.synthetic_marker_set(1025, 0, root_marker=False)
    disc = N.discover_units(markers)
    admitted = disc['refused'] is None and len(disc['units']) == 1025
    scope = refuses(lambda: N.unit_scope_descriptor(disc['units'], [], None, disc['prunedTrees'], None))
    d9 = refuses(lambda: N.d9_map('native.scope-root-limit'))
    codes = {r['code'] for r in REGISTRY['records']}
    named = sorted(c for c in codes if 'SCOPE_ROOT' in c.upper() or 'scope-root' in c
                   or 'WORKSPACE_ROOT' in c.upper() or 'workspace-root' in c)
    text = (SNAP / 'docs/v2/contracts/product-v1/native-evidence.md').read_text()
    prose = [l.strip() for l in text.splitlines() if '1024' in l]
    d9_rows = [l for l in text.splitlines() if '4096 first-party' in l]
    gap = admitted and scope[0] and scope[1].startswith('ValidationError') and d9[0] and not named
    return ('GAP' if gap else 'OK'), {
        'discoveryAdmits1025Units': admitted, 'scopeDescriptorRefusal': scope,
        'refusalIsUntypedSchemaError': scope[1].split(':')[0],
        'noD9MappingForScopeBound': d9, 'registeredScopeDetailCodes': named,
        'contractProse': prose[:4], 'd9TableRowForUnitCap': [r.strip()[:180] for r in d9_rows],
        'consequence': 'a project with 1025..4096 first-party unit directories has no defined class, exit or domain detail'}


@probe('P10', 'A-3 explicit Cargo workspace root keeps member folding and member target pruning')
def p10():
    markers = {'Cargo.toml': {'sha256': 'a' * 64, 'isCargoWorkspace': True},
               'crates/core/Cargo.toml': {'sha256': 'b' * 64},
               'crates/util/Cargo.toml': {'sha256': 'c' * 64}}
    auto = N.discover_units(markers)
    explicit = N.discover_units(markers, ['.'])
    member = N.discover_units(markers, ['crates/core'])
    files = ['src/lib.rs', 'crates/core/src/lib.rs', 'crates/core/target/debug/gen.rs', 'crates/core/src/target/x.rs']
    mem_auto = {r['path']: (r['membership'], r['reason']) for r in N.assign_membership(explicit['units'], files)['rows']}
    same = ([{k: v for k, v in u.items() if k != 'provenance'} for u in auto['units']]
            == [{k: v for k, v in u.items() if k != 'provenance'} for u in explicit['units']])
    folded = explicit['units'][0]['memberPackageRoots'] == ['crates/core', 'crates/util']
    member_alone = len(member['units']) == 1 and member['units'][0]['unitKind'] == 'cargo-package'
    pruned = mem_auto['crates/core/target/debug/gen.rs'] == ('syntax-only', 'host-ignore-convention')
    source_target = mem_auto['crates/core/src/target/x.rs'][0] == 'program-member'
    ok = same and folded and member_alone and pruned and source_target
    return ('OK' if ok else 'GAP'), {'explicitEqualsAutomatic': same, 'memberPackageRoots': explicit['units'][0]['memberPackageRoots'],
                                     'memberAloneIsCargoPackage': member_alone,
                                     'memberTargetPruned': mem_auto['crates/core/target/debug/gen.rs'],
                                     'memberSrcTargetIsSource': mem_auto['crates/core/src/target/x.rs']}


@probe('P11', 'SHOULD-4 confidence floor precedes the existential one-rung shortcut')
def p11():
    req = {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'minConfidenceMillionths': 900000,
           'completeness': 'partial-ok', 'quantifier': 'existential', 'unresolvedEdgePolicy': 'forbid',
           'externalConsumerPolicy': 'forbid'}
    rc = {'state': 'not-applicable', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}

    def view(conf):
        return {'clones': {'relation': 'clones', 'resolution': 'normalized-body-hash', 'coverage': 'complete',
                           'confidenceMillionths': conf, 'resolutionCompleteness': rc},
                'declares': {'relation': 'declares', 'resolution': 'syntactic', 'coverage': 'complete',
                             'confidenceMillionths': 1000000, 'resolutionCompleteness': rc}}
    low2, low1 = N.sufficiency_v2(req, view(100000)), N.sufficiency_v1(req, view(100000))
    high = N.sufficiency_v2(req, view(1000000))
    ok = (low2.get('deficiency') == 'confidence-floor-unmet' and low1.get('deficiency') == 'confidence-floor-unmet'
          and high.get('satisfied') is True)
    return ('OK' if ok else 'GAP'), {'v2AtFloor100000': low2.get('deficiency'), 'v1OracleAtFloor100000': low1.get('deficiency'),
                                     'v2At1000000': high.get('satisfied')}


@probe('P12', 'SHOULD-2/A-1 operational grant admission before Plan; close_run operation/principal join')
def p12():
    grant, ctx = copy.deepcopy(SF['grantBase']), copy.deepcopy(SF['ctxBase'])
    grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None,
                 runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
    argv = ['bin/opensip-test-runner', '--ci']
    grant['argvDigest'] = W.payload_digest(argv)
    digest = M.owner_digest(grant['owners'])
    grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest
    ctx.update(projectId=grant['projectId'], snapshotId=grant['snapshotId'], argvDigest=grant['argvDigest'])
    ctx['semanticGrantPrincipals'] = [{'kind': 'trusted-repository-code', 'closureId': 'closure2:' + '9' * 64,
                                       'ownerSourceDigest': '9' * 64}]
    with_projection = S.admit_repo_execution_grant(grant, ctx)
    ctx.pop('semanticGrantPrincipals')
    without = S.admit_repo_execution_grant(grant, ctx)
    ignored = with_projection == without and without['result'] == 'ADMIT'
    test_runner_projects_nothing = S.semantic_projection_for_grants([grant]) == []
    consumed = S.admit_plan_execution_projection([], [grant], 'host-prepared')['result'] == 'REFUSE'
    # close_run: prepare-code iff a trusted-repository-code principal; imports require read-import
    run, objects, blobs = F.build(resolved=True, has_match=True)
    plan = copy.deepcopy(objects[run['planId']][1])
    grant_rec = C.parse(blobs[plan['semanticGrantDigest']])
    bad = dict(grant_rec, analysisOperations=sorted(set(grant_rec['analysisOperations']) | {'prepare-code'}))
    raw = C.canonical(bad)
    blobs[hashlib.sha256(raw).hexdigest()] = raw
    plan['semanticGrantDigest'] = hashlib.sha256(raw).hexdigest()
    F.rekey(objects, run['planId'], plan, run)
    prepare_without_principal = refuses(lambda: M.N.IM.close_run(run, objects, blobs))
    r2, o2, b2 = F.graph_with_import()
    p2 = copy.deepcopy(o2[r2['planId']][1])
    g2 = C.parse(b2[p2['semanticGrantDigest']])
    g2 = dict(g2, analysisOperations=[o for o in g2['analysisOperations'] if o != 'read-import'])
    raw2 = C.canonical(g2)
    b2[hashlib.sha256(raw2).hexdigest()] = raw2
    p2['semanticGrantDigest'] = hashlib.sha256(raw2).hexdigest()
    F.rekey(o2, r2['planId'], p2, r2)
    import_without_read_import = refuses(lambda: M.N.IM.close_run(r2, o2, b2))
    ok = (ignored and test_runner_projects_nothing and consumed
          and prepare_without_principal[0] and import_without_read_import[0])
    return ('OK' if ok else 'GAP'), {'ctxProjectionNeverConsulted': ignored,
                                     'testRunnerProjectsNoPlanPrincipal': test_runner_projects_nothing,
                                     'testRunnerRefusedAsConsumedPreparation': consumed,
                                     'prepareCodeWithoutPrincipalRefused': prepare_without_principal,
                                     'importWithoutReadImportRefused': import_without_read_import}


@probe('P13', 'SHOULD-3/A-5 UNKNOWN backup admits with disclosure; detected requires an explicit choice')
def p13():
    unknown = S.storage_write_admission('UNKNOWN', False, None, False, False)
    detected_ci = S.storage_write_admission('BACKED_UP', False, None, True, False)
    detected_flag = S.storage_write_admission('BACKED_UP', True, None, False, False)
    ident = {state: M.N.IM.storage_admission(state) for state in ('unknown', 'detected', 'not-detected')}
    text = (SNAP / 'docs/v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    read_set = 'Pruned trees and the read set' in text
    ok = (unknown['result'] == 'ADMIT' and 'unknown-disclosed' in json.dumps(unknown)
          and detected_ci['result'] == 'REFUSE' and 'storage.backup-choice-required' in json.dumps(detected_ci)
          and detected_flag['result'] == 'ADMIT' and read_set
          and ident['unknown']['admitted'] is True and ident['unknown']['backupDisclosure'] == 'unknown'
          and ident['detected']['admitted'] is False
          and ident['detected']['detail'] == 'storage.backup-choice-required')
    return ('OK' if ok else 'GAP'), {'unknown': unknown, 'detectedInCi': detected_ci['result'],
                                     'detectedWithFlag': detected_flag['result'],
                                     'identityUnknown': ident, 'a5ReadSetParagraphPresent': read_set}


@probe('P14', 'CX-02 a missing required pivot makes an empty-both-sides comparison indeterminate')
def p14():
    needed = ['empty-both-sides-missing-policy-pivot-is-indeterminate',
              'empty-both-sides-missing-detector-pivot-is-indeterminate',
              'empty-both-sides-no-missing-pivot-remains-pass']
    base_art = make_baseline(POL['basePolicy'], POL['scopeAll'], POL['waiversFp2'], SUBBED['ruleCoverage']['full'])
    rule_of = {CONST['FP1']: ('no-unused-export', 'ts-detector'), CONST['FP2']: ('no-unused-export', 'ts-detector'),
               CONST['FP3']: ('no-unused-export', 'ts-detector'), CONST['FP4']: ('no-unused-export', 'ts-detector'),
               CONST['FP5']: ('runtime-unhit-export', 'ts-detector'), CONST['FP6']: ('stale-file-advisory', 'ts-detector')}
    outcomes = {}
    for case in SUBBED['comparisonCases']:
        if case['id'] not in needed:
            continue
        base = copy.deepcopy(base_art)
        if 'baselineEntries' in case:
            base['descriptor']['entries'] = copy.deepcopy(case['baselineEntries'])
            base['baselineId'] = W.wid('baseline2', 'workflow.baseline', base['descriptor'])
        bd = dict(base['descriptor'])
        bd['_baselineId'] = base['baselineId']
        cur_ctx = {'policyDigest': W.doc_digest(POL[case['currentPolicy']]),
                   'scopeDigest': W.doc_digest(POL[case['currentScope']]),
                   'waiverSetDigest': W.doc_digest(POL[case['currentWaivers']]),
                   'detectorClosureIds': [case['currentDetector']['closureId']],
                   'evidenceAvailability': fixture_evidence(case['currentEvidence'], case.get('importOverrides'))}
        bmap = {e['fingerprint']: e for e in BS['entries']}
        presence, entry_rules = {}, {}
        for fp, pr in case['presence'].items():
            presence[fp] = {'B': fp in bmap, 'E0': pr['E0'], 'E1': pr['E1'], 'E2': pr['E2'], 'E3': pr['E3'],
                            'E4': pr['E4'], 'waivedB': bmap[fp]['waived'] if fp in bmap else False,
                            'waivedC': pr['waivedC']}
            entry_rules[fp] = case.get('entryRules', {}).get(fp) or rule_of[fp]
        current = {'runId': CONST['RUN1'], 'snapshotId': CONST['SNAP1'],
                   'projectId': case.get('currentProject', CONST['PRJ']), 'context': cur_ctx,
                   'ruleCoverage': {r['ruleId']: r for r in SUBBED['ruleCoverage'][case['currentRuleCoverage']]},
                   'presence': presence, 'entryRules': entry_rules}
        cd = case.get('currentDetectors', {'ts-detector': dict(case['currentDetector'])})
        current['context']['detectorClosureIds'] = sorted(d['closureId'] for d in cd.values())
        current['boundPivots'] = case.get('boundPivots', ['E1', 'E2', 'E3'])
        for over in case.get('ruleCoverageOverride', []):
            current['ruleCoverage'][over['ruleId']].update(over)
        res = W.compare(bd, current, SUBBED['hosts'][case['host']], case['profile'], cd,
                        tuple(case.get('acceptOrigins', [])))
        d = res['descriptor']
        outcomes[case['id']] = {'verdict': d['verdict'], 'entriesObserved': len(d['entries']),
                                'gatingCount': d['counts']['gating'], 'pivotsAvailable': d['pivotsAvailable'],
                                'remedyCode': (d.get('remedy') or {}).get('code'),
                                'declaredExpectation': case['expect']['verdict']}
    agree = all(v['verdict'] == v['declaredExpectation'] for v in outcomes.values())
    empty = all(v['entriesObserved'] == 0 for v in outcomes.values())
    verdicts = {k: v['verdict'] for k, v in outcomes.items()}
    ok = (agree and empty and len(outcomes) == 3
          and verdicts['empty-both-sides-missing-policy-pivot-is-indeterminate'] == 'indeterminate'
          and verdicts['empty-both-sides-missing-detector-pivot-is-indeterminate'] == 'indeterminate'
          and verdicts['empty-both-sides-no-missing-pivot-remains-pass'] == 'pass')
    return ('OK' if ok else 'GAP'), {'reExecutedComparisons': outcomes, 'allEntrySetsEmpty': empty,
                                     'modelAgreesWithDeclaredExpectation': agree}


@probe('P15', 'CX-04 closed identifier/digest patterns assert the actual end of input')
def p15():
    docs = sorted(list((SCRATCH / 'workflows' / 'schemas').glob('*.schema.json'))
                  + [SCRATCH / 'native' / 'native-evidence.schemas.v2.json',
                     SCRATCH / 'foundation' / 'identity-schemas.v2.json',
                     SCRATCH / 'security' / 'security-lifecycle.schemas.v1.json',
                     SCRATCH / 'foundation' / 'product-configuration.schema.v2.json',
                     SCRATCH / 'foundation' / 'product-quality-report.schema.v3.json',
                     SCRATCH / 'foundation' / 'import-source-context.schema.json',
                     SCRATCH / 'foundation' / 'g13-result-schema.v5.json'])
    dollar, strict, total = [], 0, 0
    for d in docs:
        for m in re.finditer(r'"pattern"\s*:\s*"((?:[^"\\]|\\.)*)"', d.read_text()):
            pat = m.group(1)
            total += 1
            if pat.endswith('$') or re.search(r'\$(?!\))', pat.replace('\\$', '')):
                dollar.append({'document': d.name, 'pattern': pat[:120]})
            if '(?![' in pat:
                strict += 1
    suffixes = {}
    for name, value in (('Hash', 'a' * 64), ('ProjectId', 'prj1-' + 'a' * 64)):
        schema = dict(M.N.IM.SCHEMA, **{'$ref': '#/$defs/' + name})
        C.validate(schema, value)
        suffixes[name] = {s: refuses(lambda v=value + s, sc=schema: C.validate(sc, v))[0] for s in ('\n', '\r\n', ' ')}
    text_ok = C.parse(C.canonical({'m': 'line one\nline two'}))['m'] == 'line one\nline two'
    ok = not dollar and all(all(v.values()) for v in suffixes.values()) and text_ok
    return ('OK' if ok else 'GAP'), {'patternsScanned': total, 'endOfInputAssertions': strict,
                                     'dollarAnchoredRemaining': dollar, 'suffixRefusals': suffixes,
                                     'ordinaryNewlineTextPreserved': text_ok}


@probe('P16', 'CX-05 confidence field admits only integer gte/lte')
def p16():
    doc = 'workflows/schemas/policy-document.schema.json'
    def rule(field, cmp, value):
        return {'field': field, 'cmp': cmp, 'value': value}
    good = refuses(lambda: W.validate_import_record(doc, '#/$defs/FieldFilter', rule('confidenceMillionths', 'gte', 900000)))
    bad_op = refuses(lambda: W.validate_import_record(doc, '#/$defs/FieldFilter', rule('confidenceMillionths', 'prefix', 'x')))
    bad_float = refuses(lambda: W.validate_import_record(doc, '#/$defs/FieldFilter', rule('confidenceMillionths', 'gte', 0.9)))
    string_numeric = refuses(lambda: W.validate_import_record(doc, '#/$defs/FieldFilter', rule('target', 'gte', 1)))
    ok = (not good[0]) and bad_op[0] and bad_float[0] and string_numeric[0]
    return ('OK' if ok else 'GAP'), {'integerGteAdmitted': not good[0], 'stringOperatorRefused': bad_op,
                                     'floatRefused': bad_float, 'numericOperatorOnStringFieldRefused': string_numeric}


@probe('P17', 'SHOULD-9 only a gating rule makes the verdict indeterminate; disclosure is uniform')
def p17():
    text = (SNAP / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
    prose = ('Only an enabled gating rule at the policy’s severity threshold' in text
             or 'Only an enabled gating rule' in text)
    uniform = 'Missing required evidence and incomplete coverage\nfollow the same rule' in text or \
              'Missing required evidence and incomplete coverage' in text
    ids = {c['id'] for c in CASES['comparisonCases']}
    cases = {'required-coverage-unknown-with-zero-findings-is-indeterminate',
             'required-coverage-unsatisfied-nongating-rule-does-not-gate'}
    ok = prose and uniform and cases <= ids
    return ('OK' if ok else 'GAP'), {'contractStatesGatingOnlyRule': prose, 'evidenceAndCoverageUniform': uniform,
                                     'casesPresent': sorted(cases & ids)}


@probe('P18', 'SHOULD-8 trust-recovery authorization class names the recovery authority, not root keys')
def p18():
    cmd = next(c for c in INVENTORY['commands'] if c['name'] == 'trust-recovery-import')
    cls = cmd.get('authorizationClass')
    schema = C.parse((SCRATCH / 'workflows' / 'schemas' / 'command-inventory.schema.json').read_bytes())
    enum = next((v['enum'] for k, v in schema['$defs'].items() if 'uthorization' in k and 'enum' in v), None)
    root_note = json.dumps(schema).find('root-signed') >= 0
    ok = cls == 'recovery-authority-quorum' and not root_note
    return ('OK' if ok else 'GAP'), {'authorizationClass': cls, 'classEnum': enum,
                                     'schemaStillSaysRootSigned': root_note}


@probe('P19', 'AR-15 current narrative: headings, citations and count claims match the reproduced reports')
def p19():
    contracts = sorted((SNAP / 'docs/v2/contracts/product-v1').glob('*.md'))
    dupes, tmp = {}, {}
    for f in contracts:
        heads = [l.split()[1] if len(l.split()) > 1 else l for l in f.read_text().splitlines() if l.startswith(('## ', '### '))]
        seen, d = set(), []
        for h in heads:
            if h in seen:
                d.append(h)
            seen.add(h)
        if d:
            dupes[f.name] = d
        hits = [l.strip()[:100] for l in f.read_text().splitlines() if '/tmp/' in l]
        if hits:
            tmp[f.name] = hits
    R = Path('/tmp/opensip-design-corrections/post-reset-review.v3/reports')
    sec = C.parse((R / 'security-lifecycle-report.rerun.json').read_bytes())
    nat = C.parse((R / 'native-evidence-report.rerun.json').read_bytes())
    wfr = C.parse((R / 'workflows-report.rerun.json').read_bytes())
    integ = C.parse((R / 'integration-report.rerun.json').read_bytes())
    fl = C.parse((R / 'foundation-launcher.json').read_bytes())
    fnd = sum(C.parse((R / 'foundation-reports' / n).read_bytes()).get('passed', 0)
              for n in ('foundation-report.json', 'identity-report.json', 'product-quality-report.json',
                        'product-configuration-report.json'))
    summary = C.parse((SCRATCH / 'validation-summary.v1.json').read_bytes())
    actual = {'foundation': fnd, 'security': sec['counts']['pass'], 'securitySweeps': len(sec['sweeps']),
              'native': nat['cases']['passed'], 'workflows': wfr['passed'], 'integration': integ['passed'],
              'foundationPins': fl['sourceFileCount']}
    claimed = {'foundation': summary['foundation']['checksPassed'], 'security': summary['security']['casesPassed'],
               'securitySweeps': summary['security']['invariantSweepsPassed'], 'native': summary['native']['casesPassed'],
               'workflows': summary['workflows']['checksPassed'], 'integration': summary['integration']['checksPassed'],
               'foundationPins': summary['foundation']['sourcePinsVerified']}
    sec_text = (SNAP / 'docs/v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    nat_text = (SNAP / 'docs/v2/contracts/product-v1/native-evidence.md').read_text()
    prose_counts = {'security444': 'runs 444 cases' in sec_text, 'securityNine': 'nine invariant sweeps' in sec_text,
                    'native100': '100 cases: 35 positive, 65' in nat_text, 'native86': '86-def' in nat_text}
    empty_pin = [p for p in C.parse((SCRATCH / 'native' / 'source-pins.v2.json').read_bytes())['pins']
                 if p['path'].endswith('native-fix-handoff.v3.md')]
    ok = (not dupes and not tmp and actual == claimed and all(prose_counts.values()) and not empty_pin)
    return ('OK' if ok else 'GAP'), {'duplicateHeadings': dupes, 'tmpCitations': tmp,
                                     'reproducedCounts': actual, 'validationSummaryClaims': claimed,
                                     'countsAgree': actual == claimed, 'contractProseCounts': prose_counts,
                                     'emptyHandoffStillPinned': empty_pin}


@probe('P20', 'installation revisions written by crash recovery cannot be attached to any Attempt history')
def p20():
    intent = TJF['records']['intentUpdateSchemaChange']
    journal = S.transition_journal_record(intent, TJF['ctxBase']['namespaceRegistry'])
    committed = dict(journal, state='COMMITTED')
    done = dict(journal, state='DONE')
    continuation = refuses(lambda: M.installation_journal_history(intent, [committed, done]))
    full = M.installation_journal_history(intent, [dict(journal, state=s) for s in
                                                  ('LEASED', 'PREPARING', 'PREPARED', 'COMMITTED', 'DONE')])
    text = (SNAP / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
    prose = [l.strip() for l in text.splitlines() if 'installationJournalRefs' in l or 'RESUME-COMMIT' in l]
    gap = continuation[0] and len(full) == 5
    return ('GAP' if gap else 'OK'), {
        'recoveryContinuationRefused': continuation, 'originalAttemptHistoryAdmitted': len(full),
        'contractProse': prose[:3],
        'consequence': 'a recovery that retains COMMITTED then DONE under the next fence produces durable '
                       'revisions that installation_journal_history refuses and that no Attempt may name'}


@probe('P21', 'AR-01 exact admission spot vectors')
def p21():
    schema = {'type': 'integer'}
    cases = {'floatSpelled': refuses(lambda: C.parse(b'{"a":1.0}')),
             'exponent': refuses(lambda: C.parse(b'{"a":1e0}')),
             'negativeZero': refuses(lambda: C.parse(b'{"a":-0}')),
             'duplicateKey': refuses(lambda: C.parse(b'{"a":1,"a":2}')),
             'loneSurrogate': refuses(lambda: C.parse(b'{"a":"\\ud800"}')),
             'boolNotInteger': refuses(lambda: C.validate(schema, True))}
    depth_ok = refuses(lambda: C.parse(('[' * 32 + ']' * 32).encode()))[0] is False
    depth_bad = refuses(lambda: C.parse(('[' * 33 + ']' * 33).encode()))[0]
    ok = all(v[0] for v in cases.values()) and depth_ok and depth_bad
    return ('OK' if ok else 'GAP'), {'refusals': cases, 'depth32Admits': depth_ok, 'depth33Refused': depth_bad}


@probe('P22', 'SHOULD-1 a hash-valid import outside the evaluated closure is not hidden finding evidence')
def p22():
    run, objects, blobs = F.build(resolved=True, has_match=True)

    def put(value):
        raw = C.canonical(value)
        blobs[hashlib.sha256(raw).hexdigest()] = raw
        return hashlib.sha256(raw).hexdigest()

    empty = put({})
    closure = next(k for k, (d, v) in objects.items() if d == 'closure')
    foreign = {'schemaVersion': 2, 'kind': 'runtime', 'payloadSchemaDigest': empty, 'payloadDigest': empty,
               'sourceCorrespondenceDigest': empty, 'buildDigest': empty, 'producerClosure': closure,
               'adapterClosure': closure, 'blobs': [], 'scopeDigest': empty, 'observationDigest': empty,
               'completeness': 'complete', 'omissions': []}
    fid = M.N.IM.identifier('import', foreign)
    objects[fid] = ('import', foreign)
    fp = {'schemaVersion': 2, 'ruleStableId': 'no-consumer', 'detectorSemanticsMajor': 2,
          'subjectKey': {'language': 'typescript', 'kind': 'symbol', 'logicalPath': 'a.ts', 'qualifiedName': 'foo',
                         'discriminator': 'one'}, 'relatedSubjectKeys': []}
    fpk = M.N.IM.identifier('finding-fingerprint', fp)
    objects[fpk] = ('finding-fingerprint', fp)
    finding = {'schemaVersion': 2, 'fingerprint': fpk, 'ruleClosure': closure, 'subjectId': 'foo',
               'messageCode': 'unused', 'parameterDigest': put({}), 'severity': 'error',
               'evidenceRefs': [{'domain': 'import', 'digest': fid.split(':')[1]}]}
    fid2 = M.N.IM.identifier('finding', finding)
    objects[fid2] = ('finding', finding)
    pk = objects[run['evaluationSealId']][1]['proofBundleId']
    proof = copy.deepcopy(objects[pk][1])
    proof['findingIds'] = [fid2]
    F.rekey(objects, pk, proof, run)
    ek = run['evidenceId']
    ev = copy.deepcopy(objects[ek][1])
    ev['findingIds'] = [fid2]
    F.rekey(objects, ek, ev, run)
    hidden = refuses(lambda: M.N.IM.close_run(run, objects, blobs))
    return ('OK' if hidden[0] else 'COUNTEREXAMPLE'), {'hiddenImportEvidenceRefused': hidden}


@probe('P23', 'crosswalk/dispositions still name the predecessor review; application must repoint them')
def p23():
    cw = C.parse((SCRATCH / 'correction-crosswalk.proposed.json').read_bytes())
    paths = {i['review']['path'] for i in cw['items']}
    subjects = {i['review']['subjectManifestSha256'] for i in cw['items']}
    verdicts = {i['review']['overallVerdict'] for i in cw['items']}
    statuses = {i['status'] for i in cw['items']}
    disp = C.parse((SCRATCH / 'post-reset-dispositions.v3.proposed.json').read_bytes())
    pending = {f['disposition'] for f in disp['findings']}
    summary = C.parse((SCRATCH / 'validation-summary.v1.json').read_bytes())
    honest = (summary['claudeFinalReview'] == 'PENDING-FROZEN-V3' and summary['readinessChanged'] is False
              and pending == {'CORRECTED-PENDING-REVIEW'} and verdicts == {'CHANGES_REQUIRED'})
    return ('OK' if honest else 'GAP'), {'crosswalkReviewPaths': sorted(paths), 'crosswalkSubjects': sorted(subjects),
                                         'crosswalkVerdicts': sorted(verdicts), 'crosswalkStatuses': sorted(statuses),
                                         'dispositionStates': sorted(pending),
                                         'validationSummaryFinalReview': summary['claudeFinalReview'],
                                         'readinessChanged': summary['readinessChanged']}


@probe('P24', 'registered public codes reachable only from the standalone native instrument')
def p24():
    inp, markers, files, root = boundary_fixture()
    # security refuses an explicit root crossing the nested project before native ever runs
    crossing = copy.deepcopy(inp)
    crossing['explicitJoins'] = ['apps/site']
    sec = S.discovery(crossing)
    standalone = N.discover_units(markers, ['apps/site'],
                                  S.DD.boundary_inventory_from_provenance(S.discovery(inp)['provenance']))
    host = refuses(lambda: M.admit_repository_discovery(crossing, markers, files))
    codes = {r['code'] for r in REGISTRY['records']}
    return 'OK', {'securityRefusal': {'refusal': sec.get('refusal'), 'detail': sec.get('detail')},
                  'standaloneNativeRefusal': standalone['refused'] and standalone['refused']['detail'],
                  'hostCompositionRefused': host,
                  'bothCodesRegisteredPublicly': sorted(c for c in codes if c in
                                                        ('PROJECT.EXPLICIT_PATH_INVALID', 'native.explicit-root-crosses-boundary')),
                  'note': 'the operational host composition emits only PROJECT.EXPLICIT_PATH_INVALID; the native '
                          'counterpart is reachable from the standalone instrument, which is not an operational surface'}


@probe('P25', 'consent vocabulary across security, test-execution and repair-apply records')
def p25():
    sec = C.parse((SCRATCH / 'security' / 'security-lifecycle.schemas.v1.json').read_bytes())['$defs']['Consent']['properties']['mode']['enum']
    test = C.parse((SCRATCH / 'workflows' / 'schemas' / 'test-execution.schema.json').read_bytes())['$defs']['TestExecutionStepParams']['properties']['consentSource']['enum']
    repair = C.parse((SCRATCH / 'workflows' / 'schemas' / 'invocation-record.schema.json').read_bytes())['$defs']['RepairApplyParams']['properties']['consentSource']['enum']
    text = (SNAP / 'docs/v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    mapping_stated = '`pre-existing-policy` | `interactive-consent`) maps to\n`policy-record` | `interactive-explicit`' in text \
        or 'maps to `policy-record` | `interactive-explicit`' in text.replace('\n', ' ')
    repair_mapping = 'RepairApplyParams' in text and 'consentSource' in text
    # the repair projection carries no consent mode at all
    proj_fields = sorted(M.repair_authorization_projection.__doc__ and [] or [])
    return 'OK', {'securityConsentModes': sec, 'testExecutionConsentSource': test,
                  'repairApplyConsentSource': repair, 'testMappingStatedInContract': mapping_stated,
                  'repairMappingStatedInContract': repair_mapping,
                  'note': 'three spellings of one concept; only the test-execution mapping is stated, and the '
                          'repair projection carries no consent mode for the workflow to check'}


@probe('P26', 'MUST-1 goldens carry the security/native/identity details and class/exit agree')
def p26():
    goldens = INVENTORY['goldens']
    named_in_v1 = ('trust-recovery-import-refused', 'store-migrate-corrupt-footprint', 'query-evidence-purged')
    rows = {g['id']: g for g in goldens}
    common = C.parse((SCRATCH / 'workflows' / 'schemas' / 'common.schema.json').read_bytes())
    enum = set(common['$defs']['DomainDetailCode']['enum'])
    detail_of = {}
    for gid in named_in_v1:
        g = rows.get(gid)
        detail_of[gid] = None if g is None else g.get('detail') or g.get('domainDetail')
    carried = {k: (v in enum if isinstance(v, str) else False) for k, v in detail_of.items()}
    exits = {g['id']: (g['class'], g['exitCode']) for g in goldens}
    table = {'success': 0, 'policy-failed': 1, 'request-rejected': 2, 'indeterminate': 3,
             'operational-failed': 4, 'interrupted': 130}
    bad_exit = {k: v for k, v in exits.items() if table.get(v[0]) != v[1]}
    unregistered = sorted({d for g in goldens for d in [g.get('detail')] if isinstance(d, str) and d not in enum})
    ok = all(carried.values()) and not bad_exit and not unregistered
    return ('OK' if ok else 'GAP'), {'goldens': len(goldens), 'v1NamedGoldenDetails': detail_of,
                                     'v1NamedGoldensCarryRegisteredDetail': carried,
                                     'classExitDisagreements': bad_exit,
                                     'goldenDetailsOutsideRegistry': unregistered}


@probe('P27', 'registry totality: every public code has an owner/selector and is admitted by the envelope')
def p27():
    records = REGISTRY['records']
    shape = [r for r in records if set(r) != {'code', 'owner', 'selector'}]
    owners = sorted({r['owner'] for r in records})
    dupes = sorted({r['code'] for r in records if [x['code'] for x in records].count(r['code']) > 1})
    refused = []
    for r in records:
        try:
            W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail',
                                     {'code': r['code'], 'remedy': 'see the owning contract'})
        except Exception as exc:
            refused.append({'code': r['code'], 'error': type(exc).__name__})
    # every projection lands on a lawful closed StepTermination branch with the owner's own class
    classes = {}
    for key in sorted(S.D9):
        d9 = S.d9(key)
        code = {r['internalCode']: r['publicCode'] for r in REGISTRY['internalAliases']}.get(key, key)
        if code not in {r['code'] for r in records}:
            continue
        try:
            t = M.public_termination(d9, code, 'remedy')
            classes.setdefault(t['class'], 0)
            classes[t['class']] += 1
        except Exception as exc:
            classes.setdefault('REFUSED:' + type(exc).__name__, 0)
            classes['REFUSED:' + type(exc).__name__] += 1
    ok = not shape and not dupes and not refused and not any(k.startswith('REFUSED') for k in classes)
    return ('OK' if ok else 'GAP'), {'records': len(records), 'owners': owners, 'malformedRecords': shape,
                                     'duplicateCodes': dupes, 'refusedByEnvelopeSchema': refused,
                                     'securityProjectionClasses': classes}


@probe('P28', 'consent vocabulary contradiction between the two owning contracts; two reference residues')
def p28():
    sec_text = (SNAP / 'docs/v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    wf_text = (SNAP / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
    sec_sentence = next((l.strip() for l in sec_text.replace('\n', ' ').split('. ')
                         if 'consentSource' in l and 'policy-record' in l), None)
    wf_sentence = next((l.strip() for l in wf_text.splitlines()
                        if 'consentSource' in l and 'pre-existing-policy' in l), None)
    enum = C.parse((SCRATCH / 'security' / 'security-lifecycle.schemas.v1.json').read_bytes())['$defs']['Consent']['properties']['mode']['enum']
    wf_names_nonexistent = wf_sentence is not None and 'pre-existing-policy -> pre-existing-policy' in wf_sentence
    sec_names_correct = sec_sentence is not None and 'policy-record' in sec_sentence
    # residue 1: close_run cannot distinguish retention loss from admission refusal for a missing blob
    run, objects, blobs = F.build(resolved=True, has_match=True)
    plan = objects[run['planId']][1]
    missing = refuses(lambda: M.N.IM.close_run(run, objects, {k: v for k, v in blobs.items()
                                                              if k != plan['analysisSpecDigest']}))
    typed_missing = missing[0] and missing[1].startswith('AdmissionError')
    # residue 2: the scope function still reads a key the closed intent cannot carry
    src = (SCRATCH / 'security' / 'security_lifecycle_model_v1.py').read_text()
    dead = "intent.get('reselectsStore', False)" in src
    closed_keys = 'reselectsStore' not in S.TRANSITION_INTENT_KEYS
    return 'OK', {'securityConsentModeEnum': enum, 'securityContractSentence': (sec_sentence or '')[:300],
                  'workflowContractSentence': (wf_sentence or '')[:300],
                  'workflowNamesSecurityValueThatDoesNotExist': wf_names_nonexistent,
                  'securityStatesCorrectMapping': sec_names_correct,
                  'missingBlobRefusal': missing[1][:160], 'missingBlobIsTypedAdmissionError': typed_missing,
                  'deadReselectsStoreParameter': dead, 'intentSchemaCannotCarryIt': closed_keys}


# ===================================================================== write
report = {
    'standing': 'INDEPENDENT REVIEWER PROBES; design/reference evidence over synthetic fixtures only; '
                'not product qualification and not the blind consumer-B litmus',
    'reviewer': 'fresh actual Claude session; started claude-fable-5-1 (interrupted by API 429, no verdict), '
                'completed on claude-opus-5; authored none of the subject bytes',
    'subjectManifestSha256': 'e3365d6e64cb5b0260ec7261af5c3e554504c9ab9515456f680aeb01b31b76fd',
    'syntheticTcbInputs': ['signatures', 'OS/custody observations', 'evaluator callbacks', 'pivot presences',
                           'fence/lease observations', 'trust clock instants'],
    'counts': {},
    'probes': results,
}
for r in results:
    report['counts'][r['status']] = report['counts'].get(r['status'], 0) + 1
OUT.write_text(json.dumps(report, indent=1, default=str) + '\n')
print('\n' + json.dumps(report['counts']))
sys.exit(0)
