"""Custody + regular copy of the retained v1 work tree into this v2 runtime.

usage: python -I -B setup_v2.py
Expected bytes: every source38 manifest path; the 21 v1 changed files use v1 receipts/final-custody-and-diff.json workSha256.
Each copied file is written from bytes read once, re-hashed, and checked for a distinct inode and nlink 1. v1 is never written.
"""
import hashlib, json, os, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2')
V1 = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
SRC = V1 / 'work/source38-work'
DST = RT / 'work/source38-work'
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
WANT = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


man_raw = MAN.read_bytes()
if sha(man_raw) != WANT:
    raise SystemExit('source38 manifest mismatch')
expected = {x['path']: x['sha256'] for x in rows(json.loads(man_raw))}
v1_final_raw = (V1 / 'receipts/final-custody-and-diff.json').read_bytes()
v1_final = json.loads(v1_final_raw)
v1_changed = {r['path']: r['workSha256'] for r in v1_final['changedFiles']}
expected.update(v1_changed)
if DST.exists():
    raise SystemExit('refusing to overwrite ' + str(DST))
names = set()
bad, linked, copied = [], [], 0
for d, ds, fs in os.walk(SRC):
    for f in fs:
        sp = Path(d) / f
        rel = str(sp.relative_to(SRC))
        names.add(rel)
        data = sp.read_bytes()
        if expected.get(rel) != sha(data):
            bad.append(rel)
        dp = DST / rel
        dp.parent.mkdir(parents=True, exist_ok=True)
        dp.write_bytes(data)
        os.chmod(dp, os.stat(sp).st_mode & 0o777 | 0o200)
        st_s, st_d = os.stat(sp), os.stat(dp)
        if st_d.st_ino == st_s.st_ino or st_d.st_nlink != 1 or sha(dp.read_bytes()) != expected.get(rel):
            linked.append(rel)
        copied += 1
res = {'source38ManifestSha256': sha(man_raw), 'manifestOk': True, 'v1FinalCustodySha256': sha(v1_final_raw), 'v1ChangedFiles': len(v1_changed),
       'copied': copied, 'expectedPaths': len(expected), 'mismatch': bad, 'missing': sorted(set(expected) - names), 'unexpected': sorted(names - set(expected)),
       'copyNotIndependent': linked, 'workTree': str(DST)}
(RT / 'receipts').mkdir(parents=True, exist_ok=True)
(RT / 'receipts/v1-custody-and-copy.json').write_text(json.dumps(res, indent=1) + '\n')
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in res.items()}, indent=1))
sys.exit(1 if (bad or linked or res['missing'] or res['unexpected']) else 0)
