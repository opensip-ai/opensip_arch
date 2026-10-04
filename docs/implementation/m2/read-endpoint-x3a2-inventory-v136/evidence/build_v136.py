"""Build inventory136 by adding exactly two rows, the read side's lent
selected store endpoint and its tests (unit X3a-2, law X3a r5 items 4 and 8:
crates/security/src/installation_endpoint.rs and
crates/security/src/installation_endpoint_tests.rs), to the inventory the
product lock selects, and write its successor record.

The parent follows the lock: inventory135 (unit M3-P0, selected at product
5e25d04 and still at 3f6f9a5). The changed host and storage readers
(installation_selection.rs, installation_records.rs, installation_lineage.rs,
native_marker.rs) and the changed security files are already planned rows;
their bytes change, their rows do not. Their descriptions are refreshed by
the unit's description successor (read-endpoint-x3a2-descriptions), which
binds directly to inventory136.

Projection. The lock binds one hundred inheritance rows to inventory135 (the
sixteen carried unchanged from inventory81 onward, D1's thirty-nine
overrides with D2's four supersessions folded, and D3's forty-five overrides
with its seventeen supersessions folded, all projected at inventory135). No bound
contract successor has a passage on inventory135. Once inventory136 is
selected, inventory135 is an ancestor and the one hundred rows are inherited
by stable file path; the rows sorted after the two inserted paths move by
two.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory136. Usage: build_v136.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v136.json'
RECORD = M + 'read-endpoint-x3a2-inventory-v136/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound its inherited
# rows.
PRIOR = {
    M + 'repository-file-inventory.v135.json': (M + 'm3-p0-scaffolds-inventory-v135/successor.json', 'inventory135', 'M3-P0'),
}
INHERITED, DIRECT, FOLDED = 100, 0, 0
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory136 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/installation_endpoint.rs', 'opensip-security', 'composition',
        "Lend the read session's selected store endpoint to the installation readers outside security (law X3a r5 item 4, unit X3a-2). InstallationReadFence::store_endpoint runs the session's endpoint admission (the retained values validated in memory on the session ledger, then one full session recheck; any refusal latches and carries its law X3a item 5 row) and returns a ReadStoreEndpoint borrowed from that fence: no public constructor, not Clone, not serializable. It lends the decoded selection pair, S from the opened endpoint marker, the marker bytes and the admitted node chain of the session's one read, at most MAX_LINEAGE_NODES nodes. Its recheck is the session's full recheck, which compares every required file's full sample. Its filesystem samples (the pair's; I's, the fence carrier's and the marker's) each follow a full recheck; a file is reopened no-follow by its name under the retained I, judged private, must keep the session's full sample and must be on H's filesystem. It reads and captures no file. It grants only the base a later owner §8 binding is derived from: no namespace, project, lease, journal, ledger, blob, commit or trust authority."),
    row('crates/security/src/installation_endpoint_tests.rs', 'opensip-security', 'test',
        "Check the lent endpoint on scratch account homes with a creator-published P0: the fence lends the endpoint of its one read (the files' bytes as read, S from the marker, the one root node), a second lend shares the same retained values, and the admission is charged; an in-place rewrite of the pair, the marker, the root node or state.v1 after the read fails the readers' recheck as required-files-changed and latches; the readers' samples are H's and follow the full recheck, and a marker replaced at its name refuses the sample itself and latches; and on a 48-deep home a 64-node chain (G 0 to 63) is lent whole, with two endpoint admissions and two reader rechecks within the owner's caps, totals printed."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# Both rows belong to opensip-security, an existing package; no edge is
# added or changed.
packages = {p['id']: p for p in inherited['packages']}
assert packages['opensip-security']['path'] == 'crates/security', 'the security package is declared in the parent'
planned = {r['path'] for r in inherited['files']}
CHANGED = ['crates/host/src/installation_lineage.rs', 'crates/host/src/installation_records.rs',
           'crates/host/src/installation_selection.rs', 'crates/security/src/custody/installation_read.rs',
           'crates/security/src/custody/installation_read_tests.rs', 'crates/security/src/custody/store_endpoint.rs',
           'crates/security/src/installation_observation.rs', 'crates/security/src/lib.rs',
           'crates/storage/src/store_root/native_marker.rs']
assert set(CHANGED) <= planned, 'a changed path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive read-side endpoint layout (unit X3a-2, law X3a r5 items 4 and 8): the read session\'s selected store endpoint lent to the host and storage installation readers, and its tests; the changed readers use rows already planned; no package edge, no release, distribution, custody, profile, boot, trust or creator qualification'
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
moved = sum(p['parentSelector'] != p['candidateSelector'] for p in projection)
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive read-side endpoint layout (unit X3a-2); independent review and lead assent required',
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
    'projectionRule': f'Resolve all {INHERITED} effective descriptions by stable file path from the meanings the lock binds to {parent_name}: its {INHERITED} inheritance rows (the sixteen carried unchanged from inventory81 onward, D1\'s thirty-nine overrides with D2\'s four supersessions folded, and D3\'s forty-five overrides with its seventeen supersessions folded, as inventory135 projected them). No bound contract successor has a passage override or supersession on {parent_name}. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'inherited': INHERITED, 'direct': DIRECT, 'supersessionsFolded': folded, 'selectorsMoved': moved}))
