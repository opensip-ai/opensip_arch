import concurrent.futures, hashlib, json, pathlib, shutil, tarfile, urllib.request

root = pathlib.Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95')
pins = json.loads(pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-p-2026-10-05/evidence/rust-component-pins.json').read_text())['components']
def acquire(pin):
    archive = root / pin['url'].rsplit('/', 1)[1]
    if not archive.exists():
        temporary = archive.with_suffix('.download')
        with urllib.request.urlopen(pin['url'], timeout=120) as source, temporary.open('wb') as target:
            shutil.copyfileobj(source, target)
        temporary.rename(archive)
    raw = archive.read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
    unpacked = root / ('unpacked-' + pin['component'])
    unpacked.mkdir(exist_ok=True)
    with tarfile.open(archive) as source:
        source.extractall(unpacked, filter='data')
    component_root = next(unpacked.iterdir())
    component = component_root / (pin['component'] if pin['component'] == 'rustc' else pin['component'] + '-aarch64-apple-darwin')
    if not component.exists():
        component = component_root / pin['component']
    assert component.is_dir(), list(component_root.iterdir())
    shutil.copytree(component, root / 'sysroot', dirs_exist_ok=True)
    return dict(pin, archive=str(archive), verified=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(acquire, pins))
report = {'standing': 'G2 AUTHORING TEST TOOLCHAIN ONLY; NOT PRODUCTION SELECTION', 'components': results, 'sysroot': str(root / 'sysroot')}
pathlib.Path('/tmp/opensip-implementation/g2-authoring/acquisition.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'verifiedComponents': len(results), 'sysroot': report['sysroot']}))
