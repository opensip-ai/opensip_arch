"""Build inventory137 by adding exactly two rows, the cfg(test) modules of
unit J2a's pure invocation model and outcome matrix (law M3-J1 r5 items 4,
5, 8 and 10: crates/host/src/invocation_tests.rs and
crates/host/src/outcomes_tests.rs), to the inventory the product lock
selects, and write its successor record.

The parent follows the lock: inventory136 (unit X3a-2, selected at product
cca4fe4 and still at d2c00a9). The production files the unit writes,
crates/host/src/invocation.rs (new bytes for a row planned since the
original inventory), crates/host/src/outcomes.rs and crates/host/src/lib.rs,
are already planned rows; their bytes change, their rows do not. No
description successor accompanies this inventory.

Projection. The lock binds one hundred inheritance rows to inventory136
(inventory135's one hundred, re-parented at X3a-2's integration), and the
bound description successor read-endpoint-x3a2-descriptions has three
direct overrides on inventory136 (installation_records.rs,
installation_selection.rs, native_marker.rs). No bound contract successor
has a passage supersession on inventory136. Once inventory137 is selected,
inventory136 is an ancestor and all one hundred and three meanings are
inherited by stable file path; the rows sorted after each inserted path
move by one per inserted path before them.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory137. Usage: build_v137.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v137.json'
RECORD = M + 'host-invocation-j2a-inventory-v137/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound its inherited
# rows.
PRIOR = {
    M + 'repository-file-inventory.v136.json': (M + 'read-endpoint-x3a2-inventory-v136/successor.json', 'inventory136', 'X3a-2'),
}
DESCRIPTIONS = M + 'read-endpoint-x3a2-descriptions/successor.json'
INHERITED, DIRECT, FOLDED = 100, 3, 0
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory137 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/host/src/invocation_tests.rs', 'opensip-host', 'test',
        "Check J2a (law M3-J1 r5 items 4, 5, 8 and 10, host side), included as invocation.rs's cfg(test) module, with no installation, home, lock, process or signal: the three M3 requests (default, analyze, analyze --ephemeral) build [analysis, render] with retry none and R2's Creator, Creator and Outside entries; WS section 1's step-list rules on the WFC refusal cases (forward and self dependency; duplicate, unknown and ninth dependency; 65 and no steps; a terminal gate on analysis; a required step on an optional one; a retried mutation), each item 10's row 2 with its workflow key in the operational record, and the lawful WFC lists passing; the durable join chain J-alpha to J-iota and the ephemeral one without J-gamma and J-iota, ending step 0 at any join; every operation point's cancel phase, with LD-r5-1's B and C after a publish return; the cancellation source's effects, ordinals and deciding signal; settlement on the WFC cases M3's step lists express (default-analyze-render-success with retry none, policy-failed-with-run, ephemeral-result-has-no-run-and-no-authority, indeterminate-provider-unavailable, operational-fault-dominates-committed-policy-failure, cancel-before-settle-is-interrupted, cancel-after-settle-not-reclassified, cancel-mid-invocation-with-committed-run as phase D, host-io-not-retried); 8.3's rules 1 to 4; phase O's deferral; a renderer failure routed by committed evidence, with an uncertain step 0's ExecutionId and namespace disclosed beside the primary termination; an unrenderable failure envelope and a failed write ending exit 4 with no replacement; and WS:233-240's aggregate with its tie rule."),
    row('crates/host/src/outcomes_tests.rs', 'opensip-host', 'test',
        "Check J2a's M3 outcome matrix (law M3-J1 r5 item 10), included as outcomes.rs's cfg(test) module: every row's class, exit, error code, fault cause, detail, subject, runId and executionId, each validated against the selected common-v4 StepTermination schema, with D9's exit and fault pairing (host-invariant included); the internal keys of the rows that carry no detail kept for the operational record; rows 1 and 49 after FinalGate admission without a termination; row 56 (SD-5, conformed by SD-7) naming the least manifestDigest then the first class, with every refusal recorded and the conformed remedy, and row 57 (SD-7) naming the first request class with PROVIDER.NOT_SELECTED's widened remedy, both distinct from row 27; the native deficiency bridge and D9's reason map restated; ordered distinct deficiencies; NE section 10's public route registry restated key by key with each origin and envelope detail; the subject bound with its SHA-256 elision; the D9 v1.14 goldens of the analysis path; and authority on committed and ephemeral results."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# Both rows belong to opensip-host, an existing package; no edge is added
# or changed.
packages = {p['id']: p for p in inherited['packages']}
assert packages['opensip-host']['path'] == 'crates/host', 'the host package is declared in the parent'
planned = {r['path'] for r in inherited['files']}
CHANGED = ['crates/host/src/invocation.rs', 'crates/host/src/lib.rs', 'crates/host/src/outcomes.rs']
assert set(CHANGED) <= planned, 'a changed path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive host invocation-model layout (unit J2a, law M3-J1 r5 items 4, 5, 8 and 10): the cfg(test) modules of the pure invocation model and the M3 outcome matrix; the production files use rows already planned; no package edge, no release, distribution, custody, profile, boot, trust or creator qualification'
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
supersessions, direct_records = {}, set()
for binding in lock['contractSuccessors']:
    assert pin(binding['record']['path']) == binding['record'], binding['record']['path']
    record_doc = json.loads((A / binding['record']['path']).read_bytes())
    for o in record_doc.get('passageOverrides', []):
        if o['parent'] != parent:
            continue
        f = file_at(o['selector'])
        assert f['description'] == o['before'] and f['path'] not in meanings, f['path']
        meanings[f['path']] = o; sources[f['path']] = 'direct'; direct_records.add(binding['record']['path'])
    for s in record_doc.get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        path = file_at(s['selector'])['path']
        assert path not in supersessions, f'two supersessions of {path}'
        supersessions[path] = s
assert sum(v == 'inherited' for v in sources.values()) == INHERITED and sum(v == 'direct' for v in sources.values()) == DIRECT
assert direct_records == {DESCRIPTIONS}, f'direct overrides from {sorted(direct_records)}'
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
moved = sum(p['parentSelector'] != p['candidateSelector'] for p in projection)
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive host invocation-model layout (unit J2a); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'plannedRowsChanged': CHANGED,
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all {INHERITED + DIRECT} effective descriptions by stable file path from the meanings the lock binds to {parent_name}: its {INHERITED} inheritance rows (inventory135\'s one hundred, re-parented at X3a-2\'s integration: the sixteen carried unchanged from inventory81 onward, D1\'s thirty-nine overrides with D2\'s four supersessions folded, and D3\'s forty-five overrides with its seventeen supersessions folded), and the {DIRECT} direct overrides of the bound description successor read-endpoint-x3a2-descriptions on {parent_name}. No bound contract successor has a passage supersession on {parent_name}. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'inherited': INHERITED, 'direct': DIRECT, 'supersessionsFolded': folded, 'selectorsMoved': moved}))
