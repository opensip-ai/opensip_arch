import json, difflib, os
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
O = '/private/tmp/opensip-design-corrections/application-review.v45/probes/diffs/'
os.makedirs(O, exist_ok=True)
d = json.load(open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p03_out.json'))
def flat(o, p=''):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items(): out.update(flat(v, p + '/' + str(k)))
    elif isinstance(o, list):
        for i, v in enumerate(o): out.update(flat(v, p + '/' + str(i)))
    else:
        out[p] = o
    return out
for p in d['diff']:
    a = open(C + p, encoding='utf-8').read(); b = open(S + p, encoding='utf-8').read()
    name = p.replace('/', '__')
    if p.endswith('.json'):
        fa = flat(json.loads(a)); fb = flat(json.loads(b))
        keys = sorted(set(fa) | set(fb))
        ch = [(k, fa.get(k, '<absent>'), fb.get(k, '<absent>')) for k in keys if fa.get(k, '<absent>') != fb.get(k, '<absent>')]
        with open(O + name + '.txt', 'w') as f:
            for k, x, y in ch: f.write('%s\n  - %s\n  + %s\n' % (k, x, y))
        print(p, 'json leaf changes', len(ch))
    else:
        ud = list(difflib.unified_diff(a.splitlines(), b.splitlines(), 'snapshot/' + p, 'staged/' + p, n=1, lineterm=''))
        with open(O + name + '.diff', 'w') as f: f.write('\n'.join(ud) + '\n')
        print(p, 'diff lines', len(ud), '+', sum(1 for l in ud if l.startswith('+') and not l.startswith('+++')), '-', sum(1 for l in ud if l.startswith('-') and not l.startswith('---')))
