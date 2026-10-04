"""Read-only checks of contract successor B-S1. Run with python3 -I -B; it writes nothing.

1. successor.json: every override's before is the accepted parent line, parents are pinned, and
   candidates equal the subject members other than the record.
2. The two additions fragments: duplicate-free JSON; no key collides with its base bundle; every
   #/ reference resolves in the merged bundle; each V3 record equals its V2 record plus exactly the
   declared delta; the security and native pruned-tree rows mirror each other.
3. Sample instances (a no-member project, a two-member D15 workspace, and negatives) against the
   merged bundles, with a small closed-subset Draft 2020-12 validator (no third-party library).
4. The record carries no supersession: S9 is split into unit B-S9.
5. The reader registry's ids and reasons equal the schema enums; PASSAGES.md renders the record."""
import copy, hashlib, json, re
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s1/'


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


checks = {}
record = load(D + 'successor.json')
subject = load(B + 'b-s1-subject.json')

# 1. record shape -----------------------------------------------------------------------
for row in record['parents'] + record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert [r['path'] for r in record['parents']] == sorted({r['path'] for r in record['parents']})
members = {r['path'] for r in subject['files']}
assert {r['path'] for r in record['candidates']} == members - {D + 'successor.json'}
seen = set()
for o in record['passageOverrides']:
    assert set(o) == {'parent', 'selector', 'before', 'after'}
    key = (o['parent']['path'], o['selector']['line'])
    assert key not in seen
    seen.add(key)
    lines = raw(o['parent']['path']).decode('utf-8').splitlines()
    assert lines[o['selector']['line'] - 1] == o['before'], key
    assert o['after'] and o['after'] != o['before']
checks['overrides'] = len(record['passageOverrides'])

