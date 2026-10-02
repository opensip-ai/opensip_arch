"""Build inventory129 by adding exactly the six X8b rows (law X8 r3 item 4:
the test-only scenario-fixtures seam of security and storage, their tests,
and group J's two compile-fail cases) to the inventory the real product
lock selects, and write its successor record. The parent follows the lock:
inventory118 (unit X9-1, selected at product a36da7c, its fifty-five
inheritance rows bound with D1's thirty-nine overrides and D2's four
supersessions already folded). It projects the fifty-five rows inherited
through the parent.

A contract successor the lock binds may supersede an inherited row on the
parent (law VD1 item 3). Each such supersession is folded into its row's
inheritance entry: the entry's before stays the raw row text and its
effective description becomes the supersession's after. The row count stays
fifty-five. At product a36da7c no supersession names inventory118, so
nothing new is folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory129. Usage: build_v129.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v129.json'
RECORD = M + 'scenario-fixtures-x8b-inventory-v129/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v118.json': (M + 'crash-matrix-x91-inventory-v118/successor.json', 'inventory118', 'X9-1'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory129 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
GUARD = ('Compiled only under the test-only scenario-fixtures feature, which is never default, is named by no [dependencies] table '
         'and is enabled only from storage\'s and host\'s [dev-dependencies] (law X8 r3 items 4a and 4f), so it is absent from every '
         'release build and from the plain cargo check -p opensip-host surface (group J).')
CASE = ('Compile-fail case for law X8 r3 (unit X8b), compiled only by admission_tests.rs\'s driver with the pinned rustc 1.95.0 against '
        'the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse compiles, and the misuse '
        'fails with exactly one error, E0432, ')
ADDED = [
    row('crates/security/src/scenario.rs', 'opensip-security', 'service',
        "Security's test seam for the refusal suite's behavioural cases (law X8 r3 item 4c, unit X8b), doc(hidden). " + GUARD + " ScenarioHome::create publishes a synthetic P0 under a 0700 scratch home below the caller's scratch parent, every path labelled synthetic, through the real creator path with InitialCore's injected loaded image and the synthetic V2 profile set, and installs X4T-0's signed accepted store (open names one by its paths for a helper process); project makes a scratch project root; operation runs the production chain to a ProjectOperation (X1's writer, X2's root admission, first registration for a first-use candidate, namespace and lease, X3a's endpoint, X4's lease-free first read and monitor, X3b's floor step and carrier start, X2e's handoff) through the shared installation fixture's one composition, each refusal its InstallationTermination row; publish_revocation_fenced calls the shared fenced state.v1 publisher at the next revocation version and refuses, writing nothing, in any process operation ever handed a lease to; revocation_version, paths and carrier_census are read-only. It constructs no authority type itself (only operation's production-chain ProjectOperation) and accepts no receipt, guard, gate, monitor, session, permit, ReplayedRun or clock. Synthetic; no compiler qualification."),
    row('crates/security/src/scenario_tests.rs', 'opensip-security', 'test',
        "Check X8b's security seam in security's own test build with scenario-fixtures (law X8 r3 item 4c), one ordered test because the lease flag is process-wide: the scratch home labelled synthetic with X4T-0's store at revocation version 1; the fenced publication advancing the version by one for an empty revocation and for an unrelated release, an unknown subject kind refused with state.v1 unchanged; a home opened by its paths; a first-use root registered and its ProjectOperation handed out, its paths present, the publication then refused on the invariant row with state.v1 unchanged; the operation ended; the registered root admitted again; an absent root refused; an unknown namespace with no carrier."),
    row('crates/storage/src/scenario.rs', 'opensip-storage', 'service',
        "Storage's test seam for the refusal suite (law X8 r3 item 4d, unit X8b), doc(hidden). " + GUARD + " Over security's ScenarioHome: ledger_census reads (S, N)'s evidence ledger read-only (each attempt_custody row's ExecutionId and phase, and the receipt count; an absent ledger an empty census); plant_attempt writes one admitted attempt_custody row for a given ExecutionId under a binding's (N, S, G, K) store-generation digest with a freshly drawn operationRef, through X3c-1's ordinary attempt admission after creating or admitting N's directory and ledger, as an earlier process would have left it (case B4), each refusal X3d r6 item 9's ledger row. It takes values and paths, never a session, receipt or lease, and returns no authority type. Synthetic; no compiler qualification."),
    row('crates/storage/src/scenario_tests.rs', 'opensip-storage', 'test',
        "Check X8b's storage seam in storage's test build with scenario-fixtures (law X8 r3 item 4d), over security's seam: a first-use operation opened as a CommitSession; no ledger before any commit; the session's own ExecutionId planted as one admitted row with no receipt and read back by the census; the same key refused on the invariant row and a name outside the store layout refused before any effect, the census unchanged; then the session finished as a certain refusal with one REV and no SEAL in the carrier census."),
    row('crates/host/tests/refusal/cases/security_scenario_unnameable.rs', 'opensip-host', 'fixture',
        CASE + "unresolved import `opensip_security::scenario`; group J: security's test seam is absent from the plain host surface, which opensip-cli builds against. Synthetic; no compiler qualification."),
    row('crates/host/tests/refusal/cases/storage_scenario_unnameable.rs', 'opensip-host', 'fixture',
        CASE + "unresolved import `opensip_storage::scenario`; group J: storage's test seam is absent from the plain host surface. Synthetic; no compiler qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# The feature forwards, and the dev-dependencies run, only along edges the
# parent already declares: storage to security; host to storage.
for crate, edges in (('opensip-storage', ('opensip-security',)), ('opensip-host', ('opensip-storage', 'opensip-security'))):
    package = next(p for p in inherited['packages'] if p['id'] == crate)
    for edge in edges:
        assert edge in package['dependencies'], f'the {crate} -> {edge} edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive scenario-fixtures layout (law X8 r3 item 4, unit X8b: the test-only scenario seams of security and storage, their tests and group J\'s compile-fail cases); test-only, absent from every build without the scenario-fixtures feature, which only [dev-dependencies] enable; no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive scenario-fixtures layout (law X8 r3 item 4, unit X8b); independent review and lead assent required',
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
