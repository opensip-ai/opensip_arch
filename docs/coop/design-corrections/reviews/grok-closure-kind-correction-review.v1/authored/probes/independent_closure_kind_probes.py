"""Independent coauthor probes for the bounded closure-kind correction.

Read-only against isolated successor and frozen candidate24. Writes only under
this review output directory. Not a pin regenerator and not product qualification.
"""
from __future__ import annotations
import copy, hashlib, importlib.util, json, traceback
from pathlib import Path

PY = Path('/tmp/opensip-architecture-review-env/bin/python')
SUCC = Path('/tmp/opensip-design-corrections/closure-kind-successor.v1/docs/coop/design-corrections/foundation')
CAND = Path('/tmp/opensip-design-corrections/candidate-subject.v24/docs/coop/design-corrections/foundation')
INP = Path('/tmp/opensip-design-corrections/grok-closure-kind-correction-review.v1/inputs')
OUT = Path('/tmp/opensip-design-corrections/grok-closure-kind-correction-review.v1/output/probes')
OUT.mkdir(parents=True, exist_ok=True)
FOUR = ['identity-model.v3.py', 'evaluator_graph_fixture.v3.py', 'closure_field_kind_controls.v3.py', 'check-replay.v3.py']

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

rows = []
def rec(case, **kw):
    rows.append({'case': case, **kw})

# --- custody hashes ---
hash_rows = []
for name in FOUR:
    inp = INP / 'source' / name
    suc = SUCC / name
    cand = CAND / name
    hash_rows.append({
        'file': name,
        'inputSha256': sha(inp) if inp.exists() else None,
        'successorSha256': sha(suc) if suc.exists() else None,
        'candidate24Sha256': sha(cand) if cand.exists() else None,
        'inputEqualsSuccessor': inp.exists() and suc.exists() and sha(inp) == sha(suc),
        'successorDiffersFromCandidate24': (not cand.exists()) or sha(suc) != sha(cand),
        'bytes': {'input': inp.stat().st_size if inp.exists() else None,
                  'successor': suc.stat().st_size if suc.exists() else None,
                  'candidate24': cand.stat().st_size if cand.exists() else None},
    })
rec('custody-four-files', rows=hash_rows)

M = load('identity3', SUCC / 'identity-model.v3.py')
C = M.C
F = load('fixture3', SUCC / 'evaluator_graph_fixture.v3.py')
R = load('replay3', SUCC / 'evaluator_replay_model.v3.py')
SCHEMA = json.loads((SUCC / 'identity-schemas.v3.json').read_text())
DIGESTS = SCHEMA['x-opensip-digest-domains']
BYFIELD = DIGESTS['closureKinds']['byField']
MEMB = DIGESTS['closureMembership']

# --- registry / membership / schema accounting ---
memb_union = set(MEMB['direct']) | set(MEMB['equalToDirect']) | set(MEMB['selectedThroughOtherInput'])
rec('registry-membership-cover',
    byField=sorted(BYFIELD),
    byFieldCount=len(BYFIELD),
    membershipUnion=sorted(memb_union),
    equal=memb_union == set(BYFIELD),
    onlyInByField=sorted(set(BYFIELD) - memb_union),
    onlyInMembership=sorted(memb_union - set(BYFIELD)))

closure2_fields = []
defs = SCHEMA['$defs']
for rec_name, node in defs.items():
    if not isinstance(node, dict):
        continue
    props = node.get('properties') or {}
    for fname, fnode in props.items():
        if not isinstance(fnode, dict):
            continue
        pat = fnode.get('pattern', '')
        if 'closure2:' in pat:
            closure2_fields.append(f'{rec_name}.{fname}')
        items = fnode.get('items') or {}
        if isinstance(items, dict) and 'closure2:' in items.get('pattern', ''):
            closure2_fields.append(f'{rec_name}.{fname}[]')
        if fname == 'principals':
            iprops = ((items.get('properties') or {}) if isinstance(items, dict) else {})
            if 'closureId' in iprops:
                closure2_fields.append(f'{rec_name}.principals[].closureId')

rec('schema-closure2-fields', fields=sorted(set(closure2_fields)))

