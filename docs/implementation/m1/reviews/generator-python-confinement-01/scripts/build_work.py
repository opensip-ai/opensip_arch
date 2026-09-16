"""Build the trial work tree from the stable source/ copy (never candidate-03).

work/entry   prepare-inputs.py (author candidate, copied from the trial root)
work/code    prepare.py and runtime/* (only runtime/schema.ts is granted to the child)
work/inputs  raw-schemas.json (registry order, raw strings) and options.json (verbatim)
"""
import hashlib, json, shutil, sys
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
SOURCE = TRIAL / 'source'
WORK = TRIAL / 'work'
# sha256 of the stable source copy as handed to this trial.
PINS = {'prepare.py': '84b465b355f58c0f8f937b3e35d330b9284df13c42995dbf870bd972cc409d51',
        'options.json': '1719ef1860624e390af57f58c9670b60c68aa9d599eba3a4cee18d43343d7902',
        'runtime/schema.ts': '1e4c2720e3a45cd857a41e5c19c65c597f5f9372bd8fb185d8d318c2f77ab3b9',
        'runtime/exact-json.ts': 'ad51a046cc6abbfd7f9b0fa4a3b5462ac8c5e4e3831b0ba87db5dd0ae8db2336',
        'runtime/patterns.ts': '579c5b68d4e000a3e13ddc028ad762d7574a3744468bba4229be621f4916ea83',
        'runtime/pattern-profile.json': 'eba26fc0659521cd15168cd78426fd79a64efceac584c6c147996348f8cc6106',
        'schemas/registry.json': '52d48e7ab77d644e14674b5e6b3cc82805b87ee0a8ccfd43e1e381e07be8c914',
        'schemas/source-map.json': '561cf9ef76d04bab37cec2791eb61786d48c52d8ac0938d38d9e3f003022708a'}
DIALECT = 'https://json-schema.org/draft/2020-12/schema'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise SystemExit('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def forbidden(_):
        raise SystemExit('noninteger JSON number')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=forbidden, parse_constant=forbidden)


def pinned(name):
    path = SOURCE / name
    raw = path.read_bytes()
    if path.is_symlink() or sha(raw) != PINS[name]:
        raise SystemExit('source pin mismatch: ' + name)
    return raw


def main():
    if not sys.flags.isolated:
        raise SystemExit('run with python3 -I')
    blobs = {name: pinned(name) for name in PINS}
    registry = decode(blobs['schemas/registry.json'])
    raw_schemas, ids = [], set()
    for row in registry['sources']:
        raw = (SOURCE / row['sourcePath']).read_bytes()
        document = decode(raw)
        if sha(raw) != row['sourceSha256'] or document.get('$id') != row['schemaId'] or document.get('$schema') != DIALECT \
                or row['schemaId'] in ids:
            raise SystemExit('schema source mismatch: ' + row['sourcePath'])
        ids.add(row['schemaId'])
        raw_schemas.append(raw.decode('utf-8'))
    listed = sorted('schemas/sources/' + p.name for p in (SOURCE / 'schemas/sources').iterdir())
    if listed != sorted(row['sourcePath'] for row in registry['sources']):
        raise SystemExit('source directory differs from registry')

    if WORK.exists():
        shutil.rmtree(WORK)
    files = {'entry/prepare-inputs.py': (TRIAL / 'prepare-inputs.py').read_bytes(),
             'code/prepare.py': blobs['prepare.py'],
             'inputs/options.json': blobs['options.json'],
             # Same serialization candidate-03 hands its children.
             'inputs/raw-schemas.json': (json.dumps(raw_schemas, ensure_ascii=True) + '\n').encode('ascii')}
    for name in PINS:
        if name.startswith('runtime/'):
            files['code/' + name] = blobs[name]
    for name, raw in files.items():
        path = WORK / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    manifest = {'sourcePins': PINS, 'registrySha256': PINS['schemas/registry.json'], 'schemaCount': len(raw_schemas),
                'files': {name: {'sha256': sha(raw), 'bytes': len(raw)} for name, raw in sorted(files.items())}}
    (TRIAL / 'logs').mkdir(exist_ok=True)
    (TRIAL / 'logs/work-manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    print(json.dumps({'files': len(files), 'schemas': len(raw_schemas)}))


if __name__ == '__main__':
    main()
