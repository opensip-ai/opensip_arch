"""F8b step 4: install rebuild-02's observed receipt and re-pin the selected registries.

Refuses unless every changed value still holds its base (3e64266) value. Changes:
- tools/contracts/build-receipt.json: replaced byte for byte by rebuild-02's receipt.json;
- tools/contracts/toolchain.json: executables.generator and standing;
- tools/contracts/generator-closure.json: five files rows and toolchain.generator;
- schemas/registry.json: recipes[0].generatorClosureSha256 only;
- tools/typescript-lanes.json: two files rows.
All four JSON files round-trip through json.dumps(indent=2) + newline at base, so no other
byte moves. Afterwards every closure and lane row is checked against the worktree."""
import hashlib, json, sys
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True); R2 = Path(sys.argv[2]).resolve(strict=True)
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def load(p):
    raw = (W / p).read_bytes(); v = json.loads(raw)
    assert (json.dumps(v, indent=2) + '\n').encode() == raw, 'round trip: ' + p
    return raw, v
def save(p, v): (W / p).write_bytes((json.dumps(v, indent=2) + '\n').encode())
report = {}
# Receipt.
old = (W / 'tools/contracts/build-receipt.json').read_bytes()
assert pin(old)['sha256'] == 'c434cbd3e9fc24d5056aaf43b465a4024b85bb576f8b7c20b336d4466400898d'
receipt_raw = (R2 / 'receipt.json').read_bytes(); receipt = json.loads(receipt_raw)
exe = (R2 / 'opensip-contract-generator').read_bytes()
assert receipt['executable'] == {'sha256': hashlib.sha256(exe).hexdigest(), 'bytes': len(exe)}
(W / 'tools/contracts/build-receipt.json').write_bytes(receipt_raw)
report['tools/contracts/build-receipt.json'] = {'before': pin(old), 'after': pin(receipt_raw)}
# Toolchain.
raw, tc = load('tools/contracts/toolchain.json')
assert pin(raw)['sha256'] == 'dabdf7f7ae2dfc5ad279ac9819d67e3defa12e561550e5f8a247b5ea2154ff0b'
assert tc['executables']['generator'] == {'sha256': '4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959', 'bytes': 7202304}
old_standing = 'Observed offline macOS 27.0 (26A428) rebuild (contracts-generator-rebuild-01, replacing rebuild403) of identical generator sources/dependencies with the same Homebrew Rust 1.95.0; development pins, no reproducible-build or release qualification'
assert tc['standing'] == old_standing
tc['standing'] = ('Observed offline macOS 27.0 (26A428) rebuild (contracts-generator-rebuild-02, replacing rebuild-01; unit F8b) of the same '
                  'generator sources/dependencies with only license metadata added to Cargo.toml, using the same Homebrew Rust 1.95.0; '
                  'development pins, no reproducible-build or release qualification')
tc['executables']['generator']['sha256'] = receipt['executable']['sha256']
tc['executables']['generator']['bytes'] = receipt['executable']['bytes']
save('tools/contracts/toolchain.json', tc)
report['tools/contracts/toolchain.json'] = {'before': pin(raw), 'after': pin((W / 'tools/contracts/toolchain.json').read_bytes())}
# Closure.
raw, cl = load('tools/contracts/generator-closure.json')
assert pin(raw)['sha256'] == '7fcfa1049aec2d9f92f262c4a58099ca712fb2dfd166fa225defe6ccb3c7f3d8'
BEFORE = {'tools/verify_design.py': (33654, '2764cf7b5e3aaa7fb1722bab6714fe1eed4a350867f4cc369d0490342527325c'),
          'tools/contracts/Cargo.toml': (307, '6b769285e95d2aa94a420fa63d74d6a199bbe84c9ceadef75550112fb3d88a7f'),
          'tools/contracts/package.json': (259, '1c71c0980aa483c08d4adf10c90706346287e86f8c940a63002e3fb1317cacc4'),
          'tools/contracts/build-receipt.json': (8721, 'c434cbd3e9fc24d5056aaf43b465a4024b85bb576f8b7c20b336d4466400898d'),
          'tools/contracts/toolchain.json': (679, 'dabdf7f7ae2dfc5ad279ac9819d67e3defa12e561550e5f8a247b5ea2154ff0b')}
