"""Build inventory106 by adding exactly the two X4T-b rows (law X4T r9 items
7, 8 and 12; units X4T-a2 and X4T-b together) to the inventory the real
product lock selects, and write its successor record. The parent follows the
lock: inventory112 (unit X3d-0, selected at product f1b8321). It projects the
sixteen rows inherited through the parent. Run with python3 -I -B from any
directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It refuses to write over any path git already tracks, and while a lock
selects inventory106. It was first built on inventory104 at b642c45 and
rebuilt on inventory105 (X2c, 0206ce8) for review r1; X12b (inventory109,
6dd7363), X2d (inventory110, 9d51f33) and X3d-0 (inventory112, f1b8321) then
integrated, so it is rebuilt on inventory112 with the same two rows (one PRIOR
entry each)."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v106.json'
RECORD = M + 'trust-floor-x4tb-inventory-v106/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v104.json': (M + 'policy-pack-x12a-inventory-v104/successor.json', 'inventory104', 'X12a'),
    M + 'repository-file-inventory.v105.json': (M + 'first-registration-x2c-inventory-v105/successor.json', 'inventory105', 'X2c'),
    M + 'repository-file-inventory.v109.json': (M + 'policy-pack-x12b-inventory-v109/successor.json', 'inventory109', 'X12b'),
    M + 'repository-file-inventory.v110.json': (M + 'namespace-lease-x2d-inventory-v110/successor.json', 'inventory110', 'X2d'),
    M + 'repository-file-inventory.v112.json': (M + 'settlement-reserve-x3d0-inventory-v112/successor.json', 'inventory112', 'X3d-0'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory106 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/trust/floor_publication.rs', 'opensip-security', 'service',
        "Perform the fenced first read's S4 write-ahead floor publication (law X4T r9 items 7 and 8; unit X4T-b), as a child of the current-trust admission, under the installation fence with no project lock and before any lease. The retained trust current owner is the session's one read of trust/stores/S/state.v1 (its bytes, the capsule decoded from them and its full custody sample), with trust/stores/S bound by a metadata recheck, never a second content read; any change but a confirmed publication is required-files-changed. The read admits the owner's capsule through X4T-a, applies rollback check 3 against the floors of every evaluated or retained capsule this fence hold retained before (checks 1 and 2 run in every admission), and, unless report-only, publishes when F rises, L advances or the anchor changes: the before image, the S4EvaluationInputV2 from proposed_time_input's assembler, a host-trust-admission operation with its continue input for the running core, the clock-write event, the by-predecessor descriptor and the successor capsule with every other field unchanged, verified first by successor_record_bindings and current_record_bindings. The publication protocol, shared with X4B-a, reserves its writes and post-publication confirmation before the first effect (each exact reread at the platform's read_bounded_cost with the read session's attempt bound, so nothing is charged after the first effect), writes each dependency through the private-file producer with its file and directory barriers (admitting an existing record only when its bytes are equal), replaces state.v1 last through X3b's private file protocol, rereads and samples it, and advances the owner, minting ConfirmedCurrent for the gate's advance_current. Nothing is retried or deleted; failures take the host I/O, budget, incomplete or custody rows. Library only."),
    row('crates/security/src/trust/floor_publication_tests.rs', 'opensip-security', 'test',
        "Check X4T-a2 and X4T-b (law X4T r9 item 12) on ACL-scratch installations with X4T-0's signed store under a supplied fence: a floor advance is written ahead with F := tEval, the anchor rewritten and every other field, L and the time evidence unchanged, the descriptor in the predecessor's bucket, the pointer last and the retained owner advanced to the confirmed file; the next invocation's fenced read and the native reread admit the store with each accepted role's acceptance event opened by reference, at a pinned measured cost within TRUST_VIEW_COST; accepted.by naming another role's event, a missing event, another store, a non-role event or the current chain's clock-write refuses as incomplete; a confirming admission on the same clock sample writes nothing; report-only and a beyond-horizon refusal write nothing; an in-place rewrite of state.v1 is required-files-changed; check 3 refuses below this hold's floors and an unevaluated predecessor is never compared; checks 1 and 2 over retained, evaluated and unevaluated before-clocks, the evaluation wall and an S4.5 epoch input; a whole-file restore of an older self-consistent state.v1 is admitted, pinning the stated limit; the protocol admits an equal content-addressed record and refuses a foreign one before the pointer; at each reread growth boundary up to the 131072-byte parser cap (16384, 20480, 32768, 53248, 65536, 118784, 131072) a publication beside an equal record of that length completes on an exactly sufficient ledger and refuses before any effect with one byte less; a short ledger writes nothing; and a reread mode is not a fenced first read. Compiled only for tests; confers no qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive trust floor publication layout (law X4T r9, units X4T-a2 and X4T-b); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive trust floor publication layout (law X4T r9, units X4T-a2 and X4T-b); independent review and lead assent required',
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
