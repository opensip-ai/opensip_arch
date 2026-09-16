"""Regular independent capture of the application-successor root into this runtime.

usage: python -I -B capture_app_root.py
Source (read only): /tmp/opensip-design-corrections/application-successor-root.v2 (every regular file, including
pre-existing __pycache__ bytes, is captured so the capture is complete). Each file is written from bytes read once,
re-hashed, and checked for a distinct inode and nlink 1. Nothing is written to the source.
"""
import hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-application39-summary-author.v1')
SRC = Path('/tmp/opensip-design-corrections/application-successor-root.v2')
DST = RT / 'work/application-successor-root.v2'


def sha(b):
    return hashlib.sha256(b).hexdigest()


if DST.exists():
    raise SystemExit('refusing to overwrite ' + str(DST))
rows, bad, symlinks = {}, [], []
for d, ds, fs in os.walk(SRC):
    for n in ds + fs:
        if os.path.islink(os.path.join(d, n)):
            symlinks.append(os.path.relpath(os.path.join(d, n), SRC))
    for f in fs:
        sp = Path(d) / f
        if sp.is_symlink():
            continue
        rel = str(sp.relative_to(SRC))
        data = sp.read_bytes()
        rows[rel] = sha(data)
        dp = DST / rel
        dp.parent.mkdir(parents=True, exist_ok=True)
        dp.write_bytes(data)
        os.chmod(dp, os.stat(sp).st_mode & 0o777 | 0o200)
        st_s, st_d = os.stat(sp), os.stat(dp)
        if st_d.st_ino == st_s.st_ino or st_d.st_nlink != 1 or sha(dp.read_bytes()) != rows[rel]:
            bad.append(rel)
digest = sha(''.join(p + '\t' + h + '\n' for p, h in sorted(rows.items())).encode())
res = {'source': str(SRC), 'capture': str(DST), 'files': len(rows), 'symlinks': symlinks, 'copyNotIndependentOrMismatch': bad,
       'manifestDigest': digest, 'manifestDigestRecipe': 'sha256 of sorted lines path<TAB>sha256<LF>', 'hashes': dict(sorted(rows.items()))}
(RT / 'receipts').mkdir(parents=True, exist_ok=True)
(RT / 'receipts/app-root-capture.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()}, indent=1))
sys.exit(1 if (bad or symlinks) else 0)
