"""Build inventory76 from selected inventory75 by adding exactly the four
468c rows, and write its successor record. Run with python3 -I -B from any
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
    row('crates/host/src/installation_termination.rs', 'opensip-host', 'adapter',
        "Project each law 468 item 6 row onto its one public D9 termination: class, exit, error code, fault cause, domain detail and subject, exactly as the 468a diagnostic routes publish them plus law 468 r5's incomplete-installation row. The match is exhaustive, so a new row cannot compile without its termination. Nothing emits it yet: no CLI command is wired."),
    row('crates/security/src/custody/installation_routing.rs', 'opensip-security', 'composition',
        "Route the initial creator through the durable write gate (law 468 r5 items 1 and 3): Published, LostRace and NotPristine end the creator act, the attempt is dropped, and a fresh gate admits I with only this invocation's InitialPlatform. Map every creator, preparation, stage, publication and gate refusal of units 459 to 468 to its one item 6 row by exhaustive matches with no wildcard arm. Library only: no CLI command is wired, and development builds refuse at InitialCore F0."),
    row('crates/security/src/custody/installation_routing_tests.rs', 'opensip-security', 'test',
        "Check the creator-to-gate routing on scratch account homes with InitialCore and InitialPlatform built from signed on-disk test trees: a published, a not-pristine and a lost-race installation each admitted by the gate; a foreign entry, a busy fence, a gate budget, a missing premise and a rename not performed each ending in its item 6 row; the live composition refusing at F0 in a development build; and representative refusals of every family choosing their rows."),
    row('crates/security/src/installation_termination.rs', 'opensip-security', 'model',
        "The closed vocabulary of law 468 item 6: one variant per public row of creator and existing-root admission refusals, the platform decision's NT-TCB detail, and an invariant row for refusals only a broken caller reaches. A diagnostic classification for the host's D9 projection, never authority."),
]
parent = pin(M + 'repository-file-inventory.v75.json')
v75 = json.loads((A / parent['path']).read_bytes())
v76 = dict(v75)
v76['standing'] = 'PROPOSED additive creator routing and public termination layout (law 468 r5); no release, custody, profile, boot or creator qualification'
files = sorted(v75['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v75['files']) + 4
v76['files'] = files
out = A / M / 'repository-file-inventory.v76.json'
out.write_text(json.dumps(v76, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v76.json')
# Inherited rows are equal by value; nothing else changes.
old = {r['path']: r for r in v75['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v76.items() if k not in ('files', 'standing')} == {k: v for k, v in v75.items() if k not in ('files', 'standing')}
prior = json.loads((A / M / 'existing-root-gate-inventory-v75/successor.json').read_bytes())
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive creator routing and public mapping layout (law 468 r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all eight effective descriptions by stable file path from the selected inherited rows with parent inventory75. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'existing-root-routing-inventory-v76/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
