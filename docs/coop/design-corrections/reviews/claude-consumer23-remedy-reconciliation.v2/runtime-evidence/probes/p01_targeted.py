"""P01 — targeted, read-only probe of the captured author after-images (not a global suite). Builds a disposable overlay:
frozen36 docs/coop/design-corrections (minus reviews/), docs/coop/artifacts and docs/v2/contracts/product-v1, every copied file
hash-checked against frozen36, then the six changed author images overlaid and checked against after-manifest.json.

S1: missing / empty package coordinate through the public wrapper with no Run and with a purged availability observation
(schema-first ordering), the helper, the unchanged graph-query schema, a complete-tuple helper ambiguity control.
Issue 3 helper facts: the native route is total and drift-free; run_termination sees only its stage and entry inputs; a
stage-implied primary can differ from the typed-detail entry deficiency; requirement-relative deficiencies reach the helper
only if an entry declares them. No frozen, live or author byte is written."""
import copy, hashlib, importlib.util, json, os, shutil, sys

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-consumer23-remedy-reconciliation.v2'
IMG = os.path.join(BASE, 'observed-author-source')
KIT = os.path.join(BASE, 'disposable/overlay')
OUT = os.path.join(BASE, 'receipts')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = json.load(open(os.path.join(BASE, 'after-manifest.json')))
R = {'standing': 'targeted helper/wrapper probe of captured author images over frozen36; not a suite, not acceptance'}
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = bad = 0
for sub in ('docs/coop/design-corrections', 'docs/coop/artifacts', 'docs/v2/contracts/product-v1'):
    for d, dirs, fs in os.walk(os.path.join(S36, sub)):
        rel_d = os.path.relpath(d, S36)
        if rel_d.startswith('docs/coop/design-corrections/reviews'):
            dirs[:] = []
            continue
        for f in fs:
            src = os.path.join(d, f)
            dst = os.path.join(KIT, rel_d, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
            bad += sha(dst) != sha(src)
overlaid = {}
for f in man['files']:
    src = os.path.join(IMG, f['path'])
    assert sha(src) == f['sha256'], f['path']
    shutil.copyfile(src, os.path.join(KIT, f['path']))
    overlaid[f['path']] = {'imageEqualsAfterManifest': True, 'equalsFrozen36': f['equalsFrozen36']}
R['overlay'] = {'copiedFromFrozen36': copied, 'copyMismatches': bad, 'overlaid': overlaid}
DC = os.path.join(KIT, 'docs/coop/design-corrections')
R['graphQuerySchemaUnchanged'] = sha(os.path.join(DC, 'workflows/schemas/evaluator3/graph-query.schema.json')) == sha(
    os.path.join(S36, 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


CK = load('ckq_overlay', os.path.join(DC, 'workflows/check-query-projection.v3.py'))
Q = CK.Q
U1 = 'a' * 64
shapes = {'package-absent-coordinate': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app'},
          'package-empty-coordinate': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': ''},
          'package-with-coordinate': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': 'app/package.json'}}


def outcome(fn):
    try:
        fn()
        return 'not refused'
    except Q.QueryRefusal as exc:
        return '%s / %s' % (exc.error_code, exc.detail)


s1 = {}
for label, ep in shapes.items():
    req = CK.request('graph.neighbors', CK.project_id(), {'runId': CK.run_id()},
                     {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': copy.deepcopy(ep)})
    s1[label] = {
        'rawRequestSchemaAdmits': CK.valid(CK.GQ + '#/$defs/GraphQueryRequestV1', req)[0],
        'wrapperNoRun': outcome(lambda: Q.execute_graph_query(req, host=CK.host_obs())),
        'wrapperNoRunPurgedObservation': outcome(lambda: Q.execute_graph_query(req, host=CK.host_obs(availability='purged'))),
        'wrapperDummyRunPurgedObservation': outcome(lambda: Q.execute_graph_query(req, {'projectId': req['projectId']}, {}, {}, host=CK.host_obs(availability='purged'))),
        'helper': outcome(lambda: Q.parse_endpoint_syntax(ep, 'endpoint'))}
R['S1'] = s1
key = Q.endpoint_tuple(shapes['package-with-coordinate'])
R['S1ambiguityHelperOnly'] = {'admit_vertices_with_marked_key': outcome(lambda: Q.admit_vertices([('endpoint', shapes['package-with-coordinate'])], {key: shapes['package-with-coordinate']}, {key})),
                              'endpointTupleIsTheWholeIdentity': list(key)}
print('S1:', json.dumps(s1, indent=1), '\nambiguity helper:', R['S1ambiguityHelperOnly'], '\ngraph-query schema unchanged:', R['graphQuerySchemaUnchanged'], flush=True)

N = load('nat_overlay', os.path.join(DC, 'native/native_evidence_model.v2.py'))
R['nativeRouteTotal'] = {d: N.native_deficiency_d9(d)['code'] for d in N.SCHEMAS['$defs']['DeficiencyV2']['enum']}
R['nativeRouteDrift'] = N.d9_route_drift()
try:
    N.native_deficiency_d9('verdict-indeterminate')
    R['nativeRouteRefusesNonMember'] = False
except Exception:  # noqa: BLE001
    R['nativeRouteRefusesNonMember'] = True
st = {k: N.stage_authority(k) for k in ('complete', 'budget-exhausted', 'unavailable', 'crash')}
E = lambda d, c=None, rel='references': {'relation': rel, 'deficiency': d, 'nativeCause': c}
rows = {
    'complete/no-entries': ([], 'complete'),
    'complete/entry-declares-required-relation-missing': ([E('required-relation-missing')], 'complete'),
    'complete/entry-declares-confidence-floor-unmet': ([E('confidence-floor-unmet')], 'complete'),
    'budget-stage/entry-resolution-incomplete': ([E('resolution-incomplete')], 'budget-exhausted'),
    'budget-stage/no-entries': ([], 'budget-exhausted'),
    'unavailable-stage/entry-budget-exhausted': ([E('budget-exhausted')], 'unavailable'),
    'crash/entry-input-closure': ([E('input-closure-incomplete', 'lockfile-missing')], 'crash')}
out = {}
for label, (entries, kind) in rows.items():
    t = N.run_termination(st[kind], entries)
    out[label] = {'d9': t['d9'], 'typedDetailDeficiency': (t['typedDetail'] or {}).get('deficiency'), 'nativeCauses': (t['typedDetail'] or {}).get('nativeCauses')}
R['runTermination'] = out
R['helperSignature'] = str(__import__('inspect').signature(N.run_termination))
R['observations'] = {
    'helperInputsAreOnlyStageAndEntries': R['helperSignature'] == '(stage: dict, coverage_entries: list[dict]) -> dict',
    'requirementRelativeDeficiencyReachesHelperOnlyIfAnEntryDeclaresIt': out['complete/no-entries']['d9']['class'] == 'success'
                                                                         and out['complete/entry-declares-required-relation-missing']['d9']['code'] == 'COVERAGE.REQUIRED_RELATION_MISSING',
    'stageImpliedPrimaryCanDifferFromTypedDetail': out['budget-stage/entry-resolution-incomplete']['d9']['code'] == 'COVERAGE.BUDGET_EXHAUSTED'
                                                   and out['budget-stage/entry-resolution-incomplete']['typedDetailDeficiency'] == 'resolution-incomplete',
    'faultedStageKeepsOwnTermination': out['crash/entry-input-closure']['d9']['class'] == 'operational-failed'}
print('native route:', R['nativeRouteTotal'], '| drift:', R['nativeRouteDrift'], '| refuses non-member:', R['nativeRouteRefusesNonMember'])
print('run_termination:', json.dumps(out, indent=1))
print('observations:', R['observations'])
R['imagesUnchangedAfter'] = all(sha(os.path.join(IMG, f['path'])) == f['sha256'] for f in man['files'])
R['frozen36OverlaySourcesUnchanged'] = all(sha(os.path.join(S36, f['path'])) == f['frozen36Sha256'] for f in man['files'])
json.dump(R, open(os.path.join(OUT, 'p01-targeted.json'), 'w'), indent=1, default=str)
print('images unchanged:', R['imagesUnchangedAfter'], '| frozen36 unchanged:', R['frozen36OverlaySourcesUnchanged'], '\nwrote p01-targeted.json')