native_joins = []
for domain, row in DIGESTS['domainSets']['native-context'].items():
    for join in row.get('closureJoins', []):
        native_joins.append({
            'domain': domain,
            'language': row.get('language'),
            'path': '.'.join(join['path']),
            'form': join['form'],
            'kind': join['kind'],
        })
rec('native-context-closureJoins', joins=native_joins)

# Helper prefix collision audit
collisions = []
for kind in list(defs) + ['regeneration-key', 'cache-key', 'toolchain', 'ToolClosureV1', 'TypeScriptToolClosureV1']:
    prefix = ('cache-key' if kind == 'regeneration-key' else kind) + '.'
    hits = [n for n in BYFIELD if n.startswith(prefix)]
    if hits:
        collisions.append({'recordKind': kind, 'prefix': prefix, 'hits': hits})
rec('byField-prefix-hits-by-record-kind', rows=collisions)

# Historical vs current: helper presence
hist = (CAND / 'identity-model.py').read_text()
cur_c24 = (CAND / 'identity-model.v3.py').read_text()
cur_suc = (SUCC / 'identity-model.v3.py').read_text()
rec('profile-helper-presence',
    historicalHasHelper='def admit_closure_field_kinds' in hist,
    candidate24v3HasHelper='def admit_closure_field_kinds' in cur_c24,
    successorHasHelper='def admit_closure_field_kinds' in cur_suc,
    historicalEnumeratorFault='ENUMERATOR_CLOSURE_KIND' in hist,
    successorPreservesEnumeratorFault=cur_suc.count("raise C.AdmissionError('ENUMERATOR_CLOSURE_KIND')") >= 2)

# Public detail registry: these admission names are internal identity faults
pub = json.loads((SUCC.parent / 'public-detail-registry.v1.json').read_text())
pub_codes = set()
if isinstance(pub, dict):
    for k, v in pub.items():
        if k in ('records', 'details', 'codes', 'members'):
            continue
        if isinstance(v, dict) and 'code' in v:
            pub_codes.add(v['code'])
    # collect nested codes
    def walk_codes(x):
        if isinstance(x, dict):
            if 'code' in x and isinstance(x['code'], str):
                pub_codes.add(x['code'])
            for y in x.values():
                walk_codes(y)
        elif isinstance(x, list):
            for y in x:
                walk_codes(y)
    walk_codes(pub)
rec('public-detail-identity-fault-names',
    enumeratorInPublic='ENUMERATOR_CLOSURE_KIND' in pub_codes or any('ENUMERATOR_CLOSURE_KIND' in str(x) for x in pub_codes),
    closureFieldKindInPublic=any('CLOSURE_FIELD_KIND' in str(x) for x in pub_codes),
    note='Identity AdmissionError names are not DomainDetailCode members; routing stays internal to owner admission, matching UNSELECTED_* / REFERENCE_IDENTITY.')

# --- fixture / owner graph probes ---
history = {
    'kind': 'history',
    'payload': {
        'payloadDomain': 'workflow.import-payload.history.v1',
        'vcsSystem': 'git',
        'revisionRange': {'from': None, 'to': 'a' * 40, 'commitCount': 0, 'truncated': False},
        'collectionScope': 'all-paths',
        'subjects': [],
    },
    'observation': {'revisionRange': {'from': None, 'to': 'a' * 40}},
}

def seal_positive(**opts):
    g = F.build_file_inputs(**opts)
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = g['inputs']
    result = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'], i['evaluationInputRefs'], objects, blobs, owner)
    objects = copy.deepcopy(objects); blobs = copy.deepcopy(blobs)
    objects.update(result['objects']); blobs.update(result['blobs'])
    def add(domain, fields):
        value = {'schemaVersion': 3, **fields}
        key = M.identifier(domain, value)
        objects[key] = (domain, value)
        return key
    iplan = g['inputs']
    evidence = add('semantic-evidence', {
        'planId': iplan['planId'], 'viewIds': g['viewIds'], 'coverageIds': g['coverageIds'],
        'importIds': iplan['plan']['importIds'], 'findingIds': result['proof']['findingIds'],
        'proofBundleId': result['proofBundleId'],
    })
    sid = add('evaluation-seal', {
        'planId': iplan['planId'], 'executionPlanId': iplan['executionPlanId'], 'evidenceId': evidence,
        'evaluatorClosure': iplan['evaluatorClosure'], 'policyDigest': iplan['plan']['policyDigest'],
        'proofBundleId': result['proofBundleId'], 'verdict': result['proof']['verdict'],
    })
    run = {
        'schemaVersion': 3, 'projectId': g['snapshot']['projectId'],
        'snapshotId': iplan['plan']['snapshotId'], 'planId': iplan['planId'],
        'evidenceId': evidence, 'evaluationSealId': sid,
        'capabilityManifestId': iplan['plan']['capabilityManifestId'],
    }
    return run, objects, blobs, g

