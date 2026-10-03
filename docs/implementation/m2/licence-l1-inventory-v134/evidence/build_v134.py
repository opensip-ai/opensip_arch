"""Build inventory134 by adding exactly one row, the product root LICENSE
(unit L1, owner decision D14: Apache-2.0, recorded in
docs/implementation/m3/analysis-quality/PLAN.md), to the inventory the real
product lock selects, and write its successor record. The parent follows the
lock: inventory133 (unit X9-5, selected at product 8dcfe37 and still at
91cb45a, where X9-4 landed with no inventory successor; its fifty-five
inheritance rows bound with D1's thirty-nine overrides and D2's four
supersessions already folded). It projects the fifty-five rows inherited
through the parent. The README, the root package.json, the eleven Cargo
manifests, the two package.json files of apps/report and providers/typescript
and the two dependency policies are already planned rows; their bytes change
(a license field, a Licence section, two localSources pins), their rows do
not.

A contract successor the lock binds may supersede an inherited row on the
parent (law VD1 item 3). Each such supersession is folded into its row's
inheritance entry: the entry's before stays the raw row text and its
effective description becomes the supersession's after. The row count stays
fifty-five. At product 91cb45a no supersession names inventory133, so
nothing new is folded.

Run with python3 -I -B from any directory. Deterministic for a given lock:
rerunning reproduces the same bytes. It writes only its own two paths,
refuses to write over any path git already tracks, and refuses while a lock
selects inventory134. Usage: build_v134.py [LOCK]; the lock defaults to the
product checkout's design-lock.json."""
import hashlib, json, subprocess, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v134.json'
RECORD = M + 'licence-l1-inventory-v134/successor.json'
LOCK = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip/design-lock.json')
# Each admissible parent and the successor record that bound the fifty-five
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v133.json': (M + 'crash-matrix-x95-inventory-v133/successor.json', 'inventory133', 'X9-5'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(LOCK.read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory134 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('LICENSE', 'repository', 'documentation',
        "State the product's licence: the Apache License, Version 2.0 (owner decision D14), as the canonical apache.org text, byte-identical to the architecture repository's root LICENSE. Each product Cargo package and package.json declares license Apache-2.0; the isolated generator and boundary-checker tooling manifests gain the field with their next pinned closure successor. Not runtime input; no release or distribution qualification."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
assert not any(r['path'] in {a['path'] for a in ADDED} for r in inherited['files']), 'an added path is already a row of the parent'
# The LICENSE row belongs to the repository package and adds no edge.
assert any(p['id'] == 'repository' and p['dependencies'] == [] for p in inherited['packages']), 'the repository package is declared in the parent'
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive licence layout (unit L1, owner decision D14: Apache-2.0): the product root LICENSE; documentation only, no package edge, no release, distribution, custody, profile, boot, trust or creator qualification'
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
# Bound supersessions on the parent (VD1): path -> (before, after). Each
# names its row's current effective description as its before.
supersessions = {}
for binding in lock['contractSuccessors']:
    assert pin(binding['record']['path']) == binding['record'], binding['record']['path']
    for s in json.loads((A / binding['record']['path']).read_bytes()).get('passageSupersessions', []):
        if s['parent'] != parent:
            continue
        i = int(s['selector']['jsonPointer'].split('/')[2])
        path = inherited['files'][i]['path']
        assert path not in supersessions, f'two supersessions of {path}'
        supersessions[path] = (s['before'], s['after'])
# The lock's inheritance rows bind exactly the prior record's projection to
# the parent; each is carried by stable file path to its new index, with any
# bound supersession folded into its effective description.
bound = {json.dumps(o['selector'], sort_keys=True): o for o in lock['inventoryPassageInheritance']}
assert len(bound) == len(prior['descriptionOverrideProjection']) == 55
projection = []
for p in prior['descriptionOverrideProjection']:
    o = bound[json.dumps(p['candidateSelector'], sort_keys=True)]
    assert o['parent'] == parent and o['before'] == p['before'] and o['after'] == p['effectiveDescription'], p['filePath']
    i = int(p['candidateSelector']['jsonPointer'].split('/')[2])
    assert inherited['files'][i]['path'] == p['filePath'] and inherited['files'][i]['description'] == p['before'], p['filePath']
    effective = p['effectiveDescription']
    if p['filePath'] in supersessions:
        before, after = supersessions.pop(p['filePath'])
        assert before == effective, f'{p["filePath"]}: a supersession must name the current meaning'
        effective = after
    projection.append({'filePath': p['filePath'], 'parentSelector': p['candidateSelector'],
                       'candidateSelector': {'jsonPointer': f"/files/{index[p['filePath']]}/description"},
                       'before': p['before'], 'effectiveDescription': effective})
assert not supersessions, f'supersessions of rows with no inheritance entry: {sorted(supersessions)}'
projection.sort(key=lambda p: p['filePath'])
assert len({p['filePath'] for p in projection}) == len(projection) == 55
folded = sum(1 for p, q in zip(sorted(prior['descriptionOverrideProjection'], key=lambda p: p['filePath']), projection) if p['effectiveDescription'] != q['effectiveDescription'])
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED additive licence layout (unit L1, owner decision D14); independent review and lead assent required',
    'parent': parent,
    'candidate': candidate,
    'parentArtifactBytesUnchanged': True,
    'inheritedRowsEqualByValue': True,
    'packageDependencyGraphUnchanged': True,
    'pendingDecisionsInheritedUnchanged': True,
    'addedFiles': [r['path'] for r in ADDED],
    'carriedUnresolvedObligations': prior['carriedUnresolvedObligations'],
    'descriptionOverrideProjection': projection,
    'projectionRule': f'Resolve all fifty-five effective descriptions by stable file path from the selected inherited rows with parent {parent_name}: the sixteen rows carried unchanged from inventory81 onward and the thirty-nine D1 description overrides, with D2\'s four passage supersessions already folded into their effective descriptions, all bound to {parent_name} by the lock' + (f', with {folded} further bound passage supersessions folded into their effective descriptions' if folded else '') + '. Preserve exact before/effective text and projected selector; never drop inherited meaning.',
}
(A / RECORD).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'parent': parent_name, 'files': len(files), 'added': len(ADDED), 'projectionRows': len(projection), 'supersessionsFolded': folded}))
