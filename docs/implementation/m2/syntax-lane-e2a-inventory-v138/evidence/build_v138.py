"""Build inventory138 by adding exactly the twenty-two rows of unit E2a, the
grammar closure lane SYN-LANE (law M3-E1 r4 items 4 to 6, 19 and 20, under
native-linked-v1), to inventory137 (unit J2a), and write its successor
record.

All twenty-two rows are in the existing `tooling` package (path `tools`): the
lane, its pins, the one retained upstream licence, the eight generated grammar
definition records, the six SYN-NS closure members, the four generated
SymbolTableV1 records and the lane's tests. tools/README.md is a planned row
whose bytes change and whose description stays true. No package, edge,
crate dependency or pending decision changes.

The parent is inventory137 (unit J2a, built in parallel on inventory136 and
not yet integrated), as the lead assigned. While the given lock still selects
inventory136, J2a's staged entry and its re-projected inheritance are applied
in memory from J2a's own evidence/verify_scratch.py (its SCRATCH-J2A
placeholders), exactly as J2a stages them; once J2a is integrated the lock
selects inventory137 directly. Only the parent's candidate, record and bound
meanings are used, which are the same either way.

Projection. Every meaning the lock binds to inventory137 is inherited by
stable file path once inventory138 is selected: the one hundred and three
inheritance rows inventory137 projected (inventory136's one hundred and the
three direct overrides of read-endpoint-x3a2-descriptions on inventory136).
No bound contract successor has a passage override or supersession on
inventory137.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory138. Usage: build_v138.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v138.json'
RECORD = M + 'syntax-lane-e2a-inventory-v138/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
J2A = M + 'host-invocation-j2a-inventory-v137'
# Each admissible parent: the successor record that bound its inherited rows,
# its name, its unit, and the inherited, direct and folded meaning counts the
# lock binds to it.
PRIOR = {
    M + 'repository-file-inventory.v137.json': (J2A + '/successor.json', 'inventory137', 'J2a', 103, 0, 0),
}
def with_parent(lock):
    """The lock selecting inventory137: as given once J2a is integrated, else
    with J2a's staged entry applied in memory."""
    if lock['inventorySuccessors'][-1]['candidate']['path'] in PRIOR:
        return lock, 'integrated'
    spec = importlib.util.spec_from_file_location('j2a_scratch', A / J2A / 'evidence/verify_scratch.py')
    j2a = importlib.util.module_from_spec(spec); spec.loader.exec_module(j2a)
    return j2a.staged(lock), 'J2a staged in memory'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock, parent_mode = with_parent(json.loads(LOCK.read_bytes()))
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory138 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, role, description, generated=False):
    return {'path': path, 'package': 'tooling', 'role': role, 'description': description, 'generated': generated, 'standing': 'proposed'}
G = 'tools/grammar/closure/opensip-interface/'
CODE = {
    'javascript': ('tree-sitter-javascript v0.25.0', 15, 265, 36),
    'rust': ('tree-sitter-rust v0.24.2', 15, 355, 31),
    'tsx': ('tree-sitter-typescript v0.23.2 (its tsx grammar)', 14, 400, 43),
    'typescript': ('tree-sitter-typescript v0.23.2 (its typescript grammar)', 14, 383, 40),
}
DATA = {
    'json': ('.json', 'JSON (RFC 8259)'),
    'markdown': ('.md', 'Markdown (CommonMark 0.31.2)'),
    'toml': ('.toml', 'TOML (v1.0.0)'),
    'yaml': ('.yaml and .yml', 'YAML (1.2.2)'),
}
LEVELS = ['L0-verbatim', 'L1-lexical', 'L2-comment-insensitive', 'L3-identifier-insensitive']
ADDED = [
    row('tools/grammar/grammar_lane.py', 'entrypoint',
        "Run the grammar closure lane SYN-LANE (law M3-E1 r4 items 4 to 6 and 19, unit E2a) for native-linked-v1: verify the four pinned crate archives by crates.io checksum, size and VCS record; read each pinned upstream member in memory, or its retained copy, by sha256, length and git blob; require every compiled member set to equal the include closure of its crate build's compile roots; recompute each code grammar's canonical SymbolTableV1 from its generated parser.c; build the eight canonical grammar definition records; bind the SYN-NS copies to the successor the design lock selects; and check, rewrite or materialize the retained outputs. Executes no upstream code; never writes the bundle manifest or build receipt; not closure admission, signing, a dependency policy or release qualification."),
    row('tools/grammar/lane.json', 'registry',
        "Pin the SYN-LANE inputs for native-linked-v1: the tree-sitter runtime v0.27.0 and the rust v0.24.2, typescript v0.23.2 and javascript v0.25.0 grammar releases (tag, full commit, crates.io archive checksum and size, archive VCS record); every retained runtime and code-row member at its upstream path with its role, sha256, length and git blob, and the crate-build compile model that proves the compiled set; the eight grammar rows, with the four data-document format definitions; the grammar registry they must cover; and the six SYN-NS members with the bundle manifest's normalizer object. A pin links nothing: SYN-DEP selects and links the crates."),
    row('tools/grammar/upstream/tree-sitter-typescript/LICENSE', 'documentation',
        "Retain tree-sitter-typescript's MIT licence from its pinned v0.23.2 tag (git blob aa9f858d), which the crate archive omits, so the typescript and tsx rows retain their upstream licence and ship its notice. Third-party text; not product code."),
]
for g, (upstream, abi, symbols, fields) in CODE.items():
    ADDED.append(row(f'{G}grammar/{g}/definition.v1.json', 'registry',
        f"Retain the generated canonical definition record of the {g} grammar row (law M3-E1 items 4 to 6) under native-linked-v1: {upstream} at its commit; every compiled source, grammar.json, node-types.json and the licence by closure path, sha256 and length; the tree-sitter v0.27.0 runtime sources; null module, shim and shim ABI; language ABI {abi}; the SymbolTableV1 digest; and the notices. Its sha256 is the row's grammarDigest. Not admission.", True))
    ADDED.append(row(f'tools/grammar/symbol-tables/{g}.v1.json', 'registry',
        f"Retain the generated canonical SymbolTableV1 of the {g} grammar (law M3-E1 A11), read from its pinned parser.c: {symbols} symbols with the names and named and visible flags tree-sitter's safe Language API reports, ERROR never a row, and {fields} fields, language ABI {abi}. Its sha256 is the definition record's symbolTableSha256, which the host's T-native recomputation from the linked Language (unit E2b) must equal.", True))