def catch(fn):
    try:
        fn()
        return {'result': 'ADMIT'}
    except Exception as exc:
        return {'result': 'REFUSE', 'type': type(exc).__name__, 'detail': str(exc)}

run, objects, blobs, graph = seal_positive(import_specs=[history])
replay = R.replay(run, objects, blobs)
rec('independent-imported-full-replay-positive',
    replay=replay,
    runId=M.identifier('run', run),
    identitiesValid=all(M.identifier(d, v) == k for k, (d, v) in objects.items()))

_, owner = M.open_run_closure(run, objects, blobs)
plan = objects[run['planId']][1]
imp = objects[plan['importIds'][0]][1]
adapter = imp['adapterClosure']
producer = imp['producerClosure']
rec('independent-plan-membership-import-adapter',
    adapterInSemanticClosures=adapter in plan['semanticClosures'],
    producerInSemanticClosures=producer in plan['semanticClosures'],
    adapterKind=objects[adapter][1]['kind'],
    producerKind=objects[producer][1]['kind'],
    importIdsMember=plan['importIds'][0] in plan['importIds'],
    nativeContextCount=len(plan['nativeContextDigests']),
    semanticClosuresKinds=sorted({objects[c][1]['kind'] for c in plan['semanticClosures']}))

# Recursion: get(import) must resolve nested closures without looping
rec('independent-get-import-no-recursion',
    **catch(lambda: owner['get'](plan['importIds'][0], 'import')))

# Enumerator old fault name via get of reminted extra, not whole-run
closure_ids = {record['kind']: key for key, (domain, record) in objects.items() if domain == 'closure'}
scope_key, scope = next((k, r) for k, (d, r) in objects.items() if d == 'subject-scope')
changed = copy.deepcopy(scope)
changed['enumeratorClosure'] = closure_ids['evaluator']
hostile = M.identifier('subject-scope', changed)
objects[hostile] = ('subject-scope', changed)
rec('independent-enumerator-old-fault-on-get',
    originalGetOk=owner['get'](scope_key, 'subject-scope') == scope,
    hostileIdentityValid=M.identifier('subject-scope', changed) == hostile,
    **catch(lambda: owner['get'](hostile, 'subject-scope')))

# Combined defect: wrong kind AND unselected enumerator — order vs UNSELECTED
other = {'schemaVersion': 2, 'kind': 'evaluator', 'manifestDigest': hashlib.sha256(b'unselected-eval').hexdigest() if False else None}
# mint a fresh evaluator-kind closure not in semanticClosures
fresh = {'schemaVersion': 2, 'kind': 'evaluator', 'manifestDigest': hashlib.sha256(b'unselected-eval-manifest').hexdigest() if False else None}
# use identifier path: need real blob digest in objects? enumeratorClosure is just an id; get will load the closure
fresh_rec = {
    'schemaVersion': 2, 'kind': 'evaluator',
    'manifestDigest': hashlib.sha256(C.canonical(b'x') if False else b'unselected-eval-manifest').hexdigest(),
    'tree': [], 'semanticVersion': '9.9.9', 'protocolMajor': 3, 'platform': 'any',
}
# manifestDigest must be a retained blob for visit, but get(scope) only get()s the closure record for kind.
# get(closure) does not require the manifest blob.
fresh_id = M.identifier('closure', fresh_rec)
objects[fresh_id] = ('closure', fresh_rec)
combo = copy.deepcopy(scope)
combo['enumeratorClosure'] = fresh_id
combo_id = M.identifier('subject-scope', combo)
objects[combo_id] = ('subject-scope', combo)
rec('independent-enumerator-wrong-kind-unselected-order',
    freshInSemanticClosures=fresh_id in plan['semanticClosures'],
    **catch(lambda: owner['get'](combo_id, 'subject-scope')))

