"""Custody + regular independent copy of the fixed successor capture's core docs into this runtime.

usage: python -I -B setup_copy.py
Source (read only): /tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source
Excluded: docs/coop/design-corrections/reviews/** (historical evidence), hashed for custody but not copied.
Every copied file is written from bytes read once, re-hashed, and checked for a distinct inode and nlink 1.
"""
import hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1')
SRC = Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
DST = RT / 'work/source'
EXCLUDE = 'docs/coop/design-corrections/reviews/'


def sha(b):
    return hashlib.sha256(b).hexdigest()


if DST.exists():
    raise SystemExit('refusing to overwrite ' + str(DST))
full, core, bad, symlinks = {}, {}, [], []
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
        full[rel] = sha(data)
        if rel.startswith(EXCLUDE):
            continue
        core[rel] = full[rel]
        dp = DST / rel
        dp.parent.mkdir(parents=True, exist_ok=True)
        dp.write_bytes(data)
        os.chmod(dp, os.stat(sp).st_mode & 0o777 | 0o200)
        st_s, st_d = os.stat(sp), os.stat(dp)
        if st_d.st_ino == st_s.st_ino or st_d.st_nlink != 1 or sha(dp.read_bytes()) != core[rel]:
            bad.append(rel)


def manifest_digest(rows):
    return sha(''.join(p + '\t' + h + '\n' for p, h in sorted(rows.items())).encode())


res = {'source': str(SRC), 'work': str(DST), 'excludedPrefix': EXCLUDE, 'symlinks': symlinks,
       'sourceFiles': len(full), 'excludedFiles': len(full) - len(core), 'copiedFiles': len(core), 'copyNotIndependentOrMismatch': bad,
       'sourceFullManifestDigest': manifest_digest(full), 'coreManifestDigest': manifest_digest(core),
       'manifestDigestRecipe': 'sha256 of sorted lines "path<TAB>sha256<LF>"', 'core': core}
(RT / 'receipts').mkdir(parents=True, exist_ok=True)
(RT / 'receipts/source-custody-and-copy.json').write_text(json.dumps(res, indent=1) + '\n')
(RT / 'receipts/source-full-manifest.json').write_text(json.dumps(full, indent=1, sort_keys=True) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()}, indent=1))
sys.exit(1 if (bad or symlinks) else 0)
