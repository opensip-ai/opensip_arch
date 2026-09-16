import json, difflib, os
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
O = '/private/tmp/opensip-design-corrections/application-review.v45/probes/bdiffs/'
os.makedirs(O, exist_ok=True)
m = json.load(open(S + 'application-subject.v45.json'))
summary = []
for e in m['files']:
    if e['beforeSha256'] is None: continue
    p = e['path']
    if p.startswith('docs/operations/document-') :
        summary.append((p, 'LARGE-SKIPPED')); continue
    a = open(S + 'before/' + p, 'rb').read(); b = open(S + 'files/' + p, 'rb').read()
    try:
        a = a.decode('utf-8'); b = b.decode('utf-8')
    except Exception:
        summary.append((p, 'BINARY')); continue
    ud = list(difflib.unified_diff(a.splitlines(), b.splitlines(), 'before/' + p, 'staged/' + p, n=1, lineterm=''))
    plus = sum(1 for l in ud if l.startswith('+') and not l.startswith('+++'))
    minus = sum(1 for l in ud if l.startswith('-') and not l.startswith('---'))
    summary.append((p, '+%d -%d' % (plus, minus)))
    if len(ud) < 4000:
        open(O + p.replace('/', '__') + '.diff', 'w').write('\n'.join(ud) + '\n')
for s in summary: print(*s)
