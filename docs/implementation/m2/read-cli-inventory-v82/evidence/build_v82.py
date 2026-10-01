"""Build the X10a inventory from its parent by adding exactly the three X10a
rows, and write its successor record. By default the parent is X1a's
inventory81 and the candidate is inventory82. If X10a is integrated before
X1a, run with `--parent 80 --candidate 81` instead (X1a is then renumbered).
The projection carries every effective description override bound to the
parent: its inherited rows and any direct contract overrides on it. Run with
python3 -I -B from any directory. Deterministic: rerunning reproduces the
same bytes."""
import argparse, hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
ARGS = argparse.ArgumentParser()
ARGS.add_argument('--parent', type=int, default=81)
ARGS.add_argument('--candidate', type=int, default=82)
ARGS.add_argument('--prior', default='ordinary-writer-inventory-v81')
ARGS = ARGS.parse_args()
P, C = ARGS.parent, ARGS.candidate
UNIT = f'read-cli-inventory-v{C}'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('apps/cli/tests/doctor_tests.rs', 'opensip-cli', 'test',
        "Run the real built opensip doctor with no override (law X10 items 5 and 7): a development build ends at CORE.NO_EMBEDDED_RELEASE, exit 2, with a command-envelope v7 schema-valid kind failure envelope in JSON and the matching human lines, and the account's real installation untouched; doctor takes no flags and the agent format is not applicable; help and completion list doctor. Source pins keep every environment, home, feature, test or debug selector out of the binary, the doctor ingress and the request path, require exactly one producer call in the ingress, and refuse a features table on the crates of that path."),
    row('crates/host/src/doctor_ingress.rs', 'opensip-host', 'adapter',
        "The opensip doctor ingress (law X10 r3), beside the metadata ingress under the same process-custody request authority; doctor writes nothing durable. It makes exactly one producer call, observe_installation_for_doctor, the process's one attempt, read receipt and observation session, with the native account and the authenticated release and profile producers as its only inputs, and passes doctor's other checks as empty. A produced report or a report that cannot be produced is a kind doctor envelope carrying the assembled DoctorResult unchanged; an unreachable installation is a kind failure envelope with its law 468 item 6 row as termination and its one detail in errors (HOST.IO_FAILURE for the host I/O row). Exit codes derive from the class only. Remedies are the selected golden's where one exists and otherwise one fixed text per row."),
    row('crates/host/src/doctor_ingress_tests.rs', 'opensip-host', 'test',
        "Check the doctor ingress from every value the security layer produces (law X10 items 4, 5 and 7): native-shaped complete and incomplete installations with no other checks, explicitly synthetic report-bound inputs (one other defect plus the note, 255 plus the note versus 256, partial 256 versus 257) and every law 468 item 6 row. Each envelope is validated against the selected command-envelope v7 source schema, its exit derives from its class, and its human output equals the lines its JSON facts imply, the complete termination included; an unproducible envelope without or with an altered nested doctor kind fails validation."),
]
parent = pin(M + f'repository-file-inventory.v{P}.json')
v80 = json.loads((A / parent['path']).read_bytes())
v81 = dict(v80)
v81['standing'] = 'PROPOSED additive read-only CLI layout (law X10 r3); no release, custody, profile, boot or creator qualification'
files = sorted(v80['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v80['files']) + 3
v81['files'] = files
(A / M / f'repository-file-inventory.v{C}.json').write_text(json.dumps(v81, indent=2) + '\n')
candidate = pin(M + f'repository-file-inventory.v{C}.json')
old = {r['path']: r for r in v80['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v81.items() if k not in ('files', 'standing')} == {k: v for k, v in v80.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / ARGS.prior / 'successor.json').read_bytes())
assert prior['candidate'] == parent, 'the prior successor must have produced the parent'
overrides = {}
def add(path, selector, before, after):
    assert path not in overrides, path
    assert v80['files'][int(selector['jsonPointer'].split('/')[2])]['path'] == path, path
    overrides[path] = {'filePath': path, 'parentSelector': selector,
                       'candidateSelector': {'jsonPointer': f"/files/{index[path]}/description"},
                       'before': before, 'effectiveDescription': after}
for p in prior['descriptionOverrideProjection']:
    add(p['filePath'], p['candidateSelector'], p['before'], p['effectiveDescription'])
# Direct contract overrides on the parent (461b's apply when the parent is
# inventory80; X10b overrides no inventory).
for unit in ('stale-descriptions-461b', 'read-cli-x10b'):
    record = json.loads((A / M / unit / 'successor.json').read_bytes())
    for o in record['passageOverrides']:
        if o['parent'] == parent:
            path = v80['files'][int(o['selector']['jsonPointer'].split('/')[2])]['path']
            add(path, o['selector'], o['before'], o['after'])
projection = [overrides[k] for k in sorted(overrides)]
assert len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive read-only CLI layout (law X10 r3); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all sixteen effective descriptions by stable file path from the rows bound to inventory{P}: the eight rows inherited through inventory80 and the eight 461b description overrides on inventory80. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / UNIT / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