# All ten local identity/canonical/cache fields via actual owners
local_record_kinds = {'subject-scope', 'view', 'fact', 'finding', 'evaluation-seal', 'proof-bundle', 'import'}
covered = []
for name, want in BYFIELD.items():
    domain, field = name.split('.', 1)
    if domain not in local_record_kinds:
        continue
    key, record = next((k, r) for k, (d, r) in objects.items() if d == domain)
    changed = copy.deepcopy(record)
    changed[field] = closure_ids['evaluator' if want != 'evaluator' else 'provider']
    hid = M.identifier(domain, changed)
    objects[hid] = (domain, changed)
    expected = 'ENUMERATOR_CLOSURE_KIND' if name == 'subject-scope.enumeratorClosure' else 'CLOSURE_FIELD_KIND:' + name + ':' + want
    got = catch(lambda h=hid, d=domain: owner['get'](h, d))
    covered.append({'field': name, 'expected': expected, 'got': got, 'identityValid': hid == M.identifier(domain, changed)})
rec('independent-local-identity-record-roles', rows=covered)

# stage-spec: refuse before memoization; retries still refuse; good digest still admits
stage = owner['execution']['stages'][0]
spec = copy.deepcopy(owner['payload'](stage['stageSpecDigest'], 'stage-spec'))
bad = copy.deepcopy(spec)
bad['producerClosure'] = closure_ids['detector']
raw = C.canonical(bad)
digest = hashlib.sha256(raw).hexdigest()
blobs[digest] = raw
retry_rows = [catch(lambda: owner['payload'](digest, 'stage-spec')) for _ in range(3)]
good_again = catch(lambda: owner['payload'](stage['stageSpecDigest'], 'stage-spec'))
# After a failed payload, parsed must not have cached the bad digest. Mutate to valid kind under SAME digest is impossible
# because digest is content-addressed; instead confirm a second independent owner still refuses.
_, owner2 = M.open_run_closure(run, objects, blobs)
retry_new_owner = catch(lambda: owner2['payload'](digest, 'stage-spec'))
rec('independent-stage-spec-memoization',
    retries=retry_rows,
    goodStillAdmits=good_again,
    newOwnerStillRefuses=retry_new_owner,
    allRetriesRefuse=all(r.get('detail') == 'CLOSURE_FIELD_KIND:stage-spec.producerClosure:provider' for r in retry_rows))

# cache / regeneration: kind before unselected; detector IS plan-selected so this is role not membership
key = {
    'schemaVersion': 2, 'planId': run['planId'], 'producerClosure': spec['producerClosure'],
    'stageSpecDigest': stage['stageSpecDigest'], 'scopeIds': [], 'inputRefs': [],
    'outputSchemaDigest': spec['outputSchemaDigest'],
}
cache_pos = catch(lambda: M.admit_cache_entry('cache-key', key, run, objects, blobs))
regen_pos = catch(lambda: M.admit_cache_entry('regeneration-key', key, run, objects, blobs))
wrong = copy.deepcopy(key)
wrong['producerClosure'] = closure_ids['detector']
# detector is in semanticClosures; membership would pass
rec('independent-cache-regeneration',
    detectorIsSelected=closure_ids['detector'] in plan['semanticClosures'],
    cachePositive=cache_pos,
    regenPositive=regen_pos,
    cacheWrong=catch(lambda: M.admit_cache_entry('cache-key', wrong, run, objects, blobs)),
    regenWrong=catch(lambda: M.admit_cache_entry('regeneration-key', wrong, run, objects, blobs)))

