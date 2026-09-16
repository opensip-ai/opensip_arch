"""Explicit offline generator build from locked dependency archive bytes.

The receipt records an observed trusted-host build, not reproducible-build proof.
No build or dependency installation is performed by a normal product build.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
import tomllib


class BuildError(ValueError):
    pass


SOURCES = ('Cargo.toml', 'Cargo.lock', 'src/main.rs', 'src/presence.rs', 'src/integers.rs')


def pin(raw):
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def unpack_archive(raw, name, version, checksum, destination):
    if pin(raw)['sha256'] != checksum:
        raise BuildError('dependency archive checksum mismatch: ' + name)
    prefix = name + '-' + version
    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        for member in archive:
            path = PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != prefix:
                raise BuildError('unsafe dependency archive path')
            if member.isdir():
                continue
            if not member.isfile() or len(path.parts) < 2:
                raise BuildError('nonregular dependency archive member')
            relative = '/'.join(path.parts[1:])
            if relative in files or relative == '.cargo-checksum.json':
                raise BuildError('duplicate or reserved archive member')
            reader = archive.extractfile(member)
            if reader is None:
                raise BuildError('unreadable archive member')
            content = reader.read()
            files[relative] = content
    if 'Cargo.toml' not in files:
        raise BuildError('archive lacks package manifest')
    # No writes until every member and the entire archive digest are admitted.
    destination.mkdir()
    for relative, content in files.items():
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(content)
    checksums = {name: pin(content)['sha256'] for name, content in sorted(files.items())}
    (destination / '.cargo-checksum.json').write_text(json.dumps({'files': checksums, 'package': checksum}) + '\n')
    return {'name': name, 'version': version, **pin(raw), 'fileCount': len(files)}


def build(root, archives, cargo, rustc, output):
    if not sys.flags.isolated or sys.flags.optimize:
        raise BuildError('invoke Python with -I and without optimization')
    if output.exists():
        raise BuildError('build output directory must not already exist')
    sources = {name: (root / name).read_bytes() for name in SOURCES}
    lock = tomllib.loads(sources['Cargo.lock'].decode())
    manifest = tomllib.loads(sources['Cargo.toml'].decode())
    if manifest['package']['name'] != 'opensip-contract-generator' or 'workspace' not in manifest:
        raise BuildError('expected isolated generator workspace')
    tool_paths = {'cargo': Path(cargo).resolve(strict=True), 'rustc': Path(rustc).resolve(strict=True)}
    for path in tool_paths.values():
        if not path.is_absolute() or not path.is_file():
            raise BuildError('absolute compiler executable required')
    tool_pins = {name: {'path': str(path), **pin(path.read_bytes())} for name, path in tool_paths.items()}
    packages = lock['package']
    keys = [(p['name'], p['version']) for p in packages]
    if len(keys) != len(set(keys)):
        raise BuildError('duplicate lock package')
    roots = [p for p in packages if 'source' not in p]
    if len(roots) != 1 or roots[0]['name'] != manifest['package']['name']:
        raise BuildError('unexpected path dependency in generator lock')
    with tempfile.TemporaryDirectory(prefix='opensip-generator-build-') as temporary:
        work = Path(temporary).resolve()
        project, vendor = work / 'project', work / 'vendor'
        project.mkdir(); vendor.mkdir()
        for name, content in sources.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        dependencies = []
        for package in sorted(packages, key=lambda p: (p['name'], p['version'])):
            if 'source' not in package:
                continue
            if package['source'] != 'registry+https://github.com/rust-lang/crates.io-index':
                raise BuildError('unselected dependency source')
            name, version = package['name'], package['version']
            if not re.fullmatch(r'[A-Za-z0-9_-]+', name) or not re.fullmatch(r'[A-Za-z0-9.+-]+', version):
                raise BuildError('invalid package archive name')
            raw = (archives / (name + '-' + version + '.crate')).read_bytes()
            dependencies.append(unpack_archive(raw, name, version, package['checksum'], vendor / (name + '-' + version)))
        config = '[source.crates-io]\nreplace-with = "verified-vendor"\n[source.verified-vendor]\ndirectory = ' + json.dumps(str(vendor)) + '\n'
        cargo_home = work / 'cargo-home'; cargo_home.mkdir()
        (cargo_home / 'config.toml').write_text(config)
        home = work / 'home'; home.mkdir()
        # Cargo also reads .cargo/config{,.toml} from cwd ancestors, separately
        # from CARGO_HOME. Refuse an ambient ancestor file rather than inheriting
        # wrappers, flags, sources or target settings outside the build receipt.
        for parent in (project, *project.parents):
            if any((parent / '.cargo' / name).exists() for name in ('config', 'config.toml')):
                raise BuildError('ambient ancestor Cargo configuration is not selected')
        # An empty environment excludes caller wrappers, cfg/feature overrides,
        # profiles, credentials and user/global Cargo configuration.
        env = {'PATH': '/usr/bin:/bin', 'HOME': str(home), 'CARGO_HOME': str(cargo_home),
               'CARGO_TARGET_DIR': str(work / 'target'), 'RUSTC': str(tool_paths['rustc']),
               'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC', 'CARGO_INCREMENTAL': '0'}
        versions = {}
        for name in tool_paths:
            versions[name] = subprocess.check_output([str(tool_paths[name]), '-vV'], cwd=work, env=env, text=True)
        host = next((line[6:] for line in versions['rustc'].splitlines() if line.startswith('host: ')), None)
        if not host or not re.fullmatch(r'[A-Za-z0-9_-]+', host):
            raise BuildError('compiler host target missing')
        command = [str(tool_paths['cargo']), 'build', '--locked', '--offline', '--release', '--target', host,
                   '--manifest-path', str(project / 'Cargo.toml'), '--message-format=json']
        result = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True)
        if result.returncode:
            raise BuildError('offline generator build failed: ' + result.stderr)
        artifact = work / 'target' / host / 'release' / 'opensip-contract-generator'
        binary = artifact.read_bytes()
        for name, path in tool_paths.items():
            if pin(path.read_bytes()) != {k: tool_pins[name][k] for k in ('sha256', 'bytes')}:
                raise BuildError('compiler executable changed during build')
        receipt = {'schemaVersion': 1, 'standing': 'observed offline trusted-host build; not reproducible-build or release qualification',
                   'sources': [{'path': name, **pin(raw)} for name, raw in sorted(sources.items())],
                   'builder': pin(Path(__file__).read_bytes()), 'python': pin(Path(sys.executable).read_bytes()),
                   'tools': tool_pins, 'versions': versions, 'dependencies': dependencies,
                   'target': host, 'profile': 'release', 'locked': True, 'offline': True,
                   'environment': env, 'command': command, 'vendorConfig': config,
                   'stdout': pin(result.stdout.encode()), 'stderr': pin(result.stderr.encode()),
                   'executable': pin(binary),
                   'trustedHost': 'macOS kernel, loader, system linker, compiler native libraries and build scripts; no network-effect sandbox claim for compilation'}
        output.mkdir(parents=True)
        executable = output / 'opensip-contract-generator'; executable.write_bytes(binary); executable.chmod(0o700)
        (output / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        (output / 'build.stdout.jsonl').write_text(result.stdout)
        (output / 'build.stderr.log').write_text(result.stderr)
    return {'output': str(output), 'executable': receipt['executable'], 'dependencyArchives': len(dependencies)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent / 'contracts')
    parser.add_argument('--archives', type=Path, required=True)
    parser.add_argument('--cargo', required=True)
    parser.add_argument('--rustc', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build(args.root.resolve(), args.archives.resolve(), args.cargo, args.rustc, args.output.resolve())))
    except (OSError, ValueError, KeyError, tarfile.TarError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'build refused: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
