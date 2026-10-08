#!/usr/bin/env python3
"""Check the actual C3a inflater graph against its exact selected P0 rows.

Read-only: accepts already captured locked/offline Cargo metadata. It neither
runs Cargo nor grants source, native launch, component or custody authority.
"""
import argparse
import hashlib
import json
import io
import tarfile
from pathlib import Path
import tomllib


def check(repository, metadata, policy, cargo_home):
    rows = {row['name']: row for row in policy['rows']}
    if set(rows) != {'miniz_oxide', 'adler2'}:
        raise ValueError('selected inflater closure must contain exactly two rows')
    packages = {p['id']: p for p in metadata['packages']}
    nodes = {node['id']: node for node in metadata['resolve']['nodes']}
    ids = {}
    for name, row in rows.items():
        matches = [p for p in packages.values() if p['name'] == name]
        if len(matches) != 1:
            raise ValueError(f'{name}: one exact version required')
        package = matches[0]
        if package['version'] != row['version'] or package['source'] != row['source']:
            raise ValueError(f'{name}: selected version/source mismatch')
        if package['links'] is not None or any('custom-build' in t['kind'] for t in package['targets']):
            raise ValueError(f'{name}: build script/links outside selection')
        if nodes[package['id']]['features'] != row['resolvedFeatures']:
            raise ValueError(f'{name}: resolved features outside selection')
        archives = list((cargo_home / 'registry/cache').glob('*/' + name + '-' + row['version'] + '.crate'))
        if len(archives) != 1:
            raise ValueError(f'{name}: unique selected original cached archive required')
        raw = archives[0].read_bytes()
        if len(raw) != row['archiveBytes'] or hashlib.sha256(raw).hexdigest() != row['checksum']:
            raise ValueError(f'{name}: archive pin mismatch')
        source_root = Path(package['manifest_path']).parent
        original_files = set()
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
            prefix = name + '-' + row['version'] + '/'
            for member in archive:
                if not member.isfile() or not member.name.startswith(prefix):
                    raise ValueError(f'{name}: unexpected original archive member')
                relative = member.name[len(prefix):]
                if not relative or any(part in {'', '.', '..'} for part in relative.split('/')) or relative in original_files:
                    raise ValueError(f'{name}: ambiguous original archive path')
                original_files.add(relative)
                actual = source_root / relative
                if actual.is_symlink() or not actual.is_file() or actual.read_bytes() != archive.extractfile(member).read():
                    raise ValueError(f'{name}: compiled source bytes differ from selected archive: {relative}')
        actual_files = {p.relative_to(source_root).as_posix() for p in source_root.rglob('*') if p.is_file()}
        if actual_files - original_files - {'.cargo-ok', '.cargo-checksum.json'}:
            raise ValueError(f'{name}: extra extracted source files outside original archive')
        manifest = tomllib.loads((source_root / 'Cargo.toml').read_text())
        if manifest['package'].get('build', False) is not False or manifest['package'].get('links'):
            raise ValueError(f'{name}: unexpected manifest build/links')
        lib = (source_root / 'src/lib.rs').read_text()
        if '#![forbid(unsafe_code)]' not in lib:
            raise ValueError(f'{name}: selected unsafe-code refusal missing')
        if any(p.suffix.lower() in {'.c', '.cc', '.cpp', '.s', '.asm'} for p in source_root.rglob('*') if p.is_file()):
            raise ValueError(f'{name}: native source outside P0 selection')
        ids[name] = package['id']
    for name, identity in ids.items():
        dependency_names = sorted(packages[d['pkg']]['name'] for d in nodes[identity]['deps'])
        if dependency_names != sorted(rows[name]['dependencies']):
            raise ValueError(f'{name}: actual external closure differs from selected row')
    host = None
    for identity in metadata['workspace_members']:
        package = packages[identity]
        path = Path(package['manifest_path'])
        if not path.is_relative_to(repository):
            raise ValueError('workspace manifest outside actual repository')
        doc = tomllib.loads(path.read_text())
        declarations = []
        for table in [doc, *doc.get('target', {}).values()]:
            for field in ['dependencies', 'dev-dependencies', 'build-dependencies']:
                for name, declaration in table.get(field, {}).items():
                    actual = declaration.get('package', name) if isinstance(declaration, dict) else name
                    if actual in rows:
                        declarations.append((actual, field, declaration))
        if package['name'] == 'opensip-host':
            host = package
            if declarations != [('miniz_oxide', 'dependencies', {'version': '=0.9.1', 'default-features': False})]:
                raise ValueError('host must declare only the exact no-feature P0 inflater row')
        elif declarations:
            raise ValueError('P0 inflater declared by another workspace consumer')
    if host is None or ids['miniz_oxide'] not in [d['pkg'] for d in nodes[host['id']]['deps']]:
        raise ValueError('actual host graph does not contain the selected inflater')
    lock = tomllib.loads((repository / 'Cargo.lock').read_text())
    for name, row in rows.items():
        selected = [p for p in lock['package'] if p['name'] == name]
        if len(selected) != 1 or any(selected[0].get(k) != row[k] for k in ['version', 'source', 'checksum']):
            raise ValueError(f'{name}: Cargo.lock closure pin mismatch')
    return {'passed': True, 'consumer': 'opensip-host', 'linkingScope': 'C3a decoder library',
            'selectedRows': 2, 'resolvedOptionalFeatures': [], 'productQualification': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--policy', type=Path, required=True)
    parser.add_argument('--cargo-home', type=Path, required=True)
    args = parser.parse_args()
    result = check(args.repository.resolve(), json.loads(args.metadata.read_text()),
                   json.loads(args.policy.read_text()), args.cargo_home)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
