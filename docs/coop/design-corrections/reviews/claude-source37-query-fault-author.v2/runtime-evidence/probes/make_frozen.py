"""Verified frozen37 baseline tree (no overlay) for attributing a pre-existing failure. Writes only under this runtime."""
import hashlib, json, os, shutil, sys

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v2'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v37'
MAN37 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
DEST = RT + '/work/source37-frozen'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and 'sha256' in o[0]:
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x


assert sha(MAN37) == '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
want = {r['path']: r['sha256'] for r in rows(json.load(open(MAN37)))}
if os.path.exists(DEST):
    sys.exit('refusing to reuse ' + DEST)
bad = []
for p, s in want.items():
    src = os.path.join(SRC, p)
    if not os.path.isfile(src) or sha(src) != s:
        bad.append(p)
        continue
    os.makedirs(os.path.dirname(os.path.join(DEST, p)), exist_ok=True)
    shutil.copyfile(src, os.path.join(DEST, p))
extra = []
for d, ds, fs in os.walk(SRC):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), SRC)
        if rel not in want:
            extra.append(rel)
post = [p for p, s in want.items() if sha(os.path.join(DEST, p)) != s]
res = {'manifestSha256': sha(MAN37), 'entries': len(want), 'sourceMismatch': bad, 'sourceUnlisted': extra, 'copyMismatch': post, 'dest': DEST}
json.dump(res, open(RT + '/receipts/copy-frozen37.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
assert not bad and not extra and not post
