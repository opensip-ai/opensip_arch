"""Build inventory125 by adding exactly the ten X7a rows (law X7 r5 items 1
to 5, 8 and 10, read under X3b r10, X3d r6, X5 r3, X6 r3, X8 r3, X9 r1 and
X12 r3:
the host finalization tests and law X8 r3 item 3's owner rows for this unit,
groups A, B, D, E and G) to the inventory the real product lock selects, and
write its successor record. The parent follows the lock: inventory124 (unit
X6a, selected at product 81214cb, its fifty-five inheritance rows bound with
D1's thirty-nine overrides and D2's four supersessions already folded).
crates/host/src/finalization.rs is already a planned row of the parent, so
it is kept by value and not added. It projects the fifty-five rows inherited
through the parent.

A contract successor the lock binds may supersede an inherited row on the
parent (law VD1 item 3). Each such supersession is folded into its row's
inheritance entry: the entry's before stays the raw row text and its
effective description becomes the supersession's after. The row count stays
fifty-five. At product 81214cb no supersession names inventory124, so
nothing new is folded; D2's four are already in the parent's projection.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory125."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v125.json'
RECORD = M + 'finalization-x7a-inventory-v125/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v124.json': (M + 'recovery-capture-x6a-inventory-v124/successor.json', 'inventory124', 'X6a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory125 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
# Law X8 r3 item 3's owner rows for unit X7a (item 3c, and the export rule
# for the exported AuthoritativeRun): (file, group, what the case pins, the
# expected code, rustc 1.95.0's fragment).
CASES = [
    ["host_authoritative_run_raw_json.rs", "A", "the exported authoritative projection authoritative_run takes &PublishedCommit and nothing else, so a raw JsonValue holding a Run cannot stand in for it (X7 r5 item 2, DR-G27)", "E0308", "mismatched types"],
    ["host_authoritative_run_bool.rs", "B", "a boolean verified cannot stand in for the &PublishedCommit that authoritative_run takes", "E0308", "mismatched types"],
    ["host_authoritative_run_run_id.rs", "B", "a RunId &str cannot stand in for the &PublishedCommit that authoritative_run takes", "E0308", "mismatched types"],
    ["host_authoritative_run_replayed.rs", "B", "a replayed but uncommitted &ReplayedRun cannot stand in for the &PublishedCommit that authoritative_run takes, so replay alone never promotes a Run", "E0308", "mismatched types"],
    ["host_authoritative_run_literal.rs", "D", "the exported AuthoritativeRun cannot be forged as a struct literal; its fields are private and authoritative_run is its only constructor", "none", "cannot construct `AuthoritativeRun` with struct literal syntax due to private fields"],
    ["host_authoritative_run_default.rs", "D", "AuthoritativeRun has no Default", "E0277", "the trait bound `AuthoritativeRun: Default` is not satisfied"],
    ["host_authoritative_run_deserialize.rs", "D", "AuthoritativeRun cannot be read back from serialized bytes", "E0277", "the trait bound `AuthoritativeRun: serde::Deserialize<'de>` is not satisfied"],
    ["host_authoritative_run_clone.rs", "E", "AuthoritativeRun cannot be cloned", "E0277", "the trait bound `AuthoritativeRun: Clone` is not satisfied"],
    ["host_authoritative_run_serialize.rs", "G", "AuthoritativeRun cannot be serialized as a previous session's label", "E0277", "the trait bound `AuthoritativeRun: serde::Serialize` is not satisfied"],
]
def case_row(file, group, what, code, fragment):
    return row('crates/host/tests/refusal/cases/' + file, 'opensip-host', 'fixture',
        f"Compile-fail case for law X8 r3 (unit X7a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse fails with exactly one error, {code}, {fragment}; group {group}: {what}. Synthetic; no compiler qualification.")
ADDED = [
    row('crates/host/src/finalization_tests.rs', 'opensip-host', 'test',
        "Check X7a (law X7 r5 item 10, host side), included as finalization.rs's cfg(test) module, with no scratch installation, home or lock: every row of item 3's table through injected X3d outcomes (a delivered commit is authoritative with its RunId and the delivered exit 0, 1 or 3, with any optional failure disclosed beside it; a failed required delivery and a latch after admission are both DELIVERY.REQUIRED_FAILED, delivery-required, DELIVERY.RENDERER_FAILED_AFTER_COMMIT, exit 4, with the RunId retained; CommitUndetermined is DURABILITY.COMMIT_FAILED with the ExecutionId as subject, the namespace beside it, no RunId and the read-only recovery remedy; a refusal is its X3d item 9 row unchanged; ExistingAttempt is the invariant row with its ExecutionId as subject, the binding's namespace beside it and the later read-only recovery remedy, with no recovery in the writer's invocation; CarrierCapacityExhausted is item 6a's busy row naming the namespace); every caller-constructible CommitOutcome and NotPrepared joins one attempt; a failed end-path settlement is disclosed beside the outcome and never rewrites it; the delivery phase over a scripted renderer and sink (a latched commit starts nothing, a renderer, exit, write or flush failure fails once with no retry and no optional effect, an optional failure never changes the exit); over the synthetic replay corpus, a replay refusal ends before any admission on the replay join's row and remedy, and admission runs once after a successful replay with its refusal on its own row; an ephemeral label is never authoritative and has no RunId; and source pins show finalization is the host's only commit coordinator, its order (replay, admission, open, prepare, publish, finish, then delivery), the one authoritative literal inside authoritative_run(&PublishedCommit), no recovery, admission, gate, fence, ledger, lifecycle, retry or wildcard arm of its own, no 458c read entry, receipt or read session, X2 lease or storage reader (the delivery phase reads nothing from the store; only the commit facade's two exact use lines), and X9's two x7.delivery points. A ProjectOperation cannot be built from the host's tests before X9-1's support surface or X8b's scenario seam (law X9 r1 gap G1), so the session-level integration rows are not here. Synthetic fixtures; no compiler qualification."),
] + [case_row(*c) for c in CASES]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert any(r['path'] == 'crates/host/src/finalization.rs' for r in inherited['files']), 'finalization.rs is a planned row of the parent'
host = next(p for p in inherited['packages'] if p['id'] == 'opensip-host')
for edge in ('opensip-evaluator', 'opensip-security', 'opensip-storage', 'opensip-contracts', 'opensip-platform'):
    assert edge in host['dependencies'], f'the host -> {edge} edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive host finalization layout (law X7 r5, unit X7a: the finalization coordinator tests, with law X8 r3 item 3 owner rows); library only, nothing finalizes a commit from a command; no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive host finalization layout (law X7 r5, unit X7a, with law X8 r3 item 3 owner rows); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, with D2\'s four passage supersessions already folded into their effective descriptions, all bound to {parent_name} by the lock' + (f', with {folded} further bound passage supersessions folded into their effective descriptions' if folded else '') + '. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'supersessionsFolded': folded}))
