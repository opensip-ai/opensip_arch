"""Build inventory105 by adding exactly the two X2c rows (law X2 r8 item 6,
with the registry replacement primitive and the create-or-admit of
I/host, I/host/projects and .opensip) to the inventory the real product lock
selects, and write its successor record. The parent follows the lock:
inventory104 (unit X12a, selected at product b642c45). It projects the
sixteen rows inherited through the parent. Run with python3 -I -B from any
directory. Deterministic for a given lock: rerunning reproduces the same
bytes. It refuses to write over any path git already tracks, and while a
lock selects inventory105."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v105.json'
RECORD = M + 'first-registration-x2c-inventory-v105/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v104.json': (M + 'policy-pack-x12a-inventory-v104/successor.json', 'inventory104', 'X12a'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory105 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/first_registration.rs', 'opensip-security', 'composition',
        "First registration of a project root (law X2 r8 item 6, unit X2c) on the law 468 durable write gate, under its held fence and on its one ledger, with the write-gate entries for project admission and item 6a tracking. Preconditions before any effect: a FirstUseCandidate with the marker positively absent, the admission's own recheck, the tracking observation rechecked, no entry beside P0's lineage under transitions (the active-transition-recovery gate), a present host or projects judged private, up to eight independent ProjectId and UUIDv4 namespace candidates checked against all history and a no-follow occupancy lookup, and capacity (rows, the RESERVED and ACTIVE documents and the worst later terminal spelling within 4 MiB, and the all-registered wrapper, within 4096 rows; PROJECT.SCOPE_LIMIT with S12 subjects). The registry replacement primitive, used for RESERVED and ACTIVE: reconfirm the current owner R by its retained descriptor and full sample and by name, with project-registry.v1 absent; build the complete canonical document and validate it with the same decoder; write a fresh exclusive private temporary name in I with F_FULLFSYNC, confirmed by identity and exact bytes; rename it over the registry; I's barrier and a name recheck by identity. R advances R0 to R1 to R2 only through these confirmed publications, and the gate's retained registry sample with it. The namespace I/host/projects/N is published whole from a private stage holding exactly two empty private lease files, by an exclusive rename with its parent's barrier; host and projects are created or admitted as 465 item 3 does; .opensip is created or admitted under S3 custody with item 1's premise; the 92-byte marker is created no-replace with its file and directory barriers. Every current owner is rechecked before ACTIVE, ACTIVE is built from R1's document, and R2 must classify the root Eligible. Each effect reserves its confirmation work first; any refusal spends the gate, with no retry and no deletion, and leftovers are the registry owner's explicit-recovery cases. Each refusal names its item 8 row; the public projection is the composition owner's. A cfg(test) seam stops at each step and scripts candidate draws. Library only: no lease (X2d) and no handoff (X2e)."),
    row('crates/security/src/custody/first_registration_tests.rs', 'opensip-security', 'test',
        "Check X2c on scratch homes with a creator-published P0, an ordinary writer over 462's signed test trees, and scratch projects (no real home, installation or Git): canonical UUIDv4 candidates, exact document lengths and later spellings and R0's exact re-encoding, and the S12 scope-limit and identity rows; a whole registration (one ACTIVE random row binding the root's path and incarnation, private host and projects, a namespace with exactly two empty private leases, a 0700 .opensip and the exact 0600 marker, no temporary left, the gate's and the project's rechecks passing, a read session then classifying Eligible, and a second registration refused); a reused .opensip and existing parents admitted and never changed; Eligible, RESERVED and one-sided roots refused with nothing written; a VCS change after the observation, a transition entry and a non-private host refused before any effect; eight colliding ProjectId draws, eight occupied namespace paths and failed entropy as host I/O; 4097 rows, a RESERVED document over 4 MiB and a worst later terminal spelling over 4 MiB as PROJECT.SCOPE_LIMIT before any effect; a stop at each of the eleven steps leaving its durable prefix, spending the writer and classifying as the registry owner's recovery cases; a registry rewritten or a marker replaced before ACTIVE refused without ACTIVE; and a later registry change seen by the registered project's recheck."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive first project registration layout (law X2 r8 item 6, unit X2c); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive first project registration layout (law X2 r8 item 6, unit X2c); independent review and lead assent required',
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
