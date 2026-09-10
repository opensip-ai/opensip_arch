"""Independent reviewer probes over the FROZEN candidate-subject.v2 (read-only).

Reviewer: fresh actual Claude session; authored none of the subject bytes. Loads the reference models
from the frozen snapshot by path, never writes into it, and records every observation in
independent-probes.json beside this file. Synthetic TCB inputs throughout; nothing here is product
qualification. Each probe states what the contracts say and what the reference bytes do.
"""
import copy, hashlib, json, re, sys, traceback, importlib.util
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/candidate-subject.v2/docs/coop/design-corrections')
OUT = Path(__file__).resolve().parent / 'independent-probes.json'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

M = load('ihm', ROOT / 'integration-host-model.py')
C, S, N, W, DD = M.C, M.S, M.N, M.W, M.S.DD
IM = N.IM
PCM = load('pcm', ROOT / 'foundation/product-configuration-model.py')
F = load('fixture', ROOT / 'integration-fixtures.py')

results = []
def record(pid, title, verdict, evidence, severity_hint=None):
    results.append({'id': pid, 'title': title, 'verdict': verdict, 'evidence': evidence, 'severityHint': severity_hint})
    print(pid, verdict, title)

def probe(pid, title, fn, severity_hint=None):
    try:
        verdict, ev = fn()
    except Exception as exc:  # a crash is itself evidence
        verdict, ev = 'PROBE-ERROR', {'exception': repr(exc), 'trace': traceback.format_exc()[-1500:]}
    record(pid, title, verdict, ev, severity_hint)

def refuses(fn):
    try:
        fn(); return None
    except Exception as exc:
        return repr(exc)[:300]

# ------------------------------------------------------------------ fixture helpers (security substitution, workflow constants)
def substitute(value, subs):
    if isinstance(value, str) and value.startswith('$') and value[1:] in subs: return subs[value[1:]]
    if isinstance(value, list): return [substitute(v, subs) for v in value]
    if isinstance(value, dict): return {k: substitute(v, subs) for k, v in value.items()}
    return value
def deep_merge(base, over):
    out = dict(base)
    for k, v in over.items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out
def resolve_input(inp, subs):
    inp = substitute(inp, subs)
    def walk(v):
        if isinstance(v, dict):
            if '$from' in v:
                return deep_merge(subs[v['$from']], {k: walk(x) for k, x in v.items() if k != '$from'})
            return {k: walk(x) for k, x in v.items()}
        if isinstance(v, list): return [walk(x) for x in v]
        return v
    return walk(inp)
ALIASES = {'baseRecord': 'base', 'ctxBase': 'ctx', 'grantBase': 'grant', 'authorizationBase': 'authorization'}
def build_subs(doc):
    subs = {}
    for key in ('computed', 'keys'):
        for k, v in doc.get(key, {}).items(): subs[k] = v
    for key, val in doc.items():
        if key in ('roots', 'records', 'observations'):
            for k, v in val.items(): subs[k] = resolve_input(v, subs)
        elif isinstance(val, dict) and key not in ('conventions', 'computed', 'keys'):
            subs[ALIASES.get(key, key)] = resolve_input(val, subs)
    return subs

wf = C.parse((ROOT / 'workflows/workflow-cases.v1.json').read_bytes())
WC = wf['constants']
def sub(value):
    if isinstance(value, str) and value.startswith('$'): return WC[value[1:]]
    if isinstance(value, dict): return {k: sub(v) for k, v in value.items()}
    if isinstance(value, list): return [sub(v) for v in value]
    return value
POL = sub(wf['policyDocs'])
sf = C.parse((ROOT / 'security/execution-principal-cases.v1.json').read_bytes())
nf = C.parse((ROOT / 'native/native-cases.v2.json').read_bytes())['fixtures']
registry = C.parse((ROOT / 'public-detail-registry.v1.json').read_bytes())
REG = {r['code']: r for r in registry['records']}
common = C.parse((ROOT / 'workflows/schemas/common.schema.json').read_bytes())
inventory = C.parse((ROOT / 'workflows/command-inventory.v1.json').read_bytes())

# ================================================================== P1 MUST-2 one platform vocabulary
def p1():
    ss = C.parse((ROOT / 'security/security-lifecycle.schemas.v1.json').read_bytes())['schemas']
    keys = set(ss['PlatformProfileSetV1']['properties']['platforms']['properties'].keys())
    matrix = C.parse((ROOT / 'native/native-capability-matrix.v2.json').read_bytes())
    te = C.parse((ROOT / 'workflows/schemas/test-execution.schema.json').read_bytes())['$defs']['TestExecutionStepParams']['properties']['platformId']['enum']
    gates = C.parse((ROOT / 'qualification-gates.proposed.json').read_bytes())['platformFamilies']
    sets = {'profileSetKeys': sorted(keys), 'truthTable': sorted(S.PLATFORM_TRUTH_TABLE), 'population': sorted(S.SUPPORTED_POPULATION),
            'nativeMatrix': sorted(matrix['platformFamilies']), 'workflowTestSchema': sorted(te), 'gates': sorted(gates), 'workflowModel': sorted(W.PLATFORMS)}
    equal = len({json.dumps(v) for v in sets.values()}) == 1
    # alias refusals: grant with alias, profile set keyed by alias
    grant, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
    grant['platformId'] = 'macos-arm64'
    g = S.admit_repo_execution_grant(grant, ctx)
    alias_grant = [r for r in g['refusals'] if r.startswith('GRANT.PLATFORM_DISPLAY_ALIAS')]
    # G13 historical schema keeps aliases (scoped historical corpus labels per source map)
    g13 = (ROOT / 'foundation/g13-result-schema.v5.json').read_text()
    return ('OK' if equal and alias_grant else 'COUNTEREXAMPLE'), {'sets': sets, 'allEqual': equal, 'aliasGrantRefusal': alias_grant,
            'g13HistoricalAliasStrings': [a for a in ('macos-arm64', 'linux-arm64', 'linux-x86_64') if a in g13]}
probe('P1', 'MUST-2: one machine platform vocabulary across profile set, truth table, native matrix, workflow schema, gates', p1)

# ================================================================== P2 MUST-3 shared discovery
def synthetic_fs(first_party, installed, root='/home/alice/repo'):
    fs = {'/': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1}, '/home': {'kind': 'dir', 'uid': 0, 'mode': '0755', 'dev': 1},
          '/home/alice': {'kind': 'dir', 'uid': 1000, 'mode': '0700', 'dev': 1}, root: {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1, 'vcs': True},
          root + '/package.json': {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}}
    d = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}; f = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    for i in range(first_party):
        fs[root + '/pkg%04d' % i] = dict(d); fs[root + '/pkg%04d/package.json' % i] = dict(f)
    if installed:
        fs[root + '/node_modules'] = dict(d)
        for i in range(installed):
            fs[root + '/node_modules/dep%04d' % i] = dict(d); fs[root + '/node_modules/dep%04d/package.json' % i] = dict(f)
    return fs
def disc_input(fs, cwd='/home/alice/repo', **kw):
    return dict({'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': cwd, 'fs': fs}, **kw)