# 2. additions fragments ------------------------------------------------------------------
SLS = load('docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json')
NES = load('docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
sadd = load(D + 'schemas/security-lifecycle.schemas.v1.b-s1-additions.json')
nadd = load(D + 'schemas/native-evidence.schemas.v2.b-s1-additions.json')
assert sadd['base'] == pin('docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json')
assert nadd['base'] == pin('docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
assert not set(sadd['$defs']) & set(SLS['$defs']) and not set(sadd['schemas']) & set(SLS['schemas'])
assert not set(nadd['$defs']) & set(NES['$defs'])
SM = copy.deepcopy(SLS)
SM['$defs'].update(sadd['$defs'])
SM['schemas'].update(sadd['schemas'])
NM = copy.deepcopy(NES)
NM['$defs'].update(nadd['$defs'])


def resolve(bundle, ref):
    assert ref.startswith('#/'), ref
    node = bundle
    for tok in ref[2:].split('/'):
        node = node[tok.replace('~1', '/').replace('~0', '~')]
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


for bundle, frag in ((SM, sadd), (NM, nadd)):
    n = 0
    for ref in refs({k: frag[k] for k in ('$defs', 'schemas') if k in frag}):
        resolve(bundle, ref)
        n += 1
    checks.setdefault('refsResolved', 0)
    checks['refsResolved'] += n


def without(d, *keys):
    d = copy.deepcopy(d)
    for k in keys:
        d.pop(k, None)
    return d


# V3 = V2 + declared delta, record by record.
v2, v3 = SLS['schemas']['DiscoveryProvenanceV2'], sadd['schemas']['DiscoveryProvenanceV3']
new = ('memberRepositories', 'workspaceDeclarations', 'memberConfigs')
assert v3['required'] == v2['required'] + list(new)
p2, p3 = copy.deepcopy(v2['properties']), copy.deepcopy(v3['properties'])
for k in new:
    p3.pop(k)
assert p3.pop('schemaVersion') == {'const': 3} and p2.pop('schemaVersion') == {'const': 2}
assert p3['prunedTrees'].pop('items') == {'$ref': '#/$defs/PrunedTreeRowV3'}
assert p2['prunedTrees'].pop('items') == {'$ref': '#/$defs/PrunedTreeRowV2'}
assert p3['prunedTrees'].pop('description').startswith(p2['prunedTrees'].pop('description'))
assert p2 == p3 and without(v2, 'properties', 'required', 'description') == without(v3, 'properties', 'required', 'description')

r2, r3 = SLS['$defs']['PrunedTreeRowV2'], sadd['$defs']['PrunedTreeRowV3']
assert r3['properties']['reason']['enum'] == r2['properties']['reason']['enum'] + ['opensip-custody-state']
assert without(r2, 'description', 'properties') == without(r3, 'description', 'properties')
assert without(r2['properties'], 'reason') == without(r3['properties'], 'reason')

a2, a3 = SLS['schemas']['AdmittedBoundaryInventoryV2'], sadd['schemas']['AdmittedBoundaryInventoryV3']
assert a3['required'] == a2['required'] + ['memberRepositories']
q2, q3 = copy.deepcopy(a2['properties']), copy.deepcopy(a3['properties'])
q3.pop('memberRepositories')
assert q3.pop('schemaVersion') == {'const': 3} and q2.pop('schemaVersion') == {'const': 2}
assert q3['prunedTrees']['items']['properties']['reason'].pop('enum') == \
    q2['prunedTrees']['items']['properties']['reason'].pop('enum') + ['opensip-custody-state']
assert q2 == q3

res2, res3 = SLS['schemas']['DiscoveryResultV2'], sadd['schemas']['DiscoveryResultV3']
assert res3['oneOf'][0] == {**res2['oneOf'][0], 'properties': {**res2['oneOf'][0]['properties'],
                                                                'provenance': {'$ref': '#/schemas/DiscoveryProvenanceV3'}}}
rf2, rf3 = copy.deepcopy(res2['oneOf'][1]['properties']), copy.deepcopy(res3['oneOf'][1]['properties'])
assert rf3.pop('refusal')['enum'] == rf2.pop('refusal')['enum'] + ['PROJECT.SCOPE_LIMIT']
assert rf3.pop('provenance') == {'$ref': '#/schemas/DiscoveryProvenanceV3'} and rf2.pop('provenance')
assert rf3.pop('d9') == {'$ref': '#/$defs/DiscoveryD9V1'} and rf2.pop('d9') == {'$ref': '#/$defs/D9'}
assert rf2 == rf3
d9 = sadd['$defs']['DiscoveryD9V1']
assert d9['properties']['code']['enum'] == SLS['$defs']['D9']['properties']['code']['enum'] + ['REQUEST.UNSATISFIABLE']

n2, n3 = NES['$defs']['PrunedTreeV2'], nadd['$defs']['PrunedTreeV3']
assert without(n2, 'description', 'properties') == without(n3, 'description', 'properties')
assert n3['properties']['reason']['enum'] == r3['properties']['reason']['enum']
assert without(n3, 'description') == {**without(r3, 'description'), 'properties': {
    **r3['properties'], 'reason': {'type': 'string', **r3['properties']['reason']}}}, 'pruned-tree mirror'
na2, na3 = NES['$defs']['AdmittedBoundaryInventoryV2'], nadd['$defs']['AdmittedBoundaryInventoryV3']
assert na3['properties']['memberRepositories'] == a3['properties']['memberRepositories']
ub1, ub2 = NES['$defs']['UnitBoundariesV1'], nadd['$defs']['UnitBoundariesV2']
assert ub2['required'] == ub1['required'] + ['memberRepositories']
assert without(ub2['properties'], 'memberRepositories') == ub1['properties']
checks['v3Deltas'] = 'exact'

# 3. sample instances ---------------------------------------------------------------------


class Invalid(Exception):
    pass


def validate(bundle, schema, value, at='$'):
    if '$ref' in schema:
        validate(bundle, resolve(bundle, schema['$ref']), value, at)
    if 'oneOf' in schema:
        hits = 0
        for s in schema['oneOf']:
            try:
                validate(bundle, s, value, at)
                hits += 1
            except Invalid:
                pass
        if hits != 1:
            raise Invalid('%s oneOf matched %d' % (at, hits))
    t = schema.get('type')
    if t is not None:
        types = t if isinstance(t, list) else [t]
        ok = {'object': lambda v: isinstance(v, dict), 'array': lambda v: isinstance(v, list),
              'string': lambda v: isinstance(v, str), 'null': lambda v: v is None,
              'boolean': lambda v: isinstance(v, bool),
              'integer': lambda v: isinstance(v, int) and not isinstance(v, bool)}
        if not any(ok[x](value) for x in types):
            raise Invalid('%s type %s' % (at, t))
    if 'const' in schema and (value != schema['const'] or type(value) is not type(schema['const'])):
        raise Invalid('%s const' % at)
    if 'enum' in schema and not any(value == e and type(value) is type(e) for e in schema['enum']):
        raise Invalid('%s enum %r' % (at, value))
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', 1 << 62):
            raise Invalid('%s length' % at)
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise Invalid('%s pattern' % at)
    if isinstance(value, int) and not isinstance(value, bool):
        if value < schema.get('minimum', -(1 << 64)) or value > schema.get('maximum', 1 << 64):
            raise Invalid('%s range' % at)
    if isinstance(value, dict):
        for k in schema.get('required', []):
            if k not in value:
                raise Invalid('%s missing %s' % (at, k))
        props = schema.get('properties', {})
        for k, v in value.items():
            if k in props:
                validate(bundle, props[k], v, at + '.' + k)
            elif schema.get('additionalProperties') is False:
                raise Invalid('%s extra %s' % (at, k))
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', 1 << 62):
            raise Invalid('%s items count' % at)
        if schema.get('uniqueItems') and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            raise Invalid('%s unique' % at)
        for i, v in enumerate(value):
            if 'items' in schema:
                validate(bundle, schema['items'], v, '%s[%d]' % (at, i))
        order = schema.get('x-opensip-order')
        key = None
        if order == 'utf8':
            key = lambda v: v.encode('utf-8')
        elif order == 'path':
            key = lambda v: v['path'].encode('utf-8')
        elif isinstance(order, dict):
            key = lambda v: tuple(str(v[k]).encode('utf-8') for k in order['by'])
        if key is not None:
            ks = [key(v) for v in value]
            if any(a >= b for a, b in zip(ks, ks[1:])):
                raise Invalid('%s order %r' % (at, order))


def ok(bundle, schema, value):
    validate(bundle, schema, value)


def bad(bundle, schema, value, why):
    try:
        validate(bundle, schema, value)
    except Invalid:
        return
    raise AssertionError('accepted a negative sample: ' + why)


W = '/Users/u/ws'
H = '0' * 64
absent = lambda r: {'readerId': r, 'readerVersion': 1, 'state': 'absent', 'path': None, 'contentSha256': None,
                    'stateSubject': None, 'unresolved': []}
base_prov = {'schemaVersion': 3, 'mode': 'vcs-default', 'ci': True, 'selectedRoot': '/Users/u/repo',
             'configPath': None, 'walked': [], 'stopReason': 'VCS', 'custodyWaiver': None, 'authorizedGroupIds': [],
             'vcs': {'kind': 'directory', 'target': None, 'followed': False}, 'nestedRepositories': [],
             'nestedProjects': [], 'unitSource': 'automatic',
             'units': [{'path': '/Users/u/repo', 'kind': 'workspace-auto', 'markers': ['Cargo.toml']}],
             'excludedUnits': [],
             'prunedTrees': [{'path': '/Users/u/repo/.git', 'reason': 'vcs-tree', 'markerCount': None,
                              'markerCountBasis': 'not-enumerated'},
                             {'path': '/Users/u/repo/.opensip', 'reason': 'opensip-custody-state',
                              'markerCount': None, 'markerCountBasis': 'not-enumerated'}],
             'explicitPathWasSymlink': None, 'warnings': [], 'memberRepositories': [],
             'workspaceDeclarations': [absent('cargo-config-patch'), absent('npm-workspaces-members')],
             'memberConfigs': []}
PROV = SM['schemas']['DiscoveryProvenanceV3']
ok(SM, PROV, base_prov)
ws = copy.deepcopy(base_prov)
ws.update({'mode': 'cwd-default', 'selectedRoot': W, 'stopReason': 'HOME', 'vcs': None,
           'units': [{'path': W + '/serde', 'kind': 'workspace-auto', 'markers': ['Cargo.toml']},
                     {'path': W + '/serde-json', 'kind': 'workspace-auto', 'markers': ['Cargo.toml']}],
           'prunedTrees': [{'path': W + '/.opensip', 'reason': 'opensip-custody-state', 'markerCount': None,
                            'markerCountBasis': 'not-enumerated'},
                           {'path': W + '/serde-json/.git', 'reason': 'vcs-tree', 'markerCount': None,
                            'markerCountBasis': 'not-enumerated'},
                           {'path': W + '/serde/.git', 'reason': 'vcs-tree', 'markerCount': None,
                            'markerCountBasis': 'not-enumerated'}],
           'nestedRepositories': [W + '/scratch-clone'],
           'memberRepositories': [
               {'path': W + '/serde', 'declaredBy': [{'source': 'reader', 'readerId': 'cargo-config-patch',
                                                       'readerVersion': 1, 'path': W + '/.cargo/config.toml',
                                                       'contentSha256': H}]},
               {'path': W + '/serde-json', 'declaredBy': [{'source': 'reader', 'readerId': 'cargo-config-patch',
                                                            'readerVersion': 1, 'path': W + '/.cargo/config.toml',
                                                            'contentSha256': H}]}],
           'workspaceDeclarations': [
               {'readerId': 'cargo-config-patch', 'readerVersion': 1, 'state': 'read',
                'path': W + '/.cargo/config.toml', 'contentSha256': H, 'stateSubject': None,
                'unresolved': [{'entry': 'patch.crates-io.itoa', 'reason': 'patch-entry-not-path', 'subject': None},
                               {'entry': 'patch.crates-io.ryu', 'reason': 'member-excluded',
                                'subject': 'member-vcs-unsupported:core.worktree'}]},
               absent('npm-workspaces-members')],
           'memberConfigs': [W + '/serde/opensip.json']})
ok(SM, PROV, ws)
for why, mutate in [
        ('unknown pruned reason', lambda p: p['prunedTrees'][0].update(reason='opensip-state')),
        ('V2 version', lambda p: p.update(schemaVersion=2)),
        ('member-excluded without subject', lambda p: p['workspaceDeclarations'][0]['unresolved'][1].update(subject=None)),
        ('plain reason with subject', lambda p: p['workspaceDeclarations'][0]['unresolved'][0].update(subject='x')),
        ('unordered members', lambda p: p['memberRepositories'].reverse()),
        ('one reader row', lambda p: p['workspaceDeclarations'].pop()),
        ('refused with entries', lambda p: p['workspaceDeclarations'][0].update(state='refused', stateSubject='parse')),
        ('unknown reader', lambda p: p['workspaceDeclarations'][1].update(readerId='pnpm-workspace')),
        ('65 members', lambda p: p.update(memberRepositories=[
            {'path': '%s/m%03d' % (W, i), 'declaredBy': [{'source': 'config-workspace-roots', 'path': '%s/m%03d' % (W, i)}]}
            for i in range(65)]))]:
    p = copy.deepcopy(ws)
    mutate(p)
    bad(SM, PROV, p, why)
inv = {'schemaVersion': 3, 'source': 'security.discovery', 'selectedRoot': W, 'nestedRepositories': ['scratch-clone'],
       'nestedProjects': [], 'custodyExcludedUnits': [],
       'prunedTrees': [{'path': '.opensip', 'reason': 'opensip-custody-state', 'markerCount': None,
                        'markerCountBasis': 'not-enumerated'}],
       'memberRepositories': ['serde', 'serde-json']}
ok(SM, SM['schemas']['AdmittedBoundaryInventoryV3'], inv)
ok(NM, NM['$defs']['AdmittedBoundaryInventoryV3'], inv)
bad(NM, NM['$defs']['AdmittedBoundaryInventoryV3'], {**inv, 'memberRepositories': ['/abs']}, 'absolute member')
bad(SM, SM['schemas']['AdmittedBoundaryInventoryV3'], {**inv, 'memberRepositories': ['serde-json', 'serde']}, 'order')
refusal = {'status': 'REFUSE', 'refusal': 'PROJECT.SCOPE_LIMIT', 'path': W, 'detail': 'members:65>64',
           'd9': {'class': 'request-rejected', 'exit': 2, 'code': 'REQUEST.UNSATISFIABLE'}, 'provenance': ws}
ok(SM, SM['schemas']['DiscoveryResultV3'], refusal)
checks['samples'] = 'pass'

# 4. no supersession ---------------------------------------------------------------------
assert 'passageSupersessions' not in record and set(record) == {'schemaVersion', 'standing', 'parents',
                                                                 'passageOverrides', 'candidates'}
assert all('native_evidence_model' not in r['path'] for r in record['parents'])
checks['supersessions'] = 0

# 5. registry and rendering ---------------------------------------------------------------
reg = load(D + 'registry/workspace-declaration-readers.v1.json')
ids = [r['readerId'] for r in reg['readers']]
assert ids == sorted(ids) == sadd['$defs']['WorkspaceDeclarationV1']['oneOf'][0]['properties']['readerId']['enum']
assert all(r['readerVersion'] == 1 for r in reg['readers'])
reasons = [r['reason'] for r in reg['unresolvedReasons']]
u = sadd['$defs']['UnresolvedDeclarationEntryV1']['oneOf']
assert sorted(reasons) == sorted(u[0]['properties']['reason']['enum'] + u[1]['properties']['reason']['enum'])
assert {r['reason'] for r in reg['unresolvedReasons'] if r['subject'] != 'null'} == set(u[0]['properties']['reason']['enum'])
text = raw(D + 'PASSAGES.md').decode('utf-8')
for o in record['passageOverrides']:
    assert o['after'] in text and o['before'] in text
checks['registry'] = ids
print(json.dumps({'passed': True, **checks}, indent=1))
