"""Build inventory78 from selected inventory77 by adding exactly the two
458c-b1 rows, and write its successor record. Run with python3 -I -B from any
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
    row('crates/security/src/custody/installation_session.rs', 'opensip-security', 'service',
        "The read side's observation path (law 458c r5 items 5, 6, 7 and 11). One session per process on one failure-latching ledger with the owner's limits; one observation per session. It reaches I through the durable write gate's own step 0 and step 1 code, shared rather than copied, with no barrier: a charged, retained, no-follow walk from the root to I under the read receipt's sealed lending, a positive absence only when the first missing suffix component is observed absent under its retained parent, and lifecycle.fence opened through the retained I. The lock wait repeats one nonblocking attempt on that same descriptor, paced at 25 ms, for at most 5 s and 201 attempts, all reserved before the first; busy retries, any other failure stops on the host I/O row, and a lock still busy at the bound is the busy row. Under the held fence it runs the receipt's rechecks and the full recheck set, reads the required members charged before they run (the fixed members up front, each lineage node before its own read), records missing, undecodable or misbound members as structural findings, and runs the same full recheck over every captured file, also after a failed read. Every refusal takes exactly the write gate's row. Never a write capability. Library only: no consumer uses it yet."),
    row('crates/security/src/custody/installation_session_tests.rs', 'opensip-security', 'test',
        "Check the observation path on scratch account homes, with P0 published by the creator composition and the read receipt built from signed on-disk test trees, and an injected wait clock: a complete I observed under the fence with no barrier; positive absence at each suffix component, and a symlink, a file or a custody refusal at a suffix name not taken for absence; a missing H on the write gate's row; no premise refusing at the root; a busy fence retried on the same descriptor to 5 s or 201 attempts, freed during the wait, or ending on a wait error; the wait reserved before its first attempt; a required file's mode, link count or identity changed before the final recheck; every finding of an incomplete I; a deep home well within the caps; and no ordinary fence acquire in the source."),
]
parent = pin(M + 'repository-file-inventory.v77.json')
v77 = json.loads((A / parent['path']).read_bytes())
v78 = dict(v77)
v78['standing'] = 'PROPOSED additive read-side observation path layout (law 458c r5); no release, custody, profile, boot or creator qualification'
files = sorted(v77['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v77['files']) + 2
v78['files'] = files
out = A / M / 'repository-file-inventory.v78.json'
out.write_text(json.dumps(v78, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v78.json')
old = {r['path']: r for r in v77['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v78.items() if k not in ('files', 'standing')} == {k: v for k, v in v77.items() if k not in ('files', 'standing')}
prior = json.loads((A / M / 'read-premise-inventory-v77/successor.json').read_bytes())
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive read-side observation path layout (law 458c r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all eight effective descriptions by stable file path from the selected inherited rows with parent inventory77. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'read-observation-inventory-v78/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