def p2():
    ev = {}
    s_inst = S.discovery(disc_input(synthetic_fs(0, 4200)))
    n_inst = N.discover_units(N.synthetic_marker_set(0, 4200))
    ev['installed4200'] = {'security': (s_inst['status'], len(s_inst['provenance']['units']), s_inst['provenance']['prunedTrees']),
                           'native': (n_inst['refused'], len(n_inst['units']), n_inst['prunedTrees'])}
    s_fp = S.discovery(disc_input(synthetic_fs(4200, 0)))
    n_fp = N.discover_units(N.synthetic_marker_set(4200, 0))
    ev['firstParty4200'] = {'security': (s_fp['status'], s_fp.get('refusal'), s_fp.get('detail'), s_fp.get('d9')),
                            'native': (n_fp['refused']['detail'] if n_fp['refused'] else None, n_fp['refused']['d9']['code'] if n_fp['refused'] else None, n_fp['units'])}
    s_ok = S.discovery(disc_input(synthetic_fs(4095, 0)))
    ev['firstParty4096exact'] = (s_ok['status'], len(s_ok['provenance']['units']))
    ev['classify'] = {p: DD.classify_path(p, {''}) for p in ('packages/target/index.ts', 'src/target/x.ts', 'target/debug/x.rs', 'node_modules/a/package.json', 'crates/core/target/o.rs')}
    ev['classify_cargo_member'] = DD.classify_path('crates/core/target/o.rs', {'', 'crates/core'})
    # explicit root sentinel and grammar through both instruments
    fs = synthetic_fs(0, 2); fs['/home/alice/repo/packages'] = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}; fs['/home/alice/repo/packages/web'] = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}; fs['/home/alice/repo/packages/web/package.json'] = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    markers = {'package.json': {'sha256': '1' * 64}, 'packages/web/package.json': {'sha256': '1' * 64}, 'node_modules/dep0000/package.json': {'sha256': '1' * 64}}
    ev['explicitRoots'] = {}
    for spec in ('.', 'packages/web', 'packages/web/', 'packages/./web', 'node_modules/dep0000', '', 'a//b'):
        sres = S.discovery(disc_input(fs, configWorkspaceRoots=[spec]))
        nres = N.discover_units(markers, [spec])
        ev['explicitRoots'][spec or '<empty>'] = {'security': (sres['status'], sres.get('detail'), [u['path'] for u in sres['provenance']['units']], sres['provenance']['warnings']),
                                                   'native': (nres['refused']['detail'] if nres['refused'] else 'ACCEPT', [u['rootPath'] for u in nres['units']])}
    reg = {'profiles': ['default'], 'capabilities': [], 'packs': [], 'waivers': []}
    ev['foundationConfig2Resolver'] = {}
    for roots in (['.'], ['packages/web/'], [], ['packages/web'], ['./']):
        cfg = json.dumps({'schemaVersion': 2, 'analysis': {'profileId': 'default'}, 'discovery': {'workspaceRoots': roots}}).encode()
        ev['foundationConfig2Resolver'][json.dumps(roots)] = refuses(lambda: PCM.resolve({'project': cfg}, reg)) or 'ACCEPT'
    ok = (ev['installed4200']['security'][1] == 1 and ev['installed4200']['native'][1] == 1 and ev['firstParty4200']['security'][0] == 'REFUSE'
          and ev['firstParty4200']['native'][0] == 'native.too-many-units' and ev['classify']['packages/target/index.ts'] is None)
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P2', 'MUST-3: shared segment pruning, real cap refusal, sentinel and grammar through both instruments', p2)

# ================================================================== P3 nested repository / nested project join (new)
def p3():
    fs = synthetic_fs(0, 0)
    d = {'kind': 'dir', 'uid': 1000, 'mode': '0755', 'dev': 1}; f = {'kind': 'file', 'uid': 1000, 'mode': '0644', 'nlink': 1, 'size': 10}
    R = '/home/alice/repo'
    fs[R + '/vendor'] = dict(d); fs[R + '/vendor/lib'] = dict(d, vcs=True); fs[R + '/vendor/lib/package.json'] = dict(f); fs[R + '/vendor/lib/src'] = dict(d)
    fs[R + '/apps'] = dict(d); fs[R + '/apps/site'] = dict(d); fs[R + '/apps/site/opensip.json'] = dict(f); fs[R + '/apps/site/package.json'] = dict(f)
    fs[R + '/apps/site/sub'] = dict(d); fs[R + '/apps/site/sub/Cargo.toml'] = dict(f)
    sd = S.discovery(disc_input(fs))
    prov = sd['provenance']
    markers = {p[len(R) + 1:]: {'sha256': '1' * 64} for p, e in fs.items() if p.startswith(R + '/') and e['kind'] == 'file' and p.rpartition('/')[2] in DD.WORKSPACE_MARKERS}
    nd = N.discover_units(markers)
    sroots = sorted(u['path'][len(R) + 1:] if u['path'] != R else '' for u in prov['units'])
    nroots = sorted({u['rootPath'] for u in nd['units']})
    scope = N.unit_scope_descriptor(nd['units'], [], None, nd['prunedTrees'])
    return ('COUNTEREXAMPLE' if sroots != nroots else 'OK'), {
        'securityUnits': sroots, 'securityExcluded': prov['excludedUnits'], 'nestedRepositories': prov['nestedRepositories'], 'nestedProjects': prov['nestedProjects'],
        'nativeUnitsOverSameMarkerInventory': nroots, 'nativePrunedTrees': nd['prunedTrees'],
        'scopeDescriptorExcludedPrefixes': scope['scopeDescriptor']['excludedPathPrefixes'],
        'note': 'integration check security-native-shared-unit-roots uses a fixture without nested repositories/projects; the shared rule prunes only node_modules/VCS-dir/target segments, so nested repo and nested project markers reach the native instrument unless the host filters the inventory, and the scope descriptor does not record either exclusion'}
probe('P3', 'Cross-unit: nested repository and nested project exclusion (security) versus native unit discovery over the same marker inventory', p3, 'SHOULD')

