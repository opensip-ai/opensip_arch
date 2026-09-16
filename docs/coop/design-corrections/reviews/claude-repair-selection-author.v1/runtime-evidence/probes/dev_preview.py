"""Development probe: full evaluator3 repair_preview driven by a FULL ADMITTED Run."""
import copy, importlib.util, json
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v1/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
WF = SRC / 'docs/coop/design-corrections/workflows'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load('dev_replay', FOUND / 'check-replay.v3.py')
N = load('dev_native', SRC / 'docs/coop/design-corrections/native/native_evidence_model.v2.py')
M3 = load('dev_wf3', WF / 'workflows_model.v3.py')
M1 = load('dev_wf1', WF / 'workflows_model.v1.py')
S = M3.closed_world_selection()

print('v3 selector installed :', M3.CLOSED_WORLD_SELECTOR is not None)
print('v1 profile untouched  :', M1.CLOSED_WORLD_SELECTOR is None)

CLOSED = N.closed_world_v2(package_json={'private': True},
                           entry_points={'state': 'all', 'source': 'explicit'},
                           unresolved=[], external_consumers='none-declared')
OPEN = N.closed_world_v2(package_json={'private': True},
                         entry_points={'state': 'partial', 'source': 'recognized'},
                         unresolved=[], external_consumers='unknown')

F, R, MM = P.F, P.R, P.M
_orig = F.fixture_helpers


def build(assign, **kw):
    seen = []

    def helpers():
        H = _orig()
        base = H.coverage_result

        def coverage_result(sd, universe, resolved, blobs=None, inv=None, unresolved=()):
            payload = base(sd, universe, resolved, blobs, inv, unresolved)
            if universe not in seen:
                seen.append(universe)
            payload['entry']['closedWorld'] = copy.deepcopy(
                assign(payload['key'], seen.index(universe)))
            return payload

        H.coverage_result = coverage_result
        return H

    F.fixture_helpers = helpers
    try:
        g = F.build_file_inputs(**kw)
        seed, objects, blobs, _ = F.seal_fixture(g)
        _, owner = MM.open_run_closure(seed, objects, blobs)
        i = g['inputs']
        res = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                       i['evaluationInputRefs'], objects, blobs, owner)
        run, objects, blobs = P.seal(g, res, objects, blobs)
        return MM.close_run(run, objects, blobs), run, objects, blobs
    finally:
        F.fixture_helpers = _orig


TREE = {'README.md': b'# Synthetic fixture\n',
        'src/index.ts': b'export const x = 1;\n',
        'extensionless': b'fixture\n'}
RECIPE = {'contributionId': 'core.repair', 'recipeId': 'remove-unused-export',
          'recipeVersion': '1.0.0', 'closureId': 'closure2:' + 'c' * 64}
TRUST = {RECIPE['closureId']: 'admitted'}
REQS = [{'relation': 'imports', 'minResolution': 'resolved-target',
         'completeness': 'complete', 'satisfied': True}]


def preview(run_id, run, objects, blobs, targets, edits, project='prj1-' + '4' * 64):
    view = S.RetainedRunView(run, objects, blobs)
    snap = M3.tree_snapshot_id(project, TREE)
    adapter = {'authority': 'authoritative', 'availability': 'retained',
               'sealedAssurance': 'replayable', 'runId': run_id,
               'planId': run['planId'], 'snapshotId': snap,
               'findings': targets, 'retained': view, 'evidenceOrigin': 'native-analysis'}
    return M3.repair_preview(project, TREE, adapter, RECIPE, targets, edits, REQS,
                             ['**'], TRUST)


# ---- positive: every entry agrees eligible
rid_pos, run_pos, o_pos, b_pos = build(lambda key, idx: CLOSED, multiple_universes=True)
view = S.RetainedRunView(run_pos, o_pos, b_pos)
fps = sorted({f['fingerprint'] for _, f in view.matched_findings() if f.get('fingerprint')})
plan = preview(rid_pos, run_pos, o_pos, b_pos, fps[:1],
               [{'path': 'src/index.ts', 'action': 'delete'}])
print('\nPOSITIVE run', rid_pos)
print('  applicable', plan['descriptor']['applicable'])
print('  repairPlanId', plan['repairPlanId'])
print('  closedWorld', json.dumps(plan['descriptor']['closedWorld']))

# ---- conflicting negative: package entries of universe #2 dissent, and NO evidence
#      requirement names `package`
rid_neg, run_neg, o_neg, b_neg = build(
    lambda key, idx: OPEN if (idx == 1 and key['relation'] == 'package') else CLOSED,
    multiple_universes=True)
plan2 = preview(rid_neg, run_neg, o_neg, b_neg, fps[:1],
                [{'path': 'src/index.ts', 'action': 'delete'}])
print('\nCONFLICTING NEGATIVE run', rid_neg)
print('  applicable', plan2['descriptor']['applicable'])
print('  repairPlanId', plan2['repairPlanId'])
print('  closedWorld', json.dumps(plan2['descriptor']['closedWorld']))
print('  unmet', json.dumps(plan2['descriptor']['unmetPreconditions'], indent=1)[:900])

# ---- create-only on the dissenting Run
plan3 = preview(rid_neg, run_neg, o_neg, b_neg, fps[:1],
                [{'path': 'src/new.ts', 'action': 'create', 'postimage': b'x\n'}])
print('\nCREATE-ONLY on the dissenting Run')
print('  applicable', plan3['descriptor']['applicable'],
      '| unmet', plan3['descriptor']['unmetPreconditions'])
print('  closedWorld', json.dumps(plan3['descriptor']['closedWorld']))
print('  repairPlanId', plan3['repairPlanId'])

# ---- pre-selected record refused by evaluator3
try:
    bad = dict(runId=rid_neg, planId=run_neg['planId'],
               snapshotId=M3.tree_snapshot_id('prj1-' + '4' * 64, TREE),
               authority='authoritative', availability='retained',
               sealedAssurance='replayable', findings=fps[:1],
               closedWorld=copy.deepcopy(CLOSED), evidenceOrigin='native-analysis')
    M3.repair_preview('prj1-' + '4' * 64, TREE, bad, RECIPE, fps[:1],
                      [{'path': 'src/index.ts', 'action': 'delete'}], REQS, ['**'], TRUST)
    print('\nPRE-SELECTED RECORD: NOT REFUSED (unexpected)')
except M3.Refusal as r:
    print('\nPRE-SELECTED RECORD refused:', r.detail, '|', str(r.remedy)[:120])
