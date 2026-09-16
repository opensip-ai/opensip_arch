"""Probe 06d — supply exactly the three pinned review files the pin gates require.
The gate is satisfied with the frozen bytes, never by editing the gate."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
DST = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
man = {r['path']: r for r in json.load(open(MAN))['files']}
NEED = [
    'docs/coop/design-corrections/reviews/native-author-feedback.v1.md',
    'docs/coop/design-corrections/reviews/security-author-feedback.v1.md',
    'docs/coop/design-corrections/reviews/workflows-author-feedback.v1.md',
]
for rel in NEED:
    s = os.path.join(SRC, rel)
    h = hashlib.sha256(open(s, 'rb').read()).hexdigest()
    assert h == man[rel]['sha256'] and os.path.getsize(s) == man[rel]['bytes'], rel
    d = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
    print('supplied pinned file', rel, h[:16])

bad, verified = [], 0
for dp, dn, fn in os.walk(DST):
    for f in fn:
        p = os.path.join(dp, f)
        r = os.path.relpath(p, DST)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rec = man.get(r)
        if rec is None or rec['sha256'] != h or rec['bytes'] != os.path.getsize(p):
            bad.append(r)
        else:
            verified += 1
print('copy verified=%d mismatches=%d' % (verified, len(bad)), bad[:5])