changed = []
for row in cl['files']:
    if row['path'] in BEFORE:
        assert (row['bytes'], row['sha256']) == BEFORE[row['path']], row['path']
        new = pin((W / row['path']).read_bytes()); row['bytes'], row['sha256'] = new['bytes'], new['sha256']
        changed.append(row['path'])
assert sorted(changed) == sorted(BEFORE)
assert cl['toolchain']['generator'] == {'sha256': '4388e707035e0ea4b0c3dcd9206e55fd7045e58658a443fb13e04a12847a6959', 'bytes': 7202304}
cl['toolchain']['generator']['sha256'] = receipt['executable']['sha256']; cl['toolchain']['generator']['bytes'] = receipt['executable']['bytes']
assert cl['toolchain'] == tc['executables']
for row in cl['files']:
    assert pin((W / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row['path']
save('tools/contracts/generator-closure.json', cl)
closure_raw = (W / 'tools/contracts/generator-closure.json').read_bytes()
report['tools/contracts/generator-closure.json'] = {'before': pin(raw), 'after': pin(closure_raw), 'rowsChanged': sorted(changed), 'rows': len(cl['files'])}
# Registry.
raw, reg = load('schemas/registry.json')
assert pin(raw)['sha256'] == 'cde02c13dfbc55068f99c6dec4c8dea0548669d7bedfe688b57aefa35312d26a' and len(reg['recipes']) == 1
assert reg['recipes'][0]['generatorClosureSha256'] == '7fcfa1049aec2d9f92f262c4a58099ca712fb2dfd166fa225defe6ccb3c7f3d8'
reg['recipes'][0]['generatorClosureSha256'] = pin(closure_raw)['sha256']
save('schemas/registry.json', reg)
report['schemas/registry.json'] = {'before': pin(raw), 'after': pin((W / 'schemas/registry.json').read_bytes())}
# Lane registry.
raw, ln = load('tools/typescript-lanes.json')
assert pin(raw)['sha256'] == '288c961944de8293edc8bb37fc8a0678fa39225c87f58fd96e55b135e9394dd4'
LBEFORE = {'tools/verify_design.py': BEFORE['tools/verify_design.py'],
           'tools/typescript-boundary/package.json': (515, '98ae9218de30d736c7dcd28cab71c882e4ab9cf78aded2c7b6bf126864fe9806')}
lchanged = []
for row in ln['files']:
    if row['path'] in LBEFORE:
        assert (row['bytes'], row['sha256']) == LBEFORE[row['path']], row['path']
        new = pin((W / row['path']).read_bytes()); row['bytes'], row['sha256'] = new['bytes'], new['sha256']; lchanged.append(row['path'])
assert sorted(lchanged) == sorted(LBEFORE)
for row in ln['files']:
    if '/node_modules/' not in row['path']:
        assert pin((W / row['path']).read_bytes()) == {'bytes': row['bytes'], 'sha256': row['sha256']}, row['path']
save('tools/typescript-lanes.json', ln)
lanes_raw = (W / 'tools/typescript-lanes.json').read_bytes()
assert pin(lanes_raw) == {'bytes': 35396, 'sha256': '4d27f6d7c711c8471717da36b931fbcbd7466ef96a34a2d9bba494cd8ef15db1'}
report['tools/typescript-lanes.json'] = {'before': pin(raw), 'after': pin(lanes_raw), 'rowsChanged': sorted(lchanged), 'rows': len(ln['files'])}
print(json.dumps(report, indent=2))
