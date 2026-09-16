"""Closed options and materialized generator dependency checks."""
import hashlib
import json
from pathlib import Path
import re
import shutil


def validate_options(options, sources):
    keys = {'schemaVersion','standing','owners','entryPoints','deniedRefs','providerEntryPoints','reportEntryPoint','openObligations','sourceMappings'}
    if type(options) is not dict or set(options) != keys or type(options['schemaVersion']) is not int or options['schemaVersion'] != 1:
        raise ValueError('unsupported generator options')
    source_rows = [row for row, _, _ in sources.values()]
    fields = ('schemaId','declaredMajor','profile','semanticValidatorOwner')
    expected = sorted(({k: row[k] for k in fields} for row in source_rows),key=lambda row: row['schemaId'])
    if options['sourceMappings'] != expected:
        raise ValueError('source major/profile/semantic owner differs from selected options')
    owners = {}
    namespaces = set()
    for row in options['owners']:
        if type(row) is not dict or set(row) != {'schemaId','namespace','module'}:
            raise ValueError('invalid source owner row')
        namespace = row['namespace']
        if not isinstance(namespace,str) or not re.fullmatch('[A-Z][A-Za-z0-9]*',namespace):
            raise ValueError('invalid type namespace')
        if row['schemaId'] in owners or namespace in namespaces or row['module'] not in ('evidence','identity','invocation','output','protocol'):
            raise ValueError('duplicate or invalid source owner')
        owners[row['schemaId']] = row
        namespaces.add(namespace)
    if set(owners) != {r['schemaId'] for r in source_rows}:
        raise ValueError('source owner coverage mismatch')
    # Prefix overlap would make Rust impl ownership ambiguous.
    if any(a != b and a.startswith(b) for a in namespaces for b in namespaces):
        raise ValueError('ambiguous type namespace prefixes')
    refs = []
    names = set()
    for row in options['entryPoints']:
        if type(row) is not dict or set(row) != {'ref','typeName','module'}:
            raise ValueError('invalid entrypoint row')
        ref, name = row['ref'], row['typeName']
        if not isinstance(ref,str) or ref.count('#') != 1 or not isinstance(name,str) or not re.fullmatch('[A-Z][A-Za-z0-9]*',name):
            raise ValueError('invalid entrypoint ref/name')
        owner = owners.get(ref.split('#')[0])
        if not owner or not name.startswith(owner['namespace']) or row['module'] != owner['module'] or name in names:
            raise ValueError('entrypoint ownership or unique name mismatch')
        refs.append(ref);names.add(name)
    if not refs or refs != sorted(set(refs)):
        raise ValueError('entrypoints must be sorted unique')
    for key in ('providerEntryPoints','deniedRefs'):
        rows=options[key]
        if type(rows) is not list or any(type(x) is not str for x in rows) or rows != sorted(set(rows)):
            raise ValueError('invalid '+key)
    if not options['providerEntryPoints'] or not set(options['providerEntryPoints']) <= set(refs) or set(options['deniedRefs']) & set(refs):
        raise ValueError('invalid provider roots or superseded selection')
    if options['reportEntryPoint'] not in refs:
        raise ValueError('report root lacks explicit owner')
    if type(options['standing']) is not str or type(options['openObligations']) is not list:
        raise ValueError('options status malformed')


def tree_files(root):
    """Regular package files only; no symlink traversal or undeclared side inputs."""
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('symlink in materialized dependency tree')
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError('nonregular dependency input')
        raw=p.read_bytes()
        rows.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    if not rows:
        raise ValueError('empty materialized dependency')
    return rows


def copy_typescript(source, destination, expected):
    # pnpm's package entry is a symlink; only its resolved in-workspace package
    # content is admitted. Nested links and unknown additional files refuse.
    package=source.resolve(strict=True)
    workspace=source.parents[1].resolve(strict=True)
    if not package.is_relative_to(workspace):
        raise ValueError('TypeScript resolves outside its tooling workspace')
    if tree_files(package) != expected:
        raise ValueError('materialized TypeScript package differs from pinned closure')
    shutil.copytree(package,destination)
    if tree_files(destination) != expected:
        raise ValueError('TypeScript package changed during snapshot')
