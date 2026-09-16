"""v3 setup. Reads only frozen37, the retained v2 runtime and root's public encoding review.

Creates, in this runtime only:
  work/frozen37  frozen docs/ (reviews/ and caches excluded), key files verified against exact manifest pins
  work/v2final   exact copy of v2 work/edited (retained v2 delta baseline, never edited)
  work/edited    exact copy of v2 work/edited (v3 edits go here)
Verifies the nine v2 hashes against v2 review.json, that root's captured files equal the final v2 DDL and
attempt-custody bytes, and writes a whole-tree hash manifest of v2 work/edited for an exact v2 -> v3 delta.
"""
import hashlib, json, shutil
from pathlib import Path

FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
EXPECT = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
V2 = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
ROOT = Path('/tmp/opensip-design-corrections/root-carrier-encoding-review.v1')
BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')


def sha(b):
    return hashlib.sha256(b).hexdigest()


v2review = json.loads((V2 / 'review.json').read_bytes())
nine = v2review['files']
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
shutil.copytree(V2 / 'work/edited/docs', BASE / 'work/v2final/docs', symlinks=True, dirs_exist_ok=False)
shutil.copytree(V2 / 'work/edited/docs', BASE / 'work/edited/docs', symlinks=True, dirs_exist_ok=False)
rows = []
for f in nine:
    rel = f['path']
    rows.append({'path': rel, 'frozen37': f['frozen37'], 'v2': f['v2'],
                 'frozenAgrees': sha((FROZEN / rel).read_bytes()) == f['frozen37'] and sorted(pins.get(rel, set())) == [f['frozen37']],
                 'frozenCopyAgrees': sha((BASE / 'work/frozen37' / rel).read_bytes()) == f['frozen37'],
                 'v2RuntimeAgrees': sha((V2 / 'work/edited' / rel).read_bytes()) == f['v2'],
                 'v2finalCopyAgrees': sha((BASE / 'work/v2final' / rel).read_bytes()) == f['v2'],
                 'editedCopyAgrees': sha((BASE / 'work/edited' / rel).read_bytes()) == f['v2']})
tree = {str(p.relative_to(V2 / 'work/edited')): sha(p.read_bytes()) for p in sorted((V2 / 'work/edited').rglob('*')) if p.is_file()}
tree_bytes = (json.dumps(tree, sort_keys=True, indent=0) + '\n').encode()
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p00-v2-edited-tree-manifest.json').write_bytes(tree_bytes)
copies_equal = all(sha((BASE / 'work/v2final' / k).read_bytes()) == v and sha((BASE / 'work/edited' / k).read_bytes()) == v for k, v in tree.items())
ddl_rel = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
ac_rel = 'docs/v2/architecture/attempt-custody.schema.v1.json'
record = {
    'manifestSha256': sha(mbytes), 'manifestMatches': sha(mbytes) == EXPECT,
    'rootCaptured': {n: sha((ROOT / n).read_bytes()) for n in ('captured-carrier.sql', 'captured-attempt.json', 'probe.py', 'report.json', 'assessment.md')},
    'rootCapturedCarrierEqualsV2Final': (ROOT / 'captured-carrier.sql').read_bytes() == (V2 / 'work/edited' / ddl_rel).read_bytes(),
    'rootCapturedAttemptEqualsV2Final': (ROOT / 'captured-attempt.json').read_bytes() == (V2 / 'work/edited' / ac_rel).read_bytes(),
    'v2Review': {n: sha((V2 / n).read_bytes()) for n in ('review.json', 'review.md', 'proposed-edits.diff', 'v1-to-v2.diff')},
    'v2EditedTreeFiles': len(tree), 'v2EditedTreeManifestSha256': sha(tree_bytes), 'copiesEqualV2Tree': copies_equal, 'rows': rows,
}
record['allAgree'] = (record['manifestMatches'] and record['rootCapturedCarrierEqualsV2Final'] and record['rootCapturedAttemptEqualsV2Final']
                      and copies_equal and record['v2Review']['proposed-edits.diff'] == v2review['diffs']['proposedEditsFrozen37ToV2']['sha256']
                      and all(all(v for k, v in r.items() if k.endswith('Agrees')) for r in rows))
(BASE / 'receipts' / 'p00-setup.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'rows'}, indent=2))
if not record['allAgree']:
    raise SystemExit(1)
