"""Attempt a FULL ADMITTED asymmetric Run: universe B owns the unsafe path only through its
retained SYMBOL extent, with no source-path subject scope."""
import copy, importlib.util, json, traceback
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
SYMBOL_ROWS = [{'nativeSubjectId': 'ts-symbol:src/index.ts#x', 'qualifiedName': 'x'}]
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


# baseline: default OFF must be unchanged
try:
    rid0, *_ = build(lambda k, i: CLOSED, multiple_universes=True)
    print('default-off baseline still admits:', rid0)
except Exception as exc:
    print('DEFAULT-OFF BROKE:', exc)
    traceback.print_exc()

print()
try:
    rid, run, objects, blobs = build(
        lambda key, idx: CLOSED if key['relation'] != 'declares' else OPEN,
        multiple_universes=True, symbol_rows=SYMBOL_ROWS, symbol_only_second_program=True)
    print('ASYMMETRIC RUN ADMITTED:', rid)
except Exception as exc:
    print('ASYMMETRIC RUN REFUSED:', type(exc).__name__, str(exc)[:400])
    traceback.print_exc()
    raise SystemExit(0)

view = S.RetainedRunView(run, objects, blobs)
ep = view.enumeration_plan()
print('cells:', [(c['capabilityId'], c['kinds'],
                  [(b['ordinal'], (b['universe'] or 'null')[:10],
                    [(e['kind'], e['paths']) for e in b['extents']]) for b in c['programBindings']])
                 for c in ep['cells']])
print('scopes:')
for sid, sc in sorted(view.subject_scopes().items()):
    print('   ', sc['relation'], '@', sc['resolution'], 'srcU', sc['sourceUniverse'][:10],
          'subjects', sc['subjects'])
print('coverage:')
for cid, _c, sc, pl in view.coverage_records():
    print('   ', pl['key']['relation'], 'srcU', pl['key']['sourceUniverse'][:10],
          'eligible', pl['entry']['closedWorld']['deadCodeRepairEligible'])

fps = sorted({f['fingerprint'] for _, f in view.matched_findings() if f.get('fingerprint')})
print('matched fingerprints:', [f[:22] for f in fps])
for fid, f in view.matched_findings():
    print('   ', f['fingerprint'][:20], '->', view.subject(f['subjectId'])['universe'][:10])

EDIT = [{'path': 'src/index.ts', 'action': 'delete'}]
out = S.derive(view, [], EDIT)
print('\n--- derive with NO targets, one unsafe edit (ownership comes from the census alone)')
print('censusUniverses ', [u[:10] for u in out['ownership']['censusUniverses']])
print('witnessUniverses', [u[:10] for u in out['ownership']['witnessUniverses']])
print('relevant        ', [u[:10] for u in out['relevantUniverses']])
print('eligible        ', out['eligible'])
print('closedWorld     ', json.dumps(out['closedWorld']))
for u in out['unmetPreconditions']:
    print('   remedy:', u['remedy'][:220])

# What the SOURCE-PATH-SCOPE-ONLY law would have concluded on this same admitted Run.
witness_only = S.source_path_scope_witnesses(view, ['src/index.ts'])
print('\nsource-path-scope-only owners:', [u[:10] for u in sorted(witness_only)])
print('census owners                :', [u[:10] for u in out['ownership']['censusUniverses']])
print('OMITTED BY THE OLD LAW       :',
      sorted(set(out['ownership']['censusUniverses']) - set(witness_only)))
