"""Verify the frozen39 manifest from LIVE and every member in its snapshot, then make this runtime's regular-file capture.

usage: python -I -B capture_frozen39.py
LIVE manifest (read only): /Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json
Snapshot (read only): manifest snapshotRoot. Every row: bytes read once, sha256 and length checked, written to
work/source/<path>, re-hashed, distinct inode and nlink 1. Extra snapshot files and symlinks are reported.
"""
import hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1')
LIVE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json')
WANT = 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'
DST = RT / 'work/source'


def sha(b):
    return hashlib.sha256(b).hexdigest()


raw = LIVE.read_bytes()
if sha(raw) != WANT:
    raise SystemExit('manifest sha mismatch')
manifest = json.loads(raw)
snap = Path(manifest['snapshotRoot'])
if DST.exists():
    raise SystemExit('refusing to overwrite ' + str(DST))
bad_hash, bad_len, missing, not_regular, copy_bad = [], [], [], [], []
total = 0
for row in manifest['files']:
    src = snap / row['path']
    if not src.exists():
        missing.append(row['path'])
        continue
    if src.is_symlink() or not src.is_file():
        not_regular.append(row['path'])
        continue
    data = src.read_bytes()
    total += len(data)
    if sha(data) != row['sha256']:
        bad_hash.append(row['path'])
    if len(data) != row['bytes']:
        bad_len.append(row['path'])
    dp = DST / row['path']
    dp.parent.mkdir(parents=True, exist_ok=True)
    dp.write_bytes(data)
    os.chmod(dp, os.stat(src).st_mode & 0o777 | 0o200)
    st_s, st_d = os.stat(src), os.stat(dp)
    if st_d.st_ino == st_s.st_ino or st_d.st_nlink != 1 or sha(dp.read_bytes()) != row['sha256']:
        copy_bad.append(row['path'])
listed = {r['path'] for r in manifest['files']}
extra = []
for d, ds, fs in os.walk(snap):
    for f in fs:
        rel = str((Path(d) / f).relative_to(snap))
        if rel not in listed:
            extra.append(rel)
res = {'liveManifest': str(LIVE), 'manifestSha256': sha(raw), 'manifestBytes': len(raw), 'snapshotRoot': str(snap),
       'members': len(manifest['files']), 'fileCountField': manifest['fileCount'], 'totalBytesField': manifest['totalBytes'],
       'bytesRead': total, 'missing': missing, 'notRegular': not_regular, 'hashMismatch': bad_hash, 'lengthMismatch': bad_len,
       'extraSnapshotFiles': extra, 'copyNotIndependentOrMismatch': copy_bad, 'capture': str(DST)}
res['ok'] = not (missing or not_regular or bad_hash or bad_len or copy_bad) and total == manifest['totalBytes'] and len(manifest['files']) == manifest['fileCount']
(RT / 'receipts').mkdir(parents=True, exist_ok=True)
(RT / 'receipts/frozen39-verify-and-capture.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
sys.exit(0 if res['ok'] else 1)
