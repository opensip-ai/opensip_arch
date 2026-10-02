"""Build inventory128 by adding exactly the one X11a row (law X11 r1 items 2,
6 and 7: the binary and source pins that no creator command is live in M2,
in a new apps/cli/tests/creator_commands_tests.rs) to the inventory the real
product lock selects, and write its successor record. No production file
changes, so every existing row stays by value. The parent follows the lock:
inventory127 (unit X6c, selected at product bccb6b4, with D1's thirty-nine
overrides and D2's four supersessions already folded into its projection).
It projects the fifty-five rows inherited through the parent. Run with
python3 -I -B from any directory. Deterministic for a given lock: rerunning
reproduces the same bytes. It writes only its own two paths, refuses to write
over any path git already tracks, and refuses while a lock selects
inventory128."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v128.json'
RECORD = M + 'cli-pins-x11a-inventory-v128/successor.json'
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v127.json': (M + 'settlement-sweep-x6c-inventory-v127/successor.json', 'inventory127', 'X6c'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory128 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('apps/cli/tests/creator_commands_tests.rs', 'opensip-cli', 'test',
        "Run the real built opensip with no override (law X11 r1 items 2 and 6; unit X11a): no creator command is live in M2. For every input row of item 2 in both formats, in several orders of --format and --client-correlation-id, the default analysis, analyze, fit and audit (with or without further words), each of them with any of item 2's ten creator flags, with --format agent, html or sarif, and help for analyze, fit, audit or default end on the parser's existing refusal: exit 2, request-rejected REQUEST.UNKNOWN_OPTION with its exact diagnostic, errors empty except OUTPUT.FORMAT_NOT_APPLICABLE's one registered error, the exact command-envelope v7 bytes (schema-valid) or the failure renderer's exact human lines apart from a fresh well-formed req1_ id, and empty standard error; competing parser failures are pinned at the bytes the parser emits. Every run leaves the account's real installation (existence, device, inode, mode and modification time, read by the test process only) and a scratch working directory with invalid configuration and package data byte for byte unchanged. help and completion bash, zsh and fish keep exactly the four-row catalogue (completion, doctor, help, version), byte for byte. Source pins: the production text of apps/cli/src and the host's outcomes, doctor ingress, request and lib names no creator, ordinary writer, gate, pack admission or commit symbol, apps/cli/src does not call installation_entry, and in opensip-security run_initial_creator and admit_ordinary_writer are each defined once, pub(crate), and not named by lib.rs."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive CLI creator-refusal pin layout (law X11 r1 items 6 and 7, unit X11a); tests only, no command enabled; no release, custody, profile, boot or creator qualification'
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
# The lock's inheritance rows bind exactly the prior record's projection to
# the parent; each is carried by stable file path to its new index.
bound = {json.dumps(o['selector'], sort_keys=True): o for o in lock['inventoryPassageInheritance']}
assert len(bound) == len(prior['descriptionOverrideProjection']) == 55
projection = []
for p in prior['descriptionOverrideProjection']:
    o = bound[json.dumps(p['candidateSelector'], sort_keys=True)]
    assert o['parent'] == parent and o['before'] == p['before'] and o['after'] == p['effectiveDescription'], p['filePath']
    i = int(p['candidateSelector']['jsonPointer'].split('/')[2])
    assert inherited['files'][i]['path'] == p['filePath'] and inherited['files'][i]['description'] == p['before'], p['filePath']
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
# Passage supersessions the lock binds on the parent (law VD1 item 3; D2's
# README, "After selection"): each ends the meaning its row's one inheritance
# entry carries. Fold each into that entry: the raw before stays, and the
# supersession's after becomes the effective description. The count stays 55.
# D2's four are on inventory122; X5a folded them, and the lock binds them to
# inventory127 as plain inheritance rows, so none is left to fold on that
# parent and D2's after text is checked instead.
by_selector = {json.dumps(p['parentSelector'], sort_keys=True): p for p in projection}
folded = 0
for binding in lock['contractSuccessors']:
    for s in json.loads((A / binding['record']['path']).read_bytes()).get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        p = by_selector[json.dumps(s['selector'], sort_keys=True)]
        assert s['before'] == p['effectiveDescription'], p['filePath']
        p['effectiveDescription'] = s['after']
        folded += 1
d2 = json.loads((A / M / 'description-batch-d2/successor.json').read_bytes())['passageSupersessions']
assert folded == (4 if parent == d2[0]['parent'] else 0), folded
effective = {p['filePath']: p['effectiveDescription'] for p in projection}
d2_rows = json.loads((A / d2[0]['parent']['path']).read_bytes())['files']
for s in d2:
    path = d2_rows[int(s['selector']['jsonPointer'].split('/')[2])]['path']
    assert effective[path] == s['after'], f'D2 must stay folded: {path}'
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 55
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive CLI creator-refusal pin layout (law X11 r1 items 6 and 7, unit X11a); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, all bound to {parent_name} by the lock, with contract successor D2\'s four passage supersessions folded in (their after text is the effective description). Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
