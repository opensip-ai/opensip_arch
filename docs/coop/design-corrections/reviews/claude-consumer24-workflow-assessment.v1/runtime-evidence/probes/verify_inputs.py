"""Verify source37/source38 manifests + snapshots and the consumer24 kit manifest; record hashes. Read-only.

usage: python -I -B verify_inputs.py LABEL
"""
import hashlib, json, os, sys

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1'
MAN = {'source37': ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json',
                    '/tmp/opensip-design-corrections/candidate-subject.v37',
                    '245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'),
       'source38': ('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json',
                    '/tmp/opensip-design-corrections/candidate-subject.v38',
                    '2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5'),
       'kit37': ('/tmp/opensip-design-corrections/consumer-b.v24/subject/consumer-input-manifest.json',
                 '/tmp/opensip-design-corrections/consumer-b.v24/subject',
                 'e57ef3a785d5e25cfdfd02955cb4249f5f2443da1790832dce50d9d64bb4cc3c')}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def rows(o):
    if isinstance(o, list) and o and isinstance(o[0], dict) and 'path' in o[0] and ('sha256' in o[0] or 'sha' in o[0]):
        return o
    if isinstance(o, dict):
        for v in o.values():
            x = rows(v)
            if x:
                return x
    return None


res = {}
for label, (man, root, want) in MAN.items():
    got = sha(man)
    doc = json.load(open(man))
    r = rows(doc)
    listed = {x['path']: x.get('sha256') or x.get('sha') for x in r}
    bad = [p for p, s in listed.items() if not os.path.isfile(os.path.join(root, p)) or sha(os.path.join(root, p)) != s]
    extra = []
    for d, ds, fs in os.walk(root):
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), root)
            if rel not in listed and os.path.join(d, f) != man:
                extra.append(rel)
    res[label] = {'manifest': man, 'manifestSha256': got, 'expected': want, 'manifestOk': got == want, 'entries': len(listed),
                  'mismatchOrMissing': bad[:30], 'mismatchCount': len(bad), 'unlisted': extra[:30], 'unlistedCount': len(extra),
                  'parent': doc.get('parentSubjectSha256')}
s37 = {x['path']: x.get('sha256') for x in rows(json.load(open(MAN['source37'][0])))}
s38 = {x['path']: x.get('sha256') for x in rows(json.load(open(MAN['source38'][0])))}
res['source37to38'] = {'changed': sorted(p for p in s38 if p in s37 and s37[p] != s38[p]),
                       'added': sorted(p for p in s38 if p not in s37), 'removed': sorted(p for p in s37 if p not in s38)}
res['source37to38']['counts'] = {k: len(v) for k, v in res['source37to38'].items() if isinstance(v, list)}
os.makedirs(RT + '/receipts', exist_ok=True)
json.dump(res, open(RT + '/receipts/verify-inputs.' + sys.argv[1] + '.json', 'w'), indent=1)
summary = {k: {kk: vv for kk, vv in v.items() if kk not in ('changed', 'added', 'removed')} for k, v in res.items()}
print(json.dumps(summary, indent=1))
print(json.dumps({k: [p for p in v if '/reviews/' not in p] for k, v in res['source37to38'].items() if k != 'counts'}, indent=1))
