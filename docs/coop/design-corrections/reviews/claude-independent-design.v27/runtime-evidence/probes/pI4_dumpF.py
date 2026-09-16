"""PROBE I4 (v27) — dump the full F-01..F-14 finding records from the embedded JSON block
in claude-author-package-review.v1/review.md, so each remedy can be assessed on snapshot27."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-author-package-review.v1'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
md = open(os.path.join(BASE, 'review.md'), encoding='utf-8').read()

# find fenced json blocks
blocks = re.findall(r'```json\s*\n(.*?)\n```', md, re.S)
print('fenced json blocks:', len(blocks), [len(b) for b in blocks])
findings = None
whole = None
for b in blocks:
    try:
        o = json.loads(b)
    except Exception as ex:
        print('  unparsed block (%d bytes): %s' % (len(b), str(ex)[:90]))
        continue
    def scan(o, path=''):
        global findings, whole
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, list) and v and isinstance(v[0], dict) and str(v[0].get('id', '')).startswith('F-'):
                    findings, whole = v, o
                    print('  findings at %s/%s' % (path, k))
                scan(v, path + '/' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                scan(v, path + '/%d' % i)

    if isinstance(o, dict):
        print('  parsed block keys:', list(o)[:25])
        scan(o)
print()
if findings is None:
    # fall back: brace-match from each '"id": "F-01"' occurrence
    print('no fenced block parsed; scanning raw')
    raise SystemExit(1)

print('findings rows:', len(findings))
print('finding keys :', sorted(findings[0]))
for f in findings:
    print('\n' + '=' * 100)
    print('%s  [%s]' % (f.get('id'), f.get('severity', f.get('class', '?'))))
    for k, v in f.items():
        if k == 'id':
            continue
        print('  %-22s %s' % (k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))

json.dump({'source': 'review.md embedded json (review.json absent)',
           'reviewMdSha256': hashlib.sha256(open(os.path.join(BASE, 'review.md'), 'rb').read()).hexdigest(),
           'findings': findings,
           'otherTopKeys': [k for k in whole if not (isinstance(whole[k], list) and whole[k] and isinstance(whole[k][0], dict) and str(whole[k][0].get('id', '')).startswith('F-'))]},
          open(os.path.join(OUT, 'pI4-findingsF-full.json'), 'w'), indent=1)
print('\nother top-level keys in that block:', [k for k in whole])
