"""Build the X10b contract successor record: the doctor-report-not-producible
golden's situation and remedy in the three accepted command inventories. Run with python3 -I -B from
any directory. Deterministic: rerunning reproduces the same bytes."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
D = M + 'read-cli-x10b/'
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def get(doc, pointer):
    node = doc
    for part in pointer.strip('/').split('/'):
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node
INVENTORIES = [
    'docs/coop/design-corrections/workflows/command-inventory.v3.json',
    'docs/implementation/m1/metadata-v2/command-inventory.v4.json',
    'docs/implementation/m1/source-selection-v2/reference/composed-owners/command-inventory.proposed.json',
]
GOLDEN = 26
SITUATION = 'the bounded doctor report cannot be produced: more entries than its bound, or an entry that cannot be bounded; nothing is truncated'
REMEDY = 'Resolve the report-production failure and run doctor again.'
overrides = []
parents = []
for path in INVENTORIES:
    parent = pin(path); parents.append(parent)
    doc = json.loads((A / path).read_bytes())
    assert doc['goldens'][GOLDEN]['id'] == 'doctor-report-not-producible', path
    for field, after in (('situation', SITUATION), ('remedy', REMEDY)):
        pointer = f'/goldens/{GOLDEN}/{field}'
        overrides.append({'parent': parent, 'selector': {'jsonPointer': pointer},
                          'before': get(doc, pointer), 'after': after})
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED X10b read-only CLI wording successor (law X10 r3 items 3 and 8): the doctor-report-not-producible golden situation and remedy in the three accepted command inventories; text-only, no schema, registry, generated code or product change; exact frozen candidate requires actual independent review and root assent.',
    'parents': parents,
    'passageOverrides': overrides,
    'candidates': sorted([pin(D + 'README.md'), pin(D + 'evidence/verify_scratch.py'), pin(D + 'evidence/build_x10b.py')], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'evidence/build_x10b.py'),
            pin(D + 'evidence/verify_scratch.py'), pin(D + 'successor.json')], key=lambda r: r['path'])}
(A / M / 'read-cli-x10b-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'overrides': len(overrides), 'parents': len(parents)}))
