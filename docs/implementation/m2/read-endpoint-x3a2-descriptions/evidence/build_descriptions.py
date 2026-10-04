"""Build unit X3a-2's description successor record and its subject manifest.

Law X3a r5 item 8 gives unit X3a-2 "description overrides for the changed
host and storage readers". This contract successor carries them. Its only
parent is the unit's own inventory candidate, inventory136
(read-endpoint-x3a2-inventory-v136), so every entry is on the final
inventory once both are bound, and verify_design checks it without
projecting it.

Each row of evidence/descriptions.json (path, before, after) becomes one
passageOverrides entry (D1's form) on a plain row of inventory136. It
refuses when:
- inventory136 is not the X3a-2 inventory record's candidate, or its bytes
  differ from that pin;
- a row is inherited: inventory136's record projects a meaning for it, so
  an override would conflict with that projection (installation_lineage.rs
  is such a row; its inherited meaning already describes the read-side
  adoption);
- a row's before differs from its raw inventory136 description;
- an after is empty, unchanged or contains a newline;
- a path is duplicated.

Run with python3 -I -B from any directory. Deterministic. A parent-only
rebuild after inventory136 is rebuilt needs no edit, since rows are found by
path; it needs a new review, because the pins change."""
import hashlib, json
from pathlib import Path
A = Path(__file__).resolve().parents[5]
M = 'docs/implementation/m2/'
D = M + 'read-endpoint-x3a2-descriptions/'
INVENTORY_RECORD = M + 'read-endpoint-x3a2-inventory-v136/successor.json'
EVIDENCE = ['evidence/build_descriptions.py', 'evidence/descriptions.json']
PRODUCT = '3f6f9a5'


def pin(p):
    b = (A / p).read_bytes()
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


inventory_record = json.loads((A / INVENTORY_RECORD).read_bytes())
parent = inventory_record['candidate']
assert parent['path'] == M + 'repository-file-inventory.v136.json', 'the parent must be inventory136'
assert pin(parent['path']) == parent, 'inventory136 bytes differ from its record pin'
inventory = json.loads((A / parent['path']).read_bytes())
index = {row['path']: i for i, row in enumerate(inventory['files'])}
inherited = {p['filePath'] for p in inventory_record['descriptionOverrideProjection']}
rows = json.loads((A / D / 'evidence/descriptions.json').read_bytes())
assert len({r['path'] for r in rows}) == len(rows), 'duplicate path'
overrides = []
for r in sorted(rows, key=lambda r: index[r['path']]):
    i = index[r['path']]
    assert r['path'] not in inherited, f'{r["path"]}: an inherited row takes a supersession, not an override'
    assert inventory['files'][i]['description'] == r['before'], f'{r["path"]}: before differs from the raw description'
    assert isinstance(r['after'], str) and r['after'] and r['after'] != r['before'] and '\n' not in r['after'], r['path']
    overrides.append({'parent': parent, 'selector': {'jsonPointer': f'/files/{i}/description'},
                      'before': r['before'], 'after': r['after']})
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED X3a-2 description successor (law X3a r5 item 8): refreshed descriptions of '
                 f'{len(overrides)} plain rows of {Path(parent["path"]).name}, the host and storage readers whose '
                 f'text no longer describes the file once they adopt the read session\'s selected store endpoint '
                 f'(product {PRODUCT} plus unit X3a-2); description-only, no schema, registry, generated code, '
                 'inventory or product change; exact frozen candidate requires actual independent review and root assent.'),
    'parents': [parent],
    'passageOverrides': overrides,
    'passageSupersessions': [],
    'candidates': sorted([pin(D + 'README.md')] + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'successor.json')]
           + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path'])}
(A / M / 'read-endpoint-x3a2-descriptions-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'parent': parent['path'], 'overrides': {o['selector']['jsonPointer']: inventory['files'][int(o['selector']['jsonPointer'].split('/')[2])]['path'] for o in overrides}}, indent=1))
