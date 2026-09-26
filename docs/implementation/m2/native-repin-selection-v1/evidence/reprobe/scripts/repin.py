"""Re-pin OpenSIP generator host pins in the SCRATCH product copy only (macOS 27 reprobe).

Refuses to touch anything outside /Users/sb/opensip-deps/confinement-reprobe-01/product.
Python runtime files are re-pinned only when the signature-equivalence evidence
(sigequiv.json) says the old pin and the installed file differ only in signature.
"""
from pathlib import Path
import hashlib, json, shutil, sys

BASE = Path('/Users/sb/opensip-deps/confinement-reprobe-01')
P = BASE / 'product'
C = P / 'tools/contracts'
REBUILD = Path('/Users/sb/opensip-deps/contracts-generator-rebuild-01')
SIGEQUIV = Path('/Users/sb/opensip-deps/native-repin-01/evidence-inputs/sigequiv.json')
assert P.resolve() == P and 'opensip-deps/confinement-reprobe-01/product' in str(P)


def pin(path):
    raw = Path(path).read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def dump(path, value):
    raw = (json.dumps(value, indent=2) + '\n').encode()
    path.write_bytes(raw)
    return raw


changes = {'runtimePins': [], 'files': {}}


def repin_row(row, *, require_sig=None):
    n, h = pin(row['path'])
    if (n, h) != (row['bytes'], row['sha256']):
        if require_sig is not None:
            s = require_sig.get(row['path'])
            if not (s and s['pinnedSha256'] == row['sha256'] and s['pinnedBytes'] == row['bytes']
                    and s['installedSha256'] == h and s['installedBytes'] == n and s['unsignedEqual'] is True):
                sys.exit('refuse: not signature-only drift: ' + row['path'])
        entry = {'path': row['path'], 'old': {'bytes': row['bytes'], 'sha256': row['sha256']}, 'new': {'bytes': n, 'sha256': h}}
        if entry not in changes['runtimePins']:
            changes['runtimePins'].append(entry)
        row['bytes'], row['sha256'] = n, h


# 1. confinement profile: OS-owned runtime files and sandbox-exec.
conf = json.loads((C / 'confinement-profile.json').read_bytes())
for row in [*conf['runtimeFiles'], conf['sandboxExecutable']]:
    repin_row(row)
dump(C / 'confinement-profile.json', conf)

# 2. Python profiles: signature-only Homebrew drift, names and counts unchanged.
sig = {r['path']: r for r in json.loads(SIGEQUIV.read_bytes())}
for name, count in (('native-python-profile.json', 142), ('python-profile.json', 28)):
    v = json.loads((C / name).read_bytes())
    profile, nfiles = v['profile'], len(v['files'])
    assert nfiles == count, (name, nfiles)
    for row in [v['executable'], v['library'], *v['files'], *v.get('nativeLibraries', [])]:
        repin_row(row, require_sig=sig)
    assert v['profile'] == profile and len(v['files']) == count
    dump(C / name, v)

# 3. toolchain: python child executable and rebuilt generator.
tc = json.loads((C / 'toolchain.json').read_bytes())
child = json.loads((C / 'native-python-profile.json').read_bytes())['executable']
n, h = pin(child['path'])
assert (n, h) == (child['bytes'], child['sha256'])
tc['executables']['python'] = {'bytes': n, 'sha256': h}
receipt_raw = (REBUILD / 'receipt.json').read_bytes()
receipt = json.loads(receipt_raw)
n, h = pin(REBUILD / 'opensip-contract-generator')
assert receipt['executable'] == {'sha256': h, 'bytes': n}
tc['executables']['generator'] = {'sha256': h, 'bytes': n}
node = tc['executables']['node']
assert pin('/Users/sb/.nvm/versions/node/v24.16.0/bin/node') == (node['bytes'], node['sha256'])
dump(C / 'toolchain.json', tc)

# 4. build receipt: exact rebuild receipt bytes.
(C / 'build-receipt.json').write_bytes(receipt_raw)

# 5. closure: toolchain + five tools/contracts rows.
closure = json.loads((C / 'generator-closure.json').read_bytes())
closure['toolchain'] = tc['executables']
touched = []
for row in closure['files']:
    n, h = pin(P / row['path'])
    if (n, h) != (row['bytes'], row['sha256']):
        touched.append(row['path'])
        row['bytes'], row['sha256'] = n, h
expected = sorted('tools/contracts/' + x for x in ['build-receipt.json', 'confinement-profile.json', 'native-python-profile.json', 'python-profile.json', 'toolchain.json'])
assert sorted(touched) == expected, touched
closure_raw = dump(C / 'generator-closure.json', closure)

# 6. registry recipe closure digest.
reg = json.loads((P / 'schemas/registry.json').read_bytes())
assert len(reg['recipes']) == 1
reg['recipes'][0]['generatorClosureSha256'] = hashlib.sha256(closure_raw).hexdigest()
dump(P / 'schemas/registry.json', reg)

for rel in [*expected, 'tools/contracts/generator-closure.json', 'schemas/registry.json']:
    n, h = pin(P / rel)
    changes['files'][rel] = {'bytes': n, 'sha256': h}
changes['closureRowsChanged'] = touched
print(json.dumps(changes, indent=2))
