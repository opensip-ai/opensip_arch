"""Build inventory102 by adding exactly the two X3c-2 rows (law X3c r7 items 4
to 7, 9 to 11) to the inventory the real product lock selects, and write its
successor record. The parent follows the lock: inventory99 (unit X2b-2,
selected at product 66bdd05). It projects the sixteen rows inherited through
the parent. Run with python3 -I -B from any directory. Deterministic for a
given lock: rerunning reproduces the same bytes. It refuses to write over any
path git already tracks, and while a lock selects inventory102. inventory100
(the unreviewed build on inventory97) is superseded and left unchanged."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v102.json'
RECORD = M + 'ledger-blob-x3c2-inventory-v102/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v99.json': (M + 'git-tracking-inventory-v99/successor.json', 'inventory99', 'X2b-2'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory102 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/storage/src/ledger_store/project_commit.rs', 'opensip-storage', 'store',
        "Publish one commit's objects and prepare, stage and commit its evidence-ledger transaction (law X3c r7 items 4 to 7 and 9 to 11; unit X3c-2), as project_ledger.rs's child module commit. Objects: publication takes the durably admitted attempt; every declared object's length and SHA-256 are checked, and every byte reserved on the operation ledger, before the first write, so a commit that cannot be reserved refuses on the budget row and is never truncated; each object is published into objects/sha256 through blob_store (private temporary file, file barrier, exclusive link, directory barrier) or, only after an exclusive-link collision with unchanged visibility, confirmed byte for byte with its own barriers; an unequal, short or long file, a second link, a shared-writable mode or a non-regular entry at the name is LEDGER.CORRUPT and never overwritten; a failure stops publication and nothing is deleted, renamed or reused. PreparedLedger: BEGIN IMMEDIATE with busy_timeout 0 on the admitted, whole-schema-verified ledger, taken only with the published set (so after every barrier); busy is LEDGER.BUSY_TIMEOUT and holds nothing; owned, single use, not Clone, no SQL surface, and Drop only rolls back. Staging in the open transaction, charged with the COMMIT before the first insert: the exact receipt and association through stage_recovery_pair, the Run material whose blob digests must equal the published objects exactly, the initial availability record, and the Run's pins as a first publication under the attempt's operationRef; any failure drops the transaction, so all rows or none. The owned PreparedLedgerCommit adapter's one consuming method performs only COMMIT: success is Committed, an error or lost connection is Undetermined (DURABILITY.COMMIT_FAILED with the ExecutionId retained), never retried or read back, and the attempt row is never settled. X3d holds the journal transaction, level 4 and the AdmissionPermit around these calls. Crash points and a COMMIT fault hook exist only under cfg(test). Only tests construct a location."),
    row('crates/storage/src/ledger_store/project_commit_tests.rs', 'opensip-storage', 'test',
        "Check X3c-2 on X3c-1's scratch location with a held test writer lease: objects published new (0600, one link, both barriers, no residue) then confirmed byte for byte by a second attempt without rewriting; a wrong length or digest or a repeated digest refused as the invariant row before any write; unequal, short and long bytes, a directory, a link, a shared-writable file and a second hard link at an object name refused as LEDGER.CORRUPT and left unchanged, with earlier objects kept; a commit short of budget refused before the first object; a crash at each object step (temporary write, before the file barrier, after the link, and before the directory barrier with the link lost) keeping earlier objects and the residue, the attempt row admitted and nothing staged, with the next attempt completing; a busy ledger refused at once holding nothing, and a held PreparedLedger busy to other writers; another attempt's objects refused; a staged commit invisible until COMMIT, then every row present and joined as recovery reads it with the attempt still admitted; a failure at each stager (pair collision, blob set, availability Run and generation, pin Run, a reused pin operation) and an operation mismatch committing nothing; a dropped ledger or adapter committing nothing; an injected COMMIT error classified undetermined with nothing committed or retried; staging short of budget; the item 10 rows; and a source pin that the module deletes, settles, waits on and reads back nothing."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive evidence object publication and prepared ledger commit layout (law X3c r7); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive evidence object publication and prepared ledger commit layout (law X3c r7); independent review and lead assent required',
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
