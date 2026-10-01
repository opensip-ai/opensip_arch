"""Build inventory90 from inventory87 (unit X4T-0, selected at product 5b5f04c)
by adding exactly the two X4T-a rows, and write its successor record. It
projects the sixteen rows inherited through inventory87. Run with python3 -I
-B. Deterministic: rerunning reproduces the same bytes. It refuses to write
over any path git already tracks."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v90.json'
RECORD = M + 'current-trust-inventory-v90/successor.json'
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/trust/current_trust_admission.rs', 'opensip-security', 'service',
        "Admit the installation's current trust read-only (law X4T r5, unit X4T-a), as a child of the retained-head composition in ordinary_targets. A pre-acceptance capsule is refused as F absent (TRUST.NO_ADMITTED_TIME_CONTEXT) before any read. Otherwise it binds the capsule, descriptor and event chain with current_record_bindings::bind (capture_p2 on the native path), bounds the descriptor at 32 events, checks each accepted role's accepted.by against the loaded events of that role, binds the root head with bind_retained_head, opens the root admission record, and authenticates the accepted state from the accepted root through the existing retained-head shared authentication at a 16-link, 16 MiB chain budget. It opens the catalog and revocation heads (body, envelope, admission), history and timeEvidence itself with Budget::load, reverifies the catalog envelope and verifies the revocation list with verify_revocation over exactly those bytes, merges the empty global policy (and a project policy when supplied) for Effective::digest(), evaluates S4 time on the fenced read only (report-only proposes no writes; a reread admits none), and takes the role machine's continuation standing. It returns AdmittedCurrentTrust (standing, S6 epoch, time outcome, revoked subjects) or a refusal naming its law 468 item 6 row. It writes nothing; the write-ahead floor is X4T-b's and consumption is X4a's."),
    row('crates/security/src/trust/current_trust_admission_tests.rs', 'opensip-security', 'test',
        "Check the read-only current-trust admission over X4T-0's signed store: an accepted store is admitted for state schemas 1 and 2 with its epoch, empty-policy digest and install-gate standing; a creator-only capsule is F absent before any read; each continuation refusal names its role and state under CONTINUE-CORE-NOT-TRUSTED; an expired or stale index is admitted as existing-only; time is admitted only on the fenced read, report-only proposes no writes, and the payload-future, beyond-horizon and in-session refusals take their rows; the policy digest is equal on both reads; accepted.by must name a loaded event of that role; each member X4T-a opens is required; the measured view cost is pinned within TRUST_VIEW_COST; the event, chain and ledger bounds refuse on the budget row; and the native read through a supplied fence admits the written store and refuses a replaced record."),
]
parent = pin(M + 'repository-file-inventory.v87.json')
v87 = json.loads((A / parent['path']).read_bytes())
v90 = dict(v87)
v90['standing'] = 'PROPOSED additive read-only current-trust admission (law X4T r5, unit X4T-a); no release, custody, profile, boot or creator qualification'
files = sorted(v87['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v87['files']) + 2
v90['files'] = files
(A / OUT).write_text(json.dumps(v90, indent=2) + '\n')
candidate = pin(OUT)
old = {r['path']: r for r in v87['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v90.items() if k not in ('files', 'standing')} == {k: v for k, v in v87.items() if k not in ('files', 'standing')}
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
    'standing': 'PROPOSED additive read-only current-trust admission (law X4T r5, unit X4T-a); independent review and lead assent required',
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
