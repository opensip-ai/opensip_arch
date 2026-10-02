"""Check EC1 without writing anything. Applies every passage override in memory, checks the
before text against the accepted parents, and checks the vector: the inventory body hashes to
manifestDigest, the two descriptors differ only by kind, both ids recompute from H, they differ,
the core id equals the product fixture's expected closure, and the evaluator descriptor fits the
identity closure schema's closed shape and kind list. Run with python3 -I -B, optionally giving
the product checkout to re-read the fixture."""
import hashlib, json, sys
from pathlib import Path
A = Path(__file__).resolve().parents[5]
D = A / 'docs/implementation/m2/core-evaluator-closure-ec1'
W = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def H(domain, x):
    c = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode() + b'\x00'
                          + len(c).to_bytes(8, 'big') + c).hexdigest()


def resolve(doc, pointer):
    for token in pointer[1:].split('/'):
        doc = doc[token.replace('~1', '/').replace('~0', '~')]
    return doc


def assign(doc, pointer, value):
    tokens = pointer[1:].split('/')
    for token in tokens[:-1]:
        doc = doc[token]
    doc[tokens[-1]] = value


record = json.loads((D / 'successor.json').read_bytes())
applied = {}
for o in record['passageOverrides']:
    p = o['parent']
    raw = (A / p['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == p['sha256'] and len(raw) == p['bytes'], p['path']
    if 'line' in o['selector']:
        lines = applied.setdefault(p['path'], raw.decode('utf-8').splitlines())
        assert lines[o['selector']['line'] - 1] == o['before'], o['selector']
        lines[o['selector']['line'] - 1] = o['after']
    else:
        doc = applied.setdefault(p['path'], json.loads(raw))
        assert resolve(doc, o['selector']['jsonPointer']) == o['before'], o['selector']
        assign(doc, o['selector']['jsonPointer'], o['after'])
    assert all(w in o['after'].split() for w in o['before'].split())  # inserts only
    assert 'EC1' in o['after'] and o['after'] != o['before']

schemas = applied['docs/coop/design-corrections/foundation/identity-schemas.v3.json']
closure = schemas['$defs']['closure']
v = json.loads((D / 'evidence/vector.json').read_bytes())
body = bytes.fromhex(v['inventoryBody']['hex'])
assert len(body) == v['inventoryBody']['bytes'] and hashlib.sha256(body).hexdigest() == v['inventoryBody']['sha256']
core, ev = v['coreDescriptor'], v['evaluatorDescriptor']
assert core['kind'] == 'core' and ev['kind'] == 'evaluator'
assert {k: x for k, x in core.items() if k != 'kind'} == {k: x for k, x in ev.items() if k != 'kind'}
assert core['manifestDigest'] == hashlib.sha256(body).hexdigest()
assert v['coreClosure'] == 'closure2:' + H('closure', core)
assert v['evaluatorClosure'] == 'closure2:' + H('closure', ev)
assert v['coreClosure'] != v['evaluatorClosure']
assert hashlib.sha256(C(core)).hexdigest() == v['coreDescriptorCanonicalSha256']
assert hashlib.sha256(C(ev)).hexdigest() == v['evaluatorDescriptorCanonicalSha256']
# The evaluator descriptor is an ordinary identity closure; the core one is not (kind core is
# security's projection, outside the identity kind list).
assert set(ev) == set(closure['required']) == set(closure['properties'])
assert ev['kind'] in closure['properties']['kind']['enum'] and 'core' not in closure['properties']['kind']['enum']
assert all(set(m) == {'path', 'sha256', 'bytes'} for m in ev['tree'])
assert [m['path'] for m in ev['tree']] == sorted(m['path'] for m in ev['tree'])
assert schemas['x-opensip-digest-domains']['closureKinds']['byField']['evaluation-seal.evaluatorClosure'] == 'evaluator'
if W is not None:
    fx = v['source']['fixture']
    raw = (W / fx['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == fx['sha256']
    case = [json.loads(l) for l in raw.decode('utf-8').splitlines() if json.loads(l)['label'] == v['source']['label']][0]
    assert case['expected']['descriptor'] == core and case['expected']['closure'] == v['coreClosure']
    assert bytes.fromhex(case['raw']) == body
    # Every accepted case of the fixture: the derivation changes only kind, and the ids differ.
    n = 0
    for line in raw.decode('utf-8').splitlines():
        q = json.loads(line)
        if q['expected'].get('ok') is True:
            d = q['expected']['descriptor']
            assert 'closure2:' + H('closure', d) == q['expected']['closure']
            assert 'closure2:' + H('closure', dict(d, kind='evaluator')) != q['expected']['closure']
            n += 1
    assert n == 53, n
print(json.dumps({'passed': True, 'overrides': len(record['passageOverrides']),
                  'coreClosure': v['coreClosure'], 'evaluatorClosure': v['evaluatorClosure'],
                  'fixtureCasesChecked': W is not None}))
