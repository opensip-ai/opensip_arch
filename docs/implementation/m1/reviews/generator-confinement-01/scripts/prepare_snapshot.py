"""Build a verified, self-contained generator-child snapshot inside this trial.

Reuses candidate-03's own registry/closure checks (read-only import) and writes
only below <trial>/work. Mirrors generate_contracts.generate() up to the first
child process; it does not run any child and grants no product authority.
"""
import hashlib, importlib.util, json, shutil, sys
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
CAND = Path('/private/tmp/opensip-implementation/m1-generator-integration-candidate-03')
NODE = Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node')
GENERATOR = Path('/private/tmp/opensip-implementation/m1-generator-integration-candidate-02/tools/contracts/target/debug/opensip-contract-generator')
FORMAT_GENERATOR = Path('/private/tmp/opensip-implementation/m1-generator-format-trial-01/target/debug/opensip-generator-format-trial')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if not sys.flags.isolated:
        raise SystemExit('run with python3 -I')
    G = load(CAND / 'tools/generate_contracts.py', 'candidate03_generate')
    _, sources, recipes, registry_sha = G.registry(CAND)
    row, options = recipes[0]
    closure = G.decode(G.checked(CAND, 'tools/contracts/generator-closure.json', row['generatorClosureSha256']))
    # Root is concurrently editing candidate-03, so a stale closure pin is
    # recorded rather than fatal. This trial qualifies confinement, not pins.
    pinned, stale, missing = {}, [], []
    for pin in closure['files']:
        path = G.local(CAND, pin['path'], existing=False)
        if not path.is_file():
            missing.append(pin['path'])
            continue
        raw = path.read_bytes()
        if sha(raw) != pin['sha256'] or len(raw) != pin['bytes']:
            stale.append(pin['path'])
        pinned[pin['path']] = raw
    for key, path in (('generator', GENERATOR), ('node', NODE)):
        raw = path.read_bytes()
        pin = closure['toolchain'][key]
        if sha(raw) != pin['sha256'] or len(raw) != pin['bytes']:
            raise SystemExit('toolchain pin mismatch: ' + key)

    work = TRIAL / 'work'
    if work.exists():
        shutil.rmtree(work)
    snapshot, inputs, bindir = work / 'snapshot', work / 'inputs', work / 'bin'
    for name, raw in pinned.items():
        dst = snapshot / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(raw)
    adapter = load(snapshot / 'tools/contracts/adapter.py', 'snapshot_adapter')
    adapter.validate_options(options, sources)
    adapter.validate_source_map(G.decode(pinned['schemas/source-map.json']), sources, options)
    adapter.copy_typescript(CAND / 'tools/contracts/node_modules/typescript',
                            snapshot / 'tools/contracts/node_modules/typescript', closure['typescriptPackageFiles'])
    prepare = load(snapshot / 'tools/contracts/prepare.py', 'snapshot_prepare')
    inputs.mkdir(parents=True)
    prepare.prepare({v[0]['schemaId']: v[2] for v in sources.values()}, options, inputs)
    (inputs / 'options.json').write_text(json.dumps(options, ensure_ascii=True) + '\n')
    (inputs / 'raw-schemas.json').write_text(json.dumps([v[1].decode('utf-8') for v in sources.values()], ensure_ascii=True) + '\n')
    (inputs / 'provenance.json').write_text(json.dumps({'registrySha256': registry_sha,
        'generatorClosureSha256': row['generatorClosureSha256']}) + '\n')
    bindir.mkdir()
    for name, path in (('node', NODE), ('generator', GENERATOR), ('format-generator', FORMAT_GENERATOR)):
        (bindir / name).write_bytes(path.read_bytes())
        (bindir / name).chmod(0o500)
    manifest = {str(p.relative_to(work)): sha(p.read_bytes()) for p in sorted(work.rglob('*')) if p.is_file()}
    (TRIAL / 'logs/snapshot-manifest.json').write_text(json.dumps(
        {'registrySha256': registry_sha, 'generatorClosureSha256': row['generatorClosureSha256'],
         'closurePinsStale': stale, 'closurePinsMissing': missing,
         'formatGeneratorSource': str(FORMAT_GENERATOR), 'files': manifest}, indent=1) + '\n')
    print(json.dumps({'files': len(manifest), 'expectedOutputs': sorted(o['path'] for o in row['outputs'])}))


if __name__ == '__main__':
    main()
