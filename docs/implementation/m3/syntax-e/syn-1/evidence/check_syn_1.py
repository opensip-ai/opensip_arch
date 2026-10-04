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
  5. the record's candidates, the subject and PASSAGES.md agree with the files;
  6. the emitted forms (r2, RF-SYN1-1). The NE:306 key table has exactly one row per route key. For each of the
     eleven existing keys, the table's form equals, character for character, the literal emission the native
     reference model makes (read with ast, never imported) in all three copies: the frozen NEM and B-S9's two
     selected copies. For each M3-E1 chain key, every subject spelling item 5 gives occurs in the law bytes and
     maps to a table form, and every table form is accounted for. A bare form has no colon. The result is
     evidence/key-forms.json (--write writes it; otherwise the check compares with it).

Usage: python3.14 -I -B evidence/check_syn_1.py [--product /path/to/opensip] [--write]
"""
from __future__ import annotations

import argparse
import ast
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
MODELS = [NEM, 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py',
          'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py']
# How the model's non-literal subject parts are written in the table.
PLACEHOLDERS = {'grammar["grammarId"]': '<grammarId>', 'grammar_id': '<grammarId>', 'suffix': '<suffix>',
                'grammar["languageId"]': '<languageId>', 'grammar["syntaxClass"]': '<syntaxClass>',
                'row["syntaxClass"]': '<syntaxClass>'}
# M3-E1 r3 item 5's subject spellings (exactly as in the law bytes) and the table forms each one becomes.
E1_SUBJECTS = {
    'native.syntax-grammar-bundle-manifest-mismatch': [
        ('`<member>:<path\\|size\\|canonical\\|digest>`', ':<member>:path|size|canonical|digest'),
        ('`descriptor:<field>`', ':descriptor:<field>'),
        ('`unlisted:<path>`', ':unlisted:<treePath>'),
        ('`runtime-pin`', ':runtime-pin')],
    'native.syntax-grammar-definition-mismatch': [
        ('`<g>:<path\\|size\\|canonical\\|digest>`', ':<grammarId>:path|size|canonical|digest'),
        ('`<g>:<field>`', ':<grammarId>:grammarId|languageId|syntaxClass|suffixes|grammarVersion'),
        ('`<g>:member:<path>`', ':<grammarId>:member:<treePath>')],
    'native.syntax-grammar-normalization-map-mismatch': [
        ('`missing\\|size\\|canonical`', ':missing|size|canonical'),
        ('`normalizerId\\|levels\\|<level>:<missing\\|path\\|digest\\|bytes>`', ':normalizerId|levels'),
        ('`normalizerId\\|levels\\|<level>:<missing\\|path\\|digest\\|bytes>`', ':<level>:missing|path|digest|bytes')],
    'native.syntax-grammar-execution-model-mismatch': [('`<g>`', ':<grammarId>')],
    'native.syntax-grammar-engine-mismatch': [('`<field>`', ':<field>')],
    'native.syntax-grammar-module-invalid': [('`<g>:<reason>`', ':<grammarId>:<reason>'),
                                             ('`<g>:admission-call`', ':<grammarId>:admission-call')],
    'native.syntax-grammar-module-import-forbidden': [('`<g>`', ':<grammarId>')],
    'native.syntax-grammar-module-exports-mismatch': [('`<g>:<export>`', ':<grammarId>:<export>')],
    'native.syntax-grammar-abi-mismatch': [('`<g>`', ':<grammarId>')],
    'native.syntax-grammar-symbol-table-mismatch': [('`<g>:<digest\\|languageAbi\\|bounds>`',
                                                     ':<grammarId>:digest|languageAbi|bounds')],
    'native.syntax-normalizer-kind-unknown': [('`<g>:<kind>`', ':<grammarId>:<name>')],
    'native.syntax-grammar-build-mismatch': [
        ('`<g>:<field>`', ':<grammarId>:grammarDigest|languageAbi|symbolTableSha256|runtimeVersion'),
        ('`<g>:<field>`', ':<grammarId>:linked-symbol-table')],
    'native.syntax-grammar-bundle-not-the-registry': [('`-bundle-not-the-registry` |', '')],
}
E1_WIDENED = {'native.syntax-normalizer-kind-unknown': 'E-7: <kind> widens to <name> (a node kind, anonymous token '
                                                      'or field of normalizer.v1.json or a mapped level file)'}


def model_emissions(path):
    """{key: [(line, template)]} for every refusals.append(...) whose literal head is a native.syntax- key."""
    src = read(path).decode('utf-8')
    out = {}
    for node in ast.walk(ast.parse(src)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'append'
                and isinstance(node.func.value, ast.Name) and node.func.value.id == 'refusals' and node.args):
            continue
        head = node.args[0]
        while isinstance(head, ast.BinOp):
            head = head.left
        if not (isinstance(head, ast.Constant) and isinstance(head.value, str)
                and head.value.startswith('native.syntax-')):
            continue
        parts = []

        def flat(e):
            if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
                flat(e.left)
                flat(e.right)
            elif isinstance(e, ast.Constant) and isinstance(e.value, str):
                parts.append(e.value)
            else:
                text = ast.get_source_segment(src, e)
                assert text in PLACEHOLDERS, f'{path}:{node.lineno}: unmapped subject expression {text!r}'
                parts.append(PLACEHOLDERS[text])
        flat(node.args[0])
        template = ''.join(parts)
        if template.startswith('native.syntax-'):
            out.setdefault(template.split(':', 1)[0], []).append((node.lineno, template))
    return out


def key_table(after):
    """The NE:306 key table: {key: [forms]} in row order."""
    rows = {}
    lines = after.split('\n')
    start = lines.index('| Key | Emitted form | Subject | Raised when | Branch |')
    for line in lines[start + 2:]:
        if not line.startswith('| `native.'):
            break
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line)[1:-1]]
        assert len(cells) == 5, line
        key = cells[0].strip('`')
        forms = [f.strip().strip('`').replace('\\|', '|') for f in cells[1].split('; ')]
        assert key not in rows
        rows[key] = {'forms': forms, 'subject': cells[2], 'branch': cells[4]}
    return rows


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
    parser.add_argument('--write', action='store_true')
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

    # 6. emitted forms (r2, RF-SYN1-1)
    table = key_table(next(e['after'] for e in record['passageOverrides'] if e['selector']['line'] == 306))
    assert set(table) == named and len(table) == 25, sorted(set(table) ^ named)
    law_text = read(LAW).decode('utf-8')
    emissions = {path: model_emissions(path) for path in MODELS}
    first = emissions[MODELS[0]]
    assert set(first) == model, sorted(set(first) ^ model)
    forms_report = {}
    for key, row in table.items():
        entry = {'forms': row['forms'], 'branch': row['branch']}
        for form in row['forms']:
            assert form == key or form.startswith(key + ':'), (key, form)
        if key in model:
            for path in MODELS:
                got = emissions[path].get(key, [])
                assert [tpl for _, tpl in got] == row['forms'], (path, key, got, row['forms'])
            entry['source'] = 'native reference model, unchanged'
            entry['modelLines'] = {path: [ln for ln, _ in emissions[path][key]] for path in MODELS}
            entry['bare'] = row['forms'] == [key]
        elif key == NEW_KEY:
            assert row['forms'] == [key], 'LD-13: the absence key is bare'
            entry['source'] = 'this unit (LD-13)'
            entry['bare'] = True
        else:
            pairs = E1_SUBJECTS[key]
            for spelling, _ in pairs:
                assert spelling in law_text, (key, spelling)
            assert sorted(key + suffix for _, suffix in pairs) == sorted(row['forms']), (key, row['forms'])
            entry['source'] = 'M3-E1 r3 item 5'
            entry['lawSpellings'] = [{'law': s, 'table': key + suffix} for s, suffix in pairs]
            entry['bare'] = row['forms'] == [key]
            if key in E1_WIDENED:
                entry['widened'] = E1_WIDENED[key]
        if entry['bare']:
            assert ':' not in row['forms'][0]
        forms_report[key] = entry
    bare = sorted(k for k, v in forms_report.items() if v['bare'])
    assert bare == sorted(['native.syntax-grammar-version-not-from-manifest',
                           'native.syntax-grammar-bundle-not-in-closure',
                           'native.syntax-normalizer-spec-not-in-closure', NEW_KEY,
                           'native.syntax-grammar-bundle-not-the-registry']), bare
    report = {'schemaVersion': 1,
              'standing': ('Generated by check_syn_1.py: every syntax grammar context key of the NE:306 table, its '
                           'emitted form(s), and where each form comes from. Evidence, not law.'),
              'models': [pin(m, read(m)) for m in MODELS], 'law': pin(LAW, read(LAW)),
              'keys': forms_report, 'bare': bare}
    out = (json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    target = ARCH / UNIT / 'evidence/key-forms.json'
    if args.write:
        target.write_bytes(out)
    else:
        assert target.read_bytes() == out, 'key-forms.json differs; rerun with --write and rebuild'

    # 5. record, subject and passages
    subject = json.loads(read(f'{BASE}/syn-1-subject.json'))
    for row in subject['files']:   # with --write the report is new, so the subject is compared on the next run
        if args.write and row['path'] == f'{UNIT}/evidence/key-forms.json':
            continue
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
                      'keyTableRows': len(table), 'bareKeys': bare, 'modelCopiesAudited': len(MODELS),
                      'existingModelKeys': len(model), 'newLawKeys': len(expected_new), 'unitKey': NEW_KEY,
                      'copies': [pin(c, read(c)) for _, c in PAIRS], 'findings': findings}, indent=1))


if __name__ == '__main__':
    main()