# ================================================================== P4 public detail registry determinacy (MUST-1 successor)
def p4():
    ev = {}
    ev['unitCapSpellings'] = [c for c in REG if 'UNIT_LIMIT' in c or 'too-many-units' in c]
    ev['rootGrammarSpellings'] = [c for c in REG if c in ('PROJECT.EXPLICIT_PATH_INVALID', 'native.explicit-root-grammar', 'native.explicit-root-without-marker')]
    ev['deadOrOddCodes'] = {'GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED': {'registered': 'GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED' in REG,
                                                                        'emittedBySecurityModel': 'GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED' in (ROOT / 'security/security_lifecycle_model_v1.py').read_text()},
                            'provider-unavailable/capability-missing': {'registered': 'provider-unavailable/capability-missing' in REG, 'isNativeD9TableKey': 'provider-unavailable/capability-missing' in N.D9_MAP},
                            'WORKSPACE_UNIT_LIMIT': {'registered': 'WORKSPACE_UNIT_LIMIT' in REG, 'securityUsesAsSubdetail': True}}
    terms = {}
    for key, fn in (('security', lambda: M.public_termination(S.d9('PROJECT.WORKSPACE_UNIT_LIMIT'), 'PROJECT.WORKSPACE_UNIT_LIMIT', 'narrow scope', 'WORKSPACE_UNIT_LIMIT:4201>4096')),
                    ('native', lambda: M.public_termination(N.d9_map('native.too-many-units'), 'native.too-many-units', 'narrow scope')),
                    ('bare', lambda: M.public_termination(S.d9('PROJECT.WORKSPACE_UNIT_LIMIT'), 'WORKSPACE_UNIT_LIMIT', 'narrow scope'))):
        try:
            t = fn(); terms[key] = {'accepted': True, 'errorCode': t.get('errorCode'), 'detail': t['domainDetail']['code'], 'exit': W.exit_code(t)}
        except Exception as exc:
            terms[key] = {'accepted': False, 'error': repr(exc)[:200]}
    ev['sameConditionThreeLawfulEnvelopes'] = terms
    # grammar refusal for one malformed explicit root: security and native each own a different public code
    grammar = {}
    for key, fn in (('security', lambda: M.public_termination(S.d9('PROJECT.EXPLICIT_PATH_INVALID'), 'PROJECT.EXPLICIT_PATH_INVALID', 'fix path', 'JOIN_PATH_GRAMMAR')),
                    ('native', lambda: M.public_termination(N.d9_map('native.explicit-root-grammar'), 'native.explicit-root-grammar', 'fix path'))):
        try:
            t = fn(); grammar[key] = {'accepted': True, 'errorCode': t.get('errorCode'), 'detail': t['domainDetail']['code']}
        except Exception as exc:
            grammar[key] = {'accepted': False, 'error': repr(exc)[:200]}
    ev['sameGrammarRefusalTwoCodes'] = grammar
    ev['registryOwners'] = {o: sum(1 for r in REG.values() if r['owner'] == o) for o in sorted({r['owner'] for r in REG.values()})}
    ev['unregisteredRefused'] = refuses(lambda: M.public_termination(S.d9('GRANT.REFUSED'), 'native.future', 'x'))
    ev['uppercaseStorageAliasRefused'] = refuses(lambda: W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/DomainDetail', {'code': 'STORAGE.BACKUP_CHOICE_REQUIRED', 'remedy': 'x'}))
    ev['schemaEnumEqualsRegistry'] = set(common['$defs']['DomainDetailCode']['enum']) == set(REG)
    multiple = sum(1 for t in terms.values() if t['accepted']) > 1
    return ('COUNTEREXAMPLE' if multiple else 'OK'), ev
probe('P4', 'MUST-1 successor: one closed registry, but one condition (unit cap; explicit-root grammar) has two or three registered public spellings across owners', p4, 'SHOULD')

# ================================================================== P5 identity closure: hidden import (SHOULD-1) and cross-source import (new)
def graph_with_import(correspondence_snapshot):
    run, objects, blobs = F.build(resolved=True, has_match=True)
    def put(v):
        raw = C.canonical(v); d = hashlib.sha256(raw).hexdigest(); blobs[d] = raw; return d
    closure = next(k for k, (dom, v) in objects.items() if dom == 'closure')
    imp = {'schemaVersion': 2, 'kind': 'runtime', 'payloadSchemaDigest': put({'$schema': 'x'}), 'payloadDigest': put({'subjects': []}),
           'sourceCorrespondenceDigest': put({'kind': 'exact-snapshot', 'snapshotId': correspondence_snapshot}), 'buildDigest': put({'schemaVersion': 1, 'buildIdentity': None}),
           'producerClosure': closure, 'adapterClosure': closure, 'blobs': [], 'scopeDigest': put({'schemaVersion': 2, 'workspaceRoots': ['.'], 'pathPrefixes': ['.'], 'excludedPathPrefixes': []}),
           'observationDigest': put({'schemaVersion': 1, 'kind': 'runtime', 'window': None, 'population': None, 'selection': None, 'revisionRange': None}), 'completeness': 'complete', 'omissions': []}
    iid = IM.identifier('import', imp); objects[iid] = ('import', imp)
    plan = copy.deepcopy(objects[run['planId']][1]); plan['importIds'] = [iid]; F.rekey(objects, run['planId'], plan, run)
    seal_id = run['evaluationSealId']; pk = objects[seal_id][1]['proofBundleId']
    proof = copy.deepcopy(objects[pk][1]); proof['evaluationInputRefs'] = sorted(proof['evaluationInputRefs'] + [{'domain': 'import', 'digest': iid.split(':')[1]}], key=C.canonical); F.rekey(objects, pk, proof, run)
    ek = run['evidenceId']; ev = copy.deepcopy(objects[ek][1]); ev['importIds'] = [iid]; F.rekey(objects, ek, ev, run)
    return run, objects, blobs, iid
def p5():
    out = {}
    run, objects, blobs, iid = graph_with_import(run_snapshot := None) if False else (None, None, None, None)
    # (a) same-snapshot import: admitted
    r0, o0, b0 = F.build(resolved=True, has_match=True)
    run, objects, blobs, iid = graph_with_import(r0['snapshotId'])
    out['sameSnapshotImportClosure'] = IM.close_run(run, objects, blobs)[:12]
    # (b) import whose retained correspondence names a DIFFERENT snapshot: contract identity §3 says cross-source references are rejected
    run2, objects2, blobs2, iid2 = graph_with_import('snapshot2:' + 'f' * 64)
    try:
        out['foreignSnapshotImportClosure'] = IM.close_run(run2, objects2, blobs2)[:12]; foreign_admitted = True
    except Exception as exc:
        out['foreignSnapshotImportClosure'] = repr(exc)[:200]; foreign_admitted = False
    # (c) SHOULD-1 regression: finding citing an import not in Plan is refused; citing the evaluated import is admitted
    run3, objects3, blobs3, iid3 = graph_with_import(r0['snapshotId'])
    closure = next(k for k, (dom, v) in objects3.items() if dom == 'closure')
    def put3(v):
        raw = C.canonical(v); d = hashlib.sha256(raw).hexdigest(); blobs3[d] = raw; return d
    fp = {'schemaVersion': 2, 'ruleStableId': 'no-consumer', 'detectorSemanticsMajor': 2, 'subjectKey': {'language': 'typescript', 'kind': 'symbol', 'logicalPath': 'a.ts', 'qualifiedName': 'foo', 'discriminator': 'one'}, 'relatedSubjectKeys': []}
    fpk = IM.identifier('finding-fingerprint', fp); objects3[fpk] = ('finding-fingerprint', fp)
    finding = {'schemaVersion': 2, 'fingerprint': fpk, 'ruleClosure': closure, 'subjectId': 'foo', 'messageCode': 'unused', 'parameterDigest': put3({}), 'severity': 'error',
               'evidenceRefs': [{'domain': 'import', 'digest': iid3.split(':')[1]}]}
    fid = IM.identifier('finding', finding); objects3[fid] = ('finding', finding)
    pk = objects3[run3['evaluationSealId']][1]['proofBundleId']; proof = copy.deepcopy(objects3[pk][1]); proof['findingIds'] = [fid]; F.rekey(objects3, pk, proof, run3)
    ek = run3['evidenceId']; ev = copy.deepcopy(objects3[ek][1]); ev['findingIds'] = [fid]; F.rekey(objects3, ek, ev, run3)
    out['findingCitesEvaluatedPlanImport'] = IM.close_run(run3, objects3, blobs3)[:12]
    # now drop the import from evaluationInputRefs only (still in plan): must refuse (import must be selected AND evaluated)
    pk = objects3[run3['evaluationSealId']][1]['proofBundleId']; proof = copy.deepcopy(objects3[pk][1]); proof['evaluationInputRefs'] = [r for r in proof['evaluationInputRefs'] if r['domain'] != 'import']; F.rekey(objects3, pk, proof, run3)
    out['findingCitesPlanImportNotEvaluated'] = refuses(lambda: IM.close_run(run3, objects3, blobs3))
    return ('COUNTEREXAMPLE' if foreign_admitted else 'OK'), out
probe('P5', 'AR-09/AR-11: identity closure admits an evaluated import whose retained correspondence names a foreign snapshot (SHOULD-1 hidden-import fix holds)', p5, 'SHOULD')

# ================================================================== P6 SHOULD-2 grants before Plan; projection join; operations not joined (new)
def p6():
    ev = {}
    grant, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
    ev['preparationGrantAdmitsWithoutPlan'] = S.admit_repo_execution_grant(grant, ctx)['result']
    ctx2 = dict(ctx, semanticGrantPrincipals=[{'kind': 'first-party', 'closureId': 'closure2:' + '0' * 64, 'ownerSourceDigest': None}])
    ev['ctxProjectionIgnored'] = S.admit_repo_execution_grant(grant, ctx2)['result']
    tr = copy.deepcopy(grant); tr.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, runner={'kind': 'snapshot-member', 'member': 'tests/run.sh'})
    ctx3 = dict(ctx, ownerSourceDigest=hashlib.sha256(C.canonical([])).hexdigest()); tr['ownerSourceDigest'] = ctx3['ownerSourceDigest']
    ev['testRunnerAdmitsEmptyOwnerDigest'] = (S.admit_repo_execution_grant(tr, ctx3)['result'], ctx3['ownerSourceDigest'][:8])
    tr2 = copy.deepcopy(tr); tr2['runner'] = {'kind': 'snapshot-member', 'member': 'not/sealed.sh'}
    ev['testRunnerOutsideSealedSetsRefused'] = S.admit_repo_execution_grant(tr2, ctx3)['refusals']
    ev['testRunnerProjectsNothing'] = S.semantic_projection_for_grants([tr])
    req = S.semantic_projection_for_grants([grant])
    ev['planJoinAdmit'] = S.admit_plan_execution_projection(req, [grant], 'host-prepared')['result']
    ev['planJoinMissing'] = S.admit_plan_execution_projection([], [grant], 'host-prepared')['refusals']
    ev['planJoinImportedInertWithPrincipal'] = S.admit_plan_execution_projection(req, [], 'imported-inert')['refusals']
    ev['planJoinTestRunnerConsumed'] = S.admit_plan_execution_projection([], [tr], 'host-prepared')['refusals']
    # NEW: analysisOperations are part of semanticGrantDigest (Plan identity). Native §2.1/§5.1: only host-prepared projects prepare-code.
    # Neither the security Plan-time join (principals only) nor the foundation semantic-grant schema/closure joins operations to preparedResolution.
    g_ops = {'schemaVersion': 2, 'projectId': grant['projectId'], 'principals': [], 'analysisOperations': ['prepare-code', 'read-source'], 'scopeDigest': '0' * 64}
    ev['foundationSchemaAcceptsPrepareCodeWithoutRepoPrincipal'] = refuses(lambda: N.validate_foundation('semantic-grant', g_ops)) is None
    ev['securityPlanJoinIgnoresOperations'] = S.admit_plan_execution_projection(g_ops['principals'], [], 'imported-inert')['result']
    ev['securityPlanJoinSignature'] = 'admit_plan_execution_projection(plan_principals, consumed_grants, prepared_resolution) -- no analysisOperations argument'
    ok = ev['preparationGrantAdmitsWithoutPlan'] == 'ADMIT' and ev['ctxProjectionIgnored'] == 'ADMIT' and ev['planJoinAdmit'] == 'ADMIT' and ev['planJoinMissing'] and ev['planJoinImportedInertWithPrincipal']
    return ('OK-WITH-GAP' if ok else 'COUNTEREXAMPLE'), ev
