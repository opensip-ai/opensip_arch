"""Deterministically build exact FX-CAP-1 subjects from the pinned product lock.

No acceptance is manufactured. --check compares bytes without writing. Only this
package is written; accepted parents, product sources and design-lock stay inert.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ARCH = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = 'docs/implementation/fallow-expansion/capacity-r1/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'
COMMON = 'docs/coop/design-corrections/workflows/schemas/common.schema.json'
COMMON3 = 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json'
EXCEPTION = (' A third narrowly scoped reviewed exception (FX-CAP-1): '
             'analysis-spec.requestedCapabilities.maxItems increases from 1024 to 11264; '
             'plan.nativeContextDigests.maxItems increases from 128 to 1024; '
             'CapabilityAvailabilityStepV1.notices.maxItems increases from 1024 to 11264 '
             'in both workflow common schema versions. Existing majors, fields, domains, '
             'preimages, meanings and authority are retained. Every earlier admitted '
             'record preserves its exact bytes, identity and replay result; older readers '
             'may refuse the larger sets and never truncate or reinterpret them. No directly '
             'registered payload-schema document changes, so no historical payload reader '
             'row is added; retained schema dependency closures remain exact. All other '
             'schema/domain changes and HSR reader-extension rules retain their prior law.')


def raw(path):
    return (ARCH / path).read_bytes()


def pin(path, value=None):
    value = raw(path) if value is None else value
    return {'path': path, 'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}


def pointer(document, selector):
    for token in selector.strip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        document = document[int(token)] if isinstance(document, list) else document[token]
    return document


def replace_pointer(document, selector, value):
    pieces = selector.rsplit('/', 1)
    parent = pointer(document, pieces[0])
    parent[pieces[1].replace('~1', '/').replace('~0', '~')] = value


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def build(lock_path):
    lock = json.loads(lock_path.read_bytes())
    accepted = {}
    for key in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(raw(lock['approvals'][key]['path']))['files']:
            accepted[row['path']] = row
    meanings = {}
    for binding in lock['contractSuccessors']:
        record = json.loads(raw(binding['record']['path']))
        for row in record['candidates']:
            accepted[row['path']] = row
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
            meanings[key] = (binding['record'], entry)
    parents = [pin(path) for path in (NE, IE, WS, IDS, COMMON, COMMON3)]
    for row in parents:
        assert accepted[row['path']]['sha256'] == row['sha256'], row['path']
    overrides, supersessions = [], []

    def change(path, selector, after):
        key = (path, json.dumps(selector, sort_keys=True))
        before = (raw(path).decode().splitlines()[selector['line'] - 1]
                  if 'line' in selector else str(pointer(json.loads(raw(path)), selector['jsonPointer'])))
        item = {'parent': pin(path), 'selector': selector, 'before': before, 'after': after}
        if key in meanings:
            owner, entry = meanings[key]
            item['before'] = entry['after']
            item['supersedes'] = {'record': owner, 'parent': pin(path), 'selector': selector}
            supersessions.append(item)
        else:
            overrides.append(item)

    def effective(path, selector):
        key = (path, json.dumps(selector, sort_keys=True))
        if key in meanings:
            return meanings[key][1]['after']
        if 'line' in selector:
            return raw(path).decode().splitlines()[selector['line'] - 1]
        return str(pointer(json.loads(raw(path)), selector['jsonPointer']))

    for path, selector, old, new in [
        (IDS, '/$defs/analysis-spec/properties/requestedCapabilities/maxItems', 1024, 11264),
        (IDS, '/$defs/plan/properties/nativeContextDigests/maxItems', 128, 1024),
        (COMMON, '/$defs/CapabilityAvailabilityStepV1/properties/notices/maxItems', 1024, 11264),
        (COMMON3, '/$defs/CapabilityAvailabilityStepV1/properties/notices/maxItems', 1024, 11264),
    ]:
        assert effective(path, {'jsonPointer': selector}) == str(old)
        change(path, {'jsonPointer': selector}, str(new))
    change(IE, {'line': 214}, effective(IE, {'line': 214}) + EXCEPTION)
    selector = {'jsonPointer': '/x-opensip-evaluator-profile/majorLaw'}
    change(IDS, selector, effective(IDS, selector) + EXCEPTION)

    for line in (1115, 1117, 1119):
        before = effective(NE, {'line': line})
        assert '1024' in before
        change(NE, {'line': line}, before.replace('1024', '11264'))
    for line in (1317,):
        before = effective(WS, {'line': line})
        change(WS, {'line': line}, before.replace('1024', '11264'))
    before = effective(NE, {'line': 3534})
    old = '(1024, which the matrix-fixed default exceeds from94 TypeScript units)'
    assert old in before
    change(NE, {'line': 3534}, before.replace(old, '(11264 under FX-CAP-1; all other bounded-selection fields keep their own limits)'))
    before = effective(NE, {'line': 4276})
    start = before.index('The **analysis-spec** array')
    end = before.index('The public code is shared', start)
    paragraph = ('The **analysis-spec** array `requestedCapabilities` has limit11264 '
                 '(contract successor FX-CAP-1). The current selected matrix requests11 '
                 'capabilities per TypeScript unit and10 per Rust unit, so1024 all-TypeScript '
                 'selected language program units require11264 rows and fit the cardinality '
                 'bound. Colocated TypeScript and Rust units count separately for this sizing '
                 'target while workspaceRoots still deduplicates their root. This raises no '
                 'root, file, path, record-byte, frame, stage, dependency or work bound and '
                 'does not guarantee that every1024-unit input fits those independent bounds. '
                 'There is no new1024-unit admission ceiling. A matrix expansion reassesses '
                 'this target by a reviewed successor; it does not silently raise this constant. ')
    after = before[:start] + paragraph + before[end:]
    after = after.replace('`nativeContextDigests` has limit128', '`nativeContextDigests` has limit1024 (FX-CAP-1)')
    old = ('far below its own1024 while129 units whose compiler closure, standard library and effective '
           'options differ pass the workspace bound and cannot be expressed in the Plan')
    new = ('far below its own11264 while1025 distinct admitted contexts cannot be expressed in the Plan, '
           'including when colocated language units share selected workspace roots; identical full '
           'context descriptors still deduplicate')
    assert old in after
    after = after.replace(old, new)
    change(NE, {'line': 4276}, after)
    before = effective(NE, {'line': 4280})
    old = 'any of those would be a new product capability and none is selected here.'
    new = ('those require their own selection. FX-CAP-1 selects only the two coordinated '
           'identity array maxima and both per-step notice maxima; sharding and extra '
           'invocation steps remain unselected.')
    assert old in before
    change(NE, {'line': 4280}, before.replace(old, new))

    outputs = {}
    for path, name in [(IDS, 'identity-schemas.v3.json'), (COMMON, 'common.schema.json'),
                       (COMMON3, 'evaluator3-common.schema.json')]:
        document = json.loads(raw(path))
        # Carry previously selected annotations before applying this successor.
        for (parent, encoded_selector), (_, entry) in meanings.items():
            selector = json.loads(encoded_selector)
            if parent == path and 'jsonPointer' in selector:
                old = pointer(document, selector['jsonPointer'])
                value = json.loads(entry['after']) if not isinstance(old, str) else entry['after']
                replace_pointer(document, selector['jsonPointer'], value)
        for entry in overrides + supersessions:
            if entry['parent']['path'] == path and 'jsonPointer' in entry['selector']:
                selector = entry['selector']['jsonPointer']
                old = pointer(document, selector)
                replace_pointer(document, selector, entry['after'] if isinstance(old, str) else json.loads(entry['after']))
        outputs[BASE + 'schemas/' + name] = encoded(document)
    passages = '# FX-CAP-1 exact passages\n\n'
    for entry in overrides + supersessions:
        passages += '## ' + entry['parent']['path'] + ' ' + json.dumps(entry['selector']) + '\n\n'
        passages += 'Before:\n~~~text\n' + entry['before'] + '\n~~~\nAfter:\n~~~text\n' + entry['after'] + '\n~~~\n\n'
    outputs[BASE + 'PASSAGES.md'] = passages.encode()
    candidates = [pin(BASE + name) for name in ['CONTRACT.md', 'build.py', 'cases.json']]
    candidates += [pin('docs/implementation/fallow-expansion/evidence/' + name)
                   for name in ['capacity-shapes.json', 'capacity_shape_spike.py']]
    candidates += [pin(path, value) for path, value in sorted(outputs.items())]
    record = {'schemaVersion': 1, 'standing': 'PROPOSED FX-CAP-1: exact coordinated cardinality expansion, same-major bounded exception; requires independent acceptance and root assent',
              'parents': parents, 'passageOverrides': overrides, 'passageSupersessions': supersessions,
              'candidates': sorted(candidates, key=lambda p: p['path'])}
    outputs[BASE + 'successor.json'] = encoded(record)
    subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(BASE + 'successor.json', outputs[BASE + 'successor.json'])], key=lambda p: p['path'])}
    outputs[BASE + 'subject.json'] = encoded(subject)
    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lock', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip-fx-design/design-lock.json'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, value in build(args.lock).items():
        target = ARCH / path
        if args.check:
            assert target.read_bytes() == value, path
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(value)
    print('FX-CAP-1 deterministic subject checked' if args.check else 'FX-CAP-1 proposed subject built')
