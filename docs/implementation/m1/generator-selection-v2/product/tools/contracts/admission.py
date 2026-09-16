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

