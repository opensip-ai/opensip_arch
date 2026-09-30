"""Build inventory77 from selected inventory76 by adding exactly the two
458c-a rows, and write its successor record. Run with python3 -I -B from any
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
    row('crates/security/src/custody/read_premise.rs', 'opensip-security', 'composition',
        "Produce the read side's premise receipt (law 458c r5 items 1 to 4): the process's one attempt, the actor, InitialCore and InitialPlatform, exactly the creator's producers, with no intent, storage choice, disclosure, effect or fence. The receipt is private and not Clone, holds its own attempt, and lends only the sealed ReadPremiseQualification that InitialPlatform alone implements: the check that a filesystem is H's and the omission premise with 465 item 4's scope, no barrier policy. Every refusal ends in its law 468 item 6 row through 468c's maps. Library only: no read path uses it yet."),
    row('crates/security/src/custody/read_premise_tests.rs', 'opensip-security', 'test',
        "Check the read premise receipt on scratch account homes with InitialCore and InitialPlatform built from signed on-disk test trees: a premise lent when the platform mints one and its absence not a refusal; no intent, effect or fence and a charged recheck; the live InitialCore refusing at F0 in a development build; one attempt per process; account, filesystem and budget refusals choosing their rows; a receipt of another attempt refused; and the receipt opaque, not Clone, lending only the sealed qualification."),
]
parent = pin(M + 'repository-file-inventory.v76.json')
v76 = json.loads((A / parent['path']).read_bytes())
v77 = dict(v76)
v77['standing'] = 'PROPOSED additive read-side premise receipt layout (law 458c r5); no release, custody, profile, boot or creator qualification'
files = sorted(v76['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v76['files']) + 2
v77['files'] = files
out = A / M / 'repository-file-inventory.v77.json'
out.write_text(json.dumps(v77, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v77.json')
old = {r['path']: r for r in v76['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v77.items() if k not in ('files', 'standing')} == {k: v for k, v in v76.items() if k not in ('files', 'standing')}
prior = json.loads((A / M / 'existing-root-routing-inventory-v76/successor.json').read_bytes())
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive read-side premise receipt layout (law 458c r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all eight effective descriptions by stable file path from the selected inherited rows with parent inventory76. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'read-premise-inventory-v77/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
