import json, os, re, posixpath, collections, unicodedata
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
m = json.load(open(S + 'application-subject.v45.json'))
staged = {e['path'] for e in m['files']}
ACT = 'docs/coop/design-corrections/application-activation.v1.json'
def post_path(p):
    if p in staged: return S + 'files/' + p
    if os.path.exists(R + p): return R + p
    return None
def slug(h):
    h = h.strip().lower()
    h = re.sub(r'<[^>]+>', '', h)
    h = re.sub(r'[`*_~]', '', h) if False else h.replace('`', '')
    out = []
    for ch in h:
        cat = unicodedata.category(ch)
        if ch in ' -': out.append('-' if ch == ' ' else ch)
        elif ch == '_' or cat[0] in 'LN': out.append(ch)
    return ''.join(out)
_anchor_cache = {}
def anchors(fp):
    if fp in _anchor_cache: return _anchor_cache[fp]
    txt = open(fp, encoding='utf-8', errors='replace').read()
    seen = collections.Counter(); out = set()
    infence = False
    for line in txt.splitlines():
        if line.lstrip().startswith('```'): infence = not infence; continue
        if infence: continue
        mm = re.match(r'^(#{1,6})\s+(.*?)\s*#*\s*$', line)
        if mm:
            t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', mm.group(2))
            t = t.replace('*', '').replace('_', '_')
            s = slug(t)
            n = seen[s]; seen[s] += 1
            out.add(s if n == 0 else '%s-%d' % (s, n))
    for mm in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', txt): out.add(mm.group(1))
    for mm in re.finditer(r'\bid="([^"]+)"', txt): out.add(mm.group(1))
    _anchor_cache[fp] = out
    return out
link_re = re.compile(r'(?<!\!)\[(?:[^\]\[]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
tot = 0; bad = []; act = []
mds = sorted(p for p in staged if p.endswith('.md') and not p.startswith('docs/coop/COORDINATOR-DECISIONS'))
# COORDINATOR-DECISIONS: only check the new D-372 section
for p in mds + ['docs/coop/COORDINATOR-DECISIONS.md']:
    txt = open(S + 'files/' + p, encoding='utf-8').read()
    if p.endswith('COORDINATOR-DECISIONS.md'):
        txt = txt[txt.index('## D-372 — complete intended-product design'):]
    infence = False; lines = []
    for line in txt.splitlines():
        if line.lstrip().startswith('```'): infence = not infence; continue
        if not infence: lines.append(line)
    for mm in link_re.finditer('\n'.join(lines)):
        t = mm.group(1)
        if re.match(r'^[a-z]+:', t): continue
        tot += 1
        path, _, frag = t.partition('#')
        if path == '': target = p
        else: target = posixpath.normpath(posixpath.join(posixpath.dirname(p), path))
        if target == ACT:
            act.append(p); continue
        fp = post_path(target)
        if fp is None:
            bad.append((p, t, 'MISSING')); continue
        if os.path.isdir(fp): continue
        if frag and target.endswith('.md'):
            if frag not in anchors(fp): bad.append((p, t, 'ANCHOR'))
print('links checked', tot, 'activation-target links', len(act), sorted(collections.Counter(act).items()))
print('failures', len(bad))
for b in bad: print('  ', b)
