"""Print exact contexts for every unrouted gate hit reported by p05 (inherited accounts, cited sections, gate reverse mentions)."""
import json, re, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/application-review.v46/probes')
S = '/private/tmp/opensip-design-corrections/application-stage.v46/files/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
rm = json.load(open(S + 'docs/coop/design-corrections/readiness-row-map.v1.json'))
qg = json.load(open(S + 'docs/coop/design-corrections/qualification-gates.applied.v1.json'))
aa = json.load(open(SNAP + 'docs/coop/completion/architecture-application.v1.json'))
p05 = json.load(open('/private/tmp/opensip-design-corrections/application-review.v46/probes/out/p05_row_gates.json'))

def ptr(doc, p):
    for part in p.strip('/').split('/'):
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc

def ctx(text, g, w=170):
    n = g[4:]
    out = []
    for m in re.finditer(r'G' + n + r'\b|G\d\d(?:\s*(?:\.\.|–|-)\s*(?:DR-)?G?)\d\d', text):
        s = m.group(0)
        if 'G' + n not in s and not re.search(r'\.\.|–|-', s):
            continue
        out.append('…' + text[max(0, m.start() - w):m.end() + 60].replace('\n', ' ') + '…')
    return out[:3]

rows = {r['id']: r for r in rm['rows']}
for rep in p05['rows']:
    rid = rep['row']; row = rows[rid]
    if rep['missingVsInherited']:
        c = row.get('compatibleInheritedAccount')
        t = json.dumps(ptr(aa, c['selector']), ensure_ascii=False) if c else row['additionalInheritedAccount'].get('fragment', '')
        for g in rep['missingVsInherited']:
            print('INH', rid, g, ctx(t, g))
    if rep['missingVsSectionExact']:
        for key, (ge, gw) in rep['sectionDetail'].items():
            fname, rest = key.split('#'); sid, ln = rest.split('@')
            path = next(ps['path'] for ps in row['productSuccessors'] if ps['path'].endswith(fname))
            lines = open(SNAP + path, encoding='utf-8').read().splitlines()
            # exact section text
            i = int(ln) - 1; j = next((k for k in range(i + 1, len(lines)) if re.match(r'^#{1,6}\s', lines[k])), len(lines))
            text = '\n'.join(lines[i:j])
            for g in ge:
                if g in rep['missingVsSectionExact']:
                    print('SEC', rid, g, fname + ' §' + sid, ctx(text, g, 130)[:2])
for it in qg['items']:
    if it['id'] in ('DR-G30', 'DR-G26'):
        t = json.dumps(it, ensure_ascii=False)
        for m in re.finditer(r'DR-1\d\d', t):
            print('REV', it['id'], '…' + t[max(0, m.start() - 200):m.end() + 80] + '…')
