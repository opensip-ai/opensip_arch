"""Build inventory111 by adding exactly the four X2e/X3b-3 rows (law X2 r8
item 7a, the checked operation handoff, composed with law X3b r10 items 1, 3,
3a and 4, unit X3b-3) to the inventory the real product lock selects, and
write its successor record. The parent follows the lock: inventory108 (unit
X3b-4, selected at product 97f630a; built on inventory112, unit X3d-0, at
product f1b8321, for the r1 review, and first on inventory110, unit X2d, at
product 9d51f33). It projects the sixteen rows inherited
through the parent. Run with python3 -I -B from any directory.
Deterministic for a given lock: rerunning reproduces the same bytes. It
writes only its own two paths, refuses to write over any path git already
tracks, and refuses while a lock selects inventory111."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v111.json'
RECORD = M + 'operation-handoff-x2e-inventory-v111/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v108.json': (M + 'journal-rollover-x3b4-inventory-v108/successor.json', 'inventory108', 'X3b-4'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory111 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/operation_handoff.rs', 'opensip-security', 'composition',
        "The checked operation handoff (law X2 r8 item 7a, unit X2e) composed with the grant journal's floor step, carrier start and end step (law X3b r10 items 1, 3, 3a and 4, unit X3b-3), on one ordinary writer's law 468 gate under one held installation fence. In order: the selected store endpoint joined from the gate's one read (law X3a r5); the subject's namespace admitted (X2d, no lock); at the lease-free point, with R current and no project lock held, I/trust confirmed private and N's absolute spelling admitted only if a no-follow status finds the retained N, then X3b's floor step on the write receipt's attempt ledger (X3b's operation ledger) followed by the gate's and the receipt's rechecks; the APPEND-WRITE or EXCLUSIVE lease (X2d); the join, rechecking the subject, the namespace, each locked carrier's binding and the gate, and deriving owner §8's five-field binding {schemaVersion 1, N, S, G, K} from the ACTIVE row and the admitted endpoint; the transfer of the owners out of the fenced gate, never copied; X3b's carrier start on the attempt ledger (INIT creation when the floor step found INIT, the start against the floor step's observation, the append lock), then every owner rechecked again with a registered subject's namespace held to the started footprint; and only then the fence's release, ending the gate's ledger. Any refusal spends the gate and releases the append lock, the lease and then the fence. ProjectOperation is private and not Clone: the started carrier and start tail, the held lease, the binding and the ACTIVE row snapshot, the subject's owners, the carrier place, the endpoint values and required files' full samples with the retained chain to I (no fence), and the write receipt, whose attempt ledger charges the operation's journal steps. Its end path drops the append lock and releases the lease; the end step is then not entered when the owner reports an uncertain journal outcome or when the attempt ledger is closed (law X3b r10 item 4): ProjectOperation::end returns NotEntered, with no fence walk, read or copy and nothing disclosed; otherwise, on the attempt ledger, it retakes the fence by the shared charged walk, no-follow fence open and S7's bounded wait, requires the walked I to be the retained I and trust, host, projects and N still bound by name, runs, when the owner reports X3d's CarrierCapacityExhausted with every journal outcome certain, X3b-4's rollover (law X3b r10 item 13) under its own EXCLUSIVE lease, then the end step's probe, read and floor copy, and releases the fence; a failure is a value that never rewrites the operation's outcome, and a rollover outcome is returned for disclosure on its own row. CarrierPlace, built only here, is the one input of the carrier location's production constructor. Rows: the endpoint's 468c row, X2's item 8 rows, X3b's item 8 carrier rows and the budget row. OperationGuard (X4a) is a seam not built here; no read-session handoff. Library only."),
    row('crates/security/src/custody/operation_handoff_tests.rs', 'opensip-security', 'test',
        "Check X2e with X3b-3 on scratch homes with a creator-published P0, ordinary writers over 462's signed test trees and a registered scratch project (no real home, installation or Git), other holders simulated by nonblocking flocks on separate descriptors and S7's wait run on a scripted clock: a fresh registration's APPEND-WRITE handoff (fence released, writer.lease held and readers.lease free, the INIT floor, the created carrier and its COMMITTED 0 witness, owner §8's binding equal to the ACTIVE row's N and the endpoint's S, G and K, then an end step leaving the floor unchanged and nothing locked); an Eligible root's EXCLUSIVE handoff, a certain append leaving the floor until the end step copies it forward, and the next writer's start at that tail; the floor step written before the lease when EXCLUSIVE then refuses busy, with no carrier created; a busy writer.lease skipping the floor step and refusing busy with nothing written; a floorLost quarantine refused before any lease with nothing written; a budget cut at the handoff's last charge, after the carrier start, releasing the lease and the fence, with the next writer starting on what it left; an uncertain outcome releasing the lease with no fence taken and no copy, and the next writer's floor step copying forward; a busy fence at the end waited for within S7's bound, then disclosed as the busy row with the lease already released; a closed attempt ledger not entering the end step (no walk while the fence is held elsewhere, no copy, nothing disclosed), and the next writer's floor step copying forward; a moved namespace refusing the end copy as required-files-changed with the fence released; a capacity exhaustion reported at an exhausted tail rolling the generation over under the retaken fence (TERMINAL closing generation 1, witness COMMITTED at generation 2) and copying the floor to generation 2's empty tail, with the next writer starting there; the rollover's outcome returned whatever the attempt-ledger charge returned, with the copy's result beside it: a failed reservation (Refused on the budget, no copy), a writer.lease taken by another writer before the rollover (Skipped, then the copy Skipped), a floor I/O refusal (Refused on the host I/O row, then the copy's host I/O failure), an undetermined OPEN at X3b-4's test point (Undetermined on the durability row, no copy), and a copy failure after Rolled (Rolled kept, generation 2 open, the copy's host I/O failure); and a source pin that the carrier location's only production constructor takes this module's carrier place."),
    row('crates/security/src/journal_store/carrier_operation.rs', 'opensip-security', 'composition',
        "The grant journal's half of the operation handoff (law X3b r10 items 1, 3, 3a, 4 and 11; unit X3b-3, composed with X2e): the carrier location's production constructor, which takes only the carrier place X2e's handoff confirms; the floor step at X2's lease-free point, keeping the committed tail the start must confirm; inside the handoff under the fence and the writer lease, item 3a's creation when the floor step found INIT, item 4's carrier start against that observation and item 6's append lock from it, with a skipped floor step (busy writer.lease) refusing on the busy row if the lease was nevertheless taken; and the end step's probe, read and forward-only floor copy after certain outcomes, or, after a capacity exhaustion, the end step from its step 3 (X3b-4's rollover, then the copy). It adds no carrier semantics and composes only X3b-1's, X3b-2's and X3b-4's steps. A cfg(test) helper plants a committed tail with X3b-2's reserved-slot technique, and cfg(test) re-exports carry X3b-4's rollover test points, for the composition owner's tests. Library only."),
    row('crates/security/src/journal_store/carrier_operation_tests.rs', 'opensip-security', 'test',
        "Check X3b-3's journal half on X3b-1's scratch carrier fixture: an INIT floor step writing only the floor, the start creating the carrier and its witness at tail (1, 0), the end copy unchanged before appends and forward after a certain RA, and the next floor step and start at that tail; an INIT floor found without a carrier resuming creation at the start; a floor step skipped on a busy writer.lease leaving nothing to confirm, so the start refuses busy and writes nothing; and the end copy skipped while another writer holds the lease."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive operation handoff and journal composition layout (law X2 r8 item 7a, unit X2e, with law X3b r10, unit X3b-3); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive operation handoff and journal composition layout (law X2 r8 item 7a, unit X2e, with law X3b r10, unit X3b-3); independent review and lead assent required',
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
