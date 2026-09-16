"""Probe 06c — restore the one report file the refused run rewrote INSIDE THE COPY,
and re-confirm the FROZEN snapshot itself is byte-unchanged."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
DST = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
man = {r['path']: r for r in json.load(open(MAN))['files']}

rel = 'docs/coop/design-corrections/native/native-evidence-report.v2.json'
frozen = os.path.join(SRC, rel)
fh = hashlib.sha256(open(frozen, 'rb').read()).hexdigest()
print('frozen snapshot file unchanged:', fh == man[rel]['sha256'],
      'bytes ok:', os.path.getsize(frozen) == man[rel]['bytes'])
shutil.copy2(frozen, os.path.join(DST, rel))

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
