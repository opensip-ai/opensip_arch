"""Build inventory104 by adding exactly the five X12a rows (law X12 r3 items 2
to 7 and 9, evaluator side) to the inventory the real product lock selects,
and write its successor record. The parent follows the lock: inventory101
(unit X3b-2, selected at product 9dbefb9). It projects the sixteen rows
inherited through the parent. Run with python3 -I -B from any directory.
Deterministic for a given lock: rerunning reproduces the same bytes. It
refuses to write over any path git already tracks, and while a lock selects
inventory104. It was first built on inventory102 at 920941b; X3b-2 then
integrated, so it is rebuilt on inventory101 with the same five rows."""
import hashlib, json, subprocess
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
OUT = M + 'repository-file-inventory.v104.json'
RECORD = M + 'policy-pack-x12a-inventory-v104/successor.json'
# Each admissible parent and the successor record that bound the sixteen
# inherited rows to it.
PRIOR = {
    M + 'repository-file-inventory.v102.json': (M + 'ledger-blob-x3c2-inventory-v102/successor.json', 'inventory102', 'X3c-2'),
    M + 'repository-file-inventory.v101.json': (M + 'journal-append-x3b2-inventory-v101/successor.json', 'inventory101', 'X3b-2'),
}
tracked = subprocess.run(['git', '-C', str(A), 'ls-files', OUT, RECORD], capture_output=True, text=True, check=True)
assert not tracked.stdout.strip(), f'refusing to overwrite tracked paths: {tracked.stdout}'
lock = json.loads(Path('/Users/sb/code/opensip-ai/opensip/design-lock.json').read_bytes())
assert all(s['candidate']['path'] != OUT for s in lock['inventorySuccessors']), 'inventory104 is selected; refusing to rebuild it'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def row(path, package, role, description):
    return {'path': path, 'package': package, 'role': role, 'description': description, 'generated': False, 'standing': 'proposed'}
ADDED = [
    row('crates/evaluator/src/pack-registry.json', 'opensip-evaluator', 'registry',
        "Embed the bundled first-party policy-pack registry compiled into the signed core with include_bytes! (law X12 r3 items 2 to 4; unit X12a): rows {packId, name, version, policyDocument, policySha256, contributions} with packId exactly <name>:<version>, matched byte for byte, each document a sibling include_bytes! file whose canonical bytes hash to policySha256. Zero rows in M2, with an empty documents table: every named pack is refused as not bundled until the DR-131 row and its content arrive in X12c. Never read at run time from a project, installation, account, environment, flag or network, and never a release-declaration row."),
    row('crates/evaluator/src/policy_pack_tests.rs', 'opensip-evaluator', 'test',
        "Check X12a (law X12 r3 item 10, evaluator side) over a cfg(test) synthetic registry: NT-1 wrong identities (wrong name or version, bare name, leading zero, case, whitespace and newline, and opensip.preview.typescript.pack:1 itself, not bundled in M2) refused as not bundled with the presented ID; user and third-party supplied documents, including the bundled document's exact bytes, refused by identity; NT-2 script, hook, exec and include members and string expressions refused as imperative with the member's JSON Pointer in canonical order, and non-JSON or non-policy bytes refused as invalid; the test pack admitted with its policy and program digests; bundled digest, contribution, rule-law, imperative, lexical, schema and limit defects and self-inconsistent registries as host-invariant faults, never the caller's imperative row; zero release rows; a source pin that no production path names the test registry or reads at run time; the classifier's pinned closed schema; a 512-rule document reaching no limit; and check_plan_pack over a corpus Plan and derived test-pack Plans."),
    row('crates/evaluator/tests/fixtures/policy-pack-plan-fixture.json', 'opensip-evaluator', 'fixture',
        "Retain the SYNTHETIC corpus Plan and analysis-spec record (copied unchanged from evaluator-parameter-fixtures.json case budget-one-packet, naming policyPackIds fixture.file-observed) from which the X12a tests derive test-pack Plans for check_plan_pack. Test input only, never a release pack or Plan."),
    row('crates/evaluator/tests/fixtures/policy-pack-test-fixture.policy.json', 'opensip-evaluator', 'fixture',
        "Retain the SYNTHETIC test pack's PolicyDocumentV2 bytes: exactly the golden-typescript policy blob of plan-policy-fixtures.json (raw SHA-256 24e41265...). Compiled only into the evaluator's cfg(test) registry; never a release pack."),
    row('crates/evaluator/tests/fixtures/policy-pack-test-registry.json', 'opensip-evaluator', 'fixture',
        "Retain the SYNTHETIC cfg(test) pack registry with its one row opensip.test.fixture.pack:1 (contribution fixture) over the test pack document. Never compiled into a release build or selectable by a production path."),
]
selected = lock['inventorySuccessors'][-1]['candidate']
assert selected['path'] in PRIOR, f'unexpected selected inventory {selected["path"]}'
prior_path, parent_name, parent_unit = PRIOR[selected['path']]
parent = pin(selected['path'])
assert parent == selected, f'{parent_name} bytes differ from the lock'
inherited = json.loads((A / parent['path']).read_bytes())
candidate_doc = dict(inherited)
candidate_doc['standing'] = 'PROPOSED additive bundled policy-pack registry and declarative-only pack admission layout (law X12 r3, unit X12a); no release, custody, profile, boot or creator qualification'
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
    'standing': 'PROPOSED additive bundled policy-pack registry and declarative-only pack admission layout (law X12 r3, unit X12a); independent review and lead assent required',
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
