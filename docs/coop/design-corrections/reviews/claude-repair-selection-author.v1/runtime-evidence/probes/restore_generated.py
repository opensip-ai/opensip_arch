"""Restore any generated report a checker wrote into the author source.

Root's ownership list excludes generated reports in the source. Running
check_native_evidence.v2.py with cwd inside the tree made it rewrite its own report there.
That is an unintended side effect of RUNNING a lane, not an authored change, and it is
restored to the exact frozen31 bytes here.
"""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
FROZEN = '/tmp/opensip-design-corrections/candidate-subject.v31'
HERE = os.path.dirname(os.path.abspath(__file__))

DECLARED = {
    'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/workflows/schemas/repair.schema.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
    'docs/coop/design-corrections/workflows/workflows_model.v3.py',
    'docs/coop/design-corrections/workflows/workflows_model.v1.py',
    'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py',
    'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py',
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


baseline = {r['path']: r for r in json.load(open(os.path.join(HERE, 'author-source-baseline.json')))['files']}
restored = []
for rel, row in sorted(baseline.items()):
    if rel in DECLARED:
        continue
    full = os.path.join(SRC, rel)
    if sha(full) != row['sha256']:
        frozen = os.path.join(FROZEN, rel)
        assert sha(frozen) == row['sha256'], rel
        shutil.copy2(frozen, full)
        restored.append({'path': rel, 'restoredToSha256': row['sha256'],
                         'reason': 'generated report rewritten by running a checker in-tree'})
        print('restored', rel)

json.dump(restored, open(os.path.join(HERE, 'restored-generated.json'), 'w'), indent=2)
print('restored count', len(restored))
