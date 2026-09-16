"""Probe 03 — print the unified diff of the normative (non-pin) changed owners."""
import difflib, json, os, sys

REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
R26 = '/tmp/opensip-design-corrections/candidate-subject.v26'
R27 = '/tmp/opensip-design-corrections/candidate-subject.v27'
m26 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v26.json')))['files']}
m27 = {r['path']: r for r in json.load(open(os.path.join(REV, 'candidate-subject.v27.json')))['files']}
changed = sorted(p for p in set(m26) & set(m27) if m26[p]['sha256'] != m27[p]['sha256'])

want = sys.argv[1:] if len(sys.argv) > 1 else None
PIN = ('source-pins', 'evaluator3-source-pins', 'workflows-report.v1.json')
out = []
for rel in changed:
    base = rel.split('/')[-1]
    if want:
        if not any(w in rel for w in want):
            continue
    elif any(p in base for p in PIN):
        continue
    a = open(os.path.join(R26, rel), encoding='utf-8', errors='replace').read().splitlines()
    b = open(os.path.join(R27, rel), encoding='utf-8', errors='replace').read().splitlines()
    d = list(difflib.unified_diff(a, b, fromfile='v26/' + rel, tofile='v27/' + rel, n=2, lineterm=''))
    out.append('\n'.join(d))
print(('\n' + '=' * 100 + '\n').join(out))
