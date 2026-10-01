"""Build inventory108 by adding exactly the two X3b-4 rows (law X3b r10 items
4a, 5, 5a, 8, 9, 11 and 13: grant-generation rollover) to the inventory the
real product lock selects, and write its successor record. The parent
follows the lock: inventory106 (units X4T-a2 and X4T-b, selected at product
704251e). It was first built on inventory105 at 0206ce8 (the unreviewed r1),
then on inventory109 at 6dd7363, inventory110 at 9d51f33 and inventory112 at
f1b8321 (accepted at r3).
It projects the sixteen rows inherited through the parent. Run with
python3 -I -B from any directory. Deterministic for a given lock: rerunning
reproduces the same bytes. It refuses to write over any path git already
tracks, and while a lock selects inventory108."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v108.json'
RECORD = M + 'journal-rollover-x3b4-inventory-v108/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v105.json': (M + 'first-registration-x2c-inventory-v105/successor.json', 'inventory105', 'X2c'),
    M + 'repository-file-inventory.v106.json': (M + 'trust-floor-x4tb-inventory-v106/successor.json', 'inventory106', 'X4T-b'),
    M + 'repository-file-inventory.v109.json': (M + 'policy-pack-x12b-inventory-v109/successor.json', 'inventory109', 'X12b'),
    M + 'repository-file-inventory.v110.json': (M + 'namespace-lease-x2d-inventory-v110/successor.json', 'inventory110', 'X2d'),
    M + 'repository-file-inventory.v112.json': (M + 'settlement-reserve-x3d0-inventory-v112/successor.json', 'inventory112', 'X3d-0'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory108 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/journal_store/carrier_rollover.rs', 'opensip-security', 'composition',
        "Grant-generation rollover (law X3b r10 item 13, with items 4a, 5, 5a, 8 and 9; unit X3b-4), as carrier_floor.rs's macOS child module rollover, and the end step's exhaustion input (item 4 step 3). end_step_after_exhaustion takes X3d's CarrierCapacityExhausted {grantGeneration, provenTailSeq} and the released operation's operationRef, runs the rollover, then X3b-1b's floor copy (steps 4 and 5), which after an undetermined rollover copies nothing and is not entered on an attempt ledger the rollover closed (r10); the composition owner holds the fence around it with no project lock held. The rollover refuses an input on which a SEAL still fits (seal_fits) as a broken composition, then makes one fixed reservation on the attempt ledger before any lease (leases, classification with the predecessor and tail queries, witness and floor reads, the entropy draw and clock sample, step 3's one REVERT or ADVANCE witness write, one TERMINAL append at item 5's cost, and OPEN's witness write); a failed reservation takes no lease. It takes EXCLUSIVE as writer.lease then readers.lease LOCK_EX|LOCK_NB, never waiting, and on either busy releases what it took and returns Skipped. Under the lease it observes the carrier start's state (classification, binding, predecessor check, the committed tail, the witness) and the floor (with item 4a's open-successor exception), and decides by item 13's table in order: any quarantine or floor regression refuses; a later generation or an open successor is AlreadyRolled; a closing TERMINAL the witness names OK or ADVANCE is OPEN only; an open generation 9223372036854775807 refuses on the invariant row; a tail below the proven tail refuses as floor regression or uncertainTailLoss; an open in-window tail at or above the proof closes. Closing mints the TERMINAL's operationRef (op- and 16 host-CSPRNG bytes as hex, once per attempt, never the released operation's, no redraw) and one UTC clock sample in the frozen YYYY-MM-DDTHH:MM:SSZ shape before any write, writes a REVERT or ADVANCE witness as the start does, makes its own JournalAppendLock, appends the TERMINAL with cause grantGenerationClosure through item 5 inside item 5a's window, then OPENs G+1 by the witness COMMITTED (G+1, 0, null) alone, drops the lock, and releases readers.lease then writer.lease. It writes no floor (the end step's copy writes (G+1, 0, null) after the lease is released), no carrier row but the TERMINAL, and no carrier_capacity_pause or quarantine row. After a failure after visibility nothing follows in the operation (no reconciliation, carrier read, witness write or floor copy; r9 item 5): the lock is dropped, the lease released, and the outcome disclosed as DURABILITY.COMMIT_FAILED, leaving a crash-table state the next writer's floor step and start reconcile. Decision refusals leave the attempt ledger open for the end step's copy. Outcomes are Skipped, AlreadyRolled, Rolled, Refused and Undetermined, each with item 8's row. Crash and fault hooks, and injectable entropy and clock, exist only under cfg(test). Library only."),
    row('crates/security/src/journal_store/carrier_rollover_tests.rs', 'opensip-security', 'test',
        "Check X3b-4 (law X3b r10 item 11's r7 and r9 cases, and r10's end step on a closed ledger) on scratch installations, with tails near the cap and later generations planted by X3b-2's lifted-and-reinstalled trigger: item 4a's successor witness (COMMITTED 0 is OK and the floor step copies (G+1, 0, null); PENDING 1 is REVERT and copies L; COMMITTED n > 0 is uncertainTailLoss); OPEN from OK and from ADVANCE writing only the witness, with the floor step copying the closing TERMINAL and the end step then (G+1, 0, null); a PENDING after a TERMINAL, an absent, malformed or foreign witness on a closed generation, each refusing with nothing written; generation 9223372036854775807 refusing OPEN on the invariant row at the floor step and the start; the predecessor check (a gap and an unclosed predecessor) refused at the floor step, the start, the end step and the rollover, and a closed predecessor admitted; floor regression against a floor at (G+1, 0) with a witness still naming G, and that floor unchanged against an open successor; r9's open-successor exception (a floor at (G+1, 0, null) with PENDING (G+1, 1) unchanged at the floor step and the end step and AlreadyRolled at the rollover, the next start reverting to COMMITTED (G+1, 0), and (G+1, 1), or (G+1, 0) against a witness naming G, regression at all three); a start after OPEN appending seq 1 of G+1 on the genesis chain. Item 13: a whole rollover in step order with EXCLUSIVE held from both leases to their release and the floor unchanged throughout, no capacity-pause row, the end step then writing (G+1, 0, null) and the next operation appending in G+1; a fresh op- token per attempt that never equals the released operation's, and the frozen body with one UTC clock sample; a reused token, a failed draw and an unrenderable clock refused before any effect; busy writer.lease and readers.lease skipping with nothing written and nothing held; AlreadyRolled; OPEN only on a durable TERMINAL; floor regression and the RF-2 restores at ...988 and ...989 under a proof of ...990 refused before any write, and a decision refusal leaving the attempt ledger open for the end step's copy; an open last generation refused with no TERMINAL; a non-exhaustion input refused before the reservation; busy at level 3 on the busy row; a crash at every crash-table row recovered by the next writer; an uncertain outcome at each effect disclosed on the durability row with nothing following it (the durable state equal to process death at the same point), the end step reading and copying nothing, and the next writer reconciling; the one reservation charged exactly to the attempt ledger before any lease, covering a measured rollover, with a gate ledger untouched and a short ledger taking no lease; the production entry point with host entropy and clock; no end step entered on an attempt ledger the rollover closed (r10), the next writer's floor step copying instead; a source pin that no reconciliation is reachable from an uncertain outcome (the withdrawn reconciliation named nowhere, the undetermined paths building their outcome only, and the uncertain end step returning before any probe or read); and a source pin that the module never waits and writes no floor or marker."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive grant-generation rollover layout (law X3b r10, unit X3b-4); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive grant-generation rollover layout (law X3b r10, unit X3b-4); independent review and lead assent required',
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
