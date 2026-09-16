"""Offline explicit wheel materialization; never called during generation/build.

The caller selects the lock bytes and supplies the downloaded wheel directory.
No package manager, setup code, entry point, .pth file or network is executed.
"""
from pathlib import Path, PurePosixPath
import argparse
import base64
import csv
import hashlib
import io
import json
import os
import platform
import re
import shutil
import stat
import sys
import tempfile
import zipfile


def read_regular(path, limit):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > limit:
            raise ValueError('nonregular, linked or oversized provisioning input')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            raise ValueError('provisioning input exceeds bound')
        return raw
    finally:
        os.close(fd)


def member_path(name):
    if not isinstance(name, str) or not name or not name.isascii() or '\\' in name or '\0' in name or ':' in name:
        raise ValueError('noncanonical wheel member')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or path.as_posix() != name:
        raise ValueError('escaping or noncanonical wheel member')
    return name


def provision(lock_path, wheel_dir, destination):
    if not sys.flags.isolated or sys.flags.optimize:
        raise ValueError('isolated Python without optimization required')
    lock = json.loads(read_regular(lock_path, 1024 * 1024))
    if lock['schemaVersion'] != 1 or lock['hostProfile'] != {'os': sys.platform, 'machine': platform.machine(), 'python': list(sys.version_info[:2])}:
        raise ValueError('unselected provisioning host')
    if len(lock['wheels']) != 5:
        raise ValueError('exact five wheel closure required')
    materialized = {}
    distributions = []
    for wheel in lock['wheels']:
        filename = member_path(wheel['filename'])
        if '/' in filename or not filename.endswith('.whl'):
            raise ValueError('wheel filename required')
        archive = read_regular(wheel_dir / filename, 16 * 1024 * 1024)
        if len(archive) != wheel['bytes'] or hashlib.sha256(archive).hexdigest() != wheel['sha256']:
            raise ValueError('wheel archive bytes differ')
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            infos = z.infolist()
            names = [member_path(i.filename) for i in infos]
            if len(names) > 512 or len(names) != len(set(names)) or sum(i.file_size for i in infos) > 64 * 1024 * 1024:
                raise ValueError('wheel member set or byte budget invalid')
            for info in infos:
                mode = info.external_attr >> 16
                if info.is_dir() or (stat.S_IFMT(mode) not in (0, stat.S_IFREG)) or info.file_size > 16 * 1024 * 1024:
                    raise ValueError('nonregular or oversized wheel member')
            records = [n for n in names if n.endswith('.dist-info/RECORD')]
            if len(records) != 1:
                raise ValueError('one wheel RECORD required')
            rows = list(csv.reader(io.StringIO(z.read(records[0]).decode('utf-8'))))
            if any(len(row) != 3 for row in rows) or len(rows) != len(names) or len({r[0] for r in rows}) != len(rows):
                raise ValueError('invalid RECORD rows')
            record = {r[0]: (r[1], r[2]) for r in rows}
            if set(record) != set(names):
                raise ValueError('RECORD does not cover exact archive')
            selected = []
            for name in names:
                raw = z.read(name)
                digest, length = record[name]
                if name == records[0]:
                    if digest or length:
                        raise ValueError('RECORD self-entry must be unhashed')
                    continue
                expected = 'sha256=' + base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip('=')
                if digest != expected or not re.fullmatch(r'0|[1-9][0-9]*', length) or len(raw) != int(length):
                    raise ValueError('wheel member integrity mismatch')
                if name in materialized:
                    raise ValueError('duplicate cross-wheel member')
                materialized[name] = raw
                selected.append(name)
            distributions.append({'name': wheel['name'], 'version': wheel['version'], 'files': sorted(selected), 'excludedNonModuleOrBytecode': [records[0]]})
    actual = [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} for name, raw in sorted(materialized.items())]
    if actual != lock['files']:
        raise ValueError('materialized runtime snapshot differs from lock')
    # Validate every member before writing. Publish one fresh directory only.
    if destination.exists() or destination.is_symlink():
        raise ValueError('fresh provisioning destination required')
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.python-provision-', dir=destination.parent))
    try:
        for name, raw in materialized.items():
            path = stage / 'python-packages' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        manifest = {'schemaVersion': 1, 'standing': 'Runtime snapshot extracted from explicitly pinned wheels; no installer execution', 'distributions': distributions, 'files': actual}
        (stage / 'python-packages.json').write_text(json.dumps(manifest, indent=2) + '\n')
        # Existing targets are never replaced. The parent output directory is
        # controlled by this explicit developer operation, not repository input.
        if destination.exists() or destination.is_symlink():
            raise ValueError('provisioning destination appeared')
        stage.rename(destination)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {'wheels': len(distributions), 'runtimeFiles': len(actual)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path, required=True)
    parser.add_argument('--wheel-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(provision(args.lock, args.wheel_dir, args.output)))
