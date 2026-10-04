"""I1-a: materialize I1-L's two product schema copies and re-pin every selected
consumer of their bytes, in a product worktree at main 5e25d04.

Two phases, each refusing unless every value it changes still holds its base
value (the bytes at 5e25d04), so a rerun on a changed tree stops:

  pins      before generation
    - schemas/sources/identity-v3.schema.json and policy-v2.schema.json become
      I1-L's accepted copies byte for byte (materialization-map.json of I1-L);
    - schemas/source-map.json and schemas/admission-source-map.json re-point
      both rows' architectureSource to those copies;
    - schemas/admission-source-map.json's registryArchitectureSource names
      I1-a's own architecture copy of the admission registry
      (i1-a/schemas/admission-registry.json, frozen by freeze_i1a.py with the
      same bytes as the product file written here);
    - schemas/admission-registry.json: both source rows and the policy-v2
      alias row carry the new bytes and sha256;
    - tools/contracts/generator-closure.json: the identity-v3, policy-v2 and
      source-map.json rows; every other row and the toolchain are unchanged;
    - schemas/registry.json: both sourceSha256 values, the recipe's sorted
      sourceSha256s, and generatorClosureSha256;
    - crates/identity/src/schema_registry.rs: both SourcePin lengths and
      digests, in rustfmt's array layout;
    - crates/evaluator/src/atom-registry.json: fieldFilterSchema moves to
      I1-L's design policy-document copy (path, bytes, sha256);
      scannerIdentitySchema takes the product identity copy's bytes and
      sha256 (its fixturePath is kept).

  policies  after generation has written the outputs
    - tools/contracts/dependency-policy.json: every localSources row whose
      file changed (only generated outputs may change);
    - tools/identity/dependency-policy.json: src/schema_registry.rs.

Every JSON file round-trips through json.dumps(indent=2) plus a newline at
base, so no other byte moves. Usage: apply_i1a.py WORKTREE pins|policies"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
W = Path(sys.argv[1]).resolve(strict=True); PHASE = sys.argv[2]
L = 'docs/implementation/m3/preview-pack-i1/i1-l'
U = 'docs/implementation/m3/preview-pack-i1/i1-a'
BASE = '5e25d04'
def dig(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def apin(p): return {'path': p, **dig((A / p).read_bytes())}
def load(p):
    raw = (W / p).read_bytes(); v = json.loads(raw)
    assert (json.dumps(v, indent=2) + '\n').encode() == raw, 'round trip: ' + p
    return raw, v
def save(p, v): (W / p).write_bytes((json.dumps(v, indent=2) + '\n').encode())
def base(p): return subprocess.run(['git', '-C', str(W), 'show', f'{BASE}:{p}'], capture_output=True, check=True).stdout
def at_base(p): assert (W / p).read_bytes() == base(p), 'not at base: ' + p
report = {}
def record(p, before): report[p] = {'before': dig(before), 'after': dig((W / p).read_bytes())}

if PHASE == 'pins':
    PIDS = {'path': 'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json', 'bytes': 197480,
            'sha256': '311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f'}
    PPDS = {'path': 'docs/implementation/m1/source-selection-v2/schemas/sources/policy.v2.schema.json', 'bytes': 26534,
            'sha256': 'b221b5ed6f8e6e3ffbcfa65358c0fe26a2bc7909550c6e1bec44894f413c9b55'}
    PDS = {'path': 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json', 'bytes': 27863,
           'sha256': 'c8b0a907a7b8019be4c6ed5b1d217ac7689bbbba2873679c42b86499280a3595'}
    assert apin(PIDS['path']) == PIDS and apin(PPDS['path']) == PPDS and apin(PDS['path']) == PDS
    mapping = json.loads((A / L / 'materialization-map.json').read_bytes())
    copies = {row['productPath']: row for row in mapping['files']}
    assert set(copies) == {'schemas/sources/identity-v3.schema.json', 'schemas/sources/policy-v2.schema.json'}
    new = {}
    for product, old in (('schemas/sources/identity-v3.schema.json', PIDS), ('schemas/sources/policy-v2.schema.json', PPDS)):
        row = copies[product]
        before = (W / product).read_bytes(); at_base(product)
        assert dig(before) == {'bytes': old['bytes'], 'sha256': old['sha256']} == row['before'], product
        raw = (A / row['candidatePath']).read_bytes()
        assert dig(raw) == row['after'], product
        (W / product).write_bytes(raw); record(product, before)
        new[product] = {'path': row['candidatePath'], **dig(raw)}
    IDN, POL = new['schemas/sources/identity-v3.schema.json'], new['schemas/sources/policy-v2.schema.json']
    OLD = {'schemas/sources/identity-v3.schema.json': PIDS, 'schemas/sources/policy-v2.schema.json': PPDS}
    # The design policy-document copy differs from PDS only in Atom and AtomSuccessorV1
    # among its $defs; FieldFilter is unchanged, so the atom registry's
    # fieldFilterShapeEquality note stays true of the moved pin.
    DPDS = apin(L + '/design/workflows/schemas/policy-document.v2.schema.json')
    assert DPDS['bytes'] == 28042 and DPDS['sha256'].startswith('45581464')
    old_defs, new_defs = (json.loads((A / p).read_bytes())['$defs'] for p in (PDS['path'], DPDS['path']))
    assert set(old_defs) == set(new_defs) and sorted(k for k in old_defs if old_defs[k] != new_defs[k]) == ['Atom', 'AtomSuccessorV1']
    # Generation source map.
    p = 'schemas/source-map.json'; at_base(p); raw, sm = load(p); hit = []
    for row in sm['sources']:
        if row['implementationPath'] in OLD:
            old = OLD[row['implementationPath']]
            assert row['architectureSource'] == {'path': old['path'], 'sha256': old['sha256'], 'bytes': old['bytes']}
            target = new[row['implementationPath']]
            row['architectureSource'] = {'path': target['path'], 'sha256': target['sha256'], 'bytes': target['bytes']}; hit.append(row['implementationPath'])
    assert sorted(hit) == sorted(OLD); save(p, sm); record(p, raw)
    # Admission registry (product); its architecture copy is frozen with the same bytes.
    p = 'schemas/admission-registry.json'; at_base(p); raw, ar = load(p); hit = []
    for row in ar['sources'] + ar['aliases']:
        if row['sourcePath'] in OLD:
            old = OLD[row['sourcePath']]
            assert (row['bytes'], row['sha256']) == (old['bytes'], old['sha256'])
            row['bytes'], row['sha256'] = new[row['sourcePath']]['bytes'], new[row['sourcePath']]['sha256']; hit.append(row['sourcePath'])
    assert sorted(hit) == sorted(['schemas/sources/identity-v3.schema.json', 'schemas/sources/policy-v2.schema.json', 'schemas/sources/policy-v2.schema.json'])
    save(p, ar); record(p, raw)
    registry_copy = {'path': U + '/schemas/admission-registry.json', **dig((W / p).read_bytes())}
    # Admission source map.
    p = 'schemas/admission-source-map.json'; at_base(p); raw, am = load(p); hit = []
    assert am['registryArchitectureSource'] == {'path': 'docs/implementation/m2/existing-root-diagnostics-468a/schemas/admission-registry.json',
                                                'bytes': 17170, 'sha256': '595fc28d3ebf5442c6737e00c76729e83d5f707ca4e858a69b355a14761c5f11'}
    am['registryArchitectureSource'] = {'path': registry_copy['path'], 'bytes': registry_copy['bytes'], 'sha256': registry_copy['sha256']}
    for row in am['sources']:
        if row['implementationPath'] in OLD:
            old = OLD[row['implementationPath']]
            assert row['architectureSource'] == {'path': old['path'], 'sha256': old['sha256'], 'bytes': old['bytes']}
            target = new[row['implementationPath']]
            row['architectureSource'] = {'path': target['path'], 'sha256': target['sha256'], 'bytes': target['bytes']}; hit.append(row['implementationPath'])
    assert sorted(hit) == sorted(OLD); save(p, am); record(p, raw)
    # Generator closure: three rows.
    p = 'tools/contracts/generator-closure.json'; at_base(p); raw, cl = load(p); hit = []
    source_map_before = base('schemas/source-map.json')
    BEFORE = {**{k: (v['bytes'], v['sha256']) for k, v in OLD.items()},
              'schemas/source-map.json': (len(source_map_before), hashlib.sha256(source_map_before).hexdigest())}
    for row in cl['files']:
        if row['path'] in BEFORE:
            assert (row['bytes'], row['sha256']) == BEFORE[row['path']], row['path']
            d = dig((W / row['path']).read_bytes()); row['bytes'], row['sha256'] = d['bytes'], d['sha256']; hit.append(row['path'])
    assert sorted(hit) == sorted(BEFORE)
    for row in cl['files']:
        assert dig((W / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row['path']
    save(p, cl); record(p, raw)
    report[p]['rowsChanged'] = sorted(hit); report[p]['rows'] = len(cl['files'])
    closure_sha = hashlib.sha256((W / p).read_bytes()).hexdigest()
    # Generation registry.
    p = 'schemas/registry.json'; at_base(p); raw, reg = load(p); hit = []
    for row in reg['sources']:
        if row['sourcePath'] in OLD:
            assert row['sourceSha256'] == OLD[row['sourcePath']]['sha256']
            row['sourceSha256'] = new[row['sourcePath']]['sha256']; hit.append(row['sourcePath'])
    assert sorted(hit) == sorted(OLD) and len(reg['recipes']) == 1
    recipe = reg['recipes'][0]
    assert recipe['generatorClosureSha256'] == 'bb093a9c3cd78fb69917799309f2574b5145436a03138b0e3cb77926d4cd2120'
    assert recipe['sourceSha256s'] == sorted(recipe['sourceSha256s'])
    swap = {OLD[k]['sha256']: new[k]['sha256'] for k in OLD}
    assert sum(s in swap for s in recipe['sourceSha256s']) == 2
    recipe['sourceSha256s'] = sorted(swap.get(s, s) for s in recipe['sourceSha256s'])
    assert set(recipe['sourceSha256s']) == {r['sourceSha256'] for r in reg['sources']}
    recipe['generatorClosureSha256'] = closure_sha
    save(p, reg); record(p, raw)
    # Native source pins: rustfmt's layout for these arrays (12-space indent, lines
    # filled to 99 columns), checked against all 48 existing pins first.
    p = 'crates/identity/src/schema_registry.rs'; at_base(p); raw = (W / p).read_bytes(); text = raw.decode()
    def layout(nums):
        lines, cur = [], ' ' * 11
        for n in nums:
            tok = f' {n},'
            if len(cur) + len(tok) > 99:
                lines.append(cur); cur = ' ' * 11
            cur += tok
        return ''.join(line + '\n' for line in lines + [cur])
    arrays = re.compile(r'        sha256: \[\n((?:            [0-9, ]+\n)+)        \],\n')
    found = arrays.findall(text)
    assert len(found) == 48 and all(layout([int(x) for x in re.findall(r'\d+', body)]) == body for body in found)
    for product, old in OLD.items():
        target = new[product]
        def block(b, s): return (f'        path: "{product}",\n        bytes: {b},\n        sha256: [\n'
                                 + layout(list(bytes.fromhex(s))) + '        ],\n')
        before_block = block(old['bytes'], old['sha256'])
        assert text.count(before_block) == 1, product
        text = text.replace(before_block, block(target['bytes'], target['sha256']))
    (W / p).write_bytes(text.encode()); record(p, raw)
    # Atom registry pins.
    p = 'crates/evaluator/src/atom-registry.json'; at_base(p); raw, at = load(p)
    assert at['fieldFilterSchema'] == PDS
    at['fieldFilterSchema'] = {'path': DPDS['path'], 'bytes': DPDS['bytes'], 'sha256': DPDS['sha256']}
    scanner = at['scannerIdentitySchema']
    assert scanner == {'bytes': PIDS['bytes'], 'sha256': PIDS['sha256'],
                       'fixturePath': 'reference/archroot/docs/coop/design-corrections/foundation/identity-schemas.v3.json'}
    scanner['bytes'], scanner['sha256'] = IDN['bytes'], IDN['sha256']
    save(p, at); record(p, raw)
    report['admissionRegistryArchitectureCopy'] = registry_copy
elif PHASE == 'policies':
    p = 'tools/contracts/dependency-policy.json'; at_base(p); raw, dp = load(p); hit = []
    root = W / 'crates/contracts'
    for row in dp['localSources']:
        old = base('crates/contracts/' + row['path'])
        assert (row['bytes'], row['sha256']) == (len(old), hashlib.sha256(old).hexdigest()), row['path']
        now = (root / row['path']).read_bytes()
        if now != old:
            assert row['path'].startswith('src/generated/'), 'only generated contracts sources may change: ' + row['path']
            d = dig(now); row['bytes'], row['sha256'] = d['bytes'], d['sha256']; hit.append(row['path'])
    assert hit, 'no generated contracts source changed'
    save(p, dp); record(p, raw); report[p]['rowsChanged'] = sorted(hit)
    p = 'tools/identity/dependency-policy.json'; at_base(p); raw, ip = load(p); hit = []
    for row in ip['localSources']:
        old = base('crates/identity/' + row['path'])
        assert (row['bytes'], row['sha256']) == (len(old), hashlib.sha256(old).hexdigest()), row['path']
        now = (W / 'crates/identity' / row['path']).read_bytes()
        if now != old:
            d = dig(now); row['bytes'], row['sha256'] = d['bytes'], d['sha256']; hit.append(row['path'])
    assert hit == ['src/schema_registry.rs'], hit
    save(p, ip); record(p, raw); report[p]['rowsChanged'] = hit
else:
    raise SystemExit('usage: apply_i1a.py WORKTREE pins|policies')
print(json.dumps(report, indent=2))
