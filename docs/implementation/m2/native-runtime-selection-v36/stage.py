"""Stage exact reviewed-candidate source bytes privately; never mutate live product.

This developer helper checks the v2 archive map and baseline. Successful staging
is source integrity evidence, not source acceptance or permission to publish.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe(name):
    p = PurePosixPath(name)
    require(not p.is_absolute() and p.parts and '..' not in p.parts
            and str(p) == name and '\\' not in name, 'unsafe member: ' + name)
    return p


def pinned(root, row):
    p = root / safe(row['path'])
    require(not p.is_symlink() and p.is_file(), 'nonregular input: ' + str(p))
    raw = p.read_bytes()
    require(digest(raw) == {k: row[k] for k in ('bytes', 'sha256')},
            'pin mismatch: ' + str(p))
    return raw


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--architecture', required=True, type=Path)
    args.add_argument('--product', required=True, type=Path)
    args.add_argument('--output', required=True, type=Path)
    a = args.parse_args()
    unit = Path(__file__).resolve().parent
    mapping = json.loads((unit / 'materialization-map.json').read_bytes())
    baseline = json.loads((unit / 'baseline.json').read_bytes())
    require(mapping['schemaVersion'] == 2, 'map version')
    require(not a.output.exists(), 'output already exists')
    head = subprocess.check_output(['git', '-C', str(a.product), 'rev-parse', 'HEAD'], text=True).strip()
    require(head == baseline['productHead'] == mapping['baseProductHead'], 'base HEAD changed')
    base = {r['path']: r for r in baseline['files']}
    tracked = subprocess.check_output(['git', '-C', str(a.product), 'ls-files', '-z']).decode().split('\0')[:-1]
    require(len(base) == len(baseline['files']) and set(base) == set(tracked), 'base file set changed')
    for row in baseline['files']:
        pinned(a.product, row)
    pinned(a.architecture, mapping['sourceArchive'])
    manifest = json.loads(pinned(a.architecture, mapping['sourceManifest']))
    rows = {r['path']: r for r in manifest['files']}
    require(len(rows) == len(manifest['files']), 'duplicate manifest member')
    archive = a.architecture / mapping['sourceArchive']['path']
    # Complete verification precedes extraction or output creation.
    with tarfile.open(archive, 'r:xz') as t:
        members = t.getmembers()
        require(len(members) == len(rows) and len({m.name for m in members}) == len(rows), 'archive member set')
        for m in members:
            safe(m.name)
            require(m.isfile() and m.name in rows, 'unexpected archive member')
            require(digest(t.extractfile(m).read()) == {k: rows[m.name][k] for k in ('bytes', 'sha256')}, 'archive member digest')
    candidate = {p[8:]: r for p, r in rows.items() if p.startswith('product/')}
    changes = {r['productPath']: r for r in mapping['files']}
    unchanged = {r['path']: r for r in mapping['unchanged']}
    require(len(changes) == len(mapping['files']) and len(unchanged) == len(mapping['unchanged']), 'duplicate map')
    require(not set(changes) & set(unchanged), 'overlapping map')
    require(set(candidate) == set(changes) | set(unchanged) | {'design-lock.json'}, 'incomplete map')
    require(set(base) <= set(candidate), 'baseline path omitted')
    for rel, row in changes.items():
        safe(rel)
        require(rel != 'design-lock.json' and row['archiveMember'] == 'product/' + rel, 'invalid mapped member')
        require(row['after'] == {k: candidate[rel][k] for k in ('bytes', 'sha256')}, 'mapped after mismatch')
        before = {k: base[rel][k] for k in ('bytes', 'sha256')} if rel in base else None
        require(before == row['before'], 'mapped before mismatch')
        require(before != row['after'], 'unchanged file in delta')
        if before is None:
            require(not (a.product / rel).exists() and not (a.product / rel).is_symlink(), 'new destination occupied')
    for rel, row in unchanged.items():
        require(row == base[rel] and {k: row[k] for k in ('bytes', 'sha256')} == {k: candidate[rel][k] for k in ('bytes', 'sha256')}, 'unchanged source mismatch')
    a.output.mkdir(parents=True)
    for rel in base:
        dst = a.output / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(a.product / rel, dst)
    with tarfile.open(archive, 'r:xz') as t:
        for m in t:
            if m.name.startswith('product/') and m.name[8:] in changes:
                raw = t.extractfile(m).read()
                require(digest(raw) == changes[m.name[8:]]['after'], 'archive changed during staging')
                dst = a.output / m.name[8:]
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(raw)
    for rel, row in candidate.items():
        if rel != 'design-lock.json':
            pinned(a.output, {**row, 'path': rel})
    require((a.output / 'design-lock.json').read_bytes() == (a.product / 'design-lock.json').read_bytes(), 'live selected lock lost')
    for row in baseline['files']:
        pinned(a.product, row)
    print(json.dumps({'staged': str(a.output), 'archiveMembersVerified': len(rows),
                      'nonLockSourceFilesVerified': len(candidate) - 1,
                      'mapped': len(changes), 'unchangedNonLock': len(unchanged),
                      'liveProductUnchanged': True, 'runtimeAcceptance': False}))


if __name__ == '__main__':
    main()
