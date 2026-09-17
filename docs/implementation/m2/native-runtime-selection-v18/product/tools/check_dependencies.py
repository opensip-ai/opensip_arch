"""Check the contracts dependency and resolved-feature selection for one workspace.

This developer check complements review. It is not a runtime sandbox or proof
that arbitrary native code has no effects.
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


def check_sources(package, policy):
    """Enforce the exact previously reviewed local source set, not a text lint."""
    if policy.get('schemaVersion') != 2 or package.get('source') is not None:
        raise DependencyError('selected local contracts source profile required')
    manifest = Path(package['manifest_path'])
    directory = manifest.parent
    rows = policy['localSources']
    if (not isinstance(rows, list) or not rows
            or any(not isinstance(row, dict) or set(row) != {'path', 'bytes', 'sha256'}
                   or not isinstance(row['path'], str) for row in rows)):
        raise DependencyError('invalid local source pins')
    paths = [row['path'] for row in rows]
    if paths != sorted(set(paths)) or 'Cargo.toml' not in paths:
        raise DependencyError('local source pins must be sorted, unique and include manifest')
    observed = {'Cargo.toml'}
    for file in (directory / 'src').rglob('*'):
        if file.is_symlink():
            raise DependencyError('linked contracts source refused')
        if file.is_file():
            observed.add(file.relative_to(directory).as_posix())
        elif not file.is_dir():
            raise DependencyError('nonregular contracts source refused')
    if observed != set(paths):
        raise DependencyError('local contracts source set differs from reviewed selection')
    for row in rows:
        name = row['path']
        if (set(row) != {'path', 'bytes', 'sha256'} or not isinstance(name, str)
                or not name or '\\' in name or '\0' in name
                or any(part in ('', '.', '..') for part in name.split('/'))):
            raise DependencyError('invalid local source pin')
        file = directory
        for part in name.split('/'):
            file = file / part
            if file.is_symlink():
                raise DependencyError('linked contracts source refused')
        raw = file.read_bytes()
        if (type(row['bytes']) is not int or len(raw) != row['bytes']
                or hashlib.sha256(raw).hexdigest() != row['sha256']):
            raise DependencyError('local contracts source bytes differ: ' + name)
    return len(rows)


def check(metadata, lock, policy, *, feature_profile='standalone'):
    # The caller selects one exact reviewed lane; never accept a union or
    # automatically fall back to whichever profile fits the observed metadata.
    profiles = {'standalone': policy['resolvedFeatures']}
    additional = policy.get('resolvedFeatureProfiles', {})
    if not isinstance(additional, dict) or 'standalone' in additional:
        raise DependencyError('invalid resolved feature profiles')
    profiles.update(additional)
    if feature_profile not in profiles:
        raise DependencyError('unknown resolved feature profile: ' + feature_profile)
    selected_features = profiles[feature_profile]
    names = {row['name'] for row in policy['dependencies']}
    if (not isinstance(selected_features, dict) or set(selected_features) != names
            or any(not isinstance(fs, list) or any(not isinstance(f, str) for f in fs)
                   or fs != sorted(set(fs)) for fs in selected_features.values())):
        raise DependencyError('feature profile must cover the exact dependency set with sorted unique features')
    packages = {row['id']: row for row in metadata['packages']}
    nodes = {row['id']: row for row in metadata['resolve']['nodes']}
    roots = [row for row in packages.values() if row['name'] == policy['subjectPackage']]
    if len(roots) != 1:
        raise DependencyError('expected exactly one contracts package')
    root = roots[0]
    sources = check_sources(root, policy)
    targets = [target for target in root['targets'] if target['kind'] not in (['test'], ['bench'], ['example'])]
    if len(targets) != 1 or targets[0]['kind'] != ['lib']:
        raise DependencyError('contracts production package must have one library target')
    expected = {(row['name'], row['version']): row for row in policy['dependencies']}
    if len(expected) != len(policy['dependencies']):
        raise DependencyError('duplicate dependency policy row')
    lock_rows = {(row['name'], row['version']): row for row in lock['package']}
    pending = [root['id']]
    seen = set()
    found = {}
    while pending:
        package_id = pending.pop()
        if package_id in seen:
            continue
        seen.add(package_id)
        package, node = packages[package_id], nodes[package_id]
        if package_id != root['id']:
            key = (package['name'], package['version'])
            if key not in expected or package.get('source') != 'registry+https://github.com/rust-lang/crates.io-index':
                raise DependencyError('unselected contracts dependency: ' + str(key))
            pinned = lock_rows.get(key, {})
            if pinned.get('source') != package['source'] or pinned.get('checksum') != expected[key]['checksum']:
                raise DependencyError('dependency source/checksum mismatch: ' + str(key))
            if package.get('links') is not None:
                raise DependencyError('native linked dependency is not selected')
            actual = sorted(node['features'])
            wanted = selected_features[package['name']]
            if actual != wanted:
                raise DependencyError('unselected resolved features: ' + package['name'] + ' ' + str(actual))
            found[key] = actual
        for edge in node['deps']:
            # The caller requests a concrete filter-platform. cfg(any()) is the
            # known false version-coupling edge, never a compiled dependency.
            kinds = [kind for kind in edge['dep_kinds'] if kind['kind'] != 'dev' and kind.get('target') != 'cfg(any())']
            if kinds:
                pending.append(edge['pkg'])
    if set(found) != set(expected):
        raise DependencyError('resolved contracts closure differs from selected closure')
    return {'passed': True, 'featureProfile': feature_profile, 'package': root['name'], 'dependencyCount': len(found), 'localSourceFilesVerified': sources,
            'features': {name: features for (name, _), features in sorted(found.items())},
            'productQualification': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--policy', type=Path, default=Path(__file__).resolve().parent / 'contracts/dependency-policy.json')
    parser.add_argument('--feature-profile', default='standalone',
                        help='Explicit reviewed profile; standalone is the conservative default')
    args = parser.parse_args()
    try:
        raw = subprocess.check_output([args.cargo, 'metadata', '--locked', '--offline', '--format-version', '1',
                                       '--filter-platform', args.target, '--manifest-path', str(args.manifest.resolve())])
        metadata = json.loads(raw)
        lock_path = Path(metadata['workspace_root']) / 'Cargo.lock'
        result = check(metadata, tomllib.loads(lock_path.read_text()), json.loads(args.policy.read_bytes()), feature_profile=args.feature_profile)
        result.update(workspace=metadata['workspace_root'], target=args.target)
        print(json.dumps(result, sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'dependency check refused: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