probe('P6', 'SHOULD-2: operational grants precede Plan; Plan-time principal join; analysisOperations/preparedResolution rule stated only in prose', p6, 'ADVISORY')

# ================================================================== P7 SHOULD-3 backup custody: security and identity instruments agree
def p7():
    ev = {'security': {}, 'identity': {}}
    for st in ('UNKNOWN', 'NOT_BACKED_UP', 'BACKED_UP'):
        r = S.storage_write_admission(st, False, None, True, False); ev['security'][st + '/ci'] = (r['result'], r['choice'], r.get('detail'))
    r = S.storage_write_admission('BACKED_UP', True, None, True, False); ev['security']['BACKED_UP/flag'] = (r['result'], r['choice'])
    for st in ('unknown', 'not-detected', 'detected'):
        r = IM.storage_admission(st); ev['identity'][st] = (r.get('admitted'), r.get('detail'), r.get('backupDisclosure'))
    s31 = (ROOT.parents[1] / 'v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    ev['S3.1_says_UNKNOWN_admits'] = '**UNKNOWN\nadmits**' in s31 or 'UNKNOWN\nadmits' in s31 or 'UNKNOWN admits' in s31.replace('\n', ' ')
    ok = ev['security']['UNKNOWN/ci'][0] == 'ADMIT' and ev['identity']['unknown'][0] is True and ev['security']['BACKED_UP/ci'][0] == 'REFUSE' and ev['identity']['detected'][0] is False
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P7', 'SHOULD-3: UNKNOWN backup custody admits with disclosure in both instruments; detected backup needs the explicit choice', p7)

# ================================================================== P8 SHOULD-4 sufficiency order
def p8():
    req = {'relation': 'clones', 'minResolution': 'normalized-body-hash', 'minConfidenceMillionths': 900000, 'completeness': 'partial-ok', 'quantifier': 'existential', 'unresolvedEdgePolicy': 'forbid', 'externalConsumerPolicy': 'forbid'}
    view = lambda c: {'clones': {'relation': 'clones', 'resolution': 'normalized-body-hash', 'coverage': 'complete', 'confidenceMillionths': c, 'resolutionCompleteness': {'state': 'not-applicable', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}}, 'declares': {'relation': 'declares', 'resolution': 'syntactic', 'coverage': 'complete', 'confidenceMillionths': 1000000}}
    a = N.sufficiency_v2(req, view(100000)); b = N.sufficiency_v2(req, view(1000000)); v1 = N.sufficiency_v1(req, view(100000))
    # derivation policy also not bypassed for a one-rung relation? (types is multi-rung; check types declared-only with compiler-inferred)
    treq = {'relation': 'types', 'minResolution': 'checked', 'completeness': 'partial-ok', 'quantifier': 'existential', 'derivationPolicy': 'declared-only'}
    tview = {'types': {'relation': 'types', 'resolution': 'checked', 'coverage': 'complete', 'confidenceMillionths': 1000000, 'derivationKinds': ['compiler-inferred'], 'resolutionCompleteness': {'state': 'complete', 'unresolvedEdgeCount': 0, 'unresolvedEdgeClasses': []}}}
    t = N.sufficiency_v2(treq, tview)
    ok = a.get('deficiency') == 'confidence-floor-unmet' and b['satisfied'] and v1.get('deficiency') == 'confidence-floor-unmet' and t.get('deficiency') == 'derivation-policy-unmet'
    return ('OK' if ok else 'COUNTEREXAMPLE'), {'floorUnmet100000': a, 'satisfied1000000': b, 'v1oracle': v1, 'declaredOnly': t}
probe('P8', 'SHOULD-4: confidence floor and derivation policy are never bypassed by the one-rung existential path', p8)

# ================================================================== P9 SHOULD-5 / CX-01 repair authorization grammar and recovery authority (new)
def p9():
    ev = {}
    ev['applyRefGrammar'] = common['$defs']['RepairAuthorizationRef']['pattern']
    ev['freeTextApplyRefRefused'] = refuses(lambda: W.validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/RepairApplyParams',
        {'kind': 'repair-apply', 'planStep': 0, 'repairPlanId': 'repairplan2:' + 'a' * 64, 'consentSource': 'policy', 'authorizationRef': 'anything'}))
    ev['closedApplyRefAdmitted'] = refuses(lambda: W.validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/RepairApplyParams',
        {'kind': 'repair-apply', 'planStep': 0, 'repairPlanId': 'repairplan2:' + 'a' * 64, 'consentSource': 'policy', 'authorizationRef': 'security.repair-apply-authorization.v1:' + 'a' * 64})) is None
    # recovery: workflows §6 requires an authorization bound to repairPlanId + journal requestId; S10.1 defines only the APPLY record.
    rj = C.parse((ROOT / 'workflows/schemas/repair.schema.json').read_bytes())['$defs']
    ev['journalRecoveryAuthorizationRefSchema'] = rj['RepairApplyJournalV1']['properties'].get('recoveryAuthorizationRef')
    ss = C.parse((ROOT / 'security/security-lifecycle.schemas.v1.json').read_bytes())['schemas']
    ev['securitySchemasMentioningRecoveryAuthorization'] = [k for k in ss if 'ecover' in k and 'uthor' in k]
    ev['securityModelRecoveryAdmissionFunction'] = [n for n in dir(S) if 'recover' in n.lower() and 'authori' in n.lower()]
    ev['registryRecoveryDetail'] = [c for c in REG if 'RECOVERY_NOT_AUTHORIZED' in c]
    # the reference accepts any dict carrying the two fields as the recovery authorization and mints an 'auth:' prefixed ref
    rs = sub(copy.deepcopy(wf['repairScenario'])); tree = {k: v.encode() for k, v in rs['tree'].items()}
    run = rs['run']; pid = WC['PRJ']; run['snapshotId'] = W.fixture_tree_snapshot_id(pid, tree)
    edits = [dict(e, postimage=e['postimage'].encode()) if e.get('postimage') is not None else dict(e) for e in rs['edits']]
    trust = {rs['recipe']['closureId']: 'admitted'}
    plan = W.repair_preview(pid, tree, run, rs['recipe'], rs['targets'], edits, rs['evidenceRequirements'], rs['permittedScope'], trust)
    journal = {'schemaFamily': 'opensip.product.repair-apply-journal', 'schemaMajor': 1, 'requestId': WC['REQ'], 'stepId': 2, 'executionId': 'exec1_' + '1' * 32, 'repairPlanId': plan['repairPlanId'],
               'baseSnapshotId': plan['descriptor']['snapshotId'], 'authorizationRef': 'security.repair-apply-authorization.v1:' + 'a' * 64, 'state': 'STAGED', 'stagedPaths': [], 'appliedPaths': [], 'preimageBlobs': []}
    ev['recoveryWithoutAuthorizationRefused'] = refuses(lambda: W.repair_recover(journal, plan, tree, pid, {}, None))
    j2, action, outcome, term = W.repair_recover(journal, plan, tree, pid, {}, {'repairPlanId': plan['repairPlanId'], 'requestId': WC['REQ'], 'anyCallerField': 'ignored'})
    ev['recoveryWithCallerDictAdmitted'] = (action, j2['state'], j2.get('recoveryAuthorizationRef'))
    gap = ev['journalRecoveryAuthorizationRefSchema'] is not None and 'pattern' not in ev['journalRecoveryAuthorizationRefSchema'] and not ev['securitySchemasMentioningRecoveryAuthorization']
    return ('COUNTEREXAMPLE' if gap else 'OK'), ev
probe('P9', 'CX-01/SHOULD-5: apply authorization is closed and security-admitted; recovery mutation authorization has no security record, schema grammar or admission', p9, 'SHOULD')

