"""Build inventory95 from inventory93 (unit X2b-1, selected at product 8452ab9)
by adding exactly the two X2b-2 rows, and write its successor record. It
projects the sixteen rows inherited through inventory93. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes. It refuses to write over any path git already tracks.
v94 (ledger creation) and v96 (current trust) are in flight; this unit is
rebuilt on its real predecessor before integration if needed."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v95.json'
RECORD = M + 'git-tracking-inventory-v95/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/git_tracking.rs', 'opensip-security', 'composition',
        "Observe whether the project marker is tracked by any enclosing Git repository (law X2 r5 item 6a and item 1's Git premise scope, unit X2b-2): the process environment read only to refuse (GIT_*, XDG_CONFIG_HOME, a HOME other than H); positive no-follow lookups of .git, .hg, .svn and .jj at every directory of the retained chain up to /, refusing another VCS, a .git that is not a directory, and a .git at or above H or off H's volume; for every enclosing repository the admitted layout (.git custody under the premise, commondir and config.worktree positively absent, the required repository config capped at 64 KiB under a closed parse refusing include, includeIf, core.worktree, a true core.bare, extensions.*, a format version other than 0 and precomposeunicode false) and the index decoded exactly (versions 2, 3 and 4 with extended flags, padding and prefix compression, the trailing SHA-1 checked, link, sdir and unknown required extensions refused); the marker path relative to each worktree root matched ASCII-case-insensitively, gitlinks never matching; the global sources under H; and the fixed system sources read as item 1 states. Every step is charged; the evidence is re-observed and compared for the held-fence recheck. A tracked marker is marker-tracked, inadmissible evidence vcs-unsupported, I/O the host I/O row. Nothing is written. Library only."),
    row('crates/security/src/custody/git_tracking_tests.rs', 'opensip-security', 'test',
        "Check the tracking observation: SHA-1 against FIPS vectors; the closed config parse and every refusal; the environment refusal; synthetic indexes of every version, extension and refusal, and real git indexes of versions 2, 3 and 4 decoded exactly against git ls-files; and, on scratch homes with scratch repositories built by real git under a cleared environment, no repository, an untracked marker, a tracked marker in every index version and after the file is gone, a case-variant entry, outer repositories, gitlinks and subdirectory roots, every layout refusal, the global sources, the environment, the system sources read as item 1 states (including the read-only /etc probe), and the recheck and budget."),
]
parent = pin(M + 'repository-file-inventory.v93.json')
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive Git tracking observation layout (law X2 r5); no release, custody, profile, boot or creator qualification'
files = sorted(inherited['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(inherited['files']) + 2
candidate_doc['files'] = files
(A / OUT).write_text(json.dumps(candidate_doc, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in inherited['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in candidate_doc.items() if k not in ('files', 'standing')} == {k: v for k, v in inherited.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'project-admission-inventory-v93/successor.json').read_bytes())
assert prior['candidate'] == parent, 'inventory93 is not the selected X2b-1 candidate'
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive Git tracking observation layout (law X2 r5); independent review and lead assent required',
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
