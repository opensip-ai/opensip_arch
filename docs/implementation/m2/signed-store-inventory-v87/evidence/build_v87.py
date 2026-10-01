"""Build inventory87 from inventory84 (unit X2a, committed, under review) by
adding exactly the two X4T-0 rows, and write its successor record. It
projects the sixteen rows inherited through inventory84. Inventory85 (X3b-1)
and the reserved inventory86 (X4T-a) are siblings, not parents: this unit is
renumbered and rebuilt at integration. Run with python3 -I -B. Deterministic:
rerunning reproduces the same bytes. It refuses to write over any path git
already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v87.json'
RECORD = M + 'signed-store-inventory-v87/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/trust/accepted_store_fixture.rs', 'opensip-security', 'fixture',
        "Generate a signed accepted trust store for tests only (law X4T r4 item 13, X4T-0), declared solely under cfg(test). It builds a real P0 publication with the product initial_publication producer, then one retained publication at revision 2: a root, revocation, catalog and payload manifest signed with the public test-only quorum seeds; the payload metadata closure, a bootstrap operation, an S4 evaluation input as time evidence with a signed time source; ordinary root and catalog/revocation admission records and a list revocation history; an S4 clock-write event and, per role, an accepted EV-PRESENT-PAYLOAD role event plus one conditioning event for an expired, stale-revocation, quorum-lost or revoked target, with their role-change and publication-event rows; and the retained-phase capsule and descriptor. Every record is canonically encoded and admitted by its closed shape before it is written; files are content-addressed in the trust locators. It is the only constructor of these kinds and no production path reaches it; X4B owns the real producers."),
    row('crates/security/src/trust/accepted_store_fixture_tests.rs', 'opensip-security', 'test',
        "Check the signed accepted-store generator: every immutable file is canonical and addressed by its digest and each kind passes its closed shape; the root, catalog and revocation envelopes carry real ed25519 quorum signatures over their bodies by their owning role; current_record_bindings::bind, publication_events::bind_events (from P0's roles and event head) and bind_retained_head (through the capsule clock) accept the generated store for state schemas 1 and 2; chosen role states publish with their accepted standing, INDEX-only catalog and revoked or quorum-lost evidence; capture_p2 accepts the written store through a supplied native fence on a scratch installation; a store with no accepted role is not offered; and a source pin shows the constructor is declared only under cfg(test) and named by no other source file."),
]
parent = pin(M + 'repository-file-inventory.v84.json')
v84 = json.loads((A / parent['path']).read_bytes())
v87 = dict(v84)
v87['standing'] = 'PROPOSED additive test-only signed accepted-store generator (law X4T r4 item 13); no release, custody, profile, boot or creator qualification'
files = sorted(v84['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v84['files']) + 2
v87['files'] = files
(A / OUT).write_text(json.dumps(v87, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in v84['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v87.items() if k not in ('files', 'standing')} == {k: v for k, v in v84.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'project-chain-inventory-v84/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory84 is not the committed X2a candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive test-only signed accepted-store generator (law X4T r4 item 13); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory84, which carries them unchanged from inventory83. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
