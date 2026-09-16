"""Initial parent custody for frozen source38 and creation of an independent regular-copy work tree.

usage: python -I -B setup_work.py
Verifies the source38 manifest bytes and every listed file once, then copies file contents (read/write of bytes, not
hardlinks/clones) into work/source38-work, verifying each copy's hash and that its inode differs from the parent.
"""
import hashlib, json, os, sys

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v38'
WANT = '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'
DST = RT + '/work/source38-work'


def sha_bytes(b):
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


man_bytes = open(MAN, 'rb').read()
res = {'manifest': MAN, 'manifestSha256': sha_bytes(man_bytes), 'expected': WANT}
res['manifestOk'] = res['manifestSha256'] == WANT
if not res['manifestOk']:
    print(json.dumps(res, indent=1))
    sys.exit(2)
listed = {x['path']: x['sha256'] for x in rows(json.loads(man_bytes))}
if os.path.exists(DST):
    print('work tree already exists; refusing to overwrite', DST)
    sys.exit(3)
bad, copied, linked = [], 0, []
for rel, want in sorted(listed.items()):
    sp = os.path.join(SRC, rel)
    data = open(sp, 'rb').read()
    if sha_bytes(data) != want:
        bad.append(rel)
        continue
    dp = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    with open(dp, 'wb') as f:
        f.write(data)
    os.chmod(dp, os.stat(sp).st_mode & 0o777 | 0o200)
    st_s, st_d = os.stat(sp), os.stat(dp)
    if st_d.st_ino == st_s.st_ino or st_d.st_nlink != 1 or sha_bytes(open(dp, 'rb').read()) != want:
        linked.append(rel)
    copied += 1
unlisted = []
for d, ds, fs in os.walk(SRC):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), SRC)
        if rel not in listed:
            unlisted.append(rel)
res.update({'entries': len(listed), 'parentMismatch': bad, 'parentUnlisted': unlisted, 'copied': copied,
            'copyNotIndependentOrMismatch': linked, 'workTree': DST})
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/parent-custody-and-copy.json', 'w'), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in res.items()}, indent=1))
