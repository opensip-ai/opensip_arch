"""Build inventory91 from inventory87 (unit X4T-0, selected at product
5b5f04c) by adding exactly the three X3b-1a rows, and write its successor
record. It projects the sixteen rows inherited through inventory87. It
replaces the unselected inventory85 candidate, whose parent inventory84 is
no longer current. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any path git already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v91.json'
RECORD = M + 'journal-carrier-inventory-v91/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/platform/src/filesystem/file_replace.rs', 'opensip-platform', 'adapter',
        "Rename one child onto another name under the same retained directory, charged before the names are copied or any native call (law X3b r4 item 5's file protocol): a no-follow status read refuses a present non-regular target, then one renameat replaces a regular target atomically or creates a missing one. A rename error is the caller's to reconcile as durability-undetermined. Mechanism only: the temporary file's own durability, the directory barrier after it and which names a caller renames belong to the caller. No custody or authority."),
    row('crates/security/src/journal_store/carrier_floor.rs', 'opensip-security', 'composition',
        "The grant-journal carrier floor step and floor-first carrier creation (law X3b r4 items 2, 3, 3a and 5; unit X3b-1a). The private file protocol publishes a witness or floor by a fresh exclusive private temporary name, write and read-back with F_FULLFSYNC, rename, directory barrier, and a no-follow reopen confirming the same file and bytes. The floor step probes writer.lease without waiting and releases it at once (busy skips and writes nothing), observes the floor under trust/carrier-floors, the carrier and the witness read-only, classifies the carrier by format before any floor decision (inherited, footprint and project-binding refusals), decides by the floor table (INIT, resume, copy forward never down, floorLost, uncertainTailLoss, regression, and reconcile_witness as a read-only decision), and writes only the floor, with no project lock held. Creation re-observes INIT, creates the database exclusively and private, sets the WAL and fullfsync writer pragmas, applies the DDL and publishes the format row in one BEGIN IMMEDIATE transaction, takes the file and namespace barriers, and writes the witness COMMITTED 0. Each refusal names its item 8 row; the public mapping, the carrier start's witness writes, the end step and the append are later units. CarrierLocation has no production constructor until X3b-3. Library only."),
    row('crates/security/src/journal_store/carrier_floor_tests.rs', 'opensip-security', 'test',
        "Check X3b-1a on scratch installations: the digest is SHA-256 of canonical N; floor-first INIT, then INIT pending, creation, the WAL and fullfsync pragmas and the format row, then unchanged; a busy writer lease skips with nothing written, and the probe is released before any floor write; every floor-table row (floorLost, INIT resume, uncertainTailLoss including generation 2 at lastSeq 0, witnesslessRestore, witnessMalformed, protocol violation, OK, REVERT and ADVANCE copy forward never down, regression and equal-hash checks); the empty-journal and empty-database crash states; format dispatch before the floor (formats 1 and 2, a partial or unpublished format-3 set, non-database bytes); carrier and floor project-binding and a malformed floor; creation refused outside INIT; the file protocol's rename replacement with no adopted temporary; and a short ledger writing no floor."),
]
parent = pin(M + 'repository-file-inventory.v87.json')
parent_inventory = json.loads((A / parent['path']).read_bytes())
candidate_inventory = dict(parent_inventory)
candidate_inventory['standing'] = 'PROPOSED additive journal carrier floor layout (law X3b r4); no release, custody, profile, boot or creator qualification'
files = sorted(parent_inventory['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(parent_inventory['files']) + 3
candidate_inventory['files'] = files
(A / OUT).write_text(json.dumps(candidate_inventory, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in parent_inventory['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_inventory.items() if k not in ('files', 'standing')} == {k: v for k, v in parent_inventory.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'signed-store-inventory-v87/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory87 is not the selected X4T-0 candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive journal carrier floor layout (law X3b r4); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory87, which carries them unchanged from inventory84. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
