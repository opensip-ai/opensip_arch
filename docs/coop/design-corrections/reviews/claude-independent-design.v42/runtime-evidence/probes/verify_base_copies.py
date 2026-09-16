"""Re-verify the disposable copies this review imported owner modules from (work/base40, work/base41, work/source42,
work/source42-pkg) against their formal manifests after all probes and checkers ran: every member hash+length, no missing, no
unlisted files. Writes receipts/copy-verification-final.json."""
import hashlib, json, os

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v42'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
COPIES = {'work/base40': 'candidate-subject.v40.json', 'work/base41': 'candidate-subject.v41.json',
          'work/source42': 'candidate-subject.v42.json', 'work/source42-pkg': 'candidate-subject.v42.json'}


def sha_len(p):
    h, n = hashlib.sha256(), 0
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


out = {}
for rel, man in COPIES.items():
    root = os.path.join(RT, rel)
    raw = open(REV + man, 'rb').read()
    rows = {r['path']: r for r in json.loads(raw)['files']}
    bad, missing = [], []
    for p, r in rows.items():
        fp = os.path.join(root, p)
        if not os.path.isfile(fp):
            missing.append(p)
            continue
        h, n = sha_len(fp)
        if h != r['sha256'] or n != r['bytes']:
            bad.append(p)
    extra = [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs if os.path.relpath(os.path.join(d, f), root) not in rows]
    out[rel] = {'manifest': man, 'manifestSha256': hashlib.sha256(raw).hexdigest(), 'members': len(rows), 'mismatched': bad[:20], 'missing': missing[:20],
                'unlisted': sorted(extra)[:20], 'verified': not (bad or missing or extra)}
json.dump(out, open(RT + '/receipts/copy-verification-final.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
