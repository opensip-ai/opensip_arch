"""v2 setup. Reads only: frozen37, the retained v1 runtime and root's public provisional probe.

Creates new disposable trees in this runtime only:
  work/frozen37  frozen docs/ (reviews/ and caches excluded), key files verified against exact manifest pins
  work/v1final   exact copy of v1 work/edited (retained v1 delta baseline, never edited)
  work/edited    exact copy of v1 work/edited (v2 edits go here)
Verifies the nine v1 after-hashes against v1 review.json, that root's captured DDL equals the v1 final DDL, and
writes a whole-tree hash manifest of v1 work/edited so the v1 -> v2 delta is exact.
"""
import hashlib, json, shutil
from pathlib import Path

FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
EXPECT = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
V1 = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
ROOTPROBE = Path('/tmp/opensip-design-corrections/root-carrier-provisional-read.v1')
BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')


def sha(b):
    return hashlib.sha256(b).hexdigest()


v1review = json.loads((V1 / 'review.json').read_bytes())
nine = v1review['proposedEdits']['files']
extra = ['docs/coop/completion/security-schemas.v2/grant-journal.sql',
         'docs/coop/completion/security-schemas.v2/journal-record.schema.json',
         'docs/coop/completion/security-completion.v1.md',
         'docs/coop/design-corrections/security/check-integrated-carrier.v1.py',
         'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
         'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
         'docs/coop/design-corrections/public-detail-registry.v1.json',
         'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
         'docs/coop/artifacts/d9-exit-contract.v1.14.json',
         'docs/v2/architecture/implementation-normative-inputs.v5.json',
         'docs/v2/architecture/implementation-coverage.v1.json',
         'docs/v2/architecture/commit-recovery-plan.v1.json',
         'docs/v2/architecture/carrier-fault-cases.v1.json']
mbytes = MANIFEST.read_bytes()
pins = {}


def walk(o):
    if isinstance(o, dict):
        if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
            pins.setdefault(o['path'], set()).add(o['sha256'])
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)


walk(json.loads(mbytes))
ignore = shutil.ignore_patterns('reviews', '__pycache__')
shutil.copytree(FROZEN / 'docs', BASE / 'work/frozen37/docs', ignore=ignore, symlinks=True, dirs_exist_ok=False)
shutil.copytree(V1 / 'work/edited/docs', BASE / 'work/v1final/docs', symlinks=True, dirs_exist_ok=False)
shutil.copytree(V1 / 'work/edited/docs', BASE / 'work/edited/docs', symlinks=True, dirs_exist_ok=False)

rows = []
for f in nine:
    rel = f['path']
    rows.append({'path': rel, 'frozenSha256': f['before'], 'v1Sha256': f['after'],
                 'manifestExact': sorted(pins.get(rel, set())),
                 'frozenAgrees': sha((FROZEN / rel).read_bytes()) == f['before'] and sorted(pins.get(rel, set())) == [f['before']],
                 'frozenCopyAgrees': sha((BASE / 'work/frozen37' / rel).read_bytes()) == f['before'],
                 'v1RuntimeAgrees': sha((V1 / 'work/edited' / rel).read_bytes()) == f['after'],
                 'v1finalCopyAgrees': sha((BASE / 'work/v1final' / rel).read_bytes()) == f['after'],
                 'editedCopyAgrees': sha((BASE / 'work/edited' / rel).read_bytes()) == f['after']})
for rel in extra:
    raw = (FROZEN / rel).read_bytes()
    rows.append({'path': rel, 'frozenSha256': sha(raw), 'manifestExact': sorted(pins.get(rel, set())),
                 'frozenAgrees': sorted(pins.get(rel, set())) == [sha(raw)],
                 'frozenCopyAgrees': sha((BASE / 'work/frozen37' / rel).read_bytes()) == sha(raw),
                 'v1finalEqualsFrozen': sha((BASE / 'work/v1final' / rel).read_bytes()) == sha(raw)})
tree = {}
for p in sorted((V1 / 'work/edited').rglob('*')):
    if p.is_file():
        tree[str(p.relative_to(V1 / 'work/edited'))] = sha(p.read_bytes())
tree_bytes = (json.dumps(tree, sort_keys=True, indent=0) + '\n').encode()
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p00-v1-edited-tree-manifest.json').write_bytes(tree_bytes)
copies_equal = all(sha((BASE / 'work/v1final' / k).read_bytes()) == v and sha((BASE / 'work/edited' / k).read_bytes()) == v
                   for k, v in tree.items())
v1_ddl = V1 / 'work/edited/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
record = {
    'manifestSha256': sha(mbytes), 'manifestMatches': sha(mbytes) == EXPECT,
    'rootProbeDdlSha256': sha((ROOTPROBE / 'grant-journal.carrier.v3.sql').read_bytes()),
    'v1FinalDdlSha256': sha(v1_ddl.read_bytes()),
    'rootProbeDdlEqualsV1Final': (ROOTPROBE / 'grant-journal.carrier.v3.sql').read_bytes() == v1_ddl.read_bytes(),
    'v1ReviewJsonSha256': sha((V1 / 'review.json').read_bytes()), 'v1ReviewMdSha256': sha((V1 / 'review.md').read_bytes()),
    'v1ProposedEditsDiffSha256': sha((V1 / 'proposed-edits.diff').read_bytes()),
    'v1EditedTreeFiles': len(tree), 'v1EditedTreeManifestSha256': sha(tree_bytes), 'copiesEqualV1Tree': copies_equal,
    'rows': rows,
}
record['allAgree'] = (record['manifestMatches'] and record['rootProbeDdlEqualsV1Final'] and copies_equal
                      and record['v1ProposedEditsDiffSha256'] == v1review['proposedEdits']['sha256']
                      and all(all(v for k, v in r.items() if k.endswith('Agrees') or k == 'v1finalEqualsFrozen') for r in rows))
(BASE / 'receipts' / 'p00-setup.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'rows'}, indent=2))
print([r['path'] for r in rows if not all(v for k, v in r.items() if k.endswith('Agrees') or k == 'v1finalEqualsFrozen')])
if not record['allAgree']:
    raise SystemExit(1)
