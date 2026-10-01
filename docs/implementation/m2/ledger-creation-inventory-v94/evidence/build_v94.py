"""Build inventory94 from inventory93 (unit X2b-1, selected at product 8452ab9)
by adding exactly the three X3c-1 rows, and write its successor record. It
projects the sixteen rows inherited through inventory93. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any other unit's inventory: the only
tracked paths it may rewrite are this unit's own (inventory94 and its
successor record), and only while they are not selected by a lock."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v94.json'
RECORD = M + 'ledger-creation-inventory-v94/successor.json'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory94 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/store_custody.rs', 'opensip-security', 'service',
        "Store-data custody for the per-project store directories and files (law X3c r6 items 1 and 2), under a supplied retained store directory and the caller's namespace writer lease. create_or_admit_store_directory applies 465 item 3: a charged exclusive 0700 create with the zero-rights owner allow, or, only on a raw EEXIST, a fresh no-follow admission of the existing entry judged private; then the exact name, the parent's filesystem, the directory's own barrier and its parent's barrier. A link or non-directory at the name is a kind refusal; an existing mode or ACL is never changed. create_store_file makes one private 0600 file exclusively after a no-follow absence sample, and open_store_file opens an existing regular file no-follow and judges it private. Store data, not trust state; it selects no store, admits no namespace and grants nothing. Library only."),
    row('crates/storage/src/ledger_store/project_ledger.rs', 'opensip-storage', 'store',
        "Place, create and open the per-(S, N) evidence ledger and admit the attempt (law X3c r6 items 1 to 3, 9 and 10; unit X3c-1). Owner201's spellings: I/stores/S/projects/N/ledger.sqlite with its -wal and -shm, and objects under projects/N/objects/sha256. projects/, projects/N/, objects/ and objects/sha256/ are created or admitted through security's store custody. A new ledger is created exclusively, WAL is selected, then one BEGIN IMMEDIATE runs the selected DDL fragments in their pinned order and COMMITs under synchronous=FULL and fullfsync, the namespace directory is barriered, and the file is reopened through open_existing with a whole-schema equality against the same DDL. An empty file with no -wal is the only resumable creation state; every other stored state is LEDGER.CORRUPT, and nothing is migrated or adopted. The attempt_custody row (admitted, this namespace) is committed in its own non-waiting transaction before any object; a reused ExecutionId is the invariant row and a failed COMMIT is durability-undetermined. Every step is charged. Refusals name their item 10 row; the host projection is X3d's. No object publication, staging, commit, settlement or read-back. Only tests construct a location."),
    row('crates/storage/src/ledger_store/project_ledger_tests.rs', 'opensip-storage', 'test',
        "Check X3c-1 on a scratch installation under the temp directory with a held test writer lease: owner201 spellings and component grammar; directories created then admitted 0700, and a non-private, linked or non-directory entry refused on the CONFIG.CUSTODY_REFUSED custody row with its existing subject and left unchanged; ledger creation committing exactly the selected schema in WAL and then admitted unchanged; an empty file with no -wal resumed; every other creation footprint (empty with -wal, non-database bytes, WAL with no schema, a partial schema, an extra object, rollback-journal mode) refused as LEDGER.CORRUPT; a foreign file mode, a link or a directory at the ledger name refused on the custody row; a replaced ledger name refused as required-files-changed; the attempt row committed before any object directory; a reused ExecutionId and a foreign or settled record refused as the invariant row with nothing written; a busy ledger refused at once, both at attempt admission and during creation; a short ledger refused before any directory; the item 10 rows; and a source pin that the module deletes, renames, publishes and settles nothing."),
]
parent = pin(M + 'repository-file-inventory.v93.json')
parent_doc = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(parent_doc)
candidate_doc['standing'] = 'PROPOSED additive evidence ledger layout and creation (law X3c r6); no release, custody, profile, boot or creator qualification'
files = sorted(parent_doc['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(parent_doc['files']) + 3
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in parent_doc['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in parent_doc.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'project-admission-inventory-v93/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory93 is not the committed X2b-1 candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive evidence ledger layout and creation (law X3c r6); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory93, which carries them unchanged from inventory91. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
