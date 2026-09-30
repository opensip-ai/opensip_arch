"""Build inventory80 from selected inventory79 by adding exactly the four
458c-c rows, and write its successor record. Run with python3 -I -B from any
directory. Deterministic: rerunning reproduces the same bytes."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/host/src/doctor_report.rs', 'opensip-host', 'adapter',
        "The doctor report assembler (law 458c r6 items 7, 10 and 12, owner section 5 Diagnostics). A complete installation adds the informational INSTALLATION.DURABILITY_NOT_CHECKED entry with the owner's fixed text, which takes one of the 256 slots: 255 actual defects plus the note is a report, 256 is not. A report without the note keeps the 256-entry bound. defectsFound counts actual defects only, and DOCTOR.DEFECTS_FOUND is set only when that count is positive. A report that cannot be produced is HOST.IO_FAILURE / DOCTOR.REPORT_NOT_PRODUCIBLE, exit 4, and latches the report session; nothing is truncated and no envelope member is added. Doctor's installation check projects an unreachable installation onto its law 468 item 6 row with no report, and each structural finding of a reachable incomplete installation onto one CONFIG.CUSTODY_REFUSED entry with its installation-incomplete subject and fixed remedy. Library only: nothing emits it yet."),
    row('crates/host/src/doctor_report_tests.rs', 'opensip-host', 'test',
        "Check the doctor report assembler against every vector of the reference doctor-cases.json, restated with its two inherited stand-in codes: note placement, owner text and count exclusion; the 255-plus-note and 256 partial bounds; the latch; refusal of an actual defect carrying the note's code; one entry per installation finding with its subject and remedy; a finding too long for a bounded subject as not producible rather than truncated; and an unreachable installation on its row with no report."),
    row('crates/security/src/custody/installation_doctor.rs', 'opensip-security', 'service',
        "Doctor's installation check (law 458c r6 items 7 and 12). It observes I through the same read receipt and observation session as every read command, and differs only at item 7's end: a reachable I that is incomplete or contradictory is not a refusal for doctor, and each structural finding is returned in member order, never collapsed. Every refusal before or at a recheck, and every ordinary read failure, ends on its law 468 item 6 row exactly as for any read command. The fence is released before the result is returned. Library only."),
    row('crates/security/src/custody/installation_doctor_tests.rs', 'opensip-security', 'test',
        "Check doctor's installation check on scratch account homes with a creator-published P0: a complete installation with the fence released; every missing member its own finding in member order; an undecodable pair, marker or node, and a missing node, as their findings; and a missing home, a fence busy through the wait, and a member refused custody each ending on its row with no report."),
]
parent = pin(M + 'repository-file-inventory.v79.json')
v79 = json.loads((A / parent['path']).read_bytes())
v80 = dict(v79)
v80['standing'] = 'PROPOSED additive doctor report layout (law 458c r6); no release, custody, profile, boot or creator qualification'
files = sorted(v79['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v79['files']) + 4
v80['files'] = files
out = A / M / 'repository-file-inventory.v80.json'
out.write_text(json.dumps(v80, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v80.json')
old = {r['path']: r for r in v79['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v80.items() if k not in ('files', 'standing')} == {k: v for k, v in v79.items() if k not in ('files', 'standing')}
prior = json.loads((A / M / 'read-migration-inventory-v79/successor.json').read_bytes())
index = {r['path']: i for i, r in enumerate(files)}
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive doctor report layout (law 458c r6); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all eight effective descriptions by stable file path from the selected inherited rows with parent inventory79. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'doctor-report-inventory-v80/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
