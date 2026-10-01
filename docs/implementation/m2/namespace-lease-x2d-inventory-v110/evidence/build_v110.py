"""Build inventory110 by adding exactly the two X2d rows (law X2 r8 item 7,
namespace admission and leases, returning FencedNamespace with the fence
still held) to the inventory the real product lock selects, and write its
successor record. The parent follows the lock: inventory105 (unit X2c,
selected at product 0206ce8) at first build, inventory109 (unit X12b,
selected at product 6dd7363) after the rebase. It projects the sixteen rows inherited through
the parent. Run with python3 -I -B from any directory. Deterministic for a
given lock: rerunning reproduces the same bytes. It writes only its own two
paths, refuses to write over any path git already tracks, and refuses while
a lock selects inventory110."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v110.json'
RECORD = M + 'namespace-lease-x2d-inventory-v110/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v105.json': (M + 'first-registration-x2c-inventory-v105/successor.json', 'inventory105', 'X2c'),
    M + 'repository-file-inventory.v109.json': (M + 'policy-pack-x12b-inventory-v109/successor.json', 'inventory109', 'X12b'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory110 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/namespace_lease.rs', 'opensip-security', 'composition',
        "Namespace admission and leases (law X2 r8 item 7, unit X2d) under a held installation fence, on the fence holder's one ledger: the ordinary writer's law 468 gate (APPEND-WRITE or EXCLUSIVE) or the 458c read session (SHARED-READ only). For an Eligible root with its item 6a tracking observation (N from R0's ACTIVE row) or a project the same writer has just registered (N from R2's ACTIVE row, which must still classify Eligible), never from a caller: the root admission's recheck (chain, incarnation, marker, registry owner, v1 absence) with the tracking recheck, or the registered project's recheck; then I/host, I/host/projects and N confirmed private, exactly named and on their parents' device, and writer.lease and readers.lease opened no-follow and judged private, all retained, with no project lock taken. That NamespaceTarget is the seam where X3b's floor step runs (X3b r8 items 1 and 3, composed by X3b-3): fence held, R current, no project lock. The lease rechecks the subject, the directories and both retained carriers again, then, as one effect reserved before the first lock, takes S7's locks without blocking (SHARED-READ readers.lease LOCK_SH|LOCK_NB; APPEND-WRITE writer.lease LOCK_EX|LOCK_NB; EXCLUSIVE writer.lease then readers.lease, both LOCK_EX|LOCK_NB) on the retained carriers and rechecks each locked carrier's name binding and the directories, then the holder's full recheck. A busy carrier is the busy row; a busy or failed lock or any later refusal releases every lock already taken, in reverse order, while the fence is still held, and spends the gate or latches the session. Absent namespace objects are the incomplete row, custody is 468's custody row, a change is required-files-changed, and FirstUseCandidate is a broken composition. The result, FencedNamespace (the held lease, the ACTIVE row snapshot and the root admission), borrows the fence holder, has no upgrade and never releases the fence: it can be rechecked or dropped, which releases its lease, until item 7a's handoff (X2e). No fence-free lease (item 7's recovery exception is X6's). Library only."),
    row('crates/security/src/custody/namespace_lease_tests.rs', 'opensip-security', 'test',
        "Check X2d on scratch homes with a creator-published P0, an ordinary writer over 462's signed test trees registering a scratch project (no real home, installation or Git), and other holders simulated by nonblocking flocks on separate descriptors: each refusal's item 8 row; a fresh registration's APPEND-WRITE (writer.lease exclusive, readers.lease free, the fence held throughout, the lease released on drop and the fence only with the writer); an Eligible root's EXCLUSIVE with both carriers locked; a read session's SHARED-READ (other readers coexist, EXCLUSIVE refused, the writer's carrier free); busy carriers for EXCLUSIVE, APPEND-WRITE and SHARED-READ as the busy row with no lock left, the fence still held and the gate spent or the session latched; FirstUseCandidate and one-sided roots refused before any namespace object; a missing carrier or N as incomplete, a non-private N or carrier and a linked carrier as custody; a replaced carrier, a new VCS marker and a rewritten registry between the target and the lease refused with no lock; the target holding no project lock, so the floor step's probe succeeds through the retained namespace; the lease's recheck seeing a replaced carrier; and a budget cut anywhere in the lease step leaving no lock."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive namespace admission and lease layout (law X2 r8 item 7, unit X2d); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive namespace admission and lease layout (law X2 r8 item 7, unit X2d); independent review and lead assent required',
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
