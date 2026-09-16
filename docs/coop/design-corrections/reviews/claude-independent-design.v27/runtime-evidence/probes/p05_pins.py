"""Probe 05 — every changed pin ledger must (a) change only digest/byte values,
(b) name paths that exist in frozen27 with exactly the frozen27 bytes."""
import difflib, hashlib, json, os, re

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
R26 = '/tmp/opensip-design-corrections/candidate-subject.v26'
R27 = '/tmp/opensip-design-corrections/candidate-subject.v27'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
m27 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v27.json')))['files']}

PINS = [
 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
 'docs/coop/design-corrections/foundation/source-pins.v1.json',
 'docs/coop/design-corrections/native/source-pins.v2.json',
 'docs/coop/design-corrections/security/source-pins.v1.json',
 'docs/coop/design-corrections/workflows/source-pins.v1.json',
 'docs/coop/design-corrections/workflows/workflows-report.v1.json',
]
res = {}
HEX = re.compile(r'[0-9a-f]{64}')
for rel in PINS:
    a = open(os.path.join(R26, rel), encoding='utf-8').read().splitlines()
    b = open(os.path.join(R27, rel), encoding='utf-8').read().splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    nonhex = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        # a pure digest swap: stripping 64-hex tokens makes the lines identical
        old = [HEX.sub('<H>', x) for x in a[i1:i2]]
        new = [HEX.sub('<H>', x) for x in b[j1:j2]]
        if old != new:
            nonhex.append({'tag': tag, 'v26': a[i1:i2][:3], 'v27': b[j1:j2][:3]})
    d = json.load(open(os.path.join(R27, rel), encoding='utf-8'))
    rows = d.get('files') if isinstance(d, dict) else None
    pinstat = None
    if isinstance(rows, list) and rows and isinstance(rows[0], dict) and 'path' in rows[0]:
        ok = sum(1 for r in rows
                 if r['path'] in m27 and m27[r['path']]['sha256'] == r.get('sha256'))
        pinstat = {'rows': len(rows), 'matchingFrozen27': ok, 'mismatched': len(rows) - ok,
                   'mismatchSample': [r['path'] for r in rows
                                      if not (r['path'] in m27 and m27[r['path']]['sha256'] == r.get('sha256'))][:5]}
    res[rel] = {'nonDigestOnlyChanges': nonhex, 'nonDigestOnlyCount': len(nonhex),
                'pinStatus': pinstat, 'topKeys': list(d) if isinstance(d, dict) else None}

json.dump(res, open(os.path.join(OUT, 'p05-pins.json'), 'w'), indent=1)
for k, v in res.items():
    print('%-64s nonDigestChanges=%d  pins=%s' % (
        k.split('/')[-2] + '/' + k.split('/')[-1], v['nonDigestOnlyCount'], v['pinStatus']))
    for n in v['nonDigestOnlyChanges'][:3]:
        print('     ', n)
