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
import stat
import sys
from pathlib import Path, PurePosixPath
import subprocess
import tempfile


class GenerationError(ValueError):
    pass


def collect_outputs(root, expected, max_bytes=134217728):
    """Read only declared, unlinked regular files after all children exit.

    Open every directory and file without following symlinks. Child-generated
    links must never make the trusted parent read or overwrite outside bytes.
    """
    directories = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    result = {}
    remaining = max_bytes
    def walk(fd, prefix):
        nonlocal remaining
        for name in sorted(os.listdir(fd)):
            relative = prefix + name
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode) and relative in directories:
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                try: walk(child, relative + '/')
                finally: os.close(child)
            elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and relative in expected:
                child = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                try:
                    opened = os.fstat(child)
                    if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1 or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                        raise GenerationError('generated file changed during collection')
                    if opened.st_size > remaining:
                        raise GenerationError('generated output byte limit exceeded')
                    with os.fdopen(child, 'rb', closefd=False) as stream:
                        raw = stream.read(remaining + 1)
                    remaining -= len(raw)
                    if remaining < 0:
                        raise GenerationError('generated output byte limit exceeded')
                    result[relative] = raw
                finally: os.close(child)
            else:
                raise GenerationError('undeclared, linked or nonregular generated output')
    if not root.exists():
        raise GenerationError('generator emitted a different output set')
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try: walk(fd, '')
    finally: os.close(fd)
    if set(result) != expected:
        raise GenerationError('generator emitted a different output set')
    return result


def directory_identity(path):
    """Identity of a parent-created root, never following a child-made link."""
    value = path.lstat()
    if not stat.S_ISDIR(value.st_mode):
        raise GenerationError('child root is no longer a parent-created directory')
    return value.st_dev, value.st_ino


def verify_directory_roots(roots):
    for path, expected in roots.items():
        if directory_identity(path) != expected:
            raise GenerationError('parent-created child directory was replaced')


def child_profile(executable, reads, writes):
    """macOS development profile; system runtime remains explicitly trusted."""
    quote = lambda path: json.dumps(str(Path(path).resolve(strict=True)))
    return '\n'.join([
        '(version 1)', '(deny default)', '(import "system.sb")', '(deny network*)',
        '(deny network-outbound (literal "/private/var/run/syslog"))',
        '(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))',
        '(deny file-write* (subpath "/cores"))',
        '(allow process-exec (literal ' + quote(executable) + '))',
        '(allow file-read* (literal ' + quote(executable) + ')' + ''.join(' (subpath ' + quote(p) + ')' for p in [*reads, *writes]) + ')',
        '(allow file-read-metadata' + ''.join(' (path-ancestors ' + quote(p) + ')' for p in [executable, *reads, *writes]) + ')',
        '(allow file-write* ' + ' '.join('(require-all (subpath ' + quote(p) + ') (require-not (literal ' + quote(p) + ')))' for p in writes) + ')',
    ]) + '\n'


