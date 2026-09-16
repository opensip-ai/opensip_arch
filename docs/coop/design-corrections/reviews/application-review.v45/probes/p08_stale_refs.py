import json, os, re, collections
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
m = json.load(open(S + 'application-subject.v45.json'))
cm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
snap = {e['path']: e['sha256'] for e in cm['files']}
staged = {e['path']: e for e in m['files']}
d = json.load(open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p03_out.json'))
old = {snap[p]: p for p in d['diff']}
pat = re.compile(('|'.join(old)).encode())
hits = collections.defaultdict(list)
for p in snap:
    if not p.endswith(('.json', '.md', '.py', '.txt', '.sql')): continue
    src = (S + 'files/' + p) if p in staged else (C + p)
    b = open(src, 'rb').read()
    for mm in set(pat.findall(b)):
        hits[old[mm.decode()]].append(p)
for p in staged:
    if p in snap or not p.endswith(('.json', '.md', '.py')): continue
    b = open(S + 'files/' + p, 'rb').read()
    for mm in set(pat.findall(b)):
        hits[old[mm.decode()]].append(p)
for k, v in sorted(hits.items()):
    cur = [x for x in v if '/reviews/' not in x and not x.startswith('docs/coop/design-corrections/reviews')]
    print(k, 'total referrers', len(v), 'non-review referrers', len(cur))
    for x in cur: print('    ', x)
