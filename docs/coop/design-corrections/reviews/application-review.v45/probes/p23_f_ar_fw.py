import json, re
R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
v36 = json.load(open(R + 'claude-independent-design.v36/review.json'))
fd = v36.get('fDispositions')
print('v36 fDispositions type', type(fd).__name__)
items = fd.items() if isinstance(fd, dict) else [(x['id'], x) for x in fd]
for k, v in items:
    cur = [kk for kk in v if 'ispositionOn' in kk or kk.endswith('Disposition')]
    print(k, '|', v.get('severity'), '|', v.get('area'), '|', {kk: v[kk] for kk in cur}, '| limits:', (v.get('limits') or '')[:160])
for p in ['docs/v2/contracts/product-v1/security-and-lifecycle.md', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md', 'docs/v2/contracts/product-v1/native-evidence.md', 'docs/v2/contracts/product-v1/identity-and-evidence.md', 'docs/v2/contracts/product-v1/admission-and-qualification.md', 'docs/v2/contracts/product-v1/README.md']:
    txt = open(C + p, encoding='utf-8').read()
    tags = sorted(set(re.findall(r'AR-\d\d', txt)))
    heads = [l for l in txt.splitlines() if re.match(r'^#{1,3} ', l)]
    print(p.split('/')[-1], 'AR tags mentioned', tags)
    if 'native' in p: [print('   ', h) for h in heads[:40]]
sm = open(C + 'docs/coop/design-corrections/current-source-map.proposed.md', encoding='utf-8').read()
rows = [l for l in sm.splitlines() if re.match(r'^\|\s*FW-\d\d', l)]
print('source map FW rows', len(rows))
for l in rows: print('  ', l[:330])
i = sm.find('Fallow constraint applicability')
print('fallow heading present', i >= 0)
