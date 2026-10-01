"""Build inventory109 by adding exactly the one X12b row (law X12 r3 items 1,
5, 7 and 8, host side, with item 10's host cases) to the inventory the real
product lock selects, and write its successor record. The parent follows the
lock, whatever it selects: at first build, inventory105 (unit X2c, selected
at product 0206ce8). The sixteen inherited rows are projected from the
successor record the lock binds to that parent, so the script reruns
unchanged on a new parent (v106 and v108 are in flight). Run with
python3 -I -B from any directory. Deterministic for a given lock: rerunning
reproduces the same bytes. It refuses to write over any path git already
tracks, and while a lock selects inventory109."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v109.json'
RECORD = M + 'policy-pack-x12b-inventory-v109/successor.json'
LOCK = Path('/Users/sb/code/opensip-ai/opensip/design-lock.json')
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory109 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/host/src/configuration_tests.rs', 'opensip-host', 'test',
        "Check X12b (law X12 r3 item 10, host side) through configuration.rs's admit_policy_selection over the release registry, which has zero rows: NT-1 wrong identities (wrong name or version, bare name, leading zero, case, whitespace and newline, the empty string, opensip.preview.typescript.pack:1 itself, and the evaluator's cfg(test) ID, unreachable from the host) are row 1 with the presented ID; user and third-party supplied documents, including the test pack's exact bytes, are row 2; NT-2 script, hook, exec and include members and a string emitWhen are row 3 with the JSON Pointer; non-JSON and non-policy bytes are row 3a; a selection of zero or several sources is row 1 count:<n> before any source is read; bundled defects map to row 4 with subject pack:<packId>. Every row maps to its published route with codes that parse as their generated members, renders through the shared failure envelope valid against command-envelope v7, carries the X12-0 CONFIG.INVALID remedy byte for byte on rows 1, 2 and 3a, and is never truncated; a source pin shows admission calls only admit_pack and reaches no evaluation, provider, facts, Coverage, custody, lock, ledger or I/O."),
]
selected = lock['inventorySuccessors'][-1]
parent = pin(selected['candidate']['path'])
assert parent == selected['candidate'], 'the selected parent inventory differs from the lock'
assert pin(selected['record']['path']) == selected['record'], 'the selected successor record differs from the lock'
parent_name = Path(parent['path']).stem.replace('repository-file-', '').replace('.v', '')
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive host policy-pack admission layout (law X12 r3, unit X12b); no release, custody, profile, boot or creator qualification'
paths = {r['path'] for r in inherited['files']}
assert 'crates/host/src/configuration.rs' in paths, 'configuration.rs must already be a planned row'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + len(ADDED)
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
host = next(p for p in inherited['packages'] if p['id'] == 'opensip-host')
assert 'opensip-evaluator' in host['dependencies'], 'host -> evaluator must already be a permitted edge'
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / selected['record']['path']).read_bytes())
assert prior['candidate'] == parent, f'{parent_name} is not the candidate of the selected record'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive host policy-pack admission layout (law X12 r3, unit X12b); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all sixteen effective descriptions by stable file path from the rows bound to {parent_name}, which carries them unchanged from inventory81 onward. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
