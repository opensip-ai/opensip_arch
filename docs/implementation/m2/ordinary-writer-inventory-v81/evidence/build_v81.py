"""Build inventory81 from selected inventory80 by adding exactly the two X1a
rows, and write its successor record. It projects the eight rows inherited
through inventory80 and the eight 461b description overrides on inventory80.
Run with python3 -I -B from any directory. Deterministic: rerunning
reproduces the same bytes."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/security/src/custody/ordinary_writer.rs', 'opensip-security', 'composition',
        "The ordinary writer's admission (law X1 r1 items 2 to 7). A writer that is not a creator produces the write receipt (the same producer composition as the read side's, typed Write), rechecks it, enters the law 468 durable write gate with the receipt's sealed DurableBarrierQualification as the gate's only input, and rechecks the receipt again while the gate's fence is held; a failed second recheck releases the fence and returns nothing. OrdinaryWriteAdmission grants exactly what DurableInstallation grants: the held fence and confirmed durability, with no store, trust, project, id, grant or commit standing, no serialized form and no conversion into a read session. An absent I is INSTALLATION.NOT_INITIALIZED through the gate's positive absence; nothing is created. Every refusal is its law 468 item 6 row through 468c's maps. Library only: no command is wired."),
    row('crates/security/src/custody/ordinary_writer_tests.rs', 'opensip-security', 'test',
        "Check the ordinary writer's admission on scratch account homes with a creator-published P0 and 462's signed test trees: admission with the fence held, a recheck and release; a development build at CORE.NO_EMBEDDED_RELEASE; an absent I as INSTALLATION.NOT_INITIALIZED with nothing created, and a non-directory at a suffix name not taken as absence; a step 2 recheck refusal that never enters the gate and a step 4 refusal that releases the held fence; busy and budget rows; one attempt and one gate per process; and type-level and source pins that each purpose's receipt lends only its own sealed qualification and that only InitialPlatform implements either."),
]
parent = pin(M + 'repository-file-inventory.v80.json')
v80 = json.loads((A / parent['path']).read_bytes())
v81 = dict(v80)
v81['standing'] = 'PROPOSED additive ordinary writer layout (law X1 r1); no release, custody, profile, boot or creator qualification'
files = sorted(v80['files'] + ADDED, key=lambda r: r['path'])
assert len({r['path'] for r in files}) == len(files) == len(v80['files']) + 2
v81['files'] = files
out = A / M / 'repository-file-inventory.v81.json'
out.write_text(json.dumps(v81, indent=2) + '\n')
candidate = pin(M + 'repository-file-inventory.v81.json')
old = {r['path']: r for r in v80['files']}
assert all(old[r['path']] == r for r in files if r['path'] in old)
assert {k: v for k, v in v81.items() if k not in ('files', 'standing')} == {k: v for k, v in v80.items() if k not in ('files', 'standing')}
index = {r['path']: i for i, r in enumerate(files)}
prior = json.loads((A / M / 'doctor-report-inventory-v80/successor.json').read_bytes())
projection = []
for p in prior['descriptionOverrideProjection']:
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': p['effectiveDescription']})
# 461b's accepted description overrides on inventory80, now inherited.
b461 = json.loads((A / M / 'stale-descriptions-461b/successor.json').read_bytes())
for o in b461['passageOverrides']:
    assert o['parent'] == parent, o['parent']
    i = int(o['selector']['jsonPointer'].split('/')[2])
    path = v80['files'][i]['path']
    assert v80['files'][i]['description'] == o['before'], path
    projection.append({'filePath': path, 'parentSelector': o['selector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[path]}/description"},
                       'before': o['before'], 'effectiveDescription': o['after']})
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 16
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive ordinary writer layout (law X1 r1); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': 'Resolve all sixteen effective descriptions by stable file path from the selected inherited rows with parent inventory80: the eight rows inherited through inventory80 and the eight 461b description overrides on inventory80. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / M / 'ordinary-writer-inventory-v81/successor.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection)}))