for g, (suffixes, name) in DATA.items():
    ADDED.append(row(f'{G}grammar/{g}/definition.v1.json', 'registry',
        f"Retain the generated canonical definition record of the {g} data-document row (law M3-E1 items 4 and 8): suffix {suffixes}, grammarVersion format-definition.v1, the {name} format reference and parse none. No parser is pinned, linked or run. Its sha256 is the row's grammarDigest.", True))
ADDED.append(row(f'{G}grammar/normalizer.v1.json', 'registry',
    "Retain contract successor SYN-NS's native normalizer specification at its closure tree path, byte for byte: the member the bundle manifest's normalizer.specificationDigest names. The lane binds it to the candidate the design lock selects; E2c implements it."))
ADDED.append(row(f'{G}normalization/specification-map.v1.json', 'registry',
    "Retain SYN-NS's IE normalization specification map, the grammar closure tree's second root (law M3-E1 item 4, A6), byte for byte, as the design lock selects it."))
for level in LEVELS:
    ADDED.append(row(f'{G}normalization/levels/{level}.v1.json', 'registry',
        f"Retain SYN-NS's {level} level specification at its fixed closure tree path, byte for byte, as the IE map's {level} row names it and the design lock selects it."))
ADDED.append(row('tools/tests/test_grammar_lane.py', 'test',
    "Exercise the grammar closure lane: the identity canonical profile; the parser.c symbol-table reader, its refusals and the ERROR exception; conditional include closures; crate-archive pins and unsafe members; lane-specification and registry-coverage refusals; and, with the pinned archives, the byte-identical rebuild, drift refusals, a reproducible closed materialization and the SYN-NS binding."))
ADDED.sort(key=lambda r: r['path'])
assert len(ADDED) == 22
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit, INHERITED, DIRECT, FOLDED = PRIOR[selected['path']]
assert lock['inventorySuccessors'][-1]['record']['path'] == prior_path, 'the selected inventory has another successor record'
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
packages = {p['id']: p for p in inherited['packages']}
assert packages['tooling']['path'] == 'tools' and packages['tooling']['dependencies'] == [], 'the tooling package is declared in the parent'
planned = {r['path'] for r in inherited['files']}
CHANGED = ['tools/README.md']
assert set(CHANGED) <= planned, 'a changed path is not a planned row of the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = ('PROPOSED additive grammar closure lane (unit E2a, law M3-E1 r4 items 4 to 6, 19 and 20; SYN-LANE under native-linked-v1): '
                             'the lane, its pins, the one retained upstream licence, the eight grammar definition records, the four SymbolTableV1 records, '
                             'the six SYN-NS closure members and the lane tests, all in the tooling package; no package edge, crate dependency, closure '
                             'admission, signing, release, distribution or product qualification')
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
# No added row has a bound meaning, and the one changed row keeps whatever it has.
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
    'standing': 'PROPOSED additive grammar closure lane (unit E2a, SYN-LANE); independent review and lead assent required',
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
