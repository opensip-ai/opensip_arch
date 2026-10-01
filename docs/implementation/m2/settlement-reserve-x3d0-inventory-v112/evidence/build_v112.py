"""Build inventory112 by adding exactly the one X3d-0 row (law X3d r6 item 8,
the settlement reserve in WorkLedger; item 13's unit X3d-0) to the inventory
the real product lock selects, and write its successor record. The parent
follows the lock: inventory110 (unit X2d, selected at product 9d51f33). It
projects the sixteen rows inherited through the parent. Run with python3 -I
-B from any directory. Deterministic for a given lock: rerunning reproduces
the same bytes. It writes only its own two paths, refuses to write over any
path git already tracks, and refuses while a lock selects inventory112."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v112.json'
RECORD = M + 'settlement-reserve-x3d0-inventory-v112/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v110.json': (M + 'namespace-lease-x2d-inventory-v110/successor.json', 'inventory110', 'X2d'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory112 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/platform/tests/settlement_reserve_tests.rs', 'opensip-platform', 'test',
        "Exercise the public settlement reserve of the work ledger (law X3d r6 items 8 and 13, unit X3d-0): a reserve charged to used at once and never refunded; a settlement still spendable after a nested failure, an unwind, a swallowed failure, a budget overrun or a postcheck overrun has closed the ledger, which still refuses every scope, charge, run, record and effect outside it; charges inside it, including nested run, effect, ReservedPostchecks and prepaid, drawing only from the allowance with used unchanged, even past exhausted limits; an overrun inside it refused ReservedPostcheck before the work, and an Err, a swallowed failure or an unwind inside it latching both the settlement and the ledger, so no second step runs; a successful settlement leaving an open ledger open; a second reservation, before or after the spend, and a reservation on a closed ledger or beyond the limits refused on existing BudgetFailure variants, taking nothing and latching; a reserve from another instance refused Closed before its action; another ledger unchanged; and a source pin that no production source names reserve_settlement or SettlementReserve until X3d-1. Pure accounting and borrow tests; no journal, carrier, native effect or end-path qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive work-ledger settlement reserve test layout (law X3d r6 items 8 and 13, unit X3d-0); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive work-ledger settlement reserve test layout (law X3d r6 items 8 and 13, unit X3d-0); independent review and lead assent required',
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
