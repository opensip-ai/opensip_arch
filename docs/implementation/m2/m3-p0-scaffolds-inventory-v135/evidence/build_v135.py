"""Build inventory135 by adding exactly one row, the host-workspace dependency
selection policy tools/host/dependency-policy.json (unit M3-P0, plan
docs/implementation/m3/M3-PLAN-r6.md:208; law M3-C r7 item 12's pure-Rust
inflater row), to the inventory the real product lock selects, and write its
successor record.

The parent follows the lock: inventory134 (unit L1, selected at product
2967905 and still at cd5958b). The crates/components and crates/syntax
scaffolds (Cargo.toml and src/lib.rs of each), the root Cargo.toml and
Cargo.lock are already planned rows; their bytes are new or change, their
rows do not.

Projection. The lock binds fifty-five inheritance rows to inventory134 (the
sixteen carried from inventory81 onward and D1's thirty-nine overrides, with
D2's four supersessions folded). Contract successor D3 (description batch
d3) binds forty-five passage overrides and seventeen passage supersessions
directly to inventory134. Once inventory135 is selected, inventory134 is an
ancestor: its forty-five direct overrides are inherited too, and each of the
seventeen supersessions folds into the inherited row it names (law VD1). The
projection therefore has one hundred rows, seventeen of them folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory135. Usage: build_v135.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v135.json'
RECORD = M + 'm3-p0-scaffolds-inventory-v135/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound its inherited
# rows.
PRIOR = {
    M + 'repository-file-inventory.v134.json': (M + 'licence-l1-inventory-v134/successor.json', 'inventory134', 'L1'),
}
INHERITED, DIRECT, FOLDED = 55, 45, 17
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory135 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('tools/host/dependency-policy.json', 'tooling', 'registry',
        "Select, ahead of linking, the external crates that an accepted M3 law assigns to a host-workspace package: exact crate, version, crates.io checksum and archive size, licence, consumer and linking unit, declaration, resolved features, and build-script, links and unsafe facts (first rows, unit M3-P0: law M3-C r7 item 12's pure-Rust inflater and its one dependency, for unit C3a's CRATE-ARCHIVE-1 decoder in opensip-host). A row links nothing; the unit that links it declares the crate exactly as the row states and adds its closure check. The workspace's existing dependencies keep their own owners. Not a closure policy, native purity proof or product qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# The row belongs to the tooling package, which declares no dependency, so
# it adds no edge. The scaffold rows and both package rows already exist.
packages = {p['id']: p for p in inherited['packages']}
assert packages['tooling']['dependencies'] == [] and packages['tooling']['path'] == 'tools', 'the tooling package is declared in the parent'
assert packages['opensip-syntax']['path'] == 'crates/syntax' and packages['opensip-components']['path'] == 'crates/components'
planned = {r['path'] for r in inherited['files']}
REALIZED = ['crates/components/Cargo.toml', 'crates/components/src/lib.rs', 'crates/syntax/Cargo.toml', 'crates/syntax/src/lib.rs']
CHANGED = ['Cargo.lock', 'Cargo.toml']
assert set(REALIZED + CHANGED) <= planned, 'a scaffold path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive scaffold layout (unit M3-P0): the host-workspace dependency selection policy with law M3-C r7 item 12\'s pure-Rust inflater rows; the crates/components and crates/syntax scaffolds and their workspace membership use rows already planned; no package edge, no release, distribution, custody, profile, boot, trust or creator qualification'
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
def file_at(selector):
    parts = selector['jsonPointer'].split('/')
    assert len(parts) == 4 and parts[1] == 'files' and parts[2].isdigit() and parts[3] == 'description', selector
    return inherited['files'][int(parts[2])]
# Every meaning bound to the parent, by stable file path: the lock's
# inheritance rows, then each contract successor's direct override on the
# parent. Each must name its row's raw parent text as before.
meanings, sources = {}, {}
for o in lock['inventoryPassageInheritance']:
    assert o['parent'] == parent, 'an inheritance row is bound to another parent'
    f = file_at(o['selector'])
    assert f['description'] == o['before'] and f['path'] not in meanings, f['path']
    meanings[f['path']] = o; sources[f['path']] = 'inherited'
supersessions = {}
for binding in lock['contractSuccessors']:
    assert pin(binding['record']['path']) == binding['record'], binding['record']['path']
    record_doc = json.loads((A / binding['record']['path']).read_bytes())
    for o in record_doc.get('passageOverrides', []):
        if o['parent'] != parent:
            continue
        f = file_at(o['selector'])
        assert f['description'] == o['before'] and f['path'] not in meanings, f['path']
        meanings[f['path']] = o; sources[f['path']] = 'direct'
    for s in record_doc.get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        path = file_at(s['selector'])['path']
        assert path not in supersessions, f'two supersessions of {path}'
        supersessions[path] = s
assert sum(v == 'inherited' for v in sources.values()) == INHERITED and sum(v == 'direct' for v in sources.values()) == DIRECT
# The inherited rows are exactly the prior record's projection.
assert sorted((p['filePath'], p['before'], p['effectiveDescription']) for p in prior['descriptionOverrideProjection']) == \
       sorted((path, o['before'], o['after']) for path, o in meanings.items() if sources[path] == 'inherited')
projection, folded = [], 0
for path, o in sorted(meanings.items()):
    effective = o['after']
    if path in supersessions:
        s = supersessions.pop(path)
        assert s['before'] == effective and s['selector'] == o['selector'], f'{path}: a supersession must name the current meaning'
        effective = s['after']; folded += 1
    projection.append({'filePath': path, 'parentSelector': o['selector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[path]}/description"},
                       'before': o['before'], 'effectiveDescription': effective})
assert not supersessions, f'supersessions of rows with no bound meaning: {sorted(supersessions)}'
assert len(projection) == INHERITED + DIRECT and folded == FOLDED
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive scaffold layout (unit M3-P0); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'plannedRowsRealized': REALIZED,
    'plannedRowsChanged': CHANGED,
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all {INHERITED + DIRECT} effective descriptions by stable file path from the meanings the lock binds to {parent_name}: the {INHERITED} inheritance rows (the sixteen carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, with D2\'s four passage supersessions already folded) and contract successor D3\'s {DIRECT} direct passage overrides, with D3\'s {FOLDED} passage supersessions on {parent_name} folded into the effective descriptions of the inherited rows they name. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'inherited': INHERITED, 'direct': DIRECT, 'supersessionsFolded': folded}))
