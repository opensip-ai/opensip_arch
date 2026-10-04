"""Check CRC-1 without writing anything.

Usage: check_crc_1.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and cd5958b; both read only, through `git show`).

It re-derives, independently of build_crc_1.py:
1. every parent pin against the arch bytes, and every parent as accepted in the product lock;
2. every `before` against its parent (line selectors on text parents only, JSON Pointers on JSON
   parents), that no selector is already bound in the lock, and that every `after` only inserts;
3. the overridden identity schema copy: only the three named strings change, the closure kind list
   and `closureKinds.byField` are unchanged, and the kinds each core role closure needs exist;
4. that the IE paragraph names every field and condition of law M3-C r7 item 9 (r6's X-C1), and
   (r2, GROK2 RF-1) that its three statements of `semanticClosures` membership (IE:285, IE:1377,
   the IDS-L selectionLaw) say the same thing: never selected otherwise, not even explicitly;
5. the vector: body digest, the five descriptors differing only by kind, every id and canonical
   digest recomputed, each descriptor fitting the identity closure's closed shape; EC1's two
   values; and, from the product fixture, all 53 accepted cases;
6. that the README states every changed passage by path and selector.
Run with python3 -I -B at nice -n 19.
"""
import copy, difflib, hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
D = A / 'docs/implementation/m3/snapshot-plan-c/crc-1'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', 'cd5958b')
IDS = 'docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def H(domain, x):
    c = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode() + b'\x00'
                          + len(c).to_bytes(8, 'big') + c).hexdigest()


def tokens(pointer):
    return [t.replace('~1', '/').replace('~0', '~') for t in pointer[1:].split('/')]


def resolve(doc, pointer):
    for t in tokens(pointer):
        doc = doc[t]
    return doc


def assign(doc, pointer, value):
    ts = tokens(pointer)
    for t in ts[:-1]:
        doc = doc[t]
    doc[ts[-1]] = value


record = json.loads((D / 'successor.json').read_bytes())
lock = json.loads(show('design-lock.json'))
accepted, bound = {}, set()
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads((A / lock['approvals'][key]['path']).read_bytes())['files']:
        accepted[row['path']] = row
for b in lock['contractSuccessors']:
    rec = json.loads((A / b['record']['path']).read_bytes())
    for row in rec['candidates'] + [b['record']]:
        accepted[row['path']] = row
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        bound.add((e['parent']['path'], json.dumps(e['selector'], sort_keys=True)))

# 1-2. Parents, befores, selectors, inserts.
parents = {p['path']: p for p in record['parents']}
assert [p['path'] for p in record['parents']] == sorted(parents)
docs, texts = {}, {}
for path, p in parents.items():
    raw = (A / path).read_bytes()
    assert len(raw) == p['bytes'] and hashlib.sha256(raw).hexdigest() == p['sha256'], path
    assert {k: accepted[path][k] for k in ('sha256', 'bytes')} == {'sha256': p['sha256'], 'bytes': p['bytes']}, path
    try:
        docs[path] = json.loads(raw)
    except ValueError:
        texts[path] = raw.decode('utf-8').splitlines()
original = {path: copy.deepcopy(doc) for path, doc in docs.items()}
seen = set()
for o in record['passageOverrides']:
    path, sel = o['parent']['path'], o['selector']
    assert parents[path] == o['parent']
    key = (path, json.dumps(sel, sort_keys=True))
    assert key not in seen and key not in bound, key
    seen.add(key)
    if path in texts:
        assert set(sel) == {'line'}
        assert texts[path][sel['line'] - 1] == o['before'], key
        texts[path][sel['line'] - 1] = o['after']
    else:
        assert set(sel) == {'jsonPointer'}
        assert resolve(docs[path], sel['jsonPointer']) == o['before'], key
        assign(docs[path], sel['jsonPointer'], o['after'])
    ops = difflib.SequenceMatcher(None, o['before'], o['after'], autojunk=False).get_opcodes()
    assert all(tag in ('equal', 'insert') for tag, *_ in ops) and o['before'] != o['after'], key
    assert 'CRC-1' in o['after'], key
