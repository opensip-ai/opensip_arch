"""Build the D3 description-batch contract successor record and its subject manifest.

D3 refreshes stale descriptions on the inventory the product lock selects, in one record
with both of verify_design's forms:
- a plain row (no inheritance entry) gets a passageOverrides entry whose before is the
  row's raw description (D1's form);
- an inherited row (exactly one inheritance entry) gets a passageSupersessions entry (law
  VD1 r1) whose before is the row's current meaning and whose supersedes names the row's
  chain tail: its latest supersession if one exists, else its one root override (D2's form).

For each row of evidence/descriptions.json (path, before, after) it refuses when:
- a row has more than one inheritance entry;
- a plain row's before differs from the raw description, or the path already has a
  supersession chain (an override would restate a superseded meaning);
- an inherited row's before differs from the inheritance entry's after or from the tail's
  after, or the raw text differs from the entry's before;
- the root is ambiguous (two different root overrides);
- the after text is empty, unchanged or contains a newline;
- a path is duplicated.

Run with python3 -I -B:

    python3 -I -B build_d3.py [product-checkout]

Deterministic. A parent-only rebuild after another inventory integrates needs no edit, since
rows are found by path; it needs a new review, because the pins change."""
import hashlib, json, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip')
M = 'docs/implementation/m2/'
D = M + 'description-batch-d3/'
EVIDENCE = ['evidence/build_d3.py', 'evidence/descriptions.json', 'evidence/verify_scratch.py']
PRODUCT = '3d2d5b5'


def pin(p):
    b = (A / p).read_bytes()
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


documents = {}


def document(p):
    if p not in documents:
        documents[p] = json.loads((A / p).read_bytes())
    return documents[p]


def row_path(entry):
    """The file path an inventory description passage selects, else None."""
    parts = entry['selector'].get('jsonPointer', '').split('/')
    if len(parts) != 4 or parts[1] != 'files' or parts[3] != 'description' or 'repository-file-inventory' not in entry['parent']['path']:
        return None
    return document(entry['parent']['path'])['files'][int(parts[2])]['path']


lock = json.loads((W / 'design-lock.json').read_text())
parent = lock['inventorySuccessors'][-1]['candidate']
assert pin(parent['path']) == parent, 'selected inventory bytes differ from the lock pin'
inventory = document(parent['path'])
index = {row['path']: i for i, row in enumerate(inventory['files'])}
inheritance = {}
for entry in lock['inventoryPassageInheritance']:
    assert entry['parent'] == parent, 'an inheritance entry is not on the selected inventory'
    inheritance.setdefault(entry['selector']['jsonPointer'], []).append(entry)

# Every meaning-bearing entry per file path, in lock order.
roots, links = {}, {}
for binding in lock['contractSuccessors']:
    record = json.loads((A / binding['record']['path']).read_bytes())
    for kind, entries in (('override', record.get('passageOverrides', [])), ('supersession', record.get('passageSupersessions', []))):
        for entry in entries:
            path = row_path(entry)
            if path is None:
                continue
            named = {'record': binding['record'], 'parent': entry['parent'], 'selector': entry['selector']}
            (roots if kind == 'override' else links).setdefault(path, []).append((named, entry))

rows = json.loads((A / D / 'evidence/descriptions.json').read_bytes())
assert len({r['path'] for r in rows}) == len(rows), 'duplicate path'
overrides, supersessions = [], []
for r in sorted(rows, key=lambda r: index[r['path']]):
    i = index[r['path']]
    pointer = f'/files/{i}/description'
    assert isinstance(r['after'], str) and r['after'] and r['after'] != r['before'] and '\n' not in r['after'], r['path']
    inherited = inheritance.get(pointer, [])
    assert len(inherited) <= 1, f'{r["path"]}: more than one inheritance entry'
    if not inherited:
        assert r['path'] not in links, f'{r["path"]}: a superseded meaning cannot take an override'
        assert inventory['files'][i]['description'] == r['before'], f'{r["path"]}: before differs from the raw description'
        overrides.append({'parent': parent, 'selector': {'jsonPointer': pointer}, 'before': r['before'], 'after': r['after']})
        continue
    if r['path'] in links:
        # verify_design checks the chain's linearity; its tail is the last link.
        tail_named, tail = links[r['path']][-1]
    else:
        candidates = roots.get(r['path'], [])
        assert candidates and all(c[1]['after'] == candidates[0][1]['after'] for c in candidates), f'{r["path"]}: ambiguous root'
        tail_named, tail = candidates[0]
    assert r['before'] == inherited[0]['after'] == tail['after'], f'{r["path"]}: before is not the current meaning'
    assert inventory['files'][i]['description'] == inherited[0]['before'], f'{r["path"]}: raw text changed'
    supersessions.append({'parent': parent, 'selector': {'jsonPointer': pointer}, 'before': r['before'],
                          'after': r['after'], 'supersedes': tail_named})
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED D3 description-batch contract successor (EXIT-PLAN D1/D2 follow-up; law VD1 r1): '
                 f'refreshed descriptions of {len(overrides) + len(supersessions)} rows of {Path(parent["path"]).name} '
                 f'whose text no longer describes the file at product {PRODUCT}: {len(overrides)} plain rows by passage '
                 f'override and {len(supersessions)} inherited rows by explicit supersession; description-only, no schema, '
                 'registry, generated code, inventory or product change; exact frozen candidate requires actual '
                 'independent review and root assent.'),
    'parents': [parent],
    'passageOverrides': overrides,
    'passageSupersessions': supersessions,
    'candidates': sorted([pin(D + 'README.md')] + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path']),
}
(A / D / 'successor.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
subject = {'schemaVersion': 1, 'files': sorted([pin(D + 'README.md'), pin(D + 'successor.json')]
           + [pin(D + e) for e in EVIDENCE], key=lambda r: r['path'])}
(A / M / 'description-batch-d3-subject.json').write_text(json.dumps(subject, indent=2) + '\n')
print(json.dumps({'parent': parent['path'], 'overrides': [o['selector']['jsonPointer'] for o in overrides],
                  'supersessions': [
                      {'selector': s['selector']['jsonPointer'], 'supersedes': s['supersedes']['record']['path'],
                       'supersedesSelector': s['supersedes']['parent']['path'] + '#' + s['supersedes']['selector']['jsonPointer']}
                      for s in supersessions]}, indent=1))
