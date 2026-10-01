"""Build inventory92 from inventory91 (unit X3b-1a, selected at product
7e676a9) by adding exactly the two X3b-1b rows, and write its successor
record. It projects the sixteen rows inherited through inventory91. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any path git already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v92.json'
RECORD = M + 'journal-start-inventory-v92/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/journal_store/carrier_start.rs', 'opensip-security', 'composition',
        "The grant-journal carrier start, the end step and the post-uncertainty reconciliation (law X3b r6 item 4, item 5's uncertain outcomes; unit X3b-1b; X3d r3 item 7 relies on them). The start, under the fence and the operation lease, opens and classifies the carrier (format and SHA-256(N) binding), reads the tail and the witness, confirms the tail equals the floor step's observation before any write, then runs reconcile_witness: OK writes nothing, REVERT, ADVANCE and INIT write only the witness COMMITTED at the committed tail by the private file protocol, and QUARANTINE refuses writing nothing; it writes no floor and returns the start tail for X4's epoch binding. reconcile_after_uncertain, still under the lease, reopens and reconciles, writing only the witness on REVERT or ADVANCE, and yields a reconciled tail only on OK, REVERT or ADVANCE. The end step, under the fence with no project lock, probes writer.lease without waiting (busy skips), reads the tail to copy while the probe is held (the committed tail, or after an uncertain outcome only the reconciled tail, or nothing), releases the probe, and copies the floor forward only if higher; a missing floor is floorLost and a floor above the tail is regression, each writing nothing. Taking the fence and lease is the composition owner's (X3b-3). Library only."),
    row('crates/security/src/journal_store/carrier_start_tests.rs', 'opensip-security', 'test',
        "Check X3b-1b on scratch installations: the floor step reports the tail the start must confirm (INIT, skipped, current); a consistent start writes nothing and returns the start tail; a moved tail or a missing carrier refuses before any write; REVERT, ADVANCE and INIT write only the witness and never the floor; QUARANTINE at start (witnessless restore, malformed witness, protocol violation) refuses and writes nothing; reconciliation after an uncertain outcome is copyable only on OK, REVERT or ADVANCE, writing the witness only on REVERT or ADVANCE; the end step copies the committed tail forward and never down, releases its probe, refuses regression and a lost floor without writing; a busy writer lease skips the copy; after an uncertain outcome only the reconciled tail is copied and without one nothing runs; and a floor bound to another namespace refuses at end."),
]
parent = pin(M + 'repository-file-inventory.v91.json')
parent_inventory = json.loads((A / parent['path']).read_bytes())
candidate_inventory = dict(parent_inventory)
candidate_inventory['standing'] = 'PROPOSED additive journal carrier start and end step layout (law X3b r6); no release, custody, profile, boot or creator qualification'
files = sorted(parent_inventory['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(parent_inventory['files']) + 2
candidate_inventory['files'] = files
(A / OUT).write_text(json.dumps(candidate_inventory, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in parent_inventory['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_inventory.items() if k not in ('files', 'standing')} == {k: v for k, v in parent_inventory.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'journal-carrier-inventory-v91/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory91 is not the selected X3b-1a candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive journal carrier start and end step layout (law X3b r6); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory91, which carries them unchanged from inventory87. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
