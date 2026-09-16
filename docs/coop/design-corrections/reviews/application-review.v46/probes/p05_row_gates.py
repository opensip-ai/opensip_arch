"""Independent per-row release-gate cross-check for all 28 condition-2 rows (v46 row map)."""
import json, re, os, hashlib
S = '/private/tmp/opensip-design-corrections/application-stage.v46/files/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
OUT = '/private/tmp/opensip-design-corrections/application-review.v46/probes/out/'
rm = json.load(open(S + 'docs/coop/design-corrections/readiness-row-map.v1.json'))
qg = json.load(open(S + 'docs/coop/design-corrections/qualification-gates.applied.v1.json'))

TOK = re.compile(r'(?:DR-)?G(\d\d)(?:\s*(?:\.\.|–|—|-)\s*(?:DR-)?G?(\d\d))?\b')
def gates(text):
    out = set()
    for m in TOK.finditer(text):
        a = int(m.group(1)); b = m.group(2)
        # only treat as range when explicit .. or en dash and the second is a number
        if b is not None:
            b = int(b)
            if 1 <= a < b <= 32 and b - a < 10:
                out.update(range(a, b + 1)); continue
        if 1 <= a <= 32: out.add(a)
    return {'DR-G%02d' % x for x in out}

def sections(path):
    lines = open(SNAP + path, encoding='utf-8').read().splitlines()
    heads = []
    for i, l in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(?:§\s*)?([A-Z]?\d+(?:\.\d+)*)\.?\s', l)
        if m: heads.append((i, len(m.group(1)), m.group(2)))
    res = {}
    allheads = [i for i, l in enumerate(lines) if re.match(r'^#{1,6}\s', l)]
    for idx, (i, lvl, sid) in enumerate(heads):
        nxt_any = next((j for j in allheads if j > i), len(lines))
        nxt_same = next((j for (j, l2, _) in heads[idx + 1:] if l2 <= lvl), len(lines))
        res[sid] = ('\n'.join(lines[i:nxt_any]), '\n'.join(lines[i:nxt_same]), i + 1)
    return res

reg_lines = open(SNAP + 'docs/v2/architecture/08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
aa = json.load(open(SNAP + 'docs/coop/completion/architecture-application.v1.json'))
def ptr(doc, p):
    for part in p.strip('/').split('/'):
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc

secache = {}; unmatched = []
report = []
for idx, row in enumerate(rm['rows']):
    rid = row['id']; routed = set(row['releaseGates'])
    reg = [ (n + 1, l) for n, l in enumerate(reg_lines) if l.startswith('| ' + rid + ' ') or l.startswith('| ' + rid + '|') or l.startswith('| **' + rid)]
    regG = set().union(*[gates(l) for _, l in reg]) if reg else set()
    textG = gates(row['sourceObligation'] + ' ' + row['sourceRequiredEvidence'] + ' ' + row['disposition'])
    inhG = set(); inhSrc = None
    if row.get('additionalInheritedAccount'):
        inhG |= gates(row['additionalInheritedAccount'].get('fragment', ''))
        inhSrc = row['additionalInheritedAccount'].get('selector')
    if row.get('compatibleInheritedAccount'):
        c = row['compatibleInheritedAccount']
        try:
            inhG |= gates(json.dumps(ptr(aa, c['selector']), ensure_ascii=False)); inhSrc = c['selector']
        except Exception as e:
            inhSrc = 'ERR ' + str(e)
    secExact = set(); secWide = set(); secDetail = {}
    for ps in row['productSuccessors']:
        p = ps['path']
        h = hashlib.sha256(open(SNAP + p, 'rb').read()).hexdigest()
        if h != ps['sha256']: unmatched.append((rid, p, 'HASH MISMATCH'))
        if p not in secache: secache[p] = sections(p)
        for sid in ps['sections']:
            key = sid.lstrip('§')
            if key not in secache[p]:
                unmatched.append((rid, p, sid)); continue
            ex, wide, ln = secache[p][key]
            ge, gw = gates(ex), gates(wide)
            secExact |= ge; secWide |= gw
            if ge or gw: secDetail[p.split('/')[-1] + '#' + sid + '@' + str(ln)] = [sorted(ge), sorted(gw - ge)]
    report.append({'row': rid, 'index': idx, 'routed': sorted(routed),
                   'registerLines': [n for n, _ in reg], 'registerGates': sorted(regG), 'missingVsRegister': sorted(regG - routed),
                   'rowTextGates': sorted(textG), 'missingVsRowText': sorted(textG - routed),
                   'inheritedSelector': inhSrc, 'inheritedGates': sorted(inhG), 'missingVsInherited': sorted(inhG - routed),
                   'sectionExactGates': sorted(secExact), 'missingVsSectionExact': sorted(secExact - routed),
                   'missingVsSectionWide': sorted(secWide - routed), 'sectionDetail': secDetail})
# reverse: gate items mentioning rows
rev = {}
rowgates = {r['id']: set(r['releaseGates']) for r in rm['rows']}
for it in qg['items']:
    t = json.dumps(it, ensure_ascii=False)
    ids = set(re.findall(r'DR-1\d\d', t))
    rev[it['id']] = {'rowsMentioned': sorted(ids), 'rowsMentionedNotRouting': sorted(i for i in ids if i in rowgates and it['id'] not in rowgates[i])}
allRouted = set().union(*rowgates.values())
json.dump({'rows': report, 'unmatchedSections': unmatched, 'gateReverse': rev, 'gatesNeverRouted': sorted({'DR-G%02d' % i for i in range(1, 33)} - allRouted), 'totalMemberships': sum(len(v) for v in rowgates.values())}, open(OUT + 'p05_row_gates.json', 'w'), indent=1, ensure_ascii=False)
for r in report:
    print(r['row'], 'routed', ','.join(g[4:] for g in r['routed']), '| -reg', ','.join(g[4:] for g in r['missingVsRegister']), '| -text', ','.join(g[4:] for g in r['missingVsRowText']), '| -inh', ','.join(g[4:] for g in r['missingVsInherited']), '| -secExact', ','.join(g[4:] for g in r['missingVsSectionExact']), '| -secWide', ','.join(g[4:] for g in r['missingVsSectionWide']))
print('unmatched', unmatched)
print('never routed', sorted({'DR-G%02d' % i for i in range(1, 33)} - allRouted), 'memberships', sum(len(v) for v in rowgates.values()))
print('reverse issues', {k: v['rowsMentionedNotRouting'] for k, v in rev.items() if v['rowsMentionedNotRouting']})
