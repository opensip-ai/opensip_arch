"""Smoke the rewritten selection module against a FULL ADMITTED Run."""
import copy, importlib.util, json
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
WF = SRC / 'docs/coop/design-corrections/workflows'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load('dev_replay', FOUND / 'check-replay.v3.py')
N = load('dev_native', SRC / 'docs/coop/design-corrections/native/native_evidence_model.v2.py')
S = load('dev_select', WF / 'repair_closed_world_selection.v1.py')
F, R, M = P.F, P.R, P.M

CLOSED = N.closed_world_v2(package_json={'private': True},
                           entry_points={'state': 'all', 'source': 'explicit'},
                           unresolved=[], external_consumers='none-declared')
OPEN = N.closed_world_v2(package_json={'private': True},
                         entry_points={'state': 'partial', 'source': 'recognized'},
                         unresolved=[], external_consumers='unknown')
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
            payload['entry']['closedWorld'] = copy.deepcopy(assign(payload['key'], seen.index(universe)))
            return payload

        H.coverage_result = coverage_result
        return H

    F.fixture_helpers = helpers
    try:
        g = F.build_file_inputs(**kw)
        seed, objects, blobs, _ = F.seal_fixture(g)
        _, owner = M.open_run_closure(seed, objects, blobs)
        i = g['inputs']
        res = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                       i['evaluationInputRefs'], objects, blobs, owner)
        run, objects, blobs = P.seal(g, res, objects, blobs)
        return M.close_run(run, objects, blobs), run, objects, blobs
    finally:
        F.fixture_helpers = _orig


rid, run, objects, blobs = build(lambda key, idx: OPEN if idx == 1 else CLOSED,
                                 multiple_universes=True)
print('ADMITTED', rid)
view = S.RetainedRunView(run, objects, blobs)
ep = view.enumeration_plan()
print('enumeration cells:', [(c['capabilityId'], c['kinds'], len(c['programBindings'])) for c in ep['cells']])

fps = sorted({f['fingerprint'] for _, f in view.matched_findings() if f.get('fingerprint')})
out = S.derive(view, fps[:1], [{'path': 'src/index.ts', 'action': 'delete'}])
print('\nrelevantUniverses  ', [u[:12] for u in out['relevantUniverses']])
print('censusUniverses    ', [u[:12] for u in out['ownership']['censusUniverses']])
print('witnessUniverses   ', [u[:12] for u in out['ownership']['witnessUniverses']])
print('witnessOnly        ', out['ownership']['witnessOnlyUniverses'])
print('unresolvedOwnership', out['unresolvedOwnership'])
print('eligible           ', out['eligible'])
print('closedWorld        ', json.dumps(out['closedWorld']))
print('unmet remedies:')
for u in out['unmetPreconditions']:
    print('   ', u['remedy'][:230])

print('\ncensus provenance rows for one universe:')
u0 = out['relevantUniverses'][0]
for row in out['universeSources'][u0]:
    print('   ', json.dumps(row))

zero = S.derive(view, [], [{'path': 'src/new.ts', 'action': 'create'}])
print('\ncreate-only, no targets -> closedWorld', json.dumps(zero['closedWorld']))
print('EMPTY sentinel equals   ', json.dumps(S.EMPTY_DISPLAY_SUMMARY))
print('SELECTION_ORDER_KEY     ', S.SELECTION_ORDER_KEY)