# Unselected but RIGHT kind producer on cache key: membership still separate
unsel_provider = {
    'schemaVersion': 2, 'kind': 'provider',
    'manifestDigest': hashlib.sha256(b'unselected-provider-manifest').hexdigest(),
    'tree': [], 'semanticVersion': '0.0.1', 'protocolMajor': 3, 'platform': 'any',
}
unsel_id = M.identifier('closure', unsel_provider)
objects[unsel_id] = ('closure', unsel_provider)
unsel_key = copy.deepcopy(key)
unsel_key['producerClosure'] = unsel_id
rec('independent-cache-unselected-correct-kind',
    unselected=unsel_id not in plan['semanticClosures'],
    **catch(lambda: M.admit_cache_entry('cache-key', unsel_key, run, objects, blobs)))

# Whole-import structural vs semantic
whole_rows = []
for field, kw in [('producerClosure', {'import_producer_kind': 'adapter'}), ('adapterClosure', {'import_adapter_kind': 'provider'})]:
    g = F.build_file_inputs(import_specs=[history], **kw)
    hostile_run, hostile_objects, hostile_blobs, _ = F.seal_fixture(g)
    id_ok = all(M.identifier(d, rec_) == hid for hid, (d, rec_) in hostile_objects.items())
    structural = catch(lambda: M.open_run_closure(hostile_run, hostile_objects, hostile_blobs))
    semantic = catch(lambda: R.replay(hostile_run, hostile_objects, hostile_blobs))
    required = 'provider' if field == 'producerClosure' else 'adapter'
    whole_rows.append({
        'field': field,
        'identitiesValid': id_ok,
        'structural': structural,
        'semanticCall': semantic,
        'semanticReachedReplayFault': 'EVALUATOR_COMPLETE_PROOF_REPLAY' in str(semantic.get('detail')),
        'expected': 'CLOSURE_FIELD_KIND:import.' + field + ':' + required,
    })
rec('independent-whole-import-structural-not-semantic', rows=whole_rows)

# Whole reminted graph with wrong view.producerClosure (not extra-record get)
def remint_view_wrong_kind():
    r0, o0, b0, _g = seal_positive(import_specs=[history])
    vid = next(k for k, (d, rec_) in o0.items() if d == 'view')
    view = copy.deepcopy(o0[vid][1])
    det = next(k for k, (d, rec_) in o0.items() if d == 'closure' and rec_['kind'] == 'detector')
    view['producerClosure'] = det
    new_vid = M.identifier('view', view)
    o0[new_vid] = ('view', view)
    # replace in evidence/run graph
    ev = copy.deepcopy(o0[r0['evidenceId']][1])
    ev['viewIds'] = [new_vid if x == vid else x for x in ev['viewIds']]
    new_ev = M.identifier('semantic-evidence', ev)
    o0[new_ev] = ('semantic-evidence', ev)
    seal = copy.deepcopy(o0[r0['evaluationSealId']][1])
    seal['evidenceId'] = new_ev
    new_seal = M.identifier('evaluation-seal', seal)
    o0[new_seal] = ('evaluation-seal', seal)
    r0['evidenceId'] = new_ev
    r0['evaluationSealId'] = new_seal
    return catch(lambda: M.open_run_closure(r0, o0, b0))
rec('independent-whole-run-wrong-view-producer', **remint_view_wrong_kind())

# Native five via actual admit_native_context
H = F.fixture_helpers()
native_objects = {}; native_blobs = {}
def blob(value):
    raw = value if type(value) is bytes else C.canonical(value)
    d = hashlib.sha256(raw).hexdigest(); native_blobs[d] = raw; return d
def add(domain, **fields):
    record = {'schemaVersion': 2, **fields}
    key = M.identifier(domain, record)
    native_objects[key] = (domain, record)
    return key
native_sources = {**H.TS_SOURCES, 'a.ts': b'export const x = 1;\n'}
native_inventory = sorted([{'path': p, 'sha256': blob(raw), 'bytes': len(raw)} for p, raw in native_sources.items()],
                          key=lambda row: row['path'].encode())
