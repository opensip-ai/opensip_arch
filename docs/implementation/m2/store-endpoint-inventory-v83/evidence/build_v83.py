"""Build inventory83 from inventory82 (unit X10a, committed) by adding exactly
the two X3a-1 rows, and write its successor record. It projects the sixteen
rows inherited through inventory82. Run with python3 -I -B from any
directory. Deterministic: rerunning reproduces the same bytes. It refuses to
write over any path git already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v83.json'
RECORD = M + 'store-endpoint-inventory-v83/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', '--error-unmatch', OUT, RECORD],
                         capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/store_endpoint.rs', 'opensip-security', 'composition',
        "Admit the selected store endpoint (law X3a items 1, 2, 5 and 7) from the values one session already read once: the selection pair, the opened endpoint's marker, the node chain and the trust current record. Admission reads no file. Charged on the session's own ledger, it checks that S is the marker's, that the chain starts at the pair's exact (S, G, K) and ends at exactly one root, that the pair names the receipt's selected core and a K that core supports (else STATE.SCHEMA_UNSUPPORTED), and that the trust current record's C.store is the admitted triple; a core, chain or C.store breach is the incomplete-installation row. The caller then runs one full session recheck. Its producers are the ordinary writer's admission and the read session; the creator path produces none. SelectedStoreEndpoint is private, not Clone, borrowed from the session holding the fence, and grants only the base an owner section 8 binding is later derived from: no namespace, project, lease, journal, ledger, blob, commit or trust authority. Library only."),
    row('crates/security/src/custody/store_endpoint_tests.rs', 'opensip-security', 'test',
        "Check the store endpoint on scratch account homes with a creator-published P0 and 462's signed test trees: a read session admits the endpoint of its one read; each join refuses on its own row (a foreign core, an unsupported K, a C.store differing in S, G or K, an empty chain or a second root); an in-place rewrite after the read fails the session's recheck as required-files-changed and latches; and a source pin that admission reads no file."),
]
parent = pin(M + 'repository-file-inventory.v82.json')
v82 = json.loads((A / parent['path']).read_bytes())
v83 = dict(v82)
v83['standing'] = 'PROPOSED additive store endpoint layout (law X3a); no release, custody, profile, boot or creator qualification'
files = sorted(v82['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v82['files']) + 2
v83['files'] = files
(A / OUT).write_text(json.dumps(v83, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in v82['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v83.items() if k not in ('files', 'standing')} == {k: v for k, v in v82.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'read-cli-inventory-v82/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory82 is not the committed X10a candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive store endpoint layout (law X3a); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory82, which carries them unchanged from inventory81. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
