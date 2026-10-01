"""Build inventory93 from inventory91 (unit X3b-1a, selected at product 7e676a9)
by adding exactly the two X2b-1 rows, and write its successor record. It
projects the sixteen rows inherited through inventory91. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any path git already tracks. Unit X2b-1's
reviewed rows are unchanged from inventory88 (r2), rebased onto the linear
chain."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v93.json'
RECORD = M + 'project-admission-inventory-v93/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/project_admission.rs', 'opensip-security', 'composition',
        "Admit a project root under a held installation fence (law X2 r5 items 2 to 5, unit X2b-1): S3 root selection (an explicit path examined once, or the upward walk from the launch directory over retained no-follow handles, at most 256 levels: launch custody refuses, ancestor custody is a boundary, a present opensip.json is custody-checked and selects its directory, then a VCS marker selects the repository root, and home, filesystem root and mount change select the launch); X2a's chain walk; the root's incarnation (APFS volume UUID, inode and native birth); the marker at .opensip/project-id.v1 (.opensip by S3 directory custody under the premise, the marker judged private and read exactly); one capture of the complete registry (the judged file, unchanged, at most 4 MiB, decoded whole, project-registry.v1 positively absent; unavailable never empty); and the registry owner's classification (Eligible, FirstUseCandidate, RecoveryNeeded, OneSided, Contradiction). ProjectRootAdmission is private and not Clone, rechecks chain, volume, marker and registry, and grants nothing until item 6a's tracking (X2b-2). Every step is charged first; each refusal names its item 8 row. Nothing is created. Library only."),
    row('crates/security/src/custody/project_admission_tests.rs', 'opensip-security', 'test',
        "Check project root admission on scratch homes: S3 selection (no candidate selects the launch at the home boundary; every VCS marker kind, including a .git file, selects the repository root; a nested opensip.json wins over an enclosing repository; a config failing custody, a directory or a symlink in its place refuses; launch custody refuses while ancestor custody is a boundary; an explicit path is examined once; selection is charged and refuses on a short ledger), the registry owner's classification table, and admissions through a real read session on a published scratch installation: a first-use candidate on the empty registry, an eligible registered project, one-sided and contradictory rows, a malformed or non-private marker, an unavailable registry (v1 present, malformed), a registry rewritten after the session read, an outside-home root refused before any registry read, and a recheck that sees a marker created afterwards."),
]
parent = pin(M + 'repository-file-inventory.v91.json')
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive project root admission layout (law X2 r5); no release, custody, profile, boot or creator qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + 2
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'journal-carrier-inventory-v91/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory91 is not the selected X3b-1a candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive project root admission layout (law X2 r5); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory91, which carries them unchanged from inventory87. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
