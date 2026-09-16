"""Generate only the closed registry's outputs from explicitly pinned local inputs.

Development tool. This does not confer product admission or release authority.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath
import subprocess
import tempfile


class GenerationError(ValueError):
    pass


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise GenerationError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def forbidden(_):
        raise GenerationError('noninteger JSON number in generation input')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=forbidden, parse_constant=forbidden)


def closed(value, keys, label):
    if type(value) is not dict or set(value) != set(keys):
        raise GenerationError('unknown or missing ' + label + ' fields')


def sorted_unique(values, label):
    if type(values) is not list or not values or any(type(v) is not str for v in values) or values != sorted(set(values)):
        raise GenerationError(label + ' must be sorted unique nonempty strings')


def digest(value):
    if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise GenerationError('invalid SHA-256')
    return value


def local(root, value, *, existing=True):
    if type(value) is not str or not value or '\\' in value:
        raise GenerationError('invalid repository-relative path')
    path = PurePosixPath(value)
    if path.is_absolute() or str(path) != value or any(p in ('', '.', '..') for p in value.split('/')):
        raise GenerationError('noncanonical repository-relative path')
    result = root
    for part in path.parts:
        result = result / part
        if result.is_symlink():
            raise GenerationError('symlink in generation input/output path')
    if existing and not result.is_file():
        raise GenerationError('missing regular input: ' + value)
    return result


def checked(root, path, expected):
    raw = local(root, path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest(expected):
        raise GenerationError('input digest mismatch: ' + path)
    return raw


def registry(root):
    raw = local(root, 'schemas/registry.json').read_bytes()
    value = decode(raw)
    closed(value, ['schemaVersion', 'sources', 'recipes'], 'registry')
    if type(value['schemaVersion']) is not int or value['schemaVersion'] != 1:
        raise GenerationError('unsupported registry version')
    if type(value['sources']) is not list or not value['sources'] or type(value['recipes']) is not list or not value['recipes']:
        raise GenerationError('sources and recipes must be nonempty arrays')
    source_map = {}
    ids = set()
    source_paths = []
    for row in value['sources']:
        closed(row, ['sourcePath', 'sourceSha256', 'schemaId', 'declaredMajor', 'profile', 'semanticValidatorOwner'], 'source')
        key = digest(row['sourceSha256'])
        if key in source_map or type(row['schemaId']) is not str or not row['schemaId'] or row['schemaId'] in ids:
            raise GenerationError('duplicate source digest or schema ID')
        if type(row['declaredMajor']) is not int or row['declaredMajor'] < 1 or row['profile'] != 'opensip-exact-schema-reference-1':
            raise GenerationError('unsupported declared schema profile')
        if type(row['semanticValidatorOwner']) is not str or not row['semanticValidatorOwner']:
            raise GenerationError('semantic owner required')
        source_raw = checked(root, row['sourcePath'], key)
        document = decode(source_raw)
        if type(document) is not dict or document.get('$id') != row['schemaId'] or document.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise GenerationError('source document identity/dialect mismatch')
        source_map[key] = (row, source_raw, document)
        source_paths.append(row['sourcePath'])
        ids.add(row['schemaId'])
    sorted_unique(source_paths, 'source paths')
    recipes = []
    outputs = set()
    recipe_ids = []
    for row in value['recipes']:
        closed(row, ['recipeId', 'generatorClosureSha256', 'optionsPath', 'optionsSha256', 'sourceSha256s', 'outputs'], 'recipe')
        recipe_ids.append(row['recipeId'])
        digest(row['generatorClosureSha256'])
        options = decode(checked(root, row['optionsPath'], row['optionsSha256']))
        sorted_unique(row['sourceSha256s'], 'recipe source digests')
        if any(key not in source_map for key in row['sourceSha256s']):
            raise GenerationError('recipe references unregistered source')
        if type(row['outputs']) is not list or not row['outputs']:
            raise GenerationError('recipe outputs required')
        paths = []
        for output in row['outputs']:
            closed(output, ['path', 'language', 'roles'], 'output')
            path = output['path']
            local(root, path, existing=False)
            prefix = 'crates/contracts/src/generated/' if output['language'] == 'rust' else None
            if output['language'] == 'typescript':
                prefix = next((p for p in ('providers/typescript/src/generated/', 'apps/report/src/generated/') if path.startswith(p)), None)
            extension = '.rs' if output['language'] == 'rust' else '.ts'
            if not prefix or not path.startswith(prefix) or not path.endswith(extension) or '/' in path[len(prefix):]:
                raise GenerationError('output outside declared generated consumer')
            sorted_unique(output['roles'], 'output roles')
            if not set(output['roles']) <= {'carrier', 'shape-validator', 'module-index'} or path in outputs:
                raise GenerationError('invalid roles or duplicate output owner')
            outputs.add(path)
            paths.append(path)
        sorted_unique(paths, 'recipe output paths')
        recipes.append((row, options))
    sorted_unique(recipe_ids, 'recipe IDs')
    return value, source_map, recipes, hashlib.sha256(raw).hexdigest()


def import_file(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate(root, *, generator, node, rustfmt, write):
    value, sources, recipes, registry_sha = registry(root)
    if len(recipes) != 1 or recipes[0][0]['recipeId'] != 'contracts-v1':
        raise GenerationError('this adapter implements only contracts-v1')
    row, options = recipes[0]
    if set(row['sourceSha256s']) != set(sources):
        raise GenerationError('contracts-v1 requires the exact selected source closure')
    closure_raw = checked(root, 'tools/contracts/generator-closure.json', row['generatorClosureSha256'])
    closure = decode(closure_raw)
    closed(closure, ['schemaVersion', 'files', 'toolchain', 'typescriptPackageFiles', 'hostProfile', 'nativeLibraries'], 'generator closure')
    if type(closure['schemaVersion']) is not int or closure['schemaVersion'] != 1:
        raise GenerationError('unsupported generator closure')
    # This candidate is a development-host profile, not a portable release tool
    # qualification. Native loader/kernel/builtins are its declared trusted host.
    if closure['hostProfile'] != {'os':sys.platform, 'scope':'development-trusted-host'}:
        raise GenerationError('generator host profile mismatch')
    if type(closure['files']) is not list or not closure['files']:
        raise GenerationError('generator closure files required')
    pinned = {}
    for pin in closure['files']:
        closed(pin, ['path', 'sha256', 'bytes'], 'generator file pin')
        raw = checked(root, pin['path'], pin['sha256'])
        if type(pin['bytes']) is not int or pin['bytes'] != len(raw):
            raise GenerationError('generator input byte length mismatch')
        pinned[pin['path']] = raw
    sorted_unique([pin['path'] for pin in closure['files']], 'generator file paths')
    required = {'tools/generate_contracts.py','tools/contracts/adapter.py','tools/contracts/prepare.py',
        'tools/contracts/render-types.cjs','tools/contracts/generate-ts.cjs','tools/contracts/rustfmt.toml',
        'tools/contracts/package.json','tools/contracts/pnpm-lock.yaml','tools/contracts/pnpm-workspace.yaml',
        'tools/contracts/Cargo.toml','tools/contracts/Cargo.lock','tools/contracts/src/main.rs',
        'tools/contracts/src/presence.rs','tools/contracts/src/integers.rs',
        'tools/contracts/runtime/exact-json.ts','tools/contracts/runtime/schema.ts',
        'tools/contracts/runtime/patterns.ts','tools/contracts/runtime/pattern-profile.json'}
    if set(pinned) != required:
        raise GenerationError('generator source closure differs from adapter input set')
    paths = {'generator': generator, 'node': node, 'rustfmt':rustfmt, 'python':sys.executable}
    if type(closure['toolchain']) is not dict or set(closure['toolchain']) != set(paths):
        raise GenerationError('toolchain input set mismatch')
    executable_bytes = {}
    for key, supplied in paths.items():
        pin = closure['toolchain'][key]
        closed(pin, ['sha256','bytes'], 'tool executable pin')
        path = Path(supplied)
        if not path.is_absolute() or not path.is_file():
            raise GenerationError('absolute regular executable path required: '+key)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest(pin['sha256']) or type(pin['bytes']) is not int or len(raw) != pin['bytes']:
            raise GenerationError('tool executable differs from closure: '+key)
        executable_bytes[key] = raw
    if type(closure['nativeLibraries']) is not list:
        raise GenerationError('native tool library pins required')
    for pin in closure['nativeLibraries']:
        closed(pin,['path','sha256','bytes'],'native library pin')
        path=Path(pin['path'])
        if not path.is_absolute() or not path.is_file():
            raise GenerationError('missing native tool library')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest(pin['sha256']) or type(pin['bytes']) is not int or len(raw)!=pin['bytes']:
            raise GenerationError('native tool library changed')
    sorted_unique([pin['path'] for pin in closure['nativeLibraries']],'native library paths')
    with tempfile.TemporaryDirectory(prefix='opensip-contracts-') as tmp:
        work = Path(tmp)
        for name, raw in pinned.items():
            dst=work/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        # Code now runs only from its verified snapshot. Provisioning/install and
        # compiling the generator are separate explicit operations, never hidden
        # in a drift check or an ordinary consumer build.
        adapter = import_file(work/'tools/contracts/adapter.py','contracts_adapter')
        adapter.validate_options(options,sources)
        adapter.copy_typescript(root/'tools/contracts/node_modules/typescript',
            work/'tools/contracts/node_modules/typescript',closure['typescriptPackageFiles'])
        prepare = import_file(work/'tools/contracts/prepare.py','contracts_prepare')
        inputs=work/'inputs';inputs.mkdir()
        prepare.prepare({v[0]['schemaId']:v[2] for v in sources.values()},options,inputs)
        (inputs/'options.json').write_text(json.dumps(options,ensure_ascii=True)+'\n')
        (inputs/'raw-schemas.json').write_text(json.dumps([v[1].decode('utf-8') for v in sources.values()],ensure_ascii=True)+'\n')
        provenance={'registrySha256':registry_sha,'generatorClosureSha256':row['generatorClosureSha256']}
        (inputs/'provenance.json').write_text(json.dumps(provenance)+'\n')
        executables={}
        for key in ('generator','node'):
            path=work/key;path.write_bytes(executable_bytes[key]);path.chmod(0o700);executables[key]=str(path)
        # rustfmt uses its relative native library loader path. Its verified
        # executable and explicit native dependencies stay in the trusted host.
        executables['rustfmt']=str(Path(rustfmt).resolve(strict=True))
        home=work/'home';home.mkdir()
        env={'PATH':'/usr/bin:/bin','HOME':str(home),'LANG':'C','LC_ALL':'C','TZ':'UTC'}
        output=work/'output'
        def run(argv):
            subprocess.run(argv,cwd=work,env=env,check=True)
        run([executables['generator'],str(inputs),str(output)])
        rust_files=sorted((output/'crates/contracts/src/generated').glob('*.rs'))
        header='// Generated by contracts-v1; inert carriers, not admission.\n// Registry SHA-256: '+registry_sha+'\n// Generator closure SHA-256: '+row['generatorClosureSha256']+'\n'
        for path in rust_files:
            text=path.read_text();path.write_text(header+text.split('\n',1)[1])
        run([executables['rustfmt'],'--edition','2024','--config-path',str(work/'tools/contracts/rustfmt.toml'),*[str(p) for p in rust_files]])
        run([executables['node'],str(work/'tools/contracts/generate-ts.cjs'),str(inputs),str(output)])
        actual={str(p.relative_to(output)):p.read_bytes() for p in output.rglob('*') if p.is_file()}
        expected={o['path'] for o in row['outputs']}
        if set(actual) != expected or len(actual) != 8:
            raise GenerationError('generator emitted a different output set')
        existing=set()
        for parent in {str(Path(p).parent) for p in expected}:
            directory=local(root,parent,existing=False)
            if directory.exists():
                for path in directory.rglob('*'):
                    if path.is_symlink() or not path.is_file():
                        raise GenerationError('unexpected generated directory member')
                    existing.add(str(path.relative_to(root)))
        if existing-expected:
            raise GenerationError('undeclared checked-in generated output')
        changed=[name for name,raw in sorted(actual.items()) if name not in existing or local(root,name).read_bytes()!=raw]
        if not write and changed:
            raise GenerationError('generated output drift: '+', '.join(changed))
        if write:
            # Preflight every destination before any replacement. Each file is
            # atomically replaced; an interrupted eight-file update is detectable
            # by the next drift check, not represented as an atomic transaction.
            destinations=[(local(root,name,existing=False),actual[name]) for name in changed]
            for destination,raw in destinations:
                destination.parent.mkdir(parents=True,exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=destination.parent,prefix='.contracts-',delete=False) as handle:
                    handle.write(raw);temp=Path(handle.name)
                try: os.replace(temp,destination)
                finally: temp.unlink(missing_ok=True)
        print(json.dumps({'outputs':len(actual),'changed':changed,'write':write,'registrySha256':registry_sha}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--generator',required=True,help='explicit previously built and pinned Rust generator')
    parser.add_argument('--node',required=True)
    parser.add_argument('--rustfmt',required=True)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    try:
        generate(args.root.resolve(),generator=args.generator,node=args.node,rustfmt=args.rustfmt,write=args.write)
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        parser.exit(1,'generation refused: '+str(exc)+'\n')


if __name__ == '__main__':
    main()
