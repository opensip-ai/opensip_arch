"""Stage pinned candidate files privately; does not select or edit a live tree."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import subprocess


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe(name):
    require(isinstance(name, str) and name and '\\' not in name, 'invalid path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == name,
            'noncanonical relative path')
    return path


def read(root, name):
    path = root
    for part in safe(name).parts:
        path = path / part
        require(not path.is_symlink(), 'linked input: ' + name)
    require(path.is_file(), 'missing regular input: ' + name)
    return path.read_bytes()


def pinned(root, row, name=None):
    raw = read(root, name or row['path'])
    require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
            'input digest mismatch: ' + (name or row['path']))
    return raw


def main():
    parser = argparse.ArgumentParser()
    for name in ('architecture', 'product', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    unit = Path(__file__).resolve().parent
    baseline = json.loads((unit / 'baseline.json').read_bytes())
    mapping = json.loads((unit / 'materialization-map.json').read_bytes())
    require(not args.output.exists(), 'output must be fresh')
    head = subprocess.check_output(['git', '-C', str(args.product), 'rev-parse', 'HEAD'], text=True).strip()
    require(head == baseline['productHead'] == mapping['baseProductHead'], 'product HEAD changed')
    tracked = set(subprocess.check_output(['git', '-C', str(args.product), 'ls-files', '-z']).decode().split('\0')[:-1])
    base = {row['path']: row for row in baseline['files']}
    require(len(base) == len(baseline['files']) and set(base) == tracked, 'baseline file set changed')
    source = {name: pinned(args.product, row) for name, row in base.items()}
    changes = {row['productPath']: row for row in mapping['files']}
    unchanged = {row['path']: row for row in mapping['unchanged']}
    require(len(changes) == len(mapping['files']) and len(unchanged) == len(mapping['unchanged']),
            'duplicate materialization path')
    require(not set(changes) & set(unchanged), 'overlapping materialization paths')
    require(set(changes) | set(unchanged) == tracked - {'design-lock.json'}, 'incomplete materialization')
    for name, row in changes.items():
        require(row['before'] == {key: base[name][key] for key in ('bytes', 'sha256')}, 'before pin differs')
        source[name] = pinned(args.architecture, row['after'], row['candidatePath'])
    for name, row in unchanged.items():
        require(row == base[name], 'unchanged baseline differs')
    # Complete verification precedes output creation. The inherited lock is
    # deliberately unchanged and does not claim this candidate is approved.
    args.output.mkdir(parents=True)
    for name, raw in source.items():
        target = args.output / safe(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        shutil.copymode(args.product / name, target)
    print(json.dumps({'passed': True, 'mapped': len(changes), 'unchangedNonLock': len(unchanged),
                      'trackedFiles': len(source), 'selected': False, 'liveProductModified': False}))


if __name__ == '__main__':
    main()
