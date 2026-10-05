"""Build inventory140 by adding exactly the one row of unit I1-c, the X12c
preview pack's release row (law M3-I1 r3 item 5; contract successor I1-P), to
inventory139 (unit J3a), and write its successor record.

The one row is the bundled policy document
crates/evaluator/src/preview-typescript-pack.v1.policy.json, in the existing
opensip-evaluator package. The registry, policy.rs and the two test files
I1-c changes are planned rows of the parent; their rows are carried by value
(the README lists the descriptions this makes out of date). No package, edge,
crate dependency or pending decision changes.

The parent is inventory139 (unit J3a, built on inventory138, which the lock
at product 083ad5c selects, and not yet integrated), as the lead assigned:
the next number on the highest existing candidate. While the given lock still
selects inventory138, J3a's staged entry and its re-projected inheritance are
applied in memory from J3a's own evidence/verify_scratch.py (its SCRATCH-J3A
placeholders), exactly as J3a stages them; once J3a is integrated the lock
selects inventory139 directly. Only the parent's candidate, record and bound
meanings are used, which are the same either way.

Projection. Every meaning the lock binds to inventory139 is inherited by
stable file path once inventory140 is selected: the one hundred and three
inheritance rows inventory139 projected. No bound contract successor has a
passage override or supersession on inventory139.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory140. Usage: build_v140.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v140.json'
RECORD = M + 'preview-pack-i1c-inventory-v140/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
J3A = M + 'durable-entry-j3a-inventory-v139'
# Each admissible parent: the successor record that bound its inherited rows,
# its name, its unit, and the inherited, direct and folded meaning counts the
# lock binds to it.
PRIOR = {
    M + 'repository-file-inventory.v139.json': (J3A + '/successor.json', 'inventory139', 'J3a', 103, 0, 0),
}
def with_parent(lock):
    """The lock selecting inventory139: as given once J3a is integrated, else
    with J3a's staged entry applied in memory."""
    if lock['inventorySuccessors'][-1]['candidate']['path'] in PRIOR:
        return lock, 'integrated'
    spec = importlib.util.spec_from_file_location('j3a_scratch', A / J3A / 'evidence/verify_scratch.py')
    j3a = importlib.util.module_from_spec(spec); spec.loader.exec_module(j3a)
    return j3a.staged(lock), 'J3a staged in memory'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock, parent_mode = with_parent(json.loads(LOCK.read_bytes()))
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory140 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
ADDED = [
    {'path': 'crates/evaluator/src/preview-typescript-pack.v1.policy.json', 'package': 'opensip-evaluator', 'role': 'registry',
     'description': ("Embed the bundled PolicyDocumentV2 of the DR-131 preview pack opensip.preview.typescript.pack:1 (law M3-I1 r3 item 5, "
                     "contract successor I1-P; unit I1-c), compiled into the signed core with include_bytes! as the one RELEASE_PACKS.documents "
                     "entry, under the name the release row's policyDocument gives: exactly item 5.2's 574 canonical bytes with no trailing newline "
                     "(raw SHA-256 96675a5e..., the row's policySha256), one gating error rule module-import-cycle over typescript file subjects whose "
                     "emitWhen is the root-only cycle-representative atom on imports at resolved-target, contribution opensip.preview.typescript. "
                     "Admitted only by its exact packId; never read at run time, never admitted as supplied bytes, and never a release-declaration row."),
     'generated': False, 'standing': 'proposed'},
]
assert len(ADDED) == 1
# Planned rows whose bytes change. Their rows are carried by value; the
# README names the descriptions this makes out of date.
CHANGED = sorted([
    'crates/evaluator/src/pack-registry.json',
    'crates/evaluator/src/policy.rs',
    'crates/evaluator/src/policy_pack_tests.rs',
    'crates/host/src/configuration_tests.rs',
])
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit, INHERITED, DIRECT, FOLDED = PRIOR[selected['path']]
assert lock['inventorySuccessors'][-1]['record']['path'] == prior_path, 'the selected inventory has another successor record'
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
packages = {p['id']: p for p in inherited['packages']}
assert packages['opensip-evaluator']['path'] == 'crates/evaluator', 'the opensip-evaluator package is declared in the parent'
planned = {r['path'] for r in inherited['files']}
assert set(CHANGED) <= planned, 'a changed path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = ('PROPOSED additive release policy document for the X12c preview pack (unit I1-c, law M3-I1 r3 item 5, contract '
                             'successor I1-P): the one bundled document of the release row opensip.preview.typescript.pack:1, in the '
                             'opensip-evaluator package; no package edge, crate dependency, run-time read, evaluation semantics, release, '
                             'distribution or product qualification')
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
# No added or changed row has a bound meaning.
assert not set(meanings) & ({a['path'] for a in ADDED} | set(CHANGED))
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
    'standing': 'PROPOSED additive release policy document for the X12c preview pack (unit I1-c); independent review and lead assent required',
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
    'projectionRule': f'Resolve all {INHERITED + DIRECT} effective descriptions by stable file path from the meanings the lock binds to {parent_name}: its {INHERITED} inheritance rows (as {parent_name} projected them) and the {DIRECT} direct passage overrides that bound contract successors place on {parent_name}, with {FOLDED} supersessions folded. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'parentMode': parent_mode, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'inherited': INHERITED, 'direct': DIRECT, 'supersessionsFolded': folded, 'selectorsMoved': moved}))
