import json, re
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
rm = json.load(open(S + 'docs/coop/design-corrections/readiness-row-map.v1.json'))
def gates_in(text):
    out = set()
    for a, b in re.findall(r'\bG(\d\d)\s*[–-]\s*(?:DR-)?G?(\d\d)\b', text):
        for i in range(int(a), int(b) + 1): out.add('DR-G%02d' % i)
    for a in re.findall(r'\bG(\d\d)\b', text):
        out.add('DR-G%02d' % int(a))
    return {g for g in out if 1 <= int(g[-2:]) <= 32}
_cache = {}
def section_text(path, sel):
    lines = _cache.setdefault(path, open(C + path, encoding='utf-8').read().splitlines())
    start = None; level = None
    for i, l in enumerate(lines):
        mm = re.match(r'^(#{1,6})\s+(?:§\s*)?(S?\d+(?:\.\d+)*)[.)]?\s', l + ' ')
        if start is None and mm and mm.group(2) == sel:
            start = i; level = len(mm.group(1)); continue
        if start is not None:
            m2 = re.match(r'^(#{1,6})\s', l)
            if m2 and len(m2.group(1)) <= level:
                return '\n'.join(lines[start:i])
    return '\n'.join(lines[start:]) if start is not None else ''
reg = open(C + 'docs/v2/architecture/08-decision-and-readiness-register.md', encoding='utf-8').read().splitlines()
for r in rm['rows']:
    cited = set(); per = {}
    for s in r['productSuccessors']:
        for sec in s['sections']:
            g = gates_in(section_text(s['path'], sec))
            if g: per[s['path'].split('/')[-1] + '#' + sec] = sorted(g)
            cited |= g
    hist = set()
    for l in reg:
        if l.startswith('| ' + r['id'] + ' |'):
            hist |= gates_in(l)
    rg = set(r['releaseGates'])
    src = gates_in(r.get('sourceRequiredEvidence', '') + ' ' + r.get('sourceObligation', ''))
    print('==', r['id'], 'releaseGates', sorted(rg))
    print('   named in cited sections but not routed:', sorted(cited - rg), {k: v for k, v in per.items() if set(v) - rg})
    print('   named in historical register row(s) but not routed:', sorted(hist - rg))
    print('   named in source obligation/evidence but not routed:', sorted(src - rg))