def verify_confinement(value):
    closed(value, ['profile', 'runtimeFiles', 'sandboxExecutable', 'timeoutSeconds'], 'child confinement')
    if value['profile'] != 'macos-seatbelt-development-1' or sys.platform != 'darwin' or type(value['timeoutSeconds']) is not int or value['timeoutSeconds'] != 300:
        raise GenerationError('unselected generator child confinement profile')
    if type(value['runtimeFiles']) is not list:
        raise GenerationError('confinement runtime files must be a list')
    for row in [*value['runtimeFiles'], value['sandboxExecutable']]:
        closed(row, ['path', 'sha256', 'bytes'], 'confinement runtime pin')
    paths = ['/System/Library/CoreServices/SystemVersion.plist', '/System/Library/Sandbox/Profiles/dyld-support.sb', '/System/Library/Sandbox/Profiles/system.sb']
    if [row['path'] for row in value['runtimeFiles']] != paths:
        raise GenerationError('unselected confinement runtime files')
    rows = [*value['runtimeFiles'], value['sandboxExecutable']]
    if value['sandboxExecutable'].get('path') != '/usr/bin/sandbox-exec':
        raise GenerationError('unselected confinement executable')
    for row in rows:
        closed(row, ['path', 'sha256', 'bytes'], 'confinement runtime pin')
        raw = Path(row['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest(row['sha256']) or type(row['bytes']) is not int or len(raw) != row['bytes']:
            raise GenerationError('confinement runtime changed')


def verify_python_profile(value):
    closed(value, ['schemaVersion', 'profile', 'standing', 'executable', 'library', 'files', 'directories', 'metadataLandmark'], 'Python profile')
    if type(value['schemaVersion']) is not int or value['schemaVersion'] != 1 or value['profile'] != 'cpython-3.14.6-macos-preparation-1':
        raise GenerationError('unselected Python preparation profile')
    for row in [value['executable'], value['library']]:
        closed(row, ['path', 'sha256', 'bytes'], 'Python executable/library pin')
        if type(row['path']) is not str:
            raise GenerationError('Python runtime path must be text')
    library = Path(value['library']['path'])
    prefix = library.parent
    if library.name != 'Python' or value['executable']['path'] != str(prefix / 'Resources/Python.app/Contents/MacOS/Python'):
        raise GenerationError('Python executable/framework profile mismatch')
    stdlib = prefix / 'lib/python3.14'
    files = value['files']
    if type(files) is not list or len(files) != 28:
        raise GenerationError('Python preparation module count changed')
    for row in files:
        closed(row, ['path', 'sha256', 'bytes'], 'Python module pin')
        if type(row['path']) is not str:
            raise GenerationError('Python module path must be text')
    sorted_unique([row['path'] for row in files], 'Python module paths')
    for row in files:
        path = Path(row['path'])
        if not path.is_relative_to(stdlib) or 'site-packages' in path.parts or not (path.suffix == '.py' or path.suffix == '.so'):
            raise GenerationError('Python module outside selected standard library')
    if value['directories'] != sorted({str(Path(row['path']).parent) for row in files}):
        raise GenerationError('Python directory grants differ from selected module parents')
    if value['metadataLandmark'] != str(stdlib / 'os.py'):
        raise GenerationError('Python prefix landmark mismatch')
    for row in [value['executable'], value['library'], *files]:
        closed(row, ['path', 'sha256', 'bytes'], 'Python runtime pin')
        path = Path(row['path'])
        if not path.is_absolute() or path.resolve(strict=True) != path or not path.is_file():
            raise GenerationError('Python runtime path is not canonical regular file')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest(row['sha256']) or type(row['bytes']) is not int or len(raw) != row['bytes']:
            raise GenerationError('Python preparation runtime changed')


def python_child_profile(value, entry, raw_schemas, options, code, output):
    verify_python_profile(value)
    paths = [value['executable']['path'], value['library']['path'], *[row['path'] for row in value['files']],
             *value['directories'], str(entry), str(raw_schemas), str(options), str(code / 'prepare.py'), str(code / 'runtime/schema.ts')]
    quote = lambda path: json.dumps(str(Path(path).resolve(strict=True)))
    return '\n'.join([
        '(version 1)', '(deny default)', '(import "system.sb")', '(deny network*)',
        '(deny network-outbound (literal "/private/var/run/syslog"))',
        '(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))',
        '(deny file-write* (subpath "/cores"))',
        '(allow process-exec (literal ' + quote(value['executable']['path']) + '))',
        '(allow file-read* ' + ' '.join('(literal ' + quote(path) + ')' for path in paths) + ')',
        '(allow file-read* (subpath ' + quote(output) + '))',
        '(allow file-write* (require-all (subpath ' + quote(output) + ') (require-not (literal ' + quote(output) + '))))',
        '(allow file-read-metadata (literal ' + quote(value['metadataLandmark']) + '))',
        '(allow file-read-metadata ' + ' '.join('(path-ancestors ' + quote(path) + ')' for path in [*paths, str(output), value['metadataLandmark']]) + ')',
    ]) + '\n'


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
        if type(row['sourcePath']) is not str or not row['sourcePath'].startswith('schemas/sources/'):
            raise GenerationError('source outside schemas/sources')
        local(root,row['semanticValidatorOwner'],existing=False)
        if not row['semanticValidatorOwner'].startswith(('crates/','apps/','providers/')) or not row['semanticValidatorOwner'].endswith(('.rs','.ts')):
            raise GenerationError('semantic owner is not a product source path')
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
            expected_roles = (['module-index'] if path == 'crates/contracts/src/generated/mod.rs'
                else ['carrier', 'shape-validator'] if path == 'apps/report/src/generated/report.ts'
                else ['carrier'])
            if output['roles'] != expected_roles:
                raise GenerationError('output roles differ from owned contract: '+path)
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


def generate(root, *, generator, node, write):
    if not sys.flags.isolated or sys.flags.optimize:
        raise GenerationError('invoke Python with -I and without optimization')
    value, sources, recipes, registry_sha = registry(root)
    if len(recipes) != 1 or recipes[0][0]['recipeId'] != 'contracts-v1':
        raise GenerationError('this adapter implements only contracts-v1')
    row, options = recipes[0]
    if set(row['sourceSha256s']) != set(sources):
        raise GenerationError('contracts-v1 requires the exact selected source closure')
    closure_raw = checked(root, 'tools/contracts/generator-closure.json', row['generatorClosureSha256'])
    closure = decode(closure_raw)
    closed(closure, ['schemaVersion', 'files', 'toolchain', 'typescriptPackageFiles', 'hostProfile', 'nativeLibraries', 'confinement'], 'generator closure')
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
    required = {'tools/contracts/prepare-inputs.py','tools/contracts/python-profile.json','tools/build_contracts.py','tools/contracts/build-receipt.json','schemas/source-map.json','tools/generate_contracts.py','tools/contracts/adapter.py','tools/contracts/prepare.py',
        'tools/contracts/render-types.cjs','tools/contracts/generate-ts.cjs','tools/contracts/validate-schemas.cjs',
        'tools/contracts/package.json','tools/contracts/pnpm-lock.yaml','tools/contracts/pnpm-workspace.yaml',
        'tools/contracts/Cargo.toml','tools/contracts/Cargo.lock','tools/contracts/src/main.rs',
        'tools/contracts/src/presence.rs','tools/contracts/src/integers.rs',
        'tools/contracts/runtime/exact-json.ts','tools/contracts/runtime/schema.ts',
        'tools/contracts/runtime/patterns.ts','tools/contracts/runtime/pattern-profile.json'}
    if set(pinned) != required:
        raise GenerationError('generator source closure differs from adapter input set')
    paths = {'generator': generator, 'node': node, 'python':sys.executable}
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
    if closure['nativeLibraries'] != []:
        raise GenerationError('in-process formatter selects no non-system native libraries')
    verify_confinement(closure['confinement'])
    with tempfile.TemporaryDirectory(prefix='opensip-contracts-') as tmp:
        work = Path(tmp).resolve()
        for name, raw in pinned.items():
            dst=work/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        # Code now runs only from its verified snapshot. Provisioning/install and
        # compiling the generator are separate explicit operations, never hidden
        # in a drift check or an ordinary consumer build.
        adapter = import_file(work/'tools/contracts/adapter.py','contracts_adapter')
        adapter.validate_build_receipt(decode(pinned['tools/contracts/build-receipt.json']), pinned, closure['toolchain']['generator'])
        adapter.validate_options(options,sources)
        adapter.validate_source_map(decode(pinned['schemas/source-map.json']),sources,options)
        adapter.copy_typescript(root/'tools/contracts/node_modules/typescript',
            work/'tools/contracts/node_modules/typescript',closure['typescriptPackageFiles'])
        original_inputs=work/'source-inputs';original_inputs.mkdir()
        options_raw=(json.dumps(options,ensure_ascii=True)+'\n').encode()
        schemas_raw=(json.dumps([v[1].decode('utf-8') for v in sources.values()],ensure_ascii=True)+'\n').encode()
        options_path=original_inputs/'options.json';options_path.write_bytes(options_raw)
        schemas_path=original_inputs/'raw-schemas.json';schemas_path.write_bytes(schemas_raw)
        prepared_output=work/'prepared-output';prepared_output.mkdir()
        python_cwd=work/'python-cwd';python_cwd.mkdir()
        python_profile=decode(pinned['tools/contracts/python-profile.json'])
        code=work/'tools/contracts';entry=code/'prepare-inputs.py'
        profile_path=work/'python-profile.sb'
        profile_path.write_text(python_child_profile(python_profile,entry,schemas_path,options_path,code,prepared_output))
        preparation=subprocess.run(['/usr/bin/sandbox-exec','-f',str(profile_path),python_profile['executable']['path'],
            '-I','-B','-S',str(entry),str(schemas_path),str(options_path),str(code),str(prepared_output)],
            cwd=python_cwd,env={},stdin=subprocess.DEVNULL,close_fds=True,capture_output=True,text=True,
            timeout=closure['confinement']['timeoutSeconds'])
        if preparation.returncode:
            raise GenerationError('Python preparation failed: '+preparation.stderr.strip())
        verify_python_profile(python_profile)
        prepared=collect_outputs(prepared_output,{'owners.json','rust-projection.json','ts-projection.json'})
        if prepared['owners.json'] != (json.dumps(options['owners'], indent=2)+'\n').encode():
            raise GenerationError('prepared owner mapping differs from parent options')
        inputs=work/'inputs';inputs.mkdir()
        for name,raw in prepared.items(): (inputs/name).write_bytes(raw)
        (inputs/'options.json').write_bytes(options_raw)
        (inputs/'raw-schemas.json').write_bytes(schemas_raw)
        provenance={'registrySha256':registry_sha,'generatorClosureSha256':row['generatorClosureSha256']}
        (inputs/'provenance.json').write_text(json.dumps(provenance)+'\n')
        executables={}
        for key in ('generator','node'):
            path=work/key;path.write_bytes(executable_bytes[key]);path.chmod(0o700);executables[key]=str(path)
        home=work/'home';home.mkdir()
        env={'PATH':'/usr/bin:/bin','HOME':str(home),'LANG':'C','LC_ALL':'C','TZ':'UTC'}
        output=work/'output';output.mkdir()
        scratch=work/'runtime-scratch';scratch.mkdir()
        directory_roots = {path: directory_identity(path) for path in (output, scratch, home)}
        def run(argv, reads, writes):
            verify_directory_roots(directory_roots)
            profile=work/'child-profile.sb'
            profile.write_text(child_profile(argv[0], reads, writes))
            result = subprocess.run(['/usr/bin/sandbox-exec','-f',str(profile),*argv], cwd=scratch,
                env=env, stdin=subprocess.DEVNULL, close_fds=True, capture_output=True, text=True,
                timeout=closure['confinement']['timeoutSeconds'])
            verify_directory_roots(directory_roots)
            if result.returncode:
                raise GenerationError('generator child failed: ' + result.stderr.strip())
        code=work/'tools/contracts'
        run([executables['node'],str(code/'validate-schemas.cjs'),str(inputs),str(scratch)], [code,inputs], [scratch])
        run([executables['generator'],str(inputs),str(output)], [inputs], [output])
        run([executables['node'],str(code/'generate-ts.cjs'),str(inputs),str(output)], [code,inputs], [output])
        verify_confinement(closure['confinement'])
        expected={o['path'] for o in row['outputs']}
        actual=collect_outputs(output, expected)
        if len(actual) != 8:
            raise GenerationError('generator emitted a different output set')
        header='// Generated by contracts-v1; inert carriers, not admission.\n// Registry SHA-256: '+registry_sha+'\n// Generator closure SHA-256: '+row['generatorClosureSha256']+'\n'
        for name in sorted(actual):
            if name.endswith('.rs'):
                text=actual[name].decode('utf-8')
                if '\n' not in text:
                    raise GenerationError('generated Rust header missing')
                actual[name]=(header+text.split('\n',1)[1]).encode('utf-8')
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
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    try:
        generate(args.root.resolve(),generator=args.generator,node=args.node,write=args.write)
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        parser.exit(1,'generation refused: '+str(exc)+'\n')


if __name__ == '__main__':
    main()
