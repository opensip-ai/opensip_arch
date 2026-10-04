"""Read-only content checks for contract successor SYN-1F, written independently of build_syn_1f.py.

It checks:
  1. each of the nine JSON copies equals its parent except that the one NativeCause copy it holds gains exactly
     "source-parse-error" at its code-point position; nothing else changes (deep comparison);
  2. the mirror invariant: after the edit every copy's cause list equals SYN-1's owner copy
     (native-evidence.schemas.v2.json#/$defs/NativeCause/enum) as a list, which is what EXM:851 and the
     enumeration model's drift check compare, and, before it, every parent equals the frozen owner;
  3. the identity copies keep I1-L's member and every override I1-L carried (their parents are I1-L's copies);
  4. design and product copies keep their parents' relations;
  5. the execution-input contract override is insert-only;
  6. the record, the subject and PASSAGES.md agree with the files.

Usage: python3.14 -I -B evidence/check_syn_1f.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-1f'
OWNER = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
OWNER_COPY = f'{BASE}/syn-1/design/native/native-evidence.schemas.v2.json'
CAUSE = ['$defs', 'NativeCause', 'enum']
IDS_CAUSE = ['$defs', 'evaluation-deficiency', 'properties', 'nativeCause', 'oneOf', 0, 'enum']
EXC = 'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md'
CRC1 = 'docs/implementation/m3/snapshot-plan-c/crc-1/successor.json'


def apply_pointer(doc, pointer, before, after):
    parts = [x.replace('~1', '/').replace('~0', '~') for x in pointer[1:].split('/')]
    holder = doc
    for k in parts[:-1]:
        holder = holder[int(k)] if isinstance(holder, list) else holder[k]
    assert holder[parts[-1]] == before, pointer
    holder[parts[-1]] = after


def read(path):
    return (ARCH / path).read_bytes()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def at(doc, keys):
    for k in keys:
        doc = doc[k]
    return doc


def main():
    record = json.loads(read(f'{UNIT}/successor.json'))
    report = json.loads(read(f'{UNIT}/evidence/copies-report.json'))
    owner = json.loads(read(OWNER))['$defs']['NativeCause']['enum']
    expected = sorted(owner + ['source-parse-error'])
    owner_copy = json.loads(read(OWNER_COPY))['$defs']['NativeCause']['enum'] if (ARCH / OWNER_COPY).exists() else None
    assert owner_copy in (None, expected), 'SYN-1\'s owner copy disagrees'
    seen_copies, carried_total = [], []
    for row in report['copies']:
        parent_path, copy_path = row['parent']['path'], row['copy']['path']
        keys = IDS_CAUSE if 'identity' in copy_path else CAUSE
        parent, copy = json.loads(read(parent_path)), json.loads(read(copy_path))
        carried = [c['jsonPointer'] for c in row['boundOverridesCarried']]
        if carried:
            # only CRC-1's overrides, which bind first, are carried; apply them to get the effective parent
            crc1 = [e for e in json.loads(read(CRC1))['passageOverrides'] if e['parent']['path'] == parent_path]
            assert sorted(carried) == sorted(e['selector']['jsonPointer'] for e in crc1), carried
            # CRC-1 r4 is bound at the base (392499e), so its overrides are ordinary bound entries of the lock
            assert all(c['record'] in ('crc-1', 'crc-1 (binds first)') for c in row['boundOverridesCarried'])
            assert pin(parent_path, read(parent_path)) == crc1[0]['parent']
            for e in crc1:
                apply_pointer(parent, e['selector']['jsonPointer'], e['before'], e['after'])
                apply_pointer(copy, e['selector']['jsonPointer'], e['after'], e['after'])
            carried_total.append((copy_path, len(crc1)))
        assert at(parent, keys) == owner, f'{parent_path} is not an exact owner copy'
        assert at(copy, keys) == expected, copy_path
        holder_p, holder_c = at(parent, keys[:-1]), at(copy, keys[:-1])
        holder_p.pop(keys[-1])
        holder_c.pop(keys[-1])
        assert parent == copy, f'{copy_path} changes something else'
        lines_p, lines_c = read(parent_path).decode().split('\n'), read(copy_path).decode().split('\n')
        assert len(lines_c) == len(lines_p) + 1, copy_path
        seen_copies.append(copy_path)
    assert len(seen_copies) == 9
    assert carried_total == [(f'{UNIT}/design/foundation/identity-schemas.v3.json', 3)], carried_total
    assert CRC1 in [p['path'] for p in record['parents']], 'SYN-1F must name CRC-1 as a parent (it binds first)'
    # 3. identity copies descend from I1-L's copies
    for name in ('design/foundation/identity-schemas.v3.json', 'product/schemas/sources/identity-v3.schema.json'):
        text = read(f'{UNIT}/{name}').decode('utf-8')
        assert text.count('"cycle-representative"') == 2, name
    # (the deep comparison in 1 already proves each identity copy is its I1-L parent plus the member, so
    # I1-L's member and every override I1-L carried are kept)
    # 4. byte-equal pairs
    for d, p in [('execution-inputs.schema.v1.json', 'execution-inputs-v1.schema.json'),
                 ('subject-inventory.schema.v1.json', 'subject-inventory-v1.schema.json'),
                 ('enumeration-plan.schema.v1.json', 'enumeration-plan-v1.schema.json')]:
        assert read(f'{UNIT}/design/foundation/{d}') == read(f'{UNIT}/product/schemas/sources/{p}')
    # 5. EXC override
    (entry,) = record['passageOverrides']
    exc_lines = read(EXC).decode('utf-8').splitlines()
    line = entry['selector']['line']
    assert entry['parent']['path'] == EXC and exc_lines[line - 1] == entry['before']
    assert entry['after'].startswith(entry['before'] + '\n\n')
    assert exc_lines[line] == ''
    # 6. record and subject
    subject = json.loads(read(f'{BASE}/syn-1f-subject.json'))
    for row in subject['files']:
        assert pin(row['path'], read(row['path'])) == row, row['path']
    rec = pin(f'{UNIT}/successor.json', read(f'{UNIT}/successor.json'))
    assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {rec['path']}
    passages = read(f'{UNIT}/PASSAGES.md').decode('utf-8')
    assert entry['after'] in passages
    print(json.dumps({'passed': True, 'copies': len(seen_copies), 'member': 'source-parse-error',
                      'ownerCopyChecked': owner_copy is not None, 'causeList': expected,
                      'carriedFromCrc1': carried_total,
                      'override': f'{EXC}:{line}'}, indent=1))


if __name__ == '__main__':
    main()