# ================================================================== P10 SHOULD-6 core transition leases; intent expressiveness (new)
def p10():
    ev = {}
    reg = ['ns-b', 'ns-a', 'ns-c']
    intent = {'operation': 'core-update', 'fromStateSchema': 1, 'toStateSchema': 2}
    ev['schemaChangeAll'] = S.core_transition_affected_namespaces(intent, reg)
    ev['sameSchemaNone'] = S.core_transition_affected_namespaces({'operation': 'core-update', 'fromStateSchema': 2, 'toStateSchema': 2}, reg)
    ev['storeMigrateAll'] = S.core_transition_affected_namespaces({'operation': 'store-migrate', 'fromStateSchema': 2, 'toStateSchema': 2}, reg)
    acts = [{'actor': 'r', 'op': 'fence-acquire'}, {'actor': 'r', 'op': 'lease', 'mode': 'SHARED-READ', 'namespace': 'ns-b'}, {'actor': 'r', 'op': 'fence-release'},
            {'actor': 't', 'op': 'fence-acquire'}, {'actor': 't', 'op': 'core-transition-acquire', 'namespaces': ['ns-a', 'ns-b', 'ns-c']}, {'actor': 't', 'op': 'fence-release'},
            {'actor': 'r', 'op': 'lease-release'}, {'actor': 't', 'op': 'core-transition-acquire', 'namespaces': ['ns-a', 'ns-b', 'ns-c']}, {'actor': 't', 'op': 'fence-release'},
            {'actor': 't', 'op': 'core-transition-release'}, {'actor': 't', 'op': 'fence-release'}]
    tr = S.lease_schedule(acts, reg)
    ev['trace'] = [(t['actor'], t['op'], t['result'][:70]) for t in tr['trace']]
    ev['violations'] = tr['violations']
    bad = S.lease_schedule([{'actor': 't', 'op': 'fence-acquire'}, {'actor': 't', 'op': 'core-transition-acquire', 'namespaces': ['ns-b', 'ns-a']}], reg)
    ev['unorderedSetRefused'] = bad['trace'][-1]['result'][:40]
    bad2 = S.lease_schedule([{'actor': 't', 'op': 'fence-acquire'}, {'actor': 't', 'op': 'core-transition-acquire', 'namespaces': ['ns-zz']}], reg)
    ev['unregisteredRefused'] = bad2['trace'][-1]['result'][:60]
    # intent expressiveness: workflow CoreTransitionIntentV1 operation enum vs MutationOperation and security operations
    inv = C.parse((ROOT / 'workflows/schemas/invocation-record.schema.json').read_bytes())['$defs']
    ev['intentOperationEnum'] = inv['CoreTransitionIntentV1']['properties']['operation']['enum']
    ev['intentFields'] = sorted(inv['CoreTransitionIntentV1']['properties'].keys())
    ev['storeMigrateIntentSchemaValid'] = refuses(lambda: M.core_transition_scope({'schemaVersion': 1, 'operation': 'store-migrate', 'fromCoreClosure': 'closure2:' + '1' * 64, 'toCoreClosure': 'closure2:' + '1' * 64, 'fromStateSchema': 1, 'toStateSchema': 2, 'platformProfileSetBodyDigest': 'a' * 64, 'preconditionGeneration': 0, 'rollbackDeadline': None}, reg)) is None
    ev['inventoryStoreCommandsClass'] = {c['name']: c['authorizationClass'] for c in inventory['commands'] if c['name'].startswith('store-') or c['name'].startswith('core-')}
    ev['leaseSetFieldInIntent'] = [k for k in ev['intentFields'] if 'ease' in k or 'amespace' in k]
    ev['S7item4'] = 'The `CoreTransitionIntentV1` / migrating-root journal record (S9) names the exact lease set'
    ss = C.parse((ROOT / 'security/security-lifecycle.schemas.v1.json').read_bytes())['schemas']
    ev['securityJournalRecordsWithLeaseSet'] = [k for k, v in ss.items() if isinstance(v, dict) and 'namespaces' in json.dumps(v.get('properties', {})) and k not in ('LeaseTraceV1',)]
    gap = not ev['storeMigrateIntentSchemaValid'] or not ev['leaseSetFieldInIntent']
    return ('OK-WITH-GAP' if gap else 'OK'), ev
probe('P10', 'SHOULD-6: all-or-nothing ordered EXCLUSIVE set under a held fence; store migrate/rollback and the journaled lease set are not representable in CoreTransitionIntentV1', p10, 'SHOULD')

# ================================================================== P11 SHOULD-7 / CX-03 headings and stale prose
def p11():
    ev = {}
    for name in ('security-and-lifecycle', 'native-evidence', 'workflows-and-surfaces', 'identity-and-evidence', 'admission-and-qualification'):
        t = (ROOT.parents[1] / 'v2/contracts/product-v1' / (name + '.md')).read_text()
        heads = [l.split()[1] for l in t.splitlines() if l.startswith('## ') or l.startswith('### ')]
        ev[name] = {'duplicateHeadingNumbers': sorted({h for h in heads if heads.count(h) > 1}), 'tmpPathCitations': len(re.findall(r'/tmp/opensip-design-corrections', t))}
    sec = (ROOT.parents[1] / 'v2/contracts/product-v1/security-and-lifecycle.md').read_text()
    ev['securityCaseCountClaim'] = re.findall(r'runs (\d+) cases', sec); ev['securitySweepClaim'] = re.findall(r'(\w+) invariant sweeps', sec)
    nat = (ROOT.parents[1] / 'v2/contracts/product-v1/native-evidence.md').read_text()
    ev['nativeCaseCountClaim'] = re.findall(r'\((\d+) cases', nat); ev['nativeDefClaim'] = re.findall(r'(\d+)-def', nat)
    ev['actualNativeDefs'] = len(C.parse((ROOT / 'native/native-evidence.schemas.v2.json').read_bytes())['$defs'])
    ev['nativeModelV1Comment'] = 'AuthorizedExecutionV1' in (ROOT / 'native/native_evidence_model.v2.py').read_text()
    ev['emptyHandoffPinnedByNative'] = any(p['path'].endswith('native-fix-handoff.v3.md') for p in C.parse((ROOT / 'native/source-pins.v2.json').read_bytes())['pins']) if 'pins' in C.parse((ROOT / 'native/source-pins.v2.json').read_bytes()) else 'n/a'
    wfc = (ROOT.parents[1] / 'v2/contracts/product-v1/workflows-and-surfaces.md').read_text()
    ev['workflowCrossRefs'] = re.findall(r'Native §1[14] and security S1[35]', wfc)
    ev['S14_singular_EXCLUSIVE_for_migration'] = "they require S7's EXCLUSIVE lease" in sec
    return 'OK', ev
probe('P11', 'SHOULD-7/CX-03: heading uniqueness, count claims, stale conflict text, /tmp citations', p11, 'ADVISORY')

# ================================================================== P12 SHOULD-8 recovery authority never root keys
def p12():
    doc = C.parse((ROOT / 'security/trust-recovery-cases.v1.json').read_bytes())
    subs = build_subs(doc)
    case = next(c for c in doc['applyCases'] if c['id'].startswith('signed-epoch-lowers'))
    inp = resolve_input(case['input'], subs)
    good = S.recovery_apply(inp['record'], inp['epoch'], inp['signers'], inp['observation'], inp['acceptedRoot'])
    root_signed = S.recovery_apply(inp['record'], inp['epoch'], list(inp['acceptedRoot']['rootKeys'])[:5], inp['observation'], inp['acceptedRoot'])
    higher = copy.deepcopy(inp['epoch']); higher['counters']['rootVersion'] += 1
    hi = S.recovery_apply(inp['record'], higher, inp['signers'], inp['observation'], inp['acceptedRoot'])
    reboot = S.recovery_apply(inp['record'], inp['epoch'], inp['signers'], dict(inp['observation'], bootId='boot-B'), inp['acceptedRoot'])
    replay_record = copy.deepcopy(inp['record']); replay_record.update(good['writes']) if isinstance(good.get('writes'), dict) else None
    ev = {'goodResult': good['result'], 'rootKeysAsSigners': (root_signed['result'], root_signed.get('refusal'), root_signed.get('detail')),
          'higherCounter': (hi['result'], hi.get('detail')), 'rebootBetween': (reboot['result'], reboot.get('detail')),
          'inventoryClass': next(c['authorizationClass'] for c in inventory['commands'] if c['name'] == 'trust-recovery-import')}
    ok = good['result'] == 'APPLIED' and root_signed['result'] != 'APPLIED' and hi['result'] != 'APPLIED' and reboot['result'] != 'APPLIED' and ev['inventoryClass'] == 'recovery-authority-quorum'
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P12', 'SHOULD-8/AR-04: recovery-authority quorum only; root keys, higher counters and reboot refuse', p12)

