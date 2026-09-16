"""Verify the exact reviewed pure-identity production dependency/source closure.

This developer check is source/metadata verification, not an OS sandbox,
transitive memory-safety proof, or product qualification.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib

class DependencyError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise DependencyError(message)

def relative(name):
    require(isinstance(name, str) and name and '\\' not in name and '\0' not in name,
            'invalid source path')
    require(all(p not in ('', '.', '..') for p in name.split('/')) and not name.startswith('/'),
            'unsafe source path')
    return name

def file_pin(root, row):
    path = root
    for part in relative(row['path']).split('/'):
        path = path / part
        require(not path.is_symlink(), 'linked source refused: ' + str(path))
    require(path.is_file(), 'missing source: ' + str(path))
    raw = path.read_bytes()
    require(type(row['bytes']) is int and len(raw) == row['bytes'] and
            hashlib.sha256(raw).hexdigest() == row['sha256'], 'source bytes differ: ' + str(path))

def census(root, rows, *, local):
    require(not root.is_symlink(), 'linked package root refused')
    paths = [relative(r['path']) for r in rows]
    require(paths == sorted(set(paths)) and 'Cargo.toml' in paths, 'source census must be sorted/unique')
    if local:
        observed = {'Cargo.toml'}
        roots = [root / 'src']
    else:
        observed = set()
        roots = [root]
    for directory in roots:
        require(directory.is_dir() and not directory.is_symlink(), 'missing/linked source directory')
        for path in directory.rglob('*'):
            require(not path.is_symlink(), 'linked source refused: ' + str(path))
            if path.is_file():
                name = path.relative_to(root).as_posix()
                if not local and name in ('.cargo-ok', '.cargo-checksum.json'):
                    continue
                observed.add(name)
            else:
                require(path.is_dir(), 'nonregular source refused')
    require(observed == set(paths), 'source census differs: ' + str(root))
    for row in rows:
        file_pin(root, row)
    return len(rows)

def target_sources(package, rows):
    root = Path(package['manifest_path']).parent.resolve()
    allowed = {row['path'] for row in rows}
    for target in package['targets']:
        if target['kind'] in (['test'], ['bench'], ['example']):
            continue
        try:
            source = Path(target['src_path']).resolve().relative_to(root).as_posix()
        except ValueError as exc:
            raise DependencyError('production target escapes package') from exc
        require(source in allowed, 'production target not in source census')

def check(metadata, lock, policy, archives):
    require(policy.get('schemaVersion') == 1 and policy.get('subjectPackage') == 'opensip-identity',
            'identity policy required')
    packages = {p['id']: p for p in metadata['packages']}
    nodes = {p['id']: p for p in metadata['resolve']['nodes']}
    roots = [p for p in packages.values() if p['name'] == policy['subjectPackage']]
    require(len(roots) == 1 and roots[0].get('source') is None, 'one local identity package required')
    root = roots[0]
    targets = [t for t in root['targets'] if t['kind'] not in (['test'], ['bench'], ['example'])]
    require(len(targets) == 1 and targets[0]['kind'] == ['lib'], 'one identity production lib required')
    local_count = census(Path(root['manifest_path']).parent, policy['localSources'], local=True)
    target_sources(root, policy['localSources'])
    expected = {(p['name'], p['version']): p for p in policy['dependencies']}
    require(len(expected) == len(policy['dependencies']), 'duplicate dependency policy')
    locked = {(p['name'], p['version']): p for p in lock['package']}
    require(len(locked) == len(lock['package']), 'ambiguous lock package tuples')
    visited = set()
    pending = [root['id']]
    found = set()
    source_count = local_count
    while pending:
        package_id = pending.pop()
        if package_id in visited:
            continue
        visited.add(package_id)
        package, node = packages[package_id], nodes[package_id]
        require(package.get('links') is None, 'native links not selected')
        require(not any(any(k in ('custom-build', 'proc-macro') for k in t['kind'])
                        for t in package['targets']), 'build/proc-macro target not selected')
        if package_id == root['id']:
            require(sorted(node['features']) == policy['rootFeatures'], 'identity features differ')
        else:
            key = (package['name'], package['version'])
            require(key in expected, 'unselected identity dependency: ' + repr(key))
            selected = expected[key]
            require(package.get('source') == 'registry+https://github.com/rust-lang/crates.io-index',
                    'unselected dependency source')
            pinned = locked.get(key, {})
            require(pinned.get('source') == package['source'] and
                    pinned.get('checksum') == selected['checksum'], 'registry checksum differs')
            require(sorted(node['features']) == selected['resolvedFeatures'], 'resolved features differ: ' + key[0])
            archive = archives / (key[0] + '-' + key[1] + '.crate')
            require(archive.is_file() and not archive.is_symlink(), 'missing/linked crate archive')
            require(hashlib.sha256(archive.read_bytes()).hexdigest() == selected['checksum'],
                    'crate archive checksum differs')
            source_count += census(Path(package['manifest_path']).parent, selected['sources'], local=False)
            target_sources(package, selected['sources'])
            found.add(key)
        for edge in node['deps']:
            if any(k['kind'] != 'dev' and k.get('target') != 'cfg(any())' for k in edge['dep_kinds']):
                pending.append(edge['pkg'])
    require(found == set(expected), 'identity production closure differs from selected set')
    return {'passed': True, 'package': root['name'], 'dependencyCount': len(found),
            'sourceFilesVerified': source_count, 'registryTuples': [list(k) for k in sorted(found)],
            'productQualification': False, 'memorySafetyProof': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--target', required=True)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--archives', required=True, type=Path)
    parser.add_argument('--policy', required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = subprocess.check_output([args.cargo, 'metadata', '--locked', '--offline',
                                       '--format-version', '1', '--filter-platform', args.target,
                                       '--manifest-path', str(args.manifest.resolve())])
        metadata = json.loads(raw)
        lock = tomllib.loads((Path(metadata['workspace_root']) / 'Cargo.lock').read_text())
        print(json.dumps(check(metadata, lock, json.loads(args.policy.read_bytes()), args.archives), sort_keys=True))
    except (DependencyError, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        raise SystemExit('identity dependency check failed: ' + str(exc)) from exc

if __name__ == '__main__':
    main()
