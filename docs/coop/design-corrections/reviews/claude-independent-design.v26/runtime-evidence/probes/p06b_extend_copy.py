"""Probe 06b — extend the disposable copy to every pinned path the checkers require
(the whole docs/ tree except the huge historical reviews/ subtree), then re-verify
EVERY copied byte against the frozen manifest before any checker runs.
The pin gate is satisfied by supplying the pinned bytes, never by editing the gate."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
DST = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
EXCLUDE_PREFIX = 'docs/coop/design-corrections/reviews/'

man = {r['path']: r for r in json.load(open(MAN))['files']}
copied = 0
skipped = 0
for dp, dn, fn in os.walk(os.path.join(SRC, 'docs')):
    for f in fn:
        s = os.path.join(dp, f)
        rel = os.path.relpath(s, SRC)
        if rel.startswith(EXCLUDE_PREFIX):
            skipped += 1
            continue
        d = os.path.join(DST, rel)
        if os.path.isfile(d):
            continue
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        copied += 1

bad, verified = [], 0
for dp, dn, fn in os.walk(DST):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, DST)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rec = man.get(rel)
        if rec is None:
            bad.append(('not-in-manifest', rel))
        elif rec['sha256'] != h or rec['bytes'] != os.path.getsize(p):
            bad.append(('hash-or-length', rel))
        else:
            verified += 1

res = {'newlyCopied': copied, 'skippedReviewFiles': skipped,
       'totalVerifiedAgainstFrozenManifest': verified,
       'mismatchCount': len(bad), 'mismatches': bad[:20]}
json.dump(res, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/disposable-copy-verification-2.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