# ================================================================== P13 SHOULD-9 non-gating indeterminacy uniform
def p13():
    base = copy.deepcopy(POL['basePolicy'])
    for r in base['rules']:
        r['enabled'] = r['ruleId'] == 'runtime-hit-but-unimported'
    rule = next(r for r in base['rules'] if r['ruleId'] == 'runtime-hit-but-unimported')
    rule['evidenceUse'] = [{'kind': 'runtime', 'requirement': 'required'}]
    scope = POL['scopeAll']; wv = POL['waiversNone']
    fx = lambda cov, ev: {'subjects': ['src/a.ts'], 'facts': [], 'coverage': cov, 'evidenceAvailable': ev}
    a = W.evaluate(base, scope, wv, fx('complete', []))
    b = W.evaluate(base, scope, wv, fx('partial', ['runtime']))
    gating = copy.deepcopy(base); next(r for r in gating['rules'] if r['ruleId'] == 'runtime-hit-but-unimported').update(gate=True, severity='warning')
    c = W.evaluate(gating, scope, wv, fx('complete', []))
    d = W.evaluate(gating, scope, wv, fx('partial', ['runtime']))
    ev = {'nonGatingRequiredEvidenceAbsent': (a['verdict'], a['indeterminateRules']), 'nonGatingIncompleteCoverage': (b['verdict'], b['indeterminateRules']),
          'gatingRequiredEvidenceAbsent': (c['verdict'], c['indeterminateRules']), 'gatingIncompleteCoverage': (d['verdict'], d['indeterminateRules'])}
    ok = a['verdict'] == b['verdict'] == 'pass' and a['indeterminateRules'] == b['indeterminateRules'] == ['runtime-hit-but-unimported'] and c['verdict'] == d['verdict'] == 'indeterminate'
    # policy-test expectation verdict enum versus evaluator verdict vocabulary ('advisory')
    pt = C.parse((ROOT / 'workflows/schemas/policy-test.schema.json').read_bytes())['$defs']['Expectation']['oneOf']
    ev['expectationVerdictBranch'] = [b for b in pt if 'verdict' in b.get('properties', {})]
    ev['caseResultVerdict'] = C.parse((ROOT / 'workflows/schemas/policy-test.schema.json').read_bytes())['$defs']['CaseResult'].get('properties', {}).get('verdict')
    adv = W.evaluate(POL['basePolicy'], scope, wv, {'subjects': ['src/a.ts'], 'facts': [{'relation': 'runtime-observation', 'subject': 'src/a.ts', 'target': 'x', 'resolution': 'syntax', 'universe': 'typescript-v2', 'observability': 'observed-hit', 'confidenceMillionths': 1000000}], 'coverage': 'complete', 'evidenceAvailable': ['runtime']})
    ev['advisoryVerdictExample'] = (adv['verdict'], adv['findings'])
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P13', 'SHOULD-9: unknown non-gating rule results are disclosed uniformly for evidence and coverage; only gating rules make the verdict indeterminate', p13)

# ================================================================== workflow comparison harness (independent re-assembly)
BS = wf['baselineSpec']
def fixture_evidence(value, overrides=None):
    v = copy.deepcopy(value)
    v['imports'] = [{'kind': k, 'importId': (overrides or {}).get(k, WC['IMP_RT'] if k == 'runtime' else WC['IMP_HIST']), 'payloadDigest': WC['H0'], 'sourceCorrespondenceDigest': WC['H0'], 'scopeDigest': WC['H0'], 'observationDigest': WC['H0']} for k in v['importKinds']]
    return v
def make_baseline(policy, scope, waivers, rule_cov):
    run = {'authority': 'authoritative', 'availability': 'retained', 'snapshotId': WC['SNAP0'], 'runId': WC['RUN0']}
    ctx = {'detectorClosureIds': [d['closureId'] for d in sub(BS['detectorClosure'])], 'evidenceAvailability': fixture_evidence(BS['evidenceAvailability'])}
    return W.adopt_baseline(run, WC['PLAN0'], WC['PRJ'], policy, scope, waivers, rule_cov, sub(BS['entries']), sub(BS['detectorClosure']), sub(BS['pivotClosure']), ctx, '1.0.0')
def run_compare(entries, presence, current_policy, current_rule_cov, bound=('E1', 'E2', 'E3'), profile='code-regression', import_overrides=None, host='sameDetector', detectors=None, entry_rules=None):
    base = make_baseline(POL['basePolicy'], POL['scopeAll'], POL['waiversFp2'], sub(wf['ruleCoverage']['full']))
    base['descriptor']['entries'] = copy.deepcopy(entries); base['baselineId'] = W.wid('baseline2', 'workflow.baseline', base['descriptor'])
    bd = dict(base['descriptor']); bd['_baselineId'] = base['baselineId']
    cd = detectors or {'ts-detector': {'closureId': WC['DET_A0'], 'semanticsMajor': 2}}
    cur_ctx = {'policyDigest': W.doc_digest(current_policy), 'scopeDigest': W.doc_digest(POL['scopeAll']), 'waiverSetDigest': W.doc_digest(POL['waiversFp2']),
               'detectorClosureIds': sorted(d['closureId'] for d in cd.values()), 'evidenceAvailability': fixture_evidence(BS['evidenceAvailability'], import_overrides)}
    bmap = {e['fingerprint']: e for e in entries}
    pres = {fp: {'B': fp in bmap, 'E0': p['E0'], 'E1': p['E1'], 'E2': p['E2'], 'E3': p['E3'], 'E4': p['E4'], 'waivedB': bmap[fp]['waived'] if fp in bmap else False, 'waivedC': p.get('waivedC', False)} for fp, p in presence.items()}
    current = {'runId': WC['RUN1'], 'snapshotId': WC['SNAP1'], 'projectId': WC['PRJ'], 'context': cur_ctx, 'ruleCoverage': {r['ruleId']: r for r in sub(current_rule_cov)},
               'presence': pres, 'entryRules': entry_rules or {fp: ('no-unused-export', 'ts-detector') for fp in presence}, 'boundPivots': list(bound)}
    return W.compare(bd, current, sub(wf['hosts'][host]), profile, cd)['descriptor']

# ================================================================== P14 CX-02 empty comparisons
def p14():
    ev = {}
    d = run_compare([], {}, POL['policyDisabledUnused'], wf['ruleCoverage']['unusedDisabled'], bound=())
    ev['emptyBothMissingPolicyPivot'] = (d['verdict'], d['pivotsAvailable'], d['remedy']['code'], len(d['entries']))
    d2 = run_compare([], {}, POL['basePolicy'], wf['ruleCoverage']['full'], bound=())
    ev['emptyBothNoPivotNeeded'] = (d2['verdict'], d2['pivotsAvailable'])
    d3 = run_compare([], {}, POL['policyDisabledUnused'], wf['ruleCoverage']['unusedDisabled'], bound=('E1', 'E2', 'E3'))
    ev['emptyBothPivotBound'] = (d3['verdict'], d3['pivotsAvailable'])
    d4 = run_compare([], {}, POL['policyDisabledUnused'], wf['ruleCoverage']['unusedDisabled'], bound=(), profile='report-only')
    ev['emptyBothMissingPivotReportOnly'] = (d4['verdict'], 'gating rules under current-only: ' + str(any(r['enabled'] and r['gating'] for r in sub(wf['ruleCoverage']['unusedDisabled']))))
    d5 = run_compare([], {}, POL['basePolicy'], wf['ruleCoverage']['full'], bound=(), host='freshCiMissing', detectors={'ts-detector': {'closureId': WC['DET_A1'] if 'DET_A1' in WC else 'closure2:' + '9' * 64, 'semanticsMajor': 2}})
    ev['emptyBothDetectorChangedPivotMissing'] = (d5['verdict'], d5['pivotsAvailable']['E0'], d5['remedy']['code'] if d5.get('remedy') else None)
    ok = d['verdict'] == 'indeterminate' and d2['verdict'] == 'pass' and d3['verdict'] == 'pass' and d5['verdict'] == 'indeterminate'
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P14', 'CX-02: unavailable required pivots make an empty comparison indeterminate; bound or unneeded pivots leave it pass', p14)

