import json, re
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
def heads(p):
    out = set()
    for l in open(C + p, encoding='utf-8').read().splitlines():
        mm = re.match(r'^#{1,6}\s+(.*)$', l)
        if not mm: continue
        t = mm.group(1).strip()
        m2 = re.match(r'^(?:§\s*)?(S?\d+(?:\.\d+)*)[.)]?\s', t + ' ')
        if m2: out.add(m2.group(1))
    return out
rm = json.load(open(S + 'docs/coop/design-corrections/readiness-row-map.v1.json'))
bad = []; n = 0
cache = {}
for r in rm['rows']:
    for s in r['productSuccessors']:
        hs = cache.setdefault(s['path'], heads(s['path']))
        for sec in s['sections']:
            n += 1
            if sec not in hs: bad.append((r['id'], s['path'].split('/')[-1], sec))
print('section selectors', n, 'unresolved', bad)
for p, hs in cache.items(): print(p.split('/')[-1], sorted(hs, key=lambda x: [int(y) if y.isdigit() else y for y in re.split(r'[.S]', x) if y])[:80])
# gate coverage
gates = set('DR-G%02d' % i for i in range(1, 33))
used = set(g for r in rm['rows'] for g in r['releaseGates'])
print('gates not named by any row', sorted(gates - used))
for g in ['DR-G06', 'DR-G10', 'DR-G11', 'DR-G17']:
    print(g, [r['id'] for r in rm['rows'] if g in r['releaseGates']])
# compatible inherited selectors
ia = json.load(open(C + 'docs/coop/completion/architecture-application.v1.json'))
for r in rm['rows']:
    c = r.get('compatibleInheritedAccount')
    if c:
        idx = int(c['selector'].split('/')[-1])
        row = ia['rows'][idx]
        rid = row.get('id') or row.get('row') or row.get('rowId')
        if rid != r['id']: print('INHERITED SELECTOR MISMATCH', r['id'], c['selector'], rid)
print('inherited selectors checked', sum(1 for r in rm['rows'] if r.get('compatibleInheritedAccount')))
# additional inherited fragments
import hashlib
cd = open(C + 'docs/coop/COORDINATOR-DECISIONS.md', encoding='utf-8').read()
for r in rm['rows']:
    a = r.get('additionalInheritedAccount')
    if a and 'fragment' in a:
        ok_frag = hashlib.sha256(a['fragment'].encode()).hexdigest() == a['fragmentSha256']
        present = a['fragment'] in cd
        print('fragment', r['id'], a['selector'], 'sha ok', ok_frag, 'present verbatim in snapshot decisions', present)
    elif a:
        print('whole-file inherited', r['id'], a['path'], hashlib.sha256(open(C + a['path'], 'rb').read()).hexdigest() == a['sourceSha256'])
