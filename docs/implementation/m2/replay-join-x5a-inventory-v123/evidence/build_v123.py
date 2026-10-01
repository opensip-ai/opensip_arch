"""Build inventory123 by adding exactly the four X5a rows (law X5 r3 item 9:
the evaluator's unavailable-evidence accessor, the host replay join's tests,
and law X8 r3 item 3's two owner rows for this unit, groups C and E) to the
inventory the real product lock selects, and write its successor record.
The parent follows the lock: inventory122 (unit X3d-2, selected at product
933e78b, with contract successor D1's thirty-nine overrides already joined
to its projection and D2's four supersessions bound on it). crates/host/src/fact_admission.rs is already a planned
row of the parent, so it is kept by value and not added. It projects the
fifty-five rows inherited through the parent.

Contract successor D2 (law VD1 r1; four passageSupersessions on
inventory122) is bound at product 933e78b. Each supersession the lock binds is folded into its row's inheritance entry (VD1
item 3; D2's README, "After selection"): the entry's before stays the raw
row text and its effective description becomes D2's after. The row count
stays fifty-five. Under a lock that binds no supersession, nothing is
folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory123."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v123.json'
RECORD = M + 'replay-join-x5a-inventory-v123/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v122.json': (M + 'commit-facade-x3d2-inventory-v122/successor.json', 'inventory122', 'X3d-2'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory123 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
# Law X8 r3 item 3's owner rows for unit X5a (law X5 r3 item 5f): (file,
# group, what the case pins, the expected code, rustc 1.95.0's fragment).
CASES = [
    ["host_run_candidate_unnameable.rs", "C", "the build plan's inert RunCandidate, the host's crate-private RunCandidateInputs, is unnameable outside the host, so it cannot stand in for the ReplayedRun that storage's prepare_commit takes (X3d r6 item 11)", "E0603", "module `fact_admission` is private"],
    ["evaluator_replayed_second_prepare_commit.rs", "E", "prepare_commit consumes the ReplayedRun, so one replay reaches at most one commit", "E0382", "use of moved value: `replayed`"],
]
def case_row(file, group, what, code, fragment):
    return row('crates/host/tests/refusal/cases/' + file, 'opensip-host', 'fixture',
        f"Compile-fail case for law X8 r3 (unit X5a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with exactly one error, {code}, {fragment}; group {group}: {what}. Synthetic; no compiler qualification.")
ADDED = [
    row('crates/evaluator/src/unavailable_evidence.rs', 'opensip-evaluator', 'validator',
        "Classify which replay refusals are promised retained bytes the supplied inputs lack (law X5 r3 item 5a; unit X5a): the exported inert UnavailableEvidence (Object(key) or Blob(raw digest), whose reference is the key or the digest as 64 lowercase hex) and ReplayError::unavailable_evidence, which descends every variant of ReplayError and of each evaluator and identity error type reachable from it (the walk, evaluation, reconstruction, native, plan, policy, stage, predicate, view, import, payload, run-link, body, coverage and enumeration-join errors; GraphError, RetainedInputError and CaptureError) and returns Some exactly for RetainedInputError::MissingObject and MissingBlob wherever they are nested, because replay_run walks the whole closure before any top-level read. Every match is exhaustive with no wildcard arm, so a new variant does not compile until it is classified; a text-only payload is never inspected; pure, no I/O, grants nothing, and replay_run is unchanged. Its cfg(test) module checks Some at every nesting (top level, the walk's Graph and native Retention, the evaluation's Reconstruction), None for every other refusal and for text that names a missing input, the reference spelling, and pins the descent's twenty-four types with no wildcard arm and no text inspection."),
    row('crates/host/src/fact_admission_tests.rs', 'opensip-host', 'test',
        "Check X5a (law X5 r3 item 8, host side), included as fact_admission.rs's cfg(test) module, on the synthetic replay corpus with no scratch installation: all 101 cases go through replay_candidate with REPLAY_LIMITS, the lawful ones returning the claimed RunId, the forged-output ones evidence.regeneration-mismatch with the claimed RunId as subject, and the corpus missing-blob case evidence.missing with its digest although the evaluator reports it under the walk; removing each member of one lawful case's claimed closure, one at a time, is evidence.missing naming exactly that reference, and removing an ambient member still replays; schema and identity failures are EVALUATION.INPUT_REFUSED on the provider-return route; every ReplayError variant maps to its row and remedy, each rendered through the shared failure envelope valid against command-envelope v7 with no run member; the remedies equal the fault-contract routes and identity carriers byte for byte; REPLAY_LIMITS holds item 5e's values, each of its nine dimensions admits the corpus at its measured exact need, at most the constant, and refuses one below on the structural row, and the capture-entry bound holds at the constant itself with ambient padding; and source pins show the join calls replay_run exactly once, mints no ReplayedRun, RunId or verdict, wires no check_plan_pack and reaches no custody, storage, ledger or I/O, and that every production caller passes REPLAY_LIMITS (vacuous until X7a), with a self-check refusing caller-chosen limits."),
] + [case_row(*c) for c in CASES]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert any(r['path'] == 'crates/host/src/fact_admission.rs' for r in inherited['files']), 'fact_admission.rs is a planned row of the parent'
host = next(p for p in inherited['packages'] if p['id'] == 'opensip-host')
assert 'opensip-evaluator' in host['dependencies'], 'the host -> evaluator edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive replay join layout (law X5 r3, unit X5a: the evaluator unavailable-evidence accessor and the host replay join, with law X8 r3 item 3 owner rows); library only, nothing replays into a commit from a command; no release, custody, profile, boot or creator qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + len(ADDED)
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / prior_path).read_bytes())
assert prior['candidate'] == parent, f'{parent_name} is not the selected {parent_unit} candidate'
# Bound supersessions on the parent (VD1): path -> (before, after). Each
# names its row's current effective description as its before.
supersessions = {}
for binding in lock['contractSuccessors']:
    assert pin(binding['record']['path']) == binding['record'], binding['record']['path']
    for s in json.loads((A / binding['record']['path']).read_bytes()).get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        i = int(s['selector']['jsonPointer'].split('/')[2])
        path = inherited['files'][i]['path']
        assert path not in supersessions, f'two supersessions of {path}'
        supersessions[path] = (s['before'], s['after'])
# The lock's inheritance rows bind exactly the prior record's projection to
# the parent; each is carried by stable file path to its new index, with any
# bound supersession folded into its effective description.
bound = {json.dumps(o['selector'], sort_keys=True): o for o in lock['inventoryPassageInheritance']}
assert len(bound) == len(prior['descriptionOverrideProjection']) == 55
projection = []
for p in prior['descriptionOverrideProjection']:
    o = bound[json.dumps(p['candidateSelector'], sort_keys=True)]
    assert o['parent'] == parent and o['before'] == p['before'] and o['after'] == p['effectiveDescription'], p['filePath']
    i = int(p['candidateSelector']['jsonPointer'].split('/')[2])
    assert inherited['files'][i]['path'] == p['filePath'] and inherited['files'][i]['description'] == p['before'], p['filePath']
    effective = p['effectiveDescription']
    if p['filePath'] in supersessions:
        before, after = supersessions.pop(p['filePath'])
        assert before == effective, f'{p["filePath"]}: a supersession must name the current meaning'
        effective = after
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': effective})
assert not supersessions, f'supersessions of rows with no inheritance entry: {sorted(supersessions)}'
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 55
folded = sum(1 for p, q in zip(sorted(prior['descriptionOverrideProjection'], key=lambda p: p['filePath']), projection) if p['effectiveDescription'] != q['effectiveDescription'])
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive replay join layout (law X5 r3, unit X5a, with law X8 r3 item 3 owner rows); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, all bound to {parent_name} by the lock' + (f', with {folded} bound passage supersessions folded into their effective descriptions' if folded else '') + '. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'supersessionsFolded': folded}))