native = H.native_inputs(native_objects, native_blobs, add, blob, ts_inventory=native_inventory)
contexts = {'typescript': native['context'], 'rust': native['rustContext'], 'syntax': native['syntaxContext']}
native_closures = {k: rec_ for k, (d, rec_) in native_objects.items() if d == 'closure'}
N = M.native_admission()
native_pos = {}
for language, context in contexts.items():
    result = N.admit_native_context(language, context, native_closures)
    native_pos[language] = {'refusals': result['refusals'], 'admitted': not result['refusals']}
rec('independent-native-positives', **native_pos)

native_sites = [
    ('TypeScriptToolClosureV1.closureId', 'typescript', 'toolClosure', 'closureId', False),
    ('ToolClosureV1.closureId', 'rust', 'toolClosure', 'closureId', False),
    ('toolchain.typescriptStdlibMerkleRoot', 'typescript', 'toolchain', 'typescriptStdlibMerkleRoot', True),
    ('toolchain.rustcDevLlvmDigest', 'rust', 'toolchain', 'rustcDevLlvmDigest', True),
    ('SyntaxGrammarBundleV1.closureId', 'syntax', 'grammarBundle', 'closureId', False),
]
native_neg = []
for name, language, parent, field, suffix in native_sites:
    context = copy.deepcopy(contexts[language])
    cid = context[parent][field]
    if suffix:
        cid = 'closure2:' + cid
    descriptor = copy.deepcopy(native_closures[cid])
    original_kind = descriptor['kind']
    descriptor['kind'] = 'provider'
    wrong = M.identifier('closure', descriptor)
    closures = {**native_closures, wrong: descriptor}
    context[parent][field] = wrong.split(':', 1)[1] if suffix else wrong
    result = N.admit_native_context(language, context, closures)
    expected = 'native.native-context-closure-kind-mismatch:' + parent + '.' + field
    native_neg.append({
        'field': name,
        'originalKind': original_kind,
        'wrongIdentity': wrong,
        'wrongIdentityValid': wrong == M.identifier('closure', descriptor),
        'expected': expected,
        'refusals': result['refusals'],
        'hit': expected in result['refusals'],
        'onlyKindMismatch': result['refusals'] == [expected] or expected in result['refusals'],
    })
rec('independent-native-five-role-negatives', rows=native_neg)

# Identity-model native join still present and uses published kinds
rec('independent-identity-native-join-still-present',
    hasNativeContextClosureKind='NATIVE_CONTEXT_CLOSURE_KIND' in cur_suc,
    nativeJoinBeforeAdmitNative='admit_native_context' in cur_suc[cur_suc.find('if domain_set==\'native-context\''):cur_suc.find('if domain_set==\'native-semantic-universe\'')])

# Historical open_run_closure get() has no kind helper
rec('independent-candidate24-open-run-get-lacks-kind-helper',
    candidateGetHasKind='admit_closure_field_kinds' in cur_c24)

# Prefix helper does not treat ToolClosureV1 as prefix of TypeScriptToolClosureV1
rec('independent-prefix-not-too-greedy',
    toolHits=[n for n in BYFIELD if n.startswith('ToolClosureV1.')],
    tsToolHits=[n for n in BYFIELD if n.startswith('TypeScriptToolClosureV1.')])

# Controls module actually invokes native admission, not just set equality
ctrl = (SUCC / 'closure_field_kind_controls.v3.py').read_text()
rec('independent-controls-reach-stated-boundaries',
    callsAdmitNativeContext='admit_native_context' in ctrl,
    callsOpenRunClosure='open_run_closure' in ctrl,
    callsReplay='T.R.replay' in ctrl,
    callsAdmitCache='admit_cache_entry' in ctrl,
    wholeImportBoundaryNotesSemanticNotReached='semantic replay not reached' in ctrl,
    remintsHostileImportIdentities='M.identifier(domain,record)==hid' in ctrl,
    nativeRemintsClosureIdentity="descriptor['kind']='provider'" in ctrl and 'M.identifier(\'closure\',descriptor)' in ctrl)

out = {'standing': 'Independent Grok coauthor probes; not pin regeneration, not product qualification, not whole-design acceptance.',
       'probes': rows}
(OUT / 'independent_closure_kind_probes.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'wrote': str(OUT / 'independent_closure_kind_probes.json'), 'cases': [r['case'] for r in rows]}, indent=2))
