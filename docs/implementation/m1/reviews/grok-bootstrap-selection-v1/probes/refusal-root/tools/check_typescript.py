"""Run selected TypeScript lanes after actual design approval verification.

Explicit developer maintenance command. The reviewed checkout is the trust
anchor; this does not execute analyzed repository modules or install packages.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import signal
import stat
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def closed(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(label + ': unexpected fields')


def local(root, name):
    if (not isinstance(name, str) or not name or '\\' in name or '\0' in name
            or any(part in ('', '.', '..') for part in name.split('/'))):
        raise ValueError('canonical relative path required')
    current = root
    for part in name.split('/'):
        current = current / part
        if current.is_symlink():
            raise ValueError('linked input refused: ' + name)
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError('regular input required: ' + name)
    return current


def pinned(root, pin):
    closed(pin, ('path', 'bytes', 'sha256'), 'input pin')
    if (type(pin['bytes']) is not int or pin['bytes'] < 0
            or not isinstance(pin['sha256'], str) or len(pin['sha256']) != 64
            or any(c not in '0123456789abcdef' for c in pin['sha256'])):
        raise ValueError('malformed input pin')
    raw = local(root, pin['path']).read_bytes()
    if len(raw) != pin['bytes'] or hashlib.sha256(raw).hexdigest() != pin['sha256']:
        raise ValueError('input bytes differ: ' + pin['path'])
    return raw


def terminate(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def check(args):
    if not sys.flags.isolated or sys.flags.optimize:
        raise ValueError('isolated Python without optimization required')
    # Caller --root cannot choose the executable preflight module.
    spec = importlib.util.spec_from_file_location('design_preflight', HERE / 'verify_design.py')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    root = args.root.resolve(strict=True)
    architecture = args.architecture.resolve(strict=True)
    lock_path = local(root, 'design-lock.json')
    approval = verifier.verify(architecture, verifier.decode(lock_path.read_bytes()), root)
    raw = local(root, 'tools/typescript-lanes.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    selected = [row for unit in approval['contractSuccessors'] for row in unit['inputs']
                if row['sha256'] == digest and row['bytes'] == len(raw)]
    if len(selected) != 1:
        raise ValueError('TypeScript lane registry is not selected exactly once by an accepted design unit')
    registry = verifier.decode(raw)
    closed(registry, ('schemaVersion', 'node', 'files', 'lanes'), 'lane registry')
    if type(registry['schemaVersion']) is not int or registry['schemaVersion'] != 1:
        raise ValueError('unsupported lane registry')
    if not isinstance(registry['files'], list) or not registry['files']:
        raise ValueError('checker input closure required')
    paths = [row['path'] for row in registry['files']]
    if paths != sorted(set(paths)):
        raise ValueError('checker input pins must be sorted and unique')
    inputs = {row['path']: pinned(root, row) for row in registry['files']}
    for rel, actual in [('tools/check_typescript.py', Path(__file__)),
                        ('tools/verify_design.py', HERE / 'verify_design.py')]:
        if inputs.get(rel) != actual.read_bytes():
            raise ValueError('trusted entry point differs from selected closure: ' + rel)
    entry = 'tools/typescript-boundary/bin/check-boundary.mjs'
    if entry not in inputs:
        raise ValueError('checker entry point absent from selected closure')
    closed(registry['node'], ('bytes', 'sha256'), 'Node pin')
    executable = args.node.resolve(strict=True)
    info = executable.stat()
    if (not stat.S_ISREG(info.st_mode) or type(registry['node']['bytes']) is not int
            or info.st_size != registry['node']['bytes']):
        raise ValueError('Node executable type/length differs from selected pin')
    node_raw = executable.read_bytes()
    if (type(registry['node']['bytes']) is not int
            or len(node_raw) != registry['node']['bytes']
            or hashlib.sha256(node_raw).hexdigest() != registry['node']['sha256']):
        raise ValueError('Node executable differs from selected pin')
    lanes = registry['lanes']
    if not isinstance(lanes, list) or not lanes:
        raise ValueError('at least one lane required')
    names = []
    for lane in lanes:
        closed(lane, ('name', 'record', 'toolPolicy'), 'lane')
        if not isinstance(lane['name'], str) or not lane['name'] or lane['name'] in names:
            raise ValueError('unique nonempty lane names required')
        names.append(lane['name'])
        if lane['toolPolicy'] is not None and not isinstance(lane['toolPolicy'], str):
            raise ValueError('toolPolicy must be an architecture path or null')
    if args.lane is not None and args.lane not in names:
        raise ValueError('unknown selected lane')
    # No ambient NODE_OPTIONS, NODE_PATH, ESBUILD_BINARY_PATH or user npm config.
    # This is trusted-tool execution, not a malicious-tool sandbox or a claim
    # that every dynamic third-party loader is statically enumerated.
    env = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC'}
    results = []
    with tempfile.TemporaryDirectory(prefix='opensip-typescript-check-') as temp:
        for index, lane in enumerate(lanes):
            if args.lane is not None and lane['name'] != args.lane:
                continue
            record = Path(temp) / (str(index) + '.json')
            record.write_text(json.dumps(lane['record']) + '\n')
            command = [str(executable), str(root / entry), '--root', str(root),
                       '--lane-record', str(record), '--design-lock', str(lock_path),
                       '--architecture', str(architecture)]
            if lane['toolPolicy'] is not None:
                command.extend(['--tool-policy', lane['toolPolicy']])
            # Stream diagnostics without retaining unbounded output in memory.
            process = subprocess.Popen(command, cwd=root, env=env, start_new_session=True)
            try:
                code = process.wait(timeout=300)
            except subprocess.TimeoutExpired:
                terminate(process)
                code = 124
            except BaseException:
                terminate(process)
                raise
            results.append({'lane': lane['name'], 'exitCode': code})
    return {'passed': all(row['exitCode'] == 0 for row in results), 'lanes': results,
            'registrySha256': digest,
            'standing': 'Selected developer boundary checks; unresolved loader limitations remain in checker output.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=HERE.parent)
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--node', type=Path, required=True)
    parser.add_argument('--lane', help='Check one selected lane; default checks all selected lanes')
    result = check(parser.parse_args())
    print(json.dumps(result))
    sys.exit(0 if result['passed'] else 1)
