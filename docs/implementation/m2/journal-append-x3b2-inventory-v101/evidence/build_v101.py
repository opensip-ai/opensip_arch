"""Build inventory101 by adding exactly the two X3b-2 rows (law X3b r6 items
5, 6, 8, 9 and 11) to the inventory the real product lock selects, and write
its successor record. The parent follows the lock: inventory102 (unit X3c-2,
selected at product 920941b) now; inventory99 (unit X2b-2, product 66bdd05)
was the parent before X3c-2 integrated. Either way it projects the sixteen rows inherited through
the parent. Run with python3 -I -B from any directory. Deterministic for a
given lock: rerunning reproduces the same bytes. It refuses to write over any
path git already tracks, and while a lock selects inventory101."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v101.json'
RECORD = M + 'journal-append-x3b2-inventory-v101/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v99.json': (M + 'git-tracking-inventory-v99/successor.json', 'inventory99', 'X2b-2'),
    M + 'repository-file-inventory.v102.json': (M + 'ledger-blob-x3c2-inventory-v102/successor.json', 'inventory102', 'X3c-2'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory101 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/journal_store/carrier_append.rs', 'opensip-security', 'composition',
        "The grant-journal append protocol (law X3b r6 items 5, 6, 8 and 9; unit X3b-2), as carrier_floor.rs's macOS child module append, under the operation lease the caller holds. JournalAppendLock (level 4) is one in-process mutex per carrier, made only from the CarrierStart it consumes, holding the committed tail its appends follow and two latches that are never reset: REV (after which no SEAL or RA is appended, S6) and undetermined. Level 3: begin opens the carrier read-write through the retained namespace (the same file before and after), sets the WAL and fullfsync writer pragmas with busy_timeout 0, takes BEGIN IMMEDIATE (busy is LEDGER.BUSY_TIMEOUT at once and holds nothing, F06), re-admits the exact definitions, the format row and the SHA-256(N) binding in that transaction, and confirms the tail is the lock's and the witness names it (COMMITTED at the tail, or a PENDING beyond it that a certain failure left), refusing while level 4 is held or after an undetermined outcome. Level 4 is only tried after level 3, never waited on; the held value is the borrow X4's checkpoint receives, and dropping it releases level 4 and then rolls back any open level 3. One append, with both witness publications, their confirmations and the commit reserved before the first effect: build the record at tail + 1 (SEAL, REV, CLN and RA as closed schema-3 bodies through the existing parser, TERMINAL as the frozen recordSchema-1 body with cause grantGenerationClosure only at the reserved slot; the physical operationRef grammar, the domain-framed body hash, chain_law 1 from the genesis value, ordinary records refused at the reserved slot), witness PENDING by the file protocol, INSERT and COMMIT, witness COMMITTED. A SEAL keeps level 4 held after its commit until released (r5); other records release it on return. Failures before visibility are certain; a failure after the PENDING rename, a failed or lost COMMIT, and any failure after the commit are durability-undetermined: the lock latches, refuses every further effect, and reconciles through X3b-1b's reconcile_after_uncertain, writing only the witness. Refusals name item 8's rows, and a broken composition (wrong carrier, lock order, after REV, capacity, the terminal slot, an unbuildable record) the invariant row. Nothing here takes the fence or a lease or writes trust state; grant-generation rollover is not here. Crash and fault hooks exist only under cfg(test). Library only."),
    row('crates/security/src/journal_store/carrier_append_tests.rs', 'opensip-security', 'test',
        "Check X3b-2 on scratch installations: SEAL, REV, CLN, RA and TERMINAL bodies, the domain-framed hash, the genesis and chain_law 1 previous values, and each build refusal (operationRef grammar, fixture or non-run3 Run, non-object epoch, overlong reason, malformed wall clock, a missing previous hash); every protocol step in order, the floor untouched, no temporary witness left, and the reader's own prefix admission accepting the appended RA, SEAL, REV and CLN; a SEAL holding level 4 until released, no level 3 under it and no second record, then level 4 released before level 3; a stop before the record releasing both and committing nothing; a busy journal refused within a second holding nothing; no SEAL or RA after a REV while CLN and REV follow; a crash after each step reconciling by the next floor step and start to OK, REVERT, REVERT, REVERT, ADVANCE and OK; failures before visibility certain with the next append completing, and failures after it undetermined, latching every further effect and reconciling to the stated tail that the end step alone copies; TERMINAL only at the reserved slot, an ordinary record refused there, and nothing after it; a moved tail, a foreign witness and another carrier refused before any write; the reservation refusing before the first effect and covering a measured witness publication; and a source pin that the module never waits, retries, writes trust state or stores a quarantine marker."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive grant-journal append protocol layout (law X3b r6); no release, custody, profile, boot or creator qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + 2
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
    'standing': 'PROPOSED additive grant-journal append protocol layout (law X3b r6); independent review and lead assent required',
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
