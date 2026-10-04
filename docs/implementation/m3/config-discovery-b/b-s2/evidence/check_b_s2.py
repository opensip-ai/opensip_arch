"""Read-only checks of contract successor B-S2. Run with python3 -I -B; it writes nothing.

1. successor.json: each override's before is the accepted IE line, lines 543 to 546 are untouched
   (left to M3-C's VCS-1), and candidates equal the subject members other than the record.
2. The fragment: vcs-observation-v2 equals the accepted bundle's vcs-observation and the product
   copy's; every #/ reference resolves in the merged bundle; the record name and the snapshot's
   vcsDigest selector are unchanged.
3. Samples against the merged bundle with a small closed-subset validator: schema-2 records (none,
   git) admit exactly as before; schema-3 records admit; negatives refuse. Prints canonical-byte
   vectors (identity section 3 canonical JSON) and their SHA-256 for C1b to pin."""
import copy, hashlib, json, re
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s2/'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDS = 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'
COPY = 'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json'


def raw(p):
    return (A / p).read_bytes()


def load(p):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out, (p, k)
            out[k] = v
        return out
    return json.loads(raw(p), object_pairs_hook=unique)


def pin(p):
    b = raw(p)
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


record = load(D + 'successor.json')
subject = load(B + 'b-s2-subject.json')
for row in record['parents'] + record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}
lines = raw(IE).decode('utf-8').splitlines()
assert [o['selector']['line'] for o in record['passageOverrides']] == [542, 547]
for o in record['passageOverrides']:
    assert lines[o['selector']['line'] - 1] == o['before'] and o['after'] and o['after'] != o['before']
assert not any(543 <= o['selector']['line'] <= 546 for o in record['passageOverrides'])

ids, prod = load(IDS), load(COPY)
frag = load(D + 'schemas/identity-schemas.v3.b-s2-additions.json')
assert frag['base'] == pin(IDS) and frag['alsoAppliesTo'] == [pin(COPY)]
assert frag['$defs']['vcs-observation-v2'] == ids['$defs']['vcs-observation'] == prod['$defs']['vcs-observation']
assert set(frag['$defs']) & set(ids['$defs']) == {'vcs-observation'}
assert ids['$defs']['snapshot']['properties']['vcsDigest']['x-opensip-digest']['record']['selector'] == '#/$defs/vcs-observation'
M = copy.deepcopy(ids)
M['$defs'].update(frag['$defs'])


def resolve(ref):
    assert ref.startswith('#/'), ref
    node = M
    for tok in ref[2:].split('/'):
        node = node[tok]
    return node


def refs(node):
    if isinstance(node, dict):
        if '$ref' in node:
            yield node['$ref']
        for v in node.values():
            yield from refs(v)
    elif isinstance(node, list):
        for v in node:
            yield from refs(v)


n = 0
for r in refs(frag['$defs']):
    resolve(r)
    n += 1


class Invalid(Exception):
    pass


def validate(schema, value, at='$'):
    if '$ref' in schema:
        validate(resolve(schema['$ref']), value, at)
    if 'oneOf' in schema:
        hits = 0
        for s in schema['oneOf']:
            try:
                validate(s, value, at)
                hits += 1
            except Invalid:
                pass
        if hits != 1:
            raise Invalid('%s oneOf %d' % (at, hits))
    if 'not' in schema:
        try:
            validate(schema['not'], value, at)
        except Invalid:
            pass
        else:
            raise Invalid('%s not' % at)
    t = schema.get('type')
    if t is not None:
        ok = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
        if t == 'null':
            if value is not None:
                raise Invalid('%s null' % at)
        elif not isinstance(value, ok[t]):
            raise Invalid('%s type' % at)
    if 'const' in schema and (value != schema['const'] or type(value) is not type(schema['const'])):
        raise Invalid('%s const' % at)
    if 'enum' in schema and value not in schema['enum']:
        raise Invalid('%s enum' % at)
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', 1 << 62):
            raise Invalid('%s length' % at)
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise Invalid('%s pattern' % at)
    if isinstance(value, dict):
        for k in schema.get('required', []):
            if k not in value:
                raise Invalid('%s missing %s' % (at, k))
        for k, v in value.items():
            if k in schema.get('properties', {}):
                validate(schema['properties'][k], v, at + '.' + k)
            elif schema.get('additionalProperties') is False:
                raise Invalid('%s extra %s' % (at, k))
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', 1 << 62):
            raise Invalid('%s count' % at)
        for i, v in enumerate(value):
            validate(schema['items'], v, '%s[%d]' % (at, i))
        if schema.get('x-opensip-order') == 'path':
            ks = [v['path'].encode('utf-8') for v in value]
            if any(a >= b for a, b in zip(ks, ks[1:])):
                raise Invalid('%s order' % at)


