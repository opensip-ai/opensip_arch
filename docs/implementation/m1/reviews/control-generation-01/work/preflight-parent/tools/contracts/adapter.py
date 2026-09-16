"""Closed options and materialized generator dependency checks."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tomllib


def validate_build_receipt(receipt, pinned, executable_pin):
    """Join reviewed build evidence to this recipe; not remote attestation."""
    fields = {'schemaVersion', 'standing', 'sources', 'builder', 'python', 'tools', 'versions',
              'dependencies', 'target', 'profile', 'locked', 'offline', 'environment', 'command',
              'vendorConfig', 'stdout', 'stderr', 'executable', 'trustedHost'}
    if type(receipt) is not dict or set(receipt) != fields or type(receipt['schemaVersion']) is not int or receipt['schemaVersion'] != 1:
        raise ValueError('unsupported generator build receipt')
    def pin(raw):
        return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    expected_sources = [{'path': name, **pin(pinned['tools/contracts/' + name])}
                        for name in ('Cargo.lock', 'Cargo.toml', 'src/integers.rs', 'src/main.rs', 'src/presence.rs')]
    if receipt['sources'] != expected_sources:
        raise ValueError('generator build receipt source mismatch')
    if receipt['builder'] != pin(pinned['tools/build_contracts.py']):
        raise ValueError('generator build receipt builder mismatch')
    if receipt['executable'] != executable_pin:
        raise ValueError('generator build receipt executable mismatch')
    if receipt['profile'] != 'release' or receipt['locked'] is not True or receipt['offline'] is not True:
        raise ValueError('unselected generator build profile')
    lock = tomllib.loads(pinned['tools/contracts/Cargo.lock'].decode())
    expected = sorted((p['name'], p['version'], p['checksum']) for p in lock['package'] if 'source' in p)
    actual = []
    for row in receipt['dependencies']:
        if set(row) != {'name', 'version', 'sha256', 'bytes', 'fileCount'} or type(row['bytes']) is not int or row['bytes'] <= 0 or type(row['fileCount']) is not int or row['fileCount'] <= 0:
            raise ValueError('invalid generator build dependency receipt')
        actual.append((row['name'], row['version'], row['sha256']))
    if actual != expected:
        raise ValueError('generator build receipt dependency mismatch')


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
    superseded=sorted('urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/'+name
        for name in ('HelloV3','HelloAckV3','ProtocolLimitsV3'))
    if options['deniedRefs'] != superseded:
        raise ValueError('native2 handshakes must remain superseded by provider-handshake1')
    if not options['providerEntryPoints'] or not set(options['providerEntryPoints']) <= set(refs) or any(ref == denied or ref.startswith(denied + '/') for ref in refs for denied in options['deniedRefs']):
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


def validate_source_map(mapping, sources, options):
    if type(mapping) is not dict or set(mapping)!={'schemaVersion','sources'} or type(mapping['schemaVersion']) is not int or mapping['schemaVersion']!=1:
        raise ValueError('unsupported source map')
    if type(mapping['sources']) is not list:
        raise ValueError('invalid source map rows')
    owners={row['schemaId']:row for row in options['owners']}
    actual={}
    for row in mapping['sources']:
        keys={'implementationPath','architectureSource','declaredMajor','namespace','module','standing','schemaId','profile','semanticValidatorOwner'}
        if type(row) is not dict or set(row)!=keys or row['implementationPath'] in actual:
            raise ValueError('invalid or duplicate source map row')
        pin=row['architectureSource']
        if type(pin) is not dict or set(pin)!={'path','sha256','bytes'} or type(pin['bytes']) is not int:
            raise ValueError('invalid architecture source pin')
        name=pin['path']
        if type(name) is not str or not name.startswith('docs/') or '\\' in name or str(Path(name))!=name or any(part in ('','.','..') for part in name.split('/')):
            raise ValueError('invalid architecture source path')
        actual[row['implementationPath']]=row
    if set(actual)!={row['sourcePath'] for row,_,_ in sources.values()}:
        raise ValueError('source map coverage differs from registry')
    for row,raw,_ in sources.values():
        mapped=actual[row['sourcePath']];pin=mapped['architectureSource']
        if pin['sha256']!=row['sourceSha256'] or pin['bytes']!=len(raw):
            raise ValueError('source map bytes differ from registry')
        if any(mapped[key]!=row[key] for key in ('schemaId','declaredMajor','profile','semanticValidatorOwner')):
            raise ValueError('source map owner differs from registry')
        if any(mapped[key]!=owners[row['schemaId']][key] for key in ('namespace','module')):
            raise ValueError('source map module differs from options')
