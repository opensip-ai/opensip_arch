"""Local link and anchor check of every staged Markdown file against the post-application tree (live repo overlaid with staged files)."""
import json, os, re, urllib.parse
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
S = PK + 'files/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
m = json.load(open(PK + 'application-subject.v46.json'))
staged = {e['path'] for e in m['files']}
ACT = 'docs/coop/design-corrections/application-activation.v1.json'

def body(rel):
    if rel in staged: return open(S + rel, encoding='utf-8').read()
    return open(R + rel, encoding='utf-8').read()
def exists(rel):
    return rel in staged or os.path.exists(R + rel)
def isdir(rel):
    return os.path.isdir(R + rel) or any(p.startswith(rel.rstrip('/') + '/') for p in staged)

def slugs(text):
    res = set(); seen = {}
    infence = False
    for line in text.splitlines():
        if line.startswith('```'): infence = not infence; continue
        if infence: continue
        mm = re.match(r'^#{1,6}\s+(.*?)\s*#*\s*$', line)
        if mm:
            t = mm.group(1)
            t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
            t = re.sub(r'<[^>]+>', '', t)
            s = t.strip().lower()
            s = re.sub(r'[^\w\- ]', '', s, flags=re.UNICODE).replace(' ', '-')
            n = seen.get(s, 0); seen[s] = n + 1
            res.add(s if n == 0 else f'{s}-{n}')
        for a in re.findall(r'<a\s+(?:name|id)="([^"]+)"', line): res.add(a)
        for a in re.findall(r'\{#([\w\-]+)\}', line): res.add(a)
    return res

LINK = re.compile(r'(?<!!)\[(?:[^\[\]]|\[[^\]]*\])*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
results = {'files': 0, 'links': 0, 'ok': 0, 'activationTargets': [], 'failures': [], 'coordinatorHistoricalFailures': 0}
slugcache = {}
# D-372 body range in COORDINATOR
coord = open(S + 'docs/coop/COORDINATOR-DECISIONS.md', encoding='utf-8').read().splitlines()
d372 = [i for i, l in enumerate(coord) if re.match(r'^## D-372\b', l)]
d372_start = d372[0] if d372 else None
d372_end = next((i for i in range(d372_start + 1, len(coord)) if re.match(r'^## D-\d+', coord[i])), len(coord)) if d372_start is not None else None
results['d372Lines'] = [d372_start + 1 if d372_start is not None else None, d372_end]
for rel in sorted(p for p in staged if p.endswith('.md')):
    text = open(S + rel, encoding='utf-8').read()
    results['files'] += 1
    lines = text.splitlines()
    infence = False
    for ln, line in enumerate(lines):
        if line.startswith('```'): infence = not infence; continue
        if infence: continue
        for mm in LINK.finditer(line):
            tgt = mm.group(1)
            if re.match(r'^[a-z]+:', tgt) or tgt.startswith('//'): continue
            results['links'] += 1
            path, _, frag = tgt.partition('#')
            path = urllib.parse.unquote(path)
            if path == '':
                trel = rel
            else:
                trel = os.path.normpath(os.path.join(os.path.dirname(rel), path)).replace(os.sep, '/')
            hist = rel == 'docs/coop/COORDINATOR-DECISIONS.md' and not (d372_start is not None and d372_start <= ln < d372_end)
            if trel == ACT:
                results['activationTargets'].append((rel, ln + 1)); continue
            ok = exists(trel) or isdir(trel)
            why = None if ok else 'missing path'
            if ok and frag and trel.endswith('.md') and not isdir(trel):
                if trel not in slugcache: slugcache[trel] = slugs(body(trel))
                if urllib.parse.unquote(frag).lower() not in slugcache[trel] and frag not in slugcache[trel]:
                    ok = False; why = 'missing anchor'
            if ok: results['ok'] += 1
            elif hist: results['coordinatorHistoricalFailures'] += 1
            else: results['failures'].append((rel, ln + 1, tgt, why))
print(json.dumps(results, indent=1))
