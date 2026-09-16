"""Explicit macOS development child boundary, not release qualification."""
from pathlib import Path
import hashlib
import json
import stat
import sys
import os
import selectors
import signal
import subprocess
import time


def capture_child(argv, *, cwd, env, timeout=300, max_bytes=8 * 1024 * 1024):
    """Drain both pipes with one byte/time budget; kill the group on refusal.

    Log files are written by the parent. Giving a confined Node process a file
    descriptor for a disallowed parent log can abort its stdio initialization.
    """
    buffers = [bytearray(), bytearray()]
    failure = None
    deadline = time.monotonic() + timeout
    with subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          close_fds=True, start_new_session=True) as child:
        try:
            with selectors.DefaultSelector() as selector:
                for index, stream in enumerate((child.stdout, child.stderr)):
                    os.set_blocking(stream.fileno(), False)
                    selector.register(stream, selectors.EVENT_READ, index)
                remaining = max_bytes
                while selector.get_map():
                    left = deadline - time.monotonic()
                    if left <= 0:
                        failure = 'child time limit exceeded'
                        break
                    for key, _ in selector.select(min(left, 1)):
                        data = os.read(key.fileobj.fileno(), min(65536, remaining + 1))
                        if not data:
                            selector.unregister(key.fileobj)
                            continue
                        buffers[key.data].extend(data[:remaining])
                        remaining -= len(data)
                        if remaining < 0:
                            failure = 'child combined log byte limit exceeded'
                            break
                    if failure:
                        break
                if not failure:
                    try:
                        child.wait(timeout=max(0, deadline-time.monotonic()))
                    except subprocess.TimeoutExpired:
                        failure = 'child time limit exceeded'
        finally:
            if failure or child.poll() is None:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            child.wait()
        return child.returncode, bytes(buffers[0]), bytes(buffers[1]), failure


def verify_runtime(profile):
    if sys.platform != 'darwin' or profile['profile'] != 'cpython-3.14.6-macos-native-renderer-development-1':
        raise ValueError('unselected Python runtime profile')
    paths = []
    for row in [profile['executable'], profile['library'], *profile['files'], *profile['nativeLibraries']]:
        p = Path(row['path'])
        if not p.is_absolute() or p.resolve(strict=True) != p or not stat.S_ISREG(p.lstat().st_mode):
            raise ValueError('noncanonical Python runtime file')
        b = p.read_bytes()
        if type(row['bytes']) is not int or len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
            raise ValueError('Python runtime bytes changed')
        paths.append(p)
    for row in profile['nativeAliases']:
        if str(Path(row['path']).resolve(strict=True)) != row['target'] or Path(row['target']) not in paths:
            raise ValueError('Python native library alias changed')
    return sorted(set(paths))


def python_profile(profile, reads, output):
    files = verify_runtime(profile)
    # Literal module grants avoid reading ambient .pyc, site-packages or modules
    # outside the selected list. Directories are readable for import discovery.
    directories = sorted(set(p.parent for p in files))
    literal = files + directories
    aliases = [row['path'] for row in profile['nativeAliases']]
    q = lambda p: json.dumps(str(Path(p).resolve(strict=True)))
    lines = [
        '(version 1)', '(deny default)', '(import "system.sb")', '(deny network*)',
        '(deny network-outbound (literal "/private/var/run/syslog"))',
        '(deny file-read* (literal "/private/etc/passwd") (literal "/private/etc/master.passwd"))',
        '(deny file-write* (subpath "/cores"))',
        '(allow process-exec (literal ' + q(profile['executable']['path']) + '))',
        '(allow file-read* ' + ' '.join('(literal ' + q(p) + ')' for p in literal) + ')',
        '(allow file-read* ' + ' '.join('(literal ' + json.dumps(p) + ')' for p in aliases) + ')',
        '(allow file-read* ' + ' '.join('(subpath ' + q(p) + ')' for p in [*reads, output]) + ')',
        '(allow file-read-metadata ' + ' '.join('(path-ancestors ' + q(p) + ')' for p in [*literal, *reads, output]) + ')',
        '(allow file-read-metadata ' + ' '.join('(path-ancestors ' + json.dumps(p) + ')' for p in aliases) + ')',
        '(allow file-write* (require-all (subpath ' + q(output) + ') (require-not (literal ' + q(output) + '))))',
    ]
    return '\n'.join(lines) + '\n'
