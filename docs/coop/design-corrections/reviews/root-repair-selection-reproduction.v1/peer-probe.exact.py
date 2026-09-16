"""Probe: a FULL admitted synthetic Run carrying two DISTINCT native ClosedWorldV2 records.

Read-only with respect to the frozen source. Nothing here is written back into the
subject tree; all output goes to this probe's own directory. This is author-side
synthetic evidence, not compiler or provider qualification.

What it establishes, in order:
  1. The retained native record that owns ClosedWorldV2 is ViewEntryV3, i.e. ONE
     ClosedWorldV2 per Coverage entry, keyed by CoverageKeyV2
     (relation, resolution, sourceUniverse, targetUniverse, subjectScopeCommitment).
  2. A Run can be built, admitted at the native producer boundary
     (admit_coverage_result_v3) and CLOSED (close_run, complete evaluator3 replay)
     while carrying two entries whose ClosedWorldV2 differ, including differing
     deadCodeRepairEligible.
  3. No retained record in that Run's closure carries a Run-level ClosedWorldV2, so
     `run['closedWorld']` -- the field workflows_model.v1.repair_preview reads -- has
     no publication law to be derived from.
"""
import copy, json, importlib.util, sys, hashlib
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v31')
FOUND = SRC / 'docs/coop/design-corrections/foundation'
OUT = Path(__file__).resolve().parent / 'probe-two-closed-worlds.json'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

P = load('probe_replay_check', FOUND / 'check-replay.v3.py')
F, R, M, E = P.F, P.R, P.M, P.E
N = load('probe_native_model', SRC / 'docs/coop/design-corrections/native/native_evidence_model.v2.py')

report = {'scope': 'repair ClosedWorld selection law', 'steps': []}

def step(name, **kw):
    row = {'step': name, **kw}
    report['steps'].append(row)
    print(json.dumps(row)[:1200])
    return row

# --- 1. Owner shape: where ClosedWorldV2 actually lives in the retained record graph.
nschema = json.loads((SRC / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text())
defs = nschema['$defs']
step('owner-shape',
     closedWorldRequiredMembers=sorted(defs['ClosedWorldV2']['required']),
     memberCount=len(defs['ClosedWorldV2']['required']),
     viewEntryV3RequiresClosedWorld='closedWorld' in defs['ViewEntryV3']['required'],
     coverageResultV3=sorted(defs['CoverageResultV3']['required']),
     coverageKeyV2Coordinates=sorted(defs['CoverageKeyV2']['required']),
     recordsDefiningAClosedWorldProperty=sorted(
         k for k, v in defs.items()
         if isinstance(v, dict) and 'closedWorld' in (v.get('properties') or {})))

# --- 2. Two lawful, self-consistent ClosedWorldV2 records, each MINTED BY THE OWNER's
#        own producer helper (native_evidence_model.closed_world_v2), not hand-written.
CLOSED = N.closed_world_v2(
    package_json={'private': True},
    entry_points={'state': 'all', 'source': 'explicit'},
    unresolved=[], external_consumers='none-declared')
OPEN = N.closed_world_v2(
    package_json={'private': True},
    entry_points={'state': 'partial', 'source': 'recognized'},
    unresolved=[], external_consumers='unknown')
step('two-owner-minted-records', closed=CLOSED, open_=OPEN,
     deadCodeRepairEligibleDiffers=CLOSED['deadCodeRepairEligible'] != OPEN['deadCodeRepairEligible'])

# --- 3. Build the Run. The ONLY change to the fixture is that the second universe's
#        Coverage entries carry OPEN instead of CLOSED. Everything else -- scopes, facts,
#        commitments, the producer boundary, the evaluator -- is the frozen source's own.
_orig_helpers = F.fixture_helpers
_seen_universes = []

def patched_helpers():
    H = _orig_helpers()
    base = H.coverage_result

    def coverage_result(scope_descriptor, universe, resolved, blobs=None,
                        inventory_paths=None, unresolved=()):
        payload = base(scope_descriptor, universe, resolved, blobs, inventory_paths, unresolved)
        if universe not in _seen_universes:
            _seen_universes.append(universe)
        payload['entry']['closedWorld'] = copy.deepcopy(
            OPEN if _seen_universes.index(universe) == 1 else CLOSED)
        return payload

    H.coverage_result = coverage_result
    return H

F.fixture_helpers = patched_helpers

g = F.build_file_inputs(multiple_universes=True)
step('graph-built', universes=len(_seen_universes), views=len(g['viewIds']),
     coverageRecords=len(g['coverageIds']))

seed, objects, blobs, _ = F.seal_fixture(g)
_, owner = M.open_run_closure(seed, objects, blobs)
i = g['inputs']
result = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'],
                  i['evaluationInputRefs'], objects, blobs, owner)
run, objects, blobs = P.seal(g, result, objects, blobs)
run_id = M.close_run(run, objects, blobs)
step('run-admitted', runId=run_id, closeRun='ADMIT',
     note='close_run runs the complete evaluator3 semantic replay, not a schema check')

# --- 4. Read the ClosedWorldV2 records back out of the CLOSED Run, by walking the
#        retained closure run -> evidence -> coverage2 -> payload blob.
evidence = objects[run['evidenceId']][1]
entries = []
for cid in evidence['coverageIds']:
    domain, cov = objects[cid]
    payload = json.loads(blobs[cov['payloadDigest']])
    entries.append({
        'coverageId': cid,
        'key': payload['key'],
        'closedWorld': payload['entry']['closedWorld'],
    })

distinct = sorted({json.dumps(e['closedWorld'], sort_keys=True) for e in entries})
step('retained-coverage-entries',
     entryCount=len(entries),
     distinctClosedWorldRecords=len(distinct),
     distinctDeadCodeRepairEligible=sorted({e['closedWorld']['deadCodeRepairEligible'] for e in entries}),
     perEntry=[{'relation': e['key']['relation'], 'resolution': e['key']['resolution'],
                'sourceUniverse': e['key']['sourceUniverse'][:12],
                'targetUniverse': e['key']['targetUniverse'][:12],
                'subjectScopeCommitment': e['key']['subjectScopeCommitment'][:19],
                'deadCodeRepairEligible': e['closedWorld']['deadCodeRepairEligible'],
                'exportsClosed': e['closedWorld']['exportsClosed'],
                'reasons': e['closedWorld']['reasons']} for e in entries])

# --- 5. Does ANY retained record in the closed Run carry a Run-level closedWorld?
carriers = []
for key, (domain, value) in objects.items():
    if isinstance(value, dict) and 'closedWorld' in value:
        carriers.append({'id': key, 'domain': domain})
step('run-level-closedworld-carriers',
     retainedRecordsCarryingClosedWorld=carriers,
     runRecordKeys=sorted(run.keys()),
     evidenceRecordKeys=sorted(evidence.keys()),
     note='the ONLY carrier is the Coverage payload blob, one per entry; no run3/evidence3/view2 field exists')

OUT.write_text(json.dumps(report, indent=2, default=str) + '\n')
print('\nWROTE', OUT)
