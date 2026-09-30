"""Build inventory79 from selected inventory78 by adding exactly the four
458c-b2 rows, and write its successor record. Run with python3 -I -B from any
directory. Deterministic: rerunning reproduces the same bytes."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/installation_read.rs', 'opensip-security', 'service',
        "The read session for installation readers (law 458c r5 item 8). It keeps a complete I that the observation session admitted: the held fence, the retained chain, the account and the read receipt, with the observation session's one ledger. Every later capture and recheck is charged to that ledger before it runs (item 6). A capture opens prefixes and a leaf only through the retained I and its retained descendants: each directory judged private by the owner's predicate on a charged capture and named exactly, the file judged a private regular file, bounded, named, on H's filesystem, read, judged again and reopened by name. Its failures are values, so the full recheck (item 5 step 4) runs after every capture, over the fence, the observation's required files and every file captured since; any refusal latches the session. Between full rechecks, the held-fence check samples the carrier's name and identity, and a capture's own recheck samples its edges and file. It lends the trust readers a held-fence view and charges their retained budget to the same ledger. Nothing walks from the root again. Never a write capability."),
    row('crates/security/src/custody/installation_read_tests.rs', 'opensip-security', 'test',
        "Check the read session on scratch account homes with a creator-published P0: no production installation reader's source reaches the ordinary fence's uncharged acquire, its native root or directory-path inspection; the trust readers' charges land on the session ledger and a refused charge latches it; the held-fence view lends the retained I, charges its rechecks, refuses a replaced carrier and latches; and a changed carrier's custody is refused by the full recheck."),
    row('crates/security/src/custody/installation_read_fixture.rs', 'opensip-security', 'test',
        "Test support for installation readers on scratch account homes: publish a real P0 with the creator composition under a scratch H, then hold read fences on it through the observation session with the read receipt over signed on-disk test trees, and write further files below I as private creations. It never opens the real account's I."),
    row('crates/security/src/installation_observation_tests.rs', 'opensip-security', 'test',
        "Check the readers' captures through the read session on a creator-published P0: original bytes and descriptor fenced until consumption; request bounds before any native step or charge; missing, aliased, foreign or wrong-kind leaves never read as initialization, and oversize on the incomplete row; mutations at every capture phase refused; consumption rechecking the file, its edges and the held fence, with chain and carrier custody on the full recheck; a failed capture still running the full recheck and staying the cause; a captured file joining the full recheck; every capture charged, and an exhausted ledger on the budget row; and descendants retaining every edge, refusing foreign, aliased or missing prefixes and earlier-ancestor changes."),
]
parent = pin(M + 'repository-file-inventory.v78.json')
v78 = json.loads((A / parent['path']).read_bytes())
v79 = dict(v78)
v79['standing'] = 'PROPOSED additive installation-reader migration layout (law 458c r5); no release, custody, profile, boot or creator qualification'
files = sorted(v78['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v78['files']) + 4
v79['files'] = files
out = A / M / 'repository-file-inventory.v79.json'
out.write_text(json.dumps(v79, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v79.json')
old = {r['path']: r for r in v78['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v79.items() if k not in ('files', 'standing')} == {k: v for k, v in v78.items() if k not in ('files', 'standing')}
prior = json.loads((A / M / 'read-observation-inventory-v78/successor.json').read_bytes())
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive installation-reader migration layout (law 458c r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all eight effective descriptions by stable file path from the selected inherited rows with parent inventory78. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'read-migration-inventory-v79/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
