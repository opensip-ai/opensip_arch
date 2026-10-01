"""Build inventory113 by adding exactly the two X4B-a rows (law X4B r5 items 2
to 6 and 10: the first trust acceptance producer) to the inventory the real
product lock selects, and write its successor record. The parent follows the
lock: inventory116 (unit X4a, selected at product a34dc6b). It projects the
sixteen rows inherited through the parent. Run with python3 -I -B from any
directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It refuses to write over any path git already tracks, and while a lock
selects inventory113. It was first built on inventory114 at daa7b01
(reviewed at r1), then rebuilt on inventory117 (c2352ae) and inventory116
(a34dc6b) with the same two rows; PRIOR maps inventory114, inventory117 and
inventory116."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v113.json'
RECORD = M + 'trust-bootstrap-x4ba-inventory-v113/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v114.json': (M + 'crash-matrix-x90-inventory-v114/successor.json', 'inventory114', 'X9-0'),
    M + 'repository-file-inventory.v117.json': (M + 'refusal-suite-x8a-inventory-v117/successor.json', 'inventory117', 'X8a'),
    M + 'repository-file-inventory.v116.json': (M + 'live-guards-x4a-inventory-v116/successor.json', 'inventory116', 'X4a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory113 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/trust/trust_bootstrap.rs', 'opensip-security', 'service',
        "Produce first trust acceptance from the running core's embedded bootstrap payload (law X4B r5 items 2 to 6; unit X4B-a), as a macOS child of the current-trust admission, under the held installation fence on the retained P0 state.v1 owner. The payload is exactly what InitialCore retains (law 463 r9): the root chain, the revocation pair, the bootstrap manifest (TR-BUNDLE), the core inventory (TR-CORE), the catalog pair (TR-INDEX) and the component-manifest pairs (TR-COMPONENT). Every signature is verified again: the chain from the embedded root binding within ChainBudget{16 links, 16 MiB}, the list under the final root, re-filtering every link, the index-0 root and its own quorum; each document's envelope at its role's threshold with the list's keyIds excluded. A bootstrap without a signed catalog, or any document that fails, refuses PAYLOAD-NOT-ADMISSIBLE before any write. S4 step 2 runs on the caller's one clock sample (F := max(W, A), L := A, the anchor, expiry from the presented documents). Each carried role's sequence goes through role_machine::decide: PresentOrdinary, then Clock when expired or stale, then Revoke when the payload's own list names its signer, namespace, release or catalog snapshot. Every record (objects, payload closure, operation, time evidence with the payload's signed time source, root and metadata admissions, revocation history, clock-write and role events with their role changes, the revision-2 descriptor and the retained capsule) is canonically encoded, admitted by its closed shape and bound by current_record_bindings, successor_record_bindings and publication_events before floor_publication's shared protocol publishes it, state.v1 last, advancing the retained owner from the confirming reread. Not wired to the fenced first read (X4B-b); grants nothing."),
    row('crates/security/src/trust/trust_bootstrap_tests.rs', 'opensip-security', 'test',
        "Check X4B-a (law X4B r5 item 10) on ACL-scratch installations holding 467's P0 publication under a supplied fence, with test-signed releases (public quorum62 seeds) produced into an InitialCore through 463's injected-image constructor: P0 is accepted with TR-BUNDLE, TR-COMPONENT, TR-CORE and TR-INDEX trusted from one EV-PRESENT-PAYLOAD each and the one confirming admission admits the store without writing; X4T-a's native reread and every record's canonical content address accept it; the fresh-install time rules (tEval = max(W, A), payload-future, beyond-horizon and its boundary) write nothing on refusal; an expired catalog, an expired root, a stale list, a revoked signer whose quorum survives and expired-and-revoked give their event sequences, accepted.by and revokedBy, and X4T's continuation row or ExistingOnly; inactive and rejected entries record no event; a revoked counted signer that leaves a catalog or component manifest below threshold writes nothing; a missing catalog or a document signed outside its role writes nothing; no component manifest leaves TR-COMPONENT unbootstrapped; a crash before the pointer and a rerun; a changed state.v1; a short ledger; a non-P0 predecessor and a foreign root binding; and a two-root chain recorded in full, with the reader's current FirstIdentity refusal pinned as a stated gap."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive first trust acceptance producer layout (law X4B r5, unit X4B-a); library only, not wired; no release, custody, profile, boot or creator qualification'
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
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive first trust acceptance producer layout (law X4B r5, unit X4B-a); independent review and lead assent required',
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
