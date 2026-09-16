import os, hashlib, json

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
r = os.path.join(ROOT, 'docs/v2/contracts/product-v1')
m = json.load(open(MAN))
idx = {x['path']: x for x in m['files']}
out = []
for n in sorted(os.listdir(r)):
    p = os.path.join(r, n)
    b = open(p, 'rb').read()
    rel = 'docs/v2/contracts/product-v1/' + n
    txt = b.decode('utf-8')
    lines = txt.count('\n') + (0 if txt.endswith('\n') else 1)
    sha = hashlib.sha256(b).hexdigest()
    ok = idx[rel]['sha256'] == sha and idx[rel]['bytes'] == len(b)
    out.append(dict(name=n, sha256=sha, bytes=len(b), lines=lines, manifestMatch=ok))
    print('%-38s %s bytes=%-7d lines=%-5d manifestMatch=%s' % (n, sha, len(b), lines, ok))
json.dump(out, open('/tmp/opensip-design-corrections/claude-independent-design.v26/probes/contract-hashes.json', 'w'), indent=1)
