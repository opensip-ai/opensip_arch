"""Build the D1 description-batch contract successor record and its subject manifest.

Reads evidence/descriptions.json (path, before, after per row), resolves each path in the
inventory the product lock selects, and writes one JSON Pointer description override per row
on that inventory. It refuses when a before text differs from the selected row, when a row is
one of the lock's inherited (projected) description rows (those wait for VD1), on a duplicate
path, or on an unchanged or empty after text. Run with python3 -I -B:

    python3 -I -B build_d1.py [product-checkout]

Deterministic: rerunning against the same lock reproduces the same bytes. A parent-only
rebuild after another inventory integrates needs no edit, since rows are found by path."""
import hashlib, json, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip')
M = 'docs/implementation/m2/'
D = M + 'description-batch-d1/'
EVIDENCE = ['evidence/build_d1.py', 'evidence/descriptions.json', 'evidence/verify_scratch.py']
def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
lock = json.loads((W / 'design-lock.json').read_text())
parent = lock['inventorySuccessors'][-1]['candidate']
assert pin(parent['path']) == parent, 'selected inventory bytes differ from the lock pin'
inventory = json.loads((A / parent['path']).read_bytes())
index = {row['path']: i for i, row in enumerate(inventory['files'])}
inherited = {lock_row['selector']['jsonPointer'] for lock_row in lock['inventoryPassageInheritance']}
rows = json.loads((A / D / 'evidence/descriptions.json').read_bytes())
assert len({r['path'] for r in rows}) == len(rows), 'duplicate path'
overrides = []
for r in sorted(rows, key=lambda r: index[r['path']]):
    i = index[r['path']]
    pointer = f'/files/{i}/description'
    assert pointer not in inherited, f'{r["path"]} is an inherited override row (VD1)'
    assert inventory['files'][i]['description'] == r['before'], f'{r["path"]} before differs'
    assert isinstance(r['after'], str) and r['after'] and r['after'] != r['before'], r['path']
    assert '\n' not in r['after'], r['path']
    overrides.append({'parent': parent, 'selector': {'jsonPointer': pointer}, 'before': r['before'], 'after': r['after']})
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED D1 description-batch contract successor (EXIT-PLAN D1): refreshed descriptions of '
                 f'{len(overrides)} plain rows of {Path(parent["path"]).name} whose text no longer describes the file at '
                 'product 8240856; description-only, no schema, registry, generated code, inventory or product change; '
                 'inherited (projected) rows are left to VD1; exact frozen candidate requires actual independent review '
                 'and root assent.'),
    'parents': [parent],
    'passageOverrides': overrides,
    'candidates': sorted([pin(D + 'README.md')] + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'successor.json')]
           + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path'])}
(A / M / 'description-batch-d1-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'parent': parent['path'], 'overrides': len(overrides), 'inheritedRowsExcluded': len(inherited)}))