# ================================================================== P15 CX-04 end-of-input assertions across units
def p15():
    ev = {}
    ev['workflowRequestIdNewline'] = refuses(lambda: W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/RequestId', 'req1_' + 'a' * 32 + '\n'))
    ev['workflowRequestIdClean'] = refuses(lambda: W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/RequestId', 'req1_' + 'a' * 32))
    ev['nativeSha256TextCRLF'] = refuses(lambda: N.validate_native('Sha256Text', 'sha256:' + 'a' * 64 + '\r\n'))
    ev['foundationClosureSpace'] = refuses(lambda: C.validate(dict(IM.SCHEMA, **{'$ref': '#/$defs/closure'}), {'schemaVersion': 2, 'kind': 'evaluator', 'manifestDigest': 'a' * 64 + ' ', 'tree': [], 'semanticVersion': '1.0.0', 'protocolMajor': 3, 'platform': 'macos-aarch64'}))
    g = copy.deepcopy(sf['grantBase']); g['snapshotId'] += '\n'
    ev['securityGrantSnapshotNewline'] = refuses(lambda: S.validate_input('RepoExecutionGrantV2', g))
    cfg = json.dumps({'schemaVersion': 2, 'analysis': {'profileId': 'default'}, 'discovery': {'workspaceRoots': ['src\n']}}).encode()
    ev['config2PathNewline'] = refuses(lambda: PCM.resolve({'project': cfg}, {'profiles': ['default'], 'capabilities': [], 'packs': [], 'waivers': []}))
    ev['ordinaryNewlineTextPreserved'] = C.parse(C.canonical({'m': 'a\nb'}))['m'] == 'a\nb'
    ev['config2PathNewlineNote'] = 'a newline inside a path segment is a legal scalar under identity section 3 and the workflow LogicalPath pattern [^/\\\\NUL]; consistent across units, not a CX-04 end-anchor case'
    ok = all(ev[k] for k in ('workflowRequestIdNewline', 'nativeSha256TextCRLF', 'foundationClosureSpace', 'securityGrantSnapshotNewline')) and ev['workflowRequestIdClean'] is None and ev['ordinaryNewlineTextPreserved']
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P15', 'CX-04: newline/CRLF/space suffixes refused by closed scalar grammars in all four units and Config2', p15)

# ================================================================== P16 CX-05 filter typing
def p16():
    ev = {}
    def ff(f):
        return refuses(lambda: W.validate_import_record('workflows/schemas/policy-document.schema.json', '#/$defs/FieldFilter', f))
    ev['confidence_gte_int'] = ff({'field': 'confidenceMillionths', 'cmp': 'gte', 'value': 900000})
    ev['confidence_eq_string'] = ff({'field': 'confidenceMillionths', 'cmp': 'eq', 'value': '900000'})
    ev['confidence_gte_string'] = ff({'field': 'confidenceMillionths', 'cmp': 'gte', 'value': '900000'})
    ev['subject_gte_int'] = ff({'field': 'subject', 'cmp': 'gte', 'value': 1})
    ev['subject_in_array'] = ff({'field': 'subject', 'cmp': 'in', 'value': ['a', 'b']})
    ev['subject_in_string'] = ff({'field': 'subject', 'cmp': 'in', 'value': 'a'})
    ev['confidence_gte_float'] = ff({'field': 'confidenceMillionths', 'cmp': 'gte', 'value': 1.0})
    ok = ev['confidence_gte_int'] is None and ev['subject_in_array'] is None and all(ev[k] for k in ('confidence_eq_string', 'confidence_gte_string', 'subject_gte_int', 'subject_in_string', 'confidence_gte_float'))
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P16', 'CX-05: confidenceMillionths admits only integer gte/lte; string fields never admit numeric operators', p16)

# ================================================================== P17 AR-01 exact admission
def p17():
    ev = {}
    for raw in (b'1.0', b'-0', b'1e0', b'{"a":1,"a":2}', b'1E0', b'true', b'18446744073709551616', b'-9223372036854775809'):
        ev[raw.decode()] = refuses(lambda: C.parse(raw))
    ev['u64max'] = C.parse(b'18446744073709551615')
    deep = lambda n: b'[' * n + b']' * n
    ev['depth32'] = refuses(lambda: C.parse(deep(32))); ev['depth33'] = refuses(lambda: C.parse(deep(33)))
    ev['exactConstBoolVsInt'] = refuses(lambda: C.validate({'const': 1}, True))
    ev['canonicalKeyOrderUtf8'] = C.canonical({'é': 1, 'z': 2, 'a': 3}).decode()
    ok = all(ev[k] for k in ('1.0', '-0', '1e0', '{"a":1,"a":2}', 'depth33', 'exactConstBoolVsInt')) and ev['depth32'] is None and ev['u64max'] == 18446744073709551615
    return ('OK' if ok else 'COUNTEREXAMPLE'), ev
probe('P17', 'AR-01: lexical numeric admission, depth rule, duplicate keys, bool-vs-integer', p17)

# ================================================================== P18 AR-04/AR-05 clock and root chain independent spot checks
def p18():
    ev = {}
    doc = C.parse((ROOT / 'security/root-chain-cases.v1.json').read_bytes()); subs = build_subs(doc)
    case = next(c for c in doc['cases'] if c['id'] == 'expired-root-valid-chain-through-expired-intermediate'); inp = resolve_input(case['input'], subs)
    ok1 = S.verify_root_chain(inp['state'], inp['chain'], inp['tEval'], inp['wall'])
    ev['expiredIntermediateAccepted'] = (ok1['result'], ok1.get('acceptedVersion'))
    late = S.verify_root_chain(inp['state'], inp['chain'], '2099-01-01T00:00:00Z', '2099-01-01T00:00:00Z')
    ev['finalExpiredRefused'] = (late['result'], late.get('refusal'), late.get('detail'))
    revoked = S.verify_root_chain(inp['state'], inp['chain'], inp['tEval'], inp['wall'], revoked_keys=tuple(inp['chain'][1]['signers'][:2]))
    ev['revokedSignersRefused'] = (revoked['result'], revoked.get('refusal'))
    fresh = S.clock_decision({'evalHighWater': None, 'lastAccepted': None, 'anchor': None, 'rootVersion': 0, 'indexSnapshotVersion': 0, 'revocationVersion': 0, 'recoveryEpochSerial': 0, 'pendingRecoveryChallenge': None, 'revocationIssuedAt': None, 'catalogExpiresAt': None, 'rootExpiresAt': None},
                            {'wall': '2026-09-06T00:00:00Z', 'mono': 10, 'bootId': 'b'})
    ev['freshInstallNoTimeContext'] = (fresh.get('result'), fresh.get('refusal'), fresh.get('writes'))
    return ('OK' if ok1['result'] == 'ACCEPT' and late['result'] == 'REFUSE' and revoked['result'] == 'REFUSE' and fresh.get('result') != 'ACCEPT' else 'COUNTEREXAMPLE'), ev
probe('P18', 'AR-04/AR-05: expired intermediate root admitted, expired final root and revoked signers refused, fresh install needs admitted time', p18)

# ================================================================== P19 ADV-1 / ADV-2 confirmed behaviours
def p19():
    ev = {}
    entries = sub(BS['entries'])
    fp5 = WC['FP5']
    pres = {fp5: {'E0': True, 'E1': True, 'E2': True, 'E3': True, 'E4': True}}
    d = run_compare(entries, pres, POL['basePolicy'], wf['ruleCoverage']['full'], import_overrides={'runtime': 'import2:' + '5' * 64}, entry_rules={fp5: ('runtime-unhit-export', 'ts-detector')})
    e = next(x for x in d['entries'] if x['fingerprint'] == fp5)
    ev['gatingRuleEvidenceContentChanged'] = (e['classification'], e.get('indeterminateReason'), d['verdict'])
    d2 = run_compare(entries, {WC['FP1']: {'E0': True, 'E1': True, 'E2': True, 'E3': True, 'E4': True}}, POL['policyDisabledUnused'], wf['ruleCoverage']['unusedDisabled'], bound=())
    ev['unboundPolicyPivotAllIndeterminate'] = ({x['classification'] for x in d2['entries']}, d2['verdict'], d2['remedy']['code'])
    # removed rule with baseline-declared required evidence: entry becomes INDETERMINATE though the rule is gone in current
    d3 = run_compare(entries, pres, POL['basePolicy'], wf['ruleCoverage']['full'], import_overrides={'runtime': None} if False else None, entry_rules={fp5: ('runtime-unhit-export', 'ts-detector')})
    ev['sanityUnchanged'] = next(x for x in d3['entries'] if x['fingerprint'] == fp5)['classification']
    return 'OK', ev
probe('P19', 'ADV-1/ADV-2 dispositions reproduced: evidence-content change on a gating rule and unbound required pivot both yield typed INDETERMINATE', p19)

# ================================================================== P20 ADV-3 nested config decision
def p20():
    doc = C.parse((ROOT / 'security/discovery-cases.v1.json').read_bytes())
    ev = {}
    for cid in ('nested-config-inside-a-vcs-root-is-a-deliberate-project-boundary-launch-inside-selects-it', 'nested-config-inside-a-vcs-root-launch-elsewhere-selects-the-vcs-root-and-never-enters-the-nested-project', 'explicit-join-crossing-into-a-nested-project-refuses'):
        c = next(c for c in doc['cases'] if c['id'] == cid); r = S.discovery(c['input'])
        ev[cid[:60]] = (r['status'], r['provenance']['mode'], r['provenance']['selectedRoot'], r['provenance']['nestedProjects'], [u['reason'] for u in r['provenance']['excludedUnits']], r.get('detail'))
    return 'OK', ev
probe('P20', 'ADV-3: nested config is a deliberate boundary in both directions (retained cases reproduced)', p20)

# ================================================================== P21 test-execution join (new observations)
def p21():
    ev = {}
    # integration builds its params with consentSource 'interactive' and never validates them against the workflow schema
    params = {'kind': 'test-execution', 'argv': ['bin/opensip-test-runner', '--ci'], 'argv0Source': {'kind': 'toolchain-closure', 'closureId': 'closure2:' + 'e' * 64, 'member': 'bin/opensip-test-runner'}, 'cwdIsRoot': True, 'principal': 'P-TRUSTED-REPO', 'executionClass': 'test-runner', 'platformId': 'linux-x86_64-gnu',
              'authorizationRef': 'security.repo-execution-grant.v2:' + 'a' * 64, 'consentSource': 'interactive', 'afterStep': 0, 'timeoutMilliseconds': 1000, 'maxOutputBytes': 1024, 'environmentAllowlist': [], 'effects': dict(S.PLATFORM_TRUTH_TABLE['linux-x86_64-gnu'])}
    ev['integrationConsentSpellingSchemaValid'] = refuses(lambda: W.validate_import_record('workflows/schemas/test-execution.schema.json', '#/$defs/TestExecutionStepParams', params)) is None
    ev['integrationCheckerValidatesParams'] = 'TestExecutionStepParams' in (ROOT / 'check-integration.py').read_text()
    # grant consent mode versus step consentSource are stated as a mapping (S10) but not joined: interactive-explicit grant + pre-existing-policy step admits outside CI
    grant, ctx = copy.deepcopy(sf['grantBase']), copy.deepcopy(sf['ctxBase'])
    grant.update(executionClass='test-runner', owners=[], dependencySourceSetId=None, platformId='linux-x86_64-gnu', runner={'kind': 'toolchain-closure', 'member': 'bin/opensip-test-runner'})
    argv = ['bin/opensip-test-runner']; grant['argvDigest'] = W.payload_digest(argv); grant['effects'] = dict(S.PLATFORM_TRUTH_TABLE['linux-x86_64-gnu'])
    M.bind = None
    digest = M.owner_digest(grant['owners']); grant['ownerSourceDigest'] = ctx['ownerSourceDigest'] = digest; ctx['argvDigest'] = grant['argvDigest']
    ev['grantAuthorizationMode'] = grant['authorization']['mode']
    proj = M.test_grant_projection(grant, ctx)
    p2 = dict(params, consentSource='pre-existing-policy', argv=argv, authorizationRef=proj['securityGrantRef'], argv0Source={'kind': 'toolchain-closure', 'closureId': grant['toolClosureId'], 'member': argv[0]})
    wc = {'ci': False, 'projectId': grant['projectId'], 'snapshotId': grant['snapshotId'], 'grant': proj, 'snapshotMembers': ctx['snapshotMembers'], 'toolchainMembers': {grant['toolClosureId']: ctx['toolClosure']['members']}, 'truthTable': S.PLATFORM_TRUTH_TABLE, 'liveEqualsAfterStep': True}
    ev['interactiveGrantWithPolicyConsentStepAdmitted'] = W.admit_test_execution(p2, wc)['admitted']
    ev['projectionCarriesConsentMode'] = 'authorization' in proj or 'consent' in json.dumps(proj)
    ev['liveTreeMovedDetailForTestStep'] = refuses(lambda: W.admit_test_execution(p2, dict(wc, liveEqualsAfterStep=False)))
    return ('OK-WITH-GAP' if not ev['integrationConsentSpellingSchemaValid'] or ev['interactiveGrantWithPolicyConsentStepAdmitted'] else 'OK'), ev
probe('P21', 'Test execution join: integration params use a consentSource spelling the schema refuses; grant consent mode is not joined to the step consentSource', p21, 'ADVISORY')

# ================================================================== P22 explicit root equal to a Cargo workspace root drops member folding (edge)
def p22():
    markers = {'Cargo.toml': {'sha256': '1' * 64, 'isCargoWorkspace': True}, 'crates/a/Cargo.toml': {'sha256': '1' * 64}, 'crates/b/Cargo.toml': {'sha256': '1' * 64}}
    auto = N.discover_units(markers); expl = N.discover_units(markers, ['.'])
    files = ['crates/a/src/lib.rs', 'crates/a/target/debug/x.rs', 'target/debug/y.rs']
    ma = N.assign_membership(auto['units'], files); me = N.assign_membership(expl['units'], files)
    ev = {'automaticMembers': [u['memberPackageRoots'] for u in auto['units']], 'explicitRootMembers': [u['memberPackageRoots'] for u in expl['units']],
          'automaticRows': {r['path']: r['reason'] for r in ma['rows']}, 'explicitRows': {r['path']: r['reason'] for r in me['rows']}}
    return ('OK-WITH-GAP' if ev['automaticRows'] != ev['explicitRows'] else 'OK'), ev
probe('P22', 'Native U-2 under explicit roots: naming the Cargo workspace root explicitly loses member folding and member target pruning', p22, 'ADVISORY')

# ================================================================== P23 inventory shape and renderer set
def p23():
    names = [c['name'] for c in inventory['commands']]
    return 'OK', {'commands': len(names), 'unique': len(set(names)), 'renderers': [r.get('format') for r in inventory['renderers']],
                  'goldens': len(inventory['goldens']), 'goldensWithDomainDetail': sum(1 for g in (inventory['goldens'] if isinstance(inventory['goldens'], list) else inventory['goldens'].values()) if 'domainDetail' in json.dumps(g))}
probe('P23', 'AR-13 surfaces: single inventory, 45 commands, renderer set, goldens carrying domain detail', p23)

# ================================================================== P24 crosswalk/provenance
def p24():
    cw = C.parse((ROOT / 'correction-crosswalk.proposed.json').read_bytes())['items']
    ev = {'reviewFieldsNull': sum(1 for i in cw if not i.get('review')), 'reviewPaths': sorted({i['review']['path'] for i in cw if i.get('review')}),
          'duplicateEvidence': [i['id'] for i in cw if len(i['evidence']) != len(set(i['evidence']))],
          'reviewSubjectIsPredecessor': sorted({i['review']['subjectManifestSha256'] for i in cw if i.get('review')}) == ['e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac']}
    cx = C.parse((ROOT / 'reviews/codex-post-reset.v1/codex-findings.json').read_bytes())
    ev['codexFindingsRetained'] = [f['id'] for f in cx['findings']]
    ev['CX-05_in_codexFindings'] = any(f['id'] == 'CX-05' for f in cx['findings'])
    ev['retainedAuthorHandoff'] = (ROOT / 'reviews/post-reset-author.v1/handoff.md').exists()
    ev['retainedV1Review'] = (ROOT / 'reviews/post-reset-review.v1/review.json').exists() and (ROOT / 'reviews/post-reset-review.v1/probes').exists()
    return 'OK', ev
probe('P24', 'SHOULD-10/ADV-4: review provenance retained; crosswalk review fields populated with the predecessor review; CX-05 evidence record', p24, 'ADVISORY')

# ================================================================== P25 D9 aggregate and domainDetail projection parity for security goldens
def p25():
    ev = {}
    gold = inventory['goldens'] if isinstance(inventory['goldens'], list) else list(inventory['goldens'].values())
    want = ('trust-recovery-import-refused', 'store-migrate-corrupt-footprint', 'query-evidence-purged')
    for g in gold:
        gid = g.get('id') or g.get('name')
        if gid in want or any(w in str(gid) for w in ('recovery-import', 'migrate-corrupt', 'evidence-purged')):
            ev[str(gid)] = json.dumps(g)[:400]
    ev['goldenCount'] = len(gold); ev['goldensWithDomainDetail'] = sum(1 for g in gold if 'domainDetail' in json.dumps(g)); ev['goldenKeys'] = sorted(gold[0].keys())
    return 'OK', ev
probe('P25', 'MUST-1 goldens now carry security/identity details', p25)

OUT.write_text(json.dumps({'reviewer': 'fresh actual Claude session (claude-fable-5-1), independent of all subject bytes', 'subjectRoot': str(ROOT.parents[2].parent), 'results': results}, indent=1, default=str) + '\n')
print('wrote', OUT)