for row in record['candidates']:
    raw = (A / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
    assert row['path'] not in accepted, row['path']

# 3. The identity schema copy.
POINTERS = {'/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact',
            '/x-opensip-digest-domains/closureKinds/note',
            '/x-opensip-digest-domains/closureMembership/selectionLaw'}
before_ids, after_ids = original[IDS], docs[IDS]
masked = [copy.deepcopy(before_ids), copy.deepcopy(after_ids)]
for doc in masked:
    for p in POINTERS:
        assign(doc, p, None)
assert masked[0] == masked[1], 'the identity copy changes more than the three strings'
closure = after_ids['$defs']['closure']
kinds = closure['properties']['kind']['enum']
assert {'evaluator', 'detector', 'provider', 'adapter'} <= set(kinds) and 'core' not in kinds
by_field = after_ids['x-opensip-digest-domains']['closureKinds']['byField']
assert by_field == before_ids['x-opensip-digest-domains']['closureKinds']['byField']
assert by_field['finding.ruleClosure'] == 'detector' and by_field['import.adapterClosure'] == 'adapter'
PROVIDER_FIELDS = ['subject-scope.enumeratorClosure', 'view.producerClosure', 'fact.producerClosure',
                   'stage-spec.producerClosure', 'import.producerClosure', 'cache-key.producerClosure']
assert all(by_field[f] == 'provider' for f in PROVIDER_FIELDS)

# 4. The IE paragraph carries item 9's whole rule.
ie285 = [o for o in record['passageOverrides'] if o['parent']['path'] == IE and o['selector'] == {'line': 285}][0]['after']
for needle in ['core detector closure', 'core provider closure', 'core adapter closure', 'TR-CORE-signed core inventory body',
               'exactly two admitted uses', 'import.producerClosure', 'import.adapterClosure', '`dependency`',
               '`prepared`', 'native.semantic-universe.syntax.v2', 'subject-scope.enumeratorClosure',
               'view.producerClosure', 'fact.producerClosure', 'stage-spec.producerClosure', 'enumerator.closureId',
               'CandidateProducerResultV1.producerClosure', 'exactly when the Plan selects a syntax universe',
               'never the producer of a TypeScript or Rust record', 'detectorClosure', 'finding.ruleClosure',
               'contributions', 'cache-key.producerClosure', 'EC1', 'CR-1', 'kind `grammar`']:
    assert needle in ie285, needle
# RF-1 (r2): the three membership statements agree, and none grants explicit selection.
afters = {(o['parent']['path'], json.dumps(o['selector'], sort_keys=True)): o['after'] for o in record['passageOverrides']}
SELECTION = '{"jsonPointer": "/x-opensip-digest-domains/closureMembership/selectionLaw"}'
for key in [(IE, '{"line": 285}'), (IE, '{"line": 1377}'), (IDS, SELECTION)]:
    assert 'exactly when the Plan selects' in afters[key], key
    assert 'is never selected otherwise, not even explicitly' in afters[key], key
    assert 'adapter closure is never a' in afters[key] or 'It is never a `plan.semanticClosures` member' in afters[key], key
assert not any('explicitly included' in a for a in afters.values())

# 5. The vector.
v = json.loads((D / 'evidence/vector.json').read_bytes())
body = bytes.fromhex(v['inventoryBody']['hex'])
assert len(body) == v['inventoryBody']['bytes'] and hashlib.sha256(body).hexdigest() == v['inventoryBody']['sha256']
core = v['coreDescriptor']
assert core['kind'] == 'core' and core['manifestDigest'] == hashlib.sha256(body).hexdigest()
assert [c['kind'] for c in v['closures']] == ['core', 'evaluator', 'detector', 'provider', 'adapter']
for c in v['closures']:
    d = dict(core, kind=c['kind'])
    assert c['closure'] == 'closure2:' + H('closure', d)
    assert c['descriptorCanonicalSha256'] == hashlib.sha256(C(d)).hexdigest()
    if c['kind'] != 'core':
        assert set(d) == set(closure['required']) == set(closure['properties']) and d['kind'] in kinds
assert len({c['closure'] for c in v['closures']}) == 5
assert all(set(m) == {'path', 'sha256', 'bytes'} for m in core['tree'])
assert [m['path'] for m in core['tree']] == sorted(m['path'] for m in core['tree'])
ec1 = json.loads((A / v['source']['ec1Vector']['path']).read_bytes())
assert hashlib.sha256((A / v['source']['ec1Vector']['path']).read_bytes()).hexdigest() == v['source']['ec1Vector']['sha256']
assert ec1['coreClosure'] == v['closures'][0]['closure'] and ec1['evaluatorClosure'] == v['closures'][1]['closure']
fx = v['source']['fixture']
raw = show(fx['path'])
assert hashlib.sha256(raw).hexdigest() == fx['sha256'] and len(raw) == fx['bytes']
n = 0
for line in raw.decode('utf-8').splitlines():
    q = json.loads(line)
    if q['label'] == v['source']['label']:
        assert q['expected']['descriptor'] == core and bytes.fromhex(q['raw']) == body
        assert q['expected']['closure'] == v['closures'][0]['closure']
    if q['expected'].get('ok') is True:
        d = q['expected']['descriptor']
        assert 'closure2:' + H('closure', d) == q['expected']['closure']
        assert len({H('closure', dict(d, kind=k)) for k in ('core', 'evaluator', 'detector', 'provider', 'adapter')}) == 5
        n += 1
assert n == v['fixtureCases']['accepted'] == 53

# 6. The README states every changed passage.
readme = (D / 'README.md').read_text(encoding='utf-8')
for o in record['passageOverrides']:
    sel = o['selector']
    assert o['parent']['path'] in readme, o['parent']['path']
    assert (('| %d |' % sel['line']) if 'line' in sel else ('`%s`' % sel['jsonPointer'])) in readme, sel
print(json.dumps({'passed': True, 'rev': REV, 'overrides': len(record['passageOverrides']),
                  'parents': len(parents), 'boundAtRev': len(lock['contractSuccessors']),
                  'closures': {c['kind']: c['closure'] for c in v['closures']}, 'fixtureCases': n}, indent=1))
