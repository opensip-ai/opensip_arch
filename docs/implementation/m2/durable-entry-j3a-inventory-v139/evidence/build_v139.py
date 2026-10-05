"""Build inventory139 by adding exactly the sixteen rows of unit J3a, the
durable entry of law M3-J1 r6 (items 2 and 3, with successors S2 to S7 and
S10's item 2), to inventory138 (unit E2a), and write its successor record.

All sixteen rows are compile-fail cases of law X8 r3's refusal suite in the
existing opensip-host package, under crates/host/tests/refusal/cases/: the
full capability set of the two exported identity types J3a adds to
opensip-platform (RequestIdentity and ReservedExecutionId: a literal from
bytes, Default, Deserialize, conversions from bytes and from text, Clone and
Serialize), item 3a's census row for ReservedExecutionId's one feature-only
constructor (the crash matrix's inject-id reservation), and CommitSession
given another ExecutionId (J-C4, J-C4b; X3d r9 S10.7). Every other file J3a
changes is a planned row whose description stays true. No package, edge,
crate dependency or pending decision changes.

The parent is inventory138 (unit E2a), which the lock at product b7b87b7
selects: J2a's inventory137 and E2a's inventory138 are integrated, and the
lead's rule stages J3a's candidate on the highest existing candidate. If
another unit stages inventory139 first, this candidate moves to the next
version on that one.

Projection. Every meaning the lock binds to inventory138 is inherited by
stable file path once inventory139 is selected: the one hundred and three
inheritance rows inventory138 projected. No bound contract successor has a
passage override or supersession on inventory138.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory139. Usage: build_v139.py [LOCK]; the lock defaults to the
product checkout's design-lock.json, which must select inventory138."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v139.json'
RECORD = M + 'durable-entry-j3a-inventory-v139/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
E2A = M + 'syntax-lane-e2a-inventory-v138'
# Each admissible parent: the successor record that bound its inherited rows,
# its name, its unit, and the inherited, direct and folded meaning counts the
# lock binds to it.
PRIOR = {
    M + 'repository-file-inventory.v138.json': (E2A + '/successor.json', 'inventory138', 'E2a', 103, 0, 0),
}
def with_parent(lock):
    """The lock, which must select inventory138."""
    assert lock['inventorySuccessors'][-1]['candidate']['path'] in PRIOR, 'the lock does not select inventory138'
    return lock, 'integrated'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock, parent_mode = with_parent(json.loads(LOCK.read_bytes()))
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory139 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
CASES = 'crates/host/tests/refusal/cases/'
DRIVER = ("Compile-fail case for law X8 r3 (unit J3a), compiled only by admission_tests.rs's driver with the pinned rustc 1.95.0 "
          "against the plain cargo check -p opensip-host surface, never a Cargo target: the control without --cfg x8_misuse "
          "compiles, and the misuse fails with exactly one error, ")
def case(name, error, meaning):
    return {'path': CASES + name, 'package': 'opensip-host', 'role': 'fixture',
            'description': f'{DRIVER}{error}; {meaning} Synthetic; no compiler qualification.',
            'generated': False, 'standing': 'proposed'}
ADDED = []
for ty, slug, ctor in [
    ('RequestIdentity', 'request_identity', 'whose only constructor is the CSPRNG draw RequestIdentity::draw (law M3-J1 r6 item 2, J-C4)'),
    ('ReservedExecutionId', 'reserved_execution_id', 'whose only constructor is the process registry, reserve_execution_id (law M3-J1 r6 item 2, J-C4b; X3d r9 S10.7)'),
]:
    literal = ('E0451, field `bytes` of struct `RequestIdentity` is private' if ty == 'RequestIdentity'
               else 'E0451, fields `bytes` and `rendered` of struct `ReservedExecutionId` are private')
    ADDED += [
        case(f'platform_{slug}_literal.rs', literal, f'group D: {ty}, {ctor}, cannot be built from bytes as a struct literal.'),
        case(f'platform_{slug}_default.rs', f'E0277, the trait bound `{ty}: Default` is not satisfied', f'group D: {ty} has no Default.'),
        case(f'platform_{slug}_deserialize.rs', f"E0277, the trait bound `{ty}: serde::Deserialize<'de>` is not satisfied", f'group D: {ty} cannot be read back from serialized text.'),
        case(f'platform_{slug}_from_bytes.rs', f'E0277, the trait bound `{ty}: From<[u8; 16]>` is not satisfied', f'group D: no conversion builds {ty} from bytes.'),
        case(f'platform_{slug}_from_text.rs', f'E0277, the trait bound `{ty}: FromStr` is not satisfied', f'group D: {ty} cannot be parsed from text.'),
        case(f'platform_{slug}_clone.rs', f'E0277, the trait bound `{ty}: Clone` is not satisfied', f'group E: {ty} cannot be cloned.'),
        case(f'platform_{slug}_serialize.rs', f'E0277, the trait bound `{ty}: serde::Serialize` is not satisfied', f'group G: {ty} cannot be serialized.'),
    ]
ADDED += [
    case('platform_reserved_execution_id_injected_absent.rs', 'E0432, unresolved import `opensip_platform::crash_barrier`',
         "group F (item 3a's census): ReservedExecutionId's one constructor from text, the crash matrix's inject-id reservation at "
         "x3d.session.execution-draw (X3d r9 S10.1), exists only under the test-only crash-matrix feature and is absent from the plain surface."),
    case('security_commit_session_open_reserved.rs', 'E0061, this function takes 1 argument but 2 arguments were supplied',
         'group F: CommitSession accepts no other ExecutionId, not even one reserved in the process registry; open draws and reserves its own '
         '(X3d r9 S10.1 and S10.7, J-C4b).'),
]
ADDED.sort(key=lambda r: r['path'])
assert len(ADDED) == 16
# Planned rows whose bytes change; each description stays true.
CHANGED = sorted([
    'crates/host/src/request.rs',
    'crates/host/tests/admission_tests.rs',
    'crates/platform/src/crash_barrier.rs',
    'crates/platform/src/lib.rs',
    'crates/security/src/custody/commit_session.rs',
    'crates/security/src/custody/commit_session_tests.rs',
    'crates/security/src/custody/installation_admission_tests.rs',
    'crates/security/src/custody/installation_parent_tests.rs',
    'crates/security/src/custody/installation_publication_tests.rs',
    'crates/security/src/custody/installation_read_fixture.rs',
    'crates/security/src/custody/installation_routing.rs',
    'crates/security/src/custody/installation_routing_tests.rs',
    'crates/security/src/custody/installation_session_tests.rs',
    'crates/security/src/custody/installation_stage.rs',
    'crates/security/src/custody/ordinary_writer.rs',
    'crates/security/src/custody/read_premise.rs',
    'crates/security/src/initial_installation.rs',
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
assert packages['opensip-host']['path'] == 'crates/host', 'the opensip-host package is declared in the parent'
planned = {r['path'] for r in inherited['files']}
assert set(CHANGED) <= planned, 'a changed path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = ('PROPOSED additive refusal-suite cases for the durable entry (unit J3a, law M3-J1 r6 items 2 and 3 with successors '
                             'S2 to S7 and X3d r9 S10.1): the full X8 capability set of RequestIdentity and ReservedExecutionId, item 3a\'s '
                             'census row for the crash matrix\'s inject-id reservation, and CommitSession given another ExecutionId, all in the '
                             'opensip-host package; no package edge, crate dependency, command wiring, release, distribution or product qualification')
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
# No added row has a bound meaning, and the changed rows keep whatever they have.
assert not set(meanings) & {a['path'] for a in ADDED}
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
    'standing': 'PROPOSED additive refusal-suite cases for the durable entry (unit J3a); independent review and lead assent required',
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
