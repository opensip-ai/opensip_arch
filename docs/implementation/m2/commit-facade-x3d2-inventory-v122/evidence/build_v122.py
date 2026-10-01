"""Build inventory122 by adding exactly the twenty-one X3d-2 rows (law X3d r6
items 1, 3, 4, 6, 8 and 9 and item 13's X3d-2 list: storage's commit facade;
law X8 r3 item 3's owner rows for PreparedCommit, PublishedCommit and the
facade's groups A to C and H) to the inventory the real product lock selects,
and write its successor record. The parent follows the lock: inventory119
(unit X3d-1, selected at product 8240856). crates/storage/src/commit.rs is
already a planned row whose description stays true, so it is kept by value
and not added. It projects the sixteen rows inherited through the parent. Run
with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory122.

Contract successor D1 (39 description overrides on inventory119) is bound in
the lock at product 7be09a7. As 461b's were at inventory81, its overrides
join the projection here: the inherited rows stay equal by value to
inventory119's bytes, and the projection grows from sixteen rows to
fifty-five (the sixteen bound to inventory119 and D1's thirty-nine)."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v122.json'
RECORD = M + 'commit-facade-x3d2-inventory-v122/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v119.json': (M + 'commit-session-x3d1-inventory-v119/successor.json', 'inventory119', 'X3d-1'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory122 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
# Law X8 r3 item 3's owner rows for unit X3d-2: (file, group, what the case
# pins, the expected code or none, rustc 1.95.0's message fragment).
CASES = [
    ["storage_prepare_commit_raw_json.rs", "A", "a raw JSON value holding a Run cannot stand in for the ReplayedRun that storage's prepare_commit takes", "E0308", "mismatched types"],
    ["storage_prepare_commit_contracts_run.rs", "A", "the generated contracts Run record (Identity3Run) cannot stand in for the ReplayedRun that prepare_commit takes", "E0308", "mismatched types"],
    ["storage_prepare_commit_bool.rs", "B", "a boolean verified cannot stand in for the ReplayedRun that prepare_commit takes", "E0308", "mismatched types"],
    ["storage_published_commit_verified.rs", "B", "no boolean verified field makes a PublishedCommit", "E0560", "has no field named `verified`"],
    ["storage_prepare_commit_retained_inputs.rs", "C", "structural-only input, the inert RetainedInputs, cannot stand in for the ReplayedRun that prepare_commit takes", "E0308", "mismatched types"],
    ["storage_prepared_commit_literal.rs", "D", "PreparedCommit cannot be forged as a struct literal", "none", "cannot construct `PreparedCommit` with struct literal syntax due to private fields"],
    ["storage_prepared_commit_default.rs", "D", "PreparedCommit has no Default", "E0277", "the trait bound `PreparedCommit: Default` is not satisfied"],
    ["storage_prepared_commit_deserialize.rs", "D", "PreparedCommit cannot be deserialized", "E0277", "the trait bound `PreparedCommit: serde::Deserialize<'de>` is not satisfied"],
    ["storage_prepared_commit_clone.rs", "E", "PreparedCommit cannot be cloned", "E0277", "the trait bound `PreparedCommit: Clone` is not satisfied"],
    ["storage_prepared_commit_serialize.rs", "G", "PreparedCommit cannot be serialized", "E0277", "the trait bound `PreparedCommit: serde::Serialize` is not satisfied"],
    ["storage_published_commit_literal.rs", "D", "PublishedCommit cannot be forged as a struct literal", "none", "cannot construct `PublishedCommit` with struct literal syntax due to private fields"],
    ["storage_published_commit_default.rs", "D", "PublishedCommit has no Default", "E0277", "the trait bound `PublishedCommit: Default` is not satisfied"],
    ["storage_published_commit_deserialize.rs", "D", "PublishedCommit cannot be deserialized", "E0277", "the trait bound `PublishedCommit: serde::Deserialize<'de>` is not satisfied"],
    ["storage_published_commit_clone.rs", "E", "PublishedCommit cannot be cloned", "E0277", "the trait bound `PublishedCommit: Clone` is not satisfied"],
    ["storage_published_commit_serialize.rs", "G", "PublishedCommit cannot be serialized", "E0277", "the trait bound `PublishedCommit: serde::Serialize` is not satisfied"],
    ["storage_prepare_commit_consumed_session.rs", "E", "a CommitSession consumed by prepare_commit cannot prepare a second commit", "E0382", "use of moved value: `session`"],
    ["storage_prepared_commit_publish_twice.rs", "E", "publish consumes the PreparedCommit, so it publishes once", "E0382", "use of moved value: `prepared`"],
    ["storage_prepared_commit_publish_adapter.rs", "H", "storage's facade takes no external adapter: publish takes none", "E0061", "this method takes 0 arguments but 1 argument was supplied"],
    ["storage_prepare_commit_seal_outcome.rs", "H", "storage's facade takes no external SealOutcome: prepare_commit takes the replay and the session alone", "E0061", "this function takes 2 arguments but 3 arguments were supplied"],
]
def case_row(file, group, what, code, fragment):
    reason = f'exactly one error without a code, {fragment}' if code == 'none' else f'exactly one error, {code}, {fragment}'
    return row('crates/host/tests/refusal/cases/' + file, 'opensip-host', 'fixture',
        f"Compile-fail case for law X8 r3 (unit X3d-2), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with {reason}; group {group}: {what}. Synthetic; no compiler qualification.")
ADDED = [
    row('crates/storage/src/commit_tests.rs', 'opensip-storage', 'test',
        "Check X3d-2's storage half without a session (storage cannot build a CommitSession: security's fixtures are cfg(test) there and law X8 r3 item 4's scenario-fixtures seam is X8b's), on a scratch private I/stores/S under the per-process scratch parent, with the evaluator's real replay of the corpus Run that security's SEAL tests replay, included as commit.rs's cfg(test) module: the plan declares exactly the retained typed objects (each frame its identity's H preimage, published under its H digest) and raw blobs, once each, and the commit inventory lists them; a Run of another project or another evaluator closure does not bind; the store generation digest is store-instance-lineage v1's recipe; a prepared commit publishes every frame and blob, stages the receipt (sequence 1, replayable, the unsigned local-custody signer), the thirteen-field association, the Run material, generation-0 retained availability and no pins with nothing visible to another connection until its one COMMIT, after which the pair joins the admitted attempt with settlement pending; the receipt counter orders stored canonical decimals by length then bytes (2, 9, 10, 100 give 101) and refuses a full u64 on the invariant row; a SEAL binding whose RunId, carrier digest or operationRef does not join stages nothing; an error from the evidence COMMIT is undetermined with the attempt still admitted; the publication reserve equals exactly what attempt admission and the objects charge, and one byte short refuses on the budget row before the attempt row and any object; a reused ExecutionId is refused before any object; every ledger row maps to its existing termination; and x3d.publish.published is placed once, after the one PublishedCommit construction."),
    row('crates/storage/src/schema_sources.rs', 'opensip-storage', 'adapter',
        "Supply storage's commit facade with the selected schema registry from compiled exact raw schema documents (the same files, in the order RegisteredSchemas::source_requirements pins), compiled once per process: the staging owners admit the Run manifest, the commit inventory and the availability record with it, the public prepare_commit(ReplayedRun, CommitSession) takes no registry (law X8 r3 group H), and storage cannot reach host's embedded copy. No runtime path lookup, schema fallback or semantic evidence authority; any absent, extra, reordered or replaced source refuses the whole registry by its full-document pin."),
] + [case_row(*c) for c in CASES]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert any(r['path'] == 'crates/storage/src/commit.rs' for r in inherited['files']), 'commit.rs is a planned row of the parent'
storage = next(p for p in inherited['packages'] if p['id'] == 'opensip-storage')
assert 'opensip-evaluator' in storage['dependencies'], 'the storage -> evaluator edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive storage commit facade layout (law X3d r6, unit X3d-2, with law X8 r3 item 3 owner rows); library only, nothing commits from a command; no release, custody, profile, boot or creator qualification'
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
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
# D1's accepted description overrides on inventory119, now inherited.
D1 = M + 'description-batch-d1/successor.json'
d1_pin = pin(D1)
assert any(c['record'] == d1_pin for c in lock['contractSuccessors']), 'D1 must be bound in the lock'
d1 = json.loads((A / D1).read_bytes())
assert len(d1['passageOverrides']) == 39
for o in d1['passageOverrides']:
    assert o['parent'] == parent, o['parent']
    i = int(o['selector']['jsonPointer'].split('/')[2])
    path = inherited['files'][i]['path']
    assert inherited['files'][i]['description'] == o['before'], path
    projection.append({'filePath': path, 'parentSelector': o['selector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[path]}/description"},
                       'before': o['before'], 'effectiveDescription': o['after']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 55
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive storage commit facade layout (law X3d r6, unit X3d-2, with law X8 r3 item 3 owner rows); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows bound to {parent_name}, carried unchanged from inventory81 onward, and the thirty-nine D1 description overrides on {parent_name}. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
