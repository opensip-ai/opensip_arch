"""Verify the frozen source37 manifest and exact bytes of every file this correction reads, edits or runs,
then create two disposable copies (baseline, edited) of frozen docs/ with reviews/ and caches excluded.

Frozen bytes are only read. An existing copy is never overwritten.
"""
import hashlib, json, shutil
from pathlib import Path

FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
EXPECT = '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
KEY = [
    'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
    'docs/coop/design-corrections/security/carrier-format.v3.md',
    'docs/coop/design-corrections/security/carrier-migration.v1.md',
    'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
    'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
    'docs/coop/design-corrections/security/check-carrier-v3.py',
    'docs/coop/design-corrections/security/check-integrated-carrier.v1.py',
    'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
    'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
    'docs/coop/design-corrections/security/source-pins.v1.json',
    'docs/coop/design-corrections/public-detail-registry.v1.json',
    'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
    'docs/coop/design-corrections/current-source-map.proposed.md',
    'docs/v2/architecture/attempt-custody.schema.v1.json',
    'docs/v2/architecture/commit-recovery-readonly.v3.md',
    'docs/v2/architecture/commit-recovery-plan.v1.json',
    'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/store-instance-lineage.v1.json',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
    'docs/v2/architecture/implementation-normative-inputs.v5.json',
    'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/contracts/product-v1/security-and-lifecycle.md',
    'docs/v2/contracts/product-v1/identity-and-evidence.md',
    'docs/coop/artifacts/d9-exit-contract.v1.14.json',
    'docs/coop/completion/security-schemas.v2/grant-journal.sql',
    'docs/coop/completion/security-schemas.v2/journal-record.schema.json',
    'docs/coop/completion/security-completion.v1.md',
    'docs/coop/completion/security_unit_lib_v8.py',
    'docs/operations/check_implementation_planning.py',
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


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
rows = []
for rel in KEY:
    raw = (FROZEN / rel).read_bytes()
    exact = sorted(pins.get(rel, set()))
    rows.append({'path': rel, 'sha256': sha(raw), 'bytes': len(raw), 'manifestExact': exact,
                 'agrees': exact == [sha(raw)]})
ignore = shutil.ignore_patterns('reviews', '__pycache__')
for name in ('baseline', 'edited'):
    shutil.copytree(FROZEN / 'docs', BASE / 'work' / name / 'docs', ignore=ignore, symlinks=True, dirs_exist_ok=False)
for r in rows:
    r['baselineEqual'] = sha((BASE / 'work/baseline' / r['path']).read_bytes()) == r['sha256']
    r['editedEqual'] = sha((BASE / 'work/edited' / r['path']).read_bytes()) == r['sha256']
record = {'manifestSha256': sha(mbytes), 'manifestMatches': sha(mbytes) == EXPECT, 'rows': rows,
          'allAgree': all(r['agrees'] for r in rows),
          'allCopiesEqual': all(r['baselineEqual'] and r['editedEqual'] for r in rows)}
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p00-copy-verify.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: v for k, v in record.items() if k != 'rows'}, indent=2))
print([r['path'] for r in rows if not r['agrees']])
if not (record['manifestMatches'] and record['allAgree'] and record['allCopiesEqual']):
    raise SystemExit(1)
