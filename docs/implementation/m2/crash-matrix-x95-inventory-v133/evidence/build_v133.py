"""Build inventory133 by adding exactly the two X9-5 rows (law X9 r15 item 12
with r10 to r13, unit X9-5: host's crash-matrix target and its separate
required-runs file) to the inventory the real product lock selects, and write
its successor record. The parent follows the lock: inventory131 (unit X9-2,
selected at product b999ae3 and still at eb0d503, where X9-3 landed with no
inventory successor; its fifty-five inheritance rows bound with D1's
thirty-nine overrides and D2's four supersessions already folded). It
projects the fifty-five rows inherited through the parent. Host's support
module, its manifest and security's site pins are already planned rows;
their bytes change, their rows do not.

A contract successor the lock binds may supersede an inherited row on the
parent (law VD1 item 3). Each such supersession is folded into its row's
inheritance entry: the entry's before stays the raw row text and its
effective description becomes the supersession's after. The row count stays
fifty-five. At product eb0d503 no supersession names inventory131, so
nothing new is folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory133. Usage: build_v133.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v133.json'
RECORD = M + 'crash-matrix-x95-inventory-v133/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v131.json': (M + 'crash-matrix-x92-inventory-v131/successor.json', 'inventory131', 'X9-2'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory133 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/host/tests/commit_matrix_tests.rs', 'opensip-host', 'test',
        "The crash matrix's host rows (law X9 r15 item 12, unit X9-5, with r10 to r13): F01, F12's and F40's caller route, F16, F17, F32 with X3b item 13's rollover crash table, F39's delivery half and F53's store-gc step, run through host's own commit coordinator and store-gc step in fresh processes. Built only with an explicit --features crash-matrix (required-features), and whole-file under the support predicate. Its children are this binary re-executed by X9-0's driver under the scripted wall clock: fixture; candidate (r10's host order: one operation entry, CommitSession::open, X3d-3's candidate and r12's distinct variant written to disk with the session's core closure, then the session's refused end); finalize (host's finalize_commit runner, which replays before any custody); store-gc (host's store_gc runner); recover; and a publisher that revokes the session's core closure under the installation fence. The parent transcribes nothing: it runs each reviewed host required row's script step by step by blocking record reads, records r12's timing guard on the parent's monotonic clock for runs that arm the observer tick, captures the post state, runs item 8's ladder through host where a row leaves an attempt, and writes one run record per run and the run set's matrix.json with r11's three-run host census. Nothing sleeps, polls or waits on a timer. Synthetic; no compiler qualification."),
    row('crates/host/tests/fixtures/crash-matrix/required-runs.v1.json', 'opensip-host', 'fixture',
        "Host's reviewed required runs of the crash matrix (law X9 r10: X9-5's rows only, a file separate from storage's), opensip.x9.required-runs.v1 canonical JSON with storage's clockEpoch. Unit X9-5 transcribes its 94 rows (F01 4, F12 2, F16 1, F17 1, F32 76, F39 1, F40 3, F53 6) from law X9 r15 before any lead run: F32's kill points and their crash-table windows from the unarmed host census's exhausted-carrier run, and every expected value from the law's row or the owning law's outcome it names, never read back from a run. Each row names its case, variant, owning units, labels, a step-by-step script (candidate variants, the reserved-slot plant, arms, runs, awaits with kill, revocation or live-writer actions, mutations, and r12's distinct R2) and expected per-step values. Host's crash-matrix target reads it; tools/check_crash_matrix.py check-unit --unit X9-5 checks run sets against it, and X9-6's check takes it beside storage's file. Synthetic; no compiler qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# Host's matrix target calls only along edges the parent already declares:
# host to storage, security, evaluator, identity and platform.
for crate, edges in (('opensip-host', ('opensip-storage', 'opensip-security', 'opensip-evaluator', 'opensip-identity', 'opensip-platform')),):
    package = next(p for p in inherited['packages'] if p['id'] == crate)
    for edge in edges:
        assert edge in package['dependencies'], f'the {crate} -> {edge} edge is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive crash-matrix layout (law X9 r15 item 12, unit X9-5: host\'s crash-matrix target and its reviewed required runs); a test target built only with the crash-matrix feature and its test-only data; no release, custody, profile, boot, trust or creator qualification'
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
    'standing': 'PROPOSED additive crash-matrix layout (law X9 r15 item 12, unit X9-5); independent review and lead assent required',
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
