"""Check declared and resolved internal Cargo edges against the selected inventory.

Read-only developer check. This covers Cargo manifests/metadata, including
inactive optional and target/dev/build declarations. It does not inspect macro
expansion or prove native code purity. External dependency/feature review and
source import checks are separate requirements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tomllib


class BoundaryError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise BoundaryError(message)


def explicit(value):
    if isinstance(value, dict):
        require(value.get('workspace') is not True, 'package manifests must not inherit workspace values')
        for child in value.values():
            explicit(child)
    elif isinstance(value, list):
        for child in value:
            explicit(child)


def manifest_internal_edges(document, directory, paths, policy, name):
    """Read inactive declarations too; stale metadata cannot hide a new edge."""
    found = []
    tables = [(None, document), *document.get('target', {}).items()]
    for target, table in tables:
        for section, kind in [('dependencies', None), ('build-dependencies', 'build'), ('build_dependencies', 'build'), ('dev-dependencies', 'dev'), ('dev_dependencies', 'dev')]:
            for alias, raw in table.get(section, {}).items():
                dep = {'version': raw} if isinstance(raw, str) else raw
                owner = dep.get('package', alias)
                dep_path = dep.get('path')
                if dep_path is None:
                    require(owner not in policy, 'internal manifest dependency must name its local owner path')
                    continue
                path = (directory / dep_path).resolve(strict=True)
                require(paths.get(path) == owner, 'unknown manifest local dependency owner')
                require(owner in policy[name]['dependencies'], 'forbidden manifest internal edge: ' + name + ' -> ' + owner)
                found.append((owner, alias, str(path), kind, target, dep.get('optional', False)))
    return found


def check(repository: Path, metadata, inventory, lane):
    repository = repository.resolve(strict=True)
    require(lane in ('host', 'rust-provider'), 'unknown Cargo lane')
    rows = inventory['packages']
    policy = {row['id']: row for row in rows if row['kind'] in ('rust-library', 'rust-binary')}
    require(len(policy) == sum(row['kind'] in ('rust-library', 'rust-binary') for row in rows), 'duplicate inventory package')
    paths = {}
    for name, row in policy.items():
        path = (repository / row['path']).resolve()
        require(path.is_relative_to(repository), 'inventory package path escapes repository')
        require(path not in paths, 'duplicate inventory package path')
        paths[path] = name
        require(len(row['dependencies']) == len(set(row['dependencies'])) and set(row['dependencies']) <= policy.keys(), 'invalid inventory edge')
    packages = {row['id']: row for row in metadata['packages']}
    require(len(packages) == len(metadata['packages']), 'duplicate Cargo package id')
    local = {}
    declarations = []
    for package_id, package in packages.items():
        name = package['name']
        if package['source'] is not None:
            require(name not in policy, 'registry package shadows an internal owner')
            continue
        manifest = Path(package['manifest_path']).resolve(strict=True)
        require(paths.get(manifest.parent) == name and manifest.name == 'Cargo.toml', 'unknown or relocated local package')
        require(name not in local.values(), 'duplicate local package owner')
        local[package_id] = name
        manifest_doc = tomllib.loads(manifest.read_text())
        explicit(manifest_doc)
        require(manifest_doc['package']['name'] == name, 'metadata package differs from manifest')
        for target in package['targets']:
            require(Path(target['src_path']).resolve(strict=True).is_relative_to(manifest.parent), 'Cargo target crosses package source boundary')
        observed = []
        for dep in package['dependencies']:
            dep_path = dep.get('path')
            if dep_path is None:
                require(dep['name'] not in policy, 'internal dependency must name its local owner path')
                continue
            target = paths.get(Path(dep_path).resolve(strict=True))
            require(target is not None and target == dep['name'], 'unknown or aliased local dependency owner')
            require(target in policy[name]['dependencies'], 'forbidden declared internal edge: ' + name + ' -> ' + target)
            require(dep.get('kind') in (None, 'build', 'dev'), 'unknown Cargo dependency kind')
            observed.append((target, dep.get('rename') or dep['name'], str(Path(dep_path).resolve()), dep.get('kind'), dep.get('target'), dep.get('optional', False)))
            declarations.append({'from': name, 'to': target, 'kind': dep.get('kind'), 'target': dep.get('target'), 'optional': dep.get('optional'), 'rename': dep.get('rename')})
        declared = manifest_internal_edges(manifest_doc, manifest.parent, paths, policy, name)
        require(len(observed) == len(set(observed)) and set(observed) == set(declared), 'Cargo metadata internal declarations differ from current manifest')
    workspace_ids = metadata['workspace_members']
    require(len(workspace_ids) == len(set(workspace_ids)), 'duplicate workspace member')
    require(set(workspace_ids) <= local.keys(), 'workspace contains an unowned member')
    workspace_names = {local[pid] for pid in workspace_ids}
    allowed = {'opensip-rust-provider'} if lane == 'rust-provider' else set(policy) - {'opensip-rust-provider'}
    require(bool(workspace_names) and workspace_names <= allowed, 'workspace crosses host/provider boundary')
    require(set(metadata['workspace_default_members']) <= set(workspace_ids), 'default member outside workspace')
    expected_root = repository / 'providers/rust' if lane == 'rust-provider' else repository
    require(Path(metadata['workspace_root']).resolve() == expected_root, 'unexpected workspace root')
    nodes = {node['id']: node for node in metadata['resolve']['nodes']}
    require(len(nodes) == len(metadata['resolve']['nodes']) and nodes.keys() <= packages.keys(), 'invalid resolve graph')
    require(local.keys() <= nodes.keys(), 'local package missing from resolve graph')
    resolved = []
    for source, node in nodes.items():
        for edge in node['deps']:
            require(edge['pkg'] in packages, 'unresolved Cargo package id')
            if edge['pkg'] not in local:
                continue
            require(source in local, 'external package imports a local product owner')
            a, b = local[source], local[edge['pkg']]
            require(b in policy[a]['dependencies'], 'forbidden resolved internal edge: ' + a + ' -> ' + b)
            resolved.append({'from': a, 'to': b, 'kinds': edge['dep_kinds']})
    return {'passed': True, 'lane': lane, 'workspacePackages': sorted(workspace_names),
            'localPackages': sorted(local.values()), 'declaredInternalEdges': declarations,
            'resolvedInternalEdges': resolved, 'sourcePurityQualified': False, 'productQualification': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True, type=Path)
    parser.add_argument('--metadata', required=True, type=Path, help='Cargo metadata --locked --offline --format-version 1 from this exact workspace')
    parser.add_argument('--inventory', required=True, type=Path, help='Inventory selected by the separate design verification preflight')
    parser.add_argument('--lane', required=True, choices=('host', 'rust-provider'))
    args = parser.parse_args()
    try:
        result = check(args.repository, json.loads(args.metadata.read_bytes()), json.loads(args.inventory.read_bytes()), args.lane)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, 'package boundary check refused: ' + str(exc) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
