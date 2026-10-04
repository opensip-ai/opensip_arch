"""Read-only content checks for contract successor SYN-1, written independently of build_syn_1.py.

It reads only the architecture repository (and, with --product, two read-only `git show` blobs). It checks:
  1. every passage override is insert-only: `before` is the parent line, and removing the inserted text from
     `after` gives `before` back;
  2. each JSON copy equals its parent except that NativeCause and input-closure-incomplete.allowedCauses gain
     exactly "source-parse-error" at its code-point position, and that row's `rule` changes; nothing else;
  3. both copies keep the parents' relation (the product copy differs from the design copy exactly as the
     product parent differs from the design parent);
  4. every key the new route row names is an existing native-model key, a key law M3-E1 r3 names, or the one key
     this unit adds (native.syntax-grammar-closure-absent), and every M3-E1 syntax key is named;
  5. the record's candidates, the subject and PASSAGES.md agree with the files.

Usage: python3.14 -I -B evidence/check_syn_1.py [--product /path/to/opensip]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-1'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
NEM = 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
LAW = f'{BASE}/PROPOSAL-r3.md'
PAIRS = [('docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
          f'{UNIT}/design/native/native-evidence.schemas.v2.json'),
         ('docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json',
          f'{UNIT}/product/schemas/sources/native-v2.schema.json')]
CAUSE = ['$defs', 'NativeCause', 'enum']
ALLOWED = ['x-opensip-deficiency-cause-registry', 'deficiencies', 'input-closure-incomplete', 'allowedCauses']
RULE = ['x-opensip-deficiency-cause-registry', 'deficiencies', 'input-closure-incomplete', 'rule']
NEW_KEY = 'native.syntax-grammar-closure-absent'


def read(path):
    return (ARCH / path).read_bytes()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def at(doc, keys):
    for k in keys:
        doc = doc[k]
    return doc


def strip(doc, keys):
    """Remove the value at keys (for the 'nothing else changed' comparison)."""
    for k in keys[:-1]:
        doc = doc[k]
    doc.pop(keys[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', type=Path)
    args = parser.parse_args()
    record = json.loads(read(f'{UNIT}/successor.json'))
    findings = []

    # 1. insert-only overrides
    ne_lines = read(NE).decode('utf-8').splitlines()
    for entry in record['passageOverrides']:
        line = entry['selector']['line']
        before, after = entry['before'], entry['after']
        assert ne_lines[line - 1] == before, line
        if after.startswith(before):
            continue
        prefix = 0
        while prefix < len(before) and before[prefix] == after[prefix]:
            prefix += 1
        suffix = len(before) - prefix
        assert after.endswith(before[prefix:]) and len(after) > len(before), f'NE:{line} is not insert-only'
        assert after[:prefix] + after[len(after) - suffix:] == before, f'NE:{line} is not insert-only'
    lines = sorted(e['selector']['line'] for e in record['passageOverrides'])
    assert lines == [288, 306, 3366, 3530, 3541], lines

    # 2-3. JSON copies
    parents, copies = [], []
    for parent_path, copy_path in PAIRS:
        parent, copy = json.loads(read(parent_path)), json.loads(read(copy_path))
        for keys in (CAUSE, ALLOWED):
            old, new = at(parent, keys), at(copy, keys)
            assert 'source-parse-error' not in old and old == sorted(old)
            assert new == sorted(old + ['source-parse-error']), keys
        assert at(parent, RULE) != at(copy, RULE) and 'thirteen' in at(copy, RULE) and 'twelve' in at(parent, RULE)
        p2, c2 = json.loads(read(parent_path)), json.loads(read(copy_path))
        for keys in (CAUSE, ALLOWED, RULE):
            strip(p2, keys)
            strip(c2, keys)
        assert p2 == c2, f'{copy_path} changes something else'
        parents.append(read(parent_path).decode().split('\n'))
        copies.append(read(copy_path).decode().split('\n'))
        # raw-line view: exactly two inserted lines and one changed line
        added = len(copies[-1]) - len(parents[-1])
        assert added == 2, (copy_path, added)
    import difflib
    rel_parent = [x for x in difflib.unified_diff(parents[0], parents[1], lineterm='', n=0) if not x.startswith('@@')]
    rel_copy = [x for x in difflib.unified_diff(copies[0], copies[1], lineterm='', n=0) if not x.startswith('@@')]
    assert rel_parent[2:] == rel_copy[2:], 'the copies lost their parents\' relation'

    # 4. route-row keys
    row = next(e['after'] for e in record['passageOverrides'] if e['selector']['line'] == 3530).split('\n')[1]
    named = set(re.findall(r'`(native\.syntax-[a-z-]+)`', row))
    model = set(re.findall(r'native\.syntax-[a-z-]+', read(NEM).decode('utf-8')))
    law = set(re.findall(r'native\.syntax-[a-z-]+', read(LAW).decode('utf-8')))
    law_short = {'native.syntax-grammar' + k for k in re.findall(r'`(-[a-z-]+)`', read(LAW).decode('utf-8'))
                 if k.endswith(('mismatch', 'invalid', 'forbidden', 'registry'))}
    known = model | law | law_short
    unknown = named - known - {NEW_KEY}
    assert not unknown, unknown
    expected_new = {'native.syntax-grammar-bundle-manifest-mismatch', 'native.syntax-grammar-definition-mismatch',
                    'native.syntax-grammar-normalization-map-mismatch', 'native.syntax-grammar-execution-model-mismatch',
                    'native.syntax-grammar-engine-mismatch', 'native.syntax-grammar-module-invalid',
                    'native.syntax-grammar-module-import-forbidden', 'native.syntax-grammar-module-exports-mismatch',
                    'native.syntax-grammar-abi-mismatch', 'native.syntax-grammar-symbol-table-mismatch',
                    'native.syntax-grammar-bundle-not-the-registry', 'native.syntax-grammar-build-mismatch',
                    'native.syntax-normalizer-kind-unknown'}
    missing = (model | expected_new | {NEW_KEY}) - named
    assert not missing, missing
    assert expected_new <= known, expected_new - known
    assert 'native.syntax-backend-fault' in law and 'native.syntax-backend-fault' not in named

    # 5. record, subject and passages
    subject = json.loads(read(f'{BASE}/syn-1-subject.json'))
    for row in subject['files']:
        assert pin(row['path'], read(row['path'])) == row, row['path']
    rec_pin = pin(f'{UNIT}/successor.json', read(f'{UNIT}/successor.json'))
    assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {rec_pin['path']}
    passages = read(f'{UNIT}/PASSAGES.md').decode('utf-8')
    for entry in record['passageOverrides']:
        assert entry['after'] in passages and entry['before'] in passages

    # product base blobs equal the product parent (optional)
    if args.product:
        blob = subprocess.run(['git', '-C', str(args.product), 'show', 'cd5958b:schemas/sources/native-v2.schema.json'],
                              check=True, capture_output=True).stdout
        assert blob == read(PAIRS[1][0]), 'product native source differs from its accepted parent'

    print(json.dumps({'passed': True, 'overrides': len(record['passageOverrides']), 'routeKeys': len(named),
                      'existingModelKeys': len(model), 'newLawKeys': len(expected_new), 'unitKey': NEW_KEY,
                      'copies': [pin(c, read(c)) for _, c in PAIRS], 'findings': findings}, indent=1))


if __name__ == '__main__':
    main()
