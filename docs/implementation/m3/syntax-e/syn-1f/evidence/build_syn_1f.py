"""Build contract successor SYN-1F (law M3-E1 r3, item 19: the foundation mirrors of SYN-1) deterministically.

Writes, under docs/implementation/m3/syntax-e/:
  syn-1f/design/foundation/{execution-inputs.schema.v1.json, identity-schemas.v3.json,
      subject-inventory.schema.v1.json, enumeration-plan.schema.v1.json, evaluator-projection-registry.v1.json}
  syn-1f/product/schemas/sources/{execution-inputs-v1, identity-v3, subject-inventory-v1,
      enumeration-plan-v1}.schema.json
  syn-1f/PASSAGES.md, syn-1f/materialization-map.json, syn-1f/evidence/copies-report.json,
  syn-1f/successor.json and syn-1f-subject.json.

Each JSON copy is its parent's raw bytes with every passage override the product lock binds to that parent
applied in place (none is bound on any of the nine parents; asserted), and one edit: "source-parse-error"
inserted at its code-point position (before "source-replacement-outside-snapshot") in the one NativeCause copy
the parent holds. Nothing else changes.

The identity copies descend from I1-L's selected copies (bound at product 0ceb9ad), not from the frozen
identity-schemas.v3.json, so they keep I1-L's member and the four (design) or two (product) overrides I1-L
carried. The execution-input contract gets one insert-only line override (section 6).

Usage: python3.14 -I -B evidence/build_syn_1f.py [--product /path/to/opensip] [--check]
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-1f'
BASE_REV = '392499e'   # product main with CRC-1 r4 bound (83 contract successors)
F = 'docs/coop/design-corrections/foundation'
ARS = 'docs/implementation/m2/admission-runtime-selection-v1/schemas/sources'
I1L = 'docs/implementation/m3/preview-pack-i1/i1-l'
EXC = f'{F}/execution-inputs-contract.v1.md'
# CRC-1 (M3-C's closure-role successor, in review) overrides three strings of I1-L's design identity copy. SYN-1F
# binds after it: its record is a parent here, so verify_design refuses SYN-1F until CRC-1 is bound, and the copy
# carries CRC-1's overrides. If CRC-1's bytes change, SYN-1F is rebuilt; --without-crc-1 builds the other order.
CRC1 = 'docs/implementation/m3/snapshot-plan-c/crc-1/successor.json'
CRC1_SHA256 = '29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166'   # CRC-1 r4, accepted and bound at 392499e
NES = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
MEMBER = 'source-parse-error'
NEXT_MEMBER = 'source-replacement-outside-snapshot'
CAUSE = '/$defs/NativeCause/enum'
IDS_CAUSE = '/$defs/evaluation-deficiency/properties/nativeCause/oneOf/0/enum'

# parent -> (copy path, NativeCause pointer, product path or None, role)
COPIES = {
    f'{F}/execution-inputs.schema.v1.json':
        (f'{UNIT}/design/foundation/execution-inputs.schema.v1.json', CAUSE, None,
         'EXS: the execution-input owner, which EXM:851 holds equal to NES'),
    f'{I1L}/design/foundation/identity-schemas.v3.json':
        (f'{UNIT}/design/foundation/identity-schemas.v3.json', IDS_CAUSE, None,
         'IDS, as I1-L\'s selected copy'),
    f'{F}/subject-inventory.schema.v1.json':
        (f'{UNIT}/design/foundation/subject-inventory.schema.v1.json', CAUSE, None, 'subject inventory'),
    f'{F}/enumeration-plan.schema.v1.json':
        (f'{UNIT}/design/foundation/enumeration-plan.schema.v1.json', CAUSE, None, 'ENS: enumeration plan'),
    f'{F}/evaluator-projection-registry.v1.json':
        (f'{UNIT}/design/foundation/evaluator-projection-registry.v1.json', CAUSE, None,
         'evaluator projection registry (design only)'),
    f'{ARS}/execution-inputs-v1.schema.json':
        (f'{UNIT}/product/schemas/sources/execution-inputs-v1.schema.json', CAUSE,
         'schemas/sources/execution-inputs-v1.schema.json', 'selected product source of EXS'),
    f'{I1L}/product/schemas/sources/identity-v3.schema.json':
        (f'{UNIT}/product/schemas/sources/identity-v3.schema.json', IDS_CAUSE,
         'schemas/sources/identity-v3.schema.json', 'I1-L\'s selected product source copy of IDS'),
    f'{ARS}/subject-inventory-v1.schema.json':
        (f'{UNIT}/product/schemas/sources/subject-inventory-v1.schema.json', CAUSE,
         'schemas/sources/subject-inventory-v1.schema.json', 'selected product source of the subject inventory'),
    f'{ARS}/enumeration-plan-v1.schema.json':
        (f'{UNIT}/product/schemas/sources/enumeration-plan-v1.schema.json', CAUSE,
         'schemas/sources/enumeration-plan-v1.schema.json', 'selected product source of ENS'),
}
# For the identity product source, the product still holds the frozen m1 copy until I1-a lands.
PRODUCT_TODAY = {'schemas/sources/identity-v3.schema.json':
                 'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json'}

EXC257 = '\n'.join([
    '**The syntax-only `clones-near` envelope (contract successor SYN-1F of law M3-E1, items 14a and 14b).** A '
    'syntax-only `clones-near` binding\'s executed result is exactly one retained `CandidateProducerResultV1`, which '
    'this section and `derive_outcome` admit **unchanged**: no new state, field, refusal code or derivation is '
    'added. Its `producerClosure` is the binding\'s `enumerator.closureId`, which for syntax-universe work is the '
    'core provider closure (law M3-C r6 item 9 and cross-law item X-C1, recorded by identity\'s closure-role '
    'successor CRC-1; this successor adds no closure-role text). Its `stageOrdinal` is the binding row\'s syntax '
    'stage, and its census is the Plan `candidateSourcePaths` that M3-C r6\'s C4a builds (X-C2). Its '
    '`(deficiency, nativeCause)` pair, `examinedPaths`, groups and `sourceBodies` follow native-evidence §1.2\'s '
    'per-file parse outcomes and group retention rule (contract successor SYN-1), so its `nativeCause` may be '
    '`source-parse-error`, now a member of this bundle\'s `NativeCause` copy, and only under '
    '`input-closure-incomplete`. The enumeration-local `source-syntax-invalid` stays distinct: it is a '
    'subject-inventory deficiency for manifest parse failure and never appears on a candidate envelope.',
])
TEXT = [(EXC, 257, EXC257, 'item 19 SYN-1F: EXC section 6 and EXM\'s candidate derivation apply unchanged to '
                           'item 14a\'s syntax-only envelope, with the producer of item 14b')]

STANDING = (
    'PROPOSED SYN-1F foundation successor (law M3-E1 r3, item 19, SYN-1F), joined with SYN-1. source-parse-error '
    'enters exactly the five foundation NativeCause copies, at its code-point position, as complete successor '
    'copies: execution-inputs.schema.v1.json#/$defs/NativeCause/enum, '
    'identity-schemas.v3.json#/$defs/evaluation-deficiency/properties/nativeCause/oneOf/0/enum (from I1-L\'s '
    'selected copy, keeping its member and carried overrides), subject-inventory.schema.v1.json#/$defs/NativeCause/'
    'enum, enumeration-plan.schema.v1.json#/$defs/NativeCause/enum and '
    'evaluator-projection-registry.v1.json#/$defs/NativeCause/enum; and the four selected product source copies '
    'that E2s materializes (execution-inputs-v1, identity-v3 from I1-L\'s product copy, subject-inventory-v1, '
    'enumeration-plan-v1). One insert-only line override of execution-inputs-contract.v1.md section 6: the '
    'syntax-only clones-near envelope is admitted unchanged, with the producer of M3-E1 item 14b as M3-C r6 '
    'X-C1 and CRC-1 record it. No new state, field, refusal code, DeficiencyV2 member or reason vocabulary; no '
    'model or checker change. Binds together with SYN-1, immediately after it. Exact frozen candidate requires '
    'actual independent review and root assent.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def read(path):
    return (ARCH / path).read_bytes()


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def git_show(product, rev, path):
    return subprocess.run(['git', '-C', str(product), 'show', f'{rev}:{path}'], check=True,
                          capture_output=True).stdout


def pointer_get(doc, pointer):
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


def lock_state(product, with_crc1=True):
    lock = json.loads(git_show(product, BASE_REV, 'design-lock.json'))
    accepted = {}
    for name in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(read(lock['approvals'][name]['path']))['files']:
            accepted[row['path']] = row
    for binding in lock['inventorySuccessors']:
        accepted[binding['parent']['path']] = binding['parent']
        accepted[binding['candidate']['path']] = binding['candidate']
    bound = {}
    for binding in lock['contractSuccessors']:
        assert pin(binding['record']['path'], read(binding['record']['path'])) == binding['record']
        record = json.loads(read(binding['record']['path']))
        accepted[binding['record']['path']] = binding['record']
        for row in record['candidates']:
            accepted[row['path']] = row
        name = binding['record']['path'].split('/')[-2]
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            bound.setdefault(entry['parent']['path'], []).append((name, entry))
    bound_records = {b['record']['path']: b['record'] for b in lock['contractSuccessors']}
    if CRC1 in bound_records and bound_records[CRC1]['sha256'] != CRC1_SHA256:
        raise SystemExit('the lock binds another CRC-1 record: rebuild SYN-1F on it (and update CRC1_SHA256)')
    if with_crc1 and CRC1 not in bound_records:
        raw = read(CRC1)
        if sha(raw) != CRC1_SHA256:
            raise SystemExit('CRC-1 changed: rebuild SYN-1F on its new bytes (and update CRC1_SHA256)')
        accepted[CRC1] = pin(CRC1, raw)   # binds first: SYN-1F names it as a parent
        for entry in json.loads(raw)['passageOverrides']:
            if entry['parent']['path'] in COPIES:
                bound.setdefault(entry['parent']['path'], []).append(('crc-1 (binds first)', entry))
    return lock, accepted, bound


EFFECTIVE = {}   # parent -> its effective text (bound and binds-first overrides applied), before SYN-1F's edit


def pointer_set(doc, pointer, value):
    parts = pointer[1:].split('/')
    parent = pointer_get(doc, '/' + '/'.join(parts[:-1])) if len(parts) > 1 else doc
    parent[parts[-1].replace('~1', '/').replace('~0', '~')] = value


def json_copy(parent, pointer, bound):
    raw = read(parent)
    text = raw.decode('utf-8')
    expected = json.loads(raw)
    carried = []
    for name, entry in bound.get(parent, []):
        if entry['parent'] != pin(parent, raw) or set(entry['selector']) != {'jsonPointer'}:
            raise SystemExit(f'a bound entry on {parent} names another revision or is not a pointer')
        ptr = entry['selector']['jsonPointer']
        old, new = json.dumps(entry['before']), json.dumps(entry['after'])
        if text.count(old) != 1 or pointer_get(expected, ptr) != entry['before']:
            raise SystemExit(f'cannot place bound override {ptr} in {parent}')
        text = text.replace(old, new)
        pointer_set(expected, ptr, entry['after'])
        carried.append({'record': name, 'jsonPointer': ptr})
    members = pointer_get(expected, pointer)
    owner = json.loads(read(NES))['$defs']['NativeCause']['enum']
    if members != owner:
        raise SystemExit(f'{parent}{pointer} is not an exact copy of the owner enum')
    effective_text = text
    lines = text.split('\n')
    want = [json.dumps(m) for m in members]
    assert carried == [] or pointer not in [c['jsonPointer'] for c in carried]
    hits = [i for i, line in enumerate(lines) if line.rstrip().endswith('[')
            and [x.strip().rstrip(',') for x in lines[i + 1:i + 1 + len(members)]] == want
            and lines[i + 1 + len(members)].strip().startswith(']')]
    if len(hits) != 1:
        raise SystemExit(f'cannot place {pointer} in {parent}: {hits}')
    at = hits[0] + 1 + members.index(NEXT_MEMBER)
    indent = lines[at][:len(lines[at]) - len(lines[at].lstrip())]
    lines.insert(at, indent + json.dumps(MEMBER) + ',')
    members.insert(members.index(NEXT_MEMBER), MEMBER)
    text = '\n'.join(lines)
    out = text.encode('utf-8')
    EFFECTIVE[parent] = effective_text
    if json.loads(out) != expected:
        raise SystemExit(f'{parent}: copy does not parse to the expected document')
    hunks = [{'parentLines': [i1 + 1, i2], 'copyLines': [j1 + 1, j2]} for tag, i1, i2, j1, j2 in
             difflib.SequenceMatcher(None, raw.decode().split('\n'), text.split('\n'), autojunk=False).get_opcodes()
             if tag != 'equal']
    return out, {'parent': pin(parent, raw), 'copy': pin(COPIES[parent][0], out), 'role': COPIES[parent][3],
                 'jsonPointer': pointer, 'newMemberLine': at + 1, 'boundOverridesCarried': carried, 'hunks': hunks}


def overrides():
    out = []
    for parent, line, insertion, _why in TEXT:
        raw = read(parent)
        lines = raw.decode('utf-8').splitlines()
        before = lines[line - 1]
        assert lines[line] == '', 'a block insertion needs the blank line after its anchor line'
        out.append({'parent': pin(parent, raw), 'selector': {'line': line}, 'before': before,
                    'after': before + '\n\n' + insertion})
    return out


def passages_md(entries):
    parts = ['# SYN-1F passages (generated by evidence/build_syn_1f.py; do not edit)', '',
             'Each `after` keeps its `before` text word for word and only inserts.', '']
    for (parent, line, _i, why), entry in zip(TEXT, entries):
        parts += [f'## {parent}:{line}', '', f'Parent: {entry["parent"]["bytes"]} bytes, '
                  f'`{entry["parent"]["sha256"]}`.', '', f'Source: {why}.', '', '`before`:', '', '~~~~text',
                  entry['before'], '~~~~', '', '`after`:', '', '~~~~text', entry['after'], '~~~~', '']
    return ('\n'.join(parts)).encode('utf-8')


def check(record, subject, files, accepted, bound, lock):
    members = subject['files']
    paths = [row['path'] for row in members]
    assert paths == sorted(set(paths)), 'subject paths must be sorted and unique'
    record_path = f'{UNIT}/successor.json'
    assert {r['path'] for r in record['candidates']} == set(paths) - {record_path}
    for row in members:
        assert pin(row['path'], files[row['path']]) == row
        assert row['path'] not in accepted, f'candidate reuses an accepted path: {row["path"]}'
    parents = record['parents']
    assert [p['path'] for p in parents] == sorted({p['path'] for p in parents}) and parents
    for row in parents:
        assert accepted.get(row['path'], {}).get('sha256') == row['sha256'], row['path']
        assert accepted[row['path']]['bytes'] == row['bytes']
        assert pin(row['path'], read(row['path'])) == row
        assert row['path'] not in paths
    parent_map = {p['path']: p for p in parents}
    seen = set()
    for entry in record['passageOverrides']:
        assert set(entry) == {'parent', 'selector', 'before', 'after'}
        assert parent_map.get(entry['parent']['path']) == entry['parent']
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        assert key not in seen
        seen.add(key)
        assert entry['after'] and entry['before'] != entry['after']
        raw = read(entry['parent']['path'])
        assert raw.decode('utf-8').splitlines()[entry['selector']['line'] - 1] == entry['before']
        try:
            json.loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError('v4 JSON parent passages require JSON Pointer selectors')
        for name, other in bound.get(entry['parent']['path'], []):
            assert json.dumps(other['selector'], sort_keys=True) != key[1], f'selector already bound by {name}'
    for binding in lock['contractSuccessors']:
        assert binding['record']['path'] != record_path


def build(product, with_crc1=True):
    lock, accepted, bound = lock_state(product, with_crc1)
    files, reports = {}, []
    for parent, (path, pointer, product_path, _role) in COPIES.items():
        out, report = json_copy(parent, pointer, bound)
        files[path] = out
        if product_path:
            today = PRODUCT_TODAY.get(product_path, parent)
            if git_show(product, BASE_REV, product_path) != read(today):
                raise SystemExit(f'product {product_path} differs from {today}')
            report['productPath'] = product_path
            report['productToday'] = pin(today, read(today))
        reports.append(report)
    # Design and product copies keep their parents' relations: byte-equal pairs stay byte-equal, and the
    # identity pair differs exactly as I1-L's pair does.
    for design, prod in [('execution-inputs.schema.v1.json', 'execution-inputs-v1.schema.json'),
                         ('subject-inventory.schema.v1.json', 'subject-inventory-v1.schema.json'),
                         ('enumeration-plan.schema.v1.json', 'enumeration-plan-v1.schema.json')]:
        assert files[f'{UNIT}/design/foundation/{design}'] == files[f'{UNIT}/product/schemas/sources/{prod}']

    def body(raw):
        return raw.decode().split('\n')
    rel_parent = list(difflib.unified_diff(EFFECTIVE[f'{I1L}/design/foundation/identity-schemas.v3.json'].split('\n'),
                                           EFFECTIVE[f'{I1L}/product/schemas/sources/identity-v3.schema.json'].split('\n'),
                                           lineterm='', n=0))
    rel_copy = list(difflib.unified_diff(body(files[f'{UNIT}/design/foundation/identity-schemas.v3.json']),
                                         body(files[f'{UNIT}/product/schemas/sources/identity-v3.schema.json']),
                                         lineterm='', n=0))
    strip = lambda d: [x for x in d if not x.startswith(('@@', '---', '+++'))]
    assert strip(rel_parent) == strip(rel_copy), 'identity copies lost their parents\' relation'
    passage_overrides = overrides()
    files[f'{UNIT}/PASSAGES.md'] = passages_md(passage_overrides)
    files[f'{UNIT}/materialization-map.json'] = dumps({
        'schemaVersion': 1,
        'standing': ('Exact schema source bytes for unit E2s: it copies each candidate to its product path and '
                     're-points the generation and admission source maps at it. The identity-v3 copy descends from '
                     'I1-L\'s product copy, so it also carries I1-L\'s cycle-representative member: E2s lands after '
                     'I1-a, or applies I1-a\'s identity source change with it. E2s also re-pins the evaluator '
                     'registries, the admission registry and the generated carriers, which this map does not fix. '
                     'Independent review and root assent are required before selection.'),
        'baseProductRev': BASE_REV,
        'files': [{'productPath': r['productPath'], 'candidatePath': r['copy']['path'],
                   'before': {'bytes': r['productToday']['bytes'], 'sha256': r['productToday']['sha256']},
                   'after': {'bytes': r['copy']['bytes'], 'sha256': r['copy']['sha256']}}
                  for r in sorted(reports, key=lambda r: r.get('productPath', '')) if 'productPath' in r]})
    files[f'{UNIT}/evidence/copies-report.json'] = dumps({
        'schemaVersion': 1, 'baseProductRev': BASE_REV, 'member': MEMBER,
        'owner': {'path': NES, 'jsonPointer': CAUSE, 'note': 'every parent enum equals the owner enum before the '
                                                              'edit; contract successor SYN-1 inserts the same member '
                                                              'at the same position in the owner copy'},
        'copies': reports})
    static = [f'{UNIT}/README.md', f'{UNIT}/evidence/build_syn_1f.py', f'{UNIT}/evidence/check_syn_1f.py',
              f'{UNIT}/evidence/verify_scratch.py']
    for path in static:
        files[path] = read(path)
    parents = sorted({EXC} | set(COPIES) | ({CRC1} if with_crc1 and CRC1 in accepted else set()))
    record = {'schemaVersion': 1, 'standing': STANDING, 'parents': [pin(p, read(p)) for p in parents],
              'passageOverrides': passage_overrides, 'candidates': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{UNIT}/successor.json'] = dumps(record)
    subject = {'schemaVersion': 1, 'files': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{BASE}/syn-1f-subject.json'] = dumps(subject)
    check(record, subject, files, accepted, bound, lock)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--without-crc-1', action='store_true',
                        help='build for the other order (SYN-1F before CRC-1): no CRC-1 parent or carried override')
    args = parser.parse_args()
    files = build(args.product.resolve(), not args.without_crc_1)
    generated = [p for p in files if p.startswith(UNIT + '/') and not p.endswith(('README.md', '.py'))]
    generated.append(f'{BASE}/syn-1f-subject.json')
    for path in sorted(set(generated)):
        target = ARCH / path
        if args.check:
            if target.read_bytes() != files[path]:
                raise SystemExit(f'differs: {path}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    print(json.dumps({'subject': pin(f'{BASE}/syn-1f-subject.json', files[f'{BASE}/syn-1f-subject.json']),
                      'successor': pin(f'{UNIT}/successor.json', files[f'{UNIT}/successor.json']),
                      'overrides': len(json.loads(files[f'{UNIT}/successor.json'])['passageOverrides']),
                      'candidates': len(json.loads(files[f'{UNIT}/successor.json'])['candidates']),
                      'checked': args.check}))


if __name__ == '__main__':
    main()
