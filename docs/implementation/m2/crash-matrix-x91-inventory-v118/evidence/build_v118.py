"""Build inventory118 by adding exactly the eight X9-1 rows (law X9 r2 item
12: the crash-matrix support surface of security, storage and host, the
pinned shared fixture-gate site list of law X8 r3 item 4b, and the census of
the integrated path) to the inventory the real product lock selects, and
write its successor record. The parent follows the lock: inventory128 (unit
X11a, selected at product 099de03, its fifty-five inheritance rows bound
with D1's thirty-nine overrides and D2's four supersessions already folded);
PRIOR also maps inventory125, inventory126 and inventory127, so a
parent-only rebuild follows whichever the lock selects. It projects the
fifty-five rows inherited through the parent.

A contract successor the lock binds may supersede an inherited row on the
parent (law VD1 item 3). Each such supersession is folded into its row's
inheritance entry: the entry's before stays the raw row text and its
effective description becomes the supersession's after. The row count stays
fifty-five. At product 099de03 no supersession names inventory128, so
nothing new is folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory118."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v118.json'
RECORD = M + 'crash-matrix-x91-inventory-v118/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v125.json': (M + 'finalization-x7a-inventory-v125/successor.json', 'inventory125', 'X7a'),
    M + 'repository-file-inventory.v126.json': (M + 'recovery-admission-x6b-inventory-v126/successor.json', 'inventory126', 'X6b'),
    M + 'repository-file-inventory.v127.json': (M + 'settlement-sweep-x6c-inventory-v127/successor.json', 'inventory127', 'X6c'),
    M + 'repository-file-inventory.v128.json': (M + 'cli-pins-x11a-inventory-v128/successor.json', 'inventory128', 'X11a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory118 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
GUARD = ('Compiled only under the test-only crash-matrix feature, which no manifest enables from a dependency table and which the '
         'crate refuses in any build without debug assertions (law X9 r1 item 2), so it is absent from every release build.')
ADDED = [
    row('crates/security/src/crash_matrix_support.rs', 'opensip-security', 'service',
        "Security's synthetic crash-matrix support surface (law X9 r1 item 6, unit X9-1), doc(hidden). " + GUARD + " It produces inputs on disk and returns paths, values and outcomes, never an authority type: SyntheticInstallation (create, or open by paths in a matrix child) through the real creator path with InitialCore's injected loaded image and the synthetic V2 profile set; X4T-0's signed accepted store written in place; publish_revocation, a thin caller of the shared fenced state.v1 publisher, returning the revocation version before and after; the inherited format-1 and format-2 carrier fixture; X3b-2's reserved-slot technique; and the FIXTURE and PROFILE_STANDING labels every run records. Every producer is a thin caller of a site on the pinned shared fixture-gate list. Synthetic; no compiler qualification."),
    row('crates/security/src/crash_matrix_support/post_state.rs', 'opensip-security', 'service',
        "Law X9 r1 item 7's post-state (unit X9-1), under the test-only crash-matrix feature: raw (every regular file under a scratch root by relative path, size and SHA-256), logical (every SQLite database dumped table by table from a private copy of its file and -wal, the operational witness and floor files decoded, the object set, and trustState, the trust store reduced to one digest over its files normalized one by one) and normalizedSha256 (logical with every drawn value, ExecutionId, op- and req1_ token, staging and temporary-name nonce, drawn identifier, digest over drawn content and timestamp, replaced by a placeholder numbered in order of first appearance, members ordered by their unnumbered shape, and every native clock sample or wall-clock datum replaced by its member name alone, law X9 r2 item 7). Capturing opens, locks, checkpoints and creates nothing under the root."),
    row('crates/security/src/crash_matrix_support/run_record.rs', 'opensip-security', 'service',
        "Law X9 r1 item 7's run writer (unit X9-1, with law X9 r2 items 3 and 6), under the test-only crash-matrix feature: one canonical opensip.x9.run.v1 record per run, runs/<case>-<variant>.json, never replacing an existing file, carrying the product, the host with the synthetic-signed-v2 fixture and BASELINE-ATTESTED standing, the run set's clock (epoch and the x9-ordinal-3600 script), each child's role, ordinal, exit, lastHeld point, trace record count and digest (X9-0's trace lines without the process id) and outcome, the post-state, the ladder, the transcribed expected value and the caller's verdict; and a census with its kill set in matrix.json's shape. It records and decides no verdict."),
    row('crates/security/src/crash_matrix_census.rs', 'opensip-security', 'test',
        "X9-1's census of security's integrated path and its verified kills (law X9 r1 items 5 and 12, r2 item 3), compiled only for this crate's tests with the crash-matrix feature. Every process of a run is a matrix child under the scripted wall clock numbered in spawn order: a fixture child at ordinal 0 publishes the synthetic installation, X4T-0's accepted store and a project root; the next child drives X1's writer, X2c's first registration, X2d's namespace and leases, X3b's floor step, creation and start, X2e's handoff with X4a's monitor, SEAL, REV and CLN appends, the end path, an exhausted generation's rollover, an EXCLUSIVE operation and the shared fenced publisher. Unarmed and traced, its records are the pinned census (277 points, kill set 437), with no durability primitive outside a scope, and two census runs agree point for point. Verified SIGKILL deaths and injected failures: the pending-witness rename (the next writer reverts), the SEAL commit (it advances), fail-after and fail-before at the SEAL commit, the fence and lease freed by the kernel, a held lease resumed to the census outcome, and the trust pointer rename; two runs' post-states differ raw and agree normalized, trust store included; and a killed run recorded in the checker's run shape."),
    row('crates/security/src/crash_matrix_sites.rs', 'opensip-security', 'test',
        "X9-1's pin of every source site that names a test-only feature (law X9 r1 item 6, law X8 r3 item 4b), in every security test build: it scans every cfg and cfg! in crates/*/src and crates/*/tests and requires exactly the pinned table, the shared fixture gates under the one joint predicate any(test, feature = crash-matrix, feature = scenario-fixtures) (Image::Injected with the injected image and synthetic V2 profile set, HomeSource::Fixture with the creator path on a scratch H and the gate's test constructor, X4T-0 and its accessor, and the fenced state.v1 publisher, each with the closure it needs), the crash-matrix-only carrier fixtures, each crate's guard and support module, the census tests and X9-0's and X9 r2's platform sites; with a scanner self-test, a no-sleep pin over X9-1's sources, and tests of the shared producers (accepted trust installed, the fenced publisher advancing the revocation version and refusing without writing while another holder has the fence, a writer admitted) and of the inherited carrier fixture."),
    row('crates/storage/src/crash_matrix_support.rs', 'opensip-storage', 'service',
        "Storage's crash-matrix support surface (law X9 r1 item 6, unit X9-1), doc(hidden). " + GUARD + " It forwards security's surface unchanged; the shared fixture gates live in security, so storage adds no second site. Nothing here returns an authority type."),
    row('crates/storage/src/ledger_store/project_commit_census.rs', 'opensip-storage', 'test',
        "X9-1's census of storage's ledger path (law X9 r1 items 5 and 12, r2 item 3), a child module of X3c-2's tests compiled only with the crash-matrix feature, reusing their crate-private scratch location with its held writer.lease named x2.lease.writer: in a matrix child under the scripted clock, the store directories and ledger creation, the attempt row, two objects, the evidence transaction, its four stagings and its COMMIT. Unarmed and traced, its records are the pinned census (46 points, kill set 70). Verified deaths and injections: after the attempt commit (the admitted row only), a torn object write (unadopted staging residue), before the evidence commit (rolled back, the objects kept) and fail-after and fail-before at the evidence commit (undetermined either way). And the forwarded support surface works from storage, where security has no cfg(test): a synthetic installation, accepted trust, the fenced publisher, open by paths, the post-state, and the inherited carrier fixture."),
    row('crates/host/src/crash_matrix_support.rs', 'opensip-host', 'service',
        "Host's crash-matrix support surface (law X9 r1 item 6, unit X9-1), doc(hidden). " + GUARD + " It forwards storage's surface, which forwards security's, unchanged; item 6's synthetic run candidate for the evaluator's replay joins it with X9-5. Nothing here returns an authority type."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
for crate, edges in (('opensip-security', ('opensip-platform',)), ('opensip-storage', ('opensip-security', 'opensip-platform')),
                     ('opensip-host', ('opensip-storage', 'opensip-security', 'opensip-platform'))):
    package = next(p for p in inherited['packages'] if p['id'] == crate)
    for edge in edges:
        assert edge in package['dependencies'], f'the {crate} -> {edge} edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive crash-matrix support layout (law X9 r2, unit X9-1: the test-only support surface of security, storage and host, the pinned shared fixture-gate site list, the barrier points at the integrated sites, the scripted wall clock and the census of the integrated path); test-only, absent from every build without the crash-matrix feature; no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive crash-matrix support layout (law X9 r2, unit X9-1); independent review and lead assent required',
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
