"""Development probe: drive the new selection module from a FULL ADMITTED Run."""
import copy, importlib.util, json, sys
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
S = load('dev_select', WF / 'repair_closed_world_selection.v1.py')

print('SOURCE_PATH_RELATIONS', sorted(S.SOURCE_PATH_RELATIONS))
print('universeRules', S.SOURCE_PATH_UNIVERSE_RULES)

CLOSED = N.closed_world_v2(package_json={'private': True},
                           entry_points={'state': 'all', 'source': 'explicit'},
                           unresolved=[], external_consumers='none-declared')
OPEN = N.closed_world_v2(package_json={'private': True},
                         entry_points={'state': 'partial', 'source': 'recognized'},
                         unresolved=[], external_consumers='unknown')
print('CLOSED', CLOSED)
print('OPEN  ', OPEN)

F, R, M = P.F, P.R, P.M
_orig = F.fixture_helpers


def build(assign, **kw):
    """Build + admit a Run whose per-entry closedWorld is chosen by `assign(key)`."""
    seen = []

    def helpers():
        H = _orig()
        base = H.coverage_result

        def coverage_result(scope_descriptor, universe, resolved, blobs=None,
                            inventory_paths=None, unresolved=()):
            payload = base(scope_descriptor, universe, resolved, blobs, inventory_paths, unresolved)
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
        _, owner = M.open_run_closure(seed, objects, blobs)
        i = g['inputs']
        result = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                          i['evaluationInputRefs'], objects, blobs, owner)
        run, objects, blobs = P.seal(g, result, objects, blobs)
        run_id = M.close_run(run, objects, blobs)
        return run_id, run, objects, blobs
    finally:
        F.fixture_helpers = _orig


# --- multi-universe, disagreeing by universe
run_id, run, objects, blobs = build(lambda key, idx: OPEN if idx == 1 else CLOSED,
                                    multiple_universes=True)
print('\nADMITTED', run_id)
view = S.RetainedRunView(run, objects, blobs)

scopes = view.subject_scopes()
print('scopes:')
for sid, sc in sorted(scopes.items()):
    print('  ', sc['relation'], '@', sc['resolution'], 'srcU', sc['sourceUniverse'][:10],
          'tgtU', sc['targetUniverse'][:10], 'subjects', sc['subjects'])

fps = sorted({f['fingerprint'] for _, f in view.matched_findings() if f.get('fingerprint')})
print('matched fingerprints', [f[:24] for f in fps])
for fid, f in view.matched_findings():
    print('   ', f['fingerprint'][:20], '->', view.subject(f['subjectId'])['universe'][:10],
          f['subject']['logicalPath'])

EDITS_UNSAFE = [{'path': 'src/index.ts', 'action': 'delete'}]
EDITS_CREATE = [{'path': 'src/new.ts', 'action': 'create'}]

out = S.derive(view, fps[:1], EDITS_UNSAFE)
print('\n--- unsafe, one target fingerprint')
print(json.dumps({k: v for k, v in out.items() if k != 'universeSources'}, indent=1)[:2600])

out2 = S.derive(view, fps[:1], EDITS_CREATE)
print('\n--- create-only')
print(json.dumps({k: v for k, v in out2.items()
                  if k in ('gateActivated', 'eligible', 'relevantUniverses',
                           'unmetPreconditions', 'closedWorld')}, indent=1))

out3 = S.derive(view, [], EDITS_CREATE)
print('\n--- create-only, no targets (empty selection)')
print(json.dumps({k: v for k, v in out3.items()
                  if k in ('gateActivated', 'eligible', 'relevantUniverses',
                           'selectedCoverage', 'closedWorld')}, default=str, indent=1)[:900])

out4 = S.derive(view, fps[:1], [{'path': 'nowhere/absent.ts', 'action': 'delete'}])
print('\n--- unsafe path with no retained owner')
print(json.dumps({k: v for k, v in out4.items()
                  if k in ('gateActivated', 'eligible', 'unownedUnsafePaths',
                           'relevantUniverses', 'unmetPreconditions')}, indent=1)[:1200])
