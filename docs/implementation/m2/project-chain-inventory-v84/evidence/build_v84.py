"""Build inventory84 from inventory83 (unit X3a-1, committed, under review)
by adding exactly the two X2a rows, and write its successor record. It
projects the sixteen rows inherited through inventory83. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any path git already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v84.json'
RECORD = M + 'project-chain-inventory-v84/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/project_chain.rs', 'opensip-security', 'composition',
        "Walk and judge the project chain (law X2 r5 items 1 to 3 and 9, and the custody half of item 4): one retained, no-follow, charged walk from / to a selected project root. The root must be strictly below H and outside H/Library/Application Support/OpenSIP, judged lexically before any open. / through the directory above the root takes the shared 468 step 0 external-ancestor judgment with the invocation's omission premise; the root takes S3 directory custody (owner the invoking user or root, no other-write, group-write and ACL write grants only for explicit trust groups, ACL readable or omitted under the premise); every directory from H down must be on H's own volume. The root's native birth is sampled with the existing sampler, charged first, with no mtime or ctime substitute. ProjectChain is private and not Clone, holds the retained chain, spelling and birth, rechecks names, custody, volume and birth for the held-fence recheck set, and grants nothing. Each refusal names its item 8 row and subject; selection, the registry, ProjectRootAdmission, tracking and public projection are X2b's. Nothing is created. Library only."),
    row('crates/security/src/custody/project_chain_tests.rs', 'opensip-security', 'test',
        "Check the project chain walk on scratch homes under the temp directory with a test omission premise: an ordinary root below H is admitted and charged; without a premise the omitted ACL at / refuses; H, roots outside H, a sibling extending H's name and any spelling inside the installation's parent are outside-home before any open; bad spellings, missing roots and links refuse; group- or other-writable ancestors and ACL write grants refuse; the root follows S3 custody with explicit trust groups; an omitted root ACL passes only through the premise; another volume from H down is volume-unsupported; the recheck sees mode, rename and replacement; a short ledger refuses on the budget and stays closed; a 64-level project fits well inside the owner caps; and nothing is created."),
]
parent = pin(M + 'repository-file-inventory.v83.json')
v83 = json.loads((A / parent['path']).read_bytes())
v84 = dict(v83)
v84['standing'] = 'PROPOSED additive project chain layout (law X2 r5); no release, custody, profile, boot or creator qualification'
files = sorted(v83['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v83['files']) + 2
v84['files'] = files
(A / OUT).write_text(json.dumps(v84, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in v83['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v84.items() if k not in ('files', 'standing')} == {k: v for k, v in v83.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'store-endpoint-inventory-v83/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory83 is not the committed X3a-1 candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive project chain layout (law X2 r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory83, which carries them unchanged from inventory82. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
