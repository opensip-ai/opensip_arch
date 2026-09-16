"""Check the contracts dependency and resolved-feature selection for one workspace.

This developer check complements review. It is not a runtime sandbox or proof
that arbitrary native code has no effects.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tomllib


class DependencyError(ValueError):
    pass


def check(metadata, lock, policy):
    packages = {row['id']: row for row in metadata['packages']}
    nodes = {row['id']: row for row in metadata['resolve']['nodes']}
    roots = [row for row in packages.values() if row['name'] == policy['subjectPackage']]
    if len(roots) != 1:
        raise DependencyError('expected exactly one contracts package')
    root = roots[0]
    targets = [target for target in root['targets'] if target['kind'] not in (['test'], ['bench'], ['example'])]
    if len(targets) != 1 or targets[0]['kind'] != ['lib']:
        raise DependencyError('contracts production package must have one library target')
    declared_dev = policy.get('devDependencies')
    if declared_dev != []:
        raise DependencyError('this contracts profile selects no development dependencies')
    if any(edge.get('kind') == 'dev' for edge in root['dependencies']):
        raise DependencyError('unselected contracts development dependency')
    if nodes[root['id']]['features'] != policy.get('subjectResolvedFeatures'):
        raise DependencyError('unselected contracts root features')
    if root['features'] != policy.get('subjectDeclaredFeatures'):
        raise DependencyError('unselected declared contracts features')
    fields=('name','source','req','kind','rename','optional','uses_default_features','features','target')
    actual_direct=[{key:row[key] for key in fields} for row in root['dependencies'] if row['kind']!='dev']
    if actual_direct != policy.get('directDependencies'):
        raise DependencyError('unselected declared direct dependency or feature')
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
            wanted = sorted(policy['resolvedFeatures'][package['name']])
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
    return {'passed': True, 'package': root['name'], 'dependencyCount': len(found),
            'features': {name: features for (name, _), features in sorted(found.items())},
            'productQualification': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--policy', type=Path, default=Path(__file__).resolve().parent / 'contracts/dependency-policy.json')
    args = parser.parse_args()
    try:
        raw = subprocess.check_output([args.cargo, 'metadata', '--locked', '--offline', '--format-version', '1',
                                       '--filter-platform', args.target, '--manifest-path', str(args.manifest.resolve())])
        metadata = json.loads(raw)
        lock_path = Path(metadata['workspace_root']) / 'Cargo.lock'
        result = check(metadata, tomllib.loads(lock_path.read_text()), json.loads(args.policy.read_bytes()))
        result.update(workspace=metadata['workspace_root'], target=args.target)
        print(json.dumps(result, sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'dependency check refused: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