OBS = {'$ref': '#/$defs/vcs-observation'}
OLD = ids['$defs']['vcs-observation']


def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


INV = hashlib.sha256(b'[]').hexdigest()
v2_none = {'schemaVersion': 2, 'kind': 'none', 'commitId': None, 'dirty': False, 'sourceInventoryDigest': INV}
v2_git = {'schemaVersion': 2, 'kind': 'git', 'commitId': 'a' * 40, 'dirty': True, 'sourceInventoryDigest': INV}
for v in (v2_none, v2_git):
    validate(OBS, v)
    validate(OLD, v)  # the same record admits under the accepted schema 2
v3 = {'schemaVersion': 3, 'kind': 'none', 'commitId': None, 'dirty': False, 'sourceInventoryDigest': INV,
      'members': [{'path': 'serde', 'kind': 'git', 'commitId': '0123456789abcdef0123456789abcdef01234567', 'dirty': True},
                  {'path': 'serde-json', 'kind': 'git', 'commitId': 'fedcba9876543210fedcba9876543210fedcba98', 'dirty': True}]}
validate(OBS, v3)
negatives = {
    'schema 3 under the accepted schema': (OLD, v3),
    'top-level git': (OBS, {**v3, 'kind': 'git', 'commitId': 'a' * 40}),
    'top-level dirty': (OBS, {**v3, 'dirty': True}),
    'no members': (OBS, {**v3, 'members': []}),
    'members on schema 2': (OBS, {**v2_none, 'members': v3['members']}),
    'schema 3 without members': (OBS, {k: v for k, v in v3.items() if k != 'members'}),
    'unordered members': (OBS, {**v3, 'members': list(reversed(v3['members']))}),
    'uppercase commit': (OBS, {**v3, 'members': [{**v3['members'][0], 'commitId': 'A' * 40}]}),
    'sha256 commit': (OBS, {**v3, 'members': [{**v3['members'][0], 'commitId': 'a' * 64}]}),
    'hg member': (OBS, {**v3, 'members': [{**v3['members'][0], 'kind': 'hg'}]}),
    'absolute member path': (OBS, {**v3, 'members': [{**v3['members'][0], 'path': '/serde'}]}),
    'dot-dot member path': (OBS, {**v3, 'members': [{**v3['members'][0], 'path': '../serde'}]}),
    '65 members': (OBS, {**v3, 'members': [{'path': 'm%03d' % i, 'kind': 'git', 'commitId': 'a' * 40, 'dirty': True}
                                           for i in range(65)]}),
}
for why, (schema, value) in negatives.items():
    try:
        validate(schema, value)
    except Invalid:
        continue
    raise AssertionError('accepted: ' + why)
vectors = {name: {'canonical': canonical(v).decode('utf-8'), 'sha256': hashlib.sha256(canonical(v)).hexdigest()}
           for name, v in (('schema2-none', v2_none), ('schema2-git', v2_git), ('schema3-two-members', v3))}
print(json.dumps({'passed': True, 'overrides': [542, 547], 'refsResolved': n, 'schema2Unchanged': True,
                  'negativesRefused': len(negatives), 'vectors': vectors}, indent=1))
