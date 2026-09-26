"""Apply the macOS 27 native re-pin to the SCRATCH product copy only.

Takes confinement-profile.json, native-python-profile.json, python-profile.json and
build-receipt.json byte-for-byte from the confinement-reprobe-01 scratch product (after
checking every host pin in them against the installed file now), rewrites toolchain.json
(new python/generator pins and a truthful standing string), then recomputes the five
tools/contracts closure rows, the closure toolchain and the registry recipe closure digest.
Refuses to write outside /Users/sb/opensip-deps/native-repin-01/product.
"""
from pathlib import Path
import hashlib, json, sys

BASE = Path('/Users/sb/opensip-deps/native-repin-01')
P = BASE / 'product'
C = P / 'tools/contracts'
REPROBE = Path('/Users/sb/opensip-deps/confinement-reprobe-01/product/tools/contracts')
REBUILD = Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01')
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
STANDING = ('Observed offline macOS 27.0 (26A428) rebuild (contracts-generator-rebuild-01, replacing rebuild403) '
            'of identical generator sources/dependencies with the same Homebrew Rust 1.95.0; '
            'development pins, no reproducible-build or release qualification')
assert P.resolve() == P and str(P).startswith('/Users/sb/opensip-deps/native-repin-01/')


def pin(path):
    raw = Path(path).read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def dump(path, value):
    raw = (json.dumps(value, indent=2) + '\n').encode()
    assert str(path.resolve()).startswith(str(P) + '/')
    path.write_bytes(raw)
    return raw


def check_host(row):
    if pin(row['path']) != {'bytes': row['bytes'], 'sha256': row['sha256']}:
        sys.exit('refuse: host file differs from re-pin: ' + row['path'])


log = {'hostPinsChecked': 0, 'copied': {}, 'files': {}}
# 1-3. Profiles from the re-probe, rechecked against the installed files.
for name in ('confinement-profile.json', 'native-python-profile.json', 'python-profile.json'):
    raw = (REPROBE / name).read_bytes()
    v = json.loads(raw)
    rows = [*v['runtimeFiles'], v['sandboxExecutable']] if name.startswith('confinement') else \
           [v['executable'], v['library'], *v['files'], *v.get('nativeLibraries', [])]
    for row in rows:
        check_host(row)
        log['hostPinsChecked'] += 1
    (C / name).write_bytes(raw)
    log['copied'][name] = pin(C / name)
# 4. Build receipt: exact rebuild receipt bytes.
receipt_raw = (REBUILD / 'receipt.json').read_bytes()
assert (REPROBE / 'build-receipt.json').read_bytes() == receipt_raw
receipt = json.loads(receipt_raw)
generator = pin(REBUILD / 'opensip-contract-generator')
assert receipt['executable'] == {'sha256': generator['sha256'], 'bytes': generator['bytes']}
(C / 'build-receipt.json').write_bytes(receipt_raw)
# 5. Toolchain.
tc = json.loads((C / 'toolchain.json').read_bytes())
child = json.loads((C / 'native-python-profile.json').read_bytes())['executable']
check_host(child)
assert pin(NODE) == tc['executables']['node']
tc['standing'] = STANDING
tc['executables']['generator'] = {'sha256': generator['sha256'], 'bytes': generator['bytes']}
tc['executables']['python'] = {'bytes': child['bytes'], 'sha256': child['sha256']}
assert json.loads((REPROBE / 'toolchain.json').read_bytes())['executables'] == tc['executables']
dump(C / 'toolchain.json', tc)
# 6. Closure.
closure = json.loads((C / 'generator-closure.json').read_bytes())
closure['toolchain'] = tc['executables']
touched = []
for row in closure['files']:
    now = pin(P / row['path'])
    if now != {'bytes': row['bytes'], 'sha256': row['sha256']}:
        touched.append(row['path'])
        row['bytes'], row['sha256'] = now['bytes'], now['sha256']
expected = sorted('tools/contracts/' + x for x in ['build-receipt.json', 'confinement-profile.json', 'native-python-profile.json', 'python-profile.json', 'toolchain.json'])
assert sorted(touched) == expected, touched
closure_sha = hashlib.sha256(dump(C / 'generator-closure.json', closure)).hexdigest()
# 7. Registry.
reg = json.loads((P / 'schemas/registry.json').read_bytes())
assert len(reg['recipes']) == 1
reg['recipes'][0]['generatorClosureSha256'] = closure_sha
dump(P / 'schemas/registry.json', reg)
for rel in [*expected, 'tools/contracts/generator-closure.json', 'schemas/registry.json']:
    log['files'][rel] = pin(P / rel)
log['closureRowsChanged'] = touched
print(json.dumps(log, indent=2))
